"""The single command that regenerates the report (spec §8).

    python scripts/run_experiment.py --snapshot <snapshot_id> --out results/<run_id>/

Runs every method of spec §1 through the walk-forward harness (spec §6) over the
frozen out-of-sample period, computes the metric registry of §7 and the decision
rules of protocol §6, and writes an immutable run directory:

    <out>/manifest.json     snapshot, git commit, protocol/spec versions, seeds, env
    <out>/outcomes.csv      per-method §14.1 disclosures, all cost levels, bootstrap CIs
    <out>/decisions.csv     one row per candidate: all sixteen §6.1-§6.4 comparisons
    <out>/calibration.csv   §7.8 return-interval coverage per method
    <out>/folds_<M>.csv     per-fold comparison against the best baseline
    <out>/report.md         the rendered report

**This run is EXPLORATORY.** It is not the confirmatory experiment. Per protocol
§12.2 a run counts as an experiment only if a claim will rest on it, and per
DEC-20261015-012 this is a non-confirmatory run: the registered confirmatory
experiment is Test D (`EXP-H2-20261017-001`) and it has not been executed. The
manifest and the report both say so, because a number this easy to produce is a
number this easy to over-claim.

Output is deliberately ASCII-only: this has to be runnable on a Windows console
whose default code page is not UTF-8, and a report generator that crashes while
announcing its own success is not a tool anyone keeps.
"""

from __future__ import annotations

import argparse
import sys
import time
from datetime import datetime
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

import robustfolio.backtest as backtest  # noqa: E402
from robustfolio import report as reporting  # noqa: E402
from robustfolio.data import list_snapshots, load_snapshot  # noqa: E402


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument(
        "--snapshot",
        default=None,
        help="immutable snapshot id; defaults to the newest one on disk",
    )
    parser.add_argument(
        "--out",
        type=Path,
        default=None,
        help="output directory; defaults to results/<snapshot>-<timestamp>/",
    )
    parser.add_argument(
        "--no-bootstrap",
        action="store_true",
        help="skip the 2000-replication bootstrap (~30s); CIs become NaN",
    )
    parser.add_argument(
        "--no-calibration",
        action="store_true",
        help="skip the section 7.8 return-interval coverage sweep",
    )
    parser.add_argument(
        "--family-size",
        type=int,
        default=None,
        help="multiple-testing family size N (protocol 12.6); defaults to the frozen value",
    )
    parser.add_argument(
        "--skip-certify",
        action="store_true",
        help="skip the structural check; the certificate still enforces itself per rebalance",
    )
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)

    if args.snapshot is None:
        ids = list_snapshots()
        if not ids:
            print("no snapshot on disk; run scripts/build_snapshot.py first", file=sys.stderr)
            return 2
        args.snapshot = ids[0]
    if args.out is None:
        stamp = datetime.now().strftime("%Y%m%d-%H%M%S")
        args.out = Path("results") / f"{args.snapshot}-{stamp}"

    snapshot = load_snapshot(args.snapshot)
    returns = snapshot.monthly_total_returns()
    rf = snapshot.rf_monthly()

    print(f"snapshot   : {args.snapshot}")
    print(f"universe   : {returns.shape[1]} tickers, {returns.shape[0]} months")
    print(f"out        : {args.out}")
    print(f"status     : EXPLORATORY (DEC-20261015-012); not the confirmatory experiment")
    print()
    print(f"{'method':<8}{'rebalances':>11}{'folds':>7}{'turnover':>10}{'net ann':>10}{'gross ann':>11}{'s':>8}")
    print("-" * 62)

    results: dict[str, backtest.BacktestResult] = {}
    started = time.time()
    for method in backtest.METHOD_IDS:
        began = time.time()
        result = backtest.run_method(snapshot, method)
        results[method] = result
        print(
            f"{method:<8}{len(result.weights):>11}{result.folds.nunique():>7}"
            f"{result.annualized_turnover():>10.3f}"
            f"{(result.net_returns(10).mean() * 12):>9.4f}"
            f"{(result.gross_returns.mean() * 12):>9.4f}"
            f"{time.time() - began:>8.1f}"
        )
    elapsed = time.time() - started
    print("-" * 62)
    print(f"{len(results)} methods, {sum(len(r.weights) for r in results.values())} rebalances, "
          f"{elapsed:.1f}s")

    if not args.skip_certify:
        problems = []
        for method, result in results.items():
            over = (result.diagnostics["residual"].astype(float) > 1e-7).sum()
            if over:
                problems.append(f"{method}: {over} rebalances failed the acceptance certificate")
            if len(result.weights) != 168 or result.folds.nunique() != 14:
                problems.append(
                    f"{method}: {len(result.weights)} rebalances / "
                    f"{result.folds.nunique()} folds, expected 168 / 14 (protocol 13.1)"
                )
        if problems:
            print()
            for problem in problems:
                print(f"STRUCTURAL FAILURE: {problem}", file=sys.stderr)
            return 1
        print("certificate: every rebalance accepted (spec 5.6); structure matches protocol 13.1")

    kwargs = {"bootstrap": not args.no_bootstrap, "calibration_window": not args.no_calibration}
    if args.family_size is not None:
        kwargs["family_size"] = args.family_size
    run = reporting.build_report(results, snapshot_id=args.snapshot, rf=rf, **kwargs)

    print()
    best = run.decisions["baseline"].iloc[0] if len(run.decisions) else "n/a"
    print(f"decision rule (protocol 6.1-6.4), best baseline = {best}")
    for method, row in run.decisions.iterrows():
        print(
            f"  {method}: PSR={row['psr']:.3f} DSR={row['dsr']:.3f} "
            f"gap={row['sharpe_gap']:+.3f} folds={int(row['folds_won'])}/"
            f"{int(row['folds_required'])} costs={int(row['cost_levels_won'])}/"
            f"{int(row['cost_levels_required'])} -> {row['verdict']}"
        )

    if run.calibration is not None and len(run.calibration):
        print()
        print("calibration of next-month return intervals (spec 7.8, return half only):")
        for method, row in run.calibration.iterrows():
            print(
                f"  {method}: coverage {row['coverage']:.3f} "
                f"({int(row['hits'])}/{int(row['months_evaluated'])}) "
                f"target 0.80-1.00 -> {'ok' if row['in_target_range'] else 'OUT'}"
            )

    written = run.write(args.out)
    print()
    print(f"wrote {len(written)} files to {args.out}")
    for name in ("manifest", "outcomes", "decisions", "calibration", "report"):
        if name in written:
            print(f"  {written[name].name}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
