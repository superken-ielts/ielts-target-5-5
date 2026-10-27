# 07 — Lộ trình JLPT N5 (GENKI I) và video bài giảng tiếng Nhật

Tài liệu này gồm bốn phần:

- đánh giá bản thiết kế **"MASTER BLUEPRINT: GENKI I (3rd Ed.) × IELTS Target 5.0 Video Pipeline"** (người học gửi ở
  đợt 15);
- những chỗ đã sửa khi chuyển 15 tập của bản thiết kế thành video;
- lộ trình N5 trong tab Sách, dựng từ GENKI I Textbook, Workbook và audio trong `books/Genki/`;
- cách làm video tiếng Nhật, độ phủ hiện tại và kế hoạch các bài sau:
  - Unit 0 có 19 video ngắn để học không cần mở sách (đợt 23, thay năm video của đợt 17);
  - bài 1–3 có bốn video kỹ năng 5–10 phút mỗi bài (đợt 16).

| Thành phần | Ở đâu |
|---|---|
| Sách, audio, hồ sơ lộ trình | `books/Genki/` — `book.yaml` (mẫu `lessons-v1`), `book.json`, `plan.json`, `report.md`, `web/` (đoạn PDF) |
| Kịch bản và video | `books/Genki/lessons/U00-<nn>-<phần>.yaml` (Unit 0), `U0u-<kỹ năng>.yaml` (bài 1–3), `EP_0u_0p.yaml` (bài 4–5) + `.mp4`, `lessons.json` |
| Mẫu lộ trình khai hết trong `book.yaml` | `agents/book_ingest/lessons.py` |
| Tiếng Nhật trong công cụ dựng video | `agents/lesson_video/ja.py` (furigana, cách đọc, romaji), `jpcard.py` (cảnh `jp`) |
| Nhóm lộ trình trong tab Sách | `books/catalog.json › courses` (`ielts`, `ja-n5`) |

In lại bảng độ phủ video (mục 4.1):

```bash
cd agents && python -m lesson_video coverage ../books/Genki --unit U00 --unit U01 --unit U02 --unit U03 --unit U04 --unit U05
```

---

## 1. Bản thiết kế nói gì

| Mục | Nội dung |
|---|---|
| Phạm vi | GENKI I bài 1–5. Mỗi bài 3 tập (15 tập): **Part A** ngữ pháp cốt lõi, **Part B** mẫu câu, **Part C** nói và viết theo một chủ đề IELTS (tự giới thiệu, đồ dùng, thói quen, khu nhà ở, du lịch). Có kế hoạch cho bài 6–12. |
| Một đoạn (segment) | `speaker`, `voice`, `lang_code`, `speed`, `pause_after_sec`, `audio_text` và `visual {header, jp_main, romaji, sub_en, sub_vi}` |
| Giọng | Emma `bf_emma` (tiếng Anh giọng Anh, tốc độ 1.0) giảng; `jp_tutor` `jf_alpha` (0.88; Part C 0.90 trong JSON, nhưng phần chữ ghi 0.92) đọc câu tiếng Nhật |
| Màn hình | 1920×1080, ba tầng: tiếng Nhật + romaji, giải thích tiếng Anh, nghĩa tiếng Việt và ghi chú Hán-Việt. Màu navy / teal / amber, phông macOS (Hiragino) |
| Công cụ | `render_from_md.py` (Kokoro `KPipeline`) đọc JSON nằm trong khối code của các file Markdown; `build_video_from_md.py` vẽ slide bằng PIL rồi ghép từng đoạn bằng ffmpeg, hứa "zero drift" |

## 2. Đánh giá

### 2.1 Nên giữ

- **Ba tầng chữ** Nhật — Anh — Việt, kèm **Hán-Việt** (留学生 = lưu học sinh, 会社員 = hội xã viên). Đây là lợi thế thật
  của người Việt khi học chữ Hán; ít giáo trình nào làm.
- **Nối ngữ pháp với chủ đề IELTS Speaking**: tự giới thiệu (Part 1), thói quen, khu nhà ở, một chuyến đi (Part 2).
  Người học luyện một chủ đề bằng hai thứ tiếng nên nhớ ý lâu hơn.
- Giọng Nhật đọc chậm (0.88) để **nhại theo (shadowing)**; đoạn văn mẫu Part C dùng được làm bài viết mẫu.
- Kịch bản có cấu trúc (người nói, tốc độ, khoảng lặng, chữ trên màn hình) — chuyển sang YAML của `lesson_video` gần
  như một đối một.

### 2.2 Chỗ sai về nội dung — đã sửa trong kịch bản

Đối chiếu với mục lục và trang ngữ pháp của GENKI I (3rd Edition). Mỗi kịch bản ghi lại chỗ sửa ở đầu file.

| Tập | Bản thiết kế | Đã sửa thành | Căn cứ |
|---|---|---|---|
| EP 1.3 | "six-sentence paragraph" | 7 câu ("seven-sentence", "Ghép 7 câu") | Đoạn văn mẫu có 7 câu |
| EP 2.2 | これは日本の本じゃないです (sách của Nhật) | これは日本語の本じゃないです。英語の本ですよ。 | Đối với 英語の本 và nghĩa tiếng Việt "sách tiếng Nhật"; GENKI bài 2 phân biệt 日本の本 / 日本語の本 |
| EP 2.3 | câu cuối dịch lệch | "This book is in Japanese, you know!" cho この本は日本語の本ですよ | Khớp câu tiếng Nhật |
| EP 3.1 | ～ませんか là điểm ngữ pháp 4; "checkGrammar" | điểm **5**; "check Grammar" | Mục lục bài 3 |
| EP 3.2 | trợ từ là điểm 2a, 2b; từ chỉ thời gian là 3 | trợ từ を・で・に・へ là điểm **3**, từ chỉ thời gian là **4** | Mục lục bài 3 |
| EP 3.3 | trạng từ tần suất là điểm 5 | điểm **6** | Mục lục bài 3 |
| EP 4.2 | と là điểm 5, ～時間 là 6 | ～時間 là **6**, と là **8** (điểm 5 là も, điểm 7 là たくさん) | Mục lục bài 4 |
| EP 5.1 | "Grammar Point 1a / 1b" | điểm **1** (tính từ ở hiện tại), điểm **3** (tính từ bổ nghĩa danh từ) | Mục lục bài 5 |
| EP 5.2 | tính từ quá khứ "1c", 好き/きらい "2", ～ましょう "3" | điểm **2**, **4**, **5** | Mục lục bài 5 |
| Part C | tốc độ 0.92 (phần chữ) / 0.90 (JSON) | **0.90** | Lấy theo JSON, nơi thật sự điều khiển giọng |

Những chỗ khác **đã ghi nhận nhưng giữ nguyên**:
- Danh sách ngữ pháp bài 4 của bản thiết kế thiếu も và たくさん. Lộ trình liệt kê đủ.
- Bản thiết kế giải nghĩa ～ましょうか của bài 5 thành "đề nghị giúp". Thực ra đó là điểm 7 của bài 6; ở bài 5 nó nghĩa là "ta cùng … nhé?".
- Câu "ITの会社員" (EP 1.2) hơi gượng; tự nhiên hơn là "IT企業の会社員" hoặc "ITの仕事をしています".
- Bản thiết kế nói dùng "màu của IELTS Target". Thực tế sách IELTS Target dùng băng tiêu đề đỏ. Bộ video N5 giữ navy / teal / amber làm màu riêng.

