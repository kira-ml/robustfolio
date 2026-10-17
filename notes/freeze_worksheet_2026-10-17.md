# Freeze Worksheet — 2026-10-17

**Owner:** Ken Ira Lacson Talingting
**Purpose:** Decision-ready sheet for the `evaluation_protocol.md` freeze session. Every `[PROPOSED]` value in §18, every open freeze-session note, and every finding from DEC-20261015-015 and DEC-20261017-019 is restated here with a **recommended value**, a **rationale**, and a **source tag**.
**Not a Tier 0 document. Not a contract. Not a decision.** The recommendations below are proposals. Only the owner's confirmation at the freeze session converts them into frozen values.
**Consumed by:** `evaluation_protocol.md` §18 freeze session.
**Supersedes:** nothing. **Superseded by:** the frozen `evaluation_protocol.md`.
**Companion input:** [`freeze_inputs_2026-10-15.md`](freeze_inputs_2026-10-15.md) (DEC-20261015-015 findings), [`tests_BCD_spec_2026-10-17.md`](tests_BCD_spec_2026-10-17.md) (DEC-20261017-020).

**Source tags**

- `[Paper: …]` — directly specified by a cited source.
- `[Convention]` — a standard default; no single canonical source.
- `[Judgment]` — owner decision; no canonical source.
- `[Derived]` — computed from the project's own data or from a stated first-principles condition.
- `[Phase 1]` — carried from the exploratory Phase 1 configuration.

---

## 0. Summary — the values to freeze if every recommendation is accepted

| Where | Proposed now | Recommend | Tag |
|-------|--------------|-----------|-----|
| §5.2 estimation window | 36 | **60** months, rolling | Judgment |
| §5.2 test / step | 12 / 12 | **12 / 12** | Judgment |
| §5.2 convention | ambiguous (code: expanding-within-test) | **rolling 60-month, re-estimated monthly** | Judgment + framing §5 |
| §5.3 embargo | 1 month | **1 month**, §5.3 scoped to hyperparameter selection only | Paper: López de Prado 2018 |
| §6.1 significance | DSR p<0.05 AND PSR>0.95 | **keep**, with PSR threshold stated as `SR* = SR_best_baseline` | Paper: Bailey & López de Prado 2014 |
| §6.2 materiality | ΔSharpe ≥0.20; turnover ≤2×; MDD ≤ +5pp | **keep** | Convention |
| §6.3 robustness | 3 cost levels; 60% folds; no fold >40% | **keep** | Judgment |
| §12.8 FDR | q = 0.10 | **keep q = 0.10** (convention, not DSR) | Convention |
| §13.1 bootstrap | block 6; 2000 reps | **keep** | Judgment |
| §4.2 baseline set | B1–B5 | **keep B1–B5**; `inverse_vol` demoted to extension | Judgment |
| §4.3 estimation window | 36 | **60** (match §5.2) | Judgment |
| §4.3 `w_max` | 0.30 | **0.30, applied uniformly to every method incl. B1/B2** | Judgment (fixes F1) |
| §4.3 risk aversion γ | 5 | **≈10**, after an empirical scale check | Derived |
| §4.4 B2 solver | unspecified | **cyclic-coordinate-descent ERC**; ε = 1e-6 | Paper: Spinu 2013 / Griveau-Billion 2013 |
| §4.4 B5 penalty λ | κ (10bps) | **λ = κ = 0.001** (monthly return per unit one-way turnover), convex QP | Derived |
| §5.4.1 sources | Yahoo adjusted | **raw unadjusted + corporate actions + SHA-256 snapshots** | Judgment (fixes F8) |
| §5.4.2 eligibility history | 36 months | **60 months at first rebalance** | Judgment |
| §5.4.6 missing rf | silent 0 | **forward-fill ≤1 month, else FRED DGS1MO** | Judgment (fixes 4c) |
| §5.4.9 cache | none | **content-addressed; confirmatory runs read snapshots only** | Judgment (fixes 4a) |
| §5.5.1 impact term | off | **off** (MVP) | Judgment |
| §5.5.3 κ levels | 0/5/10/20/50 | **keep**; baseline κ = 10bps | Convention |
| §5.5.4 execution | close of t | **signals through close t−1; execute close t−1; hold month t** | Judgment (no lookahead) |
| §5.5.5 rf convention | mixed | **same R_f for gross and net Sharpe** | Judgment (fixes 1) |
| §5.5.6 λ | κ or tuned | **λ = κ**; tuned λ is a registered extension | Derived |
| §7 H1.1 | max weight >0.40 | **test on *uncapped* sample MVO** | Judgment (fixes cap trap, §11) |
| §7 H1.2 | turnover ratio >2.0 | **keep** | Judgment |
| §8.3 time-boxes | as listed | **keep** | Judgment |
| §8.6 K7 | 3 invalidations | **keep** | Judgment |
| §14.3 decision time-box | 1 week | **keep** | Judgment |

