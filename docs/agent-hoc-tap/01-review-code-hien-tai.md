# 01 — Review mã nguồn hiện tại

Đã đọc `web/app.template.html` (3.625 dòng: toàn bộ HTML và JS, lướt phần CSS và hằng số
nội dung), `web/build.py`, cấu trúc `web/phase1-days.json` và danh mục markdown trước khi lập
kế hoạch. Mục đích: biết chỗ nào giữ nguyên, chỗ nào phải
sửa trước khi gắn hệ thống sách vào, và chỗ nào là điểm tích hợp.

Số dòng trong file này tính theo commit `b7be8f5`.

## 1. Kiến trúc hiện tại trong một trang

| Thành phần | Hiện trạng |
|---|---|
| Mã nguồn | Một file `web/app.template.html`: CSS (dòng 6–531), HTML 7 tab (531–1006), JS thuần không thư viện (1006–3625) |
| Dựng | `web/build.py` nhúng mọi file `.md` và `phase1-days.json` vào hai chỗ đánh dấu, xuất `ielts-companion.html` (Claude Artifact) và `index.html` (tự host) |
| Dữ liệu lộ trình | Hằng số trong JS: `PHASES`, `W` (40 tuần), `LPLAN`, `RPLAN`, `GRAM`, `ROTA`, `ROTA1`, `CUES1/2`, `RES` |
| Trạng thái | Một object `S` (`DEF()` dòng 1448): `startDate, blocks, hours, vocab, shortDays, dayDone, mocks, errors, sessions, essays` |
| Lưu trữ | `localStorage` theo slug học viên + capability `db`: `students/<slug>/progress/main`, `students/<slug>/essays/<id>`, `roster/<slug>` |
| AI | Capability `sample` cho công cụ chấm Writing (`buildPrompt()` dòng 3487, đọc điểm bằng regex `parseBand()` dòng 3446) |
| Hiển thị | Dựng DOM thủ công, `renderAll()` (dòng 2182) vẽ lại toàn bộ khi trạng thái đổi |
| Bản tự host | Không có `window.claude` → tự ẩn chấm bài, chỉ lưu `localStorage` |

## 2. Điểm mạnh nên giữ

- **Không phụ thuộc thư viện, một file HTML.** Dễ đăng lên Artifact, dễ tự host, chạy ngoại tuyến sau lần tải đầu.
- **An toàn XSS ở phần dữ liệu người dùng.** Mọi chỗ hiện dữ liệu người nhập đều dùng `textContent`; `innerHTML` chỉ dùng cho icon cố định và markdown của chính repo.
- **Build tái lập được.** Đã chạy lại `python3 web/build.py` trên một bản sao repo: hai file đầu ra trùng khớp với bản đã commit (`git status` sạch).
- **Một nguồn dữ liệu cho giáo án ngày.** `phase1-days.json` sinh cả bản web lẫn `01a-…md`, không bao giờ lệch.
- **Hạ cấp có kiểm soát.** Thiếu capability thì ẩn tính năng, không vỡ trang.

Hệ thống sách sẽ giữ đúng các nguyên tắc này: JS thuần, dữ liệu người dùng chỉ qua
`textContent`, build tái lập được, hai bản dựng đều chạy.

## 3. Điểm tích hợp cho hệ thống sách

| Chỗ trong mã | Dòng | Thay đổi khi có sách |
|---|---|---|
| Nav + panel `p-res` (tab Tài liệu) | 834, 999 | Đổi thành tab **Sách**: phân đoạn "Sách của tôi" và "Tài liệu miễn phí" — giữ đủ 7 tab trên điện thoại |
| `todayBlocks()` | 1653 | Thêm chế độ sách cho tuần có phiên Target 5.0: 75′ phiên + 30′ nói + 15′ từ vựng; ngày bận 30′ + 15′ + 15′ |
| `renderToday()` | 1789 | Block phiên sách có nút "Mở phiên"; tự tick khi phiên kết thúc |
| `W` (40 tuần) | 1019 | Tuần 6–25 ghi rõ unit Target 5.0; tuần 19 và 26 đổi mock sang Target Test 2 và Cambridge 20 GT Test 1 |
| `renderRoadmap()` | 1968 | Hiện unit dự kiến theo `plan.json` cho tuần 6–25 |
| `renderSkillGrid()` / `openSkill()` | 2202, 2224 | Lối tắt tới phiên Listening/Reading của unit đang học |
| `logSession()` | 2328 | Thêm trường `src:"book"` và `ref` (phiên nào, câu nào) |
| Thêm lỗi vào sổ (`erAdd`) | 3310 | Tách thành hàm `addError({k,a,b,n,ref})` để phiếu trả lời gọi lại |
| `buildPrompt()` + `gRun` | 3487, 3521 | Tách thành `gradeWriting({text,type,context})` dùng chung cho tab Luyện tập và phiên Writing |
| `renderProgress()` | 2115 | Thẻ Target 5.0: phiên đã xong, dự kiến tuần xong, gợi ý rút gọn |
| `exportBundle()` / nhập JSON | 3138, 3206 | Thêm tiến độ sách (không kèm file sách), nâng `schema` lên 3 |
| `wipeStudent()` / `btnReset` | 2610, 3372 | Xóa cả tài liệu tiến độ sách trên máy chủ |
| `boot()` | 3571 | Tách `connectSync()`, đăng ký thêm tài liệu tiến độ sách |
| `build.py` | 51, `main()` | Nhúng thêm `web/src/**` và thư viện vendor (PDF.js, fflate) |

