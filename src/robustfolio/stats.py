"""Inference layer (spec §7.8-§7.11): PSR, DSR, stationary block bootstrap, calibration.

Everything here answers "how sure are we", and everything here is easy to get
subtly wrong in a way that produces a plausible number. Three traps that this
module handles explicitly rather than by convention:

**PSR and DSR are stated in per-period Sharpe units.** §7.9 says the benchmark
``SR*`` is in per-period units, and the ``sqrt(T-1)`` scaling only makes sense if
``SR_hat`` is too. Annualized values are converted at the boundary
(:func:`annualized_to_per_period`) and never passed in raw, because a factor of
``sqrt(12)`` inside a ``Phi`` is the difference between a p-value of 0.03 and one
of 0.49.

**Skewness and kurtosis come from §7.6, not from a second definition.** The
denominator is ``1 - gamma_3 SR_hat + ((gamma_4 - 1)/4) SR_hat^2`` with ``gamma_4``
**non-excess** and both **bias-corrected**. :func:`robustfolio.metrics.skew_kurt`
is the only place those two moments are computed, and it is imported here.

**The DSR's ``N = 1`` case is a convention, not a formula limit.** §7.10 defines
``SR_0 = sqrt(V) [(1-gamma) Phi^-1(1 - 1/N) + gamma Phi^-1(1 - 1/(N e))]``. At
``N = 1`` the first term is ``Phi^-1(0) = -inf``, so the *formula* diverges; the
frozen note therefore specifies the value directly -- ``V`` = the analytic
estimator variance and "``SR_0`` approximately 0 ... reduces the DSR to a PSR
against zero". :func:`expected_max_sharpe` returns exactly ``0.0`` there and says
why: the expected maximum of one draw from a mean-zero distribution is its mean,
which is zero. Implemented as the note rather than the formula, because the
formula's answer (``DSR = 0``) is not what the note describes and not what §6.1's
decision rule is meant to test.

The bootstrap is the only randomness in the project (spec §10.2). It is seeded
from ``config.SEED`` and the seed is recorded in every run manifest. A fresh
generator is drawn per call from that same seed, so two calls with the same
sample length share their block structure: across methods the confidence
intervals reuse the same resampling. That is a variance-reduction choice
(common random numbers), stated here because it is visible in the numbers.
"""

from __future__ import annotations

import math
from dataclasses import dataclass
from typing import Callable

import numpy as np
import pandas as pd
from scipy import stats as sps

from .config import (
    BOOTSTRAP_BLOCK_MEAN,
    BOOTSTRAP_REPS,
    CI_LEVEL_REPORT,
    DSR_FAMILY_SIZE,
    EULER_MASCHERONI,
    SEED,
)
from .metrics import PERIODS_PER_YEAR, skew_kurt

__all__ = [
    "BootstrapInterval",
    "annualized_to_per_period",
    "bootstrap_ci",
    "calibration_coverage",
    "dsr",
    "dsr_pvalue",
    "expected_max_sharpe",
    "per_period_sharpe",
    "prediction_interval",
    "psr",
    "stationary_bootstrap_indices",
]


# --------------------------------------------------------------------------- #
# Sharpe in the units PSR/DSR are defined in
# --------------------------------------------------------------------------- #

def per_period_sharpe(excess_monthly: pd.Series) -> float:
    """``mean / std(ddof=1)`` of a monthly excess-return series -- **not** annualized.

    This is the quantity PSR and DSR consume (§§7.9-7.10). It is taken on the
    excess series directly, so the caller is responsible for having subtracted
    ``r_f`` already (protocol §2; a zero substitute is forbidden by §5.4.6).

    Guarded on the series' *range* rather than on ``std == 0``, for the reason
    spelled out in :func:`robustfolio.metrics.sharpe`: a constant series can
    compute a standard deviation of ~1e-19 and therefore an absurd Sharpe.
    """
    r = excess_monthly.dropna().astype(float)
    values = r.to_numpy(dtype=float)
    if values.size < 2 or values.max() == values.min():
        return float("nan")
    sd = float(r.std(ddof=1))
    if sd == 0.0 or not np.isfinite(sd):
        return float("nan")
    return float(r.mean() / sd)