---

## 1. Measurement protocol

### §5.2 — Walk-forward

| Item | As written | Recommendation | Tag | Rationale |
|------|-----------|----------------|-----|-----------|
| Estimation window | 36 | **60** | Judgment | Problem framing §5 names non-stationarity as a root cause; but with 15 assets a 36-month sample covariance is poorly conditioned (T/p ≈ 2.4). 60 is better conditioned and preserves Phase 1 continuity. Declare window a swept dimension (see Tests B/C/D). |
| Test window | 12 | **12** | Judgment | 12 observations/fold; non-overlapping folds are needed for the §6.3 "≥60% of folds" criterion to be meaningful. |
| Step | 12 | **12** | Judgment | Non-overlapping. A step of 1 would create overlapping folds and violate fold independence. |
| Convention (DEC-015 finding 4d) | not stated; code is expanding-within-test | **rolling 60-month window, re-estimated every month** | Judgment | The code's `train + test.iloc[:t]` is neither pure rolling nor pure expanding. Pick one and name it. Rolling is the more conservative choice under non-stationarity (framing §5). The code must be changed to match; that change is post-freeze. |

### §5.3 — Purged CV and embargo (DEC-015 finding 3-adjacent; freeze_inputs §3)

**Recommendation:** Retain §5.3 but scope it explicitly: walk-forward (§5.2) is the **sole evaluation structure**. Purged k-fold CV applies **only** if a method requires fitted hyperparameters, and then only on training data, never touching test. Embargo = **1 month**. Mark §5.3 `[SCOPED: hyperparameter selection only]`.
**Tag:** `[Paper: López de Prado 2018, Ch. 7]` for the method; `[Judgment]` for the 1-month embargo.
**Rationale:** In strict walk-forward there is no train/test overlap, so purging is unnecessary for evaluation. Leaving §5.3 unscoped is the ambiguity that freeze_inputs §3 flagged. If no method is tuned (all parameters frozen), §5.3 becomes inert — which is the correct, simplest outcome.

### §§6.1–6.3 — Thresholds

| Item | As written | Recommendation | Tag | Rationale |
|------|-----------|----------------|-----|-----------|
| §6.1 DSR | p < 0.05 | **keep** | Paper | Bailey & López de Prado (2014); `SR*` = expected max SR under N independent trials. |
| §6.1 PSR | > 0.95 "against the best baseline" | **keep, and state `SR* = SR_best_baseline` explicitly** | Paper | Resolves freeze_inputs §2: without the explicit threshold, the two bullets are the same test written twice. DSR uses `SR* = SR_0`; PSR uses `SR* = SR_best_baseline`. |
| §6.2 materiality | ΔSharpe ≥ 0.20; turnover ≤ 2× baseline; MDD within 5pp | **keep** | Convention | 0.20 annualized net Sharpe is a defensible economic-materiality floor for a monthly strategy. |
| §6.3 robustness | ≥3 cost levels; ≥60% folds; no fold >40% | **keep** | Judgment | Adequate defense against single-fold and single-cost-level flukes. |

### §12.8, §13.1

| Item | As written | Recommendation | Tag | Rationale |
|------|-----------|----------------|-----|-----------|
| §12.8 FDR | q = 0.10 | **keep q = 0.10** | Convention | Benjamini-Hochberg (1995); 0.10 is the common exploratory/omics default. **Not** from the DSR paper (freeze_inputs §4). Record this provenance. |
| §13.1 block length | 6 months | **keep** | Judgment | `T^(1/3)` heuristic for T = 168 → ≈5.5. Politis & Romano (1994) is the method's origin, not the value. |
| §13.1 replications | 2000 | **keep** | Judgment | Standard; local compute allows it. |
| §13.1 confidence level | 90% reporting / 95% decision | **keep** | Judgment | |

---

## 2. Baselines (§4)

### §4.2 — Baseline set

