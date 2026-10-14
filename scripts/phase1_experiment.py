"""Phase 1 smoke test.

Tests problem_framing.md H1.1, H1.2 and the §3.1 cost claim.

Expected under the framing: sample MVO shows extreme weights and high
turnover; 1/N is competitive net of cost. If both hold, the framing is
not falsified. If either fails, we learn that before building Phase 2.
"""
from __future__ import annotations

import sys
from pathlib import Path

import pandas as pd

# Make src importable without installing the package.
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from robustfolio import backtest, data, metrics  # noqa: E402

RESULTS_DIR = Path(__file__).resolve().parents[1] / "results"
RESULTS_DIR.mkdir(exist_ok=True)


METHODS = [
    "equal_weight",
    "inverse_vol",
    "sample_mvo",
    "unconstrained_sample_mvo",
    "ledoit_wolf_mvo",
    "turnover_penalized_mvo",
]

TRAIN_MONTHS = 60
TEST_MONTHS = 12
STEP_MONTHS = 12
COST_BPS = 10.0
# L1 penalty coefficient. 0.01 was numerically inert against SLSQP's
# ftol=1e-9. 0.1 is large enough to visibly change weights; this is a
# smoke test of the mechanism, not a tuned result.
TURNOVER_PENALTY = 0.1
MAX_WEIGHT = 0.4


def main() -> None:
    print("Loading monthly returns...")
    returns = data.load_monthly_returns()
    rf = data.load_risk_free_rate()
    print(f"Universe: {list(returns.columns)}")
    print(f"Period:   {returns.index.min().date()} -> {returns.index.max().date()}")
    print(f"Months:   {len(returns)}")
    print()

    rows = []
    for method in METHODS:
        print(f"Running {method}...")
        try:
            result = backtest.walk_forward(
                returns,
                method=method,
                train_months=TRAIN_MONTHS,
                test_months=TEST_MONTHS,
                step_months=STEP_MONTHS,
                cost_bps=COST_BPS,
                turnover_penalty=TURNOVER_PENALTY,
                max_weight=MAX_WEIGHT,
            )
        except Exception as e:
            print(f"  FAILED: {e}")
            continue

        gross_sharpe = metrics.annualized_sharpe(result.gross_returns)
        net_sharpe = metrics.annualized_sharpe(result.net_returns, rf_monthly=rf)
        turnover = metrics.realized_annualized_turnover(result.realized_turnover)
        mdd = metrics.max_drawdown(result.net_returns)
        max_w = metrics.max_abs_weight(result.weights)

        rows.append(
            {
                "method": method,
                "gross_sharpe": round(gross_sharpe, 3),
                "net_sharpe": round(net_sharpe, 3),
                "cost_drag": round(gross_sharpe - net_sharpe, 3),
                "annual_turnover": round(turnover, 3),
                "max_drawdown": round(mdd, 3),
                "max_abs_weight": round(max_w, 3),
            }
        )

    df = pd.DataFrame(rows).sort_values("net_sharpe", ascending=False)
    out_path = RESULTS_DIR / "phase1_results.csv"
    df.to_csv(out_path, index=False)

    print()
    print("=" * 70)
    print("Phase 1 results (net Sharpe sorted)")
    print("=" * 70)
    print(df.to_string(index=False))
    print()
    print(f"Saved to {out_path}")

    # ---- Interpret against the framing ----
    print()
    print("Framing check:")
    if "unconstrained_sample_mvo" in df["method"].values and "sample_mvo" in df["method"].values:
        mvo_unc = df[df["method"] == "unconstrained_sample_mvo"].iloc[0]
        mvo_cap = df[df["method"] == "sample_mvo"].iloc[0]
        ew = df[df["method"] == "equal_weight"].iloc[0] if "equal_weight" in df["method"].values else None

        h11 = mvo_unc["max_abs_weight"] > 0.40
        h12 = mvo_cap["annual_turnover"] > 2 * (ew["annual_turnover"] if ew is not None else 1.0)

        print(f"  H1.1 (sample MVO max weight > 0.40): {h11}  (observed: {mvo_unc['max_abs_weight']})")
        print(f"  H1.2 (sample MVO turnover > 2x 1/N): {h12}  (observed: {mvo_cap['annual_turnover']})")
        if not h11 and not h12:
            print("  -> BOTH FAILED. Problem framing may need revision per K2.")
        elif not h11 or not h12:
            print("  -> One passed, one failed. Note which, and proceed with caution.")
        else:
            print("  -> Both passed. Framing not falsified. Proceed to Phase 2.")

    print()
    print("Diagnostic: mean weights per method (top 5 by weight)")
    for method in METHODS:
        try:
            r = backtest.walk_forward(
                returns, method=method,
                train_months=TRAIN_MONTHS, test_months=TEST_MONTHS,
                step_months=STEP_MONTHS, cost_bps=COST_BPS,
                turnover_penalty=TURNOVER_PENALTY, max_weight=MAX_WEIGHT,
            )
            mean_w = r.weights.mean().sort_values(ascending=False)
            top5 = ", ".join(f"{t}={v:.3f}" for t, v in mean_w.head(5).items())
            print(f"  {method:28s} {top5}")
        except Exception as e:
            print(f"  {method:28s} FAILED: {e}")



if __name__ == "__main__":
    main()