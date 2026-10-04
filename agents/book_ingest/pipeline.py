"""Chạy nối các bước: scan → structure → match → review → plan → pack → validate.

Mỗi bước ghi kết quả vào <thư mục sách>/work/, bước sau đọc lại. Gặp mục duyệt còn mở
thì dừng (mã thoát 2) để người duyệt quyết định, rồi chạy lại là đi tiếp từ chỗ dừng.
"""
from __future__ import annotations

import json
from dataclasses import dataclass, field
from pathlib import Path

from . import audio, chunks as ck, review as rv, scan as sc, structure as st, templates, validate as vd
from .ocr import OcrCache
from .profile import Profile, load
from .schemas import dump

OK, NEEDS_REVIEW, INVALID = 0, 2, 3


@dataclass
class Result:
    code: int
    messages: list[str] = field(default_factory=list)


def work_dir(book_dir: Path) -> Path:
    return Path(book_dir) / "work"


def _write(path: Path, data) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")


def _read(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def step_scan(profile: Profile, force: bool = False) -> dict:
    out = work_dir(profile.root) / "scan.json"
    if out.exists() and not force:
        data = _read(out)
        # file nguồn đổi cỡ thì quét lại
        if all((profile.root / v["path"]).exists() and (profile.root / v["path"]).stat().st_size == v["bytes"]
               for v in data["pdfs"].values()) and len(data["audio"]) == sum(
                   1 for fid, s in profile.files.items() if s.get("kind") == "audio"
                   for f in profile.path(fid).iterdir() if f.suffix.lower() in sc.AUDIO_EXT):
            return data
    data = sc.scan(profile)
    _write(out, data)
    return data


def run(book_dir: Path, force: bool = False, allow_ocr: bool = True, say=print) -> Result:
    book_dir = Path(book_dir)
    res = Result(OK)
    log = lambda m: (res.messages.append(m), say(m))  # noqa: E731
    profile = load(book_dir)
    work = work_dir(book_dir)
    review_path = work / "review.json"
    old = rv.load(review_path)

    data = step_scan(profile, force)
    log(f"[scan] {len(data['pdfs'])} PDF, {len(data['audio'])} audio, {len(data['duplicates'])} cặp trùng")

    ocr = OcrCache(work / "ocr-cache.json")
    if allow_ocr and not ocr.available:
        log("[ocr] chưa cài rapidocr-onnxruntime — chỉ dùng cache OCR có sẵn")
    structure = st.build(profile, data, rv.decisions(old), ocr, allow_ocr=allow_ocr)
    ocr.save()
    _write(work / "structure.json", structure)
    log(f"[structure] {len(structure['units'])} unit, {len(structure['reviews'])} review, độ lệch trang {structure['pageOffset']}")

    matched = audio.match(profile, data, structure)
    _write(work / "match.json", matched)
    log(f"[match] {len(matched['tracks'])} track ghép được cho {len(matched['byUnit'])} unit")

    review = rv.merge(old, structure["review"] + matched["review"])
    rv.save(review_path, review)
    pending = rv.open_items(review)
    if pending:
        log(f"[review] còn {len(pending)} mục cần duyệt: " + ", ".join(i.id for i in pending))
        log(f"         chạy `book review {book_dir}` rồi chạy lại `book ingest {book_dir}`")
        res.code = NEEDS_REVIEW
        return res

    # Quyết định có thể đổi cấu trúc (ví dụ trang đầu module) → dựng lại với quyết định mới nhất.
    structure = st.build(profile, data, rv.decisions(review), ocr, allow_ocr=allow_ocr)
    _write(work / "structure.json", structure)
    matched = audio.match(profile, data, structure)
    skipped = {i.subject for i in review.items if (i.decision or {}).get("skip") or (
        (i.decision or {}).get("accept") and (i.proposal or {}).get("skip"))}
    matched["tracks"] = [t for t in matched["tracks"] if t["path"] not in skipped]

    parts = {}
    for fid, info in data["pdfs"].items():
        if ck.wanted(profile, fid, info["bytes"]):
            ranges = ck.plan_ranges(profile, structure, info["pages"])
            parts[fid] = ck.write(profile, fid, info["sha256"], ranges, work)
            log(f"[chunks] {fid}: {len(parts[fid])} đoạn, {sum(c['bytes'] for c in parts[fid]) / 1e6:.0f} MB → web/")

    book = templates.build_book(profile, data, structure, matched, parts)
    plan = templates.build_plan(profile, book)
    _write(book_dir / "book.json", dump(book))
    _write(book_dir / "plan.json", dump(plan))
    (book_dir / "report.md").write_text(report(profile, data, structure, matched, review, plan), encoding="utf-8")
    log(f"[pack] book.json, plan.json, report.md → {book_dir}")

    problems = vd.validate(book_dir)
    if problems:
        for p in problems:
            log(f"[validate] {p}")
        res.code = INVALID
    else:
        s = vd.summary(book_dir)
        log(f"[validate] OK — {s['units']} unit, {s['reviews']} review, {s['tests']} test, "
            f"{s['tracks']} track, {s['sessions']} phiên, tuần {s['weeks'][0]}–{s['weeks'][1]}")
    return res


def report(profile: Profile, data: dict, structure: dict, matched: dict, review, plan) -> str:
    rows = [f"# Báo cáo nhập sách — {profile.title}", "",
            "Sinh tự động bởi `book ingest`. Đừng sửa tay; sửa book.yaml hoặc work/review.json rồi chạy lại.", "",
            "## File", "", "| File | Trang/độ dài | Cỡ | Lớp chữ |", "|---|---|---|---|"]
    for fid, f in data["pdfs"].items():
        rows.append(f"| {fid}: `{f['path']}` | {f['pages']} trang | {f['bytes'] / 1e6:.1f} MB | {f['textLayerRatio']:.0%} |")
    total = sum(a["durationSec"] or 0 for a in data["audio"])
    rows.append(f"| audio: {len(data['audio'])} file | {total / 60:.0f} phút | "
                f"{sum(a['bytes'] for a in data['audio']) / 1e6:.0f} MB | — |")
    rows += ["", f"Độ lệch trang Course Book: trang in N = trang PDF N + {structure['pageOffset']}.", "",
             "## Cấu trúc", "", "| Unit | Trang PDF | Module (trang PDF) | Track | Tin cậy |", "|---|---|---|---|---|"]
    for k, u in structure["units"].items():
        mods = " · ".join(f"{m} {r[0]}–{r[1]}" for m, r in u["modules"].items())
        rows.append(f"| {k} {u['title']} | {u['pages'][0]}–{u['pages'][1]} | {mods} | "
                    f"{len(matched['byUnit'].get(k, []))} | {u['confidence']:.1f} |")
    for key, label in (("answerKey", "Answer key"), ("tapescript", "Tapescript")):
        idx = structure.get(key)
        if idx:
            rows += ["", f"**{label}** trang {idx['pages'][0]}–{idx['pages'][1]}: OCR {idx['ocrPages']} trang, "
                         f"tìm thấy {len(idx['units'])} unit/review, {len(idx['index'])} mục"
                     + (f", {len(idx['tracks'])} track" if idx.get("tracks") else "") + "."]
    rows += ["", "## Mục duyệt", ""]
    if not review.items:
        rows.append("Không có mục nào.")
    for i in review.items:
        d = json.dumps(i.decision, ensure_ascii=False) if i.decision else "chưa quyết"
        rows.append(f"- `{i.id}` [{i.severity}] {i.message} — **{d}**")
    weeks = [plan.sessions[0].week, plan.sessions[-1].week] if plan.sessions else ["?", "?"]
    rows += ["", "## Kế hoạch", "",
             f"{len(plan.sessions)} phiên × {plan.minutesPerSession} phút, {plan.sessionsPerWeek} phiên/tuần, "
             f"tuần {weeks[0]}–{weeks[1]}."]
    if profile.missing:
        rows += ["", "Thiếu trong bộ dữ liệu: " + ", ".join(profile.missing) + "."]
    return "\n".join(rows) + "\n"
