"""Sách giả sinh lúc chạy test — không có trang sách thật nào trong test.

Bố cục giống IELTS Target 5.0 thu nhỏ: 2 section × 2 unit × 12 trang, mỗi module mở đầu
bằng một băng đỏ; Unit 4 cố ý có thêm một băng thừa. Answer key và Tapescript "đã OCR"
bằng cách ghi sẵn ocr-cache.json, nên test không cần cài OCR.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

import pymupdf
import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from book_ingest import pdfutil  # noqa: E402

OFFSET = 2
UNITS = [(1, "One", 3), (2, "Two", 15), (3, "Three", 31), (4, "Four", 43)]
REVIEWS = [(1, 27), (2, 55)]
LAYOUT = [0, 2, 4, 7, 9, 10]

PROFILE = """\
book: fake-book
title: Fake Book
template: target-gt-v1
start_week: 6
sessions_per_week: 6
files:
  course-book: {kind: pdf, path: course.pdf, page_offset: %(offset)d}
  audio:
    kind: audio
    dir: audio
    pattern: '^Unit(?P<unit>\\d+)_listening_(?P<part>\\d)(?P<ex>[A-Za-z]+)\\.mp3$'
modules: [speaking-vocab, listening, reading, writing, consolidation, exam-practice]
module_offsets: [0, 2, 4, 7, 9, 10]
toc:
  sections:
    - {id: S1, title: Section 1, units: [[1, One, 3], [2, Two, 15]], review: [1, 27]}
    - {id: S2, title: Section 2, units: [[3, Three, 31], [4, Four, 43]], review: [2, 55]}
  key_vocab: [59, 60]
  answer_key: [61, 62]
  tapescript: [63, 64]
missing: [work-book, test-books]
"""

# Dòng OCR giả: [x0, y0, x1, y1, chữ, độ tin]
ANSWER_PAGES = {
    61: [[.1, .10, .4, .12, "Unit 1, Listening 2A", .99], [.1, .50, .4, .52, "Unit 2, Reading 1B", .99],
         [.6, .10, .9, .12, "Unit 3, Listening 1C", .99]],
    62: [[.1, .10, .4, .12, "Unit 4, Writing A", .99], [.1, .60, .4, .62, "Academic section", .99],
         [.1, .70, .4, .72, "Unit 1, Reading 3A", .99]],
}
TAPESCRIPT_PAGES = {
    63: [[.1, .10, .3, .12, "Track 1", .99], [.1, .13, .4, .15, "Unit 1 Listening 1", .99],
         [.1, .16, .6, .18, "CNow listen and check your ideas.", .99],
         [.1, .50, .4, .52, "Unit 2-Listening 1", .99], [.1, .53, .6, .55, "B Listen again", .99]],
    64: [[.1, .10, .4, .12, "Unit 3Listening1", .99], [.1, .13, .6, .15, "AListen and complete", .99],
         [.6, .10, .9, .12, "Unit 4 Listening 2", .99], [.6, .13, .9, .15, "Pronunciation check", .99],
         [.6, .80, .9, .82, "TEST 1", .99]],
}


def mp3(seconds: float) -> bytes:
    """MP3 hợp lệ tối thiểu: các khung MPEG-1 Layer III 128 kbps, 44.1 kHz chứa toàn số 0."""
    frame = b"\xff\xfb\x90\x64" + b"\x00" * 413
    return frame * max(1, int(seconds * 44100 / 1152))


def make_book(root: Path, offset: int = OFFSET, extra_banner: bool = True) -> Path:
    root.mkdir(parents=True, exist_ok=True)
    doc = pymupdf.open()
    last_printed = 64
    banners = set()
    for _, _, start in UNITS:
        banners |= {start + o for o in LAYOUT}
    if extra_banner:
        banners.add(43 + 11)
    for _, start in REVIEWS:
        banners |= {start, start + 2}
    for pdf_page in range(1, last_printed + OFFSET + 1):
        page = doc.new_page(width=595, height=842)
        printed = pdf_page - OFFSET
        if printed in banners:
            page.draw_rect(pymupdf.Rect(40, 10, 300, 40), color=(0.85, 0.1, 0.1), fill=(0.85, 0.1, 0.1))
        page.insert_text((60, 420), f"printed page {printed}", fontsize=14)
    doc.save(str(root / "course.pdf"))
    (root / "book.yaml").write_text(PROFILE % {"offset": offset}, encoding="utf-8")

    audio = root / "audio"
    audio.mkdir()
    names = ("Unit1_listening_1c.mp3", "Unit2_listening_1b.mp3", "Unit3_listening_1a.mp3",
             "Unit4_listening_2pro.mp3", "random.mp3")
    for k, name in enumerate(names):          # độ dài khác nhau để không bị coi là file trùng
        (audio / name).write_bytes(mp3(3 + k))

    sha = pdfutil.sha256_file(root / "course.pdf")
    cache = {}
    for printed, lines in {**ANSWER_PAGES, **TAPESCRIPT_PAGES}.items():
        cache[f"course-book:{sha[:12]}:{printed + OFFSET}"] = lines
    (root / "work").mkdir()
    (root / "work" / "ocr-cache.json").write_text(json.dumps(cache), encoding="utf-8")
    pdfutil.open_pdf.cache_clear()
    return root


@pytest.fixture
def fake_book(tmp_path: Path) -> Path:
    return make_book(tmp_path / "fake-book")