### 2.3 Cách đọc — giọng đọc sai, sửa bằng `say`

Chữ trên màn hình giữ đúng như sách. Chỗ nào bộ đọc đọc sai thì ghi cách đọc vào `say`. Lệnh `check` tự so cách đọc
với furigana (mục 4.3).

| Giọng | Chữ | Bộ đọc đọc | `say` |
|---|---|---|---|
| Nhật (misaki) | 九時, 七時 | きゅうじ, ななじ | くじ, しちじ (GENKI dạy hai cách này) |
| Nhật | 二十八歳 | はちさい | 二十はっさい |
| Nhật | 日本, 日本語 | にっぽん, にっぽんご | にほん, にほんご |
| Nhật | ベトナム人, 日曜日 | ベトナムひと, にちようひ | ベトナムじん, にちようび |
| Nhật | IT (chữ Latin trong câu Nhật) | bỏ qua | chữ IT kèm furigana アイティー, `say` アイティー |
| Nhật | 午前九時半 | きゅうじ; còn viết `say` toàn kana (ごぜんくじはん) thì は bị đọc như trợ từ "wa" | 午前くじ半 |
| Anh (bf_emma) | cách viết kiểu bản thiết kế: a-re, chi-ka-ku, Genki, des | ay-ree, kye-kah-koo, jeng-kee… | ah-reh, chee-kah-koo, Ghen-kee, dess, mahss, mah-sen, koh-reh, nee-jee-kahn… |
| Anh | IELTS | đọc từng chữ cái | eye-elts |

### 2.4 Sư phạm — chỗ yếu và cách bù trong lộ trình

| Chỗ yếu | Hệ quả | Cách bù |
|---|---|---|
| Mỗi tập chỉ ~30–45 giây (15 tập ≈ 9 phút cho 5 bài) | Video là phần làm nóng, không thay được bài học | Lộ trình lấy **sách làm trục**: mỗi bài 6 phiên × 60 phút, mỗi phiên mở đúng trang và track (mục 3); video gắn vào phiên Part A/B/C. Đợt 16: bài 1–3 có bốn video 5–10 phút mỗi bài, gắn vào bốn phiên (mục 4.1) |
| Bắt đầu ngay bằng ngữ pháp, dựa vào romaji | Không học kana thì không đọc được sách, không thi được N5 | Thêm **Unit 0** (hệ chữ, chào hỏi, số đếm) và phiên **Đọc – viết** mỗi bài (読み書き: hiragana bài 1, katakana bài 2, chữ Hán và bài đọc bài 3–12) |
| JLPT N5 chỉ thi đọc, nghe, chữ – từ, ngữ pháp; không thi nói, viết | Part C (nói – viết theo chủ đề IELTS) có ích cho IELTS hơn cho N5 | Giữ Part C (hai mục tiêu cùng lúc), thêm khối **Ôn thi JLPT N5** (4 phiên: 文字・語彙, 文法・読解, 聴解, thi thử trọn đề) và phiên Workbook có 聞く練習 |
| Khoảng lặng 1,8–2,5 giây sau câu Nhật | Ngắn để nhại theo câu dài | Trong app: "Lặp chương này", lặp đoạn A–B, tốc độ 0,75×. Video bài 1–3 (đợt 16) không chèn khoảng lặng dài — người học tự dừng video (ý người học ở đợt 14); phần nhắc lại dùng bản ghi có khoảng lặng của chính sách (K0u-02, K0u-04) |
| Lời giảng tiếng Anh khoảng B1 | Nặng với người học IELTS band 3–4 | Phụ đề tiếng Việt ở tầng 3; sách GENKI cũng giảng bằng tiếng Anh, nên đây là luyện đọc hiểu tiếng Anh thêm |
| Romaji ở mọi tập | Dễ lệ thuộc romaji | Đề xuất bỏ dòng romaji từ Unit 3 (khi đã học xong hai bảng kana), chỉ giữ cho từ mới. Bài 1–3 (đợt 16) còn romaji ở thẻ câu mẫu; thẻ hội thoại, bài đọc, thẻ đố và thẻ × không có romaji |

### 2.5 Kỹ thuật — vì sao dựng bằng `lesson_video` thay cho script của bản thiết kế

| Bản thiết kế | Vấn đề | `lesson_video` |
|---|---|---|
| `KPipeline` (Kokoro bản PyTorch) | Tải model và giọng từ Hugging Face khi chạy (máy này chặn), nặng | Cùng model Kokoro-82M, bản ONNX q8 (~92 MB) qua `kokoro-onnx`; tiếng Nhật tách âm bằng `misaki[ja]` — đúng bộ tách âm Kokoro dùng khi huấn luyện |
| Phông macOS (Hiragino) | Không chạy trên Linux / CI | Noto Sans CJK JP (`fonts-noto-cjk`), dự phòng IPAGothic, Hiragino, Yu Gothic |
| Emoji trong tiêu đề | Ra ô vuông với phông PIL | Bỏ emoji |
| `textwrap` theo số ký tự | Cắt chữ Nhật / Anh sai chỗ, không có furigana | Đo bề rộng bằng pixel, quy tắc cấm đầu / cuối dòng (kinsoku), furigana trên chữ Hán, tự thu cỡ chữ cho vừa ô |
| Ghép từng đoạn bằng ffmpeg | Mỗi đoạn AAC có phần đệm, cộng dồn thành lệch tiếng — "zero drift" không đúng | Một dải tiếng liền, thời điểm khung hình tính theo số mẫu; có chương (nút nhảy chương, "Lặp chương này") |
| 1920×1080, 60 fps cho slide tĩnh | Tốn dung lượng vô ích | 1280×720, 15 fps, H.264: mỗi tập 0,3–0,6 MB |
| JSON nằm trong khối code Markdown | Sai một dấu phẩy là hỏng cả tập, không kiểm tra được | YAML + `lesson_video check`: furigana, cách đọc so với misaki, romaji, giọng đúng thứ tiếng |
| Pipeline riêng | Hai bộ công cụ cho cùng việc | Dùng chung `lesson_video`: `lessons.json`, gắn vào phiên học, thẻ unit hiện mục lục video |

### 2.6 Kết luận

Ý tưởng tốt khi dùng làm **lớp bổ trợ**: ba tầng chữ có Hán-Việt, nối với chủ đề IELTS, giọng Nhật để nhại theo. Nhưng
như bản thiết kế viết thì chưa đủ để học tới N5: tập quá ngắn, thiếu kana, dựa vào romaji, và pipeline có lỗi kỹ thuật.
Đã làm:
- dựng lại cả 15 tập bằng `lesson_video`, sửa những chỗ ở mục 2.2–2.3;
- đặt các tập vào một lộ trình lấy GENKI I làm trục (mục 3);
- đợt 16: với bài 1–3, thay 9 tập 27–43 giây bằng 12 video 5–10 phút, mỗi bài bốn video Speaking, Writing,
  Listening (phát audio gốc của sách) và Reading (mục 4.1). Bài 4–5 vẫn là tập ngắn của bản thiết kế.

