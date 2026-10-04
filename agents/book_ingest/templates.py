"""Bước 5 — áp mẫu phiên, sinh book.json và plan.json (docs/agent-hoc-tap/02 mục 3.3–3.5).

Mẫu `target-gt-v1` (IELTS Target 5.0, phần General Training):
  unit   → 7 phiên: speaking-vocab · listening · reading · writing-learn · writing-review
           · consolidation (gồm Exam practice) · workbook
  review → 2 phiên;  test → 3 phiên.
Thiếu Work Book thì phiên 7 thành "Ôn unit + sổ lỗi"; thiếu sách Test thì phiên Test giữ chỗ
trong lịch và ghi chú dùng đề Cambridge GT.
"""
from __future__ import annotations

from typing import Optional

from . import __version__
from .profile import Profile
from .schemas import Activity, AudioFile, Book, BookInfo, Chunk, Item, PdfFile, Plan, Ref, Section, Session, Source

INFO_KEYS = {"role": "role", "module": "module", "author": "author", "publisher": "publisher", "cefr": "cefr",
             "band_from": "bandFrom", "band_to": "bandTo", "summary": "summary", "start_when": "startWhen"}

MODULE_TITLE = {
    "speaking-vocab": "Speaking & Vocabulary", "listening": "Listening", "reading": "Reading",
    "writing": "Writing", "consolidation": "Consolidation", "exam-practice": "Exam practice",
}
MODULE_SKILL = {
    "speaking-vocab": "speaking", "listening": "listening", "reading": "reading",
    "writing": "writing", "consolidation": "vocab", "exam-practice": "other",
}
CORE_STEPS = ["speaking-vocab", "writing-learn", "writing-review", "test-lr", "test-ws"]
TEMPLATES = {"target-gt-v1"}


def _ref(pdf: str, rng: Optional[list[int]], label: Optional[str] = None) -> Optional[Ref]:
    return Ref(pdf=pdf, pages=list(rng), label=label) if rng else None


def _lookup(idx: Optional[dict], unit_key: str, module: str) -> Optional[list[int]]:
    if not idx:
        return None
    return idx["index"].get(f"{unit_key}:{module}") or idx["units"].get(unit_key) or idx["pages"]


def build_book(profile: Profile, scan: dict, structure: dict, matched: dict,
               chunks: Optional[dict] = None) -> Book:
    if profile.template not in TEMPLATES:
        raise ValueError(f"Chưa có mẫu phiên `{profile.template}`. Mẫu có sẵn: {sorted(TEMPLATES)}")
    files: dict = {}
    for fid, info in scan["pdfs"].items():
        files[fid] = PdfFile(kind="pdf", path=info["path"], pages=info["pages"],
                             pageOffset=profile.offset(fid), bytes=info["bytes"], sha256=info["sha256"],
                             chunks=[Chunk.model_validate(c) for c in (chunks or {}).get(fid, [])])
    for t in matched["tracks"]:
        files[t["id"]] = AudioFile(kind="audio", path=t["path"], title=t["title"], unit=t["unit"],
                                   durationSec=t["durationSec"], bytes=t["bytes"], sha256=t["sha256"],
                                   script=_ref("course-book", t.get("script"), "Tapescript"))

    ak, ts = structure.get("answerKey"), structure.get("tapescript")
    kv = _ref("course-book", structure.get("keyVocab"), "Key exam vocabulary")
    ex = structure.get("extract")
    has_workbook = "work-book" in profile.files
    has_tests = any(k.startswith("test") for k in profile.files)

    sections: list[Section] = []
    for sec in profile.sections:
        items: list[Item] = []
        for u in sec.units:
            st = structure["units"][str(u.no)]
            uk, uid = str(u.no), f"U{u.no:02d}"
            acts: list[Activity] = []
            for mod, rng in st["modules"].items():
                a = Activity(
                    id=f"{uid}-{mod}", module=mod, skill=MODULE_SKILL.get(mod, "other"),
                    title=f"Unit {u.no} · {MODULE_TITLE.get(mod, mod)}",
                    pdf="course-book", pages=rng,
                    printedPages=[rng[0] - profile.offset("course-book"), rng[1] - profile.offset("course-book")],
                    confidence=st["confidence"],
                )
                if mod in ("listening", "reading", "writing", "exam-practice", "speaking-vocab"):
                    a.answer = _ref("course-book", _lookup(ak, uk, mod), "Answer key")
                if mod in ("listening", "exam-practice"):
                    a.script = _ref("course-book", _lookup(ts, uk, mod), "Tapescript")
                if mod == "speaking-vocab":
                    a.vocab = kv
                if mod == "listening":
                    a.tracks = matched["byUnit"].get(uk, [])
                    if ex and uk in ex["units"]:
                        # Bản trích nhẹ (vài MB) mở nhanh trên điện thoại hơn cuốn 100 MB.
                        a.alt = [Ref(pdf="course-book", pages=rng, label="Course Book")]
                        a.pdf, a.pages = ex["file"], ex["units"][uk]
                acts.append(a)
            acts.append(Activity(
                id=f"{uid}-unit-review", module="workbook" if has_workbook else "unit-review", skill="other",
                title=f"Unit {u.no} · {'Work Book' if has_workbook else 'Ôn unit + sổ lỗi'}",
                answer=_ref("course-book", (ak or {}).get("units", {}).get(uk) or (ak or {}).get("pages"), "Answer key"),
                vocab=kv,
                note=None if has_workbook else
                "Bộ sách chưa có Work Book: làm lại các câu sai của unit, ghi sổ lỗi, ôn Key exam vocabulary.",
            ))
            items.append(Item(id=uid, kind="unit", no=u.no, title=u.title, pages=st["pages"], activities=acts))

        if sec.review_no is not None:
            rv = structure["reviews"][str(sec.review_no)]
            rk = f"R{sec.review_no}"
            answer = _ref("course-book", (ak or {}).get("index", {}).get(f"{rk}:review"), "Answer key")
            items.append(Item(id=rk, kind="review", no=sec.review_no, title=f"Review {sec.review_no}", pages=rv["pages"],
                              activities=[
                                  Activity(id=f"{rk}-part{i + 1}", module="review", skill="other",
                                           title=f"Review {sec.review_no} · phần {i + 1}", pdf="course-book",
                                           pages=part, answer=answer)
                                  for i, part in enumerate(rv["parts"])
                              ]))
            tk = f"T{sec.review_no}"
            items.append(Item(id=tk, kind="test", no=sec.review_no, title=f"Test {sec.review_no}", activities=[
                Activity(id=f"{tk}-test", module="test", skill="other", title=f"Test {sec.review_no}",
                         script=_ref("course-book", (ts or {}).get("index", {}).get(f"{tk}:test"), "Tapescript"),
                         note=None if has_tests else
                         "Bộ dữ liệu chưa có sách Test của Target 5.0 — làm một đề Cambridge IELTS GT thay thế.")
            ]))
        sections.append(Section(id=sec.id, title=sec.title, items=items))

    return Book(
        id=profile.book, title=profile.title, edition=profile.edition, template=profile.template,
        source=Source(agent=f"book-ingest {__version__}", profileSha256=profile.sha256),
        info=BookInfo(**{INFO_KEYS[k]: v for k, v in profile.info.items() if k in INFO_KEYS}),
        files=files, sections=sections, keyVocab=kv,
        skipped=[{"title": s.get("title"), "printed": [s.get("from"), s.get("to")]} for s in profile.skip],
        missing=profile.missing,
    )


