# Country-ETF sample — 2005–2026

**Status:** Pre-specified external replication, executed 2026-11-05. The protocol is dated 2026-11-05, but the repository does not independently establish that its final content was frozen before execution. The sample is **not labeled confirmatory**; the broader project remains exploratory because the corrected test was derived from the first sample.

**Claim-status note (2026-11-08).** The country results were written at 19:51:35 on 2026-11-05. The protocol file was last written at 20:08:45, and both were committed together at 20:09:27. See [`notes/audit_2026-11-08.md`](../../../notes/audit_2026-11-08.md).

This folder holds the published tables for the second sample:

- `outcomes.csv` — seven methods, 252 months, 21 folds, net excess Sharpe at the five reported cost levels with bootstrap intervals.
- `decisions.csv` — the two candidates against the best baseline, with the paired significance gate, materiality, turnover, drawdown, cost-level and fold checks.
- `folds_M1.csv`, `folds_M2.csv` — per-fold comparisons.
- `manifest.json` — snapshot id, window, counts, best baseline.

**Snapshot:** `yahoo-countryetf-1998-01-01_2026-09-30-2026-11-05-269a4565`

**Snapshot status:** built locally from Yahoo/FRED and **not distributed**. Exact reproduction of these tables requires an independently obtained archive. The committed CSVs are the record; the universe list and builder are in `notes/` and `scripts/`.

**Protocol record:** [`notes/confirmatory_country_etfs_2026-11-05.md`](../../../notes/confirmatory_country_etfs_2026-11-05.md)
**Result note:** [`notes/country_sample_result_2026-11-05.md`](../../../notes/country_sample_result_2026-11-05.md)

**Result in one line:** the best baseline was 1/N, both treatments underperformed it, and the
treatment advantage did not replicate. The benchmark lesson did.
