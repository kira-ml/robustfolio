#!/usr/bin/env python
"""Build the working paper and the LinkedIn carousel, with Typst.

The paper and the carousel are second renderings of numbers that already exist in
``docs/published-run/``, so they must not restate them. This script writes every
measurement the paper quotes into ``paper/generated/numbers.typ`` and every
paired-inference value into ``paper/generated/paired.typ``. ``paper/paper.typ``
and ``paper/carousel.typ`` contain the argument and no measurement at all, which
``tests/test_paper.py`` and ``tests/test_carousel.py`` check by looking for the
table values in their sources.

    python scripts/build_paper.py
    python scripts/build_paper.py --out <paper.pdf> --carousel-out <carousel.pdf>

Typst is an optional dependency (``pip install -e ".[paper]"``), because the
harness and the reproduction path must not need a typesetting engine.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

import make_onepager as page  # noqa: E402  (path is set above)

PUBLISHED = ROOT / "docs" / "published-run"
PAIRED_JSON = PUBLISHED / "paired_inference.json"
CAP_SWEEP_JSON = PUBLISHED / "cap_sweep.json"
COUNTRY_DIR = PUBLISHED / "country-sample"
COUNTRY_UNIVERSE_CSV = ROOT / "notes" / "pit_candidates_country_2026-11-05.csv"
PAPER_DIR = ROOT / "paper"
GENERATED = PAPER_DIR / "generated"
DEFAULT_OUT = ROOT / "essays" / "robustfolio-working-paper.pdf"
DEFAULT_CAROUSEL_OUT = ROOT / "essays" / "robustfolio-carousel.pdf"
UNIVERSE_CSV = ROOT / "notes" / "pit_candidates_2026-10-17.csv"

#: The cost levels the run reports. The columns exist in ``outcomes.csv``; this
#: tuple only names them, and ``numbers_module`` fails if one is missing.
COSTS = (0, 5, 10, 20, 50)

#: Display names, as in ``docs/model_and_method_spec.md`` §1. Not measurements:
#: the results table uses ids only, and this table exists for the reader.
METHOD_NAMES = {
    "B1": "Equal weight",
    "B2": "Risk parity",
    "B3": "Sample MVO",
    "B4": "Minimum variance",
    "B5": "Turnover-penalised MVO",
    "M1": "Shrinkage-covariance MVO",
    "M2": "Black--Litterman MVO",
}

#: Facts the paper quotes that are *not* in the published tables: design
#: diagnostics and cross-machine observations. Each is pinned by
#: ``tests/test_paper.py`` to the file that owns it, so the page cannot drift
#: from the artefact it borrowed from. ``(name, value, owner)``.
SOURCED_FACTS = (
    ("n-part", 3.14, "notes/power_and_effective_bets_2026-10-17.md"),
    ("n-ent", 5.03, "notes/power_and_effective_bets_2026-10-17.md"),
    ("mp-low", 0.452, "notes/power_and_effective_bets_2026-10-17.md"),
    ("mp-high", 1.762, "notes/power_and_effective_bets_2026-10-17.md"),
    ("mp-below", 12, "notes/power_and_effective_bets_2026-10-17.md"),
    ("smallest-eig", 0.0053, "notes/power_and_effective_bets_2026-10-17.md"),
    ("edge-ratio", 85, "notes/power_and_effective_bets_2026-10-17.md"),
    ("level-mde", 0.67, "notes/power_and_effective_bets_2026-10-17.md"),
    ("paired-mde-980", 0.134, "notes/power_and_effective_bets_2026-10-17.md"),
    ("paired-mde-950", 0.212, "notes/power_and_effective_bets_2026-10-17.md"),
    ("fold-null-rate", 0.212, "notes/power_and_effective_bets_2026-10-17.md"),
    ("kkt-worst", "1.49e-11", "README.md"),
    ("kkt-bar", "1e-7", "README.md"),
    ("blas-diff", "4.163e-17", "docs/decision_log.md"),
    ("worst-diff", "4.698e-12", "docs/decision_log.md"),
    ("tolerance", "1e-9", "docs/published-run/README.md"),
)


def _num(value: float) -> str:
    """A Typst float literal that keeps the table's digits.

    ``repr`` is the shortest string that round-trips the binary value, which is
    the most precision that exists. Exponent form is rejected rather than
    guessed at: every number in these tables is O(1), so seeing one would mean
    the table changed shape and the paper should be looked at.
    """
    text = repr(float(value))
    if "e" in text or "E" in text:
        raise ValueError(f"{value!r} needs exponent notation; check the table")
    return text


def _lit(value) -> str:
    if isinstance(value, str):
        return f'"{value}"'
    if isinstance(value, int) and not isinstance(value, bool):
        # A count stays a count: ``12.0 of the 18 eigenvalues`` is a typo waiting
        # to happen, and the note it comes from counts in integers.
        return str(value)
    return _num(value)


def _count_assets() -> int:
    """The universe size, counted from the candidate list rather than typed."""
    lines = [line for line in UNIVERSE_CSV.read_text(encoding="utf-8").splitlines() if line.strip()]
    return len(lines) - 1


def numbers_module(outcomes, decisions, n_assets: int) -> str:
    """The whole of ``numbers.typ``: every measurement the paper can print."""
    headline = int(outcomes["headline_cost_bps"].iloc[0])
    n_methods = len(outcomes)
    months = int(outcomes["rebalances"].iloc[0])
    folds = int(outcomes["folds"].iloc[0])
    best = str(decisions["baseline"].iloc[0])

    missing = [f"net_sharpe_{c}bps" for c in COSTS if f"net_sharpe_{c}bps" not in outcomes.columns]
    if missing:
        raise ValueError(f"the sweep columns are not in outcomes.csv: {missing}")

    order = sorted(outcomes.index, key=lambda m: float(outcomes.loc[m, "net_sharpe"]), reverse=True)
    rows = [
        {
            "id": m,
            "point": float(outcomes.loc[m, "net_sharpe"]),
            "low": float(outcomes.loc[m, "net_sharpe_ci_low"]),
            "high": float(outcomes.loc[m, "net_sharpe_ci_high"]),
            "turnover": float(outcomes.loc[m, "turnover_annualized"]),
            "drawdown": float(outcomes.loc[m, "max_drawdown"]),
            "candidate": m in decisions.index,
            "sweep": [float(outcomes.loc[m, f"net_sharpe_{c}bps"]) for c in COSTS],
        }
        for m in order
    ]

    lines = [
        "// Generated by scripts/build_paper.py from docs/published-run/*.csv.",
        "// Do not edit. Every measurement the paper quotes is written here once,",
        "// so the prose cannot disagree with the tables it is derived from.",
        "",
        f"#let headline-bps = {headline}",
        f"#let n-assets = {n_assets}",
        f"#let n-methods = {n_methods}",
        f"#let n-months = {months}",
        f"#let n-folds = {folds}",
        f"#let n-solves = {n_methods * months}",
        f"#let n-cost-levels = {len(COSTS)}",
        f"#let cost-levels = ({', '.join(str(c) for c in COSTS)})",
        f"#let ci-level = {int(round(float(outcomes['net_sharpe_ci_level'].iloc[0]) * 100))}",
        f"#let ci-reps = {int(outcomes['net_sharpe_ci_reps'].iloc[0])}",
        f"#let ci-block = {_num(outcomes['net_sharpe_ci_block'].iloc[0])}",
        f"#let psr-bar = {_num(decisions['psr_threshold'].iloc[0])}",
        f"#let gap-bar = {_num(decisions['sharpe_gap_threshold'].iloc[0])}",
        f"#let dsr-bar = {_num(decisions['dsr_threshold'].iloc[0])}",
        f"#let turnover-limit = {_num(decisions['turnover_ratio_max'].iloc[0])}",
        f"#let drawdown-min = {_num(decisions['drawdown_slack_min'].iloc[0])}",
        f"#let fold-limit = {_num(decisions['max_fold_share_limit'].iloc[0])}",
        f"#let cost-required = {int(decisions['cost_levels_required'].iloc[0])}",
        f"#let folds-required = {int(decisions['folds_required'].iloc[0])}",
        f"#let best = \"{best}\"",
        "",
        "#let rows = (",
    ]

    for row in rows:
        sweep = ", ".join(_num(value) for value in row["sweep"])
        lines += [
            "  (",
            f'    id: "{row["id"]}",',
            f'    point: {_num(row["point"])},',
            f'    low: {_num(row["low"])},',
            f'    high: {_num(row["high"])},',
            f'    turnover: {_num(row["turnover"])},',
            f'    drawdown: {_num(row["drawdown"])},',
            f'    candidate: {"true" if row["candidate"] else "false"},',
            f"    sweep: ({sweep}),",
            "  ),",
        ]
    lines += ["  )", ""]

    gate_keys = ("psr", "dsr", "gap", "turnover", "drawdown", "cost", "folds", "share")
    lines.append("#let verdicts = (")
    for method in decisions.index:
        record = decisions.loc[method]
        gates = {
            "psr": bool(record["pass_psr"]),
            "dsr": bool(record["pass_dsr"]),
            "gap": bool(record["pass_sharpe_gap"]),
            "turnover": bool(record["pass_turnover"]),
            "drawdown": bool(record["pass_drawdown"]),
            "cost": bool(record["pass_cost_levels"]),
            "folds": bool(record["pass_folds"]),
            "share": bool(record["pass_fold_share"]),
        }
        gate_text = ", ".join(f"{key}: {'true' if gates[key] else 'false'}" for key in gate_keys)
        gap = float(record["sharpe_gap"])
        sweep_gaps = [
            float(outcomes.loc[method, f"net_sharpe_{c}bps"]) - float(outcomes.loc[best, f"net_sharpe_{c}bps"])
            for c in COSTS
        ]
        lines += [
            "  (",
            f'    id: "{method}",',
            f'    psr: {_num(record["psr"])},',
            f'    dsr: {_num(record["dsr_pvalue"])},',
            f'    gap: {_num(gap)},',
            f'    sweep-low: {_num(min(sweep_gaps))},',
            f'    sweep-high: {_num(max(sweep_gaps))},',
            f'    folds-won: {int(record["folds_won"])},',
            f'    cost-won: {int(record["cost_levels_won"])},',
            f'    fold-share: {_num(record["max_fold_share"])},',
            f'    turnover-ratio: {_num(record["turnover_ratio"])},',
            f'    drawdown-slack: {_num(record["drawdown_slack"])},',
            f'    passed: {sum(gates.values())},',
            f'    gates: ({gate_text}),',
            f'    verdict: "{record["verdict"]}",',
            "  ),",
        ]
    lines += ["  )", ""]

    lines.append("#let sourced = (")
    for name, value, _owner in SOURCED_FACTS:
        lines.append(f"  {name}: {_lit(value)},")
    lines += ["  )", ""]

    return "\n".join(lines)


def paired_module(payload: dict) -> str:
    """The paired-inference values the carousel quotes, as a Typst dictionary.

    The JSON is produced by ``scripts/paired_inference.py`` and copied into
    ``docs/published-run/`` so the carousel is reproducible without a local run
    directory. Nothing here is recomputed or rounded: the carousel formats the
    full-precision value with its own ``fmt`` helper.
    """
    lines = [
        "// Generated by scripts/build_paper.py from docs/published-run/paired_inference.json.",
        "// Do not edit. The carousel formats these values; it does not type them.",
        "",
        "#let paired = (",
        f"  bar: {_num(payload['bar'])},",
        f"  n-months: {int(payload['n_months'])},",
        "  methods: (",
    ]
    for method, row in payload["methods"].items():
        dsr = row["dsr_p"]
        lines += [
            f"    {method}: (",
            f"      delta: {_num(row['point_delta_sr'])},",
            f"      ci-low: {_num(row['ci90_low'])},",
            f"      ci-high: {_num(row['ci90_high'])},",
            f"      p-positive: {_num(row['p_positive'])},",
            f"      p-one-sided: {_num(row['p_one_sided'])},",
            f"      p-exceeds: {_num(row['p_exceeds_bar'])},",
            f"      rho: {_num(row['rho'])},",
            f'      equivalence: "{row["equivalence"]}",',
            f"      psr: {_num(row['psr_registered'])},",
            f"      psr-required: {_num(row['psr_required_delta'])},",
            f"      psr-mde: {_num(row['psr_mde_80'])},",
            f"      psr-power: {_num(row['psr_power_at_bar_simulated'])},",
            f"      candidate-sr: {_num(row['candidate_net_sharpe'])},",
            f"      baseline-sr: {_num(row['baseline_net_sharpe'])},",
            f"      dsr: (n1: {_num(dsr['1'])}, n2: {_num(dsr['2'])}, n7: {_num(dsr['7'])}),",
            f"      folds-positive: {int(row['folds_positive'])},",
            f"      folds-total: {int(row['folds_total'])},",
            f"      fold-min: {_num(row['fold_min_delta'])},",
            f"      fold-max: {_num(row['fold_max_delta'])},",
            "    ),",
        ]
    comparator = payload["comparator"]
    lines += [
        "  ),",
        "  comparator: (",
        f'    best: "{comparator["best"]}",',
        f'    second: "{comparator["second"]}",',
        f"    margin: {_num(comparator['margin'])},",
        "  ),",
        ")",
        "",
    ]
    return "\n".join(lines)


def cap_sweep_module(records: list[dict]) -> str:
    """The cap-sweep values the carousel quotes, as a Typst dictionary.

    The JSON is produced by ``scripts/cap_sweep.py`` and copied into
    ``docs/published-run/``. The carousel reads ``m1`` and ``m2`` for the paired
    differences and ``b3`` for the baseline level; the B5 failures are named so
    the slide can say the arm is incomplete instead of silently dropping it.
    """
    def rows_for(method: str, *, with_delta: bool) -> list[dict]:
        return [
            row
            for row in records
            if row.get("method") == method and row.get("status") == "ok"
        ]

    lines = [
        "// Generated by scripts/build_paper.py from docs/published-run/cap_sweep.json.",
        "// Do not edit. The carousel formats these values; it does not type them.",
        "",
        "#let cap-sweep = (",
    ]
    for method, key in (("M1", "m1"), ("M2", "m2")):
        lines.append(f"  {key}: (")
        for row in rows_for(method, with_delta=True):
            lines += [
                "    (",
                f"      cap: {_num(row['w_max'])},",
                f"      net: {_num(row['net_sharpe'])},",
                f"      gross: {_num(row['gross_sharpe'])},",
                f"      cost: {_num(row['cost_drag'])},",
                f"      turnover: {_num(row['turnover'])},",
                f"      maxw: {_num(row['max_weight'])},",
                f"      n-assets: {_num(row['n_assets'])},",
                f"      delta: {_num(row['delta_vs_b3'])},",
                f"      low: {_num(row['ci_low'])},",
                f"      high: {_num(row['ci_high'])},",
                "    ),",
            ]
        lines.append("  ),")
    lines.append("  b3: (")
    for row in rows_for("B3", with_delta=False):
        lines += [
            "    (",
            f"      cap: {_num(row['w_max'])},",
            f"      net: {_num(row['net_sharpe'])},",
            "    ),",
        ]
    lines.append("  ),")
    failed = [
        row["w_max"]
        for row in records
        if row.get("method") == "B5" and row.get("status") != "ok"
    ]
    lines.append(
        "  b5-incomplete: (" + ", ".join(_num(value) for value in failed) + "),"
    )
    lines += [")", ""]
    return "\n".join(lines)


def _count_country_assets() -> int:
    lines = [
        line
        for line in COUNTRY_UNIVERSE_CSV.read_text(encoding="utf-8").splitlines()
        if line.strip()
    ]
    return len(lines) - 1


def country_module(outcomes, decisions) -> str:
    """The new-sample values the paper and carousel quote, as a Typst dictionary."""
    n_months = int(outcomes["rebalances"].iloc[0])
    n_folds = int(outcomes["folds"].iloc[0])
    best = str(decisions["baseline"].iloc[0])
    order = sorted(
        outcomes.index,
        key=lambda m: float(outcomes.loc[m, "net_sharpe"]),
        reverse=True,
    )
    lines = [
        "// Generated by scripts/build_paper.py from docs/published-run/country-sample/.",
        "// Do not edit. The paper and carousel format these values.",
        "",
        "#let country = (",
        f"  n-months: {n_months},",
        f"  n-folds: {n_folds},",
        f"  n-assets: {_count_country_assets()},",
        f'  best: "{best}",',
        "  rows: (",
    ]
    for method in order:
        lines += [
            "    (",
            f'      id: "{method}",',
            f"      net: {_num(outcomes.loc[method, 'net_sharpe'])},",
            f"      turnover: {_num(outcomes.loc[method, 'turnover_annualized'])},",
            f"      drawdown: {_num(outcomes.loc[method, 'max_drawdown'])},",
            f"      candidate: {'true' if method in decisions.index else 'false'},",
            "    ),",
        ]
    lines += ["  ),", "  decisions: ("]
    for method in decisions.index:
        record = decisions.loc[method]
        lines += [
            "    (",
            f'      id: "{method}",',
            f"      delta: {_num(record['paired_delta'])},",
            f"      low: {_num(record['paired_ci90_low'])},",
            f"      high: {_num(record['paired_ci90_high'])},",
            f"      p-positive: {_num(record['paired_p_positive'])},",
            f"      gap: {_num(record['sharpe_gap'])},",
            f"      turnover-ratio: {_num(record['turnover_ratio'])},",
            f"      cost-won: {int(record['cost_levels_won'])},",
            f"      folds-won: {int(record['folds_won'])},",
            f"      folds-required: {int(record['folds_required'])},",
            f'      verdict: "{record["verdict"]}",',
            "    ),",
        ]
    lines += ["  ),", ")", ""]
    return "\n".join(lines)


def draw_figure(data: dict, path: Path) -> None:
    """The interval figure, drawn by the one-pager's own routine at print size."""
    import matplotlib

    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    fig = plt.figure(figsize=(6.3, 3.15), dpi=300)
    fig.patch.set_facecolor("white")
    page._draw_interval_plot(fig, data, [0.085, 0.105, 0.795, 0.78], annotate_y=-0.66)
    # Headroom for the two header annotations, so they clear the top row's interval
    # instead of running through it.
    fig.axes[0].set_ylim(len(data["rows"]) - 0.5, -1.05)
    path.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(path, dpi=300, facecolor="white", bbox_inches="tight", pad_inches=0.02)
    plt.close(fig)


