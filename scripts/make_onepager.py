"""Draw the one-page summary from the published run tables.

    python scripts/make_onepager.py --out essays/one-pager

Writes ``<out>.pdf`` (the artefact to post or print) and ``<out>.png`` (a preview,
and what this script was developed against).

Everything numeric on the page comes from the two tables the release publishes --
``docs/published-run/outcomes.csv`` and ``docs/published-run/decisions.csv`` -- so
the page cannot say a number the published artefacts do not. The prose is fixed;
the values, the interval, the winning baseline, the verdicts and the row order are
read. Re-running this after a new run re-draws the page rather than leaving it
describing the old one.

Why generated rather than drawn
-------------------------------
A hand-made graphic is a number written into a second place, and the number most
likely to be typed by hand is the number the author is proudest of. That is finding
F29, and a marketing asset is exactly where it does the most damage: the page is
public, nobody checks it against the table, and it cannot be re-derived. A few
facts on the page are not in the published tables at all (the engine certificate,
the two reproduction failures). Those are declared in :data:`BORROWED_FACTS` with
the file that owns each one, and ``tests/test_onepager.py`` asserts each literal is
still present there -- so the page cannot outlive the claim it quotes.

Conventions taken from ``make_figures.py`` and required by protocol SS14.2 / E3 SS4:

* the exploratory, non-confirmatory status is printed on the page rather than
  passed in as a flag, because a flag that can be set to CONFIRMATORY is a flag
  that can be wrong;
* the metric is *excess* net Sharpe and says so, at a named cost level, with its
  interval and its bootstrap parameters implied by the columns read;
* the verdict is printed with the words the frozen policy requires -- the
  hypothesis is "untested, not falsified" -- rather than a friendlier paraphrase;
* ASCII in the figure, so a missing glyph cannot turn a label into a box.
"""

from __future__ import annotations

import argparse
import sys
import textwrap
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
import pandas as pd  # noqa: E402
from matplotlib.patches import Rectangle  # noqa: E402

REPO_ROOT = Path(__file__).resolve().parents[1]

#: Where the release publishes what this page reads. Two files, no run directory.
PUBLISHED_DIR = REPO_ROOT / "docs" / "published-run"

#: A4 portrait, in inches. "One page" means one page of paper as well as one page
#: of a scroll: this is the size that prints.
PAGE_INCHES = (8.27, 11.69)
MARGIN_X = 0.075
CONTENT_W = 1.0 - 2 * MARGIN_X

#: Read from ``make_figures.py`` so the post and the repository read as one
#: artefact: candidates carry weight, baselines are context, and the reference
#: baseline keeps one colour across every figure in the project.
CANDIDATE_COLOURS = {"M1": "#1f77b4", "M2": "#d62728"}
BASELINE_COLOUR = "#8c8c8c"
REFERENCE_COLOUR = "#2ca02c"
INK = "#101010"
MUTED = "#616161"
RULE = "#d5d5d5"
ALERT = "#a3123a"
ALERT_WASH = "#fbf1f4"
FONT = "DejaVu Sans"

#: E3 SS3 fixes this phrase for any public statement of the project's status:
#: *"pre-registered, mechanically evaluated, non-confirmatory"*. It is a module
#: constant so the page cannot paraphrase it, and the test asserts it is on the page.
FIXED_PUBLIC_PHRASING = "pre-registered, mechanically evaluated, non-confirmatory"