## 4. Lỗi và rủi ro cần xử lý

Thứ tự theo mức độ. Bốn lỗi đầu phải sửa ở Giai đoạn 0, trước khi thêm bất kỳ dữ liệu
mới nào vào đồng bộ, vì hệ thống sách sẽ dựa vào đúng tầng đồng bộ này.

### B1 — Cao: đồng bộ gắn cứng vào slug lúc mở trang, gốc `mac-dinh` dùng chung giữa người lạ

Vị trí: `rootSlug()` dòng 1468, `boot()` dòng 3571–3622.

- Người mới mở trang chưa đặt tên → `rootSlug()` trả `"mac-dinh"` → `boot()` đọc
  `students/mac-dinh/progress/main`. Nếu tài liệu chưa có, `boot()` tự rước bản cũ
  `progress/main` (dòng 3598) sang đó; nếu vẫn chưa có, nó tạo mới. Người chưa đặt tên
  nào tick một ô cũng ghi vào đúng gốc này.
- Người tiếp theo mở trang: `remoteCount >= localCount` (dòng 3609) là `0 >= 0`, nên toàn
  bộ trạng thái của người trước được nạp. Màn đặt tên báo "Đã thấy dữ liệu học từ trước"
  và chuyển hết sang tên của người mới.
- Sau khi đặt tên hoặc đổi tên, `onSnapshot` (dòng 3617) vẫn nghe tài liệu của slug cũ.
  Khi ai đó ghi vào `mac-dinh`, callback thay toàn bộ `S` bằng dữ liệu đó rồi lưu vào gốc
  của mình. Đồng thời thay đổi từ thiết bị khác của chính mình không về cho tới khi tải lại.

Sửa: tách `connectSync(slug)`; chỉ đọc/ghi máy chủ khi đã có slug thật; giữ hàm hủy của
`onSnapshot` và đăng ký lại khi `applyProfile()` đổi slug; bỏ việc tự rước `progress/main`
(hoặc chỉ làm khi người dùng bấm "Nhận dữ liệu bản cũ").

### B2 — Trung bình: hợp nhất đồng bộ chọn nguyên khối theo số ô tick

Vị trí: dòng 3606–3610 và 3617–3620.

Khi mở trang, bản nào có nhiều `blocks + hours` hơn thì thắng nguyên khối. Buổi luyện,
bài viết, sổ lỗi, điểm thi thử ghi lúc ngoại tuyến ở thiết bị có ít ô tick hơn sẽ mất.
Sổ lỗi không có `id` và bị xóa bằng `splice` (dòng 2172), nên không thể hợp nhất đúng.

Sửa: `mergeState(local, remote)` theo từng trường — map hợp theo khóa, mảng hợp theo
`id`; thêm `id` cho `errors` và `mocks`; nút "Đã xử lý" đánh dấu `done` thay vì xóa.

### B3 — Trung bình: thay đổi cục bộ bị ghi đè trong cửa sổ 900 ms

Vị trí: `save()` dòng 1534–1543, `onSnapshot` dòng 3617.

`save()` hoãn ghi 900 ms. Nếu trong lúc đó có snapshot từ thiết bị khác, callback thay
`S`, rồi lệnh ghi đang chờ đẩy lên bản đã bị thay — cú tick vừa rồi mất. Cờ
`hasPendingWrites` chỉ biết những lệnh đã gửi đi.

Sửa: khi `saveTimer` đang chờ thì hợp nhất bằng `mergeState()` thay vì thay thế.

### B4 — Trung bình: tài liệu tiến độ không có trần, lỗi vượt cỡ bị nuốt

Vị trí: `DEF()` dòng 1448, `logSession()` dòng 2330, `save()` dòng 1541.

