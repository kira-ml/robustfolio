"""The social cards are generated too, so they get the same treatment as the page.

Three things are worth testing about an image whose only job is to be glanced at.

**It must be the shape its destination asks for.** A 4:5 file is what a feed shows
without cropping; a 2:1 file is what a link preview draws. Those are pixels in the
delivered file, not inches in a variable, so the test reads the PNG header.

**It must not state a number the page does not.** Both cards read the published
tables through ``make_onepager.load``. The positive control below changes a value in
memory and requires the card to change with it -- a card that silently ignored the
table would pass every string assertion that quotes today's numbers.

**It must carry the fixed public phrasing.** A post is a public artefact under E3
SS4, so the status token and the cost level travel with the image, not only with the
text beside it.

There is also a geometry check, because both cards are hand-placed: text that runs
past the margin, or down into the footer, is the failure mode that a rendered image
shows and a string assertion cannot.
"""

from __future__ import annotations

import struct
import sys
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO_ROOT / "scripts"))

import make_cards as cards  # noqa: E402
import make_onepager as page  # noqa: E402

PUBLISHED = REPO_ROOT / "docs" / "published-run"

FOOTER_STRINGS = (page.EYEBROW, "github.com/kira-ml/robustfolio    |    generated from docs/published-run/")


def _load() -> dict:
    return page.load(PUBLISHED)


def _texts(fig) -> str:
    return "\n".join(text.get_text() for text in fig.texts)


def _png_size(path: Path) -> tuple[int, int]:
    """Width and height from the PNG header, which is what a reader downloads."""
    head = path.read_bytes()[:24]
    assert head[:8] == b"\x89PNG\r\n\x1a\n", "not a PNG"
    width, height = struct.unpack(">II", head[16:24])
    return width, height


# --------------------------------------------------------------------------- #
# The shapes
# --------------------------------------------------------------------------- #

def test_the_social_card_is_four_by_five(tmp_path: Path) -> None:
    """1200x1500: the tallest shape a feed shows without cropping it."""
    written = cards.draw(_load(), tmp_path / "one-pager")
    social = next(p for p in written if p.name.endswith("-social.png"))

    assert _png_size(social) == cards.SOCIAL_PIXELS


def test_the_link_card_is_two_by_one(tmp_path: Path) -> None:
    """1280x640: the size GitHub asks for a social preview."""
    written = cards.draw(_load(), tmp_path / "one-pager")
    card = next(p for p in written if p.name.endswith("-card.png"))

    assert _png_size(card) == cards.CARD_PIXELS


# --------------------------------------------------------------------------- #
# The numbers come from the tables
# --------------------------------------------------------------------------- #

def test_the_headline_figure_is_the_published_gap_and_bar() -> None:
    """The one number the cards are built around is read, not typed."""
    facts = cards.facts(_load())

    assert facts["method"] == "M2"
    assert facts["baseline"] == "B3"
    assert facts["gap"] == pytest.approx(0.06422945637394395, abs=1e-15)
    assert facts["bar"] == pytest.approx(0.20, abs=1e-15)
    assert facts["verdict"] == "FAILURE"
    assert facts["bps"] == 10


def test_the_gap_on_the_card_follows_the_table() -> None:
    """Positive control: change the table in memory and the card must change too.

    This is the F29 guard. A card that hard-coded ``+0.064`` would satisfy every
    assertion about today's numbers and still be wrong after the next run.
    """
    data = _load()
    for decision in data["candidates"]:
        decision["gap"] = 0.111

    fig, _ = cards.layout_social(data)
    assert "+0.111" in _texts(fig)
    assert "+0.064" not in _texts(fig)


def test_the_verdict_on_the_card_is_the_published_verdict() -> None:
    data = _load()
    fig, _ = cards.layout_social(data)

    for decision in data["candidates"]:
        assert decision["verdict"] in _texts(fig)


# --------------------------------------------------------------------------- #
# The words the policy requires
# --------------------------------------------------------------------------- #

@pytest.mark.parametrize("layout", [cards.layout_social, cards.layout_card])
def test_each_card_carries_the_fixed_public_phrasing(layout) -> None:
    """E3 SS3 fixes the phrase and SS4 makes the post, not just the page, an artefact."""
    fig, _ = layout(_load())
    body = _texts(fig)

    assert page.EYEBROW in body
    assert "PRE-REGISTERED, MECHANICALLY EVALUATED, NON-CONFIRMATORY" in body
    assert "NET OF 10 bps ONE-WAY COSTS" in body


@pytest.mark.parametrize("layout", [cards.layout_social, cards.layout_card])
def test_each_card_says_where_its_numbers_came_from(layout) -> None:
    """A number on a card must be traceable to the table it was read from."""
    fig, _ = layout(_load())

    assert "generated from docs/published-run/" in _texts(fig)


# --------------------------------------------------------------------------- #
# Geometry
# --------------------------------------------------------------------------- #

def test_the_social_card_stays_inside_its_margin() -> None:
    fig, _ = cards.layout_social(_load())

    assert page.margin_breaches(fig, margin=page.MARGIN_X) == []


def test_the_link_card_stays_inside_its_margin() -> None:
    fig, _ = cards.layout_card(_load())
    margin = 0.058  # cards.layout_card's own margin; the page's is wider

    assert page.margin_breaches(fig, margin=margin) == []


@pytest.mark.parametrize(
    "layout,expect_axes",
    [(cards.layout_social, 1), (cards.layout_card, 0)],
)
def test_only_the_social_card_draws_the_evidence(layout, expect_axes: int) -> None:
    """The 4:5 card carries the interval chart; at 2:1 it would be unreadable.

    Pinned so the chart cannot quietly disappear from the card that has room for it,
    or appear on the one that does not.
    """
    fig, _ = layout(_load())

    assert len(fig.axes) == expect_axes


@pytest.mark.parametrize("layout", [cards.layout_social, cards.layout_card])
def test_no_text_runs_into_the_footer(layout) -> None:
    """Content has to stop above the rule that separates it from the status line."""
    fig, _ = layout(_load())
    fig.canvas.draw()
    invert = fig.transFigure.inverted()

    lowest = min(
        invert.transform((0.0, text.get_window_extent(fig.canvas.get_renderer()).y0))[1]
        for text in fig.texts
        if text.get_text() not in FOOTER_STRINGS
    )
    assert lowest > 0.12, f"content reaches figure y={lowest:.3f}, the rule is at 0.105"
