import copy
import json
import shutil
from pathlib import Path

import pytest
import yaml
from pydantic import ValidationError

from lesson_video import cli, script as sc, timeline, tts, video
from lesson_video.slides import H, W, Slides

ROOT = Path(__file__).resolve().parents[2]
REAL = ROOT / "books" / "ielts_target_5_0"

LESSON = {
    "id": "T-1", "activity": "U01-speaking-vocab", "title": "Unit 1", "subtitle": "Speaking 1", "tag": "UNIT 1",
    "speakers": {"a": {"name": "Ann", "role": "teacher", "voice": "slt"},
                 "b": {"name": "Ben", "role": "student", "voice": "rms", "color": "#1F5FAD"}},
    "scenes": [
        {"kind": "title", "chapter": "Intro", "lines": [{"a": "Hello."}, {"b": "Hi!", "vi": "Chào!"}]},
        {"kind": "pairs", "chapter": "Match",
         "items": [{"n": 1, "q": "Where are you from?", "answer": "b"}, {"n": 2, "q": "How old are you?", "answer": "a"}],
         "options": [{"k": "a", "text": "I'm 24."}, {"k": "b", "text": "From Hue."}],
         "lines": [{"a": "Match.", "focus": 0}, {"wait": 2.5, "note": "Try"}, {"b": "One is b.", "reveal": 1},
                   {"b": "Two is a.", "focus": 1, "reveal": [2]}]},
        {"kind": "qa", "items": [{"q": "Where are you from?", "a": "From Hue.", "by": "a", "ask": "b", "phrases": ["I'm from…"]}],
         "lines": [{"b": "Where are you from?", "focus": 0}, {"a": "From Hue.", "reveal": 0}]},
        {"kind": "practice", "chapter": "Your turn", "items": [{"q": "Where are you from?", "hint": "I'm from…"}],
         "lines": [{"a": "Where are you from?", "focus": 0}, {"wait": 3}]},
    ],
}


def quiet(_msg):
    pass


def mini_book(tmp_path: Path) -> Path:
    bdir = tmp_path / "book"
    (bdir / "lessons").mkdir(parents=True)
    book = {"files": {}, "sections": [{"items": [{"id": "U01", "activities": [{"id": "U01-speaking-vocab"}]}]}]}
    (bdir / "book.json").write_text(json.dumps(book), encoding="utf-8")
    return bdir


def test_lines_are_normalised():
    lesson = sc.Lesson.model_validate(copy.deepcopy(LESSON))
    ln = lesson.scenes[1].lines
    assert (ln[2].speaker, ln[2].text, ln[2].reveal) == ("b", "One is b.", ["1"])
    assert ln[1].speaker is None and ln[1].wait == 2.5
    assert lesson.scenes[0].lines[1].vi == "Chào!"
    assert [c for _, c in lesson.chapters()] == ["Intro", "Match", "Your turn"]
    data = copy.deepcopy(LESSON)
    sc.Lesson.model_validate(data)
    assert data == LESSON                                              # không sửa dữ liệu đầu vào
    assert sc.Lesson.model_validate(lesson.model_dump()) == lesson     # dạng chuẩn đọc lại được


@pytest.mark.parametrize("patch", [
    lambda d: d["scenes"][0]["lines"].append({"zed": "who?"}),                       # người nói lạ
    lambda d: d["scenes"][0]["lines"].append({"a": "x", "b": "y"}),                   # hai người một dòng
    lambda d: d["scenes"][1]["lines"].append({"a": "x", "reveal": 9}),                # reveal không có mục
    lambda d: d["scenes"][1]["lines"].append({"a": "x", "focus": 5}),                 # focus ngoài số mục
    lambda d: d["scenes"][1]["items"][0].pop("answer"),                               # mục thiếu khóa
    lambda d: d["scenes"][2]["items"][0].update(by="zed"),                            # vai không có thật
    lambda d: d["speakers"]["a"].update(color="red"),                                 # màu sai dạng
])
def test_bad_scripts_are_rejected(patch):
    data = copy.deepcopy(LESSON)
    patch(data)
    with pytest.raises((ValidationError, ValueError)):
        sc.Lesson.model_validate(data)


