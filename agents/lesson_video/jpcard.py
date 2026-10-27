"""Cảnh `jp` — thẻ ba tầng của video N5 (docs/agent-hoc-tap/07-lo-trinh-n5-tieng-nhat.md), nền navy:

    thanh đầu: nhãn cam (`tag` của bài) + tiêu đề cảnh (`heading`), cảnh nhiều thẻ thì thêm "thẻ k/n"
    tầng 1, thẻ trắng: người đang nói (hoặc nhãn file nghe của sách đang phát), chữ Nhật (`jp`, có furigana) và `romaji`;
            chữ đang được đọc tô nền cam, chữ vừa đọc xong trong câu tô nền xanh nhạt (dòng `hl` / `step` của kịch bản)
    tầng 2, thẻ xanh: đúng câu đang nói — lời người nói tiếng Anh, hoặc nghĩa tiếng Anh của câu tiếng Nhật / file nghe
    tầng 3, thẻ xanh đậm viền cam: tiếng Việt của câu đó; câu không có thì hai tầng hiện `en`, `vi` của thẻ

Chữ trộn Latin – Nhật vẽ bằng hai phông (Liberation Sans có dấu tiếng Việt; Noto Sans CJK JP hoặc IPAGothic
cho kana, chữ Hán), canh cùng đường chân chữ. Xuống dòng theo từ với chữ Latin, theo từng chữ với chữ Nhật,
không để dấu câu Nhật đứng đầu dòng; nhóm furigana `{漢字|かんじ}` không bị tách.
"""
from __future__ import annotations

import re
from dataclasses import dataclass
from typing import Optional

from PIL import Image, ImageDraw

from . import ja
from .slides import H, W, font

P = {
    "bg": "#0F2537", "bar": "#163853", "teal": "#00A8B5", "amber": "#F39C12", "card": "#FAFCFE",
    "en": "#173A56", "vi": "#132F46", "ink": "#0F2537", "romaji": "#008291", "white": "#F5F8FA",
    "gold": "#FFD773", "muted": "#A0B9CD", "ruby": "#3F6178", "track": "#24496A",
    "now": "#FFD98E", "done": "#D6EEF1",   # nền chữ đang đọc / vừa đọc xong
}
HEADER = (40, 27, W - 40, 83)
TIER1 = (40, 103, W - 40, 383)
TIER2 = (40, 403, W - 40, 537)
TIER3 = (40, 557, W - 40, 690)
X0, TEXT_W = 72, W - 40 - 72 - 30
JP_SIZES = range(60, 21, -1)     # chữ Nhật trên thẻ: thẻ ngắn (một hàng chữ cái) chữ to để nhìn rõ nét
TIER_SIZES = range(26, 15, -1)   # chữ tầng 2, 3
NO_START = set("、。，．・：；？！ー）」』】〉》〕］｝)]}?!.,:;…‥～〜ぁぃぅぇぉっゃゅょゎァィゥェォッャュョヮ")
NO_END = set("（「『【〈《〔［｛([{")
SEPARATORS = ("|", "/", "—", "vs.", "・")
STRONG = ("|", "/", "・")                 # vạch ngăn giữa các nhóm: ngắt ở đây trước "—" (nối hai vế một cặp)
LABEL = re.compile(r"^Q?\d+\.$")         # số thứ tự "5." / "Q2." đi cùng phần sau, không đứng cuối dòng


def _kata(ch: str) -> bool:
    return 0x30A1 <= ord(ch) <= 0x30FA or ch == "ー"
LABEL_EN = "ENGLISH EXPLANATION / MEANING"
LABEL_VI = "NGHĨA TIẾNG VIỆT & GHI CHÚ HÁN-VIỆT"


