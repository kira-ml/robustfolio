"""Draw the two social derivatives of the one-page summary.

    python scripts/make_cards.py --out essays/one-pager

Writes ``<out>-social.png`` (1200x1500, 4:5 -- the shape a feed shows without
cropping) and ``<out>-card.png`` (1280x640, 2:1 -- the shape GitHub, Slack and X use
for a link preview).

Why derivatives rather than a crop of the A4 page: that page is 1:1.41, the feed is
1:1.25 and the link card is 2:1, so one file cannot be all three. Cropping a
document to a feed shape cuts the masthead or the footer; shrinking it to 2:1 makes
the type unreadable. These carry *less* than the page on purpose: at thumbnail size
only the title and one number survive, so those are what they are built around.

Every number is read from the same published tables as the page, through
``make_onepager.load`` -- so a card cannot state a value the page does not, and
re-running this after a new run redraws rather than leaving the cards describing the
old one. E3 SS3's fixed phrasing and E3 SS4's cost disclosure are on both, because a
post is a public artefact (P4), not merely the document it links to.

Type sizes are *measured* rather than guessed: hand-picked point sizes are how the
first draft of the 4:5 card ran off the right edge on three separate lines, which is
F29's failure mode in a different medium -- a value written down where nothing
recomputes it.
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
from matplotlib.font_manager import FontProperties  # noqa: E402
from matplotlib.patches import Rectangle  # noqa: E402
from matplotlib.textpath import TextPath  # noqa: E402

REPO_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(Path(__file__).resolve().parent))

import make_onepager as page  # noqa: E402

#: 4:5 at 150 dpi. Asserted against the written file, not against these numbers.
SOCIAL_INCHES = (8.0, 10.0)
SOCIAL_DPI = 150
SOCIAL_PIXELS = (1200, 1500)

#: 2:1 at 100 dpi, which is the size GitHub asks for a social preview.
CARD_INCHES = (12.8, 6.4)
CARD_DPI = 100
CARD_PIXELS = (1280, 640)

#: Big type has a tighter leading than a document does.
SPACING = 1.22

#: A little room for the difference between a measured glyph run and its rendering.
SAFETY = 0.98

URL = "github.com/kira-ml/robustfolio"


# --------------------------------------------------------------------------- #
# Measuring, so a size is a result rather than an opinion
# --------------------------------------------------------------------------- #

def text_width_in(body: str, *, size: float, weight: str = "normal") -> float:
    """Width of ``body`` at ``size`` in inches, from the glyphs themselves."""
    prop = FontProperties(family=page.FONT, size=size, weight=weight)
    return TextPath((0.0, 0.0), body, prop=prop).get_extents().width / 72.0


def wrap_to_width(body: str, *, size: float, weight: str = "normal",
                  max_width_in: float) -> str:
    """Greedy word wrap against measured width instead of a character count."""
    limit = max_width_in * SAFETY
    lines: list[str] = []
    current = ""
    for word in body.split():
        trial = f"{current} {word}".strip()
        if current and text_width_in(trial, size=size, weight=weight) > limit:
            lines.append(current)
            current = word
        else:
            current = trial
    if current:
        lines.append(current)
    return "\n".join(lines)


def fit_size(body: str, *, size: float, weight: str = "normal",
             max_width_in: float) -> float:
    """The largest size no bigger than ``size`` at which ``body`` fits on one line."""
    measured = text_width_in(body, size=size, weight=weight)
    if measured <= max_width_in * SAFETY:
        return size
    return size * (max_width_in * SAFETY) / measured


# --------------------------------------------------------------------------- #
# Layout
# --------------------------------------------------------------------------- #

class _Cursor:
    """A downward cursor in figure fraction, for a page of a given height.

    ``make_onepager._Flow`` is the same idea but divides by the A4 height, and
    generalising it would mean editing the file that draws the verified page. Two
    small cursors are cheaper than a refactor of a frozen artefact.
    """

    def __init__(self, fig, *, top: float, margin: float, height_in: float) -> None:
        self.fig = fig
        self.y = top
        self.margin = margin
        self.height_in = height_in

    def text(self, body: str, *, size: float, colour: str = page.INK,
             weight: str = "normal", gap_after: float = 0.0) -> None:
        lines = body.count("\n") + 1
        self.fig.text(
            self.margin, 1.0 - self.y, body,
            fontsize=size, color=colour, fontweight=weight,
            fontfamily=page.FONT, va="top", ha="left", linespacing=SPACING,
        )
        self.y += lines * size * SPACING / (72.0 * self.height_in) + gap_after

    def space(self, amount: float) -> None:
        self.y += amount


def _centre_vertically(fig, *, content_height: float) -> None:
    """Shift every text drawn so far so the block sits in the middle of the page.

    Texts are drawn top-down from ``y = 1`` with ``va="top"``, so a block of height
    ``h`` starts at the top edge and ends at ``1 - h``. Centring it means moving its
    top edge to ``(1 + h) / 2``, which is a *downward* shift of ``(1 - h) / 2``. The
    first version of this function added that amount instead of subtracting it and
    pushed the title off the top of the card; the rendered image, not the test, was
    what showed it.
    """
    delta = (content_height - 1.0) / 2.0
    for text in fig.texts:
        x, y = text.get_position()
        text.set_position((x, y + delta))


def facts(data: dict) -> dict:
    """The one number the cards are built around, read from the tables.

    "Strongest" means the candidate the frozen metric ranks first -- not the one
    with the largest gap, although they coincide here. Choosing by the metric keeps
    the card from picking whichever candidate flatters the sentence.
    """
    candidates = [row for row in data["rows"] if row["candidate"]]
    top = max(candidates, key=lambda row: row["point"])
    decision = next(c for c in data["candidates"] if c["method"] == top["method"])
    return {
        "method": top["method"],
        "baseline": data["best_baseline"],
        "gap": decision["gap"],
        "bar": data["thresholds"]["gap"],
        "verdict": decision["verdict"],
        "bps": data["headline_bps"],
    }


def _footer(fig, *, margin: float, width: float, width_in: float,
            status_size: float, url_size: float) -> None:
    """The two lines that make the card a public artefact rather than a poster.

    ``page.EYEBROW`` is reused verbatim: it carries E3 SS3's fixed phrasing and the
    cost level, and the test for the page already pins that string. Drawing a
    second, friendlier status line here is how a summary and its post start
    disagreeing.
    """
    fig.add_artist(
        Rectangle((margin, 0.105), width, 0.0012,
                  facecolor=page.RULE, edgecolor="none",
                  transform=fig.transFigure)
    )
    fig.text(margin, 0.075, page.EYEBROW,
             fontsize=fit_size(page.EYEBROW, size=status_size, weight="bold",
                               max_width_in=width_in),
             color=page.MUTED, fontweight="bold", fontfamily=page.FONT,
             va="center", ha="left")
    fig.text(margin, 0.042, f"{URL}    |    generated from docs/published-run/",
             fontsize=url_size, color=page.MUTED, fontfamily=page.FONT,
             va="center", ha="left")


def layout_social(data: dict):
    """The 4:5 card, for a feed. Built around the title, one number, and the chart."""
    fig = plt.figure(figsize=SOCIAL_INCHES, dpi=SOCIAL_DPI, facecolor="white")
    width_in = page.CONTENT_W * SOCIAL_INCHES[0]
    cursor = _Cursor(fig, top=0.050, margin=page.MARGIN_X,
                     height_in=SOCIAL_INCHES[1])
    f = facts(data)

    cursor.text(page.PROJECT_NAME, size=11.5, weight="bold", gap_after=0.004)
    cursor.text(
        wrap_to_width(page.PROJECT_SUBJECT, size=9.8, max_width_in=width_in),
        size=9.8, colour=page.MUTED, gap_after=0.0,
    )
    cursor.space(0.030)

    # 28 pt, not 32: at 32 the measured wrap leaves "it." alone on a third line.
    # The point size is a consequence of the wrap, not the other way round.
    cursor.text(
        wrap_to_width(" ".join(page.TITLE), size=28.0, weight="bold",
                      max_width_in=width_in),
        size=28.0, weight="bold", gap_after=0.022,
    )

    cursor.text(
        wrap_to_width(page.DECK, size=15.5, max_width_in=width_in),
        size=15.5, colour=page.MUTED, gap_after=0.026,
    )

    # "Best candidate" rather than "M2": the card is read by people who have no
    # key for the method labels. The names are on the chart, where they have one.
    cursor.text(
        f"Best candidate beat the best baseline by {f['gap']:+.3f}.",
        size=17.0, weight="bold", gap_after=0.002,
    )
    cursor.text(f"The bar was {f['bar']:.2f}.   Verdict: {f['verdict']}.",
                size=17.0, weight="bold", colour=page.ALERT, gap_after=0.030)

    cursor.text(page.FAILURE_LABEL, size=10.0, colour=page.ALERT,
                weight="bold", gap_after=0.006)
    cursor.text(
        wrap_to_width(page.FAILURE_TEXT, size=12.0, max_width_in=width_in),
        size=12.0, colour=page.MUTED,
    )

    # The chart is the project's signature, and it is the one element that makes
    # this evidence rather than a quotation. Same function the A4 page uses.
    top = cursor.y + 0.014
    height = 0.245
    page._draw_interval_plot(
        fig, data,
        [page.MARGIN_X, 1.0 - top - height, page.CONTENT_W, height],
    )

    _footer(fig, margin=page.MARGIN_X, width=page.CONTENT_W, width_in=width_in,
            status_size=9.4, url_size=8.4)
    return fig, cursor


def layout_card(data: dict):
    """The 2:1 card, for a link preview. Only what survives a 600px preview."""
    fig = plt.figure(figsize=CARD_INCHES, dpi=CARD_DPI, facecolor="white")
    margin = 0.058
    width_in = (1.0 - 2.0 * margin) * CARD_INCHES[0]
    cursor = _Cursor(fig, top=0.0, margin=margin, height_in=CARD_INCHES[1])
    f = facts(data)

    cursor.text(page.MASTHEAD, size=11.5, weight="bold", gap_after=0.0)
    cursor.space(0.085)

    # A narrower measure for the title than the body: at the full width the measured
    # wrap breaks after "I", which is grammatical and reads badly. 0.92 puts the
    # break where the title itself puts it.
    cursor.text(
        wrap_to_width(" ".join(page.TITLE), size=36.0, weight="bold",
                      max_width_in=width_in * 0.92),
        size=36.0, weight="bold", gap_after=0.030,
    )
    cursor.text(
        f"Best candidate beat the best baseline by {f['gap']:+.3f}; "
        f"the bar was {f['bar']:.2f}.",
        size=16.0, colour=page.MUTED, gap_after=0.008,
    )
    cursor.text(f"Under the frozen rule: {f['verdict']}.",
                size=16.0, weight="bold", colour=page.ALERT)

    _centre_vertically(fig, content_height=cursor.y)
    _footer(fig, margin=margin, width=1.0 - 2.0 * margin, width_in=width_in,
            status_size=8.6, url_size=8.0)
    return fig, cursor


def draw(data: dict, out_base: Path) -> list[Path]:
    """Render both cards. Returns the files written."""
    out_base.parent.mkdir(parents=True, exist_ok=True)
    written = []
    for suffix, layout in (("-social", layout_social), ("-card", layout_card)):
        fig, _ = layout(data)
        path = out_base.with_name(out_base.name + suffix).with_suffix(".png")
        fig.savefig(path, facecolor="white")
        written.append(path)
        plt.close(fig)
    return written


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--out", type=Path, default=REPO_ROOT / "essays" / "one-pager",
                        help="output basename; -social.png and -card.png are written")
    parser.add_argument("--published", type=Path, default=page.PUBLISHED_DIR,
                        help="directory holding the published tables")
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)
    data = page.load(args.published)
    for path in draw(data, args.out):
        display = path.relative_to(REPO_ROOT) if path.is_relative_to(REPO_ROOT) else path
        print(f"wrote {display}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
