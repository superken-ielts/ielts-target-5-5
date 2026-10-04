---
name: book-ingest
description: Nhập một bộ sách (PDF + audio) thành book.json và plan.json cho tab Sách của app học. Dùng khi người dùng thêm sách mới vào books/, muốn chạy lại agent nhập sách, sửa hồ sơ book.yaml, hoặc giải các mục trong hộp duyệt (work/review.json).
---

# Agent nhập sách

Agent chỉ làm một việc: biến thư mục `books/<sách>/` (PDF, MP3) thành `book.json`, `plan.json`,
`report.md` để app hiện menu học theo lộ trình. Code ở `agents/book_ingest/`, hợp đồng dữ liệu ở
`docs/agent-hoc-tap/02-kien-truc-va-hop-dong-du-lieu.md` mục 3.

## Chuẩn bị

```bash
cd agents
pip install -e '.[ocr,dev]'      # hoặc: uv pip install -e '.[ocr,dev]'
```

`ocr` (rapidocr-onnxruntime) chỉ cần khi sách là bản scan và chưa có `work/ocr-cache.json`.

## Sách mới

1. `python -m book_ingest inventory ../books/<sách>` — xem file nào có, PDF có lớp chữ không.
2. Tìm trang mục lục, rồi viết hồ sơ:
   - `python -m book_ingest profile ../books/<sách> --pdf <file.pdf> --pages 1-8` vẽ các trang
     đầu ra `work/profile/`. Đọc ảnh trang Contents và viết `book.yaml` theo mẫu
     `books/ielts_target_5_0/book.yaml`: `toc` (số trang IN), `files`, `page_offset`, mẫu tên audio.
   - Hoặc `--llm api` (cần `ANTHROPIC_API_KEY` và extra `[llm]`) để Claude đọc mục lục và ghi
     `book.draft.yaml`; vẫn phải kiểm tra `page_offset`, `files` trước khi đổi tên thành `book.yaml`.
3. `python -m book_ingest ingest ../books/<sách>`.

## Hộp duyệt

`ingest` thoát mã 2 khi còn mục chưa chắc. Xem bằng `python -m book_ingest review ../books/<sách> --list`.

- Mở trang được nêu trong `evidence` (vẽ bằng PyMuPDF) để kiểm tra trước khi quyết.
- Đồng ý đề xuất: `review --accept-all` (chỉ khi đã kiểm tra từng mục) hoặc `review` để hỏi từng mục.
- Sửa giá trị: ghi `"decision": {"value": {...}}` vào mục đó trong `work/review.json`.
- Chạy lại `ingest`; quyết định được giữ theo `id` của mục.

Mục `info` không chặn đóng gói. Không tự sửa số liệu trong `book.json` — sửa `book.yaml` hoặc quyết
định trong `review.json` rồi chạy lại.

## Sau khi đóng gói

1. `python -m book_ingest validate ../books/<sách>` phải ra `OK`.
2. `python3 web/build.py` để nhúng book.json/plan.json vào app (tab Sách).
3. `cd agents && python -m pytest -q`.
4. Commit `book.yaml`, `book.json`, `plan.json`, `report.md`, `work/` (cache OCR giúp người khác chạy lại
   không cần OCR) và hai bản dựng của `web/`.

## Mẫu phiên

Chỉ có `target-gt-v1` (IELTS Target 5.0 GT: 7 phiên/unit, 2/review, 3/test). Sách có cấu trúc khác cần
thêm mẫu trong `agents/book_ingest/templates.py` và luật đếm phiên trong `validate.py`.
