"""Kịch bản bài giảng: đọc file YAML, kiểm tra, chuẩn hóa câu thoại.

Mỗi cảnh (scene) là một kiểu slide; mỗi dòng trong `lines` là một câu thoại của một người nói
(khóa là mã người nói, ví dụ `emma: "Hello"`) hoặc một khoảng lặng có đếm ngược (`wait: 8`) để người
học tự nói. `focus` chọn mục đang nói tới, `reveal` mở dần đáp án; cả hai giữ nguyên tới dòng sau.
"""
from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Literal, Optional

import yaml
from pydantic import BaseModel, ConfigDict, Field, ValidationError, field_validator, model_validator

Kind = Literal["title", "bullets", "vocab", "match", "pairs", "qa", "compare", "errors", "practice"]

# Khóa bắt buộc của từng mục theo kiểu cảnh
ITEM_KEYS: dict[str, tuple[str, ...]] = {
    "title": (),
    "bullets": ("en",),
    "vocab": ("w", "vi", "ex"),
    "match": ("n", "q", "answer"),
    "pairs": ("n", "q", "answer"),
    "qa": ("q", "a"),
    "compare": ("title", "lines"),
    "errors": ("wrong", "right"),
    "practice": ("q",),
}
LINE_FIELDS = {"say", "vi", "focus", "reveal", "wait", "pause", "note"}


class _M(BaseModel):
    model_config = ConfigDict(extra="forbid")


class Speaker(_M):
    name: str
    role: str = ""
    voice: str
    color: str = "#C8102E"

    @field_validator("color")
    @classmethod
    def _hex(cls, v: str) -> str:
        if not re.fullmatch(r"#[0-9A-Fa-f]{6}", v):
            raise ValueError(f"màu phải dạng #RRGGBB: {v}")
        return v


class ImageRef(_M):
    pdf: str
    page: int = Field(ge=1)
    clip: tuple[float, float, float, float]


class Line(_M):
    speaker: Optional[str] = None
    text: str = ""
    say: Optional[str] = None
    vi: str = ""
    focus: Optional[int] = None
    reveal: list[str] = []
    wait: float = Field(0, ge=0, le=60)
    pause: float = Field(0, ge=0, le=10)
    note: str = ""

    @field_validator("reveal", mode="before")
    @classmethod
    def _list(cls, v):
        if v is None:
            return []
        return [str(x) for x in (v if isinstance(v, list) else [v])]

    @model_validator(mode="after")
    def _kind(self):
        if bool(self.speaker) == bool(self.wait):
            raise ValueError("mỗi dòng là một câu thoại (khóa = mã người nói) hoặc một khoảng lặng `wait`")
        if self.speaker and not self.text.strip():
            raise ValueError(f"câu thoại của {self.speaker} trống")
        return self

    @property
    def spoken(self) -> str:
        return self.say or self.text


class Scene(_M):
    kind: Kind
    chapter: str = ""
    heading: str = ""
    heading_vi: str = ""
    items: list[dict] = []
    options: list[dict] = []
    image: Optional[ImageRef] = None
    lines: list[Line]

    @model_validator(mode="after")
    def _items(self):
        need = ITEM_KEYS[self.kind]
        for i, it in enumerate(self.items):
            miss = [k for k in need if k not in it]
            if miss:
                raise ValueError(f"cảnh {self.kind}: mục {i} thiếu {', '.join(miss)}")
        if need and not self.items:
            raise ValueError(f"cảnh {self.kind} cần `items`")
        if self.kind == "pairs" and not self.options:
            raise ValueError("cảnh pairs cần `options` (cột đáp án a, b, c…)")
        if self.kind == "match" and not self.image:
            raise ValueError("cảnh match cần `image`")
        if not self.lines:
            raise ValueError("cảnh không có câu thoại nào")
        keys = self.reveal_keys()
        for ln in self.lines:
            if ln.focus is not None and not 0 <= ln.focus < max(len(self.items), 1):
                raise ValueError(f"focus {ln.focus} ngoài số mục ({len(self.items)})")
            bad = [r for r in ln.reveal if r not in keys]
            if bad:
                raise ValueError(f"reveal không khớp mục nào: {bad}")
        return self

    def reveal_keys(self) -> set[str]:
        if self.kind in ("match", "pairs"):
            return {str(it["n"]) for it in self.items}
        return {str(i) for i in range(len(self.items))}