EYEBROW = (
    "PRE-REGISTERED, MECHANICALLY EVALUATED, NON-CONFIRMATORY"
    "    |    NET OF 10 bps ONE-WAY COSTS"
)
#: The project's name and its subject. ``TITLE`` is the *display* title, and it is
#: the flagship essay's title -- ``essays/README.md`` lists this page under it -- so
#: the title cannot also carry the identity: a sheet opened from a feed, with the
#: post text scrolled away, has to say which project it belongs to and what that
#: project is. The subject states the question in the flagship's register, so it
#: keeps out the two domain words the frozen title guidance keeps out of the
#: flagship (``notes/release_essay_draft.md``, "avoid 'portfolio' and 'backtest' in
#: the flagship"). The name is a name and is exempt from that.
PROJECT_NAME = "ROBUSTFOLIO"
#: It says what was compared, not how it was tested. The earlier version --
#: "an out-of-sample, cost-aware test of robust methods against five baselines" --
#: identified the project to a specialist and to nobody else: *robust methods*,
#: *baselines* and *cost-aware* are all vocabulary a reader needs before the
#: title arrives. The count is checked against the published rows by
#: ``test_onepager``, because a hand-written "7" is exactly the number that
#: survives a run that added a method; the sample phrase is checked against
#: ``SAMPLE_DESCRIPTION``, so the masthead and the chart cannot describe
#: different samples.
PROJECT_SUBJECT = "7 ways to spread money across 18 US ETFs, 168 out-of-sample months"
MASTHEAD = f"{PROJECT_NAME}  \u00b7  {PROJECT_SUBJECT}"

TITLE = ("I tried to break my own result", "before I published it.")
DECK = (
    "Four defences against fooling yourself, one that failed, "
    "and a null I can stand behind."
)

SECTION_DEFENCES = "THE FOUR DEFENCES, AND THE ONE THAT FAILED"
FAILURE_LABEL = "THE DEFENCE THAT FAILED"
FAILURE_TEXT = (
    "Validating the report generator required running the frozen configuration \u2014 "
    "which WAS the confirmatory configuration. The registered test is re-designated "
    "NON-CONFIRMATORY: the hypothesis is untested, not falsified."
)

SECTION_EVIDENCE = "THE NULL UNDERNEATH IT"
SECTION_REPRO = "AND THE REPRODUCTION CLAIM THAT FAILED TWICE"

FOOTER = (
    "Don't trust the summary \u2014 run the check.  verify_release.py prints EXACT or WITHIN,",
    "and the verdict it compared.   github.com/kira-ml/robustfolio",
    "Generated from docs/published-run/ by scripts/make_onepager.py: the page is a script, not a screenshot.",
)

#: (literal that appears on the page, the file that owns the claim). The test
#: asserts each literal is still in the file named (case-insensitively, since the
#: page shouts the eyebrow), which is what keeps a borrowed number from drifting
#: away from the artefact it was borrowed from.
BORROWED_FACTS = (
    ("18 US ETFs", "README.md"),
    ("168 out-of-sample months", "README.md"),
    ("10 bps", "README.md"),
    ("1,176 solves", "README.md"),
    ("zero rejections", "README.md"),
    ("1.49e-11", "README.md"),
    ("1e-7", "README.md"),
    ("4.2e-17", "README.md"),
    ("4.698e-12", "README.md"),
    ("untested, not falsified", "docs/results_reporting_and_claims_policy.md"),
)

#: The phrases E3 SS4 requires to be present when a number is quoted in public.
#: Asserted by the test rather than remembered at the moment of posting.
REQUIRED_DISCLOSURE_PHRASES = (
    "EXPLORATORY",
    "NON-CONFIRMATORY",
    "excess",
    "10 bps",
    "90%",
    "not an investable return",
    "untested",
)


def _read_table(path: Path) -> pd.DataFrame:
    """Read a published table at full precision (finding F28: the default is lossy)."""
    return pd.read_csv(path, index_col=0, float_precision="round_trip")