## 3. Lộ trình N5 trong tab Sách

### 3.1 Dữ liệu

| File | Nội dung |
|---|---|
| `Genki I 3rd Edition Textbook.pdf` | 392 trang, **trang in = trang PDF − 8** (trang in 36 = PDF 44) |
| `Genki I 3rd Edition Workbook.pdf` | 157 trang, **trang in = trang PDF − 4** (trang in 16 = PDF 20) |
| `Genki I 3rd Edition Textbook/` | 236 MP3, 409 phút: `JWS_01–13` (hệ chữ), `K00_01–05` (chào hỏi, số), `K01–K12` (会話・文法), `Y01–Y12` (読み書き) |
| `Genki I 3rd Edition Workbook/` | 50 MP3, 52 phút: `W00` (số đếm), `W01_A…W12_C` (聞く練習), `W02_1` (số đếm bài 2), `WY_1–8` (nghe – viết hiragana), `W_JWS1/2` (bảng hiragana / katakana) |

Mã track trong app là **nhãn in cạnh bài tập trong sách**: `K01_05.mp3` → `K01-05`, `W01_A.mp3` → `W01-A`, `W_JWS1.mp3`
→ `W-JWS1`. Học viên thấy nhãn ◀) K01-05 trong trang sách thì bấm nút cùng tên trên thanh audio.

Agent cắt hai PDF thành **51 đoạn** (Textbook 26, Workbook 25; 70 MB). Mỗi đoạn là phần 会話・文法 hoặc 読み書き của một
bài, nên mở trang tức thì cả trên điện thoại. Sách không có đáp án Workbook: đáp án nằm ở sách GENKI Answer Key
(`missing: [answer-key]`).

### 3.2 Một bài = 6 phiên × 60 phút

| Bước | Phiên | Mở trang | Track | Video bài 1–3 | Video bài 4–5 |
|---|---|---|---|---|---|
| `words` | Hội thoại & từ vựng | 会話 (Dialogue) + 単語 (Vocabulary) | hội thoại, từ vựng J-E / E-J | Listening | — |
| `part-a` (lõi) | Part A · Ngữ pháp cốt lõi | 文法 (Grammar) + 表現ノート / Culture Notes | — | — (ngữ pháp giảng trong Speaking, Writing) | EP u.1 |
| `part-b` | Part B · Mẫu câu | 練習 (Practice) | các bài luyện có nhãn track | Speaking | EP u.2 |
| `part-c` (lõi) | Part C · Nói & viết theo chủ đề | まとめの練習 (Review Exercises) + Pair Work + Useful Expressions | track trong phần ôn (nếu có) | Writing | EP u.3 |
| `read-write` | Đọc – viết | 読み書き của bài (Textbook) + nút trang Workbook 読み書き | `Y…` (+ `WY`, `W-JWS2`) | Reading | — |
| `workbook` | Workbook & ôn bài | Workbook phần 会話・文法 của bài | `W…` (聞く練習) | — | — |

Unit 0 có hai phiên: **Hệ chữ Nhật & hiragana** (Japanese Writing System, track JWS + W-JWS1, trang Workbook 11–12)
và **Chào hỏi & số đếm** (あいさつ, すうじ, track K00 + W00, trang Workbook 13–15).

Từ đợt 17, mỗi phiên Unit 0 có video. Video có đủ bảng chữ, câu chào, số đếm và phát audio gốc, nên học được không cần
mở sách:
- phiên Hệ chữ: Hiragana 1, Hiragana 2, Katakana & chữ Hán;
- phiên Chào hỏi: Greetings, Numbers.

Khối **Ôn thi JLPT N5** dùng đề mẫu
chính thức của JLPT (jlpt.jp), không có trang sách. Tổng: **13 unit + 1 khối ôn thi = 78 phiên ≈ 79 giờ**. Mặc định
4 phiên/tuần, tức **20 tuần**; chọn được 3–5 phiên/tuần. Học song song, không tính vào 12 giờ/tuần của IELTS.

### 3.3 Trang (số in) và track của từng bài

| Bài | Hội thoại & từ vựng | Part A | Part B | Part C | Đọc – viết (Textbook · Workbook) | Workbook |
|---|---|---|---|---|---|---|
| 0 | JWS 20–27 · chào hỏi, số 30–35 | | | | Workbook 11–12, 13–15 | |
| 1 | 36–40 · K01-01…08 | 41–45 | 46–53 · K01-09…23 | 54–55 · K01-24 | 296–299 · 121–127 · Y01-1…6, WY-1…8 | 16–22 · W01-A…D |
| 2 | 56–59 · K02-01…06 | 60–66 | 67–75 · K02-07…15 | 76–81 | 300–303 · 23–24, 128–132 · Y02-1…3, W-JWS2 | 25–31 · W02-1, W02-A…C |
| 3 | 82–85 · K03-01…06 | 86–93 | 94–99 · K03-07…15 | 100–101 | 304–307 · 133–134 · Y03 | 32–40 · W03-A…D |
| 4 | 102–106 · K04-01…08 | 107–114 | 115–124 · K04-09…19 | 124–127 | 308–311 · 135–136 · Y04 | 41–49 · W04-A…C |
| 5 | 128–131 · K05-01…08 | 132–137 | 138–143 · K05-09…16 | 144–145 | 312–317 · 137–138 · Y05-1…2 | 50–58 · W05-A…C |
| 6 | 146–149 · K06-01…08 | 150–155 | 156–163 · K06-09…15 | 163–165 | 318–323 · 139–140 · Y06 | 59–68 · W06-A…C |
| 7 | 166–169 · K07-01…06 | 170–175 | 176–183 · K07-07…14 | 183–185 | 324–328 · 141–142 · Y07 | 69–77 · W07-A…C |
| 8 | 186–189 · K08-01…06 | 190–197 | 198–205 · K08-07…18 | 205–209 | 329–333 · 143–144 · Y08 | 78–86 · W08-A…C |
| 9 | 210–213 · K09-01…08 | 214–218 | 219–226 · K09-09…17 | 226–229 | 334–339 · 145–146 · Y09-1…2 | 87–95 · W09-A…C |
| 10 | 230–233 · K10-01…06 | 234–238 | 239–248 · K10-07…15 | 248–253 | 340–345 · 147–148 · Y10 | 96–104 · W10-A…C |
| 11 | 254–257 · K11-01…10 | 258–263 | 264–268 · K11-11…14 | 269–271 | 346–351 · 149–150 · Y11-1…2 | 105–110 · W11-A…C |
| 12 | 272–275 · K12-01…06 | 276–281 | 282–289 · K12-07…14 | 290–294 | 352–356 · 151–152 · Y12 | 111–118 · W12-A…C |

Hai phiên dùng chung một trang khi まとめの練習 bắt đầu giữa trang (bài 4, 6, 7, 8, 9, 10). Trang 28–29 (nhân vật) không
thuộc phiên nào. Báo cáo đầy đủ: `books/Genki/report.md`.

### 3.4 Cách dò ranh giới, cách sửa