def _write_numbers() -> Path:
    """Write the paper's interpolated numbers for whichever document needs them."""
    outcomes = page._read_table(PUBLISHED / "outcomes.csv")
    decisions = page._read_table(PUBLISHED / "decisions.csv")
    path = GENERATED / "numbers.typ"
    path.write_text(
        numbers_module(outcomes, decisions, _count_assets()),
        encoding="utf-8",
        newline="\n",
    )
    return path


def _write_country() -> Path:
    outcomes = page._read_table(COUNTRY_DIR / "outcomes.csv")
    decisions = page._read_table(COUNTRY_DIR / "decisions.csv")
    path = GENERATED / "country.typ"
    path.write_text(
        country_module(outcomes, decisions), encoding="utf-8", newline="\n"
    )
    return path


def compile_pdf(out: Path) -> None:
    import typst

    out.parent.mkdir(parents=True, exist_ok=True)
    typst.compile(str(PAPER_DIR / "paper.typ"), output=str(out), root=str(ROOT))


def compile_carousel(out: Path) -> None:
    import typst

    out.parent.mkdir(parents=True, exist_ok=True)
    typst.compile(str(PAPER_DIR / "carousel.typ"), output=str(out), root=str(ROOT))


def build_carousel(out: Path = DEFAULT_CAROUSEL_OUT) -> tuple[Path, Path, Path]:
    """Write ``paired.typ`` / ``cap_sweep.typ`` and compile the carousel."""
    payload = json.loads(PAIRED_JSON.read_text(encoding="utf-8"))
    cap_records = json.loads(CAP_SWEEP_JSON.read_text(encoding="utf-8"))
    GENERATED.mkdir(parents=True, exist_ok=True)
    paired = GENERATED / "paired.typ"
    paired.write_text(paired_module(payload), encoding="utf-8", newline="\n")
    cap = GENERATED / "cap_sweep.typ"
    cap.write_text(cap_sweep_module(cap_records), encoding="utf-8", newline="\n")
    _write_numbers()
    _write_country()
    compile_carousel(out)
    return paired, cap, out


