# robustfolio Documentation Index

**Version:** 1.1
**Status:** Active
**Last Updated:** 2026-10-15

This folder contains the foundational contracts, protocols, and decision records for the `robustfolio` project.
The purpose of this documentation is to **prevent predictable failure modes** before writing code: unclear objectives, data leakage, overfitting, unrealistic cost assumptions, scope creep, and unfalsifiable claims.

Read this file first. It is the map and status board for all project documentation.

---

## Documentation Principles

1. **One decision per document.** If a document answers multiple unrelated decisions, split it.
2. **Status is explicit.** Every document must declare: `draft`, `active`, `frozen`, or `deprecated`.
3. **Freeze before experiments.** Evaluation protocols, data contracts, cost models, and kill criteria must be `frozen` before running any experiment that tests a hypothesis.
4. **No duplication.** If a topic is covered elsewhere, link to it instead of repeating.
5. **Update the log.** Every major change to a frozen document requires a decision log entry.

---

## Status Board

Only documents that currently exist are listed. Documents that are planned but not yet written are listed under "Not yet written" below.

| # | Document | Version | Status | Purpose | Last Updated |
|---|----------|---------|--------|---------|--------------|
| 1 | [`README.md`](README.md) | 1.1 | Active | Index and status board | 2026-10-15 |
| 2 | [`problem_framing.md`](problem_framing.md) | 2.0 | Foundational | Problem statement, stakeholders, causal model, references | 2026-10-14 |
| 3 | [`project_charter.md`](project_charter.md) | 1.1 | Draft | Mission, deliverables, non-goals, phase gates, decision rights | 2026-10-14 |
| 4 | [`scope_and_non_goals.md`](scope_and_non_goals.md) | 1.0 | Draft | Authoritative scope: MVP, extensions, out-of-scope | 2026-10-14 |
| 5 | [`success_metrics_and_evaluation_protocol.md`](success_metrics_and_evaluation_protocol.md) | 1.0 | Draft | Primary/secondary metrics, baselines, walk-forward, deflated Sharpe, cost sensitivity | 2026-10-14 |
| 6 | [`falsification_and_kill_criteria.md`](falsification_and_kill_criteria.md) | 1.0 | Draft | Hypotheses, falsification tests, kill/pivot/stop triggers, sunk-cost firewall | 2026-10-14 |
| 7 | [`data_contract_and_point_in_time_policy.md`](data_contract_and_point_in_time_policy.md) | 1.0 | Draft | Data sources, universe, survivorship, corporate actions, point-in-time rules | 2026-10-14 |
| 8 | [`cost_model_and_frictions.md`](cost_model_and_frictions.md) | 1.0 | Draft | Fixed-bps cost model, execution timing, sensitivity levels, limitations | 2026-10-14 |
| 9 | [`benchmark_and_baseline_spec.md`](benchmark_and_baseline_spec.md) | 1.0 | Draft | Baseline set (B1–B5), mathematical definitions, fair-comparison rules | 2026-10-14 |
| 10 | [`experiment_registry_and_preregistration.md`](experiment_registry_and_preregistration.md) | 1.0 | Draft | Pre-registration rules, registry structure, denominator discipline | 2026-10-14 |
| 11 | [`risk_register_and_premortem.md`](risk_register_and_premortem.md) | 1.0 | Draft | Failure modes, ratings, mitigations, triggers, pre-mortem scenarios | 2026-10-14 |

**Status legend:**
- `Foundational` — the problem contract; changes require strong justification.
- `Draft` — written but not yet reviewed or confirmed.
- `Active` — current, may still change.
- `Frozen` — locked; changes require a decision log entry.
- `Deprecated` — no longer used; kept for historical reference.

---

## Not yet written

The following documents are referenced by the charter deliverables list or by other documents, but do not exist yet. They are not tracked here as rows because a status board of unwritten documents is a wish list, not a status board.

The authoritative list of planned deliverables lives in [`project_charter.md`](project_charter.md) §4. In priority order:

1. `model_and_method_spec.md` — **highest priority.** Referenced by `benchmark_and_baseline_spec.md` and `experiment_registry_and_preregistration.md`; the project cannot run its first experiment without it.
2. `decision_log.md` — created on first use.
3. `reproducibility_and_environment.md` — written when the Python environment is first set up.
4. `results_reporting_and_claims_policy.md` — written before Phase 4 (reporting).
5. `architecture_decision_records/` — created when the first irreversible technical decision is made.
6. `glossary.md` — written when a reader is confused, not speculatively.
7. `open_source_and_license_policy.md` — written before public release.
8. `roadmap_and_phase_gates.md` — **declined.** The charter §6 already contains phase gates; a separate file would duplicate.

---

## How to Use This Documentation

- **Before coding:** Ensure `problem_framing.md`, `project_charter.md`, and `scope_and_non_goals.md` are at least `Draft`.
- **Before running a backtest:** Confirm `data_contract_and_point_in_time_policy.md` and `cost_model_and_frictions.md` are `Frozen`. Log the experiment in `experiment_registry_and_preregistration.md` before execution.
- **Before comparing methods:** Ensure `success_metrics_and_evaluation_protocol.md`, `falsification_and_kill_criteria.md`, and `benchmark_and_baseline_spec.md` are `Frozen`.
- **When making a technical decision:** Record it in `decision_log.md`. If irreversible and architectural, also record it in `architecture_decision_records/`.
- **When something fails or surprises:** Update `risk_register_and_premortem.md` and `decision_log.md`.

---

## Model Tags Used in This Project

This project applies the following mental models explicitly:

- **[First Principles]** — Reduce to fundamentals.
- **[Bayesian]** — Update beliefs with evidence; track calibration.
- **[Experimental]** — Falsification, pre-registration, walk-forward.
- **[Systems]** — Feedback loops, delays, bottlenecks.
- **[Inversion]** — Pre-mortem, failure modes, kill criteria.
- **[Expected Value]** — Opportunity cost, risk of ruin.
- **[Information Theory]** — Compression, signal vs noise.
- **[Learning Loop]** — Experiment registry, decision log, iteration.

Model tags appear in documents where they materially shape the content.

---

## Revision History

| Date | Version | Change | Author |
|------|---------|--------|--------|
| 2026-10-13 | 1.0 | Initial index and status board | — |
| 2026-10-15 | 1.1 | Removed 9 rows for unwritten documents; corrected statuses to match actual file headers; replaced planned-document rows with a single prioritized "Not yet written" section; added version column; declined `roadmap_and_phase_gates.md` as a duplicate of charter §6 | Ken Ira Lacson Talingting |

---

*This document is a living index. Update it whenever a document is added, its status changes, or a principle is revised.*