def annualized_to_per_period(annualized_sr: float) -> float:
    """Annualized Sharpe -> per-period, by dividing by ``sqrt(12)`` (§7.9).

    Written as a function rather than inline ``/ sqrt(12)`` so that every
    conversion in the project is greppable and there is exactly one of them.
    """
    return float(annualized_sr) / math.sqrt(PERIODS_PER_YEAR)


# --------------------------------------------------------------------------- #
# §7.9 Probabilistic Sharpe ratio
# --------------------------------------------------------------------------- #

def psr(excess_monthly: pd.Series, benchmark_sr_per_period: float) -> float:
    """``Phi((SR_hat - SR*) sqrt(T-1) / sqrt(1 - g3 SR_hat + ((g4-1)/4) SR_hat^2))`` (§7.9).

    ``SR_hat`` is computed from ``excess_monthly`` in per-period units; ``SR*``
    must be in the same units (use :func:`annualized_to_per_period`). ``g3`` and
    ``g4`` are the bias-corrected skewness and non-excess kurtosis of the same
    series (§7.6).

    Raises if the denominator's argument is non-positive. That is not defensive
    padding: a non-positive argument means the third and fourth moments are
    inconsistent with a positive Sharpe, which cannot happen for genuine return
    data and can happen for a misaligned series. A silent ``nan`` or a clipped
    value here would be a fabricated p-value.
    """
    r = excess_monthly.dropna().astype(float)
    n = len(r)
    if n < 2:
        return float("nan")
    sr = per_period_sharpe(r)
    gamma3, gamma4 = skew_kurt(r)
    if not (np.isfinite(sr) and np.isfinite(gamma3) and np.isfinite(gamma4)):
        return float("nan")
    argument = 1.0 - gamma3 * sr + (gamma4 - 1.0) / 4.0 * sr * sr
    if argument <= 0.0:
        raise ValueError(
            f"PSR denominator is non-positive ({argument:.6g}) for SR={sr:.6g}, "
            f"skew={gamma3:.6g}, kurtosis={gamma4:.6g}, T={n}; refusing to report "
            "a p-value from inconsistent moments (spec 7.9)"
        )
    z = (sr - float(benchmark_sr_per_period)) * math.sqrt(n - 1) / math.sqrt(argument)
    return float(sps.norm.cdf(z))


# --------------------------------------------------------------------------- #
# §7.10 Deflated Sharpe ratio
# --------------------------------------------------------------------------- #

def expected_max_sharpe(variance: float, family_size: int) -> float:
    """``SR_0``, the expected maximum Sharpe under ``family_size`` independent trials (§7.10).

    ``sqrt(V) [(1 - gamma) Phi^-1(1 - 1/N) + gamma Phi^-1(1 - 1/(N e))]``.

    ``N = 1`` returns exactly ``0.0`` by the frozen convention: the expected
    maximum of a single draw from a mean-zero distribution is the mean, ``0``.
    The general formula has no finite ``N = 1`` limit (its first term is
    ``Phi^-1(0) = -inf``), so this branch is the convention doing real work
    rather than a numerical courtesy -- and without it the DSR would collapse to
    ``0`` and §6.1 would reject every method for having run once.
    """
    if family_size < 1:
        raise ValueError(f"family_size must be >= 1, got {family_size!r}")
    if family_size == 1:
        return 0.0
    if not np.isfinite(variance) or variance < 0.0:
        raise ValueError(f"variance must be finite and non-negative, got {variance!r}")
    gamma = EULER_MASCHERONI
    first = sps.norm.ppf(1.0 - 1.0 / family_size)
    second = sps.norm.ppf(1.0 - 1.0 / (family_size * math.e))
    return float(math.sqrt(variance) * ((1.0 - gamma) * first + gamma * second))


