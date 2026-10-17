# robustfolio Documentation Index

**Version:** 1.6
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
| 1 | [`README.md`](README.md) | 1.6 | Active | Index and status board | 2026-10-17 |
| 2 | [`problem_framing.md`](problem_framing.md) | 2.4 | Foundational | Problem statement, stakeholders, causal model, references | 2026-10-17 |
| 3 | [`scope_and_non_goals.md`](scope_and_non_goals.md) | 1.4 | **Active** | Authoritative scope: MVP, extensions, out-of-scope | 2026-10-17 |
| 4 | [`evaluation_protocol.md`](evaluation_protocol.md) | 2.4 | **Frozen** | Metrics, protocol, thresholds, hypotheses, triggers, firewalls, governance, baselines, data contract, cost model, registry rules | 2026-10-17 |
| 5 | [`model_and_method_spec.md`](model_and_method_spec.md) | 1.1 | **Frozen** | Exact method, estimator, optimizer, harness, and metric definitions (absorbs F7) | 2026-10-17 |
| 6 | [`decision_log.md`](decision_log.md) | 1.3 | Active | Immutable record of governance, experiment, and pivot decisions; includes the experiment registry ledger (Appendix A) | 2026-10-17 |
| 7 | [`risk_register_and_premortem.md`](risk_register_and_premortem.md) | 1.3 | **Active** | Failure modes, ratings, mitigations, triggers, pre-mortem scenarios | 2026-10-17 |

**Working inputs (not Tier 0 documents):** the freeze worksheet [`../notes/freeze_worksheet_2026-10-17.md`](../notes/freeze_worksheet_2026-10-17.md) (the decisions behind protocol v2.3, with rationale and sources); the Tests B/C/D specification [`../notes/tests_BCD_spec_2026-10-17.md`](../notes/tests_BCD_spec_2026-10-17.md); the freeze inputs [`../notes/freeze_inputs_2026-10-15.md`](../notes/freeze_inputs_2026-10-15.md); the Phase 1 DSR inputs [`../notes/dsr_inputs_phase1.json`](../notes/dsr_inputs_phase1.json); the confirmed point-in-time candidate universe [`../notes/pit_universe_2026-10-17.md`](../notes/pit_universe_2026-10-17.md) v1.0 (18 ETFs, anchor 2012-06 — DEC-20261017-024) with its machine-readable list [`../notes/pit_candidates_2026-10-17.csv`](../notes/pit_candidates_2026-10-17.csv).

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

---

*This document is a living index. Update it whenever a document is added, its status changes, or a principle is revised.*