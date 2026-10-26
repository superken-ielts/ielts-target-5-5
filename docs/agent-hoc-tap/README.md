# Hệ thống agent học tập — kế hoạch triển khai

Kế hoạch hiện thực hóa technical summary *"Hệ thống agent học tập: từ sách đến app học"*
(04/10/2026) trên mã nguồn hiện có của repo: biến bộ IELTS Target 5.0 (PDF + MP3) thành
menu sách và phiên học trong app, rồi dùng lại cho sách khác và các agent sau.

Thư mục này là tài liệu kỹ thuật. Từ đợt 2, `web/build.py` nhúng cả thư mục vào app học: xem ở tab **Kế hoạch**
(nhóm "Agent học tập — checklist và kế hoạch") hoặc từ thẻ "Agent nhập sách" ở tab **Sách**.

| File | Nội dung |
|---|---|
| [01-review-code-hien-tai.md](01-review-code-hien-tai.md) | Kiến trúc app hiện tại, điểm tích hợp, 10 lỗi và rủi ro (B1–B10), ràng buộc kỹ thuật |
| [02-kien-truc-va-hop-dong-du-lieu.md](02-kien-truc-va-hop-dong-du-lieu.md) | Cấu trúc thư mục, schema `book.yaml` / `book.json` / `plan.json` / `review.json` / tiến độ, thuật toán từng bước nhập sách, thiết kế tích hợp từng tab |
| [03-ke-hoach-trien-khai.md](03-ke-hoach-trien-khai.md) | 10 quyết định cần chốt, đường găng theo tuần học, 5 giai đoạn với spike và cổng kiểm tra, chiến lược test, rủi ro |
| [04-checklist.md](04-checklist.md) | Checklist từng task (P0-01 … P4-07) kèm điều kiện đạt và cổng G0–G4 |
| [05-lich-su-thay-doi.md](05-lich-su-thay-doi.md) | Lịch sử từng đợt triển khai: file thêm/sửa/xóa, chỗ làm khác plan, kết quả kiểm thử, việc còn treo |
| [06-video-bai-giang.md](06-video-bai-giang.md) | Video bài giảng (chỉ Course Book): Unit 1–3 phần nào có video, lịch sử từng video, quy trình, kiểu cảnh, cách đọc, kế hoạch Unit 4 |
| [07-lo-trinh-n5-tieng-nhat.md](07-lo-trinh-n5-tieng-nhat.md) | Lộ trình JLPT N5 với GENKI I: đánh giá bản thiết kế "Genki I × IELTS Target 5.0", chỗ đã sửa, 78 phiên với trang và track của từng phần, video tiếng Nhật (Unit 0: năm video; bài 1–3: bốn video kỹ năng mỗi bài), kế hoạch bài 4–12 |
| [08-giai-doan-0-a1-a2.md](08-giai-doan-0-a1-a2.md) | Giai đoạn 0 trước lộ trình IELTS: vì sao chọn English Unlimited, 79 phiên của cuốn A2, cách dò trang và track (OCR nhãn cam, đối chiếu Teacher's Book), mốc A2 Key, cuốn A1 đang chờ sách, kế hoạch video |

## Trạng thái

**Đợt 1 (04/10/2026):** agent nhập sách `agents/book_ingest` đã chạy trên IELTS Target 5.0 (120 phiên, 59 track,
27 đoạn PDF) và app có tab **Sách** để học theo lộ trình.

**Đợt 2 (04/10/2026):** tab Sách có màn danh sách sách (trình độ, thời lượng, số tháng học xong) và màn chi tiết để
chọn học bất kỳ unit nào; bộ tài liệu này xem được ngay trong app (tab Kế hoạch). Chi tiết ở file 05; việc còn lại
tick ở file 04.

**Đợt 3 (05/10/2026):** công cụ `agents/lesson_video` dựng video bài giảng từ kịch bản hai người nói (giọng Flite miễn
phí); hai video Unit 1 Speaking 1 và 2 gắn vào Unit 1 trong tab Sách.

**Đợt 4 (05/10/2026):** video đọc bằng giọng Kokoro-82M (bản q8) — Emma `af_heart`, Tom `am_michael` (giọng Mỹ, người dùng chọn qua video mẫu); Flite giữ làm dự phòng.

**Đợt 5 (06/10/2026):** thêm hai video Unit 1 Writing 1 và 2, mỗi video có thư mẫu đọc thành tiếng.

**Đợt 6 (06/10/2026):** video Unit 1 Writing 3 (giải bài A, B, C, thư mẫu); Workbook chưa có trong bộ sách nên chưa giải đề Workbook trang 6.

**Đợt 7 (06/10/2026):** video Unit 1 Vocabulary 1–3 (đáp án và thêm ví dụ); thẻ unit hiện mục lục video theo từng phần.

**Đợt 8 (06/10/2026):** sửa nút phóng to / thu nhỏ của trình xem trang sách (50%–300%, nhãn mức phóng, phím tắt).

**Đợt 9 (06/10/2026):** video Unit 1 Consolidation, Exam practice Listening và Reading — Unit 1 có 9 video; hồ sơ
video bài giảng (file 06) làm căn cứ cho Unit 2.

**Đợt 10 (06/10/2026):** 12 video Unit 2 cho mọi phần có trang sách, lần đầu phát file nghe của sách trong video
(Listening) và tô từ khóa khi dạy dò tìm (Reading); hồ sơ video (file 06) thêm Unit 2 và kế hoạch Unit 3.

**Đợt 11 (06/10/2026):** video Unit 1 Listening và Reading — Unit 1 (13 video) và Unit 2 (12 video) đủ video cho
mọi phần có trang trong Course Book; bỏ Workbook (bộ sách không có), chỉ làm Course Book.

**Đợt 12 (07/10/2026):** 11 video Unit 3 — Unit 1–3 đủ video cho mọi phần có trang trong Course Book (36 video);
hồ sơ video (file 06) thêm Unit 3 và kế hoạch Unit 4.

**Đợt 13 (07/10/2026):** nghe / xem lặp lại trong tab Sách:
- lặp một bài hoặc cả danh sách;
- hẹn giờ dừng;
- đếm thời gian nghe trong ngày;
- lặp đoạn A–B và lặp chương trên video.

**Đợt 14 (19/10/2026):** 4 video luyện nói thêm cho Unit 1 (khoảng 35 phút, 115 cặp hỏi – đáp):
- Tom và Emma hỏi đáp qua lại về các chủ đề của Unit 1;
- 4 buổi thi thử Speaking, hai người thay nhau làm giám khảo;
- không có khoảng lặng chờ, người học tự tạm dừng video để nói.

Công cụ dựng video có thêm cảnh `shadow` và dòng `echo` (khoảng lặng để nhắc lại).

**Đợt 15 (25/10/2026):** lộ trình **tiếng Nhật JLPT N5** với GENKI I (3rd Edition) trong tab Sách:
- 78 phiên, mỗi phiên mở đúng trang Textbook / Workbook và đúng track audio của phần đó;
- 15 video bài 1–5, dựng lại từ bản thiết kế "Genki I × IELTS Target 5.0" sau khi đánh giá và sửa nội dung;
- công cụ dựng video đọc được tiếng Nhật (giọng `jf_alpha`, furigana, tự kiểm tra cách đọc). Chi tiết ở file 07.

**Đợt 16 (25/10/2026):** GENKI bài 1–3 có **12 video 5–10 phút**, mỗi bài bốn video, thay cho 9 tập ngắn cũ:
- Speaking và Writing làm trước, rồi Listening (phát audio hội thoại gốc của sách) và Reading (bài tập 読み書き);
- mỗi video gắn vào đúng phiên luyện kỹ năng đó: Hội thoại & từ vựng, Part B, Part C, Đọc – viết;
- cảnh tiếng Nhật có nhiều thẻ, phát được file nghe của sách và có thẻ đố. Lệnh `prune` bỏ video không còn kịch bản.

**Đợt 17 (26/10/2026):** Unit 0 của GENKI có **5 video** để người chưa biết gì tiếng Nhật học không cần mở sách:
- phiên Hệ chữ: Hiragana 1 (46 chữ), Hiragana 2 (゛゜, âm ghép, っ, trường âm), Katakana & chữ Hán;
- phiên Chào hỏi & số đếm: Greetings, Numbers;
- video có đủ bảng chữ, mẹo phát âm cho người Việt, audio gốc của sách và bài đố có đáp án;
- thẻ tiếng Nhật xuống dòng được bằng `\n`, nên bảng chữ hiện thành bảng như trong sách.

**Đợt 18 (26/10/2026):** **Giai đoạn 0** cho người học lại từ đầu hoặc dưới band 3.0, đứng trước tuần 1 trong nhóm IELTS:
- English Unlimited A2 Elementary: 79 phiên (16 tuần), mỗi phiên mở đúng trang Coursebook, track audio và trang đáp án
  Teacher's Book;
- sau Unit 4, 9, 14 có một phiên ôn với bài nghe Achievement test; cuối sách là đề mẫu A2 Key để quyết định sang
  Giai đoạn 1;
- thẻ A1 Starter đứng trước, chờ Coursebook đầy đủ. Chi tiết ở file 08.

## Tóm tắt trong năm dòng

1. **Sửa trước khi xây:** tầng đồng bộ hiện tại có lỗi trộn dữ liệu giữa người chưa đặt tên và
   mất thay đổi khi hai máy cùng ghi (B1–B3) — sửa ở Giai đoạn 0, trước khi thêm dữ liệu sách.
2. **Pipeline nhập sách** là CLI Python chạy trên máy cá nhân, mỗi bước một file kết quả (chạy
   tiếp được), AI chỉ ở bước đọc mục lục và nghe audio không tên; LangGraph bọc lại ở Giai đoạn 4.
3. **App** giữ nguyên kiến trúc một file JS thuần, thêm tab Sách và màn hình Phiên học; file sách
   nằm trong IndexedDB của trình duyệt, tiến độ đồng bộ ở tài liệu riêng.
4. **Chế độ không gói** cho phép học Target 5.0 đúng lịch từ tuần 6 ngay cả khi pipeline chưa xong.
5. **Bản quyền:** repo chỉ có code, schema, skill; `.gitignore` và CI chặn file sách từ ngày đầu.

## Việc làm ngay

1. Đọc mục 2 file 03 và chốt D1–D10 (hoặc đồng ý mặc định).
2. Báo người học đang ở tuần mấy để chọn thứ tự ở mục 3 file 03.
3. Khi có script inventory (P0-15), chạy trên máy có bộ sách và gửi kết quả — kết quả không chứa nội dung sách.
