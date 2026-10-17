"""Draw the headline figures from a published run directory.

    python scripts/make_figures.py --run results/<run_id>/ --out results/<run_id>/figures/

Everything comes from the run directory (``net_excess_returns.csv``,
``outcomes.csv``, ``manifest.json``) -- the harness is not re-run. That is the
point of publishing the return series: the figure is a function of the artefact a
reader already has, so a reader who dislikes our plot can make their own without
reproducing the pipeline.

Two figures:

``equity_curve.png``  cumulative net *excess* return and its drawdown, all methods
``net_sharpe_ci.png`` the primary metric per method with its bootstrap interval

Conventions imposed by protocol §14.2, and enforced here rather than remembered:

* every figure states the cost level it is net of;
* every figure states whether the run is exploratory or confirmatory, taken from
  the run's own ``manifest.json`` rather than from the person plotting;
* no figure is titled or annotated as if cumulative net excess return were an
  investable or absolute return -- it is a diagnostic path of a metric's input.

Labels are ASCII on purpose: a missing glyph in the reader's font stack turns an
axis label into a box, and "10 bps" does not need a Greek letter.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

import matplotlib

matplotlib.use("Agg")  # no display in CI; must precede pyplot import

import matplotlib.pyplot as plt  # noqa: E402
import matplotlib.dates as mdates  # noqa: E402
import pandas as pd  # noqa: E402

matplotlib.rcParams["axes.unicode_minus"] = False
matplotlib.rcParams["figure.dpi"] = 150

#: Candidates get weight; baselines are context and should not shout.
CANDIDATE_COLOURS = {"M1": "#1f77b4", "M2": "#d62728"}
BASELINE_COLOUR = "#8c8c8c"
REFERENCE_COLOUR = "#2ca02c"


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--run", type=Path, required=True,
                        help="published run directory")
    parser.add_argument("--out", type=Path, default=None,
                        help="where to write the PNGs; defaults to <run>/figures/")
    return parser.parse_args(argv)


def _read_csv(path: Path) -> pd.DataFrame:
    """Read a published table at full precision.

    ``pandas.read_csv`` is lossy by one ULP at its default settings (finding
    F28), which is invisible in a plot but not in a check, so one reader is used
    everywhere to keep the two consistent.
    """
    return pd.read_csv(path, index_col=0, float_precision="round_trip")


def _style(method: str) -> dict:
    if method in CANDIDATE_COLOURS:
        return {"color": CANDIDATE_COLOURS[method], "linewidth": 2.0, "zorder": 3}
    if method == "B1":
        return {"color": REFERENCE_COLOUR, "linewidth": 1.4, "zorder": 2}
    return {"color": BASELINE_COLOUR, "linewidth": 1.1, "alpha": 0.9, "zorder": 1}


def _provenance(run: Path, headline_bps: object, status: str) -> str:
    return (
        f"net of {headline_bps} bps one-way cost   |   {status} run"
        f"   |   run {run.name}   |   not an investable return"
    )


def _status(manifest: dict) -> str:
    """The run's own scope, read rather than assumed.

    A figure that calls a run confirmatory when its manifest does not is exactly
    the failure protocol §14.2 forbids, and finding F26 is open precisely because
    the confirmatory run's blindness was consumed. So the label comes from
    ``manifest.json`` and an unreadable manifest is labelled as unreadable.
    """
    scope = str(manifest.get("scope", ""))
    if "EXPLORATORY" in scope.upper():
        return "EXPLORATORY"
    if "CONFIRMATORY" in scope.upper():
        return "CONFIRMATORY"
    return "STATUS-NOT-STATED"


def equity_curve(run: Path, out: Path, status: str) -> Path:
    returns = _read_csv(run / "net_excess_returns.csv")
    # The index is written as text; without this the axis is categorical, which
    # both crowds the labels and silences the date locator below.
    returns.index = pd.to_datetime(returns.index)
    outcomes = _read_csv(run / "outcomes.csv")
    headline = int(outcomes["headline_cost_bps"].iloc[0])

    growth = (1.0 + returns).cumprod()
    drawdown = growth / growth.cummax() - 1.0

    figure, (top, bottom) = plt.subplots(
        2, 1, figsize=(9, 7), sharex=True, gridspec_kw={"height_ratios": [2, 1]}
    )

    for method in growth.columns:
        style = _style(method)
        top.plot(growth.index, growth[method], label=method, **style)
        bottom.plot(drawdown.index, drawdown[method], **style)

    top.set_ylabel("cumulative net excess return\n(multiple of 1.0)")
    top.axhline(1.0, color="black", linewidth=0.8, linestyle=":", zorder=0)
    top.set_title("Cumulative net excess return, walk-forward out-of-sample")
    top.legend(ncol=4, fontsize=8, frameon=False, loc="upper left")
    top.grid(alpha=0.25)

    bottom.set_ylabel("drawdown")
    bottom.set_xlabel("month-end")
    bottom.grid(alpha=0.25)
    # Yearly ticks: 168 month labels are unreadable and hide the shape.
    bottom.xaxis.set_major_locator(mdates.YearLocator())
    bottom.xaxis.set_major_formatter(mdates.DateFormatter("%Y"))

    figure.text(0.5, 0.012, _provenance(run, headline, status),
                ha="center", fontsize=7.5, color="#444444")
    figure.tight_layout(rect=(0, 0.045, 1, 1))

    path = out / "equity_curve.png"
    figure.savefig(path)
    plt.close(figure)
    return path


def net_sharpe_ci(run: Path, out: Path, status: str) -> Path:
    outcomes = _read_csv(run / "outcomes.csv")
    headline = int(outcomes["headline_cost_bps"].iloc[0])

    frame = outcomes
    values = frame["net_sharpe"]
    low = frame.get("net_sharpe_ci_low")
    high = frame.get("net_sharpe_ci_high")
    level = frame.get("net_sharpe_ci_level")

    order = sorted(values.index, key=lambda m: values[m])
    positions = range(len(order))
    colours = [
        CANDIDATE_COLOURS.get(m, REFERENCE_COLOUR if m == "B1" else BASELINE_COLOUR)
        for m in order
    ]

    figure, ax = plt.subplots(figsize=(8, 4))
    if low is not None and high is not None:
        errors = [
            [values[m] - low[m] for m in order],
            [high[m] - values[m] for m in order],
        ]
        ax.errorbar(
            list(positions), [values[m] for m in order], yerr=errors,
            fmt="none", ecolor="black", elinewidth=1.2, capsize=4, zorder=2,
        )
    ax.scatter(list(positions), [values[m] for m in order], c=colours, s=70, zorder=3)

    ax.set_xticks(list(positions))
    ax.set_xticklabels(order)
    ax.set_ylabel("annualised net excess Sharpe")
    ax.axhline(0.0, color="black", linewidth=0.9, linestyle="--")
    ax.grid(axis="y", alpha=0.25)

    if level is not None and len(level.dropna()):
        caption = f"interval: {level.dropna().iloc[0]:.0%} stationary block bootstrap"
    else:
        caption = "no interval available in this run"
    ax.set_title(f"Primary metric at {headline} bps: {caption}", fontsize=10)

    figure.text(0.5, 0.012, _provenance(run, headline, status),
                ha="center", fontsize=7.5, color="#444444")
    figure.tight_layout(rect=(0, 0.05, 1, 1))

    path = out / "net_sharpe_ci.png"
    figure.savefig(path)
    plt.close(figure)
    return path


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)
    run = Path(args.run)
    if not (run / "outcomes.csv").exists():
        print(f"not a run directory (no outcomes.csv): {run}", file=sys.stderr)
        return 2

    manifest_path = run / "manifest.json"
    manifest = json.loads(manifest_path.read_text(encoding="utf-8")) if manifest_path.exists() else {}
    status = _status(manifest)

    out = Path(args.out) if args.out is not None else run / "figures"
    out.mkdir(parents=True, exist_ok=True)

    written = []
    if (run / "net_excess_returns.csv").exists():
        written.append(equity_curve(run, out, status))
    else:
        print("no net_excess_returns.csv; skipping the equity curve", file=sys.stderr)
    written.append(net_sharpe_ci(run, out, status))

    print(f"run        : {run.name}")
    print(f"status     : {status}")
    print(f"snapshot   : {manifest.get('snapshot_id', 'unknown')}")
    for path in written:
        print(f"wrote      : {path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
