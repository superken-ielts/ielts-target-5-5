"""Chép lời audio của sách để viết kịch bản video khi bản PDF không có lời bài nghe (Scripts / Tapescript).

    python -m lesson_video transcribe ../books/<sách> 1.7 1.20     # mọi track từ 1.7 tới 1.20 theo thứ tự trong book.json
    python -m lesson_video transcribe ../books/<sách> 1.3          # một track

Mỗi track: tìm khoảng lặng bằng ffmpeg `silencedetect`, gộp phần có tiếng thành đoạn ≤ 18 giây, đọc từng đoạn bằng
Parakeet TDT 0.6B v2 (tiếng Anh, có dấu câu) qua sherpa-onnx. Kết quả ở books/<sách>/work/transcripts/:
`<track>.json` (đoạn: start, end, text, words = [[giây, từ], …] tính từ đầu file) và `<track>.txt` để đọc nhanh.
Mốc từng từ dùng cho `start` / `end` của dòng `track` trong kịch bản (cắt đúng một câu của audio gốc).

Cần `pip install sherpa-onnx` và model `sherpa-onnx-nemo-parakeet-tdt-0.6b-v2-int8` (tải từ GitHub releases của
k2-fsa/sherpa-onnx, mục asr-models; Hugging Face bị chặn thì vẫn tải được), giải nén vào ~/.cache/lesson_video/asr/
hoặc chỉ đường bằng `--model` / biến LESSON_ASR_MODEL. Lời chép là bản nháp: tên riêng hay sai (Sameh → Sami),
nên đối chiếu với trang sách và Teacher's Book trước khi đưa lên màn hình.
"""
from __future__ import annotations

import json
import os
import re
import subprocess
from pathlib import Path
from typing import Optional

from .tts import HOME

MODEL_NAME = "sherpa-onnx-nemo-parakeet-tdt-0.6b-v2-int8"
RATE = 16000


class ASRError(RuntimeError):
    pass


def speech_spans(silences: list[tuple[float, float]], duration: float, min_len: float = 0.15) -> list[list[float]]:
    """Phần có tiếng = phần nằm giữa các khoảng lặng (bỏ mẩu ngắn hơn `min_len`)."""
    out, t = [], 0.0
    for s, e in silences:
        if s - t > min_len:
            out.append([round(t, 2), round(s, 2)])
        t = max(t, e)
    if duration - t > min_len:
        out.append([round(t, 2), round(duration, 2)])
    return out


def group(spans: list[list[float]], max_len: float = 18.0, join_gap: float = 1.2) -> list[list[float]]:
    """Gộp các phần có tiếng kề nhau (nghỉ < `join_gap` giây) thành đoạn dài tối đa `max_len` giây."""
    out: list[list[float]] = []
    for s, e in spans:
        if out and e - out[-1][0] <= max_len and s - out[-1][1] < join_gap:
            out[-1][1] = e
        else:
            out.append([s, e])
    return out


def words(tokens: list[str], times: list[float], offset: float) -> list[list]:
    """Ghép mảnh từ (token BPE, `▁` = đầu từ) thành từ kèm giây bắt đầu, tính từ đầu file."""
    out: list[list] = []
    for tok, t in zip(tokens, times):
        piece = tok.replace("▁", " ")
        if not out or piece.startswith(" "):
            if piece.strip():
                out.append([round(offset + t, 2), piece.strip()])
        else:
            out[-1][1] += piece
    return out


def silences(path: Path, noise: str = "-38dB", dur: float = 0.45) -> list[tuple[float, float]]:
    log = subprocess.run(["ffmpeg", "-i", str(path), "-af", f"silencedetect=noise={noise}:d={dur}", "-f", "null", "-"],
                         capture_output=True, text=True).stderr
    starts = [float(x) for x in re.findall(r"silence_start: ([\d.]+)", log)]
    ends = [float(x) for x in re.findall(r"silence_end: ([\d.]+)", log)]
    return list(zip(starts, ends))


def model_dir(model: Optional[str] = None) -> Path:
    d = Path(model or os.environ.get("LESSON_ASR_MODEL") or HOME / "asr" / MODEL_NAME).expanduser()
    if not (d / "tokens.txt").exists():
        raise ASRError(f"không thấy model chép lời ở {d} — tải {MODEL_NAME}.tar.bz2 (GitHub k2-fsa/sherpa-onnx, "
                       "releases › asr-models) rồi giải nén vào ~/.cache/lesson_video/asr/")
    return d


def recognizer(model: Optional[str] = None, threads: int = 4):
    try:
        import sherpa_onnx
    except ImportError as e:
        raise ASRError("chưa cài sherpa-onnx: pip install sherpa-onnx") from e
    d = model_dir(model)
    return sherpa_onnx.OfflineRecognizer.from_transducer(
        encoder=str(d / "encoder.int8.onnx"), decoder=str(d / "decoder.int8.onnx"), joiner=str(d / "joiner.int8.onnx"),
        tokens=str(d / "tokens.txt"), num_threads=threads, model_type="nemo_transducer")


def transcribe_file(rec, path: Path) -> dict:
    import numpy as np

    raw = subprocess.run(["ffmpeg", "-v", "error", "-i", str(path), "-ac", "1", "-ar", str(RATE), "-f", "f32le", "-"],
                         capture_output=True, check=True).stdout
    x = np.frombuffer(raw, dtype=np.float32)
    dur = len(x) / RATE
    segs = []
    for s, e in group(speech_spans(silences(path), dur)):
        a = max(0.0, s - 0.1)
        st = rec.create_stream()
        st.accept_waveform(RATE, x[int(a * RATE):int(min(dur, e + 0.15) * RATE)])
        rec.decode_stream(st)
        r = st.result
        if r.text.strip():
            segs.append({"start": s, "end": e, "text": r.text.strip(), "words": words(list(r.tokens), list(r.timestamps), a)})
    return {"duration": round(dur, 2), "segments": segs}


def track_ids(book: dict, first: str, last: Optional[str] = None) -> list[str]:
    order = [k for k, f in book["files"].items() if f.get("kind") == "audio"]
    for t in (first, last or first):
        if t not in order:
            raise ASRError(f"không có track `{t}` trong book.json")
    i, j = order.index(first), order.index(last or first)
    if j < i:
        raise ASRError(f"khoảng track {first}..{last} phải đi xuôi")
    return order[i:j + 1]


def run(bdir: Path, first: str, last: Optional[str] = None, model: Optional[str] = None, say=print) -> list[Path]:
    bdir = Path(bdir)
    book = json.loads((bdir / "book.json").read_text(encoding="utf-8"))
    ids = track_ids(book, first, last)
    rec = recognizer(model)
    out_dir = bdir / "work" / "transcripts"
    out_dir.mkdir(parents=True, exist_ok=True)
    written = []
    for t in ids:
        data = {"track": t, "file": book["files"][t]["path"], **transcribe_file(rec, bdir / book["files"][t]["path"])}
        (out_dir / f"{t}.json").write_text(json.dumps(data, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
        (out_dir / f"{t}.txt").write_text(to_text(data), encoding="utf-8")
        written.append(out_dir / f"{t}.json")
        say(f"{t} ({data['duration']:.0f}s): {len(data['segments'])} đoạn")
    return written


def to_text(data: dict) -> str:
    rows = [f"# {data['track']} · {data['file']} · {data['duration']:.1f}s (chép tự động, soát với sách trước khi dùng)"]
    rows += [f"[{s['start']:7.2f}–{s['end']:7.2f}] {s['text']}" for s in data["segments"]]
    return "\n".join(rows) + "\n"
