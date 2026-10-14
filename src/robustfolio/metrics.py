"""Performance and turnover metrics."""
from __future__ import annotations

import numpy as np
import pandas as pd


def annualized_sharpe(monthly_returns: pd.Series, rf_monthly: pd.Series | None = None) -> float:
    r = monthly_returns.dropna()
    if len(r) < 2 or r.std() == 0:
        return np.nan
    if rf_monthly is not None:
        excess = r - rf_monthly.reindex(r.index).fillna(0.0)
    else:
        excess = r
    return float(excess.mean() / excess.std() * np.sqrt(12))


def annualized_turnover(weights: pd.DataFrame) -> float:
    """One-way annualized turnover: sum |w_t - w_{t-1}^+| per year."""
    deltas = weights.diff().abs().sum(axis=1).dropna()
    if len(deltas) == 0:
        return 0.0
    return float(deltas.mean() * 12)


def max_drawdown(monthly_returns: pd.Series) -> float:
    cum = (1 + monthly_returns.fillna(0)).cumprod()
    peak = cum.cummax()
    dd = (cum - peak) / peak
    return float(dd.min())


def max_abs_weight(weights: pd.DataFrame) -> float:
    return float(weights.abs().max().max())



def realized_annualized_turnover(realized_turnover: pd.Series) -> float:
    """Annualized realized one-way turnover, averaged across rebalances."""
    t = realized_turnover.dropna()
    if len(t) == 0:
        return 0.0
    return float(t.mean() * 12)