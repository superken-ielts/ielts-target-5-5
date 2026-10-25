"""Cảnh `jp` — thẻ ba tầng của video N5 (docs/agent-hoc-tap/07-lo-trinh-n5-tieng-nhat.md), nền navy:

    thanh đầu: nhãn cam (`tag` của bài) + tiêu đề cảnh (`heading`)
    tầng 1, thẻ trắng: người đang nói, chữ Nhật (`jp`, có furigana) và `romaji`
    tầng 2, thẻ xanh: giải thích / nghĩa tiếng Anh (`en`)
    tầng 3, thẻ xanh đậm viền cam: nghĩa tiếng Việt, ghi chú Hán-Việt (`vi`)

Chữ trộn Latin – Nhật vẽ bằng hai phông (Liberation Sans có dấu tiếng Việt; Noto Sans CJK JP hoặc IPAGothic
cho kana, chữ Hán), canh cùng đường chân chữ. Xuống dòng theo từ với chữ Latin, theo từng chữ với chữ Nhật,
không để dấu câu Nhật đứng đầu dòng; nhóm furigana `{漢字|かんじ}` không bị tách.
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import Optional

from PIL import Image, ImageDraw

from . import ja
from .slides import H, W, font

P = {
    "bg": "#0F2537", "bar": "#163853", "teal": "#00A8B5", "amber": "#F39C12", "card": "#FAFCFE",
    "en": "#173A56", "vi": "#132F46", "ink": "#0F2537", "romaji": "#008291", "white": "#F5F8FA",
    "gold": "#FFD773", "muted": "#A0B9CD", "ruby": "#3F6178", "track": "#24496A",
}
HEADER = (40, 27, W - 40, 83)
TIER1 = (40, 103, W - 40, 383)
TIER2 = (40, 403, W - 40, 537)
TIER3 = (40, 557, W - 40, 690)
X0, TEXT_W = 72, W - 40 - 72 - 30
NO_START = set("、。，．・：；？！ー）」』】〉》〕］｝)]}?!.,:;…‥～〜ぁぃぅぇぉっゃゅょゎァィゥェォッャュョヮ")
NO_END = set("（「『【〈《〔［｛([{")
LABEL_EN = "ENGLISH EXPLANATION / MEANING"
LABEL_VI = "NGHĨA TIẾNG VIỆT & GHI CHÚ HÁN-VIỆT"


def _f(cjk: bool, size: int, bold: bool):
    return font(("jp-bold" if bold else "jp") if cjk else ("bold" if bold else "regular"), size)


def _runs(s: str):
    """Chia chuỗi thành các đoạn liền nhau cùng loại chữ (Nhật / không phải Nhật)."""
    out: list[tuple[bool, str]] = []
    for ch in s:
        c = ja.is_cjk(ch)
        if out and out[-1][0] == c:
            out[-1] = (c, out[-1][1] + ch)
        else:
            out.append((c, ch))
    return out


def width(d: ImageDraw.ImageDraw, s: str, size: int, bold: bool = False) -> float:
    return sum(d.textlength(t, font=_f(c, size, bold)) for c, t in _runs(s))


def draw_mixed(d: ImageDraw.ImageDraw, x: float, baseline: float, s: str, size: int, fill: str, bold: bool = False) -> float:
    for c, t in _runs(s):
        f = _f(c, size, bold)
        d.text((x, baseline), t, font=f, fill=fill, anchor="ls")
        x += d.textlength(t, font=f)
    return x


@dataclass
class Unit:
    base: str
    ruby: Optional[str] = None
    space: bool = False
    w: float = 0.0
    bw: float = 0.0


def units(d, text: str, size: int, rsize: int, bold: bool) -> list[Unit]:
    out: list[Unit] = []
    for base, ruby in ja.segments(text):
        if ruby:
            out.append(Unit(base, ruby))
            continue
        word = ""
        for ch in base:
            if ch == " " or ja.is_cjk(ch):
                if word:
                    out.append(Unit(word))
                    word = ""
                if ch == " ":
                    if out and not out[-1].space:
                        out.append(Unit(" ", space=True))
                else:
                    out.append(Unit(ch))
            else:
                word += ch
        if word:
            out.append(Unit(word))
    for i, u in enumerate(out):
        u.bw = u.w = width(d, u.base, size, bold)
        if u.ruby:
            # furigana dài hơn chữ Hán được tràn sang chữ bên cạnh (không phải chữ có furigana) tối đa một chữ nhỏ
            # mỗi bên, để không giãn cách câu
            sides = sum(1 for j in (i - 1, i + 1) if 0 <= j < len(out) and not out[j].ruby and not out[j].space)
            extra = width(d, u.ruby, rsize) + 2 - u.bw
            u.w += max(0.0, extra - sides * 0.9 * rsize)
    return out


def _break(us: list[Unit], limit: float) -> list[list[Unit]]:
    lines: list[list[Unit]] = []
    cur: list[Unit] = []
    w = 0.0
    for u in us:
        if cur and w + u.w > limit and not u.space:
            nxt: list[Unit] = []
            # cấm đầu dòng: dấu câu, chữ nhỏ → kéo chữ trước theo xuống dòng sau
            while u.base[0] in NO_START and len(cur) > 1 and not cur[-1].space:
                nxt.insert(0, cur.pop())
                if nxt[0].base[0] not in NO_START:
                    break
            # cấm cuối dòng: mở ngoặc
            while len(cur) > 1 and cur[-1].base[-1] in NO_END:
                nxt.insert(0, cur.pop())
            while cur and cur[-1].space:
                cur.pop()
            lines.append(cur)
            cur, w = nxt, sum(x.w for x in nxt)
        if u.space and not cur:
            continue
        cur.append(u)
        w += u.w
    while cur and cur[-1].space:
        cur.pop()
    if cur:
        lines.append(cur)
    return lines


@dataclass
class Block:
    lines: list[list[Unit]]
    size: int
    rsize: int
    bold: bool
    ruby: bool

    @property
    def band(self) -> int:
        return self.rsize + 4 if self.ruby else 0

    @property
    def step(self) -> int:
        return int(self.size * 1.24) + self.band

    @property
    def height(self) -> int:
        return self.step * len(self.lines)


def layout(d, text: str, size: int, limit: float, bold: bool = False) -> Block:
    rsize = max(13, round(size * 0.48))
    us = units(d, text, size, rsize, bold)
    return Block(_break(us, limit), size, rsize, bold, any(u.ruby for u in us))


def fit(d, text: str, sizes: range, limit: float, max_h: float, max_lines: int = 99, bold: bool = False) -> Block:
    """Cỡ chữ lớn nhất trong `sizes` để đoạn văn vừa chiều cao `max_h` và tối đa `max_lines` dòng."""
    b = None
    for size in sizes:
        b = layout(d, text, size, limit, bold)
        if b.height <= max_h and len(b.lines) <= max_lines:
            return b
    return b


def paint(d, b: Block, x: float, y: float, fill: str, ruby_fill: str) -> float:
    for k, line in enumerate(b.lines):
        top = y + k * b.step
        base = top + b.band + round(b.size * 0.92)
        cx = x
        for u in line:
            bx = cx + (u.w - u.bw) / 2
            draw_mixed(d, bx, base, u.base, b.size, fill, b.bold)
            if u.ruby:
                rw = width(d, u.ruby, b.rsize)
                draw_mixed(d, cx + (u.w - rw) / 2, top + round(b.rsize * 0.95), u.ruby, b.rsize, ruby_fill)
            cx += u.w
    return y + b.height


def _tier(d, box, fill, outline, bar, label, text, ink):
    x0, y0, x1, y1 = box
    d.rounded_rectangle(box, 13, fill=fill, outline=outline, width=2)
    d.rounded_rectangle((x0, y0, x0 + 12, y1), 8, fill=bar)
    d.text((X0, y0 + 13), label, font=font("bold", 16), fill=bar)
    if text:
        b = fit(d, text, range(23, 15, -1), TEXT_W, y1 - y0 - 50, 3)
        paint(d, b, X0, y0 + 40, ink, ink)


def render(slides, fr, progress: float) -> Image.Image:
    lesson = slides.L
    sc = lesson.scenes[fr.scene]
    it = sc.items[fr.focus or 0]
    img = Image.new("RGB", (W, H), P["bg"])
    d = ImageDraw.Draw(img)

    # thanh đầu: nhãn cam + tiêu đề cảnh
    d.rounded_rectangle(HEADER, 11, fill=P["bar"])
    tag = lesson.tag or "JLPT N5"
    ft = font("bold", 17)
    tw = d.textlength(tag, font=ft) + 30
    d.rounded_rectangle((53, 37, 53 + tw, 73), 7, fill=P["amber"])
    d.text((53 + tw / 2, 55), tag, font=ft, fill=P["bg"], anchor="mm")
    title = sc.heading or lesson.subtitle or lesson.title
    hx = 53 + tw + 20
    size = 23
    while size > 15 and width(d, title, size) > HEADER[2] - 16 - hx:
        size -= 1
    draw_mixed(d, hx, 55 + round(size * 0.36), title, size, P["white"])

    # tầng 1: người đang nói, chữ Nhật có furigana, romaji
    x0, y0, x1, y1 = TIER1
    d.rounded_rectangle(TIER1, 16, fill=P["card"], outline=P["teal"], width=3)
    sp = lesson.speakers.get(fr.speaker or "")
    if sp:
        chip = ("JP · " if sp.lang == "ja" else "EN · ") + sp.name.upper() + (" — " + sp.role.upper() if sp.role else "")
        fb = font("bold", 16)
        bw = d.textlength(chip, font=fb) + 28
        d.rounded_rectangle((63, y0 + 17, 63 + bw, y0 + 48), 8, fill=sp.color)
        d.text((63 + 14, y0 + 33), chip, font=fb, fill="#FFFFFF", anchor="lm")
    top, bottom = y0 + 62, y1 - 16
    rom = str(it.get("romaji") or "")
    rb = fit(d, rom, range(22, 15, -1), TEXT_W, 90, 3) if rom else None
    gap = 12 if rb else 0
    room = bottom - top - (rb.height + gap if rb else 0)
    jb = fit(d, str(it["jp"]), range(46, 21, -1), TEXT_W, room)
    y = top + max(0, (room - jb.height) / 2)
    y = paint(d, jb, X0, y, P["ink"], P["ruby"])
    if rb:
        paint(d, rb, X0, max(y + gap, bottom - rb.height), P["romaji"], P["romaji"])

    # tầng 2, 3: tiếng Anh, tiếng Việt
    _tier(d, TIER2, P["en"], P["teal"], P["teal"], LABEL_EN, str(it.get("en") or ""), P["white"])
    _tier(d, TIER3, P["vi"], P["amber"], P["amber"], LABEL_VI, str(it.get("vi") or ""), P["gold"])

    # thanh tiến độ
    d.rounded_rectangle((40, 703, W - 40, 707), 2, fill=P["track"])
    if progress > 0:
        d.rounded_rectangle((40, 703, 40 + max(4, (W - 80) * min(progress, 1)), 707), 2, fill=P["amber"])
    return img
