# 08 — Giai đoạn 0: nền tảng A1–A2 trước lộ trình IELTS (English Unlimited)

Lộ trình 40 tuần bắt đầu từ band 3.0. Giai đoạn 0 dành cho người học lại từ đầu hoặc dưới band 3.0, để người học khác
cũng dùng được app từ con số 0. Giai đoạn này đứng **trước tuần 1** và không tính vào 40 tuần.

| Thành phần | Ở đâu |
|---|---|
| Sách, audio, hồ sơ lộ trình A2 | `books/book_english_unlimited_a2_elemetary/`: `book.yaml` (mẫu `lessons-v1`), `book.json`, `plan.json`, `report.md`, `web/` (32 đoạn PDF) |
| Sách A1 (chưa có) | Bộ tài liệu A1 đã gỡ khỏi repo ngày 26/10 (commit `7117894`); xem mục 4 |
| Vị trí trong tab Sách | `books/catalog.json`: nhóm `ielts`, hai thẻ A1 và A2 đứng trước IELTS Target 5.0 |
| Mẫu lộ trình | `agents/book_ingest/lessons.py`: nhãn track theo đĩa `track: "1.{n}"`, một PDF khai hai lần |
| Video bài giảng | `books/book_english_unlimited_a2_elemetary/lessons/` (kịch bản `.yaml`, `.mp4`, `lessons.json`); sổ tay ở mục 6 |
| Lời bài nghe (chép tự động) | `books/book_english_unlimited_a2_elemetary/work/transcripts/<track>.txt` / `.json`; lệnh `lesson_video transcribe` |

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

## 4. English Unlimited A1 Starter — chưa có sách

Thư mục `books/book_english_unlimited_A1_Starter/` từng có:
- Teacher's Book (ghi chú Unit 1–10);
- CD1 (92 track) và CD2 (69 track), đủ cả hai;
- Teacher's Pack: Progress test 1–10 kèm đáp án, worksheet, thang chấm Speaking;
- wordlist.

File Coursebook chỉ là **bản mẫu** 26 trang: mục lục, Unit 3 và một phần Unit 9. Chưa đủ để dựng lộ trình, vì mỗi
phiên cần trang sách để làm bài. Ngày 26/10 người học gỡ cả thư mục khỏi repo (commit `7117894`).

