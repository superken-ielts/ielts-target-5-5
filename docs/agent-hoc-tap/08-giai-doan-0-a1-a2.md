# 08 — Giai đoạn 0: nền tảng A1–A2 trước lộ trình IELTS (English Unlimited)

Lộ trình 40 tuần bắt đầu từ band 3.0. Giai đoạn 0 dành cho người học lại từ đầu hoặc dưới band 3.0, để người học khác
cũng dùng được app từ con số 0. Giai đoạn này đứng **trước tuần 1** và không tính vào 40 tuần.

| Thành phần | Ở đâu |
|---|---|
| Sách, audio, hồ sơ lộ trình A2 | `books/book_english_unlimited_a2_elemetary/`: `book.yaml` (mẫu `lessons-v1`), `book.json`, `plan.json`, `report.md`, `web/` (32 đoạn PDF) |
| Sách A1 (chưa nhập) | `books/book_english_unlimited_A1_Starter/`: Teacher's Book, 2 CD, Teacher's Pack, wordlist; Coursebook mới là bản mẫu |
| Vị trí trong tab Sách | `books/catalog.json`: nhóm `ielts`, hai thẻ A1 và A2 đứng trước IELTS Target 5.0 |
| Mẫu lộ trình | `agents/book_ingest/lessons.py`: nhãn track theo đĩa `track: "1.{n}"`, một PDF khai hai lần |

---

## 1. Vì sao chọn English Unlimited

Người học hỏi có nên thêm một cuốn IELTS cho band 0–3.5 kiểu *Bridge to IELTS* không. Kết luận ở đợt 17–18:

- *Bridge to IELTS* bắt đầu từ khoảng band 3.5. Phần lớn nội dung trùng với IELTS Target 5.0, nên không lấp được
  khoảng 0 → 3.0.
- Dưới band 3.0, thứ còn thiếu là tiếng Anh tổng quát A1–A2: vốn từ, thì hiện tại và quá khứ, nghe hội thoại chậm,
  nói câu đơn về bản thân. Sách luyện thi chưa phải lúc này.
- English Unlimited (Cambridge) xây theo khung CEFR: mỗi unit là các việc làm được bằng tiếng Anh. Phần lớn là chủ đề
  của IELTS General Training và Speaking Part 1:
  - giới thiệu người quen, nhờ và mời;
  - thuê phòng, gọi món, mua vé;
  - khám bệnh, kể một chuyến đi.

  Sách có Teacher's Book (đáp án từng bài) và Class Audio, nên tự học được. Danh sách sách ở file 05 mục K cũng xếp
  English Unlimited A1, A2 vào mức "mất gốc".
- Mốc ra là **đề mẫu A2 Key** (Cambridge English, miễn phí): đo được trình độ A2 thật, không cần thang band IELTS.

Người đã ở band 3.0 (như người học hiện tại) làm đề mẫu A2 Key trước. Đạt thì vào thẳng Giai đoạn 1, chỉ học những
unit còn yếu.

## 2. Lộ trình A2 trong tab Sách

**79 phiên** gồm 75 phiên học, 1 phiên ôn sau mỗi chặng (3 phiên) và 4 phiên đề mẫu A2 Key. Phiên mặc định 60 phút;
Target activity và Look again 45 phút. Tổng khoảng 72 giờ. Ở nhịp 5 phiên/tuần là 16 tuần; chọn được 4–6 phiên/tuần
(20–14 tuần).

| Chặng | Mục | Phiên |
|---|---|---|
| 1 · CD1 | Intro (About you) | 2 |
| | Unit 1–4 | 20 |
| | Achievement test 1 | 1 |
| 2 · CD2 | Unit 5–9 | 25 |
| | Achievement test 2 | 1 |
| 3 · CD3 | Unit 10–14 | 25 |
| | Achievement test 3 | 1 |
| | Mốc A2 Key | 4 |

Mỗi unit có 8 trang, chia thành 5 phiên. Mỗi phiên mở đúng trang Coursebook và các track của phần đó. Nút
*Teacher's Book* mở đúng trang ghi chú và đáp án của phần đó:

