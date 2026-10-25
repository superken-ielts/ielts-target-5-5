"""Video tiếng Nhật (lộ trình N5): furigana, romaji, cảnh `jp` ba tầng, tốc độ từng câu, đối chiếu cách đọc."""
import copy
import json
from pathlib import Path

import pytest

from lesson_video import ja, script as sc, timeline, tts
from lesson_video.slides import H, W, Slides

JP = {
    "id": "J-1", "activity": "U01-part-a", "title": "Unit 1", "subtitle": "Part A", "tag": "TARGET N5 • 5.0",
    "gap": 0, "scene_gap": 0,
    "speakers": {
        "emma": {"name": "Emma", "role": "grammar & topic guide", "voice": {"kokoro": "bf_emma"}, "color": "#00A8B5",
                 "speed": 1.0},
        "yuki": {"name": "Yuki", "role": "Japanese tutor", "lang": "ja", "voice": {"kokoro": "jf_alpha"},
                 "color": "#F39C12", "speed": 0.88},
    },
    "scenes": [
        {"kind": "jp", "chapter": "Pattern", "heading": "Unit 1.1: Core Pattern [ X は Y です ]",
         "items": [{"jp": "X は Y です", "romaji": "X wa Y desu", "en": "'Wa' marks the topic.",
                    "vi": "Trợ từ 'は' (đọc là 'wa') đánh dấu chủ đề."}],
         "lines": [{"emma": "Our first grammar point is X wa Y des.", "pause": 0.6}]},
        {"kind": "jp", "chapter": "Shadowing", "heading": "Shadowing: Time",
         "items": [{"jp": "いま、{午前九時半|ごぜんくじはん}です。わたしは{IT|アイティー}の{会社員|かいしゃいん}です。",
                    "romaji": "Ima, gozen ku-ji han desu. Watashi wa ai-tii no kaishain desu.",
                    "en": "It is 9:30 AM now. I am an IT company employee.",
                    "vi": "Bây giờ là 9 giờ rưỡi sáng. Tôi là nhân viên công ty IT."}],
         "lines": [{"yuki": "いま、午前九時半です。わたしはITの会社員です。",
                    "say": "いま、午前くじ半です。わたしはアイティーの会社員です。", "pause": 1.8, "speed": 0.9}]},
    ],
}


def quiet(_msg):
    pass


def lesson(patch=None):
    data = copy.deepcopy(JP)
    if patch:
        patch(data)
    return sc.Lesson.model_validate(data)


# ---------- furigana, romaji (không cần misaki) ----------
def test_ruby_markup():
    text = "わたしは {留学生|りゅうがくせい}です。{IT|アイティー}"
    assert ja.plain(text) == "わたしは 留学生です。IT"
    assert ja.reading(text) == "わたしは りゅうがくせいです。アイティー"
    assert ja.segments("{持|も}ち{物|もの}") == [("持", "も"), ("ち", None), ("物", "もの")]
    assert ja.kana_only(ja.reading(text)) == "ワタシハリュウガクセイデスアイティー"
    assert ja.check_markup(text) == []
    assert "chữ Hán chưa có furigana: 何" in ja.check_markup("お{仕事|しごと}は何ですか")[0]
    assert "furigana trống" in ja.check_markup("{学生|}")[0]
    assert "phải viết bằng kana" in ja.check_markup("{学生|学生}")[0]
    assert "viết sai" in ja.check_markup("{学生|がくせい です")[0]


@pytest.mark.parametrize("kana,romaji", [
    ("りゅうがくせい", "ryuugakusei"), ("コーヒー", "koohii"), ("アイティー", "aitii"), ("ソフトウェア", "sofutowea"),
    ("いっしょ", "issho"), ("にじゅうはっさい", "nijuuhassai"), ("マッチャ", "matcha"), ("ファン", "fan"),
    ("じゃないです", "janaidesu"), ("ちょっと", "chotto"), ("べんきょう", "benkyou"), ("にっ ぽん", "nippon"),
])
def test_kana_romaji(kana, romaji):
    assert ja.kana_romaji(kana).replace(" ", "") == romaji


def test_romaji_normalisation():
    assert ja.norm_romaji("Nijuu-hassai desu. / Watashi wa ai-tii") == "nijuuhassaidesuwatashiwaaitii"
    assert ja.norm_romaji("shimbun, matcha") == ja.norm_romaji("shinbun, maccha")


# ---------- cảnh jp ----------
def test_jp_scene_validates():
    les = lesson()
    assert les.speakers["yuki"].lang == "ja" and les.speakers["emma"].lang == "en"
    ln = les.scenes[1].lines[0]
    assert (ln.speed, ln.pause, ln.spoken) == (0.9, 1.8, JP["scenes"][1]["lines"][0]["say"])


@pytest.mark.parametrize("patch,msg", [
    (lambda d: d["scenes"][0]["items"].append({"jp": "です"}), "đúng một mục"),
    (lambda d: d["scenes"][0]["lines"].append({"wait": 2}), "không có khoảng lặng"),
    (lambda d: d["scenes"][1]["items"][0].update(jp="{午前|ごぜん}九時です"), "chưa có furigana: 九 時"),
    (lambda d: d["scenes"][1]["lines"][0].pop("say"), "chữ Latin hoặc chữ số"),
    (lambda d: d["speakers"]["yuki"].update(voice={"kokoro": "af_heart"}), "không phải giọng Nhật"),
    (lambda d: d["scenes"][0]["lines"].append({"wait": 1, "speed": 0.8}), "chỉ dùng cho câu thoại"),
])
def test_bad_jp_scripts_are_rejected(patch, msg):
    with pytest.raises(ValueError, match=msg):
        lesson(patch)


