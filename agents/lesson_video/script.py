"""Kịch bản bài giảng: đọc file YAML, kiểm tra, chuẩn hóa câu thoại.

Mỗi cảnh (scene) là một kiểu slide; mỗi dòng trong `lines` là một câu thoại của một người nói
(khóa là mã người nói, ví dụ `emma: "Hello"`) hoặc một khoảng lặng có đếm ngược (`wait: 8`) để người
học tự nói. `focus` chọn mục đang nói tới, `reveal` mở dần đáp án; cả hai giữ nguyên tới dòng sau.

Người nói `lang: ja` đọc tiếng Nhật (giọng Kokoro jf_*, jm_*). Chữ Nhật hiển thị viết furigana ngay trong câu:
`{留学生|りゅうがくせい}` (xem ja.py); `check` so cách bộ đọc đọc câu thoại với furigana.
"""
from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Literal, Optional, Union

import yaml
from pydantic import BaseModel, ConfigDict, Field, ValidationError, field_validator, model_validator

from . import ja

Kind = Literal["title", "bullets", "vocab", "match", "pairs", "qa", "compare", "errors", "practice",
               "order", "timing", "letter", "blanks", "mcq", "passage", "shadow", "jp"]

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
    "order": ("k", "text", "pos"),      # sắp xếp: mỗi mục có vị trí đúng `pos`
    "timing": ("label", "minutes"),     # chia thời gian: thanh ngang theo số phút
    "letter": ("text",),                # thư mẫu: mỗi mục một đoạn; `note` ghi chú lề, `body: false` không đếm từ
    "blanks": ("n", "answer"),          # ô trống số n, mở ra thì hiện `answer` (+ `tip`); có `q` chứa ___ thì là câu điền từ, `hint` = từ gốc
    "mcq": ("n", "q", "options", "answer"),  # trắc nghiệm: `options` là danh sách, `answer` là a, b, c… hoặc một nhãn trong `keys`
    "passage": ("text",),               # bài đọc trên màn hình (có phụ đề): mỗi mục một đoạn, `label` đầu đoạn; dòng thoại `mark` tô từ khóa
    "shadow": ("text",),                # nghe – nhắc lại: mỗi mục một câu mẫu chữ to; `by` người nói (màu), `vi` nghĩa, `tip` mẹo phát âm
    "jp": ("jp",),                      # thẻ ba tầng (video N5): `jp` chữ Nhật có furigana, `romaji`, `en` giải thích, `vi` nghĩa;
                                        # "\n" trong `jp` / `romaji` là xuống dòng bắt buộc (bảng chữ: mỗi hàng một dòng);
                                        # nhiều thẻ thì dòng thoại chọn thẻ đang hiện bằng `focus`; `quiz: true` = thẻ đố
                                        # nghe / đọc (câu Nhật đọc lên nhưng chưa hiện chữ, hoặc chữ Hán chưa có furigana; không đối chiếu)
}
# `read: <người nói>` (chỉ trong cảnh letter): người đó đọc nguyên đoạn `focus` của thư
# `echo: true` (câu thoại): sau câu là khoảng lặng đếm ngược dài theo câu để người học nhắc lại (shadowing)
# `speed` (câu thoại): tốc độ đọc riêng của câu này (mặc định: `speed` của người nói, rồi tới --speed của lệnh build)
LINE_FIELDS = {"say", "vi", "focus", "reveal", "wait", "pause", "note", "read", "mark", "track", "start", "end", "echo",
               "speed"}


class _M(BaseModel):
    model_config = ConfigDict(extra="forbid")


