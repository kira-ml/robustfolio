"""The LinkedIn carousel is generated from the paired-inference JSON, not typed.

It gets the same treatment as the one-pager and the paper:

1. it must be the right shape — eight slides, the format a LinkedIn document
   post expects;
2. every headline number must be present in the rendered PDF;
3. the source must not contain a measurement that should have come from
   ``paper/generated/paired.typ``;
4. the committed PDF must not silently lag the source.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

import pandas as pd
import pytest

REPO_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO_ROOT / "scripts"))

import build_paper  # noqa: E402

COMMITTED = REPO_ROOT / "essays" / "robustfolio-carousel.pdf"
SOURCE = REPO_ROOT / "paper" / "carousel.typ"


@pytest.fixture(scope="module")
def built(tmp_path_factory):
    pytest.importorskip("typst", reason="the paper extra is not installed")
    pypdf = pytest.importorskip("pypdf", reason="the paper extra is not installed")
    out = tmp_path_factory.mktemp("carousel") / "carousel.pdf"
    build_paper.build_carousel(out)
    return out, pypdf


def _text(path: Path, pypdf) -> str:
    return "\n".join(page.extract_text() or "" for page in pypdf.PdfReader(str(path)).pages)


def test_it_has_eight_slides(built):
    out, pypdf = built
    assert len(pypdf.PdfReader(str(out)).pages) == 8


def test_every_headline_number_is_in_the_pdf(built):
    out, pypdf = built
    text = _text(out, pypdf)
    for value in (
        "0.8538", "0.72", "0.917", "0.147", "0.064", "0.587",
        "0.3527", "0.3193", "0.2710",
    ):
        assert value in text, f"{value!r} is missing from the rendered carousel"


def test_the_reading_is_stated(built):
    out, pypdf = built
    text = " ".join(_text(out, pypdf).split()).replace("\u2019", "'")
    for phrase in (
        "My own test rejected my best method",
        "It couldn't see a win that size",
        "What this is",
        "Portfolio construction is an estimation problem",
        "A portfolio is a set of assumptions",
        "A benchmark, not a backtest",
        "First on the metric",
        "The bar was",
        "A test can be rigorous and still answer the wrong question",
        "The same data, the right test",
        "NOT MATERIAL",
        "paired resampling test",
        "A new market. A different winner",
        "The benchmark lesson replicated",
        "The benchmark is the binding constraint",
        "equal weight beat both treatments",
    ):
        assert phrase in text, f"{phrase!r} is missing from the rendered carousel"


def test_source_does_not_type_the_headline_measurements():
    source = SOURCE.read_text(encoding="utf-8")
    for value in ("0.8538", "0.917", "0.147", "0.0642", "0.587"):
        assert value not in source, (
            f"{value!r} is typed into paper/carousel.typ; it should come from "
            "paper/generated/paired.typ"
        )


def test_committed_pdf_is_the_same_length(built):
    if not COMMITTED.exists():
        pytest.skip("no committed carousel; scripts/build_paper.py has not been run")
    out, pypdf = built
    assert len(pypdf.PdfReader(str(COMMITTED)).pages) == len(pypdf.PdfReader(str(out)).pages)


def test_cap_sweep_reproduces_the_frozen_arm():
    """The 0.30 arm must be the published B3/M1/M2 run, or the sweep is not comparable."""
    records = json.loads(
        (REPO_ROOT / "docs" / "published-run" / "cap_sweep.json").read_text(encoding="utf-8")
    )
    by_key = {
        (row["w_max"], row["method"]): row
        for row in records
        if row["status"] == "ok"
    }
    outcomes = pd.read_csv(
        REPO_ROOT / "docs" / "published-run" / "outcomes.csv", index_col=0
    )
    for method in ("B3", "M1", "M2"):
        got = by_key[(0.30, method)]["net_sharpe"]
        want = float(outcomes.loc[method, "net_sharpe"])
        assert abs(got - want) < 1e-9


def test_cap_sweep_typ_names_the_incomplete_arm():
    records = json.loads(
        (REPO_ROOT / "docs" / "published-run" / "cap_sweep.json").read_text(encoding="utf-8")
    )
    text = build_paper.cap_sweep_module(records)
    assert "m1:" in text
    assert "m2:" in text
    assert "b5-incomplete: (0.4, 1.0)" in text
