# Point-in-Time Candidate Universe — Reconstruction Record — 2026-10-17

**Owner:** Ken Ira Lacson Talingting
**Purpose:** Reconstruct the point-in-time (PIT) candidate universe required by `evaluation_protocol.md` §5.4.7 and consumed by `model_and_method_spec.md` §3.1/§3.3. This is the last **Gate 1** data blocker (protocol §8.4).
**Status:** **Confirmed** — v1.0, owner-confirmed 2026-10-17 (DEC-20261017-024). C1–C3 confirmed as drafted (§0). Writing and confirming were kept as separate acts, per the freeze discipline.
**Not a Tier 0 document. Not a contract.** The contract is `model_and_method_spec.md` §3.3 and `evaluation_protocol.md` §5.4; this note supplies the membership the contract consumes.
**Companion artifact:** [`pit_candidates_2026-10-17.csv`](pit_candidates_2026-10-17.csv) — the same list in the snapshot's `universe_pit.csv` column format (`ticker, first_eligible, last_eligible, source_note`).
**Related:** `evaluation_protocol.md` §4.3, §5.4.2, §5.4.5, §5.4.7, §5.4.8, §8.4; `model_and_method_spec.md` §3.1–§3.4; `scope_and_non_goals.md` §3.1; `decision_log.md` DEC-20261017-020 (finding N3); `risk_register_and_premortem.md` R-D02.
**Logged by:** DEC-20261017-024 (owner confirmation of C1–C3).

**What this is not.** It is not a snapshot. No prices, actions, or risk-free series exist yet. It defines *membership* only; the snapshot builder (§5.4.9) will embed it as `universe_pit.csv`.

---

## 0. The decisions this record records

**All three were confirmed by the owner on 2026-10-17 (DEC-20261017-024): C1 as stated; C2 as drafted (18 instruments); C3 accepted as documented**, with the archived-PIT-screen upgrade declined.

**C1 — The anchor.** The candidate list is fixed as of the **backtest start**, read as the first out-of-sample month, **2012-06**. Consequence: a candidate must carry continuous monthly prices across the first estimation window (2007-06 … 2012-05), i.e. **inception on or before 2007-05-31**.
*Not load-bearing, recorded for the record:* the alternative reading — anchor = the data start (2007-06) — yields the **same** list, because "listed at 2007-06" and "60 valid months by 2012-06" describe the same set. The interpretation changes the *wording* of the rule, not the membership.

**C2 — The pool.** 18 instruments, one liquid representative per bucket (§3), inside the §5.4.2 target of 15–25.

**C3 — The residual survivorship limitation** (§5) and whether to accept it as documented or fund an archived-screen upgrade.

---

## 1. The anchor, and why it is 2012-06

The anchor is forced by already-frozen values; it is not a new choice.

1. §5.4.2 requires ≥ 60 months of history and sets "minimum history at backtest start: 60 months".
2. §4.3 sets the estimation window to 60 months, rolling.
3. §13.1 fixes the stationary-bootstrap block length at 6 months and notes the \(T^{1/3}\) heuristic **"for \(T = 168\) months"** — i.e. the frozen protocol presumes a **168-month** out-of-sample record.
4. §5.2 is a walk-forward: the first out-of-sample fold begins immediately after the first 60-month window, and folds step 12 months.

