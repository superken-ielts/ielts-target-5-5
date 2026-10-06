# 06 — Video bài giảng: hồ sơ Unit 1–2, quy trình và kế hoạch Unit 3

Gom lại toàn bộ việc làm video bài giảng cho **IELTS Target 5.0** — Unit 1 (đợt 3–9) và Unit 2 (đợt 10): phần nào
đã có video, phần nào chưa và vì sao, cách làm một video từ đầu tới lúc gắn vào app, những lỗi đã gặp. Dùng file
này làm căn cứ khi làm **Unit 3** (mục 7) và các unit sau.

Công cụ: `agents/lesson_video` (xem `agents/README.md`). Kịch bản và video: `books/ielts_target_5_0/lessons/`.
Bảng độ phủ ở mục 1–2 in lại được bất cứ lúc nào:

```bash
cd agents && python -m lesson_video coverage ../books/ielts_target_5_0 --unit U01 --unit U02 --unit U03
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
| **Listening** (Listening tr. 12–13; track U01-L1C, L1D, L2A) | Đợt 9 công cụ chưa chèn được file nghe của sách vào video | Làm được ngay: từ đợt 10 có dòng `track` (phát file MP3 của sách trong video) — làm theo mẫu `U02-listening-*.yaml` |
| **Reading** (sách tr. 14–16) | Chưa có yêu cầu; bài đọc dài 3 trang | Làm ngay theo mẫu `U02-reading-*.yaml` (cảnh `passage` tô từ khóa, `letter` đọc bài, `mcq`, `pairs`) |
| **Ôn unit + sổ lỗi** | Không có trang sách — là phiên tự ôn (làm lại câu sai, ghi sổ lỗi) | Không cần video |
| **Workbook tr. 6** (P2-36) | Workbook **không có** trong bộ sách đã nhập | Khi người dùng thêm Workbook hoặc gửi ảnh trang |

## 2. Unit 2 · Learning — độ phủ video

<!-- coverage:U02 -->

**Kết luận:** Unit 2 có video cho **mọi phần có trang sách** (6/7 phần; phần còn lại là phiên tự ôn). Lần đầu
video **phát file nghe thật của sách** (Listening: Track 15–22) và có cảnh **bài đọc tô từ khóa** để dạy dò tìm.
Chưa làm: Workbook trang 8 (chưa có Workbook), Exercise C–D của Listening/Reading chỉ hướng dẫn tự đánh giá.

## 3. Lịch sử từng video

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
| 10 | `U02-speaking-1` Vocabulary 1 & Speaking 1 | Chính tả 8 môn học, đuôi -ics, nối tranh, kể về trường cũ, quá khứ đơn (có / bất quy tắc), *Watch out!*, đuôi -ed /t/ /d/ /ɪd/ | blanks, vocab, match, qa, errors, practice | Chắc chắn (chính tả, dạng quá khứ) + gợi ý (nối tranh); Track 12–13 |
| 10 | `U02-speaking-2` Speaking 2 & Vocabulary 2 | Track 14 đọc lại với **ba giọng** (Emma giám khảo, Tom, Mai `af_bella`), chọn câu trả lời hay hơn, trả lời + lý do + chi tiết, P/N 10 câu, cụm từ thích / không thích, bài nói mẫu của Mai | mcq + `hide_text` + `roles`, compare, blanks, vocab, letter | Tapescript Track 14 + gợi ý |
| 10 | `U02-listening-1` Listening 1: numbers | -teen / -ty, số hàng trăm có *and*, số hàng nghìn; **phát Track 15–17 của sách** | compare, blanks (lưới), bullets + `track` | Tapescript Track 16 |
| 10 | `U02-listening-2` Listening 1: months, ordinals, dates | Sắp chữ thành tên tháng, trọng âm tháng, số thứ tự, hai cách đọc ngày, nghe – viết 4 ngày; **Track 18–21** | blanks, bullets, compare, practice + `track` | Tapescript Track 21 |
| 10 | `U02-listening-3` Listening 2 | 12 câu hỏi cuộc gọi đăng ký khóa nhiếp ảnh, **phát nguyên Track 22**, đáp án kèm câu nghe được, bẫy 96/69, course / class / lesson | blanks (12 dòng) + `track` | Answer key Listening 2A |
| 10 | `U02-reading-1` Reading 1: scanning | Đọc lướt 5 trích đoạn học lái xe, **dò tìm có tô vàng từ khóa**, đúng / sai, skimming ≠ scanning | `passage` + `mark`, blanks, mcq, compare | Suy ra từ bài, kèm câu bằng chứng |
| 10 | `U02-reading-2` Reading 2: practise scanning | Trang web "Swimming – safe and fun!" (đọc thành tiếng, 2 trang), nối tranh, 6 câu trả lời ngắn, từ vựng trong ngữ cảnh, collocations | letter (`words`), match, passage + `mark`, blanks, pairs | Answer key Reading 2B + gợi ý |
| 10 | `U02-writing-1` Writing 1 & 2 | Ba phần của thư, độ dài từng phần, quảng cáo và ghi chú của học viên, chọn câu mở đầu tốt nhất, viết câu mở đầu | order, qa, match (✗), mcq (`keys` 1–4) | Gợi ý |
| 10 | `U02-writing-2` Writing 3 & 4 | Câu chủ đề 4-1-2-3, lời hứa → thực tế, xóa 5 từ thừa, **thư phàn nàn hoàn chỉnh đọc thành tiếng (2 trang)**, cụm từ thư phàn nàn | order, compare, qa, errors, letter (`words`), vocab | Answer key Writing 3A, 4B |
| 10 | `U02-consolidation` Consolidation | Từ để hỏi, Track 23 đọc lại, đến lượt bạn, 8 môn học, have / fail / pass / apply / do, trọng âm Track 25, sửa 6 lỗi | blanks, qa, practice, errors, bullets | Tapescript Track 23 + gợi ý |
| 10 | `U02-exam-reading` Exam practice: Reading | Exam tip bài thi Đọc, cách làm, Emma đọc "Are A Levels Just Too Easy?" (2 trang), câu 1–7 chọn đoạn A–D, 8–12 trả lời ngắn, từ khóa | bullets, letter (`words`), pairs, blanks, vocab | Suy ra từ bài, kèm câu bằng chứng |
| 10 | `U02-exam-writing` Exam practice: Writing | Đúng / sai 8 câu về bài thi Viết phần 1, đề thư gửi Learn Fast Driving School, chia 20 phút, dàn ý, **thư mẫu Terry Black**, từ nối, bảng soát lỗi 3 phút | blanks, bullets, timing, letter (`words`), vocab | Answer key Exam Practice Writing B + gợi ý |

Đợt 4 dựng lại hai video Speaking bằng Kokoro (trước đó là Flite). Mọi video hiện tại: Kokoro q8, Emma `af_heart`,
Tom `am_michael` (và Mai `af_bella` trong `U02-speaking-2`), tốc độ 0,9.

## 4. Quy trình làm một video (đã dùng cho cả 21 video)

1. **Đọc trang sách**: mở trang trong app (tab Sách → phiên học) hoặc kết xuất ảnh trang bằng PyMuPDF; ghi lại số
   trang PDF (`page` trong kịch bản là trang PDF, không phải số in). PDF là bản quét — không có lớp chữ, chép tay
   hoặc OCR bằng `rapidocr_onnxruntime` để lấy chữ.
2. **Tìm đáp án**: Answer key và Tapescript ở cuối sách (số trang PDF ở `answer`, `script` của từng hoạt động trong
   `book.json`). Answer key không có đa số bài của Unit 1 — khi đó ghi rõ "đáp án gợi ý" ở đầu kịch bản và nói
   trong video. Bài nghe **có file MP3** trong `book.json › files` (mã `U02-L1B`…) thì phát thẳng bằng dòng
   `{track: U02-L2A, note: "Track 22 · Listening 2A"}`; **không có file** (ví dụ Track 9, Track 14) thì cho các giọng
   **đọc lại Tapescript** trong cảnh `hide_text: true`.
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

## 5. Kiểu cảnh và khi nào dùng

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
| `passage` | `text` (+ `label`, `note`) | Bài đọc trên màn hình **kèm phụ đề**; dòng thoại `mark` tô vàng cụm từ trong đoạn `focus` — dạy dò tìm | Unit 2 Reading 1, 2 |

Trường của cảnh: `chapter` (tên chương — nút nhảy trong app), `heading`, `heading_vi`, `hide_text` (bài nghe:
thanh phụ đề chỉ hiện người nói và "Listen carefully…"), `roles` (vai trong cảnh, ví dụ
`{emma: receptionist, tom: guest}`), `words` (thư / bài đọc chia hai trang `letter`: số từ của cả bài).
Trường của dòng thoại: `say`, `vi`, `focus`, `reveal`, `wait` + `note` (đếm ngược), `pause`, `read` (chỉ trong
`letter`), `mark` (chỉ trong `passage`), `track` + `start` / `end` + `note` (phát file nghe của sách, thanh phụ đề
hiện nút ▶ và nhãn). Có thể dùng neo YAML (`items: &notes` … `items: *notes`) để cảnh nghe và cảnh đáp án dùng
chung một danh sách câu. Thêm người nói thứ ba chỉ cần khai trong `speakers` (ví dụ Mai `af_bella`).

Mẹo bố cục: thư / bài đọc trên ~170 từ thì chia hai cảnh `letter` (chữ to hơn) và đặt `words`; câu điền từ quá dài
tự thu nhỏ cho vừa một dòng; đáp án `✓` / `✗` trong cảnh `match` dùng phông có ký hiệu.

## 6. Cách đọc (`say`) và những lỗi đã gặp

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
| M-E-R-T-O-N, P-H, I-C-S (đánh vần, cụm chữ) | `em, ee, ar, tee, oh, en` · `P, H` · `I, C, S` | Tách từng chữ bằng dấu phẩy; trên màn hình viết `ph`, `-ics` cho dễ đọc |
| A levels, an A grade | `eigh levels`, `an eigh grade` | Tên kỳ thi / điểm, không phải mạo từ |
| 1970s, 9.00 a.m. | `nineteen seventies`, `nine in the morning` | Năm, giờ đọc theo kiểu nói |
| Picture a / b / c | `Picture eigh`, `Picture B` | "Picture a" đọc thành mạo từ |
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
- **Dựng nhiều video**: Kokoro dùng hết CPU — xếp hàng từng video một (một khóa `flock`), không chạy song song;
  12 video Unit 2 mất khoảng 2,5 giờ. Sửa slide sau khi đã dựng chỉ tốn ~1 phút mỗi video nhờ bộ nhớ tiếng.
- **Bài đọc dài trên một trang**: chữ nhỏ khó đọc → chia hai trang (đợt 10).

## 7. Kế hoạch Unit 3 · Work (sách in tr. 34–45)

Tên mục lấy bằng OCR trang PDF 35–46; kiểm lại khi viết kịch bản. Làm theo đúng khuôn Unit 2 (12 video).

| Phần (`activity`) | Trang in | Mục trong sách | Video đề xuất (mẫu) | Đáp án / nghe |
|---|---|---|---|---|
| Speaking & Vocabulary (`U03-speaking-vocab`) | 34–35 | Speaking 1: talking about work (4 ảnh nghề nghiệp, *This picture shows… This is a good job because…*); Vocabulary 1: jobs and saying what you do (nghe – chép tên nghề, giới từ work for / as / in / with); tính từ P/N (interesting, rewarding, challenging…); Speaking 2: talking about jobs (would you / could you, **Part 2 cue card** "Describe a job…", 1 phút chuẩn bị, nói 2 phút) | `U03-speaking-1` (như `U02-speaking-1`), `U03-speaking-2` (thêm cảnh `timing` 1 + 2 phút cho Part 2) | Answer key tr. 266–267; Track 28–30 không có file → đọc lại (`hide_text`) |
| Listening (`U03-listening`) | 36–37 | Listening 1: listening for gist (4 trích đoạn – tranh, dự đoán); Listening 2: practise listening for gist (4 trích đoạn, câu 5–12 trắc nghiệm); Key vocabulary | `U03-listening-1`, `U03-listening-2` (như `U02-listening-*`, dòng `track`) | Có MP3: U03-L1B, U03-L1F, U03-L2A; Answer key Listening 2A |
| Reading (`U03-reading`) | 38–40 | Reading 1: scanning for paraphrased language; Reading 2: practise scanning (quảng cáo tuyển dụng); Key vocabulary in context | `U03-reading-1`, `U03-reading-2` (như `U02-reading-*`, `passage` + `mark` cho cụm diễn đạt lại) | Answer key Reading 2B |
| Writing (`U03-writing`) | 41–42 | Writing 1: register (trang trọng / thân mật); Writing 2: a letter of application | `U03-writing-1`, `U03-writing-2` (thư xin việc mẫu theo Answer key Writing 2D "Dear Mr Lucas") | Answer key Writing 2D |
| Consolidation (`U03-consolidation`) | 43 | Speaking (hỏi giám khảo về từ không biết, nói 1 phút), Vocabulary (cụm hai phần), Errors | `U03-consolidation` | Gợi ý |
| Exam practice (`U03-exam-practice`) | 44–45 | Listening (làm việc tại nhà, đúng / sai), Reading | `U03-exam-listening`, `U03-exam-reading` | Tapescript tr. 284; file nghe kiểm trong `book.json` trước |
| Ôn unit + sổ lỗi | — | — | Không cần | — |

## 8. Kiểm tra trước khi commit

```bash
cd agents && python -m lesson_video check ../books/ielts_target_5_0/lessons/*.yaml
python -m pytest -q                       # kịch bản đã commit khớp lessons.json, video có thật, độ phủ Unit 1–2
cd .. && python3 web/build.py && git diff --stat
node --test "tests/web/*.test.mjs"        # mục lục video đúng thứ tự phần trong sách
node tests/web/book.e2e.mjs               # nút video trên thẻ unit mở đúng phiên
```

Soát tay mỗi video: nghe đoạn đầu, một đoạn có tên riêng / số, đoạn đọc thư hoặc bài nghe và một đoạn phát file
nghe của sách (âm lượng ngang giọng đọc); xem khung hình cảnh mới; thời lượng và số chương trong `lessons.json` hợp lý.
