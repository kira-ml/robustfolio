"""Detect silent SLSQP fallbacks in Phase 1 methods. Zero source changes."""
from __future__ import annotations

import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from robustfolio import backtest, data  # noqa: E402

METHODS = [
    "sample_mvo",
    "unconstrained_sample_mvo",
    "ledoit_wolf_mvo",
    "turnover_penalized_mvo",
]

RETURNS = data.load_monthly_returns()

print(f"Universe: {list(RETURNS.columns)}")
print(f"Months:   {len(RETURNS)}")
print()

for method in METHODS:
    result = backtest.walk_forward(
        RETURNS,
        method=method,
        train_months=60,
        test_months=12,
        step_months=12,
        cost_bps=10.0,
        turnover_penalty=0.1,
        max_weight=0.4,
    )
    n_assets = result.weights.shape[1]
    ew = 1.0 / n_assets
    # Exact-equality check across all columns; tolerance 1e-9.
    deviations = (result.weights - ew).abs().max(axis=1)
    fallbacks = int((deviations < 1e-9).sum())
    total = len(result.weights)
    pct = 100.0 * fallbacks / total if total else 0.0
    print(f"{method:28s} {fallbacks:4d} / {total:4d} fallbacks ({pct:5.1f}%)")