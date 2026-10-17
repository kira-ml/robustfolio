# Risk Register and Pre-Mortem: robustfolio

**Version:** 1.4
**Status:** Active — owner-activated 2026-10-17 (DEC-20261017-021)
**Owner:** Ken Ira Lacson Talingting
**Created:** 2026-10-14
**Last Updated:** 2026-10-17
**Supersedes:** 1.3 (PIT universe resolution + snapshot/leakage findings)
**Related:** [`problem_framing.md`](problem_framing.md), [`evaluation_protocol.md`](evaluation_protocol.md), [`decision_log.md`](decision_log.md), [`scope_and_non_goals.md`](scope_and_non_goals.md)

---

## 0. Purpose of This Document

This document:

1. Enumerates the failure modes that could cause `robustfolio` to fail its mission.
2. Rates each risk by likelihood, impact, and detectability.
3. Specifies mitigations, detection signals, and triggers.
4. Runs a **pre-mortem**: assumes the project has failed, and works backward to find the causes.
5. Establishes a review cadence so the register stays current.

It is a **living document**. Unlike the frozen contracts, this register is updated whenever a new risk is discovered, a mitigation proves ineffective, or a risk materializes.

**Its primary enemy is not failure. It is silent failure** — the project continuing as if nothing is wrong while its foundations are eroding.

---

## 1. Philosophy

Three principles govern this register.

1. **Inversion first.** The most useful question is not "how do we succeed?" but "how would we fail?" Every risk entry starts from that question.
2. **Rank by detectability, not only severity.** A high-impact risk that is easy to detect is less dangerous than a moderate-impact risk that is invisible.
3. **Every risk has a trigger and an owner.** A risk without a trigger is a worry. A worry without an owner is drift.

The register is the operational arm of [Inversion]. Its contents feed directly into [`evaluation_protocol.md`](evaluation_protocol.md) §§7–8 and [`decision_log.md`](decision_log.md).

---

## 2. Risk Scoring

> **Confirmed at activation (2026-10-17).** Ratings are fixed until the first phase-gate review, which may re-rate them.

### 2.1 Likelihood

| Score | Label | Meaning |
|-------|-------|---------|
| 1 | Rare | < 5% chance over project lifetime |
| 2 | Unlikely | 5–20% |
| 3 | Possible | 20–50% |
| 4 | Likely | 50–80% |
| 5 | Almost certain | > 80% |

### 2.2 Impact

| Score | Label | Meaning |
|-------|-------|---------|
| 1 | Negligible | Cosmetic; no effect on conclusions |
| 2 | Minor | Weakens one finding; correctable |
| 3 | Moderate | Weakens a family of findings; requires rework |
| 4 | Major | Invalidates a phase; forces pivot |
| 5 | Severe | Kills the project or corrupts all results |

### 2.3 Detectability

| Score | Label | Meaning |
|-------|-------|---------|
| 1 | Obvious | Failure is immediately visible |
| 2 | Easy | Detected by routine checks |
| 3 | Moderate | Detected by deliberate review |
| 4 | Hard | Detected only by targeted tests |
| 5 | Invisible | Detected only after external review or too late |

### 2.4 Risk priority number (RPN)

\[
\text{RPN} = \text{Likelihood} \times \text{Impact} \times \text{Detectability}
\]

Range: 1–125. Interpretation:

- **≥ 60**: Critical. Must have an active mitigation and a monitoring trigger.
- **30–59**: High. Requires a mitigation and phase-gate review.
- **10–29**: Moderate. Monitored; mitigation if it escalates.
- **< 10**: Low. Documented; no active work.

---

## 3. Risk Categories

Risks are grouped by which part of the project they attack. This aids targeted review.

