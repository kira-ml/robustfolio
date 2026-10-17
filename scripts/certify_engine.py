"""Certify the engine on the frozen snapshot (spec §5.6).

Runs the *production* walk-forward harness (``robustfolio.backtest``) for every
method over the frozen out-of-sample period (2012-06 .. 2026-05) and checks that
every rebalance carries a passing optimality certificate.

Why it drives the harness instead of rebuilding the rebalance loop: an earlier
version of this script rebuilt it, and passed B5 a constant equal-weight initial
holding. Production passes B5 the *drifted* previous holding. Those are different
optimisation problems, so the script certified a problem the project never runs.
It reported B5 clean (worst residual 3.8e-12) while production rejected seven
rebalances, the worst at 1.5e-3. Evidence that the artifact under test did not
produce is not evidence.

This is not an experiment (protocol §12.2): it forms no portfolio, reports no
strategy metric, and cannot be cited for or against any hypothesis. It prints a
table and exits non-zero if any rebalance fails to certify.

    python scripts/certify_engine.py
    python scripts/certify_engine.py --snapshot <snapshot_id> --json results/certify.json
"""

from __future__ import annotations

import argparse
import json
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from robustfolio import backtest, optimize  # noqa: E402
from robustfolio.data import load_snapshot  # noqa: E402

DEFAULT_SNAPSHOT = "yahoo-usetf-2007-01-01_2026-09-30-2026-10-17-2ad06139"

#: Protocol §13.1: 168 monthly rebalances, in 14 folds of 12 months.
EXPECTED_REBALANCES = 168
EXPECTED_FOLDS = 14


def summarise(result) -> dict:
    """Certificate and structure of one method's run."""
    diagnostics = result.diagnostics
    residual = diagnostics["residual"].astype(float)
    violation = diagnostics["max_violation"].astype(float)
    iterations = diagnostics["solver_iterations"]
    worst_month = result.weights.index[residual.values.argmax()]
    # B1 is arithmetic: it forms no covariance, so it records no condition number.
    cond = diagnostics["cond"] if "cond" in diagnostics.columns else None
    return {
        "method": result.method,
        "rebalances": int(len(residual)),
        "folds": int(result.folds.nunique()),
        "first_rebalance": result.weights.index[0].date().isoformat(),
        "last_rebalance": result.weights.index[-1].date().isoformat(),
        "universe_min": int(diagnostics["n_assets"].min()),
        "universe_max": int(diagnostics["n_assets"].max()),
        "worst_residual": float(residual.max()),
        "worst_residual_at": worst_month.date().isoformat(),
        "n_over_acceptance": int((residual > optimize.ACCEPT_TOL).sum()),
        "worst_violation": float(violation.max()),
        "cond_min": None if cond is None else float(cond.min()),
        "cond_max": None if cond is None else float(cond.max()),
        "formulations": {str(k): int(v) for k, v in
                         diagnostics["formulation"].value_counts().items()},
        "max_solver_iterations": None if iterations.isna().all() else int(iterations.max()),
        "solver_statuses": {str(k): int(v) for k, v in
                            diagnostics["solver_status"].fillna("none").value_counts().items()},
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--snapshot", default=DEFAULT_SNAPSHOT)
    parser.add_argument("--json", type=Path, default=None)
    args = parser.parse_args()

    snapshot = load_snapshot(args.snapshot)
    started = time.time()

    summaries: list[dict] = []
    failures: list[dict] = []
    for method in backtest.METHOD_IDS:
        try:
            summaries.append(summarise(backtest.run_method(snapshot, method)))
        except optimize.SolverFailure as exc:
            failures.append({"method": method, "error": str(exc)})

    elapsed = time.time() - started
    solves = sum(entry["rebalances"] for entry in summaries)

    # --- structural checks ------------------------------------------------- #
    problems: list[str] = []
    if not failures:
        for entry in summaries:
            if entry["rebalances"] != EXPECTED_REBALANCES:
                problems.append(f"{entry['method']}: {entry['rebalances']} rebalances, "
                                f"expected {EXPECTED_REBALANCES} (protocol §13.1)")
            if entry["folds"] != EXPECTED_FOLDS:
                problems.append(f"{entry['method']}: {entry['folds']} folds, "
                                f"expected {EXPECTED_FOLDS} (protocol §13.1)")
            if entry["first_rebalance"] != summaries[0]["first_rebalance"]:
                problems.append(f"{entry['method']}: first rebalance "
                                f"{entry['first_rebalance']} disagrees with "
                                f"{summaries[0]['first_rebalance']}")
            if entry["last_rebalance"] != summaries[0]["last_rebalance"]:
                problems.append(f"{entry['method']}: last rebalance "
                                f"{entry['last_rebalance']} disagrees with "
                                f"{summaries[0]['last_rebalance']}")
            if entry["n_over_acceptance"]:
                problems.append(f"{entry['method']}: {entry['n_over_acceptance']} "
                                f"rebalances over the acceptance tolerance")

    print(f"snapshot      : {args.snapshot}")
    print(f"acceptance    : residual and violation <= {optimize.ACCEPT_TOL:.0e} (spec 5.6)")
    print(f"solver        : cvxpy + CLARABEL, all tolerances {optimize.SOLVER_TOL:.0e} (finding F17)")
    print(f"solves        : {solves} certified in {elapsed:.1f}s")
    print()

    header = ("method", "rebalances", "folds", "universe", "worst residual", "at",
              "worst viol", "iters", "over")
    print("%-7s%11s%7s%10s%16s%13s%12s%7s%6s" % header)
    for entry in summaries:
        print("%-7s%11d%7d%10s%16.3e%13s%12.3e%7s%6d"
              % (entry["method"], entry["rebalances"], entry["folds"],
                 f"{entry['universe_min']}..{entry['universe_max']}",
                 entry["worst_residual"], entry["worst_residual_at"],
                 entry["worst_violation"],
                 "-" if entry["max_solver_iterations"] is None
                 else entry["max_solver_iterations"],
                 entry["n_over_acceptance"]))
    print()

    for entry in summaries:
        condition = ("cond n/a" if entry["cond_min"] is None
                     else f"cond {entry['cond_min']:.2e}..{entry['cond_max']:.2e}")
        print(f"  {entry['method']}: {entry['formulations']}  "
              f"solver said {entry['solver_statuses']}  {condition}")

    if args.json:
        args.json.parent.mkdir(parents=True, exist_ok=True)
        args.json.write_text(
            json.dumps({
                "snapshot": args.snapshot,
                "acceptance_tolerance": optimize.ACCEPT_TOL,
                "solver_tolerance": optimize.SOLVER_TOL,
                "elapsed_seconds": elapsed,
                "solves": solves,
                "methods": summaries,
                "structural_problems": problems,
                "failures": failures,
            }, indent=2) + "\n",
            encoding="utf-8",
        )
        print(f"\nwrote {args.json}")

    if failures:
        print("\nFAILED to certify:")
        for failure in failures:
            print(f"  {failure['method']}: {failure['error']}")
        return 1
    if problems:
        print("\nFAILED structural checks:")
        for problem in problems:
            print(f"  {problem}")
        return 1
    print("\nAll rebalances certified; structure matches protocol 13.1.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
