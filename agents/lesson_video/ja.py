"""Tiếng Nhật trong kịch bản: furigana, cách đọc, romaji và đối chiếu với bộ tách âm của Kokoro.

Chữ hiển thị viết furigana ngay trong câu: `わたしは {留学生|りゅうがくせい}です。` — video vẽ `りゅうがくせい`
nhỏ phía trên `留学生`. Cách đọc mong đợi của một câu lấy từ furigana; giọng Nhật của Kokoro tách âm bằng
misaki (fugashi + unidic-lite), và misaki hay đọc sai số đếm, tên nước (九時 → きゅうじ, 日本語 → にっぽんご,
ベトナム人 → ベトナムにん). Vì vậy trước khi dựng, `check` so cách misaki đọc câu thoại với furigana; lệch thì
viết câu thoại hoặc `say` bằng kana ở chỗ bị đọc sai.

Phần misaki chỉ nạp khi cần (`pip install "misaki[ja]"`); phần furigana, kana, romaji chạy không cần gì thêm.
"""
from __future__ import annotations

import re
from functools import lru_cache
from typing import Optional

RUBY = re.compile(r"\{([^{}|]*)\|([^{}|]*)\}")
SMALL = set("ァィゥェォャュョヮ")
PARTICLES = {"は": "ワ", "へ": "エ", "を": "ヲ"}  # trợ từ đọc khác chữ viết


class JaError(RuntimeError):
    pass


# ---------- ký tự ----------
def is_kanji(ch: str) -> bool:
    o = ord(ch)
    return 0x4E00 <= o <= 0x9FFF or 0x3400 <= o <= 0x4DBF or 0xF900 <= o <= 0xFAFF or ch == "々"


def is_kana(ch: str) -> bool:
    return 0x3041 <= ord(ch) <= 0x309F or 0x30A0 <= ord(ch) <= 0x30FF


def is_cjk(ch: str) -> bool:
    """Ký tự cần phông Nhật: kana, chữ Hán, dấu câu và chữ toàn khổ của Nhật."""
    o = ord(ch)
    return is_kana(ch) or is_kanji(ch) or 0x3000 <= o <= 0x303F or 0xFF00 <= o <= 0xFFEF or 0x31F0 <= o <= 0x31FF


def kata(s: str) -> str:
    """Hiragana → katakana; ký tự khác giữ nguyên."""
    return "".join(chr(ord(c) + 0x60) if 0x3041 <= ord(c) <= 0x3096 else c for c in s)


def kana_only(s: str) -> str:
    """Chỉ giữ kana (đổi sang katakana): bỏ dấu câu, khoảng trắng, chữ Latin để so cách đọc."""
    return "".join(c for c in kata(s) if 0x30A1 <= ord(c) <= 0x30FC)


# ---------- furigana ----------
def check_markup(text: str) -> list[str]:
    """Lỗi cú pháp furigana và chữ Hán chưa có furigana trong một chuỗi hiển thị."""
    problems = []
    for m in RUBY.finditer(text):
        base, reading = m.group(1), m.group(2)
        if not base.strip() or not reading.strip():
            problems.append(f"furigana trống: {m.group(0)}")
        elif any(is_kanji(c) or c.isascii() and c.isalpha() for c in reading):
            problems.append(f"furigana phải viết bằng kana: {m.group(0)}")
    rest = RUBY.sub("", text)
    if "{" in rest or "}" in rest or "|" in rest:
        problems.append(f"furigana viết sai — dạng đúng là {{漢字|かんじ}}: {text}")
    bare = sorted({c for c in rest if is_kanji(c)}, key=rest.index)
    if bare:
        problems.append("chữ Hán chưa có furigana: " + " ".join(bare) + " — viết dạng {漢字|かんじ}")
    return problems


def segments(text: str) -> list[tuple[str, Optional[str]]]:
    """[(chữ, furigana hoặc None)] theo thứ tự trong câu."""
    out, pos = [], 0
    for m in RUBY.finditer(text):
        if m.start() > pos:
            out.append((text[pos:m.start()], None))
        out.append((m.group(1), m.group(2)))
        pos = m.end()
    if pos < len(text):
        out.append((text[pos:], None))
    return out


def plain(text: str) -> str:
    """Chữ hiển thị bỏ furigana: `{留学生|りゅうがくせい}です` → `留学生です`."""
    return RUBY.sub(r"\1", text)


def reading(text: str) -> str:
    """Cách đọc theo furigana: `{留学生|りゅうがくせい}です` → `りゅうがくせいです`."""
    return RUBY.sub(r"\2", text)


# ---------- romaji (kiểu gõ phím: おう → ou, ー lặp nguyên âm, ん → n) ----------
_KANA = dict(zip(
    "アイウエオカキクケコガギグゲゴサシスセソザジズゼゾタチツテトダヂヅデドナニヌネノハヒフヘホバビブベボ"
    "パピプペポマミムメモヤユヨラリルレロワヰヱヲンヴァィゥェォャュョヮ",
    "a i u e o ka ki ku ke ko ga gi gu ge go sa shi su se so za ji zu ze zo ta chi tsu te to da ji zu de do "
    "na ni nu ne no ha hi fu he ho ba bi bu be bo pa pi pu pe po ma mi mu me mo ya yu yo ra ri ru re ro "
    "wa i e o n vu a i u e o ya yu yo wa".split()))


