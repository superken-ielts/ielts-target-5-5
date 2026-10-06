# Bản web — Bạn đồng hành IELTS

Trang web đi kèm bộ kế hoạch, dùng để học trên điện thoại. Một file HTML duy nhất,
không cần server, không phụ thuộc thư viện ngoài. Toàn bộ 16 file markdown của lộ
trình được nhúng thẳng vào trang, nên đọc được cả kế hoạch mà không cần mở máy tính.

## Trang có gì

| Tab | Nội dung |
|---|---|
| **Hôm nay** | Bốn block của ngày hôm nay với nội dung cụ thể theo đúng tuần đang học, có ô đánh dấu hoàn thành. Nút chuyển sang khung rút gọn cho ngày bận chỉ có 1 tiếng (ẩn vào Chủ nhật vì Chủ nhật cố định 1 tiếng). Khối **Chi tiết ngày hôm nay** mở ra đủ năm phần kèm link bài học. Nút **Hoàn thành hôm nay** để chốt ngày, và màn chặn buộc đóng sổ những ngày cũ còn treo trước khi sang ngày mới. |
| **Lộ trình** | Toàn bộ 40 tuần, nhóm theo 4 giai đoạn, tuần hiện tại được đánh dấu. Chạm vào một tuần để xem trọng tâm của cả 4 kỹ năng và các mốc kiểm tra theo tháng. |
| **Sách** | Danh sách sách của lộ trình kèm trình độ, thời lượng, số tháng học xong theo nhịp. Chạm một sách để xem mọi section, unit và chọn học unit bất kỳ (hoặc theo thứ tự lộ trình). Mỗi phiên mở đúng trang sách (PDF), đáp án, tapescript, phát audio có ±5 giây, tốc độ, lặp A–B, video bài giảng (Unit 1: Speaking 1–2, Vocabulary 1–3, Writing 1–3 — thẻ unit xếp video theo từng phần), đồng hồ 75 phút, ghi lỗi vào sổ lỗi, và cộng giờ học khi xong. Xem mục *Tab Sách* bên dưới. |
| **Luyện tập** | Bốn kỹ năng tách riêng, chọn kỹ năng nào thì vào thẳng phần luyện của kỹ năng đó. Nội dung lấy theo đúng tuần đang học. Mỗi buổi luyện đều ghi được kết quả vào lịch sử. |
| **Tài liệu** | Danh sách tài liệu miễn phí bên ngoài, bấm là mở. |
| **Kế hoạch** | Toàn bộ 16 file markdown, đọc ngay trong trang. Có mục lục cho từng tài liệu, tìm kiếm không dấu trên toàn bộ nội dung, và liên kết giữa các tài liệu bấm được. |
| **Tiến độ** | Biểu đồ giờ học 12 tuần gần nhất, bảng điểm thi thử, sổ lỗi, và xuất/nhập toàn bộ lịch sử ra file JSON. |
| **Lịch sử** | Mọi học viên đang học trên trang, lọc theo tên (không cần dấu) và sắp theo lần học gần nhất, số giờ hoặc tên. Chạm một người để mở lịch sử đầy đủ của họ. Hiện chưa phân quyền — xem mục dưới. |

### Bên trong tab Luyện tập

| Kỹ năng | Có gì |
|---|---|
| **Listening** | Nguồn nghe của đúng tuần đó kèm link mở thẳng, quy trình 4 lượt có ô đánh dấu từng lượt, đồng hồ chép chính tả 10 phút, và ô ghi số câu đúng. |
| **Reading** | Dạng bài của tuần, bảng phân bổ 15/17/23 phút cho ba section General Training, đồng hồ đếm ngược có sẵn bốn mốc, và ô ghi số câu đúng kèm thời gian thực tế. |
| **Writing** | Công cụ chấm bài bằng AI, ô lưu điểm vào lịch sử, và danh sách bài đã chấm — bấm vào một bài cũ để đọc lại bài viết và nhận xét. |
| **Speaking** | Ngân hàng đề Part 1 và Part 2, đồng hồ tự chuyển từ 1 phút chuẩn bị sang 2 phút nói, và ô ghi số giây nói được cùng số lần dừng quá 3 giây. |

