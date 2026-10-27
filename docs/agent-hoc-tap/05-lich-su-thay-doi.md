# 05 — Lịch sử thay đổi

Ghi lại từng đợt triển khai: thêm, sửa, xóa file nào và vì sao. Trạng thái từng task ở
[04-checklist.md](04-checklist.md).

---

## Đợt 23 — 27/10/2026: GENKI Unit 0 làm lại — 19 video ngắn, chữ sáng theo chỗ đang đọc

Nhánh `claude/nifty-darwin-23vvae`, đẩy lên `main`. Người học góp ý về năm video Unit 0 của đợt 17:
- chữ trên màn hình không khớp lời Emma;
- giọng Nhật đọc mà không có lời dịch tiếng Anh, tiếng Việt;
- học quá nhanh, cần chia nhỏ hơn;
- cả đoạn hiện một lúc nên không biết giọng Nhật đang đọc tới đâu;
- tất cả cần chậm hơn một nhịp, và cần nói bài học để làm gì.

**Công cụ dựng video (`agents/lesson_video/`)**
- `jpcard.py`: tầng 2–3 hiện đúng câu đang nói — Emma: "EMMA SAYS" + lời của cô, "DỊCH LỜI EMMA" + `vi`; câu tiếng
  Nhật, file nghe: "ENGLISH" + `en`, "TIẾNG VIỆT" + `vi`; đếm ngược: "YOUR TURN" + `note`. Dòng thiếu thì hiện `en` /
  `vi` của thẻ như cũ. Tô sáng: chữ đang đọc nền cam nhạt gạch chân cam, chữ vừa đọc nền xanh nhạt, romaji sáng theo.
  Đếm ngược có nhãn cam và vòng số ở góc thẻ. Chữ Nhật trên thẻ tới 60 px (thẻ một hàng chữ cái nhìn rõ nét).
- `timeline.py`: khung hình mang `en`, `hl`, `done`. Câu tiếng Nhật có `step` đọc từng phần (mỗi phần một khung, nghỉ
  `step` giây); dòng `track` có `step` tách file nghe theo khoảng lặng (`speech_spans`, `track_spans`), mỗi đoạn một
  chữ, chữ sáng trước tiếng 0.15 giây, chỗ nghỉ giãn ra ≥ `step`. `echo` sau câu đọc từng phần tính cả chỗ nghỉ.
- `script.py`: dòng thoại có `en`, `hl` (số, danh sách, `all`), `step`; bài có `step`. `reading_plan` (dùng chung cho
  `check` và lúc dựng) quyết định chữ nào sáng và câu đọc thành mấy phần. Cảnh `jp` nay có `wait` / `echo`. `check` so
  từng phần của câu đọc từng phần với đúng chữ của nó, báo số phần khác số chữ được tô, và số đoạn có tiếng của file
  nghe khác số chữ được tô.
- `ja.py`: `card_tokens`, `romaji_tokens`, `split_parts`, `as_said`; âm ghép đọc riêng (みょ, りょ, ぎょ… — misaki đọc
  tách thành hai âm ở mọi cách viết) đưa thẳng âm vị cho Kokoro; `check_line` báo chữ cái hay âm ghép đọc riêng bị đọc
  sai (へ → "e" như trợ từ).

**19 video mới** (`books/Genki/lessons/U00-01-start` … `U00-19-numbers-2`, UNIT0_TOTAL, thay `U00-hiragana-1`,
`U00-hiragana-2`, `U00-katakana`, `U00-greetings`, `U00-numbers`: xóa kịch bản rồi `prune` bỏ khỏi `lessons.json` và
xóa `.mp4`)
- Start here: Unit 0 học gì, để làm gì (đọc được bài 1, chào hỏi và số dùng ngay ở bài 1), thứ tự video, cách xem.
- Hiragana 1–9: ba loại chữ và nguyên âm; hàng か さ, た な, は ま, や ら わ ん (mỗi chữ Yuki đọc riêng, người học nhắc
  lại, rồi cả hàng có YOUR TURN; cả bảng với JWS-01); luyện tập (chữ dễ nhầm, chữ viết tay, nghe – viết); ゛゜ (JWS-02);
  âm ghép (JWS-03); っ, trường âm, nhịp, cao độ (JWS-04…08).
- Katakana 1–4: hàng ア–ホ; hàng マ–ン, cả bảng, chữ dễ nhầm (JWS-09); dấu, âm ghép, ー (JWS-10…12); âm ngoại lai
  (JWS-13), từ mượn, tên tiếng Việt, làm quen chữ Hán.
- Greetings 1–3: mỗi câu chào Emma nói tình huống → Yuki / Takeshi → lượt bạn → audio gốc K00-01 cắt đúng câu đó;
  video 3 là luyện tập: 10 tình huống đố, tự giới thiệu.
- Numbers 1–2: 0–20 từng số, cách đọc thứ hai; hàng chục, 100; audio K00-02 tô từng số; bài A, B, C; nghe – viết.
- Mỗi video mở đầu bằng "In this video" (học gì, để làm gì). Câu nào cũng có lời dịch. Nhịp: Emma 0.9, Yuki / Takeshi
  0.78, nghỉ 0.8 giây giữa hai câu, 1.5 giây giữa hai cảnh, 0.9 giây giữa hai chữ (audio sách 1.2 giây).

**Sửa khác**
- `books/Genki/book.yaml`: tóm tắt sách và ghi chú hai phiên Unit 0 nói 19 video; chạy lại agent nhập sách
  (`book.json`).
- Tài liệu: file 07 mục 4.1 (bảng 19 video), 4.2 (lời dịch từng dòng, tô sáng, `step`, `wait` / `echo` trong cảnh
  `jp`, video Unit 0 3–5 phút), 4.3 (tầng 2–3 theo câu, tô sáng, đọc từng chữ, âm vị âm ghép), 4.4 (lỗi đã gặp), 4.6
  (mốc thời gian audio JWS / K00 lấy bằng ASR); `agents/README.md`; checklist P2-54.
- Test (`agents/tests/test_japanese_video.py`): chữ của thẻ, romaji, các phần của câu; `reading_plan`; đọc từng chữ
  (khung, chỗ nghỉ, `echo`); tầng 2–3 theo câu; vẽ tô sáng và đếm ngược; tách file nghe theo khoảng lặng (wav giả ba
  tiếng bíp) và báo lệch số đoạn; kiểm cách đọc từng phần (へ); âm vị âm ghép. E2E: thẻ GENKI có 37 video, Unit 0 có 19
  nút video theo thứ tự (Start, Hiragana × 9, Katakana × 4, Greetings × 3, Numbers × 2), mỗi video 2–5 phút.

## Đợt 22 — 26/10/2026: Video Giai đoạn 0 — Unit 3 (4 video)

Nhánh `claude/nifty-darwin-23vvae`, đẩy lên `main`. Làm theo sổ tay ở file 08 mục 6. Xong đợt này là đủ phần đã hẹn:
Intro và Unit 1–3 (15 video).

**Bốn video Unit 3 · Your time** (27:44, mỗi video gắn vào một phiên của unit)
- `U03-lesson-1` — Reading · Happiness is …: free time, pronouns, don't / doesn't (6:23): tám bài đăng "Happiness
  is …" đọc từng câu (hai cảnh, mỗi cảnh bốn bài cho chữ đủ to); đại từ chủ ngữ và tân ngữ; hoạt động lúc rảnh (1.31,
  mười hai cụm); sáu câu mẫu "Happiness is …" của Mai; don't / doesn't (1.32, bảy câu; bài 2a); Moira và Sam làm gì lúc
  rảnh (Tom và Mai kể lại vì thiếu 1.33); Your turn; lỗi hay gặp.
- `U03-lesson-2` — Listening · Do you like New Year? always / often, do / does questions (8:40): Min và Paul nói về
  năm mới (1.34, phát nguyên hai bài), bài 3a (phát lại sáu câu), 's và s', trạng từ tần suất (phát lại bốn câu), trọng
  âm (1.35, chín từ), Tết của Mai, câu hỏi với do / does (câu hỏi phát từ 1.34 vì thiếu 1.36), sắp xếp câu hỏi (1.37,
  tám câu), Your turn, lỗi hay gặp.
- `U03-target` — Speaking · Invite someone out (5:06): Rocio và Léon mời bạn (1.38), Task vocabulary (phát lại sáu
  câu của 1.38), hỏi trước – mời – trả lời, nói điều mình thích và không thích, chuẩn bị ba lời mời, hội thoại mẫu Mai
  mời Tom, Your turn, lỗi hay gặp.
- `U03-explore` — Explore Speaking · go, conversation topics, phone messages (7:35): Keyword go (bài 1a, bảng bốn
  cách dùng, bài 2a), Across cultures (Ruth kể lại vì thiếu 1.39; Amina 1.40), ở Việt Nam thì sao, Rocio gọi tìm
  Blake (1.41) và tờ ghi tin nhắn, sáu câu điện thoại (1.42), Your turn ghi tin nhắn theo thẻ vai bài 5a.

**Track thiếu của Unit 3** (CD1 thiếu 1.33, 1.36, 1.39): 1.36 thay bằng câu hỏi có sẵn trong 1.34; 1.33 và 1.39 không
có ở track nào, nên nhân vật kể lại theo đáp án Teacher's Book và màn hình ghi rõ không có audio (sổ tay mục 6.5).

### File thêm

| File | Vai trò |
|---|---|
| `books/book_english_unlimited_a2_elemetary/lessons/U03-*.yaml`, `U03-*.mp4` | Kịch bản và video Unit 3 |

### File sửa

| File | Thay đổi |
|---|---|
| `books/book_english_unlimited_a2_elemetary/lessons/lessons.json` | Thêm bốn video Unit 3 (do lệnh `build` ghi) |
| `docs/agent-hoc-tap/08-giai-doan-0-a1-a2.md` | Mục 6.8 (độ phủ Unit 3), mục 5 (việc tiếp theo) |
| `docs/agent-hoc-tap/04-checklist.md` (P2-53) | Đợt 22 |
| `tests/web/book.e2e.mjs` | Thẻ A2 có 15 video; Unit 3: nút video theo thứ tự phiên (Reading, Listening, Speaking, Explore) |
| `web/index.html`, `web/ielts-companion.html` | Bản dựng lại |

### Kiểm thử

- `python3 web/build.py && git diff --stat`: bản dựng khớp nguồn; A2 79 phiên, 15 video.
- `cd agents && python -m pytest -q`: 127 test qua (hồi quy "video A2 khớp `lessons.json`" chạy trên 15 video).
- `node --test "tests/web/*.test.mjs"`: 16 test qua.
- `node tests/web/book.e2e.mjs`: E2E OK; Intro, Unit 1–3 có nút video theo thứ tự phiên, dài 5–10 phút.
- `python -m lesson_video phonemes` trên bốn kịch bản Unit 3: 0 câu có ⚠.
- Bốn video: H.264 1280×720 + AAC, có chương, độ lớn trung bình −17 dB.
- Giao diện ở khổ điện thoại: thẻ Unit 3 hiện "Video bài giảng · 4", mỗi video nằm dưới phiên của nó; phiên Bài 1 mở
  `U03-lesson-1.mp4`. Không có lỗi JS.

### Còn treo

- P2-53: Unit 4–14 chưa có video. Unit 4 dùng tiếp CD1 (đã chép lời tới 1.57); từ Unit 5 cần chép lời CD2, CD3 trước
  (`python -m lesson_video transcribe ../books/book_english_unlimited_a2_elemetary 2.1 2.57`).

---

## Đợt 21 — 26/10/2026: Video Giai đoạn 0 — Unit 2 (4 video)

Nhánh `claude/nifty-darwin-23vvae`, đẩy lên `main`. Làm theo sổ tay ở file 08 mục 6.

**Bốn video Unit 2 · Away from home** (27:51, mỗi video gắn vào một phiên của unit)
- `U02-lesson-1` — Listening · I miss my friends: offers, requests, a / an / some (8:17): tranh A–D trang 18 (lưới
  2×2), bốn người nhớ gì khi xa nhà (1.21, phát từng người), email của Scott, Carly và Scott gọi điện (1.22, phát
  nguyên bài), Scott vui vẻ mang gì; mời và nhờ (phát lại hai câu của 1.22), đáp lời mời và lời nhờ; a / an / some
  (1.23, mười cụm); trọng âm (1.24); tình huống nói mẫu của Tom và Mai; lỗi hay gặp.
- `U02-lesson-2` — Reading · Sofasurfing: present simple, interests and wants (6:50): trang Sofasurfing.com, hồ sơ
  của Melek và Fiona đọc từng câu, điểm chung của hai người; hiện tại đơn (1.25, tám câu), thêm s sau he / she / it;
  thư trả lời của Fiona (bài 5); sở thích và mong muốn; hồ sơ mẫu của Mai.
- `U02-target` — Speaking · Take care of a guest (6:06): thư của Akira, Koji tới nhà Erkan (1.26), Task vocabulary
  (phát lại năm cặp câu của 1.26), mẫu câu của chủ nhà và khách, hội thoại mẫu Mai làm chủ nhà ở Huế, Your turn hai
  vai, lỗi hay gặp.
- `U02-explore` — Explore Writing · in, an email to ask for something (6:37): Keyword in (nơi chốn, thời gian, ngôn
  ngữ; bài 2a), từ loại trong từ điển, ba email của Ju-Yung và Erkan, lời chào và lời kết thư, ba lời nhờ, viết hoa,
  email mẫu của Mai gửi Fiona, Your turn.

**Soát cách đọc thành lệnh** `python -m lesson_video phonemes <kịch bản>` (`agents/lesson_video/phonemes.py`)
- In phiên âm Kokoro (cùng bộ tách âm khi đọc) của các câu có tên riêng, chữ cái rời, số, từ đồng tự; đánh dấu ⚠ ba lỗi
  đã gặp: động từ `use` đọc /juːs/, `live(s)` đọc /laɪv/, `read` hiện tại đọc /rɛd/. Thay cho đoạn script tạm ở
  bước 4 của sổ tay.
- Lỗi `use` tìm ra ở đợt này: câu mệnh lệnh ("Use these phrases", "For the past, use was and were") và sau danh từ
  ("people use both", "nobody uses") bị đọc như danh từ. Sửa `say` (`yooz`, `yoozes`) ở 13 câu của 7 kịch bản; dựng
  lại `U00-personal-info`, `U01-target` (đã đẩy ở đợt 19, 20), `U02-explore`, `U02-lesson-1`. Video dựng lại chỉ đọc
  lại các câu đã sửa (bộ nhớ đệm giữ phần còn lại).

**Vướng và cách xử lý** (đã ghi vào sổ tay file 08 mục 6.5–6.7)
- Track 1.27 (nghe lại Task vocabulary) thiếu trong bộ CD1: năm cặp câu có sẵn trong 1.26, nên cắt từ đó.
- Kokoro đọc động từ `lives` / `live` thành /laɪvz/ sau danh từ và tên riêng: viết `say` là `livz` / `liv`. Lỗi tìm
  ra khi soát phiên âm, trước lúc dựng.
- Nhãn A–D của dải tranh bị cắt sang ô bên cạnh khi chia `grid: 4`: chọn `clip` bắt đầu trước nhãn tranh đầu.
- Máy khởi động lại khi đang dựng `U02-explore`: chạy lại hàng đợi, các câu đã đọc lấy từ bộ nhớ đệm.
- Commit làm trong một `git worktree` ở `origin/main` để hàng đợi dựng Unit 3 vẫn chạy.

### File thêm

| File | Vai trò |
|---|---|
| `books/book_english_unlimited_a2_elemetary/lessons/U02-*.yaml`, `U02-*.mp4` | Kịch bản và video Unit 2 |
| `agents/lesson_video/phonemes.py` | Lệnh `phonemes`: soát cách Kokoro đọc, cảnh báo lỗi đã gặp |

### File sửa

| File | Thay đổi |
|---|---|
| `books/book_english_unlimited_a2_elemetary/lessons/lessons.json` | Thêm bốn video Unit 2 (do lệnh `build` ghi) |
| `books/book_english_unlimited_a2_elemetary/lessons/U00-personal-info.*`, `U01-target.*` | `say` cho động từ `use`; dựng lại |
| `agents/lesson_video/cli.py`, `agents/tests/test_lesson_video.py` | Lệnh `phonemes`; test chọn câu cần soát và cảnh báo |
| `agents/README.md`, `CLAUDE.md` | Lệnh `phonemes` |
| `docs/agent-hoc-tap/08-giai-doan-0-a1-a2.md` | Mục 6.4 (bước 4 dùng lệnh `phonemes`), 6.5 (track thiếu, commit trong worktree), 6.6 (`use`), 6.8 (độ phủ Unit 2) |
| `docs/agent-hoc-tap/04-checklist.md` (P2-53) | Đợt 21 |
| `tests/web/book.e2e.mjs` | Thẻ A2 có 11 video; Intro, Unit 1, Unit 2: nút video theo thứ tự phiên, dài 5–10 phút |
| `web/index.html`, `web/ielts-companion.html` | Bản dựng lại |

### Kiểm thử

- `python3 web/build.py && git diff --stat`: bản dựng khớp nguồn; A2 79 phiên, 11 video.
- `cd agents && python -m pytest -q`: 127 test qua (thêm 1: chọn câu cần soát cách đọc và cảnh báo lỗi đã gặp; hồi quy
  "video A2 khớp `lessons.json`" chạy trên 11 video).
- `node --test "tests/web/*.test.mjs"`: 16 test qua.
- `node tests/web/book.e2e.mjs`: E2E OK; Intro, Unit 1, Unit 2 có nút video theo thứ tự phiên, dài 5–10 phút.
- `python -m lesson_video phonemes` trên cả 15 kịch bản A2 (kể cả Unit 3 chưa dựng): 0 câu có ⚠.
- Sáu video mới và dựng lại: H.264 1280×720 + AAC, có chương, độ lớn trung bình −17 dB.
- Giao diện ở khổ điện thoại: thẻ Unit 2 hiện "Video bài giảng · 4", mỗi video nằm dưới phiên của nó; phiên Bài 1 mở
  `U02-lesson-1.mp4`. Không có lỗi JS.