def dsr(
    excess_monthly: pd.Series,
    *,
    family_size: int = DSR_FAMILY_SIZE,
    trial_sharpes_per_period: pd.Series | None = None,
) -> float:
    """Deflated Sharpe ratio: PSR evaluated at ``SR_0`` (§7.10, protocol §6.1).

    ``V`` is the variance of the family's **per-period** trial Sharpes for
    ``N >= 2`` (required argument there), and the analytic estimator variance
    ``(1 + SR_hat^2 / 2) / T`` for ``N = 1`` (the frozen convention, O6).

    ``V`` is computed and returned for the manifest even in the ``N = 1`` case
    where it does not change the answer, so a future reviewer can see the value
    that the convention bypassed.
    """
    r = excess_monthly.dropna().astype(float)
    n = len(r)
    if n < 2:
        return float("nan")
    sr = per_period_sharpe(r)

    if family_size == 1:
        variance = (1.0 + 0.5 * sr * sr) / n
    else:
        if trial_sharpes_per_period is None:
            raise ValueError(
                f"family_size={family_size} requires trial_sharpes_per_period: V is the "
                "variance of the family's per-period trial Sharpes (spec 7.10)"
            )
        trials = pd.Series(trial_sharpes_per_period).dropna().astype(float)
        if len(trials) != family_size:
            raise ValueError(
                f"family_size={family_size} but {len(trials)} trial Sharpes were supplied; "
                "the multiple-testing denominator and the trial set must agree (protocol 12.6)"
            )
        variance = float(trials.var(ddof=1))

    return psr(r, expected_max_sharpe(variance, family_size))


def dsr_pvalue(deflated: float) -> float:
    """``1 - DSR``, the quantity protocol §6.1 compares against 0.05."""
    return float(1.0 - deflated)


# --------------------------------------------------------------------------- #
# §7.11 Stationary block bootstrap
# --------------------------------------------------------------------------- #

def stationary_bootstrap_indices(
    n: int,
    *,
    mean_block: float = BOOTSTRAP_BLOCK_MEAN,
    reps: int = BOOTSTRAP_REPS,
    seed: int = SEED,
) -> np.ndarray:
    """``(reps, n)`` positional index matrix from the stationary bootstrap (§7.11).

    Politis & Romano (1994): geometric block lengths with mean ``mean_block``, so
    at each step a new block starts with probability ``1 / mean_block`` and
    otherwise the previous position advances by one, wrapping at the end. Rows
    are the replicates, columns the draw positions.

    The implementation is fully vectorised -- restarts are drawn in bulk and the
    "position of the last restart" is a running maximum -- because a Python loop
    over ``reps * n`` (= 336,000 steps per interval) would make a 28-interval
    report crawl for no reason.
    """
    if n < 1:
        raise ValueError(f"n must be >= 1, got {n!r}")
    if mean_block <= 0.0:
        raise ValueError(f"mean_block must be > 0, got {mean_block!r}")
    if reps < 1:
        raise ValueError(f"reps must be >= 1, got {reps!r}")

    rng = np.random.default_rng(seed)
    starts = rng.integers(0, n, size=(reps, n))
    restart = rng.random(size=(reps, n)) < (1.0 / float(mean_block))
    restart[:, 0] = True  # every replicate begins a block

    positions = np.arange(n)
    last_restart = np.maximum.accumulate(
        np.where(restart, positions, -1), axis=1
    )
    offset = positions - last_restart
    base = np.take_along_axis(starts, last_restart, axis=1)
    return (base + offset) % n


@dataclass(frozen=True)
class BootstrapInterval:
    """A percentile bootstrap interval, with everything needed to reproduce it."""

    point: float
    low: float
    high: float
    level: float
    reps: int
    mean_block: float
    seed: int
    n: int
    n_usable: int

    @property
    def width(self) -> float:
        return float(self.high - self.low)

    def __str__(self) -> str:  # pragma: no cover - presentation only
        return (f"{self.point:.4f} [{self.low:.4f}, {self.high:.4f}] "
                f"({self.level:.0%}, B={self.reps})")


