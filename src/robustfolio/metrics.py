"""Performance and risk metrics (spec §7.1-§7.7).

One function per metric, each written where §7 puts it, each with exactly one
definition:

===  ==============  ========================================================
§    function        definition
===  ==============  ========================================================
7.1  sharpe          mean(r - rf) / std(r - rf, ddof=1) * sqrt(12)
7.2  turnover        12 * mean_t sum_i |w_i(t) - w_i(t^-)|
7.3  max_drawdown    min_t (W_t / max_{s<=t} W_s - 1), W from net returns
7.4  cvar            mean of the worst ceil(0.05 T) net months
7.5  cost_drag       SR_gross - SR_net under the *same* rf
7.6  skew_kurt       bias-corrected skewness, non-excess kurtosis
7.7  autocorr1       corr(r_t, r_{t-1})
===  ==============  ========================================================

Three deliberate choices, each because the alternative is a silent second
definition:

**Turnover takes the harness's per-month turnover series, not a weight frame.**
§7.2 states plainly that the Phase 1 ``annualized_turnover`` -- which called
``weights.diff()`` and therefore treated pre-rebalance weights as the previous
*post*-rebalance weights -- is deleted, and that only the canonical definition
exists in the rewrite. Drift is computed in exactly one place
(:func:`robustfolio.backtest.drift_weights`; risk R-C01), so taking the weights
here would reintroduce the bug this project already fixed once.
``BacktestResult.annualized_turnover`` delegates to :func:`turnover`, so the
formula ``12 * mean`` is written once.

**A single rf series is threaded through, never defaulted to zero.** §7.1 and
protocol §2 require the *same* ``r_f`` for gross and net, and protocol §5.4.6
forbids a zero substitute. Every function here that needs ``r_f`` takes it as an
argument rather than treating a missing series as zero.

**Covariance of the sample is ``ddof=1`` throughout**, matching §7.1's explicit
``std(..., ddof=1)`` and the §4.2 estimator convention.

``sharpe`` is the one metric that is allowed to decide anything (protocol §2);
everything else here is a diagnostic or a constraint check.
"""

from __future__ import annotations

import numpy as np
import pandas as pd
from scipy import stats as sps

__all__ = [
    "annualized_turnover",
    "autocorr1",
    "cost_drag",
    "cvar",
    "max_drawdown",
    "sharpe",
    "skew_kurt",
]

#: Months per year, for annualizing a monthly Sharpe (§7.1).
PERIODS_PER_YEAR = 12


def sharpe(
    monthly_returns: pd.Series,
    rf_monthly: pd.Series | None = None,
) -> float:
    """Annualized Sharpe of monthly returns, in excess of ``rf_monthly`` (§7.1).

    ``mean(r - r_f) / std(r - r_f, ddof=1) * sqrt(12)``. ``r_f`` is aligned by
    index and is never zero-substituted: a month with no observed ``r_f`` is
    dropped, and if that empties the series the result is ``nan`` rather than a
    number computed against an assumed zero rate (protocol §5.4.6).

    Returns ``nan`` when fewer than two months survive or the excess series has
    zero dispersion. A Sharpe of a constant series is undefined, not infinite,
    and the caller must see that rather than an ``inf`` that propagates.

    The degeneracy test is on the *range*, not on ``std == 0``. Summing 24 copies
    of a value that is not exactly representable leaves the computed mean one ulp
    off the value, so ``std`` comes back as ~1e-19 rather than 0 and this function
    would cheerfully return a Sharpe of 2e16 on a constant series. ``max == min``
    is exact for the genuine case and changes nothing on real data.
    """
    r = monthly_returns.dropna().astype(float)
    if rf_monthly is not None:
        rf = rf_monthly.reindex(r.index)
        keep = r.index[rf.notna()]
        r = r.loc[keep] - rf.loc[keep].astype(float)
    values = r.to_numpy(dtype=float)
    if values.size < 2 or values.max() == values.min():
        return float("nan")
    sd = float(r.std(ddof=1))
    if sd == 0.0 or not np.isfinite(sd):
        return float("nan")
    return float(r.mean() / sd * np.sqrt(PERIODS_PER_YEAR))


