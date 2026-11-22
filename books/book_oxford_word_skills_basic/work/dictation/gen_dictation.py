"""Sinh kịch bản video nghe – viết (dictation) cho Oxford Word Skills Basic (đợt 36) — docs/agent-hoc-tap/09 mục 5.9.

python3 books/book_oxford_word_skills_basic/work/dictation/gen_dictation.py [U02 U03 …]
    dữ liệu từng unit ở units_*.py (cùng thư mục), ghi lessons/<id>.yaml; không ghi unit nào thì sinh lại tất cả.
    Kịch bản .yaml là bản sinh ra: sửa dữ liệu ở đây rồi chạy lại, không sửa tay .yaml.

Mỗi mục:
  book / extra: (answer, vi, ex, keys, opts)  — keys: mục Word list mà dòng phủ (chuỗi / danh sách / None = không phải
                từ của Word list); opts: {"s": cách đọc answer, "se": cách đọc câu ví dụ, "pos": từ loại}
  phrases:      (câu, vi, người đọc "emma" | "tom", opts)  — opts: {"s": cách đọc}
"""
import importlib
import json
import os
import sys
from pathlib import Path

HERE = Path(__file__).parent
sys.path.insert(0, str(HERE))
ONES = ["zero", "one", "two", "three", "four", "five", "six", "seven", "eight", "nine", "ten", "eleven", "twelve",
        "thirteen", "fourteen", "fifteen", "sixteen", "seventeen", "eighteen", "nineteen"]
TENS = ["", "", "twenty", "thirty", "forty", "fifty", "sixty", "seventy", "eighty", "ninety"]
PER = 6
WORD_PAUSE = 1.5   # sau mỗi từ (giây) — video chạy liền, người học tự tạm dừng khi cần
SENT_PAUSE = 2.0   # sau mỗi câu giao tiếp


