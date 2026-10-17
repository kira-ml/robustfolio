"""Metric definitions of spec §7.1-§7.7, against independent arithmetic.

Every assertion here recomputes the quantity from its formula rather than from
the implementation, so a refactor that keeps the tests green has to keep the
*definition* intact. The two definitional traps are covered explicitly: the rf
series must actually be used (§7.1/§7.5), and lag-1 autocorrelation must be the
correlation of the paired lags (§7.7), not pandas' whole-series-mean variant.
"""

from __future__ import annotations

import numpy as np
import pandas as pd
import pytest
from scipy import stats as sps

from robustfolio import metrics


@pytest.fixture
def months() -> pd.DatetimeIndex:
    return pd.date_range("2015-01-31", periods=24, freq="ME")


def test_sharpe_matches_the_spec_formula(months):
    rng = np.random.default_rng(7)
    r = pd.Series(rng.normal(0.006, 0.04, len(months)), index=months)

    expected = r.mean() / r.std(ddof=1) * np.sqrt(12)

    assert metrics.sharpe(r) == pytest.approx(expected, rel=1e-12)


def test_sharpe_uses_ddof_one_not_ddof_zero(months):
    rng = np.random.default_rng(8)
    r = pd.Series(rng.normal(0.006, 0.04, len(months)), index=months)

    population = r.mean() / r.std(ddof=0) * np.sqrt(12)

    # ddof=1 has the larger denominator, so it reports the smaller Sharpe.
    assert metrics.sharpe(r) != pytest.approx(population, rel=1e-6)
    assert metrics.sharpe(r) < population


def test_sharpe_subtracts_the_risk_free_rate(months):
    rng = np.random.default_rng(10)
    r = pd.Series(rng.normal(0.006, 0.04, len(months)), index=months)
    rf = pd.Series(0.004, index=months)

    excess = r - rf
    expected = excess.mean() / excess.std(ddof=1) * np.sqrt(12)

    assert metrics.sharpe(r, rf) == pytest.approx(expected, rel=1e-12)
    # A 4%/yr risk-free rate is not a rounding error on a 6%/yr mean.
    assert metrics.sharpe(r, rf) != pytest.approx(metrics.sharpe(r), rel=1e-3)


def test_sharpe_of_a_constant_series_is_undefined_not_astronomical(months):
    """A constant series must give nan, not 2e16.

    Summing many copies of a value that is not exactly representable leaves the
    computed mean one ulp off, so ``std`` comes back ~1e-19 rather than 0. The
    guard is therefore on the range, not on the standard deviation.
    """
    r = pd.Series(0.01, index=months, dtype=float)
    rf = pd.Series(0.004, index=months)

    assert np.isnan(metrics.sharpe(r))
    assert np.isnan(metrics.sharpe(r, rf))  # constant excess, zero range


def test_sharpe_drops_unmatched_rf_months_instead_of_substituting_zero(months):
    """Protocol §5.4.6 forbids a zero substitute; §7.1 needs the same rf for both legs."""
    rng = np.random.default_rng(9)
    r = pd.Series(rng.normal(0.006, 0.04, len(months)), index=months)
    rf = pd.Series(0.002, index=months[:18])  # only 18 of 24 months observed

    excess = r.loc[months[:18]] - rf
    expected = excess.mean() / excess.std(ddof=1) * np.sqrt(12)

    assert metrics.sharpe(r, rf) == pytest.approx(expected, rel=1e-12)
    assert metrics.sharpe(r, rf) != pytest.approx(metrics.sharpe(r), rel=1e-9)


def test_sharpe_needs_two_observations():
    assert np.isnan(metrics.sharpe(pd.Series([0.01])))
    assert np.isnan(metrics.sharpe(pd.Series([0.01, 0.01])))  # zero dispersion


def test_annualized_turnover_is_twelve_times_the_mean():
    turnover = pd.Series([0.10, 0.20, 0.30])

    assert metrics.annualized_turnover(turnover) == pytest.approx(12 * 0.20)
    assert metrics.annualized_turnover(turnover) == pytest.approx(turnover.mean() * 12)


def test_annualized_turnover_takes_the_series_not_the_weights():
    """§7.2: the canonical series is the drifted |w(t) - w(t^-)|, computed by the harness.

    This test exists to pin the *interface*: passing a weight frame must fail
    loudly, because a weight frame invites `weights.diff()` -- the Phase 1
    definition §7.2 explicitly deletes.
    """
    weights = pd.DataFrame({"A": [0.5, 0.6], "B": [0.5, 0.4]})

    with pytest.raises((TypeError, ValueError, KeyError, AttributeError)):
        metrics.annualized_turnover(weights)  # type: ignore[arg-type]


