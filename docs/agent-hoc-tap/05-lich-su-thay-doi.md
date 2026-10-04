# 05 — Lịch sử thay đổi

Ghi lại từng đợt triển khai: thêm, sửa, xóa file nào và vì sao. Trạng thái từng task ở
[04-checklist.md](04-checklist.md).

---

## Đợt 2 — 04/10/2026: danh sách sách, chọn unit tự do, xem checklist trong app

Nhánh `claude/gallant-ramanujan-ym30oy` đặt lại từ `main` tại `754d175` (đã merge PR #2).

### Yêu cầu

1. Xem checklist những gì đã triển khai cho agent ngay trên UI.
2. Bấm menu Sách → danh sách sách, mỗi sách có thông tin lộ trình: học bao lâu, từ trình độ nào, học xong đạt tới đâu.
3. Bấm vào một sách → liệt kê mọi section và unit để chọn học bất kỳ unit nào.

### Đã làm

| Yêu cầu | Cách làm |
|---|---|
| Checklist trên UI | `build.py` nhúng `docs/agent-hoc-tap/*.md` vào tab Kế hoạch, nhóm "Agent học tập — checklist và kế hoạch" (checklist đứng đầu, ô tick hiện sẵn). Thẻ "Agent nhập sách" cuối màn danh sách sách đếm task đã xong theo giai đoạn (đọc thẳng từ checklist) và có nút mở Checklist, Lịch sử thay đổi. Link tương đối giữa các tài liệu nay bấm được |
| Danh sách sách | Menu Sách luôn mở màn danh sách. Sách đã nhập hiện: vai trò và tuần trong lộ trình, tác giả/NXB, trình độ (Band 3.5 → 5.0 · CEFR A2–B1), nội dung (3 section · 15 unit · 3 review · 3 test · 59 track), thời lượng (120 phiên × 75 phút ≈ 150 giờ), học xong trong (khoảng 4–5,5 tháng ở nhịp 7–5 phiên/tuần; nhịp đang chọn ra số tuần và tháng), bắt đầu khi nào, mục tiêu, tiến độ, nút "Xem unit & chọn bài học" và "Học tiếp". Bốn sách còn lại của lộ trình (Cambridge 20 GT, Trainer 2 GT, Barron's Writing, Cambridge 21 GT) hiện mờ kèm "chưa nhập vào app" |
| Chi tiết sách, chọn unit | Màn chi tiết có nút quay về danh sách, thẻ giới thiệu, phiên kế tiếp, tiến độ, cài đặt, quản lý file, rồi "Chọn unit để học": 3 section, 21 thẻ (15 unit, 3 review, 3 test) — mỗi thẻ có trang in, số phiên, chấm trạng thái từng phiên, nút Học / Học tiếp / Ôn lại và danh sách phiên để chọn lẻ. Bấm Học ở một unit thì "Phiên kế tiếp" chuyển sang chế độ unit tự chọn cho tới khi unit đó xong; nút "Quay về theo lộ trình" bỏ chế độ này |

### File thêm

| File | Vai trò |
|---|---|
| `books/catalog.json` | Thứ tự và vai trò 5 sách trong lộ trình 40 tuần (tuần, mục tiêu, giới thiệu ngắn cho sách chưa nhập) |

### File sửa

| File | Thay đổi |
|---|---|
| `agents/book_ingest/schemas.py` | Model `BookInfo` (role, module, author, publisher, cefr, bandFrom, bandTo, summary, startWhen); `Book.info` |
| `agents/book_ingest/profile.py`, `templates.py` | Đọc `info` trong `book.yaml`, ghi vào `book.json` (khóa lạ bị bỏ qua) |
| `agents/tests/test_pipeline.py` | Test `info` đi từ `book.yaml` sang `book.json` |
| `schemas/book.schema.json` | Xuất lại theo model mới |
| `books/ielts_target_5_0/book.yaml` | Thêm mục `info` (tác giả theo bìa sách; trình độ theo technical summary) |
| `books/ielts_target_5_0/book.json` | Chạy lại agent: thêm `info`; `plan.json` không đổi |
| `web/build.py` | Nhúng `docs/agent-hoc-tap/` vào tab Kế hoạch; nhúng `books/catalog.json` vào chỗ đánh dấu `/*__BOOK_CATALOG__*/` |
| `web/app.template.html` | +9 dòng nhãn và nhóm tài liệu agent trong `DOCMETA`/`DOCGROUPS`; `const BOOK_CATALOG`; `mdInline` tìm link tương đối theo tên file (2 dòng) |
| `web/src/book/core.js` | `focusOf`, `nextSession` theo unit tự chọn, `itemSessions`, `itemCounts`, `entrySession`, `duration`, `checklistStats` |
| `web/src/book/ui.js` | Màn danh sách sách, màn chi tiết với thẻ unit, nút Học theo unit, nút quay về lộ trình, thẻ Agent nhập sách; menu Sách luôn mở danh sách; nút quay lại trong phiên ghi "← Danh sách unit" |
| `web/src/book/book.css` | Kiểu thẻ sách, dòng thông tin, thẻ unit, chấm tiến độ |
| `tests/web/book-core.test.mjs` | +3 test: unit tự chọn, thời lượng theo nhịp, đếm checklist |
| `tests/web/book.e2e.mjs` | Đi qua danh sách → chi tiết; thêm bước chọn Unit 7 rồi quay về lộ trình, bước mở checklist và bấm link sang lịch sử |
| `web/README.md`, `docs/agent-hoc-tap/04-checklist.md`, `README.md` (thư mục docs), `02-kien-truc-va-hop-dong-du-lieu.md` | Mô tả tab Sách mới; task P2-27 … P2-29; trạng thái; sửa ghi chú cũ "thư mục này không nhúng vào app" |
| `web/index.html`, `web/ielts-companion.html` | Bản dựng lại (thêm tài liệu agent và catalog, khoảng +120 KB) |

Không xóa file nào.

### Kiểm thử

| Lệnh | Kết quả |
|---|---|
| `cd agents && python -m pytest -q` | 12 passed |
| `node --test "tests/web/*.test.mjs"` | 11 passed |
| `node tests/web/book.e2e.mjs` | 11/11 bước OK |
| `python3 web/build.py` | 22 tài liệu (thêm 6 tài liệu agent) + 1 sách 120 phiên |

---

## Đợt 1 — 04/10/2026: agent nhập sách + tab Sách

Nhánh `claude/gallant-ramanujan-ym30oy`, dựa trên `main` tại `89133a0` (commit thêm bộ sách
IELTS Target 5.0 vào `books/ielts_target_5_0/`).

### Phạm vi theo yêu cầu

- Agent **chỉ** phục vụ nhập sách: biến PDF + MP3 thành menu học theo lộ trình.
- Thêm menu học vào web, **hạn chế đụng code cũ**: các bản sửa lỗi đồng bộ B1–B4, tích hợp tab Hôm nay,
  Tiến độ chưa làm trong đợt này (xem mục "Chưa làm").
- Không bàn về nguồn gốc dữ liệu sách; dữ liệu nằm trong repo theo lựa chọn của chủ repo.

### Kết quả trên IELTS Target 5.0

| Hạng mục | Kết quả |
|---|---|
| Course Book | `IELTS_Target_5.0.pdf`: 325 trang, bản scan (lớp chữ ~5%, chỉ watermark), có mã hóa `/Encrypt`, độ lệch trang in → PDF là 1 |
| Bản trích Listening | `Target5.0_Listening_R.pdf`: 90 trang — bìa, 2 trang Listening mỗi unit (trang 2N–2N+1), Answer key 32–42, Tapescript 43–90 |
| Audio | 59 file `UnitN_listening_<bài>.mp3`, 113 phút, đủ 15 unit; ghép 59/59 theo tên |
| Cấu trúc | 15 unit × 6 module nhận ra bằng băng tiêu đề đỏ: 14 unit khớp ngay; Unit 15 có băng thừa (Exam practice dài 4 trang) → 1 mục duyệt, đã đồng ý gộp |
| OCR | 57 trang (Answer key 9, Tapescript 48), chạy một lần ~4 phút, cache trong `work/ocr-cache.json` |
| Answer key | Trang đáp án riêng cho từng unit và từng module (Listening, Reading, Writing, Exam practice) + Review 3 |
| Tapescript | Khoảng trang từng unit + TEST 1–3; 58/59 track có trang tapescript chính xác (U02-L1I dùng khoảng Listening của Unit 2) |
| Đoạn PDF cho web | 27 đoạn, 86 MB trong `books/ielts_target_5_0/web/` — mở một trang tải ~3–6 MB thay vì ~70 MB |
| Kế hoạch | 120 phiên × 75 phút, 6 phiên/tuần, tuần 6–25; `book validate` OK |

### Phát hiện về dữ liệu làm thay đổi cách làm

1. **PDF là bản scan** → bước "hiểu cấu trúc" không đọc được chữ. Ranh giới module nhận bằng màu băng tiêu đề
   (code tất định); Answer key và Tapescript lập chỉ mục bằng OCR (RapidOCR, tùy chọn, có cache).
2. **PDF.js đọc gần hết file 100 MB chỉ để mở một trang.** Nguyên nhân: PDF.js luôn kiểm tra trang cuối khi mở
   tài liệu (`checkLastPage`), còn file này có cây trang phẳng 325 trang với page dict nằm rải cạnh ảnh scan
   → 280 yêu cầu Range (~72 MB). Đo bằng log máy chủ. Cách xử lý đúng như quyết định D5 của plan: agent cắt
   Course Book thành đoạn theo unit/review/phần đáp án/tapescript.
3. **Thiếu Work Book và 3 quyển Test.** Phiên 7 của mỗi unit thành "Ôn unit + sổ lỗi" (dùng trang đáp án + Key
   exam vocabulary); phiên Test giữ chỗ trong lịch, ghi chú làm đề Cambridge GT, và vẫn trỏ tới tapescript
   TEST 1–3 có trong Course Book.
4. **Tên audio đã chuẩn** (`Unit4_listening_3b.mp3`) → không cần Whisper; ghép theo mẫu tên trong `book.yaml`.
5. **OCR dính chữ** ("Unit 13Listening3", "CNow listen…", "Unit 12-Speaking 3") → regex tiêu đề không bắt buộc
   khoảng trắng, chấp nhận dấu gạch; nhận "TEST n" làm mốc riêng để phần Test không bị tính vào Unit 15.

### File thêm

| File | Vai trò |
|---|---|
| `agents/pyproject.toml`, `agents/README.md` | Dự án Python `book-ingest`, lệnh `book`; extras `[ocr]`, `[llm]`, `[review]`, `[dev]` |
| `agents/book_ingest/schemas.py` | Model Pydantic: `Book`, `Activity`, `Ref`, `PdfFile` (+ `Chunk`), `AudioFile`, `Plan`, `Session`, `Review`, `TocDraft` |
| `agents/book_ingest/profile.py` | Đọc `book.yaml`, tính trang cuối từng phần, đổi trang in ↔ trang PDF |
| `agents/book_ingest/pdfutil.py` | sha256, mở PDF, đo băng tiêu đề đỏ, vẽ trang |
| `agents/book_ingest/ocr.py` | OCR tùy chọn (RapidOCR) có cache JSON, thứ tự đọc trang hai cột |
| `agents/book_ingest/scan.py` | Bước quét: số trang, lớp chữ, sha256, file trùng, độ dài audio; lệnh `inventory` |
| `agents/book_ingest/structure.py` | Ranh giới module, kiểm tra độ lệch trang, review chia 2 phần, chỉ mục Answer key/Tapescript (theo unit, module, track, TEST) |
| `agents/book_ingest/audio.py` | Ghép audio theo mẫu tên, ID track `U04-L3B`, gắn trang tapescript từng track |
| `agents/book_ingest/review.py` | Hộp duyệt `work/review.json`: gộp, giữ quyết định cũ, `--accept-all`, duyệt từng mục trên terminal |
| `agents/book_ingest/templates.py` | Mẫu phiên `target-gt-v1` → `book.json` và `plan.json` |
| `agents/book_ingest/chunks.py` | Cắt PDF lớn thành đoạn theo cấu trúc sách, ổn định giữa các lần chạy, dùng lại đoạn cũ |
| `agents/book_ingest/validate.py` | Kiểm tra schema + V3 (trang nằm trong file/đoạn), V4 (track), V5 (độ dài), V7 (số phiên), V8 (file, cỡ, sha256) |
| `agents/book_ingest/pipeline.py` | Chạy nối các bước, dừng ở hộp duyệt (mã 2), ghi `report.md` |
| `agents/book_ingest/llm.py` | Bước đọc mục lục: `manual` (vẽ trang cho Claude Code) và `api` (Claude qua SDK `anthropic`, structured output `TocDraft`, mặc định `claude-opus-5-5`) |
| `agents/book_ingest/cli.py`, `__init__.py`, `__main__.py` | Lệnh `inventory`, `profile`, `ingest`, `review`, `validate`, `schemas` |
| `agents/tests/*` | Sách giả sinh lúc chạy (băng đỏ, OCR giả, MP3 tối thiểu); test pipeline, regex, LLM giả, schema, hồi quy trên sách thật |
| `.claude/skills/book-ingest/SKILL.md` | Skill để Claude Code vận hành agent cho sách mới |
| `schemas/{book,plan,review}.schema.json` | JSON Schema xuất từ Pydantic |
| `books/ielts_target_5_0/book.yaml` | Hồ sơ sách, viết ở chế độ manual sau khi đọc trang Contents (PDF trang 4) |
| `books/ielts_target_5_0/{book.json,plan.json,report.md}` | Đầu ra của agent |
| `books/ielts_target_5_0/work/*` | Kết quả từng bước + cache OCR + `chunks.json` + `review.json` (quyết định duyệt) — commit để chạy lại không cần OCR |
| `books/ielts_target_5_0/web/course-book-p*.pdf` | 27 đoạn PDF cho app |
| `web/src/book/core.js` | Hàm thuần: phiên kế tiếp, đếm, tuần dự kiến, dự báo tuần xong, `canSkip`, hợp nhất tiến độ theo `t`, đồng hồ theo mốc thời gian, tìm đoạn PDF, ghép file nhập |
| `web/src/book/ui.js` | Tab Sách: menu theo section/unit, phiên kế tiếp, tiến độ, cài đặt nhịp học, quản lý file (nhập IndexedDB), màn hình Phiên học (đồng hồ, trang sách, đáp án, tapescript, từ vựng, audio, ghi sổ lỗi, kết thúc phiên), trình xem PDF, đồng bộ `students/<slug>/books/<id>` |
| `web/src/book/book.css` | Giao diện tab Sách, dùng lại biến màu và class sẵn có |
| `web/vendor/pdfjs/*` | PDF.js 4.10.38 bản legacy + LICENSE (Apache-2.0) + VERSION.txt |
| `web/serve.py` | Máy chủ chạy thử có HTTP Range |
| `tests/web/book-core.test.mjs` | 8 test `node:test` cho `core.js` và gói sách thật |
| `tests/web/book.e2e.mjs` | E2E Playwright 8 bước trên `web/index.html` |
| `.gitignore`, `CLAUDE.md` | Bỏ qua rác (`.DS_Store`, cache Python, ảnh lỗi e2e, sản phẩm phụ của agent); quy ước repo |
| `docs/agent-hoc-tap/05-lich-su-thay-doi.md` | File này |

### File sửa

| File | Thay đổi |
|---|---|
| `web/app.template.html` | **+12 dòng, không xóa dòng nào**: chỗ đánh dấu `/*__BOOK_CSS__*/` trong `<style>`; `<section id="p-book">` sau tab Lộ trình; nút menu **Sách** (thứ 3); `const BOOKS = /*__BOOKS__*/{}` và `/*__BOOK_JS__*/` trước phần khởi động; `BookUI.init()` sau `renderRootNote()` |
| `web/build.py` | Gom `books/*/book.json` + `plan.json`, chèn mã/CSS tab Sách (chặn chuỗi đóng thẻ), thay chỗ đánh dấu của Sách trước tài liệu; không nhúng `agents/`, `.claude/`, `books/`, `vendor/`, `CLAUDE.md` vào tab Kế hoạch; xét đường dẫn tương đối khi lọc thư mục |
| `web/index.html`, `web/ielts-companion.html` | Bản dựng lại (thêm ~140 KB: dữ liệu sách + mã tab Sách) |
| `web/README.md` | Thêm dòng tab Sách, mục "Tab Sách" (nguồn file, đoạn PDF, nơi lưu tiến độ, giới hạn bản Claude), cập nhật bảng file |
| `docs/agent-hoc-tap/04-checklist.md` | Tick các task đã làm, ghi chú task làm khác plan hoặc hoãn |
| `docs/agent-hoc-tap/README.md` | Thêm file 05 vào mục lục |

### File xóa

| File | Lý do |
|---|---|
| `.DS_Store`, `books/.DS_Store` | Bỏ khỏi git (file hệ thống macOS); thêm vào `.gitignore` |

Không xóa hay đổi tên file sách nào của người dùng.

### Khác với plan

| Mục | Plan | Đã làm | Vì sao |
|---|---|---|---|
| Tab Sách | Thay tab Tài liệu (giữ 7 tab) | Thêm tab thứ 8 "Sách" | Không đụng tab cũ theo yêu cầu; thanh menu dạng flex vẫn vừa trên điện thoại 390 px |
| CLI | Typer | `argparse` (thư viện chuẩn) | Bớt một phụ thuộc |
| Độ lệch trang | Đọc số in ở chân trang | Kiểm tra băng tiêu đề ở trang đầu mọi unit, dò 0–20 nếu lệch | Sách scan không có lớp chữ |
| Ghép audio | rapidfuzz + suy theo thứ tự + Whisper | Chỉ theo mẫu tên trong `book.yaml`, tên lạ → mục duyệt | Tên file đã chuẩn; Whisper/rapidfuzz để lúc có sách cần |
| Màn hình duyệt | Streamlit | Terminal (`review`, `--accept-all`, `--list`) | Chỉ có 1 mục cần duyệt |
| Vendor PDF.js | Nhúng vào HTML, worker từ Blob | File riêng `web/vendor/pdfjs/`, tải lười; dự phòng jsDelivr | Không làm bản dựng nặng thêm 1,8 MB |
| Gói sách | Zip theo section | Đoạn PDF + file rời trong `books/` | Sách đã ở trong repo; app đọc trực tiếp hoặc nhập file rời |
| Thư mục làm việc | Ngoài repo, pipeline từ chối ghi vào git repo | `books/<sách>/work/` trong repo, commit | Chủ repo để sách trong repo; cache OCR giúp người khác chạy lại |
| Hợp đồng `book/1` | `answerPages`, `vocabPages`, `generatedAt` | `answer`/`script`/`vocab`/`alt` dạng `Ref {pdf,pages}`; `source.profileSha256` thay thời điểm | Đáp án và tapescript nằm ở file khác file bài; đầu ra phải ổn định giữa các lần chạy |
| Đồng bộ tiến độ sách | Đăng ký `onSnapshot` trong `connectSync()` | Đọc và hợp nhất khi mở tab Sách, ghi sau 900 ms | Không sửa `boot()` cũ; hợp nhất theo từng phiên nên không mất dữ liệu |

### Quyết định áp dụng theo mặc định (chưa chốt chính thức — P0-01)

D1 cả hai bản (Claude, tự host) đều có tab Sách; D2 CLI + skill, LangGraph để Giai đoạn 4; D3 SDK `anthropic`;
D5 cắt PDF (bắt buộc với file này); D6 `<audio>` gốc; D7 `students/<slug>/books/<id>`, không vào `roster`;
D9 hàm `canSkip` chặn bỏ phiên lõi; D10 pipeline chạy trên máy cá nhân hoặc container. D4 (tuần 6–12) và D8
(AI chữa bài trong phiên) chưa động tới.

### Kiểm thử đã chạy

| Lệnh | Kết quả |
|---|---|
| `cd agents && python -m pytest -q` | 11 passed (gồm hồi quy: chạy lại pipeline trên sách thật cho ra `book.json`/`plan.json` giống hệt) |
| `node --test "tests/web/*.test.mjs"` | 8 passed |
| `node tests/web/book.e2e.mjs` | 8/8 bước OK trên Chromium khổ 390 px: các tab cũ vẫn chạy; tab Sách hiện 120 phiên; mở trang sách tải < 15 MB; xong phiên cộng đúng 1 giờ vào giờ học hôm nay; audio phát và tua +5s; tải lại trang còn tiến độ; nhập file vào IndexedDB; xem trang từ đoạn đã nhập khi máy chủ không có file |
| `python -m book_ingest validate ../books/ielts_target_5_0 --hashes` | OK — 15 unit, 3 review, 3 test, 59 track, 120 phiên, tuần 6–25 |
| `python3 web/build.py` | Nhúng 16 tài liệu (không đổi) + 1 sách 120 phiên |

Chưa kiểm tra được: iPhone/Android thật, bản đăng trên Claude (nạp PDF.js, IndexedDB, micro — spike S0.1–S0.4).

### Chưa làm trong đợt này

- Sửa lỗi đồng bộ B1–B8 (P0-04 … P0-07) — hoãn theo yêu cầu không đụng code cũ. B1 vẫn còn: người chưa đặt
  tên dùng chung gốc `mac-dinh` trên máy chủ.
- Nối tab Hôm nay, Lộ trình, Tiến độ, Luyện tập với sách (P2-14, P2-15, P2-16, P2-21).
- Phiếu trả lời theo câu, Writing/Speaking trong phiên, luật xếp lớp và rút gọn, chế độ không gói
  (P2-10 … P2-12, P2-17, P2-18, P2-20). Dự báo tuần xong và cảnh báo quá tuần 30 đã có.
- CI, `tools/check_repo.py` (không còn hợp vì sách nằm trong repo), Streamlit, Whisper, fixture "sách kiểu khác".
- Đăng lại artifact trên Claude (P2-25) — cần chủ tài khoản; bản dựng đã sẵn sàng.

### Chạy lại

```bash
cd agents && pip install -e '.[ocr,dev]'          # hoặc pip install pymupdf pyyaml pydantic mutagen
python -m book_ingest ingest ../books/ielts_target_5_0
cd .. && python3 web/build.py && python3 web/serve.py   # mở http://localhost:8000/web/index.html → tab Sách
```

---

## Trước đợt 1

| Commit | Nội dung |
|---|---|
| `2c24941` (PR #1, đã merge) | Thêm `docs/agent-hoc-tap/01–04` + README; `web/build.py` bỏ qua `docs/` |
| `f670068` | `05-tai-lieu-mien-phi.md` thêm mục K (bộ sách chốt, lọc danh sách tổng hợp); checklist P0-08, P3-10 |
| `185e885` | Merge `main` (`89133a0` — thêm bộ sách IELTS Target 5.0) vào nhánh làm việc |