### Còn treo

- P2-53: Unit 3 (4 video) ở đợt sau; Unit 4–14 chưa làm.

---

## Đợt 20 — 26/10/2026: Video Giai đoạn 0 — Unit 1 (4 video)

Nhánh `claude/nifty-darwin-23vvae`, đẩy lên `main`. Làm theo sổ tay ở file 08 mục 6.

**Bốn video Unit 1 · People in your life** (26:33, mỗi video gắn vào một phiên của unit)
- `U01-lesson-1` — Listening · Nice to meet you: people you know, 's, am / is / are (6:59): từ chỉ người trong gia
  đình và người quen (phát từng từ của 1.8), ai là ai ở bữa tiệc của Rob (1.7), sở hữu 's, giới thiệu nhau (1.9),
  am / is / are (1.10, tám câu), câu hỏi với Are / Is (1.11), Your turn.
- `U01-lesson-2` — Reading · Life's work: jobs, was / were (6:12): bốn nghề (tranh trang 12), bài phỏng vấn Rob đọc
  từng câu, xếp các việc của Rob theo thời gian, tính từ tả công việc (từng cặp trái nghĩa của 1.12), was / were
  (1.13), việc đầu tiên của Sally (1.14), Your turn: việc đầu tiên, tốt nhất, tệ nhất.
- `U01-target` — Speaking · Talk about someone you know well (5:56): Michel nói về Roberto, Donna nói về Adam (1.15),
  Task vocabulary (1.16), chuẩn bị ghi chú, bài nói mẫu của Mai về bạn Lan, Your turn, lỗi hay gặp, viết hồ sơ ngắn
  (bài viết của Look again).
- `U01-explore` — Explore Speaking · OK, greetings, Sorry, can you say that again? (7:26): Keyword OK (tranh A–D trang
  15), chào hỏi ở các nước (sáu tranh, 1.17–1.18), ở Việt Nam thì sao, Maite và Krishnan (1.19), Sorry, which …?,
  hỏi lại để kiểm tra thông tin, Your turn.

