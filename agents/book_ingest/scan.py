"""Bước 1 — quét kho file: số trang, lớp chữ, sha256, file trùng, thông tin audio."""
from __future__ import annotations

import json
import shutil
import subprocess
from pathlib import Path
from typing import Optional

from . import pdfutil
from .profile import Profile

WATERMARKS = ("www.frenglish.ru", "hocdedang.com | IELTS materials")
AUDIO_EXT = {".mp3", ".m4a", ".wav", ".ogg"}


def audio_duration(path: Path) -> Optional[float]:
    try:
        from mutagen import File as MFile  # type: ignore
        m = MFile(str(path))
        if m is not None and getattr(m, "info", None) and getattr(m.info, "length", None):
            return round(float(m.info.length), 2)
    except Exception:
        pass
    if shutil.which("ffprobe"):
        try:
            out = subprocess.run(
                ["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", str(path)],
                capture_output=True, text=True, timeout=30)
            return round(float(out.stdout.strip()), 2)
        except Exception:
            return None
    return None


def scan(profile: Profile) -> dict:
    root = profile.root
    pdfs: dict[str, dict] = {}
    for fid in profile.pdf_ids():
        p = profile.path(fid)
        if not p.exists():
            raise FileNotFoundError(f"Thiếu file {p} (files.{fid}.path trong book.yaml)")
        doc = pdfutil.open_pdf(str(p))
        n = len(doc)
        sample = range(1, n + 1, max(1, n // 40))
        with_text = sum(1 for i in sample if pdfutil.text_chars(doc, i, WATERMARKS) > 200)
        pdfs[fid] = {
            "path": p.relative_to(root).as_posix(),
            "pages": n,
            "bytes": p.stat().st_size,
            "sha256": pdfutil.sha256_file(p),
            "textLayerRatio": round(with_text / len(sample), 2),
        }

    audio: list[dict] = []
    for fid, spec in profile.files.items():
        if spec.get("kind") != "audio":
            continue
        d = profile.path(fid)
        if not d.is_dir():
            raise FileNotFoundError(f"Thiếu thư mục audio {d}")
        for f in sorted(d.iterdir()):
            if f.suffix.lower() not in AUDIO_EXT:
                continue
            audio.append({
                "group": fid,
                "path": f.relative_to(root).as_posix(),
                "name": f.name,
                "bytes": f.stat().st_size,
                "sha256": pdfutil.sha256_file(f),
                "durationSec": audio_duration(f),
            })

    seen: dict[str, str] = {}
    dups = []
    for a in audio:
        if a["sha256"] in seen:
            dups.append([seen[a["sha256"]], a["path"]])
        else:
            seen[a["sha256"]] = a["path"]

    known = {v["path"] for v in pdfs.values()} | {a["path"] for a in audio}
    other = sorted(
        p.relative_to(root).as_posix() for p in root.rglob("*")
        if p.is_file() and p.relative_to(root).parts[0] not in ("work", "web")   # đầu ra của agent
        and p.name not in ("book.yaml", "book.draft.yaml", "book.json", "plan.json", "report.md", ".DS_Store")
        and p.relative_to(root).as_posix() not in known
    )
    return {"pdfs": pdfs, "audio": audio, "duplicates": dups, "other": other}


def inventory(root: Path) -> str:
    """Danh sách file để gửi khi cần gỡ lỗi — không in nội dung sách."""
    rows = []
    for p in sorted(Path(root).rglob("*")):
        if not p.is_file() or p.name == ".DS_Store":
            continue
        rel = p.relative_to(root).as_posix()
        size = p.stat().st_size
        extra = ""
        if p.suffix.lower() == ".pdf":
            doc = pdfutil.open_pdf(str(p))
            n = len(doc)
            sample = range(1, n + 1, max(1, n // 40))
            ratio = sum(1 for i in sample if pdfutil.text_chars(doc, i, WATERMARKS) > 200) / len(sample)
            extra = f"pdf {n} trang, lớp chữ {ratio:.0%}"
        elif p.suffix.lower() in AUDIO_EXT:
            d = audio_duration(p)
            extra = f"audio {d:.1f}s" if d else "audio"
        rows.append(f"{rel}\t{size:,} B\t{extra}")
    return "\n".join(rows)


def write(work: Path, data: dict) -> Path:
    work.mkdir(parents=True, exist_ok=True)
    out = work / "scan.json"
    out.write_text(json.dumps(data, ensure_ascii=False, indent=1), encoding="utf-8")
    return out
