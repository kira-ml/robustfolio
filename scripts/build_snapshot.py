#!/usr/bin/env python
"""Build an immutable point-in-time snapshot (spec §3.1, protocol §5.4.9).

Usage
-----
    python scripts/build_snapshot.py                     # defaults
    python scripts/build_snapshot.py --end 2026-09-30 --retrieval-date 2026-10-17

The snapshot is written to ``data/snapshots/<snapshot_id>/`` and is append-only:
if the directory already exists the script refuses to touch it (protocol §5.4.9).
Snapshots are git-ignored; the confirmed candidate list they embed is not
(``notes/pit_candidates_2026-10-17.csv``, DEC-20261017-024).
"""

from __future__ import annotations

import argparse
import hashlib
import json
import subprocess
import sys
import uuid
from datetime import date, datetime, timezone
from pathlib import Path

import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from robustfolio import data as data_mod  # noqa: E402


def _git_commit() -> str:
    try:
        return subprocess.run(
            ["git", "rev-parse", "HEAD"], cwd=data_mod.REPO_ROOT,
            capture_output=True, text=True, check=True,
        ).stdout.strip()
    except Exception:  # noqa: BLE001
        return "unknown"


def _last_day_of_previous_month(today: date | None = None) -> pd.Timestamp:
    today = pd.Timestamp(today or date.today())
    return (today.replace(day=1) - pd.Timedelta(days=1)).normalize()


def _bundle_hash(hashes: dict[str, str]) -> str:
    blob = json.dumps(sorted(hashes.items()), sort_keys=True)
    return hashlib.sha256(blob.encode("utf-8")).hexdigest()


