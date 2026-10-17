"""Expected-return and covariance estimators (spec §4).

All estimators take a ``T x N`` frame of monthly **simple** returns over the
estimation window and return μ (an ``N``-vector) and/or Σ (an ``N x N`` matrix).
Columns are sorted lexicographically by the caller; no estimator may see data
after *t*.

Two members of the method set differ from B3 in exactly one component by design
(spec §1, "Design rule"): M1 differs only in Σ, M2 differs only in μ. That is
what makes H2.1 and H2.2 single-factor tests rather than confounded ones, so the
estimators below must not quietly change anything else.

**Known defect, recorded not hidden (finding F16).** ``sklearn``'s
``LedoitWolf`` builds on the maximum-likelihood empirical covariance
(``ddof=0``), whereas spec §4.2 pins the sample covariance to ``ddof=1``
("matching ``pandas.DataFrame.cov``"). M1's Σ therefore differs from B3's by the
shrinkage *and* by a factor ``T/(T-1)`` in its base. At ``T = 60`` that is a
1.7% uniform scale difference. It is left as specified (the spec names the
sklearn estimator) and must not be silently "corrected"; see the note in
``ledoit_wolf_cov``.
"""

from __future__ import annotations

import numpy as np
import pandas as pd
from sklearn.covariance import LedoitWolf

from .config import GAMMA

__all__ = [
    "sample_mean",
    "sample_cov",
    "ledoit_wolf_cov",
    "ledoit_wolf_shrinkage",
    "equilibrium_returns",
    "black_litterman_returns",
    "equal_weight",
    "inverse_vol",
]


def _as_matrix(returns: pd.DataFrame) -> tuple[np.ndarray, list[str]]:
    if not isinstance(returns, pd.DataFrame):
        raise TypeError("estimators take a pandas DataFrame of monthly returns")
    if returns.isna().any().any():
        raise ValueError(
            "estimator received NaN: gaps must be resolved by the data layer "
            "(spec §3.3), never by an estimator"
        )
    if len(returns) < 2:
        raise ValueError(f"need at least 2 observations, got {len(returns)}")
    return returns.to_numpy(dtype=float), list(returns.columns)


# --------------------------------------------------------------------------- #
# Expected returns
# --------------------------------------------------------------------------- #

def sample_mean(returns: pd.DataFrame) -> pd.Series:
    """Arithmetic mean of monthly simple returns (spec §4.1). Used by B3, B5, M1."""
    _as_matrix(returns)  # reject gaps here rather than averaging over them
    return returns.mean()


def equilibrium_returns(
    cov: pd.DataFrame | np.ndarray,
    gamma: float = GAMMA,
    w_ref: np.ndarray | None = None,
) -> pd.Series:
    """Reverse-optimised equilibrium excess returns, ``Pi = gamma * Sigma * w_ref``.

    ``w_ref`` is the equal-weight vector because the MVP has no
    capitalisation weights (spec §4.4). ``Pi`` is in monthly excess-return units.
    """
    sigma, names = _cov_arrays(cov)
    n = sigma.shape[0]
    if w_ref is None:
        w_ref = np.full(n, 1.0 / n, dtype=float)
    w_ref = np.asarray(w_ref, dtype=float)
    if w_ref.shape != (n,):
        raise ValueError(f"w_ref must have shape ({n},), got {w_ref.shape}")
    return pd.Series(gamma * (sigma @ w_ref), index=names)


def black_litterman_returns(
    sample_mean: pd.Series,
    cov: pd.DataFrame | np.ndarray,
    gamma: float = GAMMA,
) -> pd.Series:
    """No-views Black-Litterman posterior (spec §4.5).

    With the view matrix ``P = I``, view returns ``Q = mu_hat``, prior covariance
    ``tau * Sigma`` and view uncertainty ``Omega = tau * Sigma``, the posterior is

        mu_BL = [(tau S)^-1 + (tau S)^-1]^-1 [(tau S)^-1 Pi + (tau S)^-1 Q]
              = (Pi + mu_hat) / 2

    The closed form is used deliberately: it removes solver and tuning ambiguity.
    ``tau = 1/T`` cancels identically, so it does not appear as a parameter --
    the honest characterisation, which reporting language must use, is
    "Bayesian shrinkage of the sample mean exactly halfway toward the
    equilibrium prior", not "alpha from views" (spec §4.5).
    """
    sigma, names = _cov_arrays(cov)
    mu = _as_series(sample_mean, names, "sample_mean")
    prior = equilibrium_returns(
        pd.DataFrame(sigma, index=names, columns=names), gamma=gamma
    )
    posterior = 0.5 * (prior + mu)
    if posterior.isna().any():
        # A label mismatch between mu and the covariance silently produces an
        # all-NaN posterior under pandas alignment. Refuse rather than emit it.
        raise ValueError(
            "black_litterman_returns produced NaN: mu and cov labels do not "
            "align (spec §4 fixes a single column ordering)"
        )
    return posterior