| Code | Category | Scope |
|------|----------|-------|
| **R-M** | Methodological | Overfitting, multiple testing, p-hacking, denominator suppression |
| **R-D** | Data | Leakage, survivorship, adjusted-price lookahead, source failure |
| **R-C** | Cost | Cost model errors, drift-weight bugs, unrealistic assumptions |
| **R-E** | Execution | Code bugs, environment drift, unreproducible results |
| **R-P** | Process | Goalpost-moving, sunk cost, scope creep, documentation erosion |
| **R-S** | Strategic | Weak problem, weak baselines, false gap claim, no improvement |
| **R-H** | Human | Motivation, isolation, time budget, distraction, burnout |
| **R-X** | External | Data source TOS changes, API deprecation, compute loss |

---

## 4. Risk Register

> Ratings confirmed at activation (2026-10-17).

| ID | Risk | Cat | L | I | D | RPN | Mitigation | Detection Trigger |
|----|------|-----|---|---|---|-----|-----------|-------------------|
| **R-M01** | Multiple testing inflates significance | M | 4 | 5 | 4 | **80** | Deflated Sharpe; pre-registration; family-size denominator frozen at Phase 3 | Any result relying on unadjusted p-value; denominator not reported |
| **R-M02** | Silent p-hacking via unregistered trials | M | 3 | 5 | 5 | **75** | Append-only registry; exploratory labeling; disclosure rule | Any metric reported without a registry entry |
| **R-M03** | Denominator suppression | M | 2 | 5 | 4 | 40 | Registry review at gate; git audit trail | Trial count in registry < number of metric-bearing runs |
| **R-M04** | Overfitting to walk-forward folds | M | 3 | 4 | 3 | 36 | Purged CV; embargo; hold-out test period | In-sample ≈ OOS performance with no plausible cause |
| **R-M05** | Metric definition drifts after results | M | 2 | 4 | 3 | 24 | Frozen protocol; decision log for any change | Any change to `evaluation_protocol.md` after Phase 1 begins |
| **R-D01** | Adjusted-price lookahead | D | 4 | 5 | 5 | **100** | Raw + corporate actions reconstruction; leakage test | Adjusted prices used without reconstruction; failing leakage test |
| **R-D02** | Survivorship bias in universe | D | 4 | 5 | 4 | **80** | Point-in-time membership reconstruction; delisted assets retained | Candidate universe matches today's live tickers exactly |
| **R-D03** | Data source API/format change | D | 4 | 3 | 2 | 24 | Snapshot immutability; adapter isolation | Ingestion failure; schema mismatch on re-fetch |
| **R-D04** | Missing data silently imputed | D | 3 | 4 | 4 | 48 | Quality report per snapshot; imputation flag; bounded forward-fill | Quality report missing; imputed values unlabeled |
| **R-D05** | Risk-free rate convention mismatch | D | 2 | 2 | 3 | 12 | Documented convention; consistency test | Sharpe reported with different rf across methods |
| **R-D06** | Universe eligibility drift (the investable set changes over the sample) | D | 4 | 2 | 3 | 24 | Eligibility rule frozen (protocol §5.4.2); the per-month eligible count is reported with every run | Results quoted for a universe size that does not match the month it came from |
| **R-C01** | Drifted-weight bug (turnover understated) | C | 4 | 5 | 4 | **80** | Unit test for drifted weights; cross-check with naive turnover | Turnover near zero; turnover drops after refactor |
| **R-C02** | Cost model misaligned with penalty λ | C | 3 | 4 | 3 | 36 | λ = κ alignment test; documented in method spec | Penalized method's turnover not responsive to κ |
| **R-C03** | One-way vs two-way turnover confusion | C | 3 | 3 | 2 | 18 | Convention documented; label in every report | Turnover numbers inconsistent across documents |
| **R-C04** | Cost applied to target, not drifted weights | C | 3 | 4 | 4 | 48 | Reuse drifted-weight function; integration test | Costs lower than manual check |
| **R-E01** | Code bug in optimizer or solver | E | 4 | 4 | 3 | 48 | Unit tests per method; solver convergence checks; sanity fixtures | Convergence failures; weights violating constraints |
| **R-E02** | Environment drift (non-reproducible) | E | 3 | 4 | 3 | 36 | Lockfile; pinned versions; snapshot + commit hash per run | Re-run produces different numbers |
| **R-E03** | Random seed not controlled | E | 2 | 3 | 2 | 12 | Seeds in registry; determinism test | Results vary between identical runs |
| **R-E04** | Silent numeric instability | E | 3 | 3 | 4 | 36 | Condition number checks; diagonal loading documented | Large weight changes from tiny input changes |
| **R-P01** | Goalpost-moving after results | P | 3 | 5 | 4 | **60** | Frozen protocol; decision log; version bump rule | Any threshold change after Phase 3 begins |
| **R-P02** | Sunk-cost continuation past kill trigger | P | 4 | 4 | 3 | 48 | Sunk-cost firewall ([`evaluation_protocol.md`](evaluation_protocol.md) §9); time-box enforcement | "Just one more thing" after failed gate |
| **R-P03** | Scope creep (new asset class, method, or frequency) | P | 4 | 3 | 2 | 24 | [`scope_and_non_goals.md`](scope_and_non_goals.md) §5; amendment required | New method appearing without a registry entry |
| **R-P04** | Documentation erosion | P | 4 | 3 | 3 | 36 | Phase-gate review; status board updates | Status board out of date; `[FILL]` remains after activation |
| **R-P05** | Kill without decision log | P | 3 | 2 | 2 | 12 | Hard Rule 4 in [`evaluation_protocol.md`](evaluation_protocol.md) §8.1 | Owner stops work without a log entry |
| **R-S01** | No improvement over baselines | S | 3 | 4 | 2 | 24 | Falsification K1; stop-and-report path | Phase 3 results show no method meeting success criteria |
| **R-S02** | Baselines too weak (fake wins) | S | 3 | 5 | 3 | 45 | [`evaluation_protocol.md`](evaluation_protocol.md) §4; B5 as strong baseline | Robust method beats B3 but loses to B1 or B5 |
| **R-S03** | Gap claim false (existing tool covers it) | S | 3 | 4 | 3 | 36 | R1 tool scan; kill trigger K3 | Tool scan reveals equivalent benchmark |
| **R-S04** | Problem framing falsified in Phase 1 | S | 2 | 4 | 2 | 16 | Falsification H1.1, H1.2; pivot path | Sample MVO not extreme or high-turnover on primary dataset |
| **R-S05** | Report-only-positive-results pressure | S | 2 | 4 | 3 | 24 | [`problem_framing.md`](problem_framing.md) §13; "negative result is success" language | Wording in reporting that downplays negative findings |
| **R-H01** | Time budget exhausted before completion | H | 4 | 3 | 2 | 24 | Phase time-boxes; [`evaluation_protocol.md`](evaluation_protocol.md) §8.3 | Any phase exceeding time-box |
| **R-H02** | Motivation loss / abandonment | H | 3 | 4 | 4 | 48 | Phase gates; small deliverables; decision log | No commits for > 3 weeks |
| **R-H03** | Solo researcher blind spots | H | 4 | 3 | 4 | 48 | Reasoning partner escalation; optional external review | Owner cannot articulate why a decision was made |
| **R-H04** | Distraction by new project ideas | H | 4 | 3 | 3 | 36 | Scope discipline; decision log for any new idea | New "urgent" ideas after each gate |
| **R-X01** | Data source TOS change | X | 3 | 3 | 2 | 18 | Adapter isolation; alternate sources documented | Ingestion failure; legal notice |
| **R-X02** | Compute environment loss | X | 2 | 3 | 2 | 12 | Snapshots and lockfile stored externally | Machine failure; disk corruption |

