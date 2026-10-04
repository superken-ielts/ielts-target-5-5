"""Bước 3 — ghép audio với bài học.

Tên file theo mẫu trong book.yaml (files.audio.pattern) cho biết unit, phần nghe và bài,
ví dụ Unit4_listening_3b.mp3 → Unit 4, Listening 3, bài B → ID track U04-L3B.
Tên không khớp mẫu thì thành mục duyệt; không đoán bừa.
"""
from __future__ import annotations

import re

from .profile import Profile
from .schemas import ReviewItem


def ex_order(ex: str) -> int:
    return ord(ex[0]) - 96 if len(ex) == 1 else 100


def track_id(unit: int, part: str, ex: str) -> str:
    return f"U{unit:02d}-L{part}{ex.upper() if len(ex) == 1 else ex.lower()}"


def match(profile: Profile, scan: dict, structure: dict) -> dict:
    items: list[ReviewItem] = []
    tracks: list[dict] = []
    known_units = {u.no for u in profile.all_units()}
    script_tracks = (structure.get("tapescript") or {}).get("tracks", {})
    ts_pages = (structure.get("tapescript") or {}).get("pages")

    for a in scan["audio"]:
        spec = profile.files[a["group"]]
        m = re.match(spec.get("pattern", r"$^"), a["name"])
        if not m or int(m.group("unit")) not in known_units:
            items.append(ReviewItem(
                id=f"track-unused:{a['name']}", kind="track-unused", severity="warn", subject=a["name"],
                message=f"Tên file {a['name']} không khớp mẫu {spec.get('pattern')} hoặc unit không có trong mục lục.",
                confidence=0.0, proposal={"skip": True}, evidence=[{"type": "audio", "file": a["path"]}],
            ))
            continue
        unit = int(m.group("unit"))
        part = m.group("part")
        ex = m.group("ex").lower()
        t = {
            "id": track_id(unit, part, ex),
            "unit": unit, "part": part, "ex": ex,
            "title": f"Listening {part}{ex.upper() if len(ex) == 1 else ' ' + ex}",
            "path": a["path"], "bytes": a["bytes"], "sha256": a["sha256"], "durationSec": a["durationSec"],
            "confidence": 1.0,
        }
        page = script_tracks.get(f"{unit}:{part}:{ex}")
        if page and ts_pages:
            t["script"] = [page, min(page + 1, ts_pages[1])]
        tracks.append(t)

    tracks.sort(key=lambda t: (t["unit"], t["part"], ex_order(t["ex"]), t["ex"]))
    ids = [t["id"] for t in tracks]
    for dup in sorted({i for i in ids if ids.count(i) > 1}):
        items.append(ReviewItem(
            id=f"duplicate-track:{dup}", kind="duplicate-file", severity="warn", subject=dup,
            message=f"Có nhiều file cùng là track {dup}.", proposal={"keep": "first"},
        ))
    for a, b in scan.get("duplicates", []):
        items.append(ReviewItem(
            id=f"duplicate-file:{b}", kind="duplicate-file", severity="warn", subject=b,
            message=f"{b} trùng nội dung với {a}.", proposal={"skip": True},
        ))

    by_unit: dict[str, list[str]] = {}
    for t in tracks:
        by_unit.setdefault(str(t["unit"]), []).append(t["id"])
    for u in sorted(known_units):
        if str(u) not in by_unit:
            items.append(ReviewItem(
                id=f"track-missing:U{u:02d}", kind="track-missing", severity="warn", subject=f"U{u:02d}",
                message=f"Unit {u} không có file audio nào cho phần Listening.", proposal={"accept": True},
            ))
    return {"tracks": tracks, "byUnit": by_unit, "review": [i.model_dump(exclude_none=True) for i in items]}
