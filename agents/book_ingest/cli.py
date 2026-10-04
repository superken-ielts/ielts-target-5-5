"""Dòng lệnh `book` (hoặc `python -m book_ingest`).

    book inventory  <thư mục sách>            liệt kê file, không in nội dung sách
    book profile    <thư mục sách> --pdf X --pages 1-8 [--llm manual|api]
    book ingest     <thư mục sách> [--force] [--no-ocr]
    book review     <thư mục sách> [--accept-all | --list]
    book validate   <thư mục sách> [--hashes]
    book schemas    [--out schemas/]
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from . import llm, pipeline, review as rv, scan as sc, validate as vd
from .schemas import SCHEMAS


def _pages(spec: str) -> list[int]:
    out: list[int] = []
    for part in spec.split(","):
        if "-" in part:
            a, b = part.split("-")
            out += list(range(int(a), int(b) + 1))
        else:
            out.append(int(part))
    return out


def export_schemas(out: Path) -> list[Path]:
    out.mkdir(parents=True, exist_ok=True)
    paths = []
    for name, model in SCHEMAS.items():
        p = out / f"{name}.schema.json"
        p.write_text(json.dumps(model.model_json_schema(by_alias=True), ensure_ascii=False, indent=1) + "\n",
                     encoding="utf-8")
        paths.append(p)
    return paths


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(prog="book", description="Agent nhập sách → book.json, plan.json")
    sub = ap.add_subparsers(dest="cmd", required=True)

    p = sub.add_parser("inventory", help="liệt kê file của bộ sách")
    p.add_argument("dir", type=Path)

    p = sub.add_parser("profile", help="đọc mục lục để viết book.yaml")
    p.add_argument("dir", type=Path)
    p.add_argument("--pdf", required=True, help="file PDF chính, đường dẫn tương đối trong thư mục sách")
    p.add_argument("--pages", default="1-8", help="trang PDF chứa mục lục, ví dụ 4 hoặc 3-5")
    p.add_argument("--llm", choices=["manual", "api"], default="manual")
    p.add_argument("--model", default=None)

    p = sub.add_parser("ingest", help="chạy toàn bộ luồng nhập sách")
    p.add_argument("dir", type=Path)
    p.add_argument("--force", action="store_true", help="quét lại file dù đã có work/scan.json")
    p.add_argument("--no-ocr", action="store_true", help="không chạy OCR, chỉ dùng cache")

    p = sub.add_parser("review", help="duyệt các mục chưa chắc")
    p.add_argument("dir", type=Path)
    g = p.add_mutually_exclusive_group()
    g.add_argument("--accept-all", action="store_true", help="đồng ý mọi đề xuất")
    g.add_argument("--list", action="store_true", help="chỉ liệt kê")

    p = sub.add_parser("validate", help="kiểm tra gói sách")
    p.add_argument("dir", type=Path)
    p.add_argument("--hashes", action="store_true", help="kiểm tra cả sha256 (chậm với file lớn)")

    p = sub.add_parser("schemas", help="xuất JSON Schema")
    p.add_argument("--out", type=Path, default=Path(__file__).resolve().parents[2] / "schemas")

    a = ap.parse_args(argv)

    if a.cmd == "inventory":
        print(sc.inventory(a.dir))
        return 0
    if a.cmd == "profile":
        pdf = a.dir / a.pdf
        pages = _pages(a.pages)
        work = pipeline.work_dir(a.dir)
        if a.llm == "manual":
            guide = llm.manual(pdf, pages, work)
            print(f"Đã vẽ trang {pages} và ghi hướng dẫn: {guide}")
            return 0
        toc = llm.api(pdf, pages, model=a.model)
        files = {"course-book": {"kind": "pdf", "path": a.pdf, "page_offset": 0}}
        out = a.dir / "book.draft.yaml"
        out.write_text(llm.draft_yaml(toc, files, a.dir.name.replace("_", "-")), encoding="utf-8")
        print(f"Đã ghi bản nháp {out} — kiểm tra rồi đổi tên thành book.yaml")
        return 0
    if a.cmd == "ingest":
        return pipeline.run(a.dir, force=a.force, allow_ocr=not a.no_ocr).code
    if a.cmd == "review":
        path = pipeline.work_dir(a.dir) / "review.json"
        review = rv.load(path)
        if a.list:
            for i in review.items:
                print(f"[{i.severity}] {i.id}: {i.message} → {i.decision or 'chưa quyết'}")
            return 0
        n = rv.accept_all(review) if a.accept_all else rv.interactive(review)
        rv.save(path, review)
        left = len(rv.open_items(review))
        print(f"Đã quyết {n} mục, còn {left} mục mở.")
        return 0 if left == 0 else pipeline.NEEDS_REVIEW
    if a.cmd == "validate":
        problems = vd.validate(a.dir, check_hashes=a.hashes)
        for p in problems:
            print(p)
        if not problems:
            print("OK", json.dumps(vd.summary(a.dir), ensure_ascii=False))
        return 0 if not problems else pipeline.INVALID
    if a.cmd == "schemas":
        for p in export_schemas(a.out):
            print(p)
        return 0
    return 1


if __name__ == "__main__":
    sys.exit(main())
