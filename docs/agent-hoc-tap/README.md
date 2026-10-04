# Hệ thống agent học tập — kế hoạch triển khai

Kế hoạch hiện thực hóa technical summary *"Hệ thống agent học tập: từ sách đến app học"*
(04/10/2026) trên mã nguồn hiện có của repo: biến bộ IELTS Target 5.0 (PDF + MP3) thành
menu sách và phiên học trong app, rồi dùng lại cho sách khác và các agent sau.

Thư mục này là tài liệu kỹ thuật, `web/build.py` không nhúng nó vào app học.

| File | Nội dung |
|---|---|
| [01-review-code-hien-tai.md](01-review-code-hien-tai.md) | Kiến trúc app hiện tại, điểm tích hợp, 10 lỗi và rủi ro (B1–B10), ràng buộc kỹ thuật |
| [02-kien-truc-va-hop-dong-du-lieu.md](02-kien-truc-va-hop-dong-du-lieu.md) | Cấu trúc thư mục, schema `book.yaml` / `book.json` / `plan.json` / `review.json` / tiến độ, thuật toán từng bước nhập sách, thiết kế tích hợp từng tab |
| [03-ke-hoach-trien-khai.md](03-ke-hoach-trien-khai.md) | 10 quyết định cần chốt, đường găng theo tuần học, 5 giai đoạn với spike và cổng kiểm tra, chiến lược test, rủi ro |
| [04-checklist.md](04-checklist.md) | Checklist từng task (P0-01 … P4-07) kèm điều kiện đạt và cổng G0–G4 |
| [05-lich-su-thay-doi.md](05-lich-su-thay-doi.md) | Lịch sử từng đợt triển khai: file thêm/sửa/xóa, chỗ làm khác plan, kết quả kiểm thử, việc còn treo |

## Trạng thái

**Đợt 1 (04/10/2026):** agent nhập sách `agents/book_ingest` đã chạy trên IELTS Target 5.0 (120 phiên, 59 track,
27 đoạn PDF) và app có tab **Sách** để học theo lộ trình. Chi tiết ở file 05; việc còn lại tick ở file 04.

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
