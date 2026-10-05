"""Bộ đọc giọng nói. Mặc định Flite (CMU, miễn phí, chạy offline, có sẵn trên Ubuntu: gói libflite1).

Giọng Flite dùng được: slt (nữ, Mỹ), rms (nam, Mỹ), awb (nam, Scotland), kal16 (nam, Mỹ).
`silent` không đọc gì — chỉ sinh im lặng dài theo số chữ, để thử bố cục nhanh và để test.
"""
from __future__ import annotations

import ctypes
import ctypes.util
from ctypes import POINTER, Structure, c_char_p, c_float, c_int, c_short, c_void_p

import numpy as np


class TTSError(RuntimeError):
    pass


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

    def __init__(self, stretch: float = 1.1):
        lib = _load("flite")
        if lib is None or _load("flite_usenglish") is None or _load("flite_cmulex") is None:
            raise TTSError("Không thấy thư viện Flite. Ubuntu/Debian: sudo apt install libflite1; macOS: brew install flite")
        lib.flite_init()
        lib.flite_text_to_wave.restype = POINTER(_Wave)
        lib.flite_text_to_wave.argtypes = [c_char_p, c_void_p]
        lib.flite_feat_set_float.argtypes = [c_void_p, c_char_p, c_float]
        lib.delete_wave.argtypes = [POINTER(_Wave)]
        self.lib, self.stretch, self._voices = lib, stretch, {}

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


class Silent:
    name = "silent"
    RATE = 16000

    def describe(self, voice: str) -> str:
        return "silent"

    def synth(self, text: str, voice: str) -> tuple[np.ndarray, int]:
        sec = 0.4 + 0.06 * len(text)
        return np.zeros(int(sec * self.RATE), dtype=np.int16), self.RATE


def get(name: str, stretch: float = 1.1):
    if name == "flite":
        return Flite(stretch=stretch)
    if name == "silent":
        return Silent()
    raise TTSError(f"bộ đọc không hỗ trợ: {name} (flite, silent)")