def load(folder: Path) -> dict:
    """Everything the page draws, read from the published tables.

    Returned as a plain dict so a test can check the page against the artefacts
    without rendering anything.
    """
    outcomes = _read_table(folder / "outcomes.csv")
    decisions = _read_table(folder / "decisions.csv")

    baselines = sorted({str(value) for value in decisions["baseline"]})
    if len(baselines) != 1:
        raise ValueError(
            f"the candidates are compared against {baselines}; the page can only "
            "state one reference baseline"
        )
    best_baseline = baselines[0]

    headline = int(outcomes["headline_cost_bps"].iloc[0])
    if headline != 10:
        raise ValueError(
            f"the published table's headline cost is {headline} bps; the page's "
            "eyebrow and disclosure both say 10, so both must change together"
        )

    rows = [
        {
            "method": method,
            "point": float(outcomes.loc[method, "net_sharpe"]),
            "low": float(outcomes.loc[method, "net_sharpe_ci_low"]),
            "high": float(outcomes.loc[method, "net_sharpe_ci_high"]),
            "level": float(outcomes.loc[method, "net_sharpe_ci_level"]),
            "candidate": method in set(decisions.index),
        }
        for method in outcomes.index
    ]
    rows.sort(key=lambda row: row["point"], reverse=True)

    candidates = [
        {
            "method": str(method),
            "verdict": str(decisions.loc[method, "verdict"]),
            "psr": float(decisions.loc[method, "psr"]),
            "dsr_pvalue": float(decisions.loc[method, "dsr_pvalue"]),
            "gap": float(decisions.loc[method, "sharpe_gap"]),
        }
        for method in decisions.index
    ]

    return {
        "rows": rows,
        "candidates": candidates,
        "best_baseline": best_baseline,
        "headline_bps": headline,
        "thresholds": {
            "psr": float(decisions["psr_threshold"].iloc[0]),
            "gap": float(decisions["sharpe_gap_threshold"].iloc[0]),
        },
    }


#: The sample description, which belongs on the chart rather than in the eyebrow:
#: a reader asking "over what?" looks at the axis. E3 SS2 rows 2 and 7 want the
#: period and the universe stated, and a graphic has no `manifest.json` to point at.
SAMPLE_DESCRIPTION = "18 US ETFs, 168 out-of-sample months"


def _defences(data: dict) -> tuple[tuple[str, str], ...]:
    """The four rules, with every number in them read rather than typed."""
    psr = " and ".join(f"{c['psr']:.3f}" for c in data["candidates"])
    dsr = " and ".join(f"{c['dsr_pvalue']:.4f}" for c in data["candidates"])
    bar = f"{data['thresholds']['psr']:.2f}"
    return (
        (
            "Freeze before looking.",
            "Metric, thresholds and decision rule dated before the run \u2014 so the "
            "benchmark could not be chosen after the answer was known.",
        ),
        (
            "Prove no leakage mechanically.",
            "A test suite rather than a code review, and one of its tests is recorded "
            "as vacuous rather than passed.",
        ),
        (
            "Certify the numerics.",
            "1,176 solves, zero rejections, worst KKT residual 1.49e-11 against a "
            "1e-7 acceptance bar.",
        ),
        (
            "Require significance AND materiality AND robustness.",
            f"Both candidates pass a p-value against zero ({dsr}) and fail the one "
            f"against the best baseline ({psr} against a bar of {bar}). The rule "
            "requires both.",
        ),
    )


def disclosure(data: dict) -> str:
    """SS14.2's disclosure for the figure, in one sentence."""
    return (
        "EXPLORATORY AND NON-CONFIRMATORY. Net excess Sharpe at the "
        f"{data['headline_bps']} bps headline cost: dot at the point estimate, bar at "
        "its 90% bootstrap interval. No confirmatory test exists, so the hypotheses "
        "are untested rather than falsified. Not an investable return."
    )


def _reproduction_block() -> tuple[str, str]:
    return (
        "A claim of bit-for-bit reproduction \u2014 mine \u2014 failed twice. 4.2e-17 on one "
        "column: a BLAS kernel picks its summation order at run time from the CPU's "
        "features. 4.698e-12 on thirteen: a solver's output is a property of (data, "
        "code, machine), not of (data, code).",
        "The claim is now split: decisions compared exactly, measurements bounded, and "
        "the observed difference printed on every run.",
    )


# --------------------------------------------------------------------------- #
# Drawing
# --------------------------------------------------------------------------- #

def _line_height(points: float, lines: int = 1, spacing: float = 1.42) -> float:
    """Height of ``lines`` of text in figure fraction, for the flow cursor."""
    return points * spacing * lines / (72.0 * PAGE_INCHES[1])


