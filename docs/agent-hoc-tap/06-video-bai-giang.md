# 06 — Video bài giảng: hồ sơ Unit 1, quy trình và kế hoạch Unit 2

Gom lại toàn bộ việc làm video bài giảng cho **IELTS Target 5.0 · Unit 1** (đợt 3–9): phần nào đã có video, phần
nào chưa và vì sao, cách làm một video từ đầu tới lúc gắn vào app, những lỗi đã gặp. Dùng file này làm căn cứ
khi làm **Unit 2** (mục 6) và các unit sau.

Công cụ: `agents/lesson_video` (xem `agents/README.md`). Kịch bản và video: `books/ielts_target_5_0/lessons/`.
Bảng độ phủ ở mục 1 in lại được bất cứ lúc nào:

```bash
cd agents && python -m lesson_video coverage ../books/ielts_target_5_0 --unit U01 --unit U02
```

---

## 1. Unit 1 · Life — độ phủ video

Bảng in bằng lệnh `coverage` sau đợt 9 (thời lượng và số chương lấy từ `lessons.json`):

### U01 · Life — 4/7 phần có video, 9 video, 1:05:09

| Phần | Trang | Video | Dài | Chương |
|---|---|---|---|---|
| Speaking & Vocabulary | sách tr. 10–11 | `U01-speaking-1` — Speaking 1: talking about personal information | 7:14 | 8 |
| Speaking & Vocabulary | sách tr. 10–11 | `U01-speaking-2` — Speaking 2: exchanging personal information | 6:16 | 9 |
| Speaking & Vocabulary | sách tr. 10–11 | `U01-vocabulary` — Vocabulary 1–3: family, stages of life, key words | 8:24 | 12 |
| Listening | Listening tr. 12–13 | **chưa có video** | — | — |
| Reading | sách tr. 14–16 | **chưa có video** | — | — |
| Writing | sách tr. 17–18 | `U01-writing-1` — Writing 1: organizing your writing | 7:08 | 12 |
| Writing | sách tr. 17–18 | `U01-writing-2` — Writing 2: types of letter / starting and ending letters | 7:58 | 10 |
| Writing | sách tr. 17–18 | `U01-writing-3` — Writing 3: organizing points in a personal letter | 8:30 | 10 |
| Consolidation | sách tr. 19 | `U01-consolidation` — Consolidation: Speaking, Vocabulary, Errors | 6:52 | 10 |
| Exam practice | sách tr. 20–21 | `U01-exam-listening` — Exam practice: Listening | 7:08 | 11 |
| Exam practice | sách tr. 20–21 | `U01-exam-reading` — Exam practice: Reading | 5:40 | 8 |
| Ôn unit + sổ lỗi | — | **chưa có video** | — | — |

**Kết luận:** Unit 1 có video cho 4/7 phần — Speaking & Vocabulary, Writing, Consolidation, Exam practice (đủ các
phần người dùng yêu cầu). Chưa có video:

| Phần | Vì sao chưa làm | Khi nào làm |
|---|---|---|
| **Listening** (Listening tr. 12–13; track U01-L1C, L1D, L2A) | Bài nghe có file MP3 thật của sách; người học nghe trong phiên học (trình phát track có sẵn). Công cụ video **chưa chèn được đoạn audio của sách** vào video — chỉ đọc lời bằng Kokoro | Khi thêm kiểu cảnh phát track (đề xuất `audio: {track: U01-L2A, from, to}`), hoặc nếu người dùng muốn video giải đáp án bằng giọng đọc lại Tapescript như bài Exam practice |
| **Reading** (sách tr. 14–16) | Chưa có yêu cầu; bài đọc dài 3 trang | Có thể làm ngay theo mẫu `U01-exam-reading.yaml` (cảnh `letter` đọc bài, `mcq`, `pairs`) |
| **Ôn unit + sổ lỗi** | Không có trang sách — là phiên tự ôn (làm lại câu sai, ghi sổ lỗi) | Không cần video |
| **Workbook tr. 6** (P2-36) | Workbook **không có** trong bộ sách đã nhập | Khi người dùng thêm Workbook hoặc gửi ảnh trang |

