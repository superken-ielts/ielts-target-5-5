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