Mỗi kỹ năng có đường biểu diễn tiến bộ của 14 buổi gần nhất, hiện ra khi đã ghi đủ
3 buổi.

### Dữ liệu được lưu ở đâu

Mọi thứ nằm dưới **gốc mang tên học viên**. Tên được chuyển thành slug không dấu —
"Nguyễn Văn Đức" thành `nguyen-van-duc` — và slug đó là thư mục gốc của toàn bộ dữ liệu:

| Loại | Nơi lưu | Lý do |
|---|---|---|
| Tiến độ, giờ học, ngày đã chốt, buổi luyện, điểm bài viết, sổ lỗi | `students/<slug>/progress/main` | Nhỏ gọn, đồng bộ tức thì giữa các thiết bị |
| Nội dung bài viết và nhận xét đầy đủ | `students/<slug>/essays/<id>`, mỗi bài một tài liệu | Một tài liệu tối đa 256KB, mà mỗi bài kèm nhận xét đã khoảng 4KB — gộp chung sẽ tràn sau vài chục bài |
| Bản sao cục bộ | `localStorage`, khóa `ielts-gt-40w-v1:<slug>` | Để trang hiện ngay lúc mở, không phải chờ mạng |
| Hồ sơ học viên | `localStorage`, khóa `ielts-gt-40w-v1:profile` | Con trỏ tới gốc đang dùng, không nằm trong gốc nào |
| Danh bạ học viên | `roster/<slug>`, mỗi người một dòng tóm tắt | Xem mục dưới |

Nhờ vậy hai người dùng chung một máy hoặc một tài khoản sẽ không đè lên nhau. Đổi tên
học viên sẽ tạo gốc mới và chuyển toàn bộ tiến độ hiện tại sang đó, có hỏi xác nhận.

File JSON xuất ra mang tên `ielts-<slug>-<ngày>.json` và có trường `student` ghi rõ của
ai, nên gom nhiều file của nhiều người vẫn phân biệt được.

### Vì sao cần danh bạ `roster/`

Tiến độ nằm ở `students/<slug>/progress/main`. Một tài liệu nằm sâu như vậy chỉ đọc được
khi đã biết slug — kho dữ liệu không cho liệt kê `students/` từ bên ngoài. Nên mỗi người,
mỗi lần lưu, tự ghi một dòng tóm tắt vào `roster/<slug>`: tên, ngày bắt đầu, tổng giờ, số
ngày đã chốt, số buổi luyện, điểm thi thử gần nhất và ngày học gần nhất. Tab **Lịch sử**
liệt kê đúng bộ sưu tập đó, rồi chỉ khi bấm vào một người mới mở tiến độ đầy đủ của họ.

Hệ quả: một học viên chỉ xuất hiện trong danh sách **sau lần đầu họ mở trang** kể từ khi
có tính năng này. Trang cũng giữ một bản danh bạ trong `localStorage` để bản tự host —
vốn không có kho chung — vẫn liệt kê được những người đã dùng chính trình duyệt đó.

**Chưa phân quyền.** Ai mở được trang thì xem được lịch sử của tất cả mọi người, kể cả
bài viết đã chấm và sổ lỗi. Đây là lựa chọn có chủ đích ở thời điểm hiện tại, không phải
sơ suất. Muốn siết lại thì khai báo `rules` cho capability `db` lúc đăng bản mới — ví dụ
để `roster` ai cũng đọc được nhưng `students/` thì chỉ chủ sở hữu, hoặc chuyển hẳn dữ
liệu cá nhân xuống `data/users/<id>/` để mỗi người chỉ thấy phần của mình.

Nút **Tải file JSON** ở tab Tiến độ gom tất cả lại thành một file duy nhất, gồm cả
nội dung bài viết. Nút **Nhập lại** đọc ngược file đó về — dùng khi đổi máy, hoặc khi
muốn quay lại một bản sao lưu cũ.

### Hai mức xóa

