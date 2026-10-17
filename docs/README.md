# robustfolio Documentation Index

**Version:** 1.11
**Status:** Active
**Last Updated:** 2026-10-17

This folder contains the foundational contracts, protocols, and decision records for the `robustfolio` project.
The purpose of this documentation is to **prevent predictable failure modes** before writing code: unclear objectives, data leakage, overfitting, unrealistic cost assumptions, scope creep, and unfalsifiable claims.

Read this file first. It is the map and status board for all project documentation.

---

## Documentation Principles

1. **One decision per document.** If a document answers multiple unrelated decisions, split it.
2. **Status is explicit.** Every document must declare: `draft`, `active`, `frozen`, or `retired`.
3. **Freeze before experiments.** Evaluation protocols, data contracts, cost models, and kill criteria must be `frozen` before running any experiment that tests a hypothesis.
4. **No duplication.** If a topic is covered elsewhere, link to it instead of repeating.
5. **Update the log.** Every major change to a frozen document requires a decision log entry.

---

## Status Board

The active documentation set is seven files. All other Tier 0 documents have been merged into these per DEC-20261015-017 and DEC-20261015-018.

| # | Document | Version | Status | Purpose | Last Updated |
|---|----------|---------|--------|---------|--------------|
| 1 | [`README.md`](README.md) | 1.11 | Active | Index and status board | 2026-10-17 |
| 2 | [`problem_framing.md`](problem_framing.md) | 2.4 | Foundational | Problem statement, stakeholders, causal model, references | 2026-10-17 |
| 3 | [`scope_and_non_goals.md`](scope_and_non_goals.md) | 1.4 | **Active** | Authoritative scope: MVP, extensions, out-of-scope | 2026-10-17 |
| 4 | [`evaluation_protocol.md`](evaluation_protocol.md) | 2.4 | **Frozen** | Metrics, protocol, thresholds, hypotheses, triggers, firewalls, governance, baselines, data contract, cost model, registry rules | 2026-10-17 |
| 5 | [`model_and_method_spec.md`](model_and_method_spec.md) | 1.1 | **Frozen** | Exact method, estimator, optimizer, harness, and metric definitions (absorbs F7) | 2026-10-17 |
| 6 | [`decision_log.md`](decision_log.md) | 1.5 | Active | Immutable record of governance, experiment, and pivot decisions; includes the experiment registry ledger (Appendix A) | 2026-10-17 |
| 7 | [`risk_register_and_premortem.md`](risk_register_and_premortem.md) | 1.4 | **Active** | Failure modes, ratings, mitigations, triggers, pre-mortem scenarios | 2026-10-17 |

**Working inputs (not Tier 0 documents):** the freeze worksheet [`../notes/freeze_worksheet_2026-10-17.md`](../notes/freeze_worksheet_2026-10-17.md) (the decisions behind protocol v2.3, with rationale and sources); the Tests B/C/D specification [`../notes/tests_BCD_spec_2026-10-17.md`](../notes/tests_BCD_spec_2026-10-17.md); the freeze inputs [`../notes/freeze_inputs_2026-10-15.md`](../notes/freeze_inputs_2026-10-15.md); the Phase 1 DSR inputs [`../notes/dsr_inputs_phase1.json`](../notes/dsr_inputs_phase1.json); the confirmed point-in-time candidate universe [`../notes/pit_universe_2026-10-17.md`](../notes/pit_universe_2026-10-17.md) v1.0 (18 ETFs, anchor 2012-06 — DEC-20261017-024) with its machine-readable list [`../notes/pit_candidates_2026-10-17.csv`](../notes/pit_candidates_2026-10-17.csv); the snapshot and leakage-suite evidence record [`../notes/snapshot_and_leakage_evidence_2026-10-17.md`](../notes/snapshot_and_leakage_evidence_2026-10-17.md) v1.0 (snapshot `…-2ad06139`, §5.4.8 suite pass — DEC-20261017-025); the design diagnostics [`../notes/power_and_effective_bets_2026-10-17.md`](../notes/power_and_effective_bets_2026-10-17.md) v1.1 (effective bets of the universe, power of the registered tests, finding F15 — DEC-20261017-028).