def bootstrap_ci(
    sample: pd.Series | pd.DataFrame,
    statistic: Callable[[pd.Series | pd.DataFrame], float],
    *,
    level: float = CI_LEVEL_REPORT,
    reps: int = BOOTSTRAP_REPS,
    mean_block: float = BOOTSTRAP_BLOCK_MEAN,
    seed: int = SEED,
) -> BootstrapInterval:
    """Percentile interval for ``statistic`` under the stationary bootstrap (§7.11).

    ``sample`` is a Series (or a DataFrame whose **rows stay paired** under
    resampling -- so pass ``[returns, rf]`` as two columns rather than two
    arguments when the statistic needs both). Non-finite rows are dropped
    *before* resampling, and the count that survives is reported as
    ``n_usable``: silently bootstrapping a shorter series than the caller thinks
    it passed is how a confidence interval ends up narrower than the data
    justifies.

    The ``point`` estimate is the statistic on the original sample, not the mean
    of the replicates. For a biased statistic those differ, and the report should
    quote the estimate the method actually produced.
    """
    if isinstance(sample, pd.DataFrame):
        usable = sample.replace([np.inf, -np.inf], np.nan).dropna()
    else:
        usable = pd.Series(sample).replace([np.inf, -np.inf], np.nan).dropna()
    usable = usable.reset_index(drop=True)  # position-addressed from here on
    n = len(usable)
    n_usable = int(n)

    if n < 2:
        return BootstrapInterval(
            point=float("nan"), low=float("nan"), high=float("nan"),
            level=float(level), reps=int(reps), mean_block=float(mean_block),
            seed=int(seed), n=int(n), n_usable=n_usable,
        )

    point = float(statistic(usable))
    indices = stationary_bootstrap_indices(n, mean_block=mean_block, reps=reps, seed=seed)
    draws = np.fromiter(
        (statistic(usable.iloc[row]) for row in indices), dtype=float, count=reps
    )
    draws = draws[np.isfinite(draws)]
    if draws.size == 0:
        low = high = float("nan")
    else:
        tail = (1.0 - float(level)) / 2.0
        low, high = np.percentile(draws, [100.0 * tail, 100.0 * (1.0 - tail)])
    return BootstrapInterval(
        point=point, low=float(low), high=float(high),
        level=float(level), reps=int(reps), mean_block=float(mean_block),
        seed=int(seed), n=int(n), n_usable=n_usable,
    )


# --------------------------------------------------------------------------- #
# §7.8 Calibration (return half only -- see finding F24)
# --------------------------------------------------------------------------- #

def prediction_interval(
    trailing_monthly_returns: pd.Series,
    *,
    level: float = CI_LEVEL_REPORT,
    reps: int = BOOTSTRAP_REPS,
    mean_block: float = BOOTSTRAP_BLOCK_MEAN,
    seed: int = SEED,
) -> tuple[float, float]:
    """Bootstrap percentile interval for **one month's** return, from a trailing window.

    The object of the interval is a single month's return, so the draws are the
    pooled resampled *values*, not the resampled *means* -- a mean's interval is
    narrower by ``sqrt(n)`` and would under-cover by construction.

    Honest note: for a one-month horizon the stationary bootstrap's block
    structure affects the dependence of the draws, not their marginal
    distribution, so this interval is very close to the empirical 5th/95th
    percentiles of the window. The bootstrap earns its place here on the
    *volatility* half of §7.8, which is not implemented -- see finding F24.
    """
    values = pd.Series(trailing_monthly_returns).replace([np.inf, -np.inf], np.nan).dropna()
    values = values.reset_index(drop=True)
    n = len(values)
    if n < 2:
        return float("nan"), float("nan")
    indices = stationary_bootstrap_indices(n, mean_block=mean_block, reps=reps, seed=seed)
    draws = values.to_numpy()[indices]          # (reps, n) pooled draws
    tail = (1.0 - float(level)) / 2.0
    low, high = np.percentile(draws, [100.0 * tail, 100.0 * (1.0 - tail)])
    return float(low), float(high)


def calibration_coverage(
    low: pd.Series,
    high: pd.Series,
    realized: pd.Series,
) -> tuple[float, int, int]:
    """Empirical coverage of next-month prediction intervals (§7.8).

    Returns ``(coverage, hits, usable)``. Index-aligned: rows where any of the
    three is missing are excluded from the denominator rather than counted as
    misses -- a missing realisation is not evidence against the model, and
    counting it as such would make coverage depend on data gaps rather than on
    calibration.
    """
    frame = pd.DataFrame(
        {
            "low": pd.Series(low, dtype=float),
            "high": pd.Series(high, dtype=float),
            "realized": pd.Series(realized, dtype=float),
        }
    ).dropna()
    usable = int(len(frame))
    if usable == 0:
        return float("nan"), 0, 0
    hits = int(
        ((frame["realized"] >= frame["low"]) & (frame["realized"] <= frame["high"])).sum()
    )
    return hits / usable, hits, usable
