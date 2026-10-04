"""Đọc hồ sơ cuốn sách (book.yaml) và đổi số trang in sang chỉ số trang PDF."""
from __future__ import annotations

import hashlib
from dataclasses import dataclass, field
from pathlib import Path
from typing import Optional

import yaml


class ProfileError(ValueError):
    pass


@dataclass
class UnitSpec:
    no: int
    title: str
    printed_start: int
    printed_end: int = 0


@dataclass
class SectionSpec:
    id: str
    title: str
    units: list[UnitSpec]
    review_no: Optional[int] = None
    review_printed: Optional[list[int]] = None   # [đầu, cuối]


@dataclass
class Profile:
    root: Path
    raw: dict
    sha256: str
    book: str
    title: str
    edition: str
    template: str
    start_week: int
    sessions_per_week: int
    files: dict
    modules: list[str]
    module_offsets: list[int]
    banner_top: float
    banner_min_red: float
    sections: list[SectionSpec]
    key_vocab: Optional[list[int]]
    skip: list[dict]
    answer_key: Optional[list[int]]
    tapescript: Optional[list[int]]
    listening_extract: Optional[dict]
    missing: list[str] = field(default_factory=list)
    review_threshold: float = 0.9

    # --- quy đổi trang -------------------------------------------------
    def offset(self, file_id: str) -> int:
        return int(self.files.get(file_id, {}).get("page_offset", 0))

    def pdf_page(self, printed: int, file_id: str = "course-book") -> int:
        return printed + self.offset(file_id)

    def pdf_range(self, printed: list[int], file_id: str = "course-book") -> list[int]:
        return [self.pdf_page(printed[0], file_id), self.pdf_page(printed[1], file_id)]

    def path(self, file_id: str) -> Path:
        spec = self.files[file_id]
        return self.root / (spec.get("path") or spec.get("dir"))

    def pdf_ids(self) -> list[str]:
        return [k for k, v in self.files.items() if v.get("kind") == "pdf"]

    def all_units(self) -> list[UnitSpec]:
        return [u for s in self.sections for u in s.units]


def _pair(v, name) -> Optional[list[int]]:
    if v is None:
        return None
    if not (isinstance(v, list) and len(v) == 2 and all(isinstance(x, int) for x in v) and v[0] <= v[1]):
        raise ProfileError(f"{name} phải là [trang đầu, trang cuối], nhận được {v!r}")
    return v


def load(book_dir: Path) -> Profile:
    book_dir = Path(book_dir)
    path = book_dir / "book.yaml"
    if not path.exists():
        raise ProfileError(f"Không thấy {path}. Chạy `book profile` để tạo bản nháp.")
    text = path.read_bytes()
    raw = yaml.safe_load(text) or {}
    for key in ("book", "title", "template", "files", "toc"):
        if key not in raw:
            raise ProfileError(f"book.yaml thiếu khóa `{key}`")
    toc = raw["toc"]
    sections: list[SectionSpec] = []
    for s in toc.get("sections", []):
        units = [UnitSpec(no=int(u[0]), title=str(u[1]), printed_start=int(u[2])) for u in s.get("units", [])]
        rv = s.get("review")
        sections.append(SectionSpec(
            id=s["id"], title=s.get("title", s["id"]), units=units,
            review_no=int(rv[0]) if rv else None,
            review_printed=[int(rv[1]), 0] if rv else None,
        ))
    if not sections:
        raise ProfileError("toc.sections đang trống")

    # Trang cuối của mỗi phần = trang đầu của phần kế tiếp − 1.
    starts: list[tuple[str, object, int]] = []
    for s in sections:
        for u in s.units:
            starts.append(("unit", u, u.printed_start))
        if s.review_printed:
            starts.append(("review", s, s.review_printed[0]))
    tail = []
    for key in ("key_vocab", "answer_key", "tapescript"):
        if toc.get(key):
            tail.append(toc[key][0])
    tail += [int(x["from"]) for x in toc.get("skip", [])]
    for i, (kind, obj, start) in enumerate(starts):
        nxt = starts[i + 1][2] if i + 1 < len(starts) else min([t for t in tail if t > start], default=None)
        if nxt is None:
            raise ProfileError(f"Không xác định được trang cuối của phần bắt đầu ở trang in {start}")
        if nxt <= start:
            raise ProfileError(f"Mục lục không tăng dần quanh trang in {start}")
        if kind == "unit":
            obj.printed_end = nxt - 1
        else:
            obj.review_printed[1] = nxt - 1

    modules = raw.get("modules") or ["speaking-vocab", "listening", "reading", "writing", "consolidation", "exam-practice"]
    offsets = raw.get("module_offsets") or []
    if offsets and len(offsets) != len(modules):
        raise ProfileError("module_offsets phải có cùng số phần tử với modules")
    banner = raw.get("banner") or {}
    return Profile(
        root=book_dir,
        raw=raw,
        sha256=hashlib.sha256(text).hexdigest(),
        book=str(raw["book"]),
        title=str(raw["title"]),
        edition=str(raw.get("edition", "")),
        template=str(raw["template"]),
        start_week=int(raw.get("start_week", 1)),
        sessions_per_week=int(raw.get("sessions_per_week", 6)),
        files=raw["files"],
        modules=list(modules),
        module_offsets=list(offsets),
        banner_top=float(banner.get("top", 0.08)),
        banner_min_red=float(banner.get("min_red", 0.03)),
        sections=sections,
        key_vocab=_pair(toc.get("key_vocab"), "toc.key_vocab"),
        skip=list(toc.get("skip", [])),
        answer_key=_pair(toc.get("answer_key"), "toc.answer_key"),
        tapescript=_pair(toc.get("tapescript"), "toc.tapescript"),
        listening_extract=raw.get("listening_extract"),
        missing=list(raw.get("missing", [])),
        review_threshold=float(raw.get("review_threshold", 0.9)),
    )