**Recommendation.** Confirm the MVP set as **B1 (1/N), B2 (risk parity), B3 (sample MVO), B4 (minimum variance), B5 (turnover-penalized MVO, λ=κ)**. No extension is promoted. `inverse_vol` — currently implemented — is an **extension** under §4.2 and **must be removed from the MVP comparison** or registered as a separate extension experiment (`scope_and_non_goals.md` §4.3).
**Tag:** `[Judgment]` + `[Inversion]`.
**Rationale:** Resolves DEC-20261017-019 F2. Two MVP baselines (B2, B4) are missing while a non-MVP method is present; that is the §7 scope-creep signal.

### §4.3 — Common definitions

| Item | As written | Recommendation | Tag | Rationale |
|------|-----------|----------------|-----|-----------|
| Estimation window | 36 | **60** | Judgment | Match §5.2. |
| `w_max` | 0.30 | **0.30, uniform across all methods** | Judgment | Resolves F1. A baseline that bypasses the box constraint (§4.7 invalidation condition) makes the comparison invalid. 0.30 forces ≥4 assets with a 15-asset universe. Equal weight (0.067) is unaffected. |
| Risk aversion γ | 5 | **≈10** | Derived | γ is currently under-determined. The objective `μ'w − (γ/2)w'Σw` is return-dominated unless the two terms are of comparable magnitude. Using Phase-1-scale monthly values (μ_p ≈ 0.005, w'Σw ≈ 9e-4), balance requires γ ≈ 2μ_p / (w'Σw) ≈ 10. **Confirm empirically before freezing.** γ = 1.0 (current code) makes B3 a strawman — maximally return-seeking, hence maximally extreme — which is the R-S02 "fake wins" failure mode. γ must be a *representative* optimizer, not a caricature. |

### §4.4 — Per-baseline specifications

**B2 — Risk parity (ERC).** Recommendation: solve via **cyclic coordinate descent** (Spinu 2013; Griveau-Billion et al. 2013) or a convex log-barrier formulation. Diagonal loading **ε = 1e-6**. Add an ERC verification test: `max|RC_i − RC_j| < 1e-8` at convergence. `[Paper]` + `[Judgment]`.

**B5 — Turnover-penalized MVO (L1).** Recommendation: **λ = κ = 0.001** in monthly-return units per unit of one-way turnover, and solve as a **convex QP with auxiliary variables** `u_i ≥ |w_i − w_i^-|` (linear constraints), *not* the current subgradient SLSQP. `[Derived]`.
**Rationale:** Resolves DEC-20261015-015 finding 2. Under the proportional cost model, `λ = κ` aligns the penalty with the actual cost (§5.5.6). Phase 1's λ = 0.1 was ~2× the return term and ~20× the risk term — it tested "minimize turnover", not "penalize turnover". Also resolves DEC-20261017-019 F4: `sample_mvo` and `unconstrained_sample_mvo` differed on cap *and* penalty; the MVP comparison now varies one dimension at a time.

---

## 3. Data contract (§5.4)

### §5.4.1 — Sources (DEC-019 F8; the satisfiability judgment call)

**Recommendation — the two-tier contract.** Freeze the MVP source as:

1. **Raw unadjusted OHLCV** from a free source (Yahoo via `yfinance` with `auto_adjust=False`), stored as an immutable snapshot.
2. **Corporate-action history** (splits, dividends) from the same adapter, snapshotted separately.
3. **Point-in-time adjusted series reconstructed** at evaluation time from actions with ex-date ≤ t (§5.4.4).
4. **Risk-free rate** from FRED `DGS1MO` (already the §5.4.1 proposal).

Any residual reliance on a vendor-adjusted series is **downgraded to exploratory** and disclosed.
**Tag:** `[Judgment]` + `[First Principles]` (point-in-time or nothing).
**Rationale:** The §5.4 contract as drafted is not currently satisfiable (F8): `data.py` uses `auto_adjust=True` with no snapshot. Freezing an unsatisfiable contract invites a K6 invalidation on the first confirmatory run. The two-tier formulation is satisfiable at the $0 data budget and keeps the point-in-time requirement intact for the primary path.

### §5.4.2 — Universe and eligibility

| Item | As written | Recommendation | Tag | Rationale |
|------|-----------|----------------|-----|-----------|
| Candidate size | 15–25 | **freeze at the Phase 1 universe of 15** | Judgment | Smallest sufficient (MDL). Expansions require a §8 amendment. |
| Minimum history at start | 5 years | **60 months** | Judgment | Must match the estimation window; a 36-month-eligible asset cannot fill a 60-month window. Resolves the internal inconsistency between the 5-year start rule and the 36-month eligibility rule. |
| Eligibility history | 36 months | **60 months at first rebalance** | Judgment | As above. |
| ADV threshold | $5M | **keep $5M**, note non-binding | Judgment | All 15 ETFs carry ADV ≫ $5M; the rule is inert for this universe but correct in principle. |

