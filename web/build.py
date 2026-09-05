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

PLACEHOLDER = "/*__DOCS__*/{}"

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
    if PLACEHOLDER not in tpl:
        sys.exit(f"Khong thay cho danh dau {PLACEHOLDER} trong {TEMPLATE.name}.")

    docs = collect_docs()
    if not docs:
        sys.exit("Khong tim thay file .md nao de nhung.")

    payload = js_safe(json.dumps(docs, ensure_ascii=False, separators=(",", ":")))
    artifact = tpl.replace(PLACEHOLDER, payload)
    OUT_ARTIFACT.write_text(artifact, encoding="utf-8")

    head_tags = re.findall(HEAD_TAG_RE, artifact, re.M)
    body = re.sub(HEAD_TAG_RE + r"\n?", "", artifact, flags=re.M)
    standalone = HEAD.format(head_tags="\n".join(head_tags)) + body.lstrip() + "\n</body>\n</html>\n"
    OUT_STANDALONE.write_text(standalone, encoding="utf-8")

    total_words = sum(len(v.split()) for v in docs.values())
    print(f"Da nhung {len(docs)} file markdown ({total_words:,} tu).")
    for rel in docs:
        print(f"  - {rel}")
    print()
    print(f"{OUT_ARTIFACT.name:24s} {len(artifact):>9,} bytes  -> dang len Claude Artifact")
    print(f"{OUT_STANDALONE.name:24s} {len(standalone):>9,} bytes  -> tu host")


if __name__ == "__main__":
    main()
