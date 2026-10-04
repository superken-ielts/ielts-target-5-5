# 03 — Kế hoạch triển khai

Năm giai đoạn, bốn cổng kiểm tra như technical summary. Khác biệt chính: Giai đoạn 0 sửa
trước các lỗi đồng bộ tìm thấy khi review (file 01), và có một lối tắt "chế độ không gói"
để việc học tuần 6 không phải chờ pipeline xong.

Checklist chi tiết từng task: [04-checklist.md](04-checklist.md). Mã task (P0-03, P2-14…)
dùng chung giữa hai file.

## 1. Nguyên tắc triển khai

1. **Lát cắt dọc trước, làm rộng sau.** Unit 1 chạy trọn từ PDF gốc tới màn hình Phiên học
   trên điện thoại rồi mới làm 14 unit còn lại, xếp lớp, rút gọn.
2. **Qua cổng mới sang giai đoạn sau.** Cổng là danh sách kiểm tra cụ thể, không phải cảm giác.
3. **Dùng thật 1–2 tuần trước khi làm tiếp.** Rủi ro lớn nhất của dự án tự build là build lấn giờ học.
4. **Người chưa nhập sách thấy app y như cũ.** Mọi tính năng sách bật theo dữ liệu, không
   thay hành vi hiện tại khi không có sách.
5. **Bản quyền trước tiên.** `.gitignore` và kiểm tra CI có trước khi file sách đầu tiên được mở.

Định nghĩa "xong" cho mỗi task: có code, có test (trừ task thuần giao diện), `python3 web/build.py`
chạy sạch và đã commit hai bản dựng, tài liệu liên quan đã cập nhật, không có nội dung sách
trong diff, task giao diện đã thử trên điện thoại.

## 2. Quyết định cần chốt

Bốn quyết định còn mở trong technical summary, cộng sáu quyết định phát sinh khi review.
Cột "Đề xuất" là mặc định nếu không có ý kiến khác.

| # | Quyết định | Đề xuất | Vì sao | Đổi hướng khi |
|---|---|---|---|---|
| D1 | Nơi chạy app | **Giữ Claude Artifact làm bản chính** cho Giai đoạn 2; file sách trong IndexedDB từng máy. Bản tự host vẫn chạy đủ phần sách, thành PWA ở Giai đoạn 3 | Đã có đồng bộ, chấm Writing không cần API key, người học đang dùng | Spike S0.1 hoặc S0.2 thất bại trên iPhone → Phiên học chuyển sang bản tự host PWA ngay Giai đoạn 2 |
| D2 | Hướng nhập sách | **CLI Python tất định + Claude Code skill ở Giai đoạn 1; bọc LangGraph ở Giai đoạn 4** | Mới có một sách; bước duyệt và chạy tiếp đã có nhờ "mỗi bước một file". Mỗi bước viết như một node nên bọc vào graph là việc cơ học. LangGraph đáng giá khi có agent thứ hai | Muốn đầu tư nền tảng ngay → dựng graph từ đầu, thêm khoảng 2–3 ngày |
| D3 | Thư viện gọi LLM | **SDK chính thức `anthropic`, structured outputs với model Pydantic**, model mặc định `claude-opus-5-5`; sau giao diện `llm.extract()` | Structured outputs có sẵn trong SDK, ít phụ thuộc hơn Pydantic AI; giao diện riêng giúp đổi sau dễ | Cần chạy nhiều nhà cung cấp → thêm Pydantic AI sau cùng giao diện |
| D4 | Tuần 6–12 | **Phiên Target 5.0 thay Block A và D** của giáo án ngày; điểm ngữ pháp tuần 6–12 giữ làm tham khảo trong "Chi tiết ngày" và buổi ôn Chủ nhật | Khung 2 giờ của technical summary (75′ + 30′ + 15′) không còn chỗ cho block ngữ pháp riêng | Thấy hổng ngữ pháp → dùng 15′ từ vựng xen kẽ ngữ pháp |
| D5 | Gói sách | **Cắt PDF theo đoạn ≤ 60 trang, zip theo section**, app nhận cả zip lẫn file rời | Giới hạn bộ nhớ Safari iOS; chép và nhập từng phần | Spike S0.2 cho thấy PDF nguyên cuốn vẫn mượt → bỏ cắt |
| D6 | Trình phát audio | **`<audio>` gốc + nút tự làm**; wavesurfer để sau | Giải mã cả track để vẽ sóng tốn bộ nhớ, không thêm giá trị học | Cần chọn đoạn A–B bằng mắt trên sóng âm |
| D7 | Riêng tư tiến độ sách | **`students/<slug>/books/…`** (cùng mức như tiến độ hiện tại), **không** vào `roster` và tab Lịch sử | Đồng nhất với cách app đang chạy; riêng tư thật cần đổi cả app sang `data/users/<id>/` | Có người học khác dùng chung trang → làm task chuyển sang `data/users/<id>/` |
| D8 | AI chữa bài | Artifact: `sample`; tự host: FastAPI giữ key, Giai đoạn 3 | Không cần backend cho tới khi chấm phát âm | — |
| D9 | Xếp lớp bỏ unit | **Bỏ 4 phiên không lõi, giữ 3 phiên Speaking/Writing** | Technical summary: không cắt Speaking và Writing | Muốn bỏ trọn unit → đổi một hằng số |
| D10 | Nơi chạy pipeline | **Máy cá nhân**, Python 3.12 + uv, ffmpeg; Docling và WhisperX là extra tùy chọn | Sách nằm trên máy; không đưa sách lên cloud | — |

