"""PSR, DSR, bootstrap, calibration (spec §7.8-§7.11).

The three things worth testing here are the ones that produce plausible-but-wrong
numbers: a unit slip of sqrt(12) inside an inverse normal, the N = 1 DSR
convention, and a "block bootstrap" that never forms blocks. Each has an exact
test rather than a statistical one wherever an exact one exists.
"""

from __future__ import annotations

import math

import numpy as np
import pandas as pd
import pytest

from robustfolio import metrics, stats
from robustfolio.config import EULER_MASCHERONI, SEED


@pytest.fixture
def excess() -> pd.Series:
    rng = np.random.default_rng(20261017)
    index = pd.date_range("2012-06-30", periods=168, freq="ME")
    return pd.Series(rng.normal(0.004, 0.04, 168), index=index)


# --------------------------------------------------------------------------- #
# Units
# --------------------------------------------------------------------------- #

def test_per_period_sharpe_is_the_annualized_one_over_sqrt_twelve(excess):
    annualized = metrics.sharpe(excess)

    assert stats.per_period_sharpe(excess) == pytest.approx(annualized / math.sqrt(12), rel=1e-12)
    assert stats.annualized_to_per_period(annualized) == pytest.approx(
        stats.per_period_sharpe(excess), rel=1e-12
    )


def test_psr_is_one_half_when_the_benchmark_is_the_estimate(excess):
    """SR* = SR_hat makes the numerator exactly zero, so PSR = Phi(0) = 0.5."""
    sr = stats.per_period_sharpe(excess)

    assert stats.psr(excess, sr) == pytest.approx(0.5, rel=1e-12)


def test_psr_matches_the_spec_formula(excess):
    from scipy import stats as sps

    benchmark = 0.05
    sr = stats.per_period_sharpe(excess)
    gamma3, gamma4 = metrics.skew_kurt(excess)
    argument = 1.0 - gamma3 * sr + (gamma4 - 1.0) / 4.0 * sr * sr
    expected = sps.norm.cdf(
        (sr - benchmark) * math.sqrt(len(excess) - 1) / math.sqrt(argument)
    )

    assert stats.psr(excess, benchmark) == pytest.approx(float(expected), rel=1e-12)


def test_psr_declines_monotonically_as_the_benchmark_rises(excess):
    values = [stats.psr(excess, b) for b in (-0.05, 0.0, 0.05, 0.10)]

    assert values == sorted(values, reverse=True)


def test_psr_refuses_a_non_positive_denominator_instead_of_fabricating(excess, monkeypatch):
    """A negative argument means the moments are inconsistent with the Sharpe.

    Silently returning nan (or clipping to a tiny positive) would fabricate a
    p-value, and this number gates §6.1.
    """
    monkeypatch.setattr("robustfolio.stats.skew_kurt", lambda series: (100.0, 0.0))

    with pytest.raises(ValueError, match="PSR denominator"):
        stats.psr(excess, 0.0)


def test_psr_returns_nan_when_the_moments_are_unavailable():
    assert np.isnan(stats.psr(pd.Series([0.01, 0.02, 0.03]), 0.0))  # T < 4


# --------------------------------------------------------------------------- #
# §7.10 DSR, including the N = 1 convention
# --------------------------------------------------------------------------- #

def test_expected_max_sharpe_is_zero_at_family_size_one():
    """The frozen convention (O6): E[max of one draw] = 0.

    The general formula has no finite N = 1 limit -- its first term is
    Phi^-1(0) = -inf -- so this is the convention doing real work. Without it,
    the DSR would be 0 and §6.1 would reject a method merely for having run once.
    """
    assert stats.expected_max_sharpe(variance=1.0, family_size=1) == 0.0
    assert stats.expected_max_sharpe(variance=0.0, family_size=1) == 0.0