| Phiên | Trang (unit bắt đầu ở trang s) | Nội dung | Lõi |
|---|---|---|---|
| Bài 1 | s, s+1 | Bài X.1: nghe hoặc đọc, ngữ pháp, từ vựng, phát âm, nói | |
| Bài 2 | s+2, s+3 | Bài X.2 | |
| Target activity | s+4 | Nhiệm vụ nói của unit (kể về một người, thuê phòng, gọi món…) | ✓ |
| Explore | s+5, s+6 | Keyword, Across cultures hoặc Independent learning. Unit lẻ có Explore Speaking, unit chẵn có Explore Writing | ✓ |
| Look again | s+7 | Review, Extension (Spelling and sounds), Self-assessment 1–5 | |

- **Hướng dẫn từng phiên** viết bằng tiếng Việt, lấy theo mục lục sách (trang 2–5). Bước mặc định chứa cách học
  chung. Phần riêng của từng unit nằm ở các trường `l1`, `l2`, `ta`, `ex`, `la` của mục. Ghi chú bước dùng được mọi
  trường của mục (đợt 18).
- **Achievement test 1–3** nằm sau Unit 4, 9 và 14, theo Teacher's Book. Đề giấy nằm trong Teacher's DVD-ROM nên
  không có ở đây. App có bài nghe (track cuối của mỗi đĩa) và nút mở trang Look again của các unit trong chặng để
  chấm lại Self-assessment.
- **Mốc A2 Key** có 4 phiên: Reading & Writing 60 phút, Listening khoảng 35 phút, Speaking tự luyện, rồi chấm điểm
  và quyết định. Đúng khoảng 70% mỗi phần thì sang Giai đoạn 1. Đây là mốc tham khảo; kỳ thi thật đạt A2 từ 120 điểm
  thang Cambridge English Scale. Đề tải ở cambridgeenglish.org (A2 Key → Preparation), nên phiên không có trang sách
  hay track. Bước nghe đặt id `listening-test`, không đặt `listening`: luật V4 bắt mọi bước `listening` phải có track.
- `missing` có `test-books`, nên thẻ các bài test hiện "chưa có sách Test".
- Tuần trong lộ trình A2 đếm riêng (bắt đầu tuần 1). Học xong thì đặt lại ngày bắt đầu lộ trình 40 tuần cho Giai
  đoạn 1. Ghi chú "Bắt đầu khi" của sách nói điều này.

## 3. Dò trang và track

### 3.1 Trang

| File | Trang in | Trang PDF |
|---|---|---|
| Coursebook Part 1 (`course-book`) | 1–49 (Intro trang 7) | trang in + 1 |
| Coursebook Part 1 lần hai (`course-book-u6`) | 50–65 (Unit 6–7) | trang in + 2 |
| Coursebook Part 2 (`course-book-2`) | 66–121 (Unit 8–14) + 122–123 (Activities) | trang in − 65 |
| Teacher's Book (`teachers-book`) | 1–124 | bằng trang in |

- **Trang quét trùng.** Part 1 có trang 49 quét hai lần (PDF 50 và 51 giống nhau). App tính trang in bằng
  `trang PDF − pageOffset`, mỗi file một số. Vì thế Part 1 khai hai lần: hai id, cùng `path`, `page_offset` 1 và 2. Mỗi
  id có đoạn PDF riêng (`course-book-p…`, `course-book-u6-p…`), không cần sửa app.
- `item.pages` (dòng "Trang 50–57" trên thẻ unit) tính theo file `course-book`. Kết quả vẫn đúng với mọi unit, vì app
  đổi ngược bằng cùng độ lệch đó.
- **Trang Activities 122–123** có phiếu đăng ký (Intro bài 8a), đáp án quiz (Unit 2 Look again) và thông tin Student
  A / B cho bốn bài nói cặp (Unit 3, 10, 11, 13). Các trang này gắn vào phiên tương ứng bằng `alt`.
- **Teacher's Book:** trang của từng phiên lấy từ tiêu đề cỡ chữ lớn ("1.1", "1.2", "1.3 Target activity",
  "1 Explore", "1 Look again"). Một trang Teacher's Book có thể vừa là cuối phần này vừa là đầu phần sau; khi đó
  trang ấy thuộc cả hai phiên.

### 3.2 Track

- Mỗi đĩa đánh số lại từ 1: `Track No07.mp3` ở CD1 là bài **1.7** in trong sách. Thư mục audio khai
  `track: "1.{n}"`; `{n}` là số cuối trong tên file.
- Track 01 của mỗi đĩa gồm lời giới thiệu đĩa rồi tới bài 1.1, 2.1, 3.1. Đã kiểm bằng nhận dạng giọng nói thô
  (pocketsphinx, chạy ngoài repo): "English Unlimited Elementary, published by Cambridge…", tiếp theo là "I'm from
  Wales and I can speak some French…".