def build_plan(profile: Profile, book: Book) -> Plan:
    steps_unit = [
        ("speaking-vocab", ["speaking-vocab"], "Speaking & Vocabulary"),
        ("listening", ["listening"], "Listening"),
        ("reading", ["reading"], "Reading"),
        ("writing-learn", ["writing"], "Writing: học kỹ năng, dàn ý, viết"),
        ("writing-review", ["writing"], "Writing: chấm, viết lại"),
        ("consolidation", ["consolidation", "exam-practice"], "Consolidation & Exam practice"),
        ("workbook", ["unit-review"], None),
    ]
    sessions: list[Session] = []

    def add(sec_id, item, kind, step, act_ids, title, note=None):
        seq = len(sessions) + 1
        sessions.append(Session(
            id=f"{sec_id}-{item.id}-{len([s for s in sessions if s.item == item.id]) + 1}",
            seq=seq, week=profile.start_week + (seq - 1) // profile.sessions_per_week,
            section=sec_id, item=item.id, kind=kind, step=step, core=step in CORE_STEPS,
            activityIds=act_ids, title=title, note=note))

    for sec in book.sections:
        for item in sec.items:
            have = {a.module: a.id for a in item.activities}
            if item.kind == "unit":
                for step, mods, label in steps_unit:
                    ids = [have[m] for m in mods if m in have] or ([have["workbook"]] if "workbook" in have else [])
                    wb = next((a for a in item.activities if a.id.endswith("-unit-review")), None)
                    if step == "workbook" and wb:
                        ids, label = [wb.id], wb.title.split(" · ", 1)[1]
                    add(sec.id, item, "unit", step, ids, f"Unit {item.no} · {label}")
            elif item.kind == "review":
                for i, a in enumerate(item.activities):
                    add(sec.id, item, "review", f"review-{i + 1}", [a.id], a.title)
            else:
                act = item.activities[0]
                for step, label in (("test-lr", "Listening + Reading"), ("test-ws", "Writing + Speaking"),
                                    ("test-grade", "Chấm và ghi sổ lỗi")):
                    add(sec.id, item, "test", step, [act.id], f"Test {item.no} · {label}", act.note)

    return Plan(
        bookId=book.id, template=book.template, startWeek=profile.start_week,
        sessionsPerWeek=profile.sessions_per_week, minutesPerSession=75,
        rules={"placementThreshold": 0.8, "shortenIfFinishAfterWeek": 30,
               "consolidationSkipWorkbook": 0.8, "coreSteps": CORE_STEPS},
        sessions=sessions,
    )