def annualized_turnover(monthly_turnover: pd.Series) -> float:
    """``12 * mean_t`` of the one-way portfolio turnover at each rebalance (§7.2).

    The input is the harness's ``turnover`` series, i.e. ``sum_i |w_i(t) -
    w_i(t^-)|`` per rebalance with drift already applied (protocol §5.5.2,
    §5.5.5). This function does no differencing of its own -- that arithmetic
    belongs to the harness and exists in one place.
    """
    series = pd.Series(monthly_turnover).dropna().astype(float)
    if series.empty:
        return float("nan")
    return float(PERIODS_PER_YEAR * series.mean())


def max_drawdown(net_monthly_returns: pd.Series) -> float:
    """Largest peak-to-trough decline in cumulative net return, as a negative number (§7.3).

    Input must be **net** returns: the drawdown is a wealth-path property, and a
    gross wealth path would flatter every method with turnover.
    """
    r = net_monthly_returns.dropna().astype(float)
    if r.empty:
        return float("nan")
    wealth = (1.0 + r).cumprod()
    peak = wealth.cummax()
    return float((wealth / peak - 1.0).min())


def cvar(net_monthly_returns: pd.Series, level: float = 0.05) -> float:
    """Expected shortfall in the worst ``level`` of months, as a monthly return (§7.4).

    With ascending returns ``r_(1) <= ... <= r_(T)`` and ``k = ceil(level * T)``,
    this is ``mean(r_(1), ..., r_(k))`` -- the *empirical* tail mean, not a fitted
    parametric one. Reported as a negative number for a loss.
    """
    r = np.sort(net_monthly_returns.dropna().astype(float).to_numpy())
    if r.size == 0:
        return float("nan")
    k = int(np.ceil(level * r.size))
    k = max(1, min(k, r.size))
    return float(r[:k].mean())


def cost_drag(
    gross_monthly_returns: pd.Series,
    net_monthly_returns: pd.Series,
    rf_monthly: pd.Series | None = None,
) -> float:
    """``SR_gross - SR_net`` under the **same** rf series (§7.5, protocol §2).

    This is the whole point of the frozen convention: if gross Sharpe omitted
    ``r_f`` while net Sharpe included it, this difference would measure the rate
    level as much as the frictions. Both legs are passed the same ``r_f`` here,
    so the difference is attributable to cost alone.
    """
    return sharpe(gross_monthly_returns, rf_monthly) - sharpe(net_monthly_returns, rf_monthly)


def skew_kurt(monthly_returns: pd.Series) -> tuple[float, float]:
    """Bias-corrected skewness and **non-excess** kurtosis (§7.6).

    ``scipy.stats.skew(bias=False)`` and ``scipy.stats.kurtosis(fisher=False,
    bias=False)``. The exact values matter beyond description: they are the
    arguments of the PSR/DSR denominator (§§7.9-§7.10), so a Fisher (excess)
    kurtosis here would shift every PSR by ``(gamma_4 - 1)`` in the wrong place.
    """
    r = monthly_returns.dropna().astype(float)
    if len(r) < 4:
        return float("nan"), float("nan")
    return (
        float(sps.skew(r, bias=False)),
        float(sps.kurtosis(r, fisher=False, bias=False)),
    )


def autocorr1(monthly_returns: pd.Series) -> float:
    """Lag-1 autocorrelation ``corr(r_t, r_{t-1})`` of net monthly returns (§7.7).

    Pearson correlation of the paired series, which is what §7.7's formula says.
    This coincides with ``pandas.Series.autocorr(1)``, and the test suite pins
    that equality rather than asserting a difference: pandas implements
    ``autocorr`` as ``self.corr(self.shift(lag))``, i.e. exactly this paired
    Pearson correlation, so there is no whole-series-mean variant to diverge from.
    """
    r = monthly_returns.dropna().astype(float)
    if len(r) < 3:
        return float("nan")
    current = r.to_numpy()[1:]
    lagged = r.to_numpy()[:-1]
    if current.std(ddof=1) == 0.0 or lagged.std(ddof=1) == 0.0:
        return float("nan")
    return float(np.corrcoef(current, lagged)[0, 1])
