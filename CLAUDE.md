# Quy ước repo

Lộ trình tự học IELTS General Training 3.0 → 5.5 (markdown ở gốc repo), app học một file HTML (`web/`),
và agent nhập sách (`agents/`). Kế hoạch kỹ thuật và checklist: `docs/agent-hoc-tap/`.

## Sửa app

- Sửa `web/app.template.html` hoặc `web/src/book/*`, **không** sửa `web/index.html`, `web/ielts-companion.html`
  hay `01a-giao-an-tung-ngay-giai-doan-1.md` — ba file này do build sinh ra.
- Sau mỗi lần sửa template, mã tab Sách, bất kỳ file `.md` nào hoặc `books/*/book.json`: chạy `python3 web/build.py`
  và commit cả hai bản dựng.
- JS thuần, không framework. Dữ liệu từ người dùng hoặc từ gói sách chỉ hiện bằng `textContent`.
- Mã chèn vào trang không được chứa chuỗi đóng thẻ `</` (build sẽ báo lỗi).

## Agent nhập sách

- Skill: `.claude/skills/book-ingest/SKILL.md`. Chạy: `cd agents && python -m book_ingest ingest ../books/<sách>`.
- Không sửa tay `book.json` / `plan.json` / `report.md`: sửa `book.yaml` hoặc quyết định trong `work/review.json`
  rồi chạy lại. Đổi model trong `schemas.py` thì chạy `python -m book_ingest schemas`.

## Video bài giảng

- Kịch bản `books/<sách>/lessons/<id>.yaml`; dựng: `cd agents && python -m lesson_video build ../books/<sách>/lessons/<id>.yaml`
  rồi chạy `python3 web/build.py`. Cần ffmpeg và giọng Kokoro (model q8 + file giọng ở `~/.cache/lesson_video/kokoro/`,
  xem `agents/README.md`); không có model thì công cụ dùng Flite (`libflite1`) — đừng commit video Flite đè video Kokoro.
- Không sửa tay `lessons.json` / `.mp4`. Chữ trên màn hình ở dòng thoại, cách đọc khác (chữ cái, số, tên riêng) ở `say`.
- Làm video mới: theo quy trình và bảng độ phủ ở `docs/agent-hoc-tap/06-video-bai-giang.md`; xong thì cập nhật bảng đó
  (`python -m lesson_video coverage ../books/<sách> --unit U0x`).

## Kiểm tra trước khi commit

```bash
python3 web/build.py && git diff --stat                 # bản dựng phải khớp nguồn
cd agents && python -m pytest -q && cd ..                 # agent (kể cả hồi quy trên sách thật)
node --test "tests/web/*.test.mjs"                        # hàm thuần của tab Sách
node tests/web/book.e2e.mjs                               # đầu-cuối, cần Playwright
```

## Ghi lại thay đổi

Mỗi đợt triển khai: tick `docs/agent-hoc-tap/04-checklist.md` và ghi chi tiết thêm/sửa/xóa vào
`docs/agent-hoc-tap/05-lich-su-thay-doi.md`.
