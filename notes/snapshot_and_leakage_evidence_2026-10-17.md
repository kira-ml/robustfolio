# Snapshot and leakage-suite evidence - 2026-10-17

**Status:** Evidence record - the §5.4.8 leakage suite passes; the Phase 1 experiment is unblocked
**Owner:** Ken Ira Lacson Talingting
**Decision:** DEC-20261017-025
**Authority:** [`evaluation_protocol.md`](../docs/evaluation_protocol.md) §5.4.8, §5.4.9, §8.4; [`model_and_method_spec.md`](../docs/model_and_method_spec.md) §3; DEC-20261017-024 (PIT candidate universe)

---

## 0. What this records

The frozen documents describe a point-in-time data layer that did not exist. This note
records the snapshot that now exists, the code that produces it, and the result of the
five §5.4.8 leakage tests. Protocol §5.4.8 is explicit: "Before any experiment runs ...
Any failing test blocks the experiment." The tests now pass, so the data blocker on the
Phase 1 experiment is cleared.

This is the first change to `src/` or `scripts/` since the protocol freeze (DEC-20261015-015
forbade pre-freeze code changes; the freeze completed in DEC-20261017-021).

---

## 1. The snapshot

| Field | Value |
|-------|-------|
| Snapshot ID | `yahoo-usetf-2007-01-01_2026-09-30-2026-10-17-2ad06139` |
| Bundle SHA-256 | `2ad0613913df9065b62ba2291abc391402c1eb13d36937ba8c2bbc09d637d707` |
| Window | 2007-01-01 … 2026-09-30 (last **complete** month, so no partial month enters a return) |
| Retrieval date | 2026-10-17 |
| Candidates | 18 (`notes/pit_candidates_2026-10-17.csv`, DEC-20261017-024) |
| Daily rows | 4,966 |
| Corporate actions | 2,294 (2 splits, 2,292 dividends) |
| Risk-free | 4,941 `DGS1MO` daily observations |
| Built from commit | `382279c` |
| Location | `data/snapshots/<id>/` (git-ignored; the tracked definition is the CSV under `notes/`) |

Files, with the SHA-256 recorded in the manifest:

| File | SHA-256 |
|------|---------|
| `prices_raw.parquet` | `9bc4bc255972d53f4cc26f0f006eed8a3dc99624baf21d84df280df80979cb7c` |
| `actions.parquet` | `58b881da613a40ed42af1d159bdcf1cbeb7153565e5ebcbfc4a4166036cc4e88` |
| `rf_dgs1mo.parquet` | `f55eee9f0b22de96ac8dd35cbf0cdd44c0197d44284c22a3f9fde65406056b95` |
| `universe_pit.csv` | `9288df99293b2c174202498d732cc9e21148905178465d580cb9698a023c6b99` |
| `quality_report.md` | `ef87f752f31159ca128a64ef11145f33bf21617b3f23b5387cd61360162d484b` |

---

## 2. What the code implements

| Piece | File | Contract |
|-------|------|----------|
| Snapshot reader, PIT reconstruction, eligibility, rf | `src/robustfolio/data.py` | spec §3.1-§3.4 |
| Snapshot builder (the only network caller) | `scripts/build_snapshot.py` | protocol §5.4.9 |
| Leakage suite | `tests/test_leakage_suite.py`, `tests/conftest.py` | protocol §5.4.8 |

Rules implemented, each cited from the frozen text:

* **Snapshot in, nothing else.** `load_snapshot(snapshot_id)` is the only entry point and
  never touches the network. Vendor specifics live in one fenced `VENDOR ADAPTERS` block
  (protocol §5.4.1); downstream code takes a `Snapshot`.
* **Point-in-time or nothing.** `Snapshot.truncated(t)` returns a view containing only what
  was knowable at `t`; every derived value at `t` is asserted identical whether computed from
  the full snapshot or its truncation (protocol §5.4.3).
* **Splits** back-adjust historical prices (divide before the ex-date by the ratio);
  **cash dividends** are added to the return on the ex-date and never back-adjust the price
  level (protocol §5.4.5, both bullets). A dividend is divided by the product of split
  ratios strictly after its ex-date so it stays in the same basis as the price.
* **Eligibility** = membership window AND ≥ 60 consecutive valid months AND trailing-3-month
  average daily dollar volume > $5M AND a positive price (spec §3.3, protocol §5.4.2).
* **Missing data**: isolated gaps forward-filled ≤ 3 days; a month whose month-end is still
  missing after that is invalid for that asset (protocol §5.4.6).
* **Risk-free**: FRED `DGS1MO`, never zero-filled (protocol §5.4.6).
* **Immutability**: content-addressed ID, per-file digests, append-only (the builder refuses to
  overwrite an existing snapshot ID; corrections create a new snapshot).

---

## 3. §5.4.8 leakage suite result

Run: `.venv\Scripts\python.exe -m pytest tests -v` → **14 passed, 1 skipped**.

| # | §5.4.8 test | Verdict | Evidence |
|---|-------------|---------|----------|
| 1 | Time-travel | **Pass** | `test_1_time_travel_real` (8 random month-ends, 2012-06…2026-05), `test_1_time_travel_synthetic` (12 month-ends), plus a power control |
| 2 | Survivorship | **Skipped - vacuous in-sample** | `test_2_survivorship_is_vacuous_in_sample` records that no candidate delisted; the mechanism itself is verified by `test_2_survivorship_mechanism_is_wired` |
| 3 | Adjusted price | **Pass** | `test_3_adjusted_prices_use_only_known_actions`, `test_3_future_actions_do_not_affect_past`, `test_3_split_does_not_leak_a_spurious_return`, `test_3_dividend_branch_is_exercised` |
| 4 | Universe reconstruction | **Pass** | `test_4_membership_matches_archived_list`, `test_4_nobody_is_a_member_before_its_first_eligible_date`, `test_4_frozen_anchor_universe_is_complete` |
| 5 | Determinism | **Pass** | `test_5_same_snapshot_same_output`, `test_5_snapshot_is_byte_immutable` |

