"""Đọc từng câu thoại, ghép tiếng thành một dải, tính khung hình nào hiện trong bao lâu."""
from __future__ import annotations

import hashlib
import json
import math
import subprocess
from dataclasses import dataclass, field
from pathlib import Path
from typing import Callable, Optional

import numpy as np

from . import ja
from .script import Lesson, reading_plan
from .tts import TTSError

LEAD = 0.5   # im lặng đầu video
TAIL = 1.5   # im lặng cuối video
PEAK = 0.8   # chuẩn hóa đỉnh mỗi câu để hai giọng to ngang nhau
ECHO_RATIO, ECHO_EXTRA = 1.3, 1.0  # `echo`: người học cần lâu hơn người đọc một chút để nhắc lại cả câu
VAD_RATE = 16000  # tách file nghe theo khoảng lặng ở tần số cố định: `check` và lúc dựng ra cùng một kết quả
LEADIN = 0.15     # file nghe đọc từng chữ: chữ sau sáng lên trước tiếng một chút


def echo_seconds(spoken: float) -> int:
    """Khoảng lặng (giây, số nguyên để đếm ngược tròn) cho người học nhắc lại một câu dài `spoken` giây."""
    return max(3, math.ceil(spoken * ECHO_RATIO + ECHO_EXTRA))


@dataclass
class Frame:
    scene: int
    focus: Optional[int]
    revealed: frozenset
    speaker: Optional[str]
    text: str
    vi: str
    countdown: Optional[int] = None
    note: str = ""
    mark: tuple = ()  # cụm từ tô vàng (cảnh passage)
    audio: str = ""   # đang phát file nghe của sách (mã file)
    start: float = 0.0
    dur: float = 0.0
    en: str = ""      # cảnh jp: nghĩa tiếng Anh của câu tiếng Nhật / file nghe đang phát
    hl: tuple = ()    # cảnh jp: chữ trên thẻ đang được đọc (số thứ tự theo ja.card_tokens)
    done: tuple = ()  # cảnh jp: chữ vừa đọc xong trong câu này


@dataclass
class Timeline:
    frames: list[Frame]
    audio: np.ndarray
    rate: int
    chapters: list[tuple[float, str]] = field(default_factory=list)

    @property
    def total(self) -> float:
        return len(self.audio) / self.rate


def _resample(x: np.ndarray, src: int, dst: int) -> np.ndarray:
    if src == dst or not len(x):
        return x
    n = int(round(len(x) * dst / src))
    return np.interp(np.linspace(0, len(x) - 1, n), np.arange(len(x)), x.astype(np.float32)).astype(np.int16)


def _norm(x: np.ndarray) -> np.ndarray:
    peak = int(np.abs(x.astype(np.int32)).max()) if len(x) else 0
    if peak == 0:
        return x
    return np.clip(x.astype(np.float32) * (PEAK * 32767 / peak), -32768, 32767).astype(np.int16)


def _decode(path: Path, rate: int, start: float, end: Optional[float]) -> np.ndarray:
    """Đọc một đoạn file nghe (mp3, wav…) thành mono int16 ở tần số `rate` bằng ffmpeg."""
    cmd = ["ffmpeg", "-v", "error", "-ss", f"{start:.3f}"] + (["-to", f"{end:.3f}"] if end is not None else [])
    cmd += ["-i", str(path), "-ac", "1", "-ar", str(rate), "-f", "s16le", "-"]
    out = subprocess.run(cmd, capture_output=True, check=True).stdout
    return np.frombuffer(out, dtype=np.int16).copy()


def speech_spans(x: np.ndarray, rate: int, floor_db: float = -35.0, min_sil: float = 0.2, min_speech: float = 0.08,
                 win: float = 0.02) -> list[tuple[float, float]]:
    """Các đoạn có tiếng (giây) của một đoạn nghe: khung 20 ms to hơn đỉnh − 35 dB là có tiếng. Nghỉ ngắn hơn
    `min_sil` (âm ngắt っ, phụ âm tắc) không tách chữ; mẩu ngắn hơn `min_speech` (tiếng lách cách) bỏ đi."""
    n = max(1, int(rate * win))
    k = len(x) // n
    if k == 0:
        return []
    rms = np.sqrt((x[:k * n].astype(np.float32).reshape(k, n) ** 2).mean(axis=1))
    if rms.max() <= 0:
        return []
    edges = np.diff(np.concatenate([[0], (rms > rms.max() * 10 ** (floor_db / 20)).astype(np.int8), [0]]))
    merged: list[list[float]] = []
    for a, b in zip(np.flatnonzero(edges == 1) * n / rate, np.flatnonzero(edges == -1) * n / rate):
        if merged and a - merged[-1][1] < min_sil:
            merged[-1][1] = float(b)
        else:
            merged.append([float(a), float(b)])
    return [(round(a, 3), round(b, 3)) for a, b in merged if b - a >= min_speech]


