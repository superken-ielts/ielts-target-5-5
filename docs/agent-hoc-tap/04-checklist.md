# 04 — Checklist triển khai

Đánh dấu `[x]` khi task đạt đủ điều kiện "Đạt khi" và định nghĩa "xong" ở file 03 mục 1.
Mã task dùng chung với [03-ke-hoach-trien-khai.md](03-ke-hoach-trien-khai.md); mã lỗi B1–B10
ở [01-review-code-hien-tai.md](01-review-code-hien-tai.md); schema và thuật toán ở
[02-kien-truc-va-hop-dong-du-lieu.md](02-kien-truc-va-hop-dong-du-lieu.md).

---

## Giai đoạn 0 — Chuẩn bị

### Quyết định và repo

- [ ] **P0-01** Chốt D1–D10, ghi `docs/agent-hoc-tap/decisions.md`.
  - Đạt khi: mỗi quyết định có lựa chọn, lý do một dòng, điều kiện đổi hướng.
- [ ] **P0-02** Vệ sinh repo.
  - [ ] `.gitignore`: `*.pdf *.mp3 *.m4a *.wav *.zip inbox/ work/ package/ .DS_Store __pycache__/ .venv/ node_modules/`
  - [ ] Xóa `.DS_Store` khỏi git
  - [ ] `CLAUDE.md`: sửa `app.template.html` rồi chạy build, file nào sinh tự động, không commit nội dung sách, cách chạy test
  - [x] `web/build.py` bỏ qua `docs/` để tài liệu kỹ thuật không bị nhúng vào app học
  - [ ] Bỏ đường dẫn máy cá nhân trong `web/README.md`, thay bằng đường dẫn tương đối
- [ ] **P0-03** Chặn lộ nội dung sách.
  - `tools/check_repo.py`: báo lỗi nếu repo có file media/zip, hoặc file > 1 MB ngoài `web/index.html`, `web/ielts-companion.html`, `web/vendor/`.
  - Đạt khi: thêm thử một file `.mp3` thì script trả mã lỗi.

### Sửa lỗi nền

- [ ] **P0-04** Sửa **B1** — `connectSync(slug)`.
  - Chỉ đọc/ghi máy chủ khi đã có slug thật; không còn đọc/ghi `students/mac-dinh`.
  - Giữ hàm hủy `onSnapshot`; `applyProfile()` đổi slug thì hủy và đăng ký lại.
  - Bỏ tự rước `progress/main`, hoặc chỉ làm khi người dùng bấm "Nhận dữ liệu bản cũ".
  - Đạt khi: hai trình duyệt ẩn danh mở trang chưa đặt tên không thấy dữ liệu của nhau; đổi tên xong, thay đổi từ máy thứ hai vẫn về.
- [ ] **P0-05** Sửa **B2, B3** — `mergeState(local, remote)`.
  - Map (`blocks, hours, vocab, shortDays, dayDone`) hợp theo khóa; mảng (`sessions, essays, errors, mocks`) hợp theo `id`.
  - Thêm `id` cho `errors`, `mocks` (bù `id` cho dữ liệu cũ khi đọc); "Đã xử lý" đánh dấu `done` thay vì `splice`.
  - Snapshot đến trong lúc `saveTimer` chờ thì hợp nhất, không thay thế.
  - Đạt khi: test hợp nhất trong `tests/web/` qua; thử tay ghi sổ lỗi ngoại tuyến ở máy A, tick ô ở máy B, cả hai đều còn.
- [ ] **P0-06** Sửa **B4** — đo cỡ trước khi ghi.
  - Cảnh báo khi JSON tiến độ ≥ 200 KiB; hiện lỗi thật khi máy chủ từ chối, không chỉ "Lưu trên máy này".
- [ ] **P0-07** Sửa **B5–B8**.
  - Đồng hồ tính theo `endsAt − Date.now()` (chép chính tả, Reading, Speaking).
  - Nhập JSON: chuẩn hóa `startDate` về thứ Hai; `weekHours()` dùng `mondayOf()`.
  - Nhập JSON: đẩy `essayBodies` lên `students/<slug>/essays/<id>`.
  - Một hàm định dạng tổng giờ dùng cho cả hai chỗ.

### Nội dung tĩnh

