"""The one-page summary is generated, so it can be checked like anything else.

A public graphic has two properties worth testing, and neither is aesthetic.

**It must not contain a number typed by a person.** The values, the interval, the
best baseline, the verdicts and the row order are read from
``docs/published-run/``; the prose is fixed. That is finding F29 applied to
marketing material: a hand-made post is a number written into a second place, and
the place nobody re-checks. The test renders the page data and compares it to the
tables.

**It must carry the words the policy requires.** Protocol SS14.2 and E3 SS4 say
what has to accompany a quoted number -- the exploratory status, the cost level,
the fact that the metric is excess, the interval -- and the useful time to check
that is not the moment of posting. The requirement is a module constant here and a
string assertion below, so the two cannot drift apart.

A third check is quieter and is the one that actually bit during development: the
page has to *fit on one page*. ``draw`` returns how far down the sheet it reached.
"""

from __future__ import annotations

import sys
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO_ROOT / "scripts"))

import make_onepager as onepager  # noqa: E402

PUBLISHED = REPO_ROOT / "docs" / "published-run"


# --------------------------------------------------------------------------- #
# The numbers come from the tables
# --------------------------------------------------------------------------- #

def test_every_point_estimate_on_the_page_is_the_published_one() -> None:
    """The page is drawn from the published table, not from the prose."""
    data = onepager.load(PUBLISHED)

    drawn = {row["method"]: round(row["point"], 4) for row in data["rows"]}
    assert drawn == {
        "B1": 0.5482, "B2": 0.4519, "B3": 0.7896, "B4": 0.1820, "B5": 0.7843,
        "M1": 0.7860, "M2": 0.8538,
    }


def test_the_interval_and_the_reference_baseline_are_read_too() -> None:
    """The bar and the dashed reference line are the published ones.

    These are the two things a graphic is most likely to get subtly wrong by hand:
    an interval quoted from the wrong cost level, and a baseline chosen because it
    makes the candidates look good.
    """
    data = onepager.load(PUBLISHED)

    best = next(row for row in data["rows"] if row["method"] == data["best_baseline"])
    assert data["best_baseline"] == "B3", "the rule's baseline, read from decisions.csv"
    assert best["low"] == pytest.approx(0.3311, abs=5e-5)
    assert best["high"] == pytest.approx(1.3176, abs=5e-5)
    assert best["level"] == pytest.approx(0.90, abs=1e-9)


def test_the_verdicts_on_the_page_are_the_published_ones() -> None:
    """The page prints what the decision rule returned, including the failure."""
    data = onepager.load(PUBLISHED)

    verdicts = {c["method"]: c["verdict"] for c in data["candidates"]}
    assert verdicts == {"M1": "FAILURE", "M2": "FAILURE"}


def test_the_page_requires_the_headline_cost_it_says_it_uses() -> None:
    """A guard for the one value the page hard-codes in two places.

    The eyebrow and the axis both say 10 bps. If a run is ever published at another
    headline cost, ``load`` must refuse rather than mislabel the axis.
    """
    import pandas as pd
    import tempfile

    with tempfile.TemporaryDirectory() as tmp:
        folder = Path(tmp)
        for name in ("outcomes.csv", "decisions.csv"):
            (folder / name).write_bytes((PUBLISHED / name).read_bytes())
        outcomes = pd.read_csv(folder / "outcomes.csv", index_col=0)
        outcomes["headline_cost_bps"] = 25
        outcomes.to_csv(folder / "outcomes.csv")

        with pytest.raises(ValueError, match="25 bps"):
            onepager.load(folder)


# --------------------------------------------------------------------------- #
# The words the policy requires are on it
# --------------------------------------------------------------------------- #

def test_the_page_uses_the_policy_fixed_phrasing_verbatim() -> None:
    """E3 SS3 fixes the words, so the page may not paraphrase them.

    "Pre-registered" alone is a different claim from "pre-registered, mechanically
    evaluated, non-confirmatory": the second names the mechanism and the status, and
    it is the second that the frozen policy requires a public artefact to use.
    """
    assert onepager.FIXED_PUBLIC_PHRASING.upper() in onepager.EYEBROW


