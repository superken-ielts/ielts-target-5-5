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