**Critical (RPN ≥ 60):** R-M01, R-M02, R-D01, R-D02, R-C01, R-P01.
These are the risks that, if unaddressed, will most likely produce a false result or an abandoned project.

---

## 5. Pre-Mortem

The pre-mortem assumes the project has already failed. It works backward to identify causes. This is a narrative complement to the tabular register.

### 5.1 Scenario A — The project "succeeded" but was wrong

**Assumed outcome:** The project reports a robust method beating baselines net of costs. Six months later, an external reviewer finds the result is an artifact.

**Backward causes:**

1. The adjusted-price reconstruction was incomplete; future corporate actions leaked into estimation.
2. Multiple-testing adjustment used a denominator that excluded exploratory trials.
3. The best baseline (B5) was implemented with a bug that inflated its turnover, making the robust method look better.
4. Walk-forward folds were not purged, allowing training and test overlap.
5. Reporting emphasized net Sharpe at 10 bps while hiding the break-even cost.

**Primary defenses:**

- R-D01: raw + corporate actions reconstruction, leakage test.
- R-M02: exploratory labeling and denominator honesty.
- R-C01, R-E01: drifted-weight unit test and baseline sanity fixtures.
- R-M01: purged CV and embargo.
- R-P01: frozen protocol; full reporting requirements.

