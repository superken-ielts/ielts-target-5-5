# Quy ước repo

Lộ trình tự học IELTS General Training 3.0 → 5.5 (markdown ở gốc repo), app học một file HTML (`web/`),
và agent nhập sách (`agents/`). Kế hoạch kỹ thuật và checklist: `docs/agent-hoc-tap/`.

## Sửa app

- Sửa `web/app.template.html` hoặc `web/src/book/*`, **không** sửa `web/index.html`, `web/ielts-companion.html`
  hay `01a-giao-an-tung-ngay-giai-doan-1.md` — ba file này do build sinh ra.
- Sau mỗi lần sửa template, mã tab Sách, bất kỳ file `.md` nào hoặc `books/*/book.json`: chạy `python3 web/build.py`
  và commit cả hai bản dựng.
- JS thuần, không framework. Dữ liệu từ người dùng hoặc từ gói sách chỉ hiện bằng `textContent`.
- Mã chèn vào trang không được chứa chuỗi đóng thẻ `</` (build sẽ báo lỗi).

## Agent nhập sách

- Skill: `.claude/skills/book-ingest/SKILL.md`. Chạy: `cd agents && python -m book_ingest ingest ../books/<sách>`.
- Không sửa tay `book.json` / `plan.json` / `report.md`: sửa `book.yaml` hoặc quyết định trong `work/review.json`
  rồi chạy lại. Đổi model trong `schemas.py` thì chạy `python -m book_ingest schemas`.
- Lộ trình N5 (`books/Genki/`, mẫu `lessons-v1`): trang và track của từng phiên khai ở `book.yaml › refs` (trang in,
  khoảng track `K01-09..K01-23`); mỗi track phải thuộc đúng một phiên. Xem `docs/agent-hoc-tap/07-lo-trinh-n5-tieng-nhat.md`.
- Giai đoạn 0 (`books/book_english_unlimited_a2_elemetary/`, `lessons-v1`): track theo nhãn đĩa (`track: "1.{n}"`), Part 1
  khai hai lần vì trang 49 quét trùng. Xem `docs/agent-hoc-tap/08-giai-doan-0-a1-a2.md`.
- Oxford Word Skills Basic (`books/book_oxford_word_skills_basic/`, `lessons-v1`): một PDF quét khai ba lần (`course-book`,
  `answer-key`, `word-list`) vì thiếu hai trang trắng; tên bước dùng `{title}`. Xem `docs/agent-hoc-tap/09-oxford-word-skills-basic.md`.

## Video bài giảng

- Kịch bản `books/<sách>/lessons/<id>.yaml`; dựng: `cd agents && python -m lesson_video build ../books/<sách>/lessons/<id>.yaml`
  rồi chạy `python3 web/build.py`. Cần ffmpeg và giọng Kokoro (model q8 + file giọng ở `~/.cache/lesson_video/kokoro/`,
  xem `agents/README.md`); không có model thì công cụ dùng Flite (`libflite1`) — đừng commit video Flite đè video Kokoro.
- Không sửa tay `lessons.json` / `.mp4`. Chữ trên màn hình ở dòng thoại, cách đọc khác (chữ cái, số, tên riêng) ở `say`.
  Bỏ một video: xóa `.yaml` rồi `python -m lesson_video prune ../books/<sách>`.
- Làm video mới: theo quy trình và bảng độ phủ ở `docs/agent-hoc-tap/06-video-bai-giang.md`; xong thì cập nhật bảng đó
  (`python -m lesson_video coverage ../books/<sách> --unit U0x`). Video tiếng Nhật (GENKI): quy trình và bảng độ phủ ở
  file 07 mục 4; cần `misaki[ja]` và phông Noto Sans CJK. Video Giai đoạn 0 (English Unlimited A2): sổ tay từng unit
  ở file 08 mục 6; lời bài nghe chép sẵn ở `work/transcripts/` (`python -m lesson_video transcribe`). Trước khi dựng,
  soát cách đọc bằng `python -m lesson_video phonemes <kịch bản>` (⚠ = lỗi đã gặp, sửa bằng `say`).
- IELTS Target 5.0: 4 video luyện nói thêm mỗi unit (Unit 1–3 đã có) theo khuôn, hồ sơ nhân vật Tom / Emma và danh sách
  chủ đề ở file 06 mục 9. Cảnh "Đến lượt bạn" (`practice`) không dùng `wait`: người học tự tạm dừng video.
- Từ Unit 4 (đợt 31), video sách IELTS Target 5.0 và Giai đoạn 0 có hình trong sách ở mọi video, như Oxford Word Skills
  Basic: cảnh `figure` / `image` kèm `box` (khung đỏ), trang nhiều chữ cắt thành dải — file 06 mục 8, file 09 mục 5.3a.
- Giai đoạn 0 từ Unit 5 (đợt 32): đáp án hiện tất cả một lần sau khi đọc / nghe xong (dòng `reveal` đầu tiên mở mọi
  đáp án, đứng sau `track`); cuối mỗi video là cảnh `words` — từ A2 của bài theo bảng từ English Profile của sách
  (`python -m lesson_video wordlist ../books/<sách> --unit U0x`; lần đầu cần xlrd), bốn video của unit cùng nhau đủ mọi
  từ (test kiểm) — file 08 mục 6.9.
- Video sách phải đủ mọi bài tập trên trang của phiên (đợt 33, người học: "nếu video dưới 10 phút không đủ cover bài trong
  sách thì tăng thêm cho đủ"): 5–10 phút là mức thường, bài cần dài hơn thì video dài hơn; không bỏ bài tập, bài nghe,
  luyện phát âm hay đóng vai để ép dưới 10 phút. Chỉ bỏ bài cần trang không có trong bản quét, ghi ở đầu kịch bản.
  Trước khi dựng, đối chiếu danh sách bài tập của trang sách với kịch bản (file 08 mục 6.1, 6.4).
- Oxford Word Skills Basic: mỗi unit một video 7–10 phút, không `wait` / `echo`, 1–2 phần nói theo chủ đề; khuôn, bảng `say`
  và độ phủ ở file 09 mục 5 (Unit 1–16 đã có). Unit khó (đầu kịch bản ghi `UNIT KHÓ`) tới 15 phút: thêm ôn tập và luyện
  nói chung. Mỗi unit có ít nhất một cảnh dùng hình trong sách: cảnh `figure` (khung đỏ theo `box`), `bullets` / `blanks`
  có `image` — file 09 mục 5.3a.

## Kiểm tra trước khi commit

```bash
python3 web/build.py && git diff --stat                 # bản dựng phải khớp nguồn
cd agents && python -m pytest -q && cd ..                 # agent (kể cả hồi quy trên sách thật)
node --test "tests/web/*.test.mjs"                        # hàm thuần của tab Sách
node tests/web/book.e2e.mjs                               # đầu-cuối, cần Playwright
```

## Ghi lại thay đổi

Mỗi đợt triển khai: tick `docs/agent-hoc-tap/04-checklist.md` và ghi chi tiết thêm/sửa/xóa vào
`docs/agent-hoc-tap/05-lich-su-thay-doi.md`.