def captions(lesson, it: dict, speaker: Optional[str], text: str, en: str, vi: str, note: str,
             waiting: bool) -> tuple[tuple[str, str], tuple[str, str]]:
    """(nhãn, chữ) của tầng 2 và tầng 3 cho câu đang nói: người nói tiếng Anh → đúng lời của họ và bản dịch; câu
    tiếng Nhật / file nghe → nghĩa tiếng Anh, tiếng Việt của câu; đếm ngược → việc người học cần làm. Câu không có
    chữ cho tầng nào thì tầng đó hiện `en` / `vi` của thẻ với nhãn chung (thẻ đố không lộ đáp án)."""
    sp = lesson.speakers.get(speaker or "")
    if waiting:
        a, b = (note or en, "YOUR TURN"), (vi, "LƯỢT CỦA BẠN")
    elif sp and sp.lang != "ja":
        a, b = (text, f"{sp.name.upper()} SAYS"), (vi, f"DỊCH LỜI {sp.name.upper()}")
    else:
        a, b = (en, "ENGLISH"), (vi, "TIẾNG VIỆT")
    t2 = (a[1], a[0]) if a[0] else (LABEL_EN, str(it.get("en") or ""))
    t3 = (b[1], b[0]) if b[0] else (LABEL_VI, str(it.get("vi") or ""))
    return t2, t3


def card_captions(lesson, sc, focus: int) -> tuple[list[str], list[str]]:
    """Mọi chữ tầng 2, tầng 3 hiện cùng một thẻ trong cảnh: để chia chiều cao các tầng một lần cho cả thẻ."""
    it = sc.items[focus]
    t2, t3 = [str(it.get("en") or "")], [str(it.get("vi") or "")]
    f = 0
    for ln in sc.lines:
        f = ln.focus if ln.focus is not None else f
        if f == focus:
            a, b = captions(lesson, it, ln.speaker, ln.text, ln.en, ln.vi, ln.note, not (ln.speaker or ln.track))
            t2.append(a[1])
            t3.append(b[1])
    return t2, t3


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
    tok: Optional[int] = None  # số thứ tự chữ / từ trên thẻ (ja.card_tokens; romaji: ja.romaji_tokens), để tô sáng


def units(d, text: str, size: int, rsize: int, bold: bool, seps=ja.SEP, tok: int = 0) -> tuple[list[Unit], int]:
    """Các mảnh không cắt được khi xuống dòng, kèm số thứ tự chữ trên thẻ của mỗi mảnh (`seps`: ký tự ngăn hai chữ,
    `tok`: số thứ tự chữ đầu tiên). Trả về (các mảnh, số thứ tự chữ kế tiếp)."""
    out: list[Unit] = []
    open_ = False

    def mark(ch: str) -> Optional[int]:
        nonlocal tok, open_
        if ch in seps:
            if open_:
                tok, open_ = tok + 1, False
            return None
        if ch.isspace():
            return None
        open_ = True
        return tok

    for base, ruby in ja.segments(text):
        if ruby:
            open_ = True
            out.append(Unit(base, ruby, tok=tok))
            continue
        word, wtok = "", None
        for ch in base:
            t = mark(ch)
            if ch == " " or ja.is_cjk(ch):
                if word:
                    out.append(Unit(word, tok=wtok))
                    word, wtok = "", None
                if ch == " ":
                    if out and not out[-1].space:
                        out.append(Unit(" ", space=True))
                elif _kata(ch) and out and not out[-1].ruby and out[-1].base and _kata(out[-1].base[-1]):
                    out[-1].base += ch  # từ katakana (カフェ, コーヒー) không bị cắt đôi khi xuống dòng
                else:
                    out.append(Unit(ch, tok=t))
            else:
                wtok = t if wtok is None else wtok
                word += ch
        if word:
            out.append(Unit(word, tok=wtok))
    for i, u in enumerate(out):
        u.bw = u.w = width(d, u.base, size, bold)
        if u.ruby:
            # furigana dài hơn chữ Hán được tràn sang chữ bên cạnh (không phải chữ có furigana) tối đa một chữ nhỏ
            # mỗi bên, để không giãn cách câu
            sides = sum(1 for j in (i - 1, i + 1) if 0 <= j < len(out) and not out[j].ruby and not out[j].space)
            extra = width(d, u.ruby, rsize) + 2 - u.bw
            u.w += max(0.0, extra - sides * 0.9 * rsize)
    return out, tok + open_


