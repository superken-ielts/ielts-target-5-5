"""Mẫu `lessons-v1` — lộ trình khai hết trong book.yaml (ví dụ GENKI I · lộ trình JLPT N5).

Agent không đoán cấu trúc từ PDF: mục lục, các bước và chỗ trong sách của từng bước đều khai ở book.yaml.

    toc.sections[].items[]   mỗi mục là một unit (`unit: <số>`) hoặc một bài kiểm tra (`test: <số>`)
    steps                    các bước (phiên) mặc định của mỗi unit; mục có `steps` riêng thì dùng của mục
    step                     {id, title, skill, core, minutes, note}; mục ghi đè ghi chú bằng `notes: {<bước>: …}`
    files                    (tuỳ chọn) PDF và thư mục audio, khai như mẫu sách thường; id track = tên file bỏ
                             đuôi, `_` đổi thành `-` (K01_05.mp3 → K01-05, đúng nhãn in cạnh bài tập trong sách).
                             Sách in nhãn theo đĩa (1.7 = CD1 track 7) thì thư mục audio khai `track: "1.{n}"`:
                             {n} là số cuối trong tên file (Track No07.mp3 → 1.7). Một PDF quét thiếu hoặc trùng
                             trang giữa sách thì khai hai lần (hai id, cùng `path`, khác `page_offset`)
    item.pages               (tuỳ chọn) trang in của mục trong PDF chính, hiện trên thẻ unit
    item.refs                (tuỳ chọn) chỗ trong sách của từng bước: {<bước>: {pdf, pages: [trang in đầu, cuối],
                             tracks: "K01-01..K01-08, K01-24", alt: [{pdf, pages, label}]}}; `pdf` mặc định là PDF
                             khai đầu tiên trong `files`

Mỗi bước của một mục thành một hoạt động `<mục>-<bước>` (ví dụ U01-part-a) và đúng một phiên học. Ghi chú bước
dùng được {no}, {title} và mọi trường khác của mục ({topic}, {grammar}, {kana}… — danh sách thì nối bằng `; `). Có `files` thì mỗi track phải thuộc đúng một bước
(V4), và PDF lớn được cắt thành đoạn theo các khoảng trang của từng mục (chunks.py). Video bài giảng gắn vào hoạt
động như sách thường.
"""
from __future__ import annotations

import hashlib
import re
from dataclasses import dataclass, field
from pathlib import Path
from typing import Optional

import yaml

from . import __version__
from .profile import ProfileError, _pair
from .schemas import Activity, AudioFile, Book, BookInfo, Item, PdfFile, Plan, Ref, Section, Session, Source

TEMPLATE = "lessons-v1"
SKILLS = {"listening", "reading", "writing", "speaking", "vocab", "grammar", "other"}
INFO_KEYS = {"course": "course", "role": "role", "module": "module", "author": "author", "publisher": "publisher",
             "level": "level", "cefr": "cefr", "summary": "summary", "start_when": "startWhen"}
REF_KEYS = {"pdf", "pages", "tracks", "alt"}


@dataclass
class Step:
    id: str
    title: str
    skill: str = "other"
    core: bool = False
    minutes: Optional[int] = None
    note: str = ""


@dataclass
class Place:
    """Một khoảng trang in trong một file PDF của sách."""
    pdf: str
    pages: list[int]
    label: Optional[str] = None


@dataclass
class StepRef:
    main: Optional[Place] = None
    tracks: list[str] = field(default_factory=list)   # id hoặc khoảng "A..B", chưa đối chiếu với thư mục audio
    alt: list[Place] = field(default_factory=list)