**Gate 1 status (2026-10-17).** Both data blockers are closed: the point-in-time candidate universe is confirmed (DEC-20261017-024) and the §5.4.8 leakage suite passes against an immutable snapshot (DEC-20261017-025: 14 passed, 1 skipped as vacuous in-sample). The risk-free conventions (**F10**, **F11**) are owner-confirmed (`geometric` conversion, prior-month alignment) and stamped into every snapshot manifest (DEC-20261017-026).

**Experiment registry status (2026-10-17).** Appendix A of [`decision_log.md`](decision_log.md) holds all three pre-registrations, none executed:

| ID | Test | Family | Counting | Configuration |
|----|------|--------|----------|---------------|
| `EXP-X-20261017-001` | B | X (exploratory) | no | cap sweep `w_max ∈ {0.20, 0.30, 0.40, 1.00}`, uniform |
| `EXP-X-20261017-002` | C | X (exploratory) | no | window sweep `{36, 60}`, both at 2012-06…2026-05 |
| `EXP-H2-20261017-001` | D | H2 / H3 (confirmatory) | **yes** | frozen config; **N = 1** at registration |

Two findings from the registration round are closed: **F13** (the DSR trial count for a multi-method registration) resolved as `N = 1`, owner-confirmed; **F14** (Test C's window sweep had no common evaluation period) resolved as `{36, 60}` at the frozen anchor, with the infeasible 120-month arm dropped — the universe did not exist before 2007. Both are recorded in DEC-20261017-026/027, and the B/C/D spec's §9 addendum carries the reduced-strength limitation of a two-point sweep.

**Design diagnostics status (2026-10-17).** [`../notes/power_and_effective_bets_2026-10-17.md`](../notes/power_and_effective_bets_2026-10-17.md) v1.1 and [`../scripts/diagnostics_power.py`](../scripts/diagnostics_power.py) measure two properties of the data and the test design, and are **not an experiment and not a registry entry** (protocol §12.2): no portfolio is formed and no strategy metric is reported, so nothing here counts toward the multiple-testing denominator or can be cited for or against H1–H3. The 18 candidates carry only **3–5 independent directions** (`N_part` 3.14 / `N_ent` 5.03; per-fold 2.45–3.91 / 4.13–5.71), and **12 of 18** sample eigenvalues fall below the Marchenko–Pastur lower edge (0.452) for an independent 18 × 168 panel — the smallest by 85× — so the H1 premise is **supported by the data rather than assumed**. The level test needs an annualised Sharpe of ≈ 0.67; the paired difference test detects the §6.2 threshold of 0.20 at ≥ 80% power once **ρ ≥ 0.98**. **F15** is resolved accordingly: ρ(candidate, best baseline) is reported in a design appendix, no registration is amended, and `N = 1` is unchanged. The earlier claim that the project is underpowered for a 0.2 Sharpe claim is **retracted**.

**Engine core status (2026-10-17).** The Phase 2 rewrite has begun with the estimator/optimizer core rather than the harness, because every defect in the project's history lived at that boundary: the SLSQP fallback, the expanding window inside the test period, and the fair-comparison defect where the cap applied to some methods and not others. `src/robustfolio/optimize.py` is now `cvxpy` + `CLARABEL` with **no fallback path** (§5.7): a non-accepted solve raises. Because CLARABEL exposes no duality gap, the §5.6 acceptance is enforced by a **KKT residual computed from the primal solution alone**, which is an equivalent certificate for a convex QP and independent of the solver. Three values the frozen documents cannot supply were raised and resolved by DEC-20261017-029: **F16** (sklearn's Ledoit-Wolf base uses `ddof=0` while §4.2 pins `ddof=1`, so M1 differs from B3 by shrinkage *and* a 1.7% scale factor — left as specified, quantified, not silently corrected); **F17** (§5.6 pins "solver defaults" *and* a 1e-7 residual; the defaults deliver 1.2e-4, so an explicit `SOLVER_TOL = 1e-14` is required, and tightening past it degrades the solver); **F18** (the initial `w⁻` is unpinned — the period starts flat at `w⁻ = 0`). A defect in the certificate itself is also recorded: the multipliers of the maximisation were first added rather than subtracted, which would have made the certificate accept whatever the solver returned. Evidence: `scripts/certify_engine.py` certifies **168 rebalances × 6 solver-backed methods = 1,008 solves with zero failures**, worst KKT residual `2.97e-11` (3,400× inside the acceptance threshold), `cond(Σ̂)` `1.30e4`–`6.09e5`. Risk parity's cap binds on **154 of 168** rebalances, so B2 is box-constrained by a convex homotopy rather than a cap on unnormalised weights. The walk-forward harness (`backtest.py`) is not yet rewritten.

