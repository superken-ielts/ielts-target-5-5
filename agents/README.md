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

## Video bài giảng — `lesson_video`

Công cụ riêng, không thuộc agent nhập sách: biến một kịch bản YAML hai người nói thành video MP4 để gắn vào
một hoạt động của sách.

```bash
cd agents
python -m lesson_video check ../books/ielts_target_5_0/lessons/*.yaml
python -m lesson_video build ../books/ielts_target_5_0/lessons/U01-speaking-1.yaml
python -m lesson_video build <kịch bản> --engine silent --out /tmp/xem-thu --work /tmp/khung   # xem bố cục nhanh, không giọng
```

Cần `pymupdf pyyaml pydantic pillow numpy` (`pip install -e '.[video]'`), `ffmpeg`, và thư viện **Flite** cho giọng đọc
(miễn phí, chạy offline; Ubuntu/Debian `sudo apt install libflite1`, macOS `brew install flite`). Giọng dùng:
`slt` (nữ, Mỹ) cho cô giáo, `rms` (nam, Mỹ) cho học viên; có thêm `awb`, `kal16`.

| Bước | Module | Làm gì |
|---|---|---|
| kịch bản | `script.py` | Đọc và kiểm tra YAML: người nói, cảnh (`title`, `bullets`, `vocab`, `match`, `pairs`, `qa`, `compare`, `errors`, `practice`), dòng thoại (`say` = cách đọc khác chữ hiển thị, `vi` = phụ đề tiếng Việt, `focus`, `reveal`, `wait` = đếm ngược để người học tự nói); đối chiếu `activity` với `book.json` |
| giọng đọc | `tts.py` | Flite qua `ctypes`; `silent` để thử nhanh và để test |
| dòng thời gian | `timeline.py` | Đọc từng câu, chuẩn hóa âm lượng hai giọng, ghép thành một dải tiếng; mỗi câu một khung hình, đếm ngược mỗi giây một khung; chương theo cảnh |
| slide | `slides.py` | Pillow vẽ 1280×720: thanh đầu, nội dung theo kiểu cảnh (ảnh cắt từ trang sách cho bài nối tranh), phụ đề người nói, thanh tiến độ |
| video | `video.py` | ffmpeg ghép ảnh + tiếng → H.264/AAC có chương; ghi `books/<sách>/lessons/lessons.json` (id, hoạt động, unit, thời lượng, chương, giọng) |

Sửa kịch bản `.yaml` rồi chạy lại `build`; không sửa tay `lessons.json` hay file `.mp4`. Thêm video mới: viết
`books/<sách>/lessons/<id>.yaml` với `activity` là id hoạt động trong `book.json`, chạy `build`, rồi `python3 web/build.py`.

