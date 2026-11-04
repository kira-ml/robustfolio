"""Cap sweep for the shrinkage mechanism (exploratory, 2026-11-04).

    python scripts/cap_sweep.py --out results/cap_sweep

Runs B1, B2, B3, B4, M1 and M2 at ``w_max`` in {0.20, 0.30, 0.40, 1.00} on the
frozen snapshot, and B5 at the caps where its turnover epigraph passes the frozen
1e-7 certificate. The 0.30 arm must reproduce the published B3/M1/M2 net Sharpes
to 1e-9; if it does not, the sweep is not comparable to the headline run and the
command fails.

The output is a table and a JSON. It is an exploratory mechanism test, not a
confirmatory result: see ``notes/cap_sweep_shrinkage_2026-11-04.md`` for the
pre-declared decision rule and the firewall.
"""

from __future__ import annotations

import argparse
import json
import sys
import warnings
from pathlib import Path

import pandas as pd

# CVXPY emits one warning per `optimal_inaccurate` rebalance. The certificate,
# not the warning, decides whether a solve is acceptable; the warnings are noise
# in a sweep that intentionally probes looser constraints.
warnings.filterwarnings("ignore", message="Solution may be inaccurate.*")

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
sys.path.insert(0, str(ROOT / "scripts"))

from robustfolio import backtest, data  # noqa: E402
from robustfolio.optimize import SolverFailure  # noqa: E402
import paired_inference as paired  # noqa: E402

CAPS = (0.20, 0.30, 0.40, 1.00)
METHODS = ("B1", "B2", "B3", "B4", "B5", "M1", "M2")
PUBLISHED = ROOT / "docs" / "published-run" / "outcomes.csv"
HEADLINE_BPS = 10


def _excess(result, rf: pd.Series) -> pd.Series:
    net = result.net_returns(HEADLINE_BPS)
    return net - rf.reindex(net.index)


def _sharpe(excess: pd.Series) -> float:
    return paired.annualized_sharpe(excess.dropna().to_numpy())


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--out", type=Path, default=ROOT / "results" / "cap_sweep")
    parser.add_argument("--reps", type=int, default=2000)
    args = parser.parse_args(argv)

    snapshot = data.load_snapshot(data.list_snapshots()[0])
    returns = snapshot.monthly_total_returns()
    rf = snapshot.rf_monthly()
    published = pd.read_csv(PUBLISHED, index_col=0)

    rows: list[dict] = []
    for cap in CAPS:
        by_method: dict[str, dict] = {}
        for method in METHODS:
            try:
                result = backtest.run_harness(
                    returns, snapshot.eligible, method=method, max_weight=cap
                )
            except SolverFailure as exc:
                print(f"cap {cap:.2f} {method}: SOLVER FAILURE - {exc}")
                rows.append(
                    {
                        "w_max": cap,
                        "method": method,
                        "status": "solver_failure",
                        "net_sharpe": None,
                        "gross_sharpe": None,
                        "cost_drag": None,
                        "turnover": None,
                        "max_weight": None,
                        "n_assets": None,
                        "worst_residual": None,
                        "delta_vs_b3": None,
                        "ci_low": None,
                        "ci_high": None,
                        "p_positive": None,
                        "note": str(exc),
                    }
                )
                by_method[method] = {"status": "solver_failure"}
                continue

            excess = _excess(result, rf)
            sr = _sharpe(excess)
            gross_excess = result.gross_returns - rf.reindex(result.gross_returns.index)
            gross_sr = _sharpe(gross_excess)
            worst = float(result.diagnostics["residual"].astype(float).max())
            record = {
                "w_max": cap,
                "method": method,
                "status": "ok",
                "net_sharpe": sr,
                "gross_sharpe": gross_sr,
                "cost_drag": gross_sr - sr,
                "turnover": result.annualized_turnover(),
                "max_weight": float(result.weights.max().max()),
                "n_assets": float((result.weights > 1e-9).sum(axis=1).mean()),
                "worst_residual": worst,
                "returns": excess,
            }
            by_method[method] = record
            print(
                f"cap {cap:.2f} {method}: Sharpe {sr: .4f} "
                f"turnover {record['turnover']:.3f} maxw {record['max_weight']:.3f} "
                f"residual {worst:.2e}"
            )

        baseline = by_method.get("B3", {})
        for method in ("M1", "M2", "B5"):
            record = by_method.get(method, {})
            if record.get("status") != "ok" or baseline.get("status") != "ok":
                continue
            delta = paired.paired_delta_ci(
                record["returns"],
                baseline["returns"],
                reps=args.reps,
                seed=20261017,
            )
            record["delta_vs_b3"] = delta.point
            record["ci_low"] = delta.ci_low
            record["ci_high"] = delta.ci_high
            record["p_positive"] = delta.p_positive
            print(
                f"  {method}-B3: {delta.point:+.4f} "
                f"[{delta.ci_low:+.4f}, {delta.ci_high:+.4f}] "
                f"P>0 {delta.p_positive:.3f}"
            )

        for method, record in by_method.items():
            if record.get("status") != "ok":
                continue
            rows.append(
                {
                    "w_max": cap,
                    "method": method,
                    "status": "ok",
                    "net_sharpe": record["net_sharpe"],
                    "gross_sharpe": record["gross_sharpe"],
                    "cost_drag": record["cost_drag"],
                    "turnover": record["turnover"],
                    "max_weight": record["max_weight"],
                    "n_assets": record["n_assets"],
                    "worst_residual": record["worst_residual"],
                    "delta_vs_b3": record.get("delta_vs_b3"),
                    "ci_low": record.get("ci_low"),
                    "ci_high": record.get("ci_high"),
                    "p_positive": record.get("p_positive"),
                    "note": "",
                }
            )

    frame = pd.DataFrame(rows).sort_values(["w_max", "method"]).reset_index(drop=True)
    args.out.mkdir(parents=True, exist_ok=True)
    frame.to_csv(args.out / "cap_sweep.csv", index=False)
    records = (
        frame.astype(object)
        .where(pd.notna(frame), None)
        .to_dict(orient="records")
    )
    (args.out / "cap_sweep.json").write_text(
        json.dumps(records, indent=2, allow_nan=False), encoding="utf-8"
    )

    # Validity check: the frozen 0.30 arm must reproduce the published metrics.
    for method in ("B3", "M1", "M2"):
        got = frame[(frame.w_max == 0.30) & (frame.method == method)]["net_sharpe"].iloc[0]
        want = float(published.loc[method, "net_sharpe"])
        if abs(got - want) > 1e-9:
            print(
                f"REPRODUCTION FAILURE: 0.30 {method} = {got!r}, published {want!r}",
                file=sys.stderr,
            )
            return 1

    print(f"\nwrote {args.out / 'cap_sweep.csv'}")
    print(frame.to_string(index=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