**Retired 2026-10-15 (merged per DEC-20261015-017 and DEC-20261015-018):** `project_charter.md` (→ `evaluation_protocol.md` §8; mission → `problem_framing.md`; scope → `scope_and_non_goals.md`); `benchmark_and_baseline_spec.md` (→ §4); `data_contract_and_point_in_time_policy.md` (→ §5.4); `cost_model_and_frictions.md` (→ §5.5); `experiment_registry_and_preregistration.md` (rules → §12; ledger → `decision_log.md` Appendix A); `TODO.md` (→ `decision_log.md` Appendix B). Historical content preserved in git history.

**Status legend:**
- `Foundational` — the problem contract; changes require strong justification.
- `Draft` — written but not yet reviewed or confirmed.
- `Active` — current, may still change.
- `Frozen` — locked; changes require a decision log entry.
- `Retired` — content relocated; source file deleted.

---

## Not yet written

The following documents are referenced by other documents but do not exist yet.

1. `reproducibility_and_environment.md` — written when the Python environment is first set up.
2. `results_reporting_and_claims_policy.md` — written before Phase 4 (reporting).
3. `architecture_decision_records/` — created when the first irreversible technical decision is made.
4. `open_source_and_license_policy.md` — written before public release.

---

## How to Use This Documentation

- **Before coding:** Ensure `problem_framing.md`, `scope_and_non_goals.md`, and `evaluation_protocol.md` §8 are at least `Draft`.
- **Before running a backtest:** Confirm `evaluation_protocol.md` §5.4 (data contract) and §5.5 (cost model) are `Frozen`. Log the experiment in `decision_log.md` Appendix A before execution.
- **Before comparing methods:** Ensure `evaluation_protocol.md` §§4, 6, 7, and 12 are `Frozen`.
- **Before writing Phase 2 method code:** Ensure `model_and_method_spec.md` is `Frozen` (Gate 1 entry, protocol §8.4).
- **When making a technical decision:** Record it in `decision_log.md`. If irreversible and architectural, also record it in `architecture_decision_records/`.
- **When something fails or surprises:** Update `risk_register_and_premortem.md` and `decision_log.md`.

---

## Model Tags Used in This Project

- **[First Principles]** — Reduce to fundamentals.
- **[Bayesian]** — Update beliefs with evidence; track calibration.
- **[Experimental]** — Falsification, pre-registration, walk-forward.
- **[Systems]** — Feedback loops, delays, bottlenecks.
- **[Inversion]** — Pre-mortem, failure modes, kill criteria.
- **[Expected Value]** — Opportunity cost, risk of ruin.
- **[Information Theory]** — Compression, signal vs noise.
- **[Learning Loop]** — Experiment registry, decision log, iteration.

---

## Revision History

