"""Từ vựng của sách theo English Profile — cuối mỗi video Giai đoạn 0 hiện hết từ A2 của bài (đợt 32).

    python -m lesson_video wordlist ../books/<sách> --unit U05 [--level A2]

Nguồn là bảng từ đi kèm sách: file `*Wordlist.xls` có tiêu đề "Elementary Wordlist with English Profile" (từ, từ loại,
cấp độ A1–B2, định nghĩa, ví dụ, unit). Lần đầu lệnh đọc file .xls (cần `pip install xlrd`) và ghi ra
`work/wordlist.json`; từ đó trở đi chỉ đọc file JSON (test cũng dùng file này, không cần xlrd).

Lệnh in các từ của unit ở cấp độ đã chọn (mỗi từ một dòng, từ loại viết tắt như trên màn hình) và cho biết từ nào chưa
có trong cảnh `words` của các kịch bản `lessons/<unit>-*.yaml`. Một từ nhiều nghĩa (on, quiet, rent) gộp thành một ô.
"""
from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Callable, Optional

import yaml

CACHE = "work/wordlist.json"
POS_SHORT = {"noun": "n", "verb": "v", "adjective": "adj", "adverb": "adv", "preposition": "prep", "phrase": "phr",
             "conjunction": "conj", "exclamation": "excl", "determiner": "det", "pronoun": "pron",
             "abbreviation": "abbr", "phrasal verb": "phr v", "modal verb": "modal", "number": "num"}


class WordlistError(RuntimeError):
    pass


def unit_code(label: str) -> str:
    """"Unit 05", "unit 5" → "U05"; "Intro unit" → "U00"."""
    t = label.strip().lower()
    if t.startswith("intro"):
        return "U00"
    m = re.search(r"(\d+)", t)
    return f"U{int(m.group(1)):02d}" if m else label.strip()


def key(word: str) -> str:
    """So khớp từ: bỏ dấu câu cuối ("Oh no!", "Really?"), không phân biệt hoa thường, gộp khoảng trắng."""
    return re.sub(r"\s+", " ", word.strip().rstrip("!?.").strip()).lower()


def short_pos(pos: str) -> str:
    return ", ".join(POS_SHORT.get(p.strip().lower(), p.strip()) for p in pos.split(",") if p.strip())


def _from_xls(path: Path) -> list[dict]:
    try:
        import xlrd
    except ImportError as e:
        raise WordlistError("chưa cài xlrd (đọc file .xls): pip install xlrd") from e
    book = xlrd.open_workbook(str(path))
    sheet = book.sheet_by_name("Unit order") if "Unit order" in book.sheet_names() else book.sheet_by_index(0)
    head = [str(c.value).strip().lower() for c in sheet.row(2)]
    if "unit" not in head or "definition" not in head:
        raise WordlistError(f"{path.name}: không thấy cột Unit / Definition ở dòng 3")
    out = []
    for r in range(3, sheet.nrows):
        w, pos, lvl, defin, ex, unit = (str(c.value).strip() for c in sheet.row(r)[:6])
        if w:
            out.append({"unit": unit_code(unit), "w": w, "pos": pos, "level": lvl.rstrip("?"), "def": defin, "ex": ex})
    return out


def load(bdir: Path) -> list[dict]:
    """Mọi mục của bảng từ (theo thứ tự unit trong sách). Đọc `work/wordlist.json`; chưa có thì tạo từ file .xls."""
    cache = bdir / CACHE
    if cache.exists():
        return json.loads(cache.read_text(encoding="utf-8"))["entries"]
    found = [p for p in sorted(bdir.rglob("*Wordlist.xls"))]
    if not found:
        raise WordlistError(f"không thấy file *Wordlist.xls (English Profile) trong {bdir}")
    entries = _from_xls(found[0])
    cache.parent.mkdir(parents=True, exist_ok=True)
    cache.write_text(json.dumps({"source": found[0].relative_to(bdir).as_posix(), "entries": entries},
                                ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    return entries


def unit_words(entries: list[dict], unit: str, level: str = "A2") -> list[dict]:
    """Từ của unit ở cấp độ `level`, mỗi từ một mục (nghĩa khác nhau gộp lại: từ loại nối bằng dấu phẩy)."""
    out: dict[str, dict] = {}
    for e in entries:
        if e["unit"] != unit or e["level"] != level:
            continue
        k = key(e["w"])
        if k not in out:
            out[k] = {"w": e["w"], "pos": [], "def": e["def"], "ex": e["ex"]}
        p = short_pos(e["pos"])
        if p and p not in out[k]["pos"]:
            out[k]["pos"].append(p)
    return [dict(v, pos=", ".join(v["pos"])) for v in out.values()]


def shown(bdir: Path, unit: str) -> dict[str, list[str]]:
    """Từ đã có trong cảnh `words` của các kịch bản unit: khóa từ → các id video."""
    got: dict[str, list[str]] = {}
    for path in sorted((bdir / "lessons").glob(f"{unit}-*.yaml")):
        raw = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
        for sc in raw.get("scenes", []):
            if sc.get("kind") == "words":
                for it in sc.get("items", []):
                    got.setdefault(key(str(it.get("w", ""))), []).append(str(raw.get("id", path.stem)))
    return got


def missing(bdir: Path, unit: str, level: str = "A2") -> list[str]:
    """Từ cấp độ `level` của unit chưa hiện ở cảnh `words` nào của unit."""
    have = shown(bdir, unit)
    return [w["w"] for w in unit_words(load(bdir), unit, level) if key(w["w"]) not in have]


def run(bdir: Path, unit: str, level: str = "A2", say: Callable[[str], None] = print) -> int:
    words = unit_words(load(bdir), unit, level)
    have = shown(bdir, unit)
    say(f"{unit} · {level}: {len(words)} từ (bảng từ English Profile của sách)")
    for w in words:
        where = ", ".join(have.get(key(w["w"]), [])) or "chưa có trong cảnh words"
        say(f"  - {{w: {json.dumps(w['w'], ensure_ascii=False)}, pos: {json.dumps(w['pos'])}, vi: \"\"}}"
            f"   # {w['def'][:60]} | {where}")
    miss = [w["w"] for w in words if key(w["w"]) not in have]
    say(f"chưa hiện: {len(miss)}" + (" — " + ", ".join(miss) if miss else ""))
    return 0
