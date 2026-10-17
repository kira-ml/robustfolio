"""Point-in-time data layer for robustfolio.

Implements ``model_and_method_spec.md`` §3 (data pipeline) on top of the frozen
data contract in ``evaluation_protocol.md`` §5.4.

Design rules
------------
* **Snapshot in, nothing else.** A confirmatory run reads an immutable snapshot
  directory; :func:`load_snapshot` is the only entry point and never touches the
  network (protocol §5.4.9).
* **Point-in-time or nothing.** Every value derived at ``t`` uses only rows dated
  ``<= t`` and only corporate actions whose ``ex_date <= t`` (protocol §5.4.3,
  §5.4.4). The §5.4.8 leakage suite verifies this.
* **Vendor isolation.** All vendor-specific code lives in the
  ``VENDOR ADAPTERS`` block (protocol §5.4.1). Downstream code takes a
  :class:`Snapshot` and cannot reach the network.

Corporate-action conventions (protocol §5.4.5)
----------------------------------------------
* **Split** — historical prices before the ex-date are divided by the split
  ratio, so the price series is internally consistent
  ("adjust historical prices and shares point-in-time").
* **Cash dividend** — added to the *return* on its ex-date; the price level is
  **not** back-adjusted for dividends ("do not adjust price retroactively for
  return calculation"). A dividend is quoted in the price basis of its ex-date,
  so it is divided by the product of split ratios strictly after that ex-date.
* **Merger / delisting** — terminates the series. No confirmed candidate delists
  in-sample (protocol §5.4.5), so this path is implemented but unexercised.

Implementation conventions (flagged, not silently chosen)
---------------------------------------------------------
Two constants are *not* pinned by the frozen documents. The chosen defaults are
recorded in every snapshot manifest and raised for confirmation in the decision
log (findings **F10** and **F11**):

* :data:`RF_ANNUAL_TO_MONTHLY` — the annualised-yield-to-monthly conversion.
* :data:`RF_ALIGN` — whether the yield observed at the end of month ``t`` or of
  month ``t-1`` prices the return of month ``t``.
"""

from __future__ import annotations

import hashlib
import json
import warnings
from dataclasses import dataclass, field
from pathlib import Path
from typing import Iterable

import numpy as np
import pandas as pd

# --------------------------------------------------------------------------- #
# Paths and frozen parameters
# --------------------------------------------------------------------------- #

REPO_ROOT = Path(__file__).resolve().parents[2]
DATA_DIR = REPO_ROOT / "data"
SNAPSHOTS_DIR = DATA_DIR / "snapshots"
CACHE_DIR = DATA_DIR / "cache"

#: Source of the confirmed candidate list (``notes/pit_universe_2026-10-17.md``,
#: v1.0 Confirmed, DEC-20261017-024). Copied into every snapshot as
#: ``universe_pit.csv``.
DEFAULT_UNIVERSE_CSV = REPO_ROOT / "notes" / "pit_candidates_2026-10-17.csv"

SNAPSHOT_SCHEMA_VERSION = 1

#: protocol §5.4.2 — trailing-3-month average daily dollar volume floor.
ADV_MIN_USD = 5.0e6
ADV_WINDOW_MONTHS = 3
#: protocol §5.4.2 — consecutive valid months required at entry.
MIN_HISTORY_MONTHS = 60
#: protocol §5.4.6 — forward-fill limit for isolated missing days.
MAX_FFILL_DAYS = 3

#: Finding F10 (unpinned by the frozen docs). ``"geometric"`` = (1+y)^(1/12)-1;
#: ``"simple"`` = y/12. Geometric is compounding-consistent at monthly horizons.
RF_ANNUAL_TO_MONTHLY = "geometric"
#: Finding F11. ``"prior_month"`` uses the yield observed at the last trading day
#: of month ``t-1`` to price month ``t`` (no-lookahead, consistent with §5.5.4
#: execution timing). ``"same_month"`` uses the month-``t`` observation, the
#: literal reading of §5.5.5 "as observed at t".
RF_ALIGN = "prior_month"


class SnapshotError(RuntimeError):
    """Raised when a snapshot is missing, corrupt, or internally inconsistent."""


# --------------------------------------------------------------------------- #
# VENDOR ADAPTERS (protocol §5.4.1 — the only place vendor specifics may appear)
# --------------------------------------------------------------------------- #