def _break(us: list[Unit], limit: float) -> list[list[Unit]]:
    lines: list[list[Unit]] = []
    cur: list[Unit] = []
    w = 0.0
    for u in us:
        if cur and w + u.w > limit and not u.space:
            nxt: list[Unit] = []
            # câu có dấu cách (mẫu câu, câu tách cụm): ngắt ở vạch ngăn | / ・ rồi mới tới —, không thì ở dấu
            # cách cuối, thay vì cắt giữa một từ; đoạn văn Nhật liền chữ thì ngắt ở bất kỳ chữ nào
            spaces = [k for k, x in enumerate(cur) if x.space and k and not LABEL.match(cur[k - 1].base)]
            seps = ([k for k in spaces if cur[k - 1].base in STRONG]
                    or [k for k in spaces if cur[k - 1].base in SEPARATORS])
            k = (seps or spaces or [None])[-1]
            if k is not None and (seps or sum(x.w for x in cur[k + 1:]) <= 0.5 * limit):
                nxt, cur = cur[k + 1:], cur[:k]
                while cur and (cur[-1].space or cur[-1].base in SEPARATORS):  # vạch ngăn cuối dòng là thừa
                    cur.pop()
                lines.append(cur)
                cur, w = nxt, sum(x.w for x in nxt)
                cur.append(u)
                w += u.w
                continue
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


def layout(d, text: str, size: int, limit: float, bold: bool = False, seps=ja.SEP) -> Block:
    """`\n` trong chữ là xuống dòng bắt buộc (bảng chữ cái: mỗi hàng một dòng); mỗi đoạn tự ngắt dòng như thường."""
    rsize = max(13, round(size * 0.48))
    lines: list[list[Unit]] = []
    ruby = False
    tok = 0
    for para in text.split("\n"):
        us, tok = units(d, para, size, rsize, bold, seps, tok)
        lines += _break(us, limit) or [[]]
        ruby = ruby or any(u.ruby for u in us)
    return Block(lines, size, rsize, bold, ruby)


def fit(d, text: str, sizes: range, limit: float, max_h: float, max_lines: int = 99, bold: bool = False,
        seps=ja.SEP) -> Block:
    """Cỡ chữ lớn nhất trong `sizes` để đoạn văn vừa chiều cao `max_h` và tối đa `max_lines` dòng. Dòng cuối chỉ còn
    vài chữ (dưới 1/4 dòng) thì nhỏ chữ thêm tối đa 6px nếu nhờ đó bớt được một dòng."""
    b = None
    for size in sizes:
        b = layout(d, text, size, limit, bold, seps)
        if b.height <= max_h and len(b.lines) <= max_lines:
            break
    else:
        return b
    if len(b.lines) > 1 and sum(u.w for u in b.lines[-1]) < 0.25 * limit:
        for size in range(b.size - 1, max(b.size - 7, sizes.stop), -1):
            c = layout(d, text, size, limit, bold, seps)
            if len(c.lines) < len(b.lines):
                return c
    return b


def _highlight(d, line: list[Unit], x: float, top: float, base: float, b: Block, now: set, done: set):
    """Nền sau chữ đang đọc (cam nhạt, gạch chân cam) và chữ vừa đọc xong (xanh nhạt); mỗi chữ một khối liền."""
    runs: list[list] = []  # [x0, x1, trạng thái, số thứ tự chữ]
    cx = x
    for i, u in enumerate(line):
        st = None if u.tok is None else "now" if u.tok in now else "done" if u.tok in done else None
        if u.space:  # dấu cách nằm giữa hai mảnh của cùng một chữ (romaji "ka ki") thì tô liền
            nxt = next((v for v in line[i + 1:] if not v.space), None)
            if runs and nxt is not None and runs[-1][3] == nxt.tok and abs(runs[-1][1] - cx) < 0.5:
                runs[-1][1] = cx + u.w
        elif st:
            if runs and runs[-1][2:] == [st, u.tok] and abs(runs[-1][1] - cx) < 0.5:
                runs[-1][1] = cx + u.w
            else:
                runs.append([cx, cx + u.w, st, u.tok])
        cx += u.w
    y0 = top - 2 if b.ruby else base - b.size * 0.98
    y1 = base + b.size * 0.24
    for x0, x1, st, _ in runs:
        d.rounded_rectangle((x0 - 5, y0, x1 + 5, y1), 7, fill=P[st])
        if st == "now":
            d.rounded_rectangle((x0 - 5, y1 - 4, x1 + 5, y1), 2, fill=P["amber"])


