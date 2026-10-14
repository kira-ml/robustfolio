"""Data loading. Phase 1 uses yfinance with a local Parquet cache.

Caveat (read before trusting results): Yahoo's adjusted close is not a
point-in-time source. It is acceptable for a Phase 1 smoke test whose only
job is to observe whether sample MVO misbehaves. It is NOT acceptable for
any result you intend to publish. See docs/data_contract_and_point_in_time_policy.md.
"""
from __future__ import annotations

from pathlib import Path

import pandas as pd
import yfinance as yf

# A small, liquid, diversifying set of US-listed ETFs.
# 15 tickers; covers equity (US, DM, EM), fixed income (treasuries, credit),
# commodities, real estate, and gold.
DEFAULT_UNIVERSE = [
    "SPY",  # US large-cap equity
    "IWM",  # US small-cap equity
    "EFA",  # Developed ex-US equity
    "EEM",  # Emerging market equity
    "TLT",  # Long-term treasuries
    "IEF",  # Intermediate treasuries
    "SHY",  # Short-term treasuries
    "LQD",  # Investment-grade credit
    "HYG",  # High-yield credit
    "TIP",  # TIPS
    "GLD",  # Gold
    "DBC",  # Broad commodities
    "VNQ",  # US real estate
    "RWX",  # International real estate
    "BIL",  # 1-3 month T-bills (cash proxy)
]

CACHE_DIR = Path(__file__).resolve().parents[2] / "data"


def load_monthly_returns(
    tickers: list[str] | None = None,
    start: str = "2007-01-01",
    end: str | None = None,
    use_cache: bool = True,
) -> pd.DataFrame:
    """Return a DataFrame of monthly simple returns, indexed by month-end.

    Parameters
    ----------
    tickers : list of tickers; defaults to DEFAULT_UNIVERSE.
    start, end : ISO date strings.
    use_cache : if True, read/write a Parquet cache under data/.

    Returns
    -------
    DataFrame of shape (n_months, n_tickers), simple returns (not log).
    """
    tickers = tickers or DEFAULT_UNIVERSE
    CACHE_DIR.mkdir(exist_ok=True)
    cache_file = CACHE_DIR / f"monthly_returns_{start}_{end or 'latest'}.parquet"

    if use_cache and cache_file.exists():
        cached = pd.read_parquet(cache_file)
        if not cached.empty:
            last_period = cached.index[-1].to_period("M")
            now_period = pd.Timestamp.utcnow().tz_localize(None).to_period("M")
            if last_period >= now_period:
                cached = cached.iloc[:-1]
        return cached

    # Download daily adjusted close, then take month-end and diff.
    raw = yf.download(
        tickers,
        start=start,
        end=end,
        auto_adjust=True,   # adjusted for splits and dividends
        progress=False,
    )["Close"]

    # Take last trading day of each month.
    monthly_prices = raw.resample("ME").last()

    # Drop the final row if the month is not yet complete (avoids partial-month
    # lookahead; see evaluation_protocol.md §15).
    if not monthly_prices.empty:
        last_period = monthly_prices.index[-1].to_period("M")
        now_period = pd.Timestamp.utcnow().tz_localize(None).to_period("M")
        if last_period >= now_period:
            monthly_prices = monthly_prices.iloc[:-1]

    monthly_returns = monthly_prices.pct_change().dropna(how="all")

    # Drop any column with too much missing history (Phase 1 requirement).
    min_obs = int(0.9 * len(monthly_returns))
    monthly_returns = monthly_returns.dropna(axis=1, thresh=min_obs)
    monthly_returns = monthly_returns.dropna(how="any")

    monthly_returns.to_parquet(cache_file)
    return monthly_returns


def load_risk_free_rate(start: str = "2007-01-01", end: str | None = None) -> pd.Series:
    """Monthly risk-free rate from 1-month T-bill (BIL total return proxy).

    Phase 1 approximation: use BIL monthly returns as the risk-free rate.
    A stricter implementation reads FRED DGS1MO and converts. Note this.
    """
    bil = load_monthly_returns(tickers=["BIL"], start=start, end=end)
    return bil["BIL"]