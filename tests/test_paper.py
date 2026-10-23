"""The working paper is a rendering of the published tables, not a second source.

Three things can go wrong with a document like this, and each gets a test:

* **The argument drifts from the measurements.** ``paper/paper.typ`` must not
  contain a single number it quotes; every one is interpolated from
  ``paper/generated/numbers.typ``, which this module regenerates from
  ``docs/published-run/`` before rendering. A typed figure in the prose would be
  a second source of truth for the same quantity, and the two would eventually
  disagree.
* **The document drifts from the artefacts.** The rendered PDF is checked
  against the tables it claims to quote, so a stale build cannot pass.
* **The document claims more than the run supports.** The phrases the claims
  policy forbids are checked for absence, and "absolute return" is allowed only
  where it is being denied.

The PDF is built here rather than read from ``essays/`` so the test covers the
source that produces the committed file. Typst and pypdf are the optional
``paper`` extra; without them every test in this module skips with the reason.
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

PAPER_DIR = ROOT / "paper"
PUBLISHED = ROOT / "docs" / "published-run"
COMMITTED_PDF = ROOT / "essays" / "robustfolio-working-paper.pdf"

#: U+2212, which is what ``fmt`` emits and what any interval will contain.
MINUS = "\u2212"


def _number(value: float, digits: int) -> str:
    """The string ``fmt`` in ``paper.typ`` produces, minus the typography."""
    text = f"{round(float(value), digits):.{digits}f}"
    return text.replace("-", MINUS)


def _pct(value: float, digits: int) -> str:
    return _number(float(value) * 100, digits) + "%"


def _interval(low: float, high: float) -> str:
    return f"[{_number(low, 3)}, {_number(high, 3)}]"


def _normalise(text: str) -> str:
    """Line breaks and Typst's non-breaking spaces are layout, not content.

    Hyphenation puts a break after a real hyphen (``non-`` / ``confirmatory``),
    which reads as a space once the lines are joined; a phrase check would then
    fail on a document that is correct.
    """
    joined = re.sub(r"\s+", " ", text.replace("\u00a0", " "))
    return re.sub(r"(?<=[A-Za-z])- (?=[A-Za-z])", "-", joined)


@pytest.fixture(scope="module")
def paper(tmp_path_factory):
    pytest.importorskip(
        "typst", reason="the paper extra is not installed: pip install -e .[paper]"
    )
    pypdf = pytest.importorskip(
        "pypdf", reason="the paper extra is not installed: pip install -e .[paper]"
    )
    import build_paper
    import make_onepager as page

    out = tmp_path_factory.mktemp("paper") / "working-paper.pdf"
    build_paper.build(out)

    reader = pypdf.PdfReader(str(out))
    pages = [page_text.extract_text() or "" for page_text in reader.pages]
    outcomes = page._read_table(PUBLISHED / "outcomes.csv")
    decisions = page._read_table(PUBLISHED / "decisions.csv")

    return {
        "path": out,
        "reader": reader,
        "pages": pages,
        "text": _normalise(" ".join(pages)),
        "outcomes": outcomes,
        "decisions": decisions,
        "best": str(decisions["baseline"].iloc[0]),
    }


# --------------------------------------------------------------------------- #
# Shape of the artefact
# --------------------------------------------------------------------------- #

def test_is_an_a4_working_paper(paper):
    for number, page in enumerate(paper["reader"].pages, start=1):
        box = page.mediabox
        assert abs(float(box.width) - 595.276) < 1.0, f"page {number} is not A4 wide"
        assert abs(float(box.height) - 841.890) < 1.0, f"page {number} is not A4 tall"


def test_length_is_a_paper_not_a_pamphlet(paper):
    # 8 pages of argument plus a references page. The bound is wide on purpose:
    # it catches a build that lost a section or a runaway table, not edit drift.
    assert 8 <= len(paper["pages"]) <= 12


# --------------------------------------------------------------------------- #
# What the document may and may not say
# --------------------------------------------------------------------------- #

def test_title_and_the_fixed_status_phrasing(paper):
    text = paper["text"]
    assert "The benchmark is the binding constraint" in text
    assert "EXPLORATORY AND NON-CONFIRMATORY" in text
    # The public description, quoted from docs/results_reporting_and_claims_policy.md.
    assert "pre-registered, mechanically evaluated, non-confirmatory" in text
    # The distinction the paper exists to make: a null that was not tested is not
    # a null that was established.
    assert "untested, not falsified" in text


def test_the_disclosures_are_present(paper):
    text = paper["text"]
    assert "no absolute return claim" in text
    assert "net excess sharpe" in text.lower()
    assert "does not" in text  # a paper that says nothing about its limits is suspect


def test_no_prohibited_claim(paper):
    text = paper["text"].lower()
    for phrase in (
        "beats the market",
        "outperform the market",
        "guaranteed",
        "risk-free profit",
        "gross sharpe",
        "in-sample sharpe",
        "statistically significant" ,
    ):
        assert phrase not in text, f"the paper claims {phrase!r}"

    # "Absolute return" may appear only where it is denied.
    for match in re.finditer("absolute return", text):
        assert text[max(0, match.start() - 3) : match.start()] == "no ", (
            "absolute return is mentioned without being denied"
        )


# --------------------------------------------------------------------------- #
# The numbers come from the tables, and only from the tables
# --------------------------------------------------------------------------- #

def _table_strings(paper) -> list[str]:
    """Every measurement the tables contain, in the form the paper prints it."""
    outcomes, decisions, best = paper["outcomes"], paper["decisions"], paper["best"]
    strings: list[str] = []

    for method in outcomes.index:
        strings.append(_number(outcomes.loc[method, "net_sharpe"], 4))
        strings.append(
            _interval(
                outcomes.loc[method, "net_sharpe_ci_low"],
                outcomes.loc[method, "net_sharpe_ci_high"],
            )
        )
        strings.append(_number(outcomes.loc[method, "turnover_annualized"], 2))
        strings.append(_pct(outcomes.loc[method, "max_drawdown"], 1))
        for cost in (0, 5, 10, 20, 50):
            strings.append(_number(outcomes.loc[method, f"net_sharpe_{cost}bps"], 4))

    for method in decisions.index:
        strings.append(_number(decisions.loc[method, "psr"], 3))
        strings.append(_number(decisions.loc[method, "dsr_pvalue"], 4))
        strings.append(_number(decisions.loc[method, "sharpe_gap"], 3))
        strings.append(_pct(decisions.loc[method, "max_fold_share"], 1))

    strings.append(_number(outcomes.loc[best, "net_sharpe"], 4))
    return strings


def test_every_table_value_is_in_the_rendered_pdf(paper):
    text = paper["text"]
    missing = [value for value in _table_strings(paper) if value not in text]
    assert not missing, f"the PDF does not print {missing}"


def test_the_prose_contains_no_measurements(paper):
    """A number typed into ``paper.typ`` would be a second source of truth."""
    source = (PAPER_DIR / "paper.typ").read_text(encoding="utf-8")
    typed = [value for value in _table_strings(paper) if len(value) >= 5 and value in source]
    assert not typed, f"paper.typ types measurements it should interpolate: {typed}"


def test_the_paper_reads_its_numbers_from_the_generator():
    source = (PAPER_DIR / "paper.typ").read_text(encoding="utf-8")
    assert '#import "generated/numbers.typ"' in source


def test_sourced_facts_are_in_the_file_that_owns_them():
    """Design diagnostics are quoted from prose notes, so pin them to the note.

    This is a provenance check, not a proof: it establishes that the figure is
    in the file the generator says owns it, so a reworded note or a changed
    estimate fails the build instead of silently diverging from the paper.
    """
    import build_paper

    numbers = re.compile(r"\d+(?:\.\d+)?")
    for name, value, owner in build_paper.SOURCED_FACTS:
        owner_text = (ROOT / owner).read_text(encoding="utf-8")
        if isinstance(value, str):
            assert value in owner_text, f"{name}={value!r} is not in {owner}"
        else:
            literal = f"{value:g}"
            tokens = set(numbers.findall(owner_text))
            assert literal in tokens, f"{name}={literal} is not in {owner}"


# --------------------------------------------------------------------------- #
# What the tables themselves have to show for the paper's claim to hold
# --------------------------------------------------------------------------- #

def test_every_interval_overlaps_the_baseline(paper):
    """The paper's central reading: the ranking is a ranking of estimates."""
    outcomes, best = paper["outcomes"], paper["best"]
    low_best = float(outcomes.loc[best, "net_sharpe_ci_low"])
    high_best = float(outcomes.loc[best, "net_sharpe_ci_high"])
    for method in outcomes.index:
        low = float(outcomes.loc[method, "net_sharpe_ci_low"])
        high = float(outcomes.loc[method, "net_sharpe_ci_high"])
        assert low <= high_best and high >= low_best, (
            f"{method}'s interval is disjoint from {best}'s, so the paper's "
            "statement that every interval overlaps the baseline is false"
        )


def test_the_null_is_a_null(paper):
    """Neither treatment clears the materiality bar, and both fail the rule."""
    decisions = paper["decisions"]
    bar = float(decisions["sharpe_gap_threshold"].iloc[0])
    assert all(float(gap) < bar for gap in decisions["sharpe_gap"]), (
        "a treatment now clears the materiality bar; the paper's argument "
        "no longer describes this run"
    )
    assert set(decisions["verdict"]) == {"FAILURE"}


def test_the_committed_pdf_matches_the_source(paper):
    """The file in ``essays/`` is what a reader downloads; it must not be stale."""
    if not COMMITTED_PDF.exists():
        pytest.skip("no committed PDF; scripts/build_paper.py has not been run")
    pypdf = pytest.importorskip("pypdf")
    committed = len(pypdf.PdfReader(str(COMMITTED_PDF)).pages)
    assert committed == len(paper["pages"]), (
        "essays/robustfolio-working-paper.pdf has "
        f"{committed} pages; the source builds {len(paper['pages'])}. Rebuild it."
    )
