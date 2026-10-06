"""Vẽ slide 1280×720 bằng Pillow: thanh đầu, nội dung theo kiểu cảnh, phụ đề người đang nói, thanh tiến độ."""
from __future__ import annotations

import json
import re
import subprocess
from functools import lru_cache
from pathlib import Path
from typing import Optional

from PIL import Image, ImageDraw, ImageFont

from .script import Lesson, Scene, mcq_keys
from .timeline import Frame

W, H = 1280, 720
TOP, BOTTOM = 158, 548  # vùng nội dung
C = {
    "bg": "#FAF6F1", "ink": "#1E1B18", "muted": "#6B635B", "dim": "#A79E95", "line": "#E4DAD0",
    "card": "#FFFFFF", "red": "#C8102E", "soft": "#F7E3DC", "ok": "#2E7D32", "oksoft": "#E3F1E4",
    "bad": "#C62828", "badsoft": "#FBE4E4",
}

FONT_FILES = {
    "regular": ["/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf",
                "/Library/Fonts/Arial.ttf", "C:/Windows/Fonts/arial.ttf"],
    "bold": ["/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf",
             "/Library/Fonts/Arial Bold.ttf", "C:/Windows/Fonts/arialbd.ttf"],
    "italic": ["/usr/share/fonts/truetype/liberation/LiberationSans-Italic.ttf",
               "/Library/Fonts/Arial Italic.ttf", "C:/Windows/Fonts/ariali.ttf"],
    # dấu ✓ ✗ không có trong Liberation Sans
    "symbol": ["/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
               "/Library/Fonts/Arial Unicode.ttf", "C:/Windows/Fonts/seguisym.ttf"],
}
FC_NAMES = {"regular": "Liberation Sans", "bold": "Liberation Sans:bold", "italic": "Liberation Sans:italic",
            "symbol": "DejaVu Sans:bold"}


@lru_cache(maxsize=None)
def _font_path(kind: str) -> Optional[str]:
    for p in FONT_FILES[kind]:
        if Path(p).exists():
            return p
    try:
        out = subprocess.run(["fc-match", "-f", "%{file}", FC_NAMES[kind]], capture_output=True, text=True, timeout=10)
        if out.returncode == 0 and out.stdout.strip():
            return out.stdout.strip()
    except (OSError, subprocess.SubprocessError):
        pass
    return None


@lru_cache(maxsize=None)
def font(kind: str, size: int) -> ImageFont.FreeTypeFont:
    p = _font_path(kind)
    return ImageFont.truetype(p, size) if p else ImageFont.load_default(size)


def wrap(d: ImageDraw.ImageDraw, text: str, f, width: float) -> list[str]:
    lines, cur = [], ""
    for w in text.split():
        t = (cur + " " + w).strip()
        if not cur or d.textlength(t, font=f) <= width:
            cur = t
        else:
            lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def fit(d, text: str, kind: str, size: int, width: float, max_lines: int, min_size: int = 15):
    """Cỡ chữ lớn nhất (≤ size) để đoạn văn vừa max_lines dòng."""
    while True:
        f = font(kind, size)
        lines = wrap(d, text, f, width)
        if len(lines) <= max_lines or size <= min_size:
            if len(lines) > max_lines:
                lines = lines[:max_lines]
                lines[-1] = lines[-1].rstrip(".,;:") + "…"
            return f, lines
        size -= 1


def block(d, xy, text: str, kind: str, size: int, width: float, fill: str, max_lines: int = 3,
          lead: float = 1.25, min_size: int = 15) -> int:
    """Vẽ đoạn văn tự xuống dòng; trả về tọa độ y ngay dưới đoạn."""
    if not text:
        return xy[1]
    f, lines = fit(d, text, kind, size, width, max_lines, min_size)
    x, y = xy
    step = int(f.size * lead)
    for ln in lines:
        d.text((x, y), ln, font=f, fill=fill)
        y += step
    return y


def _hex(c: str) -> tuple[int, int, int]:
    return tuple(int(c[i:i + 2], 16) for i in (1, 3, 5))


def tint(c: str, a: float) -> str:
    """Pha màu c với nền trắng (a = độ đậm)."""
    r, g, b = _hex(c)
    return "#%02X%02X%02X" % tuple(round(255 - (255 - v) * a) for v in (r, g, b))