Một tài liệu `db` tối đa 256 KiB. `errors`, `blocks`, `hours`, `dayDone` không giới hạn,
`sessions` giữ tới 800 mục. Khi ghi lỗi, trang chỉ hiện "Lưu trên máy này" — người dùng
tưởng vẫn ổn. Nhét tiến độ sách vào `S` sẽ đẩy nhanh tới trần.

Sửa: tiến độ sách nằm ở tài liệu riêng; đo kích thước JSON trước khi ghi, cảnh báo từ
200 KiB; hiện lỗi thật khi máy chủ từ chối.

### B5 — Thấp: đồng hồ chạy chậm khi khóa màn hình

Vị trí: `countdown()` dòng 3066, đồng hồ Speaking dòng 3413.

Đồng hồ trừ dần mỗi giây bằng `setInterval`. Khi khóa màn hình hoặc chuyển app, trình
duyệt bóp interval nên đồng hồ chạy chậm hoặc đứng. Phiên 75 phút của hệ thống sách
không chấp nhận được điều này.

Sửa: lưu mốc `endsAt`, mỗi lần vẽ tính `endsAt - Date.now()`; với phiên học thì lưu cả
mốc bắt đầu vào tiến độ để mở lại vẫn đúng.

### B6 — Thấp: nhập JSON không chuẩn hóa ngày bắt đầu

Vị trí: nhập JSON dòng 3223, `weekHours()` dòng 1779.

File nhập vào có `startDate` không phải thứ Hai thì được giữ nguyên. `weekNo()` dùng
`mondayOf()` còn `weekHours()` dùng ngày thô, nên giờ học bị cộng lệch tuần.

Sửa: chuẩn hóa về thứ Hai lúc nhập; `weekHours()` dùng `mondayOf()`.

### B7 — Thấp: nhập JSON không đẩy bài viết lên máy chủ

Vị trí: dòng 3229–3231. `essayBodies` chỉ ghi vào `localStorage`, nên thiết bị khác không
mở lại được nội dung bài viết đã nhập. Sửa: đẩy từng bài lên `students/<slug>/essays/<id>`.

### B8 — Thấp: hai cách hiện tổng giờ tuần

Dòng 1841 dùng `toFixed`, dòng 3268 dùng `toString` — có thể ra `7.300000000000001`.
Sửa: dùng chung một hàm định dạng.

### B9 — Rủi ro đã biết: chưa phân quyền

Ai mở được trang thì đọc và xóa được dữ liệu của mọi người (`web/README.md` ghi rõ đây là
lựa chọn có chủ đích). Tiến độ sách nhạy cảm hơn, nên ở bản đầu: không đưa vào `roster`
và tab Lịch sử; muốn riêng tư thật phải chuyển dữ liệu cá nhân sang `data/users/<id>/`
(xem quyết định D7 trong file 03).

### B10 — Vệ sinh repo

- Không có `.gitignore`; `.DS_Store` đã bị commit. Khi bắt đầu xử lý sách, một
  `git add .` nhầm là đẩy cả PDF và MP3 có bản quyền lên repo public.
- Không có test, không có CI. Build tái lập được nhưng không có gì kiểm tra điều đó.
- Chưa có `CLAUDE.md` mô tả quy ước repo (sửa template rồi chạy build, file sinh tự động).

## 5. Ràng buộc kỹ thuật hệ thống sách phải tính tới

| Ràng buộc | Hệ quả cho thiết kế |
|---|---|
| Tài liệu `db` tối đa 256 KiB | Tiến độ sách tách tài liệu riêng; câu trả lời mỗi phiên là tài liệu con |
| Capability `assets` không nhận audio, và mọi người mở được artifact đều đọc được | Không dùng `assets` cho sách — đúng như technical summary đề xuất. File sách nằm trong IndexedDB của từng trình duyệt |
| Danh sách capability của tài khoản hiện chưa có micro | Ghi âm Speaking trong artifact nhiều khả năng không chạy; phải thử ở Giai đoạn 0. Ghi âm đầy đủ dự kiến ở bản tự host |
| Script ngoài chỉ được tải từ một số CDN; Worker khác origin bị chặn | PDF.js và worker nên vendor vào build, tạo worker từ Blob — xác nhận bằng spike |
| Safari iOS giới hạn bộ nhớ canvas và có thể xóa dữ liệu web | Cắt PDF theo đoạn nhỏ, giới hạn độ phân giải khi vẽ; luôn giữ gói sách gốc để nhập lại |
| Trình duyệt bóp `setInterval` khi chạy nền | Mọi đồng hồ tính theo mốc thời gian (B5) |
| Trang render lại toàn bộ bằng `renderAll()` | Màn hình Phiên học không được nằm trong vòng render chung — PDF và audio phải sống độc lập, nếu không mỗi lần lưu là vẽ lại PDF |
