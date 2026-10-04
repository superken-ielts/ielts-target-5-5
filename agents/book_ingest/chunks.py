"""Bước 6b — cắt PDF lớn thành các đoạn nhỏ cho app (docs/agent-hoc-tap/02 mục 3.7, quyết định D5).

Vì sao: khi mở tài liệu, PDF.js luôn tải trang cuối để kiểm tra số trang. Với file có cây trang
phẳng mà mỗi page dict nằm cạnh ảnh scan của trang đó (như IELTS_Target_5.0.pdf), bước này buộc
PDF.js đọc gần hết 100 MB. Một đoạn 12 trang chỉ vài MB nên mở tức thì, trên điện thoại cũng vậy.

Ranh giới đoạn bám cấu trúc sách: phần đầu sách, từng unit, từng review, Key exam vocabulary,
Answer key, Tapescript (chia nhỏ). Phần bị bỏ qua (skip) không cắt. Kết quả ổn định: cùng file
gốc + cùng ranh giới thì không ghi lại, và PyMuPDF ghi không kèm /ID ngẫu nhiên.
"""
from __future__ import annotations

import json
from pathlib import Path

import pymupdf

from . import pdfutil
from .profile import Profile

AUTO_BYTES = 20_000_000


def wanted(profile: Profile, fid: str, size: int) -> bool:
    v = profile.files.get(fid, {}).get("web_chunks", "auto")
    return bool(v) if v != "auto" else size > AUTO_BYTES


def plan_ranges(profile: Profile, structure: dict, n_pages: int, max_pages: int = 16) -> list[list[int]]:
    """Ranh giới các đoạn. Đoạn của Answer key / Tapescript gom theo section (từ chỉ mục OCR) để phần
    của một unit không bị vắt qua hai đoạn; hai đoạn kề nhau được phép chung một trang ở ranh giới."""
    ranges: list[list[int]] = []
    units = list(structure["units"].values())
    if units and units[0]["pages"][0] > 1:
        ranges.append([1, units[0]["pages"][0] - 1])
    ranges += [list(u["pages"]) for u in units]
    ranges += [list(r["pages"]) for r in structure["reviews"].values()]
    if structure.get("keyVocab"):
        ranges.append(list(structure["keyVocab"]))
    for key in ("answerKey", "tapescript"):
        idx = structure.get(key)
        if not idx:
            continue
        a, b = idx["pages"]
        found = idx.get("units") or {}
        groups = []
        for sec in profile.sections:
            keys = [str(u.no) for u in sec.units] + ([f"R{sec.review_no}"] if sec.review_no is not None else [])
            spans = [found[k] for k in keys if k in found]
            if spans:
                groups.append([min(x[0] for x in spans), max(x[1] for x in spans)])
        tests = [v for k, v in found.items() if k.startswith("T")]
        if tests:
            groups.append([min(x[0] for x in tests), max(x[1] for x in tests)])
        if not groups:                      # không có chỉ mục OCR: chia đều
            groups = [[x, min(b, x + max_pages - 1)] for x in range(a, b + 1, max_pages)]
        covered = sorted(groups)
        # phần chưa thuộc nhóm nào (đầu mục, chỗ trống giữa nhóm) gộp vào nhóm kề
        covered[0][0], covered[-1][1] = min(covered[0][0], a), max(covered[-1][1], b)
        for i in range(1, len(covered)):
            if covered[i][0] > covered[i - 1][1] + 1:
                covered[i][0] = covered[i - 1][1] + 1
        ranges += covered

    skips = [profile.pdf_range([int(s["from"]), int(s["to"])]) for s in profile.skip]
    out: list[list[int]] = []
    for a, b in sorted({(max(1, a), min(n_pages, b)) for a, b in ranges}):
        if a > b or any(s[0] <= a and b <= s[1] for s in skips):
            continue
        if any(o[0] <= a and b <= o[1] for o in out):      # nằm trọn trong đoạn đã có
            continue
        out = [o for o in out if not (a <= o[0] and o[1] <= b)]
        out.append([a, b])
    return sorted(out)


def write(profile: Profile, fid: str, src_sha: str, ranges: list[list[int]], work: Path) -> list[dict]:
    """Ghi các đoạn vào <sách>/web/, dùng lại đoạn cũ nếu file gốc và ranh giới không đổi."""
    manifest_path = work / "chunks.json"
    manifest = json.loads(manifest_path.read_text(encoding="utf-8")) if manifest_path.exists() else {}
    old = manifest.get(fid)
    out_dir = profile.root / "web"
    if old and old["srcSha"] == src_sha and [[c["from"], c["to"]] for c in old["chunks"]] == ranges and all(
            (profile.root / c["path"]).exists() and (profile.root / c["path"]).stat().st_size == c["bytes"]
            for c in old["chunks"]):
        return old["chunks"]

    out_dir.mkdir(parents=True, exist_ok=True)
    src = pdfutil.open_pdf(str(profile.path(fid)))
    chunks = []
    for a, b in ranges:
        path = out_dir / f"{fid}-p{a:04d}-{b:04d}.pdf"
        doc = pymupdf.open()
        doc.insert_pdf(src, from_page=a - 1, to_page=b - 1)
        doc.save(str(path), garbage=3, deflate=True, no_new_id=True)
        doc.close()
        chunks.append({"path": path.relative_to(profile.root).as_posix(), "from": a, "to": b,
                       "bytes": path.stat().st_size, "sha256": pdfutil.sha256_file(path)})
    keep = {c["path"] for c in chunks}
    for stale in out_dir.glob(f"{fid}-p*.pdf"):
        if stale.relative_to(profile.root).as_posix() not in keep:
            stale.unlink()
    manifest[fid] = {"srcSha": src_sha, "chunks": chunks}
    manifest_path.write_text(json.dumps(manifest, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    return chunks
