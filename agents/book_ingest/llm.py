"""Bước hiểu mục lục — chỗ duy nhất của agent cần mô hình ngôn ngữ.

Hai chế độ (docs/agent-hoc-tap/02 mục 4.2):
- manual: vẽ các trang đầu sách thành ảnh + ghi hướng dẫn, để Claude Code (qua skill
  book-ingest) hoặc người đọc mục lục và điền book.yaml. Không cần API key.
- api: gửi ảnh trang mục lục cho Claude qua SDK `anthropic`, nhận TocDraft đúng schema
  (structured outputs), rồi ghi bản nháp book.draft.yaml để người duyệt.
"""
from __future__ import annotations

import base64
import os
from pathlib import Path
from typing import Optional

import yaml

from . import pdfutil
from .schemas import TocDraft

DEFAULT_MODEL = "claude-opus-5-5"

PROMPT = """Đây là ảnh trang mục lục (Contents) của một giáo trình tiếng Anh.
Trích ra đúng cấu trúc theo schema:
- sections: từng Section của phần General Training theo thứ tự; mỗi unit gồm số unit, tên và số trang IN bắt đầu.
- review_no / review_printed_start: Review ở cuối section (nếu có).
- key_vocab_printed, answer_key_printed, tapescript_printed: [trang in đầu, trang in cuối] nếu có.
  Trang cuối = trang bắt đầu của mục kế tiếp − 1; mục cuối cùng thì để trang cuối bằng trang đầu.
- skip_titles: tên các phần không thuộc General Training (ví dụ "Academic section").
Chỉ dùng số trang in thấy trên ảnh, không đoán."""


def render_pages(pdf: Path, pages: list[int], out_dir: Path, zoom: float = 1.6) -> list[Path]:
    doc = pdfutil.open_pdf(str(pdf))
    out_dir.mkdir(parents=True, exist_ok=True)
    paths = []
    for p in pages:
        path = out_dir / f"page-{p:03d}.png"
        path.write_bytes(pdfutil.render_png(doc, p, zoom))
        paths.append(path)
    return paths


def manual(pdf: Path, pages: list[int], work: Path) -> Path:
    out = work / "profile"
    imgs = render_pages(pdf, pages, out)
    guide = out / "README.md"
    guide.write_text(
        "# Đọc mục lục để viết book.yaml\n\n"
        f"Ảnh các trang {pages} của `{pdf.name}` nằm cùng thư mục này: "
        + ", ".join(i.name for i in imgs) + ".\n\n" + PROMPT +
        "\n\nSau đó viết `book.yaml` theo mẫu `books/ielts_target_5_0/book.yaml`: điền `toc`, đo "
        "`page_offset` (so số in ở chân trang với số trang PDF), khai báo `files` và mẫu tên audio.\n",
        encoding="utf-8")
    return guide


def api(pdf: Path, pages: list[int], client=None, model: Optional[str] = None) -> TocDraft:
    if client is None:
        import anthropic  # extra [llm]
        client = anthropic.Anthropic()
    doc = pdfutil.open_pdf(str(pdf))
    content: list[dict] = []
    for p in pages:
        data = base64.standard_b64encode(pdfutil.render_png(doc, p, 1.6)).decode("ascii")
        content.append({"type": "image", "source": {"type": "base64", "media_type": "image/png", "data": data}})
    content.append({"type": "text", "text": PROMPT})
    resp = client.messages.parse(
        model=model or os.environ.get("BOOK_LLM_MODEL", DEFAULT_MODEL),
        max_tokens=16000,
        messages=[{"role": "user", "content": content}],
        output_format=TocDraft,
    )
    if getattr(resp, "stop_reason", None) == "refusal":
        raise RuntimeError("Claude từ chối yêu cầu đọc mục lục — dùng chế độ --llm manual.")
    if resp.parsed_output is None:
        raise RuntimeError(f"Không nhận được kết quả đúng schema (stop_reason={getattr(resp, 'stop_reason', None)}).")
    return resp.parsed_output


def draft_yaml(toc: TocDraft, files: dict, book_id: str) -> str:
    """Biến TocDraft thành bản nháp book.yaml — page_offset và mẫu tên audio vẫn phải kiểm tra tay."""
    data = {
        "book": book_id,
        "title": toc.title,
        "edition": "",
        "template": "target-gt-v1",
        "start_week": 6,
        "sessions_per_week": 6,
        "files": files,
        "modules": ["speaking-vocab", "listening", "reading", "writing", "consolidation", "exam-practice"],
        "toc": {
            "sections": [
                {"id": s.id, "title": s.title,
                 "units": [[u.no, u.title, u.printed_start] for u in s.units],
                 **({"review": [s.review_no, s.review_printed_start]} if s.review_no is not None else {})}
                for s in toc.sections
            ],
            **({"key_vocab": toc.key_vocab_printed} if toc.key_vocab_printed else {}),
            **({"answer_key": toc.answer_key_printed} if toc.answer_key_printed else {}),
            **({"tapescript": toc.tapescript_printed} if toc.tapescript_printed else {}),
        },
    }
    return ("# BẢN NHÁP do LLM đọc mục lục — kiểm tra page_offset, files và skip trước khi đổi tên thành book.yaml\n"
            + yaml.safe_dump(data, allow_unicode=True, sort_keys=False))