def track_spans(path: Path, start: float = 0.0, end: Optional[float] = None) -> list[tuple[float, float]]:
    """Đoạn có tiếng của một đoạn file nghe, tính từ `start` — mỗi đoạn là một chữ khi file đọc từng chữ một."""
    return speech_spans(_decode(path, VAD_RATE, start, end), VAD_RATE)


def step_of(lesson: Lesson, ln) -> float:
    """Nghỉ giữa hai chữ khi đọc từng chữ một: `step` của câu, không thì của bài; 0 = đọc liền."""
    return ln.step if ln.step is not None else (lesson.step or 0.0)


def build(lesson: Lesson, engine, say: Callable[[str], None] = print, cache_dir: Optional[Path] = None,
          book_dir: Optional[Path] = None) -> Timeline:
    """`cache_dir`: lưu tiếng từng câu theo (bộ đọc, giọng, chữ) — dựng lại chỉ đọc những câu đã đổi.
    `book_dir`: thư mục sách, cần khi kịch bản phát file nghe (`track`)."""
    voices: dict[str, str] = {}
    for key, sp in lesson.speakers.items():  # báo lỗi giọng trước khi đọc câu nào
        try:
            voices[key] = sp.voice_for(engine.name)
        except ValueError as e:
            raise TTSError(str(e)) from None
        engine.check(voices[key])
    memo: dict[tuple, tuple[np.ndarray, int]] = {}

    def synth(text: str, voice: str, speed: Optional[float] = None) -> tuple[np.ndarray, int]:
        """`speed`: tốc độ riêng của câu hoặc người nói; None = tốc độ của bộ đọc (khóa bộ nhớ như cũ)."""
        key = (voice, text, speed)
        if key in memo:
            return memo[key]
        path = None
        if cache_dir is not None and engine.name != "silent":
            h = hashlib.sha1((f"{engine.tag}\n{voice}\n{text}" + (f"\n{speed}" if speed else "")).encode("utf-8")).hexdigest()
            path = Path(cache_dir) / h[:2] / f"{h}.npz"
            if path.exists():
                with np.load(path) as z:
                    memo[key] = (z["data"], int(z["rate"]))
                return memo[key]
        data, r = engine.synth(text, voice) if speed is None else engine.synth(text, voice, speed=speed)
        if path is not None:
            path.parent.mkdir(parents=True, exist_ok=True)
            np.savez(path, data=data, rate=r)
        memo[key] = (data, r)
        return data, r

    rate: Optional[int] = None
    parts: list[np.ndarray] = []
    frames: list[Frame] = []
    chapters: list[tuple[float, str]] = []
    pos = 0  # số mẫu đã ghép

    def silence(sec: float) -> np.ndarray:
        return np.zeros(int(round(sec * (rate or 16000))), dtype=np.int16)

    def add(samples: np.ndarray, frame: Optional[Frame]):
        nonlocal pos
        parts.append(samples)
        if frame is not None:
            frame.start = pos / rate
            frames.append(frame)
        elif frames:
            frames[-1].dur += len(samples) / rate
        if frame is not None:
            frame.dur = len(samples) / rate
        pos += len(samples)

    def countdown(si, focus, revealed, mark, seconds: float, note: str, vi: str, en: str = "", hl: tuple = ()):
        """Khoảng lặng có đếm ngược: mỗi giây một khung (giây lẻ nằm ở khung đầu)."""
        left, k = seconds, math.ceil(seconds)
        while left > 1e-6:
            step = left - (k - 1) if k > 1 else left
            add(silence(step), Frame(si, focus, frozenset(revealed), None, "", vi, countdown=k, note=note, mark=mark,
                                     en=en, hl=hl))
            left -= step
            k -= 1

    def start_audio(r: int):
        nonlocal rate, pos
        if rate is None:
            rate = r
            parts.append(silence(LEAD))
            pos = len(parts[0])

    files: Optional[dict] = None  # book.json › files, đọc khi gặp đoạn nghe đầu tiên
    spoken = sum(1 for sc in lesson.scenes for ln in sc.lines if ln.speaker)
    done = 0
    for si, sc in enumerate(lesson.scenes):
        focus, revealed, mark = None, set(), ()
        if si and rate:
            add(silence(lesson.scene_gap), None)
        if sc.chapter:
            chapters.append((pos / rate if rate else 0.0, sc.chapter))
        for ln in sc.lines:
            if ln.focus is not None:
                if ln.focus != focus:
                    mark = ()
                focus = ln.focus
            if ln.mark:
                mark = tuple(ln.mark)
            revealed |= set(ln.reveal)
            # cảnh jp: chữ nào trên thẻ sáng lên, câu đọc từng chữ một thành mấy phần (script.reading_plan)
            seq, pieces = reading_plan(lesson, sc, ln, focus or 0) if sc.kind == "jp" else ([], [])
            step = step_of(lesson, ln)
            if ln.track:
                start_audio(getattr(engine, "RATE", 16000))
                if book_dir is None:
                    raise TTSError(f"cần thư mục sách để phát {ln.track}")
                if files is None:
                    files = json.loads((Path(book_dir) / "book.json").read_text(encoding="utf-8")).get("files", {})
                if ln.track not in files:
                    raise TTSError(f"không có file nghe {ln.track} trong book.json")
                path = Path(book_dir) / files[ln.track]["path"]
                data = _norm(_decode(path, rate, ln.start, ln.end))
                kw = dict(note=ln.note, mark=mark, audio=ln.track, en=ln.en)
                spans = track_spans(path, ln.start, ln.end) if step and len(seq) > 1 else []
                if len(spans) == len(seq) > 1:  # mỗi đoạn có tiếng là một chữ: chữ đó sáng lên, nghỉ giãn ra ≥ step
                    cuts = [0] + [int(round(max(spans[k - 1][1], spans[k][0] - LEADIN) * rate))
                                  for k in range(1, len(spans))] + [len(data)]
                    for k, tok in enumerate(seq):
                        last = k == len(seq) - 1
                        pad = lesson.gap + ln.pause if last else max(0.0, step - (spans[k + 1][0] - spans[k][1]))
                        add(np.concatenate([data[cuts[k]:cuts[k + 1]], silence(pad)]),
                            Frame(si, focus, frozenset(revealed), None, "", ln.vi, hl=(tok,), done=tuple(seq[:k]), **kw))
                else:
                    add(np.concatenate([data, silence(lesson.gap + ln.pause)]),
                        Frame(si, focus, frozenset(revealed), None, "", ln.vi, hl=tuple(seq), **kw))
            elif ln.speaker:
                voice, speed = voices[ln.speaker], ln.speed or lesson.speakers[ln.speaker].speed
                if pieces and len(pieces) != len(seq):  # `check` đã báo; dựng thì đọc liền cả câu
                    pieces = []
                texts = [ja.as_said(p) for p in pieces] or [ln.spoken]
                said = 0  # số mẫu từ đầu câu tới hết phần cuối (kể cả chỗ nghỉ giữa các phần)
                for k, text in enumerate(texts):
                    data, r = synth(text, voice, speed)
                    start_audio(r)
                    data = _norm(_resample(data, r, rate))
                    last = k == len(texts) - 1
                    hl, dn = ((seq[k],), tuple(seq[:k])) if pieces else (tuple(seq), ())
                    add(np.concatenate([data, silence(lesson.gap + ln.pause if last else step)]),
                        Frame(si, focus, frozenset(revealed), ln.speaker, ln.text, ln.vi, mark=mark, en=ln.en, hl=hl,
                              done=dn))
                    said += len(data) + (0 if last else len(silence(step)))
                if ln.echo:  # chừa chỗ cho người học nhắc lại câu vừa nghe
                    name = lesson.speakers[ln.speaker].name
                    countdown(si, focus, revealed, mark, echo_seconds(said / rate),
                              ln.note or f"Your turn — repeat after {name}", f"Nhắc lại theo {name}: cùng tốc độ, cùng ngữ điệu",
                              hl=tuple(seq))
                done += 1
                if done % 10 == 0 or done == spoken:
                    say(f"  đọc {done}/{spoken} câu")
            else:
                start_audio(getattr(engine, "RATE", 16000))
                countdown(si, focus, revealed, mark, ln.wait, ln.note, ln.vi, en=ln.en, hl=tuple(seq))
                if ln.pause:
                    add(silence(ln.pause), None)
    if rate is None:
        raise ValueError("kịch bản không có câu thoại nào")
    add(silence(TAIL), None)
    if frames:  # khung đầu bắt đầu từ 0 (gồm cả khoảng lặng mở đầu)
        frames[0].dur += frames[0].start
        frames[0].start = 0.0
    audio = np.concatenate(parts)
    chapters = [(0.0 if i == 0 else t, name) for i, (t, name) in enumerate(chapters)]
    return Timeline(frames, audio, rate, chapters)