def test_timeline_is_contiguous_and_keeps_state():
    lesson = sc.Lesson.model_validate(copy.deepcopy(LESSON))
    tl = timeline.build(lesson, tts.Silent(), say=quiet)
    assert tl.frames[0].start == 0
    for a, b in zip(tl.frames, tl.frames[1:]):
        assert abs(a.start + a.dur - b.start) < 1e-6
    assert abs(sum(f.dur for f in tl.frames) - tl.total) < 1e-6
    pairs = [f for f in tl.frames if f.scene == 1]
    # đếm ngược 2,5 giây: 3 (0,5 s), 2, 1
    cd = [(f.countdown, round(f.dur, 2)) for f in pairs if f.countdown]
    assert cd == [(3, 0.5), (2, 1.0), (1, 1.0)]
    assert all(f.focus == 0 for f in pairs[:4])                    # focus giữ trong lúc đếm ngược
    assert [sorted(f.revealed) for f in pairs[-2:]] == [["1"], ["1", "2"]]
    assert tl.frames[-1].revealed == frozenset()                   # cảnh mới thì đáp án đóng lại
    times = [t for t, _ in tl.chapters]
    assert times[0] == 0 and times == sorted(times) and len(times) == 3


def test_slides_render_every_kind(tmp_path):
    bdir = mini_book(tmp_path)
    lesson = sc.Lesson.model_validate(copy.deepcopy(LESSON))
    tl = timeline.build(lesson, tts.Silent(), say=quiet)
    slides = Slides(lesson, bdir, {"a": "silent", "b": "silent"})
    for fr in tl.frames:
        img = slides.render(fr, fr.start / tl.total)
        assert img.size == (W, H)


@pytest.mark.skipif(not shutil.which("ffmpeg"), reason="cần ffmpeg")
def test_build_writes_video_and_manifest(tmp_path):
    bdir = mini_book(tmp_path)
    path = bdir / "lessons" / "T-1.yaml"
    path.write_text(yaml.safe_dump(LESSON, allow_unicode=True), encoding="utf-8")
    assert cli.main(["build", str(path), "--engine", "silent"]) == 0
    assert cli.main(["build", str(path), "--engine", "silent"]) == 0   # chạy lại không nhân đôi mục
    data = json.loads((bdir / "lessons" / "lessons.json").read_text(encoding="utf-8"))
    assert [x["id"] for x in data["lessons"]] == ["T-1"]
    entry = data["lessons"][0]
    assert (entry["item"], entry["file"], entry["label"]) == ("U01", "lessons/T-1.mp4", "Speaking 1")
    assert [c["title"] for c in entry["chapters"]] == ["Intro", "Match", "Your turn"]
    mp4 = bdir / entry["file"]
    assert mp4.stat().st_size == entry["bytes"]
    if shutil.which("ffprobe"):
        assert abs(video.probe(mp4) - entry["duration"]) < 0.5


def test_check_reports_missing_activity(tmp_path):
    bdir = mini_book(tmp_path)
    data = copy.deepcopy(LESSON)
    data["activity"] = "U99-nothing"
    assert any("U99-nothing" in m for m in sc.check(sc.Lesson.model_validate(data), bdir))


def _flite():
    try:
        return tts.Flite()
    except tts.TTSError:
        return None


@pytest.mark.skipif(_flite() is None, reason="chưa cài Flite (libflite1)")
def test_flite_two_voices():
    eng = _flite()
    a, ra = eng.synth("Where are you from?", "slt")
    b, rb = eng.synth("Where are you from?", "rms")
    assert ra == rb == 16000
    assert len(a) > 0.5 * ra and abs(a.astype(int)).max() > 1000
    assert len(a) != len(b) or (a != b).any()                       # hai giọng khác nhau
    with pytest.raises(tts.TTSError):
        eng.synth("Hello", "nobody")