class Speaker(_M):
    name: str
    role: str = ""
    voice: Union[str, dict[str, str]]   # một giọng, hoặc giọng theo bộ đọc: {kokoro: bf_emma, flite: slt}
    color: str = "#C8102E"
    lang: Literal["en", "ja"] = "en"    # ja: đọc tiếng Nhật (giọng Kokoro jf_*, jm_*)
    speed: Optional[float] = Field(None, ge=0.5, le=2.0)  # tốc độ riêng của người nói (mặc định --speed của lệnh build)

    @field_validator("voice")
    @classmethod
    def _voice(cls, v):
        if not v:
            raise ValueError("thiếu giọng đọc")
        return v

    def voice_for(self, engine: str) -> str:
        if isinstance(self.voice, str):
            return self.voice
        if engine in self.voice:
            return self.voice[engine]
        if engine == "silent":
            return next(iter(self.voice.values()))
        raise ValueError(f"{self.name}: chưa khai báo giọng cho bộ đọc {engine} (có: {', '.join(self.voice)})")

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
    grid: int = Field(1, ge=1, le=6)  # dải ảnh nằm ngang gồm `grid` tranh bằng nhau → xếp lại thành 2 hàng cho to hơn


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
    mark: list[str] = []  # cảnh passage: cụm từ tô vàng trong đoạn `focus` (giữ tới khi đổi đoạn)
    track: str = ""       # phát file nghe của sách (mã file audio trong book.json), từ giây `start` tới `end`
    start: float = Field(0, ge=0)
    end: Optional[float] = None
    echo: bool = False    # câu thoại: thêm khoảng lặng đếm ngược (dài theo câu) để người học nhắc lại
    speed: Optional[float] = Field(None, ge=0.5, le=2.0)

    @field_validator("reveal", "mark", mode="before")
    @classmethod
    def _list(cls, v):
        if v is None:
            return []
        return [str(x) for x in (v if isinstance(v, list) else [v])]

    @model_validator(mode="after")
    def _kind(self):
        if sum(map(bool, (self.speaker, self.wait, self.track))) != 1:
            raise ValueError("mỗi dòng là một câu thoại (khóa = mã người nói), một khoảng lặng `wait` hoặc một đoạn nghe `track`")
        if (self.start or self.end is not None) and not self.track:
            raise ValueError("`start` / `end` chỉ dùng với `track`")
        if self.end is not None and self.end <= self.start:
            raise ValueError(f"đoạn nghe {self.track}: `end` phải lớn hơn `start`")
        if self.speaker and not self.text.strip():
            raise ValueError(f"câu thoại của {self.speaker} trống")
        if self.echo and not self.speaker:
            raise ValueError("`echo` (chừa chỗ nhắc lại) chỉ dùng cho câu thoại")
        if self.speed is not None and not self.speaker:
            raise ValueError("`speed` chỉ dùng cho câu thoại")
        return self

    @property
    def spoken(self) -> str:
        return self.say or self.text


def mcq_keys(it: dict) -> list[str]:
    """Nhãn phương án của một câu trắc nghiệm: `keys` nếu có (ví dụ [1, 2, 3]), không thì a, b, c…"""
    if it.get("keys"):
        return [str(k) for k in it["keys"]]
    return [chr(97 + i) for i in range(len(it["options"]))]


