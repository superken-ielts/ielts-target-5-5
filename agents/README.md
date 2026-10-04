# agents/ — agent nhập sách

`book_ingest` biến một bộ sách (PDF + audio) thành ba file mà app học đọc được:

| File | Nội dung |
|---|---|
| `book.json` | Sách → section → unit/review/test → hoạt động (module, trang PDF, track, trang đáp án, trang tapescript) |
| `plan.json` | 120 phiên học theo thứ tự, mỗi phiên trỏ tới hoạt động, kèm tuần dự kiến |
| `report.md` | Tóm tắt cho người đọc: file, cấu trúc, mục đã duyệt |

Agent chỉ phục vụ việc nhập sách. Thiết kế đầy đủ ở `docs/agent-hoc-tap/`.

## Chạy

```bash
cd agents
pip install -e '.[ocr,dev]'
python -m book_ingest ingest ../books/ielts_target_5_0
python -m book_ingest validate ../books/ielts_target_5_0
python -m pytest -q
```

Không cài gì cũng chạy được bằng `PYTHONPATH=agents python3 -m book_ingest …` nếu đã có
`pymupdf pyyaml pydantic mutagen`.

## Các bước

| Bước | Module | Làm gì | AI |
|---|---|---|---|
| inventory | `scan.py` | Liệt kê file, số trang, lớp chữ, độ dài audio — không in nội dung | không |
| profile | `llm.py` | Đọc trang mục lục → `book.yaml`. `manual`: Claude Code đọc ảnh; `api`: Claude qua SDK, structured output | có |
| scan | `scan.py` | sha256, file trùng, lớp chữ, độ dài audio → `work/scan.json` | không |
| structure | `structure.py` | Trang mở đầu module nhận ra bằng băng tiêu đề đỏ; kiểm tra độ lệch trang; OCR tiêu đề Answer key, Tapescript → `work/structure.json` | OCR |
| match | `audio.py` | Ghép file audio theo mẫu tên, gắn trang tapescript từng track → `work/match.json` | không |
| review | `review.py` | Gộp mục chưa chắc vào `work/review.json`, giữ quyết định cũ, dừng nếu còn mục mở | không |
| plan / pack | `templates.py`, `pipeline.py` | Áp mẫu phiên `target-gt-v1`, ghi `book.json`, `plan.json`, `report.md` | không |
| validate | `validate.py` | Schema + kiểm tra V3, V4, V5, V7, V8 | không |

## Mã thoát

`0` xong · `2` còn mục cần duyệt · `3` gói không qua kiểm tra.