@pytest.mark.skipif(not (REAL / "lessons" / "lessons.json").exists(), reason="chưa có video bài giảng")
def test_committed_lessons_match_manifest():
    """Kịch bản đã commit hợp lệ, khớp lessons.json và file video có thật (hồi quy trên sách thật)."""
    data = json.loads((REAL / "lessons" / "lessons.json").read_text(encoding="utf-8"))
    by_id = {x["id"]: x for x in data["lessons"]}
    scripts = sorted((REAL / "lessons").glob("*.yaml"))
    assert len(scripts) == len(by_id) >= 2
    for path in scripts:
        lesson = sc.load(path)
        assert sc.check(lesson, REAL) == []
        entry = by_id[lesson.id]
        assert entry["activity"] == lesson.activity and entry["source"] == f"lessons/{path.name}"
        assert [c["title"] for c in entry["chapters"]] == [c for _, c in lesson.chapters()]
        assert (REAL / entry["file"]).stat().st_size == entry["bytes"]
        label = {"kokoro": "Kokoro", "flite": "Flite"}[entry["engine"]]
        assert len(entry["voices"]) == len(lesson.speakers) and all(label in v for v in entry["voices"])
        for sp in lesson.speakers.values():   # kịch bản khai giọng cho bộ đọc đã dùng
            sp.voice_for(entry["engine"])


def test_voice_per_engine():
    data = copy.deepcopy(LESSON)
    data["speakers"]["a"]["voice"] = {"kokoro": "bf_emma", "flite": "slt"}
    lesson = sc.Lesson.model_validate(data)
    sp = lesson.speakers["a"]
    assert (sp.voice_for("kokoro"), sp.voice_for("flite"), sp.voice_for("silent")) == ("bf_emma", "slt", "bf_emma")
    assert lesson.speakers["b"].voice_for("kokoro") == "rms"           # một giọng chung cho mọi bộ đọc
    data["speakers"]["a"]["voice"] = {"kokoro": "bf_emma"}
    lesson = sc.Lesson.model_validate(data)

    class OnlyFlite(tts.Silent):
        name, tag = "flite", "x"
    with pytest.raises(tts.TTSError, match="chưa khai báo giọng cho bộ đọc flite"):
        timeline.build(lesson, OnlyFlite(), say=quiet)                 # báo lỗi trước khi đọc câu nào


class Counting(tts.Silent):
    name, tag = "count", "count:1"

    def __init__(self):
        self.calls = 0

    def synth(self, text, voice):
        self.calls += 1
        return super().synth(text, voice)


def test_cache_only_reads_changed_lines(tmp_path):
    lesson = sc.Lesson.model_validate(copy.deepcopy(LESSON))
    n = len({(sp.voice, ln.spoken) for s in lesson.scenes for ln in s.lines if ln.speaker
             for sp in [lesson.speakers[ln.speaker]]})
    eng = Counting()
    first = timeline.build(lesson, eng, say=quiet, cache_dir=tmp_path)
    assert eng.calls == n
    eng2 = Counting()
    again = timeline.build(lesson, eng2, say=quiet, cache_dir=tmp_path)
    assert eng2.calls == 0 and (again.audio == first.audio).all()
    data = copy.deepcopy(LESSON)
    data["scenes"][0]["lines"][0]["a"] = "Hello again."
    eng3 = Counting()
    timeline.build(sc.Lesson.model_validate(data), eng3, say=quiet, cache_dir=tmp_path)
    assert eng3.calls == 1


def test_kokoro_needs_model(tmp_path, monkeypatch):
    monkeypatch.setattr(tts, "KOKORO_HOME", tmp_path / "none")
    monkeypatch.delenv("KOKORO_MODEL", raising=False)
    monkeypatch.delenv("KOKORO_VOICES", raising=False)
    assert tts.kokoro_files() == (None, None)
    with pytest.raises(tts.TTSError, match="model_quantized.onnx"):
        tts.get("kokoro")
    if _flite() is not None:
        assert tts.get("auto").name == "flite"


def test_load_voices_from_folder_and_npz(tmp_path):
    import numpy as np
    vdir = tmp_path / "voices"
    vdir.mkdir()
    np.zeros((510, 256), np.float32).tofile(vdir / "bf_emma.bin")
    np.ones((510, 256), np.float32).tofile(vdir / "am_michael.bin")
    got = tts.load_voices(vdir)
    assert sorted(got) == ["am_michael", "bf_emma"] and got["bf_emma"].shape == (510, 1, 256)
    np.savez(tmp_path / "v.npz", **got)
    assert sorted(tts.load_voices(tmp_path / "v.npz")) == ["am_michael", "bf_emma"]
    (vdir / "broken.bin").write_bytes(b"abc")
    with pytest.raises(tts.TTSError):
        tts.load_voices(vdir)