- Track cuối mỗi đĩa (1.57, 2.57, 3.62) là phần nghe của Achievement test 1–3. Teacher's Book trang 18 ghi đúng như
  vậy.
- CD1 thiếu 5 file (track 27, 33, 36, 39, 51). Khoảng `1.26..1.28` tự bỏ qua track thiếu. Một track đứng riêng thì ghi
  bài kề nó (Target activity Unit 2 chỉ còn 1.26).

Cách dò track nào thuộc trang nào:
1. **OCR nhãn cam.** Lớp chữ của Coursebook quét quá kém: chỉ tìm được 13/176 nhãn. Thay vào đó:
   - vẽ từng trang ở 200 dpi;
   - lọc vùng màu cam của nhãn audio (R > 190, G 40–130, B < 110), gộp vùng và lọc theo kích thước;
   - cắt từng nhãn, phóng to 3 lần, đọc bằng RapidOCR.

   Cách này tìm được gần hết nhãn. Khoảng 30 nhãn đọc sai (ví dụ "2 6" thay vì 2.9) được soát bằng mắt trên ảnh cắt.
2. **Gán theo trang xuất hiện đầu tiên.** Nhãn xuất hiện lại sau đó ("Listen again", Look again nhắc lại bài cũ) không
   tính. Mỗi track theo trang đó vào phiên Bài 1, Bài 2, Target activity, Explore hoặc Look again.
3. **Đối chiếu với Teacher's Book.** Teacher's Book có lớp chữ sạch. Mỗi chỗ "play recording X.Y" nằm dưới tiêu đề
   phần nào thì thuộc phần đó. Kết quả khớp với cách 2 ở **171/171** nhãn Teacher's Book có nhắc; 7 chỗ khác chỉ là số
   mục ("2.1", "3.30") bị đọc nhầm thành nhãn. Ba nhãn OCR không thấy lấy từ Teacher's Book:
   - 1.25 ở bài 2.2;
   - 3.7 (Keyword about) và 3.10 (đọc phiên âm) ở Explore Unit 10.

Kết quả: 171 track, mỗi track thuộc đúng một phiên (V4). `ingest` báo OK: 15 unit, 4 test, 79 phiên, tuần 1–16.

## 4. English Unlimited A1 Starter — đang chờ sách

Thư mục `books/book_english_unlimited_A1_Starter/` đã có:
- Teacher's Book (ghi chú Unit 1–10);
- CD1 (92 track) và CD2 (69 track), đủ cả hai;
- Teacher's Pack: Progress test 1–10 kèm đáp án, worksheet, thang chấm Speaking;
- wordlist.

File Coursebook mới là **bản mẫu** 26 trang: mục lục, Unit 3 và một phần Unit 9. Chưa đủ để dựng lộ trình, vì mỗi
phiên cần trang sách để làm bài.

Trong tab Sách, A1 hiện là thẻ "chưa nhập" đứng trước A2: có mục tiêu và ghi chú còn thiếu gì. Khi có Coursebook đầy
đủ (khoảng 100 trang trở lên; có Self-study Pack thì càng tốt), làm như A2:
1. Viết `book.yaml` mẫu `lessons-v1`, mỗi unit 5 phiên.
2. Dò nhãn track bằng OCR nhãn màu rồi đối chiếu với Teacher's Book.
3. Chạy `ingest`.

## 5. Việc tiếp theo

- **Video bài giảng cho từng unit A2** (P2-53):
  - làm như GENKI: giảng bằng tiếng Anh, chữ tiếng Việt trên màn hình, phát audio gốc của sách, video 5–10 phút;
  - làm Intro và Unit 1–3 trước;
  - Speaking (Target activity, Explore Speaking) và Writing (Explore Writing) trước, rồi Listening và Reading.

  Coursebook không có phần Scripts (trang 148–159). Vì thế lời các bài nghe phải chép lại từ audio, sau đó soát bằng
  tai. Lời này dùng cho phụ đề và câu hỏi trong video.
- **A1 Starter** (P2-52): chờ Coursebook đầy đủ.
- Đề Achievement test và đề mẫu A2 Key: nếu người học đặt file vào thư mục sách, khai thêm vào `files` và `refs` của
  bốn mục test.