Trong tab Sách, A1 vẫn là thẻ "chưa nhập" đứng trước A2, chỉ có mục tiêu và ghi chú repo chưa có sách. Khi có lại
sách (Coursebook đầy đủ, khoảng 100 trang trở lên, cùng Teacher's Book và audio; có Self-study Pack thì càng tốt),
chép vào `books/` rồi làm như A2:
1. Viết `book.yaml` mẫu `lessons-v1`, mỗi unit 5 phiên.
2. Dò nhãn track bằng OCR nhãn màu rồi đối chiếu với Teacher's Book.
3. Chạy `ingest`.

## 5. Việc tiếp theo

- **Video bài giảng cho các unit còn lại** (P2-53): làm theo sổ tay ở mục 6. Đã xong: xem bảng độ phủ ở mục 6.8.
- **A1 Starter** (P2-52): repo chưa có sách (đã gỡ ngày 26/10).
- Đề Achievement test và đề mẫu A2 Key: nếu người học đặt file vào thư mục sách, khai thêm vào `files` và `refs` của
  bốn mục test.

## 6. Video bài giảng — sổ tay làm từng unit

Người học yêu cầu ở đợt 19: "làm luôn, xong unit nào commit push lên main unit đó; làm gì thì ghi lại để unit sau
tham khảo". Mục này là bản ghi đó. Mỗi unit làm xong thì thêm một hàng vào bảng 6.8 và ghi điều mới vào 6.6–6.7.

### 6.1 Bộ video của mỗi unit

Mỗi video gắn vào đúng một phiên, id video trùng id hoạt động. Mỗi video dài 5–10 phút. Nhãn trên thẻ unit là
`subtitle`, bắt đầu bằng kỹ năng chính.

| Video (= hoạt động) | Nhãn (`subtitle`) | Nội dung | Làm thứ |
|---|---|---|---|
| `Uxx-target` | Speaking · <nhiệm vụ của unit> | Bài nghe mẫu của Target activity (audio gốc), Task vocabulary, chuẩn bị ghi chú, bài nói mẫu của Mai, Your turn, lỗi hay gặp; phần viết của unit nếu có | 1 |
| `Uxx-explore` | Explore Speaking · … hoặc Explore Writing · … | Keyword, Across cultures / Independent learning, mẫu câu Explore Speaking hoặc bài viết mẫu Explore Writing, Your turn | 2 |
| `Uxx-lesson-1` | Listening · … (hoặc Reading · …) | Bài X.1: từ vựng (nghe từ của audio gốc), bài nghe / đọc, ngữ pháp, phát âm, Your turn | 3 |
| `Uxx-lesson-2` | Reading · … (hoặc Listening · …) | Bài X.2, như trên | 4 |

- Look again không có video riêng. Bài viết của Look again (ví dụ hồ sơ ngắn ở Unit 1) đưa vào video Speaking.
- Intro có ba video:
  - `U00-introductions` (trang 7) và `U00-letters-numbers` (trang 8), gắn vào phiên `U00-intro-1`;
  - `U00-personal-info` (trang 9), gắn vào phiên `U00-intro-2`.
- Làm Speaking và Writing trước, Listening và Reading sau, như người học muốn (đợt 16).

### 6.2 Giọng và nhân vật

| Người nói | Giọng Kokoro | Vai |
|---|---|---|
| Emma | `af_heart` | giáo viên: giảng, hỏi, chữa |
| Tom | `am_michael` | người học: trả lời mẫu, đọc bài đọc ngôi thứ nhất của nhân vật nam |
| Mai | `af_bella` | người học Việt Nam: tự giới thiệu, bài nói mẫu, trả lời Your turn bằng ví dụ Việt Nam (Huế, Đà Nẵng, tên Việt) |

- Tốc độ mặc định của lệnh build là 0,9.
- Giọng là giọng Mỹ, còn audio của sách là giọng Anh. Chỗ nào khác nhau (can't, Z) thì nói rõ cả hai đều đúng, và để
  audio gốc làm mẫu.
- Mọi câu của Emma có `vi`. Câu của Tom và Mai có `vi` khi câu khó.

### 6.3 Nguồn nội dung

| Cần | Lấy ở đâu |
|---|---|
| Đề bài, chữ trên trang | Kết xuất trang Coursebook (PyMuPDF, 120 dpi) rồi đọc ảnh. PDF là bản quét, không có lớp chữ. Trang PDF = trang in + 1 (tới trang 49), + 2 (50–65), − 65 (Part 2) |
| Đáp án, ý của bài | Teacher's Book (lớp chữ sạch): `fitz.open(...)[trang - 1].get_text()`, trang theo bảng mục 3.1 |
| Lời bài nghe | `work/transcripts/<track>.txt` và `.json` (chép tự động, có mốc từng từ). Tên riêng hay sai, nên đối chiếu với trang sách và Teacher's Book |
| Mốc `start` / `end` để phát một câu | Lấy từ `words` trong `.json`: bắt đầu trước từ đầu 0,2–0,3 giây, kết thúc sau từ cuối 0,3 giây |
| Ảnh minh hoạ | `image: {pdf: course-book, page: <trang PDF>, clip: [x0, y0, x1, y1]}`, đơn vị điểm PDF. Lấy toạ độ từ ảnh 120 dpi nhân 0,6 |

Chép lời một đĩa (một lần cho cả sách; kết quả đã commit ở `work/transcripts/`):

```bash
pip install sherpa-onnx          # model Parakeet: ~/.cache/lesson_video/asr/ (xem đầu agents/lesson_video/transcribe.py)
cd agents && python -m lesson_video transcribe ../books/book_english_unlimited_a2_elemetary 2.1 2.57
```

### 6.4 Quy trình một unit

1. Đọc trang của unit (8 trang) và Teacher's Book của unit. Ghi đáp án vào đầu kịch bản.
2. Viết bốn kịch bản `books/book_english_unlimited_a2_elemetary/lessons/Uxx-*.yaml`. Chép phần đầu (speakers, tag)
   từ kịch bản của Unit 1.
3. `python -m lesson_video check <kịch bản>`.
4. Soát cách đọc: `python -m lesson_video phonemes <kịch bản>` in phiên âm Kokoro của mọi câu có tên riêng, chữ cái,
   số, từ đồng tự (live, read, use, bow, close…) và đánh dấu ⚠ các lỗi đã gặp. Sai thì viết `say` (bảng 6.6). Từ
   riêng của unit thì thêm `--watch từ …`; `--all` in mọi câu.
5. Xem trước không tiếng: `build … --engine silent --out <thư mục tạm> --work <thư mục tạm>/w`, rồi ghép vài khung
   hình mỗi cảnh thành một ảnh để soát: chữ tràn, ảnh cắt lệch, chữ quá nhỏ.
6. Dựng thật lần lượt từng video (Kokoro dùng hết 4 lõi, mỗi video 15–20 phút). Không chạy hai lần dựng cùng lúc:
   `flock /tmp/kokoro.lock python -m lesson_video build <kịch bản> --engine kokoro`. Nhiều lệnh cùng chờ một khóa
   thì không chạy theo thứ tự gọi; muốn đúng thứ tự (xong Unit này mới tới Unit sau) thì dùng một vòng lặp đọc danh
   sách id từ file, dựng từng id rồi ghi lại id đã xong. Máy khởi động lại giữa chừng thì chạy lại lệnh: tiếng các câu
   đã đọc nằm trong `~/.cache/lesson_video/tts`, nên chỉ đọc nốt phần còn lại.
7. `python3 web/build.py`. Chạy các kiểm tra ở mục 9 file 06. Mở phiên trong app xem nút video, thêm hàng vào bảng 6.8,
   ghi 04 / 05. Commit, đẩy `main` (xem mục 6.5 cuối).

### 6.5 Quy ước kịch bản

- `track: "1.7"` phải có ngoặc kép, vì YAML đọc `1.20` thành số 1.2. Bỏ câu đọc số track ở đầu file ("Track 7"):
  `start` bắt đầu sau nó.
- Bài nghe dài có lời in sẵn trong sách thì phát nguyên bài một lần. Bài điền từ thì phát từng câu, mỗi câu một dòng
  `track` kèm `focus`; `reveal` đặt ở dòng nói đáp án ngay sau.
- Bài đọc (`passage`): người đọc đọc từng câu, mỗi câu một dòng. Một dòng dài cả đoạn sẽ bị cắt ở thanh phụ đề.
  Emma chỉ ý chính bằng `mark`.
- Your turn dùng cảnh `qa`: câu hỏi kèm `pause: 1.5` (không dùng `wait` — người học tự tạm dừng, theo ý ở đợt 14),
  rồi tới câu trả lời mẫu. Ai hỏi ai trả lời thì khai `ask` / `by` (ví dụ `ask: tom, by: mai`).
- Chữ trên màn hình phải khớp lời đọc. Không viết chữ tiếng Việt vào câu tiếng Anh; nghĩa tiếng Việt để ở `vi`.
- Cảnh `letter` dùng cho hội thoại có lời in sẵn: Emma giảng trong cảnh này thì khai `roles: {emma: teacher}`, để nhãn
  không ghi "Emma is reading".
- Track bị thiếu (CD1: 1.27, 1.33, 1.36, 1.39, 1.51):
  - bài "nghe lại để kiểm tra" (1.27, 1.36) thường là các câu đã có trong bài nghe chính: cắt đúng câu đó từ track
    chính (1.26, 1.34) theo mốc từng từ;
  - bài nghe riêng không có ở track nào khác (1.33 Moira và Sam, 1.39 Ruth): nhân vật kể lại theo đáp án Teacher's Book,
    và nói rõ trên màn hình là không có audio;
  - ghi track thiếu và cách thay vào đầu kịch bản.
- Thứ tự commit (mỗi unit một lần): commit trên `origin/main`, `git push origin HEAD:main`, rồi
  `git merge -s ours origin/claude/<nhánh phiên>` và đẩy nhánh phiên. Hàng đợi dựng vẫn chạy trong lúc commit thì làm
  commit trong một `git worktree` riêng ở `origin/main`: chép file của unit sang, chạy `lesson_video prune` để
  `lessons.json` chỉ còn video đã có kịch bản, rồi dựng web và chạy kiểm tra ngay trong worktree.

### 6.6 Cách đọc (`say`) riêng của sách này

| Chữ | `say` | Ghi chú |
|---|---|---|
| Mai, Nguyen, Lan, Minh, Hoa | `My`, `Win`, `Lahn`, `Min`, `Hwah` | Tên Việt |
| Hue, Da Nang, Hanoi | `Whey`, `Dah Nahng`, `Ha Noi` | Địa danh Việt |
| Sameh, Anri, Graz, Maite, Michel, Seung-wan, Uppsala, Kyoto | `Sah-meh`, `Ahn-ree`, `Grahts`, `My-tay`, `Mee-shell`, `Sung-wan`, `Oop-sah-lah`, `Kee-oh-toh` | Tên riêng trong sách |
| Chữ cái rời: A, B, C, D, E, F, G, H, I, J, K, L, R, W, Y, Z | `eigh`, `bee`, `see`, `dee`, `ee`, `ef`, `gee`, `aitch`, `eye`, `jay`, `kay`, `el`, `ar`, `double-you`, `why`, `zee` | Đánh vần: tách bằng dấu chấm `en. gee. you.` |
| 0161 228 3434 · 152 · M20 6RU | `oh one six one, double two eight, three four three four` · `a hundred and fifty-two` · `em twenty, six, ar, you` | Số điện thoại, số nhà, mã bưu chính |
| bows (cúi chào) | `boughs` | Kokoro đọc /boʊz/ (cái nơ) |
| "the sound ay", "a short e" | viết lại câu, không đánh vần âm | Kokoro đọc ay là /aɪ/, e là /iː/ |
| page 7, Exercise 3, lesson 1.1 | `page seven`, `Exercise three`, `lesson one point one` | Số đứng riêng đọc chắc hơn khi viết thành chữ |
| lives, live (động từ) | `livz`, `liv` | Sau danh từ, tên riêng ("My mother lives", "Erkan lives") và trong danh sách từ, Kokoro đọc /laɪvz/, /laɪv/. Sau đại từ (he lives, I live) thì đúng. Lệnh `phonemes` báo ⚠ |
| use, uses (động từ) | `yooz`, `yoozes` | Câu mệnh lệnh ("Use these phrases", "For the past, use was …") và sau danh từ ("people use both", "nobody uses"), Kokoro đọc /juːs/ như danh từ. "Can I use", "We use" thì đúng. Lệnh `phonemes` báo ⚠ |
| 2009, 1989, 31 July, August 1 and 2, 9am | `two thousand and nine`, `nineteen eighty-nine`, `the thirty-first of July`, `August first and second`, `nine eigh em` | Năm, ngày tháng, giờ |
| Ju-Yung, Kildare, Sofasurfing.com | `Joo-young`, `Kill-dare`, `Sofa surfing dot com` | Tên riêng Unit 2 |
| xin chào, bún bò Huế | `sin chow`, `Boon baw Whey` | Chữ Việt trong câu tiếng Anh: viết chữ Việt ở dòng thoại, cách đọc gần đúng ở `say` |

### 6.7 Lỗi đã gặp

- Thanh đầu video luôn ghi "IELTS Target 5.0". Nay lấy tên sách từ `book.json` (đợt 19).
- Phụ đề một dòng quá dài bị cắt. Đã tách bài đọc thành từng câu (6.5).
- Ảnh cắt dính cả chữ của bài tập bên dưới: chấp nhận được khi chữ đó là đề bài (tranh chào hỏi Unit 1).
- Máy khởi động lại giữa lúc dựng: chạy lại lệnh dựng, các câu đã đọc lấy lại từ bộ nhớ đệm.
- Lệnh chờ `while pgrep -f <tên>` tự khớp với chính nó và không bao giờ dừng. Kiểm tra bằng
  `ps aux | grep "[t]ên"`.
- Ảnh dải tranh `grid: 4` chia đều theo bề ngang, nên nhãn tròn A–D ở góc tranh bị cắt sang ô bên cạnh. Chọn `clip`
  bắt đầu trước nhãn của tranh đầu khoảng 12 px (ảnh 120 dpi) để mỗi ô chứa trọn nhãn của nó. Xem ảnh đã cắt:
  `Slides(sc.load(p), sc.book_dir(p)).images[<số cảnh>].save("x.png")` (Unit 2, bài 2.1).
- Cảnh `bullets` tự đánh số, nên `en` không bắt đầu bằng "1 …" (thành "1 1 …").
- Cảnh `vocab` mà dòng đầu không có `focus` sẽ hiện "Listen and repeat · Nghe và nhắc lại theo bạn Tom". Dòng đầu
  đặt `focus: 0` khi người đọc mẫu không phải Tom (ví dụ audio gốc).
- Cảnh `letter` mà Emma đọc to cả thư (thư trả lời của Erkan, Unit 2) thì không khai `emma: teacher`: nhãn ghi "Emma
  is reading" là đúng. Lời giảng đặt ở cảnh trước hoặc sau.

### 6.8 Độ phủ video

In lại bằng: `cd agents && python -m lesson_video coverage ../books/book_english_unlimited_a2_elemetary --unit U00 --unit U01`

#### U00 · Intro · About you — 2/2 phần có video, 3 video, 19:24 (đợt 19)

| Phần | Trang | Video | Dài | Chương |
|---|---|---|---|---|
| Giới thiệu bản thân · quốc gia, ngôn ngữ, chữ cái và số | sách tr. 7–8 | `U00-introductions` — Speaking · Introduce yourself | 5:51 | 9 |
| Giới thiệu bản thân · quốc gia, ngôn ngữ, chữ cái và số | sách tr. 7–8 | `U00-letters-numbers` — Listening · Letters, numbers and addresses | 7:14 | 9 |
| Thông tin cá nhân và can · đăng ký khoá học | sách tr. 9 | `U00-personal-info` — Grammar · Personal information, my / your, can | 6:18 | 10 |

#### U01 · People in your life — 4/5 phần có video, 4 video, 26:33 (đợt 20)

| Phần | Trang | Video | Dài | Chương |
|---|---|---|---|---|
| Bài 1 · nghe – đọc, từ vựng, ngữ pháp | sách tr. 10–11 | `U01-lesson-1` — Listening · Nice to meet you: people you know, 's, am / is / are | 6:59 | 10 |
| Bài 2 · nghe – đọc, từ vựng, ngữ pháp | sách tr. 12–13 | `U01-lesson-2` — Reading · Life's work: jobs, was / were | 6:12 | 10 |
| Target activity · nhiệm vụ nói | sách tr. 14 | `U01-target` — Speaking · Talk about someone you know well | 5:56 | 10 |
| Explore Speaking · từ khoá và giao tiếp | sách tr. 15–16 | `U01-explore` — Explore Speaking · OK, greetings, Sorry, can you say that again? | 7:26 | 12 |
| Look again · ôn tập và tự đánh giá | sách tr. 17 | không làm video riêng (mục 6.1); bài viết hồ sơ ngắn nằm trong `U01-target` | — | — |

<!-- bảng độ phủ: cập nhật sau mỗi unit -->