def _has_kokoro() -> bool:
    try:
        import kokoro_onnx  # noqa: F401
    except ImportError:
        return False
    return all(tts.kokoro_files())


@pytest.mark.skipif(not _has_kokoro(), reason="chưa có model Kokoro (xem agents/README.md)")
def test_kokoro_reads_english_voices():
    eng = tts.Kokoro(*tts.kokoro_files())
    a, rate = eng.synth("Where are you from?", "bf_emma")
    assert rate == 24000 and len(a) > 0.5 * rate and abs(a.astype(int)).max() > 1000
    with pytest.raises(tts.TTSError):
        eng.check("zf_xiaobei")      # không phải giọng tiếng Anh, hoặc không có


WRITING = {
    "id": "W-1", "activity": "U01-speaking-vocab", "title": "Unit 1", "subtitle": "Writing 1", "tag": "UNIT 1",
    "speakers": {"a": {"name": "Ann", "role": "teacher", "voice": "slt"},
                 "b": {"name": "Ben", "role": "student", "voice": "rms"}},
    "scenes": [
        {"kind": "order", "chapter": "Order",
         "items": [{"k": "a", "text": "Note down ideas.", "pos": 2}, {"k": "b", "text": "Check.", "pos": 3},
                   {"k": "c", "text": "Read the question.", "pos": 1}],
         "lines": [{"a": "Put them in order."}, {"wait": 2}, {"b": "First, c.", "focus": 2, "reveal": "c"},
                   {"a": "Then a and b.", "reveal": ["a", "b"]}]},
        {"kind": "timing", "chapter": "Time",
         "items": [{"label": "Plan", "minutes": 6, "vi": "Lập dàn ý"}, {"label": "Write", "minutes": 11},
                   {"label": "Check", "minutes": 3}],
         "lines": [{"a": "Six minutes to plan.", "focus": 0, "reveal": 0}, {"a": "Eleven to write.", "focus": 1, "reveal": 1}]},
        {"kind": "letter", "chapter": "Letter",
         "items": [{"text": "Dear Sir/Madam,", "say": "Dear Sir or Madam,", "note": "Opening", "body": False},
                   {"text": "I am writing to ask about your course.", "note": "Reason"},
                   {"text": "Yours faithfully,\nMai Tran", "body": False}],
         "lines": [{"read": "a", "focus": 0}, {"read": "b", "focus": 1}, {"read": "a", "focus": 2}]},
    ],
}


def test_writing_kinds_validate_and_render(tmp_path):
    lesson = sc.Lesson.model_validate(copy.deepcopy(WRITING))
    letter = lesson.scenes[2]
    assert [(ln.speaker, ln.text) for ln in letter.lines] == [
        ("a", "Dear Sir/Madam,"), ("b", "I am writing to ask about your course."), ("a", "Yours faithfully,\nMai Tran")]
    assert letter.lines[0].spoken == "Dear Sir or Madam,"            # `say` của đoạn thư dùng khi đọc
    assert lesson.scenes[0].reveal_keys() == {"a", "b", "c"}
    tl = timeline.build(lesson, tts.Silent(), say=quiet)
    order = [f for f in tl.frames if f.scene == 0]
    assert sorted(order[-1].revealed) == ["a", "b", "c"]
    slides = Slides(lesson, mini_book(tmp_path), {})
    for fr in tl.frames:
        assert slides.render(fr, fr.start / tl.total).size == (W, H)


@pytest.mark.parametrize("patch", [
    lambda d: d["scenes"][0]["items"][1].update(pos=2),                              # pos trùng
    lambda d: d["scenes"][1]["lines"].append({"read": "a", "focus": 0}),             # read ngoài cảnh letter
    lambda d: d["scenes"][2]["lines"].append({"read": "a"}),                         # read thiếu focus
    lambda d: d["scenes"][2]["lines"].append({"read": "zed", "focus": 1}),           # người đọc lạ
    lambda d: d["scenes"][2]["lines"].append({"wait": 3}),                           # letter không có đếm ngược
    lambda d: d["scenes"][1]["items"][0].pop("minutes"),                             # timing thiếu số phút
])
def test_bad_writing_scripts_are_rejected(patch):
    data = copy.deepcopy(WRITING)
    patch(data)
    with pytest.raises((ValidationError, ValueError)):
        sc.Lesson.model_validate(data)