**Probability this scenario unfolds if defenses fail:** High. This is the most dangerous failure mode because it looks like success.

---

### 5.2 Scenario B — The project "failed" but was actually inconclusive

**Assumed outcome:** The project stops with no method beating baselines. The negative result is reported, but the framework is discarded as a failure.

**Backward causes:**

1. The gap claim was never fully validated (R-S03), so the "negative result" answers a question no one was asking.
2. Baselines were too weak in Phase 1, so Phase 3 could not detect a real effect (R-S02).
3. Time budget exhausted during Phase 2, leaving Phase 3 truncated (R-H01).
4. Code bugs made the robust methods underperform for reasons unrelated to their merit (R-E01).

**Primary defenses:**

- R1 literature/tool scan in Phase 0 ([`evaluation_protocol.md`](evaluation_protocol.md) §8.4 gate).
- Strong baseline set (B5) in [`evaluation_protocol.md`](evaluation_protocol.md) §4.
- Phase time-box enforcement ([`evaluation_protocol.md`](evaluation_protocol.md) §8.3).
- Unit tests per method before Phase 3.

**Interpretation:** A negative result that is caused by broken tooling is not a negative result. It is an untested question.

---

### 5.3 Scenario C — The project is abandoned mid-flight

**Assumed outcome:** Work stops after Phase 2. No conclusion is drawn. Documents exist but no results.

**Backward causes:**

1. Motivation faded after a gate failed (R-H02).
2. A new project idea displaced this one (R-H04).
3. Time budget was never enforced, so the project drifted (R-H01, R-P04).
4. No decision log entry recorded the stop, so the project cannot be cleanly restarted or concluded (R-P05).

**Primary defenses:**

- Small, phase-gated deliverables.
- Time-box enforcement with decision log entry required at any stop.
- Kill and stop-and-report explicitly framed as valid outcomes in [`problem_framing.md`](problem_framing.md) §13.
- Biweekly or monthly review cadence.

**Interpretation:** Abandonment is not the same as killing the project. Abandonment is silence. Killing is a decision. Only one of these is a learning outcome.

---

### 5.4 Scenario D — The project produces misleading claims

**Assumed outcome:** The project publishes a report or blog post claiming robust methods work, based on incomplete analysis. Claims are later retracted.

**Backward causes:**

1. Forbidden claims ([`evaluation_protocol.md`](evaluation_protocol.md) §14.2) were made anyway.
2. Confidence intervals were not reported.
3. Cost sensitivity was reported only at 10 bps, hiding non-robustness.
4. Exploratory results were presented as confirmatory (R-M02).
5. Sunk-cost pressure produced "positive framing" of a marginal result (R-S05, R-P02).

**Primary defenses:**

- `results_reporting_and_claims_policy.md` (Tier 2) — must be written before Phase 4.
- Frozen reporting template.
- External review (if available) before release.
- Reasoning-partner escalation rule ([`evaluation_protocol.md`](evaluation_protocol.md) §8.2).