| Nút | Ở đâu | Xóa gì | Giữ gì |
|---|---|---|---|
| **Xóa toàn bộ tiến độ** | Tiến độ → Thiết lập khác | Ngày đã chốt, giờ học, từ vựng, buổi luyện, điểm thi thử, sổ lỗi, danh sách bài viết | Tên học viên, ngày bắt đầu, phần chữ của các bài viết cũ, dòng trong tab Lịch sử (về 0) |
| **Xóa hẳn học viên** | Tiến độ → Học viên, và trong từng người ở tab Lịch sử | Tất cả những thứ trên, cộng hồ sơ, toàn bộ nội dung bài viết kèm nhận xét, và dòng trong danh bạ — cả `localStorage` lẫn `students/<slug>/…` và `roster/<slug>` trên máy chủ | Không gì cả |

Mức thứ hai bắt **gõ đúng tên học viên** mới mở khóa nút xóa, và mời tải file JSON về
trước. Nó cũng dọn luôn những bài viết mồ côi — phần chữ còn sót lại sau một lần xóa
tiến độ trước đó, vốn không còn đường nào mở lại trong trang.

Xóa chính mình thì trang quay về màn đặt tên như lần đầu mở. Xóa người khác từ tab Lịch
sử thì chỉ dòng của họ biến mất; nếu chính họ mở lại trang trên máy của họ, bản sao cục
bộ bên đó sẽ dựng lại dòng danh bạ — trang có ghi rõ điều này ngay tại nút xóa.

Lưu ý cho bản đăng trên Claude: **xóa dữ liệu duyệt web của trình duyệt là vô ích**, vì
mở lại trang là bản trên máy chủ tự tải xuống. Phải dùng đúng nút trong trang.

## Tab Sách

Dữ liệu sách do agent nhập sách sinh ra (`agents/`, xem `agents/README.md`): `books/<sách>/book.json`
và `plan.json`. `books/catalog.json` ghi thứ tự 5 sách của lộ trình 40 tuần, kể cả sách chưa nhập.
`build.py` nhúng các file này vào trang, nên danh sách sách, chi tiết unit và lộ trình chạy ở mọi bản dựng.
Checklist và lịch sử triển khai agent (`docs/agent-hoc-tap/`) cũng được nhúng, xem ở tab Kế hoạch.
Mã của tab nằm ở `web/src/book/` (`core.js` hàm thuần, `ui.js` giao diện, `book.css`), cũng được nhúng.

File sách (PDF, MP3) thì không nhúng — trang lấy theo thứ tự:

1. File đã **nhập vào trình duyệt** (tab Sách → Quản lý file sách → Nhập file sách từ máy, lưu IndexedDB).
2. File trên **máy chủ** cạnh trang: `../books/<sách>/…` — bản tự host từ gốc repo (GitHub Pages, hoặc
   `python3 web/serve.py` rồi mở `http://localhost:8000/web/index.html`).

Course Book 100 MB được agent cắt thành các đoạn nhỏ theo unit trong `books/<sách>/web/`; trang chỉ tải
đoạn chứa trang đang xem (vài MB). Trình xem phóng to / thu nhỏ từ 50% tới 300% (nút − % +, phím `+` `-` `0`).
Trình xem PDF dùng PDF.js 4.10.38 trong `web/vendor/pdfjs/`, tải lười
lúc mở trang sách; không có thì lấy cùng phiên bản trên cdn.jsdelivr.net.

Tiến độ sách lưu riêng, không đụng tiến độ cũ: `localStorage` khóa `ielts-gt-40w-v1:<slug>:book:<id>` và
`students/<slug>/books/<id>` trên máy chủ (đồng bộ khi mở tab Sách). Tab Lịch sử không hiện tiến độ sách.

Bản trên Claude không truy cập được thư mục `books/`: phải nhập file từ máy (các MP3, `Target5.0_Listening_R.pdf`
và các đoạn trong `books/ielts_target_5_0/web/`). Việc đọc PDF trong bản Claude phụ thuộc chính sách nạp script
của nền tảng — chưa kiểm tra được (spike S0.2 trong `docs/agent-hoc-tap/03`).