def test_blanks_and_unlabelled_order(tmp_path):
    data = copy.deepcopy(WRITING)
    data["scenes"] = [
        {"kind": "blanks", "chapter": "Dictation",
         "items": [{"n": i, "answer": w, "tip": "t"} for i, w in enumerate(["father", "mother", "son"], 1)],
         "lines": [{"a": "Number one: father.", "focus": 0}, {"wait": 2}, {"b": "One: father.", "reveal": 1},
                   {"b": "Two and three.", "focus": 2, "reveal": [2, 3]}]},
        {"kind": "order", "items": [{"k": "birth", "label": "", "text": "birth", "pos": 1},
                                    {"k": "death", "label": "", "text": "death", "pos": 2}],
         "lines": [{"a": "Birth, then death.", "focus": 0, "reveal": ["birth", "death"]}]},
    ]
    lesson = sc.Lesson.model_validate(data)
    assert lesson.scenes[0].reveal_keys() == {"1", "2", "3"}
    tl = timeline.build(lesson, tts.Silent(), say=quiet)
    assert sorted(tl.frames[-2].revealed) == ["1", "2", "3"]
    slides = Slides(lesson, mini_book(tmp_path), {})
    for fr in tl.frames:
        assert slides.render(fr, fr.start / tl.total).size == (W, H)
    data["scenes"][0]["lines"].append({"a": "x", "reveal": 9})
    with pytest.raises((ValidationError, ValueError)):
        sc.Lesson.model_validate(data)


EXAM = {
    "id": "E-1", "activity": "U01-speaking-vocab", "title": "Unit 1", "subtitle": "Exam practice", "tag": "UNIT 1",
    "speakers": WRITING["speakers"],
    "scenes": [
        {"kind": "blanks", "chapter": "Listen", "hide_text": True, "roles": {"a": "receptionist", "b": "guest"},
         "items": [{"n": 1, "q": "Name of guest: Charles ___", "answer": "Hunt", "tip": "H-U-N-T"},
                   {"n": 2, "q": "One of my uncles has got ten ___.", "answer": "children", "hint": "child"}],
         "lines": [{"a": "Good evening."}, {"b": "That's Charles Hunt."}, {"wait": 2}]},
        {"kind": "blanks", "chapter": "Answers",
         "items": [{"n": 1, "q": "Name of guest: Charles ___", "answer": "Hunt", "tip": "H-U-N-T"}],
         "lines": [{"b": "Hunt.", "focus": 0, "reveal": 1}]},
        {"kind": "mcq", "chapter": "Choose",
         "items": [{"n": 5, "q": "Why is the guest travelling?", "options": ["on holiday", "on business"], "answer": "b"},
                   {"n": "A", "q": "Which subject?", "keys": [1, 2, 3], "options": ["x", "y", "z"], "answer": 3}],
         "lines": [{"a": "Number five?", "focus": 0}, {"b": "On business.", "reveal": 5}, {"b": "Three.", "focus": 1, "reveal": "A"}]},
    ],
}


def test_exam_kinds_validate_and_render(tmp_path):
    lesson = sc.Lesson.model_validate(copy.deepcopy(EXAM))
    assert lesson.scenes[0].hide_text and lesson.scenes[0].roles == {"a": "receptionist", "b": "guest"}
    assert lesson.scenes[2].reveal_keys() == {"5", "A"}
    assert sc.mcq_keys(lesson.scenes[2].items[1]) == ["1", "2", "3"]
    tl = timeline.build(lesson, tts.Silent(), say=quiet)
    assert sorted(tl.frames[-1].revealed) == ["5", "A"]
    slides = Slides(lesson, mini_book(tmp_path), {})
    for fr in tl.frames:
        assert slides.render(fr, fr.start / tl.total).size == (W, H)


