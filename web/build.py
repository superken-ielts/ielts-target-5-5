#!/usr/bin/env python3
"""
Dựng trang web từ app.template.html cộng toàn bộ file markdown của lộ trình.

Sinh ra hai file, cùng nội dung nhưng khác lớp vỏ:

    ielts-companion.html   bản đăng lên Claude Artifact (không có thẻ <!doctype>,
                           <html>, <head>, <body> — nền tảng tự bọc phần đó)
    index.html             bản standalone để tự host trên Cloudflare Pages,
                           GitHub Pages hoặc mở trực tiếp bằng trình duyệt

Vì sao phải nhúng markdown vào file: trang chạy dưới một CSP chặt, không được phép
tải file từ bên ngoài. Muốn đọc tài liệu ngay trong trang thì nội dung phải nằm sẵn
trong HTML tại thời điểm dựng.

Chạy lại sau mỗi lần sửa app.template.html hoặc sửa bất kỳ file .md nào:

    python3 web/build.py
"""
import json
import pathlib
import re
import sys

WEB = pathlib.Path(__file__).parent.resolve()
ROOT = WEB.parent

TEMPLATE = WEB / "app.template.html"
OUT_ARTIFACT = WEB / "ielts-companion.html"
OUT_STANDALONE = WEB / "index.html"

P1JSON = WEB / "phase1-days.json"
P1MD = ROOT / "01a-giao-an-tung-ngay-giai-doan-1.md"

PLACEHOLDER = "/*__DOCS__*/{}"
P1_PLACEHOLDER = "/*__P1DAYS__*/{days:{},sunday:{}}"

# Lich luan phien rieng cua giai doan 1 — phai khop ROTA1 trong app.template.html.
LIS, REA, WRI, GRA = "Listening", "Reading", "Writing", "Ngữ pháp"
ROTA1 = {
    1: (LIS, "Sổ lỗi"),
    2: (REA, GRA),
    3: (WRI, LIS),
    4: (GRA, REA),
    5: (LIS, WRI),
    6: (WRI, GRA),
}
DAYNAME = {1: "Thứ Hai", 2: "Thứ Ba", 3: "Thứ Tư", 4: "Thứ Năm", 5: "Thứ Sáu", 6: "Thứ Bảy"}

# Thu tu uu tien khi liet ke; file khong nam trong danh sach van duoc gom vao cuoi.
SKIP_DIRS = {".git", "node_modules", "__pycache__"}

HEAD = """<!doctype html>
<html lang="vi">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<meta name="description" content="Lo trinh tu hoc IELTS General Training 3.0 den 5.5 trong 40 tuan: checklist theo ngay, ke hoach day du va tai lieu mien phi.">
<meta name="theme-color" content="#F1F4F3" media="(prefers-color-scheme: light)">
<meta name="theme-color" content="#0D1312" media="(prefers-color-scheme: dark)">
<link rel="icon" href="data:image/svg+xml,<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 100 100'><text y='.9em' font-size='90'>%F0%9F%93%96</text></svg>">
{head_tags}
<style>*,*::before,*::after{{box-sizing:border-box}}html,body{{margin:0}}</style>
</head>
<body>
"""

HEAD_TAG_RE = r'^\s*(<title>.*?</title>|<link\b[^>]*>)\s*$'


