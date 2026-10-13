# Data Contract and Point-in-Time Policy: robustfolio

**Version:** 1.0  
**Status:** Draft — pending owner confirmation of proposed defaults; freeze before first backtest  
**Owner:** Ken Ira Lacson Talingting  
**Created:** 2026-10-14  
**Last Updated:** 2026-10-14  
**Supersedes:** None  
**Related:** [`problem_framing.md`](problem_framing.md), [`project_charter.md`](project_charter.md), [`success_metrics_and_evaluation_protocol.md`](success_metrics_and_evaluation_protocol.md), [`cost_model_and_frictions.md`](cost_model_and_frictions.md), [`falsification_and_kill_criteria.md`](falsification_and_kill_criteria.md), [`reproducibility_and_environment.md`](reproducibility_and_environment.md)

---

## 0. Purpose of This Document

This document defines:

1. Which data sources are allowed.
2. How the investable universe is defined and how it changes over time.
3. What "point-in-time" means operationally for every field used in estimation or evaluation.
4. How corporate actions, delistings, and missing data are handled.
5. How data is versioned, snapshotted, and reproduced.
6. What quality checks run before any data is used in an experiment.

It is the **contract** between raw data and any experiment. No experiment may use data that violates this contract. Violations invalidate results (see `falsification_and_kill_criteria.md` §4 K6).

**Once frozen, this document may not be modified after seeing experimental results.** Any change requires a decision log entry and a version bump.

---

## 1. Data Philosophy

Three principles govern all data decisions:

1. **Point-in-time or nothing.** Every value used at time \( t \) must have been available at time \( t \). Retroactive values (backfilled, restated, survivor-filtered) are not permitted in estimation or evaluation.
2. **Reproducible from raw.** Every derived dataset must be reconstructible from raw snapshots plus documented transformation code. No manual edits, no undocumented joins.
3. **Honest about limits.** Where free or public data cannot satisfy point-in-time requirements, the limitation is documented and the affected claims are downgraded, not hidden.

A pipeline that produces beautiful results from corrupted data has failed. A pipeline that produces modest results from disciplined data has succeeded.

---

## 2. Data Sources

> **Note:** The following are **proposed conservative defaults** for a zero-budget, public-data project. Confirm or replace before freezing.

### 2.1 Allowed sources

| Purpose | Source | Access | Point-in-time quality |
|---------|--------|--------|----------------------|
| Adjusted daily prices | `[PROPOSED: Yahoo Finance via yfinance]` | Free | Retroactive; must be reconstructed (see §4.4) |
| Raw daily prices | `[PROPOSED: Yahoo Finance via yfinance]` | Free | Real-time at retrieval; reliable after snapshot |
| Corporate actions (splits, dividends) | `[PROPOSED: Yahoo Finance / Stooq]` | Free | Reasonable for large-cap |
| Risk-free rate (1-month T-bill) | `[PROPOSED: FRED DGS1MO]` | Free | Point-in-time |
| ETF / equity metadata (name, inception, exchange) | `[PROPOSED: Yahoo Finance / SEC EDGAR]` | Free | Reasonable |
| Universe definition (S&P 100, or equivalent) | `[PROPOSED: S&P 100 constituents as of a fixed historical date + delisted members]` | Free / manual | Must be reconstructed point-in-time |

### 2.2 Forbidden sources

- Any source whose historical values are retroactively adjusted without a raw alternative.
- Any source whose free tier has undocumented revision history.
- Any source whose terms of service prohibit research use or redistribution of derived data.
- Any proprietary or paid data without explicit budget approval (see charter §9).

### 2.3 Vendor lock-in mitigation

All ingestion code must isolate vendor-specific logic behind an adapter. Swapping sources must not require rewriting estimation or evaluation code.

---

## 3. Universe Definition

The investable universe is the set of assets eligible for allocation at any rebalance date.

### 3.1 Core universe (MVP)

`[PROPOSED]`:

- **Asset class:** US-listed ETFs covering major asset classes (equity, fixed income, commodities, real estate).
- **Candidate universe:** A fixed list of `[PROPOSED: 15–25]` liquid ETFs, each with at least `[PROPOSED: 5 years]` of history at the start of the backtest.
- **Delisted handling:** Any ETF in the candidate list that delisted during the backtest period is retained up to its delisting date, then excluded. Delisting returns are included.

### 3.2 Eligibility rules at time \( t \)

An asset is eligible at rebalance date \( t \) if and only if all of the following hold using only information available at \( t \):

1. It is a member of the candidate universe at \( t \).
2. It has at least `[PROPOSED: 36 months]` of consecutive valid price history ending at \( t \).
3. Its average daily dollar volume over the trailing `[PROPOSED: 3 months]` exceeds `[PROPOSED: $5 million]`.
4. Its price at \( t \) is positive and not flagged as erroneous (see §7).