@pytest.mark.parametrize("patch", [
    lambda d: d["scenes"][2]["items"][0].update(answer="c"),                         # đáp án ngoài a, b
    lambda d: d["scenes"][2]["items"][1].update(answer="c"),                         # đáp án ngoài keys
    lambda d: d["scenes"][2]["items"][1].update(keys=[1, 2]),                        # thiếu nhãn
    lambda d: d["scenes"][2]["items"][0].pop("options"),                             # mcq thiếu phương án
    lambda d: d["scenes"][0].update(roles={"zed": "guest"}),                         # vai cho người lạ
    lambda d: d["scenes"][1]["lines"].append({"b": "x", "reveal": 2}),               # mở ô không có
])
def test_bad_exam_scripts_are_rejected(patch):
    data = copy.deepcopy(EXAM)
    patch(data)
    with pytest.raises((ValidationError, ValueError)):
        sc.Lesson.model_validate(data)


def test_coverage_lists_parts_with_and_without_video(tmp_path):
    from lesson_video import coverage
    bdir = mini_book(tmp_path)
    book = json.loads((bdir / "book.json").read_text(encoding="utf-8"))
    book["sections"][0]["items"][0]["activities"].append({"id": "U01-writing", "title": "Unit 1 · Writing", "printedPages": [17, 18]})
    book["sections"][0]["items"].append({"id": "U02", "activities": [{"id": "U02-reading"}]})
    (bdir / "book.json").write_text(json.dumps(book), encoding="utf-8")
    entry = {"id": "T-1", "activity": "U01-speaking-vocab", "label": "Speaking 1", "duration": 75.4, "chapters": [{"t": 0, "title": "a"}]}
    video.write_manifest(bdir / "lessons", entry)
    (bdir / "lessons" / "W-1.yaml").write_text("id: W-1\nactivity: U01-writing\n", encoding="utf-8")
    units = coverage.coverage(bdir, ["U01"])
    assert [u["item"] for u in units] == ["U01"]
    parts = units[0]["parts"]
    assert [p["activity"] for p in parts] == ["U01-speaking-vocab", "U01-writing"]
    assert [v["id"] for v in parts[0]["videos"]] == ["T-1"] and parts[1]["drafts"] == ["W-1"]
    md = coverage.to_markdown(units)
    assert "1/2 phần có video, 1 video, 1:15" in md and "kịch bản chưa dựng: W-1" in md and "sách tr. 17–18" in md
    assert len(coverage.coverage(bdir)) == 2
    assert cli.main(["coverage", str(bdir), "--unit", "U02"]) == 0


@pytest.mark.skipif(not (REAL / "lessons" / "lessons.json").exists(), reason="chưa có video bài giảng")
def test_unit1_2_video_coverage():
    """Unit 1 và 2: mọi phần có trang trong Course Book đều có video; phiên ôn unit thì không (docs/agent-hoc-tap/06)."""
    from lesson_video import coverage
    for unit in coverage.coverage(REAL, ["U01", "U02"]):
        have = {p["activity"].split("-", 1)[1]: [v["id"] for v in p["videos"]] for p in unit["parts"]}
        assert not have["unit-review"], unit["item"]
        for part in ("speaking-vocab", "listening", "reading", "writing", "consolidation", "exam-practice"):
            assert have[part], f"{unit['item']} {part}"


def _wav(path: Path, seconds: float, rate: int = 16000):
    import wave
    import numpy as np
    t = np.arange(int(seconds * rate)) / rate
    data = (np.sin(2 * np.pi * 440 * t) * 8000).astype(np.int16)
    with wave.open(str(path), "wb") as w:
        w.setnchannels(1)
        w.setsampwidth(2)
        w.setframerate(rate)
        w.writeframes(data.tobytes())


READING = {
    "id": "R-1", "activity": "U01-speaking-vocab", "title": "Unit 2", "subtitle": "Reading 1", "tag": "UNIT 2",
    "speakers": WRITING["speakers"],
    "scenes": [
        {"kind": "passage", "chapter": "Scan",
         "items": [{"label": "1", "text": "You need a licence, which costs £38."},
                   {"label": "2", "text": "The test lasts about 40 minutes.", "note": "the test"}],
         "lines": [{"a": "How much?", "focus": 0, "mark": "£38"}, {"wait": 1}, {"b": "Still the same part."},
                   {"a": "How long?", "focus": 1, "mark": ["40 minutes"]}, {"b": "Another line, same part.", "focus": 1}]},
        {"kind": "blanks", "chapter": "Listen",
         "items": [{"n": 1, "answer": "18"}],
         "lines": [{"a": "Listen."}, {"track": "T-1", "note": "Track 1", "start": 0.2, "end": 1.0},
                   {"b": "Eighteen.", "reveal": 1}]},
    ],
}


