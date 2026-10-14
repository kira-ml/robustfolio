"""Long-only mean-variance optimizer via scipy SLSQP.

Constraints: sum(w) = 1, 0 <= w_i <= max_weight.
Optional L1 turnover penalty added to the objective.

This is deliberately simple. When Phase 2 starts, this module is the
one that gets replaced with cvxpy for a proper multi-period formulation.
"""
from __future__ import annotations

import numpy as np
import pandas as pd
from scipy.optimize import minimize


def mean_variance(
    mu: pd.Series,
    cov: pd.DataFrame,
    w_prev: pd.Series | None = None,
    turnover_penalty: float = 0.0,
    max_weight: float = 0.4,
    risk_aversion: float = 1.0,
) -> pd.Series:
    """Long-only mean-variance with optional L1 turnover penalty.

    Objective:  maximize  mu'w - (risk_aversion/2) w'Σw - turnover_penalty * ||w - w_prev||_1
    """
    tickers = mu.index
    n = len(tickers)
    mu_v = mu.values
    cov_v = cov.values
    w_prev_v = w_prev.values if w_prev is not None else np.zeros(n)

    def neg_objective(w: np.ndarray) -> float:
        ret = mu_v @ w
        risk = 0.5 * risk_aversion * (w @ cov_v @ w)
        to = turnover_penalty * np.abs(w - w_prev_v).sum()
        return -(ret - risk - to)

    def grad(w: np.ndarray) -> np.ndarray:
        g = mu_v - risk_aversion * (cov_v @ w)
        if turnover_penalty > 0:
            g = g - turnover_penalty * np.sign(w - w_prev_v)
        return -g

    constraints = [{"type": "eq", "fun": lambda w: w.sum() - 1.0}]
    bounds = [(0.0, max_weight)] * n
    w0 = np.ones(n) / n

    result = minimize(
        neg_objective,
        w0,
        jac=grad,
        method="SLSQP",
        bounds=bounds,
        constraints=constraints,
        options={"ftol": 1e-9, "maxiter": 500},
    )
    if not result.success or not np.all(np.isfinite(result.x)):
        # Fall back to equal weight so the backtest does not silently drop folds.
        w = np.ones(n) / n
    else:
        w = result.x

    return pd.Series(w, index=tickers)