@dataclass
class Entry:
    kind: str           # unit | test
    no: int
    title: str
    steps: list[Step]
    fields: dict = field(default_factory=dict)  # topic, grammar, kana… cho ghi chú
    notes: dict = field(default_factory=dict)
    pages: Optional[list[int]] = None           # trang in trong PDF chính
    refs: dict = field(default_factory=dict)    # bước → StepRef

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
    files: dict = field(default_factory=dict)

    # cùng giao diện với profile.Profile cho scan.py và chunks.py
    def path(self, file_id: str) -> Path:
        spec = self.files[file_id]
        return self.root / (spec.get("path") or spec.get("dir"))

    def pdf_ids(self) -> list[str]:
        return [k for k, v in self.files.items() if v.get("kind") == "pdf"]

    def pdf_range(self, place: Place) -> list[int]:
        off = int(self.files[place.pdf].get("page_offset", 0))
        return [place.pages[0] + off, place.pages[1] + off]

    def entries(self) -> list[Entry]:
        return [e for _, _, entries in self.sections for e in entries]


def is_lessons(raw: dict) -> bool:
    return raw.get("template") == TEMPLATE


def track_id(name: str, fmt: Optional[str] = None) -> str:
    stem = Path(name).stem
    if fmt:
        nums = re.findall(r"\d+", stem)
        if not nums:
            raise ProfileError(f"file audio `{name}` không có số track để ghép vào `{fmt}`")
        return fmt.format(n=int(nums[-1]))
    return stem.replace("_", "-")


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


def _files(raw) -> dict:
    files = dict(raw or {})
    for fid, spec in files.items():
        kind = (spec or {}).get("kind")
        if not (kind == "pdf" and spec.get("path") or kind == "audio" and spec.get("dir")):
            raise ProfileError(f"files.{fid}: cần `kind: pdf` + `path` hoặc `kind: audio` + `dir`")
        fmt = spec.get("track")
        if fmt is not None and (kind != "audio" or not isinstance(fmt, str) or "{n}" not in fmt
                                or not _formats(fmt)):
            raise ProfileError(f"files.{fid}.track: cần chuỗi có {{n}} (ví dụ \"1.{{n}}\") và chỉ dùng cho thư mục audio")
    return files


def _formats(fmt: str) -> bool:
    try:
        fmt.format(n=1)
        return True
    except (KeyError, IndexError, ValueError):
        return False


def _place(raw, where: str, files: dict, default_pdf: Optional[str]) -> Place:
    if not isinstance(raw, dict) or "pages" not in raw:
        raise ProfileError(f"{where}: cần `pages: [trang in đầu, trang in cuối]`")
    pdf = str(raw.get("pdf") or default_pdf or "")
    if (files.get(pdf) or {}).get("kind") != "pdf":
        raise ProfileError(f"{where}: `pdf: {pdf}` không phải file PDF khai trong `files`")
    return Place(pdf=pdf, pages=_pair(raw["pages"], f"{where}.pages"), label=raw.get("label"))


def _refs(raw, e: Entry, files: dict) -> dict:
    if not raw:
        return {}
    if not files:
        raise ProfileError(f"{e.id}: có `refs` nhưng book.yaml chưa khai `files`")
    default_pdf = next((k for k, v in files.items() if v.get("kind") == "pdf"), None)
    steps = {st.id for st in e.steps}
    out = {}
    for sid, r in raw.items():
        where = f"{e.id}.refs.{sid}"
        if sid not in steps:
            raise ProfileError(f"{e.id}: `refs` có bước không tồn tại: {sid}")
        if not isinstance(r, dict) or set(r) - REF_KEYS:
            raise ProfileError(f"{where}: chỉ nhận các khóa {sorted(REF_KEYS)}, nhận được {r!r}")
        tracks = r.get("tracks") or []
        if isinstance(tracks, str):
            tracks = tracks.split(",")
        out[sid] = StepRef(
            main=_place(r, where, files, default_pdf) if "pages" in r else None,
            tracks=[str(t).strip() for t in tracks if str(t).strip()],
            alt=[_place(a, f"{where}.alt", files, default_pdf) for a in r.get("alt") or []])
    return out


