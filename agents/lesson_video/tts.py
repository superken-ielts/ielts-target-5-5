"""Bộ đọc giọng nói, đều miễn phí và chạy offline.

- `kokoro` — Kokoro-82M (Apache-2.0) qua thư viện kokoro-onnx: giọng tự nhiên. Cần file model `.onnx`
  (bản nén q8 ~92 MB là đủ) và file giọng `.bin` (~0,5 MB mỗi giọng), tải từ Hugging Face
  onnx-community/Kokoro-82M-v1.0-ONNX (thư mục onnx/ và voices/). Giọng tiếng Anh: af_*, am_* (Mỹ), bf_*, bm_* (Anh).
- `flite` — CMU Flite qua ctypes (Ubuntu: gói libflite1): nhẹ, có sẵn, nhưng nghe máy. Giọng slt, rms, awb, kal16.
- `silent` — không đọc gì, chỉ sinh im lặng dài theo số chữ: thử bố cục nhanh và để test.
- `auto` — kokoro nếu tìm thấy model và giọng, không thì flite.
"""
from __future__ import annotations

import atexit
import ctypes
import ctypes.util
import os
import sys
import tempfile
from ctypes import POINTER, Structure, c_char_p, c_float, c_int, c_short, c_void_p
from pathlib import Path
from typing import Optional

import numpy as np

HOME = Path(os.environ.get("LESSON_VIDEO_HOME") or Path.home() / ".cache" / "lesson_video")
KOKORO_HOME = HOME / "kokoro"
KOKORO_HELP = ("Cần model Kokoro: tải onnx/model_quantized.onnx (~92 MB) và voices/<giọng>.bin từ Hugging Face "
               "onnx-community/Kokoro-82M-v1.0-ONNX, đặt vào " + str(KOKORO_HOME) + " (giọng trong thư mục voices/), "
               "hoặc chỉ đường bằng --model/--voices hay biến KOKORO_MODEL/KOKORO_VOICES; cài thư viện: pip install kokoro-onnx")


class TTSError(RuntimeError):
    pass


# ---------- Flite ----------
class _Wave(Structure):
    _fields_ = [("type", c_char_p), ("sample_rate", c_int), ("num_samples", c_int),
                ("num_channels", c_int), ("samples", POINTER(c_short))]


def _load(name: str):
    for cand in (ctypes.util.find_library(name), f"lib{name}.so.1", f"lib{name}.so", f"lib{name}.dylib"):
        if not cand:
            continue
        try:
            return ctypes.CDLL(cand, mode=ctypes.RTLD_GLOBAL)
        except OSError:
            continue
    return None


class Flite:
    name = "flite"
    VOICES = ("slt", "rms", "awb", "kal16")

    def __init__(self, speed: float = 0.9):
        lib = _load("flite")
        if lib is None or _load("flite_usenglish") is None or _load("flite_cmulex") is None:
            raise TTSError("Không thấy thư viện Flite. Ubuntu/Debian: sudo apt install libflite1; macOS: brew install flite")
        lib.flite_init()
        lib.flite_text_to_wave.restype = POINTER(_Wave)
        lib.flite_text_to_wave.argtypes = [c_char_p, c_void_p]
        lib.flite_feat_set_float.argtypes = [c_void_p, c_char_p, c_float]
        lib.delete_wave.argtypes = [POINTER(_Wave)]
        self.lib, self.stretch, self._voices = lib, 1.0 / speed, {}
        self.tag = f"flite:{self.stretch:.3f}"

    def _voice(self, voice: str):
        if voice not in self._voices:
            if voice not in self.VOICES:
                raise TTSError(f"Flite không có giọng '{voice}' (có: {', '.join(self.VOICES)})")
            vlib = _load(f"flite_cmu_us_{voice}")
            if vlib is None:
                raise TTSError(f"Thiếu thư viện giọng flite_cmu_us_{voice}")
            reg = getattr(vlib, f"register_cmu_us_{voice}")
            reg.restype, reg.argtypes = c_void_p, [c_char_p]
            v = reg(None)
            # cst_voice: {name, features, …} → con trỏ thứ hai là bảng đặc trưng của giọng
            feats = ctypes.cast(v, POINTER(c_void_p))[1]
            self.lib.flite_feat_set_float(feats, b"duration_stretch", self.stretch)
            self._voices[voice] = (vlib, v)
        return self._voices[voice][1]

    def check(self, voice: str) -> None:
        self._voice(voice)

    def describe(self, voice: str) -> str:
        return f"Flite cmu_us_{voice}"

    def synth(self, text: str, voice: str) -> tuple[np.ndarray, int]:
        w = self.lib.flite_text_to_wave(text.encode("utf-8"), self._voice(voice))
        if not w:
            raise TTSError(f"Flite không đọc được: {text!r}")
        wv = w.contents
        n = wv.num_samples * wv.num_channels
        data = np.ctypeslib.as_array(wv.samples, shape=(n,)).astype(np.int16).copy()
        rate, ch = wv.sample_rate, wv.num_channels
        self.lib.delete_wave(w)
        if ch > 1:
            data = data.reshape(-1, ch).mean(axis=1).astype(np.int16)
        return data, rate


