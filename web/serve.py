#!/usr/bin/env python3
"""Máy chủ tĩnh để chạy thử bản tự host trên máy, có hỗ trợ HTTP Range.

PDF.js chỉ tải những khoảng byte chứa trang đang xem khi máy chủ trả lời Range — với cuốn
sách 100 MB, đó là khác biệt giữa vài trăm KB và cả 100 MB. `python3 -m http.server` không
hỗ trợ Range, nên dùng file này:

    python3 web/serve.py            # rồi mở http://localhost:8000/web/index.html

GitHub Pages, Cloudflare Pages, Netlify đều hỗ trợ Range sẵn.
"""
from __future__ import annotations

import argparse
import os
import re
from functools import partial
from http import HTTPStatus
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

RANGE = re.compile(r"bytes=(\d*)-(\d*)$")


class RangeHandler(SimpleHTTPRequestHandler):
    def send_head(self):
        m = RANGE.match(self.headers.get("Range", "").strip())
        path = self.translate_path(self.path)
        if not m or os.path.isdir(path) or not os.path.isfile(path):
            return super().send_head()
        size = os.path.getsize(path)
        a, b = m.groups()
        if a == "":                       # bytes=-N: N byte cuối
            start, end = max(0, size - int(b or 0)), size - 1
        else:
            start, end = int(a), min(int(b) if b else size - 1, size - 1)
        if start > end or start >= size:
            self.send_response(HTTPStatus.REQUESTED_RANGE_NOT_SATISFIABLE)
            self.send_header("Content-Range", f"bytes */{size}")
            self.end_headers()
            return None
        f = open(path, "rb")
        f.seek(start)
        self.send_response(HTTPStatus.PARTIAL_CONTENT)
        self.send_header("Content-Type", self.guess_type(path))
        self.send_header("Content-Range", f"bytes {start}-{end}/{size}")
        self.send_header("Content-Length", str(end - start + 1))
        self.send_header("Accept-Ranges", "bytes")
        self.end_headers()
        self._remaining = end - start + 1
        return f

    def end_headers(self):
        self.send_header("Accept-Ranges", "bytes")
        super().end_headers()

    def copyfile(self, source, outputfile):
        left = getattr(self, "_remaining", None)
        if left is None:
            return super().copyfile(source, outputfile)
        while left > 0:
            chunk = source.read(min(1 << 16, left))
            if not chunk:
                break
            outputfile.write(chunk)
            left -= len(chunk)
        self._remaining = None


RangeHandler.extensions_map = {**SimpleHTTPRequestHandler.extensions_map,
                               ".mjs": "text/javascript", ".mp3": "audio/mpeg", ".json": "application/json"}


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--port", type=int, default=8000)
    ap.add_argument("--root", type=Path, default=Path(__file__).resolve().parent.parent)
    a = ap.parse_args()
    handler = partial(RangeHandler, directory=str(a.root))
    with ThreadingHTTPServer(("127.0.0.1", a.port), handler) as httpd:
        print(f"Đang phục vụ {a.root} tại http://localhost:{a.port}/web/index.html (Ctrl+C để dừng)")
        httpd.serve_forever()


if __name__ == "__main__":
    main()