def load(book_dir: Path) -> LessonsProfile:
    book_dir = Path(book_dir)
    text = (book_dir / "book.yaml").read_bytes()
    raw = yaml.safe_load(text) or {}
    for key in ("book", "title", "steps", "toc"):
        if key not in raw:
            raise ProfileError(f"book.yaml thiếu khóa `{key}`")
    files = _files(raw.get("files"))
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
                      fields={k: v for k, v in it.items()
                              if k not in ("unit", "test", "title", "steps", "notes", "pages", "refs")},
                      notes=dict(it.get("notes") or {}))
            if e.id in seen:
                raise ProfileError(f"trùng mục {e.id}")
            bad = [k for k in e.notes if k not in {st.id for st in e.steps}]
            if bad:
                raise ProfileError(f"{e.id}: `notes` có bước không tồn tại: {bad}")
            if "pages" in it:
                if not any(v.get("kind") == "pdf" for v in files.values()):
                    raise ProfileError(f"{e.id}: có `pages` nhưng book.yaml chưa khai file PDF trong `files`")
                e.pages = _pair(it["pages"], f"{e.id}.pages")
            e.refs = _refs(it.get("refs"), e, files)
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
        files=files,
    )


def chunk_ranges(p: LessonsProfile) -> dict[str, list[list[int]]]:
    """Ranh giới đoạn PDF: các khoảng trang của một mục, khoảng nào chạm hoặc kề nhau thì gộp (phần 会話・文法 và
    phần 読み書き của cùng một bài nằm xa nhau nên thành hai đoạn). Đoạn nằm trọn trong đoạn khác thì bỏ."""
    out: dict[str, list[list[int]]] = {}
    for e in p.entries():
        spans: dict[str, list[list[int]]] = {}
        for r in e.refs.values():
            for place in ([r.main] if r.main else []) + r.alt:
                spans.setdefault(place.pdf, []).append(p.pdf_range(place))
        for pdf, rs in spans.items():
            merged: list[list[int]] = []
            for a, b in sorted(rs):
                if merged and a <= merged[-1][1] + 1:
                    merged[-1][1] = max(merged[-1][1], b)
                else:
                    merged.append([a, b])
            out.setdefault(pdf, []).extend(merged)
    for pdf, rs in out.items():
        keep: list[list[int]] = []
        for a, b in sorted({(a, b) for a, b in rs}, key=lambda r: (r[0], -r[1])):
            if not any(k[0] <= a and b <= k[1] for k in keep):
                keep.append([a, b])
        out[pdf] = keep
    return out


def _expand(spec: str, order: list[str], groups: dict[str, str], where: str) -> list[str]:
    index = {t: i for i, t in enumerate(order)}
    if ".." not in spec:
        if spec not in index:
            raise ProfileError(f"{where}: không có track `{spec}` trong thư mục audio")
        return [spec]
    a, b = (x.strip() for x in spec.split("..", 1))
    for t in (a, b):
        if t not in index:
            raise ProfileError(f"{where}: không có track `{t}` trong thư mục audio (khoảng `{spec}`)")
    if groups[a] != groups[b] or index[a] > index[b]:
        raise ProfileError(f"{where}: khoảng track `{spec}` phải đi xuôi và nằm trong cùng một thư mục audio")
    return order[index[a]:index[b] + 1]