## 2. Lịch sử từng video

| Đợt | Video | Nội dung chính | Kiểu cảnh | Nguồn đáp án |
|---|---|---|---|---|
| 3 → 4 | `U01-speaking-1` Speaking 1 | Từ mới, bài A nối tranh – câu hỏi, câu trả lời mẫu, Grammar check, "Đến lượt bạn" | title, bullets, vocab, match, qa, compare, practice | Answer key + gợi ý |
| 3 → 4 | `U01-speaking-2` Speaking 2 | Bài A nối câu hỏi – câu trả lời, phát âm, lỗi thường gặp, luyện hỏi – đáp | pairs, qa, errors, practice | Answer key + gợi ý |
| 5 | `U01-writing-1` Writing 1 | Sáu bước viết, chia 20 phút, thư thân mật mẫu 160 từ đọc thành tiếng | order, timing, letter | Gợi ý (thư mẫu tự viết) |
| 5 | `U01-writing-2` Writing 2 | Các loại thư, câu mở đầu / kết thư, thư trang trọng mẫu 154 từ | pairs, compare, letter | Answer key + gợi ý |
| 6 | `U01-writing-3` Writing 3 | Bài A, B (thư của Bruno), C; thư mẫu của Lan 156 từ; cách làm đề Workbook tr. 6 | order, letter, compare | Đọc từ thư trong sách |
| 7 | `U01-vocabulary` Vocabulary 1–3 | Nghe – chép 10 từ, /ʌ/, các giai đoạn cuộc đời, từ khóa để nói, thêm ví dụ | blanks, match, order, vocab, letter | Tapescript Track 3 + gợi ý |
| 9 | `U01-consolidation` Consolidation | Speaking A–C (Phần 1 bài thi Nói), Vocabulary A–C (từ gia đình, dạng từ, trọng âm), sửa 8 lỗi | qa, practice, blanks (câu điền từ), bullets, errors | Tapescript Track 8 (trọng âm); còn lại là đáp án gợi ý |
| 9 | `U01-exam-listening` Exam practice: Listening | Điền ghi chú 1–4, trắc nghiệm 5–7, bản đồ 8–9; Emma (lễ tân) và Tom (khách) **đọc lại Track 9** theo Tapescript, chia 3 đoạn; mẹo nghe từ đồng nghĩa, bẫy | blanks + mcq + match có `hide_text`, `roles` | Tapescript Track 9 |
| 9 | `U01-exam-reading` Exam practice: Reading | Đọc lướt chọn chủ đề, Emma đọc bài "Perspectives of work…", từ khóa, nối câu 1–5 với đoạn A–E, mẹo dạng bài | mcq (`keys` 1/2/3), letter, vocab, pairs | Suy ra từ bài đọc, có câu bằng chứng |

Đợt 4 dựng lại hai video Speaking bằng Kokoro (trước đó là Flite). Mọi video hiện tại: Kokoro q8, Emma `af_heart`,
Tom `am_michael`, tốc độ 0,9.

## 3. Quy trình làm một video (đã dùng cho cả 9 video)

1. **Đọc trang sách**: mở trang trong app (tab Sách → phiên học) hoặc kết xuất ảnh trang bằng PyMuPDF; ghi lại số
   trang PDF (`page` trong kịch bản là trang PDF, không phải số in). PDF là bản quét — không có lớp chữ, chép tay
   hoặc OCR bằng `rapidocr_onnxruntime` để lấy chữ.