def page_count(path: Path) -> int:
    from pypdf import PdfReader

    return len(PdfReader(str(path)).pages)


def build(out: Path = DEFAULT_OUT) -> tuple[Path, Path, Path]:
    data = page.load(PUBLISHED)

    GENERATED.mkdir(parents=True, exist_ok=True)
    numbers = _write_numbers()

    figure = GENERATED / "intervals.png"
    draw_figure(data, figure)
    _write_country()

    compile_pdf(out)
    return numbers, figure, out


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--out", type=Path, default=DEFAULT_OUT, help="where to write the paper PDF")
    parser.add_argument(
        "--carousel-out",
        type=Path,
        default=DEFAULT_CAROUSEL_OUT,
        help="where to write the carousel PDF",
    )
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)
    numbers, figure, out = build(args.out)
    paired, cap, carousel = build_carousel(args.carousel_out)

    for path in (numbers, figure, out, paired, cap, carousel):
        rel = path.relative_to(ROOT) if path.is_relative_to(ROOT) else path
        print(f"wrote {rel}  ({path.stat().st_size:,} bytes)")

    try:
        print(f"paper: {page_count(out)} pages; carousel: {page_count(carousel)} slides")
    except ImportError:  # pragma: no cover - pypdf is in the "paper" extra
        pass
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