Agent không đoán cấu trúc GENKI. Ranh giới các phần dò một lần rồi ghi vào `book.yaml › refs`:
1. Lấy trang đầu mỗi bài từ bookmark của PDF.
2. OCR trang Textbook PDF 36–302 bằng RapidOCR ở 150 DPI. Tìm nhãn track (`K01-05`, `K05.07(J-E)` …) và đầu mục:
   chữ "Grammar" cách điệu, dòng "Grammar 1" ở đầu phần 練習, まとめの練習 / Review Exercises, Culture Notes, Useful
   Expressions.
3. Soát bằng mắt mọi trang chuyển phần. Nhiều đầu mục OCR không đọc được: 練習 của bài 6, 7; まとめの練習 của bài
   7–12, vì bài 7–12 không ghi "Review Exercises". Nhãn track bị sót thì suy ra theo thứ tự số.
4. Với Workbook: dùng mục lục (trang in 5–8), OCR thêm các trang có nhãn track đặc biệt.

Sửa một phiên: đổi `pages` / `tracks` trong `refs` của bài đó rồi chạy lại
`cd agents && python -m book_ingest ingest ../books/Genki` và `python3 web/build.py`. Agent báo lỗi trong các trường
hợp: track không có, khoảng track đi ngược, một track gán hai lần, còn track chưa thuộc phiên nào, trang vượt quá file.

## 4. Video bài giảng tiếng Nhật

### 4.1 Độ phủ (đợt 23)

Unit 0 có 19 video ngắn (đợt 23), học được không cần mở sách. Đợt này thay năm video của đợt 17, vì người học góp ý:
chữ trên màn hình không khớp lời Emma, giọng Nhật đọc mà không có lời dịch, học quá nhanh, và cả đoạn hiện một lúc nên
không biết giọng Nhật đang đọc tới đâu. Cách sửa ở mục 4.2–4.3.

| Phiên | Video | Nội dung | Dài |
|---|---|---|---|
| Hệ chữ Nhật & hiragana | `U00-01-start` | Unit 0 học gì, để làm gì (đọc được bài 1, chào hỏi và số dùng ngay ở bài 1); thứ tự 19 video; cách xem (chữ sáng màu cam, tầng Anh – Việt, YOUR TURN); mỗi ngày một video | 2:37 |
| | `U00-02-vowels` | Ba loại chữ trong một câu; あいうえお từng chữ một, mẹo phát âm cho người Việt; viết; từ chỉ có nguyên âm | 3:10 |
| | `U00-03-rows-k-s` | Hàng か, さ (し là shi); đọc từ; ôn 15 chữ | 3:00 |
| | `U00-04-rows-t-n` | Hàng た (ち, つ), な; đọc từ; ôn 25 chữ | 3:13 |
| | `U00-05-rows-h-m` | Hàng は (ふ), ま; は / へ làm trợ từ đọc khác; đọc từ; ôn 30 chữ | 3:27 |
| | `U00-06-rows-y-r-w` | Hàng や, ら, わ và ん; đọc từ; cả bảng 46 chữ với JWS-01 | 4:10 |
| | `U00-07-hiragana-practice` | Chữ dễ nhầm; chữ in khác chữ viết tay; nghe – viết 8 chữ; đọc từ đã biết (からて, すもう…) | 3:39 |
| | `U00-08-marks` | ゛ ゜ theo từng hàng (か / が…); 25 âm với JWS-02; đọc từ | 4:06 |
| | `U00-09-small-ya-yu-yo` | や to và ゃ nhỏ (びよういん / びょういん); 33 âm ghép; JWS-03; đọc từ | 4:41 |
| | `U00-10-small-tsu-long-vowels` | っ (JWS-04 từng từ); ん + hàng な (JWS-05); trường âm (JWS-06); ん đọc n / m / ng, nguyên âm bị nuốt, cao độ (JWS-07, 08); đọc từ | 4:44 |
| | `U00-11-katakana-1` | Katakana dùng khi nào; sáu chữ giống hiragana; hàng ア đến ホ theo nhóm; viết | 3:21 |
| | `U00-12-katakana-2` | Hàng マ đến ン; cả bảng với JWS-09; chữ dễ nhầm (シ ツ ソ ン…) | 3:45 |
| | `U00-13-katakana-3` | ゛゜ và ャュョ (JWS-10, 11); trường âm ー (JWS-12) | 3:39 |
| | `U00-14-katakana-4` | Âm ngoại lai (JWS-13 từng cặp); từ mượn, tên tiếng Việt; làm quen chữ Hán | 3:26 |
| Chào hỏi & số đếm | `U00-15-greetings-1` | Chào theo giờ trong ngày, cảm ơn, xin lỗi, đáp lời; mỗi câu: Emma nói tình huống → Yuki / Takeshi → lượt bạn → K00-01 | 4:01 |
| | `U00-16-greetings-2` | Tạm biệt, ở nhà, bữa ăn, gặp lần đầu, cúi chào | 3:14 |
| | `U00-17-greetings-3` | Luyện tập: 10 tình huống đố (bài A); tự giới thiệu (bài B) | 2:34 |
| | `U00-18-numbers-1` | 0–10 từng số; cách đọc thứ hai của 0, 4, 7, 9; 11–19; K00-02; đếm 1–20 | 5:13 |
| | `U00-19-numbers-2` | Hàng chục và 100; mọi số đến 99; K00-02; bài A, B, C; nghe – viết số dễ nhầm; tổng kết Unit 0 | 4:44 |

19 video, **1:10:43**, 42 MB, 3–8 chương mỗi video. Mỗi video bắt đầu bằng cảnh "In this video" (học gì, để làm gì)
và kết thúc bằng video tiếp theo học gì.

Bài 1–3 có bốn video mỗi bài, mỗi video gắn vào phiên luyện đúng kỹ năng đó:

| Bài | Listening (Hội thoại & từ vựng) | Speaking (Part B) | Writing (Part C) | Reading (Đọc – viết) | Tổng |
|---|---|---|---|---|---|
| 1 New Friends | `U01-listening` K01-01…04, đố giờ, tuổi, số điện thoại (7:20) | `U01-speaking` chào hỏi, X は Y です, か, なん, の, giờ, tuổi, hội thoại (8:07) | `U01-writing` hiragana / katakana, tên tiếng Việt, đoạn tự giới thiệu (5:31) | `U01-reading` 読み書き bài 1 với Y01-1…6 (8:29) | 29:26 |
| 2 Shopping | `U02-listening` K02-01…04, đố giá tiền, của ai, ở đâu (9:05) | `U02-speaking` これ / この / ここ, giá, ください, だれの, も, じゃないです, ね / よ (6:12) | `U02-writing` katakana, giá tiền, số bằng hiragana, đồ dùng, hội thoại mua hàng, chính tả (5:49) | `U02-reading` 読み書き bài 2 với Y02-1…3 (6:22) | 27:28 |
| 3 Making a Date | `U03-listening` K03-01…04, đố lịch một ngày (8:42) | `U03-speaking` ます / ません, を・で・に, thời gian, tần suất, ～ませんか (6:06) | `U03-writing` 15 chữ Hán, thứ tự nét, đoạn văn một ngày, tin nhắn mời, chính tả (5:56) | `U03-reading` chữ Hán số, giá tiền, まいにちのせいかつ với Y03, đúng / sai (6:45) | 27:28 |