def test_expected_max_sharpe_matches_the_formula_for_n_at_least_two():
    from scipy import stats as sps

    variance, n = 0.0025, 5
    expected = math.sqrt(variance) * (
        (1 - EULER_MASCHERONI) * sps.norm.ppf(1 - 1 / n)
        + EULER_MASCHERONI * sps.norm.ppf(1 - 1 / (n * math.e))
    )

    assert stats.expected_max_sharpe(variance, n) == pytest.approx(float(expected), rel=1e-12)
    assert stats.expected_max_sharpe(variance, n) > stats.expected_max_sharpe(variance, 2)
    assert stats.expected_max_sharpe(variance, n) < math.sqrt(variance) * 3.0  # sane bound


def test_dsr_at_n_one_is_psr_against_zero(excess):
    deflated = stats.dsr(excess, family_size=1)

    assert deflated == pytest.approx(stats.psr(excess, 0.0), rel=1e-12)
    assert stats.dsr_pvalue(deflated) == pytest.approx(1.0 - deflated, rel=1e-12)


def test_dsr_at_n_one_is_weaker_than_psr_against_a_negative_benchmark(excess):
    """SR_0 = 0 is a real hurdle: the DSR must be below a PSR against a *worse* benchmark."""
    assert stats.dsr(excess, family_size=1) < stats.psr(excess, -0.05)


def test_dsr_requires_trial_sharpes_when_the_family_is_larger_than_one(excess):
    with pytest.raises(ValueError, match="trial_sharpes_per_period"):
        stats.dsr(excess, family_size=3)


def test_dsr_rejects_a_trial_set_that_disagrees_with_the_family_size(excess):
    """Protocol §12.6: the denominator and the trial set must be the same thing."""
    with pytest.raises(ValueError, match="trial Sharpes"):
        stats.dsr(excess, family_size=3, trial_sharpes_per_period=pd.Series([0.1, 0.2]))


def test_dsr_with_a_multi_trial_family_uses_the_trial_variance(excess):
    trials = pd.Series([0.04, 0.06, 0.05])
    expected = stats.psr(
        excess, stats.expected_max_sharpe(float(trials.var(ddof=1)), 3)
    )

    assert stats.dsr(excess, family_size=3, trial_sharpes_per_period=trials) == pytest.approx(
        expected, rel=1e-12
    )


# --------------------------------------------------------------------------- #
# §7.11 Stationary block bootstrap
# --------------------------------------------------------------------------- #

def test_bootstrap_indices_have_the_expected_shape_and_range():
    indices = stats.stationary_bootstrap_indices(168, mean_block=6, reps=25, seed=SEED)

    assert indices.shape == (25, 168)
    assert indices.min() >= 0
    assert indices.max() < 168
    assert indices.dtype.kind in "iu"


def test_bootstrap_indices_are_deterministic_for_a_seed_and_differ_across_seeds():
    first = stats.stationary_bootstrap_indices(50, mean_block=6, reps=10, seed=SEED)
    same = stats.stationary_bootstrap_indices(50, mean_block=6, reps=10, seed=SEED)
    other = stats.stationary_bootstrap_indices(50, mean_block=6, reps=10, seed=SEED + 1)

    assert np.array_equal(first, same)
    assert not np.array_equal(first, other)


def test_bootstrap_blocks_are_contiguous_when_restarts_are_effectively_impossible():
    """The exact block logic: with a huge mean block length nothing restarts, so
    every replicate is one contiguous run wrapping at the end of the sample.

    This is the test that a "block bootstrap" which is secretly an IID bootstrap
    cannot pass -- and IID resampling is exactly what §13.2 says must not happen.
    """
    n, reps, mean_block = 50, 20, 1e12
    indices = stats.stationary_bootstrap_indices(n, mean_block=mean_block, reps=reps, seed=SEED)

    expected = (indices[:, [0]] + np.arange(n)[None, :]) % n
    assert np.array_equal(indices, expected)