class Lesson(_M):
    id: str = Field(pattern=r"^[A-Za-z0-9_.-]+$")
    activity: str
    title: str
    title_vi: str = ""
    tag: str = ""
    subtitle: str = ""
    speakers: dict[str, Speaker]
    gap: float = Field(0.45, ge=0, le=3)
    scene_gap: float = Field(0.8, ge=0, le=5)
    scenes: list[Scene]

    @model_validator(mode="before")
    @classmethod
    def _lines(cls, data):
        """`- emma: "Hello"` → {"speaker": "emma", "text": "Hello"}."""
        if not isinstance(data, dict):
            return data
        known = set((data.get("speakers") or {}).keys())
        for sc in data.get("scenes") or []:
            out = []
            for ln in (sc.get("lines") or []) if isinstance(sc, dict) else []:
                if not isinstance(ln, dict):
                    raise ValueError(f"dòng thoại phải là bảng khóa–giá trị: {ln!r}")
                who = [k for k in ln if k not in LINE_FIELDS]
                if len(who) > 1:
                    raise ValueError(f"một dòng chỉ có một người nói: {who}")
                if who and who[0] not in known:
                    raise ValueError(f"người nói chưa khai báo trong speakers: {who[0]}")
                row = {k: v for k, v in ln.items() if k in LINE_FIELDS}
                if who:
                    row["speaker"], row["text"] = who[0], str(ln[who[0]])
                out.append(row)
            if isinstance(sc, dict):
                sc["lines"] = out
        return data

    @model_validator(mode="after")
    def _roles(self):
        for sc in self.scenes:
            for it in sc.items:
                for k in ("ask", "by"):
                    if k in it and it[k] not in self.speakers:
                        raise ValueError(f"`{k}: {it[k]}` không phải người nói đã khai báo")
        return self

    def chapters(self) -> list[tuple[int, str]]:
        return [(i, sc.chapter) for i, sc in enumerate(self.scenes) if sc.chapter]


def load(path: Path) -> Lesson:
    raw = yaml.safe_load(Path(path).read_text(encoding="utf-8"))
    try:
        return Lesson.model_validate(raw)
    except ValidationError as e:
        raise SystemExit(f"{path}: kịch bản không hợp lệ\n{e}") from None


def book_dir(path: Path) -> Path:
    """Kịch bản nằm ở books/<sách>/lessons/ → thư mục sách là cha của lessons/."""
    return Path(path).resolve().parent.parent


def find_item(book: dict, activity: str) -> Optional[dict]:
    for sec in book.get("sections", []):
        for it in sec.get("items", []):
            if any(a.get("id") == activity for a in it.get("activities", [])):
                return it
    return None


def check(lesson: Lesson, bdir: Path) -> list[str]:
    """Đối chiếu kịch bản với book.json của sách: hoạt động có thật, trang ảnh nằm trong file."""
    problems: list[str] = []
    bj = bdir / "book.json"
    if not bj.exists():
        return [f"không thấy {bj} — chạy agent nhập sách trước"]
    book = json.loads(bj.read_text(encoding="utf-8"))
    if not find_item(book, lesson.activity):
        problems.append(f"hoạt động {lesson.activity} không có trong book.json")
    for i, sc in enumerate(lesson.scenes):
        if not sc.image:
            continue
        f = book.get("files", {}).get(sc.image.pdf)
        if not f or f.get("kind") != "pdf":
            problems.append(f"cảnh {i}: không có file PDF '{sc.image.pdf}' trong book.json")
        elif sc.image.page > f.get("pages", 0):
            problems.append(f"cảnh {i}: trang {sc.image.page} vượt số trang của {sc.image.pdf}")
    return problems