### 3.3 Universe expansions

Any expansion of the core universe (e.g., adding large-cap equities, international ETFs, or sector ETFs) requires:

- A charter amendment.
- A new pre-registered experiment.
- A fresh snapshot under this contract.

Silent expansion is scope creep and will invalidate results.

---

## 4. Point-in-Time Rules

This is the core of the contract. Each rule is stated as a prohibition, because violations are the primary corruption mode.

### 4.1 Estimation inputs

At time \( t \), the following may be used:

- Prices, returns, and volumes observed at or before \( t \).
- Corporate action information known at or before \( t \).
- Universe membership as defined at or before \( t \).

The following may **not** be used:

- Any value computed using future prices, future universe membership, or future corporate actions.
- Any revised or restated historical value that was not the value available at \( t \).
- Any index membership that was assigned after \( t \).

### 4.2 Portfolio construction

Weights at time \( t \) are computed using only information available at or before \( t \). Execution is assumed at the close of \( t \) or the open of \( t+1 \) — this choice is fixed in `cost_model_and_frictions.md` and must be consistent across all methods.

### 4.3 Returns and evaluation

Return at time \( t+1 \) is computed from prices between \( t \) and \( t+1 \). Costs are applied at \( t \) based on the weight change from \( t-1 \) to \( t \). No future information enters the return calculation.

### 4.4 Adjusted price reconstruction

Free price sources typically provide **retroactively adjusted** prices. Using them naively is a form of lookahead, because adjustments incorporate future dividends and splits.

**Required procedure:**

1. Retrieve **raw unadjusted close prices** and store them as a snapshot.
2. Retrieve **corporate action history** (splits, dividends) as a snapshot.
3. At evaluation time \( t \), compute adjusted prices using only corporate actions with ex-dates ≤ \( t \).
4. Use the point-in-time adjusted series for return computation.

If the raw unadjusted series is unavailable, the adjusted series may be used only if:

- The adjustment methodology is documented, AND
- The bias is acknowledged as a limitation, AND
- The affected claims are downgraded to "exploratory" in reporting.

### 4.5 Risk-free rate

The risk-free rate at time \( t \) is the 1-month T-bill yield as observed at \( t \), converted to a monthly rate using the convention documented in `success_metrics_and_evaluation_protocol.md` §2.

### 4.6 Point-in-time checklist per experiment

Before running any experiment, the following must be true:

- [ ] The snapshot used is identified by hash.
- [ ] Every field used is traced to a raw source with a documented transformation.
- [ ] No field is derived from future information.
- [ ] Universe membership at each rebalance date is reconstructed from point-in-time evidence, not from the present-day list.
- [ ] Corporate actions are applied only when their ex-date has passed.
- [ ] A leakage test (see §8) has passed.

Failure of any item blocks the experiment.

---

## 5. Corporate Actions

Corporate actions affect prices, returns, and weight continuity. Handling is mandatory.

| Action | Handling |
|--------|----------|
| **Stock split** | Adjust historical prices and shares point-in-time; do not adjust weights (splits are value-neutral) |
| **Cash dividend** | Add to return on ex-date; do not adjust price retroactively for return calculation |
| **Special dividend** | Treated as cash dividend; document and flag |
| **Merger / acquisition** | Asset is removed at the effective date; terminal value is added to returns |
| **Delisting** | Asset is removed at delisting date; delisting return is added (assume `[PROPOSED: -100%]` if unavailable, flag as limitation) |
| **Ticker change** | Reconciled in metadata; treated as same asset |
| **ETF inception** | Asset enters universe only after inception and eligibility rules are satisfied |

Any action not covered above must be documented before use. Undocumented adjustments invalidate the experiment.

---

## 6. Survivorship Bias Prevention

The candidate universe must include assets that **existed** during the backtest, not just those that **survive today**.

Rules:

1. The candidate list is defined **as of the backtest start date**, not as of today.
2. Assets that delisted during the backtest remain in the universe until their delisting date.
3. Delisting returns are included.
4. No asset is dropped from the candidate list because it no longer exists today.
5. The candidate list must be reconstructed from point-in-time evidence (archived ETF screens, historical fund lists, SEC filings).

If point-in-time universe membership cannot be reconstructed, the limitation is documented and the affected claims are downgraded.

---

## 7. Missing Data and Outliers

### 7.1 Missing data policy

| Case | Policy |
|------|--------|
| Isolated missing day | Forward-fill up to `[PROPOSED: 3 consecutive days]`; mark as imputed |
| Extended gap (> 3 days) | Treat asset as ineligible for the gap window; exclude from rebalance |
| Missing risk-free rate | Use last observed value; flag |
| Missing corporate action | Halt; do not proceed until reconciled |