def _reading_book(tmp_path: Path) -> Path:
    bdir = mini_book(tmp_path)
    _wav(bdir / "t1.wav", 1.5)
    book = json.loads((bdir / "book.json").read_text(encoding="utf-8"))
    book["files"]["T-1"] = {"kind": "audio", "path": "t1.wav", "durationSec": 1.5}
    (bdir / "book.json").write_text(json.dumps(book), encoding="utf-8")
    return bdir


def test_passage_marks_and_book_tracks(tmp_path):
    bdir = _reading_book(tmp_path)
    lesson = sc.Lesson.model_validate(copy.deepcopy(READING))
    assert sc.check(lesson, bdir) == []
    tl = timeline.build(lesson, tts.Silent(), say=quiet, book_dir=bdir)
    marks = [f.mark for f in tl.frames if f.scene == 0]
    assert marks[:3] == [("£38",), ("£38",), ("£38",)]          # giữ qua khoảng lặng và câu không đổi đoạn
    assert marks[3:] == [("40 minutes",), ("40 minutes",)]       # đổi đoạn thì thay cụm tô vàng
    audio = [f for f in tl.frames if f.audio]
    assert [f.audio for f in audio] == ["T-1"] and audio[0].note == "Track 1"
    assert 0.75 < audio[0].dur - lesson.gap < 0.85                 # chỉ phát đoạn 0,2–1,0 giây
    slides = Slides(lesson, bdir, {})
    for fr in tl.frames:
        assert slides.render(fr, fr.start / tl.total).size == (W, H)
    with pytest.raises(tts.TTSError):                              # thiếu thư mục sách thì báo rõ
        timeline.build(lesson, tts.Silent(), say=quiet)


def test_check_reports_bad_tracks(tmp_path):
    bdir = _reading_book(tmp_path)
    data = copy.deepcopy(READING)
    data["scenes"][1]["lines"][1].update(track="T-9")
    assert any("T-9" in p for p in sc.check(sc.Lesson.model_validate(data), bdir))
    data["scenes"][1]["lines"][1].update(track="T-1", end=9.0)
    assert any("1.5" in p for p in sc.check(sc.Lesson.model_validate(data), bdir))
    (bdir / "t1.wav").unlink()
    data["scenes"][1]["lines"][1].update(end=1.0)
    assert any("t1.wav" in p for p in sc.check(sc.Lesson.model_validate(data), bdir))


@pytest.mark.parametrize("patch", [
    lambda d: d["scenes"][1]["lines"].append({"a": "x", "mark": "18"}),            # mark ngoài cảnh passage
    lambda d: d["scenes"][1]["lines"].append({"a": "x", "track": "T-1"}),          # vừa nói vừa phát
    lambda d: d["scenes"][1]["lines"].append({"track": "T-1", "start": 2, "end": 1}),  # end trước start
    lambda d: d["scenes"][1]["lines"].append({"b": "x", "start": 1}),              # start không kèm track
    lambda d: d["scenes"][0]["items"][0].pop("text"),                              # passage thiếu chữ
])
def test_bad_reading_scripts_are_rejected(patch):
    data = copy.deepcopy(READING)
    patch(data)
    with pytest.raises((ValidationError, ValueError)):
        sc.Lesson.model_validate(data)


def test_split_letter_keeps_total_word_count(tmp_path):
    data = copy.deepcopy(WRITING)
    data["scenes"][2]["words"] = 167
    lesson = sc.Lesson.model_validate(data)
    assert lesson.scenes[2].words == 167 and lesson.scenes[0].words is None
    tl = timeline.build(lesson, tts.Silent(), say=quiet)
    slides = Slides(lesson, mini_book(tmp_path), {})
    assert slides.render(tl.frames[-1], 1.0).size == (W, H)