2. **Tìm đáp án**: Answer key và Tapescript ở cuối sách (số trang PDF ở `answer`, `script` của từng hoạt động trong
   `book.json`). Answer key không có đa số bài của Unit 1 — khi đó ghi rõ "đáp án gợi ý" ở đầu kịch bản và nói
   trong video. Bài nghe không có file MP3 (ví dụ Track 9) thì cho hai giọng **đọc lại
   Tapescript** trong cảnh `hide_text: true`.
3. **Viết kịch bản** `books/<sách>/lessons/<id>.yaml` — chép phần đầu từ một kịch bản cùng dạng (bảng ở mục 4).
   Mỗi video 6–9 phút; một phần sách dài thì tách nhiều video cùng `activity` (ví dụ `U01-exam-listening` +
   `U01-exam-reading` cùng gắn `U01-exam-practice`).
4. `python -m lesson_video check <kịch bản>` — kiểu cảnh, khóa bắt buộc, `focus` / `reveal`, hoạt động có trong
   `book.json`, ảnh cắt có trong PDF.
5. **Soát cách đọc**: câu có chữ cái đứng riêng, số, tên riêng → thêm `say` (bảng ở mục 5). Kiểm bằng
   `k.tokenizer.phonemize(text, "en-us")` của Kokoro.
6. **Xem trước không tiếng**: `python -m lesson_video build <kịch bản> --engine silent --out /tmp/x --work /tmp/x/w`
   rồi mở vài khung hình mỗi cảnh (`/tmp/x/w/<id>/f*.png`): chữ tràn, ô quá to, chữ quá nhỏ.
7. **Dựng thật**: `python -m lesson_video build <kịch bản> --engine kokoro` (≈ 10–20 phút một video trên 4 lõi;
   tiếng từng câu được nhớ ở `~/.cache/lesson_video/tts`, sửa slide rồi dựng lại chỉ mất ~1 phút). Lệnh ghi
   `<id>.mp4` và cập nhật `lessons.json`.
8. `python3 web/build.py` — nhúng `lessons.json` vào app; thẻ unit hiện mục lục video theo thứ tự phần trong sách.
9. Kiểm tra (mục 7), cập nhật `04-checklist.md`, `05-lich-su-thay-doi.md` và bảng ở mục 1 của file này.

## 4. Kiểu cảnh và khi nào dùng

| Kiểu | Khóa mỗi mục | Dùng cho | Ví dụ |
|---|---|---|---|
| `title` | — | Mở đầu, giới thiệu hai người | mọi video |
| `bullets` | `en`, `vi` | Kế hoạch, mẹo, tổng kết | mọi video |
| `vocab` | `w`, `vi`, `ex` (+ `pos`) | Từ mới kèm câu ví dụ | Speaking 1, Exam reading |
| `match` | `n`, `q`, `answer` + `image` | Nối với tranh / bản đồ cắt từ trang sách | Speaking 1, Exam listening (bản đồ) |
| `pairs` | `n`, `q`, `answer` + `options` | Nối hai cột | Speaking 2, Exam reading |
| `qa` | `q`, `a` (+ `ask`, `by`, `phrases`) | Câu hỏi – câu trả lời mẫu | Speaking, Consolidation |
| `compare` | `title`, `lines` | So sánh hai cách viết / nói | Writing |
| `errors` | `wrong`, `right` (+ `note`) | Sửa lỗi | Speaking 2, Consolidation |
| `practice` | `q` (+ `hint`) | "Đến lượt bạn" có đếm ngược | Speaking, Consolidation |
| `order` | `k`, `text`, `pos` (+ `label`, `short`) | Sắp xếp thứ tự | Writing 1, 3, Vocabulary |
| `timing` | `label`, `minutes` | Chia thời gian làm bài | Writing 1 |
| `letter` | `text` (+ `note`, `say`, `body`) | Đọc nguyên một lá thư / bài đọc, ghi chú lề | Writing, Exam reading |
| `blanks` | `n`, `answer` (+ `tip`) | Ô nghe – chép; có `q` chứa `___` (+ `hint`) thì là câu điền từ | Vocabulary, Consolidation, Exam listening |
| `mcq` | `n`, `q`, `options`, `answer` (+ `keys`) | Trắc nghiệm a/b/c hoặc 1/2/3 | Exam listening, Exam reading |