- 12 video, **1:24:22**, 59 MB, 7–11 chương mỗi video.
- Giọng Kokoro q8: Emma `bf_emma` (tốc độ 1.0), Yuki `jf_alpha` và Takeshi `jm_kumo` (0.88). Unit 0 (đợt 23) chậm
  hơn một nhịp: Emma 0.9, Yuki và Takeshi 0.78, nghỉ 0.8 giây giữa hai câu, 1.5 giây giữa hai cảnh.
- Part A và Workbook không có video riêng. Ngữ pháp của Part A được giảng trong Speaking và Writing.

Bài 4–5 vẫn là 6 tập ngắn của bản thiết kế (đợt 15):

| Bài | Part A | Part B | Part C | Tổng |
|---|---|---|---|---|
| 4 The First Date | `EP_04_01` あります / います, vị trí (0:38) | `EP_04_02` でした / ～ました, 時間, と (0:46) | `EP_04_03` khu nhà ở, cuối tuần (0:31) | 1:55 |
| 5 A Trip to Okinawa | `EP_05_01` tính từ hiện tại, bổ nghĩa (0:46) | `EP_05_02` tính từ quá khứ, 好き, ましょう (0:45) | `EP_05_03` chuyến đi Đà Nẵng (0:36) | 2:07 |

GENKI có 37 video. Bài 6–12 chưa có video.

### 4.2 Làm một video N5

1. Chép kịch bản cùng kỹ năng của bài trước: `U01-speaking.yaml`, `U01-writing.yaml`, `U01-listening.yaml` hoặc
   `U01-reading.yaml`.
   - `activity`: Listening → `U<nn>-words`, Speaking → `U<nn>-part-b`, Writing → `U<nn>-part-c`, Reading →
     `U<nn>-read-write`.
   - Ghi chú (`notes`) của bước đó trong `book.yaml › units` nói video có gì. Sửa xong chạy lại
     `python -m book_ingest ingest ../books/Genki`.
2. Cảnh `kind: jp` có một hoặc nhiều thẻ trong `items`. Mỗi thẻ có `jp` (furigana `{漢字|かな}`), `romaji`, `en`, `vi`.
   - Dòng thoại chọn thẻ bằng `focus` (đếm từ 0). Cảnh nhiều thẻ có số `k/n` ở góc phải thanh tiêu đề.
   - Câu của Yuki / Takeshi viết bằng chữ thường. Lệnh `check` gom các câu theo thẻ đang hiện rồi so với `jp` của
     thẻ: hoặc mỗi câu khớp cả thẻ (đọc hai lần), hoặc các câu ghép lại khớp thẻ. Chỗ bộ đọc sai thì viết kana trong
     câu, hoặc thêm `say`.
   - `track: K01-01` phát file nghe của sách (mã trong `book.json › files`). `start` / `end` cắt một đoạn; `note` hiện
     cạnh nhãn "BOOK AUDIO · K01-01".
   - `quiz: true` là thẻ đề: câu hỏi nghe, giá tiền viết bằng chữ Hán để tự đọc… Thẻ đề không bị kiểm cách đọc và được
     để chữ Hán không furigana. Thẻ đáp án đặt ngay sau.
   - Thẻ `× …` là câu sai: không ai đọc, không có romaji. Thẻ `○ …` ngay sau là câu đúng.
   - **Mỗi dòng mang lời dịch của chính nó** (đợt 23). Câu của Emma có `vi` (tiếng Việt của đúng câu đó). Câu tiếng
     Nhật và dòng `track` có `en` + `vi`. Với chữ cái, `en` là cách đọc (`shi — like she`), `vi` là cách đọc gần
     đúng cho người Việt (`shi — như “she” tiếng Anh, không phải “si”`). Dòng thiếu thì tầng đó hiện `en` / `vi` của
     thẻ. Câu trên thẻ đố (`quiz`) không ghi `en` / `vi` để khỏi lộ đáp án.
   - **Câu tiếng Nhật phải nằm trên thẻ đang hiện**: tầng 1 luôn hiện chữ của câu đang đọc. Câu không có trên thẻ thì
     thêm thẻ và chuyển `focus`.
   - **Tô sáng chỗ đang đọc** (đợt 23).
     - Câu tiếng Nhật và dòng `track` mặc định tô cả thẻ (trừ thẻ đố).
     - `hl` chọn chữ: số thứ tự (đếm từ 0), danh sách, hoặc `all`. Chữ của thẻ ngăn bởi dấu cách, `　`, xuống dòng,
       `・ / | 、 。 —` (`ja.card_tokens`). Câu Emma có `hl` thì chữ đó sáng lên khi cô nói về nó.
     - `step` (cả bài, hoặc từng dòng) > 0: câu tiếng Nhật nhiều phần (`か、き、く。`, `はじめまして。ゆきです。`) đọc
       từng phần, nghỉ `step` giây; phần đang đọc sáng màu cam, phần đã đọc xanh nhạt. Số phần phải bằng số chữ được
       tô (`hl` theo thứ tự đọc, ví dụ bảng hai cột).
     - Dòng `track` với `step`: file nghe tách theo khoảng lặng, mỗi đoạn có tiếng một chữ, chỗ nghỉ giãn ra ≥ `step`.
       Số đoạn phải bằng số chữ được tô — chỉnh `start` / `end` để bỏ lời giới thiệu. File đọc mỗi câu kèm lời dịch
       (K00-01) hay có っ (khoảng lặng giữa từ) thì cắt mỗi câu một dòng `start` / `end`, `hl` chữ đó và `step: 0`.
   - Cảnh `jp` có `wait` (đếm ngược để người học nói, viết, đọc thẻ đố) và `echo: true` (sau câu tiếng Nhật, đếm ngược
     dài theo câu để nhắc lại). Thẻ hiện nhãn cam "YOUR TURN · LƯỢT CỦA BẠN" và vòng đếm ngược; tầng 2–3 hiện `note` và
     `vi` của dòng. `echo` thì cả câu vừa đọc sáng lên.
3. Chạy `python -m lesson_video check <kịch bản>`. Lệnh báo các lỗi:
   - chữ Hán thiếu furigana;
   - câu đọc từng phần mà số phần khác số chữ được tô; dòng `track` mà số đoạn có tiếng khác số chữ được tô;
   - chữ cái hay âm ghép đọc riêng bị đọc sai (へ đọc "e" như trợ từ; mỗi phần của câu đọc từng phần được so riêng với
     chữ của nó);
   - cách đọc misaki khác furigana (kèm cách đọc misaki của từng chữ Hán để biết sửa chỗ nào);
   - romaji khác cách đọc (romaji kiểu GENKI được chấp nhận: `ee` = `ei`, `oo` = `ou`);
   - chữ Latin trong câu Nhật, trừ chữ có cách đọc như `{DC|ディーシー}`;
   - `focus` ngoài số thẻ;
   - giọng không phải `jf_*` / `jm_*`.
4. Lời Emma có từ Nhật hoặc tên riêng thì viết lại trong `say` cho giọng Anh (mục 2.3). Kiểm bằng
   `k.tokenizer.phonemize(text, "en-gb")`.
