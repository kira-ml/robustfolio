"""Covariance and expected-return estimators for Phase 1."""
from __future__ import annotations

import numpy as np
import pandas as pd
from sklearn.covariance import LedoitWolf


def sample_mean(returns: pd.DataFrame) -> pd.Series:
    return returns.mean()


def sample_cov(returns: pd.DataFrame) -> pd.DataFrame:
    return returns.cov()


def ledoit_wolf_cov(returns: pd.DataFrame) -> pd.DataFrame:
    """Ledoit-Wolf shrunk covariance, returned as a DataFrame."""
    lw = LedoitWolf().fit(returns.values)
    return pd.DataFrame(lw.covariance_, index=returns.columns, columns=returns.columns)


def equal_weight(returns: pd.DataFrame) -> pd.Series:
    n = returns.shape[1]
    return pd.Series(np.ones(n) / n, index=returns.columns)


def inverse_vol(returns: pd.DataFrame) -> pd.Series:
    vol = returns.std()
    w = 1.0 / vol
    return w / w.sum()