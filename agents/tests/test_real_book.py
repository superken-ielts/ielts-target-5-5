"""Hồi quy trên bộ sách thật trong repo (books/ielts_target_5_0) nếu có.

Chạy lại pipeline vào một thư mục tạm (file sách được liên kết, không chép) chỉ bằng cache
OCR đã commit, rồi so với book.json / plan.json đã commit: đầu ra phải giống hệt.
"""
import shutil
from pathlib import Path

import pytest

from book_ingest import pipeline, validate as vd

BOOK = Path(__file__).resolve().parents[2] / "books" / "ielts_target_5_0"
pytestmark = pytest.mark.skipif(not (BOOK / "book.json").exists(), reason="không có sách thật trong repo")


def test_committed_package_is_valid():
    assert vd.validate(BOOK) == []
    s = vd.summary(BOOK)
    assert (s["units"], s["reviews"], s["tests"], s["sessions"], s["tracks"]) == (15, 3, 3, 120, 59)
    assert s["weeks"] == [6, 25]


def test_pipeline_reproduces_committed_package(tmp_path):
    work = tmp_path / "book"
    work.mkdir()
    for p in BOOK.iterdir():
        if p.name in ("book.yaml",):
            shutil.copy(p, work / p.name)
        elif p.name == "work":
            (work / "work").mkdir()
            for f in ("ocr-cache.json", "review.json", "chunks.json"):   # chunks.json: dùng lại đoạn PDF có sẵn
                shutil.copy(p / f, work / "work" / f)
        elif p.name not in ("book.json", "plan.json", "report.md", ".DS_Store"):
            (work / p.name).symlink_to(p)
    res = pipeline.run(work, allow_ocr=False, say=lambda m: None)
    assert res.code == pipeline.OK, res.messages
    for name in ("book.json", "plan.json"):
        assert (work / name).read_text() == (BOOK / name).read_text(), name
