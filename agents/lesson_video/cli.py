"""Dòng lệnh `python -m lesson_video`.

    python -m lesson_video check <kịch bản.yaml>…
    python -m lesson_video build <kịch bản.yaml>… [--engine auto|kokoro|flite|silent] [--speed 0.9]
                                 [--model F.onnx] [--voices THƯ_MỤC] [--out THƯ_MỤC] [--work THƯ_MỤC] [--no-cache]

    python -m lesson_video coverage <thư mục sách> [--unit U01 …]

`build` ghi <id>.mp4 cạnh kịch bản và cập nhật lessons.json; có `--out` thì chỉ ghi video vào thư mục đó
(xem thử), không đụng lessons.json. `--work` giữ lại ảnh từng khung hình và file tiếng để soát.
Tiếng từng câu được lưu ở ~/.cache/lesson_video/tts nên dựng lại chỉ đọc những câu đã đổi.
"""
from __future__ import annotations

import argparse
import json
import sys
import tempfile
from pathlib import Path

from . import coverage, script as sc, timeline, tts, video
from .slides import Slides


def _check(paths: list[str]) -> int:
    bad = 0
    for p in paths:
        lesson = sc.load(Path(p))
        problems = sc.check(lesson, sc.book_dir(Path(p)))
        for msg in problems:
            print(f"{p}: {msg}")
        bad += bool(problems)
        if not problems:
            n = sum(1 for s in lesson.scenes for ln in s.lines if ln.speaker)
            print(f"{p}: OK — {len(lesson.scenes)} cảnh, {n} câu thoại, hoạt động {lesson.activity}")
    return 3 if bad else 0


def _build(args) -> int:
    engine = tts.get(args.engine, speed=args.speed, model=args.model, voices=args.voices)
    cache = None if args.no_cache else Path(args.cache)
    print(f"bộ đọc: {engine.name} ({engine.tag})")
    for p in args.lessons:
        path = Path(p).resolve()
        lesson = sc.load(path)
        bdir = sc.book_dir(path)
        problems = sc.check(lesson, bdir)
        if problems:
            print("\n".join(f"{p}: {m}" for m in problems))
            return 3
        print(f"{lesson.id}: đọc lời thoại ({engine.name})")
        tl = timeline.build(lesson, engine, cache_dir=cache, book_dir=bdir)
        voices = {k: engine.describe(s.voice_for(engine.name)) for k, s in lesson.speakers.items()}
        slides = Slides(lesson, bdir, voices)
        out = (Path(args.out).resolve() if args.out else path.parent) / f"{lesson.id}.mp4"
        with tempfile.TemporaryDirectory(prefix="lesson-") as tmp:
            work = Path(args.work).resolve() / lesson.id if args.work else Path(tmp)
            video.encode(lesson, tl, slides, out, work)
        got = video.probe(out)
        if got and abs(got - tl.total) > 1.0:
            print(f"{lesson.id}: video dài {got:.1f}s, lệch so với lời thoại {tl.total:.1f}s", file=sys.stderr)
            return 3
        mins, secs = divmod(int(round(tl.total)), 60)
        print(f"{lesson.id}: {out} — {mins}:{secs:02d}, {out.stat().st_size / 1e6:.1f} MB, {len(tl.chapters)} chương")
        if not args.out:
            book = json.loads((bdir / "book.json").read_text(encoding="utf-8"))
            entry = video.manifest_entry(lesson, sc.find_item(book, lesson.activity), tl, out, voices, engine.name)
            print(f"  cập nhật {video.write_manifest(path.parent, entry)}")
    return 0


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(prog="lesson_video", description="Dựng video bài giảng từ kịch bản YAML")
    sub = ap.add_subparsers(dest="cmd", required=True)
    c = sub.add_parser("check", help="kiểm tra kịch bản với book.json")
    c.add_argument("lessons", nargs="+")
    b = sub.add_parser("build", help="đọc lời, vẽ slide, ghép video")
    b.add_argument("lessons", nargs="+")
    b.add_argument("--engine", default="auto", choices=["auto", "kokoro", "flite", "silent"],
                   help="auto = kokoro nếu tìm thấy model, không thì flite")
    b.add_argument("--speed", type=float, default=0.9, help="tốc độ đọc (1.0 = bình thường; 0.9 chậm hơn cho người mới)")
    b.add_argument("--model", help="file model Kokoro .onnx (mặc định: biến KOKORO_MODEL hoặc ~/.cache/lesson_video/kokoro/*.onnx)")
    b.add_argument("--voices", help="thư mục giọng Kokoro *.bin hoặc file .npz (mặc định: KOKORO_VOICES hoặc …/kokoro/voices)")
    b.add_argument("--cache", default=str(tts.HOME / "tts"), help="thư mục lưu tiếng từng câu")
    b.add_argument("--no-cache", action="store_true", help="không dùng bộ nhớ tiếng đã đọc")
    b.add_argument("--out", help="ghi video vào thư mục này, không cập nhật lessons.json")
    b.add_argument("--work", help="giữ khung hình và file tiếng ở thư mục này")
    v = sub.add_parser("coverage", help="bảng phần nào của unit đã có video, phần nào chưa")
    v.add_argument("book", help="thư mục sách (có book.json)")
    v.add_argument("--unit", action="append", help="chỉ in unit này (lặp lại được), ví dụ --unit U01")
    args = ap.parse_args(argv)
    if args.cmd == "coverage":
        print(coverage.to_markdown(coverage.coverage(Path(args.book), args.unit)))
        return 0
    try:
        return _check(args.lessons) if args.cmd == "check" else _build(args)
    except tts.TTSError as e:
        print(e, file=sys.stderr)
        return 2
