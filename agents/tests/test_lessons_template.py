"""Mẫu lessons-v1: lộ trình khai hết trong book.yaml, không có file sách (GENKI I · lộ trình N5)."""
import json
import shutil
from pathlib import Path

import pytest

from book_ingest import lessons, pipeline, validate as vd
from book_ingest.profile import ProfileError

GENKI = Path(__file__).resolve().parents[2] / "books" / "genki_1_n5"

PROFILE = """\
book: mini-course
title: Mini Course
template: lessons-v1
start_week: 3
sessions_per_week: 2
minutes_per_session: 50
pace: [2, 3]
info: {course: ja-n5, level: JLPT N5, role: Giáo trình chính}
missing: [textbook]
steps:
  - {id: a, title: Part A, skill: grammar, core: true, note: "Bài {no}: {grammar} — {topic}"}
  - {id: b, title: Part B, skill: speaking, note: "Đọc – viết: {kana}"}
toc:
  sections:
    - id: S1
      title: Phần 1
      items:
        - unit: 0
          title: Chuẩn bị
          steps: [{id: kana, title: Hiragana, skill: reading, minutes: 30}]
        - {unit: 1, title: New Friends, topic: giới thiệu, kana: hiragana, grammar: [X は Y です, か]}
    - id: S2
      title: Phần 2
      items:
        - {unit: 2, title: Shopping, topic: mua sắm, kana: katakana, grammar: [これ], notes: {b: Riêng unit 2}}
        - test: 1
          title: Ôn thi
          steps: [{id: mock, title: Thi thử, core: true, minutes: 120}]
"""


def make(tmp_path: Path, text: str = PROFILE) -> Path:
    d = tmp_path / "course"
    d.mkdir()
    (d / "book.yaml").write_text(text, encoding="utf-8")
    return d


def test_builds_book_and_plan_without_files(tmp_path):
    d = make(tmp_path)
    res = pipeline.run(d, say=lambda m: None)
    assert res.code == pipeline.OK, res.messages
    assert vd.validate(d) == []
    book = json.loads((d / "book.json").read_text())
    plan = json.loads((d / "plan.json").read_text())
    assert book["template"] == "lessons-v1" and book["files"] == {}
    assert book["info"]["course"] == "ja-n5" and book["info"]["level"] == "JLPT N5"
    items = [i for s in book["sections"] for i in s["items"]]
    assert [i["id"] for i in items] == ["U00", "U01", "U02", "T1"]
    acts = {a["id"]: a for i in items for a in i["activities"]}
    assert list(acts) == ["U00-kana", "U01-a", "U01-b", "U02-a", "U02-b", "T1-mock"]
    assert acts["U01-a"]["note"] == "Bài 1: X は Y です; か — giới thiệu"     # chỗ thay {no}, {grammar}, {topic}
    assert acts["U02-b"]["note"] == "Riêng unit 2"                             # `notes` của mục ghi đè
    assert acts["U01-a"]["title"] == "Unit 1 · Part A" and acts["T1-mock"]["title"] == "Ôn thi · Thi thử"
    assert (acts["U00-kana"]["estMinutes"], acts["U01-a"]["estMinutes"], acts["T1-mock"]["estMinutes"]) == (30, 50, 120)
    assert "pdf" not in acts["U01-a"] and acts["U01-b"]["skill"] == "speaking"
    # mỗi hoạt động một phiên, tuần tính từ start_week theo số phiên/tuần
    assert [s["activityIds"] for s in plan["sessions"]] == [[a] for a in acts]
    assert [s["week"] for s in plan["sessions"]] == [3, 3, 4, 4, 5, 5]
    assert [s["core"] for s in plan["sessions"]] == [False, True, False, True, False, True]
    assert plan["sessions"][-1]["kind"] == "test" and plan["minutesPerSession"] == 50
    assert plan["rules"] == {"coreSteps": ["a", "mock"], "paceOptions": [2, 3]}
    assert "6 phiên" in (d / "report.md").read_text() and not (d / "work").exists()


@pytest.mark.parametrize("old,new,msg", [
    ("steps:\n  - {id: a", "stepz:\n  - {id: a", "thiếu khóa `steps`"),
    ("skill: speaking, note", "skill: singing, note", "kỹ năng"),
    ("{id: b, title: Part B", "{id: a, title: Part B", "trùng id bước"),
    ("notes: {b: Riêng unit 2}", "notes: {c: Riêng unit 2}", "bước không tồn tại"),
    ("- {unit: 2, title: Shopping", "- {unit: 1, title: Shopping", "trùng mục U01"),
    ("note: \"Đọc – viết: {kana}\"", "note: \"Đọc – viết: {kanji}\"", "chỗ thay không hợp lệ"),
])
def test_bad_profiles_are_rejected(tmp_path, old, new, msg):
    assert PROFILE.count(old) == 1
    d = make(tmp_path, PROFILE.replace(old, new))
    with pytest.raises(ProfileError, match=msg):
        lessons.build(lessons.load(d))


def test_validate_catches_activity_without_session(tmp_path):
    d = make(tmp_path)
    pipeline.run(d, say=lambda m: None)
    plan = json.loads((d / "plan.json").read_text())
    plan["sessions"] = plan["sessions"][:-1]
    (d / "plan.json").write_text(json.dumps(plan), encoding="utf-8")
    assert any("T1-mock nằm trong 0 phiên" in p for p in vd.validate(d))


@pytest.mark.skipif(not (GENKI / "book.json").exists(), reason="chưa có lộ trình N5 trong repo")
def test_genki_package_is_reproducible(tmp_path):
    assert vd.validate(GENKI) == []
    s = vd.summary(GENKI)
    assert (s["units"], s["tests"], s["sessions"]) == (13, 1, 78)
    work = tmp_path / "genki"
    work.mkdir()
    shutil.copy(GENKI / "book.yaml", work / "book.yaml")
    assert pipeline.run(work, say=lambda m: None).code == pipeline.OK
    for name in ("book.json", "plan.json", "report.md"):
        assert (work / name).read_text() == (GENKI / name).read_text(), name