def test_jp_scene_renders(tmp_path):
    les = lesson()
    tl = timeline.build(les, tts.Silent(), say=quiet)
    sl = Slides(les, tmp_path)
    for fr in tl.frames:
        img = sl.render(fr, 0.5)
        assert img.size == (W, H)
        assert img.getpixel((5, 5)) == (0x0F, 0x25, 0x37)             # nền navy
        assert img.getpixel((W // 2, 112)) == (0xFA, 0xFC, 0xFE)      # thẻ trắng tầng 1
        assert img.getpixel((60, 705)) == (0xF3, 0x9C, 0x12)          # thanh tiến độ màu cam


class Speedy(tts.Silent):
    name = "silent"   # giọng khai cho kokoro; bộ đọc silent dùng giọng đầu tiên

    def __init__(self):
        self.calls = []

    def synth(self, text, voice, speed=None):
        self.calls.append((voice, speed))
        return super().synth(text, voice, speed)


def test_line_and_speaker_speed():
    les = lesson()
    eng = Speedy()
    timeline.build(les, eng, say=quiet)
    # câu của Emma: tốc độ người nói 1.0; câu của Yuki: tốc độ riêng của câu 0.9 (thắng tốc độ người nói 0.88)
    assert eng.calls == [("bf_emma", 1.0), ("jf_alpha", 0.9)]
    a, _ = tts.Silent().synth("x" * 50, "v")
    b, _ = tts.Silent().synth("x" * 50, "v", speed=0.5)
    assert len(b) == 2 * len(a)


class FakeKokoro(Speedy):
    name, tag = "kokoro", "fake-kokoro:1"


def test_speed_is_part_of_cache_key(tmp_path):
    timeline.build(lesson(), FakeKokoro(), say=quiet, cache_dir=tmp_path)
    eng = FakeKokoro()
    timeline.build(lesson(), eng, say=quiet, cache_dir=tmp_path)
    assert eng.calls == []                                             # đọc lại từ bộ nhớ tiếng
    eng = FakeKokoro()
    timeline.build(lesson(lambda d: d["scenes"][1]["lines"][0].update(speed=1.1)), eng, say=quiet, cache_dir=tmp_path)
    assert eng.calls == [("jf_alpha", 1.1)]                            # chỉ câu đổi tốc độ phải đọc lại


# ---------- đối chiếu cách đọc với misaki ----------
needs_misaki = pytest.mark.skipif(not ja.available(), reason='chưa cài misaki[ja] (pip install "misaki[ja]")')


@needs_misaki
def test_reading_check_catches_misreadings():
    assert sc.check_japanese(lesson()) == []
    # misaki đọc 九時 là きゅうじ, 日本語 là にっぽんご: thiếu `say` thì bị chặn, có chỉ chữ Hán đọc sai
    bad = lesson(lambda d: d["scenes"][1]["lines"][0].update(say="いま、午前九時半です。わたしはアイティーの会社員です。"))
    msgs = sc.check_japanese(bad)
    assert len(msgs) == 2 and "九(キュウ)" in msgs[0] and "romaji không khớp" in msgs[1]
    assert ja.check_line("{日本語|にほんご}です", "日本語です")
    assert ja.check_line("{日本語|にほんご}です", "にほんごです") == []
    # romaji sai (ku-ji ≠ kyuu-ji) cũng bị chặn
    wrong = lesson(lambda d: d["scenes"][1]["items"][0].update(romaji="Ima, gozen kyuu-ji han desu. Watashi wa ai-tii no kaishain desu."))
    assert any("romaji không khớp" in m for m in sc.check_japanese(wrong))


def _has_kokoro_ja() -> bool:
    try:
        import kokoro_onnx  # noqa: F401
    except ImportError:
        return False
    m, v = tts.kokoro_files()
    return bool(m and v and ja.available()) and "jf_alpha" in tts.load_voices(v)


@pytest.mark.skipif(not _has_kokoro_ja(), reason="chưa có Kokoro + giọng jf_alpha + misaki[ja]")
def test_kokoro_reads_japanese():
    eng = tts.Kokoro(*tts.kokoro_files())
    a, rate = eng.synth("わたしは学生です。", "jf_alpha", speed=0.88)
    b, _ = eng.synth("わたしは学生です。", "jf_alpha", speed=1.2)
    assert rate == 24000 and len(a) > 0.8 * rate and abs(a.astype(int)).max() > 1000
    assert len(b) < len(a)                                             # đọc nhanh hơn thì ngắn hơn


def test_check_reports_japanese_problems_with_book(tmp_path):
    bdir = tmp_path / "book"
    (bdir / "lessons").mkdir(parents=True)
    book = {"files": {}, "sections": [{"items": [{"id": "U01", "activities": [{"id": "U01-part-a"}]}]}]}
    (bdir / "book.json").write_text(json.dumps(book), encoding="utf-8")
    probs = sc.check(lesson(), bdir)
    if ja.available():
        assert probs == []
    else:                                                              # không có misaki thì báo cần cài
        assert len(probs) == 1 and "misaki" in probs[0]