**Video bài giảng.** `books/<sách>/lessons/lessons.json` (do `agents/lesson_video` sinh) cũng được nhúng. Thẻ unit có
nút mở từng video; trong phiên học, hoạt động có video hiện trình phát kèm nút nhảy theo chương. File MP4 (H.264 + AAC)
lấy từ máy chủ như PDF (`../books/<sách>/lessons/…`), nên chỉ xem được ở bản tự host; trình duyệt cần phát được
MP4 H.264 (Chrome, Edge, Safari, Firefox — Chromium trần của Playwright thì không, trang sẽ báo).

## Ba file, ba vai trò

| File | Vai trò |
|---|---|
| `app.template.html` | **Bản nguồn giao diện và mã — file cần sửa khi đổi cách trang hoạt động.** Có các chỗ đánh dấu cho build chèn dữ liệu: `/*__DOCS__*/{}` cho nội dung markdown, `/*__P1DAYS__*/{...}` cho giáo án ngày, `/*__BOOKS__*/{}` cho dữ liệu sách, `/*__BOOK_JS__*/` và `/*__BOOK_CSS__*/` cho mã tab Sách. |
| `src/book/` | Mã tab Sách: `core.js` (hàm thuần, có test ở `tests/web/`), `ui.js`, `book.css`. |
| `vendor/pdfjs/` | PDF.js 4.10.38 (Apache-2.0), tải lười khi mở trang sách. |
| `serve.py` | Máy chủ chạy thử có hỗ trợ HTTP Range — `python3 -m http.server` không có, PDF.js sẽ phải tải trọn file. |
| `phase1-days.json` | **Nguồn duy nhất của giáo án từng ngày giai đoạn 1** — 12 tuần × 6 ngày, cộng phần Chủ nhật. Sửa nội dung học ở đây. |
| `build.py` | Đọc `phase1-days.json`, sinh ra file markdown giáo án, gom mọi file `.md` (trừ `docs/`, `agents/`, `.claude/`, `books/`, `vendor/`), gom `books/*/book.json` + `plan.json` và mã tab Sách, nhúng tất cả vào bản nguồn, rồi xuất hai file dưới. |
| `ielts-companion.html` | Bản dựng để đăng lên Claude Artifact. Không có thẻ `<!doctype>`/`<html>`/`<head>`/`<body>` vì nền tảng tự bọc. **Sinh ra tự động, đừng sửa tay.** |
| `index.html` | Bản dựng standalone để tự host hoặc mở trực tiếp bằng trình duyệt. **Sinh ra tự động, đừng sửa tay.** |
| `../01a-giao-an-tung-ngay-giai-doan-1.md` | Bản markdown của giáo án ngày. **Sinh ra tự động từ file JSON, đừng sửa tay.** |

Vì giáo án ngày chỉ có một nguồn là file JSON, bản web và bản markdown không bao giờ
lệch nhau. Sửa một chỗ, chạy build, cả hai đổi theo.

Chạy lại build sau **mỗi lần sửa `app.template.html` hoặc sửa bất kỳ file `.md` nào**:

```bash
cd /Users/duc.nguyen/data/projects/success/motives/motivesidp-ai-learning/ielts-target-5-5
python3 web/build.py
```

Vì sao phải nhúng markdown vào thay vì để trang tự tải file: trang chạy dưới một CSP
chặt, mọi yêu cầu ra ngoài đều bị chặn. Muốn đọc tài liệu ngay trong trang thì nội
dung phải nằm sẵn trong HTML tại thời điểm dựng. Đổi lại, trang nặng khoảng 440KB —
tải một lần rồi chạy hoàn toàn ngoại tuyến.

Khác biệt về tính năng giữa hai bản dựng:

| Tính năng | Bản Claude Artifact | Bản tự host |
|---|---|---|
| Toàn bộ lộ trình, checklist, đồng hồ, tài liệu | Có | Có |
| Đọc 16 file kế hoạch, mục lục, tìm kiếm không dấu | Có | Có |
| Lưu tiến độ | Có | Có |
| **Đồng bộ tiến độ giữa điện thoại và máy tính** | Có | Không — mỗi trình duyệt lưu riêng |
| **Chấm bài Writing bằng AI** | Có | Không — trang tự ẩn mục này và chỉ sang Write & Improve |