- [ ] **P0-08** Đổi nội dung tuần 6–25 sang Target 5.0 (theo D4).
  - `W` tuần 6–25 ghi section/unit dự kiến; tuần 19 = Target Test 2, tuần 25 = Test 3, tuần 26 = Cambridge IELTS 20 GT Test 1; tuần 27–34 Trainer 2 GT + Barron's Writing; tuần 35–40 Cambridge 20 GT + 21 GT.
  - `phase1-days.json` tuần 6–12: block chính trỏ tới phiên Target 5.0, điểm ngữ pháp giữ làm tham khảo.
  - Cập nhật `README.md` (bỏ "chỉ dùng tài liệu miễn phí"), `00`, `01`, `02`, `05`, `06` cho khớp.
  - Tài liệu mới cho người học `09-hoc-voi-ielts-target-5.md`: 7 phiên mỗi unit, khung ngày 75′ + 30′ + 15′, xếp lớp, rút gọn, cách chọn số phiên/tuần; thêm vào `DOCMETA`, `DOCGROUPS`.
  - Chạy `python3 web/build.py`, commit hai bản dựng và `01a-…md` sinh lại.

### Spike (trang thử `web/spikes/book-spike.html`, artifact riêng tư)

- [ ] **P0-09** Dựng trang thử + **S0.1** lưu Blob vào IndexedDB, đọc `storage.estimate()`, thử `persist()`; kiểm tra lại sau 24 giờ.
- [ ] **P0-10** **S0.2** PDF.js legacy vendor, worker từ Blob, vẽ đoạn 60 trang; đo thời gian trang đầu trên iPhone.
- [ ] **P0-11** **S0.3** Audio từ Blob URL: ±5 giây, tốc độ 0.75–1.25×, lặp A–B, màn hình khóa.
- [ ] **P0-12** **S0.4** `getUserMedia` + `MediaRecorder` trong artifact.
- [ ] **P0-13** **S0.5** `sample.json()` chấm 5 bài Writing theo schema tiêu chí.
- [ ] **P0-14** **S0.6** fflate giải nén luồng zip 150 MB không nén trên iPhone.
- [ ] **P0-15** **S0.7** Script inventory chạy trên máy người học (không in nội dung sách); ghi lại: lớp chữ, answer key, audio script, dạng dấu track, kiểu tên file audio.
  - Đạt khi (cả nhóm spike): bảng kết quả từng spike × từng môi trường nằm trong `decisions.md`, D1/D5 được xác nhận hoặc đổi.

### Nền test và CI

- [ ] **P0-16** Khung test: `tests/web/` chạy bằng `node --test` (không cần cài gói); `agents/tests/` chạy bằng pytest (tạo ở P1-01).
- [ ] **P0-17** `.github/workflows/ci.yml`: `tools/check_repo.py`, `python3 web/build.py && git diff --exit-code`, `node --test tests/web`, pytest khi có `agents/`.

### Cổng G0

- [ ] D1–D10 đã chốt
- [ ] B1–B4 đã sửa, có test, đã thử trên hai thiết bị thật
- [ ] Kết quả 7 spike đã ghi
- [ ] `.gitignore` + `check_repo.py` + CI chạy xanh
- [ ] Nội dung tuần 6–25 đã đổi, đã đăng lại artifact

---

## Giai đoạn 1 — Agent nhập sách

### Khung

- [ ] **P1-01** Dự án `agents/` bằng uv: Python 3.12, Typer, PyMuPDF, rapidfuzz, pydantic, jsonschema, anthropic; extras `[ocr]` Docling, `[audio]` faster-whisper, `[align]` WhisperX, `[review]` Streamlit; ruff + pytest; lệnh `book`.
- [ ] **P1-02** `schemas.py`: `FileInfo, BookProfile, TocDraft, Book, Section, Item, Activity, Plan, Session, ReviewItem, BookProgress`; lệnh xuất JSON Schema ra `schemas/`; test báo lỗi nếu `schemas/` cũ hơn code.
- [ ] **P1-03** Fixture sách giả có lớp chữ: PyMuPDF vẽ mục lục, 3 section × 2 unit, số trang in lệch 6, trang chèn làm lệch thêm, dấu track, trang đáp án; ffmpeg tạo MP3 sine với tên lộn xộn (`Track 3 (2).mp3`, `CD 1/04.mp3`, một file trùng, một file không tên).
- [ ] **P1-04** Fixture biến thể: một bản scan (trang thành ảnh) và một sách "kiểu khác" (đánh số track khác, đáp án ở file riêng).

### Quét và hồ sơ