def paint(d, b: Block, x: float, y: float, fill: str, ruby_fill: str, now=(), done=()) -> float:
    """Vẽ khối chữ từ (x, y); `now` / `done`: số thứ tự các chữ đang đọc / vừa đọc xong (tô nền)."""
    now, done = set(now), set(done)
    for k, line in enumerate(b.lines):
        top = y + k * b.step
        base = top + b.band + round(b.size * 0.92)
        if now or done:
            _highlight(d, line, x, top, base, b, now, done)
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
        b = fit(d, text, TIER_SIZES, TEXT_W, y1 - y0 - 50, 3)
        paint(d, b, X0, y0 + 40, ink, ink)


def _tier_height(d, text: str) -> int:
    """Chiều cao vừa đủ của tầng 2 / 3 (nhãn + đoạn văn), không thấp hơn 96 và không cao hơn bản thiết kế."""
    b = fit(d, text, TIER_SIZES, TEXT_W, TIER2[3] - TIER2[1] - 50, 3) if text else None
    return max(96, min(TIER2[3] - TIER2[1], 40 + (b.height if b else 0) + 12))


def tiers(d, it: dict, en: Optional[list[str]] = None, vi: Optional[list[str]] = None):
    """Ba tầng theo bản thiết kế; đoạn văn Nhật dài (chữ nhỏ hơn 30px) thì tầng 2, 3 co vừa chữ dài nhất sẽ hiện ở
    tầng đó (`en`, `vi`: mọi chữ của tầng trong lúc thẻ hiện; mặc định chữ của thẻ) để tầng 1 cao hơn.
    Trả về (tầng 1, tầng 2, tầng 3, khối chữ Nhật, khối romaji)."""
    rom, jp = str(it.get("romaji") or ""), str(it["jp"])

    def blocks(t1):
        top, bottom = t1[1] + 62, t1[3] - 16
        rb = fit(d, rom, range(22, 15, -1), TEXT_W, 90, 3, seps=ja.romaji_seps(rom)) if rom else None
        room = bottom - top - (rb.height + 12 if rb else 0)
        return fit(d, jp, JP_SIZES, TEXT_W, room), rb

    jb, rb = blocks(TIER1)
    if jb.size >= 30 or len(jb.lines) < 2:
        return TIER1, TIER2, TIER3, jb, rb
    h3 = max(_tier_height(d, t) for t in (vi or [str(it.get("vi") or "")]))
    h2 = max(_tier_height(d, t) for t in (en or [str(it.get("en") or "")]))
    t3 = (TIER3[0], TIER3[3] - h3, TIER3[2], TIER3[3])
    t2 = (TIER2[0], t3[1] - 20 - h2, TIER2[2], t3[1] - 20)
    t1 = (TIER1[0], TIER1[1], TIER1[2], t2[1] - 20)
    jb2, rb2 = blocks(t1)
    return (t1, t2, t3, jb2, rb2) if jb2.size > jb.size else (TIER1, TIER2, TIER3, jb, rb)


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
    right = HEADER[2] - 16
    if len(sc.items) > 1:  # cảnh nhiều thẻ: đang ở thẻ thứ mấy
        count = f"{(fr.focus or 0) + 1}/{len(sc.items)}"
        fc = font("bold", 18)
        d.text((right, 55), count, font=fc, fill=P["muted"], anchor="rm")
        right -= d.textlength(count, font=fc) + 18
    size = 23
    while size > 15 and width(d, title, size) > right - hx:
        size -= 1
    draw_mixed(d, hx, 55 + round(size * 0.36), title, size, P["white"])

    # tầng 1: người đang nói, chữ Nhật có furigana, romaji
    cache = slides.__dict__.setdefault("_jp_captions", {})
    key = (fr.scene, fr.focus or 0)
    if key not in cache:
        cache[key] = card_captions(lesson, sc, fr.focus or 0)
    t1, t2, t3, jb, rb = tiers(d, it, *cache[key])
    x0, y0, x1, y1 = t1
    d.rounded_rectangle(t1, 16, fill=P["card"], outline=P["teal"], width=3)
    sp = lesson.speakers.get(fr.speaker or "")
    fb = font("bold", 16)
    if fr.countdown is not None:  # lượt của người học: nhãn cam + vòng đếm ngược ở góc phải
        chip = "YOUR TURN · LƯỢT CỦA BẠN"
        bw = d.textlength(chip, font=fb) + 28
        d.rounded_rectangle((63, y0 + 17, 63 + bw, y0 + 48), 8, fill=P["amber"])
        d.text((63 + 14, y0 + 33), chip, font=fb, fill=P["bg"], anchor="lm")
        d.ellipse((x1 - 78, y0 + 12, x1 - 24, y0 + 66), fill=P["amber"])
        d.text((x1 - 51, y0 + 39), str(fr.countdown), font=font("bold", 28), fill=P["bg"], anchor="mm")
    elif fr.audio:  # đang phát file nghe của sách: nút ▶ + mã track (nhãn in trong sách) + ghi chú
        chip = "BOOK AUDIO · " + fr.audio
        bw = d.textlength(chip, font=fb) + 58
        d.rounded_rectangle((63, y0 + 17, 63 + bw, y0 + 48), 8, fill=P["teal"])
        d.polygon([(79, y0 + 24), (79, y0 + 41), (94, y0 + 32.5)], fill="#FFFFFF")
        d.text((63 + 44, y0 + 33), chip, font=fb, fill="#FFFFFF", anchor="lm")
        if fr.note:
            note = fr.note
            while len(note) > 1 and width(d, note, 18) > x1 - 30 - (63 + bw + 16):
                note = note[:-2] + "…"
            draw_mixed(d, 63 + bw + 16, y0 + 40, note, 18, P["ruby"])
    elif sp:
        chip = ("JP · " if sp.lang == "ja" else "EN · ") + sp.name.upper() + (" — " + sp.role.upper() if sp.role else "")
        bw = d.textlength(chip, font=fb) + 28
        d.rounded_rectangle((63, y0 + 17, 63 + bw, y0 + 48), 8, fill=sp.color)
        d.text((63 + 14, y0 + 33), chip, font=fb, fill="#FFFFFF", anchor="lm")
    top, bottom = y0 + 62, y1 - 16
    gap = 12 if rb else 0
    room = bottom - top - (rb.height + gap if rb else 0)
    y = top + max(0, (room - jb.height) / 2)
    y = paint(d, jb, X0, y, P["ink"], P["ruby"], fr.hl, fr.done)
    if rb:  # romaji tô sáng cùng chữ khi chia được đúng bằng số chữ trên thẻ
        rom = str(it.get("romaji") or "")
        same = len(ja.romaji_tokens(rom)) == len(ja.card_tokens(str(it["jp"])))
        paint(d, rb, X0, max(y + gap, bottom - rb.height), P["romaji"], P["romaji"],
              fr.hl if same else (), fr.done if same else ())

    # tầng 2, 3: đúng câu đang nói (tiếng Anh / nghĩa tiếng Anh, tiếng Việt)
    (l2, c2), (l3, c3) = captions(lesson, it, fr.speaker, fr.text, fr.en, fr.vi, fr.note, fr.countdown is not None)
    _tier(d, t2, P["en"], P["teal"], P["teal"], l2, c2, P["white"])
    _tier(d, t3, P["vi"], P["amber"], P["amber"], l3, c3, P["gold"])

    # thanh tiến độ
    d.rounded_rectangle((40, 703, W - 40, 707), 2, fill=P["track"])
    if progress > 0:
        d.rounded_rectangle((40, 703, 40 + max(4, (W - 80) * min(progress, 1)), 707), 2, fill=P["amber"])
    return img