### §5.4.5 — Delisting

**Recommendation:** Keep the conservative default but **flag it as untested**. All 15 candidates have inception dates before 2007 and none delisted in-sample, so the assumption is never exercised — which is itself the survivorship problem (§11 below), not a validation.
**Tag:** `[Judgment]`.

### §5.4.6 — Missing data (DEC-015 finding 4c)

| Case | Recommendation | Tag |
|------|----------------|-----|
| Isolated missing trading day | forward-fill ≤ 3 consecutive days, mark imputed | Judgment |
| Extended gap (>3 days) | asset ineligible for the gap window | Judgment |
| **Missing risk-free rate** | **forward-fill ≤ 1 month; if still missing, use the FRED DGS1MO value directly** — never substitute 0 | Judgment |

**Rationale:** The code's `.fillna(0.0)` silently substitutes a zero risk-free rate, which *overstates* Sharpe in high-rate months. Because the rf is always observable from FRED, there is no legitimate use for the zero substitution. Resolves 4c.

### §5.4.9 — Snapshots and cache (DEC-015 finding 4a)

**Recommendation:**
- Snapshot naming: `<source>-<asset_class>-<start>_<end>-<retrieval_date>-<hash8>` (as specified).
- Cache: **content-addressed by `(source, tickers, date-range, retrieval parameters)`**. A stale cache entry is never substituted for a fresh fetch.
- **Confirmatory runs must read an immutable snapshot, not the live cache.** The cache is a development convenience only.

**Tag:** `[Judgment]` + `[Inversion]`. **Rationale:** the current cache silently returns stale data (4a). Resolves it by separating "convenience cache" from "auditable snapshot".

---

## 4. Cost model (§5.5)

| Item | As written | Recommendation | Tag | Rationale |
|------|-----------|----------------|-----|-----------|
| §5.5.1 size-dependent impact | off by default | **off for MVP** | Judgment | Keeps the MVP loop minimal; documented as a limitation (§5.5.8). |
| §5.5.3 κ levels | 0/5/10/20/50 bps | **keep**; baseline κ = 10bps | Convention | Sensitivity band is the robustness device. |
| §5.5.4 execution | close of rebalance date | **signals through close of month t−1; execute at close t−1; hold through month t** | Judgment | Removes the mild optimism of computing and executing at the same close. Matches the code's one-month lag and the no-lookahead rule (§5.4.3). Document as "close-to-close, one-month lag". |
| §5.5.5 rf convention (DEC-015 finding 1) | gross uses no rf; net uses rf | **both gross and net Sharpe subtract the same PIT rf series** | Judgment | Resolves 1. `Cost drag = gross Sharpe − net Sharpe` under the same rf. Phase 1's "gross Sharpe" was a raw return-to-vol ratio, not a Sharpe; its cost-drag column conflated cost with the rf level. |
| §5.5.6 λ | κ or tuned | **λ = κ**; tuned λ is a registered extension | Derived | Cost-penalized alignment; see §4.4 B5. |

---

## 5. Governance (§8)

| Item | Recommendation | Tag | Rationale |
|------|----------------|-----|-----------|
| §8.3 time-boxes | **keep** (10 h/week; 6 months total; 2/6/6/4/4-week phases; $0 budgets) | Judgment | Realistic for a solo part-time owner; enforce via K4/K5. |
| §8.4 gate exit criteria | **usable for gates 1–4; Gate 0 not yet met — see §11** | Judgment | Gate 0 requires an R1 scan of ≥10 tools/papers/repos; the Phase 0 scan (§4.1) names 4. |
| §8.2 decision rights | **keep**; reasoning-partner escalation stands | Judgment | The framework's assignment to the reasoning partner is consistent with the roster. |

---

## 6. Falsification and triggers (§7, §8.6, §14.3)

| Item | As written | Recommendation | Tag | Rationale |
|------|-----------|----------------|-----|-----------|
| §7 H1.1 | max abs weight > 0.40 in ≥1 fold | **test on *uncapped* sample MVO** | Judgment | If a 0.30 cap is enforced uniformly, *no* capped method can exceed 0.40, so H1.1 would trivially fail by construction (see §11). The extremeness claim must be tested on the uncapped optimizer, with the capped variant reported as a separate treatment. |
| §7 H1.2 | turnover ratio > 2.0 | **keep** | Judgment | Phase 1 observed ≈7.5×; 2.0 is a conservative threshold that a cap may lower. |
| §8.6 K7 | 3 invalidations in a family | **keep** | Judgment | |
| §14.3 decision time-box | 1 week | **keep** | Judgment | |

