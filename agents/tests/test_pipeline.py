import json
from pathlib import Path

from book_ingest import pipeline, review as rv, validate as vd
from book_ingest.structure import EXERCISE, HEAD_TEST, HEAD_UNIT, module_of
from conftest import make_book


def quiet(_msg):
    pass


def run(book: Path):
    return pipeline.run(book, allow_ocr=False, say=quiet)


def test_first_run_stops_for_review(fake_book):
    res = run(fake_book)
    assert res.code == pipeline.NEEDS_REVIEW
    review = rv.load(fake_book / "work" / "review.json")
    open_ids = {i.id for i in rv.open_items(review)}
    assert open_ids == {"unit-range:U04", "track-unused:random.mp3"}
    assert not (fake_book / "book.json").exists()


def test_review_then_pack(fake_book):
    run(fake_book)
    path = fake_book / "work" / "review.json"
    review = rv.load(path)
    assert rv.accept_all(review) == 2
    rv.save(path, review)

    res = run(fake_book)
    assert res.code == pipeline.OK, res.messages
    assert vd.validate(fake_book) == []

    book = json.loads((fake_book / "book.json").read_text())
    plan = json.loads((fake_book / "plan.json").read_text())
    # 4 unit × 7 + 2 review × 2 + 2 test × 3
    assert len(plan["sessions"]) == 38
    assert plan["sessions"][0]["id"] == "S1-U01-1" and plan["sessions"][0]["week"] == 6
    assert [s["step"] for s in plan["sessions"][:7]] == [
        "speaking-vocab", "listening", "reading", "writing-learn", "writing-review", "consolidation", "workbook"]

    acts = {a["id"]: a for s in book["sections"] for i in s["items"] for a in i["activities"]}
    # trang PDF = trang in + 2; Unit 1 bắt đầu ở trang in 3
    assert acts["U01-speaking-vocab"]["pages"] == [5, 6]
    assert acts["U01-listening"]["pages"] == [7, 8]
    assert acts["U01-reading"]["pages"] == [9, 11]
    assert acts["U01-listening"]["tracks"] == ["U01-L1C"]
    # băng thừa của Unit 4 được gộp vào exam-practice
    assert acts["U04-exam-practice"]["pages"] == [55, 56]
    # tiêu đề sau "Academic section" bị bỏ qua: Unit 1 Reading dùng cả khoảng đáp án của unit
    assert acts["U01-listening"]["answer"]["pages"] == [63, 63]
    assert acts["U01-reading"]["answer"]["pages"] == [63, 63]
    # trang tapescript theo từng track nhờ OCR, kể cả bài "Pronunciation check"
    assert book["files"]["U01-L1C"]["script"]["pages"] == [65, 66]
    assert book["files"]["U04-L2pro"]["script"]["pages"] == [66, 66]
    assert "random.mp3" not in json.dumps(book)
    # phiên Test giữ chỗ, có ghi chú vì thiếu sách Test, và trỏ tới tapescript TEST 1
    t1 = acts["T1-test"]
    assert "Cambridge" in t1["note"] and t1["script"]["pages"] == [66, 66]
    # Work Book không có → phiên 7 là ôn unit
    assert acts["U01-unit-review"]["module"] == "unit-review"


def test_rerun_is_deterministic(fake_book):
    run(fake_book)
    path = fake_book / "work" / "review.json"
    review = rv.load(path)
    rv.accept_all(review)
    rv.save(path, review)
    run(fake_book)
    first = (fake_book / "book.json").read_bytes(), (fake_book / "plan.json").read_bytes()
    run(fake_book)
    assert ((fake_book / "book.json").read_bytes(), (fake_book / "plan.json").read_bytes()) == first


def test_wrong_offset_is_flagged(tmp_path):
    book = make_book(tmp_path / "b", offset=0)
    run(book)
    review = rv.load(book / "work" / "review.json")
    item = next(i for i in review.items if i.id == "page-offset:course-book")
    assert item.proposal == {"value": 2}


def test_heading_patterns():
    cases = {
        "Unit 12-Speaking 3": ("12", "speaking-vocab"),
        "Unit 13Listening3": ("13", "listening"),
        "Unit 15-Exampractice-Listening": ("15", "exam-practice"),
        "Unit 1, Listening 2A": ("1", "listening"),
        "Unit 2, Exam Practice, Writing B": ("2", "exam-practice"),
    }
    for text, (u, mod) in cases.items():
        m = HEAD_UNIT.match(text)
        assert m and m.group("u") == u and module_of(m.group("rest")) == mod, text
    assert HEAD_UNIT.match("Workbook Unit 5, Writing B").group("wb")
    for text, ok in (("CNowlisten", True), ("DListen again", True), ("C Now", True),
                     ("Listen again", False), ("I'm here", False), ("[Play track 5]", False)):
        assert bool(EXERCISE.match(text)) is ok, text
    assert HEAD_TEST.match("TEST3") and HEAD_TEST.match("TEST 1")