| Date | Version | Change | Author |
|------|---------|--------|--------|
| 2026-10-13 | 1.0 | Initial index and status board | — |
| 2026-10-15 | 1.1 | Removed 9 rows for unwritten documents; corrected statuses; replaced planned-document rows with a prioritized "Not yet written" section; declined `roadmap_and_phase_gates.md` | Ken Ira Lacson Talingting |
| 2026-10-15 | 1.2 | Replaced status board with 6-doc target set; rewrote "How to Use" to reference internal protocol sections; added "Retired" legend entry; updated "Not yet written" list | Ken Ira Lacson Talingting |
| 2026-10-17 | 1.3 | Status board updated for the freeze: `evaluation_protocol.md` v2.3 **Frozen**, `scope_and_non_goals.md` v1.3 **Active**, `risk_register_and_premortem.md` v1.2 **Active**, `problem_framing.md` v2.4. Added the "Working inputs (notes/)" pointer. Removed the false claim that `model_and_method_spec.md` is referenced by the protocol (DEC-20261017-019 finding F5d). | Ken Ira Lacson Talingting |
| 2026-10-17 | 1.4 | Added `model_and_method_spec.md` v1.0 **Draft** as the seventh active document and removed it from "Not yet written" (TODO C2 complete). Status board updated: `evaluation_protocol.md` v2.4 (§16 pre-result correction to §4.2, finding F9), `scope_and_non_goals.md` v1.4 (MVP robust-method clarification). Logged DEC-20261017-022. | Ken Ira Lacson Talingting |
| 2026-10-17 | 1.5 | `model_and_method_spec.md` v1.0 → **v1.1 Frozen** (TODO C3 complete; all `[OPEN]` items resolved; DEC-20261017-023). Documentation half of Gate 1 exit now complete. | Ken Ira Lacson Talingting |
| 2026-10-17 | 1.6 | Added the point-in-time candidate universe as a working input: [`../notes/pit_universe_2026-10-17.md`](../notes/pit_universe_2026-10-17.md) v1.0 Confirmed (18 ETFs, anchor 2012-06 — DEC-20261017-024) plus its machine-readable list. `risk_register_and_premortem.md` → v1.3 (R-D02 resolution). Gate 1 is now blocked only on the §5.4.8 leakage suite. | Ken Ira Lacson Talingting |
| 2026-10-17 | 1.7 | Added the snapshot and leakage-suite evidence record as a working input (`../notes/snapshot_and_leakage_evidence_2026-10-17.md`) and a **Gate 1 status** paragraph: both data blockers closed — the §5.4.8 leakage suite passes against snapshot `…-2ad06139` (14 passed, 1 vacuous skip) per DEC-20261017-025. Findings F10/F11 (unpinned risk-free conventions) recorded and pending owner confirmation; F12 records that the §5.4.2 liquidity floor makes the eligible universe 18 → 17 after 2021-11. | Ken Ira Lacson Talingting |
| 2026-10-17 | 1.8 | F10/F11 **owner-confirmed** (`geometric`, `prior_month`) — Gate 1 status paragraph updated; evidence record → v1.1. Added an **Experiment registry status** paragraph: the first Appendix A registrations (`EXP-X-20261017-001` Test B, `EXP-H2-20261017-001` Test D with N = 1), and the two open findings F13 (DSR trial count) and F14 (Test C's window sweep has no common period, so Test C is not registered). DEC-20261017-026. | Ken Ira Lacson Talingting |
| 2026-10-17 | 1.9 | Registry status completed: all three tests pre-registered in Appendix A. F13 resolved (`N = 1`, owner-confirmed); F14 resolved (Test C windows `{36, 60}` at the frozen 2012-06…2026-05 period; the 120-month arm dropped as infeasible). Registry paragraph replaced with a table; B/C/D spec §9 addendum updated. DEC-20261017-027. | Ken Ira Lacson Talingting |
| 2026-10-17 | 1.10 | Added the design diagnostics as a working input (`../notes/power_and_effective_bets_2026-10-17.md` v1.1) and a **design diagnostics status** paragraph: effective bets (3–5 directions, not 18), the Marchenko–Pastur comparison supporting the H1 premise, level-test MDE ≈ 0.67, paired-difference power (≥ 80% at ρ ≥ 0.98), and F15 resolved (report ρ, no amendment, `N = 1` unchanged). Retracted the "underpowered" claim. `decision_log.md` → 1.4. DEC-20261017-028. | Ken Ira Lacson Talingting |
| 2026-10-17 | 1.11 | Added an **engine core status** paragraph: the Phase 2 rewrite's estimator/optimizer core lands (`cvxpy`/`CLARABEL`, no fallback, primal-only KKT certificate), with 1,008 certified solves and zero failures. F16/F17/F18 raised and resolved (DEC-20261017-029); the certificate's own sign defect recorded. `decision_log.md` → 1.5. | Ken Ira Lacson Talingting |

---

*This document is a living index. Update it whenever a document is added, its status changes, or a principle is revised.*