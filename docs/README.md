# robustfolio Documentation Index

**Version:** 1.0  
**Status:** Active  
**Last Updated:** 2026-10-13  

This folder contains the foundational contracts, protocols, and decision records for the `robustfolio` project.  
The purpose of this documentation is to **prevent predictable failure modes** before writing code: unclear objectives, data leakage, overfitting, unrealistic cost assumptions, scope creep, and unfalsifiable claims.

Read this file first. It is the map and status board for all project documentation.

---

## Documentation Principles

1. **One decision per document.** If a document answers multiple unrelated decisions, split it.
2. **Status is explicit.** Every document must declare: `draft`, `active`, `frozen`, or `deprecated`.
3. **Freeze before experiments.** Evaluation protocols and kill criteria must be `frozen` before running any experiment that tests a hypothesis.
4. **No duplication.** If a topic is covered elsewhere, link to it instead of repeating.
5. **Update the log.** Every major change to a frozen document requires a decision log entry.

---

## Status Board

| # | Document | Status | Purpose | Last Updated |
|---|----------|--------|---------|--------------|
| 1 | [`README.md`](README.md) | Active | Index and status board | 2026-10-13 |
| 2 | [`problem_framing.md`](problem_framing.md) | Active | Real problem, decision, stakeholders, causal model, scope | 2026-10-13 |
| 3 | [`project_charter.md`](project_charter.md) | Planned | Mission, deliverables, non-goals, phase gates, decision rights | — |
| 4 | [`success_metrics_and_evaluation_protocol.md`](success_metrics_and_evaluation_protocol.md) | Planned | Primary/secondary metrics, baselines, walk-forward, deflated Sharpe, cost sensitivity | — |
| 5 | [`falsification_and_kill_criteria.md`](falsification_and_kill_criteria.md) | Planned | Hypotheses, falsification tests, stop/pivot/kill thresholds, time-boxes | — |
| 6 | [`data_contract_and_point_in_time_policy.md`](data_contract_and_point_in_time_policy.md) | Planned | Data sources, schema, survivorship, corporate actions, point-in-time rules | — |
| 7 | [`cost_model_and_frictions.md`](cost_model_and_frictions.md) | Planned | Fixed bps, slippage, rebalance timing, capacity, sensitivity ranges | — |
| 8 | [`benchmark_and_baseline_spec.md`](benchmark_and_baseline_spec.md) | Planned | Exact baselines (1/N, risk parity, sample MVO, etc.) and implementation details | — |
| 9 | [`experiment_registry_and_preregistration.md`](experiment_registry_and_preregistration.md) | Planned | How experiments are logged and locked before running | — |
| 10 | [`risk_register_and_premortem.md`](risk_register_and_premortem.md) | Planned | Failure modes, likelihood, impact, mitigation, trigger, owner | — |
| 11 | [`decision_log.md`](decision_log.md) | Planned | Why key choices were made, alternatives, rationale, revisit triggers | — |
| 12 | [`scope_and_non_goals.md`](scope_and_non_goals.md) | Planned | In-scope, out-of-scope, MVP, extensions (may point to problem_framing) | — |
| 13 | [`reproducibility_and_environment.md`](reproducibility_and_environment.md) | Planned | Python version, lockfile, seeds, deterministic flags, data snapshots | — |
| 14 | [`model_and_method_spec.md`](model_and_method_spec.md) | Planned | Formal definitions of estimators, optimizers, penalties, constraints | — |
| 15 | [`validation_and_testing_strategy.md`](validation_and_testing_strategy.md) | Planned | Unit/integration/leakage/synthetic tests, property-based tests | — |
| 16 | [`architecture_decision_records/`](architecture_decision_records/) | Planned | Template and records for irreversible technical decisions | — |
| 17 | [`results_reporting_and_claims_policy.md`](results_reporting_and_claims_policy.md) | Planned | Gross vs net, in-sample vs OOS, confidence intervals, limitations | — |
| 18 | [`roadmap_and_phase_gates.md`](roadmap_and_phase_gates.md) | Planned | Phases, deliverables, go/no-go criteria, time-boxes | — |
| 19 | [`glossary.md`](glossary.md) | Planned | Terms, definitions, notation, acronyms | — |
| 20 | [`open_source_and_license_policy.md`](open_source_and_license_policy.md) | Planned | License, contribution rules, citation, code of conduct | — |

**Status legend:**  
- `Planned` — not yet written.  
- `Draft` — written but not yet reviewed.  
- `Active` — current, may still change.  
- `Frozen` — locked; changes require a decision log entry.  
- `Deprecated` — no longer used; kept for historical reference.

---

## How to Use This Documentation

- **Before coding:** Ensure Tier 0 documents (items 1–7) are at least `draft` and reviewed. Items 4, 5, 6, and 7 must be `frozen` before any experiment that tests a hypothesis.
- **Before running a backtest:** Confirm `data_contract_and_point_in_time_policy.md` and `cost_model_and_frictions.md` are `frozen`. Log the experiment in `experiment_registry_and_preregistration.md` before execution.
- **Before comparing methods:** Ensure `success_metrics_and_evaluation_protocol.md` and `falsification_and_kill_criteria.md` are `frozen`. Use `results_reporting_and_claims_policy.md` for reporting.
- **When making a technical decision:** Record it in `architecture_decision_records/` if irreversible, or in `decision_log.md` otherwise.
- **When something fails or surprises:** Update `risk_register_and_premortem.md` and `decision_log.md`. Update priors in `success_metrics_and_evaluation_protocol.md` if warranted.

---

## Model Tags Used in This Project

This project applies the following mental models explicitly:

- **[First Principles]** — Reduce to fundamentals.
- **[Bayesian]** — Update beliefs with evidence; track calibration.
- **[Causal]** — Identify interventions and confounders.
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

---

*This document is a living index. Update it whenever a document is added, its status changes, or a principle is revised.*