VENDOR_SOURCES = {
    "prices": "Yahoo Finance via yfinance (auto_adjust=False, actions=True)",
    "rf": "FRED DGS1MO (https://fred.stlouisfed.org/graph/fredgraph.csv?id=DGS1MO)",
}

_PRICE_FIELDS = ("open", "high", "low", "close", "volume")

#: Snapshot field name -> yfinance column name (vendor translation lives here).
_YAHOO_FIELDS = {
    "open": "Open",
    "high": "High",
    "low": "Low",
    "close": "Close",
    "volume": "Volume",
}


def fetch_yahoo_raw(
    tickers: Iterable[str], start: str, end: str | None = None
) -> tuple[pd.DataFrame, pd.DataFrame]:
    """Return raw (unadjusted) daily OHLCV and the corporate-action history.

    Returns
    -------
    prices : DataFrame
        Daily index, columns ``MultiIndex(field, ticker)`` with
        ``field in {open, high, low, close, volume}``. **Unadjusted**: no split
        or dividend adjustment has been applied (protocol §5.4.4 step 1).
    actions : DataFrame
        Long frame with columns ``ticker, ex_date, kind, value`` where ``kind``
        is ``"split"`` (``value`` = ratio) or ``"dividend"`` (``value`` = cash
        per share) (protocol §5.4.4 step 2).
    """
    import yfinance as yf

    tickers = list(tickers)
    raw = yf.download(
        tickers,
        start=start,
        end=end,
        auto_adjust=False,
        actions=True,
        progress=False,
        group_by="ticker",
        threads=True,
    )
    if raw is None or raw.empty:
        raise SnapshotError(f"Yahoo returned no data for {tickers} ({start}..{end})")

    if not isinstance(raw.columns, pd.MultiIndex):
        raw.columns = pd.MultiIndex.from_product([[tickers[0]], raw.columns])
    raw.columns = raw.columns.set_names(["ticker", "field"])

    idx = pd.DatetimeIndex(raw.index)
    if idx.tz is not None:
        idx = idx.tz_localize(None)
    raw.index = idx.normalize()
    raw.index.name = "date"

    available = set(raw.columns.get_level_values("field"))
    missing = [y for y in _YAHOO_FIELDS.values() if y not in available]
    if missing:
        raise SnapshotError(f"Yahoo payload missing price fields: {sorted(missing)}")

    prices = pd.concat(
        {field: raw.xs(column, level="field", axis=1)
         for field, column in _YAHOO_FIELDS.items()},
        axis=1,
    )
    prices.columns = prices.columns.set_names(["field", "ticker"])
    prices = prices.sort_index(axis=1)

    actions = _extract_actions(raw, list(raw.columns.get_level_values("ticker").unique()))
    return prices, actions


def _extract_actions(raw: pd.DataFrame, tickers: list[str]) -> pd.DataFrame:
    rows: list[dict] = []
    for ticker in sorted(set(tickers)):
        for field, kind in (("Stock Splits", "split"), ("Dividends", "dividend")):
            try:
                series = raw.xs(field, level="field", axis=1)[ticker]
            except KeyError:
                continue
            series = pd.to_numeric(series, errors="coerce").fillna(0.0)
            for date, value in series[series != 0].items():
                if not np.isfinite(value):
                    continue
                rows.append(
                    {"ticker": ticker, "ex_date": pd.Timestamp(date), "kind": kind,
                     "value": float(value)}
                )
    out = pd.DataFrame(rows, columns=["ticker", "ex_date", "kind", "value"])
    if not out.empty:
        out = out.sort_values(["ticker", "ex_date", "kind"]).reset_index(drop=True)
    return out


def fetch_fred_dgs1mo(start: str, end: str | None = None) -> pd.DataFrame:
    """Return the FRED ``DGS1MO`` daily series (percent per annum).

    FRED marks non-observations with ``"."``; those rows are dropped rather than
    imputed (protocol §5.4.6 forbids substituting zero).
    """
    import requests

    url = "https://fred.stlouisfed.org/graph/fredgraph.csv?id=DGS1MO"
    resp = requests.get(url, timeout=60)
    resp.raise_for_status()
    from io import StringIO

    frame = pd.read_csv(StringIO(resp.text))
    frame.columns = ["date", "dgs1mo"]
    frame["date"] = pd.to_datetime(frame["date"], errors="coerce")
    frame["dgs1mo"] = pd.to_numeric(frame["dgs1mo"], errors="coerce")
    frame = frame.dropna(subset=["date"]).dropna(subset=["dgs1mo"])
    if start is not None:
        frame = frame[frame["date"] >= pd.Timestamp(start)]
    if end is not None:
        frame = frame[frame["date"] <= pd.Timestamp(end)]
    return frame.sort_values("date").reset_index(drop=True)


