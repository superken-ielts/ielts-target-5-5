# 09 — Oxford Word Skills Basic: từ vựng A1–A2 học song song, video 7–10 phút

Đợt 26, người học thêm cuốn *Oxford Word Skills Basic* vào repo (commit `cbfc72c`) và yêu cầu:
- rà cuốn sách;
- đưa vào menu tab Sách;
- học bằng video 7–10 phút, không đếm ngược;
- mỗi video có 1–2 phần luyện nói theo chủ đề từ vựng của unit.

| Thành phần | Ở đâu |
|---|---|
| Sách, hồ sơ lộ trình | `books/book_oxford_word_skills_basic/`: `Oxford_Word_Skills_Bas.pdf` (bản quét, 254 trang), `book.yaml` (mẫu `lessons-v1`), `book.json`, `plan.json`, `report.md`, `web/` (122 đoạn PDF, 83 MB) |
| Dữ liệu dò trang | `books/book_oxford_word_skills_basic/work/`: `scan.json`, `chunks.json`, `ocr-pages.json` (OCR dải đầu / chân trang), `ocr-answer-key.json` (unit nào ở trang Answer key nào) |
| Vị trí trong tab Sách | `books/catalog.json`: nhóm `ielts`, sau English Unlimited A2, trước IELTS Target 5.0 |
| Mẫu lộ trình | `agents/book_ingest/lessons.py`: tên bước dùng được `{title}`, `{no}`… như ghi chú (đợt 26, mục 4) |
| Video bài giảng | `books/book_oxford_word_skills_basic/lessons/` (kịch bản `.yaml`, `.mp4`, `lessons.json`); sổ tay ở mục 5 |

---

## 1. Đánh giá sách

### 1.1 Sách gồm gì

*Oxford Word Skills Basic* (Ruth Gairns, Stuart Redman, Oxford University Press 2008) dạy từ vựng cho trình độ
Elementary – Pre-intermediate (A1–A2).

- **80 unit ngắn**, mỗi unit 1–3 trang, gom thành **11 module** theo chủ đề. Mỗi module kết thúc bằng một bài Review
  2–6 trang:
  - Basic English;
  - People;
  - Everyday life;
  - Food and drink;
  - Getting around;
  - Places;
  - Study and work;
  - Hobbies and interests;
  - Holidays;
  - Social English;
  - Language (tính từ, trạng từ thông dụng, động từ bất quy tắc, cụm động từ, giới từ, từ nối, have, get).
- Mỗi unit theo một khuôn:
  1. Tranh hoặc bảng từ có ví dụ.
  2. 2–4 bài tập.
  3. Phần **ABOUT YOU**: nói hoặc viết về bản thân bằng từ vừa học.
  4. **Test yourself**: che bảng từ, nói lại.
- Đầu sách có Introduction (tr. 8–9) và **Starter** (tr. 10–13): cách dùng một unit, cách học từ mới (nhắc lại, ghi
  vở, viết câu, dùng từ điển), các từ chỉ dẫn bài tập (tick, underline, circle…), ký hiệu và bảng phiên âm.