def write_phase1_markdown(p1: dict) -> int:
    """Sinh file markdown giao an tung ngay tu cung mot nguon du lieu voi trang web.

    Nho vay tai lieu doc offline va trang web khong bao gio lech nhau.
    """
    days, sunday = p1["days"], p1["sunday"]
    sundays = p1.get("sundays", {})

    def part(label: str, text: str, links: list) -> list:
        """Mot phan hoc: mot dong noi dung, va neu co thi mot dong link ben duoi."""
        if not text:
            return []
        rows = [f"- **{label}** — {text}"]
        if links:
            joined = " · ".join(f"[{x['n']}]({x['u']})" for x in links)
            rows.append(f"  - Bài học: {joined}")
        return rows

    def day_block(title: str, blocks: str, d: dict) -> list:
        lk = d.get("lk", {})
        rows = [f"### {title} — {d['f']}", "", f"*Hai block chính: {blocks}*", ""]
        for label, key in (("Ngữ pháp", "g"), ("Sách", "book"), ("Viết", "w"),
                           ("Nói", "s"), ("Nghe & Đọc", "lr")):
            rows += part(label, d.get(key, ""), lk.get(key))
        rows.append("")
        return rows
    out = [
        "# 01a — Giáo án từng ngày, giai đoạn 1 (tuần 1–12)",
        "",
        "> File này được **sinh tự động** bởi `web/build.py` từ `web/phase1-days.json`.",
        "> Muốn sửa nội dung thì sửa file JSON đó rồi chạy lại build, đừng sửa trực tiếp ở đây.",
        "",
        "Mỗi ngày có một điểm ngữ pháp riêng. Đó là sợi chỉ xuyên suốt cả ngày: học ở block",
        "ngữ pháp, rồi dùng lại ngay trong bài viết và lúc nói, chứ không phải một mục tách rời.",
        "",
        "Dòng **Sách** là số unit trong *Essential Grammar in Use* của Raymond Murphy — bản bìa",
        "đỏ, trình độ sơ cấp A1–B1. Đây là **sách có bản quyền, phải mua**, và là phần **tùy chọn**:",
        "toàn bộ 12 điểm ngữ pháp lõi đều đã được phủ đầy đủ bằng các nguồn miễn phí ở dòng",
        "*Bài học*. Nếu bạn có sẵn sách thì dùng thêm cho chắc; không có cũng không thiếu gì.",
        "Số unit có thể xê dịch giữa các lần tái bản, nên khi mở sách hãy đối chiếu cả tên unit.",
        "",
        "> Lưu ý về phiên bản: đừng nhầm với *English Grammar in Use* bìa xanh (trình độ B1–B2).",
        "> Bản xanh cao hơn trình độ xuất phát 3.0 và sẽ gây nản. Bản cần dùng là bìa **đỏ**.",
        "",
        "Cột **Hai block chính** là lịch luân phiên riêng của giai đoạn 1 — từ tuần 13 lịch",
        "quay về khung chung ở [file 06](06-lich-hoc-hang-ngay.md).",
        "",
        "Khung mỗi ngày: Block A 45 phút (kỹ năng chính) · Block B 20 phút (Anki + 10 từ mới) ·",
        "Block C 30 phút (Speaking, bắt buộc) · Block D 25 phút (kỹ năng phụ hoặc sổ lỗi).",
        "Ngày bận chỉ 1 tiếng thì giữ ba việc: Anki 15 phút, kỹ năng chính 30 phút, Speaking 15 phút.",
        "",
    ]
    count = 0
    for w in sorted(days, key=int):
        out += [f"## Tuần {w}", ""]
        for ix, d in enumerate(days[w], start=1):
            blocks = d.get("b") or " + ".join(ROTA1[ix])
            out += day_block(DAYNAME[ix], blocks, d)
            count += 1
        out += day_block("Chủ nhật", "Ôn tập + kiểm tra", sundays.get(w, sunday))
        out += ["---", ""]
    P1MD.write_text("\n".join(out), encoding="utf-8")
    return count


def collect_docs() -> dict:
    """Doc moi file .md duoi thu muc goc, tru chinh cac file sinh ra."""
    docs = {}
    for path in sorted(ROOT.rglob("*.md")):
        if any(part in SKIP_DIRS for part in path.parts):
            continue
        rel = path.relative_to(ROOT).as_posix()
        docs[rel] = path.read_text(encoding="utf-8")
    return docs


def js_safe(payload: str) -> str:
    """Chan chuoi lam vo the <script> bao quanh."""
    return payload.replace("</", "<\\/").replace("<!--", "<\\!--")


def main() -> None:
    if not TEMPLATE.exists():
        sys.exit(f"Khong thay {TEMPLATE.name}. Day la file nguon can sua.")

    tpl = TEMPLATE.read_text(encoding="utf-8")
    for ph in (PLACEHOLDER, P1_PLACEHOLDER):
        if ph not in tpl:
            sys.exit(f"Khong thay cho danh dau {ph} trong {TEMPLATE.name}.")

    if not P1JSON.exists():
        sys.exit(f"Khong thay {P1JSON.name} — day la nguon giao an tung ngay.")
    p1 = json.loads(P1JSON.read_text(encoding="utf-8"))

    # Sinh markdown TRUOC khi gom tai lieu, de file vua sinh cung duoc nhung vao trang.
    n_days = write_phase1_markdown(p1)

    docs = collect_docs()
    if not docs:
        sys.exit("Khong tim thay file .md nao de nhung.")

    artifact = tpl.replace(
        P1_PLACEHOLDER,
        js_safe(json.dumps(p1, ensure_ascii=False, separators=(",", ":"))),
    ).replace(
        PLACEHOLDER,
        js_safe(json.dumps(docs, ensure_ascii=False, separators=(",", ":"))),
    )
    OUT_ARTIFACT.write_text(artifact, encoding="utf-8")

    head_tags = re.findall(HEAD_TAG_RE, artifact, re.M)
    body = re.sub(HEAD_TAG_RE + r"\n?", "", artifact, flags=re.M)
    standalone = HEAD.format(head_tags="\n".join(head_tags)) + body.lstrip() + "\n</body>\n</html>\n"
    OUT_STANDALONE.write_text(standalone, encoding="utf-8")

    total_words = sum(len(v.split()) for v in docs.values())
    print(f"Da sinh {P1MD.name} tu {P1JSON.name}: {n_days} ngay hoc.")
    print(f"Da nhung {len(docs)} file markdown ({total_words:,} tu).")
    for rel in docs:
        print(f"  - {rel}")
    print()
    print(f"{OUT_ARTIFACT.name:24s} {len(artifact):>9,} bytes  -> dang len Claude Artifact")
    print(f"{OUT_STANDALONE.name:24s} {len(standalone):>9,} bytes  -> tu host")


if __name__ == "__main__":
    main()