5. Xem trước không tiếng: `--engine silent --out /tmp/x --work /tmp/x/w`, mở `f*.png`.
6. Dựng: `python -m lesson_video build <kịch bản> --engine kokoro`.
   - Video bài 1–3 dài **5–10 phút**. Đoạn nghe của sách tính cả vào: hội thoại bài 2 dài 50 và 40 giây, bản có khoảng
     lặng 77 và 75 giây. Video Unit 0 ngắn hơn, **2,5–5 phút**, mỗi video một phần nhỏ (đợt 23).
   - Tiếng đã đọc nằm trong `~/.cache/lesson_video/tts`, nên dựng lại chỉ đọc những câu mới.
   - Bỏ một video: xóa `.yaml`, rồi chạy `python -m lesson_video prune ../books/Genki`. Lệnh bỏ mục trong
     `lessons.json` và file `.mp4`.
7. Chạy `python3 web/build.py`. In lại bảng mục 4.1 bằng lệnh `coverage`, rồi cập nhật `04-checklist.md` và
   `05-lich-su-thay-doi.md`.

### 4.3 Cảnh `jp` và phần tiếng Nhật của công cụ

- **Khung 1280×720, bốn dải.**
  - Thanh tiêu đề: nhãn amber `tag` + `heading`.
  - Tầng 1: thẻ trắng. Có nhãn người nói `JP · YUKI — …` hoặc `EN · EMMA — …` theo màu người nói, câu Nhật cỡ
    60 → 22 px (thẻ một hàng chữ cái chữ to để nhìn rõ nét), furigana trên chữ Hán, romaji màu teal.
  - Tầng 2, 3 hiện **đúng câu đang nói** (đợt 23; trước đó luôn là `en`, `vi` của thẻ nên không khớp lời Emma):
    - Emma nói: "EMMA SAYS" + chữ của câu, "DỊCH LỜI EMMA" + `vi` của câu.
    - Câu tiếng Nhật, file nghe: "ENGLISH" + `en`, "TIẾNG VIỆT" + `vi` của dòng.
    - Đếm ngược: "YOUR TURN" + `note`, "LƯỢT CỦA BẠN" + `vi`.
    - Dòng thiếu chữ cho tầng nào thì tầng đó hiện `en` / `vi` của thẻ, nhãn cũ "ENGLISH EXPLANATION / MEANING",
      "NGHĨA TIẾNG VIỆT & GHI CHÚ HÁN-VIỆT".
  - Đoạn văn dài thì tầng 1 cao lên, tầng 2–3 co lại vừa chữ dài nhất sẽ hiện ở tầng đó trong lúc thẻ còn trên màn
    hình (không nhảy khung giữa các câu).
- **Tô sáng, đọc từng chữ** (đợt 23).
  - Chữ đang đọc: nền cam nhạt, gạch chân cam. Chữ vừa đọc xong trong câu: nền xanh nhạt. Romaji sáng cùng chữ khi
    chia được đúng bằng số chữ trên thẻ (`ja.romaji_tokens`: ngăn bởi `· / | — ,` nếu có, không thì theo dấu cách;
    xuống dòng luôn ngăn).
  - `script.reading_plan` quyết định chữ nào sáng và câu đọc thành mấy phần; `check` và lúc dựng dùng chung hàm này.
  - Câu đọc từng phần: mỗi phần đọc riêng bằng Kokoro, thêm `。` cuối phần (`ja.as_said`: は đứng riêng không có 。 bị
    đọc "wa"), mỗi phần một khung hình. Kokoro không ngắt ở `、` (か、き、く、け、こ liền một mạch 1.6 giây), nên không
    tách được một câu đọc liền — phải đọc từng phần.
  - File nghe: `timeline.speech_spans` tách theo khung 20 ms (to hơn đỉnh − 35 dB là có tiếng, nghỉ < 0.2 giây không
    tách chữ, mẩu < 0.08 giây bỏ). Chữ sau sáng lên 0.15 giây trước tiếng. Tách ở 16 kHz cho cả `check` lẫn lúc dựng.
  - Âm ghép đọc riêng (みょ, りょ, ぎょ…): misaki đọc tách thành hai âm dù viết hiragana hay katakana, nên `ja.phonemes`
    đưa thẳng âm vị cho Kokoro: phụ âm mềm + nguyên âm (みょ → `mʲo`), đúng dạng misaki dùng cho âm nó đọc đúng.
- **Xuống dòng.**
  - Ưu tiên ngắt sau vạch ngăn nhóm `|` `/` `・`, rồi mới tới `—` `vs.`. Nhờ vậy cặp "オランダ — アムステルダム"
    không bị tách khi dòng còn `・`. Sau đó mới tới dấu cách.
  - Vạch ngăn ở cuối dòng bị bỏ, nên không dòng nào bắt đầu bằng `/` hay `・`.
  - Số thứ tự `5.` `Q2.` đi cùng phần sau. Danh sách đánh số viết `1. … / 2. …`, không dùng khoảng trắng toàn khổ.
  - Dòng chữ Latin đầy tới khi từ tiếp theo không vừa.
  - Dòng cuối chỉ còn vài chữ (dưới 1/4 dòng) thì nhỏ chữ thêm tối đa 6px nếu nhờ đó bớt được một dòng.
  - Áp quy tắc kinsoku. Cụm katakana liền nhau không bị tách.
  - `\n` trong `jp` / `romaji` là xuống dòng bắt buộc (đợt 17). Bảng chữ viết mỗi hàng một dòng; trong hàng và giữa
    các cột dùng khoảng trắng toàn khổ `　`. Ví dụ bảng hiragana hai cột, bảng âm ghép ba cột như sách.
- **Người nói.**
  - `lang: ja` và giọng `jf_*` / `jm_*`.
  - `speed` theo người nói hoặc theo từng dòng (0.5–2.0).
  - Tiếng nhớ theo (giọng, chữ, tốc độ).
- **Nhiều thẻ, audio của sách (đợt 16).**
  - Cảnh nhiều thẻ có số `k/n` ở góc phải thanh tiêu đề.
  - Dòng `track` thay nhãn người nói bằng nhãn teal "BOOK AUDIO · K01-01" có hình ▶, kèm `note`.
  - Số khoanh ①–⑦ và dấu ○ × vẽ bằng phông CJK, vì phông Latin không có. ✓ ✗ không có trong phông nào, nên thẻ dùng
    ○ ×.
- **Cài thêm.**
  - `misaki[ja]==0.7.4` bằng `uv pip install` (pip thường lỗi khi dựng `unidic-lite` trên Debian).
  - Phông `fonts-noto-cjk`.
  - Xem `agents/README.md`.

### 4.4 Lỗi đã gặp

- **Video dài hơn tiếng 3–8 giây** (EP 2.3, 3.3, 4.3 hỏng ở lần dựng đầu).
  - Nguyên nhân: bộ lọc `loudnorm` giữ lại ~3 giây tiếng, nên `-shortest` của ffmpeg không cắt được video. Lỗi lộ ra
    khi video chỉ có vài khung hình dài.
  - Sửa: chuẩn độ to ở một lệnh ffmpeg riêng rồi mới ghép hình (`video.py`). Độ dài video giờ khớp tiếng tới từng
    khung hình; mọi video, kể cả IELTS, dựng về sau đều theo cách này.