# --------------------------------------------------------------------------- #
# Covariance
# --------------------------------------------------------------------------- #

def sample_cov(returns: pd.DataFrame) -> pd.DataFrame:
    """Unbiased sample covariance, ``ddof=1`` (spec §4.2).

    Used by B2, B3, B4, B5, M2. Condition number is logged per fold as a
    diagnostic for Test C (risk R-E04).

    Gaps are rejected rather than skipped: ``DataFrame.cov`` silently drops NaN
    pairs, which would quietly change the sample behind each entry and therefore
    the effective estimation window. Spec §3.3 puts gap resolution in the data
    layer, so a NaN reaching here is a bug, not an input.
    """
    _as_matrix(returns)
    return returns.cov()


def _fit_ledoit_wolf(returns: pd.DataFrame):
    values, names = _as_matrix(returns)
    fitted = LedoitWolf().fit(values)
    return fitted, names


def ledoit_wolf_cov(returns: pd.DataFrame) -> pd.DataFrame:
    """Ledoit-Wolf shrunk covariance, constant-variance target (spec §4.3).

    Resolves O2: the MVP uses ``sklearn.covariance.LedoitWolf`` (Ledoit & Wolf,
    2004), whose target is ``F = sigma_bar^2 * I`` with
    ``sigma_bar^2 = tr(Sigma_hat) / N`` and the analytically optimal intensity.
    The constant-correlation target (Ledoit & Wolf, 2003) is a registered
    variant, not MVP.

    Note (finding F16): sklearn's base empirical covariance uses ``ddof=0``,
    unlike spec §4.2's ``ddof=1``. See the module docstring; the discrepancy is
    recorded rather than silently adjusted.

    The fitted intensity is available from :func:`ledoit_wolf_shrinkage` and is
    recorded per fold in the results.
    """
    fitted, names = _fit_ledoit_wolf(returns)
    return pd.DataFrame(fitted.covariance_, index=names, columns=names)


def ledoit_wolf_shrinkage(returns: pd.DataFrame) -> float:
    """The fitted Ledoit-Wolf intensity ``delta in [0, 1]`` (spec §4.3, O2).

    "The fitted delta (per fold) is recorded in the results"; this is the accessor
    for that record. It refits, so callers that need both the matrix and the
    intensity should call :func:`ledoit_wolf_cov` and this function together and
    accept the redundant fit (the matrices are 60 x 18; the cost is nil).
    """
    fitted, _ = _fit_ledoit_wolf(returns)
    return float(fitted.shrinkage_)


# --------------------------------------------------------------------------- #
# Constructors that need no estimator
# --------------------------------------------------------------------------- #

def equal_weight(returns: pd.DataFrame) -> pd.Series:
    """B1: ``w_i = 1/N`` (spec §5.2). No inputs, no solver."""
    n = returns.shape[1]
    if n == 0:
        raise ValueError("cannot form equal weights from an empty universe")
    return pd.Series(np.full(n, 1.0 / n), index=list(returns.columns))


def inverse_vol(returns: pd.DataFrame) -> pd.Series:
    """Inverse-volatility weights.

    **Not part of the MVP method set** (spec §1, "Not in MVP"): it is retained
    only as an extension candidate and must not appear in the MVP comparison
    table (DEC-20261017-019 F2).
    """
    vol = returns.std()
    if (vol <= 0).any():
        raise ValueError("inverse_vol requires strictly positive volatilities")
    w = 1.0 / vol
    return w / w.sum()


# --------------------------------------------------------------------------- #
# Helpers
# --------------------------------------------------------------------------- #

def _cov_arrays(cov: pd.DataFrame | np.ndarray) -> tuple[np.ndarray, list[str]]:
    if isinstance(cov, pd.DataFrame):
        if not cov.index.equals(cov.columns):
            raise ValueError("covariance frame must have identical row and column labels")
        return cov.to_numpy(dtype=float), list(cov.index)
    arr = np.asarray(cov, dtype=float)
    if arr.ndim != 2 or arr.shape[0] != arr.shape[1]:
        raise ValueError(f"covariance must be square, got shape {arr.shape}")
    return arr, [str(i) for i in range(arr.shape[0])]


def _as_series(value: pd.Series, names: list[str], what: str) -> pd.Series:
    if not isinstance(value, pd.Series):
        raise TypeError(f"{what} must be a pandas Series")
    if list(value.index) != list(names):
        raise ValueError(
            f"{what} index does not match the covariance labels; the method set "
            "requires a single column ordering (spec §4)"
        )
    return value.astype(float)