**Interpretation:** Misleading claims destroy the project's credibility and are worse than an honest negative result. The protocol and this register exist primarily to prevent this scenario.

---

## 6. Critical Risks — Detail

The six critical risks warrant specific attention.

### R-M01 — Multiple testing inflates significance (RPN 80)

**Why it matters:** Portfolio research routinely produces "significant" results because many methods, parameters, or metrics are tried. Without denominator discipline, the deflated Sharpe is cosmetic.

**Active mitigation:**

- Freeze the H2 and H3 family denominator at start of Phase 3.
- Report family size \( N \) on every result.
- Require deflated Sharpe p-value for every success claim.

**Trigger to escalate:** Any result reporting net Sharpe improvement without deflated Sharpe.

---

### R-M02 — Silent p-hacking (RPN 75)

**Why it matters:** The most common way research self-deceives is by running unregistered variants and reporting only the ones that worked.

**Active mitigation:**

- Append-only registry ([`decision_log.md`](decision_log.md) Appendix A).
- Exploratory labeling mandatory.
- Disclosure of exploratory work in every report.

**Trigger to escalate:** Any metric bearing on a success claim that lacks a registry entry.

---

### R-D01 — Adjusted-price lookahead (RPN 100)

**Why it matters:** Free data sources retroactively adjust prices. Using them naively is the most common and most invisible form of lookahead in retail backtesting.

**Active mitigation:**

- Reconstruct point-in-time adjusted prices from raw prices + corporate actions with ex-date ≤ \( t \).
- Run the adjusted-price leakage test before every experiment.
- If reconstruction is not feasible, downgrade affected claims to exploratory and document the limitation in [`evaluation_protocol.md`](evaluation_protocol.md) §5.4.4.

**Trigger to escalate:** Use of `auto_adjust=True` or equivalent without documentation.

---

### R-D02 — Survivorship bias (RPN 80)

**Why it matters:** Using today's live tickers as the universe excludes delisted assets and inflates historical performance.

**Active mitigation:**

- Point-in-time membership reconstruction.
- Retain delisted assets through their delisting date.
- Include delisting returns.

**Trigger to escalate:** Universe membership matches today's live tickers exactly at every rebalance.

---

### R-C01 — Drifted-weight bug (RPN 80)

**Why it matters:** If pre-rebalance weights are computed incorrectly, turnover and costs are understated. This silently inflates net Sharpe for high-turnover methods.

**Active mitigation:**

- Unit test for drifted weights (see [`evaluation_protocol.md`](evaluation_protocol.md) §5.5.5).
- Cross-check computed turnover against a naive sum of weight changes.
- Report turnover at every cost level.

**Trigger to escalate:** Turnover near zero, or turnover drops suddenly after a refactor.

---

### R-P01 — Goalpost-moving (RPN 60)

**Why it matters:** The most tempting response to a failed experiment is to adjust the threshold, metric, or test. This invalidates the entire methodological foundation.

**Active mitigation:**

- Frozen protocol; decision log required for any change.
- Version bump for any amendment.
- External-review defense required for post-result changes.

**Trigger to escalate:** Any change to `evaluation_protocol.md` after Phase 1 begins without a decision log entry.

---

## 7. Monitoring and Review

### 7.1 Cadence

| Cadence | Activity | Output |
|---------|----------|--------|
| Before each experiment | Confirm no active risk is elevated | Registry entry notes any relevant risk |
| After each experiment | Update risk register if new failure modes observed | Register row added or amended |
| At each phase gate | Full review of critical risks; re-rate | Updated register; decision log entry |
| Monthly | Skim register for drift | If nothing changed, no entry needed |
| On trigger firing | Immediate review; escalate to decision | Decision log entry; possible kill/pivot |

### 7.2 Phase-gate review checklist

Before any gate is passed:

- [ ] All critical risks (RPN ≥ 60) have active mitigations in place.
- [ ] No critical risk has had its trigger fire without a decision log entry.
- [ ] Register reflects any new risks discovered during the phase.
- [ ] Any risk materialized in this phase is documented and its impact assessed.

### 7.3 Escalation

If the reasoning partner (LLM) identifies a risk whose trigger has fired or whose mitigation is missing, it must flag it. The owner decides. Silence is not consent ([`evaluation_protocol.md`](evaluation_protocol.md) §8.2).

---

## 8. Risk Materialization Log

When a risk materializes, add an entry here. This is a narrative complement to the decision log.

| Date | Risk ID | Description | Impact | Response | Decision log entry |
|------|---------|-------------|--------|----------|--------------------|
| 2026-10-17 | R-D01 | Phase 1 ingested retroactively adjusted prices (`auto_adjust=True`) with no immutable snapshot; the §5.4.4 reconstruction and §5.4.9 snapshot rules were unsatisfied. | Phase 1 is exploratory only; no confirmatory claim depends on it. | Froze the two-tier raw + corporate-actions + snapshot contract (§5.4.1, §5.4.9). | DEC-20261017-019 (F8), DEC-20261017-021 |
| 2026-10-17 | R-D02 | The Phase 1 universe was the 15 tickers live today — the escalation trigger fired. | Unquantified upward survival bias; the delisting rules were never exercised. | Froze a required point-in-time candidate list (§5.4.7); building it is a Gate-1 task and results stay universe-conditional until it exists. | DEC-20261017-020 (N3), DEC-20261017-021 |
| 2026-10-17 | R-D02 | The point-in-time candidate list was reconstructed and confirmed — 18 instruments anchored at the backtest start 2012-06, inception cut-off 2007-05-31 (`notes/pit_universe_2026-10-17.md` v1.0). No in-scope, large, liquid, non-leveraged ETF available at 2007-06 liquidated 2012–2026, so the §5.4.8.2 survivorship test is vacuous in-sample. | The upward survival bias is now bounded and documented, but remains **argued, not measured**; results stay universe-conditional (§5.4.7). | Confirmed the list and accepted the residual; held the §5.4.7 downgrade clause in reserve; declined the archived-PIT-screen upgrade (paid source). | DEC-20261017-024 |
| 2026-10-17 | R-D01 | The first PIT reader read **raw** closes when building month-end prices, bypassing the split-adjusted reconstruction (finding caught by the new §5.4.8 suite; at the synthetic 2018 split it produced a spurious −49 % month). A genuine `DGS1MO` 0.00 (2015) was also briefly conflated with a forbidden zero-substitution. | None — both were caught by the leakage suite **before any result was computed**. They are recorded because the suite's value is demonstrated, not asserted. | Fixed both; the suite now asserts split-adjusted month-end prices and that any zero rf traces to a vendor zero. | DEC-20261017-025 |
| 2026-10-17 | R-D05 | Two risk-free conventions proved to be **unpinned by the frozen documents**: the annual-to-monthly conversion (§3.4) and which month's observation prices a given month's return (§5.4.3 vs §5.5.5). Both sit inside every net Sharpe ratio. | Low numerically (~0.009 pp/month on conversion; a one-month alignment shift), but each is a frozen-value gap that would otherwise be set silently. | Recorded as findings **F10** and **F11**; defaulted to `geometric` and `prior_month`, stamped into every snapshot manifest, and surfaced to the owner for confirmation. | DEC-20261017-025 |
| 2026-10-17 | R-D06 | Materialized: the §5.4.2 `ADV > $5M` floor binds on `RWX`, whose 3-month dollar volume falls from $15–28 M (2012–2020) to $0.99 M (2026). The eligible set is 18 for 2012-06…2021-11 and 17 thereafter (48 of 172 OOS months). | Bounded: one name of eighteen. The rule is working as written; the consequence is a time-varying investable set and a real, costed divestment. | Recorded as finding **F12** with the per-period table; the run must report the eligible count per month. No rule change. | DEC-20261017-025 |

