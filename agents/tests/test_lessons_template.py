"""Mẫu lessons-v1: lộ trình khai hết trong book.yaml, có hoặc không có file sách (GENKI I · lộ trình N5)."""
import json
import shutil
import wave
from pathlib import Path

import pymupdf
import pytest

from book_ingest import lessons, pipeline, validate as vd
from book_ingest.profile import ProfileError

GENKI = Path(__file__).resolve().parents[2] / "books" / "Genki"

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


WITH_FILES = """\
book: mini-book
title: Mini Book
template: lessons-v1
sessions_per_week: 3
files:
  course-book: {kind: pdf, label: Textbook, path: text.pdf, page_offset: 2, web_chunks: true}
  workbook: {kind: pdf, path: work.pdf, web_chunks: true}
  audio: {kind: audio, dir: audio}
steps:
  - {id: a, title: Đọc}
  - {id: b, title: Nghe, skill: listening}
toc:
  sections:
    - id: S1
      title: Phần 1
      items:
        - unit: 1
          title: Một
          pages: [1, 6]
          refs:
            a: {pages: [1, 3], tracks: K01-01..K01-02}
            b: {pdf: workbook, pages: [1, 2], tracks: "K01-03, W01-A", alt: [{pages: [7, 8]}]}
        - unit: 2
          title: Hai
          refs:
            a: {pages: [4, 6]}
"""


def make_files(tmp_path: Path, text: str = WITH_FILES) -> Path:
    d = make(tmp_path, text)
    for name, n in (("text.pdf", 12), ("work.pdf", 4)):
        doc = pymupdf.open()
        for i in range(n):
            doc.new_page().insert_text((72, 72), f"{name} {i + 1}")
        doc.save(str(d / name))
    (d / "audio").mkdir()
    for k, name in enumerate(["K01_01", "K01_02", "K01_03", "W01_A"]):
        with wave.open(str(d / "audio" / f"{name}.wav"), "wb") as w:   # 2,5 giây, mỗi file một nội dung
            w.setnchannels(1)
            w.setsampwidth(2)
            w.setframerate(8000)
            w.writeframes(bytes([k + 1, 0]) * 20000)
    return d


def test_files_refs_tracks_and_chunks(tmp_path):
    d = make_files(tmp_path)
    res = pipeline.run(d, say=lambda m: None)
    assert res.code == pipeline.OK, res.messages
    book = json.loads((d / "book.json").read_text())
    acts = {a["id"]: a for s in book["sections"] for i in s["items"] for a in i["activities"]}
    # trang in → trang PDF theo page_offset của từng file; track theo nhãn (K01_01.wav → K01-01), khoảng A..B
    assert (acts["U01-a"]["pdf"], acts["U01-a"]["pages"], acts["U01-a"]["tracks"]) == ("course-book", [3, 5], ["K01-01", "K01-02"])
    assert (acts["U01-b"]["pdf"], acts["U01-b"]["pages"], acts["U01-b"]["tracks"]) == ("workbook", [1, 2], ["K01-03", "W01-A"])
    assert acts["U01-b"]["alt"] == [{"pdf": "course-book", "pages": [9, 10], "label": "Textbook tr. 7–8"}]
    assert "pdf" not in acts["U02-b"] and acts["U02-b"]["tracks"] == []
    assert [i.get("pages") for i in book["sections"][0]["items"]] == [[3, 8], None]
    audio = {k: (f["title"], f["unit"], f["durationSec"]) for k, f in book["files"].items() if f["kind"] == "audio"}
    assert audio == {"K01-01": ("K01-01", 1, 2.5), "K01-02": ("K01-02", 1, 2.5), "K01-03": ("K01-03", 1, 2.5),
                     "W01-A": ("W01-A", 1, 2.5)}
    # đoạn PDF: các khoảng của một mục chạm hoặc kề nhau thì gộp, mục khác thành đoạn riêng
    assert [[c["from"], c["to"]] for c in book["files"]["course-book"]["chunks"]] == [[3, 5], [6, 8], [9, 10]]
    assert [[c["from"], c["to"]] for c in book["files"]["workbook"]["chunks"]] == [[1, 2]]
    assert book["files"]["course-book"]["pageOffset"] == 2 and (d / "web" / "course-book-p0009-0010.pdf").exists()
    assert vd.validate(d, check_hashes=True) == []
    report = (d / "report.md").read_text()
    assert "| U01 Một | Nghe | workbook 1–2 · course-book 7–8 | 2: K01-03, W01-A |" in report
    # chạy lại: dùng lại scan và đoạn PDF, đầu ra giữ nguyên
    before = (d / "book.json").read_text()
    assert pipeline.run(d, say=lambda m: None).code == pipeline.OK and (d / "book.json").read_text() == before


@pytest.mark.parametrize("old,new,msg", [
    ("tracks: K01-01..K01-02}", "tracks: K01-01..K01-09}", "không có track `K01-09`"),
    ("tracks: K01-01..K01-02}", "tracks: K01-02..K01-01}", "phải đi xuôi"),
    ("tracks: K01-01..K01-02}", "tracks: K01-01..K01-03}", "K01-03 được gán hai lần"),
    ("tracks: K01-01..K01-02}", "tracks: K01-01}", "1 track chưa thuộc bước nào"),
    ("            a: {pages: [4, 6]}", "            c: {pages: [4, 6]}", "bước không tồn tại: c"),
    ("            a: {pages: [4, 6]}", "            a: {pdf: audio, pages: [4, 6]}", "không phải file PDF"),
    ("            a: {pages: [4, 6]}", "            a: {pages: [6, 4]}", "U02.refs.a.pages"),
    ("            a: {pages: [4, 6]}", "            a: {page: [4, 6]}", "chỉ nhận các khóa"),
])
def test_bad_refs_are_rejected(tmp_path, old, new, msg):
    assert WITH_FILES.count(old) == 1
    d = make_files(tmp_path, WITH_FILES.replace(old, new))
    with pytest.raises(ProfileError, match=msg):
        pipeline.run(d, say=lambda m: None)


def test_refs_need_files(tmp_path):
    d = make(tmp_path, PROFILE.replace("        - {unit: 1, title: New Friends,",
                                       "        - {unit: 1, refs: {a: {pages: [1, 2]}}, title: New Friends,"))
    with pytest.raises(ProfileError, match="chưa khai `files`"):
        lessons.load(d)


@pytest.mark.skipif(not (GENKI / "book.json").exists(), reason="chưa có lộ trình N5 trong repo")
def test_genki_package_is_valid_and_reproducible(tmp_path):
    assert vd.validate(GENKI) == []
    s = vd.summary(GENKI)
    assert (s["units"], s["tests"], s["sessions"], s["tracks"], s["weeks"]) == (13, 1, 78, 286, [1, 20])
    # chạy lại vào thư mục tạm: file sách được liên kết, không chép; chunks.json để dùng lại đoạn PDF có sẵn
    work = tmp_path / "genki"
    work.mkdir()
    for p in GENKI.iterdir():
        if p.name == "book.yaml":
            shutil.copy(p, work / p.name)
        elif p.name == "work":
            (work / "work").mkdir()
            shutil.copy(p / "chunks.json", work / "work" / "chunks.json")
        elif p.name not in ("book.json", "plan.json", "report.md", ".DS_Store"):
            (work / p.name).symlink_to(p)
    res = pipeline.run(work, say=lambda m: None)
    assert res.code == pipeline.OK, res.messages
    for name in ("book.json", "plan.json", "report.md"):
        assert (work / name).read_text() == (GENKI / name).read_text(), name