Ghi kết quả vào `docs/agent-hoc-tap/decisions.md` (task P0-01), mỗi quyết định vài dòng.

## 3. Đường găng theo lịch học

Target 5.0 bắt đầu từ tuần 6. Thứ tự làm phụ thuộc người học đang ở tuần nào:

| Người học đang ở | Thứ tự |
|---|---|
| Trước tuần 3 | Giai đoạn 0 → 1 → 2 như kế hoạch |
| Tuần 3–5 | Giai đoạn 0, rồi **MVP lịch học** (P2-03 `core.js`, P2-20 chế độ không gói, P2-14 Hôm nay) trước Giai đoạn 1 |
| Đã qua tuần 6 | MVP lịch học ngay (khoảng 3 ngày): app xếp đúng phiên, đồng hồ, phiếu trả lời; người học mở sách bằng app PDF sẵn có. Gói sách nhập sau, tiến độ giữ nguyên |

Dù ở tuần nào, P0-08 (đổi nội dung tĩnh tuần 6–25 sang Target 5.0) làm sớm vì rẻ và người học
thấy ngay trong tab Hôm nay, Lộ trình.

## 4. Giai đoạn 0 — Chuẩn bị (ước tính 3–4 ngày)

**Mục tiêu:** chốt kiến trúc bằng thử nghiệm thật, sửa lỗi nền, dọn repo.

| Nhóm | Task |
|---|---|
| Quyết định | P0-01 |
| Vệ sinh repo, chống lộ sách | P0-02, P0-03 |
| Sửa lỗi đồng bộ (B1–B4) | P0-04, P0-05, P0-06 |
| Sửa lỗi nhỏ (B5–B8) | P0-07 |
| Nội dung tĩnh Target 5.0 | P0-08 |
| Spike kỹ thuật | P0-09 … P0-15 |
| Nền test và CI | P0-16, P0-17 |

### Spike

Dựng một trang thử riêng `web/spikes/book-spike.html` (không nằm trong app chính), đăng
thành một artifact riêng tư, thử trên ba môi trường: iPhone Safari (mở claude.ai và app
Claude), Android Chrome, máy tính.

| Spike | Thử | Đạt khi | Không đạt thì |
|---|---|---|---|
| S0.1 Lưu file | Chọn 1 PDF 25 MB + 5 MP3, lưu Blob vào IndexedDB, tải lại trang, mở lại sau 24 giờ; đọc `navigator.storage.estimate()` | Còn nguyên sau 24 giờ, quota ≥ 1 GB | D1 đổi: Phiên học chạy bản tự host PWA |
| S0.2 PDF.js | PDF.js bản legacy vendor sẵn, worker tạo từ Blob; vẽ đoạn 60 trang | Trang đầu < 1,5 giây trên iPhone; cuộn 10 trang không bị tải lại | Thử chạy không worker, rồi CDN; vẫn hỏng → PWA |
| S0.3 Audio | Phát từ Blob URL: ±5 giây, tốc độ, lặp A–B, màn hình khóa | Mọi thao tác chạy; lặp A–B lệch ≤ 0,3 giây | Lặp A–B bằng `requestAnimationFrame` |
| S0.4 Micro | `getUserMedia` + `MediaRecorder` trong artifact | Ghi và phát lại được | Ghi âm chỉ ở bản tự host (Giai đoạn 3) — kết quả dự kiến |
| S0.5 Chấm JSON | `sample.json()` chấm 5 bài theo schema tiêu chí | Đọc được điểm 5/5 lần | Giữ regex hiện tại làm dự phòng |
| S0.6 Giải nén | fflate giải nén luồng zip 150 MB không nén | Nhập xong, trang không tải lại | Chỉ nhận file rời |
| S0.7 Bộ sách thật | Người học chạy script inventory trên máy (không in nội dung) | Biết: PDF có lớp chữ không, có answer key và audio script không, dấu track in ra sao, tên file audio kiểu gì | — |