Trường của cảnh: `chapter` (tên chương — nút nhảy trong app), `heading`, `heading_vi`, `hide_text` (bài nghe:
thanh phụ đề chỉ hiện người nói và "Listen carefully…"), `roles` (vai trong cảnh, ví dụ
`{emma: receptionist, tom: guest}`). Trường của dòng thoại: `say`, `vi`, `focus`, `reveal`, `wait` + `note`
(đếm ngược), `pause`, `read` (chỉ trong `letter`). Có thể dùng neo YAML (`items: &notes` … `items: *notes`) để
cảnh nghe và cảnh đáp án dùng chung một danh sách câu.

## 5. Cách đọc (`say`) và những lỗi đã gặp

| Chữ trên màn hình | `say` | Vì sao |
|---|---|---|
| A (chữ cái: "from A to F", "Part A says", "Exercise A") | `eigh` | Đứng trước một từ khác, Kokoro đọc "A" thành mạo từ /ɐ/; viết `eigh` ở mọi chỗ cho chắc |
| IELTS | `eye-elts` | Đọc từng chữ cái |
| Hue, Hanoi, Da Nang, Ho Chi Minh | `Whey`, `Ha Noi`, `Dah Nahng`, `Ho Chee Min` | Tên riêng tiếng Việt |
| Nguyen Thi Anh Vien | `Win Tee Ahn Vee-en` | Tên người Việt |
| Riyadh, Lan | `Ree-yahd`, `Lahn` | Tên riêng |
| Sir/Madam | `Sir or Madam` | Dấu `/` bị bỏ qua |
| 150, 2004, 104 (số phòng) | `a hundred and fifty`, `two thousand and four`, `one oh four` | Số đọc theo cách người bản xứ nói trong ngữ cảnh |
| H-U-N-T (đánh vần) | `aitch, you, en, tee` | Chữ cái rời đọc sai |
| dấu gạch dài `–` giữa câu | thay bằng dấu chấm / phẩy | Kokoro không ngắt hơi ở `–` |

Những lỗi đã gặp và cách tránh:

- **Mạng**: Hugging Face bị chặn; model Kokoro lấy từ npm (`kokoro-q8-shards`, `kokoro-js`), xem `agents/README.md`.
  Thiếu model thì công cụ dùng Flite — **không commit video Flite đè video Kokoro** (test kiểm nhãn `engine`).
- **Chữ tràn / quá nhỏ**: câu đáp án dài trong cảnh `errors` bị thu nhỏ tới khó đọc → rút gọn (`I am writing to apply
  for the job …`) và để câu đầy đủ trong lời thoại.
- **Ô to vô ích**: ô mẹo của `blanks` và thẻ `mcq` từng kéo tới đáy khung → nay cao vừa nội dung (đợt 9).
- **Lộ đáp án trong bài nghe**: phụ đề hiện lời thoại → đặt `hide_text: true` cho cảnh nghe, tách cảnh đáp án riêng.
- **Mục lục sai thứ tự**: `lessons.json` xếp theo chữ cái (Consolidation trước Speaking) → app xếp nhóm theo thứ tự
  phần trong `book.json` (đợt 9).
- **Workbook / file nghe thiếu**: ghi rõ trong video và kịch bản; không đoán đề.
- **Cây git phải sạch** khi kết thúc lượt: dựng video lâu thì commit từng phần.

## 6. Kế hoạch Unit 2 · Learning (sách in tr. 22–33)

Tên mục lấy bằng OCR trang PDF 23–34; kiểm lại khi viết kịch bản.