**Rule:** A materialized risk always produces a decision log entry, even if the decision is "continue unchanged." This preserves the learning loop.

---

## 9. Model Tags Applied

- **[Inversion]** — Every risk starts from "how would we fail?"; pre-mortem sections make the inverted reasoning explicit.
- **[Systems]** — Risk categories, monitoring cadence, escalation rules, phase-gate review.
- **[Bayesian]** — Likelihood and impact ratings are probabilistic; register updates as evidence accumulates.
- **[Expected Value]** — RPN prioritizes by combined probability, impact, and detectability.
- **[Experimental]** — Every risk has a detection trigger and a mitigation; no risk is left purely diagnostic.
- **[Learning Loop]** — Materialization log; register updates after each experiment.
- **[Information Theory]** — Compressed to categories, ratings, mitigations, triggers; no filler.

---

## 10. Owner Action Checklist Before Activating

Before setting Status to `Active`:

- [x] Confirm or adjust likelihood ratings in §4 based on your actual discipline, tooling, and time.
- [x] Confirm or adjust impact ratings in §4.
- [x] Confirm the critical-risk set in §6 is complete. If any risk feels missing, add it.
- [x] Confirm the monitoring cadence in §7.1 matches your available time.
- [x] Confirm the phase-gate review checklist in §7.2 will actually be run.
- [x] Add a `[FILL]`-free version of the register to the repo before Phase 1 begins.

Also confirm:

- [x] You accept that the register is a living document, not a frozen one.
- [x] You accept that materialized risks always produce a decision log entry.
- [x] You accept that the reasoning partner may escalate any firing trigger.

**Activated 2026-10-17.** Version 1.2; Status `Active`.

---

## 11. Revision History

| Date | Version | Change | Author |
|------|---------|--------|--------|
| 2026-10-14 | 1.0 | Initial risk register and pre-mortem | Ken Ira Lacson Talingting |
| 2026-10-15 | 1.1 | Updated cross-references to retired documents per DEC-20261015-018: `project_charter.md`, `data_contract_and_point_in_time_policy.md`, `cost_model_and_frictions.md`, `benchmark_and_baseline_spec.md`, `success_metrics_and_evaluation_protocol.md`, and `experiment_registry_and_preregistration.md` redirected to `evaluation_protocol.md` sections. Header `Related` list trimmed to retained files. §1, §5.2, §5.4, §7.3 references updated. No risk content changed. | Ken Ira Lacson Talingting |
| 2026-10-17 | 1.2 | **Activated** at the protocol freeze (DEC-20261017-021). §2 and §4 rating notes de-proposed. §8 Risk Materialization Log opened with entries for R-D01 (adjusted-price ingestion, F8) and R-D02 (survivorship universe, N3). §10 activation checklist completed. Status `Draft` → `Active`. | Ken Ira Lacson Talingting |
| 2026-10-17 | 1.3 | §8: added the R-D02 resolution entry — the point-in-time candidate universe is confirmed (18 instruments, anchor 2012-06) and the residual survival bias accepted as documented (DEC-20261017-024). No rating changed. | Ken Ira Lacson Talingting |
| 2026-10-17 | 1.4 | Added **R-D06** (universe eligibility drift, RPN 24) to §4. §8: three entries from the first snapshot build and the §5.4.8 leakage suite — R-D01 (raw-vs-split-adjusted month-end prices; caught before any result), R-D05 (F10/F11: two unpinned risk-free conventions), R-D06 (F12: the §5.4.2 liquidity floor binds on `RWX`, so the eligible set is 18 → 17 after 2021-11). No existing rating changed; the RPN ≥ 60 critical list is unchanged. | Ken Ira Lacson Talingting |

---

*This register exists to make failure visible before it happens. A project that tracks its risks carefully is more likely to produce an honest result, positive or negative.*