class Slides:
    def __init__(self, lesson: Lesson, bdir: Path, voice_label: Optional[dict[str, str]] = None):
        self.L = lesson
        self.bdir = Path(bdir)
        self.voice_label = voice_label or {}
        self.order = list(lesson.speakers)
        self.images: dict[int, Image.Image] = {}
        for i, sc in enumerate(lesson.scenes):
            if sc.image:
                self.images[i] = self._crop(sc)

    # ---------- ảnh cắt từ trang sách ----------
    def _crop(self, sc: Scene) -> Image.Image:
        import pymupdf

        book = json.loads((self.bdir / "book.json").read_text(encoding="utf-8"))
        f = book["files"][sc.image.pdf]
        page, path = sc.image.page, self.bdir / f["path"]
        if not path.exists():  # chỉ có các đoạn PDF đã cắt → mở đoạn chứa trang
            ch = next((c for c in f.get("chunks", []) if c["from"] <= page <= c["to"]), None)
            if not ch:
                raise FileNotFoundError(f"không thấy {path} hay đoạn PDF chứa trang {page}")
            path, page = self.bdir / ch["path"], page - ch["from"] + 1
        with pymupdf.open(path) as doc:
            pix = doc[page - 1].get_pixmap(dpi=200, clip=pymupdf.Rect(*sc.image.clip))
            return Image.frombytes("RGB", (pix.width, pix.height), pix.samples)

    # ---------- khung chung ----------
    def render(self, fr: Frame, progress: float) -> Image.Image:
        img = Image.new("RGB", (W, H), C["bg"])
        d = ImageDraw.Draw(img)
        sc = self.L.scenes[fr.scene]
        self._header(d)
        if sc.kind != "title":
            self._heading(d, sc)
        getattr(self, "_k_" + sc.kind)(img, d, sc, fr)
        if sc.kind != "letter":  # thư mẫu dùng cả chiều cao, chữ đang đọc tô màu ngay trong thư
            self._caption(d, fr)
        d.rounded_rectangle((40, 711, W - 40, 715), 2, fill=C["line"])
        if progress > 0:
            d.rounded_rectangle((40, 711, 40 + max(4, (W - 80) * min(progress, 1)), 715), 2, fill=C["red"])
        return img

    def _header(self, d):
        d.rectangle((0, 0, W, 64), fill=C["card"])
        d.line((0, 64, W, 64), fill=C["line"], width=1)
        tag = self.L.tag or "LESSON"
        ft = font("bold", 22)
        tw = d.textlength(tag, font=ft)
        d.polygon([(0, 0), (tw + 56, 0), (tw + 36, 64), (0, 64)], fill=C["red"])
        d.text((24, 32), tag, font=ft, fill="#FFFFFF", anchor="lm")
        right = "IELTS Target 5.0"
        fr = font("regular", 18)
        rw = d.textlength(right, font=fr)
        d.text((W - 28, 32), right, font=fr, fill=C["muted"], anchor="rm")
        sub = self.L.subtitle or self.L.title
        fs, lines = fit(d, sub, "bold", 21, W - 28 - rw - 30 - (tw + 70), 1)
        d.text((tw + 70, 32), lines[0], font=fs, fill=C["ink"], anchor="lm")

    def _heading(self, d, sc: Scene):
        y = 82
        if sc.heading:
            f, lines = fit(d, sc.heading, "bold", 32, W - 120, 1)
            d.text((60, y), lines[0], font=f, fill=C["red"])
        if sc.heading_vi:
            f, lines = fit(d, sc.heading_vi, "italic", 20, W - 120, 1)
            d.text((60, y + 42), lines[0], font=f, fill=C["muted"])

    def _avatar(self, d, cx, cy, r, key):
        sp = self.L.speakers[key]
        d.ellipse((cx - r, cy - r, cx + r, cy + r), fill=sp.color)
        d.text((cx, cy + 1), sp.name[:1].upper(), font=font("bold", int(r * 0.95)), fill="#FFFFFF", anchor="mm")

    def _caption(self, d, fr: Frame):
        box = (40, 562, W - 40, 704)
        d.rounded_rectangle(box, 16, fill=C["card"], outline=C["line"], width=2)
        x0, width = 146, W - 40 - 146 - 26
        if fr.speaker:
            sp = self.L.speakers[fr.speaker]
            d.rounded_rectangle((box[0], box[1], box[0] + 8, box[3]), 4, fill=sp.color)
            self._avatar(d, 94, 633, 34, fr.speaker)
            scene = self.L.scenes[fr.scene]
            role = scene.roles.get(fr.speaker, sp.role)
            label = sp.name + (" · " + role if role else "")
            d.text((x0, 576), label, font=font("bold", 17), fill=sp.color)
            if scene.hide_text:  # bài nghe: không hiện lời thoại
                d.text((x0, 606), "Listen carefully…", font=font("italic", 27), fill=C["muted"])
                d.text((x0, 650), "Nghe kỹ — lời thoại được ẩn để bạn tự làm bài", font=font("italic", 19), fill=C["dim"])
                return
            y = block(d, (x0, 600), fr.text, "regular", 27, width, C["ink"], max_lines=2 if fr.vi else 3, min_size=19)
            if fr.vi:
                f, lines = fit(d, fr.vi, "italic", 19, width, 1)
                d.text((x0, max(y + 2, 672)), lines[0], font=f, fill=C["muted"])
        elif fr.audio:  # đang phát file nghe của sách
            d.ellipse((60, 599, 128, 667), fill=C["red"])
            d.polygon([(85, 615), (85, 651), (114, 633)], fill="#FFFFFF")
            d.text((x0, 586), fr.note or "Listen to the recording", font=font("bold", 26), fill=C["ink"])
            f, lines = fit(d, fr.vi or "Nghe bản ghi âm của sách", "italic", 21, width, 2)
            for k, ln in enumerate(lines):
                d.text((x0, 626 + k * 27), ln, font=f, fill=C["muted"])
        elif fr.countdown is not None:
            d.ellipse((60, 599, 128, 667), outline=C["red"], width=5)
            d.text((94, 634), str(fr.countdown), font=font("bold", 32), fill=C["red"], anchor="mm")
            d.text((x0, 586), fr.note or "Your turn", font=font("bold", 26), fill=C["ink"])
            if fr.vi:
                block(d, (x0, 626), fr.vi, "italic", 21, width, C["muted"], max_lines=2)

    # ---------- các kiểu cảnh ----------
    def _k_title(self, img, d, sc, fr):
        y = block(d, (60, 104), self.L.title, "bold", 60, W - 120, C["ink"], max_lines=1)
        if self.L.subtitle:
            y = block(d, (60, y + 6), self.L.subtitle, "bold", 32, W - 120, C["red"], max_lines=1)
        if self.L.title_vi:
            block(d, (60, y + 8), self.L.title_vi, "italic", 24, W - 120, C["muted"], max_lines=1)
        n = len(self.order)
        cw = min(420, (W - 120 - 30 * (n - 1)) // max(n, 1))
        for i, key in enumerate(self.order):
            sp = self.L.speakers[key]
            x = 60 + i * (cw + 30)
            on = fr.speaker == key
            d.rounded_rectangle((x, 362, x + cw, 520), 18, fill=C["card"],
                                outline=sp.color if on else C["line"], width=4 if on else 2)
            self._avatar(d, x + 70, 441, 44, key)
            d.text((x + 134, 400), sp.name, font=font("bold", 30), fill=C["ink"])
            d.text((x + 134, 440), sp.role, font=font("regular", 21), fill=sp.color)
            if key in self.voice_label:
                d.text((x + 134, 474), self.voice_label[key], font=font("regular", 16), fill=C["muted"])

    def _rows(self, n: int, top: int = TOP, bottom: int = BOTTOM, cap: int = 74) -> int:
        return int(min(cap, (bottom - top) / max(n, 1)))

    def _k_bullets(self, img, d, sc, fr):
        n = len(sc.items)
        rh = self._rows(n)
        for i, it in enumerate(sc.items):
            y = TOP + i * rh
            on = fr.focus == i
            if on:
                d.rounded_rectangle((52, y + 2, W - 52, y + rh - 4), 12, fill=C["soft"])
                d.rounded_rectangle((52, y + 2, 58, y + rh - 4), 3, fill=C["red"])
            faded = fr.focus is not None and not on
            d.ellipse((76, y + 10, 108, y + 42), fill=C["red"] if not faded else C["dim"])
            d.text((92, y + 26), str(i + 1), font=font("bold", 18), fill="#FFFFFF", anchor="mm")
            en_y = y + 10 if it.get("vi") else y + 14
            f, lines = fit(d, str(it["en"]), "bold", 25, W - 190, 1)
            d.text((126, en_y), lines[0], font=f, fill=C["muted"] if faded else C["ink"])
            if it.get("vi") and rh >= 56:
                f, lines = fit(d, str(it["vi"]), "italic", 19, W - 190, 1)
                d.text((126, en_y + 32), lines[0], font=f, fill=C["dim"] if faded else C["muted"])

    def _k_vocab(self, img, d, sc, fr):
        n = len(sc.items)
        rh = self._rows(n, cap=40)
        for i, it in enumerate(sc.items):
            y = TOP + i * rh
            on = fr.focus == i
            if on:
                d.rounded_rectangle((52, y, 384, y + rh - 3), 8, fill=C["soft"])
            f, lines = fit(d, str(it["w"]), "bold" if on else "regular", 20, 300, 1)
            d.text((66, y + (rh - 3) / 2), lines[0], font=f, fill=C["red"] if on else C["ink"], anchor="lm")
        x0, x1 = 410, W - 60
        d.rounded_rectangle((x0, TOP, x1, BOTTOM), 18, fill=C["card"], outline=C["line"], width=2)
        if fr.focus is None:
            d.text(((x0 + x1) / 2, 300), "Listen and repeat", font=font("bold", 40), fill=C["red"], anchor="mm")
            d.text(((x0 + x1) / 2, 352), "Nghe và nhắc lại theo bạn Tom", font=font("italic", 24), fill=C["muted"], anchor="mm")
            d.text(((x0 + x1) / 2, 410), f"{n} từ mới", font=font("regular", 22), fill=C["muted"], anchor="mm")
            return
        it = sc.items[fr.focus]
        d.text((x1 - 24, TOP + 20), f"{fr.focus + 1} / {n}", font=font("regular", 18), fill=C["muted"], anchor="ra")
        y = block(d, (x0 + 30, TOP + 26), str(it["w"]), "bold", 46, x1 - x0 - 140, C["red"], max_lines=1)
        if it.get("pos"):
            d.text((x0 + 30, y + 2), str(it["pos"]), font=font("italic", 20), fill=C["muted"])
            y += 30
        y = block(d, (x0 + 30, y + 10), str(it["vi"]), "bold", 30, x1 - x0 - 60, C["ink"], max_lines=2)
        ey = max(y + 18, 350)
        d.rounded_rectangle((x0 + 24, ey, x1 - 24, BOTTOM - 22), 12, fill=C["soft"])
        d.text((x0 + 44, ey + 14), "Example", font=font("bold", 16), fill=C["red"])
        block(d, (x0 + 44, ey + 40), str(it["ex"]), "regular", 26, x1 - x0 - 88, C["ink"],
              max_lines=max(1, (BOTTOM - 30 - ey - 40) // 32))

    def _k_match(self, img, d, sc, fr):
        pic = self.images[fr.scene]
        bw, bh = 720, BOTTOM - TOP
        s = min(bw / pic.width, bh / pic.height)
        im = pic.resize((int(pic.width * s), int(pic.height * s)), Image.LANCZOS)
        img.paste(im, (60, TOP + (bh - im.height) // 2))
        x0 = 60 + bw + 26
        n = len(sc.items)
        rh = self._rows(n, cap=66)
        for i, it in enumerate(sc.items):
            y = TOP + i * rh
            key = str(it["n"])
            on = fr.focus == i
            if on:
                d.rounded_rectangle((x0 - 8, y, W - 52, y + rh - 4), 10, fill=C["soft"])
            if key in fr.revealed:
                d.ellipse((x0, y + 8, x0 + 36, y + 44), fill=C["red"])
                ans = str(it["answer"])  # đáp án là dấu ✓ / ✗ thì cần phông có ký hiệu
                d.text((x0 + 18, y + 26), ans, font=font("symbol" if ans in ("✓", "✗") else "bold", 21), fill="#FFFFFF", anchor="mm")
            else:
                d.ellipse((x0, y + 8, x0 + 36, y + 44), outline=C["dim"], width=2)
                d.text((x0 + 18, y + 26), "?", font=font("bold", 19), fill=C["dim"], anchor="mm")
            d.text((x0 + 50, y + 14), f"{it['n']}.", font=font("bold", 21), fill=C["red"])
            block(d, (x0 + 78, y + 14), str(it["q"]), "regular", 21, W - 60 - x0 - 90, C["ink"], max_lines=2,
                  lead=1.15, min_size=17)

    def _cell(self, d, x, y, rh, text, width, fill=None):
        """Chữ trong một hàng: một dòng nếu vừa, hàng đủ cao thì cho xuống hai dòng; canh giữa theo chiều dọc."""
        f, lines = fit(d, text, "regular", 21, width, 1, min_size=18)
        if len(wrap(d, text, f, width)) > 1 and rh >= 58:
            f, lines = fit(d, text, "regular", 19, width, 2, min_size=16)
        step = int(f.size * 1.15)
        top = y + (rh - 4 - step * len(lines)) / 2
        for k, ln in enumerate(lines):
            d.text((x, top + k * step), ln, font=f, fill=fill or C["ink"])

    def _k_pairs(self, img, d, sc, fr):
        n = max(len(sc.items), len(sc.options))
        rh = self._rows(n, cap=64)
        used = {str(it["answer"]) for it in sc.items if str(it["n"]) in fr.revealed}
        cur = sc.items[fr.focus]["answer"] if fr.focus is not None else None
        lx1, rx0 = 690, 730
        for i, it in enumerate(sc.items):
            y = TOP + i * rh
            on = fr.focus == i
            if on:
                d.rounded_rectangle((52, y, lx1 + 6, y + rh - 4), 10, fill=C["soft"])
            d.text((66, y + (rh - 4) / 2), f"{it['n']}.", font=font("bold", 21), fill=C["red"], anchor="lm")
            self._cell(d, 98, y, rh, str(it["q"]), lx1 - 160)
            sx = lx1 - 44
            if str(it["n"]) in fr.revealed:
                d.rounded_rectangle((sx, y + 6, sx + 40, y + rh - 10), 8, fill=C["red"])
                d.text((sx + 20, y + (rh - 4) / 2), str(it["answer"]), font=font("bold", 21), fill="#FFFFFF", anchor="mm")
            else:
                d.rounded_rectangle((sx, y + 6, sx + 40, y + rh - 10), 8, outline=C["dim"], width=2)
        for i, op in enumerate(sc.options):
            y = TOP + i * rh
            k = str(op["k"])
            if k == cur and str(sc.items[fr.focus]["n"]) in fr.revealed:
                d.rounded_rectangle((rx0 - 8, y, W - 52, y + rh - 4), 10, fill=C["soft"])
            elif k in used:
                d.rounded_rectangle((rx0 - 8, y, W - 52, y + rh - 4), 10, fill=C["oksoft"])
            d.text((rx0 + 6, y + (rh - 4) / 2), k + ".", font=font("bold", 21), fill=C["red"], anchor="lm")
            self._cell(d, rx0 + 36, y, rh, str(op["text"]), W - 60 - rx0 - 50)

    def _k_qa(self, img, d, sc, fr):
        if fr.focus is None:  # danh sách câu hỏi
            rh = self._rows(len(sc.items), cap=60)
            for i, it in enumerate(sc.items):
                y = TOP + i * rh
                d.text((66, y + 8), f"{i + 1}.", font=font("bold", 24), fill=C["red"])
                f, lines = fit(d, str(it["q"]), "regular", 24, W - 200, 1)
                d.text((104, y + 8), lines[0], font=f, fill=C["ink"])
            return
        it = sc.items[fr.focus]
        # mặc định người nói thứ nhất hỏi, người thứ hai trả lời; mục có `ask` / `by` thì đổi vai
        ask = self.L.speakers[it.get("ask") or self.order[0]]
        ans = self.L.speakers[it.get("by") or self.order[-1]]
        d.text((60, TOP), f"Question {fr.focus + 1} of {len(sc.items)}", font=font("bold", 18), fill=C["red"])
        d.rounded_rectangle((60, TOP + 30, W - 60, TOP + 116), 14, fill=C["card"], outline=C["line"], width=2)
        d.rounded_rectangle((60, TOP + 30, 68, TOP + 116), 4, fill=ask.color)
        block(d, (90, TOP + 46), str(it["q"]), "bold", 30, W - 180, C["ink"], max_lines=2, lead=1.15, min_size=20)
        if str(fr.focus) not in fr.revealed:
            d.text((W / 2, TOP + 210), "Think: how would you answer?", font=font("italic", 28), fill=C["dim"], anchor="mm")
            d.text((W / 2, TOP + 250), "Bạn sẽ trả lời thế nào?", font=font("italic", 22), fill=C["dim"], anchor="mm")
        else:
            top, bot = TOP + 134, BOTTOM - (64 if it.get("phrases") else 0)
            d.rounded_rectangle((60, top, W - 60, bot), 14, fill=tint(ans.color, 0.08), outline=tint(ans.color, 0.35), width=2)
            d.rounded_rectangle((60, top, 68, bot), 4, fill=ans.color)
            d.text((90, top + 14), f"{ans.name}:", font=font("bold", 18), fill=ans.color)
            block(d, (90, top + 42), str(it["a"]), "regular", 27, W - 180, C["ink"],
                  max_lines=max(1, (bot - top - 52) // 34), min_size=20)
        if it.get("phrases"):
            x, y = 60, BOTTOM - 46
            d.text((x, y + 20), "Useful:", font=font("bold", 18), fill=C["muted"], anchor="lm")
            x += 80
            for ph in it["phrases"]:
                f = font("regular", 19)
                w = d.textlength(str(ph), font=f) + 28
                if x + w > W - 60:
                    break
                d.rounded_rectangle((x, y + 2, x + w, y + 38), 18, fill=C["soft"])
                d.text((x + 14, y + 20), str(ph), font=f, fill=C["ink"], anchor="lm")
                x += w + 10

    def _k_compare(self, img, d, sc, fr):
        n = len(sc.items)
        gap = 30
        bw = (W - 120 - gap * (n - 1)) / n
        for i, it in enumerate(sc.items):
            x0 = 60 + i * (bw + gap)
            x1 = x0 + bw
            on = fr.focus == i
            faded = fr.focus is not None and not on
            d.rounded_rectangle((x0, TOP, x1, BOTTOM), 18, fill=C["card"], outline=C["red"] if on else C["line"],
                                width=4 if on else 2)
            d.rounded_rectangle((x0 + 2, TOP + 2, x1 - 2, TOP + 86), 16, fill=C["soft"] if on else "#F3EEE8")
            d.rectangle((x0 + 2, TOP + 60, x1 - 2, TOP + 86), fill=C["soft"] if on else "#F3EEE8")
            block(d, (x0 + 24, TOP + 14), str(it["title"]), "bold", 26, bw - 48, C["red"] if not faded else C["muted"], max_lines=1)
            if it.get("title_vi"):
                block(d, (x0 + 24, TOP + 50), str(it["title_vi"]), "italic", 18, bw - 48, C["muted"], max_lines=1)
            y = TOP + 104
            for ln in it["lines"]:
                d.ellipse((x0 + 26, y + 11, x0 + 34, y + 19), fill=C["red"] if not faded else C["dim"])
                y = block(d, (x0 + 46, y), str(ln), "regular", 24, bw - 72, C["ink"] if not faded else C["muted"],
                          max_lines=2, lead=1.2, min_size=18) + 10
                if y > BOTTOM - 30:
                    break

    def _k_errors(self, img, d, sc, fr):
        n = len(sc.items)
        rh = self._rows(n, cap=96)
        sym = font("symbol", 24)
        for i, it in enumerate(sc.items):
            y = TOP + i * rh
            on = fr.focus == i
            faded = fr.focus is not None and not on
            d.rounded_rectangle((52, y + 2, W - 52, y + rh - 6), 12, fill=C["soft"] if on else C["card"],
                                outline=C["red"] if on else C["line"], width=2)
            mid = 52 + (W - 104) // 2
            d.text((76, y + 18), "✗", font=sym, fill=C["bad"])
            f, lines = fit(d, str(it["wrong"]), "regular", 24, mid - 130, 1)
            d.text((110, y + 18), lines[0], font=f, fill=C["bad"] if not faded else C["dim"])
            tw = d.textlength(lines[0], font=f)
            d.line((110, y + 32, 110 + tw, y + 32), fill=C["bad"] if not faded else C["dim"], width=2)
            d.text((mid + 10, y + 18), "✓", font=sym, fill=C["ok"])
            f, lines = fit(d, str(it["right"]), "bold", 24, W - 52 - mid - 70, 1)
            d.text((mid + 46, y + 18), lines[0], font=f, fill=C["ok"] if not faded else C["dim"])
            if it.get("note") and rh >= 80:
                f, lines = fit(d, str(it["note"]), "italic", 19, W - 200, 1)
                d.text((110, y + 54), lines[0], font=f, fill=C["muted"])

    def _k_practice(self, img, d, sc, fr):
        if fr.focus is None:
            d.text((W / 2, 300), "Your turn", font=font("bold", 54), fill=C["red"], anchor="mm")
            d.text((W / 2, 362), "Đến lượt bạn: nghe câu hỏi rồi trả lời thành tiếng", font=font("italic", 26),
                   fill=C["muted"], anchor="mm")
            return
        it = sc.items[fr.focus]
        d.text((W / 2, TOP + 6), f"Question {fr.focus + 1} / {len(sc.items)}", font=font("bold", 20), fill=C["red"], anchor="ma")
        f, lines = fit(d, str(it["q"]), "bold", 44, W - 200, 2, min_size=28)
        y = TOP + 56
        for ln in lines:
            d.text((W / 2, y), ln, font=f, fill=C["ink"], anchor="ma")
            y += int(f.size * 1.2)
        cy = 440
        if fr.countdown is not None:
            d.ellipse((W / 2 - 66, cy - 66, W / 2 + 66, cy + 66), outline=C["red"], width=8)
            d.text((W / 2, cy + 2), str(fr.countdown), font=font("bold", 60), fill=C["red"], anchor="mm")
        else:
            d.text((W / 2, cy), "Listen…", font=font("italic", 30), fill=C["muted"], anchor="mm")
        if it.get("hint"):
            d.text((W / 2, BOTTOM - 4), "Gợi ý: " + str(it["hint"]), font=font("italic", 20), fill=C["muted"], anchor="md")

    def _k_order(self, img, d, sc, fr):
        """Sắp xếp: cột trái các mục theo chữ cái, ô số thứ tự hiện khi mở; cột phải dựng dần thứ tự đúng."""
        n = len(sc.items)
        rh = self._rows(n, cap=64)
        lx1, rx0 = 760, 800
        for i, it in enumerate(sc.items):
            y = TOP + i * rh
            k = str(it["k"])
            if fr.focus == i:
                d.rounded_rectangle((52, y, lx1 + 6, y + rh - 4), 10, fill=C["soft"])
            label = str(it.get("label", k + "."))  # `label: ""` khi mục không có chữ cái riêng
            if label:
                d.text((66, y + (rh - 4) / 2), label, font=font("bold", 21), fill=C["red"], anchor="lm")
            self._cell(d, 98 if label else 70, y, rh, str(it["text"]), lx1 - 160)
            sx = lx1 - 44
            if k in fr.revealed:
                d.ellipse((sx + 2, y + (rh - 4) / 2 - 18, sx + 38, y + (rh - 4) / 2 + 18), fill=C["red"])
                d.text((sx + 20, y + (rh - 4) / 2), str(it["pos"]), font=font("bold", 20), fill="#FFFFFF", anchor="mm")
            else:
                d.ellipse((sx + 2, y + (rh - 4) / 2 - 18, sx + 38, y + (rh - 4) / 2 + 18), outline=C["dim"], width=2)
        d.rounded_rectangle((rx0, TOP, W - 60, BOTTOM), 16, fill=C["card"], outline=C["line"], width=2)
        d.text((rx0 + 20, TOP + 14), "Correct order", font=font("bold", 20), fill=C["red"])
        d.text((rx0 + 20, TOP + 40), "Thứ tự đúng", font=font("italic", 17), fill=C["muted"])
        by_pos = {int(it["pos"]): it for it in sc.items}
        sh = (BOTTOM - TOP - 76) / n
        for pos in range(1, n + 1):
            y = TOP + 70 + (pos - 1) * sh
            it = by_pos[pos]
            d.text((rx0 + 22, y + sh / 2), f"{pos}", font=font("bold", 20), fill=C["muted"], anchor="lm")
            if str(it["k"]) in fr.revealed:
                label = it.get("short") or it["text"]
                prefix = str(it.get("label", it["k"])).rstrip(".")
                f, lines = fit(d, f"{prefix} · {label}" if prefix else str(label), "regular", 18, W - 60 - rx0 - 70, 1, min_size=14)
                d.text((rx0 + 50, y + sh / 2), lines[0], font=f, fill=C["ink"], anchor="lm")
            else:
                d.line((rx0 + 50, y + sh / 2 + 8, W - 84, y + sh / 2 + 8), fill=C["line"], width=2)

    def _k_timing(self, img, d, sc, fr):
        """Chia thời gian: thanh ngang theo số phút (mở dần nếu cảnh có `reveal`), bảng từng bước bên dưới."""
        total = sum(float(it["minutes"]) for it in sc.items)
        progressive = any(ln.reveal for ln in sc.lines)
        shown = [not progressive or str(i) in fr.revealed for i in range(len(sc.items))]
        x0, x1, y0, y1 = 60, W - 60, TOP + 6, TOP + 70
        d.rounded_rectangle((x0, y0, x1, y1), 12, fill=C["card"], outline=C["line"], width=2)
        shades = [0.95, 0.55, 0.75, 0.4, 0.85, 0.65, 0.5]
        x = x0
        for i, it in enumerate(sc.items):
            w = (x1 - x0) * float(it["minutes"]) / total
            if shown[i]:
                col = tint(C["red"], shades[i % len(shades)]) if fr.focus in (None, i) else tint(C["red"], 0.18)
                d.rectangle((x + 1, y0 + 2, x + w - 1, y1 - 2), fill=col)
                label = f"{it['minutes']:g}'"
                if w > 34:
                    light = fr.focus not in (None, i)
                    d.text((x + w / 2, (y0 + y1) / 2), label, font=font("bold", 20),
                           fill=C["red"] if light else "#FFFFFF", anchor="mm")
            x += w
        d.text((x1, y1 + 8), f"Total: {total:g} minutes", font=font("bold", 18), fill=C["muted"], anchor="ra")
        n = len(sc.items)
        top = y1 + 40
        rh = int(min(52, (BOTTOM - top) / max(n, 1)))
        for i, it in enumerate(sc.items):
            y = top + i * rh
            if fr.focus == i:
                d.rounded_rectangle((52, y, W - 52, y + rh - 4), 10, fill=C["soft"])
            col = tint(C["red"], shades[i % len(shades)])
            d.rounded_rectangle((66, y + (rh - 4) / 2 - 9, 84, y + (rh - 4) / 2 + 9), 4, fill=col if shown[i] else C["line"])
            f, lines = fit(d, str(it["label"]), "bold" if fr.focus == i else "regular", 21, 640, 1)
            d.text((100, y + (rh - 4) / 2), lines[0], font=f, fill=C["ink"], anchor="lm")
            if it.get("vi"):
                f, lines = fit(d, str(it["vi"]), "italic", 17, 330, 1)
                d.text((760, y + (rh - 4) / 2), lines[0], font=f, fill=C["muted"], anchor="lm")
            d.text((W - 70, y + (rh - 4) / 2), f"{it['minutes']:g} min" if shown[i] else "? min",
                   font=font("bold", 21), fill=C["red"] if shown[i] else C["dim"], anchor="rm")

    def _k_letter(self, img, d, sc, fr):
        """Thư mẫu: cả lá thư trên trang giấy, đoạn đang đọc tô nền; lề phải ghi vai trò từng đoạn và số từ."""
        px0, px1, py0, py1 = 60, 890, TOP, 702
        d.rounded_rectangle((px0 + 4, py0 + 4, px1 + 4, py1 + 4), 14, fill=C["line"])
        d.rounded_rectangle((px0, py0, px1, py1), 14, fill="#FFFDF8", outline=C["line"], width=2)
        width = px1 - px0 - 64
        paras = [str(it["text"]).split("\n") for it in sc.items]

        chip_x = px1 - 196  # nhãn "… is reading" ở góc trên bên phải trang

        def layout(size):
            f = font("regular", size)
            step, gap = int(size * 1.32), int(size * 0.55)
            first = (wrap(d, paras[0][0], f, width) or [""])[0] if paras and paras[0] else ""
            # dòng đầu dài (không phải lời chào ngắn) thì chừa một hàng cho nhãn người đọc
            top = py0 + 24 if px0 + 32 + d.textlength(first, font=f) < chip_x - 12 else py0 + 56
            boxes, y = [], top
            for para in paras:
                rows = [r for part in para for r in (wrap(d, part, f, width) or [""])]
                boxes.append((y, rows))
                y += step * len(rows) + gap
            return f, step, boxes, y

        size = 23
        f, step, boxes, end = layout(size)
        while end > py1 - 18 and size > 14:
            size -= 1
            f, step, boxes, end = layout(size)
        for i, (y, rows) in enumerate(boxes):
            on = fr.focus == i
            if on:
                d.rounded_rectangle((px0 + 16, y - 5, px1 - 16, y + step * len(rows) + 1), 8, fill=C["soft"])
                d.rounded_rectangle((px0 + 16, y - 5, px0 + 21, y + step * len(rows) + 1), 2, fill=C["red"])
            for k, r in enumerate(rows):
                d.text((px0 + 32, y + k * step), r, font=f, fill=C["ink"] if fr.focus is None or on else "#5F5852")
        # lề phải: người đang đọc, vai trò từng đoạn, số từ
        nx = px1 + 30
        if fr.speaker:  # góc trên bên phải trang thư, ngang dòng lời chào (dòng ngắn)
            sp = self.L.speakers[fr.speaker]
            cx = chip_x
            self._avatar(d, cx, py0 + 26, 18, fr.speaker)
            d.text((cx + 26, py0 + 12), sp.name + " is reading", font=font("bold", 16), fill=sp.color)
            d.text((cx + 26, py0 + 31), "đang đọc thành tiếng", font=font("italic", 14), fill=C["muted"])
        for i, (y, rows) in enumerate(boxes):
            note = sc.items[i].get("note")
            if not note:
                continue
            on = fr.focus == i
            d.line((px1 + 6, y + 10, nx - 6, y + 10), fill=C["red"] if on else C["line"], width=2)
            block(d, (nx, y), str(note), "bold" if on else "regular", 17, W - 40 - nx, C["red"] if on else C["muted"],
                  max_lines=2, lead=1.15, min_size=14)
        words = sc.words or sum(len(re.findall(r"[A-Za-z0-9']+", str(it["text"]))) for it in sc.items if it.get("body", True))
        d.text((nx, py1 - 6), f"≈ {words} words", font=font("bold", 18), fill=C["muted"], anchor="ld")

    def _k_blanks(self, img, d, sc, fr):
        """Nghe – chép: các ô trống đánh số (hai hàng như trong sách); mở ra thì hiện chữ đúng và mẹo chính tả.
        Mục có `q` (câu chứa ___) thì vẽ thành danh sách câu điền từ."""
        if any(it.get("q") for it in sc.items):
            return self._blank_sentences(d, sc, fr)
        n = len(sc.items)
        cols = 5 if n > 6 else n
        rows = (n + cols - 1) // cols
        cw = (W - 120) / cols
        ch = min(150, (BOTTOM - TOP - 70) / rows)
        for i, it in enumerate(sc.items):
            r, c = divmod(i, cols)
            x0, y0 = 60 + c * cw, TOP + r * ch
            on = fr.focus == i
            d.rounded_rectangle((x0 + 6, y0 + 6, x0 + cw - 6, y0 + ch - 10), 14,
                                fill=C["soft"] if on else C["card"], outline=C["red"] if on else C["line"], width=3 if on else 2)
            d.text((x0 + 22, y0 + 18), f"{it['n']}.", font=font("bold", 22), fill=C["red"])
            if str(it["n"]) in fr.revealed:
                f, lines = fit(d, str(it["answer"]), "bold", 30, cw - 50, 1, min_size=18)
                d.text((x0 + cw / 2, y0 + ch / 2 + 4), lines[0], font=f, fill=C["ink"], anchor="mm")
            else:
                d.line((x0 + 30, y0 + ch / 2 + 18, x0 + cw - 30, y0 + ch / 2 + 18), fill=C["dim"], width=2)
        cur = sc.items[fr.focus] if fr.focus is not None else None
        if cur is not None and str(cur["n"]) in fr.revealed and cur.get("tip"):
            ty = TOP + rows * ch + 8
            d.rounded_rectangle((60, ty, W - 60, BOTTOM - 4), 12, fill=C["card"], outline=C["line"], width=2)
            d.text((80, ty + (BOTTOM - 4 - ty) / 2), "Spelling tip:", font=font("bold", 19), fill=C["red"], anchor="lm")
            f, lines = fit(d, str(cur["tip"]), "regular", 21, W - 260, 1, min_size=15)
            d.text((220, ty + (BOTTOM - 4 - ty) / 2), lines[0], font=f, fill=C["ink"], anchor="lm")

    def _blank_sentences(self, d, sc, fr):
        n = len(sc.items)
        cur = sc.items[fr.focus] if fr.focus is not None else None
        show_tip = cur is not None and str(cur["n"]) in fr.revealed and cur.get("tip")
        rh = int(min(56, (BOTTOM - TOP - (58 if show_tip else 0)) / max(n, 1)))
        # ô gợi ý: rộng 166 px, nới ra (tối đa 420 px) cho gợi ý dài như "gets better / is not so good"
        need = max((d.textlength(str(it["hint"]), font=font("italic", 19)) for it in sc.items if it.get("hint")), default=0)
        hint_x = W - 64 - int(min(max(166, need + 28), 420))
        for i, it in enumerate(sc.items):
            y = TOP + i * rh
            mid = y + (rh - 4) / 2
            on = fr.focus == i
            if on:
                d.rounded_rectangle((52, y, W - 52, y + rh - 4), 10, fill=C["soft"])
            d.text((66, mid), f"{it['n']}.", font=font("bold", 22), fill=C["red"], anchor="lm")
            q = str(it.get("q") or "___")
            before, _, after = q.partition("___")
            ans = str(it["answer"])
            room = (hint_x - 16 if it.get("hint") else W - 64) - 104
            size = 22
            while size > 15:  # câu dài thì thu nhỏ chữ cho vừa một dòng
                f, fb = font("regular", size), font("bold", size)
                need = d.textlength(before + after, font=f) + max(d.textlength(ans, font=fb), 150) + 14
                if need <= room:
                    break
                size -= 1
            f = font("regular", size)
            x = 104
            if before:
                d.text((x, mid), before, font=f, fill=C["ink"], anchor="lm")
                x += d.textlength(before, font=f) + 6
            if str(it["n"]) in fr.revealed:
                fb = font("bold", size)
                d.text((x, mid), ans, font=fb, fill=C["red"], anchor="lm")
                x += d.textlength(ans, font=fb)
                d.line((x - d.textlength(ans, font=fb), mid + 15, x, mid + 15), fill=C["red"], width=2)
            else:
                d.line((x, mid + 13, x + 150, mid + 13), fill=C["dim"], width=2)
                x += 150
            if after:  # dấu câu dính sát chỗ trống, chữ thường cách một khoảng
                d.text((x + (1 if after[0] in ".,?!;:'" else 6), mid), after, font=f, fill=C["ink"], anchor="lm")
            if it.get("hint"):
                d.rounded_rectangle((hint_x, y + 8, W - 64, y + rh - 12), 8, fill=C["card"], outline=C["line"])
                hf, hl = fit(d, str(it["hint"]), "italic", 19, W - 64 - hint_x - 16, 1, min_size=13)
                d.text(((hint_x + W - 64) / 2, mid), hl[0], font=hf, fill=C["muted"], anchor="mm")
        if show_tip:
            ty = TOP + n * rh + 6
            by = min(BOTTOM - 4, ty + 54)
            d.rounded_rectangle((60, ty, W - 60, by), 12, fill=C["card"], outline=C["line"], width=2)
            d.text((80, (ty + by) / 2), "Tip:", font=font("bold", 19), fill=C["red"], anchor="lm")
            f, lines = fit(d, str(cur["tip"]), "regular", 21, W - 220, 1, min_size=15)
            d.text((130, (ty + by) / 2), lines[0], font=f, fill=C["ink"], anchor="lm")

    def _k_passage(self, img, d, sc, fr):
        """Bài đọc trên màn hình (phần trên phụ đề): đoạn đang nói tô nền, cụm từ `mark` của dòng thoại tô vàng.
        Mục có `note` thì chừa lề phải ghi ý chính của đoạn."""
        has_note = any(it.get("note") for it in sc.items)
        x0, x1 = 60, (W - 330 if has_note else W - 60)
        lx = x0 + 16
        tx = lx + (max(d.textlength(str(it.get("label", "")), font=font("bold", 20)) for it in sc.items) + 12
                   if any(it.get("label") for it in sc.items) else 0)
        width = x1 - tx - 14
        top, bottom = TOP - 4, BOTTOM + 6

        def layout(size):
            f = font("regular", size)
            step, gap = int(size * 1.28), int(size * 0.5)
            boxes, y = [], top + 6
            for it in sc.items:
                rows = [r for part in str(it["text"]).split("\n") for r in (wrap(d, part, f, width) or [""])]
                boxes.append((y, rows))
                y += step * len(rows) + gap
            return f, step, boxes, y

        size = 22
        f, step, boxes, end = layout(size)
        while end > bottom and size > 13:
            size -= 1
            f, step, boxes, end = layout(size)
        d.rounded_rectangle((x0, top, x1, bottom), 12, fill="#FFFDF8", outline=C["line"], width=2)
        marks = [m.lower() for m in fr.mark]
        for i, (y, rows) in enumerate(boxes):
            it = sc.items[i]
            on = fr.focus == i
            if on:
                d.rounded_rectangle((x0 + 6, y - 4, x1 - 6, y + step * len(rows)), 8, fill=C["soft"])
                d.rounded_rectangle((x0 + 6, y - 4, x0 + 11, y + step * len(rows)), 2, fill=C["red"])
            if it.get("label"):
                d.text((lx, y), str(it["label"]), font=font("bold", size), fill=C["red"])
            for k, r in enumerate(rows):
                ry = y + k * step
                if on and marks:
                    low = r.lower()
                    for m in marks:
                        j = low.find(m)
                        while j >= 0:
                            a = tx + d.textlength(r[:j], font=f)
                            b = a + d.textlength(r[j:j + len(m)], font=f)
                            d.rounded_rectangle((a - 2, ry - 2, b + 2, ry + size + 4), 4, fill="#FFE07A")
                            j = low.find(m, j + len(m))
                d.text((tx, ry), r, font=f, fill=C["ink"] if fr.focus is None or on else "#5F5852")
            if it.get("note"):
                d.line((x1 + 6, y + 10, x1 + 24, y + 10), fill=C["red"] if on else C["line"], width=2)
                block(d, (x1 + 30, y), str(it["note"]), "bold" if on else "regular", 17, W - 40 - x1 - 30,
                      C["red"] if on else C["muted"], max_lines=3, lead=1.15, min_size=13)

    def _k_mcq(self, img, d, sc, fr):
        """Trắc nghiệm a/b/c (hoặc `keys` riêng, ví dụ 1/2/3): mỗi câu một thẻ; mở đáp án thì tô xanh phương án đúng."""
        n = len(sc.items)
        gap = 24
        cw = (W - 120 - gap * (n - 1)) / max(n, 1)
        oh = 52

        def height(it):  # thẻ cao vừa nội dung, các thẻ cao bằng nhau
            f, lines = fit(d, f"{it['n']}. {it['q']}", "bold", 23, cw - 44, 3, min_size=17)
            return 18 + int(f.size * 1.2) * len(lines) + 12 + oh * len(it["options"]) + 6

        bottom = min(BOTTOM, TOP + max(height(it) for it in sc.items))
        for i, it in enumerate(sc.items):
            x0 = 60 + i * (cw + gap)
            on = fr.focus == i
            d.rounded_rectangle((x0, TOP, x0 + cw, bottom), 16, fill=C["card"],
                                outline=C["red"] if on else C["line"], width=3 if on else 2)
            y = block(d, (x0 + 22, TOP + 18), f"{it['n']}. {it['q']}", "bold", 23, cw - 44, C["ink"], max_lines=3, lead=1.2, min_size=17)
            y += 12
            done = str(it["n"]) in fr.revealed
            keys = mcq_keys(it)
            for k, opt in enumerate(it["options"]):
                letter = keys[k]
                right = done and letter == str(it["answer"])
                if right:
                    d.rounded_rectangle((x0 + 14, y - 6, x0 + cw - 14, y + oh - 10), 10, fill=C["oksoft"])
                d.text((x0 + 26, y + (oh - 16) / 2), letter + ".", font=font("bold", 21), fill=C["ok"] if right else C["red"], anchor="lm")
                f, lines = fit(d, str(opt), "bold" if right else "regular", 21, cw - 90, 1, min_size=15)
                d.text((x0 + 56, y + (oh - 16) / 2), lines[0], font=f, fill=C["ink"] if not done or right else C["muted"], anchor="lm")
                y += oh