---

## 7. Cross-document consistency (§18)

| Check | Recommendation |
|-------|----------------|
| §8.6 triggers consistent with §8.3 time-boxes | Confirm — K4/K5 reference §8.3 values. |
| §9 sunk-cost firewall | Confirm acceptable as written. |
| §10 forbidden pivots | Confirm acceptable as written. |
| §14.3 authority matches §8.2 | Confirm — both assign to Owner. |
| §16 conflict resolution internally consistent | Confirm — §16 must be updated to reflect that §4/§5.4/§5.5/§12 are now internal. |

---

## 8. Resolution map — DEC-20261015-015 findings

| Finding | Status | Resolution |
|---------|--------|------------|
| 1 — gross Sharpe ≠ Sharpe | **Resolve** | §5.5.5: same rf for gross and net; §2 note updated. |
| 2 — λ scale-dominated | **Resolve** | §4.4 B5 + §5.5.6: λ = κ, convex QP. |
| 3 — SLSQP fallback | **Closed** prior | DEC-20261015-016. Remove the fallback branch in the Phase 2 rewrite. |
| 4a — stale cache | **Resolve** | §5.4.9: content-addressed cache; snapshots for confirmatory runs. |
| 4b — duplicate turnover function | **Resolve** | Single canonical definition: `Turnover(t) = Σ|w_i(t) − w_i(t⁻)|`, annualized ×12, one-way. Delete `metrics.annualized_turnover`. |
| 4c — silent zero rf | **Resolve** | §5.4.6: forward-fill ≤1 month, else FRED. |
| 4d — walk-forward convention | **Resolve** | §5.2: rolling 60-month, monthly re-estimation. |

## 9. Resolution map — DEC-20261017-019 findings

| Finding | Status | Resolution |
|---------|--------|------------|
| F1 — fair-comparison constraint defect | **Resolve** | §4.3: `w_max` applied uniformly to every method, incl. B1/B2. |
| F2 — baseline-set mismatch / scope signal | **Resolve** | §4.2: freeze B1–B5; implement B2, B4; demote `inverse_vol` to extension. |
| F3 — parameter drift | **Resolve** | Values reconciled in §0/§2/§3 of this sheet. |
| F4 — confounded MVO variants | **Resolve** | MVP comparison varies one dimension at a time; `unconstrained_sample_mvo` becomes a diagnostic-only (exploratory) variant. |
| F5 — documentation integrity | **Partly closed** | (a)–(c) repaired 2026-10-17; (d) `docs/README.md` false `model_and_method_spec.md` reference resolved with the method-spec work item. |
| F6 — Tests B/C/D undefined | **Resolve** | Defined in `tests_BCD_spec_2026-10-17.md` (DEC-20261017-020). |
| F7 — metric-implementation gap | **Defer to method spec** | CVaR, DSR, PSR, skew/kurtosis, autocorrelation, block-bootstrap CIs implemented before Gate 3. |
| F8 — PIT and snapshot gap | **Resolve** | §5.4.1 two-tier source contract + §5.4.9 snapshots. |

---

## 10. New findings surfaced while building this worksheet

These are **new** and are logged in DEC-20261017-020.

1. **Gate 0 is not met as written.** §8.4 requires R1 to document "a scan of ≥10 relevant open-source tools, papers, or repositories." The Phase 0 scan (`problem_framing.md` §4.1) names 4 (`cvxportfolio`, `PyPortfolioOpt`, `Riskfolio-Lib`, `skfolio`). Either extend the scan to ≥10 or amend the criterion. **Recommendation: extend the scan** — it is cheap and the criterion is a genuine defense against a false gap claim (K3, R-S03).
2. **H1.1 is unreachable under an enforced cap.** With a uniform `w_max = 0.30`, no method's max weight can exceed 0.40, so "max abs weight > 0.40 in ≥1 fold" cannot be satisfied by the capped models. H1.1 must be redefined to test the **uncapped** optimizer (§6 above). Without this, the framing's primary premise check fails for a definitional reason, not an empirical one.
3. **The fixed universe is survivorship-biased.** `data.py`'s 15 tickers are all alive *today*, which is precisely R-D02's detection trigger ("universe membership matches today's live tickers exactly"). §5.4.7 requires a point-in-time candidate list. All 15 incepted before 2007, so no delisting is exercised — meaning the contract's delisting rules are untested and the universe carries an unquantified upward bias. **Recommendation:** either reconstruct a PIT candidate list, or explicitly downgrade every affected claim to "universe-conditional" and record the limitation in §5.4.7.