def num(n: int) -> str:
    if n < 20:
        w = ONES[n]
    elif n < 100:
        w = TENS[n // 10] + ("-" + ONES[n % 10] if n % 10 else "")
    else:
        w = ONES[n // 100] + " hundred" + (" and " + num(n % 100).lower() if n % 100 else "")
    return w[0].upper() + w[1:]


def j(d: dict) -> str:
    return json.dumps(d, ensure_ascii=False)


def scene_block(kind, chapter, heading, heading_vi, items, lines) -> list[str]:
    out = [f"  - kind: {kind}"]
    if chapter:
        out.append(f"    chapter: {j(chapter)}")
    out += [f"    heading: {j(heading)}", f"    heading_vi: {j(heading_vi)}"]
    if items:
        out.append("    items:")
        out += [f"      - {j(it)}" for it in items]
    out.append("    lines:")
    out += [f"      - {j(ln)}" for ln in lines]
    return out + [""]


def word_items(entries, start, speaker, part_no, title_en, title_vi, chapter, intro):
    """book / extra → các cảnh dictation 6 mục: số, từ hai lần, câu ví dụ; mở đáp án khi sang mục sau."""
    out, n = [], start
    chunks = [entries[i:i + PER] for i in range(0, len(entries), PER)]
    for ci, chunk in enumerate(chunks):
        items, lines = [], []
        if ci == 0 and intro:
            lines.append({speaker: intro[0], "vi": intro[1]})
        for k, (a, vi, ex, keys, *rest) in enumerate(chunk):
            o = rest[0] if rest else {}
            it = {"n": n, "answer": a}
            if o.get("pos"):
                it["pos"] = o["pos"]
            it["vi"] = vi
            if ex:
                it["ex"] = ex
            if keys:
                it["w"] = keys if isinstance(keys, list) else [keys]
            items.append(it)
            s = o.get("s", a)
            text = f"{num(n)}. {a}. {a}. {ex}".strip()
            say = f"{num(n)}. {s}. {s}. {o.get('se', ex)}".strip()
            ln = {speaker: text}
            if say != text:
                ln["say"] = say
            ln["focus"] = k
            if k > 0:
                ln["reveal"] = [n - 1]
            ln["pause"] = WORD_PAUSE
            lines.append(ln)
            n += 1
        lines.append({speaker: "Check your answers.", "vi": "Kiểm tra bài viết của bạn.", "focus": len(chunk) - 1,
                      "reveal": [n - 1], "pause": 2.0})
        a0, a1 = items[0]["n"], items[-1]["n"]
        out += scene_block("dictation", chapter if ci == 0 else "", f"Dictation {part_no} · {title_en} ({a0}–{a1})",
                           title_vi, items, lines)
    return out, n


def sentence_items(entries, start, chapter, intro):
    out, n = [], start
    chunks = [entries[i:i + PER] for i in range(0, len(entries), PER)]
    for ci, chunk in enumerate(chunks):
        items, lines = [], []
        if ci == 0 and intro:
            lines.append({"emma": intro[0], "vi": intro[1]})
        for k, (s, vi, who, *rest) in enumerate(chunk):
            o = rest[0] if rest else {}
            items.append({"n": n, "answer": s, "vi": vi})
            sp = o.get("s", s)
            text = f"{num(n)}. {s} {s}"
            say = f"{num(n)}. {sp} {sp}"
            ln = {who: text}
            if say != text:
                ln["say"] = say
            ln["focus"] = k
            if k > 0:
                ln["reveal"] = [n - 1]
            ln["pause"] = SENT_PAUSE
            lines.append(ln)
            n += 1
        lines.append({"emma": "Check your answers.", "vi": "Kiểm tra bài viết của bạn.", "focus": len(chunk) - 1,
                      "reveal": [n - 1], "pause": 2.0})
        a0, a1 = items[0]["n"], items[-1]["n"]
        out += scene_block("dictation", chapter if ci == 0 else "", f"Dictation 3 · Useful sentences ({a0}–{a1})",
                           "Câu giao tiếp hay dùng — mỗi câu đọc hai lần; tạm dừng video để viết", items, lines)
    return out, n


def build(u: dict) -> str:
    no = int(u["unit"][1:])
    nb, nx, np_ = len(u["book"]), len(u["extra"]), len(u["phrases"])
    head = [f"# Video nghe – viết (dictation) Unit {no} · {u['topic']} — Oxford Word Skills Basic (đợt 36).",
            f"# Dựng: cd agents && python -m lesson_video build ../books/book_oxford_word_skills_basic/lessons/{u['id']}.yaml",
            "# Người học: \"mỗi chủ đề thêm 1 video luyện nghe 10 phút ko đứt quãng tôi tự pause lại để viết theo từ vựng câu",
            "# theo chủ đề phải bao gồm các từ vựng trong sách thuộc chủ đề trong sách rồi tìm thêm các từ vựng câu hay giao tiếp\".",
            "# Khuôn (file 09 mục 5.9): video chạy liền khoảng 10 phút, không đếm ngược; cảnh `dictation` ẩn chữ, mở đáp án khi sang",
            "# mục sau; phần 1 = mọi mục Word list của unit (tr. 237–254, `work/wordlist.json`) và từ trên trang unit, mỗi từ đọc hai",
            "# lần rồi một câu ví dụ; phần 2 = từ thêm theo chủ đề (ngoài sách); phần 3 = câu giao tiếp hay dùng, mỗi câu đọc hai lần.",
            f"# Soát đủ từ: python -m lesson_video wordlist ../books/book_oxford_word_skills_basic --unit {u['unit']} --level all",
            "# Sinh bằng work/dictation/gen_dictation.py từ dữ liệu work/dictation/units_*.py — sửa dữ liệu rồi sinh lại, không",
            "# sửa tay file này. Câu ngôi thứ nhất khớp hồ sơ nhân vật (file 06 mục 9.4, file 09 mục 5.7) hoặc viết trung tính."]
    head += [f"# {c}" for c in u.get("notes", [])]
    head += [f"id: {u['id']}", f"activity: {u['activity']}", f"title: {j(u['title'])}",
             f"subtitle: {j('Dictation · listen and write: ' + u['topic_en_short'])}",
             f"title_vi: {j('Nghe – viết 10 phút: ' + u['topic_vi'] + ' — từ trong sách, từ thêm, câu giao tiếp')}",
             f"tag: {j(u['tag'])}",
             "speakers:",
             "  # giọng theo bộ đọc: kokoro (mặc định khi có model) hoặc flite (dự phòng, có sẵn trên Ubuntu)",
             '  emma: {name: Emma, role: teacher, color: "#C8102E", voice: {kokoro: af_heart, flite: slt}}',
             '  tom: {name: Tom, role: student, color: "#1F5FAD", voice: {kokoro: am_michael, flite: rms}}',
             "", "scenes:"]
    nxt = u.get("next", f"Unit {no + 1}")
    intro = [
        {"emma": f"Welcome to the dictation for Unit {no}: {u['topic']}. Listen and write. The video doesn't stop, so pause it whenever you need more time to write.",
         "say": f"Welcome to the dictation for Unit {num(no).lower()}: {u['topic_say']}. Listen and write. The video doesn't stop, so pause it whenever you need more time to write.",
         "vi": f"Bài nghe – viết Unit {no}: {u['topic_vi']}. Video chạy liền — bạn tự tạm dừng khi cần thời gian viết."},
        {"emma": f"There are three parts. First, {nb} words from the book. You hear each word twice, then a sentence. Then {nx} more useful words, and {np_} useful sentences for conversation.",
         "say": f"There are three parts. First, {num(nb).lower()} words from the book. You hear each word twice, then a sentence. Then {num(nx).lower()} more useful words, and {num(np_).lower()} useful sentences for conversation.",
         "vi": f"Ba phần: {nb} từ trong sách (mỗi từ đọc hai lần, rồi một câu ví dụ), {nx} từ thêm, {np_} câu giao tiếp."},
        {"tom": "The answer appears when the next one starts. So write first, then check.",
         "vi": "Đáp án hiện khi sang mục sau: viết trước, rồi kiểm tra."},
    ]
    body = [f"  - kind: title", '    chapter: "Giới thiệu"', "    lines:"] + [f"      - {j(x)}" for x in intro] + [""]
    p1, n = word_items(u["book"], 1, "emma", 1, "Words from the book",
                       "Từ trong sách — nghe từ hai lần rồi câu ví dụ; tạm dừng video để viết", "1. Từ trong sách",
                       ("Part one. Words from the book.", "Phần 1: từ trong sách."))
    p2, n = word_items(u["extra"], n, "tom", 2, "More useful words",
                       "Từ thêm theo chủ đề (ngoài sách) — nghe hai lần rồi câu ví dụ", "2. Từ thêm theo chủ đề",
                       ("Part two. More useful words.", "Phần 2: từ thêm theo chủ đề."))
    p3, n = sentence_items(u["phrases"], n, "3. Câu giao tiếp",
                           ("Part three. Useful sentences. You hear each sentence twice.",
                            "Phần 3: câu giao tiếp — mỗi câu đọc hai lần."))
    end_items = [
        {"en": "Check your spelling with the answers on the screen.", "vi": "Soát chính tả với đáp án trên màn hình"},
        {"en": "Cover the English. Read the Vietnamese and say the word.", "vi": "Che tiếng Anh, nhìn nghĩa tiếng Việt, nói lại từ"},
        {"en": "Say five of the useful sentences out loud today.", "vi": "Nói to 5 câu giao tiếp trong hôm nay"},
    ]
    end_lines = [{"emma": it["en"], "focus": k} for k, it in enumerate(end_items)]
    end_lines.append({"tom": f"Well done! See you in {nxt}.", "say": f"Well done! See you in {u.get('next_say', 'Unit ' + num(no + 1).lower())}.",
                      "vi": f"Giỏi lắm! Hẹn gặp ở {u.get('next_vi', nxt)}."})
    end = scene_block("bullets", "Sau khi nghe – viết", "After the dictation", "Ôn lại", end_items, end_lines)
    return "\n".join(head + body + p1 + p2 + p3 + end)


if __name__ == "__main__":
    outdir = HERE.parent.parent / "lessons"
    want = sys.argv[1:]
    units = {}
    for mod in sorted(HERE.glob("units_*.py")):
        units.update(importlib.import_module(mod.stem).UNITS)
    for code in want or sorted(units):
        u = units[code]
        p = outdir / f"{u['id']}.yaml"
        tmp = p.with_suffix(".yaml.tmp")
        tmp.write_text(build(u) + "\n", encoding="utf-8")
        os.replace(tmp, p)   # thay cả file một lần (lệnh build đang chạy không đọc phải file dở)
        print(p.name, len(u["book"]), len(u["extra"]), len(u["phrases"]))
