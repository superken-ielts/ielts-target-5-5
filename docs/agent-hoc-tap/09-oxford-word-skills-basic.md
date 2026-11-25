# 09 — Oxford Word Skills Basic: từ vựng A1–A2 học song song, video 7–10 phút

Đợt 26, người học thêm cuốn *Oxford Word Skills Basic* vào repo (commit `cbfc72c`) và yêu cầu:
- rà cuốn sách;
- đưa vào menu tab Sách;
- học bằng video 7–10 phút, không đếm ngược;
- mỗi video có 1–2 phần luyện nói theo chủ đề từ vựng của unit.

Đợt 36, người học yêu cầu thêm mỗi chủ đề một video nghe – viết 10 phút chạy liền, gồm mọi từ của unit trong sách, thêm từ
và câu giao tiếp theo chủ đề (mục 5.9).

Đợt 37, người học: "tiếp tục làm video bài học unit 17-23 của oxford" — module Everyday life, mỗi unit hai video (bài giảng
mục 5.7, nghe – viết mục 5.9); không sửa video cũ.

Đợt 38, người học: "tạo các video của phần tiếp theo sách oxford xong rồi commit push main luôn" — module Food and drink
(Unit 24–28), mỗi unit hai video như đợt 37.

Đợt 39, người học: "tiếp tục module tiếp theo", rồi "xong rồi commit push lên main" — module Getting around (Unit 29–33), mỗi
unit hai video như đợt 37–38.

Đợt 40, người học: "tiếp tục module tiếp theo của oxford" — module Places (Unit 34–41), mỗi unit hai video như đợt 37–39.

