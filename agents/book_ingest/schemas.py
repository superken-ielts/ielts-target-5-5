"""Hợp đồng dữ liệu giữa agent và app (docs/agent-hoc-tap/02 mục 3).

JSON Schema xuất từ các model này nằm ở schemas/ ở gốc repo (lệnh `book schemas`).
Quy ước: số trang là chỉ số trang PDF bắt đầu từ 1; `printedPages` chỉ để hiển thị.
"""
from __future__ import annotations

from typing import Literal, Optional, Union

from pydantic import BaseModel, ConfigDict, Field, field_validator


class _M(BaseModel):
    model_config = ConfigDict(populate_by_name=True, extra="forbid")


def _range(v: Optional[list[int]]) -> Optional[list[int]]:
    if v is None:
        return v
    if len(v) != 2 or v[0] < 1 or v[1] < v[0]:
        raise ValueError(f"khoảng trang không hợp lệ: {v}")
    return v


class Ref(_M):
    """Trỏ tới một khoảng trang trong một file PDF của sách."""
    pdf: str
    pages: list[int]
    label: Optional[str] = None

    @field_validator("pages")
    @classmethod
    def check_pages(cls, v):
        return _range(v)


class Activity(_M):
    id: str
    module: str
    skill: Literal["listening", "reading", "writing", "speaking", "vocab", "grammar", "other"]
    title: str
    pdf: Optional[str] = None
    pages: Optional[list[int]] = None
    printedPages: Optional[list[int]] = None
    tracks: list[str] = []
    answer: Optional[Ref] = None
    script: Optional[Ref] = None
    vocab: Optional[Ref] = None
    alt: list[Ref] = []
    note: Optional[str] = None
    estMinutes: int = 75
    confidence: float = 1.0

    @field_validator("pages", "printedPages")
    @classmethod
    def check_pages(cls, v):
        return _range(v)


class Item(_M):
    id: str
    kind: Literal["unit", "review", "test"]
    no: int
    title: str
    pages: Optional[list[int]] = None
    activities: list[Activity] = []


class Section(_M):
    id: str
    title: str
    items: list[Item]


class Chunk(_M):
    """Một đoạn PDF nhỏ cắt từ file gốc để app tải nhanh. Trang trong book.json vẫn tính theo file gốc."""
    path: str
    from_: int = Field(alias="from")
    to: int
    bytes: int
    sha256: str


class PdfFile(_M):
    kind: Literal["pdf"]
    path: str
    pages: int
    pageOffset: int = 0
    bytes: int
    sha256: str
    chunks: list[Chunk] = []


class AudioFile(_M):
    kind: Literal["audio"]
    path: str
    title: str
    unit: int
    durationSec: Optional[float] = None
    bytes: int
    sha256: str
    script: Optional[Ref] = None


class Source(_M):
    agent: str
    profileSha256: str


class Book(_M):
    schema_: Literal["book/1"] = Field("book/1", alias="schema")
    id: str
    title: str
    edition: str = ""
    template: str
    source: Source
    files: dict[str, Union[PdfFile, AudioFile]]
    sections: list[Section]
    keyVocab: Optional[Ref] = None
    skipped: list[dict] = []
    missing: list[str] = []


class Session(_M):
    id: str
    seq: int
    week: int
    section: str
    item: str
    kind: Literal["unit", "review", "test"]
    step: str
    core: bool
    activityIds: list[str]
    title: str
    estMinutes: int = 75
    note: Optional[str] = None


class Plan(_M):
    schema_: Literal["plan/1"] = Field("plan/1", alias="schema")
    bookId: str
    template: str
    startWeek: int
    sessionsPerWeek: int
    minutesPerSession: int
    rules: dict
    sessions: list[Session]


class ReviewItem(_M):
    id: str
    kind: str
    severity: Literal["info", "warn", "error"]
    subject: str
    message: str
    confidence: Optional[float] = None
    proposal: Optional[dict] = None
    options: list[dict] = []
    evidence: list[dict] = []
    decision: Optional[dict] = None


class Review(_M):
    schema_: Literal["review/1"] = Field("review/1", alias="schema")
    agent: str = "book-ingest"
    items: list[ReviewItem] = []


class TocUnit(_M):
    no: int
    title: str
    printed_start: int


class TocSection(_M):
    id: str
    title: str
    units: list[TocUnit]
    review_no: Optional[int] = None
    review_printed_start: Optional[int] = None


class TocDraft(_M):
    """Kết quả bước đọc mục lục (LLM hoặc người điền) trước khi thành book.yaml."""
    title: str
    sections: list[TocSection]
    key_vocab_printed: Optional[list[int]] = None
    answer_key_printed: Optional[list[int]] = None
    tapescript_printed: Optional[list[int]] = None
    skip_titles: list[str] = []


def dump(model: BaseModel) -> dict:
    return model.model_dump(by_alias=True, exclude_none=True)


SCHEMAS = {"book": Book, "plan": Plan, "review": Review}