class Scene(_M):
    kind: Kind
    chapter: str = ""
    heading: str = ""
    heading_vi: str = ""
    items: list[dict] = []
    options: list[dict] = []
    image: Optional[ImageRef] = None
    hide_text: bool = False   # bài nghe: thanh phụ đề chỉ hiện người nói, ẩn lời (không lộ đáp án)
    roles: dict[str, str] = {}  # vai trong cảnh này, ví dụ {emma: receptionist} khi đóng bài nghe
    words: Optional[int] = None  # letter chia hai trang: số từ của cả lá thư (mặc định đếm các đoạn trong cảnh)
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
        if self.kind == "order" and sorted(int(it["pos"]) for it in self.items) != list(range(1, len(self.items) + 1)):
            raise ValueError("cảnh order: `pos` phải là 1…n, mỗi số một lần")
        if self.kind == "mcq":
            for it in self.items:
                letters = mcq_keys(it)
                if len(letters) != len(it["options"]):
                    raise ValueError(f"cảnh mcq: câu {it['n']} có {len(it['options'])} phương án nhưng {len(letters)} nhãn `keys`")
                if str(it["answer"]) not in letters:
                    raise ValueError(f"cảnh mcq: đáp án '{it['answer']}' của câu {it['n']} không thuộc {letters}")
        if self.kind != "passage" and any(ln.mark for ln in self.lines):
            raise ValueError("`mark` (tô từ khóa) chỉ dùng trong cảnh passage")
        if self.kind == "letter" and any(ln.wait or ln.echo for ln in self.lines):
            raise ValueError("cảnh letter không có khoảng lặng `wait` / `echo` (không có chỗ hiện đếm ngược)")
        if self.kind == "jp":
            if any(ln.wait or ln.echo for ln in self.lines):
                raise ValueError("cảnh jp không có khoảng lặng `wait` / `echo` — dùng `pause`")
            for k, it in enumerate(self.items):
                if it.get("quiz"):  # thẻ đố: được để chữ Hán không furigana (bài đọc giá tiền, chữ Hán)
                    continue
                bad = ja.check_markup(str(it["jp"]))
                if bad:
                    raise ValueError("cảnh jp" + (f", thẻ {k}" if len(self.items) > 1 else "") + ": " + "; ".join(bad))
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
        if self.kind in ("match", "pairs", "blanks", "mcq"):
            return {str(it["n"]) for it in self.items}
        if self.kind == "order":
            return {str(it["k"]) for it in self.items}
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
        data = dict(data)  # không sửa dữ liệu của người gọi
        known = set((data.get("speakers") or {}).keys())
        scenes = []
        for sc in data.get("scenes") or []:
            if not isinstance(sc, dict):
                scenes.append(sc)
                continue
            sc, out = dict(sc), []
            for ln in sc.get("lines") or []:
                if not isinstance(ln, dict):
                    raise ValueError(f"dòng thoại phải là bảng khóa–giá trị: {ln!r}")
                if "speaker" in ln or "text" in ln:  # đã ở dạng chuẩn (ví dụ từ model_dump)
                    out.append(dict(ln))
                    continue
                if "read" in ln:  # đọc nguyên một đoạn thư: chữ và cách đọc lấy từ mục `focus`
                    items = sc.get("items") or []
                    i = ln.get("focus")
                    if sc.get("kind") != "letter" or not isinstance(i, int) or not 0 <= i < len(items):
                        raise ValueError(f"`read` chỉ dùng trong cảnh letter, kèm `focus` là số thứ tự đoạn: {ln!r}")
                    if ln["read"] not in known:
                        raise ValueError(f"người nói chưa khai báo trong speakers: {ln['read']}")
                    row = {k: v for k, v in ln.items() if k in LINE_FIELDS and k != "read"}
                    row["speaker"], row["text"] = ln["read"], str(items[i]["text"])
                    if items[i].get("say") and "say" not in row:
                        row["say"] = str(items[i]["say"])
                    out.append(row)
                    continue
                who = [k for k in ln if k not in LINE_FIELDS]
                if len(who) > 1:
                    raise ValueError(f"một dòng chỉ có một người nói: {who}")
                if who and who[0] not in known:
                    raise ValueError(f"người nói chưa khai báo trong speakers: {who[0]}")
                row = {k: v for k, v in ln.items() if k in LINE_FIELDS}
                if who:
                    row["speaker"], row["text"] = who[0], str(ln[who[0]])
                out.append(row)
            sc["lines"] = out
            scenes.append(sc)
        if "scenes" in data:
            data["scenes"] = scenes
        return data

    @model_validator(mode="after")
    def _roles(self):
        for key, sp in self.speakers.items():
            if sp.lang != "ja":
                continue
            for v in ([sp.voice] if isinstance(sp.voice, str) else list(sp.voice.values())):
                if not v.startswith(("jf_", "jm_")):
                    raise ValueError(f"{sp.name} đọc tiếng Nhật (lang: ja) nhưng giọng '{v}' không phải giọng Nhật jf_*, jm_*")
        for sc in self.scenes:
            for ln in sc.lines:
                sp = self.speakers.get(ln.speaker or "")
                if sp and sp.lang == "ja" and re.search(r"[A-Za-z0-9]", ln.spoken):
                    raise ValueError(f"câu tiếng Nhật của {sp.name} có chữ Latin hoặc chữ số: {ln.spoken!r}"
                                     " — viết cách đọc bằng kana (ví dụ IT → アイティー) trong `say`")
            bad = [k for k in sc.roles if k not in self.speakers]
            if bad:
                raise ValueError(f"`roles` có người nói chưa khai báo: {', '.join(bad)}")
            for it in sc.items:
                for k in ("ask", "by"):
                    if k in it and it[k] not in self.speakers:
                        raise ValueError(f"`{k}: {it[k]}` không phải người nói đã khai báo")
            if sc.kind == "qa":  # thẻ trả lời ghi tên `by` (mặc định người nói cuối trong speakers): phải khớp người đọc
                last = list(self.speakers)[-1]
                for ln in sc.lines:
                    for r in ln.reveal:
                        by = sc.items[int(r)].get("by") or last
                        if ln.speaker and ln.speaker != by:
                            raise ValueError(f"cảnh qa: câu trả lời mục {r} do {ln.speaker} đọc nhưng thẻ ghi {by}"
                                             f" — thêm `by: {ln.speaker}` (và `ask`) cho mục đó")
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


