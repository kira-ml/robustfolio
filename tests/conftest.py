"""Shared fixtures for the robustfolio test suite.

Two snapshot fixtures are provided:

* ``synthetic_snapshot`` — built in memory, hermetic and fast. It contains a
  deliberate split and dividends so the leakage tests have real power (a test
  that cannot fail proves nothing).
* ``real_snapshot`` — the newest immutable snapshot on disk. Tests that need it
  skip with an explanatory message when no snapshot has been built yet, so the
  suite still runs on a fresh clone.
"""

from __future__ import annotations

import sys
from pathlib import Path

import numpy as np
import pandas as pd
import pytest

REPO_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO_ROOT / "src"))

from robustfolio import data as dm  # noqa: E402


# --------------------------------------------------------------------------- #
# Real snapshot
# --------------------------------------------------------------------------- #

@pytest.fixture(scope="session")
def real_snapshot() -> dm.Snapshot:
    ids = dm.list_snapshots()
    if not ids:
        pytest.skip("no snapshot on disk; run scripts/build_snapshot.py")
    return dm.load_snapshot(ids[0])


@pytest.fixture(scope="session")
def real_snapshot_id() -> str:
    ids = dm.list_snapshots()
    if not ids:
        pytest.skip("no snapshot on disk; run scripts/build_snapshot.py")
    return ids[0]


# --------------------------------------------------------------------------- #
# Synthetic snapshot
# --------------------------------------------------------------------------- #

SYNTHETIC_TICKERS = ("AAA", "BBB", "CCC")
SYNTHETIC_START = "2014-01-01"
SYNTHETIC_END = "2021-12-31"
SPLIT_DATE = pd.Timestamp("2018-06-15")     # BBB 2:1
CCC_FIRST_ELIGIBLE = "2019-06-01"           # CCC has a short record by design


def _daily_frame(close: pd.DataFrame) -> pd.DataFrame:
    """Wrap a close frame into the snapshot's (field, ticker) OHLCV layout."""
    fields = {}
    for ticker in close.columns:
        fields[("open", ticker)] = close[ticker]
        fields[("high", ticker)] = close[ticker]
        fields[("low", ticker)] = close[ticker]
        fields[("close", ticker)] = close[ticker]
        fields[("volume", ticker)] = pd.Series(1_000_000.0, index=close.index)
    frame = pd.DataFrame(fields)
    frame.columns = pd.MultiIndex.from_tuples(
        frame.columns, names=["field", "ticker"]
    )
    return frame.sort_index(axis=1)


def _base_actions() -> pd.DataFrame:
    rows = [
        {"ticker": "BBB", "ex_date": SPLIT_DATE, "kind": "split", "value": 2.0},
    ]
    for year in (2015, 2016, 2017, 2018, 2019, 2020, 2021):
        for month in (3, 6, 9, 12):
            date = pd.Timestamp(year=year, month=month, day=15)
            if date > SPLIT_DATE:  # quoted in post-split terms
                rows.append({"ticker": "BBB", "ex_date": date, "kind": "dividend", "value": 0.30})
            else:                  # quoted in pre-split terms
                rows.append({"ticker": "BBB", "ex_date": date, "kind": "dividend", "value": 0.60})
    frame = pd.DataFrame(rows, columns=["ticker", "ex_date", "kind", "value"])
    return frame.sort_values(["ticker", "ex_date", "kind"]).reset_index(drop=True)


def _base_universe() -> pd.DataFrame:
    return pd.DataFrame(
        [
            {"ticker": "AAA", "first_eligible": "2014-01-01",
             "last_eligible": "", "source_note": "synthetic"},
            {"ticker": "BBB", "first_eligible": "2014-01-01",
             "last_eligible": "", "source_note": "synthetic"},
            {"ticker": "CCC", "first_eligible": CCC_FIRST_ELIGIBLE,
             "last_eligible": "", "source_note": "synthetic"},
        ]
    )


def make_snapshot(
    *,
    actions: pd.DataFrame | None = None,
    universe: pd.DataFrame | None = None,
    snapshot_id: str = "synthetic-usetf-2014_2021-2026-10-17-deadbeef",
) -> dm.Snapshot:
    """Build an in-memory :class:`dm.Snapshot` (never touches the network)."""
    index = pd.bdate_range(SYNTHETIC_START, SYNTHETIC_END)
    steps = np.arange(len(index), dtype=float)

    aaa = 100.0 * 1.0002 ** steps
    bbb = 50.0 * 1.0002 ** steps
    bbb[index >= SPLIT_DATE] = bbb[index >= SPLIT_DATE] / 2.0  # raw price halves
    ccc = 25.0 * 1.0001 ** steps

    close = pd.DataFrame({"AAA": aaa, "BBB": bbb, "CCC": ccc}, index=index)
    close.index.name = "date"

    rf = pd.DataFrame(
        {"date": index, "dgs1mo": np.full(len(index), 2.0)}
    )

    return dm.Snapshot(
        snapshot_id=snapshot_id,
        path=Path("."),
        prices_raw=_daily_frame(close),
        actions=_base_actions() if actions is None else actions,
        rf_daily=rf,
        universe=_base_universe() if universe is None else universe,
        quality_report="synthetic",
        manifest={"synthetic": True},
    )


def with_actions(snapshot: dm.Snapshot, actions: pd.DataFrame) -> dm.Snapshot:
    """A copy of ``snapshot`` with different corporate actions (fresh cache)."""
    return dm.Snapshot(
        snapshot_id=snapshot.snapshot_id + "+patch",
        path=snapshot.path,
        prices_raw=snapshot.prices_raw,
        actions=actions,
        rf_daily=snapshot.rf_daily,
        universe=snapshot.universe,
        quality_report=snapshot.quality_report,
        manifest=snapshot.manifest,
    )


@pytest.fixture
def synthetic_snapshot() -> dm.Snapshot:
    return make_snapshot()


@pytest.fixture
def month_ends() -> pd.DatetimeIndex:
    return pd.date_range("2015-01-31", "2021-12-31", freq="ME")