def kana_romaji(k: str) -> str:
    """Katakana/hiragana → romaji. Hai chữ ghép (キャ, ティ, ウェ…) ghép theo phụ âm của chữ trước."""
    k = kata(k)
    out: list[str] = []
    gem = False
    for i, ch in enumerate(k):
        if ch == " ":  # ranh giới từ: giữ để dễ đọc, không cắt âm ngắt ッ của từ trước
            out.append(" ")
            continue
        if ch == "ッ":
            gem = True
            continue
        if ch == "ー":
            prev = next((r for r in reversed(out) if r.strip()), "")
            if prev:
                out.append(prev[-1])
            continue
        r = _KANA.get(ch)
        if r is None:
            out.append("")
            continue
        if ch in SMALL and out and out[-1].strip() and i and k[i - 1] not in SMALL and k[i - 1] not in "ッ ":
            prev = out.pop()
            stem = "w" if prev == "u" else prev[:-1]
            if r in ("ya", "yu", "yo") and not stem.endswith(("sh", "ch", "j")):
                stem += "y"
                r = r[1:]
            elif r.startswith("y"):
                r = r[1:]
            r = stem + r
        if gem:
            r = ("t" if r.startswith("ch") else r[0]) + r
            gem = False
        out.append(r)
    return "".join(out)


def norm_romaji(s: str) -> str:
    """So romaji không phân biệt hoa thường, dấu cách, gạch nối; tch = cch, m trước b/p/m = n."""
    s = re.sub(r"[^a-z]", "", s.lower().replace("ā", "aa").replace("ī", "ii").replace("ū", "uu")
               .replace("ē", "ee").replace("ō", "ou"))
    return re.sub(r"m(?=[bpm])", "n", s.replace("tch", "cch"))


# ---------- misaki (bộ tách âm của Kokoro) ----------
@lru_cache(maxsize=1)
def _g2p():
    try:
        from misaki import ja
    except ImportError:
        raise JaError('Chưa cài bộ tách âm tiếng Nhật: pip install "misaki[ja]" (xem agents/README.md)') from None
    return ja.JAG2P()


def available() -> bool:
    try:
        _g2p()
        return True
    except JaError:
        return False


def phonemes(text: str) -> str:
    """Chuỗi âm vị misaki cho Kokoro (giọng jf_*, jm_*)."""
    return _g2p()(text)


def tokens(text: str) -> list[tuple[str, str, str]]:
    """[(chữ, cách đọc katakana, từ loại)] theo cách misaki tách câu (cùng bước chuẩn hóa với lúc đọc)."""
    g = _g2p()
    out = []
    for w in g.tagger(g._normalize_text(text)):
        kana = getattr(w.feature, "kana", None) or getattr(w.feature, "pron", None) or w.surface
        out.append((w.surface, kata(kana), getattr(w.feature, "pos1", "") or ""))
    return out


def spoken_reading(text: str) -> str:
    return "".join(k for _, k, _ in tokens(text))


def spoken_romaji(text: str) -> str:
    """Romaji của câu thoại theo cách misaki đọc; trợ từ は, へ, を viết wa, e, o. Ghép cả câu rồi mới đổi,
    vì っ có thể bị tách sang từ khác (はっさい → は / っ / さい)."""
    parts = [PARTICLES[s] if pos == "助詞" and s in PARTICLES else kana for s, kana, pos in tokens(text)]
    return " ".join(kana_romaji(" ".join(kana_only(x) for x in parts if kana_only(x))).split())


def diff(expected: str, got: str) -> str:
    """Chỉ chỗ lệch đầu tiên giữa hai chuỗi kana."""
    i = next((k for k, (a, b) in enumerate(zip(expected, got)) if a != b), min(len(expected), len(got)))
    lo = max(0, i - 4)
    return f"furigana …{expected[lo:i + 6]}… ≠ bộ đọc …{got[lo:i + 6]}…"


def check_line(display: str, spoken: str, romaji: str = "") -> list[str]:
    """Câu thoại tiếng Nhật `spoken` có được đọc đúng như furigana của `display` (và khớp `romaji`) không."""
    problems = []
    want = kana_only(reading(display))
    toks = tokens(spoken)
    got = kana_only("".join(k for _, k, _ in toks))
    if want != got:
        detail = " ".join(f"{s}({k})" for s, k, _ in toks if any(is_kanji(c) for c in s))
        problems.append(f"bộ đọc không đọc như furigana: {diff(want, got)}"
                        + (f" — misaki đọc chữ Hán: {detail}" if detail else "")
                        + " → viết chỗ đó bằng kana trong `say`")
    if romaji:
        a, b = norm_romaji(romaji), norm_romaji(spoken_romaji(spoken))
        if a != b:
            problems.append(f"romaji không khớp cách đọc: '{romaji}' — cách đọc là '{spoken_romaji(spoken)}'")
    return problems
