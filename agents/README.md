# agents/ — agent nhập sách

`book_ingest` biến một bộ sách (PDF + audio) thành ba file mà app học đọc được:

| File | Nội dung |
|---|---|
| `book.json` | Sách → section → unit/review/test → hoạt động (module, trang PDF, track, trang đáp án, trang tapescript) |
| `plan.json` | 120 phiên học theo thứ tự, mỗi phiên trỏ tới hoạt động, kèm tuần dự kiến |
| `report.md` | Tóm tắt cho người đọc: file, cấu trúc, mục đã duyệt |

Agent chỉ phục vụ việc nhập sách. Thiết kế đầy đủ ở `docs/agent-hoc-tap/`.

Hai mẫu (`template` trong `book.yaml`):

| Mẫu | Sách | Cách dựng |
|---|---|---|
| `target-gt-v1` | IELTS Target 5.0 (`books/ielts_target_5_0`) | Đủ các bước ở bảng dưới: tìm trang mở đầu module bằng băng đỏ, OCR đáp án / tapescript, ghép audio theo mẫu tên, hộp duyệt |
| `lessons-v1` | GENKI I · lộ trình JLPT N5 (`books/Genki`) | Không đoán cấu trúc. Các bước học (`steps`) và chỗ trong sách của từng bước (`refs`: trang in, khoảng track `K01-09..K01-23`, trang Workbook `alt`) khai hết trong `book.yaml`. Agent chỉ quét file, cắt PDF thành đoạn theo từng bài, kiểm tra mỗi track thuộc đúng một phiên. Không có `files` thì thành lộ trình chỉ có ghi chú (`agents/book_ingest/lessons.py`, `docs/agent-hoc-tap/07-lo-trinh-n5-tieng-nhat.md` mục 3) |

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
python -m lesson_video coverage ../books/ielts_target_5_0 --unit U01   # phần nào của unit đã có video, phần nào chưa
python -m lesson_video prune ../books/Genki   # bỏ khỏi lessons.json (và xóa .mp4) những video không còn kịch bản
```

Quy trình đầy đủ, bảng cách đọc `say` và kế hoạch các unit tiếp theo: `docs/agent-hoc-tap/06-video-bai-giang.md`.

Cần `pymupdf pyyaml pydantic pillow numpy` (`pip install -e '.[video]'`) và `ffmpeg`. Giọng đọc (đều miễn phí, offline):

| Bộ đọc | Cài | Giọng trong kịch bản Unit 1 |
|---|---|---|
| **Kokoro-82M** (mặc định, Apache-2.0) | `pip install -e '.[kokoro]'`; tải từ Hugging Face `onnx-community/Kokoro-82M-v1.0-ONNX` file `onnx/model_quantized.onnx` (bản nén q8, ~92 MB) và các file giọng `voices/<giọng>.bin` (~0,5 MB mỗi giọng), đặt vào `~/.cache/lesson_video/kokoro/` (giọng trong thư mục `voices/`) hoặc chỉ đường bằng `--model`, `--voices` / biến `KOKORO_MODEL`, `KOKORO_VOICES` | Emma `af_heart` (nữ, Mỹ), Tom `am_michael` (nam, Mỹ) |
| Flite (dự phòng, nghe máy) | Ubuntu/Debian `sudo apt install libflite1`, macOS `brew install flite` | Emma `slt`, Tom `rms` |

Máy nào chặn Hugging Face thì lấy cùng các file đó từ npm:
- **Model:** gói `kokoro-q8-shards@1.0.0`, ghép 6 mảnh thành `model_quantized.onnx`.
- **Giọng:** thư mục `voices/` của gói `kokoro-js@1.2.1` (54 giọng, có `bf_emma`, `jf_alpha`).

**Video tiếng Nhật (lộ trình N5).** Người nói khai `lang: ja` với giọng Kokoro `jf_*` / `jm_*` (Yuki `jf_alpha`), cần
thêm hai thứ:
- `misaki[ja]` — bộ tách âm tiếng Nhật Kokoro dùng khi huấn luyện:
  `uv pip install --system --break-system-packages "misaki[ja]==0.7.4"` hoặc `pip install -e '.[ja]'`. Trên Debian,
  `pip` thường lỗi khi dựng `unidic-lite`; dùng `uv`.
- Phông Noto Sans CJK: `sudo apt install fonts-noto-cjk`; trên macOS dùng Hiragino.

Chữ Nhật viết furigana `{漢字|かな}`. Lệnh `check` so cách đọc của misaki với furigana, so `romaji`, chặn chữ Latin
trong câu Nhật. Chỗ bộ đọc sai (九時 → きゅうじ) thì viết `say` bằng kana. Tốc độ đặt riêng được: `speed` của người
nói hoặc của từng dòng.

`--engine auto` (mặc định) dùng Kokoro khi tìm thấy model và giọng, không thì Flite. Giọng khai theo bộ đọc:
`voice: {kokoro: af_heart, flite: slt}`. Giọng Kokoro tiếng Anh: `af_*`, `am_*` (Mỹ), `bf_*`, `bm_*` (Anh); giọng `b*`
được tách âm kiểu Anh. `--speed 0.9` (mặc định) đọc chậm hơn bình thường 10%. Tiếng từng câu lưu ở
`~/.cache/lesson_video/tts/` theo (bộ đọc, giọng, chữ), nên sửa vài câu rồi dựng lại chỉ đọc lại những câu đó.

Chữ cái, tên riêng hay bị đọc sai: viết cách đọc vào `say`, kiểm tra được với cả hai bộ đọc — chữ "A" viết `eigh`,
"IELTS" viết `eye-elts`, Huế `Whey`, Đà Lạt `Dah Lot`, Hồ Chí Minh `Ho Chee Min`.

| Bước | Module | Làm gì |
|---|---|---|
| kịch bản | `script.py` | Đọc và kiểm tra YAML: người nói, cảnh (`title`, `bullets`, `vocab`, `match` (`image.grid: 4` xếp dải tranh thành lưới 2×2), `pairs`, `qa`, `compare`, `errors`, `practice`, `jp` = thẻ ba tầng cho câu tiếng Nhật — một hoặc nhiều mục, mỗi mục `jp` (furigana `{漢字|かな}`), `romaji`, `en`, `vi`; dòng thoại chọn mục bằng `focus`, `quiz: true` = thẻ đề không kiểm cách đọc, `order` = sắp xếp thứ tự (`label: ""` khi mục không có chữ cái), `blanks` = nghe – chép vào ô trống (mục có `q` chứa `___` thì là câu điền từ, `hint` = từ gốc), `mcq` = trắc nghiệm a/b/c (`keys: [1, 2, 3]` để đổi nhãn), `passage` = bài đọc trên màn hình kèm phụ đề (dòng thoại `mark: [cụm từ]` tô vàng chỗ cần dò), `timing` = chia thời gian, `letter` = thư mẫu cả trang; mục `body: false` không tính vào số từ, `shadow` = nghe – nhắc lại: câu mẫu chữ to theo màu người nói `by`, kèm `vi`, `tip`), dòng thoại (`say` = cách đọc khác chữ hiển thị, `vi` = phụ đề tiếng Việt, `focus`, `reveal`, `wait` = đếm ngược để người học tự nói, `echo: true` = sau câu có khoảng lặng đếm ngược dài theo câu để người học nhắc lại (shadowing), `read: <người nói>` = đọc nguyên một đoạn thư); trường cảnh `hide_text: true` (bài nghe: phụ đề chỉ hiện người nói), `roles` (vai trong cảnh, ví dụ lễ tân / khách) và `words` (số từ của thư chia hai trang); dòng `track: <mã file audio trong book.json>` (+ `start`, `end`, `note`) phát file nghe của sách ngay trong video; đối chiếu `activity` với `book.json` |
| giọng đọc | `tts.py` | Kokoro qua `kokoro-onnx`; Flite qua `ctypes`; `silent` để thử nhanh và để test |
| dòng thời gian | `timeline.py` | Đọc từng câu, chuẩn hóa âm lượng các giọng, ghép thành một dải tiếng; đoạn `track` cắt file nghe của sách bằng ffmpeg rồi ghép vào cùng dải; mỗi câu một khung hình, đếm ngược mỗi giây một khung; chương theo cảnh |
| độ phủ | `coverage.py` | Bảng phần nào của unit đã có video, phần nào chưa, kịch bản chưa dựng (lệnh `coverage`) |
| slide | `slides.py` | Pillow vẽ 1280×720: thanh đầu, nội dung theo kiểu cảnh (ảnh cắt từ trang sách cho bài nối tranh), phụ đề người nói, thanh tiến độ |
| video | `video.py` | Chuẩn độ to lời nói (-16 LUFS) ở một lệnh ffmpeg riêng, rồi ghép ảnh + tiếng → H.264/AAC có chương; ghi `books/<sách>/lessons/lessons.json` (id, hoạt động, unit, thời lượng, chương, giọng) |
| tiếng Nhật | `ja.py`, `jpcard.py` | Furigana, cách đọc, romaji, gọi misaki; vẽ cảnh `jp` (chữ trộn CJK + Latin, furigana, ngắt dòng có kinsoku) |

Sửa kịch bản `.yaml` rồi chạy lại `build`; không sửa tay `lessons.json` hay file `.mp4`. Thêm video mới: viết
`books/<sách>/lessons/<id>.yaml` với `activity` là id hoạt động trong `book.json`, chạy `build`, rồi `python3 web/build.py`.
Bỏ một video: xóa `.yaml`, chạy `prune`, rồi `python3 web/build.py`.