**Cổng G0:** xem checklist. Tóm tắt: D1–D10 đã chốt, B1–B4 đã sửa và có test, spike có
kết quả ghi lại, `.gitignore` và kiểm tra CI đã chạy, nội dung tuần 6–25 đã đổi.

## 5. Giai đoạn 1 — Agent nhập sách (ước tính 8–11 ngày)

**Mục tiêu:** gói Target 5.0 đã duyệt; chạy lại với sách khác chỉ bằng một `book.yaml` mới.

| Bước | Task |
|---|---|
| Khung dự án, schema, fixture sách giả | P1-01 … P1-04 |
| Quét và hồ sơ | P1-05 … P1-08 |
| Cấu trúc, ghép audio | P1-09 … P1-13 |
| Duyệt | P1-14, P1-15 |
| Kế hoạch, đóng gói, kiểm tra | P1-16 … P1-19 |
| Skill Claude Code | P1-20 |
| Chạy thật | P1-21 … P1-23 |

Lát cắt: chạy toàn bộ luồng với **Unit 1** (một đoạn PDF + các track của nó) trước, sau đó
mới chạy cả Section 1, rồi cả sách. Lỗi ghép phát hiện ở Unit 1 rẻ hơn nhiều so với ở cả sách.

**Cổng G1:**

- `book validate` qua: 120 phiên, mọi hoạt động Listening có track, không còn mục duyệt mở.
- Kiểm tra tay 10 hoạt động chọn ngẫu nhiên: đúng trang, đúng track, đúng trang đáp án.
- Chạy lại `book ingest` lần hai: không gọi lại LLM (cache), ra đúng ID cũ.
- Fixture "sách giả kiểu khác" qua toàn bộ luồng chỉ bằng `book.yaml` riêng, không sửa code.

## 6. Giai đoạn 2 — Phiên học trong app (ước tính 11–15 ngày)

**Mục tiêu:** học được trọn một unit chỉ trong app, trên điện thoại.

| Bước | Task |
|---|---|
| Hạ tầng build, thư viện vendor, hàm thuần | P2-01 … P2-03 |
| Lưu trữ và nhập gói | P2-04, P2-05 |
| **Lát cắt dọc Unit 1:** tab Sách, màn hình Phiên học, trang sách, audio, phiếu trả lời | P2-06 … P2-10 |
| Writing, Speaking, kết thúc phiên | P2-11 … P2-13 |
| Nối vào Hôm nay, Lộ trình, Tiến độ, Luyện tập | P2-14 … P2-16, P2-21 |
| Xếp lớp, rút gọn | P2-17, P2-18 |
| Đồng bộ, chế độ không gói | P2-19, P2-20 |
| Kiểm thử, tài liệu, đăng lại | P2-22 … P2-26 |

**Cổng G2:**

- Học trọn 7 phiên của một unit chỉ trong app, trên iPhone.
- Đánh dấu ở điện thoại, mở máy tính thấy ngay; học song song hai máy không mất phiên nào.
- Hôm nay, Tiến độ, Sổ lỗi tự cập nhật sau mỗi phiên; giờ học không bị cộng hai lần.
- Tải lại trang khi mất mạng: sách và tiến độ vẫn còn.
- Người chưa nhập sách thấy app như cũ (e2e kiểm tra).
- Đã dùng thật 1–2 tuần, các lỗi ghi lại đã xử lý hoặc xếp lịch.

## 7. Giai đoạn 3 — AI chữa bài và thẻ từ (ước tính 12–16 ngày)

**Mục tiêu:** nhận xét AI có nhãn tham khảo, thẻ từ hằng ngày, script căn thời gian, và
sẵn sàng cho các sách giai đoạn sau.

| Bước | Task |
|---|---|
| Script căn thời gian, chép chính tả, shadowing | P3-01, P3-02 |
| Chữa Writing có hiệu chỉnh | P3-03 |
| Thẻ từ FSRS | P3-04 |
| Bản tự host PWA, backend, Speaking | P3-05 … P3-07 |
| Theo dõi chi phí | P3-08 |
| Sách tiếp theo trong lộ trình | P3-09, P3-10 |
| Đáp án số hóa, phiếu trả lời chấm tự động | P3-11 |