def test_the_disclosure_carries_every_phrase_the_policy_requires() -> None:
    """E3 SS4 operationalised as a string check on the sentence that ships.

    Losing one of these in an edit would be invisible: the page would still render
    and still look right.
    """
    text = onepager.disclosure(onepager.load(PUBLISHED)).lower()

    missing = [p for p in onepager.REQUIRED_DISCLOSURE_PHRASES if p.lower() not in text]
    assert missing == [], f"the disclosure lost: {missing}"


def test_the_failure_is_described_as_untested_rather_than_falsified() -> None:
    """The distinction the whole project rests on, on the one page that summarises it.

    The registered test never ran in confirmatory mode, so the hypothesis was not
    rejected -- it was not tested. A summary that says "falsified" would be a
    stronger claim than the run supports, in the direction that flatters the work.
    """
    assert "untested, not falsified" in onepager.FAILURE_TEXT
    assert "falsified" not in onepager.DECK.lower()


def test_every_borrowed_fact_is_still_in_the_file_that_owns_it() -> None:
    """The page cannot outlive the claim it quotes.

    A few facts here are not in the published tables -- the engine certificate, the
    two reproduction failures -- because no table carries them. They are declared
    with their source, and this is the check. Case-insensitive because the page
    shouts its eyebrow and the README does not.
    """
    problems = []
    for literal, owner in onepager.BORROWED_FACTS:
        body = (REPO_ROOT / owner).read_text(encoding="utf-8").lower()
        if literal.lower() not in body:
            problems.append(f"{literal!r} is no longer in {owner}")
    assert problems == []


# --------------------------------------------------------------------------- #
# It is one page
# --------------------------------------------------------------------------- #

def test_the_page_fits_on_one_sheet(tmp_path: Path) -> None:
    """Overflow is silent: the last block is simply cut off.

    ``draw`` returns the bottom of the last block as a fraction of the sheet, which
    is what makes "one page" a number instead of a look.
    """
    _, bottom = onepager.draw(onepager.load(PUBLISHED), tmp_path / "page")

    assert bottom < 0.995, (
        f"the page reaches {bottom:.3f} of the sheet and the last block is clipped"
    )


def test_no_block_crosses_the_page_margin() -> None:
    """A wrapped line that overruns the margin is invisible until it is printed.

    ``textwrap`` counts characters and characters vary in width, so the wrap width
    that fits one paragraph is a few pixels too wide for the next. The rendered
    extent is the only honest measure, and it is the renderer's job, not the eye's.
    """
    import matplotlib.pyplot as plt

    fig, _ = onepager.layout_page(onepager.load(PUBLISHED))
    try:
        breaches = onepager.margin_breaches(fig)
    finally:
        plt.close(fig)

    assert breaches == [], "text crosses the page margin: " + "; ".join(breaches)


def test_the_margin_check_can_see_a_breach() -> None:
    """A check that cannot fail is not a check, so pin the positive control.

    Without this, the test above would also pass if ``margin_breaches`` returned an
    empty list for some uninteresting reason -- an empty figure, a bad transform --
    and the page could overflow for a year without anyone hearing about it.
    """
    import matplotlib.pyplot as plt

    fig, _ = onepager.layout_page(onepager.load(PUBLISHED))
    try:
        assert onepager.margin_breaches(fig) == [], "the page itself is clean"
        fig.text(
            onepager.MARGIN_X, 0.5, "x" * 400,
            fontsize=8.0, fontfamily=onepager.FONT,
        )
        breaches = onepager.margin_breaches(fig)
    finally:
        plt.close(fig)

    assert len(breaches) == 1, f"the control line was not detected: {breaches}"
    assert "xxx" in breaches[0]
