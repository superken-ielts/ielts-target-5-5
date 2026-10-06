"""Bảng độ phủ video: mỗi phần (hoạt động) của từng unit đã có video bài giảng nào, phần nào chưa.

    python -m lesson_video coverage ../books/<sách> [--unit U01 --unit U02]

Đọc book.json (danh sách phần theo thứ tự sách), lessons/lessons.json (video đã dựng) và lessons/*.yaml
(kịch bản, kể cả kịch bản chưa dựng). In bảng Markdown để dán vào tài liệu theo dõi.
"""
from __future__ import annotations

import json
from pathlib import Path
from typing import Optional

import yaml

from .video import MANIFEST


def _clock(sec: float) -> str:
    m, s = divmod(int(round(sec)), 60)
    return f"{m // 60}:{m % 60:02d}:{s:02d}" if m >= 60 else f"{m}:{s:02d}"


def _pages(a: dict) -> str:
    p = a.get("printedPages")
    if not p:
        return "—"
    where = "Listening" if a.get("pdf") == "listening" else "sách"
    return f"{where} tr. {p[0]}" if p[0] == p[1] else f"{where} tr. {p[0]}–{p[1]}"


def coverage(bdir: Path, units: Optional[list[str]] = None) -> list[dict]:
    """Một mục cho mỗi unit: các phần theo thứ tự sách, mỗi phần kèm video đã dựng và kịch bản chưa dựng."""
    book = json.loads((bdir / "book.json").read_text(encoding="utf-8"))
    path = bdir / "lessons" / MANIFEST
    lessons = json.loads(path.read_text(encoding="utf-8"))["lessons"] if path.exists() else []
    built = {x["id"] for x in lessons}
    drafts: dict[str, list[str]] = {}
    for y in sorted((bdir / "lessons").glob("*.yaml")):
        raw = yaml.safe_load(y.read_text(encoding="utf-8")) or {}
        if raw.get("id") not in built:
            drafts.setdefault(str(raw.get("activity")), []).append(str(raw.get("id") or y.stem))
    out = []
    for sec in book["sections"]:
        for item in sec["items"]:
            if units and item["id"] not in units:
                continue
            parts = []
            for a in item["activities"]:
                vids = sorted((x for x in lessons if x["activity"] == a["id"]), key=lambda x: x["id"])
                parts.append({"activity": a["id"], "title": a.get("title", a["id"]), "pages": _pages(a), "videos": vids,
                              "drafts": drafts.get(a["id"], [])})
            out.append({"item": item["id"], "title": " · ".join(x for x in (item["id"], item.get("title")) if x), "parts": parts})
    return out


def to_markdown(units: list[dict]) -> str:
    rows = []
    for u in units:
        done = sum(1 for p in u["parts"] if p["videos"])
        vids = [v for p in u["parts"] for v in p["videos"]]
        total = sum(v["duration"] for v in vids)
        rows.append(f"### {u['title']} — {done}/{len(u['parts'])} phần có video, {len(vids)} video, {_clock(total)}")
        rows.append("")
        rows.append("| Phần | Trang | Video | Dài | Chương |")
        rows.append("|---|---|---|---|---|")
        for p in u["parts"]:
            name = p["title"].split(" · ", 1)[-1]
            if not p["videos"]:
                note = "kịch bản chưa dựng: " + ", ".join(p["drafts"]) if p["drafts"] else "**chưa có video**"
                rows.append(f"| {name} | {p['pages']} | {note} | — | — |")
            for v in p["videos"]:
                rows.append(f"| {name} | {p['pages']} | `{v['id']}` — {v['label']} | {_clock(v['duration'])} | {len(v['chapters'])} |")
        rows.append("")
    return "\n".join(rows)
