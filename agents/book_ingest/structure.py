"""Bước 2 — dựng cấu trúc sách: khoảng trang từng module, review, đáp án, tapescript.

Chỉ dùng code tất định:
- Trang mở đầu mỗi module nhận ra bằng băng tiêu đề đỏ (pdfutil.red_ratio).
- Độ lệch số trang kiểm tra bằng cách xem trang đầu mọi unit có băng tiêu đề không.
- Answer key và Tapescript lập chỉ mục bằng OCR tiêu đề "Unit 4, Listening 2A" (ocr.py, có cache).
Chỗ nào không khớp kỳ vọng thì sinh mục duyệt thay vì tự sửa.
"""
from __future__ import annotations

import re
from typing import Optional

from . import pdfutil
from .ocr import OcrCache, reading_order
from .profile import Profile
from .schemas import ReviewItem

# OCR hay dính chữ ("Unit 13Listening3") và dùng dấu gạch ("Unit 12-Speaking 3"), nên khoảng trắng
# và dấu phân cách đều không bắt buộc.
SEP = r"\s*[,.:\-\u2013\u2014]?\s*"
HEAD_UNIT = re.compile(r"^(?P<wb>work\s*book\s*)?unit\s*(?P<u>\d{1,2})" + SEP + r"(?P<rest>.*)$", re.I)
HEAD_REVIEW = re.compile(r"^review\s*(?P<n>\d)\b" + SEP + r"(?P<rest>.*)$", re.I)
HEAD_TEST = re.compile(r"^test\s*(?P<n>\d)\b", re.I)
HEAD_STOP = re.compile(r"^academic(\s+section)?\b", re.I)
# Chữ cái bài ngay sau tiêu đề track: "C Now listen…", hoặc dính liền "CNowlisten…", "AListen…".
EXERCISE = re.compile(r"^(?P<ex>[A-N])(?=[A-Z\s]|$)")


def module_of(rest: str) -> Optional[str]:
    r = rest.lower()
    if r.startswith("exam"):
        return "exam-practice"
    for key, mod in (("consolidation", "consolidation"), ("listening", "listening"), ("reading", "reading"),
                     ("writing", "writing"), ("speaking", "speaking-vocab"), ("vocabulary", "speaking-vocab"),
                     ("pronunciation", "speaking-vocab")):
        if r.startswith(key):
            return mod
    return None


def chosen(decisions: dict, rid: str, proposal: Optional[dict]) -> Optional[dict]:
    """Quyết định của người duyệt: {"accept": true} → đề xuất; {"value": {...}} → giá trị sửa; {"skip": true} → bỏ."""
    d = decisions.get(rid)
    if not d or d.get("skip"):
        return None
    if d.get("accept"):
        return proposal
    return d.get("value")


# --------------------------------------------------------------------------
# Băng tiêu đề và độ lệch trang
# --------------------------------------------------------------------------
def banner_pages(profile: Profile, doc, first: int, last: int) -> list[int]:
    return [p for p in range(first, last + 1)
            if pdfutil.red_ratio(doc, p, profile.banner_top) >= profile.banner_min_red]


def check_offset(profile: Profile, doc, items: list[ReviewItem]) -> int:
    """Trang đầu mọi unit phải có băng tiêu đề. Thử độ lệch khai báo trước, rồi dò 0..20."""
    units = profile.all_units()
    declared = profile.offset("course-book")

    def hits(k: int) -> int:
        return sum(1 for u in units
                   if 1 <= u.printed_start + k <= len(doc)
                   and pdfutil.red_ratio(doc, u.printed_start + k, profile.banner_top) >= profile.banner_min_red)

    h = hits(declared)
    if h >= 0.8 * len(units):
        return declared
    best = max(range(0, 21), key=hits)
    items.append(ReviewItem(
        id="page-offset:course-book", kind="page-offset", severity="warn", subject="course-book",
        message=(f"Độ lệch khai báo {declared} chỉ khớp {h}/{len(units)} trang đầu unit; "
                 f"độ lệch {best} khớp {hits(best)}/{len(units)}."),
        confidence=round(hits(best) / len(units), 2), proposal={"value": best},
        options=[{"value": declared}, {"value": best}],
        evidence=[{"type": "page", "file": "course-book", "page": units[0].printed_start + best}],
    ))
    return declared