# ---------- Kokoro ----------
def load_voices(path: Path) -> dict[str, np.ndarray]:
    """Thư mục *.bin (float32, 510 × 256 — dạng của kho Hugging Face và gói kokoro-js) hoặc file .npz/.bin gộp."""
    path = Path(path)
    if path.is_dir():
        out = {}
        for p in sorted(path.glob("*.bin")):
            arr = np.fromfile(p, dtype=np.float32)
            if arr.size == 0 or arr.size % 256:
                raise TTSError(f"File giọng hỏng: {p}")
            out[p.stem] = arr.reshape(-1, 1, 256)
        return out
    with np.load(path) as z:
        return {k: z[k] for k in z.files}


def kokoro_files(model: Optional[str] = None, voices: Optional[str] = None) -> tuple[Optional[Path], Optional[Path]]:
    m = model or os.environ.get("KOKORO_MODEL")
    v = voices or os.environ.get("KOKORO_VOICES")
    if not m and KOKORO_HOME.is_dir():
        found = sorted(KOKORO_HOME.glob("*.onnx"))
        m = found[0] if found else None
    if not v and KOKORO_HOME.is_dir():
        if (KOKORO_HOME / "voices").is_dir():
            v = KOKORO_HOME / "voices"
        else:
            found = sorted(KOKORO_HOME.glob("voices*.bin")) + sorted(KOKORO_HOME.glob("voices*.npz"))
            v = found[0] if found else None
    m, v = (Path(m) if m else None), (Path(v) if v else None)
    return (m if m and m.exists() else None), (v if v and v.exists() else None)


class Kokoro:
    name = "kokoro"

    def __init__(self, model: Path, voices: Path, speed: float = 0.9):
        if not 0.5 <= speed <= 2.0:
            raise TTSError(f"tốc độ Kokoro phải trong 0,5–2,0: {speed}")
        try:
            from kokoro_onnx import Kokoro as Engine
        except ImportError:
            raise TTSError("Chưa cài kokoro-onnx: pip install kokoro-onnx") from None
        self.voices = load_voices(voices)
        if not self.voices:
            raise TTSError(f"Không thấy file giọng nào trong {voices}")
        # kokoro-onnx đòi một file giọng .npz; giọng được truyền thẳng dạng mảng khi đọc nên chỉ cần file tạm
        fd, tmp = tempfile.mkstemp(suffix=".npz")
        os.close(fd)
        np.savez(tmp, **{k: v for k, v in list(self.voices.items())[:1]})
        atexit.register(lambda: Path(tmp).unlink(missing_ok=True))
        self.k = Engine(str(model), tmp)
        self.speed = speed
        self.tag = f"kokoro:{Path(model).name}:{Path(model).stat().st_size}:{speed}"

    def check(self, voice: str) -> None:
        if voice not in self.voices:
            raise TTSError(f"Kokoro không có giọng '{voice}' (có: {', '.join(sorted(self.voices))})")
        if voice[:1] not in ("a", "b"):
            raise TTSError(f"Giọng '{voice}' không phải tiếng Anh (cần af_*, am_*, bf_*, bm_*)")

    def describe(self, voice: str) -> str:
        return f"Kokoro {voice}"

    def synth(self, text: str, voice: str) -> tuple[np.ndarray, int]:
        self.check(voice)
        lang = "en-gb" if voice.startswith("b") else "en-us"
        audio, rate = self.k.create(text, self.voices[voice], speed=self.speed, lang=lang)
        return (np.clip(audio, -1, 1) * 32767).astype(np.int16), rate


# ---------- im lặng ----------
class Silent:
    name = "silent"
    tag = "silent"
    RATE = 16000

    def check(self, voice: str) -> None:
        pass

    def describe(self, voice: str) -> str:
        return "silent"

    def synth(self, text: str, voice: str) -> tuple[np.ndarray, int]:
        sec = 0.4 + 0.06 * len(text)
        return np.zeros(int(sec * self.RATE), dtype=np.int16), self.RATE


def get(name: str, speed: float = 0.9, model: Optional[str] = None, voices: Optional[str] = None):
    if name in ("auto", "kokoro"):
        m, v = kokoro_files(model, voices)
        if m and v:
            try:
                return Kokoro(m, v, speed=speed)
            except TTSError as e:
                if name == "kokoro":
                    raise
                print(f"Kokoro không dùng được ({e}) → đọc bằng Flite", file=sys.stderr)
        elif name == "kokoro":
            raise TTSError(KOKORO_HELP)
        return Flite(speed=speed)
    if name == "flite":
        return Flite(speed=speed)
    if name == "silent":
        return Silent()
    raise TTSError(f"bộ đọc không hỗ trợ: {name} (auto, kokoro, flite, silent)")