def _quality_report(snapshot_id: str, prices: pd.DataFrame, actions: pd.DataFrame,
                    rf: pd.DataFrame, universe: pd.DataFrame, start: str, end: str) -> str:
    close = prices.xs("close", level="field", axis=1)
    volume = prices.xs("volume", level="field", axis=1)
    filled = close.ffill(limit=data_mod.MAX_FFILL_DAYS)
    imputed = int((filled.notna() & close.isna()).sum().sum())
    monthly = close.resample("ME").last()
    gap_months = int(monthly.isna().sum().sum())

    lines = [
        f"# Snapshot quality report — `{snapshot_id}`",
        "",
        f"**Window:** {start} … {end}  ",
        f"**Tickers:** {len(close.columns)}  ",
        f"**Daily rows:** {len(close)}  ",
        f"**Generated (UTC):** {datetime.now(timezone.utc).isoformat(timespec='seconds')}",
        "",
        "## Corporate actions captured (protocol §5.4.4 step 2)",
        "",
    ]
    if actions.empty:
        lines.append("_None._")
    else:
        by_kind = actions.groupby("kind").size().to_dict()
        lines.append(f"Actions: " + ", ".join(f"`{k}` = {v}" for k, v in sorted(by_kind.items())))
        lines.append("")
        lines.append("| Ticker | Action | Ex-date | Value |")
        lines.append("|--------|--------|---------|-------|")
        for row in actions.itertuples(index=False):
            lines.append(f"| `{row.ticker}` | {row.kind} | {row.ex_date.date()} | {row.value:g} |")

    lines += [
        "",
        "## Missing data (protocol §5.4.6)",
        "",
        f"- Isolated missing days forward-filled (≤ {data_mod.MAX_FFILL_DAYS} consecutive): **{imputed}**",
        f"- Month-end prices still missing after the fill limit (asset ineligible in that month): **{gap_months}**",
        "",
        "## Per-ticker coverage",
        "",
        "| Ticker | First raw date | Last raw date | Rows | Dividends | Splits | First month-end | Last month-end |",
        "|--------|----------------|---------------|------|-----------|--------|-----------------|----------------|",
    ]
    div_counts = actions[actions["kind"] == "dividend"].groupby("ticker").size() if not actions.empty else {}
    split_counts = actions[actions["kind"] == "split"].groupby("ticker").size() if not actions.empty else {}
    for ticker in close.columns:
        series = close[ticker].dropna()
        first = series.index.min().date() if len(series) else "—"
        last = series.index.max().date() if len(series) else "—"
        m = monthly[ticker].dropna()
        fm = m.index.min().date() if len(m) else "—"
        lm = m.index.max().date() if len(m) else "—"
        lines.append(
            f"| `{ticker}` | {first} | {last} | {len(series)} | "
            f"{int(div_counts.get(ticker, 0))} | {int(split_counts.get(ticker, 0))} | {fm} | {lm} |"
        )

    # Unexplained price jumps (protocol §5.4.6: flag and review, retain).
    ret = close.pct_change()
    action_dates = set(zip(actions["ticker"], actions["ex_date"])) if not actions.empty else set()
    jumps = []
    for ticker in close.columns:
        series = ret[ticker].dropna()
        for ts, value in series[series.abs() > 0.50].items():
            if (ticker, ts) in action_dates:
                continue
            jumps.append((ticker, ts.date(), float(value)))
    lines += ["", "## Flagged anomalies (retained, not corrected)", ""]
    lines.append(f"- Unexplained daily moves |return| > 50% (no action on that date): **{len(jumps)}**")
    for ticker, ts, value in jumps:
        lines.append(f"  - `{ticker}` {ts}: {value:+.1%}")

    lines += [
        "",
        "## Universe (protocol §5.4.7, DEC-20261017-024)",
        "",
        "| Ticker | First eligible | Last eligible | Source note |",
        "|--------|----------------|---------------|-------------|",
    ]
    for row in universe.itertuples(index=False):
        last = getattr(row, "last_eligible", "") or "—"
        lines.append(f"| `{row.ticker}` | {row.first_eligible} | {last} | {row.source_note} |")

    lines += [
        "",
        "## Risk-free series",
        "",
        f"- Observations: {len(rf)}  ({rf['date'].min().date()} … {rf['date'].max().date()})"
        if len(rf) else "- Observations: 0",
        "",
        "## Unresolved issues / limitations",
        "",
        "1. **No in-sample delisting.** Every confirmed candidate is still listed, so the "
        "delisting path (§5.4.5) is implemented but unexercised "
        "(`notes/pit_universe_2026-10-17.md` §5).",
        "2. **Yield-to-monthly conversion (finding F10).** `RF_ANNUAL_TO_MONTHLY = "
        f"'{data_mod.RF_ANNUAL_TO_MONTHLY}'` is not pinned by the frozen docs.",
        "3. **Risk-free alignment (finding F11).** `RF_ALIGN = "
        f"'{data_mod.RF_ALIGN}'` is not pinned by the frozen docs.",
        "4. **Trailing partial month excluded.** The window ends on the last complete "
        "month so no partial-month price enters a return (protocol §15).",
        "5. Vendor series are retrieved live and can be restated by the vendor; the "
        "snapshot pins the values actually used (protocol §5.4.9).",
        "",
    ]
    return "\n".join(lines) + "\n"


