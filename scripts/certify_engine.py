"""Certify the engine against the frozen snapshot (spec §5.6).

For every monthly rebalance of the frozen out-of-sample period (2012-06 ..
2026-05), re-estimate each constructor on its trailing 60-month window using
only the assets eligible at that date, and check that the returned portfolio
satisfies the optimality certificate.

This is the evidence behind the claim "the solve is the optimum it says it is".
It is not an experiment (protocol §12.2): it forms no portfolio, reports no
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

import numpy as np
import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from robustfolio import estimators, optimize  # noqa: E402
from robustfolio.config import (  # noqa: E402
    ESTIMATION_WINDOW,
    GAMMA,
    TURNOVER_PENALTY,
)
from robustfolio.data import load_snapshot  # noqa: E402

DEFAULT_SNAPSHOT = "yahoo-usetf-2007-01-01_2026-09-30-2026-10-17-2ad06139"
OOS_START = pd.Timestamp("2012-06-01")
OOS_END = pd.Timestamp("2026-05-31")

#: The methods that go through a solver. B1 is arithmetic and has no certificate.
METHODS = ("B2", "B3", "B4", "B5", "M1", "M2")


def build_jobs(train: pd.DataFrame) -> dict:
    """The solver-backed constructors, each on its own trailing-60-month window."""
    mu = estimators.sample_mean(train)
    cov = estimators.sample_cov(train)
    shrunk = estimators.ledoit_wolf_cov(train)
    posterior = estimators.black_litterman_returns(mu, cov, gamma=GAMMA)
    w_prev = estimators.equal_weight(train)
    return {
        "B2": lambda: optimize.risk_parity(cov),
        "B3": lambda: optimize.mean_variance(mu, cov),
        "B4": lambda: optimize.minimum_variance(cov),
        "B5": lambda: optimize.mean_variance(
            mu, cov, w_prev=w_prev, turnover_penalty=TURNOVER_PENALTY
        ),
        "M1": lambda: optimize.mean_variance(mu, shrunk),
        "M2": lambda: optimize.mean_variance(posterior, cov),
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--snapshot", default=DEFAULT_SNAPSHOT)
    parser.add_argument("--json", type=Path, default=None)
    args = parser.parse_args()

    snapshot = load_snapshot(args.snapshot)
    returns = snapshot.monthly_total_returns()
    months = returns.index
    test_months = months[(months >= OOS_START) & (months <= OOS_END)]

    record = {
        name: {"worst_residual": 0.0, "worst_at": None, "worst_violation": 0.0, "failures": []}
        for name in METHODS
    }
    condition_numbers: list[float] = []
    universe_sizes: set[int] = set()
    box_constrained = 0
    n_nan = 0
    started = time.time()

    for t in test_months:
        window = months[months < t][-ESTIMATION_WINDOW:]
        train = returns.loc[window, sorted(snapshot.eligible(t))]
        if train.isna().any().any():
            # A gap inside the estimation window would be a data-layer defect,
            # not something to paper over here (spec §3.3).
            n_nan += 1
            continue
        universe_sizes.add(train.shape[1])
        condition_numbers.append(float(np.linalg.cond(estimators.sample_cov(train).to_numpy())))

        for name, job in build_jobs(train).items():
            entry = record[name]
            try:
                solution = job()
            except optimize.SolverFailure as exc:
                entry["failures"].append({"month": t.date().isoformat(), "error": str(exc)})
                continue
            if name == "B2" and solution.formulation == "erc_box_constrained":
                box_constrained += 1
            if solution.residual > entry["worst_residual"]:
                entry["worst_residual"] = solution.residual
                entry["worst_at"] = t.date().isoformat()
            entry["worst_violation"] = max(entry["worst_violation"], solution.max_violation)

    elapsed = time.time() - started
    total_failures = sum(len(entry["failures"]) for entry in record.values())

    print(f"snapshot   : {args.snapshot}")
    print(f"rebalances : {len(test_months)} ({test_months[0].date()} .. {test_months[-1].date()}), "
          f"{len(test_months) // 12} folds")
    print(f"universe   : {sorted(universe_sizes)} assets")
    print(f"cond(sigma) : {min(condition_numbers):.3e} .. {max(condition_numbers):.3e}")
    print(f"risk parity: box-constrained on {box_constrained}/{len(test_months)} rebalances")
    print(f"gaps       : {n_nan} rebalances skipped")
    print(f"elapsed    : {elapsed:.1f}s")
    print()
    print(f"{'method':<7}{'worst residual':>16}{'at':>13}{'worst violation':>18}{'failures':>10}")
    for name in METHODS:
        entry = record[name]
        print(
            f"{name:<7}{entry['worst_residual']:>16.3e}"
            f"{(entry['worst_at'] or '-'):>13}{entry['worst_violation']:>18.3e}"
            f"{len(entry['failures']):>10}"
        )

    if args.json:
        args.json.parent.mkdir(parents=True, exist_ok=True)
        args.json.write_text(
            json.dumps(
                {
                    "snapshot": args.snapshot,
                    "rebalances": len(test_months),
                    "universe_sizes": sorted(universe_sizes),
                    "cond_min": min(condition_numbers),
                    "cond_max": max(condition_numbers),
                    "risk_parity_box_constrained": box_constrained,
                    "elapsed_seconds": elapsed,
                    "methods": record,
                },
                indent=2,
            )
            + "\n",
            encoding="utf-8",
        )
        print(f"\nwrote {args.json}")

    if total_failures:
        print(f"\nFAILED: {total_failures} rebalance(s) did not certify")
        return 1
    print("\nAll rebalances certified.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