- [ ] **P1-05** `book inventory <inbox>` (nâng cấp từ script P0-15).
- [ ] **P1-06** `book scan` → `scan.json`: sha256, file trùng, lớp chữ theo tỷ lệ ký tự mỗi trang, `get_toc()`, thông tin ffprobe.
  - Đạt khi: fixture ra đúng số file, phát hiện file trùng, nhận ra bản scan.
- [ ] **P1-07** Gán vai trò file theo `files.match` + chữ trang đầu; không chắc thì mục duyệt `file-role`.
- [ ] **P1-08** `book profile` + `llm.py`.
  - Tìm trang mục lục (mục lục nhúng → tìm chữ "Contents" → hỏi người).
  - Cắt các trang đó thành PDF nhỏ, gọi SDK `anthropic` với structured outputs (`TocDraft`), model từ `BOOK_LLM_MODEL` (mặc định `claude-opus-5-5`); xử lý `stop_reason` khác bình thường.
  - Cache theo sha256 đầu vào trong `work/cache/`; lưu thô ở `work/llm/`.
  - Chế độ `--llm manual`: ghi chữ mục lục + YAML trống để Claude Code hoặc người điền.
  - Đạt khi: test dùng LLM giả (không gọi mạng) cho ra `book.yaml` đúng; chạy lại không gọi lại LLM.

### Cấu trúc và ghép audio

- [ ] **P1-09** Độ lệch trang tất định (file 02 mục 4.1), ngoại lệ thành mục duyệt `page-offset`.
- [ ] **P1-10** `book structure` → `structure.json`: khoảng trang từng module, bỏ `skip_sections`; kiểm tra V1, V2, V3, V6.
- [ ] **P1-11** Tìm dấu track trong trang sách bằng `track_marker` → danh sách (track, trang, hoạt động).
- [ ] **P1-12** Đọc số track từ tên file và thư mục theo `audio_name_patterns`; suy theo thứ tự khi số file khớp số dấu track; rapidfuzz cho ca mờ; gán mức tin cậy (file 02 mục 4.3).
- [ ] **P1-13** Whisper dự phòng (extra `[audio]`) cho file không ghép được; `book match` → `match.json` + mục duyệt `track-match`, `track-unused`, `duplicate-file`.
  - Đạt khi: fixture ghép đúng 100% file có tên chuẩn, file trùng và file không tên vào hộp duyệt.

### Duyệt

- [ ] **P1-14** `book review --cli`: lần lượt từng mục, chọn phương án / nhập giá trị / bỏ qua, ghi `review.json`.
- [ ] **P1-15** `review_app.py` (Streamlit): ảnh trang sách (PyMuPDF render) cạnh đề xuất, `st.audio` cho track, chữ whisper, nút Đồng ý / Sửa / Bỏ qua; bảng sửa khoảng trang unit.

### Kế hoạch, đóng gói, kiểm tra

- [ ] **P1-16** `templates/target_gt_v1.py` + `book plan` → `plan.json` (file 02 mục 3.4–3.5).
  - Đạt khi: 120 phiên; 6 phiên/tuần từ tuần 6 cho Section 1 tuần 6–12, Section 3 kết thúc tuần 25.
- [ ] **P1-17** `book pack`: cắt PDF theo đoạn ≤ 60 trang ở ranh giới section, đáp án thành đoạn riêng; đổi tên audio theo ID track; ghi `book.json`, `report.md`; zip không nén `__core`, `__S1…S3`, `__tests`.
- [ ] **P1-18** `book validate <pkg>`: schema + V4, V5, V7, V8.
- [ ] **P1-19** `book ingest <inbox> --work <dir>`: nối các bước, dừng ở duyệt, `--resume`, `--force <bước>`; từ chối ghi vào thư mục thuộc git repo.

### Skill

- [ ] **P1-20** `.claude/skills/book-ingest/SKILL.md`: khi nào dùng, chuỗi lệnh, cách đọc `report.md`, cách giải mục duyệt cùng người dùng, cấm dán nội dung sách vào commit/issue; trỏ từ `CLAUDE.md`.

### Chạy thật

- [ ] **P1-21** Lát cắt Unit 1 với sách thật (trên máy người học), sửa pattern trong `book.yaml`.
- [ ] **P1-22** Chạy cả Target 5.0, giải hết mục duyệt, xuất gói.
- [ ] **P1-23** Kiểm tra cổng: tay 10 hoạt động ngẫu nhiên; chạy lại lần hai; fixture "kiểu khác" qua luồng.

### Cổng G1

