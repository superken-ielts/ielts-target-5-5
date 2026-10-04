"""Kiểm tra gói sách trước khi app dùng (V3, V4, V5, V7, V8 — docs/agent-hoc-tap/02 mục 4.4)."""
from __future__ import annotations

import json
from pathlib import Path

from . import pdfutil
from .schemas import AudioFile, Book, PdfFile, Plan

EXPECTED_SESSIONS = {"target-gt-v1": lambda units, reviews, tests: units * 7 + reviews * 2 + tests * 3}


def validate(book_dir: Path, check_hashes: bool = False) -> list[str]:
    book_dir = Path(book_dir)
    problems: list[str] = []
    try:
        book = Book.model_validate_json((book_dir / "book.json").read_text(encoding="utf-8"))
        plan = Plan.model_validate_json((book_dir / "plan.json").read_text(encoding="utf-8"))
    except Exception as e:  # schema sai thì dừng luôn
        return [f"schema: {e}"]

    # V8 — file tồn tại, đúng cỡ (và đúng sha256 nếu được yêu cầu)
    for fid, f in book.files.items():
        for c in getattr(f, "chunks", []):
            cp = book_dir / c.path
            if not cp.exists():
                problems.append(f"V8 thiếu đoạn {c.path} ({fid})")
            elif cp.stat().st_size != c.bytes:
                problems.append(f"V8 sai cỡ đoạn {c.path}")
            elif check_hashes and pdfutil.sha256_file(cp) != c.sha256:
                problems.append(f"V8 sai sha256 đoạn {c.path}")
        p = book_dir / f.path
        if not p.exists():
            problems.append(f"V8 thiếu file {f.path} ({fid})")
            continue
        if p.stat().st_size != f.bytes:
            problems.append(f"V8 sai cỡ {f.path}: {p.stat().st_size} ≠ {f.bytes}")
        elif check_hashes and pdfutil.sha256_file(p) != f.sha256:
            problems.append(f"V8 sai sha256 {f.path}")

    acts = {}
    for sec in book.sections:
        for item in sec.items:
            for a in item.activities:
                acts[a.id] = a
                # V3 — khoảng trang nằm trong file
                for ref in [r for r in [a, a.answer, a.script, a.vocab, *a.alt] if r is not None]:
                    pages, pdf = getattr(ref, "pages", None), getattr(ref, "pdf", None)
                    if pages and pdf:
                        f = book.files.get(pdf)
                        if not isinstance(f, PdfFile):
                            problems.append(f"V3 {a.id} trỏ tới file PDF không tồn tại: {pdf}")
                        elif pages[1] > f.pages:
                            problems.append(f"V3 {a.id} trang {pages} vượt quá {f.pages} trang của {pdf}")
                        elif f.chunks and not any(c.from_ <= pages[0] and pages[1] <= c.to for c in f.chunks):
                            problems.append(f"V3 {a.id} trang {pages} của {pdf} không nằm trọn trong đoạn nào")
                # V4 — Listening phải có track
                if a.module == "listening":
                    if not a.tracks:
                        problems.append(f"V4 {a.id} không có track nào")
                    for t in a.tracks:
                        if not isinstance(book.files.get(t), AudioFile):
                            problems.append(f"V4 {a.id} trỏ tới track không có: {t}")

    # V3 — trang tapescript của từng track
    for fid, f in book.files.items():
        if isinstance(f, AudioFile) and f.script:
            src = book.files.get(f.script.pdf)
            if isinstance(src, PdfFile) and src.chunks and not any(
                    c.from_ <= f.script.pages[0] and f.script.pages[1] <= c.to for c in src.chunks):
                problems.append(f"V3 track {fid}: tapescript {f.script.pages} không nằm trọn trong đoạn nào")

    # V4 — mỗi track dùng đúng một lần
    used = [t for a in acts.values() for t in a.tracks]
    for fid, f in book.files.items():
        if isinstance(f, AudioFile):
            if used.count(fid) != 1:
                problems.append(f"V4 track {fid} được dùng {used.count(fid)} lần")
            # V5 — độ dài hợp lý
            if f.durationSec is not None and not (2 <= f.durationSec <= 20 * 60):
                problems.append(f"V5 track {fid} dài {f.durationSec}s, ngoài khoảng 2 giây–20 phút")

    # V7 — số phiên đúng mẫu
    kinds = [i.kind for s in book.sections for i in s.items]
    rule = EXPECTED_SESSIONS.get(book.template)
    if rule:
        want = rule(kinds.count("unit"), kinds.count("review"), kinds.count("test"))
        if len(plan.sessions) != want:
            problems.append(f"V7 plan có {len(plan.sessions)} phiên, mẫu {book.template} cần {want}")
    ids = [s.id for s in plan.sessions]
    if len(set(ids)) != len(ids):
        problems.append("V7 trùng ID phiên")
    for s in plan.sessions:
        for aid in s.activityIds:
            if aid not in acts:
                problems.append(f"V7 phiên {s.id} trỏ tới hoạt động không có: {aid}")
    return problems


def summary(book_dir: Path) -> dict:
    book = json.loads((Path(book_dir) / "book.json").read_text(encoding="utf-8"))
    plan = json.loads((Path(book_dir) / "plan.json").read_text(encoding="utf-8"))
    items = [i for s in book["sections"] for i in s["items"]]
    return {
        "units": sum(1 for i in items if i["kind"] == "unit"),
        "reviews": sum(1 for i in items if i["kind"] == "review"),
        "tests": sum(1 for i in items if i["kind"] == "test"),
        "tracks": sum(1 for f in book["files"].values() if f["kind"] == "audio"),
        "sessions": len(plan["sessions"]),
        "weeks": [plan["sessions"][0]["week"], plan["sessions"][-1]["week"]] if plan["sessions"] else [],
    }
