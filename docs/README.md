# robustfolio Documentation Index

**Version:** 1.2
**Status:** Active
**Last Updated:** 2026-10-15

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

The active documentation set is six files. All other Tier 0 documents have been merged into these per DEC-20261015-017 and DEC-20261015-018.

| # | Document | Version | Status | Purpose | Last Updated |
|---|----------|---------|--------|---------|--------------|
| 1 | [`README.md`](README.md) | 1.2 | Active | Index and status board | 2026-10-15 |
| 2 | [`problem_framing.md`](problem_framing.md) | 2.3 | Foundational | Problem statement, stakeholders, causal model, references | 2026-10-15 |
| 3 | [`scope_and_non_goals.md`](scope_and_non_goals.md) | 1.2 | Draft → Active on sign-off | Authoritative scope: MVP, extensions, out-of-scope | 2026-10-15 |
| 4 | [`evaluation_protocol.md`](evaluation_protocol.md) | 2.2 | Draft → Frozen before first confirmatory experiment | Metrics, protocol, thresholds, hypotheses, triggers, firewalls, governance, baselines, data contract, cost model, registry rules | 2026-10-15 |
| 5 | [`decision_log.md`](decision_log.md) | 1.2 | Active | Immutable record of governance, experiment, and pivot decisions; includes the experiment registry ledger (Appendix A) | 2026-10-15 |
| 6 | [`risk_register_and_premortem.md`](risk_register_and_premortem.md) | 1.1 | Draft → Active on sign-off | Failure modes, ratings, mitigations, triggers, pre-mortem scenarios | 2026-10-15 |

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

1. `model_and_method_spec.md` — **highest priority.** Referenced by `evaluation_protocol.md` §4 and §12; the project cannot run its first confirmatory experiment without it.
2. `reproducibility_and_environment.md` — written when the Python environment is first set up.
3. `results_reporting_and_claims_policy.md` — written before Phase 4 (reporting).
4. `architecture_decision_records/` — created when the first irreversible technical decision is made.
5. `open_source_and_license_policy.md` — written before public release.

---

## How to Use This Documentation

- **Before coding:** Ensure `problem_framing.md`, `scope_and_non_goals.md`, and `evaluation_protocol.md` §8 are at least `Draft`.
- **Before running a backtest:** Confirm `evaluation_protocol.md` §5.4 (data contract) and §5.5 (cost model) are `Frozen`. Log the experiment in `decision_log.md` Appendix A before execution.
- **Before comparing methods:** Ensure `evaluation_protocol.md` §§4, 6, 7, and 12 are `Frozen`.
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

---

*This document is a living index. Update it whenever a document is added, its status changes, or a principle is revised.*