Nếu chỉ dùng một bản, dùng bản Claude Artifact: nó có đủ tính năng và không cần
thiết lập gì. Bản tự host là phương án dự phòng, và là cách để giữ trang này kể cả
khi không dùng Claude nữa.

---

## Cách deploy miễn phí

Cả ba cách dưới đây đều miễn phí vĩnh viễn cho trang tĩnh, đều có HTTPS sẵn, và đều
truy cập tốt từ Việt Nam. Chỉ cần chọn một.

### Cách 1 — Cloudflare Pages (khuyến nghị)

Nhanh nhất khi truy cập từ Việt Nam vì Cloudflare có máy chủ đặt trong nước. Không
cần tài khoản GitHub.

1. Tạo tài khoản miễn phí tại [dash.cloudflare.com](https://dash.cloudflare.com)
2. Vào **Workers & Pages** → **Create** → **Pages** → **Upload assets**
3. Đặt tên dự án, ví dụ `ielts`
4. Kéo thả **riêng file `index.html`** vào (không kéo cả thư mục)
5. Bấm **Deploy**

Trang sẽ có địa chỉ dạng `https://ielts.pages.dev`. Muốn cập nhật thì vào lại dự án,
chọn **Create new deployment** và tải file mới lên.

### Cách 2 — GitHub Pages

Phù hợp nếu đã có sẵn tài khoản GitHub và muốn quản lý bằng Git.

```bash
cd /Users/duc.nguyen/data/projects/success/motives/motivesidp-ai-learning/ielts-target-5-5/web

git init
git add index.html
git commit -m "IELTS study companion"
git branch -M main
git remote add origin https://github.com/<tên-tài-khoản>/ielts.git
git push -u origin main
```

Sau đó trên GitHub: vào repo → **Settings** → **Pages** → mục **Source** chọn
**Deploy from a branch** → chọn nhánh `main` và thư mục `/ (root)` → **Save**.

Sau khoảng 1–2 phút trang sẽ chạy tại `https://<tên-tài-khoản>.github.io/ielts/`.

Lưu ý: repo phải để **Public** thì GitHub Pages mới hoạt động trên tài khoản miễn
phí. Trang này không chứa thông tin cá nhân nên để công khai không sao — tiến độ học
của bạn lưu trong trình duyệt, không nằm trong file.

### Cách 3 — Netlify Drop

Nhanh nhất nếu chỉ muốn có link ngay, không cần tài khoản.

1. Mở [app.netlify.com/drop](https://app.netlify.com/drop)
2. Kéo thả file `index.html` vào trang
3. Nhận link ngay lập tức

Không đăng ký tài khoản thì link vẫn sống nhưng bạn không quản lý được nó về sau.
Nên đăng ký tài khoản miễn phí để giữ quyền cập nhật và đổi tên miền phụ.

---

## Dùng trên điện thoại như một ứng dụng

Sau khi có địa chỉ trang, thêm vào màn hình chính để mở nhanh mà không thấy thanh
địa chỉ trình duyệt:

- **iPhone (Safari)**: mở trang → nút Chia sẻ → **Thêm vào MH chính**
- **Android (Chrome)**: mở trang → menu ba chấm → **Thêm vào màn hình chính**

## Lưu ý về dữ liệu

Tiến độ, sổ lỗi và điểm thi thử được lưu ở hai nơi tùy bản đang dùng:

- **Bản Claude Artifact**: lưu trên máy chủ, đồng bộ giữa mọi thiết bị bạn đăng nhập.
  Dòng chữ "Đồng bộ giữa các thiết bị" ở tab Tiến độ xác nhận việc này đang chạy.
- **Bản tự host**: lưu trong `localStorage` của đúng trình duyệt đó. Xóa dữ liệu
  duyệt web sẽ mất tiến độ, và điện thoại với máy tính không thấy dữ liệu của nhau.

Ngày bắt đầu tuần 1 đặt ở tab **Tiến độ** → mục **Thiết lập**. Chọn một ngày thứ Hai;
nếu chọn ngày khác trang sẽ tự lùi về thứ Hai của tuần đó.