class _Flow:
    """A downward cursor in figure fraction, so blocks can be emitted in order.

    Hand-placed coordinates are how a one-pager ends up with a gap at the bottom
    and a collision in the middle; a cursor makes the vertical budget the sum of
    the blocks, which is a number that can be adjusted. ``y`` is the distance from
    the *top* of the page, so it grows downward.
    """

    def __init__(self, fig, top: float) -> None:
        self.fig = fig
        self.y = top

    def text(
        self,
        body: str,
        *,
        size: float,
        colour: str = INK,
        weight: str = "normal",
        gap_after: float = 0.0,
        wrap: int | None = None,
        x: float = MARGIN_X,
    ) -> None:
        if wrap is not None:
            body = textwrap.fill(body, width=wrap)
        lines = body.count("\n") + 1
        self.fig.text(
            x,
            1.0 - self.y,
            body,
            fontsize=size,
            color=colour,
            fontweight=weight,
            fontfamily=FONT,
            va="top",
            ha="left",
            linespacing=1.42,
        )
        self.y += _line_height(size, lines) + gap_after

    def rule(self, *, gap_before: float = 0.0, gap_after: float = 0.0,
             colour: str = RULE) -> None:
        self.y += gap_before
        self.fig.add_artist(
            Rectangle(
                (MARGIN_X, 1.0 - self.y),
                CONTENT_W,
                0.0011,
                facecolor=colour,
                edgecolor="none",
                transform=self.fig.transFigure,
            )
        )
        self.y += 0.0011 + gap_after

    def callout(
        self,
        label: str,
        body: str,
        *,
        wrap: int,
        label_size: float = 8.0,
        body_size: float = 8.7,
    ) -> None:
        """A washed panel with a thick accent edge, sized to its wrapped text."""
        wrapped = textwrap.fill(body, width=wrap)
        lines = wrapped.count("\n") + 1
        pad_top, pad_bottom, pad_x = 0.016, 0.020, 0.022
        height = (
            _line_height(label_size, 1)
            + 0.006
            + _line_height(body_size, lines)
            + pad_top
            + pad_bottom
        )
        self.y += 0.010
        top = self.y
        # ``top`` is a distance from the top of the page, so the panel's lower
        # edge in figure coordinates is ``1 - top - height``. Passing ``1 - top``
        # alone draws the panel *upward*, over the block above it.
        bottom = 1.0 - top - height
        self.fig.add_artist(
            Rectangle((MARGIN_X, bottom), CONTENT_W, height,
                      facecolor=ALERT_WASH, edgecolor="none",
                      transform=self.fig.transFigure)
        )
        self.fig.add_artist(
            Rectangle((MARGIN_X, bottom), 0.0055, height,
                      facecolor=ALERT, edgecolor="none",
                      transform=self.fig.transFigure)
        )
        self.y += pad_top
        self.fig.text(
            MARGIN_X + pad_x, 1.0 - self.y, label,
            fontsize=label_size, color=ALERT, fontweight="bold",
            fontfamily=FONT, va="top", ha="left",
        )
        self.y += _line_height(label_size, 1) + 0.006
        self.fig.text(
            MARGIN_X + pad_x, 1.0 - self.y, wrapped,
            fontsize=body_size, color=INK, fontfamily=FONT,
            va="top", ha="left", linespacing=1.42,
        )
        self.y = top + height + 0.010


