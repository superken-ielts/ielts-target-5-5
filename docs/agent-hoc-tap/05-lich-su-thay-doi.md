# 05 — Lịch sử thay đổi

Ghi lại từng đợt triển khai: thêm, sửa, xóa file nào và vì sao. Trạng thái từng task ở
[04-checklist.md](04-checklist.md).

---

## Đợt 6 — 06/10/2026: video Unit 1 Writing 3; Workbook trang 6

Nhánh `claude/gallant-ramanujan-ym30oy` đặt lại từ `main` tại `1d204cc` (đã merge PR #6).

### Yêu cầu

Tạo video hướng dẫn học và giải bài Writing 3 (sách in trang 18); hướng dẫn tới Workbook trang 6 để giải các bài tập
Workbook; xong thì tạo PR.

### Đã làm

| Việc | Cách làm |
|---|---|
| **Writing 3: organizing points in a personal letter** (8:30, 10 chương, 7,6 MB) | 9 từ mới (host family, appearance, personality, outgoing, generous, stubborn…) · **Bài A**: chọn ý cho thư giới thiệu bản thân gửi gia đình ở Anh (nên viết / bỏ qua hoặc một câu — bài mở, nói rõ không có một đáp án duy nhất) · **Bài B**: Tom đọc thư của Bruno (còn trống lời chào, lời kết), rồi sắp xếp 9 ý theo thứ tự xuất hiện (tên → tuổi → nơi ở → gia đình → việc học → sở thích → âm nhạc → tính cách → lý do học tiếng Anh; Bruno không nói ngoại hình, món ăn) · cách Bruno gom ý thành 4 đoạn · **Bài C**: Dear Mr and Mrs Gray … Best wishes / Kind regards (Yours sincerely đúng nhưng hơi trang trọng; không dùng Yours faithfully, Love, Hi) và đọc lại thư đã điền · **Thư mẫu của Lan** (sinh viên Việt Nam, 156 từ) cùng dạng đề, chia đoạn như Bruno · cách làm bài viết Workbook trang 6 theo 5 bước |
| Workbook trang 6 | **Chưa giải được**: bộ sách đã nhập không có Workbook (`book.yaml › missing: [work-book, test-books]`). Video chỉ hướng dẫn cách làm bài viết mà sách in yêu cầu ("Go to Workbook page 6 for the writing task"), không đoán nội dung đề. Ghi task P2-36: cần file Workbook hoặc ảnh trang 6 |
| Gắn vào app | Hoạt động `U01-writing` nay có 3 video; thẻ Unit 1 có 5 nút video |

Đáp án bài A, B, C là gợi ý (Answer key không có Unit 1 Writing). Thư của Bruno là văn bản trong sách (trang 18).

### File thêm

| File | Vai trò |
|---|---|
| `books/ielts_target_5_0/lessons/U01-writing-3.yaml` | Kịch bản video Writing 3 |
| `books/ielts_target_5_0/lessons/U01-writing-3.mp4` | Video 1280×720, H.264 + AAC, có chương, tiếng chuẩn -16 LUFS |

### File sửa

| File | Thay đổi |
|---|---|
| `books/ielts_target_5_0/lessons/lessons.json` | Thêm mục Writing 3 |
| `tests/web/book-core.test.mjs`, `tests/web/book.e2e.mjs` | Unit 1 có 5 video; phiên Writing có 3 video |
| `agents/README.md`, `web/README.md`, `docs/agent-hoc-tap/04-checklist.md`, `README.md` (thư mục docs) | Ghi chú `body: false`; video Writing 1–3; task P2-35, P2-36; trạng thái |
| `web/index.html`, `web/ielts-companion.html` | Bản dựng lại |

Không xóa file nào. Mã `agents/lesson_video` không đổi.

### Kiểm thử

| Lệnh | Kết quả |
|---|---|
| `cd agents && python -m pytest -q` | 38 passed (hồi quy: 5 kịch bản khớp `lessons.json`) |
| `node --test "tests/web/*.test.mjs"` | 13 passed |
| `node tests/web/book.e2e.mjs` | 12/12 bước OK |
| `ffprobe` / `volumedetect` / khung hình trích từ MP4 | Thời lượng khớp lời thoại, 10 chương; tiếng trung bình -17,4 dB, đỉnh -0,6 dB |

---

## Đợt 5 — 06/10/2026: video Unit 1 Writing 1 và Writing 2

Nhánh `claude/gallant-ramanujan-ym30oy` đặt lại từ `main` tại `da67bcb` (đã merge PR #5).

### Yêu cầu

Tạo hai video hướng dẫn cho Writing 1 và Writing 2 của Unit 1 (sách in trang 17–18); hướng dẫn xong thì mỗi video đọc
luôn một đoạn ví dụ; rồi tạo PR.

### Đã làm

| Video | Nội dung |
|---|---|
| **Writing 1: organizing your writing** (7:08, 12 chương, 6,3 MB) | Giới thiệu Task 1 (thư ≥ 150 từ, ~20 phút) · 8 từ mới · Exam tip · Bài A: sắp xếp 6 bước (c → a → e → f → d → b, đáp án gợi ý vì Answer key không có) · Bài B: chia 20 phút (1 + 2 + 1 + 2 phút chuẩn bị, 11 phút viết, 3 phút soát lỗi) · **Ví dụ đi qua đủ 6 bước** với đề "chuyển tới thành phố mới, viết thư cho bạn": đọc đề, ghi ý, chọn ý, dàn ý theo đoạn, **Tom đọc thư mẫu thân mật 160 từ**, soát lỗi · Tổng kết + bài về nhà |
| **Writing 2: types of letter / starting and ending letters** (7:58, 10 chương, 7,1 MB) | 9 từ mới · Bài A: 6 loại thư ↔ câu mở đầu A–F (1-D, 2-F, 3-E, 4-A, 5-B, 6-C, đáp án gợi ý) · Bài B: 6 cụm từ mở đầu, đếm ngược để viết lại theo trí nhớ · Bài C: cách kết 1–5 ↔ thư A–F (thư F không có cách kết → Yours sincerely) · Bài D: Yours faithfully / Yours sincerely, Best wishes / Regards, các cách kết thân mật · **Emma đọc thư mẫu trang trọng hỏi thông tin 154 từ** (Dear Sir/Madam … Yours faithfully) · Tổng kết + bài về nhà (viết lại cho Ms Taylor → Yours sincerely) |
| Gắn vào app | Hoạt động `U01-writing` (phiên 4 "Writing: học kỹ năng" và phiên 5 "Writing: chấm, viết lại"); thẻ Unit 1 nay có 4 nút video |
| Kiểu cảnh mới | `order` (sắp xếp: số thứ tự hiện dần, cột phải dựng thứ tự đúng), `timing` (thanh ngang chia phút, mở dần từng bước), `letter` (cả lá thư trên một trang, đoạn đang đọc tô màu, ghi chú vai trò từng đoạn ở lề, đếm từ, không có thanh phụ đề); dòng `read: <người nói>` đọc nguyên một đoạn thư (lấy cả `say` của đoạn); hàng của `pairs` được xuống hai dòng |

Giọng: Kokoro q8, Emma `af_heart`, Tom `am_michael` như đợt 4; cách đọc trong `say` soát lại với Kokoro
(Sir/Madam → "Sir or Madam", 150 → "a hundred and fifty", chữ cái A → `eigh`).

### File thêm

| File | Vai trò |
|---|---|
| `books/ielts_target_5_0/lessons/U01-writing-1.yaml`, `U01-writing-2.yaml` | Kịch bản hai video |
| `books/ielts_target_5_0/lessons/U01-writing-1.mp4`, `U01-writing-2.mp4` | Video 1280×720, H.264 + AAC, có chương, tiếng chuẩn -16 LUFS |

### File sửa

| File | Thay đổi |
|---|---|
| `agents/lesson_video/script.py` | Kiểu cảnh `order`, `timing`, `letter`; dòng `read`; kiểm tra `pos` 1…n, `read` chỉ trong cảnh letter kèm `focus`, cảnh letter không có `wait` |
| `agents/lesson_video/slides.py` | Vẽ ba kiểu cảnh mới; cảnh letter bỏ thanh phụ đề; ô chữ hai dòng cho `pairs`, `order` |
| `agents/tests/test_lesson_video.py` | +7 test: ba kiểu cảnh mới dựng và vẽ được, dòng `read` lấy đúng chữ và cách đọc, 6 kịch bản sai bị chặn |
| `books/ielts_target_5_0/lessons/lessons.json` | Thêm hai mục Writing |
| `tests/web/book-core.test.mjs`, `tests/web/book.e2e.mjs` | Unit 1 có 4 video; mở video Writing từ thẻ unit vào đúng phiên Writing |
| `agents/README.md`, `web/README.md`, `docs/agent-hoc-tap/04-checklist.md`, `README.md` (thư mục docs) | Kiểu cảnh mới; video Writing trong tab Sách; task P2-34; trạng thái |
| `web/index.html`, `web/ielts-companion.html` | Bản dựng lại |

Không xóa file nào.

### Kiểm thử

| Lệnh | Kết quả |
|---|---|
| `cd agents && python -m pytest -q` | 38 passed |
| `node --test "tests/web/*.test.mjs"` | 13 passed |
| `node tests/web/book.e2e.mjs` | 12/12 bước OK |
| `ffprobe` / `volumedetect` / khung hình trích từ MP4 | Thời lượng khớp lời thoại, đủ chương; tiếng trung bình ~-18 dB, đỉnh dưới 0 dB; thư mẫu và các cảnh mới hiển thị đúng |

---

## Đợt 4 — 05/10/2026: giọng Kokoro cho video bài giảng

Nhánh `claude/gallant-ramanujan-ym30oy` đặt lại từ `main` tại `8dd99b8` (đã merge PR #4).

### Yêu cầu

Giọng Flite nghe dở; gợi ý giọng miễn phí khác. Người dùng chọn **Kokoro bản q8**.

### Đã làm

| Việc | Cách làm |
|---|---|
| Lấy model | Hugging Face bị chặn bởi chính sách mạng của môi trường cloud → dùng bản q8 trong gói npm `kokoro-q8-shards` (6 mảnh ghép lại, sha256 `fbae9257…a1478` khớp mã gói ghi; bản gốc là `model_quantized.onnx` của `onnx-community/Kokoro-82M-v1.0-ONNX`) và file giọng trong gói npm `kokoro-js` (thư mục `voices/`, 28 giọng tiếng Anh, ~0,5 MB mỗi giọng). Không commit model hay giọng: đặt ở `~/.cache/lesson_video/kokoro/` |
| Bộ đọc Kokoro | `tts.Kokoro` qua thư viện `kokoro-onnx` 0.6: đọc 24 kHz, giọng `b*` tách âm `en-gb`, còn lại `en-us`; tốc độ 0,9. `--engine auto` chọn Kokoro khi tìm thấy model + giọng (tham số, biến môi trường hoặc thư mục mặc định), không thì Flite và báo lý do |
| Chọn giọng | Video mẫu 53 giây với 4 cặp (bf_emma + am_michael · af_heart + am_michael · bf_emma + bm_george · af_bella + am_fenrir). Người dùng nghe mẫu và chọn **cặp 2**: Emma `af_heart` (nữ, giọng Mỹ), Tom `am_michael` (nam, giọng Mỹ). Lượt dựng đầu bằng cặp 1 (`bf_emma`) dừng giữa chừng; câu của Tom đã đọc dùng lại từ bộ nhớ tiếng |
| Kịch bản | `voice` khai theo bộ đọc `{kokoro: …, flite: …}`. Soát cách Kokoro tách âm: `ay` (đã dùng cho Flite) bị đọc thành "eye", `Hway` thành "aitch-way" → đổi sang `eigh`, `Whey` (đúng ở cả hai bộ đọc) |
| Dựng lại nhanh | Tiếng từng câu lưu ở `~/.cache/lesson_video/tts/` theo (bộ đọc, giọng, chữ); dựng lại chỉ đọc câu đã đổi. Kokoro trên CPU 4 nhân chậm hơn thời gian thật một chút (~5 giây cho một câu) |

### File sửa

| File | Thay đổi |
|---|---|
| `agents/lesson_video/tts.py` | Thêm `Kokoro`, `load_voices`, `kokoro_files`, chế độ `auto`; mọi bộ đọc có `check(voice)` và `tag`; Flite nhận `speed` thay cho `stretch` |
| `agents/lesson_video/script.py` | `Speaker.voice` là một giọng hoặc bảng giọng theo bộ đọc, `voice_for()`; chuẩn hóa dòng thoại không sửa dữ liệu của người gọi và đọc lại được dạng chuẩn |
| `agents/lesson_video/timeline.py` | Kiểm tra giọng trước khi đọc; bộ nhớ tiếng từng câu (`cache_dir`) |
| `agents/lesson_video/cli.py` | `--engine auto|kokoro|flite|silent`, `--speed`, `--model`, `--voices`, `--cache`, `--no-cache`; in bộ đọc đang dùng |
| `agents/lesson_video/video.py` | `lessons.json` ghi thêm `engine`; chuẩn độ to lời nói -16 LUFS khi mã hóa (tiếng Kokoro nhỏ hơn Flite, trung bình -20,5 dB) |
| `agents/tests/test_lesson_video.py` | +5 test: giọng theo bộ đọc, bộ nhớ tiếng, thiếu model Kokoro, đọc file giọng, Kokoro đọc giọng tiếng Anh (bỏ qua khi máy chưa có model); hồi quy kiểm tra giọng khớp bộ đọc đã dùng |
| `agents/pyproject.toml` | Extra `[kokoro]` (`kokoro-onnx>=0.6`) |
| `books/ielts_target_5_0/lessons/U01-speaking-1.yaml`, `U01-speaking-2.yaml` | Giọng theo bộ đọc; `say` đúng với cả hai bộ đọc |
| `books/ielts_target_5_0/lessons/U01-speaking-1.mp4`, `U01-speaking-2.mp4`, `lessons.json` | Dựng lại bằng Kokoro: Speaking 1 dài 7:14 (6,0 MB), Speaking 2 dài 6:16 (4,7 MB) — ngắn hơn bản Flite (8:06, 6:56) vì đọc liền mạch hơn; chương giữ nguyên (8 và 9) |
| `agents/README.md`, `CLAUDE.md`, `docs/agent-hoc-tap/04-checklist.md`, `README.md` (thư mục docs) | Cài và dùng Kokoro; task P2-32 |
| `web/index.html`, `web/ielts-companion.html` | Bản dựng lại (`lessons.json` mới) |

Không thêm, không xóa file nào trong repo.

### Kiểm thử

| Lệnh | Kết quả |
|---|---|
| `cd agents && python -m pytest -q` | 31 passed (kể cả Kokoro đọc giọng tiếng Anh vì máy có model) |
| `node --test "tests/web/*.test.mjs"` | 13 passed |
| `node tests/web/book.e2e.mjs` | 12/12 bước OK |
| `ffprobe` / `volumedetect` | Thời lượng khớp lời thoại; tiếng trung bình -18 dB, đỉnh dưới 0 dB |

---

## Đợt 3 — 05/10/2026: video bài giảng Unit 1 Speaking 1 và 2

Nhánh `claude/gallant-ramanujan-ym30oy` đặt lại từ `main` tại `9c436de` (đã merge PR #3).

### Yêu cầu

Tạo video nói tiếng Anh dạy Speaking Unit 1 (Speaking 1: talking about personal information; Speaking 2:
exchanging personal information), dạy cả từ mới, mỗi bài một video, giọng miễn phí có hai người; gắn video vào
section Unit 1 trong app.

### Đã làm

| Việc | Cách làm |
|---|---|
| Công cụ dựng video | `agents/lesson_video`: kịch bản YAML → đọc từng câu bằng Flite → Pillow vẽ slide → ffmpeg ghép MP4 có chương → `lessons.json`. Tách khỏi agent nhập sách, không đụng `book.json` / `plan.json` |
| Giọng đọc | Hai giọng Flite có sẵn trên Ubuntu (`libflite1`): Emma — cô giáo, `cmu_us_slt` (nữ); Tom — học viên, `cmu_us_rms` (nam). Đọc chậm hơn bình thường 10%. Hugging Face (Kokoro, Piper) bị chặn trong môi trường cloud; chạy model Kokoro lấy từ npm thì bị chặn quyền vì là model tải từ ngoài → dùng Flite |
| Speaking 1 (8:06) | Giới thiệu · Hôm nay học gì · 10 từ mới (nghe Emma, nhắc lại theo Tom, câu ví dụ) · Bài A: nối 6 tranh (ảnh cắt từ trang 10) với 6 câu hỏi, có đếm ngược để tự làm, đáp án gợi ý (Answer key của sách không có bài này) · Bài B: 6 câu trả lời mẫu kèm cụm từ hữu ích · Grammar check: Do you have…? / Have you got…? và vì sao câu 1, 3 dùng hiện tại tiếp diễn · Đến lượt bạn: 6 câu, mỗi câu 10 giây · Tổng kết, bài về nhà |
| Speaking 2 (6:56) | Giới thiệu · Hôm nay học gì · 10 từ mới · Bài A: nối 8 câu hỏi với 8 câu trả lời (Tom hỏi, Emma trả lời và đọc đáp án) · Pronunciation check (what's, âm yếu của are, do) · Watch out: 4 lỗi hay gặp · Bài C: hội thoại mẫu · Đến lượt bạn: 8 câu, mỗi câu 8 giây · Tổng kết |
| Gắn vào Unit 1 | Thẻ Unit 1 ở màn chi tiết sách có dòng "Video bài giảng" với hai nút; bấm thì mở phiên Unit 1 · Speaking & Vocabulary, cuộn tới video và phát. Trong phiên, hoạt động Speaking & Vocabulary có trình phát từng video, nút nhảy theo chương (sáng nút chương đang phát), nhớ vị trí đang xem khi quay lại. Trình duyệt không phát được MP4 H.264 hoặc không tải được file thì báo rõ |

### File thêm

| File | Vai trò |
|---|---|
| `agents/lesson_video/__init__.py`, `__main__.py`, `cli.py` | Lệnh `python -m lesson_video check|build` |
| `agents/lesson_video/script.py` | Model kịch bản (pydantic), chuẩn hóa dòng thoại, kiểm tra với `book.json` |
| `agents/lesson_video/tts.py` | Giọng Flite qua `ctypes`; bộ đọc `silent` |
| `agents/lesson_video/timeline.py` | Ghép tiếng, tính thời lượng từng khung hình, đếm ngược, chương |
| `agents/lesson_video/slides.py` | Vẽ slide 9 kiểu cảnh bằng Pillow |
| `agents/lesson_video/video.py` | ffmpeg → MP4 có chương; ghi `lessons.json` |
| `agents/tests/test_lesson_video.py` | 14 test (kể cả 7 kịch bản lỗi, Flite hai giọng, dựng video thật bằng `silent`, hồi quy kịch bản đã commit) |
| `books/ielts_target_5_0/lessons/U01-speaking-1.yaml`, `U01-speaking-2.yaml` | Kịch bản hai video |
| `books/ielts_target_5_0/lessons/U01-speaking-1.mp4` (6,7 MB), `U01-speaking-2.mp4` (5,3 MB) | Video 1280×720, H.264 + AAC mono, có chương |
| `books/ielts_target_5_0/lessons/lessons.json` | Mục lục video: hoạt động, unit, thời lượng, chương, giọng |

### File sửa

| File | Thay đổi |
|---|---|
| `agents/pyproject.toml` | Thêm gói `lesson_video`, lệnh `lesson-video`, extra `[video]` (pillow, numpy) |
| `web/build.py` | Nhúng `books/<sách>/lessons/lessons.json` vào `BOOKS[id].lessons` |
| `web/src/book/core.js` | `lessonsOf`, `lessonSession`, `chapterAt` |
| `web/src/book/ui.js` | Nút video trên thẻ unit; khối "Video bài giảng" trong hoạt động của phiên (trình phát, chương, báo lỗi) |
| `web/src/book/book.css` | Kiểu khối video, nút chương |
| `tests/web/book-core.test.mjs` | +2 test: hàm video, dữ liệu video thật trỏ đúng hoạt động và file |
| `tests/web/book.e2e.mjs` | +1 bước: Unit 1 có 2 video, mở từ thẻ unit, 8 nút chương, máy chủ trả đoạn 206 |
| `agents/README.md`, `web/README.md`, `CLAUDE.md`, `docs/agent-hoc-tap/04-checklist.md`, `README.md` (thư mục docs) | Hướng dẫn `lesson_video`; mô tả video trong tab Sách; task P2-30 … P2-33; trạng thái |
| `web/index.html`, `web/ielts-companion.html` | Bản dựng lại |

Không xóa file nào. `book.json`, `plan.json` không đổi.

### Kiểm thử

| Lệnh | Kết quả |
|---|---|
| `cd agents && python -m pytest -q` | 26 passed (12 cũ + 14 video) |
| `node --test "tests/web/*.test.mjs"` | 13 passed |
| `node tests/web/book.e2e.mjs` | 12/12 bước OK |
| `python3 web/build.py` | 22 tài liệu + 1 sách 120 phiên, 2 video |

Chromium của Playwright không có H.264 nên e2e chỉ kiểm tra trang báo lỗi rõ ràng và máy chủ phục vụ file; giải mã
video kiểm tra bằng `ffprobe` (thời lượng khớp lời thoại, có chương) và xem khung hình trích từ MP4.

### Việc còn treo

- Giọng Flite nghe máy hơn giọng thật; muốn giọng tự nhiên (Kokoro) cần cho phép tải và chạy model ngoài (P2-32).
- Bài Speaking 2B "Listen and check" cần audio của sách, nhưng hoạt động Unit 1 · Speaking & Vocabulary trong gói chưa có track nào.

---

## Đợt 2 — 04/10/2026: danh sách sách, chọn unit tự do, xem checklist trong app

Nhánh `claude/gallant-ramanujan-ym30oy` đặt lại từ `main` tại `754d175` (đã merge PR #2).

### Yêu cầu

1. Xem checklist những gì đã triển khai cho agent ngay trên UI.
2. Bấm menu Sách → danh sách sách, mỗi sách có thông tin lộ trình: học bao lâu, từ trình độ nào, học xong đạt tới đâu.
3. Bấm vào một sách → liệt kê mọi section và unit để chọn học bất kỳ unit nào.

### Đã làm

| Yêu cầu | Cách làm |
|---|---|
| Checklist trên UI | `build.py` nhúng `docs/agent-hoc-tap/*.md` vào tab Kế hoạch, nhóm "Agent học tập — checklist và kế hoạch" (checklist đứng đầu, ô tick hiện sẵn). Thẻ "Agent nhập sách" cuối màn danh sách sách đếm task đã xong theo giai đoạn (đọc thẳng từ checklist) và có nút mở Checklist, Lịch sử thay đổi. Link tương đối giữa các tài liệu nay bấm được |
| Danh sách sách | Menu Sách luôn mở màn danh sách. Sách đã nhập hiện: vai trò và tuần trong lộ trình, tác giả/NXB, trình độ (Band 3.5 → 5.0 · CEFR A2–B1), nội dung (3 section · 15 unit · 3 review · 3 test · 59 track), thời lượng (120 phiên × 75 phút ≈ 150 giờ), học xong trong (khoảng 4–5,5 tháng ở nhịp 7–5 phiên/tuần; nhịp đang chọn ra số tuần và tháng), bắt đầu khi nào, mục tiêu, tiến độ, nút "Xem unit & chọn bài học" và "Học tiếp". Bốn sách còn lại của lộ trình (Cambridge 20 GT, Trainer 2 GT, Barron's Writing, Cambridge 21 GT) hiện mờ kèm "chưa nhập vào app" |
| Chi tiết sách, chọn unit | Màn chi tiết có nút quay về danh sách, thẻ giới thiệu, phiên kế tiếp, tiến độ, cài đặt, quản lý file, rồi "Chọn unit để học": 3 section, 21 thẻ (15 unit, 3 review, 3 test) — mỗi thẻ có trang in, số phiên, chấm trạng thái từng phiên, nút Học / Học tiếp / Ôn lại và danh sách phiên để chọn lẻ. Bấm Học ở một unit thì "Phiên kế tiếp" chuyển sang chế độ unit tự chọn cho tới khi unit đó xong; nút "Quay về theo lộ trình" bỏ chế độ này |

### File thêm

| File | Vai trò |
|---|---|
| `books/catalog.json` | Thứ tự và vai trò 5 sách trong lộ trình 40 tuần (tuần, mục tiêu, giới thiệu ngắn cho sách chưa nhập) |

### File sửa

| File | Thay đổi |
|---|---|
| `agents/book_ingest/schemas.py` | Model `BookInfo` (role, module, author, publisher, cefr, bandFrom, bandTo, summary, startWhen); `Book.info` |
| `agents/book_ingest/profile.py`, `templates.py` | Đọc `info` trong `book.yaml`, ghi vào `book.json` (khóa lạ bị bỏ qua) |
| `agents/tests/test_pipeline.py` | Test `info` đi từ `book.yaml` sang `book.json` |
| `schemas/book.schema.json` | Xuất lại theo model mới |
| `books/ielts_target_5_0/book.yaml` | Thêm mục `info` (tác giả theo bìa sách; trình độ theo technical summary) |
| `books/ielts_target_5_0/book.json` | Chạy lại agent: thêm `info`; `plan.json` không đổi |
| `web/build.py` | Nhúng `docs/agent-hoc-tap/` vào tab Kế hoạch; nhúng `books/catalog.json` vào chỗ đánh dấu `/*__BOOK_CATALOG__*/` |
| `web/app.template.html` | +9 dòng nhãn và nhóm tài liệu agent trong `DOCMETA`/`DOCGROUPS`; `const BOOK_CATALOG`; `mdInline` tìm link tương đối theo tên file (2 dòng) |
| `web/src/book/core.js` | `focusOf`, `nextSession` theo unit tự chọn, `itemSessions`, `itemCounts`, `entrySession`, `duration`, `checklistStats` |
| `web/src/book/ui.js` | Màn danh sách sách, màn chi tiết với thẻ unit, nút Học theo unit, nút quay về lộ trình, thẻ Agent nhập sách; menu Sách luôn mở danh sách; nút quay lại trong phiên ghi "← Danh sách unit" |
| `web/src/book/book.css` | Kiểu thẻ sách, dòng thông tin, thẻ unit, chấm tiến độ |
| `tests/web/book-core.test.mjs` | +3 test: unit tự chọn, thời lượng theo nhịp, đếm checklist |
| `tests/web/book.e2e.mjs` | Đi qua danh sách → chi tiết; thêm bước chọn Unit 7 rồi quay về lộ trình, bước mở checklist và bấm link sang lịch sử |
| `web/README.md`, `docs/agent-hoc-tap/04-checklist.md`, `README.md` (thư mục docs), `02-kien-truc-va-hop-dong-du-lieu.md` | Mô tả tab Sách mới; task P2-27 … P2-29; trạng thái; sửa ghi chú cũ "thư mục này không nhúng vào app" |
| `web/index.html`, `web/ielts-companion.html` | Bản dựng lại (thêm tài liệu agent và catalog, khoảng +120 KB) |

Không xóa file nào.

### Kiểm thử

| Lệnh | Kết quả |
|---|---|
| `cd agents && python -m pytest -q` | 12 passed |
| `node --test "tests/web/*.test.mjs"` | 11 passed |
| `node tests/web/book.e2e.mjs` | 11/11 bước OK |
| `python3 web/build.py` | 22 tài liệu (thêm 6 tài liệu agent) + 1 sách 120 phiên |

---

## Đợt 1 — 04/10/2026: agent nhập sách + tab Sách

Nhánh `claude/gallant-ramanujan-ym30oy`, dựa trên `main` tại `89133a0` (commit thêm bộ sách
IELTS Target 5.0 vào `books/ielts_target_5_0/`).

### Phạm vi theo yêu cầu

- Agent **chỉ** phục vụ nhập sách: biến PDF + MP3 thành menu học theo lộ trình.
- Thêm menu học vào web, **hạn chế đụng code cũ**: các bản sửa lỗi đồng bộ B1–B4, tích hợp tab Hôm nay,
  Tiến độ chưa làm trong đợt này (xem mục "Chưa làm").
- Không bàn về nguồn gốc dữ liệu sách; dữ liệu nằm trong repo theo lựa chọn của chủ repo.

### Kết quả trên IELTS Target 5.0

| Hạng mục | Kết quả |
|---|---|
| Course Book | `IELTS_Target_5.0.pdf`: 325 trang, bản scan (lớp chữ ~5%, chỉ watermark), có mã hóa `/Encrypt`, độ lệch trang in → PDF là 1 |
| Bản trích Listening | `Target5.0_Listening_R.pdf`: 90 trang — bìa, 2 trang Listening mỗi unit (trang 2N–2N+1), Answer key 32–42, Tapescript 43–90 |
| Audio | 59 file `UnitN_listening_<bài>.mp3`, 113 phút, đủ 15 unit; ghép 59/59 theo tên |
| Cấu trúc | 15 unit × 6 module nhận ra bằng băng tiêu đề đỏ: 14 unit khớp ngay; Unit 15 có băng thừa (Exam practice dài 4 trang) → 1 mục duyệt, đã đồng ý gộp |
| OCR | 57 trang (Answer key 9, Tapescript 48), chạy một lần ~4 phút, cache trong `work/ocr-cache.json` |
| Answer key | Trang đáp án riêng cho từng unit và từng module (Listening, Reading, Writing, Exam practice) + Review 3 |
| Tapescript | Khoảng trang từng unit + TEST 1–3; 58/59 track có trang tapescript chính xác (U02-L1I dùng khoảng Listening của Unit 2) |
| Đoạn PDF cho web | 27 đoạn, 86 MB trong `books/ielts_target_5_0/web/` — mở một trang tải ~3–6 MB thay vì ~70 MB |
| Kế hoạch | 120 phiên × 75 phút, 6 phiên/tuần, tuần 6–25; `book validate` OK |

### Phát hiện về dữ liệu làm thay đổi cách làm

1. **PDF là bản scan** → bước "hiểu cấu trúc" không đọc được chữ. Ranh giới module nhận bằng màu băng tiêu đề
   (code tất định); Answer key và Tapescript lập chỉ mục bằng OCR (RapidOCR, tùy chọn, có cache).
2. **PDF.js đọc gần hết file 100 MB chỉ để mở một trang.** Nguyên nhân: PDF.js luôn kiểm tra trang cuối khi mở
   tài liệu (`checkLastPage`), còn file này có cây trang phẳng 325 trang với page dict nằm rải cạnh ảnh scan
   → 280 yêu cầu Range (~72 MB). Đo bằng log máy chủ. Cách xử lý đúng như quyết định D5 của plan: agent cắt
   Course Book thành đoạn theo unit/review/phần đáp án/tapescript.
3. **Thiếu Work Book và 3 quyển Test.** Phiên 7 của mỗi unit thành "Ôn unit + sổ lỗi" (dùng trang đáp án + Key
   exam vocabulary); phiên Test giữ chỗ trong lịch, ghi chú làm đề Cambridge GT, và vẫn trỏ tới tapescript
   TEST 1–3 có trong Course Book.
4. **Tên audio đã chuẩn** (`Unit4_listening_3b.mp3`) → không cần Whisper; ghép theo mẫu tên trong `book.yaml`.
5. **OCR dính chữ** ("Unit 13Listening3", "CNow listen…", "Unit 12-Speaking 3") → regex tiêu đề không bắt buộc
   khoảng trắng, chấp nhận dấu gạch; nhận "TEST n" làm mốc riêng để phần Test không bị tính vào Unit 15.

### File thêm

| File | Vai trò |
|---|---|
| `agents/pyproject.toml`, `agents/README.md` | Dự án Python `book-ingest`, lệnh `book`; extras `[ocr]`, `[llm]`, `[review]`, `[dev]` |
| `agents/book_ingest/schemas.py` | Model Pydantic: `Book`, `Activity`, `Ref`, `PdfFile` (+ `Chunk`), `AudioFile`, `Plan`, `Session`, `Review`, `TocDraft` |
| `agents/book_ingest/profile.py` | Đọc `book.yaml`, tính trang cuối từng phần, đổi trang in ↔ trang PDF |
| `agents/book_ingest/pdfutil.py` | sha256, mở PDF, đo băng tiêu đề đỏ, vẽ trang |
| `agents/book_ingest/ocr.py` | OCR tùy chọn (RapidOCR) có cache JSON, thứ tự đọc trang hai cột |
| `agents/book_ingest/scan.py` | Bước quét: số trang, lớp chữ, sha256, file trùng, độ dài audio; lệnh `inventory` |
| `agents/book_ingest/structure.py` | Ranh giới module, kiểm tra độ lệch trang, review chia 2 phần, chỉ mục Answer key/Tapescript (theo unit, module, track, TEST) |
| `agents/book_ingest/audio.py` | Ghép audio theo mẫu tên, ID track `U04-L3B`, gắn trang tapescript từng track |
| `agents/book_ingest/review.py` | Hộp duyệt `work/review.json`: gộp, giữ quyết định cũ, `--accept-all`, duyệt từng mục trên terminal |
| `agents/book_ingest/templates.py` | Mẫu phiên `target-gt-v1` → `book.json` và `plan.json` |
| `agents/book_ingest/chunks.py` | Cắt PDF lớn thành đoạn theo cấu trúc sách, ổn định giữa các lần chạy, dùng lại đoạn cũ |
| `agents/book_ingest/validate.py` | Kiểm tra schema + V3 (trang nằm trong file/đoạn), V4 (track), V5 (độ dài), V7 (số phiên), V8 (file, cỡ, sha256) |
| `agents/book_ingest/pipeline.py` | Chạy nối các bước, dừng ở hộp duyệt (mã 2), ghi `report.md` |
| `agents/book_ingest/llm.py` | Bước đọc mục lục: `manual` (vẽ trang cho Claude Code) và `api` (Claude qua SDK `anthropic`, structured output `TocDraft`, mặc định `claude-opus-5-5`) |
| `agents/book_ingest/cli.py`, `__init__.py`, `__main__.py` | Lệnh `inventory`, `profile`, `ingest`, `review`, `validate`, `schemas` |
| `agents/tests/*` | Sách giả sinh lúc chạy (băng đỏ, OCR giả, MP3 tối thiểu); test pipeline, regex, LLM giả, schema, hồi quy trên sách thật |
| `.claude/skills/book-ingest/SKILL.md` | Skill để Claude Code vận hành agent cho sách mới |
| `schemas/{book,plan,review}.schema.json` | JSON Schema xuất từ Pydantic |
| `books/ielts_target_5_0/book.yaml` | Hồ sơ sách, viết ở chế độ manual sau khi đọc trang Contents (PDF trang 4) |
| `books/ielts_target_5_0/{book.json,plan.json,report.md}` | Đầu ra của agent |
| `books/ielts_target_5_0/work/*` | Kết quả từng bước + cache OCR + `chunks.json` + `review.json` (quyết định duyệt) — commit để chạy lại không cần OCR |
| `books/ielts_target_5_0/web/course-book-p*.pdf` | 27 đoạn PDF cho app |
| `web/src/book/core.js` | Hàm thuần: phiên kế tiếp, đếm, tuần dự kiến, dự báo tuần xong, `canSkip`, hợp nhất tiến độ theo `t`, đồng hồ theo mốc thời gian, tìm đoạn PDF, ghép file nhập |
| `web/src/book/ui.js` | Tab Sách: menu theo section/unit, phiên kế tiếp, tiến độ, cài đặt nhịp học, quản lý file (nhập IndexedDB), màn hình Phiên học (đồng hồ, trang sách, đáp án, tapescript, từ vựng, audio, ghi sổ lỗi, kết thúc phiên), trình xem PDF, đồng bộ `students/<slug>/books/<id>` |
| `web/src/book/book.css` | Giao diện tab Sách, dùng lại biến màu và class sẵn có |
| `web/vendor/pdfjs/*` | PDF.js 4.10.38 bản legacy + LICENSE (Apache-2.0) + VERSION.txt |
| `web/serve.py` | Máy chủ chạy thử có HTTP Range |
| `tests/web/book-core.test.mjs` | 8 test `node:test` cho `core.js` và gói sách thật |
| `tests/web/book.e2e.mjs` | E2E Playwright 8 bước trên `web/index.html` |
| `.gitignore`, `CLAUDE.md` | Bỏ qua rác (`.DS_Store`, cache Python, ảnh lỗi e2e, sản phẩm phụ của agent); quy ước repo |
| `docs/agent-hoc-tap/05-lich-su-thay-doi.md` | File này |

### File sửa

| File | Thay đổi |
|---|---|
| `web/app.template.html` | **+12 dòng, không xóa dòng nào**: chỗ đánh dấu `/*__BOOK_CSS__*/` trong `<style>`; `<section id="p-book">` sau tab Lộ trình; nút menu **Sách** (thứ 3); `const BOOKS = /*__BOOKS__*/{}` và `/*__BOOK_JS__*/` trước phần khởi động; `BookUI.init()` sau `renderRootNote()` |
| `web/build.py` | Gom `books/*/book.json` + `plan.json`, chèn mã/CSS tab Sách (chặn chuỗi đóng thẻ), thay chỗ đánh dấu của Sách trước tài liệu; không nhúng `agents/`, `.claude/`, `books/`, `vendor/`, `CLAUDE.md` vào tab Kế hoạch; xét đường dẫn tương đối khi lọc thư mục |
| `web/index.html`, `web/ielts-companion.html` | Bản dựng lại (thêm ~140 KB: dữ liệu sách + mã tab Sách) |
| `web/README.md` | Thêm dòng tab Sách, mục "Tab Sách" (nguồn file, đoạn PDF, nơi lưu tiến độ, giới hạn bản Claude), cập nhật bảng file |
| `docs/agent-hoc-tap/04-checklist.md` | Tick các task đã làm, ghi chú task làm khác plan hoặc hoãn |
| `docs/agent-hoc-tap/README.md` | Thêm file 05 vào mục lục |

### File xóa

| File | Lý do |
|---|---|
| `.DS_Store`, `books/.DS_Store` | Bỏ khỏi git (file hệ thống macOS); thêm vào `.gitignore` |

Không xóa hay đổi tên file sách nào của người dùng.

### Khác với plan

| Mục | Plan | Đã làm | Vì sao |
|---|---|---|---|
| Tab Sách | Thay tab Tài liệu (giữ 7 tab) | Thêm tab thứ 8 "Sách" | Không đụng tab cũ theo yêu cầu; thanh menu dạng flex vẫn vừa trên điện thoại 390 px |
| CLI | Typer | `argparse` (thư viện chuẩn) | Bớt một phụ thuộc |
| Độ lệch trang | Đọc số in ở chân trang | Kiểm tra băng tiêu đề ở trang đầu mọi unit, dò 0–20 nếu lệch | Sách scan không có lớp chữ |
| Ghép audio | rapidfuzz + suy theo thứ tự + Whisper | Chỉ theo mẫu tên trong `book.yaml`, tên lạ → mục duyệt | Tên file đã chuẩn; Whisper/rapidfuzz để lúc có sách cần |
| Màn hình duyệt | Streamlit | Terminal (`review`, `--accept-all`, `--list`) | Chỉ có 1 mục cần duyệt |
| Vendor PDF.js | Nhúng vào HTML, worker từ Blob | File riêng `web/vendor/pdfjs/`, tải lười; dự phòng jsDelivr | Không làm bản dựng nặng thêm 1,8 MB |
| Gói sách | Zip theo section | Đoạn PDF + file rời trong `books/` | Sách đã ở trong repo; app đọc trực tiếp hoặc nhập file rời |
| Thư mục làm việc | Ngoài repo, pipeline từ chối ghi vào git repo | `books/<sách>/work/` trong repo, commit | Chủ repo để sách trong repo; cache OCR giúp người khác chạy lại |
| Hợp đồng `book/1` | `answerPages`, `vocabPages`, `generatedAt` | `answer`/`script`/`vocab`/`alt` dạng `Ref {pdf,pages}`; `source.profileSha256` thay thời điểm | Đáp án và tapescript nằm ở file khác file bài; đầu ra phải ổn định giữa các lần chạy |
| Đồng bộ tiến độ sách | Đăng ký `onSnapshot` trong `connectSync()` | Đọc và hợp nhất khi mở tab Sách, ghi sau 900 ms | Không sửa `boot()` cũ; hợp nhất theo từng phiên nên không mất dữ liệu |

### Quyết định áp dụng theo mặc định (chưa chốt chính thức — P0-01)

D1 cả hai bản (Claude, tự host) đều có tab Sách; D2 CLI + skill, LangGraph để Giai đoạn 4; D3 SDK `anthropic`;
D5 cắt PDF (bắt buộc với file này); D6 `<audio>` gốc; D7 `students/<slug>/books/<id>`, không vào `roster`;
D9 hàm `canSkip` chặn bỏ phiên lõi; D10 pipeline chạy trên máy cá nhân hoặc container. D4 (tuần 6–12) và D8
(AI chữa bài trong phiên) chưa động tới.

### Kiểm thử đã chạy

| Lệnh | Kết quả |
|---|---|
| `cd agents && python -m pytest -q` | 11 passed (gồm hồi quy: chạy lại pipeline trên sách thật cho ra `book.json`/`plan.json` giống hệt) |
| `node --test "tests/web/*.test.mjs"` | 8 passed |
| `node tests/web/book.e2e.mjs` | 8/8 bước OK trên Chromium khổ 390 px: các tab cũ vẫn chạy; tab Sách hiện 120 phiên; mở trang sách tải < 15 MB; xong phiên cộng đúng 1 giờ vào giờ học hôm nay; audio phát và tua +5s; tải lại trang còn tiến độ; nhập file vào IndexedDB; xem trang từ đoạn đã nhập khi máy chủ không có file |
| `python -m book_ingest validate ../books/ielts_target_5_0 --hashes` | OK — 15 unit, 3 review, 3 test, 59 track, 120 phiên, tuần 6–25 |
| `python3 web/build.py` | Nhúng 16 tài liệu (không đổi) + 1 sách 120 phiên |

Chưa kiểm tra được: iPhone/Android thật, bản đăng trên Claude (nạp PDF.js, IndexedDB, micro — spike S0.1–S0.4).

### Chưa làm trong đợt này

- Sửa lỗi đồng bộ B1–B8 (P0-04 … P0-07) — hoãn theo yêu cầu không đụng code cũ. B1 vẫn còn: người chưa đặt
  tên dùng chung gốc `mac-dinh` trên máy chủ.
- Nối tab Hôm nay, Lộ trình, Tiến độ, Luyện tập với sách (P2-14, P2-15, P2-16, P2-21).
- Phiếu trả lời theo câu, Writing/Speaking trong phiên, luật xếp lớp và rút gọn, chế độ không gói
  (P2-10 … P2-12, P2-17, P2-18, P2-20). Dự báo tuần xong và cảnh báo quá tuần 30 đã có.
- CI, `tools/check_repo.py` (không còn hợp vì sách nằm trong repo), Streamlit, Whisper, fixture "sách kiểu khác".
- Đăng lại artifact trên Claude (P2-25) — cần chủ tài khoản; bản dựng đã sẵn sàng.

### Chạy lại

```bash
cd agents && pip install -e '.[ocr,dev]'          # hoặc pip install pymupdf pyyaml pydantic mutagen
python -m book_ingest ingest ../books/ielts_target_5_0
cd .. && python3 web/build.py && python3 web/serve.py   # mở http://localhost:8000/web/index.html → tab Sách
```

---

## Trước đợt 1

| Commit | Nội dung |
|---|---|
| `2c24941` (PR #1, đã merge) | Thêm `docs/agent-hoc-tap/01–04` + README; `web/build.py` bỏ qua `docs/` |
| `f670068` | `05-tai-lieu-mien-phi.md` thêm mục K (bộ sách chốt, lọc danh sách tổng hợp); checklist P0-08, P3-10 |
| `185e885` | Merge `main` (`89133a0` — thêm bộ sách IELTS Target 5.0) vào nhánh làm việc |