- **Nút "Tapescript của track" vẫn hiện** khi track không có tapescript, ví dụ track GENKI.
  - Nguyên nhân: `.btn{display:inline-flex}` đè thuộc tính `hidden`. Sách IELTS không lộ lỗi vì track nào cũng có
    tapescript.
  - Sửa: thêm `.btn[hidden]{display:none}` vào `book.css`.
- **misaki đọc sai chữ Hán**, xem mục 2.3. Kiểm tra tự động bắt được mọi chỗ trong 15 tập.
- **misaki đọc sai ở bài 1–3 (đợt 16).**
  - Các chữ: 日本人 (thành にっぽんにん), アメリカ人 (アメリカにん), 四時 (よんじ), いま何時 (いまなんどき), 何を (なんを),
    土曜日 (どようひ), 明日 (あす, GENKI dùng あした), 時 đứng một mình (とき).
  - Chữ cái は đọc là "wa".
  - Sửa: viết kana trong câu thoại, hoặc dùng `say` (chữ cái は viết ハ).
- **Kana viết liền bị tách sai.** さんびゃく, ろっぴゃく viết bằng hiragana bị unidic tách thành さん / び / ゃ / く, nên
  giọng đọc thành "bi-ya-ku". `check` bắt được vì romaji không khớp. Sửa: câu thoại viết 三百, 六百 (misaki đọc
  đúng), thẻ vẫn hiện hiragana.
- **Romaji của こんにちは ra `konnichiha`** vì misaki giữ chữ は. Sửa: `ja._said` lấy cách phát âm của unidic cho は / へ
  cuối từ.
- **Romaji kiểu GENKI không khớp.** `gakusee`, `Soo desu ka` khác `gakusei`, `Sou`. Sửa: chuẩn hóa `ei` = `ee`,
  `ou` = `oo`.
- **Độ dài ngoài 5–10 phút.**
  - U02-writing dựng lần đầu chỉ 3:56. Thêm cảnh viết số bằng hiragana (biến âm) và cảnh chính tả.
  - U03-writing ước 4:20 trước khi dựng. Thêm cảnh thứ tự nét và cảnh chính tả.
  - U03-reading ước 5:12. Thêm mẹo đọc câu không có dấu cách và cảnh đố đúng / sai.
  - U02-listening ước 9:45. Bỏ một lần phát lại hội thoại II.
- **Ngắt dòng xấu trên thẻ** (thấy khi soát khung hình video thật).
  - Lỗi: "5." hay "Q2." treo cuối dòng; cặp nước — thủ đô bị tách đôi; dòng bắt đầu bằng `/` hay `・`; "か。" rơi
    một mình xuống dòng; chữ Latin xuống dòng sớm một từ.
  - Sửa: viết lại quy tắc ngắt dòng của `jpcard` (mục 4.3), thêm test, rồi dựng lại cả 12 video.
- **Máy khởi động lại giữa lúc dựng.** Tiếng đã đọc còn trong bộ nhớ đệm, nên dựng lại không phải đọc lại.
- **Chữ đứng một mình bị đọc sai (đợt 17, video Unit 0).**
  - は và へ đứng riêng bị đọc như trợ từ ("wa", "e"). Sửa: `say` viết katakana ハ, ヘ.
  - Âm ghép đọc rời bị tách thành hai âm, ví dụ みょ thành "mi-yo" (にゅ, ひゃ, みゃ, りゃ, ぎょ, びゃ, ぴゃ). Chỉ một mẫu
    đọc đúng cả 11 hàng: katakana "キャ。キュ。キョ、". `check` bắt được mọi chỗ vì romaji không khớp. Đợt 23 đọc từng
    âm riêng nên mẫu này không dùng được nữa (みょ, りょ, ぎょ sai ở mọi cách viết): `ja.phonemes` đưa thẳng âm vị
    (mục 4.3), `check` so âm ghép đọc riêng với romaji của chính nó.
  - フィ đứng riêng thành "fu-i", dù trong フィリピン thì đọc đúng. Các âm ngoại lai để audio gốc JWS-13 đọc, Yuki chỉ
    đọc từ ví dụ.
- **Bảng chữ dồn thành dòng dài** (cả bảng hiragana trên ba dòng, các hàng cách nhau bằng `/`). Sửa: thêm `\n` (mục
  4.3).
- **Ước tính dưới 5 phút.**
  - Hiragana 1 ước 5:10. Thêm phần chữ in khác chữ viết tay và phần nghe – viết chữ cái.
  - Numbers ước 4:51. Thêm phần nghe – viết các cặp số dễ nhầm (14 / 40, 17 / 70, 19 / 90).
- **Video Unit 0 khó theo (đợt 23, góp ý của người học).**
  - Lỗi: chữ trên màn hình không khớp lời Emma; giọng Nhật đọc mà không có lời dịch; học quá nhanh; cả đoạn hiện một
    lúc nên không biết giọng Nhật đang đọc tới đâu; không nói bài học để làm gì.
  - Nguyên nhân: tầng 2–3 luôn là `en` / `vi` của thẻ; một video gói nhiều phần; Kokoro đọc cả hàng chữ liền một mạch
    (không ngắt ở `、`); tốc độ 1.0 / 0.88, nghỉ 0.45 giây.
  - Sửa: tầng 2–3 theo câu đang nói, câu nào cũng có `vi` (và `en` với câu tiếng Nhật); tô sáng chữ đang đọc, đọc từng
    chữ (`step`), file nghe tách theo khoảng lặng; đếm ngược YOUR TURN trong cảnh `jp`; nhịp chậm hơn (mục 4.1); 19 video
    2,5–5 phút, mỗi video mở đầu bằng "học gì, để làm gì" và có video mở đầu cả Unit 0.