### 7.2 Outlier policy

- Price jumps not explained by corporate actions are flagged and reviewed before use.
- Volume spikes not explained by events are flagged but retained.
- Any manual override of a value requires a decision log entry and a data-quality note in the snapshot.

### 7.3 Data quality flags

Every snapshot has a companion quality report that lists:

- Number of missing values imputed.
- Number of outliers flagged.
- Number of corporate actions applied.
- Number of universe membership changes.
- Any unresolved data issues.

---

## 8. Leakage Tests

Before any experiment runs, the following automated tests must pass:

1. **Time-travel test:** For a random sample of timestamps, verify no field used at \( t \) contains values that could only be known after \( t \).
2. **Survivorship test:** Verify the universe at \( t \) includes assets that delisted after \( t \).
3. **Adjusted-price test:** Verify point-in-time adjusted prices do not incorporate corporate actions with ex-dates after \( t \).
4. **Universe reconstruction test:** Verify membership at \( t \) matches archived point-in-time evidence.
5. **Determinism test:** Same snapshot + same code → identical output.

Any failing test blocks the experiment.

---

## 9. Data Versioning and Snapshots

### 9.1 Snapshot definition

A **snapshot** is an immutable bundle of:

- Raw source files (prices, corporate actions, metadata).
- Retrieval timestamp.
- Source identifiers and URLs.
- SHA-256 hash of the bundle.
- Companion quality report.

Snapshots are stored under `data/snapshots/<snapshot_id>/` and never modified.

### 9.2 Snapshot naming

`<source>-<asset_class>-<start>_<end>-<retrieval_date>-<hash8>`

Example: `yf-etf-20100101_20241231-20261014-a1b2c3d4`

### 9.3 Derived datasets

Every derived dataset (e.g., point-in-time adjusted prices) records:

- The snapshot ID it derives from.
- The transformation code version (git commit).
- A hash of the output.

### 9.4 Immutability

Snapshots are append-only. Corrections create a new snapshot. The old snapshot is retained for reproducibility.

---

## 10. Reproducibility Requirements

An experiment is reproducible if a fresh environment can regenerate its results from:

- The snapshot ID.
- The transformation code version.
- The experiment registry entry.
- The environment lockfile.

Any experiment that cannot be reproduced this way is downgraded to "exploratory" and cannot support a success claim.

See `reproducibility_and_environment.md` for environment specifics.

---

## 11. What Invalidates a Result

An experiment is invalidated if any of the following occurred:

- Point-in-time violation in any field.
- Survivorship bias in universe construction.
- Undocumented corporate action adjustment.
- Use of retroactively adjusted prices without point-in-time reconstruction.
- Manual edit of a raw value without a decision log entry.
- Snapshot mismatch between estimation and evaluation.
- Failing leakage test that was not resolved before running.
- Missing data imputation beyond the policy in §7.1 without disclosure.

Invalidated results are documented and not deleted.

---

## 12. Model Tags Applied

- **[First Principles]** — Reduced data to raw observations, point-in-time transformations, and derived datasets.
- **[Inversion]** — Defined invalidation conditions and leakage tests before defining success.
- **[Experimental]** — Pre-registration, snapshot immutability, leakage tests, determinism checks.
- **[Systems]** — Snapshot versioning, derived-dataset lineage, quality flags, blocked experiments.
- **[Bayesian]** — Data quality flags propagate to claim confidence; limitations downgrade claims.
- **[Information Theory]** — Compressed to rules, prohibitions, and checklists; no filler.

---

## 13. Owner Action Checklist Before Freezing

Before setting Status to `Frozen`, confirm or replace every `[PROPOSED]` value:

- [ ] Section 2.1: confirm data sources and access method
- [ ] Section 3.1: confirm candidate universe size and minimum history
- [ ] Section 3.2: confirm eligibility thresholds (history, dollar volume)
- [ ] Section 5: confirm delisting return assumption
- [ ] Section 7.1: confirm forward-fill limit
- [ ] Section 9.2: confirm snapshot naming convention

Also confirm:

- [ ] You are willing to reconstruct point-in-time adjusted prices from raw data (§4.4). If not, downgrade all affected claims to exploratory and note it here.
- [ ] You are willing to reconstruct point-in-time universe membership (§6). If not, document the limitation and downgrade affected claims.
- [ ] The chosen data sources are legally usable for this project (§2.2).

Once confirmed, bump to Version 1.1, set Status to `Frozen`, and add a revision history row.

---

## 14. Revision History

| Date | Version | Change | Author |
|------|---------|--------|--------|
| 2026-10-14 | 1.0 | Initial data contract and point-in-time policy | Ken Ira Lacson Talingting |

---

*This document exists to prevent the most corrupting failure mode in the project: using data that could not have been known at the time. A result that violates this contract is not a result.*