| Thành phần | Ở đâu |
|---|---|
| Sách, hồ sơ lộ trình | `books/book_oxford_word_skills_basic/`: `Oxford_Word_Skills_Bas.pdf` (bản quét, 254 trang), `book.yaml` (mẫu `lessons-v1`), `book.json`, `plan.json`, `report.md`, `web/` (122 đoạn PDF, 83 MB) |
| Dữ liệu dò trang | `books/book_oxford_word_skills_basic/work/`: `scan.json`, `chunks.json`, `ocr-pages.json` (OCR dải đầu / chân trang), `ocr-answer-key.json` (unit nào ở trang Answer key nào) |
| Vị trí trong tab Sách | `books/catalog.json`: nhóm `ielts`, sau English Unlimited A2, trước IELTS Target 5.0 |
| Mẫu lộ trình | `agents/book_ingest/lessons.py`: tên bước dùng được `{title}`, `{no}`… như ghi chú (đợt 26, mục 4) |
| Video bài giảng | `books/book_oxford_word_skills_basic/lessons/` (kịch bản `.yaml`, `.mp4`, `lessons.json`); sổ tay ở mục 5; Unit 1–41 đã có (mục 5.7) |
| Video nghe – viết (đợt 36) | cùng thư mục, `<id>-dictation`; dữ liệu và bộ sinh kịch bản ở `work/dictation/`; Word list cuối sách ở `work/wordlist.json` (mục 5.9) |

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
| 17 | 3 (ABOUT YOU) | 8 câu trả lời mẫu ("a Japanese person"), có câu không ứng với câu hỏi nào (In the sitting room, About 8 hours) | Bài 2 chỉ có 6 câu hỏi: trả lời 6 câu (video nói rõ) |
| 22 | 1 | (đề in trùng) câu 10 giống hệt câu 8: *Is / Has she got a temperature?* | Đáp án cả hai câu là Has (video nói rõ) |
| 36 | 1 | 2 T (*The farmer's in the boat*) | F: trong tranh người nông dân đứng cạnh hàng rào, thuyền trống (video nói rõ — đợt 40) |
| Word list | — | like *as in* What's he/she/it like? 14, **23**, 62 · have got 10, 13, **21**, … · what's the matter? 16, **21** | Unit 21 (What's the weather like?), Unit 22, Unit 22 — có vẻ số unit của bản thảo cũ; `work/wordlist.json` xếp theo trang thật (mục 5.9) |

Gặp lỗi mới thì thêm vào bảng này. Video phải nói rõ chỗ in nhầm, vì người học chữa bài bằng Answer key.

## 4. Mẫu `lessons-v1`: tên bước có chỗ thay (đợt 26)

Trước đợt 26, mọi phiên của một bước có cùng tên, ví dụ "Unit 1 · từ vựng". Sách này có 80 unit, mỗi unit đúng một
bước, nên danh sách phiên không cho biết unit nào học gì.

Đợt 26, `lessons.py` thay chỗ trong **tên bước** như đã làm với ghi chú, dùng chung hàm `_fill`:
- `title: "{title} · từ vựng, bài tập, nói"` cho ra "Unit 1 · Numbers · từ vựng, bài tập, nói";
- chỗ thay sai (ví dụ `{bogus}`) báo `ProfileError` có ghi "tên bước".

Các sách cũ không dùng chỗ thay trong tên bước, nên `book.json` / `plan.json` của chúng không đổi (test hồi quy chạy
lại ra y hệt).

## 5. Video bài giảng — khuôn 7–10 phút (unit khó tới 15 phút)

### 5.1 Yêu cầu

- Mỗi unit một video **7–10 phút**, gắn vào phiên của unit đó.
- **Không đếm ngược:** không dùng `wait` / `echo`. Muốn người học trả lời thì Emma nói "Pause the video and try",
  "Pause the video after each sentence"…, rồi Tom (hoặc Emma) chữa ngay.
- **1–2 phần luyện nói** theo chủ đề từ vựng của unit:
  - Nói 1 (`qa`): Tom và Emma hỏi đáp qua lại;
  - Nói 2 (`practice` không có `wait`): người học tự tạm dừng và trả lời.
- **Unit khó** (đợt 29): video dài tới khoảng 15 phút. Sau phần sách thêm **ôn tập** và **luyện nói chung** theo chủ đề,
  vẫn trong cùng một video (mục 5.2, hàng 9–10). Unit khó là unit nhiều từ, từ trừu tượng, nhiều cặp dễ nhầm, hay chủ đề
  hay gặp ở IELTS Part 2. Module People có 4 unit khó: 10 My family, 13 Describing people, 14 Character, 16 Feelings;
  Everyday life có 3 (17, 19, 22 — đợt 37); Food and drink có 2 (26, 28 — đợt 38); Getting around có 2 (30, 32 — đợt 39);
  Places có 3 (35, 38, 39 — đợt 40).
  Đầu kịch bản ghi `# UNIT KHÓ (đợt …)`; test dùng dấu này để cho phép tới 15 phút.
- **Hình trong sách** (đợt 29, theo góp ý người học): tranh, bảng, đoạn văn của trang sách hiện ngay trong video, kèm
  khung đỏ chỉ đúng chỗ đang nói tới (mục 5.3a). Mọi unit đều có ít nhất một cảnh có hình (test kiểm): module People
  từ đợt 29, Unit 1–7 thêm ở đợt 30.

### 5.2 Bộ cảnh của một video

| # | Cảnh | Kiểu | Nội dung |
|---|---|---|---|
| 1 | Giới thiệu | `title` | Unit học gì; nhắc "no countdown, pause the video" |
| 2 | Từ vựng | `bullets` / `compare` | Từ của trang sách theo nhóm. Emma đọc, Tom đọc tiếp hoặc dùng từ trong câu. Thêm điểm phát âm (trọng âm, -teen / -ty), Anh – Mỹ, ngữ pháp đi kèm (Spotlight) |
| 3 | Bài tập trong sách | `blanks` (nhiều câu) hoặc `mcq` (≤ 6 câu) | Đề như sách. Emma: "Pause the video and try". Tom đọc đáp án theo Answer key, có lý do cho câu khó |
| 4 | Thêm ngoài sách (tùy unit) | `blanks` / `bullets` | Câu đố mô tả đồ vật, tự đặt câu hỏi, mẹo IELTS: đoán loại từ cần điền, xin nhắc lại câu hỏi, đánh vần tên |
| 5 | Nghe và viết | `blanks` | Emma đọc 6 câu, người học tạm dừng sau mỗi câu và viết từ còn thiếu. Tom chữa, đánh vần từ khó. Như IELTS Listening phần 1 |
| 6 | Nói 1 | `qa` | 7–10 cặp hỏi đáp về chủ đề: ABOUT YOU của sách (Emma dùng câu mẫu Answer key nếu có), chủ đề IELTS Part 1 gần nhất |
| 7 | Nói 2 · đến lượt bạn | `practice` (self-paced) | 5 câu hỏi có gợi ý. Emma đọc hết, `pause: 0.5`, câu cuối `pause: 1.0` (từ đợt 37; trước là 1.5 — mục 5.6) |
| 8 | Tổng kết | `bullets` | 4 điều cần nhớ, Test yourself của sách, unit tiếp theo |
| 9 | Ôn tập (unit khó) | `blanks` | Lỗi người Việt hay mắc (6 câu sửa lỗi) và một câu đố ôn từ (từ trái nghĩa, "ai là ai", đoán cảm xúc theo tình huống) |
| 10 | Luyện nói chung (unit khó) | `bullets` (thẻ đề) → `bullets` (ghi chú) → `letter` → `practice` → `qa` | Thẻ đề Part 2 theo chủ đề; ghi chú 1 phút của Tom; bài nói mẫu của Tom và của Emma (đổi vai giám khảo); người học tự nói theo bốn ý trên thẻ; 3 câu thảo luận kiểu Part 3 |

Hàng 9–10 nằm giữa hàng 7 và hàng 8 (tổng kết vẫn ở cuối). Hàng 2 và 3 dùng hình trong sách khi trang có tranh, bảng hay
đoạn văn (mục 5.3a).

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

### 5.3a Hình trong sách (đợt 29–30)

Người học góp ý nên đưa hình trong sách vào video. Công cụ dựng video (`lesson_video`) có:

| Cảnh | Cách hiện hình | Dùng cho |
|---|---|---|
| `figure` (mới) | Hình lớn cắt từ trang sách giữa khung; mỗi mục `items` có `box` (vùng trên hình) và `label` (nhãn, không bắt buộc). Dòng thoại `focus` vào mục nào thì vùng đó có khung đỏ | Tranh nhiều người / vật (sơ đồ gia đình, tranh động từ, tranh cảm xúc), bảng từ (bảng số Unit 1, bảng ngày – tháng Unit 3, bảng quốc tịch Unit 4, bảng câu hỏi Unit 7, phiếu mẫu Unit 9, bảng tính từ Unit 14) — khung theo từng dòng; câu có nhãn loại từ (Unit 6) — khung theo từ |
| `bullets` + `image` | Hình bên trái, danh sách từ bên phải; mục có `box` thì khung đỏ trên hình theo dòng đang học | Đồng hồ và bảng giờ trong ngày (Unit 2), ảnh bốn mùa (Unit 3), bản đồ Anh và Ireland (Unit 4), tranh lớp học (Unit 5), tranh mặt và cơ thể (Unit 12); đoạn văn (lời kể của Gemma, Sophie, Max) với danh sách từ trong Glossary; khung Spotlight |
| `blanks` câu điền từ + `image` | Hình bên trái, câu điền từ bên phải | Bài tập cần nhìn tranh (bản đồ châu Âu, Unit 4 bài 3) |
| `match` (đã có) | Hình bên trái, cột đáp án bên phải | Như các sách khác |

Cách khai:
```yaml
- kind: figure
  image: {pdf: course-book, page: 29, clip: [20, 68, 448, 296]}   # trang PDF, vùng cắt (điểm PDF)
  items:
    - {box: [24, 133, 192, 208], label: "father · mother = parents"} # cùng hệ toạ độ với clip
  lines:
    - {tom: "Dave is his father, and Maggie is his mother.", focus: 0}
```

- `page` là **trang PDF** (sách này: trang in + 1), `clip` và `box` tính bằng điểm PDF (trang 496 × 737).
- Lấy toạ độ: vẽ trang kèm lưới 25 điểm (đợt 29 dùng `grid.py` trong scratchpad: `pymupdf`, vạch đỏ theo x, xanh theo y,
  số mỗi 50 điểm), đọc vùng cần cắt, rồi xem trước khung hình (mục 5.4 bước 4).
- Khung theo dòng chữ (đoạn văn, hội thoại, Glossary — đợt 37): đo bằng máy thay vì đọc lưới. Dựng vùng bằng `pymupdf` ở 300
  dpi, thang xám; đếm điểm ảnh tối (< 110) trên mỗi hàng; mỗi dải hàng liền nhau là một dòng chữ, tâm dòng = giữa hai mép (đổi ra
  điểm PDF: y0 + hàng × 72 / 300). Khung một dòng lấy tâm ± 6 điểm; dòng sách cách nhau khoảng 12 điểm.
- Khung theo tranh (hàng tranh, đồ vật trên bàn ăn, đồ đựng — đợt 38): đo theo cả hai chiều. `blobs.py` trong scratchpad dựng
  vùng ở 200 dpi, thang xám, điểm ảnh "có mực" khi xám < 235. Nó in các dải ngang cách nhau ít nhất 3 điểm trắng, rồi trong mỗi
  dải là các đoạn theo x cách nhau ít nhất 4 điểm trắng. Mỗi đoạn là một tranh hay một nhãn; `box` lấy mép đo được, nới 2–4
  điểm. Dải thấp khoảng 10 điểm ngay dưới hàng tranh là dòng nhãn, không phải khoảng trống giữa hai hàng: `clip` phải gồm cả dải
  đó (mục 5.6).
- Đáp án hiện trên hình (đợt 39), dùng cho bài tự kiểm tra nhìn bản đồ hay tranh (Unit 29 bài 5, Unit 32 bài 3): mỗi câu hỏi
  hai mục `figure` cùng `box`. Mục thứ nhất không có `label`, dùng lúc Emma hỏi; mục thứ hai có `label` là đáp án (nhãn đỏ trên
  khung), dùng lúc Tom trả lời.
- `blanks` + `image` chỉ hợp với hình cao, hẹp: bản đồ nhỏ bài 3 Unit 31, danh sách a–j bài 1 Unit 33. Hình rộng như bản đồ
  tuyến xe buýt Unit 29 chỉ chiếm khoảng 40 % bề ngang khung hình, tên trạm cao khoảng 10 điểm ảnh ở 1080p, khó đọc; khi đó dùng
  cảnh `figure` riêng (mục 5.6).
- `box` không dùng với `grid` > 1. Hình chỉ dùng trong `match`, `figure`, `bullets`, `blanks` câu điền từ; khai sai thì
  `check` báo lỗi.
- Bảng đã ghi sẵn chữ thì bỏ `label`, để khung đỏ tự nói. Tranh không có chữ thì ghi `label` ngắn.
- Hình rộng mà thấp (hàng tranh, dải bảng) thì cắt thành nhiều cảnh nhỏ cho chữ đủ to: bảng tóc và mắt Unit 13 tách
  hai cảnh, 10 tranh cảm xúc Unit 16 tách ba cảnh. Trang có hai hình khác nhau thì mỗi hình một cảnh: Unit 3 tách bảng
  ngày – tháng (`figure`) và ảnh bốn mùa (`bullets` + `image`).
- Có hình bên trái thì danh sách chỉ còn khoảng nửa bề ngang: viết mục ngắn (`9 a.m. = in the morning`,
  `English = from England · British = from the UK`), không thì chữ bị thu nhỏ.

### 5.4 Quy trình một unit

1. Xem trang sách (`pdftoppm -f <trang PDF> -r 110`) và trang Answer key (độ phân giải cao hơn nếu chữ nhỏ). Ghi đáp
   án, đối chiếu nhãn câu hỏi với Answer key (mục 3.3).
2. Viết kịch bản theo mục 5.2–5.3a, rồi chạy:
   ```bash
   cd agents && python -m lesson_video check ../books/book_oxford_word_skills_basic/lessons/<id>.yaml
   ```
3. Soát cách đọc bằng `python -m lesson_video phonemes <kịch bản>` và sửa bằng `say` (mục 5.5).
4. Ước lượng thời lượng, rồi xem vài khung hình bằng bộ đọc im lặng (`tts.Silent()` + `Slides.render`, như
   `preview.py` trong đợt 26). Dưới 7:00 thì thêm cảnh; chữ tràn thì sửa. Từ đợt 38 dùng `scenepick.py` (scratchpad): mỗi
   cảnh có hình lấy ba khung hình (mục đầu, giữa, cuối được `focus`), ghép thành một tờ, để soát khung đỏ và mép cắt của cả
   video một lần.
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
| Hoa, Hạnh, Khoa | `Whah`, `Hahn`, `Kwah` | Tên người Việt (đợt 29: chị Hoa, mẹ Hạnh của Tom). `Hoa` đọc thành /hoʊə/, `Hwa` đọc từng chữ |
| Mr, Mrs, Ms; Mrs Green | `Mister`, `Missiz`, `Mizz`; `Missiz Green` | Danh xưng đứng riêng (Unit 9) đọc sai hoặc đọc từng chữ |
| CB2 4TX, N/A | `C B two, four T X`, `N A` | Mã bưu điện, chữ viết tắt trên form |
| Kovács, Zsuzsa | `Kovach`, `Zhoozha` | Tên Hungary trong bài 2 Unit 8 |
| Langbiang | `Lang Bee-ang` | Núi ở Đà Lạt (Unit 11) |
| live, lives (động từ) | `liv`, `livz` | Đọc /laɪv/ (⚠ của `phonemes`); "lived" đọc đúng, không cần `say` |
| used (động từ, quá khứ) | `yoozd` | Như `yooz` |
| phở bò, xôi gà, cơm tấm, bún chả | `fuh baw`, `Soy gah`, `Gum tum`, `Boon cha` | Món Việt (đợt 38): chữ có dấu bị đọc thành từng chữ cái |
| Vũng Tàu (viết Vung Tau), Ho Chi Minh City | `Voong Tau`, `Ho Chee Min City` | "Vung" đọc /vʌŋ/; Chi đọc /kaɪ/ (file 08). Bản nháp đợt 38 viết `Voong Tow` thì "Tow" thành /toʊ/ — đã sửa trước khi dựng |
| lychee | `lie-chee` | Kokoro đọc kiểu Mỹ /ˈliːtʃi/; sách dùng tiếng Anh – Anh |
| Nha Trang | `Nah Trang` | Đợt 39: "Nha" bị đọc thành từng chữ cái; `Nya` đọc /naɪə/ |
| Trại Mát, Phan Thiết, Mũi Né, Suối Tiên, Bến Thành | `Chai Mat`, `Fan Tee-et`, `Moo-ee Neh`, `Soo-ee Tee-en`, `Ben Tahn` | Địa danh Việt (đợt 39; `Ben Tahn` như Unit 19) |
| lối ra, giảm giá | `Loy rah`, `yahm yah` | Chữ Việt trên biển báo (Unit 33) |
| Cheltenham | `Cheltnum` | Kokoro đọc "Chel-ten-ham"; tiếng Anh – Anh đọc /ˈtʃeltnəm/ |
| số tuyến xe 16 (cuối câu, đứng riêng), 109 | `six-teen`, `one oh nine` | Như -teen ở trên; số tuyến đọc từng chữ số |
| km/h, mph (khi nói về chữ viết tắt) | `kay em aitch`, `em pee aitch` | M4, A46, M25 thì Kokoro đọc đúng, không cần `say` |
| Hội An, Hạ Long, Cần Thơ, Sa Pa, Huế | `Hoy Ann`, `Hah Long`, `Kahn Toh`, `Sah Pah`, `Whey` | Địa danh Việt (đợt 40; `Whey` như Giai đoạn 0) |
| Montpellier | `Mon-pel-yay` | Tên khu phố trong lời kể Unit 38 |
| DVD, DVD player | `dee vee dee` | Đọc từng chữ cái như CD; "TV" thì Kokoro đọc đúng |

Từ thường đúng, không cần `say`: Anki, Mandarin, Cantonese, Australasia, Portuguese, Egypt, comfortable, island,
Wednesday, umbrella, tomato (Kokoro đọc kiểu Mỹ; muốn kiểu Anh thì `tomahto`). Đợt 38 soát cả 184 mục Word list Unit 24–28
bằng bộ tách âm của Kokoro: đều đúng (chữ câm trong salmon, lamb; aubergine, croissant, dessert…), kể cả Wi-Fi và café — viết `why-fy`
thì Kokoro nhấn âm sau, nên đã bỏ. Đợt 40 thêm: Fansipan, Pico da Neblina, Brasilia, Recife, Stonehenge, bidet (chữ t câm),
washbasin, chest of drawers, toothpaste, saucer, hob, deli, newsagent's, chemist's — đều đúng. Thử một cách đọc mới trước
khi dựng (trong `agents/`):
`python -c "from lesson_video import phonemes; print(phonemes.tokenizer()('Voong Tau', 'en-us'))"`.

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
- **Câu điền từ hai chỗ trống chỉ hiện chỗ đầu** (đợt 29: Unit 11 bài 2, Unit 13 bài 5, Unit 14 bài 3, Unit 15 bài 2,
  Unit 16 bài 2): cảnh `blanks` chỉ vẽ một `___` mỗi câu. Tách thành mục `8a`, `8b`… (`reveal: ["8a", "8b"]`) hoặc viết lại
  câu thành một chỗ trống kèm gợi ý trong ngoặc. Tìm nhanh: `grep -n 'q: "[^"]*___[^"]*___' books/*/lessons/*.yaml`.
- **Chi tiết nhân vật mâu thuẫn với video cũ:** bản nháp Unit 15 viết Khoa học đại học ở Đà Lạt, trong khi
  `U01-speaking-practice-4` (IELTS) nói Khoa học y ở Hà Nội. Trước khi viết chi tiết mới về một người, `grep` tên người
  đó trong `books/*/lessons/*.yaml`.
- **Hình quá nhỏ:** bảng tóc – mắt (Unit 13) và 10 tranh cảm xúc (Unit 16) thu cả trang vào khung thì chữ khó đọc. Tách
  thành nhiều cảnh `figure`, mỗi cảnh một dải (mục 5.3a).
- **Sửa kịch bản khi video đang dựng:** bản dựng đọc kịch bản lúc bắt đầu, nên sửa sau đó thì video vẫn là bản cũ (Unit 14,
  câu về Khoa). Xếp dựng lại unit đó.
- **Chữ bên cạnh hình bị thu nhỏ** (đợt 30: Unit 2 "Buổi trong ngày", Unit 4 "Người của một nước"): mục dài như câu đầy đủ
  không vừa nửa khung còn lại nên bị thu nhỏ. Rút gọn mục (mục 5.3a).
- **Mép vùng cắt lộ nửa dòng chữ** của phần liền trên (đợt 30: bảng thứ hai Unit 7). Xem trước khung hình rồi nhích `clip`
  vài điểm.
- **Khung theo dòng lệch nửa dòng** (đợt 37: đoạn văn Unit 20, Spotlight too / very Unit 19): đọc lưới bằng mắt sai vài điểm,
  lần sửa thứ hai còn lệch ngược lại. Đo dòng bằng máy (mục 5.3a) thì khớp ngay. Ảnh thu nhỏ dễ đánh lừa: viền khung chạm chữ dòng
  bên cạnh vì dòng sát nhau — xem khung hình cỡ thật trước khi sửa.
- **Khoảng lặng cuối cảnh "Đến lượt bạn"** (đợt 37: Unit 17 dựng lần đầu): `pause` 1,5 giây ở câu cuối + `gap` 0,45 + `scene_gap`
  0,8 + đuôi lặng của giọng đọc = 2,96 giây, sát mức 3 giây người học cho phép. Từ đợt 37 câu cuối `pause: 1.0` (khoảng 2,5 giây),
  dựng lại Unit 17, 18; test kiểm video từ Unit 17.
- **Video ngắn hơn mức tối thiểu** (đợt 37): ước lượng đầu Unit 18 6:54, Unit 20 6:06, Unit 21 7:12, Unit 23 6:02; unit khó
  Unit 19 9:30, Unit 22 9:22 (phải trên 10 phút). Thêm cảnh ngoài sách có ích cho IELTS General Training (mặc gì khi…, nghe và
  viết giá tiền, câu hay dùng ở chợ, nhiệt độ và dự báo, đóng vai mua đồ, câu đố too / very, email xin nghỉ ốm, đọc nhãn thuốc),
  không kéo dài câu thoại.
- **Bỏ cảnh "Nghe và viết"** (mục 5.2 hàng 5) ở unit có nhiều bài trong sách (Unit 17, 19): unit đã có video nghe – viết riêng;
  ghi ở đầu kịch bản.
- **Mép cắt mất dòng nhãn hay tiêu đề** (đợt 38):
  - hàng trái cây Unit 25: dải nhãn cao khoảng 10 điểm bị tưởng là khoảng trống giữa hai hàng tranh;
  - tranh bàn ăn Unit 28: mất nhãn đồ vật;
  - tiêu đề hàng cá Unit 24, tiêu đề đồ đựng Unit 26, dòng đầu bài 3 Unit 24.

  Đo dải bằng `blobs.py` (mục 5.3a), rồi xem khung hình của mọi cảnh có hình trước khi dựng.
- **Hình quá nhỏ** (đợt 38):
  - thực đơn Unit 28 (hai cột chữ nhỏ và 8 tranh món) tách ba cảnh: món khai vị và món chính; tranh 1–4; tranh 5–8 và món
    tráng miệng;
  - Glossary và Spotlight another / some more tách hai cảnh.
- **Chữ hội thoại bên cạnh hình bị thu nhỏ** (đợt 38: hội thoại Unit 26, 27, 28): câu thoại đầy đủ như sách không vừa nửa khung.
  Rút gọn mục, ví dụ "I'd like a ham sandwich on brown bread …" (mục 5.3a).
- **Phiên làm việc khởi động lại giữa lúc dựng** (đợt 38, Unit 25): lệnh nền mất, video dở không vào `lessons.json`. Trước một
  hàng đợi dựng dài thì commit phần đã xong (kịch bản, video đã dựng). Bị ngắt thì xếp dựng lại; câu đã đọc lấy từ bộ nhớ đệm.
- **`say` tự đặt bị đọc sai** (đợt 38): `Voong Tow` (Vũng Tàu) cho "Tow" /toʊ/; `why-fy` nhấn âm sau, trong khi "Wi-Fi" vốn
  được đọc đúng. Thử từng cách đọc mới bằng bộ tách âm của Kokoro (mục 5.5) và sửa trước khi dựng. Unit 27 đã dựng nên phải dựng
  lại.
- **Dấu "…" trong đáp án nghe – viết** (đợt 38, Unit 28): đáp án "I'll have …" trông như chữ bị cắt khi soát thẻ
  (`trunc_check.py` báo), mà người học cũng không viết dấu đó. Đã bỏ dấu ba chấm ở `answer`.
- **Unit một trang ngắn** (đợt 38): Unit 24, 27 (và Unit 25) thêm cảnh ngoài sách có ích cho IELTS: tả một món ăn, câu đố con vật
  hay thịt, trái cây Việt Nam, câu đố vị, đồ uống quán Việt, câu hay dùng ở quán, câu đố tình huống.
- **Hình rộng cạnh bài tập quá nhỏ** (đợt 39, Unit 29 bài 2 và bài 5): bản đồ tuyến xe buýt đặt cạnh câu hỏi (`blanks` + `image`)
  chỉ chiếm khoảng 40 % bề ngang khung hình, tên trạm khó đọc. Bài 2 bỏ hình, ghi đủ câu hỏi; bài 5 thành cảnh `figure` với đáp án
  hiện trên hình (mục 5.3a).
- **Glossary cao, hẹp** (đợt 39, Unit 30 tr. 81): Glossary và Spotlight chung một cảnh thì chữ quá nhỏ — tách hai cảnh, như Unit 28.
- **Tranh lấn xuống bài tập** (đợt 39, Unit 32 tr. 84): `blobs.py` gộp tranh và danh sách tên thành một dải (y 91–389), nên
  đọc nhầm mép dưới của tranh; `clip` lấy thêm bài 1, tranh bị thu nhỏ. Đo lại riêng dải danh sách tên (y 354–389), rồi tách tranh
  thành nửa trên, nửa dưới; cảnh tự kiểm tra cắt bỏ danh sách tên.
- **Video ngắn hơn mức tối thiểu** (đợt 39): ước lượng đầu Unit 31 6:44, Unit 33 6:34; unit khó Unit 30 10:35, Unit 32 10:15 (sát
  10 phút). Thêm cảnh ngoài sách có ích cho IELTS: câu khi bị lạc, chỉ đường ở thành phố Việt Nam, câu đố tình huống (Unit 31);
  câu đố "Where would you see it?", thông báo thư viện và câu True / False (Unit 33); thông báo ở nhà ga (Unit 30); How far? /
  How long? (Unit 32).
- **`say` tự đặt đọc sai** (đợt 39): `Nya Trang` cho /naɪə/; thử bằng bộ tách âm thì `Nah Trang` gần nhất (mục 5.5).
- **Chi tiết nhân vật mâu thuẫn** (đợt 39, bản nháp Unit 31): "căn hộ của Tom ở trong hẻm" trái với Unit 29 (trạm xe buýt ngay
  trước hiệu thuốc dưới căn hộ) — đổi thành "nhiều bạn của Tom sống trong hẻm". Đầu kịch bản Unit 29–31 ghi vài chi tiết không có
  trong lời thoại — sửa đầu kịch bản cho khớp. Soát đầu kịch bản với lời thoại trước khi ghi mục 5.7.
- **Hàng đợi dựng bị ngắt** (đợt 40): máy chạy khởi động lại khi đang dựng Unit 37, mọi tiến trình dựng nền mất theo. Unit 35, 36
  đã xong được commit ngay làm mốc; Unit 37–39 xếp dựng lại. Hàng đợi dùng `flock` nên không theo thứ tự xếp: Unit 40 dựng trước
  Unit 38.
- **Sửa kịch bản khi lệnh dựng đã chạy** (đợt 40, Unit 40): lệnh dựng đọc kịch bản lúc bắt đầu. Bản nháp viết `ay` cho chữ cái A
  ("Write a, an or nothing", "Tick a or b") thì Kokoro đọc /aɪ/ — bảng mục 5.5 đã ghi phải viết `eigh`. Sửa lúc video đang dựng nên
  video vẫn đọc sai, phải dựng lại. So giờ sửa file với giờ "start" trong nhật ký dựng trước khi commit video.
- **Spotlight cắt nhầm cột** (đợt 40, Unit 36 tr. 95): `blobs.py` gộp Spotlight alone and lonely với khung ABOUT YOU bên cạnh, `clip`
  lấy sai cột. Xem hình kiểm tra (`scenepick.py`, đối số thứ ba là số thứ tự cảnh, không phải số thứ tự cảnh có hình) rồi đo lại
  riêng cột phải [342, 304, 488, 440].
- **Hình gần vuông thì nhỏ** (đợt 40, Unit 41): vùng hình của cảnh `figure` rộng 1160, cao 386 điểm ảnh (3 : 1), nên tranh phòng
  khách gần vuông chỉ rộng khoảng 450 điểm ảnh. Tách nửa trên, nửa dưới (mỗi nửa rộng khoảng 860 điểm ảnh, gấp đôi) cho phần giới
  thiệu 19 từ và bài tự kiểm tra; tranh cả phòng chỉ dùng cho bài 1 (đếm đồ vật) và cảnh giới từ. Tương tự: Glossary Unit 35 tách
  ba cảnh, Glossary Unit 34 bỏ la bàn.
- **Ước lượng ngắn** (đợt 40): Unit 34 ước 7:14, Unit 41 6:23 (unit một trang); unit khó Unit 38 10:12, Unit 39 9:34. Thêm cảnh
  ngoài sách: famous for / popular with, câu đố vị trí về Việt Nam (Unit 34); giới từ tả vị trí trên tranh sách, bài nói mẫu tả
  phòng khách (Unit 41); thuê nhà, tự kiểm tra tranh tòa nhà (Unit 38); do hay make, bếp Việt Nam (Unit 39).
- **Phần "từ thêm" của video nghe – viết** (đợt 40, Unit 35): Word list 54 mục nên bản nháp chỉ còn 8 từ thêm để video không quá
  11 phút; test cần ít nhất 10. Ghép dòng các mục đi cùng nhau ở phần 1 (north, south, east, west; over, under…), thêm 2 từ, bớt
  6 câu giao tiếp.
- **Câu có hai chỗ trống** (đợt 40): cảnh `blanks` chỉ điền `answer` vào `___` đầu tiên. Unit 36 bài 2 câu 4 viết
  `f___ds … → ___` nên đáp án nằm giữa từ ("f fields ds") còn chỗ trống sau mũi tên để nguyên; Unit 39 bài 1 câu 1, 7
  (`w___ m___`) và câu đố do / make (`___ the washing-up → ___`) còn thừa một chỗ trống. Mỗi câu chỉ một `___`: chữ cái bị
  thiếu trong từ viết `_ _ _` (cách nhau) hoặc `__`; chữ gợi ý của cụm hai từ đưa vào `hint` (`w… m…`). Đã dựng lại Unit 36, 39.
  Unit 27 bài 1 câu 5 (`eat here or ___ ___`, đợt 38) cũng vậy — video cũ, không sửa. Soát trước khi dựng:
  `grep -n 'q: "[^"]*___[^"]*___' lessons/*.yaml`.
- **Nhãn số dài dính vào câu** (đợt 40, Unit 39): nhãn "10a." của cảnh `blanks` dính vào chữ đầu câu ("10a.Heat"). `slides.py`
  (`text_col`) cho cột câu lùi theo nhãn dài nhất của cảnh; nhãn một – hai ký tự ("12.", "2a.") giữ vị trí cũ.
- **Nghe – viết dài hơn ước lượng tới 9 %** (đợt 40): Unit 34 ước 9:15, dựng thật 10:05 (các đợt trước 5–6 %). Unit 35 ước 10:02
  thì có thể chạm 11 phút — bớt câu trước khi dựng, còn ước 9:38. Nhắm ước lượng 9:10–9:40.

### 5.7 Độ phủ video và chi tiết nhân vật

Module Basic English đủ 7/7 unit, tổng 51:11 (đợt 26, thêm hình ở đợt 30). Module People đủ 9/9 unit, tổng 1:22:54
(đợt 29). Module Everyday life đủ 7/7 unit, tổng 1:07:37 (đợt 37). Module Food and drink đủ 5/5 unit, tổng
48:22 (đợt 38). Module Getting around đủ 5/5 unit, tổng 48:26 (đợt 39). Module Places đủ 8/8 unit, tổng 1:17:38 (đợt 40). Cả sách: 41 video bài giảng, 6:16:09, 211 cảnh có hình. Cột "Hình" là số cảnh có hình trong sách (mục 5.3a).

| Unit | Video | Dài | Chương | Hình | Bài trong sách | Nói 1 (Tom ↔ Emma) | Nói 2 (đến lượt bạn) | Thêm ngoài sách |
|---|---|---|---|---|---|---|---|---|
| 1 Numbers | `U01-numbers` | 7:26 | 12 | 2 | 1–3 | Những con số quanh bạn (8 cặp) | 5 câu | -teen / -ty, số lớn, số trong đời sống (điện thoại, giá, %) |
| 2 The time | `U02-time` | 7:14 | 11 | 2 | 1, 2, 4, Test yourself | Giờ giấc ở nước bạn (10) | 5 câu | buổi trong ngày, nearly / just after |
| 3 Days and dates | `U03-days-dates` | 7:14 | 12 | 2 | 2, 5, 6, 7 | Về bạn và đất nước bạn (9: Tết, 30/4, 2/9, sinh nhật) | 5 câu | đọc và viết ngày tháng kiểu Anh / Mỹ |
| 4 Countries and nationalities | `U04-countries` | 7:43 | 14 | 4 | 1–4 | Quê hương và ngôn ngữ (8) | 5 câu | the British / Italians, Britain và the UK, trọng âm -ese / -ian |
| 5 Classroom vocabulary | `U05-classroom` | 7:10 | 13 | 2 | 1–3 | IELTS Part 1 "Bags", "Pens and writing" (9) | 5 câu | a piece of paper, I've got, borrow / lend, đoán đồ vật "It's a thing you use to…" |
| 6 English language words | `U06-language-words` | 7:18 | 13 | 2 | 1, 2 (sửa lỗi Answer key) | Học ngữ pháp và từ (7) | 5 câu | động từ có quy tắc / bất quy tắc, chữ viết tắt trong từ điển, mẹo IELTS đoán loại từ cần điền |
| 7 Questions about language | `U07-questions-language` | 7:07 | 12 | 2 | 1, 2 | Hỏi về từ ngữ (8: exhausted, cà phê sữa đá, phở…) | 5 câu | I don't know / can't remember / not sure, tự đặt câu hỏi, chữ cái dễ nhầm, đánh vần tên |

Module People (đợt 29) — **unit khó** in đậm, video dài hơn vì có ôn tập và luyện nói chung (mục 5.1):

| Unit | Video | Dài | Chương | Hình | Bài trong sách | Nói 1 (Tom ↔ Emma) | Luyện nói chung / Nói 2 | Thêm ngoài sách |
|---|---|---|---|---|---|---|---|---|
| 8 Personal information | `U08-personal-info` | 7:15 | 12 | 2 | 1–3 | Thông tin về bạn (9) | đến lượt bạn (5 câu) | hội thoại lễ tân và Spotlight trong sách; What do you do? ≠ What are you doing?; đặt câu hỏi từ câu trả lời; mở đầu bài thi Nói IELTS |
| 9 Filling in a form | `U09-form` | 7:39 | 12 | 3 | 1, 2 (nói), Test yourself | Form và tên người Việt (10) | điền form thành tiếng (5) | phiếu mẫu trong sách (3 dải); chỉ dẫn trên form; ngày sinh kiểu Anh / Mỹ; nghe và điền form như Listening phần 1; mẹo IELTS điền form |
| **10 My family** | `U10-family` | 11:57 | 18 | 1 | 1, 2, 5, 6 | Gia đình (9) | Part 2 "a family member you spend a lot of time with" (Tom: chị Hoa, Emma: anh Jack); thảo luận (4) | sơ đồ gia đình Damon; một từ tiếng Anh ứng với nhiều cách gọi tiếng Việt; ôn tập: lỗi hay gặp, "ai là ai" |
| 11 Physical actions | `U11-actions` | 8:12 | 14 | 3 | 1, 2, 4, 5 | Đi bộ, đạp xe, leo núi, nhảy (11) | đến lượt bạn (5) | 24 tranh động từ trong sách; làm theo Emma; luyện nhanh quá khứ bất quy tắc; chuyện thứ Bảy của Tom |
| 12 Parts of the body | `U12-body` | 7:10 | 16 | 2 | 1–3 | Cơ thể và sức khỏe (9) | đến lượt bạn (5) | tranh mặt, miệng, cơ thể bên trái danh sách từ; chữ câm; my + bộ phận cơ thể; câu đố; cử chỉ; đi khám (headache, sore throat) |
| **13 Describing people** | `U13-describing-people` | 11:47 | 20 | 7 | 1, 2, 4, 5, 7, 10, 11 | Trông bạn thế nào? (9) | Part 2 "someone in your family who looks like you" (Tom và Emma: mẹ); thảo luận (3) | tranh chiều cao – cân nặng, bảng tóc – mắt, bảng tuổi, tranh X / Y; thứ tự tính từ tả tóc; dark brown eyes ≠ a black eye; ôn tập: lỗi hay gặp, "ai đây?" |
| **14 Character** | `U14-character` | 11:20 | 18 | 5 | 1–5 | Bạn là người thế nào? (9) | Part 2 "a person you know who is very kind" (Tom: ông, Emma: bà); thảo luận (3) | bảng tính từ, đoạn văn của Gemma, hai khung Spotlight; What's he like? ≠ What does he look like?; ôn tập: lỗi hay gặp, từ trái nghĩa |
| 15 Relationships | `U15-relationships` | 7:24 | 13 | 4 | 1–3, 4 (nói) | Bạn thân (9, kèm câu mẫu người Hungary) | đến lượt bạn (5) | lời kể về Max và của Sophie, hai khung Spotlight; Test yourself thành câu đố; advice không đếm được |
| **16 Feelings** | `U16-feelings` | 10:10 | 16 | 5 | 1, 2, 4, 5 | Cảm xúc của bạn (9) | Part 2 "a time when you felt very nervous" (Tom: ngày đầu đi làm thêm, Emma: buổi dạy đầu tiên ở Việt Nam); thảo luận (3) | bảng cảm giác cơ thể, 10 tranh cảm xúc, Spotlight "get + adjective"; ôn tập: lỗi (bored / boring, frightened of), đoán cảm xúc theo tình huống |

Chi tiết nhân vật mới trong các video này đều khớp file 06 mục 9.4.

Module Basic English (đợt 26):
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

Module People (đợt 29) — gia đình, ngoại hình, tính cách lần đầu được nói rõ:
- **Tom** (Trần Minh Tuấn):
  - 20 tuổi, sinh 9/3/2006, độc thân; tên tiếng Anh Tom vì ngắn và cùng chữ T với Tuấn; trên form: Surname TRAN,
    Forenames MINH TUAN; lần đầu điền form visa viết nhầm tên vào ô họ;
  - nhà 6 người: ông 78 tuổi (thầy Toán về hưu, làm vườn rau mỗi sáng, kiên nhẫn, trời mưa đau đầu gối); bố mẹ cưới năm
    1998; mẹ tên Hạnh, 50 tuổi, thấp (1m55), tóc đen ngắn hơi gợn sóng; chị Hoa 26 tuổi, y tá ở Hà Nội, gọi điện gần như
    mỗi tối, khuyên chuyện gia đình; em Bao 15 tuổi, mê bóng đá;
  - khoảng 1m75, tóc đen ngắn thẳng, mắt nâu sẫm, sáng nào cũng cạo râu; giống mẹ (mắt, nụ cười), chị Hoa cũng vậy; các dì
    bảo Tom gầy quá;
  - hơi trầm khi mới gặp, thân thiện khi đã quen, chăm chỉ, biết lắng nghe; bàn học gọn nhưng phòng bừa;
  - gãy cổ tay năm 12 tuổi (ngã xe đạp trên dốc ở Đà Lạt); ngồi laptop lâu thì đau lưng, đau cổ; trước kỳ thi không ăn
    sáng được, năm ngoái đau bụng vì căng thẳng; lo lắng thì gọi Khoa hoặc chị Hoa;
  - bóng rổ hai buổi một tuần; đã leo núi Langbiang; xe buýt đông thì đứng suốt; học từ mới thì đi quanh phòng đọc to;
  - ngày đầu làm thêm ở quán cà phê (tháng 9, khớp hồ sơ) làm rơi khay cà phê sữa đá, vỡ hai ly; tuần trước lại làm rơi
    khay đồ uống;
  - Khoa (khớp `U01-speaking-practice-4`): học y ở Hà Nội; cao trung bình, tóc đen ngắn, đeo kính, lúc nào cũng cười;
    vui tính, tốt bụng, chăm chỉ; quen 14 năm, ngồi cùng bàn từ lớp 1; gặp dịp Tết, nhắn tin gần như mỗi ngày; có chuyện
    là Tom gọi Khoa đầu tiên.
- **Emma** (Emma Louise Clarke):
  - 28 tuổi, sinh 15/9/1998, độc thân (bà hỏi chuyện này mỗi Giáng sinh); quê miền nam nước Anh; dùng Ms trên form;
  - nhà 4 người: bố mẹ 62 tuổi, sang năm nghỉ hưu, quen nhau ở đám cưới một người bạn năm 27 tuổi, bên nhau 35 năm; mẹ đeo
    kính, tóc nay đã bạc; anh Jack 30 tuổi, giống bố (cao, tóc sẫm, có râu), nhắn tin gần như mỗi ngày, gọi video hai tuần
    một lần; bà sống gần bố mẹ Emma, đan áo cho cả nhà, gửi thư sang Việt Nam;
  - cao trung bình (1m65), mảnh mai, tóc dài gợn sóng nâu sáng, mắt xanh, giống mẹ;
  - hòa đồng, khá thoải mái, ở nhà không gọn gàng; hồi thiếu niên rất nhút nhát, đi dạy giúp tự tin hơn;
  - gọi video cho mẹ mỗi Chủ nhật, nhớ nhà nhất dịp Giáng sinh; sợ nhện, hơi sợ giao thông, không đi xe máy ở TP. HCM (đi
    bộ hoặc gọi xe ôm qua ứng dụng); nhảy dở; năm 12 tuổi làm vỡ guitar của Jack; tháng trước trượt ngã trên đường ướt;
  - giận người đến muộn mà không nhắn, và xe máy chạy trên vỉa hè; sinh nhật năm ngoái học viên làm bánh có tên Emma bằng
    tiếng Việt; buổi dạy đầu tiên ở Việt Nam (lớp 20 người lớn) chào "Chào buổi sáng" sai thanh;
  - Lucy: hàng xóm, quen từ năm 5 tuổi, nay sống ở Bristol, gọi video mỗi tháng; cao, mảnh mai, tóc đỏ ngắn xoăn; rất hòa
    đồng, rất ngăn nắp.

Module Everyday life (đợt 37) — **unit khó** in đậm; mọi unit đủ bài tập trong sách (Answer key in lệch ở mục 3.3):

| Unit | Video | Dài | Chương | Hình | Bài trong sách | Nói 1 (Tom ↔ Emma) | Luyện nói chung / Nói 2 | Thêm ngoài sách |
|---|---|---|---|---|---|---|---|---|
| **17 My routine** | `U17-routine` | 13:22 | 20 | 6 | 1–9 (bài 3: Answer key in lệch) | Cuối tuần, thói quen (8) | Part 2 "your favourite day of the week" (Tom: thứ Bảy, Emma: Chủ nhật); thảo luận (3) | 10 tranh việc trong ngày, đoạn văn cuối tuần, bảng tìm cụm từ, thang tần suất; ôn tập: lỗi hay gặp |
| 18 Clothes | `U18-clothes` | 8:06 | 16 | 6 | 1–8 | Bài 7: bạn mặc gì (7) | Part 1 "Clothes" (5 câu) | tranh 12 món quần áo, bảng màu, tranh phụ kiện; wear / put on; mặc gì khi…; Nghe và viết |
| **19 Buying clothes** | `U19-buying-clothes` | 10:58 | 22 | 7 | 1–9 | Bài 9: mua sắm (6) | đóng vai mua đồ; Part 2 "the last time you bought some clothes" (Tom: sơ mi đen, Emma: giày đi bộ); thảo luận (3) | 12 tranh tả quần áo, bảng cỡ, too / very, hội thoại cửa hàng; câu hỏi thêm khi mua đồ; ôn tập: lỗi, too hay very |
| 20 Money | `U20-money` | 8:15 | 16 | 4 | 1–6 | Bài 6: tiền ở Việt Nam và ở Anh (7) | Part 1 "Money and shopping" (5 câu) | 7 tranh tiền, đoạn văn mua CD, Spotlight đọc giá, 7 quảng cáo; đọc giá đồng; nghe và viết giá; câu ở chợ; Nghe và viết |
| 21 The weather | `U21-weather` | 8:03 | 16 | 5 | 1–6 | Thời tiết quê bạn (7) | Part 1 "Weather and seasons" (5 câu) | bảng thời tiết, Spotlight a lot / a bit, ảnh bão, đoạn văn; nhiệt độ và dự báo; bài 6 về miền Nam; Nghe và viết |
| **22 Illness** | `U22-illness` | 11:06 | 18 | 4 | 1–5 (bài 1: câu 10 trùng câu 8) | Sức khỏe (6) | Part 2 "a time when you were ill" (Tom: cúm, Emma: ho mùa mưa); thảo luận (3) | 11 tranh triệu chứng, tranh lời khuyên, Glossary; Nghe và viết; ôn tập: lỗi, câu đố should; email xin nghỉ ốm |
| 23 At the chemist's | `U23-chemists` | 7:48 | 15 | 5 | 1–3 (bài 3 thành câu đố tranh) | Hiệu thuốc, tủ thuốc (5) | đóng vai ở hiệu thuốc (5 câu) | 7 tranh, hai hội thoại, Glossary và Spotlight; cần mua gì; đọc nhãn thuốc; hội thoại đau họng; Nghe và viết |

Module Everyday life (đợt 37) — sinh hoạt, mua sắm, tiền, thời tiết, sức khỏe:
- **Tom:**
  - dậy khoảng 6:30 ngày thường (U02), Chủ nhật sau 9 giờ; ăn sáng rồi mới thay đồ; đi bộ 15 phút đến trường, lớp đầu 7:30;
    ăn tối với hai bạn cùng phòng (chia nhau nấu), thứ Ba và thứ Năm ăn ở quán; ngủ khoảng 11:30, khoảng bảy tiếng; sáng thứ
    Bảy đi chợ với bạn cùng phòng, chiều chơi bóng rổ, tối xem phim khoa học viễn tưởng; Chủ nhật gọi bố mẹ ở Đà Lạt, ôn IELTS;
  - áo phông, quần bò, giày thể thao ("đồng phục sinh viên"); không đeo kính, kính râm mùa khô; luôn đeo đồng hồ (quà của
    bố); ở quán mặc sơ mi đen — mua ở chợ Bến Thành tháng 9, cỡ M, 150.000 đồng (cỡ L quá rộng); thích mua trực tuyến nhưng
    quần áo phải thử; ghi danh sách, không mua thứ không cần;
  - khoảng 700.000 đồng một tuần cho ăn uống; cước điện thoại khoảng 100.000 đồng một tháng; về Đà Lạt bằng xe khách (khoảng
    300.000 đồng, bảy tiếng); để dành tiền đi trao đổi ở Úc;
  - Đà Lạt mát quanh năm (15–25 độ), sáng sương mù, tháng 12 tối lạnh; thích tiếng mưa, ghét đi xe máy dưới mưa to;
  - cúm tháng 12 năm ngoái trước kỳ thi (sốt 39 độ, nằm ba ngày, bạn cùng phòng nấu cháo, chị Hoa dặn uống nhiều nước); email
    xin nghỉ gửi quản lý quán, Ms Linh; tuần trước đứt tay khi thái rau (đang học nấu ăn); hiệu thuốc ngay dưới căn hộ; tủ
    thuốc có băng dán, kem sát trùng, thuốc đau đầu.
- **Emma:**
  - dậy 6 giờ, học tiếng Việt nửa tiếng trước bữa sáng (U02); đi làm bằng xe ôm công nghệ (khoảng 20 phút); dạy khoảng 25
    giờ một tuần, thường xong 6 giờ chiều; học tiếng Việt tối thứ Hai và thứ Tư; ngủ khoảng 10:30; sáng thứ Bảy đi chợ rồi nấu
    món mới; Chủ nhật đi dạo, đọc truyện trinh thám, gọi cho mẹ;
  - chân váy dài, áo màu kem, xăng-đan; giày thể thao khi đi bộ đường dài; đội mũ mỗi ngày; hầu như không đeo đồng hồ; thích
    màu xanh lá; mua quần áo khoảng ba lần một năm, thường ở chợ; tháng trước mua giày đi bộ đường dài (cỡ 39, khoảng hai triệu
    đồng, thẻ ghi nợ) — ở Việt Nam khó tìm cỡ giày của Emma;
  - ở Anh vé tàu rất đắt, nước máy ở nhà hàng miễn phí; thích trà đá miễn phí ở quán nhỏ; quê ven biển lúc nào cũng có gió nhẹ,
    thời tiết hay đổi; thích ngày xuân nắng mà không nóng, thấy TP. HCM quá ẩm; ngày mưa ở nhà đọc sách, mùa mưa luôn có ô;
  - mùa mưa đầu tiên ở Việt Nam bị cảm và ho hai tuần, dược sĩ gần nhà giúp, từ đó luôn có trà gừng; ít uống thuốc; ở Anh khám
    GP, ở Việt Nam ra hiệu thuốc trước.

Module Food and drink (đợt 38) — **unit khó** in đậm; mọi unit đủ bài tập trong sách:

| Unit | Video | Dài | Chương | Hình | Bài trong sách | Nói 1 (Tom ↔ Emma) | Luyện nói chung / Nói 2 | Thêm ngoài sách |
|---|---|---|---|---|---|---|---|---|
| 24 Meat and fish | `U24-meat-fish` | 8:03 | 16 | 4 | 1–5 (bài 4 thành Nói 1) | Bài 4: Do you like …? (7) | Part 1 "Food" (5 câu) | bảng animal → meat, Spotlight pig, tranh cá và hải sản, tranh bài 3; a chicken / some chicken; câu đố con vật hay thịt; món Việt bằng tiếng Anh; tả một món ăn (Tom: phở bò); I don't eat meat; Nghe và viết |
| 25 Fruit and vegetables | `U25-fruit-vegetables` | 8:14 | 17 | 9 | 1–7 | Rau quả ở Đà Lạt, đi chợ (5) | Part 1 "Fruit" (5 câu) | hai hàng tranh trái cây, bảng vị, bốn hàng tranh rau, raw / frozen / cooked, Spotlight salad; sour ≠ bitter; trái cây Việt Nam; câu đố vị; Nghe và viết |
| **26 Buying food** | `U26-buying-food` | 11:35 | 21 | 9 | 1–8 | Đi chợ mua thực phẩm (5) | đóng vai ở chợ; Part 2 "a shop or market where you often buy food" (Tom: chợ nhỏ gần căn hộ, Emma: cửa hàng đồ nhập khẩu gần trường); thảo luận (3) | ba hàng tranh thực phẩm, đồ đựng và số lượng, Spotlight tin / can, hai hội thoại, Glossary, Spotlight how much / how many; ôn tập: lỗi hay gặp |
| 27 In a café | `U27-cafe` | 8:01 | 17 | 3 | 1–4 (bài 4 thành nghe tiếng Việt, nói tiếng Anh) | Cà phê, trà, quán (4) | Part 1 "Coffee and tea" (5 câu) | 12 tranh đồ uống và đồ ăn, hội thoại, Glossary và Spotlight; đồ uống quán Việt; cỡ ly và yêu cầu riêng; câu hay dùng ở quán; câu đố tình huống; đóng vai gọi đồ (Tom là phục vụ); Nghe và viết |
| **28 In a restaurant** | `U28-restaurant` | 12:30 | 22 | 10 | 1–9 (bài 3, 7: tự kiểm tra ở phần ôn tập) | Bài 6: chọn món (5) | đóng vai gọi món (Emma là phục vụ); Part 2 "a restaurant that you enjoyed going to" (Tom: lẩu bò ở Đà Lạt dịp Tết, Emma: hải sản ở Vũng Tàu); thảo luận (3) | tranh bàn ăn 12 đồ vật, cách nấu và thang steak, thực đơn (ba cảnh), hai hội thoại, Glossary, Spotlight another / some more; đặt bàn qua điện thoại; ôn tập: tự kiểm tra bàn ăn, lỗi hay gặp |

Module Food and drink (đợt 38) — món ăn, đi chợ, quán cà phê, nhà hàng:
- **Tom:**
  - thích thịt bò (bữa sáng yêu thích là phở bò), thích tôm, không thích mực; Đà Lạt trên núi, xa biển, nên hồi nhỏ ít ăn hải
    sản; mẹ nấu canh cá ngon nhất;
  - thích xoài và sinh tố bơ (bơ ở Đà Lạt rẻ); không thích mướp đắng, dù mẹ bảo tốt cho sức khỏe; ông trồng bắp cải, cà rốt, xà
    lách trong vườn;
  - sáng thứ Bảy đi chợ gần căn hộ với hai bạn cùng phòng (gạo, trứng, rau, thịt lợn, mì), mua bánh mì ở tiệm đầu ngõ; về Đà Lạt
    thì đi chợ với mẹ;
  - ở quán cà phê: món khách gọi nhiều nhất là cà phê sữa đá, cũng là món Tom thích nhất (ít đường); tối nào cũng có khách hỏi
    mật khẩu wifi;
  - mới ăn bít tết một lần, thích chín vừa; Tết năm nay cả nhà (ông, bố mẹ, chị Hoa từ Hà Nội về, em Bao) đi ăn lẩu bò ở một quán
    gần chợ Đà Lạt.
- **Emma:**
  - lớn lên ở thị trấn ven biển nên thích hải sản, nhất là cua và vẹm, và fish and chips; không thích vịt; cuối tuần thỉnh thoảng
    ăn sáng kiểu Anh (bacon, xúc xích);
  - thích dâu tây với kem (mùa hè ở Anh); đã thử sầu riêng một lần, không thích;
  - mua phô mai và bơ ở một cửa hàng nhỏ bán đồ nhập khẩu vì chợ không có; nhớ bánh mì kiểu Anh;
  - sáng uống cappuccino, chiều uống trà sữa kiểu Anh; đã thử cà phê trứng ở Hà Nội và rất thích; chiều thứ Bảy chấm bài ở một quán
    cà phê gần trường (yên hơn căn hộ);
  - hè năm ngoái đi Vũng Tàu với ba giáo viên cùng trường, ăn ở một quán hải sản cạnh biển — gợi nhớ quê.

Module Getting around (đợt 39) — **unit khó** in đậm; mọi unit đủ bài tập trong sách:

| Unit | Video | Dài | Chương | Hình | Bài trong sách | Nói 1 (Tom ↔ Emma) | Luyện nói chung / Nói 2 | Thêm ngoài sách |
|---|---|---|---|---|---|---|---|---|
| 29 Buses | `U29-buses` | 8:25 | 14 | 4 | 1–5 (bài 5: câu hỏi mới về bản đồ, đáp án hiện trên hình) | Bài 4: xe buýt gần nhà (6) | Part 1 "Public transport" (5 câu) | bản đồ tuyến 24 / 16, bảng hỏi – đáp, Glossary (near / outside) và Spotlight How long does it take?; đi lại ở Việt Nam (xe khách, xe giường nằm, xe ôm qua ứng dụng); Nghe và viết |
| **30 Trains** | `U30-trains` | 11:32 | 20 | 6 | 1–5 (bài 4: bảng giờ tàu hiện riêng) | Bài 5: chuyến tàu gần đây (5) | đóng vai mua vé; Part 2 "a journey that you remember" (Tom: tàu Đà Lạt – Trại Mát với ông, Emma: tàu ra Phan Thiết); thảo luận (3) | tranh ga tàu, hai Glossary, Spotlight last / book in advance, hội thoại mua vé; đường sắt Việt Nam, thông báo ở nhà ga; ôn tập: lỗi hay gặp |
| 31 Directions | `U31-directions` | 8:37 | 19 | 7 | 1–4 (bài 3: ba hội thoại, bản đồ nhỏ của sách) | Chỉ đường quanh nhà, trường (4) | đóng vai chỉ đường cho khách du lịch (5 câu) | câu hỏi đường, năm sơ đồ chỉ đường; giới từ chỉ vị trí (bài bản đồ IELTS Listening); câu khi bị lạc; chỉ đường ở thành phố Việt Nam; câu đố tình huống; Nghe và viết |
| **32 Roads and traffic** | `U32-roads-traffic` | 11:30 | 19 | 6 | 1–6 (bài 3: tự kiểm tra tranh ở phần ôn tập) | Bài 6: đường sá ở Việt Nam và ở Anh (5) | Part 2 "a place in your city where there is often a lot of traffic" (Tom: vòng xoay gần trường, Emma: đường trước trường); thảo luận (3) | tranh khu phố 12 mục (hai cảnh), hội thoại Beth – Marco, Glossary hai cảnh; giao thông ở Việt Nam; How far? / How long?; ôn tập: lỗi hay gặp, tự kiểm tra tranh |
| 33 Signs and notices | `U33-signs-notices` | 8:23 | 17 | 4 | 1–3 (bài 1: danh sách a–j của sách) | Biển báo quanh bạn (4) | biển báo trong đời sống (5 câu) | bảng 14 biển báo (ba cảnh); thêm biển báo; biển tiếng Việt → tiếng Anh; Where would you see it?; thông báo kiểu IELTS GT Reading, câu True / False; Nghe và viết |

Module Getting around (đợt 39) — xe buýt, tàu hỏa, chỉ đường, giao thông, biển báo:
- **Tom:**
  - trạm xe buýt ngay trước hiệu thuốc dưới căn hộ, tuyến 19 và 33, khoảng 15 phút một chuyến (xem giờ trên ứng dụng); về Đà Lạt
    thường đi xe khách đêm, ngủ suốt đường; trước Tết luôn đặt vé xe trước;
  - Đà Lạt không có tàu đi TP. HCM, chỉ có ga cổ và tàu du lịch đi Trại Mát; năm 10 tuổi đi tàu đó với ông (ghế gỗ, khoảng 30
    phút, ông mua cho một túi dâu tây); hè năm ngoái đi tàu ra Nha Trang với hai bạn cùng phòng (vé ngồi khoảng 300.000 đồng, đi
    thẳng khoảng tám tiếng);
  - từ căn hộ ra chợ: ra khỏi tòa nhà rẽ trái, rồi rẽ phải ở ngã rẽ đầu tiên, chợ sau trường đại học; ít hỏi đường, dùng bản đồ
    trên điện thoại; ở Đà Lạt khách du lịch hay hỏi Tom đường ra chợ; nhiều bạn sống trong hẻm;
  - thỉnh thoảng đi xe máy, ghét đi dưới mưa to; vòng xoay lớn gần trường đại học hay kẹt xe (5–7 giờ tối, khi mưa) — Tom đi sớm;
  - cửa bếp ở quán cà phê có biển Staff only; hồi nhỏ giẫm lên cỏ trong công viên ở Đà Lạt và bị nhắc "keep off the grass".
- **Emma:**
  - nhà bố mẹ ở Anh có trạm xe buýt cuối đường, đi vào trung tâm thị trấn bốn trạm, 5–10 phút; ở TP. HCM đi xe ôm công nghệ;
  - luôn đặt vé tàu trước vì được giảm giá; tháng Tư năm nay đi tàu một mình ra Phan Thiết (đặt qua ứng dụng, khoảng bốn tiếng),
    ngồi cạnh một gia đình Việt, tập nói tiếng Việt với bọn trẻ, đi qua nhiều trang trại thanh long; thích tuyến metro mới (nhanh,
    sạch);
  - quán cà phê gần trường ở góc đường, đối diện ngân hàng; luôn xem bản đồ trên điện thoại, thấy hẻm nhỏ ở TP. HCM dễ lẫn;
  - không đi xe máy, hơi sợ giao thông nên luôn qua đường ở vạch kẻ; đường trước trường đông vào giờ đưa đón học sinh và giờ cao
    điểm, giận xe máy chạy trên vỉa hè; cho rằng thành phố cần thêm xe buýt, metro;
  - biển tiếng Việt học đầu tiên: "lối ra", "giảm giá"; ngân hàng, bưu điện có biển xếp hàng; trường có biển nhắc tắt điện thoại
    trong lớp.

Module Places (đợt 40) — **unit khó** in đậm; mọi unit đủ bài tập trong sách (Answer key in lệch ở mục 3.3):

| Unit | Video | Dài | Chương | Hình | Bài trong sách | Nói 1 (Tom ↔ Emma) | Luyện nói chung / Nói 2 | Thêm ngoài sách |
|---|---|---|---|---|---|---|---|---|
| 34 My country | `U34-my-country` | 8:00 | 15 | 7 | 1–3 (bài 2: đáp án hiện trên bản đồ) | Bài 3: Việt Nam và nước Anh (5) | Part 1 "Your country" (5 câu) | bản đồ Brazil, đoạn văn, Glossary hai cảnh; famous for / popular with, high hay tall; Việt Nam bằng tiếng Anh, câu đố vị trí; Nghe và viết |
| **35 My town** | `U35-my-town` | 13:50 | 28 | 12 | 1–9 (bài 6: đoạn văn mẫu của Tom về TP. HCM) | Bài 9: TP. Hồ Chí Minh (6) | Part 2 "your hometown" (Tom: Đà Lạt, Emma: thị trấn ven biển nước Anh); thảo luận (3) | ba hàng tranh công trình, Spotlight place, bảng Facts và Opinions, Glossary ba cảnh; ôn tập: lỗi hay gặp |
| 36 The countryside | `U36-countryside` | 8:36 | 18 | 9 | 1–7 (bài 1 câu 2: Answer key in lệch) | Bài 3: quê bạn (5) | Part 1 "The countryside" (5 câu) | tranh trang trại 14 mục, đoạn Jack Robson, lời kể, Spotlight alone and lonely; nông thôn Việt Nam |
| 37 Shops | `U37-shops` | 8:29 | 17 | 6 | 1–6 (bài 6 thành Nói 1) | Bài 6: thói quen mua sắm (6) | Part 1 "Shopping" (5 câu) | bảng nơi mua sắm, Spotlight noun + shop, sáu lời nói về thói quen mua sắm, Glossary hai cảnh; mua sắm ở Việt Nam; Nghe và viết |
| **38 My home** | `U38-my-home` | 11:02 | 23 | 10 | 1–6 (bài 3: tự kiểm tra tranh ở phần ôn tập) | Bài 6: nhà của bạn (6) | Part 2 "a home you like" (Tom: nhà ở Đà Lạt, Emma: căn hộ tầng tám); thảo luận (3) | tranh tòa nhà (hai cảnh), sơ đồ nhà Bathford, quảng cáo, Glossary hai cảnh, Spotlight flat, house and home; nhà ở Việt Nam, thuê nhà; ôn tập: lỗi hay gặp |
| **39 The kitchen** | `U39-kitchen` | 10:52 | 23 | 6 | 1–6 (bài 3: tự kiểm tra tranh) | Bài 5: việc nhà ở nhà bạn (5) | Part 1 "Cooking" (5 câu); Part 2 "a time when you cooked a meal for other people" (Tom: canh cá của mẹ, Emma: bữa tối Giáng sinh); thảo luận (3) | tranh bếp 17 mục, 10 tranh việc nhà, Spotlight do + noun; do hay make, bếp Việt Nam; ôn tập: lỗi hay gặp |
| 40 Bedroom and bathroom | `U40-bedroom-bathroom` | 8:58 | 16 | 6 | 1–7 (bài 4: tự kiểm tra tranh) | Bài 7: thói quen của bạn (7) | Part 1 "Your room" (5 câu) | tờ giới thiệu, tranh phòng ngủ và phòng tắm 14 mục, bảng In the bathroom, Spotlight have + noun; sự cố trong phòng (thư GT Task 1) |
| 41 The living room | `U41-living-room` | 7:51 | 14 | 8 | 1–4 (bài 4: tự kiểm tra hai nửa tranh) | Bài 3: phòng khách của bạn (6) | bài nói mẫu của Tom; Part 1 "Your home" (5 câu) | tranh phòng khách 19 mục (hai nửa), ghi chú furniture; giới từ tả vị trí, phòng khách Việt Nam; tổng kết module |

Module Places (đợt 40) — đất nước, thành phố, nông thôn, cửa hàng, nhà, bếp, phòng ngủ, phòng tắm, phòng khách:
- **Tom:**
  - sinh ở Hà Nội, lớn lên ở Đà Lạt, muốn leo Fansipan một ngày nào đó (Unit 34); Đà Lạt có hồ, chợ, vườn hoa, chợ đêm, giờ đông
    khách du lịch hơn trước (Unit 35);
  - nhà ở Đà Lạt trên đồi, nhìn xuống thung lũng; quanh Đà Lạt trồng rau, hoa, dâu tây, cà phê, công ty của bố mua cà phê của nông
    dân; ông chăm vườn, rất khỏe so với tuổi; đôi khi Tom thấy cô đơn, nhớ nhà (Unit 36);
  - mua đồ dùng, mì gói ở cửa hàng tiện lợi dưới phố, hay đặt hàng qua ứng dụng (Unit 37);
  - căn hộ ở TP. HCM tầng ba, không có thang máy: ba phòng ngủ nhỏ, bếp nhỏ, phòng tắm, phòng khách rất nhỏ, chỗ để xe máy ở tầng
    trệt; nhà ở Đà Lạt hai tầng — tầng dưới bếp lớn, phòng khách, phòng của ông; tầng trên ba phòng ngủ, phòng tắm (Unit 38);
  - căn hộ không có lò nướng, máy rửa bát, nấu bằng bếp ga, máy giặt ở ban công; Tom đổ rác, ba người thay nhau rửa bát, không ai là
    quần áo; tháng trước nấu canh cá của mẹ cho hai bạn cùng phòng (Unit 39);
  - phòng riêng có giường đơn, bàn ghế, tủ quần áo nhỏ; phòng tắm có vòi sen, không có bồn tắm; gội đầu gần như mỗi ngày vì chơi bóng
    rổ, dùng lược, máy cạo râu điện (Unit 40);
  - phòng khách căn hộ có một cửa sổ nhỏ, sàn lát gạch, đèn và quạt trần; phòng khách nhà ở Đà Lạt có bộ bàn ghế gỗ, ảnh gia đình,
    tranh núi, buổi tối cả nhà uống trà, xem ti vi, ông luôn ngồi một ghế bành (Unit 41).
- **Emma:**
  - lớn lên ở thị trấn nhỏ ven biển miền nam nước Anh, khoảng 15.000 dân, có nhà thờ cổ, bến cảng nhỏ, bãi biển; mùa hè người Anh
    thích ra bờ biển miền tây nam (Unit 34, 35); thấy TP. HCM rất đa văn hóa, an toàn nhưng ồn (Unit 35);
  - đi Sa Pa hai năm trước; gần quê có nhiều trang trại, bố mẹ mua trứng, rau tươi ở đó; từ ban công chỉ thấy vài cây (Unit 36);
  - thấy siêu thị tiện, nhưng thích chợ vì thân thiện, được tập nói tiếng Việt (Unit 37);
  - căn hộ tầng tám có thang máy, chỗ để xe ở tầng hầm; ban đêm nhìn đèn thành phố (Unit 38);
  - có lò nướng nhỏ mua ở TP. HCM, không có máy rửa bát, máy giặt trong phòng tắm, tự làm mọi việc nhà; Giáng sinh năm ngoái nấu
    bữa tối kiểu Anh (gà quay, khoai tây nướng) cho ba giáo viên cùng trường (Unit 39);
  - phòng ngủ có giường đôi, bàn đầu giường, tủ ngăn kéo, tủ quần áo lớn; phòng tắm có bồn tắm kèm vòi sen, gương dài; ít dùng nước
    hoa, trang điểm nhẹ khi đi làm (Unit 40);
  - phòng khách có máy lạnh (nhà bố mẹ ở Anh có lò sưởi radiator), ảnh gia đình và bản đồ Việt Nam trên tường, sô-pha, bàn nước, giá
    sách — không đủ chỗ cho ghế bành (Unit 41).

### 5.8 Module Everyday life (Unit 17–23, Review tr. 61–64) — kế hoạch đợt 37

| Unit | Trang | Có thể khó (tới 15 phút) | Gợi ý phần nói | Hình trong sách (đã xem trang) |
|---|---|---|---|---|
| 17 My routine | 46–48 | Có: 3 trang, nhiều cụm động từ và trạng từ tần suất | Part 1 "Daily routine", "Weekends"; Part 2 "a typical day" | 12 tranh việc trong ngày (tr. 46); bài "What do you do at the weekend?" kèm Glossary (tr. 47); thang always → never và Spotlight every / all (tr. 48) |
| 18 Clothes | 49–50 | | Part 1 "Clothes", "Colours" | tranh quần áo, bảng màu (tr. 49); tranh phụ kiện (tr. 50) |
| 19 Buying clothes | 51–53 | Có: 3 trang, hội thoại cửa hàng | đóng vai mua đồ, hỏi cỡ, trả tiền (GT) | tranh tả quần áo long / tight / loose… (tr. 51); bảng cỡ và ảnh cửa hàng (tr. 52); hội thoại trong cửa hàng (tr. 53) |
| 20 Money | 54–55 | | Part 1 "Money", "Shopping" | tranh tiền, thẻ, hóa đơn và hội thoại (tr. 54); quảng cáo kèm Glossary (tr. 55) |
| 21 The weather | 56–57 | | Part 1 "Weather", "Seasons" | bảng ký hiệu thời tiết sunny / cloudy / windy… (tr. 56); ảnh bão và bài đọc (tr. 57) |
| 22 Illness | 58–59 | Có: nhiều triệu chứng, lời khuyên với should; chủ đề GT | đi khám, gọi xin nghỉ (GT); nối với Unit 12, 16 | 12 tranh triệu chứng (tr. 58); tranh người ốm với lời khuyên (tr. 59) |
| 23 At the chemist's | 60 | | hỏi mua thuốc (GT) | hội thoại ở hiệu thuốc và tranh đồ bán ở hiệu thuốc |

Nhân vật đã có nhiều chi tiết về giờ giấc (Unit 2), quán cà phê (Unit 16), đi khám (Unit 12) — soát mục 5.7 trước khi viết.
Phiên Review của module chưa có video. Nếu làm thì dùng cảnh `blanks` ôn từ của cả module, không đếm ngược.

Đã làm ở đợt 37 (bảng mục 5.7): unit khó là 17, 19, 22 như dự kiến. Module tiếp theo: **Food and drink** (Unit 24–28, Review
tr. 75–77) — 24 Meat and fish (tr. 65), 25 Fruit and vegetables (66–67), 26 Buying food (68–70), 27 In a café (71), 28 In a
restaurant (72–74). Chưa xem trang; unit ba trang (26, 28) có thể là unit khó, unit một trang (24, 27) cần thêm cảnh ngoài sách.

Đã làm ở đợt 38 (bảng mục 5.7): unit ba trang 26, 28 là unit khó; unit một trang 24, 27 thêm cảnh ngoài sách. Module tiếp theo:
**Getting around** (Unit 29–33, Review tr. 87–89):
- 29 Buses (tr. 78–79), 30 Trains (80–81), 31 Directions (82–83), 32 Roads and traffic (84–85), 33 Signs and notices (86);
- Answer key tr. 211 đã có đáp án Unit 29–30;
- chưa xem trang; chủ đề đi lại hay gặp ở IELTS General Training (hỏi đường, mua vé, biển báo).

Đã làm ở đợt 39 (bảng mục 5.7): unit khó là 30 Trains, 32 Roads and traffic (hai trang, hai phần, nhiều từ, chủ đề IELTS); unit
một trang 33 và unit 31 thêm cảnh ngoài sách. Module tiếp theo: **Places** (Unit 34–41, Review tr. 105–108):
- 34 My country (tr. 90), 35 My town (91–93), 36 The countryside (94–95), 37 Shops (96–97), 38 My home (98–99), 39 The kitchen
  (100–101), 40 Bedroom and bathroom (102–103), 41 The living room (104);
- chưa xem trang; unit ba trang (35) có thể là unit khó; chủ đề nơi ở, quê hương, nhà cửa hay gặp ở IELTS Part 1–2.

Đã làm ở đợt 40 (bảng mục 5.7): unit khó là 35 My town (ba trang, ba phần, "your hometown" là chủ đề IELTS hay gặp nhất), 38 My
home (nhà ở, thuê nhà — thư GT Task 1) và 39 The kitchen (17 đồ dùng, 10 cụm việc nhà, do / make); unit một trang 34, 41 thêm cảnh
ngoài sách. Module tiếp theo: **Study and work** (Unit 42–47, Review tr. 122–125):
- 42 My school (tr. 109–111), 43 University (112–113), 44 Jobs (114–115), 45 Describing a job (116–117), 46 Using a computer
  (118–119), 47 Email and the internet (120–121);
- Answer key tr. 214 đã có đáp án Unit 42 (môn học);
- chưa xem trang; unit ba trang (42) có thể là unit khó; học tập và công việc là chủ đề IELTS Part 1 bắt buộc ("Do you work or
  are you a student?"), email là chủ đề thư GT Task 1.

### 5.9 Video nghe – viết 10 phút (đợt 36)

Người học: "mỗi chủ đề thêm 1 video luyện nghe 10 phút ko đứt quãng tôi tự pause lại để viết theo từ vựng câu theo chủ đề
phải bao gồm các từ vựng trong sách thuộc chủ đề trong sách rồi tìm thêm các từ vựng câu hay giao tiếp".

**Khuôn:**
- **Mỗi unit một video thứ hai** `<id video unit>-dictation`, ví dụ `U02-time-dictation`. Video dùng cùng `activity` với
  video bài giảng, nên nằm cùng phiên, cùng thẻ unit, đứng ngay sau video bài giảng (`lessons.json` xếp theo id). Nút ghi
  "Dictation · listen and write: …".
- **Khoảng 10 phút, chạy liền, không có khoảng lặng:** không `wait` / `echo`, không đếm ngược, không dòng nào có `pause`.
  Người học: "video ko nên có pause quá 3 giây nếu có ko có càng tốt" — họ tự tạm dừng để viết. Chỉ còn khoảng ngắt tự nhiên
  0,45 giây giữa hai câu (`gap`) và 0,4 giây khi sang cảnh (`scene_gap`). Test cho phép 9–11 phút, và đo bằng ffmpeg
  (`silencedetect`, −45 dB) thì không có khoảng lặng nào từ 3 giây trở lên.
- **Ba phần**, mỗi phần một chương:
  1. *Từ trong sách* (Emma đọc).
     - Gồm mọi mục Word list của unit (`work/wordlist.json`) và từ trên trang unit không có trong Word list: Unit 1 có số
       11–20, -teen / -ty, số lớn, số điện thoại, giá tiền, %; Unit 2 có cách nói giờ; Unit 3 có thứ, tháng, số thứ tự,
       cách đọc năm.
     - Mỗi mục đọc số thứ tự, đọc từ hai lần, rồi câu ví dụ hai lần, để người học viết được cả câu.
     - Mục Word list liền nhau thì ghép một dòng (`France, French`; `grandfather, grandmother`), để Unit 4 (79 mục) vẫn vừa
       10 phút.
  2. *Từ thêm theo chủ đề* (Tom đọc): 10–25 từ ngoài sách, hay gặp và dùng được ngay. Ví dụ Unit 2: hour, on time,
     appointment; Unit 12: headache, sore throat.
  3. *Câu giao tiếp*: 14–30 câu, phần lớn là cặp hỏi – đáp, Emma và Tom đọc xen kẽ, mỗi câu đọc hai lần.
     - Câu ngôi thứ nhất khớp hồ sơ nhân vật (mục 5.7, file 06 mục 9.4), ví dụ: Tom 20 tuổi, quê Đà Lạt, sinh 9/3/2006, chị
       Hoa là y tá ở Hà Nội; Emma 28 tuổi, dạy ở TP. HCM ba năm, gọi cho mẹ mỗi Chủ nhật, sợ nhện.
     - Câu không có trong hồ sơ thì viết trung tính (He / She / They) hoặc thành câu hỏi.
- **Cảnh `dictation`** (thêm vào `agents/lesson_video` ở đợt 36):
  - tối đa 6 dòng; mỗi dòng có số `n`;
  - generator chia mỗi phần thành cảnh 6 dòng; cảnh cuối chỉ còn 1–2 dòng thì chia đều hai cảnh cuối (6 + 1 → 4 + 3,
    6 + 2 → 4 + 4), để không có cảnh gần trống (test: mỗi cảnh ít nhất 3 dòng);
  - dòng chưa `reveal` chỉ có vạch kẻ để viết; mở ra thì hiện `answer` (chữ đậm), nghĩa `vi`, câu ví dụ `ex`;
  - dòng đọc mục k + 1 mở đáp án mục k; câu "Check your answers." cuối cảnh mở mục cuối;
  - phụ đề không bao giờ hiện lời đang đọc, chỉ ghi "Listen and write…";
  - `w` là mục Word list mà dòng đó phủ (một hoặc nhiều); lệnh `wordlist` dùng `w` để soát đủ từ.
- **Word list của sách** (tr. 237–254, tức PDF 236–253; hai cột, mỗi từ kèm số unit):
  - Bản quét không có lớp chữ, nên OCR bằng rapidocr hai lần. Lần đầu lề trên 30 điểm làm mất dòng đầu mỗi cột; lần hai lề
    8 điểm thì đọc "11" thành "1l". Lấy hợp của hai lần rồi soát tay theo ảnh trang.
  - Kết quả ở `work/wordlist.json`: 1261 mục của Unit 1–41 (1087 từ khác nhau); `level` để trống vì sách không chia cấp độ.
  - Đợt 37 thêm 246 mục Unit 17–23 từ cùng hai lần OCR. Soát khoảng hở giữa các dòng OCR (dòng bị bỏ) rồi xem ảnh: sót *get dressed*
    (17); bộ tách bỏ qua dòng *red* (18). Ba mục in số unit của bản thảo cũ (mục 3.3) xếp theo trang thật: *like* vào Unit 21, *have
    got* và *what's the matter?* vào Unit 22; câu chú thích ở `make_wordlist.py` và đầu kịch bản nghe – viết.
  - Đợt 38 thêm 184 mục Unit 24–28 (157 từ chưa có ở Unit 1–23), soát như đợt 37: không sót mục nào. Mục có chú thích nghĩa
    (*can* =container, *matches* =to start a fire, *pepper* =vegetable ở Unit 25 và =spice ở Unit 28, *well done* =cooked for a
    long time…) giữ chú thích ở `def`. `make_wordlist.py` thêm loại từ `adv` (*sure*).
  - Đợt 39 thêm 127 mục Unit 29–33 (92 từ chưa có ở Unit 1–28). Soát khoảng hở như đợt 37: không sót mục nào. Sách in số của
    bản thảo cũ cho năm mục, xếp theo trang thật: *accident* 29 và *kilometres* 31 vào Unit 32 (tr. 85); *order* (out of order),
    *queue here*, *ring* (of a bell) 29 vào Unit 33 (tr. 86). *long* (a metre long) 29 không có trên trang nào nên để Unit 29 như
    sách in. `make_wordlist.py` thêm loại từ `prep` (*outside*, *opposite*).
  - Đợt 40 thêm 271 mục Unit 34–41 (219 từ chưa có ở Unit 1–33). Soát khoảng hở như đợt 37: OCR sót *enormous* (34), thêm tay
    theo ảnh trang. Từ có ở nhiều unit (*market* 35, 37; *do the shopping* 37, 39; *clean* 35, 39, 40; *floor* 38, 41…) thì unit nào
    cũng phải phủ trong video của unit đó; *wash* (danh từ) và *wash* (động từ) chung một khóa. Unit 35 có 54 mục, nhiều nhất từ
    đầu sách (mục 5.6).
  - Soát đủ từ: `python -m lesson_video wordlist ../books/book_oxford_word_skills_basic --unit U04 --level all` phải ra
    "chưa hiện: 0" (test kiểm mọi unit có video).
- **Sinh kịch bản:** dữ liệu từng unit (từ, nghĩa, câu ví dụ, mục Word list, cách đọc `s` / `se`) ở `work/dictation/units_*.py`.
  Lệnh `python3 books/book_oxford_word_skills_basic/work/dictation/gen_dictation.py U02` ghi
  `lessons/U02-time-dictation.yaml`. Kịch bản là bản sinh ra: sửa dữ liệu rồi sinh lại, không sửa tay.

**Quy trình một unit:**
1. In mục Word list của unit: `python -m lesson_video wordlist … --unit U17 --level all`. Xem trang unit để thêm từ trên trang
   mà Word list không có.
2. Viết dữ liệu: từ trong sách 20–45 dòng, từ thêm 10–25, câu 14–30. Sinh kịch bản, rồi chạy `check`, `phonemes` (sửa bằng `s`
   / `se`) và `wordlist --level all` (phải ra 0).
3. Ước lượng thời lượng bằng bộ đọc im lặng; nhắm 9:10–9:40 (bản dựng Kokoro dài hơn ước lượng 0–9 %: Unit 2 ước 9:51, dựng thật 10:25; Unit 22 ước 9:02, dựng thật 9:02; Unit 34 ước 9:15, dựng thật 10:05). Thiếu thì thêm từ, câu; không thêm `pause`.
4. Dựng video, rồi chạy `python3 web/build.py`.

**Lưu ý:**
- Bản đầu (đợt 36) có nghỉ 1,5 giây sau mỗi từ và 2 giây sau mỗi câu. Đo bản dựng Unit 2: khoảng lặng trung vị 2,0 giây,
  dài nhất 3,5 giây ở chỗ chuyển cảnh (nghỉ 2 giây + `gap` + `scene_gap` 0,8 giây). Người học yêu cầu không quá 3 giây, tốt
  nhất là không có, nên đã bỏ mọi `pause`, `scene_gap` còn 0,4, câu ví dụ đọc hai lần, thêm từ và câu cho đủ 10 phút.
  Đo lại bản dựng mới của Unit 2: khoảng lặng trung vị 0,54 giây; chỗ chuyển cảnh khoảng 1,05 giây; dài nhất 2,05 giây ở
  cuối video.
- `a.m.`, `p.m.` Kokoro đọc đúng, không cần `say`. Số -teen đứng riêng hoặc cuối câu vẫn dùng `thir-teen`… (mục 5.5).
- `phonemes` báo nhầm ở "for office use only" (Unit 9: use là danh từ) và "close friends" (Unit 15: close là tính từ); đã
  ghi ở đầu kịch bản.
- Đáp án dài thì chữ tự thu nhỏ. Đã soát: không mục nào bị cắt chữ.

**41 video, 6:47:41** (dòng của phần 1 ghép các mục Word list liền nhau, nên có khi ít hơn số mục):

| Unit | Video | Dài | Từ trong sách (dòng · mục Word list) | Từ thêm | Câu giao tiếp |
|---|---|---|---|---|---|
| 1 · Numbers | `U01-numbers-dictation` | 10:00 | 29 · 4 | 20 | 34 |
| 2 · The time | `U02-time-dictation` | 10:25 | 27 · 20 | 23 | 36 |
| 3 · Days and dates | `U03-days-dates-dictation` | 10:32 | 29 · 14 | 19 | 28 |
| 4 · Countries and nationalities | `U04-countries-dictation` | 10:55 | 43 · 79 | 10 | 20 |
| 5 · Classroom vocabulary | `U05-classroom-dictation` | 10:01 | 24 · 22 | 26 | 34 |
| 6 · English language words | `U06-language-words-dictation` | 10:26 | 22 · 17 | 26 | 32 |
| 7 · Questions about language | `U07-questions-language-dictation` | 10:01 | 23 · 19 | 27 | 35 |
| 8 · Personal information | `U08-personal-info-dictation` | 9:58 | 21 · 16 | 28 | 40 |
| 9 · Filling in a form | `U09-form-dictation` | 10:20 | 21 · 19 | 27 | 35 |
| 10 · My family | `U10-family-dictation` | 10:06 | 24 · 36 | 22 | 31 |
| 11 · Physical actions | `U11-actions-dictation` | 9:49 | 25 · 25 | 27 | 37 |
| 12 · Parts of the body | `U12-body-dictation` | 9:42 | 28 · 30 | 24 | 34 |
| 13 · Describing people | `U13-describing-people-dictation` | 9:56 | 36 · 45 | 20 | 30 |
| 14 · Character | `U14-character-dictation` | 10:18 | 28 · 30 | 24 | 32 |
| 15 · Relationships | `U15-relationships-dictation` | 10:05 | 22 · 32 | 23 | 35 |
| 16 · Feelings | `U16-feelings-dictation` | 10:04 | 22 · 25 | 28 | 35 |
| 17 · My routine | `U17-routine-dictation` | 10:22 | 31 · 46 | 17 | 28 |
| 18 · Clothes | `U18-clothes-dictation` | 9:41 | 31 · 47 | 21 | 28 |
| 19 · Buying clothes | `U19-buying-clothes-dictation` | 9:15 | 30 · 41 | 18 | 29 |
| 20 · Money | `U20-money-dictation` | 9:21 | 27 · 31 | 22 | 30 |
| 21 · The weather | `U21-weather-dictation` | 9:14 | 26 · 34 | 20 | 28 |
| 22 · Illness | `U22-illness-dictation` | 9:44 | 25 · 31 | 26 | 32 |
| 23 · At the chemist's | `U23-chemists-dictation` | 9:22 | 24 · 16 | 20 | 30 |
| 24 · Meat and fish | `U24-meat-fish-dictation` | 10:24 | 21 · 21 | 27 | 34 |
| 25 · Fruit and vegetables | `U25-fruit-vegetables-dictation` | 10:05 | 36 · 38 | 18 | 28 |
| 26 · Buying food | `U26-buying-food-dictation` | 9:48 | 35 · 47 | 18 | 30 |
| 27 · In a café | `U27-cafe-dictation` | 10:03 | 22 · 26 | 28 | 34 |
| 28 · In a restaurant | `U28-restaurant-dictation` | 9:55 | 35 · 52 | 17 | 28 |
| 29 · Buses | `U29-buses-dictation` | 10:03 | 21 · 18 | 24 | 33 |
| 30 · Trains | `U30-trains-dictation` | 10:06 | 28 · 34 | 19 | 30 |
| 31 · Directions | `U31-directions-dictation` | 10:00 | 20 · 18 | 24 | 33 |
| 32 · Roads and traffic | `U32-roads-traffic-dictation` | 10:06 | 26 · 32 | 20 | 30 |
| 33 · Signs and notices | `U33-signs-notices-dictation` | 10:06 | 23 · 25 | 24 | 32 |
| 34 · My country | `U34-my-country-dictation` | 10:05 | 25 · 19 | 20 | 28 |
| 35 · My town | `U35-my-town-dictation` | 10:10 | 45 · 54 | 10 | 18 |
| 36 · The countryside | `U36-countryside-dictation` | 9:38 | 32 · 34 | 16 | 26 |
| 37 · Shops | `U37-shops-dictation` | 9:28 | 26 · 30 | 20 | 29 |
| 38 · My home | `U38-my-home-dictation` | 9:27 | 31 · 36 | 16 | 28 |
| 39 · The kitchen | `U39-kitchen-dictation` | 9:30 | 29 · 36 | 19 | 32 |
| 40 · Bedroom and bathroom | `U40-bedroom-bathroom-dictation` | 9:33 | 34 · 39 | 16 | 29 |
| 41 · The living room | `U41-living-room-dictation` | 9:37 | 21 · 23 | 24 | 31 |

## 6. Việc tiếp theo

1. Video Unit 42 trở đi theo mục 5 (checklist P2-59), module Study and work (cuối mục 5.8). Mỗi unit hai video: bài giảng
   (mục 5) và nghe – viết (mục 5.9).
2. Có CD-ROM thì thêm audio phát âm từng từ (khai thư mục audio trong `files`, như sách có track).
3. Gặp thêm lỗi in trong Answer key thì ghi vào mục 3.3.
