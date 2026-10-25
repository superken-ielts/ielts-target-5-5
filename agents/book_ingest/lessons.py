"""Mẫu `lessons-v1` — lộ trình học không cần file sách (ví dụ GENKI I · lộ trình JLPT N5).

Không quét PDF, không OCR, không ghép audio: toàn bộ cấu trúc khai trong book.yaml.

    toc.sections[].items[]   mỗi mục là một unit (`unit: <số>`) hoặc một bài kiểm tra (`test: <số>`)
    steps                    các bước (phiên) mặc định của mỗi unit; mục có `steps` riêng thì dùng của mục
    step                     {id, title, skill, core, minutes, note}; mục ghi đè ghi chú bằng `notes: {<bước>: …}`

Mỗi bước của một mục thành một hoạt động `<mục>-<bước>` (ví dụ U01-part-a) và đúng một phiên học. Ghi chú bước
dùng được {no}, {title}, {topic}, {grammar}, {kana} lấy từ mục. Video bài giảng gắn vào hoạt động như sách thường.
"""
from __future__ import annotations

import hashlib
from dataclasses import dataclass, field
from pathlib import Path
from typing import Optional

import yaml

from . import __version__
from .profile import ProfileError
from .schemas import Activity, Book, BookInfo, Item, Plan, Section, Session, Source

TEMPLATE = "lessons-v1"
SKILLS = {"listening", "reading", "writing", "speaking", "vocab", "grammar", "other"}
INFO_KEYS = {"course": "course", "role": "role", "module": "module", "author": "author", "publisher": "publisher",
             "level": "level", "cefr": "cefr", "summary": "summary", "start_when": "startWhen"}


@dataclass
class Step:
    id: str
    title: str
    skill: str = "other"
    core: bool = False
    minutes: Optional[int] = None
    note: str = ""


@dataclass
class Entry:
    kind: str           # unit | test
    no: int
    title: str
    steps: list[Step]
    fields: dict = field(default_factory=dict)  # topic, grammar, kana… cho ghi chú
    notes: dict = field(default_factory=dict)

    @property
    def id(self) -> str:
        return f"U{self.no:02d}" if self.kind == "unit" else f"T{self.no}"

    @property
    def label(self) -> str:
        return f"Unit {self.no}" if self.kind == "unit" else self.title


@dataclass
class LessonsProfile:
    root: Path
    sha256: str
    book: str
    title: str
    edition: str
    start_week: int
    sessions_per_week: int
    minutes: int
    pace: list[int]
    info: dict
    sections: list[tuple[str, str, list[Entry]]]
    missing: list[str]


def is_lessons(raw: dict) -> bool:
    return raw.get("template") == TEMPLATE


def _steps(rows, where: str) -> list[Step]:
    if not isinstance(rows, list) or not rows:
        raise ProfileError(f"{where}: `steps` phải là danh sách bước")
    out = []
    for r in rows:
        if not isinstance(r, dict) or not r.get("id") or not r.get("title"):
            raise ProfileError(f"{where}: mỗi bước cần `id` và `title`: {r!r}")
        if r.get("skill", "other") not in SKILLS:
            raise ProfileError(f"{where}: kỹ năng `{r.get('skill')}` không hợp lệ (có: {', '.join(sorted(SKILLS))})")
        out.append(Step(id=str(r["id"]), title=str(r["title"]), skill=str(r.get("skill", "other")),
                        core=bool(r.get("core", False)), minutes=r.get("minutes"), note=str(r.get("note", "")).strip()))
    ids = [s.id for s in out]
    if len(set(ids)) != len(ids):
        raise ProfileError(f"{where}: trùng id bước: {ids}")
    return out


def load(book_dir: Path) -> LessonsProfile:
    book_dir = Path(book_dir)
    text = (book_dir / "book.yaml").read_bytes()
    raw = yaml.safe_load(text) or {}
    for key in ("book", "title", "steps", "toc"):
        if key not in raw:
            raise ProfileError(f"book.yaml thiếu khóa `{key}`")
    default = _steps(raw["steps"], "steps")
    sections = []
    seen: set[str] = set()
    for s in raw["toc"].get("sections") or []:
        entries = []
        for it in s.get("items") or []:
            kind = "unit" if "unit" in it else "test" if "test" in it else None
            if kind is None or not it.get("title"):
                raise ProfileError(f"{s.get('id')}: mỗi mục cần `unit: <số>` hoặc `test: <số>` và `title`: {it!r}")
            e = Entry(kind=kind, no=int(it[kind]), title=str(it["title"]),
                      steps=_steps(it["steps"], f"{kind} {it[kind]}") if "steps" in it else default,
                      fields={k: v for k, v in it.items() if k not in ("unit", "test", "title", "steps", "notes")},
                      notes=dict(it.get("notes") or {}))
            if e.id in seen:
                raise ProfileError(f"trùng mục {e.id}")
            bad = [k for k in e.notes if k not in {st.id for st in e.steps}]
            if bad:
                raise ProfileError(f"{e.id}: `notes` có bước không tồn tại: {bad}")
            seen.add(e.id)
            entries.append(e)
        if not entries:
            raise ProfileError(f"section {s.get('id')} không có mục nào")
        sections.append((str(s["id"]), str(s.get("title", s["id"])), entries))
    if not sections:
        raise ProfileError("toc.sections đang trống")
    pace = [int(x) for x in raw.get("pace") or []]
    return LessonsProfile(
        root=book_dir, sha256=hashlib.sha256(text).hexdigest(), book=str(raw["book"]), title=str(raw["title"]),
        edition=str(raw.get("edition", "")), start_week=int(raw.get("start_week", 1)),
        sessions_per_week=int(raw.get("sessions_per_week", 5)), minutes=int(raw.get("minutes_per_session", 45)),
        pace=pace, info=dict(raw.get("info") or {}), sections=sections, missing=list(raw.get("missing", [])),
    )


