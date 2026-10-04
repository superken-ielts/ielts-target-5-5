"""OCR tùy chọn, có cache.

Sách scan không có lớp chữ, nên muốn tìm tiêu đề "Unit 4, Listening 2A" trong Answer key
hay Tapescript thì phải OCR. OCR chậm (vài giây mỗi trang) và cần gói `rapidocr-onnxruntime`
(extra `[ocr]`), nên kết quả được lưu theo khóa (file, sha256, trang) trong work/ocr-cache.json.
Máy không cài OCR vẫn chạy lại được pipeline nhờ cache; trang chưa có trong cache thì
trả về None và bước gọi sẽ dùng giá trị dự phòng.
"""
from __future__ import annotations

import json
from pathlib import Path
from typing import Optional

import pymupdf

Line = list  # [x0, y0, x1, y1, text, conf] — toạ độ theo tỷ lệ 0..1 của trang


class OcrCache:
    def __init__(self, path: Path):
        self.path = Path(path)
        self.data: dict[str, list[Line]] = {}
        if self.path.exists():
            self.data = json.loads(self.path.read_text(encoding="utf-8"))
        self._engine = None
        self._engine_failed = False
        self.dirty = False

    def key(self, file_id: str, sha: str, page_no: int) -> str:
        return f"{file_id}:{sha[:12]}:{page_no}"

    def _get_engine(self):
        if self._engine is None and not self._engine_failed:
            try:
                from rapidocr_onnxruntime import RapidOCR  # type: ignore
                self._engine = RapidOCR()
            except Exception:
                self._engine_failed = True
        return self._engine

    @property
    def available(self) -> bool:
        return self._get_engine() is not None

    def lines(self, doc: pymupdf.Document, file_id: str, sha: str, page_no: int,
              allow_run: bool = True) -> Optional[list[Line]]:
        k = self.key(file_id, sha, page_no)
        if k in self.data:
            return self.data[k]
        if not allow_run:
            return None
        engine = self._get_engine()
        if engine is None:
            return None
        import numpy as np  # chỉ cần khi thật sự chạy OCR

        page = doc[page_no - 1]
        pix = page.get_pixmap(matrix=pymupdf.Matrix(2, 2))
        img = np.frombuffer(pix.samples, dtype=np.uint8).reshape(pix.height, pix.width, pix.n)[:, :, :3]
        res, _ = engine(img)
        out: list[Line] = []
        for box, text, conf in res or []:
            xs = [p[0] for p in box]
            ys = [p[1] for p in box]
            out.append([round(min(xs) / pix.width, 4), round(min(ys) / pix.height, 4),
                        round(max(xs) / pix.width, 4), round(max(ys) / pix.height, 4),
                        str(text), round(float(conf), 3)])
        self.data[k] = out
        self.dirty = True
        return out

    def save(self) -> None:
        if self.dirty:
            self.path.parent.mkdir(parents=True, exist_ok=True)
            self.path.write_text(json.dumps(self.data, ensure_ascii=False, sort_keys=True, separators=(",", ":")),
                                 encoding="utf-8")
            self.dirty = False


def reading_order(lines: list[Line], columns: int = 2) -> list[Line]:
    """Sắp dòng theo thứ tự đọc của trang hai cột: hết cột trái rồi tới cột phải."""
    def col(l: Line) -> int:
        cx = (l[0] + l[2]) / 2
        return min(columns - 1, int(cx * columns))
    return sorted(lines, key=lambda l: (col(l), l[1], l[0]))
