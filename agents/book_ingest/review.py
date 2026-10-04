"""Bước 4 — hộp duyệt: gộp mục chưa chắc, giữ quyết định cũ, hỏi người duyệt.

Định dạng review.json dùng chung cho mọi agent sau này (docs/agent-hoc-tap/02 mục 3.6).
Quyết định: {"accept": true} · {"value": {...}} · {"skip": true}.
Mục `info` chỉ để biết, không chặn đóng gói; mục `warn`/`error` phải có quyết định.
"""
from __future__ import annotations

import json
from pathlib import Path
from typing import Callable, Optional

from .schemas import Review, ReviewItem, dump


def load(path: Path) -> Review:
    if Path(path).exists():
        return Review.model_validate_json(Path(path).read_text(encoding="utf-8"))
    return Review()


def save(path: Path, review: Review) -> None:
    Path(path).parent.mkdir(parents=True, exist_ok=True)
    Path(path).write_text(json.dumps(dump(review), ensure_ascii=False, indent=1), encoding="utf-8")


def merge(old: Review, fresh: list[dict]) -> Review:
    decided = {i.id: i.decision for i in old.items if i.decision is not None}
    items = []
    for raw in fresh:
        item = ReviewItem.model_validate(raw)
        if item.id in decided:
            item.decision = decided[item.id]
        items.append(item)
    items.sort(key=lambda i: ({"error": 0, "warn": 1, "info": 2}[i.severity], i.id))
    return Review(items=items)


def decisions(review: Review) -> dict:
    return {i.id: i.decision for i in review.items if i.decision is not None}


def open_items(review: Review) -> list[ReviewItem]:
    return [i for i in review.items if i.severity != "info" and i.decision is None]


def accept_all(review: Review) -> int:
    n = 0
    for i in open_items(review):
        if i.proposal is not None:
            i.decision = {"accept": True}
            n += 1
    return n


def interactive(review: Review, ask: Callable[[str], str] = input, say: Callable[[str], None] = print) -> int:
    """Duyệt từng mục trên terminal. Trả về số mục đã quyết."""
    n = 0
    for item in open_items(review):
        say(f"\n[{item.severity}] {item.id}\n  {item.message}")
        if item.proposal is not None:
            say(f"  Đề xuất: {json.dumps(item.proposal, ensure_ascii=False)}")
        for k, opt in enumerate(item.options, 1):
            say(f"  {k}) {json.dumps(opt, ensure_ascii=False)}")
        ans = ask("  [a] đồng ý · [số] chọn phương án · [j] nhập JSON · [s] bỏ qua · [Enter] để sau: ").strip().lower()
        decision: Optional[dict] = None
        if ans == "a" and item.proposal is not None:
            decision = {"accept": True}
        elif ans.isdigit() and 1 <= int(ans) <= len(item.options):
            decision = {"value": item.options[int(ans) - 1]}
        elif ans == "j":
            decision = {"value": json.loads(ask("  JSON: "))}
        elif ans == "s":
            decision = {"skip": True}
        if decision:
            item.decision = decision
            n += 1
    return n