- [ ] `book validate` qua: 120 phiên, mọi Listening có track, 0 mục duyệt mở
- [ ] 10/10 hoạt động kiểm tra tay đúng trang, đúng track, đúng trang đáp án
- [ ] Chạy lại không gọi lại LLM, ID không đổi
- [ ] Fixture sách kiểu khác qua luồng chỉ bằng `book.yaml` riêng
- [ ] `git status` sạch nội dung sách; CI xanh

---

## Giai đoạn 2 — Phiên học trong app

### Hạ tầng

- [ ] **P2-01** `build.py` nhúng `web/src/book/*.js|css` và `web/vendor/**` vào chỗ đánh dấu mới trong template, thứ tự cố định; vẫn xuất hai bản; CI kiểm tra tái lập.
- [ ] **P2-02** Vendor PDF.js (bản legacy + worker dạng chuỗi để tạo Blob worker) và fflate; `web/vendor/README.md` ghi phiên bản, nguồn, giấy phép (Apache-2.0, MIT).
- [ ] **P2-03** `core.js` + test `node --test`:
  - `buildQueue(plan, progress)`, `nextSession()`, `projectFinishWeek()`, `resolveChunk(book, file, page)`
  - `applyPlacement()`, `shorteningSuggestions()`, `canSkip()` (phiên lõi luôn `false`)
  - `mergeBookProgress()` theo `t`, `skeletonPlan("target-gt-v1")`
  - Đạt khi: test phủ mọi luật ở file 02 mục 5.6; test hợp đồng: ID khung trùng ID `plan.json` của fixture.

### Lưu trữ và nhập

- [ ] **P2-04** `store.js`: IndexedDB `ielts-books` v1 (file 02 mục 3.9); object URL có thu hồi; `storage.estimate()`, `persist()`; mọi lệnh bọc try/catch, báo lỗi rõ khi hết chỗ.
- [ ] **P2-05** `import.js`: chọn nhiều file (zip hoặc rời), giải nén luồng, kiểm tra `schema` và tham chiếu, thanh tiến trình, nhập từng phần, thay bản cũ, xóa sách; cảnh báo khi dung lượng còn lại thấp.
  - Đạt khi: nhập gói mẫu từng phần; gói sai schema bị từ chối kèm lý do; dữ liệu gói chỉ hiện bằng `textContent`.

### Lát cắt dọc Unit 1

- [ ] **P2-06** Tab **Sách** thay tab Tài liệu: "Sách của tôi" (cây section → unit → phiên, trạng thái, nút Học phiên kế tiếp, cài đặt 5/6/7 phiên mỗi tuần, quản lý file) và "Tài liệu miễn phí" (`RES` như cũ).
- [ ] **P2-07** `session.js`: khung màn hình Phiên học ngoài `renderAll()`, đầu màn hình unit · phiên n/7 · module, đồng hồ 75′ theo mốc thời gian, lưu `startedAt`, đóng mở lại vẫn đúng.
- [ ] **P2-08** `pdf-view.js`: tra đoạn, vẽ trang của phiên, chỉ vẽ trang đang thấy, giới hạn canvas ~16 MP, phóng to/thu nhỏ, mở trang đáp án, giải phóng khi đóng.
- [ ] **P2-09** `audio-bar.js`: `<audio>` từ Blob, phát/dừng, ±5 giây, tốc độ 0.75/0.85/1/1.1/1.25 giữ cao độ, lặp A–B, danh sách track, nhớ vị trí, Media Session.
- [ ] **P2-10** `answer-sheet.js` + `addError()`: ô theo `questions` (mặc định 10, sửa được), tự chấm ✓/✗, câu sai vào sổ lỗi kèm `ref`, điểm vào `logSession(…, {src:"book", ref})`; chấm tự động khi có đáp án số hóa (P3-11).

### Writing, Speaking, kết thúc phiên

- [ ] **P2-11** Tách `gradeWriting({text, type, context})` từ `buildPrompt()`/`gRun`; dùng `sample.json()` (giữ regex làm dự phòng); phiên 4 soạn bài + đếm từ + đồng hồ 20/40; phiên 5 hiện bài phiên 4 + nhận xét + ô viết lại; bài lưu `S.essays` kèm `ref`; nhãn "tham khảo".
- [ ] **P2-12** Speaking trong phiên: dùng lại đồng hồ 1 + 2 phút; ghi âm khi có `getUserMedia` (bản ghi chỉ ở IndexedDB), không có thì hướng dẫn dùng app ghi âm; ghi số giây và số lần dừng.
- [ ] **P2-13** Kết thúc phiên: phút (từ đồng hồ, sửa được), ô "Cộng vào giờ học hôm nay" bật sẵn và cập nhật ngay ô Số giờ, điểm, ghi chú; "Hoàn thành" và "Lưu dở".