| Phần (`activity`) | Trang in | Mục trong sách | Video đề xuất | Đáp án / nghe |
|---|---|---|---|---|
| Speaking & Vocabulary (`U02-speaking-vocab`) | 22–23 | Vocabulary 1: subjects at school (sửa chính tả môn học, Pronunciation check); Speaking 1: looking back (nối tranh a–f, Grammar check: quá khứ đơn, *Watch out!* did); Speaking 2: answering questions about the past; Vocabulary 2: likes and preferences | `U02-speaking-1` (Vocabulary 1 + Speaking 1 + Grammar check), `U02-speaking-2` (Speaking 2 + Vocabulary 2) | Answer key ít; track phát âm của phần này không có file MP3 → đọc lại theo Tapescript |
| Listening (`U02-listening`) | 24–25 | Listening 1: numbers and dates (số, số lớn, tháng, số thứ tự, ngày tháng); Listening 2: gọi điện hỏi khóa học (ghi chú 1–12); Key vocabulary in context | Chờ kiểu cảnh phát track (8 track có MP3: U02-L1B … U02-L2A); trước mắt có thể làm video "cách đọc số và ngày tháng" không cần file nghe | Answer key có Listening 2A; Tapescript Track 12–23 |
| Reading (`U02-reading`) | 26–28 | Reading 1: scanning (5 trích đoạn trang web học lái xe, đúng/sai); Reading 2: practise scanning ("Swimming – safe and fun!"); Key vocabulary; Workbook tr. 8 | `U02-reading` (mcq/pairs/letter như `U01-exam-reading`) | Answer key có Reading 2B |
| Writing (`U02-writing`) | 29–30 | Writing 1: structuring a letter; Writing 2: stating your purpose (thư phàn nàn gửi trường ngôn ngữ); Writing 3: organizing the main part; Writing 4: closing a letter; thư hoàn chỉnh ở tr. 266 | `U02-writing-1` (1 + 2), `U02-writing-2` (3 + 4 + thư mẫu đọc thành tiếng) | Answer key có Writing 3A, 4B; thư mẫu tr. 266 |
| Consolidation (`U02-consolidation`) | 31 | Speaking; Vocabulary (school subjects); Errors | `U02-consolidation` (như `U01-consolidation`) | Gợi ý |
| Exam practice (`U02-exam-practice`) | 32–33 | Reading: "Are A Levels Just Too Easy?" (Text A–D, câu 1–7 chọn đoạn, 8–12 trả lời ≤ 3 từ, Exam tip về Reading Module); Writing: A đúng/sai về bài viết Phần 1, B thư phàn nàn gửi LearnFast Driving School ≥ 150 từ | `U02-exam-reading`, `U02-exam-writing` (giải A, dàn ý và thư mẫu B) | Answer key có Exam practice Writing B; Reading suy ra từ bài, kèm câu bằng chứng |
| Ôn unit + sổ lỗi (`U02-unit-review`) | — | — | Không cần | — |

Thứ tự đề xuất: Speaking & Vocabulary → Writing → Consolidation → Exam practice → Reading (cùng thứ tự đã làm ở
Unit 1), Listening sau khi có kiểu cảnh phát track.

## 7. Kiểm tra trước khi commit

```bash
cd agents && python -m lesson_video check ../books/ielts_target_5_0/lessons/*.yaml
python -m pytest -q                       # kịch bản đã commit khớp lessons.json, video có thật, độ phủ Unit 1
cd .. && python3 web/build.py && git diff --stat
node --test "tests/web/*.test.mjs"        # mục lục video đúng thứ tự phần trong sách
node tests/web/book.e2e.mjs               # nút video trên thẻ unit mở đúng phiên
```

Soát tay mỗi video: nghe đoạn đầu, một đoạn có tên riêng / số và đoạn đọc thư hoặc bài nghe; xem khung hình cảnh
mới; thời lượng và số chương trong `lessons.json` hợp lý.