Two supporting tests guard the risk-free series (`test_rf_is_never_zero_filled`) and the
suite's own power (`test_1_time_travel_power_control`: a dividend with an ex-date after `t`
**does** change a naive whole-sample result, so immunity to it is not vacuous).

### Test 2 is vacuous, and that is recorded rather than hidden

Every confirmed candidate still trades, so there is no delisting return to verify. The test
skips with that reason instead of passing silently, and it **fails on purpose** if the
universe ever gains a delisting, so the check cannot be forgotten. Survivorship remains
*argued by construction, not measured* - the residual accepted in DEC-20261017-024.

---

## 4. Findings raised

### F10 - annualised-yield-to-monthly conversion is not pinned
`DGS1MO` is an annualised percent. `data.RF_ANNUAL_TO_MONTHLY` defaults to `"geometric"`
(`(1+y)^(1/12)-1`, compounding-consistent); `"simple"` (`y/12`) is the alternative. At a 5%
yield the two differ by ~0.009 percentage points per month - immaterial to a Sharpe ratio,
but it is a frozen-value gap and is not silently chosen. **Owner confirmation requested.**

### F11 - risk-free observation month is not pinned
§5.5.5 says "as observed at *t*" while §5.5.4 places decisions and execution at the close of
`t-1`. `data.RF_ALIGN` defaults to `"prior_month"` (the yield observed at the last trading day
of month `t-1` prices month `t`), which is the no-lookahead reading and matches the standard
one-month-bill convention; `"same_month"` is the literal §5.5.5 reading. **Owner confirmation
requested.**

### F12 - the §5.4.2 liquidity floor is binding, so the eligible universe shrinks from 18 to 17
The candidate list has 18 instruments, but eligibility is a filter, not a membership roll.
`RWX` (SPDR Dow Jones International Real Estate) fails `ADV > $5M`:

| Period | Eligible count | RWX 3-month ADV |
|--------|----------------|-----------------|
| 2012-06 … 2021-11 | 18 | $15-28M (2012-2020) |
| 2021-12 … 2026-09 | 17 (intermittently 18) | falling; $0.99M by 2026 |

RWX qualifies for 124 months and fails for 48. This is the frozen rule working as written, not
a defect, but it must be visible: the strategy's investable set is time-varying, and a name
leaving the set generates a real, costed divestment. It is also a **finding about the universe
reconstruction**: `RWX` was added to the candidate list (DEC-20261017-024) and is now
effectively absent for the last third of the sample. No decision is required to proceed, but
the owner should know before Gate 2.

---

## 5. Confirmations

* **The derived anchor holds on real data.** All 18 candidates are eligible at the frozen
  backtest start (2012-06-29) - `test_4_frozen_anchor_universe_is_complete`. This is the first
  independent, data-level confirmation of the DEC-20261017-024 derivation (T = 168 months +
  60-month window → training 2007-06…2012-05, OOS 2012-06…2026-05).
* **Nothing is eligible before the anchor.** 65 months (2007-01…2012-05) return an empty
  eligible set; the first eligible month is 2012-06. The record is 237 months long, so there is
  headroom and no boundary artifact.
* **The split branch is genuinely exercised.** ETFs split rarely, so this was not
  guaranteed: the universe contains two real splits, `EEM` 3:1 and `SLV` 10:1, both dated
  2008-07-24. Split handling is therefore validated against real data, not only against the
  synthetic fixture.
* **OOS returns are complete**: 172 month-ends from 2012-06, no missing values.

Two real bugs were caught by the suite before any result existed: (a) month-end prices were
being read from *raw* rather than *split-adjusted* closes, which produced a spurious -49%
monthly return at the 2018 synthetic split; (b) `DGS1MO` printing a genuine 0.00 in 2015 was
initially confused with a forbidden zero-substitution. Both are fixed; the fixes are what the
"14 passed" above refers to.

---

## 6. Residual limitations

1. **Survivorship is argued, not measured** (§5.4.8 test 2 vacuous, §5.4.5 untested in-sample).
   In-scope closures 2012-2026 are absent from the candidate list; results remain
   universe-conditional and the §5.4.7 downgrade clause stays in reserve.
2. **Vendor restatement.** Yahoo and FRED can restate history. The snapshot pins the values
   actually used; a restatement makes a *new* snapshot, never a silent change.
3. **Yahoo is not a point-in-time vendor.** Raw unadjusted prices plus ex-post corporate actions
   are the satisfiable two-tier contract frozen in §5.4.1; this is a known and accepted limit,
   not an oversight.
4. **`RF_ANNUAL_TO_MONTHLY` and `RF_ALIGN`** are implementation conventions pending F10/F11.

---

## 7. Reproduction

```powershell
# build (network; creates a new immutable snapshot)
.\.venv\Scripts\python.exe scripts\build_snapshot.py --retrieval-date 2026-10-17

# verify the leakage suite
.\.venv\Scripts\python.exe -m pytest tests -v
```

Requirements added: `pytest`, `cvxpy>=1.4` (the latter for the C3 optimizer, not used here).

---

## 8. Revision history

| Version | Date | Change | Author |
|---------|------|--------|--------|
| 1.0 | 2026-10-17 | Initial evidence record: snapshot `…-2ad06139`, §5.4.8 suite pass, findings F10-F12 | Ken Ira Lacson Talingting |