### Nối vào app

- [ ] **P2-14** `todayBlocks()` chế độ sách (file 02 mục 5.4): 75′ + 30′ + 15′, ngày bận 30′ + 15′ + 15′, ngày có phiên Speaking đổi 30′ nói thành ôn sổ lỗi, Chủ nhật giữ nguyên; block Target có nút Mở phiên và tự tick.
  - Đạt khi: không có sách thì `todayBlocks()` trả đúng như cũ (test so sánh).
- [ ] **P2-15** Lộ trình: tuần 6–25 hiện unit dự kiến từ hàng đợi.
- [ ] **P2-16** Tiến độ: thẻ Target 5.0 (phiên xong/tổng, từng section, tổng phút, tuần dự kiến xong theo màu, xếp lớp); Target Test vào bảng thi thử; sổ lỗi hiện `ref`; xuất/nhập JSON `schema: 3` có `books`; "Xóa toàn bộ tiến độ" và "Xóa hẳn học viên" xử lý cả tài liệu sách (dựa trên `S.books`).
- [ ] **P2-21** Luyện tập: thẻ "Bài trong sách tuần này"; lịch sử hiện buổi từ sách kèm nhãn.

### Luật học

- [ ] **P2-17** Xếp lớp: đề nghị trước mỗi section, Review lên đầu, ≥ 80% chọn unit có câu sai, bỏ 4 phiên không lõi của unit còn lại, < 80% Review quay về cuối section; hoàn tác được.
- [ ] **P2-18** Rút gọn: dự báo > tuần 30 thì gợi ý; luật a (bỏ Work Book khi Consolidation ≥ 80%), luật b (gộp Review); người học xác nhận từng luật; phiên lõi không bao giờ bị bỏ.

### Đồng bộ và lối tắt

- [ ] **P2-19** Tiến độ sách ở `students/<slug>/books/<bookId>` + `…/answers/<sessionId>`; `connectSync()` đăng ký thêm; hợp nhất theo `t`; không ghi vào `roster`; bản tự host lưu cục bộ.
  - Đạt khi: hai máy cùng học, mỗi máy xong một phiên lúc ngoại tuyến, nối mạng lại thấy đủ cả hai.
- [ ] **P2-20** Chế độ không gói: bật trong tab Sách, dùng `skeletonPlan()`; mọi thứ trừ trang sách và audio đều chạy; nhập gói sau giữ nguyên tiến độ.

### Kiểm thử, tài liệu, đăng lại

- [ ] **P2-22** Playwright trên `web/index.html` với gói mẫu tổng hợp: luồng nhập → học → kết thúc → Hôm nay tick → xuất JSON; và luồng không có sách như cũ.
- [ ] **P2-23** Thử trên thiết bị: iPhone Safari (claude.ai, app Claude, cài ra màn hình chính), Android Chrome, máy tính; một đoạn PDF 60 trang không làm tải lại trang.
- [ ] **P2-24** Cập nhật `web/README.md` (tab Sách, nơi lưu file, cách nhập gói, giữ gói gốc) và `09-hoc-voi-ielts-target-5.md`.
- [ ] **P2-25** Đăng lại artifact, giữ capability đang có (`db`, `sample`, `downloads`); kiểm tra đồng bộ tiến độ sách bằng hai thiết bị.
- [ ] **P2-26** Dùng thật 1–2 tuần, ghi lỗi và xử lý.

### Cổng G2

- [ ] Học trọn 7 phiên một unit chỉ trong app trên iPhone
- [ ] Đồng bộ hai máy, học song song không mất phiên
- [ ] Hôm nay, Tiến độ, Sổ lỗi tự cập nhật; giờ học không cộng hai lần
- [ ] Tải lại khi mất mạng vẫn còn sách và tiến độ
- [ ] App không có sách như cũ (e2e)
- [ ] Đã dùng thật 1–2 tuần

---

## Giai đoạn 3 — AI chữa bài và thẻ từ