- **Emma đọc romaji kiểu tiếng Anh** (đợt 23, lệnh `phonemes` và soát phiên âm từng câu có romaji): chi thành "kai",
  ji thành "jai", ki thành "kai", ya thành "yuh", nguyên âm a i u e o thành tên chữ cái "ay, eye, you, ee, oh", Takeshi
  thành "Take-shi", Ai Honda thành "A-I Honda", desu thành "di-soo", ng thành "en-gee"; động từ use / uses đọc như danh
  từ. Màn hình vẫn hiện romaji, `say` viết lại:

  | Chữ | `say` | | Chữ | `say` |
  |---|---|---|---|---|
  | chi, cha / chu / cho | chee, chah / choo / cho | | a, i, u, e, o (nguyên âm Nhật) | ah, ee, oo, eh, oh |
  | ji, zu | jee, zoo | | Takeshi | Tahkehshee |
  | ki | kee | | Ai (tên) | Eye |
  | ya, yu, yo | yah, yoo, yoh | | desu | dess |
  | use / uses (động từ) | yooz / yoozes | | ng | the ng in sing |

  Còn đúng, không cần `say`: ka, sa, ta, na, ha, ma, ra, wa, ba, pa, shi, tsu, fu, Yuki; "read" quá khứ phân từ ("is read
  wa"). "hiragana" đọc /hɜːrəˈɡɑːnə/, để nguyên như video bài 1–3.
- **Từ có は đầu từ trong danh sách bị đọc như trợ từ** (đợt 23): はいく đọc "wa iku". `check` bắt được vì romaji
  không khớp. Sửa: `say` viết ハイク.
- **っ là khoảng lặng giữa từ**, nên tách file nghe theo khoảng lặng thì かった, さっか, チェック, デュエット thành hai đoạn
  (JWS-04, JWS-13). Sửa: mỗi từ một dòng `start` / `end`, `hl` chữ đó; cặp có っ thì `step: 0`.
- **K00-01 đọc mỗi câu chào bằng tiếng Nhật rồi tiếng Anh** (ASR cho thấy, mục 4.6), nên không tách theo khoảng lặng
  được. Sửa: mỗi câu chào một dòng `start` / `end`, `step: 0`; câu chào cả hai lời đều sáng, tầng 2 hiện lời dịch.
- **Romaji nhiều dòng không sáng** (`a i u e o\nka ki …`): xuống dòng bị tính là vạch ngăn kiểu `·`, nên cả dòng là một
  chữ. Sửa: chỉ `· / | — ,` mới đổi cách chia; xuống dòng luôn ngăn hai chữ.

### 4.5 Kế hoạch bài 4–12

Từ bài 4, dùng khung bốn video của bài 1–3, mỗi video 5–10 phút:

| Video | Phiên | Cách làm (theo bài 1–3) |
|---|---|---|
| Speaking | Part B | Điểm ngữ pháp của bài (bảng dưới) qua câu mẫu: Emma giảng, Yuki / Takeshi đọc; hội thoại của sách; câu hỏi về bản thân |
| Writing | Part C | Chữ (kana, chữ Hán của bài 読み書き), ghép câu, đoạn văn mẫu theo chủ đề IELTS, chính tả (かきとり, thẻ `quiz`), lỗi hay gặp (thẻ × / ○), bài tập |
| Listening | Hội thoại & từ vựng | Track K0u-01…04: nghe hai lần tìm đáp án, đáp án, đọc theo, bản có khoảng lặng; đố nghe. Hội thoại dài thì bỏ bớt một lần phát |
| Reading | Đọc – viết | Bài tập 読み書き của sách theo thứ tự (I-A, I-B, II…) với track Y; mẹo đọc; đố đúng / sai |

Bài 4–5 thay ba tập ngắn hiện có. Ngữ pháp ở cột Part A, B đi vào video Speaking và Writing; chủ đề IELTS ở cột Part C
đi vào đoạn văn mẫu của Writing.

| Bài | Part A (điểm ngữ pháp) | Part B | Part C — chủ đề IELTS |
|---|---|---|---|
| 6 | thể て, ～てください, nối hai hành động (1–3) | ～てもいいです, ～てはいけません, ～から, ～ましょうか (4–7) | Một ngày của bạn; nội quy nơi làm việc / trường (Part 1: work & study) |
| 7 | ～ている: đang làm, kết quả (1–2) | mô tả người, thể て nối câu, ～に行く, ～人 (3–6) | Tả một người trong gia đình (Part 2: describe a person) |
| 8 | thể ngắn, văn nói thân mật (1–2) | ～と思います, ～と言っていました, ～ないでください, のが好き, が, 何か/何も (3–8) | Nêu ý kiến về đồ ăn, nấu ăn (Part 3: opinions) |
| 9 | quá khứ thể ngắn (1–2) | ～と思いました…, bổ nghĩa danh từ, もう/まだ, から (3–7) | Kể một sự kiện đã xem (Part 2: an event) |
| 10 | so sánh hai / nhiều vật (1–2) | ～の, ～つもり, ～なる, どこかに/どこにも, で (3–7) | Kế hoạch kỳ nghỉ, so sánh phương tiện (Part 1/3: travel) |
| 11 | ～たい, ～たり～たりする (1–2) | ～ことがある, や (3–4) | Trải nghiệm và mong muốn: nơi muốn đến (Part 2) |
| 12 | ～んです, ～すぎる (1–2) | ～ほうがいいです, ～ので, ～なければいけません, ～でしょうか (3–6) | Sức khỏe và lời khuyên (Part 1: health) |

### 4.6 Mốc thời gian audio Unit 0 (đợt 23)

Lời giới thiệu tiếng Anh ở đầu mỗi file JWS và thứ tự chữ lấy bằng ASR (Parakeet, `transcribe.recognizer`, chạy trên
từng đoạn có tiếng). Dùng khi đặt `start` / `end` cho dòng `track`:

| File | Nội dung | Dòng `track` |
|---|---|---|
| JWS-01 | giới thiệu tới 11.1 giây; 46 hiragana từ 13.4 | `start: 13.2`, `hl` theo thứ tự đọc của bảng hai cột |
| JWS-02 | giới thiệu tới 4.4; 25 âm có dấu | `start: 4.6` |
| JWS-03 | giới thiệu tới 4.4; 33 âm ghép từ 6.7 (きゃ … ぴょ) | `start: 6.0`, `hl` theo cột của bảng ba cột |
| JWS-04 | giới thiệu tới 4.0; かった 6.3, かた 8.1, さっか 9.7, はっぱ 11.7, ざっし 13.9 | mỗi từ một dòng |
| JWS-05 | giới thiệu tới 1.5; さんねん 3.3, あんない 5.4 | `start: 3.0` |
| JWS-06 | giới thiệu tới 9.1; 9 từ trường âm từ 10.6 | `start: 10.0` |
| JWS-07 | giới thiệu tới 3.1; すきです 4.9 | `start: 4.5` |
| JWS-08 | giới thiệu tới 3.8; あさ, なまえ, たかい từ 5.5 | `start: 5.0` |
| JWS-09 | giới thiệu tới 6.7; 46 katakana | `start: 7.6` |
| JWS-10 | giới thiệu; 25 âm có dấu từ 6.5 | `start: 5.8` |
| JWS-11 | giới thiệu tới 4.4; 33 âm ghép từ 6.4 | `start: 6.0` |
| JWS-12 | giới thiệu tới 10.2; カー, スキー, スーツ, ケーキ, ボール từ 12.6 | `start: 12.0` |
| JWS-13 | giới thiệu tới 4.0; 13 cặp "âm – từ" từ 6.3 (ウィ ハロウィーン … デュ デュエット) | mỗi cặp một dòng |
| K00-01 | あいさつ 0.4; 19 câu chào, mỗi câu tiếng Nhật rồi tiếng Anh (すみません có hai lời dịch); câu thứ 18 là ほんだあいです | mỗi câu một dòng, `step: 0` |
| K00-02 | すうじ 0.5; 0–10 kèm cách đọc thứ hai (ゼロ れい … よん し よ … きゅう く じゅう, 2.2–33.2), 11–19 (12 cách đọc, 33.6–58.2), hàng chục và 100 (từ 58.4) | ba dòng, mỗi số một chữ trên thẻ |

## 5. Việc còn treo

- Video bài 4–12 theo khung bốn kỹ năng ở mục 4.5 (bài 4–5 thay ba tập ngắn hiện có).
- Đáp án Workbook: cần sách GENKI Answer Key. Khi có thì khai thêm `files` và trỏ `answer` cho phiên Workbook.
- Đề mẫu JLPT N5 và file nghe để vào thư mục sách thì khối Ôn thi có trang và track như các bài.
- Thẻ Anki từ vựng GENKI: chưa có. App có kế hoạch thẻ từ FSRS (P3-04).
