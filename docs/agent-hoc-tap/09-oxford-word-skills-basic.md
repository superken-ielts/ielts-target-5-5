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
| Video bài giảng | `books/book_oxford_word_skills_basic/lessons/` (kịch bản `.yaml`, `.mp4`, `lessons.json`); sổ tay ở mục 5; Unit 1–16 đã có (mục 5.7) |

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
  hay gặp ở IELTS Part 2. Module People có 4 unit khó: 10 My family, 13 Describing people, 14 Character, 16 Feelings.
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
| 7 | Nói 2 · đến lượt bạn | `practice` (self-paced) | 5 câu hỏi có gợi ý. Emma đọc hết, `pause: 0.5`, câu cuối `pause: 1.5` |
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
| Hoa, Hạnh, Khoa | `Whah`, `Hahn`, `Kwah` | Tên người Việt (đợt 29: chị Hoa, mẹ Hạnh của Tom). `Hoa` đọc thành /hoʊə/, `Hwa` đọc từng chữ |
| Mr, Mrs, Ms; Mrs Green | `Mister`, `Missiz`, `Mizz`; `Missiz Green` | Danh xưng đứng riêng (Unit 9) đọc sai hoặc đọc từng chữ |
| CB2 4TX, N/A | `C B two, four T X`, `N A` | Mã bưu điện, chữ viết tắt trên form |
| Kovács, Zsuzsa | `Kovach`, `Zhoozha` | Tên Hungary trong bài 2 Unit 8 |
| Langbiang | `Lang Bee-ang` | Núi ở Đà Lạt (Unit 11) |
| live, lives (động từ) | `liv`, `livz` | Đọc /laɪv/ (⚠ của `phonemes`); "lived" đọc đúng, không cần `say` |
| used (động từ, quá khứ) | `yoozd` | Như `yooz` |

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

### 5.7 Độ phủ video và chi tiết nhân vật

Module Basic English đủ 7/7 unit, tổng 51:11 (đợt 26, thêm hình ở đợt 30). Module People đủ 9/9 unit, tổng 1:22:54
(đợt 29). Cả sách: 16 video, 2:14:06, 48 cảnh có hình. Cột "Hình" là số cảnh có hình trong sách (mục 5.3a).

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

### 5.8 Module tiếp theo: Everyday life (Unit 17–23, Review tr. 61–64)

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

## 6. Việc tiếp theo

1. Video Unit 17 trở đi theo mục 5 (checklist P2-59), kế hoạch module Everyday life ở mục 5.8.
2. Có CD-ROM thì thêm audio phát âm từng từ (khai thư mục audio trong `files`, như sách có track).
3. Gặp thêm lỗi in trong Answer key thì ghi vào mục 3.3.