**Sổ tay** (file 08 mục 6) thêm điều học được khi viết kịch bản Unit 2 trong lúc chờ dựng:
- Kokoro đọc `lives` / `live` (động từ) thành /laɪvz/, /laɪv/ sau danh từ, tên riêng ("My mother lives", "Erkan
  lives") và trong danh sách từ; viết `say` là `livz` / `liv`. Video đã dựng (Intro, Unit 1) không có chỗ nào bị.
- Ảnh dải tranh `grid` chia đều theo bề ngang nên nhãn A–D bị cắt sang ô bên cạnh: chọn `clip` bắt đầu trước nhãn.
- Cảnh `bullets` tự đánh số; cảnh `vocab` cần `focus` ở dòng đầu; Emma đọc to cả thư thì không khai `emma: teacher`.
- Nhiều lệnh dựng cùng chờ một khóa `flock` thì không chạy theo thứ tự gọi: dựng theo một danh sách id trong file.
- Bảng `say`: năm, ngày tháng, giờ, tên riêng Unit 2, chữ Việt trong câu tiếng Anh.

### File thêm

| File | Vai trò |
|---|---|
| `books/book_english_unlimited_a2_elemetary/lessons/U01-*.yaml`, `U01-*.mp4` | Kịch bản và video Unit 1 |

### File sửa

| File | Thay đổi |
|---|---|
| `books/book_english_unlimited_a2_elemetary/lessons/lessons.json` | Thêm bốn video Unit 1 (do lệnh `build` ghi) |
| `docs/agent-hoc-tap/08-giai-doan-0-a1-a2.md` | Mục 6.4, 6.6, 6.7 (điều mới học được), 6.8 (độ phủ Unit 1) |
| `docs/agent-hoc-tap/04-checklist.md` (P2-53) | Đợt 20 |
| `tests/web/book.e2e.mjs` | Thẻ A2 có 7 video; Unit 1 có bốn nút video 5–10 phút theo thứ tự phiên |
| `web/index.html`, `web/ielts-companion.html` | Bản dựng lại |

### Kiểm thử

- `python3 web/build.py && git diff --stat`: bản dựng khớp nguồn; A2 79 phiên, 7 video.
- `cd agents && python -m pytest -q`: 126 test qua (hồi quy "video A2 khớp `lessons.json`" chạy trên 7 video).
- `node --test "tests/web/*.test.mjs"`: 16 test qua.
- `node tests/web/book.e2e.mjs`: E2E OK; Unit 1 có bốn nút video Listening, Reading, Speaking, Explore, dài 5–10 phút.
- Bốn video: H.264 1280×720 + AAC, có chương, độ lớn trung bình −17 dB như các video trước.
- Giao diện ở khổ điện thoại: thẻ Unit 1 hiện "Video bài giảng · 4", mỗi video nằm dưới phiên của nó; phiên Bài 1 mở
  `U01-lesson-1.mp4`. Không có lỗi JS.

### Còn treo

- P2-53: Unit 2 và Unit 3 (mỗi unit 4 video), làm tiếp ở các đợt sau.

---

## Đợt 19 — 26/10/2026: Video Giai đoạn 0 — Intro (3 video) và sổ tay làm video từng unit

Nhánh `claude/nifty-darwin-23vvae`, đẩy lên `main`.

Người học: "bắt đầu luôn, xong unit nào commit push lên main unit đó; làm gì thì note lại để unit sau tham khảo". Video
làm như GENKI: giảng tiếng Anh, chữ tiếng Việt trên màn hình, phát audio gốc của sách, mỗi video 5–10 phút; Speaking
và Writing trước, Listening và Reading sau. Đợt này là Intro; Unit 1, 2, 3 mỗi unit một đợt, một commit.

**Ba video Intro** (19:24, giảng: Emma; Tom và Mai làm mẫu)
- `U00-introductions` — Speaking · Introduce yourself (5:51, phiên `U00-intro-1`): nghe sáu người tự giới thiệu (1.1,
  phát từng người), tên nước và ngôn ngữ (từng từ của 1.2), mẫu câu, Mai và Tom giới thiệu, Your turn.
- `U00-letters-numbers` — Listening · Letters, numbers and addresses (7:14, phiên `U00-intro-1`): điền phiếu theo 1.3
  (bảy đoạn), bảng chữ cái theo nhóm âm, đánh vần tên, số nhà, mã bưu chính và số điện thoại (1.4), email và trang web,
  nghe địa chỉ đoán nước (1.5).
- `U00-personal-info` — Grammar · Personal information, my / your, can (6:18, phiên `U00-intro-2`): bài 6–8 trang 9,
  my / your / his / her, can / can't (nghe 1.6), Your turn, tự đánh giá.

**Chép lời bài nghe** (Coursebook bản quét không có phần Scripts)
- Lệnh mới `python -m lesson_video transcribe <sách> 1.1 1.57`: Parakeet TDT 0.6B v2 (int8) qua sherpa-onnx, chạy
  offline. Model tải từ GitHub releases của k2-fsa/sherpa-onnx vì Hugging Face bị chặn.
- Chia đoạn theo khoảng lặng (ffmpeg `silencedetect`), ghi `work/transcripts/<track>.txt` và `.json` có mốc từng từ.
  `start` / `end` của dòng `track` lấy từ mốc này.
- Đã chép 52 track của CD1 (Intro–Unit 4 và Achievement test 1). Tên riêng hay sai, nên đối chiếu với trang sách và Teacher's Book.

**Công cụ video**
- Thanh đầu video ghi tên sách lấy từ `book.json`. Trước đây luôn là "IELTS Target 5.0".

**Sổ tay** (file 08 mục 6, để làm các unit sau): bộ bốn video mỗi unit, giọng, nguồn nội dung, quy trình, quy ước
kịch bản, bảng `say` riêng của sách, lỗi đã gặp, bảng độ phủ.

**Vướng và cách xử lý**
- Kokoro đọc "the sound ay" thành /aɪ/ và "a short e" thành /iː/: viết lại câu ("the same sound as day / ten").
- Kyoto, bows (cúi chào), tên Việt, chữ cái rời, số điện thoại: viết `say` (bảng 6.6).
- Bài đọc một dòng dài bị cắt ở thanh phụ đề: tách mỗi câu một dòng.
- Máy khởi động lại giữa lúc dựng: chạy lại lệnh, tiếng các câu đã đọc lấy từ bộ nhớ đệm.

**Sách A1 đã gỡ khỏi repo.** Người học xoá `books/book_english_unlimited_A1_Starter/` trên `main` (commit `7117894`).
Thẻ A1 trong tab Sách và các tài liệu nay ghi "repo chưa có sách này" thay cho "thư mục đã có Teacher's Book, 2 CD".

### File thêm

| File | Vai trò |
|---|---|
| `agents/lesson_video/transcribe.py` | Lệnh `transcribe`: chép lời audio của sách, có mốc từng từ |
| `books/book_english_unlimited_a2_elemetary/work/transcripts/*.txt`, `*.json` | Lời 52 track CD1 |
| `books/book_english_unlimited_a2_elemetary/lessons/U00-*.yaml`, `U00-*.mp4`, `lessons.json` | Kịch bản và video Intro |

### File sửa

| File | Thay đổi |
|---|---|
| `agents/lesson_video/cli.py`, `agents/pyproject.toml` (`.[asr]`) | Lệnh `transcribe` |
| `agents/lesson_video/slides.py` | Tên sách trên thanh đầu lấy từ `book.json` |
| `agents/tests/test_lesson_video.py` | Test tên sách, hàm thuần của `transcribe`; hồi quy video A2 khớp `lessons.json` |
| `docs/agent-hoc-tap/08-giai-doan-0-a1-a2.md` | Mục 6 (sổ tay video), mục 4 (A1 đã gỡ), bảng đầu |
| `docs/agent-hoc-tap/04-checklist.md` (P2-52, P2-53), `06-video-bai-giang.md`, `docs/agent-hoc-tap/README.md`, `agents/README.md`, `CLAUDE.md` | Lệnh `transcribe`, chỗ để sổ tay, A1 đã gỡ |
| `books/catalog.json`, `README.md`, `00-tong-quan-va-cam-ket.md` | Thẻ A1: repo chưa có sách này |
| `tests/web/book.e2e.mjs` | Bước Giai đoạn 0: thẻ A2 có 3 video; unit Intro có ba nút video 5–10 phút, nút Grammar mở phiên Intro 2 |
| `web/index.html`, `web/ielts-companion.html` | Bản dựng lại |

### Kiểm thử

- `python3 web/build.py && git diff --stat`: bản dựng khớp nguồn; A2 79 phiên, 3 video.
- `cd agents && python -m pytest -q`: 126 test qua (thêm 3: tên sách trên thanh đầu, hàm thuần của `transcribe`, hồi
  quy "video A2 khớp `lessons.json`").
- `node --test "tests/web/*.test.mjs"`: 16 test qua.
- `node tests/web/book.e2e.mjs`: E2E OK. Bước Giai đoạn 0 thêm: thẻ A2 có 3 video; unit Intro có ba nút video dài 5–10
  phút (Speaking, Listening, Grammar); nút Grammar mở phiên Intro 2 với `U00-personal-info.mp4`.
- Giao diện ở khổ điện thoại: unit Intro hiện "Video bài giảng · 3", chia theo hai phiên; phiên Intro 1 có hai video;
  thẻ A1 ghi repo chưa có sách. Không có lỗi JS.

### Còn treo

- P2-53: Unit 1–3 (mỗi unit 4 video), làm tiếp ở các đợt sau.
- P2-52: A1 Starter — repo chưa có sách.

---

## Đợt 18 — 26/10/2026: Giai đoạn 0 — English Unlimited A2 trong tab Sách

Nhánh `claude/nifty-darwin-23vvae`, đẩy lên `main`.

Người học (band 3.0) muốn có một cuốn cho người học khác bắt đầu từ con số 0 tới band 3.5 của IELTS GT. Đề xuất của
đợt trước là Giai đoạn 0 với English Unlimited A1 Starter và A2 Elementary, mốc ra là đề mẫu A2 Key. Người học đẩy
hai bộ sách lên `main` (`books/book_english_unlimited_A1_Starter/`, `books/book_english_unlimited_a2_elemetary/`).

**Hai bộ sách nhận được**

- **A2:** đủ để nhập:
  - Coursebook quét, hai phần, tới trang 121 cùng hai trang Activities;
  - Teacher's Book có lớp chữ;
  - 3 CD, 171 track; CD1 thiếu 5 file;
  - Teacher's Pack và wordlist.
- **A1:** Teacher's Book, 2 CD đủ, Teacher's Pack. Coursebook chỉ là **bản mẫu** 26 trang (mục lục, Unit 3, một phần
  Unit 9), chưa dựng được lộ trình. A1 thành thẻ "chưa nhập" và chờ sách đầy đủ.

**Lộ trình A2: 79 phiên, 16 tuần** (file 08 mục 2)
- Intro: 2 phiên.
- 14 unit × 5 phiên: Bài 1, Bài 2, Target activity, Explore (Speaking ở unit lẻ, Writing ở unit chẵn), Look again.
  Target activity và Explore là phiên lõi.
- Sau Unit 4, 9, 14 (theo Teacher's Book): một phiên ôn với bài nghe Achievement test và các trang Look again của
  chặng.
- 4 phiên đề mẫu A2 Key: đúng khoảng 70% mỗi phần thì sang Giai đoạn 1.
- Mỗi phiên mở đúng trang Coursebook, các track của phần đó, trang Teacher's Book có đáp án; bài nói cặp có thêm
  trang Activities.
- Hướng dẫn mỗi phiên bằng tiếng Việt, lấy theo mục lục sách.
- Thẻ A1 và A2 đứng trước IELTS Target 5.0 trong nhóm IELTS. Tuần của A2 đếm riêng; học xong thì đặt lại ngày bắt
  đầu lộ trình.

**Dò trang và track** (file 08 mục 3)
- **Trang quét trùng.** Part 1 có trang 49 quét hai lần, nên khai hai lần: `course-book` lệch 1, `course-book-u6` lệch
  2. Part 2 lệch −65.
- **Nhãn track.** Mỗi đĩa đánh số lại từ 1, nên `Track No07.mp3` ở CD1 là bài 1.7. Track 01 của mỗi đĩa gồm lời giới
  thiệu đĩa rồi tới bài X.1; đã nghe thử bằng nhận dạng giọng nói thô. Track cuối mỗi đĩa là bài nghe Achievement
  test.
- **Track thuộc trang nào.** Lớp chữ Coursebook chỉ cho 13/176 nhãn. Thay vào đó:
  - lọc vùng màu cam của nhãn audio, cắt từng nhãn rồi OCR;
  - soát bằng mắt khoảng 30 nhãn đọc sai;
  - đối chiếu với "play recording X.Y" dưới từng tiêu đề phần của Teacher's Book: khớp 171/171.

**Agent nhập sách** (`lessons-v1`)
- `files.<thư mục audio>.track: "1.{n}"`: id track lấy số cuối trong tên file. Thiếu thì hai đĩa trùng id "Track-No01"
  và `ingest` báo lỗi, chỉ đúng chỗ cần khai.
- Một PDF khai hai lần với `page_offset` khác nhau. Không cần sửa app: mỗi id có đoạn PDF riêng.
- Ghi chú bước dùng được mọi trường của mục. A2 dùng `{l1}`, `{l2}`, `{ta}`, `{ex}`, `{la}`: phần chung nằm ở bước
  mặc định, phần riêng nằm ở từng unit.
- `report.md` ghi "trang in = trang PDF + 65" khi độ lệch âm. Trước đó bảng in "− -65".

**Vướng và cách xử lý**
- Bước nghe của mốc A2 Key không có track, vì audio nằm trong đề tải về. Luật V4 bắt mọi bước id `listening` phải có
  track, nên bước này đặt id `listening-test`.
- Unit chẵn cần bước Explore Writing. Dùng anchor YAML (`explore-writing: &explore-writing`, `<<: *explore`) thay vì
  chép lại cả năm bước.
- E2E cũ bấm thẻ sách đầu tiên và mặc định đó là IELTS Target 5.0. Nay thẻ đầu là Giai đoạn 0, nên test tìm thẻ theo
  đúng tiêu đề.

### File thêm

| File | Vai trò |
|---|---|
| `books/book_english_unlimited_a2_elemetary/book.yaml` | Hồ sơ lộ trình A2: trang, track, trang Teacher's Book của 79 phiên |
| `books/book_english_unlimited_a2_elemetary/book.json`, `plan.json`, `report.md`, `work/scan.json`, `work/chunks.json` | Gói do `ingest` sinh |
| `books/book_english_unlimited_a2_elemetary/web/*.pdf` | 32 đoạn PDF (Coursebook theo unit, Teacher's Book theo unit, hai trang Activities), 130 MB |
| `docs/agent-hoc-tap/08-giai-doan-0-a1-a2.md` | Thiết kế Giai đoạn 0, cách dò trang và track, A1 đang chờ, kế hoạch video |

### File sửa

| File | Thay đổi |
|---|---|
| `agents/book_ingest/lessons.py` | `track: "1.{n}"` cho thư mục audio; ghi chú bước dùng mọi trường của mục; dấu của độ lệch âm trong báo cáo |
| `agents/tests/test_lessons_template.py` | Test nhãn track theo đĩa và PDF khai hai lần; định dạng `track` sai; hồi quy gói A2 thật |
| `books/catalog.json` | Thẻ A1 (chưa nhập) và A2 trước IELTS Target 5.0; ghi chú nhóm IELTS |
| `tests/web/book.e2e.mjs` | Thứ tự thẻ Giai đoạn 0; bước A2: 19 mục, 79 phiên, phiên Unit 6 mở trang in 50 qua đoạn `course-book-u6`, track 2.15–2.18 phát được |
| `README.md`, `00-tong-quan-va-cam-ket.md` (mục 7), `01-giai-doan-1-nen-tang.md`, `05-tai-lieu-mien-phi.md` (mục K) | Giai đoạn 0 trước tuần 1 |
| `docs/agent-hoc-tap/README.md`, `04-checklist.md` (P2-51, P2-52, P2-53), `agents/README.md`, `.claude/skills/book-ingest/SKILL.md`, `CLAUDE.md` | Giai đoạn 0, tùy chọn mới của `lessons-v1` |
| `web/index.html`, `web/ielts-companion.html` | Bản dựng lại |

### Kiểm thử

- `python3 web/build.py && git diff --stat`: bản dựng khớp nguồn; A2 79 phiên, GENKI 23 video, IELTS 40 video.
- `cd agents && python -m pytest -q`: 123 test qua (thêm 6), gồm hồi quy gói A2 và GENKI (chạy lại ra `book.json`, `plan.json`,
  `report.md` y hệt).
- `node --test "tests/web/*.test.mjs"`: 16 test qua.
- `node tests/web/book.e2e.mjs`: E2E OK, có bước Giai đoạn 0 mới.
- Giao diện ở khổ điện thoại:
  - Thẻ A1 hiện mờ, ghi rõ còn thiếu gì. Thẻ A2 hiện "Elementary · CEFR A1 → A2", 171 track, 79 phiên × 60 phút.
  - Phiên Unit 1 Bài 1 mở trang 10, track 1.7–1.11 phát được.
  - Unit 6 mở trang 50 (sau trang quét trùng), Unit 8 mở trang 66 (Part 2).
  - Activities mở trang 123, Teacher's Book mở trang 90.
  - Achievement test 1 có track 1.57 và bốn nút Look again; nút Unit 3 mở trang 33.
  - Không có lỗi JS.

### Còn treo

- P2-52: A1 Starter chờ Coursebook đầy đủ.
- P2-53: video bài giảng A2, làm Intro và Unit 1–3 trước. Coursebook thiếu phần Scripts, nên lời bài nghe phải chép
  lại từ audio.

---

## Đợt 17 — 26/10/2026: GENKI Unit 0, năm video để học không cần mở sách

Nhánh `claude/nifty-darwin-23vvae`, đẩy lên `main`.

Người học chưa biết gì tiếng Nhật hỏi có nên bắt đầu từ Unit 1 không. Câu trả lời là bắt đầu từ Unit 0 (trang 20–35).
Người học muốn có video cho Unit 0 "để học nhanh, không phải mở sách và audio gốc".

**Năm video**

| Phiên | Video | Dài |
|---|---|---|
| Hệ chữ Nhật & hiragana | Hiragana 1 · 46 chữ cơ bản | 6:22 |
| | Hiragana 2 · ゛゜, âm ghép, っ, trường âm | 6:59 |
| | Katakana · từ vay mượn, âm ngoại lai, làm quen chữ Hán | 7:54 |
| Chào hỏi & số đếm | Greetings · あいさつ | 7:02 |
| | Numbers · すうじ 0–100 | 5:52 |

5 video, 34:09, 21 MB. GENKI có 23 video.

- Mỗi video có đủ bảng chữ hoặc câu chào trên màn hình.
- Audio gốc của sách (JWS-01 … JWS-13, K00-01, K00-02) phát ngay trong video, trên thẻ có đúng bảng chữ đó. Nhãn track
  lấy từ trang sách.
- Mẹo phát âm viết cho người Việt: う gần "ư", え như "ê", っ là một nhịp ngắt, hàng chục đếm như tiếng Việt.
- Bài đố có đáp án: đọc từ, nghe – viết chữ cái và số, 10 tình huống chào hỏi, làm tính.
- Ghi chú hai phiên Unit 0 và lời giới thiệu sách nói video có gì. Workbook (W-JWS1, W00) vẫn là phần làm thêm nếu có sách.

**Công cụ**
- `jpcard`: `\n` trong `jp` / `romaji` là xuống dòng bắt buộc, nên bảng chữ hiện mỗi hàng một dòng, hai hoặc ba cột
  như sách. Trước đó cả bảng hiragana dồn trên ba dòng, các hàng cách nhau bằng `/`.

**Cách đọc tiếng Nhật** (lệnh `check` bắt được hết, chi tiết ở file 07 mục 4.4)
- は, へ đứng riêng bị đọc như trợ từ → `say` viết ハ, ヘ.
- Âm ghép đọc rời bị tách thành hai âm (みょ → mi-yo) → mẫu katakana "キャ。キュ。キョ、", mẫu duy nhất đúng cả 11 hàng.
- フィ đứng riêng thành "fu-i" → để audio gốc đọc các âm ngoại lai.

**Độ dài:** Hiragana 1 ước 5:10 và Numbers ước 4:51 khi viết xong. Thêm phần nghe – viết và phần chữ in khác chữ viết
tay trước khi dựng.

### File thêm

| File | Vai trò |
|---|---|
| `books/Genki/lessons/U00-hiragana-1.yaml`, `U00-hiragana-2.yaml`, `U00-katakana.yaml`, `U00-greetings.yaml`, `U00-numbers.yaml` + `.mp4` | 5 kịch bản và video |

### File sửa

| File | Thay đổi |
|---|---|
| `agents/lesson_video/jpcard.py` | `\n` là xuống dòng bắt buộc |
| `agents/lesson_video/script.py`, `agents/README.md` | Ghi chú `\n` trong thẻ `jp` |
| `agents/tests/test_japanese_video.py` | Test xuống dòng bắt buộc |
| `books/Genki/book.yaml`, `book.json` | Ghi chú hai phiên Unit 0, lời giới thiệu sách |
| `books/Genki/lessons/lessons.json` | Thêm 5 video |
| `books/catalog.json` | Ghi chú lộ trình N5 |
| `tests/web/book.e2e.mjs` | Thẻ GENKI có 23 video; Unit 0 có 5 video Hiragana, Hiragana, Katakana, Greetings, Numbers, mỗi video 5–10 phút |
| `docs/agent-hoc-tap/07-lo-trinh-n5-tieng-nhat.md` | Video Unit 0 ở mục 3.2 và 4.1; `\n` ở mục 4.3; lỗi cách đọc ở mục 4.4 |
| `docs/agent-hoc-tap/README.md`, `04-checklist.md` (P2-50) | Trạng thái đợt 17 |
| `web/index.html`, `web/ielts-companion.html` | Bản dựng lại |

### Kiểm thử

- `python3 web/build.py && git diff --stat`: bản dựng khớp nguồn; GENKI 23 video, IELTS 40 video.
- `cd agents && python -m pytest -q`: 117 test qua, gồm hồi quy "kịch bản khớp `lessons.json`" trên `books/Genki`.
- `node --test "tests/web/*.test.mjs"`: 16 test qua.
- `node tests/web/book.e2e.mjs`: E2E OK. Bước GENKI có kiểm tra mới: Unit 0 có 5 video, mỗi video dài 5–10 phút.
- `python -m lesson_video check ../books/Genki/lessons/*.yaml`: 23/23 OK. Độ dài và kích thước 5 file `.mp4` mới khớp
  `lessons.json`.
- Giao diện:
  - Thẻ Unit 0 ở khổ điện thoại có mục lục 5 video, chia theo hai phiên.
  - Phiên Hệ chữ mở từ nút Hiragana 1 hiện ba video của phiên; bảng chữ hai cột trong video hiện đúng.
  - Phiên Chào hỏi ở khổ máy tính hiện video Greetings và Numbers.
  - Không có lỗi JS.
- Soát khung hình video thật: bảng chữ, thẻ đố, nhãn BOOK AUDIO, furigana trên chữ số.

---

## Đợt 16 — 25/10/2026: GENKI bài 1–3, bốn video kỹ năng 5–10 phút mỗi bài

Nhánh `claude/nifty-darwin-23vvae`, đẩy thẳng lên `main` theo yêu cầu người học.

Người học yêu cầu bốn điều:
- xem lại mỗi bài nên có bao nhiêu video, trước hết là bài 1–3;
- mỗi video dài 5–10 phút;
- làm Speaking và Writing trước, rồi tới Listening và Reading;
- kiểm tra giao diện rồi commit, đẩy lên `main`.

**Quyết định**

Mỗi bài có bốn video, mỗi kỹ năng một video, gắn vào phiên luyện đúng kỹ năng đó:

| Video | Phiên | Nội dung |
|---|---|---|
| Speaking | Part B · Mẫu câu | Điểm ngữ pháp của bài qua câu mẫu (Emma giảng, Yuki / Takeshi đọc), hai đoạn hội thoại của sách, câu hỏi về bản thân |
| Writing | Part C · Nói & viết | Chữ (hiragana / katakana / chữ Hán của bài), ghép câu, đoạn văn mẫu, hội thoại hoặc tin nhắn, chính tả (bài 2–3), lỗi hay gặp, bài tập |
| Listening | Hội thoại & từ vựng | Audio gốc K0u-01…04: nghe hai lần tìm đáp án, đáp án, đọc theo, bản có khoảng lặng để nhắc lại; đố nghe |
| Reading | Đọc – viết | Bài tập 読み書き của sách theo thứ tự, kèm track Y; bài 3 thêm mẹo đọc câu không có dấu cách và đố đúng / sai |

- Part A (ngữ pháp) không có video riêng. Từng điểm ngữ pháp được giảng bằng câu mẫu trong Speaking và Writing; ghi chú
  phiên Part A nói rõ điều này.
- Bỏ 9 tập 27–43 giây của bài 1–3, vì nội dung đã nằm trong video mới và tập ngắn trái yêu cầu 5–10 phút. Bài 4–5 giữ
  6 tập cũ đến khi làm theo khung mới (P2-48).
- Listening phát nguyên track hội thoại, không cắt từng câu, vì không nghe được để soát ranh giới câu.
- Không chèn khoảng lặng dài: người học tự dừng video (ý người học ở đợt 14). Phần nhắc lại dùng bản ghi có khoảng
  lặng của chính sách (K0u-02, K0u-04).

**Kết quả**

| Bài | Speaking | Writing | Listening | Reading | Tổng |
|---|---|---|---|---|---|
| 1 New Friends | 8:07 | 5:31 | 7:20 | 8:29 | 29:26 |
| 2 Shopping | 6:12 | 5:49 | 9:05 | 6:22 | 27:28 |
| 3 Making a Date | 6:06 | 5:56 | 8:42 | 6:45 | 27:28 |

- 12 video, 1:24:22, 59 MB, 7–11 chương mỗi video.
- GENKI có 18 video, gồm cả 6 tập ngắn của bài 4–5.

**Công cụ `lesson_video`**
- Cảnh `jp` có nhiều thẻ. Dòng thoại chọn thẻ bằng `focus`; thanh tiêu đề hiện số thẻ `k/n`.
- Dòng `track` trong cảnh `jp`: phát file nghe của sách, thay nhãn người nói bằng nhãn teal "BOOK AUDIO · K01-01".
- Thẻ đề `quiz: true` không bị kiểm cách đọc và được để chữ Hán không furigana, dùng cho đố nghe và bài đọc giá tiền.
- `check` kiểm cách đọc theo từng thẻ. Một thẻ đạt khi mỗi câu đọc trọn thẻ, hoặc các câu ghép lại thành thẻ.
- `ja.py`:
  - romaji kiểu GENKI (`gakusee`, `Soo desu ka`) khớp nhờ chuẩn hóa `ei` = `ee`, `ou` = `oo`;
  - は / へ cuối từ (こんにちは) lấy theo cách phát âm của unidic;
  - số khoanh ①–⑦ vẽ bằng phông CJK.
- Lệnh `prune <sách>` bỏ khỏi `lessons.json` và xóa `.mp4` của video không còn kịch bản.

**Lỗi gặp trong đợt** (chi tiết ở file 07 mục 4.4)
- misaki đọc sai một số từ: 日本人, アメリカ人, 四時, いま何時, 何を, 土曜日, 明日, 時 đứng một mình. Sửa bằng kana trong câu
  thoại hoặc `say`.
- Hiragana さんびゃく bị tách thành さん / び / ゃ / く, nên giọng đọc sai. `check` bắt được vì romaji không khớp. Câu thoại
  đổi sang 三百.
- Ba video ra ngoài khung 5–10 phút:
  - U02-writing dựng lần đầu chỉ 3:56. Thêm cảnh viết số bằng hiragana và cảnh chính tả.
  - U03-writing ước 4:20, U03-reading ước 5:12. Thêm nội dung trước khi dựng: thứ tự nét và chính tả; mẹo đọc và đố
    đúng / sai.
  - U02-listening ước 9:45. Bỏ một lần phát lại hội thoại II.
- Soát khung hình video thật thấy thẻ ngắt dòng xấu:
  - "Q2." hay "5." treo cuối dòng;
  - cặp オランダ — アムステルダム bị tách;
  - dòng bắt đầu bằng `/` hay `・`;
  - "か。" rơi một mình xuống dòng;
  - chữ Latin xuống dòng sớm một từ.

  Sửa bằng quy tắc ngắt dòng mới trong `jpcard` (file 07 mục 4.3) và vạch ` / ` giữa các câu hỏi, các mục đánh số,
  rồi dựng lại cả 12 video.

### File thêm

| File | Vai trò |
|---|---|
| `books/Genki/lessons/U0u-speaking.yaml`, `U0u-writing.yaml`, `U0u-listening.yaml`, `U0u-reading.yaml` (u = 1–3) + `.mp4` | 12 kịch bản và video |

### File sửa

| File | Thay đổi |
|---|---|
| `agents/lesson_video/script.py` | Cảnh `jp` nhiều thẻ, `track` trong cảnh `jp`, thẻ `quiz`, kiểm cách đọc theo thẻ |
| `agents/lesson_video/jpcard.py` | Số thẻ `k/n`, nhãn "BOOK AUDIO" khi phát file nghe của sách. Ngắt dòng: vạch ngăn `\|` `/` `・` trước `—`, số thứ tự đi cùng phần sau, dòng Latin đầy, tránh dòng cuối quá ngắn |
| `agents/lesson_video/ja.py` | Số khoanh dùng phông CJK, romaji kiểu GENKI, は / へ cuối từ theo cách phát âm |
| `agents/lesson_video/video.py`, `cli.py` | `prune_manifest`, lệnh `prune` |
| `agents/tests/test_japanese_video.py` | Cảnh nhiều thẻ + audio sách (vẽ nhãn, số thẻ), kiểm cách đọc theo thẻ, thẻ đề, `focus` ngoài số thẻ, romaji GENKI, こんにちは, ngắt dòng thẻ, tránh dòng cuối quá ngắn (33 test) |
| `agents/tests/test_lesson_video.py` | Hồi quy "kịch bản khớp `lessons.json`" chạy cho cả `books/Genki`; test `prune` |
| `books/Genki/book.yaml`, `book.json` | Lời giới thiệu sách; ghi chú phiên bài 1–3 nói video nào có gì |
| `books/Genki/lessons/lessons.json` | Thêm 12 video, bỏ 9 tập cũ |
| `books/catalog.json` | Ghi chú lộ trình N5 |
| `tests/web/book.e2e.mjs` | Thẻ GENKI có 18 video; Unit 1 có 4 video Listening, Speaking, Writing, Reading, mỗi video 5–10 phút; nút Speaking mở phiên Part B |
| `docs/agent-hoc-tap/07-lo-trinh-n5-tieng-nhat.md` | Mục 4 viết lại: độ phủ, cách làm video, cảnh `jp` nhiều thẻ, lỗi, kế hoạch bài 4–12 theo khung bốn kỹ năng |
| `docs/agent-hoc-tap/README.md`, `04-checklist.md` (P2-47, P2-48, P2-49), `agents/README.md`, `CLAUDE.md` | Trạng thái đợt 16, lệnh `prune` |
| `web/index.html`, `web/ielts-companion.html` | Bản dựng lại |

### File xóa

`books/Genki/lessons/EP_01_01` … `EP_03_03` (`.yaml` và `.mp4`, 9 tập).

### Kiểm thử

- `python3 web/build.py && git diff --stat`: bản dựng khớp nguồn; GENKI 18 video, IELTS 40 video.
- `cd agents && python -m pytest -q`: 117 test qua, gồm hồi quy "kịch bản khớp `lessons.json`" trên cả sách IELTS và
  `books/Genki`.
- `node --test "tests/web/*.test.mjs"`: 16 test qua.
- `node tests/web/book.e2e.mjs`: E2E OK, bước GENKI mới (18 video; Unit 1 có 4 video dài 5–10 phút; nút Speaking mở
  phiên Part B).
- `python -m lesson_video check ../books/Genki/lessons/*.yaml`: 18/18 OK. Độ dài và kích thước của cả 18 file `.mp4`
  khớp `lessons.json`.
- Giao diện: chụp tab Sách ở khổ điện thoại (390 px) và máy tính (1280 px). Đã xem thẻ GENKI, thẻ Unit 1–4 với mục lục
  video và phiên mở từ nút video (khung video, chương). Không có lỗi JS.

### Còn treo

- P2-48: video bài 4–12 theo khung bốn kỹ năng (bài 4–5 thay 6 tập ngắn).
- Đáp án Workbook: cần GENKI Answer Key.

---

## Đợt 15 — 25/10/2026: lộ trình tiếng Nhật JLPT N5 với GENKI I, đánh giá bản thiết kế video, 15 video bài 1–5

Nhánh `claude/nifty-darwin-23vvae`. Giữa đợt đã merge `main` tại `99408f5`: người học thêm GENKI I (3rd Edition)
Textbook, Workbook và audio vào `books/Genki/`.

### Yêu cầu

1. Tích hợp GENKI vào menu Sách và thêm lộ trình N5 tiếng Nhật.
2. Dựng video theo bản thiết kế "MASTER BLUEPRINT: GENKI I (3rd Ed.) × IELTS Target 5.0 Video Pipeline": 15 tập cho
   bài 1–5, kèm hai script Python. Đánh giá lại ý tưởng này.
3. Sau khi người học thêm sách và audio vào `main`: dùng thẳng các file đó. Người học xác nhận bộ sách dùng công khai,
   không cần lo bản quyền.

### Đã làm

**Đánh giá bản thiết kế** — [07-lo-trinh-n5-tieng-nhat.md](07-lo-trinh-n5-tieng-nhat.md) mục 1–2.
- Giữ ba tầng chữ Nhật — Anh — Việt kèm Hán-Việt và việc nối ngữ pháp với chủ đề IELTS.
- Sửa số thứ tự điểm ngữ pháp ở 7 tập cho khớp mục lục sách, cùng vài câu sai nghĩa.
- Không dùng hai script của bản thiết kế, vì:
  - tải model từ Hugging Face;
  - phông chỉ có trên macOS;
  - cắt chữ theo số ký tự, không có furigana;
  - ghép từng đoạn nên lệch tiếng;
  - JSON nằm trong Markdown.
- Bù chỗ yếu về sư phạm:
  - tập chỉ 30–45 giây;
  - không dạy kana;
  - dựa vào romaji;
  - N5 không thi nói – viết.

**Lộ trình N5** — file 07 mục 3.
- `books/catalog.json` có `courses`. Tab Sách gom sách theo lộ trình; trình độ "JLPT N5 · CEFR A1"; nhịp 3–5 phiên/tuần.
- Mẫu `lessons-v1` của agent nhập sách: các bước học và chỗ trong sách của từng bước khai hết trong `book.yaml`.
  - `refs: {<bước>: {pdf, pages, tracks, alt}}` — trang là số in.
  - `tracks` nhận id hoặc khoảng `A..B`.
  - Id track lấy từ tên file: `K01_05.mp3` → `K01-05`, đúng nhãn in trong sách.
  - Agent quét file, cắt PDF thành đoạn theo từng bài, kiểm tra mỗi track thuộc đúng một phiên.
  - Bản đầu của mẫu chưa có file sách: lộ trình chỉ có ghi chú. Khi sách vào `main` thì thêm `files` / `refs`.
- `books/Genki/book.yaml` có:
  - Unit 0: hệ chữ, chào hỏi, số đếm;
  - 12 bài × 6 phiên: Hội thoại & từ vựng, Part A ngữ pháp, Part B luyện tập, Part C ôn tập & nói – viết, Đọc – viết,
    Workbook;
  - 4 phiên ôn thi N5.

  Tổng 78 phiên ≈ 79 giờ, 20 tuần ở 4 phiên/tuần. Có 286 track (461 phút), PDF cắt thành 51 đoạn (70 MB).
- Ranh giới các phần của 12 bài dò bằng OCR (RapidOCR) trang Textbook PDF 36–302: nhãn track và đầu mục Grammar /
  Practice / まとめの練習 / Culture Notes / Useful Expressions. Mọi trang chuyển phần đã soát bằng mắt. Vị trí W00,
  W02-1, WY-1…8, W-JWS1/2 lấy từ OCR các trang Workbook liên quan.
- Ghi chú phiên đổi từ "nghe bằng app OTO Navi" sang "nghe track của bài". Danh sách ngữ pháp bài 6–12 và chữ Hán
  từng bài lấy theo mục lục sách.

**Video** — file 07 mục 4.
- `lesson_video` đọc được tiếng Nhật:
  - cảnh `jp`: thẻ navy ba tầng có furigana `{漢字|かな}`, romaji, tiếng Anh, tiếng Việt;
  - người nói `lang: ja` dùng giọng Kokoro `jf_alpha`, tách âm bằng `misaki[ja]`;
  - `speed` theo người nói hoặc từng dòng;
  - lệnh `check` so cách đọc của bộ đọc với furigana, so romaji, chặn chữ Latin trong câu Nhật.
- 15 kịch bản `books/Genki/lessons/EP_0u_0p.yaml` giữ lời thoại, chữ, tốc độ, khoảng lặng của bản thiết kế. Đã sửa
  nội dung, sửa cách đọc tiếng Nhật (九時, 二十八歳, 日本語, 七時, 日曜日, IT…) và cách đọc từ Nhật trong lời Emma.
- Kết quả: 15 video, 9:20 (27–46 giây mỗi tập), 0,3–0,6 MB mỗi tập.
- Model Kokoro và giọng `bf_emma`, `jf_alpha` lấy từ bản đăng lại trên npm vì máy dựng chặn Hugging Face (xem
  `agents/README.md`).

**Hai lỗi sửa trong đợt**
- **Video dài hơn tiếng.** EP 2.3, 3.3, 4.3 hỏng ở lần dựng đầu: video dài hơn tiếng 3–8 giây vì `loudnorm` giữ
  ~3 giây tiếng nên `-shortest` không cắt được. Nay chuẩn độ to ở lệnh ffmpeg riêng. Video IELTS dựng về sau cũng
  theo cách này; các video đã commit không đổi.
- **Nút "Tapescript của track" vẫn hiện** khi track không có tapescript. Nguyên nhân: `.btn{display:inline-flex}`
  đè thuộc tính `hidden`. Lỗi có từ trước, sách GENKI làm lộ ra.

### File thêm

| File | Vai trò |
|---|---|
| `agents/book_ingest/lessons.py` | Mẫu `lessons-v1`: đọc `book.yaml` (bước, `files`, `pages`, `refs`), mở rộng khoảng track, ranh giới đoạn PDF theo mục, dựng `book.json` / `plan.json` / `report.md` |
| `agents/lesson_video/ja.py` | Furigana, cách đọc kana, romaji (trợ từ は/へ/を), gọi `misaki[ja]`, kiểm tra một câu |
| `agents/lesson_video/jpcard.py` | Vẽ cảnh `jp` 1280×720: chữ trộn CJK + Latin, furigana, ngắt dòng có kinsoku, tự co chữ |
| `agents/tests/test_japanese_video.py` | 27 test: furigana, romaji, kiểm tra cảnh `jp`, vẽ, tốc độ, khóa bộ nhớ tiếng, đọc tiếng Nhật bằng Kokoro |
| `agents/tests/test_lessons_template.py` | 19 test: mẫu không file, mẫu có file (trang in → PDF, khoảng track, đoạn PDF, nhãn trang Workbook), 8 kiểu `refs` sai, hồi quy trên `books/Genki` |
| `books/Genki/book.yaml`, `book.json`, `plan.json`, `report.md`, `work/scan.json`, `work/chunks.json`, `web/*.pdf` | Lộ trình N5 và 51 đoạn PDF |
| `books/Genki/lessons/EP_*.yaml`, `EP_*.mp4`, `lessons.json` | 15 kịch bản và video |
| `docs/agent-hoc-tap/07-lo-trinh-n5-tieng-nhat.md` | Đánh giá bản thiết kế, lộ trình, video tiếng Nhật, kế hoạch Unit 6–12 |

### File sửa

| File | Thay đổi |
|---|---|
| `agents/book_ingest/pipeline.py` | Nhánh `lessons-v1`: quét file (nếu có), cắt đoạn PDF, đóng gói, kiểm tra |
| `agents/book_ingest/validate.py` | `lessons-v1`: mỗi hoạt động đúng một phiên |
| `agents/book_ingest/schemas.py`, `schemas/book.schema.json` | `BookInfo.course`, `BookInfo.level` (tùy chọn — `book.json` của IELTS không đổi) |
| `agents/lesson_video/script.py` | Kiểu cảnh `jp`, `lang` và `speed` của người nói, `speed` của dòng, kiểm tra tiếng Nhật |
| `agents/lesson_video/tts.py`, `timeline.py` | Kokoro đọc tiếng Nhật qua phiên âm misaki; tốc độ riêng từng câu (vào khóa bộ nhớ tiếng) |
| `agents/lesson_video/slides.py` | Phông `jp` / `jp-bold` (Noto Sans CJK), chuyển cảnh `jp` sang `jpcard` |
| `agents/lesson_video/video.py` | Chuẩn độ to ở bước riêng (sửa video dài hơn tiếng) |
| `agents/lesson_video/coverage.py` | Cột trang ghi "Workbook tr." cho hoạt động trên Workbook |
| `agents/pyproject.toml` | Extra `ja = ["misaki[ja]>=0.7.4"]` |
| `books/catalog.json` | `courses` (`ielts`, `ja-n5`) và sách `genki-1-n5` |
| `web/src/book/core.js` | `courseOf`, `groupCourses`, `levelText` (band hoặc JLPT), `paceOptions` |
| `web/src/book/ui.js` | Danh sách sách theo lộ trình; nội dung sách bỏ số 0, thêm số video; nhịp học, câu "học xong" và cảnh báo chậm theo lộ trình / `plan.rules`; thẻ quản lý file chỉ hiện khi sách có file; giờ học không tự cộng cho lộ trình ngoài IELTS |
| `web/src/book/book.css` | `.btn[hidden]{display:none}` |
| `tests/web/book-core.test.mjs` | Gom theo lộ trình, trình độ, nhịp; gói GENKI: trang in, track từng phiên, mỗi track thuộc đúng một hoạt động, mọi trang nằm trong một đoạn, mọi file cần có tồn tại |
| `tests/web/book.e2e.mjs` | Bước mới: thẻ GENKI (286 track, 15 video), thẻ Unit 1 "Trang 36–55", nút video EP 1.2 mở phiên Part B: "Mở trang 46–53", 15 track K01-09…K01-23, không có nút Tapescript, tải đoạn `course-book-p0044-0063.pdf` |
| `docs/agent-hoc-tap/README.md`, `04-checklist.md` (P2-46, P2-47, P2-48), `agents/README.md`, `.claude/skills/book-ingest/SKILL.md`, `web/README.md`, `CLAUDE.md` | Lộ trình N5, mẫu `lessons-v1`, video tiếng Nhật |
| `web/index.html`, `web/ielts-companion.html` | Bản dựng lại |

### File xóa

`books/genki_1_n5/` (bản đầu của lộ trình, chưa có file sách) chuyển vào `books/Genki/` cạnh PDF và audio.

### Kiểm thử

- `python3 web/build.py && git diff --stat`: bản dựng khớp nguồn.
- `cd agents && python -m pytest -q`: 109 test qua, gồm hồi quy trên sách IELTS thật và trên `books/Genki`.
- `node --test "tests/web/*.test.mjs"`: qua.
- `node tests/web/book.e2e.mjs`: E2E OK, có bước GENKI mới.
- `python -m lesson_video check ../books/Genki/lessons/*.yaml`: 15/15 OK. Độ dài mọi video khớp tiếng: video ngắn hơn
  tiếng dưới 0,07 giây.

### Còn treo

- P2-48: video Unit 6–12.
- Đáp án Workbook: cần GENKI Answer Key.
- Đề mẫu JLPT N5 kèm file nghe để vào sách thì khối ôn thi có trang và track.

---

## Đợt 14 — 19/10/2026: 4 video luyện nói thêm Unit 1 (hỏi đáp qua lại, thi thử Speaking)

Nhánh `claude/gallant-ramanujan-ym30oy` đặt lại từ `main` tại `930feee` (đã merge PR #14); xong thì đẩy thẳng lên `main`
theo yêu cầu người học.

### Yêu cầu

1. Người học đang luyện Speaking Unit 1 (chủ đề Life) và muốn một video khoảng 10 phút. Trong video, Tom và Emma hỏi
   đáp qua lại, đóng vai một buổi thi thử Speaking, và người học shadowing được giọng của cả hai.
2. Sau khi xem bản đầu: không cần phần nghe – nhắc lại, vì người học tự tạm dừng video để nói. Chủ yếu cần **càng
   nhiều nội dung càng tốt** để luyện.
3. Commit, đẩy lên `main`, và bảo đảm giao diện hiện các video sau khi sửa.

### Đã làm

Bản đầu (một video 10:22) có các phần: hỏi đáp, thi thử Phần 1–3, nghe – nhắc lại 8 câu (cảnh `shadow`, khoảng lặng
`echo`) và lượt thi thử chờ 15 giây mỗi câu. Theo góp ý của người học, bản cuối bỏ mọi khoảng lặng chờ và mở rộng thành
**4 video, 35:24, 27 chương**. Có 115 cặp hỏi – đáp (tính cả câu thi thử Phần 1 và 16 câu Phần 3) và 5 bài nói mẫu Phần 2 hiện chữ theo đoạn. Tom và Emma thay nhau
làm giám khảo, nên cả hai giọng đều có câu trả lời mẫu để shadow. Câu trả lời mẫu tự viết bằng từ vựng Unit 1. Thông tin
nhân vật giữ khớp ở cả 4 video và các video Unit 1 trước (ghi ở đầu `U01-speaking-practice.yaml`).

| Video | Hỏi qua lại | Thi thử |
|---|---|---|
| `U01-speaking-practice` Speaking practice 1 (8:45, 6 chương) | Gia đình (8 cặp), nơi ở và quê nhà (8) | Emma giám khảo, Tom thí sinh: Phần 1 (8 câu), Phần 2 "an older person in your family who you admire" (thẻ đề, ghi chú, bài nói 123 từ), Phần 3 (4 câu) |
| `U01-speaking-practice-2` Speaking practice 2 (9:21, 7 chương) | Tuổi thơ (8), thời gian rảnh (8), việc học và công việc (6) | Đổi vai, Tom giám khảo, Emma thí sinh: Phần 1 (7 câu), Phần 2 "a happy memory from your childhood", Phần 3 (4 câu) |
| `U01-speaking-practice-3` Speaking practice 3 (9:49, 8 chương) | Các giai đoạn cuộc đời (8), sinh nhật, Tết, lễ hội (8), bạn bè (6), tương lai (4) | Cùng một thẻ đề Phần 2 "a family celebration that you enjoyed" do hai người trả lời: Tom kể Tết, Emma kể kỷ niệm 50 năm ngày cưới của ông bà. Phần 3 hỏi hai chiều |
| `U01-speaking-practice-4` Speaking practice 4 (7:29, 6 chương) | Sinh hoạt hằng ngày (8), tên gọi (6), ảnh (6) | Phần 2 "a friend you have known for a long time" (Tom), Phần 3 hỏi hai chiều |

Mỗi câu hỏi hiện trước ("Think: how would you answer?") rồi mới mở câu trả lời, kèm cụm từ hay dùng và phụ đề tiếng Việt.
Đó là chỗ để người học tạm dừng tự trả lời; trong app có thể bấm "Lặp chương này" để luyện một chương nhiều lần.

Soát cách đọc bằng phiên âm của Kokoro, viết lại trong `say`:
- **Từ đồng tự:**
  - "My family lives", "My grandfather lives" → `livz`;
  - "often live with", "young couples live on their own" → `liv`;
  - "record yourself" → `re-cord`;
  - "Use the right tense" → `Yooz`;
  - "I'm used to it" → `yoost`;
  - "close my eyes" → `cloze`.
- **Tên riêng:** Tran Minh Tuan → `Chan Min Twan`, Khoa → `Kwah`, Nguyen → `Win`.

Lần dựng đầu, phông thiếu glyph "↘" nên hiện thành ô vuông. Đã đổi sang chữ, và giờ dò ký tự ngoài ASCII trước khi dựng.

### Công cụ `lesson_video`

| Thêm / sửa | Cách làm |
|---|---|
| Cảnh `shadow` | Danh sách câu (đầu cảnh), rồi từng câu chữ to trong thẻ màu người nói (`by`), nghĩa `vi`, mẹo `tip` ở đáy; tới lượt người học thì viền đỏ và đồng hồ "Now you!" (bản cuối của video không dùng; công cụ giữ cho video sau) |
| Dòng `echo: true` | Sau câu thoại, tự thêm khoảng lặng đếm ngược ⌈1,3 × độ dài câu + 1⌉ giây (ít nhất 3) với lời nhắc "Your turn — repeat after Tom"; `note` thay lời nhắc; chỉ dùng cho câu thoại, không dùng trong `letter` |
| Đếm ngược | Gom thành một hàm dùng chung cho `wait` và `echo` |
| Cảnh `letter` có `roles` | Nhãn góc trang "Tom · candidate — đang nói" thay "Tom is reading" (bài nói mẫu trong thi thử); video cũ không đổi vì chưa cảnh `letter` nào có `roles` |
| Kiểm tra cảnh `qa` | Dòng `reveal` phải do đúng người trả lời ghi trên thẻ (`by`, mặc định người nói cuối). Lỗi này lộ ra ở bản dựng đầu: ba cảnh Tom làm giám khảo ghi "Tom:" cho câu Emma trả lời. Đã thêm `ask` / `by` rồi dựng lại; mọi kịch bản cũ đều qua kiểm tra |

### File thêm

| File | Vai trò |
|---|---|
| `books/ielts_target_5_0/lessons/U01-speaking-practice.yaml`, `-2`, `-3`, `-4` (+ `.mp4`) | Kịch bản và video |

### File sửa

| File | Thay đổi |
|---|---|
| `agents/lesson_video/script.py` | Kiểu cảnh `shadow`, trường `echo`; kiểm tra người trả lời trong cảnh `qa` |
| `agents/lesson_video/timeline.py` | `echo_seconds()`, hàm đếm ngược dùng chung |
| `agents/lesson_video/slides.py` | `_k_shadow`; nhãn vai trong cảnh `letter` |
| `agents/tests/test_lesson_video.py` | +6 test (`echo` + `shadow` dựng và vẽ được; 4 kịch bản sai bị chặn; thẻ `qa` ghi sai người trả lời bị chặn) |
| `books/ielts_target_5_0/lessons/lessons.json` | Thêm 4 mục luyện nói |
| `tests/web/book-core.test.mjs`, `tests/web/book.e2e.mjs` | Unit 1: 17 video; phiên Speaking & Vocabulary có 7 video; bước mới: nút "Speaking practice 4" trên thẻ unit mở đúng phiên, đủ 4 video luyện nói theo thứ tự, có nút chương, máy chủ trả MP4 |
| `docs/agent-hoc-tap/06-video-bai-giang.md` | Bảng độ phủ Unit 1; 4 dòng lịch sử; bảng lịch sử xếp lại theo unit (các dòng Unit 3 từng chèn giữa Unit 1 và Unit 2); `shadow`, `echo`; cách đọc mới; lỗi đã gặp (từ đồng tự theo ngữ cảnh, glyph thiếu, video luyện nói không chờ) |
| `agents/README.md`, `web/README.md`, `docs/agent-hoc-tap/04-checklist.md`, `README.md` (thư mục docs) | `shadow`, `echo`; 4 video luyện nói; task P2-45; trạng thái |
| `web/index.html`, `web/ielts-companion.html` | Bản dựng lại |

Không xóa file nào.

### Kiểm thử

| Lệnh | Kết quả |
|---|---|
| `cd agents && python -m pytest -q` | 63 passed (+6: `echo` + `shadow`, 4 kịch bản sai bị chặn, thẻ `qa` ghi sai người trả lời bị chặn; hồi quy 40 kịch bản khớp `lessons.json`) |
| `node --test "tests/web/*.test.mjs"` | 14 passed (Unit 1: 17 video, nhóm Speaking & Vocabulary có 7 video đúng thứ tự) |
| `node tests/web/book.e2e.mjs` | 15/15 bước OK. Thẻ Unit 1 có 17 video, phiên Speaking & Vocabulary có 7 video. Bước mới: nút "Speaking practice 4" mở đúng phiên, đủ 4 video luyện nói theo thứ tự, có nút chương, máy chủ trả 206 khi tua |
| Ảnh chụp tab Sách (Playwright, 420 px) | Thẻ Unit 1 hiện "Speaking practice 1–4" kèm thời lượng; phiên học hiện video với các nút chương |
| `ffprobe` / `volumedetect` / khung hình trích từ MP4 | 4 video, tổng 35:24, 27 chương; tiếng trung bình −17,1 đến −17,4 dB, đỉnh ≤ −0,7 dB. Bản dựng đầu ghi "Tom:" trên thẻ câu trả lời của Emma ở ba cảnh đổi vai; đã sửa (`ask` / `by` + kiểm tra mới), dựng lại và soát lại khung hình |
| Soát cách đọc, dò ký tự | 7 từ đồng tự và 3 tên riêng viết lại trong `say` (xem trên); mạo từ "A" đầu câu đọc đúng /ɐ/; không còn ký tự thiếu glyph |

### Còn treo

- Unit 4 trở đi (kế hoạch ở file 06 mục 8).
- Video luyện nói thêm cho Unit 2, 3 nếu người học cần (làm theo mẫu 4 video này).

---

## Đợt 13 — 07/10/2026: nghe / xem lặp lại

Nhánh `claude/gallant-ramanujan-ym30oy` đặt lại từ `main` tại `b6b1b51` (đã merge PR #13).

### Yêu cầu

Thêm cơ chế lặp khi xem video / nghe file MP3, để học nghe đi nghe lại trong thời gian dài; xong thì tạo PR.

### Đã làm

Tab Sách, trong phiên học: thanh audio và danh sách video của mỗi hoạt động có thêm hàng **Lặp lại**.

| Phần | Cách chạy |
|---|---|
| Chế độ lặp | **Tắt** (phát một lần) · **Track này / Video này** (hết bài thì phát lại từ đầu) · **Cả N track / Cả N video** (hết bài thì sang bài sau, hết bài cuối thì quay về bài đầu). Audio chuyển track rồi phát tiếp luôn, kể cả khi màn hình khóa; video cuộn tới video sau rồi phát |
| Hẹn giờ dừng | Không hẹn giờ, 15 / 30 / 45 phút, 1 giờ, 1 giờ 30, 2 giờ, 3 giờ — đổi hẹn giờ thì tính lại từ lúc đó; hết giờ thì dừng và báo "Đã dừng theo hẹn giờ …" |
| Dòng trạng thái | Số lượt đã nghe hết (cả lượt quay về A), thời gian nghe lần này (còn bao lâu nếu có hẹn giờ), thời gian nghe **cả ngày** — dùng chung mọi thanh trên trang |
| Đoạn A–B | Video cũng có A / B (trước chỉ có audio); đặt lại A thì xóa B cũ (trước đây B cũ nằm trước A mới sẽ làm audio nhảy liên tục) |
| Lặp chương | Nút *Lặp chương này* trên mỗi video: lặp chương đang xem; đang lặp chương mà bấm chương khác thì lặp chương đó |
| Một bài một lúc | Phát một audio / video thì các bài khác trên trang tự dừng |
| Màn hình khóa | Nút bài trước / bài sau (Media Session) chuyển bài trong danh sách vừa phát (track audio hoặc video) |
| Ghi nhớ | Chế độ lặp và hẹn giờ nhớ riêng cho audio / video (`<LS>:repeat:audio`, `<LS>:repeat:video`); thời gian nghe trong ngày ở `<LS>:<slug>:listen`. Mỗi lần cộng tối đa 2 phút, để máy ngủ giữa chừng không làm số vọt lên |

### File sửa

| File | Thay đổi |
|---|---|
| `web/src/book/core.js` | Hàm thuần `nextOnEnd` (bài phát tiếp theo chế độ), `sleepLeft` (hẹn giờ), `addListen` (cộng thời gian nghe theo ngày), `chapterRange` (khoảng của một chương), `fmtHms` (giờ:phút:giây) |
| `web/src/book/ui.js` | `repeater()` (hàng Lặp lại dùng chung cho audio và video), `abLoop()` (đoạn A–B, lặp chương); thanh audio dùng hai hàm này; nút bài trước / bài sau trên màn hình khóa theo danh sách vừa phát; `videoBox()` có hàng A–B / lặp chương; phiên học tạo một thanh lặp cho danh sách video của mỗi hoạt động |
| `web/src/book/book.css` | Kiểu cho hàng Lặp lại, ô hẹn giờ, hàng A–B |
| `tests/web/book-core.test.mjs` | +1 test các hàm lặp |
| `tests/web/book.e2e.mjs` | +1 bước: lặp track, lặp cả 3 track (quay vòng về track đầu), A–B, hẹn giờ dừng (cho đồng hồ trang chạy nhanh), lặp chương video, nhớ chế độ |
| `web/README.md` | Mục *Nghe / xem lặp lại*; mô tả tab Sách |
| `docs/agent-hoc-tap/04-checklist.md`, `README.md` (thư mục docs) | Task P2-44; trạng thái |
| `web/index.html`, `web/ielts-companion.html` | Bản dựng lại |

Không thêm, không xóa file nào.

### Kiểm thử

| Lệnh | Kết quả |
|---|---|
| `node --test "tests/web/*.test.mjs"` | 14 passed (+1: bài phát tiếp, hẹn giờ, cộng thời gian theo ngày, khoảng chương, giờ:phút:giây) |
| `node tests/web/book.e2e.mjs` | 15/15 bước OK. Bước mới: Track này phát lại từ đầu (1 lượt); Cả 3 track đi 1 → 2 → 3 → 1 (4 lượt); A–B quay về A; hẹn giờ 15 phút dừng phát; thời gian nghe trong ngày tăng đúng; Lặp chương 0:00 → 0:18, bấm chương khác thì lặp chương đó |
| `cd agents && python -m pytest -q` | 57 passed (không đổi) |
| Ảnh chụp bề ngang 390 px và 1100 px | Nhãn ngắn (Tắt / Track này / Cả 3 track) không xuống dòng; A–B nằm hàng riêng |

### Còn treo

- Unit 4 trở đi (kế hoạch ở file 06 mục 8).

---

## Đợt 12 — 07/10/2026: 11 video Unit 3

Nhánh `claude/gallant-ramanujan-ym30oy` đặt lại từ `main` tại `80e0a4c` (đã merge PR #12).

### Yêu cầu

Tiếp tục làm video cho Unit 3, xong thì tạo PR.

### Đã làm

Làm theo kế hoạch Unit 3 ở [06-video-bai-giang.md](06-video-bai-giang.md) (viết ở đợt 10). Khác kế hoạch: Exam practice
có Listening và Reading (không có Writing) nên hai video luyện đề là `U03-exam-listening` và `U03-exam-reading`; file
nghe Track 37 không có trong bộ sách nên đọc lại bằng bốn giọng. Unit 3 có video cho **mọi phần có trang sách** — 11 video, tổng 1:09:08, 95 chương.

| Phần | Video | Nội dung |
|---|---|---|
| Speaking & Vocabulary | `U03-speaking-1` (7:22, 11 chương) | Bốn ảnh nghề (xếp lưới 2×2), bài nói mẫu 1 phút về ảnh c dùng cụm trong khung, đến lượt bạn, 8 tên nghề (Track 28 đọc lại) và trọng âm, work as / for / in / with, nói về công việc của bạn, 6 tính từ P/N, *Watch out!* (an engineer, a good job) |
| | `U03-speaking-2` (7:26, 12 chương) | Ba câu hỏi về nghề, Grammar check would / could, nối âm would you / could you, *Watch out!*, Exam tip Phần 2, hai thẻ đề, chia 1 + 2 phút, ghi chú từ khóa và **bài nói mẫu 172 từ** (thẻ B, mỗi ý một đoạn), đến lượt bạn với thẻ A (1 phút chuẩn bị, 1 phút nói, tạm dừng nếu cần thêm) |
| Listening | `U03-listening-1` (8:29, 10 chương) | Gist là gì, nhìn tranh, **phát Track 31**, nối 4 đoạn (a 2 · b 4 · c 1 · d 3), cách làm, điền đoạn văn (topic · details · word · skimming), Exam tip đoán trước, đoán từ 4 hình, **phát Track 32**, nối (1 c · 2 a · 3 d · 4 b) |
| | `U03-listening-2` (10:34, 8 chương) | **Phát Track 33** cho câu 1–4, **phát lại từng đoạn** cho câu 5–12; đáp án theo **Answer key** (b c a d · c b a a c b a b) kèm câu nghe được, bẫy *garden / car park*, *new kitchens*; design / staff / customer / product |
| Reading | `U03-reading-1` (4:35, 7 chương) | Exam tip phần 2 bài Đọc, bốn nghề (farms, flights, pitch, tips), "The Best Job I Ever Had": tìm nghề, câu E (C B A D) và F (C A D B) với **cụm diễn đạt lại tô vàng** (exhausted = very tired, a fortune = a lot of money…) |
| | `U03-reading-2` (4:12, 8 chương) | Ba quảng cáo tuyển dụng, nối với mô tả (d b a), câu 4–9 tô cụm từ (C A B C B A — **Answer key**), Exam tip đoán và tìm bằng chứng, 5 từ vựng |
| Writing | `U03-writing-1` (4:10, 7 chương) | Register là gì, VF / QF / INF cho 7 loại thư, nối 8 cách nói trang trọng – thân mật, dấu hiệu văn phong, cùng một tin viết hai kiểu |
| | `U03-writing-2` (5:40, 8 chương) | Công ty ở quảng cáo B cần người thế nào, thư nháp của Ahmed, vị trí 5 mẹo, sửa 6 chỗ quá thân mật, **thư hoàn chỉnh theo Answer key** (Writing 2D, 2 trang), 6 cụm từ thư xin việc |
| Consolidation | `U03-consolidation` (5:40, 7 chương) | Lời khuyên Phần 2 (B B A A A A), thẻ đề, **cách hỏi giám khảo** (Track 34 đọc lại), nói 1 phút, 6 cụm hai từ, trọng âm 10 từ (Track 36), sửa 8 lỗi |
| Exam practice | `U03-exam-listening` (6:47, 9 chương) | Làm việc tại nhà, Exam tip và Question-type tip, câu 1–2 (b c), chọn 6 trong 10 (A C D E G I) và vì sao loại B F H J — **Track 37 đọc lại bằng bốn giọng** (Mai, Tom = Simon, Jerry `am_liam`), phụ đề ẩn khi nghe |
| | `U03-exam-reading` (4:13, 8 chương) | "The Worst Job I Ever Had": câu 1–8 (C A D A B D B C) tô cụm diễn đạt lại, câu 9–12 ≤ 2 từ (saved, home, became busier, was late), từ khóa |

Đáp án không có trong Answer key đều ghi "suy ra" / "gợi ý" trong video và đầu kịch bản.

### Công cụ `lesson_video`

| Thêm / sửa | Cách làm |
|---|---|
| `image.grid` | Dải `grid` tranh bằng nhau nằm ngang (thường gặp trong sách) được cắt và xếp lại thành 2 hàng — tranh trong video to gấp đôi |
| Phương án `mcq` dài | Xuống tối đa hai dòng (chữ ≥ 18) thay vì thu nhỏ; số dòng tính theo chữ đậm nên ô không đổi cỡ khi mở đáp án |
| `passage` dài | Giữ chữ ≥ 19: nếu không vừa thì các đoạn không đang giảng thu gọn còn 2 dòng (hoặc 1) kèm "…", đoạn đang giảng hiện đủ |
| `mark` | Tô cả cụm bị ngắt sang dòng sau (dò trên cả đoạn rồi chia theo dòng) |

### File thêm

| File | Vai trò |
|---|---|
| `books/ielts_target_5_0/lessons/U03-*.yaml`, `U03-*.mp4` (11 cặp) | Kịch bản và video Unit 3 |

### File sửa

| File | Thay đổi |
|---|---|
| `agents/lesson_video/script.py` | `ImageRef.grid` |
| `agents/lesson_video/slides.py` | Xếp lưới ảnh; `mcq` hai dòng; `passage` thu gọn đoạn, tô cụm qua dòng |
| `agents/tests/test_lesson_video.py` | +1 test lưới ảnh / mcq dài / passage dài; độ phủ Unit 1–3 trên sách thật |
| `books/ielts_target_5_0/lessons/lessons.json` | Thêm 11 mục Unit 3 |
| `tests/web/book-core.test.mjs`, `tests/web/book.e2e.mjs` | Unit 3: 11 video, 6 nhóm theo thứ tự sách; nút "a letter of application" mở phiên Writing có 2 video |
| `docs/agent-hoc-tap/06-video-bai-giang.md` | Bảng độ phủ Unit 3, 11 dòng lịch sử, mẹo bố cục mới, cách đọc mới, **kế hoạch Unit 4** (OCR trang PDF 47–58) |
| `web/app.template.html` | Mô tả file 06 |
| `agents/README.md`, `docs/agent-hoc-tap/04-checklist.md`, `README.md` (thư mục docs) | `image.grid`; task P2-43; trạng thái |
| `web/index.html`, `web/ielts-companion.html` | Bản dựng lại |

Không xóa file nào. Video Unit 1–2 giữ nguyên (bố cục các cảnh chúng dùng không đổi đáng kể).

### Kiểm thử

| Lệnh | Kết quả |
|---|---|
| `cd agents && python -m pytest -q` | 57 passed (hồi quy: 36 kịch bản khớp `lessons.json`; độ phủ Unit 1–3 đủ sáu phần; +1 test lưới ảnh / mcq hai dòng / passage thu gọn) |
| `node --test "tests/web/*.test.mjs"` | 13 passed (Unit 3: 11 video, 6 nhóm đúng thứ tự sách) |
| `node tests/web/book.e2e.mjs` | 14/14 bước OK (bước mới: thẻ Unit 3 có 11 video, nút Writing 2 mở phiên có `U03-writing-1`, `U03-writing-2`) |
| `ffprobe` / `volumedetect` / khung hình trích từ MP4 | 11 video, tổng 1:09:08, 95 chương; tiếng trung bình −16,9 đến −19,2 dB, đỉnh ≤ −0,4 dB; khung hình lưới ảnh 2×2, "Track 33 · extract 1", đáp án mcq tô xanh, thư hai trang ≈ 152 từ, bài đọc thu gọn đoạn và tô cụm qua dòng đều đúng |
| Xem trước (`--engine silent`) + soát cách đọc | Sửa trước khi dựng: phương án mcq bị cắt (hai dòng), chữ bài đọc quá nhỏ (thu gọn đoạn), tranh quá nhỏ (`grid`), "a.s.a.p." / "Unit 3" / chữ cái rời đọc sai (viết lại trong `say`) |

### Còn treo

- Unit 4 trở đi (kế hoạch ở file 06 mục 8).

---

## Đợt 11 — 06/10/2026: video Unit 1 Listening và Reading; bỏ Workbook

Nhánh `claude/gallant-ramanujan-ym30oy` đặt lại từ `main` tại `e973c3f` (đã merge PR #11).

### Yêu cầu

Làm video Unit 1 Listening và Reading; bỏ qua Workbook vì không có sách này — tập trung vào Course Book hiện tại;
xong thì tạo PR.

### Đã làm

| Video | Nội dung |
|---|---|
| `U01-listening-1` Listening 1: listening for specific information (6:32, 7 chương) | **A** đoán loại thông tin còn thiếu — nối 10 câu với a–j (g h e b j i c f a d, suy ra từ chữ quanh chỗ trống) · **B** câu nào viết hoa, câu nào viết số · **C** phát nguyên **Track 5** để kiểm tra dự đoán · **D** phát lại **từng câu** của Track 5 (mốc `start` / `end` lấy bằng ffmpeg silencedetect) rồi chữa ngay: Ocean, 1984, 0207 389 152, Henderson, 320, Green, four, twenty years, Manchester, April 17 (theo Tapescript) · tổng kết |
| `U01-listening-2` Listening 2: practising listening for specific information (6:36, 8 chương) | Exam tip phần 1 bài thi Nghe · đọc phiếu và đoán · phát nguyên **Track 7** (Greg gọi Maggie kiểm tra dữ liệu nhân viên) · đáp án theo **Answer key**: Austin, 110, 47, three children, 2003, Moore, Cedar, 650396, 22, single — kèm câu nghe được và cách đánh vần tên · tự đánh giá, Question-type tip · address / age / marital status |
| `U01-reading-1` Reading 1: skimming (4:34, 7 chương) | Exam tip nguồn văn bản · **A** nối 6 văn bản (ảnh cắt từ trang sách) với nguồn: E A B F D C · **B** đọc lướt bằng hình, hình thức, từ khóa, dòng đầu – cuối · Exam tip mục đích · **C** C A F B D E · **D** quickly, general, before, slowly (đáp án suy ra, có giải thích) |
| `U01-reading-2` Reading 2: practise skimming (3:52, 7 chương) | Đọc sáu nguồn trước · nối văn bản A–C và D–F (hai ảnh cắt từ hai trang) theo **Answer key**: 1 B · 2 D · 3 E · 4 C · 5 A · 6 F · tự đánh giá · 6 từ trong ngữ cảnh (gets better, goes up, how you see things, person, gets married, are hurt) |

Thẻ Unit 1 trong tab Sách: **13 video trong 6 nhóm** (Speaking & Vocabulary · Listening · Reading · Writing ·
Consolidation · Exam practice). Unit 1 và Unit 2 đủ video cho mọi phần có trang trong Course Book (25 video).

**Workbook:** bỏ hẳn — P2-36 đóng ("bỏ"), hồ sơ [06-video-bai-giang.md](06-video-bai-giang.md) ghi rõ phạm vi chỉ
Course Book và file nghe đi kèm; các chỗ sách ghi "go to Workbook page …" bỏ qua.

### Công cụ

| Sửa | Cách làm |
|---|---|
| Ô gợi ý câu điền từ | Rộng 166 px như cũ, nới tới 420 px khi có gợi ý dài ("what you do at work / how you see things") thay vì thu nhỏ rồi cắt chữ |

Không thêm kiểu cảnh mới: Listening dùng lại dòng `track` (đợt 10) với `start` / `end` để phát lại từng câu.

### File thêm

| File | Vai trò |
|---|---|
| `books/ielts_target_5_0/lessons/U01-listening-1.yaml`, `.mp4` | Kịch bản và video Listening 1 |
| `books/ielts_target_5_0/lessons/U01-listening-2.yaml`, `.mp4` | Kịch bản và video Listening 2 |
| `books/ielts_target_5_0/lessons/U01-reading-1.yaml`, `.mp4` | Kịch bản và video Reading 1 |
| `books/ielts_target_5_0/lessons/U01-reading-2.yaml`, `.mp4` | Kịch bản và video Reading 2 |

### File sửa

| File | Thay đổi |
|---|---|
| `agents/lesson_video/slides.py` | Ô gợi ý nới rộng theo gợi ý dài nhất |
| `agents/tests/test_lesson_video.py` | Test độ phủ trên sách thật: Unit 1 và Unit 2 đủ sáu phần có video, phiên ôn unit thì không |
| `books/ielts_target_5_0/lessons/lessons.json` | Thêm 4 mục Unit 1 |
| `tests/web/book-core.test.mjs`, `tests/web/book.e2e.mjs` | Unit 1: 13 video, 6 nhóm theo thứ tự sách |
| `docs/agent-hoc-tap/06-video-bai-giang.md` | Phạm vi chỉ Course Book; bảng độ phủ Unit 1 mới; 4 dòng lịch sử; cách lấy mốc phát lại từng câu |
| `docs/agent-hoc-tap/04-checklist.md`, `README.md` (thư mục docs) | Task P2-42; P2-36 (Workbook) đóng — bỏ; trạng thái |
| `web/index.html`, `web/ielts-companion.html` | Bản dựng lại |

Không xóa file nào. Video cũ giữ nguyên.

### Kiểm thử

| Lệnh | Kết quả |
|---|---|
| `cd agents && python -m pytest -q` | 56 passed (hồi quy: 25 kịch bản khớp `lessons.json`; độ phủ Unit 1–2 đủ sáu phần) |
| `node --test "tests/web/*.test.mjs"` | 13 passed (Unit 1: 13 video, 6 nhóm đúng thứ tự sách) |
| `node tests/web/book.e2e.mjs` | 13/13 bước OK (thẻ Unit 1 có 13 video, 6 nhóm) |
| `ffprobe` / `volumedetect` / khung hình trích từ MP4 | 4 video, tổng 21:34, 29 chương; tiếng trung bình −17,4 đến −18,0 dB, đỉnh ≤ −0,7 dB; khung "Track 5 · sentence 3" đúng câu đang phát lại |
| Xem trước (`--engine silent`) + soát cách đọc | Sửa trước khi dựng: ô gợi ý cắt chữ (nới rộng), chi tiết "a week later" không có trong bài (bỏ) |

### Còn treo

- Unit 3 trở đi (kế hoạch ở file 06 mục 7).

---

## Đợt 10 — 06/10/2026: 12 video Unit 2; phát file nghe của sách trong video

Nhánh `claude/gallant-ramanujan-ym30oy` đặt lại từ `main` tại `a55277e` (đã merge PR #10).

### Yêu cầu

Tiếp tục làm video cho Unit 2, xong thì tạo PR.

### Đã làm

Làm theo hồ sơ [06-video-bai-giang.md](06-video-bai-giang.md) (kế hoạch Unit 2 viết ở đợt 9). Khác kế hoạch: phần
**Listening** đợt 9 định để sau vì công cụ chưa phát được file nghe của sách — đợt này thêm dòng `track` nên làm luôn
(3 video); **Reading** tách hai video và dùng cảnh mới `passage` để dạy dò tìm. Unit 2 có video cho **mọi phần có
trang sách**.

| Phần | Video | Nội dung |
|---|---|---|
| Speaking & Vocabulary | `U02-speaking-1` (8:48, 12 chương) | Chính tả 8 môn học (đánh vần từng chữ), nghĩa từng môn, đuôi -ics, nối 6 tranh (gợi ý), kể về trường cũ, Grammar check quá khứ đơn (learned, studied, decided, stopped; knew, read, thought, taught, chose), *Watch out!* (didn't + nguyên mẫu, did you…?, had to), đuôi -ed /t/ /d/ /ɪd/ (Track 13), đến lượt bạn |
| | `U02-speaking-2` (8:02, 11 chương) | Track 14 không có file nghe → Emma (giám khảo), Tom (Speaker 1), **Mai** (Speaker 2, giọng `af_bella`) đọc lại, phụ đề ẩn; chọn câu trả lời hay hơn (2, 1, 2 — gợi ý) và vì sao; trả lời + lý do + chi tiết; Vocabulary 2 P/N 10 câu; cụm từ enjoy / keen on / prefer A to B / boring; bài nói mẫu của Mai; đến lượt bạn |
| Listening | `U02-listening-1` (5:20, 6 chương) | -teen / -ty, *and* sau hundred, **phát Track 15, 16, 17** của sách, viết 8 số (18, 80, 96, 120, 243, 531, 852, 984), số hàng nghìn |
| | `U02-listening-2` (8:35, 8 chương) | Sắp chữ thành 12 tháng, trọng âm tên tháng (**Track 18**), 15 số thứ tự (**Track 19**), hai cách đọc ngày (**Track 20**), đọc ngày theo hai cách, nghe – viết 4 ngày (**Track 21**: 2 June, 21 November, 17 July, 31 August), trả lời bằng ngày |
| | `U02-listening-3` (7:12, 8 chương) | Đọc trước 12 câu, **phát nguyên Track 22** (cuộc gọi đăng ký khóa nhiếp ảnh), đáp án theo Answer key kèm câu nghe được, bẫy 96/69 và ba khóa học, tự đánh giá, course / class / lesson |
| Reading | `U02-reading-1` (5:40, 9 chương) | Đọc lướt 5 trích đoạn học lái xe, **dò tìm với từ khóa tô vàng ngay trên bài** (two hours, over 21, £38, about 40 minutes, 'L' plates), đúng / sai F F F T, định nghĩa scanning, skimming ≠ scanning |
| | `U02-reading-2` (5:33, 8 chương) | Emma đọc trang web "Swimming – safe and fun!" (2 trang), nối tranh (C, A, B — gợi ý), 6 câu trả lời ngắn có tô từ khóa (theo Answer key Reading 2B), Exam tip lấy từ trong bài, 4 danh từ và 4 cặp tính từ – danh từ |
| Writing | `U02-writing-1` (5:48, 10 chương) | Exam tip phần 1 bài thi Viết, ba phần của thư (mục đích → tình huống → điều muốn), độ dài từng phần, quảng cáo khóa tiếng Anh thương mại cắt từ trang sách với 4 lời hứa ✗, chọn câu mở đầu tốt nhất (câu 2) và vì sao ba câu kia sai, viết câu mở đầu cho 3 tình huống |
| | `U02-writing-2` (6:08, 9 chương) | Câu chủ đề 4-1-2-3 (Answer key 3A), lời hứa → thực tế, học viên muốn hoàn 50%, xóa 5 từ thừa (to, was, the, that, am — Answer key 4B), **thư phàn nàn hoàn chỉnh 228 từ đọc thành tiếng (2 trang)**, 6 cụm từ cho thư phàn nàn |
| Consolidation | `U02-consolidation` (6:19, 10 chương) | Từ để hỏi (Track 23), Track 23 đọc lại và cách trả lời, đến lượt bạn, 8 môn học, have / fail / pass / apply / do, *Watch out!* do homework / take a test, trọng âm 7 từ (Track 25), sửa 6 lỗi |
| Exam practice | `U02-exam-reading` (6:43, 8 chương) | Exam tip bài thi Đọc (3 phần, 4–6 bài, 40 câu, 60 phút), cách làm, Emma đọc "Are A Levels Just Too Easy?" (2 trang), câu 1–7 (B D A C B D C), 8–12 (10%, more than 20%, five, three, the long jump), từ khóa |
| | `U02-exam-writing` (6:12, 10 chương) | Đúng / sai 8 câu về bài thi Viết phần 1, đề thư gửi Learn Fast Driving School, chia 20 phút (3 + 3 + 11 + 3), dàn ý 5 đoạn, **thư mẫu Terry Black theo Answer key (2 trang)**, từ nối, bảng soát lỗi 3 phút |

Thẻ Unit 2 trong tab Sách: 12 video trong 6 nhóm (Speaking & Vocabulary · Listening · Reading · Writing ·
Consolidation · Exam practice). Đáp án không có trong Answer key đều ghi "gợi ý" trong video và đầu kịch bản.

### Công cụ `lesson_video`

| Thêm / sửa | Cách làm |
|---|---|
| Phát file nghe của sách | Dòng `{track: U02-L2A, note: "Track 22 · Listening 2A", start, end}`: `timeline` cắt đoạn bằng ffmpeg, chuẩn hóa đỉnh như giọng đọc, ghép vào dải tiếng; thanh phụ đề hiện nút ▶ và nhãn; `check` báo mã file sai, thiếu file, `end` vượt độ dài |
| Cảnh `passage` | Bài đọc trên màn hình (phía trên phụ đề), nhãn đầu đoạn, ghi chú lề; dòng thoại `mark: [cụm từ]` tô vàng cụm từ trong đoạn `focus` (giữ tới khi đổi đoạn); `mark` ngoài cảnh passage bị chặn |
| Thư chia hai trang | Trường cảnh `words` giữ số từ của cả lá thư khi chia hai cảnh `letter` (chữ to hơn) |
| Bố cục | Câu điền từ dài tự thu nhỏ cho vừa một dòng; chữ gợi ý (`hint`) co cho vừa ô; đáp án ✓ / ✗ trong cảnh `match` dùng phông có ký hiệu |

### File thêm

| File | Vai trò |
|---|---|
| `books/ielts_target_5_0/lessons/U02-*.yaml`, `U02-*.mp4` (12 cặp) | Kịch bản và video Unit 2 |

### File sửa

| File | Thay đổi |
|---|---|
| `agents/lesson_video/script.py` | Kiểu `passage`; dòng `mark`, `track`, `start`, `end` (một dòng là câu thoại, khoảng lặng hoặc đoạn nghe); trường cảnh `words`; `check` kiểm file nghe |
| `agents/lesson_video/timeline.py` | `build(…, book_dir)`; `_decode` (ffmpeg); khung hình có `mark`, `audio` |
| `agents/lesson_video/slides.py` | `_k_passage`; phụ đề khi phát file nghe; `words`; thu nhỏ câu điền từ dài, chữ gợi ý; phông ký hiệu cho ✓/✗ |
| `agents/lesson_video/cli.py` | Truyền thư mục sách cho `timeline.build` |
| `agents/tests/test_lesson_video.py` | +9 test: passage / mark / track (file wav tạo trong test), `check` báo file nghe sai, 5 kịch bản sai bị chặn, thư chia trang |
| `books/ielts_target_5_0/lessons/lessons.json` | Thêm 12 mục Unit 2 |
| `tests/web/book-core.test.mjs`, `tests/web/book.e2e.mjs` | Unit 2: 12 video, 6 nhóm theo thứ tự sách; nút Listening mở phiên Listening có 3 video |
| `docs/agent-hoc-tap/06-video-bai-giang.md` | Bảng độ phủ Unit 2, lịch sử 21 video, quy trình có file nghe, kiểu cảnh `passage`, cách đọc mới, **kế hoạch Unit 3** (OCR trang PDF 35–46) |
| `web/app.template.html` | Mô tả file 06 |
| `agents/README.md`, `docs/agent-hoc-tap/04-checklist.md`, `README.md` (thư mục docs) | Kiểu cảnh, dòng `track`; task P2-41; trạng thái |
| `web/index.html`, `web/ielts-companion.html` | Bản dựng lại |

Không xóa file nào. Video Unit 1 giữ nguyên.

### Kiểm thử

| Lệnh | Kết quả |
|---|---|
| `cd agents && python -m pytest -q` | 56 passed (kể cả hồi quy: 21 kịch bản khớp `lessons.json`, độ phủ Unit 1) |
| `node --test "tests/web/*.test.mjs"` | 13 passed (Unit 2: 12 video, 6 nhóm đúng thứ tự sách) |
| `node tests/web/book.e2e.mjs` | 13/13 bước OK (thêm bước Unit 2: 12 video, nút Listening mở phiên có 3 video) |
| `ffprobe` / `volumedetect` / khung hình trích từ MP4 | Tổng 1:20:22, 109 chương; thời lượng khớp lời thoại; tiếng trung bình −17,5 đến −19,7 dB, đỉnh ≤ −0,1 dB; đoạn phát file nghe của sách (đo ở Listening 1) đỉnh ngang giọng đọc, trung bình thấp hơn 3–4 dB vì bản ghi có khoảng nghỉ để nhắc lại |
| Xem trước từng cảnh (`--engine silent`) + soát cách đọc bằng phonemizer | Sửa trước khi dựng: chữ gợi ý tràn ô, thư 228 / 218 từ chữ quá nhỏ (chia hai trang), "A levels", "part A", "a.m." đọc sai, ✗ không có trong phông |

### Còn treo

- Unit 1 Listening và Reading chưa có video (công cụ đã sẵn sàng).
- Workbook vẫn thiếu (P2-36): Unit 1 trang 6, Unit 2 trang 8.

---

## Đợt 9 — 06/10/2026: video Unit 1 Consolidation và Exam practice; hồ sơ video bài giảng

Nhánh `claude/gallant-ramanujan-ym30oy` đặt lại từ `main` tại `e789ae0` (đã merge PR #9).

### Yêu cầu

Làm video hướng dẫn cho Consolidation và Exam practice để xong Unit 1; đóng gói lịch sử làm video của tất cả các
phần (phần nào có video, phần nào không) làm căn cứ cho Unit 2; xong thì tạo PR.

### Đã làm

| Việc | Cách làm |
|---|---|
| **Consolidation** (6:52, 10 chương, 5,5 MB) | **Speaking A** ba câu hỏi về Phần 1 bài thi Nói (4–5 phút, khoảng một phần ba của 11–14 phút, câu hỏi về chủ đề quen thuộc) · **B** câu dễ / khó, Tom trả lời mẫu ba câu khó (Japan, Nguyễn Thị Ánh Viên, thầy Long) · **C** sáu câu "Đến lượt bạn" có đếm ngược · **Vocabulary A** 7 câu điền từ gia đình · **B** dạng từ từ gốc (living, children, childhood, married, retirement) · **C** trọng âm theo **Tapescript Track 8**, nghe và nhắc lại · **Errors** sửa 8 câu (viết hoa tên riêng, a/an, have got, tuổi, were, I am writing to…) · tổng kết |
| **Exam practice: Listening** (7:08, 11 chương, 5,4 MB) | Đọc ghi chú trước, đoán loại từ · **Track 9 không có file nghe** trong bộ sách → Emma (lễ tân) và Tom (khách) **đọc lại đúng Tapescript**, chia ba đoạn theo nhóm câu; khi nghe, phụ đề chỉ hiện người nói và "Listen carefully…" · đáp án kèm câu nghe được: 1 Hunt, 2 two, 3 Manchester, 4 104 · 5 b, 6 c, 7 b (từ đồng nghĩa: conference = business, tiny = small; bẫy "football match") · 8 D, 9 B — lần theo lời chỉ đường trên **bản đồ cắt từ trang 20** · Question-type tip và mẹo nghe · bảng tự chấm 9 câu |
| **Exam practice: Reading** (5:40, 8 chương, 4,8 MB) | **A** đọc lướt một phút chọn chủ đề (1/2/3) → Emma đọc cả bài "Perspectives of work and job satisfaction" (đoạn đang đọc tô màu, từ khóa ở lề) → đáp án 3 và vì sao không phải 1, 2 · 6 từ khóa kèm ví dụ · **B** nối câu 1–5 với đoạn A–E: 1 C, 2 A, 3 E, 4 D, 5 B (mỗi đáp án kèm câu trong bài) · hai Question-type tip của sách + mẹo đọc · tổng kết |
| Mục lục video | Thẻ Unit 1 có **9 video trong 4 phần**, xếp theo thứ tự trong sách: Speaking & Vocabulary (3) · Writing (3) · Consolidation (1) · Exam practice (Listening, Reading). Trước đây nhóm xếp theo thứ tự chữ cái của `lessons.json` nên Consolidation sẽ đứng đầu |
| Công cụ | Kiểu cảnh **`mcq`** (thẻ mỗi câu, phương án đúng tô xanh, `keys` để dùng nhãn 1/2/3); **`blanks` dạng câu** (`q` chứa `___`, `hint` = từ gốc ở lề phải, dấu câu dính sát chỗ trống); trường cảnh **`hide_text`** và **`roles`**; ô mẹo và thẻ trắc nghiệm cao vừa nội dung; nhãn người đọc của cảnh `letter` đổi thành "đang đọc thành tiếng" (dùng cho cả bài đọc) |
| **Hồ sơ video** | [06-video-bai-giang.md](06-video-bai-giang.md): bảng độ phủ Unit 1, phần chưa có video và vì sao (Listening — chưa chèn được audio sách vào video; Reading; Ôn unit; Workbook), lịch sử 9 video, quy trình 9 bước, danh mục 14 kiểu cảnh, bảng cách đọc `say` (đã kiểm bằng phonemizer của Kokoro), lỗi đã gặp, **kế hoạch Unit 2** theo từng phần (tên mục lấy bằng OCR trang PDF 23–34). Lệnh mới `python -m lesson_video coverage` in lại bảng độ phủ |

### File thêm

| File | Vai trò |
|---|---|
| `books/ielts_target_5_0/lessons/U01-consolidation.yaml`, `.mp4` | Kịch bản và video Consolidation |
| `books/ielts_target_5_0/lessons/U01-exam-listening.yaml`, `.mp4` | Kịch bản và video Exam practice: Listening |
| `books/ielts_target_5_0/lessons/U01-exam-reading.yaml`, `.mp4` | Kịch bản và video Exam practice: Reading |
| `agents/lesson_video/coverage.py` | Bảng độ phủ video theo unit (book.json + lessons.json + kịch bản chưa dựng) |
| `docs/agent-hoc-tap/06-video-bai-giang.md` | Hồ sơ video bài giảng và kế hoạch Unit 2 |

### File sửa

| File | Thay đổi |
|---|---|
| `agents/lesson_video/script.py` | Kiểu `mcq`, `mcq_keys`; `hide_text`, `roles` (kiểm người nói); mô tả `blanks` dạng câu |
| `agents/lesson_video/slides.py` | `_k_mcq`, `_blank_sentences`; phụ đề ẩn lời trong cảnh nghe, nhãn vai theo `roles`; ô mẹo / thẻ cao vừa nội dung |
| `agents/lesson_video/cli.py` | Lệnh `coverage` |
| `agents/tests/test_lesson_video.py` | +9 test: kiểu cảnh luyện đề dựng và vẽ được, 6 kịch bản sai bị chặn, bảng độ phủ, độ phủ Unit 1 trên sách thật |
| `books/ielts_target_5_0/lessons/lessons.json` | Thêm 3 mục |
| `web/src/book/core.js`, `ui.js` | `groupLessons(lessons, order)`: nhóm video theo thứ tự phần trong `book.json` |
| `web/app.template.html` | File 06 trong tab Kế hoạch (nhóm "Agent học tập") |
| `tests/web/book-core.test.mjs`, `tests/web/book.e2e.mjs` | Unit 1 có 9 video, 4 nhóm theo thứ tự sách; nút "Exam practice: Listening" mở phiên Consolidation & Exam practice có 3 video |
| `agents/README.md`, `web/README.md`, `CLAUDE.md`, `docs/agent-hoc-tap/04-checklist.md`, `README.md` (thư mục docs) | Kiểu cảnh mới, lệnh `coverage`, quy ước làm video; task P2-39, P2-40; trạng thái |
| `web/index.html`, `web/ielts-companion.html` | Bản dựng lại |

Không xóa file nào. Sáu video cũ giữ nguyên (bố cục các kiểu cảnh chúng dùng không đổi; nếu dựng lại, nhãn người đọc trong cảnh thư sẽ là "đang đọc thành tiếng").

### Kiểm thử

| Lệnh | Kết quả |
|---|---|
| `cd agents && python -m pytest -q` | 48 passed |
| `node --test "tests/web/*.test.mjs"` | 13 passed |
| `node tests/web/book.e2e.mjs` | 12/12 bước OK (Unit 1 có 9 video, 4 nhóm theo thứ tự sách; nút Exam practice mở đúng phiên) |
| `ffprobe` / `volumedetect` / khung hình trích từ MP4 | Thời lượng khớp lời thoại; chương 10 / 11 / 8; tiếng trung bình -18,0 / -17,4 / -17,4 dB, đỉnh ≤ -0,6 dB |
| Xem trước từng cảnh bằng `--engine silent` + soát cách đọc bằng phonemizer của Kokoro | Sửa 3 chỗ trước khi dựng thật: câu đáp án quá dài (Errors 8), mẹo "IN-trests", "part A" đọc thành mạo từ |

### Còn treo

- Unit 1 Listening và Reading chưa có video (lý do và cách làm ở file 06, mục 1).
- Workbook vẫn thiếu (P2-36).

---

## Đợt 8 — 06/10/2026: sửa nút phóng to / thu nhỏ trang sách

Nhánh `claude/gallant-ramanujan-ym30oy` đặt lại từ `main` tại `79c9392` (đã merge PR #8).

### Yêu cầu

Nút phóng to / thu nhỏ hình trang bài học (trình xem PDF trong phiên học) chưa hoạt động.

### Nguyên nhân (đo trên Chromium thật)

| Màn hình | Trước khi sửa: bề ngang trang sau mỗi lần bấm + | Vì sao |
|---|---|---|
| Điện thoại 390 px, dpr 3 | 370 → 555 → 740 → 925 → 1110 px | Chạy, nhưng nút − không xuống dưới 100% |
| Laptop 1280 px, dpr 2 | 1260 → 1681 → 1681 → 1681 px (kẹt) | Cỡ hiển thị tính từ độ phân giải canvas, mà độ phân giải bị chặn ở ~16 triệu điểm ảnh (trần của Safari iOS) |
| Mọi màn hình | − ở mức đầu không làm gì | Mức nhỏ nhất là 100% (vừa khung) — không thu nhỏ được để xem trọn trang |

### Đã làm

| Việc | Cách làm |
|---|---|
| Mức phóng | 50%, 75%, **100% (vừa bề ngang khung)**, 125%, 150%, 200%, 250%, 300%; nút giữa hiện mức đang dùng ("100%"), bấm để về vừa khung; nút − / + mờ khi tới giới hạn; phím `+` `-` `0` |
| Cỡ hiển thị tách khỏi độ phân giải | Bề ngang trang = vừa khung × mức phóng (luôn đúng); chỉ độ phân giải canvas có trần 16 triệu điểm ảnh — ở mức rất lớn trên màn hình nét cao ảnh hơi mềm nhưng vẫn phóng được |
| Mượt hơn | Bấm là đổi cỡ ngay bằng CSS và giữ điểm giữa khung nhìn, rồi vẽ lại trang vào canvas mới và thay vào khi xong (không chớp trắng, không hiện "Đang mở trang…", không nhảy về đầu trang); lật trang vẫn giữ mức phóng |

Sau khi sửa: laptop dpr 2 → 1260 → 1575 → 1890 → 2520 → 3150 px; thu nhỏ 945 px (75%), 630 px (50%, thấy gần trọn trang).

### File sửa

| File | Thay đổi |
|---|---|
| `web/src/book/ui.js` | `openViewer`: bảng mức phóng, `setZoom`, `paintZoom`, nhãn %, phím tắt; `draw(keepView)` tính cỡ hiển thị theo mức phóng, vẽ vào canvas mới rồi thay |
| `web/src/book/book.css` | Kiểu nút mức phóng |
| `tests/web/book.e2e.mjs` | Bước xem trang sách: phóng 150% (bề ngang > 1,45×), thu 50% (< 0,55×, nút − mờ), về vừa khung |
| `web/README.md`, `docs/agent-hoc-tap/04-checklist.md`, `README.md` (thư mục docs) | Mô tả phóng to / thu nhỏ; task P2-38; trạng thái |
| `web/index.html`, `web/ielts-companion.html` | Bản dựng lại |

Không thêm, không xóa file nào.

### Kiểm thử

| Lệnh | Kết quả |
|---|---|
| `cd agents && python -m pytest -q` | 39 passed |
| `node --test "tests/web/*.test.mjs"` | 13 passed |
| `node tests/web/book.e2e.mjs` | 12/12 bước OK (có kiểm tra phóng to / thu nhỏ) |
| Đo tay bằng Playwright ở 390 px dpr 3, 1280 px dpr 2 và dpr 1 | Cỡ trang đổi đúng mọi mức, không lỗi JS |

---

## Đợt 7 — 06/10/2026: video Unit 1 Vocabulary 1–3; mục lục video theo từng phần

Nhánh `claude/gallant-ramanujan-ym30oy` đặt lại từ `main` tại `dfd0d51` (đã merge PR #7).

### Yêu cầu

Unit 1 thiếu phần Vocabulary 1, 2, 3 (sách in trang 11): làm một video hướng dẫn cả ba bài, đọc đáp án và thêm ví dụ
theo chủ đề; thêm mục còn thiếu vào menu; xong thì tạo PR.

### Đã làm

| Việc | Cách làm |
|---|---|
| **Vocabulary 1–3: family, stages of life, key words** (8:24, 12 chương, 7,0 MB) | **1A** nghe – chép 10 từ (Emma đọc, đếm ngược 4 giây mỗi từ), rồi Tom đọc đáp án và mẹo chính tả: father, mother, brother, sister, grandfather, son, daughter, aunt, uncle, cousin — **đáp án theo Tapescript Track 3** (sách in trang 277) · **Pronunciation check**: âm /ʌ/ trong mother, brother, son, uncle, cousin, husband… · **2A** gắn tranh: a retirement, b childhood, c death, d middle age, e birth, f adolescence (đáp án gợi ý) · **2B** thứ tự: birth → childhood → adolescence → middle age → retirement → death (+ adulthood) · thêm ví dụ dạng từ: be born, a teenager, an adult, middle-aged, retire/retired, die · **3A** sáu từ khóa (parents, relatives, retired, teenagers, children, adult) và 6 câu trả lời mẫu của Tom · Watch out (childs, he is teenager, where did you born, is retire) · **câu trả lời mẫu "Tell me about your family"** dùng từ của cả ba bài · bài về nhà: vẽ cây gia đình |
| Menu còn thiếu | Thẻ unit trong tab Sách nay là **mục lục video theo từng phần**: "Speaking & Vocabulary: ▶ Speaking 1 · ▶ Speaking 2 · ▶ Vocabulary 1–3", "Writing: ▶ Writing 1 · ▶ Writing 2 · ▶ Writing 3". Video Vocabulary gắn vào hoạt động `U01-speaking-vocab` (phiên 1), nên trong phiên học có 3 video |
| Công cụ | Kiểu cảnh `blanks` (ô trống đánh số, mở dần, mẹo chính tả); mục của `order` có thể ẩn chữ cái (`label: ""`); cảnh `letter` chừa một hàng cho nhãn người đọc khi dòng đầu dài (bài nói mẫu không có lời chào) |

### File thêm

| File | Vai trò |
|---|---|
| `books/ielts_target_5_0/lessons/U01-vocabulary.yaml` | Kịch bản video Vocabulary 1–3 |
| `books/ielts_target_5_0/lessons/U01-vocabulary.mp4` | Video 1280×720, H.264 + AAC, có chương, tiếng chuẩn -16 LUFS |

### File sửa

| File | Thay đổi |
|---|---|
| `agents/lesson_video/script.py`, `slides.py` | Kiểu cảnh `blanks`; `label` cho `order`; nhãn người đọc trong cảnh `letter` không đè chữ; chữ phụ "đang đọc bài mẫu" |
| `agents/tests/test_lesson_video.py` | +1 test: `blanks` và `order` không chữ cái dựng, vẽ được, reveal sai bị chặn |
| `books/ielts_target_5_0/lessons/lessons.json` | Thêm mục Vocabulary |
| `web/src/book/core.js` | `groupLessons` (gom video theo hoạt động) |
| `web/src/book/ui.js`, `book.css` | Thẻ unit: mỗi phần một hàng nhãn + nút video |
| `tests/web/book-core.test.mjs`, `tests/web/book.e2e.mjs` | `groupLessons`; Unit 1 có 6 video, hai nhóm "Speaking & Vocabulary", "Writing"; phiên Speaking & Vocabulary có 3 video; mở video Writing theo tên nút |
| `agents/README.md`, `web/README.md`, `docs/agent-hoc-tap/04-checklist.md`, `README.md` (thư mục docs) | Kiểu cảnh mới; mục lục video; task P2-37; trạng thái |
| `web/index.html`, `web/ielts-companion.html` | Bản dựng lại |

Không xóa file nào. Các video cũ không cần dựng lại (cảnh thư của Writing mở bằng lời chào ngắn nên bố cục không đổi).

### Kiểm thử

| Lệnh | Kết quả |
|---|---|
| `cd agents && python -m pytest -q` | 39 passed |
| `node --test "tests/web/*.test.mjs"` | 13 passed |
| `node tests/web/book.e2e.mjs` | 12/12 bước OK |
| `ffprobe` / `volumedetect` / khung hình trích từ MP4 | Thời lượng khớp lời thoại, 12 chương; tiếng trung bình -18,2 dB, đỉnh -0,8 dB |

---

## Đợt 6 — 06/10/2026: video Unit 1 Writing 3; Workbook trang 6

Nhánh `claude/gallant-ramanujan-ym30oy` đặt lại từ `main` tại `1d204cc` (đã merge PR #6).

### Yêu cầu

Tạo video hướng dẫn học và giải bài Writing 3 (sách in trang 18); hướng dẫn tới Workbook trang 6 để giải các bài tập
Workbook; xong thì tạo PR.

### Đã làm

| Việc | Cách làm |
|---|---|
| **Writing 3: organizing points in a personal letter** (8:30, 10 chương, 7,6 MB) | 9 từ mới (host family, appearance, personality, outgoing, generous, stubborn…) · **Bài A**: chọn ý cho thư giới thiệu bản thân gửi gia đình ở Anh (nên viết / bỏ qua hoặc một câu — bài mở, nói rõ không có một đáp án duy nhất) · **Bài B**: Tom đọc thư của Bruno (còn trống lời chào, lời kết), rồi sắp xếp 9 ý theo thứ tự xuất hiện (tên → tuổi → nơi ở → gia đình → việc học → sở thích → âm nhạc → tính cách → lý do học tiếng Anh; Bruno không nói ngoại hình, món ăn) · cách Bruno gom ý thành 4 đoạn · **Bài C**: Dear Mr and Mrs Gray … Best wishes / Kind regards (Yours sincerely đúng nhưng hơi trang trọng; không dùng Yours faithfully, Love, Hi) và đọc lại thư đã điền · **Thư mẫu của Lan** (sinh viên Việt Nam, 156 từ) cùng dạng đề, chia đoạn như Bruno · cách làm bài viết Workbook trang 6 theo 5 bước |
| Workbook trang 6 | **Chưa giải được**: bộ sách đã nhập không có Workbook (`book.yaml › missing: [work-book, test-books]`). Video chỉ hướng dẫn cách làm bài viết mà sách in yêu cầu ("Go to Workbook page 6 for the writing task"), không đoán nội dung đề. Ghi task P2-36: cần file Workbook hoặc ảnh trang 6 |
| Gắn vào app | Hoạt động `U01-writing` nay có 3 video; thẻ Unit 1 có 5 nút video |

Đáp án bài A, B, C là gợi ý (Answer key không có Unit 1 Writing). Thư của Bruno là văn bản trong sách (trang 18).

### File thêm

| File | Vai trò |
|---|---|
| `books/ielts_target_5_0/lessons/U01-writing-3.yaml` | Kịch bản video Writing 3 |
| `books/ielts_target_5_0/lessons/U01-writing-3.mp4` | Video 1280×720, H.264 + AAC, có chương, tiếng chuẩn -16 LUFS |

### File sửa

| File | Thay đổi |
|---|---|
| `books/ielts_target_5_0/lessons/lessons.json` | Thêm mục Writing 3 |
| `tests/web/book-core.test.mjs`, `tests/web/book.e2e.mjs` | Unit 1 có 5 video; phiên Writing có 3 video |
| `agents/README.md`, `web/README.md`, `docs/agent-hoc-tap/04-checklist.md`, `README.md` (thư mục docs) | Ghi chú `body: false`; video Writing 1–3; task P2-35, P2-36; trạng thái |
| `web/index.html`, `web/ielts-companion.html` | Bản dựng lại |

Không xóa file nào. Mã `agents/lesson_video` không đổi.

### Kiểm thử

| Lệnh | Kết quả |
|---|---|
| `cd agents && python -m pytest -q` | 38 passed (hồi quy: 5 kịch bản khớp `lessons.json`) |
| `node --test "tests/web/*.test.mjs"` | 13 passed |
| `node tests/web/book.e2e.mjs` | 12/12 bước OK |
| `ffprobe` / `volumedetect` / khung hình trích từ MP4 | Thời lượng khớp lời thoại, 10 chương; tiếng trung bình -17,4 dB, đỉnh -0,6 dB |

---

## Đợt 5 — 06/10/2026: video Unit 1 Writing 1 và Writing 2

Nhánh `claude/gallant-ramanujan-ym30oy` đặt lại từ `main` tại `da67bcb` (đã merge PR #5).

### Yêu cầu

Tạo hai video hướng dẫn cho Writing 1 và Writing 2 của Unit 1 (sách in trang 17–18); hướng dẫn xong thì mỗi video đọc
luôn một đoạn ví dụ; rồi tạo PR.

### Đã làm

| Video | Nội dung |
|---|---|
| **Writing 1: organizing your writing** (7:08, 12 chương, 6,3 MB) | Giới thiệu Task 1 (thư ≥ 150 từ, ~20 phút) · 8 từ mới · Exam tip · Bài A: sắp xếp 6 bước (c → a → e → f → d → b, đáp án gợi ý vì Answer key không có) · Bài B: chia 20 phút (1 + 2 + 1 + 2 phút chuẩn bị, 11 phút viết, 3 phút soát lỗi) · **Ví dụ đi qua đủ 6 bước** với đề "chuyển tới thành phố mới, viết thư cho bạn": đọc đề, ghi ý, chọn ý, dàn ý theo đoạn, **Tom đọc thư mẫu thân mật 160 từ**, soát lỗi · Tổng kết + bài về nhà |
| **Writing 2: types of letter / starting and ending letters** (7:58, 10 chương, 7,1 MB) | 9 từ mới · Bài A: 6 loại thư ↔ câu mở đầu A–F (1-D, 2-F, 3-E, 4-A, 5-B, 6-C, đáp án gợi ý) · Bài B: 6 cụm từ mở đầu, đếm ngược để viết lại theo trí nhớ · Bài C: cách kết 1–5 ↔ thư A–F (thư F không có cách kết → Yours sincerely) · Bài D: Yours faithfully / Yours sincerely, Best wishes / Regards, các cách kết thân mật · **Emma đọc thư mẫu trang trọng hỏi thông tin 154 từ** (Dear Sir/Madam … Yours faithfully) · Tổng kết + bài về nhà (viết lại cho Ms Taylor → Yours sincerely) |
| Gắn vào app | Hoạt động `U01-writing` (phiên 4 "Writing: học kỹ năng" và phiên 5 "Writing: chấm, viết lại"); thẻ Unit 1 nay có 4 nút video |
| Kiểu cảnh mới | `order` (sắp xếp: số thứ tự hiện dần, cột phải dựng thứ tự đúng), `timing` (thanh ngang chia phút, mở dần từng bước), `letter` (cả lá thư trên một trang, đoạn đang đọc tô màu, ghi chú vai trò từng đoạn ở lề, đếm từ, không có thanh phụ đề); dòng `read: <người nói>` đọc nguyên một đoạn thư (lấy cả `say` của đoạn); hàng của `pairs` được xuống hai dòng |

Giọng: Kokoro q8, Emma `af_heart`, Tom `am_michael` như đợt 4; cách đọc trong `say` soát lại với Kokoro
(Sir/Madam → "Sir or Madam", 150 → "a hundred and fifty", chữ cái A → `eigh`).

### File thêm

| File | Vai trò |
|---|---|
| `books/ielts_target_5_0/lessons/U01-writing-1.yaml`, `U01-writing-2.yaml` | Kịch bản hai video |
| `books/ielts_target_5_0/lessons/U01-writing-1.mp4`, `U01-writing-2.mp4` | Video 1280×720, H.264 + AAC, có chương, tiếng chuẩn -16 LUFS |

### File sửa

| File | Thay đổi |
|---|---|
| `agents/lesson_video/script.py` | Kiểu cảnh `order`, `timing`, `letter`; dòng `read`; kiểm tra `pos` 1…n, `read` chỉ trong cảnh letter kèm `focus`, cảnh letter không có `wait` |
| `agents/lesson_video/slides.py` | Vẽ ba kiểu cảnh mới; cảnh letter bỏ thanh phụ đề; ô chữ hai dòng cho `pairs`, `order` |
| `agents/tests/test_lesson_video.py` | +7 test: ba kiểu cảnh mới dựng và vẽ được, dòng `read` lấy đúng chữ và cách đọc, 6 kịch bản sai bị chặn |
| `books/ielts_target_5_0/lessons/lessons.json` | Thêm hai mục Writing |
| `tests/web/book-core.test.mjs`, `tests/web/book.e2e.mjs` | Unit 1 có 4 video; mở video Writing từ thẻ unit vào đúng phiên Writing |
| `agents/README.md`, `web/README.md`, `docs/agent-hoc-tap/04-checklist.md`, `README.md` (thư mục docs) | Kiểu cảnh mới; video Writing trong tab Sách; task P2-34; trạng thái |
| `web/index.html`, `web/ielts-companion.html` | Bản dựng lại |

Không xóa file nào.

### Kiểm thử

| Lệnh | Kết quả |
|---|---|
| `cd agents && python -m pytest -q` | 38 passed |
| `node --test "tests/web/*.test.mjs"` | 13 passed |
| `node tests/web/book.e2e.mjs` | 12/12 bước OK |
| `ffprobe` / `volumedetect` / khung hình trích từ MP4 | Thời lượng khớp lời thoại, đủ chương; tiếng trung bình ~-18 dB, đỉnh dưới 0 dB; thư mẫu và các cảnh mới hiển thị đúng |

---

## Đợt 4 — 05/10/2026: giọng Kokoro cho video bài giảng

Nhánh `claude/gallant-ramanujan-ym30oy` đặt lại từ `main` tại `8dd99b8` (đã merge PR #4).

### Yêu cầu

Giọng Flite nghe dở; gợi ý giọng miễn phí khác. Người dùng chọn **Kokoro bản q8**.

### Đã làm

| Việc | Cách làm |
|---|---|
| Lấy model | Hugging Face bị chặn bởi chính sách mạng của môi trường cloud → dùng bản q8 trong gói npm `kokoro-q8-shards` (6 mảnh ghép lại, sha256 `fbae9257…a1478` khớp mã gói ghi; bản gốc là `model_quantized.onnx` của `onnx-community/Kokoro-82M-v1.0-ONNX`) và file giọng trong gói npm `kokoro-js` (thư mục `voices/`, 28 giọng tiếng Anh, ~0,5 MB mỗi giọng). Không commit model hay giọng: đặt ở `~/.cache/lesson_video/kokoro/` |
| Bộ đọc Kokoro | `tts.Kokoro` qua thư viện `kokoro-onnx` 0.6: đọc 24 kHz, giọng `b*` tách âm `en-gb`, còn lại `en-us`; tốc độ 0,9. `--engine auto` chọn Kokoro khi tìm thấy model + giọng (tham số, biến môi trường hoặc thư mục mặc định), không thì Flite và báo lý do |
| Chọn giọng | Video mẫu 53 giây với 4 cặp (bf_emma + am_michael · af_heart + am_michael · bf_emma + bm_george · af_bella + am_fenrir). Người dùng nghe mẫu và chọn **cặp 2**: Emma `af_heart` (nữ, giọng Mỹ), Tom `am_michael` (nam, giọng Mỹ). Lượt dựng đầu bằng cặp 1 (`bf_emma`) dừng giữa chừng; câu của Tom đã đọc dùng lại từ bộ nhớ tiếng |
| Kịch bản | `voice` khai theo bộ đọc `{kokoro: …, flite: …}`. Soát cách Kokoro tách âm: `ay` (đã dùng cho Flite) bị đọc thành "eye", `Hway` thành "aitch-way" → đổi sang `eigh`, `Whey` (đúng ở cả hai bộ đọc) |
| Dựng lại nhanh | Tiếng từng câu lưu ở `~/.cache/lesson_video/tts/` theo (bộ đọc, giọng, chữ); dựng lại chỉ đọc câu đã đổi. Kokoro trên CPU 4 nhân chậm hơn thời gian thật một chút (~5 giây cho một câu) |

### File sửa

| File | Thay đổi |
|---|---|
| `agents/lesson_video/tts.py` | Thêm `Kokoro`, `load_voices`, `kokoro_files`, chế độ `auto`; mọi bộ đọc có `check(voice)` và `tag`; Flite nhận `speed` thay cho `stretch` |
| `agents/lesson_video/script.py` | `Speaker.voice` là một giọng hoặc bảng giọng theo bộ đọc, `voice_for()`; chuẩn hóa dòng thoại không sửa dữ liệu của người gọi và đọc lại được dạng chuẩn |
| `agents/lesson_video/timeline.py` | Kiểm tra giọng trước khi đọc; bộ nhớ tiếng từng câu (`cache_dir`) |
| `agents/lesson_video/cli.py` | `--engine auto|kokoro|flite|silent`, `--speed`, `--model`, `--voices`, `--cache`, `--no-cache`; in bộ đọc đang dùng |
| `agents/lesson_video/video.py` | `lessons.json` ghi thêm `engine`; chuẩn độ to lời nói -16 LUFS khi mã hóa (tiếng Kokoro nhỏ hơn Flite, trung bình -20,5 dB) |
| `agents/tests/test_lesson_video.py` | +5 test: giọng theo bộ đọc, bộ nhớ tiếng, thiếu model Kokoro, đọc file giọng, Kokoro đọc giọng tiếng Anh (bỏ qua khi máy chưa có model); hồi quy kiểm tra giọng khớp bộ đọc đã dùng |
| `agents/pyproject.toml` | Extra `[kokoro]` (`kokoro-onnx>=0.6`) |
| `books/ielts_target_5_0/lessons/U01-speaking-1.yaml`, `U01-speaking-2.yaml` | Giọng theo bộ đọc; `say` đúng với cả hai bộ đọc |
| `books/ielts_target_5_0/lessons/U01-speaking-1.mp4`, `U01-speaking-2.mp4`, `lessons.json` | Dựng lại bằng Kokoro: Speaking 1 dài 7:14 (6,0 MB), Speaking 2 dài 6:16 (4,7 MB) — ngắn hơn bản Flite (8:06, 6:56) vì đọc liền mạch hơn; chương giữ nguyên (8 và 9) |
| `agents/README.md`, `CLAUDE.md`, `docs/agent-hoc-tap/04-checklist.md`, `README.md` (thư mục docs) | Cài và dùng Kokoro; task P2-32 |
| `web/index.html`, `web/ielts-companion.html` | Bản dựng lại (`lessons.json` mới) |

Không thêm, không xóa file nào trong repo.

### Kiểm thử

| Lệnh | Kết quả |
|---|---|
| `cd agents && python -m pytest -q` | 31 passed (kể cả Kokoro đọc giọng tiếng Anh vì máy có model) |
| `node --test "tests/web/*.test.mjs"` | 13 passed |
| `node tests/web/book.e2e.mjs` | 12/12 bước OK |
| `ffprobe` / `volumedetect` | Thời lượng khớp lời thoại; tiếng trung bình -18 dB, đỉnh dưới 0 dB |

---

## Đợt 3 — 05/10/2026: video bài giảng Unit 1 Speaking 1 và 2

Nhánh `claude/gallant-ramanujan-ym30oy` đặt lại từ `main` tại `9c436de` (đã merge PR #3).

### Yêu cầu

Tạo video nói tiếng Anh dạy Speaking Unit 1 (Speaking 1: talking about personal information; Speaking 2:
exchanging personal information), dạy cả từ mới, mỗi bài một video, giọng miễn phí có hai người; gắn video vào
section Unit 1 trong app.

### Đã làm

| Việc | Cách làm |
|---|---|
| Công cụ dựng video | `agents/lesson_video`: kịch bản YAML → đọc từng câu bằng Flite → Pillow vẽ slide → ffmpeg ghép MP4 có chương → `lessons.json`. Tách khỏi agent nhập sách, không đụng `book.json` / `plan.json` |
| Giọng đọc | Hai giọng Flite có sẵn trên Ubuntu (`libflite1`): Emma — cô giáo, `cmu_us_slt` (nữ); Tom — học viên, `cmu_us_rms` (nam). Đọc chậm hơn bình thường 10%. Hugging Face (Kokoro, Piper) bị chặn trong môi trường cloud; chạy model Kokoro lấy từ npm thì bị chặn quyền vì là model tải từ ngoài → dùng Flite |
| Speaking 1 (8:06) | Giới thiệu · Hôm nay học gì · 10 từ mới (nghe Emma, nhắc lại theo Tom, câu ví dụ) · Bài A: nối 6 tranh (ảnh cắt từ trang 10) với 6 câu hỏi, có đếm ngược để tự làm, đáp án gợi ý (Answer key của sách không có bài này) · Bài B: 6 câu trả lời mẫu kèm cụm từ hữu ích · Grammar check: Do you have…? / Have you got…? và vì sao câu 1, 3 dùng hiện tại tiếp diễn · Đến lượt bạn: 6 câu, mỗi câu 10 giây · Tổng kết, bài về nhà |
| Speaking 2 (6:56) | Giới thiệu · Hôm nay học gì · 10 từ mới · Bài A: nối 8 câu hỏi với 8 câu trả lời (Tom hỏi, Emma trả lời và đọc đáp án) · Pronunciation check (what's, âm yếu của are, do) · Watch out: 4 lỗi hay gặp · Bài C: hội thoại mẫu · Đến lượt bạn: 8 câu, mỗi câu 8 giây · Tổng kết |
| Gắn vào Unit 1 | Thẻ Unit 1 ở màn chi tiết sách có dòng "Video bài giảng" với hai nút; bấm thì mở phiên Unit 1 · Speaking & Vocabulary, cuộn tới video và phát. Trong phiên, hoạt động Speaking & Vocabulary có trình phát từng video, nút nhảy theo chương (sáng nút chương đang phát), nhớ vị trí đang xem khi quay lại. Trình duyệt không phát được MP4 H.264 hoặc không tải được file thì báo rõ |

### File thêm

| File | Vai trò |
|---|---|
| `agents/lesson_video/__init__.py`, `__main__.py`, `cli.py` | Lệnh `python -m lesson_video check|build` |
| `agents/lesson_video/script.py` | Model kịch bản (pydantic), chuẩn hóa dòng thoại, kiểm tra với `book.json` |
| `agents/lesson_video/tts.py` | Giọng Flite qua `ctypes`; bộ đọc `silent` |
| `agents/lesson_video/timeline.py` | Ghép tiếng, tính thời lượng từng khung hình, đếm ngược, chương |
| `agents/lesson_video/slides.py` | Vẽ slide 9 kiểu cảnh bằng Pillow |
| `agents/lesson_video/video.py` | ffmpeg → MP4 có chương; ghi `lessons.json` |
| `agents/tests/test_lesson_video.py` | 14 test (kể cả 7 kịch bản lỗi, Flite hai giọng, dựng video thật bằng `silent`, hồi quy kịch bản đã commit) |
| `books/ielts_target_5_0/lessons/U01-speaking-1.yaml`, `U01-speaking-2.yaml` | Kịch bản hai video |
| `books/ielts_target_5_0/lessons/U01-speaking-1.mp4` (6,7 MB), `U01-speaking-2.mp4` (5,3 MB) | Video 1280×720, H.264 + AAC mono, có chương |
| `books/ielts_target_5_0/lessons/lessons.json` | Mục lục video: hoạt động, unit, thời lượng, chương, giọng |

### File sửa

| File | Thay đổi |
|---|---|
| `agents/pyproject.toml` | Thêm gói `lesson_video`, lệnh `lesson-video`, extra `[video]` (pillow, numpy) |
| `web/build.py` | Nhúng `books/<sách>/lessons/lessons.json` vào `BOOKS[id].lessons` |
| `web/src/book/core.js` | `lessonsOf`, `lessonSession`, `chapterAt` |
| `web/src/book/ui.js` | Nút video trên thẻ unit; khối "Video bài giảng" trong hoạt động của phiên (trình phát, chương, báo lỗi) |
| `web/src/book/book.css` | Kiểu khối video, nút chương |
| `tests/web/book-core.test.mjs` | +2 test: hàm video, dữ liệu video thật trỏ đúng hoạt động và file |
| `tests/web/book.e2e.mjs` | +1 bước: Unit 1 có 2 video, mở từ thẻ unit, 8 nút chương, máy chủ trả đoạn 206 |
| `agents/README.md`, `web/README.md`, `CLAUDE.md`, `docs/agent-hoc-tap/04-checklist.md`, `README.md` (thư mục docs) | Hướng dẫn `lesson_video`; mô tả video trong tab Sách; task P2-30 … P2-33; trạng thái |
| `web/index.html`, `web/ielts-companion.html` | Bản dựng lại |

Không xóa file nào. `book.json`, `plan.json` không đổi.

### Kiểm thử

| Lệnh | Kết quả |
|---|---|
| `cd agents && python -m pytest -q` | 26 passed (12 cũ + 14 video) |
| `node --test "tests/web/*.test.mjs"` | 13 passed |
| `node tests/web/book.e2e.mjs` | 12/12 bước OK |
| `python3 web/build.py` | 22 tài liệu + 1 sách 120 phiên, 2 video |

Chromium của Playwright không có H.264 nên e2e chỉ kiểm tra trang báo lỗi rõ ràng và máy chủ phục vụ file; giải mã
video kiểm tra bằng `ffprobe` (thời lượng khớp lời thoại, có chương) và xem khung hình trích từ MP4.

### Việc còn treo

- Giọng Flite nghe máy hơn giọng thật; muốn giọng tự nhiên (Kokoro) cần cho phép tải và chạy model ngoài (P2-32).
- Bài Speaking 2B "Listen and check" cần audio của sách, nhưng hoạt động Unit 1 · Speaking & Vocabulary trong gói chưa có track nào.

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