def _draw_interval_plot(fig, data: dict, rect: list[float]) -> None:
    """The seven methods, point estimate and interval, best baseline marked."""
    ax = fig.add_axes(rect)
    rows = data["rows"]
    best = data["best_baseline"]

    for index, row in enumerate(rows):
        method = row["method"]
        if method in CANDIDATE_COLOURS:
            colour = CANDIDATE_COLOURS[method]
            linewidth = 2.4
        elif method == best:
            colour = REFERENCE_COLOUR
            linewidth = 2.4
        else:
            colour = BASELINE_COLOUR
            linewidth = 1.6
        ax.plot([row["low"], row["high"]], [index, index], color=colour,
                linewidth=linewidth, solid_capstyle="round", zorder=2)
        ax.plot([row["point"]], [index], marker="o", markersize=5.0, color=colour,
                markeredgecolor="white", markeredgewidth=0.8, zorder=3)

    reference = next(row["point"] for row in rows if row["method"] == best)
    gap_bar = data["thresholds"]["gap"]

    # SS6.2's materiality bar is a distance on this same axis: a candidate clears it
    # when its dot sits at or right of the baseline plus the bar, because
    # ``sharpe_gap = candidate - baseline``. So the strip between them is exactly the
    # set of outcomes that fail the gate. Shading it costs one patch and no new
    # number -- the bar is read from ``decisions.csv``, like everything else here.
    ax.axvspan(
        reference, reference + gap_bar,
        facecolor=REFERENCE_COLOUR, alpha=0.13,
        edgecolor=REFERENCE_COLOUR, linewidth=0.8, linestyle=(0, (3, 3)),
        zorder=0.5,
    )
    ax.axvline(reference, color=REFERENCE_COLOUR, linewidth=1.0,
               linestyle=(0, (4, 3)), zorder=1)

    ax.set_yticks(range(len(rows)))
    ax.set_yticklabels(
        [row["method"] for row in rows],
        fontsize=8.6, fontfamily=FONT, color=INK,
    )
    ax.set_ylim(len(rows) - 0.5, -0.5)
    ax.set_xlim(-0.30, 1.78)
    ax.tick_params(axis="x", labelsize=8.0, colors=MUTED, length=2.5)
    ax.tick_params(axis="y", length=0)
    for side in ("top", "right", "left"):
        ax.spines[side].set_visible(False)
    ax.spines["bottom"].set_color(RULE)
    ax.grid(axis="x", color=RULE, linewidth=0.6, alpha=0.7, zorder=0)
    ax.set_axisbelow(True)
    ax.set_xlabel(
        f"net excess Sharpe at the {data['headline_bps']} bps headline cost"
        f"    |    {SAMPLE_DESCRIPTION}",
        fontsize=8.0, color=MUTED, fontfamily=FONT, labelpad=4,
    )
    ax.annotate(
        f"{best}  (best baseline)",
        xy=(reference, -0.42), xytext=(reference - 0.02, -0.42),
        fontsize=8.0, color=REFERENCE_COLOUR, fontweight="bold",
        fontfamily=FONT, va="center", ha="right", annotation_clip=False,
    )
    ax.annotate(
        f"\u00a76.2 requires a {gap_bar:.2f} gap over {best}",
        xy=(reference + gap_bar, -0.42), xytext=(reference + gap_bar + 0.02, -0.42),
        fontsize=8.0, color=MUTED, fontfamily=FONT,
        va="center", ha="left", annotation_clip=False,
    )
    for index, row in enumerate(rows):
        ax.text(
            1.72, index, f"{row['point']:.4f}",
            fontsize=8.2, color=MUTED, fontfamily=FONT, va="center", ha="right",
        )