def unit_modules(profile: Profile, doc, unit, decisions: dict, items: list[ReviewItem]) -> dict:
    s, e = profile.pdf_range([unit.printed_start, unit.printed_end])
    want = len(profile.modules)
    banners = banner_pages(profile, doc, s, e)
    rid = f"unit-range:U{unit.no:02d}"
    confidence = 1.0
    starts: list[int]

    if len(banners) == want and banners[0] == s:
        starts = banners
    elif len(banners) > want and banners[0] == s:
        starts = banners[:want]
        extra = banners[want:]
        confidence = 0.8
        items.append(ReviewItem(
            id=rid, kind="unit-range", severity="warn", subject=f"U{unit.no:02d}",
            message=(f"Unit {unit.no} có {len(banners)} băng tiêu đề, nhiều hơn {want} module. "
                     f"Đề xuất gộp trang {extra} vào module cuối ({profile.modules[-1]})."),
            confidence=confidence, proposal={"starts": starts},
            evidence=[{"type": "page", "file": "course-book", "page": p} for p in banners],
        ))
    else:
        fallback = [s + o for o in profile.module_offsets] if profile.module_offsets else []
        starts = fallback
        confidence = 0.6
        items.append(ReviewItem(
            id=rid, kind="unit-range", severity="error" if not fallback else "warn", subject=f"U{unit.no:02d}",
            message=(f"Unit {unit.no}: tìm thấy {len(banners)} băng tiêu đề ở trang {banners}, cần {want}. "
                     + ("Đề xuất dùng bố cục dự phòng module_offsets." if fallback else "Cần nhập trang đầu từng module.")),
            confidence=confidence, proposal={"starts": fallback} if fallback else None,
            evidence=[{"type": "page", "file": "course-book", "page": p} for p in range(s, e + 1)],
        ))

    proposal = next((i.proposal for i in items if i.id == rid), None)
    picked = chosen(decisions, rid, proposal)
    if picked and picked.get("starts"):
        starts, confidence = list(picked["starts"]), 1.0

    mods = {}
    for i, m in enumerate(profile.modules):
        if i >= len(starts):
            break
        end = starts[i + 1] - 1 if i + 1 < len(starts) else e
        mods[m] = [starts[i], max(starts[i], end)]
    return {"pages": [s, e], "printed": [unit.printed_start, unit.printed_end], "title": unit.title,
            "modules": mods, "banners": banners, "confidence": confidence}


def review_parts(profile: Profile, doc, sec) -> dict:
    s, e = profile.pdf_range(sec.review_printed)
    banners = banner_pages(profile, doc, s, e)
    if len(banners) >= 2 and banners[0] == s:
        parts = [[s, banners[1] - 1], [banners[1], e]]
    else:
        mid = s + (e - s + 1) // 2
        parts = [[s, mid - 1], [mid, e]] if e > s else [[s, e], [s, e]]
    return {"pages": [s, e], "printed": sec.review_printed, "parts": parts, "banners": banners}


# --------------------------------------------------------------------------
# Chỉ mục Answer key / Tapescript bằng OCR
# --------------------------------------------------------------------------
def heading_index(ocr: OcrCache, doc, file_id: str, sha: str, first: int, last: int,
                  allow_run: bool) -> dict:
    """Đọc tiêu đề theo thứ tự đọc, trả về khoảng trang cho từng (unit, module) và từng track."""
    heads: list[tuple[int, str]] = []          # (trang, khóa)
    tracks: dict[str, int] = {}
    pages_done, pages_missing = 0, []
    stop = False
    for p in range(first, last + 1):
        lines = ocr.lines(doc, file_id, sha, p, allow_run=allow_run)
        if lines is None:
            pages_missing.append(p)
            continue
        pages_done += 1
        ordered = reading_order(lines)
        for i, line in enumerate(ordered):
            text = line[4].strip()
            if HEAD_STOP.match(text):
                heads.append((p, "STOP"))
                stop = True
                break
            m = HEAD_UNIT.match(text)
            if m:
                u = int(m.group("u"))
                mod = "workbook" if m.group("wb") else module_of(m.group("rest"))
                if mod is None:
                    continue
                heads.append((p, f"{u}:{mod}"))
                if mod == "listening":
                    part = re.match(r"listening\s*(\d)", m.group("rest"), re.I)
                    if part:
                        # bài nằm ở một trong hai dòng ngay sau tiêu đề: "C Now listen…" hoặc "Pronunciation check"
                        for nxt in ordered[i + 1:i + 3]:
                            t = nxt[4].strip()
                            if t.lower().startswith("pronunciation"):
                                tracks.setdefault(f"{u}:{part.group(1)}:pro", p)
                                break
                            em = EXERCISE.match(t)
                            if em:
                                tracks.setdefault(f"{u}:{part.group(1)}:{em.group('ex').lower()}", p)
                                break
                continue
            m = HEAD_REVIEW.match(text)
            if m:
                heads.append((p, f"R{m.group('n')}:review"))
                continue
            m = HEAD_TEST.match(text)
            if m:
                heads.append((p, f"T{m.group('n')}:test"))
        if stop:
            break

    spans: dict[str, list[int]] = {}
    units: dict[str, list[int]] = {}
    for i, (p, key) in enumerate(heads):
        if key == "STOP":
            continue
        end = heads[i + 1][0] if i + 1 < len(heads) else last
        span = spans.setdefault(key, [p, end])
        span[0], span[1] = min(span[0], p), max(span[1], end)
        u = key.split(":")[0]
        us = units.setdefault(u, [p, end])
        us[0], us[1] = min(us[0], p), max(us[1], end)
    return {"pages": [first, last], "index": spans, "units": units, "tracks": tracks,
            "ocrPages": pages_done, "ocrMissing": pages_missing}