---

## 11. Freeze-session order of operations

Fix the order; the DSR firewall from `freeze_inputs` §5 still applies.

1. Confirm or replace each value in §0.
2. Write the confirmed values into `evaluation_protocol.md`; bump to v2.3; set Status `Frozen`; add the revision row.
3. Update `docs/README.md` (protocol status) and `risk_register_and_premortem.md` (activate, bump to v1.2) and `scope_and_non_goals.md` (activate, bump to v1.3) as the owner's sign-off checklists allow.
4. **Only then** compute DSR/PSR values (never before §12.1's N is fixed).
5. **Only then** register Tests B/C/D and run them.

---

## 12. What this file does not authorize

- No new methods. No new experiments. No new data sources.
- No changes to `src/` or `scripts/` (DEC-20261015-015 remains in force).
- No edits to `evaluation_protocol.md` before the freeze session.
- No DSR calculations before §12.1 is fixed.
- No registry entries.

This file is input. The freeze is judgment. The two are separate sessions.

---

## 13. Freeze-session outcome (2026-10-17)

**All recommendations in §0 were accepted by the owner on 2026-10-17** and written into `evaluation_protocol.md` v2.3 (`Frozen`) under DEC-20261017-021. This worksheet is now a confirmed record of the decisions and their rationale; it remains a working input, not a contract.

Confirmed values, as frozen:

| Item | Frozen value |
|------|--------------|
| Estimation window | 60 months, rolling, re-estimated monthly |
| Test window / step | 12 / 12 months |
| §5.3 purged CV | scoped to hyperparameter selection only; embargo 1 month; inert if nothing is tuned |
| §6.1 | DSR p < 0.05 (`SR* = SR_0`); PSR > 0.95 (`SR* = SR_best_baseline`) |
| §6.2 / §6.3 | ΔSharpe ≥ 0.20; turnover ≤ 2×; MDD within +5pp / ≥3 cost levels; ≥60% of folds; no fold > 40% |
| §7 H1.1 | 0.40, tested on the **uncapped** optimizer |
| §7 H1.2 | turnover ratio > 2.0 |
| §4.2 | baseline set B1–B5; `inverse_vol` and other extensions not promoted |
| §4.3 | `w_max = 0.30`, uniform across all methods; γ = 10 (scale-verified; balance point ≈ 12.3) |
| §4.4 B2 | CCD risk budgeting; ε = 1e-6 |
| §4.4 B5 | λ = κ = 0.001; convex QP with auxiliary variables |
| §5.4.1 | two-tier: raw unadjusted + corporate actions + snapshots |
| §5.4.2 | point-in-time candidate list (target 15–25); 60-month history; $5M ADV |
| §5.4.5 | delisting −100% default, flagged untested; PIT list required |
| §5.4.6 | forward-fill ≤3 days; missing rf forward-fill ≤1 month then FRED; never zero |
| §5.4.9 | content-addressed cache; confirmatory runs read snapshots |
| §5.5.1 / §5.5.3 | impact term off; κ = 10 bps baseline (0/5/10/20/50) |
| §5.5.4 | signals through close t−1; execute close t−1; hold month t |
| §5.5.5 | single R_f for gross and net Sharpe |
| §5.5.6 | λ = κ; tuned λ is an extension |
| §8.3 / §8.4 | time-boxes confirmed; Gate 0 requires the ≥10-item R1 scan and the protocol Frozen |
| §8.6 K7 | 3 invalidations |
| §12.8 | q = 0.10 (convention) |
| §13.1 | block 6; 2000 replications |
| §14.3 | 1-week decision time-box |

**Verification performed at the freeze.** The γ scale check was run read-only on the Phase 1 monthly-returns cache (232 months, 15 assets): equal-weight monthly return 0.00445, monthly variance 0.000721, so the term-balance point is γ ≈ 12.3 and γ = 10 gives a return:risk ratio of ≈ 1.23:1. The check also gave the sample-covariance condition number (10,803), which independently supports the 60-month window over 36.

**No `src/` or `scripts/` file was modified.** DEC-20261015-015's pre-freeze source freeze remained in force throughout.

---

**End of freeze worksheet.**