- Cuối sách:
  - **Vocabulary building** (tr. 199–201);
  - **Common irregular verbs** (tr. 202);
  - **Answer key** (tr. 205–235): đáp án mọi bài, kể cả câu trả lời mẫu cho ABOUT YOU ("Answers from a British
    person", "… from an Argentinian person");
  - **Word list** có phiên âm (tr. 237–254).
- Hơn 2.000 từ và cụm từ mới. Theo lời giới thiệu, cả bộ ba cuốn (Basic, Intermediate, Advanced) gần như phủ trọn
  Oxford 3000; cuốn Basic là phần thông dụng nhất.

### 1.2 Vì sao hợp với người học này

- **Chủ đề trùng IELTS:** phần lớn unit đúng chủ đề IELTS Speaking Part 1 (số, giờ, ngày tháng, gia đình, nhà, quần
  áo, đồ ăn, thời tiết, sở thích, kỳ nghỉ) và các tình huống General Training (điền phiếu, mua sắm, hỏi đường, biển
  báo, đi khám, công việc).
- **Tự học được:** Answer key đầy đủ và có câu trả lời mẫu. Unit ngắn, nên mỗi ngày học xong một unit trong khoảng
  30 phút.
- **Bù đúng chỗ thiếu:** giáo trình chính (English Unlimited A2, IELTS Target 5.0) dạy kỹ năng; cuốn này bù vốn từ cơ
  bản mà band 3.0 còn thiếu, theo chủ đề nên nói được ngay.

### 1.3 Hạn chế và cách bù

| Hạn chế | Cách bù |
|---|---|
| Bộ dữ liệu không có CD-ROM (không có audio phát âm, bài nghe) | Video đọc mọi từ mới bằng giọng Kokoro, có phần "Nghe và viết"; Word list cuối sách có phiên âm |
| Sách năm 2008, có vài đồ vật cũ (cassette player, CD player) | Video vẫn dạy theo sách nhưng nói rõ là đồ cũ, thêm từ hiện đại khi cần (whiteboard, screen, dictionary app) |
| Tiếng Anh – Anh (rubber, I've got) | Video nhắc từ Mỹ tương ứng (eraser, I have) và nói rõ IELTS chấp nhận cả hai |
| Answer key có chỗ in nhầm | Video đưa đáp án đúng và nhắc người học. Lỗi đã gặp ghi ở mục 3.3 |
| Trình độ A1–A2: người đã ở band 3.0 thấy hai module đầu dễ | Ghi chú `start_when`: đi nhanh Basic English và People, dồn sức từ module Everyday life |

### 1.4 Chỗ đứng trong lộ trình

Đây là sách **học song song**, không thay giáo trình chính. Người học dùng nó cùng Giai đoạn 0 (English Unlimited A2,
file 08) hoặc Giai đoạn 1 (IELTS Target 5.0): mỗi ngày một unit, 5 phiên một tuần. Tuần của cuốn này đếm riêng
(`start_week: 1`).

## 2. Lộ trình trong tab Sách

**92 phiên:** Starter unit, 80 unit, 11 phiên Review. Mỗi phiên 30 phút, 5 phiên một tuần, tổng 19 tuần.

- Mỗi unit một phiên, tên phiên có chủ đề, ví dụ "Unit 1 · Numbers · từ vựng, bài tập, nói". Phiên mở đúng trang
  sách; nút thứ hai mở trang Answer key của unit đó.
- Ghi chú phiên ghi việc cần làm:
  1. xem video (không đếm ngược);
  2. làm bài trong sách, chữa bằng Answer key;
  3. nói phần ABOUT YOU thành tiếng rồi so với câu mẫu;
  4. chép 5–8 từ vào Anki;
  5. làm Test yourself.
- Starter unit có thêm nút Vocabulary building (tr. 199–201) và Word list (tr. 237–254).
- Cuối mỗi module một phiên Review: trang bài ôn trong sách, kèm Answer key phần "Review units".

| Module | Unit | Trang Review | Answer key Review |
|---|---|---|---|
| 1 Basic English | 1–7 | 23–25 | 225 |
| 2 People | 8–16 | 42–45 | 225–226 |
| 3 Everyday life | 17–23 | 61–64 | 227 |
| 4 Food and drink | 24–28 | 75–77 | 228 |
| 5 Getting around | 29–33 | 87–89 | 228–229 |
| 6 Places | 34–41 | 105–108 | 229–230 |
| 7 Study and work | 42–47 | 122–125 | 230 |
| 8 Hobbies and interests | 48–53 | 138–140 | 230–231 |
| 9 Holidays | 54–59 | 150–152 | 231–232 |
| 10 Social English | 60–69 | 168–171 | 232–233 |
| 11 Language | 70–80 | 193–198 | 233–234 |

Không có track: sách không kèm audio (`missing: [cd-rom]`).

## 3. Dò trang

### 3.1 Độ lệch trang

File PDF là bản quét 254 trang. So với sách in, bản quét **thiếu hai trang trắng**: tr. 204 (sau trang tựa Answer
key) và tr. 236 (trước Word list). Vì vậy `book.yaml` khai cùng một PDF ba lần, mỗi lần một `page_offset`:

| id | Trang in | Trang PDF |
|---|---|---|
| `course-book` | 1–203 | trang in + 1 |
| `answer-key` | 205–235 | = trang in |
| `word-list` | 237–254 | trang in − 1 |

Cách dò:
- OCR dải chân trang bằng `rapidocr-onnxruntime` (cài bằng `pip install -e ".[ocr]"`), ra `work/ocr-pages.json`.
- Số trang in đọc được ở 244/254 trang.
- Soát thêm bằng mắt 11 trang Review và 12 trang đầu unit.

### 3.2 Trang Answer key của từng unit

OCR tiêu đề "Unit N" trên các trang 205–224, ra `work/ocr-answer-key.json`. Mỗi unit trỏ tới trang có tiêu đề của nó.
Nếu đáp án tràn sang trang sau (unit N+1 bắt đầu ở trang sau), unit trỏ tới cả hai trang. Unit 72 trỏ thêm Common
irregular verbs (tr. 202).

### 3.3 Answer key in nhầm (đã gặp)

| Unit | Bài | Answer key ghi | Đúng theo nhãn trong sách |
|---|---|---|---|
| 6 | 2 | 4 a · 5 from/in · 8 asked · 9 spoke | 4 *a preposition*: from / in · 5 *an indefinite article*: a · 8 *an irregular past simple*: spoke · 9 *a regular past simple*: asked |

Gặp lỗi mới thì thêm vào bảng này. Video phải nói rõ chỗ in nhầm, vì người học chữa bài bằng Answer key.

## 4. Mẫu `lessons-v1`: tên bước có chỗ thay (đợt 26)

Trước đợt 26, mọi phiên của một bước có cùng tên, ví dụ "Unit 1 · từ vựng". Sách này có 80 unit, mỗi unit đúng một
bước, nên danh sách phiên không cho biết unit nào học gì.

Đợt 26, `lessons.py` thay chỗ trong **tên bước** như đã làm với ghi chú, dùng chung hàm `_fill`:
- `title: "{title} · từ vựng, bài tập, nói"` cho ra "Unit 1 · Numbers · từ vựng, bài tập, nói";
- chỗ thay sai (ví dụ `{bogus}`) báo `ProfileError` có ghi "tên bước".

Các sách cũ không dùng chỗ thay trong tên bước, nên `book.json` / `plan.json` của chúng không đổi (test hồi quy chạy
lại ra y hệt).

## 5. Video bài giảng — khuôn 7–10 phút

### 5.1 Yêu cầu

- Mỗi unit một video **7–10 phút**, gắn vào phiên của unit đó.
- **Không đếm ngược:** không dùng `wait` / `echo`. Muốn người học trả lời thì Emma nói "Pause the video and try",
  "Pause the video after each sentence"…, rồi Tom (hoặc Emma) chữa ngay.
- **1–2 phần luyện nói** theo chủ đề từ vựng của unit:
  - Nói 1 (`qa`): Tom và Emma hỏi đáp qua lại;
  - Nói 2 (`practice` không có `wait`): người học tự tạm dừng và trả lời.

### 5.2 Bộ cảnh của một video

| # | Cảnh | Kiểu | Nội dung |
|---|---|---|---|
| 1 | Giới thiệu | `title` | Unit học gì; nhắc "no countdown, pause the video" |
| 2 | Từ vựng | `bullets` / `compare` | Từ của trang sách theo nhóm. Emma đọc, Tom đọc tiếp hoặc dùng từ trong câu. Thêm điểm phát âm (trọng âm, -teen / -ty), Anh – Mỹ, ngữ pháp đi kèm (Spotlight) |
| 3 | Bài tập trong sách | `blanks` (nhiều câu) hoặc `mcq` (≤ 6 câu) | Đề như sách. Emma: "Pause the video and try". Tom đọc đáp án theo Answer key, có lý do cho câu khó |
| 4 | Thêm ngoài sách (tùy unit) | `blanks` / `bullets` | Câu đố mô tả đồ vật, tự đặt câu hỏi, mẹo IELTS: đoán loại từ cần điền, xin nhắc lại câu hỏi, đánh vần tên |
| 5 | Nghe và viết | `blanks` | Emma đọc 6 câu, người học tạm dừng sau mỗi câu và viết từ còn thiếu. Tom chữa, đánh vần từ khó. Như IELTS Listening phần 1 |
| 6 | Nói 1 | `qa` | 7–10 cặp hỏi đáp về chủ đề: ABOUT YOU của sách (Emma dùng câu mẫu Answer key nếu có), chủ đề IELTS Part 1 gần nhất |
| 7 | Nói 2 · đến lượt bạn | `practice` (self-paced) | 5 câu hỏi có gợi ý. Emma đọc hết, `pause: 0.5`, câu cuối `pause: 1.5` |
| 8 | Tổng kết | `bullets` | 4 điều cần nhớ, Test yourself của sách, unit tiếp theo |

Ước lượng thời lượng: dựng thử bằng bộ đọc im lặng. Video thật lệch ước lượng từ −10 đến +27 giây (mục 5.6). Ước
lượng dưới 7:00 thì thêm cảnh ở hàng 4 (có ích cho IELTS) chứ không kéo dài câu thoại.

### 5.3 Quy ước kịch bản

- Đầu file ghi:
  - trang sách và trang Answer key;
  - bài nào theo Answer key, bài nào tự làm;
  - phần thêm ngoài sách;
  - **chi tiết nhân vật mới**.
- Đặt tên: `id: U0N-slug`, `activity: U0N-words`, `tag: "BASIC ENGLISH · UNIT N"`. Module sau dùng tên module, ví dụ
  `"PEOPLE · UNIT 10"`.
- Tom và Emma khớp hồ sơ ở file 06 mục 9.4. Chi tiết mới của các video sách này ghi ở mục 5.7 dưới đây.
- Câu ngôi thứ nhất (My…, I…, We…) do Emma hay Tom đọc, kể cả câu "Nghe và viết", là chuyện của chính nhân vật đó.
  Câu như vậy phải khớp hồ sơ; không thì viết trung tính (the hotel, the party, the football coach).
- Chữ trên màn hình dùng phông Liberation Sans: **không** dùng ✓ ✗ (không có glyph). Ký hiệu IPA (/ɪ/, /ə/…) và → thì
  hiện được.
- Bài trên 6 câu không dùng `mcq`: thẻ quá hẹp, chữ bị cắt. Dùng `blanks` dạng `"câu  →  ___"`.
- Từ ghép viết liền thì đưa cả từ vào đáp án (`notice → noticeboard`). Không tách thành `notice___`, vì ô trống có
  khoảng cách nên nhìn như hai từ.

### 5.4 Quy trình một unit

1. Xem trang sách (`pdftoppm -f <trang PDF> -r 110`) và trang Answer key (độ phân giải cao hơn nếu chữ nhỏ). Ghi đáp
   án, đối chiếu nhãn câu hỏi với Answer key (mục 3.3).
2. Viết kịch bản theo mục 5.2–5.3, rồi chạy:
   ```bash
   cd agents && python -m lesson_video check ../books/book_oxford_word_skills_basic/lessons/<id>.yaml
   ```
3. Soát cách đọc bằng `python -m lesson_video phonemes <kịch bản>` và sửa bằng `say` (mục 5.5).
4. Ước lượng thời lượng, rồi xem vài khung hình bằng bộ đọc im lặng (`tts.Silent()` + `Slides.render`, như
   `preview.py` trong đợt 26). Dưới 7:00 thì thêm cảnh; chữ tràn thì sửa.
5. Dựng từng video một (Kokoro dùng hết CPU):
   ```bash
   cd agents && python -m lesson_video build ../books/book_oxford_word_skills_basic/lessons/<id>.yaml
   ```
6. Chạy `python3 web/build.py`, rồi cập nhật bảng mục 5.7, file 04 và file 05.

### 5.5 Cách đọc (`say`) riêng của sách này

| Viết | `say` | Vì sao |
|---|---|---|
| thirteen, eighteen… (khi dạy hoặc cuối câu) | `thir-teen`, `eigh-teen` | Kokoro nhấn âm đầu, nghe như thirty |
| use (động từ) | `yooz` | Đọc /juːs/ như danh từ (⚠ của `phonemes`) |
| close (động từ: đóng cửa) | `cloze` | Đọc /kloʊs/ như tính từ. Đợt 26 thêm vào bảng ⚠ của `phonemes`. "close friends" (tính từ) đúng, để nguyên |
| chữ cái khi đánh vần | `eigh, bee, see, dee, ee, ef, gee, aitch, eye, jay, kay, el, em, en, oh, pee, ar, ess, tee, yoo, vee, double you, ex, why` | Viết "A" thì Kokoro đọc như mạo từ /ə/; "ay" đọc thành /aɪ/ |
| mạo từ khi nói về chính từ đó (*A and an are…*, *the is…*) | `eigh`, `ann`, `thee` | Dạng yếu /ə/, /ən/, /ðə/ nghe như nuốt mất |
| IELTS | `eye-elts` | Kokoro đọc từng chữ cái |
| Da Lat, Hanoi, Tran, Tuan | `Dah Lot`, `Ha Noi`, `Chan`, `Twan` | Tên Việt theo hồ sơ nhân vật |
| Czechs | `Checks` | Kokoro đọc /tʃɛkz/ |
| cà phê sữa đá, phở, bánh mì, cái ô | `kah feh suh dah`, `fuh`, `bahn mee`, `kai oh` | Chữ tiếng Việt có dấu đọc sai hoàn toàn |
| pasaporte | `pah-sah-por-tay` | Từ tiếng Tây Ban Nha |
| Wednesday đọc sai kiểu người học (cố ý) | `Wed-nes-day` | Để Emma chữa |
| CD player, the UK | `C D player`, `the U K` | Chữ viết tắt phải đọc từng chữ cái |

Từ thường đúng, không cần `say`: Anki, Mandarin, Cantonese, Australasia, Portuguese, Egypt, comfortable, island,
Wednesday, umbrella, tomato (Kokoro đọc kiểu Mỹ; muốn kiểu Anh thì `tomahto`).

### 5.6 Lỗi đã gặp

- **Video ngắn hơn 7 phút:** bản dựng đầu của Unit 1 dài 6:36. Thêm "Nghe và viết" và câu hỏi đáp thì thành 7:26.
  - Ước lượng im lặng khá sát: U01 ước 7:31, thật 7:26; U02 ước 7:03, thật 7:14; U04 ước 7:16, thật 7:43; U07 ước
    7:18, thật 7:07.
  - Unit chỉ có một trang (Unit 5, 6, 7) cần thêm 1–2 cảnh ngoài sách: ước lượng đầu tiên chỉ 5:45–6:21.
- **Thẻ `mcq` 9 câu chữ bị cắt** (Unit 4 bài 1): đổi sang `blanks` "câu → T / F (sửa)".
- **✓ ✗ không có trong phông** (Unit 5 tiêu đề phụ): viết chữ "tick / cross", trả lời Yes / No.
- **Answer key in nhầm** (Unit 6 bài 2): mục 3.3.
- **Hàng đợi dựng bị ngắt giữa chừng:** lệnh chạy nền của phiên làm việc (agent) mặc định chỉ chạy 30 phút. Ba lệnh nền
  cùng chờ một khóa `flock` bị ngắt khi đang dựng Unit 6 và Unit 7. Dựng nhiều video thì gộp vào **một** lệnh với thời
  hạn dài (tối đa 2 giờ); bị ngắt thì dựng lại, câu đã đọc lấy từ bộ nhớ đệm nên nhanh.
- **Câu nghe – viết vô tình thành chuyện của Emma, mâu thuẫn hồ sơ:**
  - Unit 3: "My birthday is on the twenty-second of June", trong khi cùng video đó Emma sinh 15/9;
  - Unit 1: "There are thirty students in my class";
  - Unit 4: "My teacher is Portuguese", trong khi cùng video có danh sách giáo viên 5 nước.

  Đã viết lại thành câu trung tính (quy ước ở mục 5.3) và dựng lại Unit 1–4.

### 5.7 Độ phủ video và chi tiết nhân vật

Module Basic English đủ 7/7 unit, tổng 51:08.

| Unit | Video | Dài | Chương | Bài trong sách | Nói 1 (Tom ↔ Emma) | Nói 2 (đến lượt bạn) | Thêm ngoài sách |
|---|---|---|---|---|---|---|---|
| 1 Numbers | `U01-numbers` | 7:26 | 12 | 1–3 | Những con số quanh bạn (8 cặp) | 5 câu | -teen / -ty, số lớn, số trong đời sống (điện thoại, giá, %) |
| 2 The time | `U02-time` | 7:14 | 11 | 1, 2, 4, Test yourself | Giờ giấc ở nước bạn (10) | 5 câu | buổi trong ngày, nearly / just after |
| 3 Days and dates | `U03-days-dates` | 7:10 | 12 | 2, 5, 6, 7 | Về bạn và đất nước bạn (9: Tết, 30/4, 2/9, sinh nhật) | 5 câu | đọc và viết ngày tháng kiểu Anh / Mỹ |
| 4 Countries and nationalities | `U04-countries` | 7:43 | 14 | 1–4 | Quê hương và ngôn ngữ (8) | 5 câu | the British / Italians, Britain và the UK, trọng âm -ese / -ian |
| 5 Classroom vocabulary | `U05-classroom` | 7:10 | 13 | 1–3 | IELTS Part 1 "Bags", "Pens and writing" (9) | 5 câu | a piece of paper, I've got, borrow / lend, đoán đồ vật "It's a thing you use to…" |
| 6 English language words | `U06-language-words` | 7:18 | 13 | 1, 2 (sửa lỗi Answer key) | Học ngữ pháp và từ (7) | 5 câu | động từ có quy tắc / bất quy tắc, chữ viết tắt trong từ điển, mẹo IELTS đoán loại từ cần điền |
| 7 Questions about language | `U07-questions-language` | 7:07 | 12 | 1, 2 | Hỏi về từ ngữ (8: exhausted, cà phê sữa đá, phở…) | 5 câu | I don't know / can't remember / not sure, tự đặt câu hỏi, chữ cái dễ nhầm, đánh vần tên |

Chi tiết nhân vật mới trong các video này đều khớp file 06 mục 9.4:
- **Tom:**
  - số yêu thích 9 (sinh 9/3, áo bóng rổ số 9); không phải người dậy sớm;
  - căn hộ cách trường khoảng 1 km; lớp IELTS khoảng 25 người;
  - năm sau hy vọng đi trao đổi ở Úc;
  - đeo ba lô đi học (laptop, vở, hai bút, điện thoại, chai nước, sách IELTS);
  - nghe giảng thì gõ laptop, luyện viết IELTS bằng tay;
  - tra từ bằng app → chép vở → Anki, ôn mỗi tối;
  - ở nhà có bàn, ghế, laptop, bảng ghim kế hoạch học; lớp hồi phổ thông khoảng 40 học sinh, bảng đen;
  - thấy mạo từ khó nhất, có sách ngữ pháp kèm đáp án; từ yêu thích "delicious";
  - thích cà phê sữa đá; họ Trần.
- **Emma:**
  - sinh 15/9, thích tháng 12; quê khoảng 15.000 dân;
  - dậy lúc 6 giờ, học tiếng Việt trước bữa sáng; đến Việt Nam ngày 4/8/2023 (khớp "dạy ở TP. HCM đã ba năm");
  - nói tiếng Anh, Pháp, chút tiếng Việt;
  - năm nay có 2 học viên Hàn, 1 học viên Nhật;
  - trường có 12 giáo viên từ 5 nước: 2 người Anh, 1 người Scotland, còn lại người Ireland, Mỹ, Úc, Việt;
  - túi có bút viết bảng, bìa phiếu bài tập, laptop, sổ ghi từ tiếng Việt; ghi từ tiếng Việt bằng bút chì (hay sai dấu);
  - hồi đi học có từ điển tiếng Pháp bằng giấy; thầy dạy tiếng Pháp giao danh sách động từ mỗi tuần;
  - lớp hiện tại nhỏ, sáng, có màn hình lớn; thấy thanh điệu tiếng Việt khó; từ yêu thích "cosy".

### 5.8 Module tiếp theo: People (Unit 8–16, Review tr. 42–45)

| Unit | Gợi ý phần nói | Ghi chú |
|---|---|---|
| 8 Personal information | IELTS Part 1 "Hometown", "Work or study" | Answer key có câu mẫu "Answers from a Greek person" |
| 9 Filling in a form | Điền phiếu như IELTS GT Listening phần 1 | Rất sát đề GT: dùng "Nghe và viết" dạng điền phiếu (tên, địa chỉ, ngày sinh, mã bưu điện) |
| 10 My family | Part 1 "Family" | Gia đình Tom và Emma đã có trong hồ sơ: bố mẹ, chị, em trai, ông |
| 11–12 Physical actions, Parts of the body | Câu đố hành động; đi khám (GT) | Unit 12 nối với Unit 22 Illness |
| 13–14 Describing people, Character | Part 2 "Describe a person you know" | Dùng bạn thân Khoa, Lucy trong hồ sơ |
| 15–16 Relationships, Feelings | Part 1 "Friends"; cảm xúc | |

Phiên Review của module chưa có video. Nếu làm thì dùng cảnh `blanks` ôn từ của cả module, không đếm ngược.

## 6. Việc tiếp theo

1. Video Unit 8 trở đi theo mục 5 (checklist P2-59).
2. Có CD-ROM thì thêm audio phát âm từng từ (khai thư mục audio trong `files`, như sách có track).
3. Gặp thêm lỗi in trong Answer key thì ghi vào mục 3.3.
