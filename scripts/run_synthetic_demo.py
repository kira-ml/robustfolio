"""Run the full pipeline on a deterministic synthetic snapshot.

    python scripts/run_synthetic_demo.py --out results/synthetic-demo

This is not a reproduction of the published sample. It is an end-to-end
demonstration that a fresh clone can exercise the real data layout, the real
walk-forward harness, all seven methods, the report builder, and the written
run directory without the restricted vendor snapshot.

The synthetic panel contains a deliberate split and quarterly dividends, so the
corporate-action path is exercised. The data are generated at run time and are
never committed.
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from robustfolio import backtest  # noqa: E402
from robustfolio import report as reporting  # noqa: E402
from robustfolio.data import Snapshot  # noqa: E402

TICKERS = ("AAA", "BBB", "CCC", "DDD", "EEE")
START = "2007-01-01"
END = "2026-05-31"
SPLIT_DATE = pd.Timestamp("2018-06-15")
SEED = 20261107


def _daily_frame(close: pd.DataFrame) -> pd.DataFrame:
    """Wrap close prices into the snapshot's (field, ticker) OHLCV layout."""
    fields = {}
    for ticker in close.columns:
        fields[("open", ticker)] = close[ticker]
        fields[("high", ticker)] = close[ticker]
        fields[("low", ticker)] = close[ticker]
        fields[("close", ticker)] = close[ticker]
        fields[("volume", ticker)] = pd.Series(1_000_000.0, index=close.index)
    frame = pd.DataFrame(fields)
    frame.columns = pd.MultiIndex.from_tuples(frame.columns, names=["field", "ticker"])
    return frame.sort_index(axis=1)


def build_synthetic_snapshot() -> Snapshot:
    """A deterministic five-asset panel with a split and dividends."""
    index = pd.bdate_range(START, END)
    rng = np.random.default_rng(SEED)

    # A common factor plus idiosyncratic noise gives correlated but not
    # identical assets; the dispersion is what makes the optimizer non-trivial.
    common = rng.normal(size=len(index))
    idiosyncratic = rng.normal(size=(len(index), len(TICKERS)))
    annual_mu = np.array([0.06, 0.045, 0.03, 0.02, 0.01])
    annual_vol = np.array([0.20, 0.15, 0.12, 0.09, 0.06])
    daily_mu = annual_mu / 252.0
    daily_vol = annual_vol / np.sqrt(252.0)
    daily_returns = daily_mu + daily_vol * (0.55 * common[:, None] + 0.45 * idiosyncratic)

    close = pd.DataFrame(
        100.0 * np.exp(np.cumsum(daily_returns, axis=0)),
        index=index,
        columns=list(TICKERS),
    )
    close.index.name = "date"

    # A real split: raw prices halve on the ex-date; the action restores the
    # pre-split series when adjusted_prices() applies it point-in-time.
    close.loc[index >= SPLIT_DATE, "AAA"] = close.loc[index >= SPLIT_DATE, "AAA"] / 2.0

    actions = pd.DataFrame(
        [{"ticker": "AAA", "ex_date": SPLIT_DATE, "kind": "split", "value": 2.0}]
    )
    dividend_rows = []
    for year in range(2007, 2027):
        for month in (3, 6, 9, 12):
            date = pd.Timestamp(year=year, month=month, day=15)
            if date > index[-1]:
                continue
            dividend_rows.append(
                {"ticker": "BBB", "ex_date": date, "kind": "dividend", "value": 0.50}
            )
    actions = pd.concat([actions, pd.DataFrame(dividend_rows)], ignore_index=True)
    actions = actions.sort_values(["ticker", "ex_date", "kind"]).reset_index(drop=True)

    rf = pd.DataFrame({"date": index, "dgs1mo": np.full(len(index), 2.0)})
    universe = pd.DataFrame(
        [
            {
                "ticker": ticker,
                "first_eligible": "2007-01-01",
                "last_eligible": "",
                "source_note": "synthetic demo",
            }
            for ticker in TICKERS
        ]
    )

    return Snapshot(
        snapshot_id="synthetic-demo-2007-01-01_2026-05-31",
        path=Path("."),
        prices_raw=_daily_frame(close),
        actions=actions,
        rf_daily=rf,
        universe=universe,
        quality_report="synthetic demonstration; not a reproduction of the published sample",
        manifest={"synthetic": True, "seed": SEED},
    )


def run_demo(out: Path, *, bootstrap: bool = False) -> dict:
    """Build the synthetic panel, run every method, write the run directory."""
    snapshot = build_synthetic_snapshot()
    results = {
        method: backtest.run_method(snapshot, method)
        for method in backtest.METHOD_IDS
    }

    if any(len(result.weights) != 168 for result in results.values()):
        raise RuntimeError("synthetic demo did not produce the expected 168 rebalances")
    if any(result.folds.nunique() != 14 for result in results.values()):
        raise RuntimeError("synthetic demo did not produce the expected 14 folds")
    for method, result in results.items():
        worst = float(result.diagnostics["residual"].astype(float).max())
        if worst > 1e-7:
            raise RuntimeError(
                f"{method} failed the acceptance certificate: worst residual {worst:.3e}"
            )

    run = reporting.build_report(
        results,
        snapshot_id=snapshot.snapshot_id,
        rf=snapshot.rf_monthly(),
        bootstrap=bootstrap,
        calibration_window=False,
    )
    if len(run.outcomes) != len(backtest.METHOD_IDS):
        raise RuntimeError("report did not include every method")
    if len(run.decisions) != 2:
        raise RuntimeError("report did not include both candidates")

    written = run.write(out)
    return {"run": run, "written": written, "snapshot": snapshot}


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument(
        "--out",
        type=Path,
        default=ROOT / "results" / "synthetic-demo",
        help="directory for the synthetic run artifacts",
    )
    parser.add_argument(
        "--bootstrap",
        action="store_true",
        help="run the 2,000-replication bootstrap (slower; default off for the demo)",
    )
    args = parser.parse_args(argv)

    result = run_demo(args.out, bootstrap=args.bootstrap)
    run = result["run"]
    print("synthetic demo: full pipeline, not a reproduction of the published sample")
    print(f"snapshot   : {result['snapshot'].snapshot_id}")
    print(f"methods    : {len(run.outcomes)}")
    print(f"decisions  : {len(run.decisions)}")
    print(f"out        : {args.out}")
    print(f"files      : {len(result['written'])}")
    print()
    print(run.outcomes[["net_sharpe", "turnover_annualized", "max_drawdown"]].to_string())
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