Therefore the record must be \(60 + 168 = 228\) months: training **2007-06 … 2012-05**, out-of-sample **2012-06 … 2026-05**. (Phase 1's exploratory sample was 232 months, 2007-06 … 2026-09; the extra 4 months fall past the last complete 12-month fold, which is consistent.)

Therefore:

- **Backtest start (§5.4.7) = 2012-06.**
- **First estimation window = 2007-06 … 2012-05.** Candidates must have a continuous monthly series across it.
- **Inception cut-off = 2007-05-31.** A fund listed 2007-06-01 has exactly 60 valid months when the first OOS fold opens — the §5.4.2 rule satisfied exactly.

**Why not anchor at 2007-06 (the data start)?** That reading would demand 60 months of history *by* 2007-06, i.e. inception ≤ 2002-06, which excludes **every** fixed-income, commodity, and real-estate instrument in scope (the earliest — `TLT`/`IEF`/`SHY`/`LQD` — launched 2002-07-22). That reading is unsatisfiable for the four required asset classes, so it cannot be the intended one. The ambiguity is resolved by satisfiability.

**Robustness to a ±1-month anchor shift.** The nearest inception to the cut-off is `HYG` (2007-04-04), which clears both a 2007-04-30 and a 2007-05-31 boundary. The membership is invariant to the harness's exact first-fold month.

---

## 2. Method — and its limits

**What the frozen rules demand of the list.** §5.4.7: defined as of the backtest start, not today; a member that later delists stays until its delisting date; delisting returns are included; nothing is dropped for not existing today; reconstructed from PIT evidence. §5.4.2: US-listed ETFs spanning equity, fixed income, commodities, real estate; 15–25 liquid names; count fixed at reconstruction; USD; long-only, unlevered.

**Method used.**

1. **Bucket coverage.** Candidates were chosen to cover the four required classes with **one liquid representative per bucket** (§3). Category labels come from the issuer's index definition.
2. **Inception screen — objective and verifiable.** Each inception date is taken from the issuer (fact sheet / prospectus) or an SEC EDGAR N-1A filing. This is genuine PIT evidence: the fund was listed and tradable on that date. All 18 satisfy inception ≤ 2007-05-31.
3. **Liquidity is delegated to the contract, not baked in here.** §5.4.2's ADV > \$5 M and positive-price conditions are *per-\(t\)* eligibility rules (§3.3), evaluated from the snapshot's volume/price data at each rebalance. The list therefore needs no PIT ADV screen of its own — which removes the hardest PIT data requirement.
4. **What was NOT obtained.** §5.4.7.5 asks for "archived ETF screens, historical fund lists, SEC filings". Step 1 is a **2026 judgement** selection of prominent, bucket-representative funds; no dated 2007/2012 AUM-or-liquidity screen was used. That is a residual survivorship exposure: funds were picked *because* they are prominent today. The inception screen bounds it (no post-hoc entrant is possible), but does not remove it. See §5.

---

## 3. The candidate list (18 instruments)

| # | Ticker | Name (short) | Bucket | Asset class | Inception | Evidence |
|---|--------|--------------|--------|-------------|-----------|----------|
| 1 | `SPY` | SPDR S&P 500 ETF Trust | US large-cap equity | Equity | 1993-01-22 | Issuer/EDGAR; first US ETF |
| 2 | `MDY` | SPDR S&P MidCap 400 ETF Trust | US mid-cap equity | Equity | 1995-05-04 | Issuer fact sheet |
| 3 | `IWM` | iShares Russell 2000 ETF | US small-cap equity | Equity | 2000-05-22 | Issuer fact sheet |
| 4 | `EFA` | iShares MSCI EAFE ETF | Developed ex-US equity | Equity | 2001-08-14 | Issuer fact sheet |
| 5 | `EEM` | iShares MSCI Emerging Markets ETF | Emerging equity | Equity | 2003-04-07 | Issuer fact sheet |
| 6 | `VNQ` | Vanguard Real Estate ETF | US real estate | Real estate | 2004-09-29 | Issuer profile |
| 7 | `RWX` | SPDR Dow Jones International Real Estate ETF | Int'l real estate | Real estate | 2006-12-15 | Issuer fact sheet |
| 8 | `GLD` | SPDR Gold Shares | Gold | Commodities | 2004-11-18 | Trust prospectus |
| 9 | `SLV` | iShares Silver Trust | Silver | Commodities | 2006-04-21 | Issuer fact sheet |
| 10 | `DBC` | Invesco DB Commodity Index Tracking Fund | Broad commodities | Commodities | 2006-02-03 | Issuer fact sheet |
| 11 | `SHY` | iShares 1–3 Year Treasury Bond ETF | Short Treasury | Fixed income | 2002-07-22 | Issuer fact sheet (launch date) |
| 12 | `IEF` | iShares 7–10 Year Treasury Bond ETF | Intermediate Treasury | Fixed income | 2002-07-22 | Issuer fact sheet |
| 13 | `TLT` | iShares 20+ Year Treasury Bond ETF | Long Treasury | Fixed income | 2002-07-22 | Issuer fact sheet |
| 14 | `LQD` | iShares iBoxx \$ Investment Grade Corporate Bond ETF | IG credit | Fixed income | 2002-07-22 | Issuer fact sheet; some vendors show 2002-07-26 |
| 15 | `AGG` | iShares Core U.S. Aggregate Bond ETF | US aggregate | Fixed income | 2003-09-22 | Issuer fact sheet |
| 16 | `TIP` | iShares TIPS Bond ETF | TIPS | Fixed income | 2003-12-04 | Issuer fact sheet |
| 17 | `HYG` | iShares iBoxx \$ High Yield Corporate Bond ETF | US high yield | Fixed income | 2007-04-04 | Issuer fact sheet |
| 18 | `MBB` | iShares MBS ETF | US MBS | Fixed income | 2007-03-13 | Issuer fact sheet (launch date) |

**Coverage (§5.4.2).** Equity 5 · Real estate 2 · Commodities 3 · Fixed income 8 · **Total 18**, inside the 15–25 target. Fixed income carries the most buckets because it holds the most distinct risk factors (rate level, curve shape, credit, inflation, prepayment).

**Instrument type.** All long-only, unlevered, USD, US-listed. `GLD`/`SLV` are grantor trusts and `DBC` is a commodity pool, not 1940-Act funds; all three are plain-vanilla, physical/futures, non-leveraged, and all three were in the Phase 1 universe.

---

## 4. O1 compliance — no cash / T-bill proxy

Excluded by rule (`model_and_method_spec.md` §3.4): `BIL`, `SHV`, `MINT`, `SGOV`, and any ≤ 3-month-T-bill or money-market ETF. Duration-bearing Treasuries (`SHY` = 1–3 y and longer) remain eligible.

Consequence for the record: the Phase 1 universe's `BIL` is dropped, so the Phase 1 `DEFAULT_UNIVERSE` in `src/robustfolio/data.py` **does not match** this list. That is expected and is a Gate-1/2 code change, not a documentation change (DEC-20261015-015).

---

## 5. Delisting / survivorship screen — evidence and residual

**Evidence gathered (2026-10-17).** ETF.com's closure database (2011–2026) and iShares' own closure page. The closure record is dominated by: (a) sub-\$100 M and single-theme funds, (b) leveraged / inverse products (out of scope, scope §5.1), (c) exchange-traded notes — unsecured debt, out of scope (§5.1), (d) term-maturity "iBonds" funds that self-liquidate by design, and (e) currency trusts. Representative scale: Global X's 2012 liquidations together were **< 1 % of the firm's AUM** (largest \$2.6 M).

**Finding.** No **in-scope** liquidation was found between 2012 and 2026 — i.e. no large, liquid, plain-vanilla, non-leveraged, non-ETN ETF in the four required classes that was available at 2007-06. Every one of the 18 candidates is still listed as of retrieval.

**Consequences.**

1. The §5.4.8.2 **survivorship test is vacuous in-sample**: there is no delisting to exercise. The frozen protocol already anticipates exactly this — §5.4.5 states the conservative −100 % delisting default is *"untested on the MVP universe (no candidate delists in-sample)"*.
2. The residual bias is therefore **argued, not measured**. The list's defensibility rests on (i) a survival-independent construction criterion (a pre-2007-06 inception screen) and (ii) the thinness of in-scope large-fund closures — not on an exercised delisting path.
3. Per §5.4.7, any result is **universe-conditional** and the limitation is recorded here. The §5.4.7 downgrade clause (→ exploratory) is **not** triggered by any missing delisted member; it is held in reserve should an archived screen later surface one.

**Options for the owner.**

- **(a) Accept as documented — recommended.** The inception screen is objective; the in-scope closure record is thin; universe-conditional claims stay flagged and the limitation is logged against R-D02.
- **(b) Upgrade to archived PIT screens.** Obtain dated 2007/2012 AUM + ADV rankings to *prove* bucket-representativeness and to search systematically for in-scope closures. This needs a paid source → budget approval (§5.4.1 forbids paid data without it).

**Chosen: (a)** — accepted as documented (DEC-20261017-024).

---

## 6. Consistency with the frozen documents

- **Count.** 18, inside §5.4.2's 15–25; fixed at reconstruction; no mid-backtest expansion (which would need a §8 amendment).
- **Overlap with Phase 1.** 14 of the Phase 1 names carry over; `BIL` is removed; `MDY`, `AGG`, `MBB`, `SLV` are added.
- **\( \gamma \) derivation.** §4.3 justifies \( \gamma = 10 \) from a term-balance point of ≈ 12.3 computed on the 15-name Phase 1 universe. This list preserves that universe's structure and its strong collinearity, so the order-of-magnitude justification stands. \( \gamma \) is frozen at 10 regardless (§16).
- **Stale cross-reference, fixed.** `notes/tests_BCD_spec_2026-10-17.md` §1 previously said "the frozen MVP universe (15 ETFs)" — the *Phase 1* universe, superseded by this list. Corrected at confirmation (DEC-20261017-024; notes files are not Tier 0, so this is a documentation tidy, not a contract change).

---

## 7. What this does and does not authorize

**Does:** define candidate *membership*, ready to be embedded in a snapshot; unblocked the point-in-time item on the Gate 1 critical path (protocol §8.4).
**Does not:** create a snapshot; supply prices, actions, or the risk-free series; authorize any confirmatory run; register any experiment (§12.4 needs a snapshot ID, which does not exist); touch `src/` or `scripts/` (DEC-20261015-015).

**Follow-ups on confirmation.**

1. ~~Freeze this list and record a decision-log entry.~~ **Done** — DEC-20261017-024; this note is v1.0 `Confirmed`.
2. Have the snapshot builder write `universe_pit.csv` from the companion CSV. **Pending** — no snapshot exists yet.
3. ~~Correct the stale "15 ETFs" reference in `notes/tests_BCD_spec_2026-10-17.md` §1.~~ **Done.**
4. ~~Update the working-inputs line in `docs/README.md` and the R-D02 entry in `risk_register_and_premortem.md` §8.~~ **Done** — `docs/README.md` v1.6; `risk_register_and_premortem.md` v1.3.
5. Run §5.4.8 tests 1, 3, 4, 5 against the snapshot (test 2 is vacuous in-sample, per §5). **Pending — the last Gate 1 item.**

---

## Model tags

- **[Inversion]** — the survivorship question is attacked by asking what *should* be missing (delisted members), not by asserting the list is complete.
- **[First Principles]** — the anchor is derived from the frozen window arithmetic, not asserted.
- **[Experimental]** — the list is a pre-registration input; membership is fixed before any result is seen.

---

## Revision history

| Date | Version | Change | Author |
|------|---------|--------|--------|
| 2026-10-17 | 0.1 | Initial draft: PIT candidate list (18 instruments), anchor derivation (2012-06 / inception ≤ 2007-05-31), inception evidence with sources, O1 compliance, delisting/survivorship screen and residual, consistency checks. Status `Draft`, pending owner confirmation of C1–C3. | Ken Ira Lacson Talingting |
| 2026-10-17 | 1.0 | **Confirmed** (DEC-20261017-024): C1 (anchor 2012-06 / inception ≤ 2007-05-31), C2 (18 instruments as drafted), C3 (survivorship limitation accepted as documented). Promoted the follow-up list; the only remaining Gate 1 item is the §5.4.8 leakage suite. | Ken Ira Lacson Talingting |