def test_bootstrap_ci_point_estimate_is_the_statistic_on_the_original_sample():
    sample = pd.Series(np.linspace(0.001, 0.02, 60))

    interval = stats.bootstrap_ci(
        sample, lambda s: float(s.mean()), level=0.9, reps=200, mean_block=6, seed=SEED
    )

    assert interval.point == pytest.approx(float(sample.mean()), rel=1e-12)
    assert interval.low <= interval.point <= interval.high
    assert interval.n_usable == 60
    assert interval.level == 0.90 and interval.reps == 200 and interval.seed == SEED


def test_bootstrap_ci_is_reproducible_and_widens_with_the_level():
    rng = np.random.default_rng(3)
    sample = pd.Series(rng.normal(0.005, 0.04, 120))

    first = stats.bootstrap_ci(sample, lambda s: float(s.mean()), level=0.90, reps=400)
    again = stats.bootstrap_ci(sample, lambda s: float(s.mean()), level=0.90, reps=400)
    wider = stats.bootstrap_ci(sample, lambda s: float(s.mean()), level=0.95, reps=400)

    assert (first.low, first.high) == (again.low, again.high)
    assert wider.low < first.low and wider.high > first.high


def test_bootstrap_ci_reports_how_many_rows_it_actually_used():
    sample = pd.Series([0.01, 0.02, np.nan, 0.03, np.nan, 0.04])

    interval = stats.bootstrap_ci(sample, lambda s: float(s.mean()), reps=100)

    assert interval.n_usable == 4
    assert interval.n == 4


def test_bootstrap_ci_on_a_degenerate_sample_is_nan_rather_than_wrong():
    interval = stats.bootstrap_ci(pd.Series([0.01]), lambda s: float(s.mean()), reps=50)

    assert np.isnan(interval.point) and np.isnan(interval.low)


def test_bootstrap_ci_keeps_dataframe_rows_paired():
    """Rows must stay together: the statistic below is a difference of two paired
    columns, and breaking the pairing would centre it on zero."""
    rng = np.random.default_rng(4)
    a = rng.normal(0.010, 0.02, 150)
    b = rng.normal(0.001, 0.02, 150)
    sample = pd.DataFrame({"a": a, "b": b})

    interval = stats.bootstrap_ci(
        sample, lambda d: float(d["a"].mean() - d["b"].mean()), reps=300
    )

    assert interval.point == pytest.approx(float(a.mean() - b.mean()), rel=1e-12)
    assert interval.low > 0.0, "paired rows were broken if this straddles zero"


# --------------------------------------------------------------------------- #
# §7.8 Calibration (return half)
# --------------------------------------------------------------------------- #

def test_prediction_interval_brackets_the_window_mean_and_covers_about_90_percent():
    rng = np.random.default_rng(5)
    window = pd.Series(rng.normal(0.005, 0.04, 60))

    low, high = stats.prediction_interval(window, level=0.90, reps=500)

    assert low < window.mean() < high
    share_inside = float(((window >= low) & (window <= high)).mean())
    assert 0.80 <= share_inside <= 1.00, "a 90% interval should contain ~90% of the window"


def test_prediction_interval_is_nan_for_a_single_observation():
    low, high = stats.prediction_interval(pd.Series([0.01]), reps=50)

    assert np.isnan(low) and np.isnan(high)


def test_calibration_coverage_is_exact_and_excludes_missing_rows():
    low = pd.Series([0.0, 0.0, 0.0, 0.0], index=[1, 2, 3, 4])
    high = pd.Series([1.0, 1.0, 1.0, 1.0], index=[1, 2, 3, 4])
    realized = pd.Series([0.5, 1.5, np.nan, 0.0], index=[1, 2, 3, 4])

    coverage, hits, usable = stats.calibration_coverage(low, high, realized)

    assert (hits, usable) == (2, 3)
    assert coverage == pytest.approx(2 / 3)


def test_calibration_coverage_is_nan_with_nothing_to_check():
    coverage, hits, usable = stats.calibration_coverage(
        pd.Series(dtype=float), pd.Series(dtype=float), pd.Series(dtype=float)
    )

    assert np.isnan(coverage) and hits == 0 and usable == 0