def build(profile: Profile, scan: dict, decisions: dict, ocr: OcrCache, allow_ocr: bool = True) -> dict:
    items: list[ReviewItem] = []
    cb = profile.path("course-book")
    doc = pdfutil.open_pdf(str(cb))
    sha = scan["pdfs"]["course-book"]["sha256"]

    check_offset(profile, doc, items)
    rid = "page-offset:course-book"
    picked = chosen(decisions, rid, next((i.proposal for i in items if i.id == rid), None))
    if picked and picked.get("value") is not None:
        profile.files["course-book"]["page_offset"] = int(picked["value"])

    units = {str(u.no): unit_modules(profile, doc, u, decisions, items) for u in profile.all_units()}
    reviews = {str(s.review_no): review_parts(profile, doc, s) for s in profile.sections if s.review_printed}

    out = {"pageOffset": profile.offset("course-book"), "units": units, "reviews": reviews}
    if profile.key_vocab:
        out["keyVocab"] = profile.pdf_range(profile.key_vocab)

    for key, rng in (("answerKey", profile.answer_key), ("tapescript", profile.tapescript)):
        if not rng:
            continue
        a, b = profile.pdf_range(rng)
        idx = heading_index(ocr, doc, "course-book", sha, a, b, allow_ocr)
        out[key] = idx
        if idx["ocrMissing"]:
            items.append(ReviewItem(
                id=f"ocr-missing:{key}", kind="ocr-missing", severity="info", subject=key,
                message=(f"{len(idx['ocrMissing'])} trang {key} chưa OCR (thiếu gói rapidocr-onnxruntime và chưa có "
                         "cache) — trang đáp án/tapescript của từng unit sẽ dùng cả khoảng."),
            ))
        for u in profile.all_units():
            if idx["ocrPages"] and str(u.no) not in idx["units"]:
                items.append(ReviewItem(
                    id=f"{key}-unit:U{u.no:02d}", kind=f"{key}-unit", severity="info", subject=f"U{u.no:02d}",
                    message=f"Không tìm thấy tiêu đề Unit {u.no} trong {key}; dùng cả khoảng {a}–{b}.",
                ))

    ex = profile.listening_extract
    if ex:
        fid = ex["file"]
        edoc = pdfutil.open_pdf(str(profile.path(fid)))
        pages = {}
        for u in profile.all_units():
            p0 = ex["first_unit_page"] + (u.no - 1) * ex["pages_per_unit"]
            rng = [p0, p0 + ex["pages_per_unit"] - 1]
            pages[str(u.no)] = rng
            if rng[1] > len(edoc) or pdfutil.red_ratio(edoc, p0, profile.banner_top) < profile.banner_min_red:
                items.append(ReviewItem(
                    id=f"extract-page:U{u.no:02d}", kind="extract-page", severity="warn", subject=f"U{u.no:02d}",
                    message=f"Trang {p0} của {fid} không có băng tiêu đề Listening như kỳ vọng cho Unit {u.no}.",
                    confidence=0.5, proposal={"pages": rng},
                    evidence=[{"type": "page", "file": fid, "page": p0}],
                ))
        out["extract"] = {"file": fid, "units": pages,
                          "answerKey": ex.get("answer_key"), "tapescript": ex.get("tapescript")}

    out["review"] = [i.model_dump(exclude_none=True) for i in items]
    return out
