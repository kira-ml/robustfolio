"""Walk-forward backtest loop."""
from __future__ import annotations

from dataclasses import dataclass, field

import numpy as np
import pandas as pd

from . import estimators, optimize


@dataclass
class BacktestResult:
    name: str
    weights: pd.DataFrame = field(default_factory=pd.DataFrame)
    gross_returns: pd.Series = field(default_factory=pd.Series)
    net_returns: pd.Series = field(default_factory=pd.Series)
    turnover: pd.Series = field(default_factory=pd.Series)
    realized_turnover: pd.Series = field(default_factory=pd.Series)


def _rebalance(
    method: str,
    train: pd.DataFrame,
    w_prev: pd.Series | None,
    turnover_penalty: float,
    max_weight: float,
) -> pd.Series:
    if method == "equal_weight":
        return estimators.equal_weight(train)
    if method == "inverse_vol":
        return estimators.inverse_vol(train)

    mu = estimators.sample_mean(train)

    if method == "sample_mvo":
        cov = estimators.sample_cov(train)
        return optimize.mean_variance(mu, cov, w_prev, 0.0, max_weight)
    if method == "unconstrained_sample_mvo":
        cov = estimators.sample_cov(train)
        return optimize.mean_variance(mu, cov, w_prev, turnover_penalty, max_weight=1.0)
    if method == "ledoit_wolf_mvo":
        cov = estimators.ledoit_wolf_cov(train)
        return optimize.mean_variance(mu, cov, w_prev, turnover_penalty, max_weight)
    if method == "turnover_penalized_mvo":
        cov = estimators.sample_cov(train)
        return optimize.mean_variance(
            mu, cov, w_prev, turnover_penalty=turnover_penalty, max_weight=max_weight
        )
    raise ValueError(f"Unknown method: {method}")


def walk_forward(
    returns: pd.DataFrame,
    method: str,
    train_months: int = 60,
    test_months: int = 12,
    step_months: int = 12,
    cost_bps: float = 10.0,
    turnover_penalty: float = 0.0,
    max_weight: float = 0.4,
) -> BacktestResult:
    """Roll forward, rebalancing monthly inside each test window.

    Weights are set at the start of each test month using data strictly
    before that month. Costs are charged on |w_t - w_{t-1}^+| at cost_bps.
    """
    dates = returns.index
    n = len(dates)
    if n < train_months + test_months:
        raise ValueError("Not enough data for the requested windows.")

    all_weights: list[pd.Series] = []
    all_gross: list[pd.Series] = []
    all_net: list[pd.Series] = []
    all_realized_turnover: list[pd.Series] = []

    w_prev: pd.Series | None = None
    prev_month_returns: pd.Series | None = None

    start = train_months
    while start + test_months <= n:
        train = returns.iloc[start - train_months : start]
        test = returns.iloc[start : start + test_months]

        for t in range(test_months):
            month_returns = test.iloc[t]
            w = _rebalance(
                method,
                train if t == 0 else pd.concat([train, test.iloc[:t]]),
                w_prev,
                turnover_penalty,
                max_weight,
            )
            gross = float((w * month_returns).sum())

            if w_prev is None or prev_month_returns is None:
                cost = 0.0
                to = 0.0
            else:
                drifted = w_prev * (1.0 + prev_month_returns)
                drifted = drifted / drifted.sum()
                to = float((w - drifted).abs().sum())
                cost = to * cost_bps / 1e4

            all_weights.append(w.rename(test.index[t]))
            all_gross.append(pd.Series(gross, index=[test.index[t]]))
            all_net.append(pd.Series(gross - cost, index=[test.index[t]]))
            all_realized_turnover.append(pd.Series(to, index=[test.index[t]]))

            prev_month_returns = month_returns
            w_prev = w

        start += step_months

    return BacktestResult(
        name=method,
        weights=pd.DataFrame(all_weights),
        gross_returns=pd.concat(all_gross),
        net_returns=pd.concat(all_net),
        realized_turnover=pd.concat(all_realized_turnover),
    )