def layout_page(data: dict):
    """Build the page and return ``(figure, flow)`` without writing anything.

    Split out from :func:`draw` so that the two properties worth asserting -- "it
    fits on one page" and "no block crosses the margin" -- can be *measured* on the
    figure instead of judged from a preview. Both are invisible at 60% zoom and
    obvious on a phone.
    """
    fig = plt.figure(figsize=PAGE_INCHES, dpi=170, facecolor="white")
    flow = _Flow(fig, top=0.038)

    # --- header ------------------------------------------------------------ #
    flow.text(MASTHEAD, size=7.8, weight="bold", gap_after=0.009)
    flow.text(EYEBROW, size=7.0, colour=MUTED, weight="bold", gap_after=0.010)
    flow.text(TITLE[0], size=18.0, weight="bold", gap_after=0.002)
    flow.text(TITLE[1], size=18.0, weight="bold", gap_after=0.008)
    flow.text(DECK, size=9.6, colour=MUTED, wrap=100, gap_after=0.010)
    flow.rule(gap_after=0.013)

    # --- the four defences ------------------------------------------------- #
    flow.text(SECTION_DEFENCES, size=7.6, colour=MUTED, weight="bold", gap_after=0.009)
    for name, body in _defences(data):
        flow.text(name, size=9.3, weight="bold", gap_after=0.001, wrap=78)
        flow.text(body, size=8.3, colour=MUTED, wrap=104, gap_after=0.006)

    # --- the one that failed ----------------------------------------------- #
    flow.callout(FAILURE_LABEL, FAILURE_TEXT, wrap=112)
    flow.rule(gap_before=0.012, gap_after=0.012)

    # --- the null, and the evidence for it --------------------------------- #
    flow.text(SECTION_EVIDENCE, size=7.6, colour=MUTED, weight="bold", gap_after=0.008)
    plot_height = 0.152
    plot_top = flow.y + 0.012
    _draw_interval_plot(
        fig, data, [MARGIN_X, 1.0 - plot_top - plot_height, CONTENT_W, plot_height]
    )
    # The axis label sits *below* the axes rather than inside the reserve, so the
    # gap has to include its height: 0.042 clears it, 0.026 drew the disclosure on
    # top of it.
    flow.y = plot_top + plot_height + 0.042
    flow.text(disclosure(data), size=7.6, colour=MUTED, wrap=120, gap_after=0.012)
    flow.rule(gap_after=0.012)

    # --- the second failure ------------------------------------------------ #
    flow.text(SECTION_REPRO, size=7.6, colour=MUTED, weight="bold", gap_after=0.008)
    for body in _reproduction_block():
        flow.text(body, size=8.3, wrap=116, gap_after=0.006)

    # --- footer ------------------------------------------------------------ #
    flow.rule(gap_before=0.009, gap_after=0.011)
    flow.text(FOOTER[0], size=7.4, colour=INK, weight="bold", gap_after=0.003)
    flow.text(FOOTER[1], size=7.4, colour=INK, weight="bold", gap_after=0.006)
    flow.text(FOOTER[2], size=6.4, colour=MUTED, wrap=120)

    return fig, flow


def margin_breaches(fig, *, margin: float = MARGIN_X, slack: float = 0.004) -> list[str]:
    """Text blocks whose ink crosses the page margin. Empty is the passing value.

    ``textwrap`` counts characters, and characters are not all the same width, so a
    wrap width that is right for one paragraph is four pixels too wide for the next.
    Measuring the rendered extent is the only way to know, and it is cheap.
    """
    fig.canvas.draw()
    renderer = fig.canvas.get_renderer()
    invert = fig.transFigure.inverted()
    breaches = []
    for text in fig.texts:
        box = text.get_window_extent(renderer=renderer)
        x0 = invert.transform((box.x0, box.y0))[0]
        x1 = invert.transform((box.x1, box.y1))[0]
        if x0 < margin - slack or x1 > 1.0 - margin + slack:
            body = " ".join(text.get_text().split())[:48]
            breaches.append(f"{body!r} spans {x0:.3f}..{x1:.3f}")
    return breaches


def draw(data: dict, out_base: Path) -> tuple[list[Path], float]:
    """Render the page and write ``<out_base>.pdf`` and ``<out_base>.png``.

    Returns the files written and the bottom of the last block as a fraction from
    the top of the page, so "does it fit on one page" is a number rather than an
    opinion -- ``tests/test_onepager.py`` asserts it, along with
    :func:`margin_breaches`.
    """
    fig, flow = layout_page(data)
    out_base.parent.mkdir(parents=True, exist_ok=True)
    written = []
    for suffix, kwargs in ((".pdf", {}), (".png", {"dpi": 150})):
        path = out_base.with_suffix(suffix)
        fig.savefig(path, facecolor="white", **kwargs)
        written.append(path)
    bottom = flow.y
    plt.close(fig)
    return written, bottom


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--out", type=Path, default=REPO_ROOT / "essays" / "one-pager",
                        help="output basename; .pdf and .png are written")
    parser.add_argument("--published", type=Path, default=PUBLISHED_DIR,
                        help="directory holding the published tables")
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)
    data = load(args.published)
    written, bottom = draw(data, args.out)
    for path in written:
        display = path.relative_to(REPO_ROOT) if path.is_relative_to(REPO_ROOT) else path
        print(f"wrote {display}")
    print(f"page used    : {bottom:.3f} of the sheet (1.000 is the bottom edge)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