def build(universe_csv: Path, start: str, end: str, retrieval_date: str,
          asset_class: str = "usetf", out_dir: Path | None = None) -> str:
    out_dir = out_dir or data_mod.SNAPSHOTS_DIR
    universe = pd.read_csv(universe_csv, dtype=str).fillna("")
    required = {"ticker", "first_eligible", "last_eligible", "source_note"}
    if not required.issubset(universe.columns):
        raise SystemExit(f"{universe_csv} must have columns {sorted(required)}")
    tickers = universe["ticker"].astype(str).tolist()
    if not 15 <= len(tickers) <= 25:
        raise SystemExit(f"protocol §5.4.2 requires 15–25 candidates; got {len(tickers)}")

    print(f"fetching {len(tickers)} tickers from Yahoo ({start} … {end}) …")
    prices, actions = data_mod.fetch_yahoo_raw(tickers, start, end)
    print(f"  prices {prices.shape}, actions {len(actions)}")
    print("fetching FRED DGS1MO …")
    rf = data_mod.fetch_fred_dgs1mo(start, end)
    print(f"  rf {len(rf)} observations")

    out_dir.mkdir(parents=True, exist_ok=True)
    staging = out_dir / f".staging-{retrieval_date}-{uuid.uuid4().hex[:8]}"
    staging.mkdir()

    prices.to_parquet(staging / data_mod.PRICE_FILE)
    actions.to_parquet(staging / data_mod.ACTIONS_FILE, index=False)
    rf.to_parquet(staging / data_mod.RF_FILE, index=False)
    (staging / data_mod.UNIVERSE_FILE).write_text(
        universe_csv.read_text(encoding="utf-8"), encoding="utf-8"
    )

    data_hashes = {
        name: data_mod.sha256_file(staging / name)
        for name in (data_mod.PRICE_FILE, data_mod.ACTIONS_FILE, data_mod.RF_FILE,
                     data_mod.UNIVERSE_FILE)
    }
    bundle = _bundle_hash(data_hashes)
    hash8 = bundle[:8]
    snapshot_id = f"yahoo-{asset_class}-{start}_{end}-{retrieval_date}-{hash8}"

    target = out_dir / snapshot_id
    if target.exists():
        raise SystemExit(
            f"snapshot already exists and snapshots are append-only: {target}\n"
            "Nothing was written. Re-run with a different --retrieval-date."
        )

    quality = _quality_report(snapshot_id, prices, actions, rf, universe, start, end)
    (staging / data_mod.QUALITY_FILE).write_text(quality, encoding="utf-8")

    sha256 = {
        name: data_mod.sha256_file(staging / name)
        for name in data_mod.SNAPSHOT_FILES
    }
    manifest = {
        "schema_version": data_mod.SNAPSHOT_SCHEMA_VERSION,
        "snapshot_id": snapshot_id,
        "asset_class": asset_class,
        "source": "yahoo",
        "source_detail": data_mod.VENDOR_SOURCES,
        "retrieval_date": retrieval_date,
        "created_utc": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "git_commit": _git_commit(),
        "window": {"start": start, "end": end},
        "tickers": tickers,
        "n_tickers": len(tickers),
        "n_daily_rows": int(len(prices)),
        "sha256": sha256,
        "bundle_sha256": bundle,
        "hash8": hash8,
        "conventions": {
            "RF_ANNUAL_TO_MONTHLY": data_mod.RF_ANNUAL_TO_MONTHLY,
            "RF_ALIGN": data_mod.RF_ALIGN,
            "MAX_FFILL_DAYS": data_mod.MAX_FFILL_DAYS,
            "ADV_MIN_USD": data_mod.ADV_MIN_USD,
            "ADV_WINDOW_MONTHS": data_mod.ADV_WINDOW_MONTHS,
            "MIN_HISTORY_MONTHS": data_mod.MIN_HISTORY_MONTHS,
        },
        "universe_source": str(universe_csv.relative_to(data_mod.REPO_ROOT)),
        "findings": ["F10 (rf annual->monthly conversion)", "F11 (rf alignment month)"],
    }
    (staging / data_mod.MANIFEST_FILE).write_text(
        json.dumps(manifest, indent=2) + "\n", encoding="utf-8"
    )

    staging.rename(target)
    print(f"\nsnapshot written: {target}")
    print(f"snapshot_id      : {snapshot_id}")
    return snapshot_id


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--universe", default=str(data_mod.DEFAULT_UNIVERSE_CSV))
    parser.add_argument("--start", default="2007-01-01")
    parser.add_argument("--end", default=None,
                        help="default: last day of the previous month (no partial month)")
    parser.add_argument("--retrieval-date", default=date.today().isoformat())
    parser.add_argument("--asset-class", default="usetf")
    parser.add_argument("--out-dir", default=None)
    args = parser.parse_args(argv)

    end = args.end or _last_day_of_previous_month().date().isoformat()
    build(
        universe_csv=Path(args.universe),
        start=args.start,
        end=end,
        retrieval_date=args.retrieval_date,
        asset_class=args.asset_class,
        out_dir=Path(args.out_dir) if args.out_dir else None,
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