def cache_key(*parts: object) -> str:
    """Content-addressed key for the development cache (protocol §5.4.9)."""
    blob = json.dumps(parts, sort_keys=True, default=str)
    return hashlib.sha256(blob.encode("utf-8")).hexdigest()[:16]


# --------------------------------------------------------------------------- #
# Snapshot
# --------------------------------------------------------------------------- #

PRICE_FILE = "prices_raw.parquet"
ACTIONS_FILE = "actions.parquet"
RF_FILE = "rf_dgs1mo.parquet"
UNIVERSE_FILE = "universe_pit.csv"
QUALITY_FILE = "quality_report.md"
MANIFEST_FILE = "manifest.json"

SNAPSHOT_FILES = (PRICE_FILE, ACTIONS_FILE, RF_FILE, UNIVERSE_FILE, QUALITY_FILE)


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as fh:
        for chunk in iter(lambda: fh.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


@dataclass
class Snapshot:
    """An immutable, point-in-time data bundle (spec §3.1).

    Treat every attribute as read-only: the on-disk directory is never modified
    after creation (protocol §5.4.9). ``_cache`` memoises derived frames only.
    """

    snapshot_id: str
    path: Path
    prices_raw: pd.DataFrame
    actions: pd.DataFrame
    rf_daily: pd.DataFrame
    universe: pd.DataFrame
    quality_report: str = ""
    manifest: dict = field(default_factory=dict)
    _cache: dict = field(default_factory=dict, repr=False)

    # -- membership ------------------------------------------------------- #

    @property
    def tickers(self) -> list[str]:
        """Candidate members, lexicographically sorted (spec §4 column order)."""
        return sorted(self.universe["ticker"].astype(str).tolist())

    def members_at(self, t) -> list[str]:
        """Candidates whose membership window covers ``t`` (protocol §5.4.7)."""
        t = pd.Timestamp(t)
        uni = self.universe
        first = pd.to_datetime(uni["first_eligible"])
        keep = first <= t
        last = pd.to_datetime(uni["last_eligible"], errors="coerce")
        keep &= last.isna() | (last >= t)
        return [x for x in uni.loc[keep, "ticker"].astype(str).tolist()]

    def listed_until(self, ticker: str):
        """Delisting date for ``ticker``, or ``None`` if still listed."""
        row = self.universe.loc[self.universe["ticker"] == ticker]
        if row.empty:
            return None
        value = row["last_eligible"].iloc[0]
        return None if pd.isna(value) or value == "" else pd.Timestamp(value)

    # -- raw accessors ---------------------------------------------------- #

    def _field(self, name: str) -> pd.DataFrame:
        key = ("field", name)
        if key not in self._cache:
            frame = self.prices_raw.xs(name, level="field", axis=1)
            self._cache[key] = frame.reindex(columns=self.tickers)
        return self._cache[key]

    def close_raw(self) -> pd.DataFrame:
        """Unadjusted daily closes, one column per candidate ticker."""
        return self._field("close")

    def volume_raw(self) -> pd.DataFrame:
        """Unadjusted daily share volume, one column per candidate ticker."""
        return self._field("volume")

    def daily_close_filled(self) -> pd.DataFrame:
        """Raw closes with isolated gaps forward-filled <= 3 days (§5.4.6)."""
        key = ("ffill",)
        if key not in self._cache:
            self._cache[key] = self.close_raw().ffill(limit=MAX_FFILL_DAYS)
        return self._cache[key]

    # -- point-in-time reconstruction (§3.2) ------------------------------ #

    def truncated(self, t) -> "Snapshot":
        """A view of this snapshot containing only what was knowable at ``t``.

        This is the operational form of the point-in-time rule (protocol §5.4.3):
        prices, corporate actions and the risk-free series are all cut at ``t``.
        The §5.4.8 leakage suite asserts that every derived value at ``t`` is
        identical whether it is computed from this snapshot or from its
        truncation — if it is not, something after ``t`` leaked in.
        """
        cutoff = pd.Timestamp(t)
        actions = self.actions
        if not actions.empty:
            actions = actions[actions["ex_date"] <= cutoff]
        rf = self.rf_daily
        if not rf.empty and "date" in rf.columns:
            rf = rf[rf["date"] <= cutoff]
        return Snapshot(
            snapshot_id=f"{self.snapshot_id}@<={cutoff.date().isoformat()}",
            path=self.path,
            prices_raw=self.prices_raw.loc[:cutoff],
            actions=actions,
            rf_daily=rf,
            universe=self.universe,
            quality_report=self.quality_report,
            manifest=self.manifest,
        )

    def adjusted_prices(self, t=None) -> pd.DataFrame:
        """Split-adjusted daily closes using **only** actions with ex_date <= t.

        The price level is not dividend-adjusted: cash dividends enter the
        return on their ex-date (§5.4.5). Returns computed from this frame are
        invariant to splits after ``t`` (the factor cancels in the ratio), which
        is what the §5.4.8 adjusted-price test checks.
        """
        cutoff = pd.Timestamp(t) if t is not None else None
        key = ("adj", cutoff)
        if key in self._cache:
            return self._cache[key]

        close = self.close_raw()
        if cutoff is not None:
            close = close.loc[:cutoff]
        out = close.copy()

        splits = self.actions[self.actions["kind"] == "split"] if not self.actions.empty \
            else self.actions
        if cutoff is not None and not splits.empty:
            splits = splits[splits["ex_date"] <= cutoff]
        for row in splits.itertuples(index=False):
            if row.ticker not in out.columns:
                continue
            ratio = float(row.value)
            if not np.isfinite(ratio) or ratio <= 0:
                continue
            mask = out.index < row.ex_date
            out.loc[mask, row.ticker] = out.loc[mask, row.ticker] / ratio

        self._cache[key] = out
        return out

    def _adjusted_dividends(self, cutoff=None) -> pd.DataFrame:
        """Dividends in the price basis of ``cutoff`` (columns ``ticker, ex_date, value``)."""
        if self.actions.empty:
            return self.actions.copy()
        div = self.actions[self.actions["kind"] == "dividend"].copy()
        splits = self.actions[self.actions["kind"] == "split"].copy()
        if cutoff is not None:
            div = div[div["ex_date"] <= cutoff]
            splits = splits[splits["ex_date"] <= cutoff]
        if div.empty:
            return div
        ratios = []
        for row in div.itertuples(index=False):
            after = splits[(splits["ticker"] == row.ticker) & (splits["ex_date"] > row.ex_date)]
            factor = float(np.prod(after["value"].to_numpy())) if len(after) else 1.0
            ratios.append(row.value / factor if factor else row.value)
        div = div.assign(value=ratios)
        return div

    # -- monthly series --------------------------------------------------- #

    def monthly_prices(self, cutoff=None, ffill: bool = True) -> pd.DataFrame:
        """Month-end prices (calendar month-end index), one column per member.

        Prices are **split-adjusted** point-in-time (spec §3.2) and isolated
        missing days are forward-filled up to the §5.4.6 limit.
        """
        adjusted = self.adjusted_prices(cutoff)
        frame = adjusted.ffill(limit=MAX_FFILL_DAYS) if ffill else adjusted
        out = frame.resample("ME").last()
        return out.reindex(columns=self.tickers)

    def monthly_total_returns(self, cutoff=None) -> pd.DataFrame:
        """Monthly **simple total returns** (dividends on their ex-date).

        ``r_m = (P_m + D_m) / P_{m-1} - 1`` on the split-adjusted basis, where
        ``D_m`` sums the (split-basis) dividends with ex-date inside month ``m``.
        """
        key = ("mret", pd.Timestamp(cutoff) if cutoff is not None else None)
        if key in self._cache:
            return self._cache[key]

        prices = self.monthly_prices(cutoff=cutoff).copy()
        prices.index = prices.index.to_period("M")

        div = self._adjusted_dividends(cutoff)
        if div.empty:
            cash = pd.DataFrame(0.0, index=prices.index, columns=prices.columns)
        else:
            cash = (
                div.assign(month=div["ex_date"].dt.to_period("M"))
                .groupby(["month", "ticker"])["value"]
                .sum()
                .unstack("ticker")
            )
            cash = cash.reindex(index=prices.index, columns=prices.columns).fillna(0.0)

        ret = (prices + cash) / prices.shift(1) - 1.0
        ret.index = ret.index.to_timestamp(how="end").normalize()
        ret = ret.reindex(columns=self.tickers)
        self._cache[key] = ret
        return ret

    # -- eligibility (§3.3) ----------------------------------------------- #

    def history_months(self, t) -> pd.Series:
        """Consecutive valid months ending at ``t``, per ticker (protocol §5.4.2)."""
        valid = self.monthly_prices(cutoff=t).notna()
        tail = valid.tail(MIN_HISTORY_MONTHS)
        counts = {}
        for col in valid.columns:
            n = 0
            for flag in tail[col].to_numpy()[::-1]:
                if bool(flag):
                    n += 1
                else:
                    break
            counts[col] = n
        return pd.Series(counts)

    def adv_3m(self, t) -> pd.Series:
        """Trailing-3-month average daily dollar volume at ``t`` (protocol §5.4.2).

        Dollar volume is raw close x raw volume — both are as-traded, so the
        product is the actual traded dollar amount even across a split.
        """
        t = pd.Timestamp(t)
        close = self.close_raw().loc[:t]
        volume = self.volume_raw().loc[:t]
        dollar = close * volume
        window = dollar.loc[dollar.index > t - pd.DateOffset(months=ADV_WINDOW_MONTHS)]
        return window.mean().reindex(self.tickers)

    def price_at(self, t) -> pd.Series:
        """Last available (<= 3-day ffill) adjusted close at or before ``t``."""
        t = pd.Timestamp(t)
        adj = self.adjusted_prices(t)
        return adj.ffill(limit=MAX_FFILL_DAYS).iloc[-1].reindex(self.tickers)

    def eligible(self, t) -> list[str]:
        """Tickers satisfying every §3.3 condition at ``t``."""
        members = set(self.members_at(t))
        hist = self.history_months(t)
        adv = self.adv_3m(t)
        price = self.price_at(t)
        keep = [
            ticker
            for ticker in self.tickers
            if ticker in members
            and hist.get(ticker, 0) >= MIN_HISTORY_MONTHS
            and np.isfinite(adv.get(ticker, np.nan))
            and adv.get(ticker, 0.0) > ADV_MIN_USD
            and np.isfinite(price.get(ticker, np.nan))
            and price.get(ticker, 0.0) > 0
        ]
        return keep

    # -- risk-free rate (§3.4) -------------------------------------------- #

    def rf_monthly(self, start=None, end=None) -> pd.Series:
        """Monthly risk-free rate from ``DGS1MO`` (protocol §5.4.6, §5.5.5).

        Never substitutes zero. See :data:`RF_ANNUAL_TO_MONTHLY` and
        :data:`RF_ALIGN` for the two unpinned conventions.
        """
        series = self.rf_daily.set_index("date")["dgs1mo"].sort_index()
        observed = series.resample("ME").last()
        filled = observed.ffill(limit=1)
        remaining = filled.isna()
        if remaining.any():  # always observable in practice; never zero
            filled = filled.ffill()
        if filled.isna().any():
            raise SnapshotError("risk-free series has leading gaps; refusing to substitute zero")

        annual = filled.astype(float) / 100.0
        if RF_ANNUAL_TO_MONTHLY == "geometric":
            monthly = (1.0 + annual) ** (1.0 / 12.0) - 1.0
        elif RF_ANNUAL_TO_MONTHLY == "simple":
            monthly = annual / 12.0
        else:  # pragma: no cover - guarded by the constant
            raise SnapshotError(f"unknown RF_ANNUAL_TO_MONTHLY={RF_ANNUAL_TO_MONTHLY!r}")

        if RF_ALIGN == "prior_month":
            monthly = monthly.shift(1)
        elif RF_ALIGN != "same_month":  # pragma: no cover - guarded by the constant
            raise SnapshotError(f"unknown RF_ALIGN={RF_ALIGN!r}")

        monthly.name = "rf_monthly"
        if start is not None:
            monthly = monthly.loc[monthly.index >= pd.Timestamp(start)]
        if end is not None:
            monthly = monthly.loc[monthly.index <= pd.Timestamp(end)]
        return monthly.dropna()


# --------------------------------------------------------------------------- #
# Snapshot I/O
# --------------------------------------------------------------------------- #


def load_snapshot(snapshot_id: str, *, verify: bool = True) -> Snapshot:
    """Read an immutable snapshot from ``data/snapshots/<snapshot_id>/``."""
    path = SNAPSHOTS_DIR / snapshot_id
    if not path.is_dir():
        raise SnapshotError(f"snapshot not found: {path}")

    manifest_path = path / MANIFEST_FILE
    manifest = json.loads(manifest_path.read_text(encoding="utf-8")) if manifest_path.exists() else {}

    if verify and manifest.get("sha256"):
        for name, digest in manifest["sha256"].items():
            target = path / name
            if not target.exists():
                raise SnapshotError(f"snapshot {snapshot_id} missing {name}")
            if sha256_file(target) != digest:
                raise SnapshotError(f"snapshot {snapshot_id} failed integrity check on {name}")

    prices = pd.read_parquet(path / PRICE_FILE)
    prices.columns = prices.columns.set_names(["field", "ticker"])
    actions = pd.read_parquet(path / ACTIONS_FILE)
    rf = pd.read_parquet(path / RF_FILE)
    universe = pd.read_csv(path / UNIVERSE_FILE, dtype=str).fillna("")

    quality = (path / QUALITY_FILE).read_text(encoding="utf-8") if (path / QUALITY_FILE).exists() else ""

    return Snapshot(
        snapshot_id=snapshot_id,
        path=path,
        prices_raw=prices,
        actions=actions,
        rf_daily=rf,
        universe=universe,
        quality_report=quality,
        manifest=manifest,
    )


def list_snapshots() -> list[str]:
    """Snapshot IDs present on disk, newest first (by retrieval date in the name)."""
    if not SNAPSHOTS_DIR.is_dir():
        return []
    names = [p.name for p in SNAPSHOTS_DIR.iterdir() if p.is_dir()]
    return sorted(names, reverse=True)


def latest_snapshot() -> str:
    names = list_snapshots()
    if not names:
        raise SnapshotError("no snapshots on disk; run scripts/build_snapshot.py first")
    return names[0]


# --------------------------------------------------------------------------- #
# LEGACY (Phase 1, exploratory) — quarantined, non-confirmatory
# --------------------------------------------------------------------------- #
# DEAD END. Superseded by the snapshot API above (DEC-20261015-015 findings 4a
# and F8; DEC-20261017-019). Kept only so the archived exploratory scripts
# (scripts/phase1_experiment.py, scripts/diagnose_slsqp.py,
# scripts/dsr_inputs_phase1.py) still run. Nothing on the confirmatory path may
# import these, and Phase 1's parameter set must not survive into a confirmatory
# run (spec §10.4).

PHASE1_UNIVERSE = [
    "SPY", "IWM", "EFA", "EEM", "TLT", "IEF", "SHY", "LQD", "HYG",
    "TIP", "GLD", "DBC", "VNQ", "RWX", "BIL",
]


def load_monthly_returns(tickers=None, start="2007-01-01", end=None, use_cache=True):
    """LEGACY Phase 1 loader (retroactively adjusted prices). Do not use."""
    warnings.warn(
        "data.load_monthly_returns is the superseded Phase 1 loader "
        "(auto_adjust=True, no snapshot). Use load_snapshot() (DEC-20261015-015).",
        DeprecationWarning,
        stacklevel=2,
    )
    import yfinance as yf

    tickers = tickers or PHASE1_UNIVERSE
    CACHE_DIR.mkdir(parents=True, exist_ok=True)
    cache_file = CACHE_DIR / f"monthly_returns_{start}_{end or 'latest'}.parquet"
    if use_cache and cache_file.exists():
        return pd.read_parquet(cache_file)

    raw = yf.download(tickers, start=start, end=end, auto_adjust=True, progress=False)["Close"]
    monthly = raw.resample("ME").last().pct_change().dropna(how="all")
    monthly = monthly.dropna(axis=1, thresh=int(0.9 * len(monthly))).dropna(how="any")
    monthly.to_parquet(cache_file)
    return monthly


def load_risk_free_rate(start="2007-01-01", end=None):
    """LEGACY Phase 1 rf (BIL proxy). Do not use (protocol §5.4.6)."""
    warnings.warn("data.load_risk_free_rate is superseded by Snapshot.rf_monthly", DeprecationWarning, stacklevel=2)
    return load_monthly_returns(tickers=["BIL"], start=start, end=end)["BIL"]
