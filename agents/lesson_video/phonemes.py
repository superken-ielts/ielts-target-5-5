"""Soát cách Kokoro đọc lời thoại tiếng Anh trước khi dựng.

    python -m lesson_video phonemes <kịch bản.yaml>… [--all] [--watch từ …]

In phiên âm (cùng bộ tách âm Kokoro dùng khi đọc) của các câu dễ đọc sai: có tên riêng, chữ cái rời, số hoặc từ đồng
tự (live, read, use…). Câu khớp một lỗi đã gặp thì đánh dấu ⚠ kèm cách sửa bằng `say` (bảng ở file 08 mục 6.6).
Lệnh chỉ để soát: từ đồng tự có khi đúng thật (live music, the use of…), nên không làm hỏng lần dựng.
"""
from __future__ import annotations

import re
from pathlib import Path
from typing import Callable, Iterator, NamedTuple

from . import script as sc

# Lỗi đã gặp: (từ trong câu, phiên âm sai, cách sửa). Chỉ sai khi từ là động từ ở hiện tại.
KNOWN = [
    (re.compile(r"\buses?\b", re.I), "jˈuːs", "use (động từ) đọc /juːs/ như danh từ → say: yooz, yoozes"),
    (re.compile(r"\blives?\b", re.I), "lˈaɪv", "live, lives (động từ) đọc /laɪv/ → say: liv, livz"),
    (re.compile(r"\breads?\b", re.I), "ɹˈɛd", "read (hiện tại) đọc /rɛd/ như quá khứ → say: reed"),
]
HOMOGRAPHS = {"live", "lives", "read", "use", "uses", "close", "record", "present", "minute", "wind", "tear", "lead",
              "object", "content", "desert", "row", "bow", "bows", "wound"}
NOT_NAMES = {"I", "I'm", "I'd", "I've", "I'll", "OK"}


class Row(NamedTuple):
    scene: int
    speaker: str
    text: str
    phonemes: str
    warnings: list[str]


def _risky(text: str, watch: set[str]) -> bool:
    words = {w.lower() for w in re.findall(r"[A-Za-z][A-Za-z'-]*", text)}
    if words & (HOMOGRAPHS | watch) or re.search(r"\d", text):
        return True
    for sentence in re.split(r"[.!?:]\s+", text):
        tokens = re.findall(r"[A-Za-z][A-Za-z'-]*", sentence)
        if any(t[0].isupper() and t not in NOT_NAMES for t in tokens[1:]):   # tên riêng giữa câu
            return True
        if any(len(t) == 1 and t not in ("a", "A", "I") for t in tokens):      # chữ cái rời
            return True
    return False


def review(lesson: sc.Lesson, phonemize: Callable[[str, str], str], watch: set[str] = frozenset(),
           every: bool = False) -> Iterator[Row]:
    """Các câu tiếng Anh cần soát (hoặc mọi câu nếu `every`), kèm phiên âm và cảnh báo lỗi đã gặp."""
    watch = {w.lower() for w in watch}
    for i, scene in enumerate(lesson.scenes):
        for ln in scene.lines:
            if not ln.speaker:
                continue
            sp = lesson.speakers[ln.speaker]
            if sp.lang != "en":
                continue
            text = ln.spoken
            if not every and not _risky(text, watch) and not any(rx.search(text) for rx, _, _ in KNOWN):
                continue
            lang = "en-gb" if sp.voice_for("kokoro").startswith("b") else "en-us"
            ph = phonemize(text, lang)
            warns = [msg for rx, bad, msg in KNOWN if rx.search(text) and bad in ph]
            yield Row(i, ln.speaker, text, ph, warns)


def tokenizer() -> Callable[[str, str], str]:
    from kokoro_onnx.tokenizer import Tokenizer   # Kokoro tách âm tiếng Anh đúng bằng bộ này khi đọc
    tok = Tokenizer()
    return tok.phonemize


def run(paths: list[str], every: bool = False, watch: list[str] = (), say=print) -> int:
    phonemize = tokenizer()
    total = 0
    for p in paths:
        lesson = sc.load(Path(p))
        rows = list(review(lesson, phonemize, set(watch), every))
        say(f"{p}: {len(rows)} câu cần soát")
        for r in rows:
            say(f"  [{r.scene}] {r.speaker}: {r.text}")
            say(f"       {r.phonemes}")
            for w in r.warnings:
                say(f"       ⚠ {w}")
            total += bool(r.warnings)
    say(f"{total} câu có ⚠ (sửa bằng `say`, hoặc bỏ qua nếu đúng là danh từ / tính từ / quá khứ)")
    return 0