def test_max_drawdown_matches_the_compounded_wealth_path():
    r = pd.Series([0.10, -0.20, 0.05])

    wealth = (1 + r).cumprod()
    expected = (wealth / wealth.cummax() - 1).min()

    assert metrics.max_drawdown(r) == pytest.approx(expected, rel=1e-12)
    assert metrics.max_drawdown(r) == pytest.approx(-0.20, rel=1e-12)
    assert metrics.max_drawdown(pd.Series([0.01, 0.02])) == 0.0


def test_cvar_is_the_mean_of_the_worst_ceiling_five_percent():
    r = pd.Series([-0.50, -0.40] + [-0.01] * 38)  # T = 40 -> k = ceil(2.0) = 2

    assert metrics.cvar(r) == pytest.approx((-0.50 + -0.40) / 2)
    assert metrics.cvar(r, level=0.05) == pytest.approx(-0.45)
    # T = 20 -> k = 1
    assert metrics.cvar(r.iloc[:20], level=0.05) == pytest.approx(-0.50)


def test_cost_drag_is_the_sharpe_difference_under_the_same_rf(months):
    rng = np.random.default_rng(11)
    gross = pd.Series(rng.normal(0.008, 0.04, len(months)), index=months)
    drag = pd.Series(rng.gamma(2.0, 0.001, len(months)), index=months)
    net = gross - drag
    rf = pd.Series(0.002, index=months)

    expected = metrics.sharpe(gross, rf) - metrics.sharpe(net, rf)

    assert metrics.cost_drag(gross, net, rf) == pytest.approx(expected, rel=1e-12)


def test_cost_drag_actually_uses_the_rf_series(months):
    """If gross Sharpe omitted rf while net Sharpe included it, this difference would
    measure the rate level. Non-constant drag makes the two legs' dispersions differ,
    which is the case where the rf term cannot cancel."""
    rng = np.random.default_rng(12)
    gross = pd.Series(rng.normal(0.008, 0.04, len(months)), index=months)
    net = gross - pd.Series(rng.gamma(2.0, 0.002, len(months)), index=months)
    rf = pd.Series(0.002, index=months)

    with_rf = metrics.cost_drag(gross, net, rf)
    without_rf = metrics.cost_drag(gross, net, None)

    assert with_rf != pytest.approx(without_rf, rel=1e-9)


def test_skew_kurt_uses_bias_corrected_non_excess_definitions(months):
    rng = np.random.default_rng(13)
    r = pd.Series(rng.normal(0.0, 1.0, len(months)), index=months)

    skew, kurt = metrics.skew_kurt(r)

    assert skew == pytest.approx(float(sps.skew(r, bias=False)), rel=1e-12)
    assert kurt == pytest.approx(float(sps.kurtosis(r, fisher=False, bias=False)), rel=1e-12)
    # The distinction that matters for the PSR denominator: gamma_4 ~ 3, not ~ 0.
    assert 1.0 < kurt < 6.0
    assert kurt != pytest.approx(float(sps.kurtosis(r, fisher=True, bias=False)), rel=1e-6)


def test_autocorr1_is_the_correlation_of_the_paired_lags(months):
    rng = np.random.default_rng(14)
    r = pd.Series(rng.normal(0.0, 0.03, len(months)), index=months)

    expected = float(np.corrcoef(r.to_numpy()[1:], r.to_numpy()[:-1])[0, 1])

    assert metrics.autocorr1(r) == pytest.approx(expected, rel=1e-12)


def test_autocorr1_agrees_with_pandas_autocorr(months):
    """§7.7 writes `corr(r_t, r_{t-1})`; `pandas.Series.autocorr(1)` is
    `self.corr(self.shift(1))`, i.e. exactly that paired Pearson correlation.

    Asserting equality (rather than a difference) is the useful check: it pins
    that our definition is the standard one, and it would catch a switch to a
    formulation that subtracts the whole-series mean from both lags.
    """
    rng = np.random.default_rng(15)
    r = pd.Series(rng.normal(0.05, 0.03, len(months)), index=months)  # non-zero mean

    ours = metrics.autocorr1(r)
    paired = float(np.corrcoef(r.to_numpy()[1:], r.to_numpy()[:-1])[0, 1])

    assert ours == pytest.approx(paired, rel=1e-12)
    assert ours == pytest.approx(float(r.autocorr(1)), rel=1e-12)


def test_autocorr1_needs_three_observations():
    assert np.isnan(metrics.autocorr1(pd.Series([0.01, 0.02])))
