"""Run the pre-registered country-ETF sample (2005-07 to 2026-06).

    python scripts/run_country_sample.py --out results/country_sample

This is the new-sample test registered in
``notes/confirmatory_country_etfs_2026-11-05.md``. It uses the same methods,
optimizer, costs and constraints as the first sample, but the corrected paired
significance gate:

    pass_paired = 5th percentile of the paired bootstrap Sharpe difference > 0

That is a 95% one-sided lower confidence bound. The level PSR and the DSR are
reported as diagnostics, not as decision gates.
"""

from __future__ import annotations

import argparse
import json
import math
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
sys.path.insert(0, str(ROOT / "scripts"))

from robustfolio import backtest, data, report, stats  # noqa: E402
from robustfolio.config import (  # noqa: E402
    BOOTSTRAP_BLOCK_MEAN,
    BOOTSTRAP_REPS,
    CI_LEVEL_DECISION,
    CI_LEVEL_REPORT,
    COST_HEADLINE_BPS,
    COST_LEVELS_BPS,
    DSR_FAMILY_SIZE,
    MATERIALITY_DRAWDOWN_SLACK,
    MATERIALITY_SHARPE_GAP,
    MATERIALITY_TURNOVER_MULTIPLE,
    ROBUSTNESS_COST_LEVELS,
    ROBUSTNESS_FOLD_FRACTION,
    ROBUSTNESS_FOLD_SHARE_MAX,
    SEED,
)
import paired_inference as paired  # noqa: E402

START = pd.Timestamp("2005-07-01")
END = pd.Timestamp("2026-06-30")
SNAPSHOT_HINT = "countryetf"
CANDIDATES = ("M1", "M2")
BASELINES = ("B1", "B2", "B3", "B4", "B5")


def _git_commit() -> str | None:
    """The commit the run was produced from, when the checkout has git."""
    try:
        return subprocess.check_output(
            ["git", "rev-parse", "HEAD"], cwd=ROOT, text=True, stderr=subprocess.DEVNULL
        ).strip()
    except (OSError, subprocess.CalledProcessError):
        return None


def _excess(result, rf: pd.Series, bps: int) -> pd.Series:
    net = result.net_returns(bps)
    return (net - rf.reindex(net.index)).dropna()


