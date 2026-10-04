"""Thao tác PDF dùng chung: mở file, đo băng tiêu đề đỏ, vẽ trang thành ảnh."""
from __future__ import annotations

import hashlib
from functools import lru_cache
from pathlib import Path

import pymupdf


def sha256_file(path: Path, chunk: int = 1 << 20) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as f:
        while True:
            b = f.read(chunk)
            if not b:
                break
            h.update(b)
    return h.hexdigest()


@lru_cache(maxsize=8)
def open_pdf(path: str) -> pymupdf.Document:
    return pymupdf.open(path)


def red_ratio(doc: pymupdf.Document, page_no: int, top: float = 0.08, width_px: int = 120) -> float:
    """Tỷ lệ điểm ảnh đỏ đậm trong dải trên cùng của trang (page_no bắt đầu từ 1).

    Sách in bằng mẫu dàn trang cố định thường đánh dấu trang mở đầu mỗi module bằng một
    băng màu. Đo màu ở độ phân giải rất thấp là đủ và không cần OCR.
    """
    page = doc[page_no - 1]
    r = page.rect
    zoom = width_px / r.width
    pix = page.get_pixmap(matrix=pymupdf.Matrix(zoom, zoom), clip=pymupdf.Rect(0, 0, r.width, r.height * top))
    s, n = pix.samples, pix.n
    hit = 0
    for k in range(0, len(s), n):
        if s[k] > 150 and s[k + 1] < 90 and s[k + 2] < 90:
            hit += 1
    total = pix.width * pix.height
    return hit / total if total else 0.0


def text_chars(doc: pymupdf.Document, page_no: int, ignore: tuple[str, ...] = ()) -> int:
    t = doc[page_no - 1].get_text()
    for w in ignore:
        t = t.replace(w, "")
    return len(t.strip())


def render_png(doc: pymupdf.Document, page_no: int, zoom: float = 2.0) -> bytes:
    return doc[page_no - 1].get_pixmap(matrix=pymupdf.Matrix(zoom, zoom)).tobytes("png")