def build(p: LessonsProfile, data: Optional[dict] = None, parts: Optional[dict] = None) -> tuple[Book, Plan]:
    """`data` là kết quả scan.scan (cần khi book.yaml có `files`), `parts` là các đoạn PDF đã cắt theo file."""
    data, parts = data or {"pdfs": {}, "audio": []}, parts or {}
    audio = {track_id(a["name"], p.files[a["group"]].get("track")): a for a in data["audio"]}
    if len(audio) != len(data["audio"]):
        raise ProfileError("hai file audio trùng id track (tên file chỉ khác `_` / `-` hoặc khác đuôi, hoặc hai thư "
                           "mục audio đánh số lại từ 1 mà chưa khai `track`)")
    order, groups = list(audio), {t: a["group"] for t, a in audio.items()}
    owner: dict[str, Entry] = {}

    def ref(place: Place, label: Optional[str] = None) -> Ref:
        return Ref(pdf=place.pdf, pages=p.pdf_range(place), label=label)

    sections: list[Section] = []
    sessions: list[Session] = []
    for sid, stitle, entries in p.sections:
        items = []
        for e in entries:
            acts = []
            for st in e.steps:
                r = e.refs.get(st.id) or StepRef()
                tracks = []
                for spec in r.tracks:
                    for t in _expand(spec, order, groups, f"{e.id}.refs.{st.id}"):
                        if t in owner or t in tracks:
                            raise ProfileError(f"track {t} được gán hai lần ({(owner.get(t) or e).id} và {e.id}/{st.id})")
                        tracks.append(t)
                owner.update({t: e for t in tracks})
                acts.append(Activity(
                    id=f"{e.id}-{st.id}", module=st.id, skill=st.skill, title=f"{e.label} · {st.title}",
                    pdf=r.main.pdf if r.main else None, pages=p.pdf_range(r.main) if r.main else None,
                    printedPages=list(r.main.pages) if r.main else None, tracks=tracks, note=_note(e, st), estMinutes=st.minutes or p.minutes,
                    alt=[ref(a, a.label or _alt_label(p, a)) for a in r.alt]))
            pages = p.pdf_range(Place(pdf=p.pdf_ids()[0], pages=e.pages)) if e.pages and p.pdf_ids() else None
            items.append(Item(id=e.id, kind=e.kind, no=e.no, title=e.title, pages=pages, activities=acts))
            for k, (st, a) in enumerate(zip(e.steps, acts), start=1):
                seq = len(sessions) + 1
                sessions.append(Session(
                    id=f"{sid}-{e.id}-{k}", seq=seq, week=p.start_week + (seq - 1) // p.sessions_per_week,
                    section=sid, item=e.id, kind=e.kind, step=st.id, core=st.core, activityIds=[a.id],
                    title=a.title, estMinutes=a.estMinutes))
        sections.append(Section(id=sid, title=stitle, items=items))
    loose = [t for t in order if t not in owner]
    if loose:
        raise ProfileError(f"{len(loose)} track chưa thuộc bước nào (thêm vào `refs.<bước>.tracks`): "
                           + ", ".join(loose[:12]) + (" …" if len(loose) > 12 else ""))

    files: dict = {}
    for fid in p.pdf_ids():
        f = data["pdfs"][fid]
        files[fid] = PdfFile(kind="pdf", path=f["path"], pages=f["pages"], bytes=f["bytes"], sha256=f["sha256"],
                             pageOffset=int(p.files[fid].get("page_offset", 0)), chunks=parts.get(fid, []))
    for t, a in audio.items():
        files[t] = AudioFile(kind="audio", path=a["path"], title=t, unit=owner[t].no, durationSec=a["durationSec"],
                             bytes=a["bytes"], sha256=a["sha256"])
    book = Book(id=p.book, title=p.title, edition=p.edition, template=TEMPLATE,
                source=Source(agent=f"book-ingest {__version__}", profileSha256=p.sha256),
                info=BookInfo(**{INFO_KEYS[k]: v for k, v in p.info.items() if k in INFO_KEYS}),
                files=files, sections=sections, missing=p.missing)
    rules = {"coreSteps": sorted({s.step for s in sessions if s.core})}
    if p.pace:
        rules["paceOptions"] = p.pace
    plan = Plan(bookId=p.book, template=TEMPLATE, startWeek=p.start_week, sessionsPerWeek=p.sessions_per_week,
                minutesPerSession=p.minutes, rules=rules, sessions=sessions)
    return book, plan


def _alt_label(p: LessonsProfile, place: Place) -> str:
    name = p.files[place.pdf].get("label") or place.pdf
    a, b = place.pages
    return f"{name} tr. {a}" + (f"–{b}" if b != a else "")