- [ ] **P3-01** `book align` (extra `[align]`): tách audio script theo track, WhisperX căn từng từ → `align/<track>.json` trong gói riêng tư; kiểm tra mẫu 5 track.
- [ ] **P3-02** Bảng script trong phiên: tô câu đang phát, chạm để tua, chế độ chép chính tả (ẩn chữ, gõ, so khác), shadowing (lặp câu N lần, có khoảng nghỉ).
- [ ] **P3-03** Chữa Writing v2: band descriptors công khai + bộ bài mẫu có điểm để hiệu chỉnh, JSON có lỗi kèm vị trí → đề xuất đưa vào sổ lỗi, đường xu hướng; script đo chênh lệch trên 10 bài mẫu.
- [ ] **P3-04** Thẻ từ FSRS (ts-fsrs vendor): thêm từ từ block 15′ (cụm từ + câu ví dụ tự đặt), hàng ôn đến hạn trong Hôm nay, đồng bộ ở tài liệu riêng có đo cỡ, xuất CSV cho Anki.
- [ ] **P3-05** Bản tự host thành PWA: manifest, service worker giữ vỏ app, cài ra màn hình chính; hướng dẫn iOS; cân nhắc OPFS.
- [ ] **P3-06** Backend FastAPI (tự host): `/grade/writing`, `/speaking/assess`; key chỉ ở server; token đơn giản cho từng học viên; CORS, giới hạn tần suất; hướng dẫn triển khai.
- [ ] **P3-07** Speaking: ghi âm ở bản tự host → Azure Pronunciation Assessment (đọc theo câu mẫu và nói tự do) + nhận xét LLM; artifact hiện "chỉ có ở bản tự host".
- [ ] **P3-08** Langfuse (tự host hoặc project riêng tư) cho pipeline và backend: từng bước, token, chi phí.
- [ ] **P3-09** Nhập **Cambridge IELTS 20 GT** bằng mẫu phiên `cambridge-test-v1` (đề → Listening, Reading, Writing, Speaking, chấm) — trước tuần 26.
- [ ] **P3-10** Nhập **IELTS Trainer 2 GT** (`trainer-gt-v1`) và Barron's IELTS Writing (mẫu theo chương) — trước tuần 27.
- [ ] **P3-11** Đáp án số hóa: bước `book answers` đọc trang đáp án thành `answers.json` (riêng tư, có duyệt); app nạp vào store `answers`, phiếu trả lời chấm tự động.

### Cổng G3

- [ ] Nhận xét Writing có nhãn tham khảo; chênh lệch trung vị ≤ 1 band trên 10 bài mẫu
- [ ] Thẻ từ đến hạn hiện mỗi ngày, đồng bộ hai máy
- [ ] Langfuse hiện chi phí từng lần chạy
- [ ] Cambridge 20 GT nhập được không sửa code lõi

---

## Giai đoạn 4 — Thêm agent khác

- [ ] **P4-01** Tầng công cụ MCP (FastMCP) từ code đã có: `doc` (chữ trang, ảnh trang, OCR), `audio` (probe, nghe đoạn đầu, căn thời gian).
- [ ] **P4-02** Bọc `book_ingest` vào LangGraph: mỗi bước một node, `interrupt()` ở bước duyệt, checkpointer SQLite trong `work/`; test gói ra giống hệt đường CLI.
- [ ] **P4-03** Hộp duyệt chung: một app Streamlit đọc `review.json` của mọi agent.
- [ ] **P4-04** Langfuse cho mọi graph.
- [ ] **P4-05** Agent phân tích Excel: chạy pandas/DuckDB trong môi trường cách ly, trả bảng + biểu đồ + nhận xét; duyệt số liệu trước khi dùng.
- [ ] **P4-06** Agent quét techpack: dùng lại công cụ `doc`; schema BOM và bảng thông số; luật kiểm tra (thiếu size, sai định dạng dung sai) viết bằng code; duyệt các mục vi phạm.
- [ ] **P4-07** Agent học công nghệ mới: tra cứu web (chạy song song), xuất `book.json` + `plan.json`; duyệt danh sách nguồn; app hiện như một cuốn sách.

### Cổng G4

- [ ] Mỗi agent là một graph riêng, dùng chung công cụ MCP và `review.json`
- [ ] Agent sách qua graph cho ra gói giống đường CLI

---

## Việc treo theo quyết định

- [ ] **X-01** (D7) Chuyển dữ liệu cá nhân sang `data/users/<id>/` + capability `user` + `rules` cho `db`, có bước chuyển dữ liệu cũ — khi có người học khác dùng chung trang.
- [ ] **X-02** (D5) OPFS cho file sách — nếu IndexedDB thiếu dung lượng.
- [ ] **X-03** (D6) wavesurfer.js — nếu cần chọn đoạn A–B trên sóng âm.