def _note(e: Entry, st: Step) -> Optional[str]:
    text = str(e.notes.get(st.id, st.note)).strip()
    if not text:
        return None
    grammar = e.fields.get("grammar") or []
    values = {"no": e.no, "title": e.title, "topic": e.fields.get("topic", ""), "kana": e.fields.get("kana", ""),
              "grammar": "; ".join(map(str, grammar)) if isinstance(grammar, list) else str(grammar)}
    try:
        return " ".join(text.format(**values).split())
    except (KeyError, IndexError, ValueError) as err:
        raise ProfileError(f"{e.id}/{st.id}: ghi chú có chỗ thay không hợp lệ ({err}): {text}") from None


def build(p: LessonsProfile) -> tuple[Book, Plan]:
    sections: list[Section] = []
    sessions: list[Session] = []
    for sid, stitle, entries in p.sections:
        items = []
        for e in entries:
            acts = [Activity(id=f"{e.id}-{st.id}", module=st.id, skill=st.skill, title=f"{e.label} · {st.title}",
                             note=_note(e, st), estMinutes=st.minutes or p.minutes) for st in e.steps]
            items.append(Item(id=e.id, kind=e.kind, no=e.no, title=e.title, activities=acts))
            for k, (st, a) in enumerate(zip(e.steps, acts), start=1):
                seq = len(sessions) + 1
                sessions.append(Session(
                    id=f"{sid}-{e.id}-{k}", seq=seq, week=p.start_week + (seq - 1) // p.sessions_per_week,
                    section=sid, item=e.id, kind=e.kind, step=st.id, core=st.core, activityIds=[a.id],
                    title=a.title, estMinutes=a.estMinutes))
        sections.append(Section(id=sid, title=stitle, items=items))
    book = Book(id=p.book, title=p.title, edition=p.edition, template=TEMPLATE,
                source=Source(agent=f"book-ingest {__version__}", profileSha256=p.sha256),
                info=BookInfo(**{INFO_KEYS[k]: v for k, v in p.info.items() if k in INFO_KEYS}),
                files={}, sections=sections, missing=p.missing)
    rules = {"coreSteps": sorted({s.step for s in sessions if s.core})}
    if p.pace:
        rules["paceOptions"] = p.pace
    plan = Plan(bookId=p.book, template=TEMPLATE, startWeek=p.start_week, sessionsPerWeek=p.sessions_per_week,
                minutesPerSession=p.minutes, rules=rules, sessions=sessions)
    return book, plan


def report(p: LessonsProfile, plan: Plan) -> str:
    rows = [f"# Báo cáo nhập sách — {p.title}", "",
            "Sinh tự động bởi `book ingest` (mẫu lessons-v1, không cần file sách). Đừng sửa tay; sửa book.yaml rồi chạy lại.",
            "", "## Cấu trúc", "", "| Mục | Tên | Phiên |", "|---|---|---|"]
    for _, stitle, entries in p.sections:
        for e in entries:
            rows.append(f"| {e.id} | {e.title} | " + " · ".join(st.title for st in e.steps) + " |")
    weeks = [plan.sessions[0].week, plan.sessions[-1].week] if plan.sessions else ["?", "?"]
    hours = sum(s.estMinutes for s in plan.sessions) / 60
    rows += ["", "## Kế hoạch", "",
             f"{len(plan.sessions)} phiên (≈ {hours:.0f} giờ), mặc định {plan.minutesPerSession} phút/phiên, "
             f"{plan.sessionsPerWeek} phiên/tuần, tuần {weeks[0]}–{weeks[1]}."]
    if p.missing:
        rows += ["", "Thiếu trong bộ dữ liệu: " + ", ".join(p.missing) + "."]
    return "\n".join(rows) + "\n"