def _note(e: Entry, st: Step) -> Optional[str]:
    text = str(e.notes.get(st.id, st.note)).strip()
    if not text:
        return None
    values = {"topic": "", "kana": "", "grammar": ""}
    values.update({k: "; ".join(map(str, v)) if isinstance(v, list) else str(v) for k, v in e.fields.items()})
    values.update(no=e.no, title=e.title)
    try:
        return " ".join(text.format(**values).split())
    except (KeyError, IndexError, ValueError) as err:
        raise ProfileError(f"{e.id}/{st.id}: ghi chú có chỗ thay không hợp lệ ({err}): {text}") from None


def _tracks_text(ids: list[str]) -> str:
    if not ids:
        return ""
    return f"{len(ids)}: " + (ids[0] if len(ids) == 1 else f"{ids[0]} … {ids[-1]}" if len(ids) > 2 else ", ".join(ids))


def report(p: LessonsProfile, book: Book, plan: Plan, data: Optional[dict] = None) -> str:
    rows = [f"# Báo cáo nhập sách — {p.title}", "",
            "Sinh tự động bởi `book ingest` (mẫu lessons-v1: cấu trúc và chỗ trong sách khai ở book.yaml). "
            "Đừng sửa tay; sửa book.yaml rồi chạy lại.", ""]
    if data:
        rows += ["## File", "", "| File | Trang/độ dài | Cỡ | Đoạn cho app |", "|---|---|---|---|"]
        for fid, f in data["pdfs"].items():
            n = len(book.files[fid].chunks)
            off = book.files[fid].pageOffset
            rows.append(f"| {fid}: `{f['path']}` | {f['pages']} trang, trang in = trang PDF {'−' if off >= 0 else '+'} "
                        f"{abs(off)} | {f['bytes'] / 1e6:.1f} MB | {n or '—'} |")
        by_group: dict[str, list[dict]] = {}
        for a in data["audio"]:
            by_group.setdefault(a["group"], []).append(a)
        for g, items in by_group.items():
            rows.append(f"| {g}: `{p.files[g]['dir']}/` | {len(items)} track, "
                        f"{sum(a['durationSec'] or 0 for a in items) / 60:.0f} phút | "
                        f"{sum(a['bytes'] for a in items) / 1e6:.0f} MB | — |")
        if data.get("duplicates"):
            rows += ["", "Audio trùng nội dung: " + "; ".join(" = ".join(d) for d in data["duplicates"]) + "."]
        rows.append("")
    rows += ["## Cấu trúc", "", "| Mục | Phiên | Trang (in) | Track |", "|---|---|---|---|"]
    for sec in book.sections:
        for item in sec.items:
            for a in item.activities:
                where = [f"{a.pdf} {_printed(book, a.pdf, a.pages)}"] if a.pdf else []
                where += [f"{r.pdf} {_printed(book, r.pdf, r.pages)}" for r in a.alt]
                rows.append(f"| {item.id} {item.title} | {a.title.split(' · ', 1)[-1]} | {' · '.join(where) or '—'} | "
                            f"{_tracks_text(a.tracks) or '—'} |")
    weeks = [plan.sessions[0].week, plan.sessions[-1].week] if plan.sessions else ["?", "?"]
    hours = sum(s.estMinutes for s in plan.sessions) / 60
    rows += ["", "## Kế hoạch", "",
             f"{len(plan.sessions)} phiên (≈ {hours:.0f} giờ), mặc định {plan.minutesPerSession} phút/phiên, "
             f"{plan.sessionsPerWeek} phiên/tuần, tuần {weeks[0]}–{weeks[1]}."]
    if p.missing:
        rows += ["", "Thiếu trong bộ dữ liệu: " + ", ".join(p.missing) + "."]
    return "\n".join(rows) + "\n"


def _printed(book: Book, pdf: str, pages: list[int]) -> str:
    off = book.files[pdf].pageOffset
    a, b = pages[0] - off, pages[1] - off
    return f"{a}" + (f"–{b}" if b != a else "")
