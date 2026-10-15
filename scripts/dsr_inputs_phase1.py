"""Compute DSR inputs from Phase 1's already-run return series.

Not an experiment. Not registered. Does not add to the multiple-testing
denominator. Output is illustrative input for the freeze session's
specification of evaluation_protocol.md §12.1 and §6.1.

See DEC-20261015-012 (Phase 1 exploratory) and DEC-20261015-015 (findings).
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

import numpy as np
import pandas as pd
from scipy import stats

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from robustfolio import backtest, data  # noqa: E402

METHODS = [
    "equal_weight",
    "inverse_vol",
    "sample_mvo",
    "unconstrained_sample_mvo",
    "ledoit_wolf_mvo",
    "turnover_penalized_mvo",
]

RETURNS = data.load_monthly_returns()
RF = data.load_risk_free_rate()

series: dict[str, pd.Series] = {}
for m in METHODS:
    r = backtest.walk_forward(
        RETURNS,
        method=m,
        train_months=60,
        test_months=12,
        step_months=12,
        cost_bps=10.0,
        turnover_penalty=0.1,
        max_weight=0.4,
    )
    series[m] = r.net_returns

per_method: dict[str, dict] = {}
for m, r in series.items():
    excess = r - RF.reindex(r.index).fillna(0.0)
    T = len(excess)
    sr_m = float(excess.mean() / excess.std())            # monthly SR
    per_method[m] = {
        "T_months": int(T),
        "SR_monthly": round(sr_m, 6),
        "SR_ann": round(sr_m * np.sqrt(12), 4),
        "skew": round(float(stats.skew(excess)), 4),
        "kurtosis_raw": round(float(stats.kurtosis(excess, fisher=False)), 4),
    }

# V[{SR_n}] across methods (Eq. 2 input)
sr_vec = np.array([per_method[m]["SR_monthly"] for m in METHODS])
V_SR = float(np.var(sr_vec, ddof=1))

# Average pairwise correlation of net returns (Eq. 8 input for N_hat)
rets_df = pd.DataFrame(series)
corr = rets_df.corr()
M = len(METHODS)
mask = np.triu(np.ones_like(corr.values, dtype=bool), k=1)
rho_hat = float(np.mean(corr.values[mask]))
N_hat = rho_hat + (1.0 - rho_hat) * M

output = {
    "note": (
        "Illustrative DSR inputs from exploratory Phase 1. "
        "Not a confirmatory result. See DEC-20261015-012, -015."
    ),
    "methods": per_method,
    "M_trials_raw": M,
    "V_of_SR_monthly": V_SR,
    "average_pairwise_corr": round(rho_hat, 4),
    "N_hat_implied_independent": round(N_hat, 4),
}

out_path = Path(__file__).resolve().parents[1] / "notes" / "dsr_inputs_phase1.json"
out_path.parent.mkdir(exist_ok=True)
out_path.write_text(json.dumps(output, indent=2))

print(json.dumps(output, indent=2))
print(f"\nSaved to {out_path}")