P3-09 và P3-10 (Cambridge IELTS 20 GT, IELTS Trainer 2 GT) phải xong trước tuần 26 — mock
Cambridge 20 Test 1 rơi vào tuần 26 và Trainer 2 bắt đầu tuần 27. Đây cũng là phép thử thật
cho mục tiêu "dùng lại với sách khác".

**Cổng G3:**

- Nhận xét Writing luôn có nhãn tham khảo; trên 10 bài mẫu có điểm, chênh lệch trung vị
  không quá 1 band (ghi rõ đây là xu hướng, không phải điểm thi).
- Thẻ từ đến hạn hiện trong block 15′ mỗi ngày, đồng bộ hai máy.
- Langfuse hiện chi phí từng lần chạy pipeline và backend.
- Cambridge 20 GT nhập được bằng mẫu phiên `cambridge-test-v1` mà không sửa code lõi.

## 8. Giai đoạn 4 — Thêm agent khác (ước tính 5–10 ngày mỗi agent)

**Mục tiêu:** các agent dùng chung bộ điều phối, tầng công cụ và hộp duyệt.

| Bước | Task |
|---|---|
| Tầng công cụ MCP từ code đã có | P4-01 |
| Bọc agent sách vào LangGraph, dừng chờ duyệt, lưu điểm chạy tiếp | P4-02 |
| Hộp duyệt chung, Langfuse cho mọi graph | P4-03, P4-04 |
| Agent Excel, techpack, học công nghệ | P4-05 … P4-07 |

Agent học công nghệ xuất đúng định dạng `book.json` + `plan.json`, nên app hiện giáo trình
công nghệ như một cuốn sách mà không cần sửa app.

**Cổng G4:** mỗi agent là một graph riêng, dùng chung công cụ MCP và định dạng `review.json`;
agent sách chạy qua graph cho ra gói giống hệt đường CLI.

## 9. Chiến lược kiểm thử

| Lớp | Công cụ | Nội dung |
|---|---|---|
| Pipeline | pytest | Từng bước trên sách giả tổng hợp; so `book.json` với file vàng |
| Hợp đồng | pytest + node:test | Cùng một gói mẫu: `book validate` và bộ kiểm tra lúc nhập của app cùng chấp nhận/từ chối; ID khung `target-gt-v1` trong JS trùng ID `plan.json` từ Python |
| Hàm thuần app | `node --test tests/web` | Hàng đợi, dự báo tuần xong, xếp lớp, rút gọn (phiên lõi không bao giờ bị bỏ), hợp nhất theo `t`, tra đoạn PDF |
| Giao diện | Playwright trên `web/index.html` | Nhập gói mẫu → mở phiên → canvas có trang → audio phát → phiếu trả lời → kết thúc → Hôm nay đã tick → JSON xuất có `books`; và app không có sách vẫn như cũ |
| Build | CI | `python3 web/build.py` rồi `git diff --exit-code` |
| Thiết bị | tay | iPhone Safari (claude.ai, app Claude, cài ra màn hình chính), Android Chrome, máy tính |
| Thực tế | dùng thật | 1–2 tuần sau mỗi giai đoạn có giao diện |

## 10. Rủi ro

| Rủi ro | Cách xử lý |
|---|---|
| Agent ghép sai audio hoặc trang mà không ai thấy | Ngưỡng tin cậy + kiểm tra V1–V8 + kiểm tra tay 10 mẫu ở cổng G1 |
| Lỗi đồng bộ hiện tại (B1–B3) làm mất tiến độ sách | Sửa ở Giai đoạn 0, trước khi có dữ liệu sách |
| Safari iOS hết bộ nhớ hoặc xóa dữ liệu | Cắt PDF, giới hạn canvas, cài ra màn hình chính, luôn giữ gói gốc để nhập lại |
| Artifact không cho micro hoặc đổi chính sách capability | Spike S0.4; bản tự host luôn chạy được mọi tính năng sách |
| Lộ nội dung sách lên repo public | `.gitignore`, kiểm tra CI, fixture tổng hợp, pipeline không ghi vào repo |
| `book.json` và app lệch schema | JSON Schema sinh từ Pydantic, test hợp đồng chạy cả hai phía |
| AI chấm Writing lệch giám khảo | Nhãn tham khảo, hiệu chỉnh bằng bài mẫu có điểm, chỉ dùng band để xem xu hướng |
| Chi phí token tăng | Cache theo sha256, chế độ `manual` qua Claude Code, Langfuse theo dõi |
| Học chậm hơn kế hoạch | Dự báo tuần xong luôn hiện; luật rút gọn khi quá tuần 30 |
| Build lấn giờ học | Lát cắt dọc, chế độ không gói, dùng thật rồi mới làm tiếp |