def check_japanese(lesson: Lesson) -> list[str]:
    """Cảnh jp có câu thoại tiếng Nhật: bộ đọc phải đọc đúng như furigana, romaji khớp cách đọc (cần misaki).

    Mỗi thẻ so với các câu tiếng Nhật đọc lúc thẻ đó đang hiện (`focus`): mỗi câu đọc trọn thẻ (đọc lại nhiều lần
    cũng được), hoặc các câu ghép lại thành thẻ."""
    problems: list[str] = []
    for i, sc in enumerate(lesson.scenes):
        if sc.kind != "jp":
            continue
        by_card: dict[int, list[str]] = {}
        focus = 0
        for ln in sc.lines:
            if ln.focus is not None:
                focus = ln.focus
            if ln.speaker and lesson.speakers[ln.speaker].lang == "ja":
                by_card.setdefault(focus, []).append(ln.spoken)
        for k, spoken in by_card.items():
            it = sc.items[k]
            if it.get("quiz"):  # thẻ đố nghe: chữ chưa hiện, thẻ đáp án ngay sau đọc lại câu đó và được đối chiếu
                continue
            where = f"cảnh {i}" + (f", thẻ {k}" if len(sc.items) > 1 else "")
            text, romaji = str(it["jp"]), str(it.get("romaji") or "")
            try:
                if len(spoken) > 1 and not any(ja.check_line(text, s, romaji) for s in spoken):
                    continue
                problems += [f"{where}: {m}" for m in ja.check_line(text, "".join(spoken), romaji)]
            except ja.JaError as e:
                return [str(e)]
    return problems


def check(lesson: Lesson, bdir: Path) -> list[str]:
    """Đối chiếu kịch bản với book.json của sách: hoạt động có thật, trang ảnh nằm trong file; câu tiếng Nhật
    đọc đúng furigana."""
    problems: list[str] = check_japanese(lesson)
    bj = bdir / "book.json"
    if not bj.exists():
        return [f"không thấy {bj} — chạy agent nhập sách trước"]
    book = json.loads(bj.read_text(encoding="utf-8"))
    if not find_item(book, lesson.activity):
        problems.append(f"hoạt động {lesson.activity} không có trong book.json")
    for i, sc in enumerate(lesson.scenes):
        for ln in sc.lines:
            if not ln.track:
                continue
            f = book.get("files", {}).get(ln.track)
            if not f or f.get("kind") != "audio":
                problems.append(f"cảnh {i}: không có file nghe '{ln.track}' trong book.json")
            elif not (bdir / f["path"]).exists():
                problems.append(f"cảnh {i}: thiếu file {f['path']}")
            elif ln.end is not None and f.get("durationSec") and ln.end > f["durationSec"] + 0.5:
                problems.append(f"cảnh {i}: {ln.track} chỉ dài {f['durationSec']:.1f} giây (end = {ln.end})")
        if not sc.image:
            continue
        f = book.get("files", {}).get(sc.image.pdf)
        if not f or f.get("kind") != "pdf":
            problems.append(f"cảnh {i}: không có file PDF '{sc.image.pdf}' trong book.json")
        elif sc.image.page > f.get("pages", 0):
            problems.append(f"cảnh {i}: trang {sc.image.page} vượt số trang của {sc.image.pdf}")
    return problems