def _find_snapshot() -> str:
    ids = [s for s in data.list_snapshots() if SNAPSHOT_HINT in s]
    if not ids:
        raise SystemExit("no countryetf snapshot on disk; run scripts/build_snapshot.py first")
    return ids[0]


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--snapshot", default=None)
    parser.add_argument("--out", type=Path, default=ROOT / "results" / "country_sample")
    parser.add_argument("--reps", type=int, default=2000)
    args = parser.parse_args(argv)

    snapshot_id = args.snapshot or _find_snapshot()
    snapshot = data.load_snapshot(snapshot_id)
    rf = snapshot.rf_monthly()

    print(f"snapshot: {snapshot_id}")
    print(f"window  : {START.date()} .. {END.date()}")
    print(f"tickers : {snapshot.monthly_total_returns().shape[1]}")

    results: dict[str, backtest.BacktestResult] = {}
    for method in backtest.METHOD_IDS:
        result = backtest.run_method(snapshot, method, start=START, end=END)
        results[method] = result
        print(
            f"  {method}: {len(result.weights)} rebalances, "
            f"{result.folds.nunique()} folds, "
            f"worst residual {float(result.diagnostics['residual'].astype(float).max()):.2e}"
        )

    outcomes = report.outcome_table(results, rf=rf, bootstrap=True)
    best = str(outcomes.loc[list(BASELINES), "net_sharpe"].astype(float).idxmax())
    best_sr = float(outcomes.loc[best, "net_sharpe"])
    best_result = results[best]

    decisions = []
    for method in CANDIDATES:
        result = results[method]
        excess = _excess(result, rf, COST_HEADLINE_BPS)
        base_excess = _excess(best_result, rf, COST_HEADLINE_BPS)
        delta = paired.paired_delta_ci(
            excess, base_excess, level=0.90, reps=args.reps, seed=20261017
        )
        gap = float(outcomes.loc[method, "net_sharpe"] - best_sr)
        turnover_ratio = float(
            outcomes.loc[method, "turnover_annualized"]
            / outcomes.loc[best, "turnover_annualized"]
        )
        mdd_slack = float(
            outcomes.loc[method, "max_drawdown"] - outcomes.loc[best, "max_drawdown"]
        )
        cost_wins = int(sum(
            float(outcomes.loc[method, f"net_sharpe_{c}bps"])
            > float(outcomes.loc[best, f"net_sharpe_{c}bps"])
            for c in COST_LEVELS_BPS
        ))
        folds = report.fold_table(result, best_result, rf=rf, cost_bps=COST_HEADLINE_BPS)
        fold_wins = int((folds["advantage_sharpe"] > 0).sum())
        fold_target = int(math.ceil(ROBUSTNESS_FOLD_FRACTION * len(folds)))
        advantages = folds["advantage_return"].astype(float)
        total = float(advantages.sum())
        max_share = float((advantages / total).max()) if np.isfinite(total) and total > 0 else float("nan")

        pass_paired = bool(delta.ci_low > 0.0)
        pass_gap = bool(gap >= MATERIALITY_SHARPE_GAP)
        pass_turnover = bool(turnover_ratio <= MATERIALITY_TURNOVER_MULTIPLE)
        pass_mdd = bool(mdd_slack >= -MATERIALITY_DRAWDOWN_SLACK)
        pass_cost = bool(cost_wins >= ROBUSTNESS_COST_LEVELS)
        pass_folds = bool(fold_wins >= fold_target)
        pass_share = bool(np.isfinite(max_share) and max_share <= ROBUSTNESS_FOLD_SHARE_MAX)

        statistical = pass_paired
        material = pass_gap and pass_turnover and pass_mdd
        robust = pass_cost and pass_folds and pass_share
        if statistical and material and robust:
            verdict = "SUCCESS"
        elif (statistical and material) or robust:
            verdict = "PARTIAL"
        else:
            verdict = "FAILURE"

        psr_diagnostic = stats.psr(
            excess, stats.annualized_to_per_period(best_sr)
        )
        trial_two = outcomes.loc[["M1", "M2"], "net_sharpe"] / math.sqrt(12)
        trial_all = outcomes["net_sharpe"] / math.sqrt(12)
        dsr_two = stats.dsr(excess, family_size=2, trial_sharpes_per_period=trial_two)
        dsr_all = stats.dsr(excess, family_size=7, trial_sharpes_per_period=trial_all)

        decisions.append({
            "method": method,
            "baseline": best,
            "baseline_net_sharpe": best_sr,
            "net_sharpe": float(outcomes.loc[method, "net_sharpe"]),
            "paired_delta": delta.point,
            "paired_ci90_low": delta.ci_low,
            "paired_ci90_high": delta.ci_high,
            "paired_p_positive": delta.p_positive,
            "pass_paired": pass_paired,
            "psr_diagnostic": psr_diagnostic,
            "dsr_p_n2_diagnostic": stats.dsr_pvalue(dsr_two),
            "dsr_p_n7_diagnostic": stats.dsr_pvalue(dsr_all),
            "sharpe_gap": gap,
            "pass_gap": pass_gap,
            "turnover_ratio": turnover_ratio,
            "pass_turnover": pass_turnover,
            "drawdown_slack": mdd_slack,
            "pass_drawdown": pass_mdd,
            "cost_levels_won": cost_wins,
            "pass_cost_levels": pass_cost,
            "folds_won": fold_wins,
            "folds_required": fold_target,
            "pass_folds": pass_folds,
            "max_fold_share": max_share,
            "pass_fold_share": pass_share,
            "statistical": statistical,
            "material": material,
            "robust": robust,
            "verdict": verdict,
        })
        print(
            f"  {method} vs {best}: delta {delta.point:+.4f} "
            f"[{delta.ci_low:+.4f}, {delta.ci_high:+.4f}] "
            f"P>0 {delta.p_positive:.3f}; gap {gap:+.4f}; {verdict}"
        )

    decisions_frame = pd.DataFrame(decisions).set_index("method")
    args.out.mkdir(parents=True, exist_ok=True)
    outcomes.to_csv(args.out / "outcomes.csv")
    decisions_frame.to_csv(args.out / "decisions.csv")
    for method in CANDIDATES:
        report.fold_table(results[method], best_result, rf=rf).to_csv(
            args.out / f"folds_{method}.csv", index=False
        )
    manifest = {
        "generated_utc": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "snapshot_id": snapshot_id,
        "git_commit": _git_commit(),
        "start": str(START.date()),
        "end": str(END.date()),
        "n_rebalances": int(len(results["B1"].weights)),
        "n_folds": int(results["B1"].folds.nunique()),
        "protocol_version": report.PROTOCOL_VERSION,
        "spec_version": report.SPEC_VERSION,
        "seed": SEED,
        "bootstrap": {
            "mean_block_months": BOOTSTRAP_BLOCK_MEAN,
            "replications": BOOTSTRAP_REPS,
            "ci_level_report": CI_LEVEL_REPORT,
            "ci_level_decision": CI_LEVEL_DECISION,
        },
        "cost_levels_bps": list(COST_LEVELS_BPS),
        "headline_cost_bps": COST_HEADLINE_BPS,
        "dsr_family_size": DSR_FAMILY_SIZE,
        "method_ids": list(backtest.METHOD_IDS),
        "baseline_ids": list(BASELINES),
        "candidate_ids": list(CANDIDATES),
        "best_baseline": best,
        "status": "pre-registered new sample; paired significance gate",
    }
    (args.out / "manifest.json").write_text(
        json.dumps(manifest, indent=2) + "\n", encoding="utf-8"
    )

    print(f"\nwrote {args.out}")
    print(outcomes[["net_sharpe", "turnover_annualized", "max_drawdown"]].to_string())
    print()
    print(decisions_frame[[
        "paired_delta", "paired_ci90_low", "pass_paired", "sharpe_gap",
        "pass_gap", "folds_won", "pass_folds", "max_fold_share", "verdict",
    ]].to_string())
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
