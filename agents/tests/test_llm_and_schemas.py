import json
from pathlib import Path
from types import SimpleNamespace

import pytest
import yaml

from book_ingest import cli, llm
from book_ingest.schemas import TocDraft, TocSection, TocUnit

REPO = Path(__file__).resolve().parents[2]


class FakeMessages:
    def __init__(self, parsed, stop_reason="end_turn"):
        self.parsed, self.stop_reason, self.calls = parsed, stop_reason, []

    def parse(self, **kw):
        self.calls.append(kw)
        return SimpleNamespace(parsed_output=self.parsed, stop_reason=self.stop_reason)


def toc():
    return TocDraft(title="Fake Book", sections=[
        TocSection(id="S1", title="Section 1", units=[TocUnit(no=1, title="One", printed_start=3)],
                   review_no=1, review_printed_start=15)],
        answer_key_printed=[20, 21])


def test_api_mode_uses_structured_output(fake_book):
    msgs = FakeMessages(toc())
    out = llm.api(fake_book / "course.pdf", [4], client=SimpleNamespace(messages=msgs), model="test-model")
    assert out.sections[0].units[0].printed_start == 3
    call = msgs.calls[0]
    assert call["output_format"] is TocDraft and call["model"] == "test-model"
    assert call["messages"][0]["content"][0]["type"] == "image"

    draft = yaml.safe_load(llm.draft_yaml(out, {"course-book": {"kind": "pdf", "path": "course.pdf"}}, "fake"))
    assert draft["toc"]["sections"][0]["units"] == [[1, "One", 3]]
    assert draft["toc"]["sections"][0]["review"] == [1, 15]


def test_api_mode_refusal(fake_book):
    msgs = FakeMessages(None, stop_reason="refusal")
    with pytest.raises(RuntimeError, match="manual"):
        llm.api(fake_book / "course.pdf", [4], client=SimpleNamespace(messages=msgs))


def test_manual_mode_renders_pages(fake_book):
    guide = llm.manual(fake_book / "course.pdf", [1, 2], fake_book / "work")
    assert guide.exists() and (guide.parent / "page-001.png").exists()


def test_exported_schemas_are_current(tmp_path):
    for p in cli.export_schemas(tmp_path):
        committed = REPO / "schemas" / p.name
        assert committed.exists(), f"chạy `python -m book_ingest schemas` để tạo {committed}"
        assert json.loads(committed.read_text()) == json.loads(p.read_text()), f"{committed} đã cũ"
