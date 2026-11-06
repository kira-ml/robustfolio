"""The research brief is a public PDF; check it still renders the key numbers.

The working paper, one-pager, and carousel have their own tests. The brief was
the remaining generated-looking document without one. This is a content check,
not a proof that every sentence is correct: it fails if the PDF stops containing
the values a reader is invited to quote.
"""

from __future__ import annotations

from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "essays" / "brief.typ"
COMMITTED = ROOT / "essays" / "robustfolio-research-brief.pdf"


@pytest.fixture(scope="module")
def built(tmp_path_factory):
    typst = pytest.importorskip("typst", reason="the paper extra is not installed")
    pypdf = pytest.importorskip("pypdf", reason="the paper extra is not installed")
    out = tmp_path_factory.mktemp("brief") / "brief.pdf"
    typst.compile(str(SOURCE), output=str(out), root=str(ROOT))
    return out, pypdf


def _text(path: Path, pypdf) -> str:
    return "\n".join(page.extract_text() or "" for page in pypdf.PdfReader(str(path)).pages)


def test_the_brief_is_two_pages(built):
    out, pypdf = built
    assert len(pypdf.PdfReader(str(out)).pages) == 2


def test_the_brief_carries_the_headline_numbers(built):
    out, pypdf = built
    text = _text(out, pypdf)
    for value in ("0.3527", "0.3193", "0.2710", "+0.064", "0.147", "0.20"):
        assert value in text, f"{value!r} is missing from the rendered brief"


def test_the_committed_brief_exists() -> None:
    assert COMMITTED.exists() and COMMITTED.stat().st_size > 0
