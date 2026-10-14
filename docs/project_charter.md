# Project Charter: robustfolio

**Version:** 1.2
**Status:** Draft — pending owner confirmation of Section 9 budgets; then flip to Active
**Owner:** Ken Ira Lacson Talingting
**Created:** 2026-10-13
**Last Updated:** 2026-10-15
**Supersedes:** 1.1
**Related:** [`problem_framing.md`](problem_framing.md), [`scope_and_non_goals.md`](scope_and_non_goals.md), [`success_metrics_and_evaluation_protocol.md`](success_metrics_and_evaluation_protocol.md), [`falsification_and_kill_criteria.md`](falsification_and_kill_criteria.md)

---

## 0. Purpose of This Document

This charter defines **why `robustfolio` exists, who owns it, what it will deliver, how it will be governed, and when it must stop.**

It does not define:

- the problem (see [`problem_framing.md`](problem_framing.md)),
- scope (see [`scope_and_non_goals.md`](scope_and_non_goals.md)),
- the measurement protocol (see [`success_metrics_and_evaluation_protocol.md`](success_metrics_and_evaluation_protocol.md)),
- the kill criteria in detail (see [`falsification_and_kill_criteria.md`](falsification_and_kill_criteria.md)).

It defines the **contract** under which those documents are created, executed, and enforced.

**Conflict resolution.** If this charter conflicts with a later document, this charter wins unless amended by a decision log entry — except for scope, where [`scope_and_non_goals.md`](scope_and_non_goals.md) is authoritative.

---

## 1. Mission

> **Build a reproducible, open-source benchmark for turnover-aware, robust portfolio rebalancing that reports honest net-of-cost out-of-sample results, and that documents its own negative findings.**

The mission has three inseparable parts:

1. **Build** a working, reproducible framework.
2. **Benchmark** robust methods against simple baselines under realistic costs.
3. **Report honestly**, including when robust methods do not beat baselines.

A version of this project that builds a framework but reports inflated results has failed. A version that reports a clean negative result has succeeded.

---

## 2. Vision (What "Done" Looks Like)

A practitioner can clone the repository, point it at public ETF data, run a single command, and obtain:

- Net-of-cost out-of-sample performance for a defined set of baselines and robust methods.
- Turnover, drawdown, cost drag, and deflated Sharpe for each method.
- A reproducible report that distinguishes gross from net and in-sample from out-of-sample.

A reader of the repository can understand, within 30 minutes, what was tested, what was found, and what was not found.

---

## 3. Primary Objective and Objective Function

**Primary objective:** Determine whether any robust, turnover-aware portfolio construction method delivers materially better **net-of-cost out-of-sample risk-adjusted return** than simple baselines, after adjusting for multiple testing.

**Objective function:**

\[
\max_{\pi} \ \mathbb{E}\left[ \text{Net Sharpe}(\pi) \right] \quad \text{subject to} \quad \text{Turnover}(\pi) \le \tau,\ \text{DD}(\pi) \le \delta
\]

where \(\tau\) and \(\delta\) are defined in the evaluation protocol.

**Secondary objective:** Produce a reusable framework and a documented negative result if the primary objective fails.

**Non-objective:** Maximizing in-sample Sharpe, maximizing the number of implemented methods, or producing a publishable positive result at the cost of rigor.

---

## 4. Deliverables

### 4.1 Documentation Deliverables (Tier 0, before code)

Status reflects the actual file state as of 2026-10-15. Documents not yet written are listed in the charter only if they gate a phase; the full planned list lives in the README "Not yet written" section.

| # | Deliverable | Status | Gate |
|---|-------------|--------|------|
| D1 | `README.md` | Active | — |
| D2 | `problem_framing.md` | Foundational (v2.1) | — |
| D3 | `project_charter.md` | Draft → Active on owner sign-off | This document |
| D4 | `scope_and_non_goals.md` | Draft → Active on owner sign-off | — |
| D5 | `success_metrics_and_evaluation_protocol.md` | Draft | Frozen before first experiment |
| D6 | `falsification_and_kill_criteria.md` | Draft | Frozen before first experiment; scheduled to merge into D5 (see §13) |
| D7 | `data_contract_and_point_in_time_policy.md` | Draft | Frozen before first backtest |
| D8 | `cost_model_and_frictions.md` | Draft | Frozen before first backtest |
| D9 | `benchmark_and_baseline_spec.md` | Draft | Frozen before method comparison |
| D10 | `experiment_registry_and_preregistration.md` | Draft | Active before first experiment |
| D11 | `risk_register_and_premortem.md` | Draft | — |
| D12 | `model_and_method_spec.md` | **Not yet written** | Frozen before Phase 1 code |

**Note on numbering.** The original list (D1–D9) omitted `scope_and_non_goals.md` and `risk_register_and_premortem.md`, both of which exist. This version includes them and renumbers. `model_and_method_spec.md` is added as D12 because it is the only missing document that gates Phase 1.

### 4.2 Code Deliverables

| # | Deliverable | Phase |
|---|-------------|-------|
| C1 | Reproducible data ingestion pipeline (point-in-time) | Phase 1 |
| C2 | Baseline implementations: 1/N, risk parity, sample MVO, min variance | Phase 1 |
| C3 | Walk-forward evaluation harness with cost model | Phase 1 |
| C4 | Robust method implementations: shrinkage covariance, Bayesian returns, turnover penalties | Phase 2 |
| C5 | Sensitivity analysis and multiple-testing adjustment (deflated Sharpe) | Phase 3 |
| C6 | Reproducible report generator (gross vs net, IS vs OOS) | Phase 4 |

### 4.3 Research Deliverables

| # | Deliverable | Phase |
|---|-------------|-------|
| R1 | Literature and tool scan validating the gap hypothesis | Phase 0 |
| R2 | Baseline behavior report (extreme weights, turnover, cost drag) | Phase 1 |
| R3 | Method comparison report with confidence intervals | Phase 3 |
| R4 | Honest conclusion: positive, negative, or mixed | Phase 4 |

---

## 5. Non-Goals (moved)

Non-goals are defined authoritatively in [`scope_and_non_goals.md`](scope_and_non_goals.md) §5. They are not duplicated here.

The scope document's "Out of Scope" list is broader and more specific than the list that previously appeared in this section. Any conflict between this charter and the scope document on the question of non-goals is resolved in favor of the scope document.

---

## 6. Phase Gates

Each phase has a **go/no-go decision**. A phase cannot begin until the prior gate is passed. Gates are enforced by the owner, not by momentum.

| Phase | Name | Entry Criteria | Exit Criteria (Go) | No-Go Action |
|-------|------|----------------|--------------------|--------------|
| 0 | Problem Validation | Charter Active | R1 complete and documents a scan of ≥10 relevant open-source tools, papers, or repositories, explicitly stating which part of the gap hypothesis remains uncovered; D5, D6, D7, D8, D9, D10 drafted | Narrow problem or stop |
| 1 | Data & Baselines | Gate 0 passed; D7, D8, D9 frozen; D12 frozen | C1, C2, C3 work; R2 shows MVO instability is real | Fix data/cost contract or stop |
| 2 | Robust Methods | Gate 1 passed | C4 implemented and unit-tested; no leakage | Reduce method scope |
| 3 | Evaluation | Gate 2 passed | C5 complete; R3 produced; multiple-testing adjusted | Extend evaluation or narrow claims |
| 4 | Reporting & Release | Gate 3 passed | C6 complete; R4 written; repo reproducible from scratch | Release as negative result or diagnostic tool |
| 5 | Extensions (optional) | Gate 4 passed and primary objective met OR clearly framed | Extension scoped and justified by priors | Do not start |

**Gate discipline:** A gate may be passed with a documented negative result. It may not be passed by relaxing the evaluation protocol after seeing results. [Bayesian] [Experimental]

---

## 7. Kill, Pivot, and Stop Criteria

Detailed thresholds live in [`falsification_and_kill_criteria.md`](falsification_and_kill_criteria.md). The charter establishes the *authority* and the *categories*:

| Category | Meaning | Authority |
|----------|---------|-----------|
| **Kill** | Stop the project; archive findings | Owner |
| **Pivot** | Change the problem framing or deliverable (e.g., diagnostic tool instead of method superiority) | Owner |
| **Stop-and-report** | Conclude with a documented negative result | Owner |
| **Continue** | Proceed to next phase | Owner |

**Hard rules:**

1. No phase may exceed its time-box without a decision log entry.
2. If the primary objective fails after Phase 3, the project must pivot to Stop-and-report rather than add complexity.
3. Adding a new method to rescue a failing result requires a pre-registered hypothesis and a new experiment entry.
4. The owner may kill the project at any time. A decision log entry is still required, even if the justification is simply "owner decision." This preserves the learning loop and prevents silent abandonment.

---

## 8. Decision Rights

| Role | Holder | Responsibility |
|------|--------|----------------|
| **Owner / Decision-maker** | Ken Ira Lacson Talingting | Final authority on scope, gates, kill/pivot, and claims |
| **Reasoning partner** | LLM (Core Mental Models OS) | Challenge assumptions, surface failure modes, apply models, flag anti-patterns |
| **Reviewer** | None (no third-party reviewer; self-review plus reasoning-partner challenge) | Sanity-check evaluation protocol and claims before release |
| **Informed** | Open-source users, readers of the repo | Consume results and documentation |

**Escalation:** If the reasoning partner identifies a violation of the evaluation protocol, kill criteria, or anti-patterns, it must flag it. The owner decides. Silence is not consent.

---

## 9. Resource Constraints

> **Note:** The values below are **proposed conservative defaults** for a solo, part-time independent researcher. They are not confirmed. The owner must confirm or replace each value before this charter becomes `Active`. Once confirmed, this section becomes the enforceable time-box source for Sections 6 and 7.

| Resource | Budget | Notes |
|----------|--------|-------|
| Time per week | 10 hours *(proposed)* | Determines feasible phase durations |
| Total time budget | 6 months *(proposed)* | Hard stop at this limit unless amended |
| Phase 0 time-box | 2 weeks *(proposed)* | Problem validation only |
| Phase 1 time-box | 6 weeks *(proposed)* | Data + baselines |
| Phase 2 time-box | 6 weeks *(proposed)* | Robust methods |
| Phase 3 time-box | 4 weeks *(proposed)* | Evaluation |
| Phase 4 time-box | 4 weeks *(proposed)* | Reporting + release |
| Compute budget | $0 *(proposed)* | Local machine only |
| Data budget | $0 *(proposed)* | Public/free data only |
| Monetary budget | $0 *(proposed)* | Preferably zero |
| Opportunity cost | Acknowledged | Time here is not spent on signal research, a general backtesting toolkit, or regime detection |

**Risk of ruin:** Low. The project risks time, not capital or reputation, provided claims are framed honestly and phase gates are enforced. [EV]

---

## 10. Assumptions and Constraints

**Assumptions (must be validated or invalidated):**

- Public ETF and large-cap equity data are sufficient to demonstrate the problem.
- Monthly rebalancing is a realistic baseline frequency.
- Fixed-bps transaction costs are a reasonable first approximation.
- Simple baselines (1/N, risk parity) are strong enough to be meaningful competitors.
- The gap hypothesis (see [`problem_framing.md`](problem_framing.md) §4.1) survives a tool scan.

**Constraints:**

- Point-in-time discipline is mandatory. No lookahead.
- All experiments must be pre-registered before execution.
- All reported performance must be net-of-cost unless explicitly labeled gross.
- All claims must survive multiple-testing adjustment.
- Code must be reproducible from a clean environment using a lockfile.

**Unknowns:**

- Whether robust methods can beat baselines net of costs.
- Whether the effect, if any, is stable across regimes.
- Whether the benchmark gap is real or already partially filled.

---

## 11. Governance Cadence

| Cadence | Activity | Output |
|---------|----------|--------|
| Before each experiment | Pre-register hypothesis, parameters, metrics, decision rule | Entry in `experiment_registry_and_preregistration.md` |
| After each experiment | Record result, update priors, decide next action | Entry + decision log if material |
| At each phase gate | Review exit criteria, decide go/no-go/pivot/kill | Decision log entry |
| Monthly | Review charter, status board, risk register | Updated docs |
| On surprise or failure | Update risk register and decision log; revisit priors | Updated docs |

---

## 12. Definition of Done

The project is **done** when all of the following are true:

1. All Tier 0 documentation is Frozen or Active, and this charter is Active.
2. Baselines and at least one robust method are implemented and unit-tested.
3. Walk-forward, net-of-cost evaluation is reproducible from a clean environment.
4. Results are reported with confidence intervals, multiple-testing adjustment, and explicit gross/net and IS/OOS labels.
5. A conclusion is stated: positive, negative, or mixed, with limitations.
6. The repository is publicly reproducible (or explicitly documented as private with a reproducible local setup).
7. The evaluation protocol and kill criteria were not weakened after seeing results.

**Done does not require a positive result.** A clean negative result satisfies the definition of done.

---

## 13. What Would Cause This Charter to Change

- A change in owner availability or time budget.
- A validated finding that the problem is already solved by existing tools.
- A pivot from "method superiority" to "diagnostic benchmark."
- A decision to expand scope to a new asset class or frequency (requires amendment, not silent expansion).
- A decision to stop the project.
- Completion of the planned merge of `falsification_and_kill_criteria.md` into `success_metrics_and_evaluation_protocol.md` (see the execution TODO, item B1), which will update references in §0, §4.1, §6, and §7.

Any change requires a decision log entry and a version bump.

---

## 14. Model Tags Applied

- **[First Principles]** — Reduced the project to mission, deliverables, gates, and authority.
- **[Inversion]** — Defined non-goals, kill criteria, and failure modes before starting.
- **[Systems]** — Defined phase gates, governance cadence, and feedback loops.
- **[Expected Value]** — Made opportunity cost and risk of ruin explicit.
- **[Information Theory]** — Compressed the charter to decisions, not descriptions.
- **[Learning Loop]** — Built in experiment registry, decision log, and prior updates.
- **[Bayesian]** — Framed assumptions as priors to be validated or invalidated.

---

## 15. Revision History

| Date | Version | Change | Author |
|------|---------|--------|--------|
| 2026-10-13 | 1.0 | Initial charter | Ken Ira Lacson Talingting |
| 2026-10-14 | 1.1 | Filled Section 9 with proposed defaults; resolved reviewer field; tightened Phase 0 exit criterion; required decision log for kills; added charter to Definition of Done; set monthly cadence | Ken Ira Lacson Talingting |
| 2026-10-15 | 1.2 | Replaced §5 (Non-Goals) with pointer to scope document (A2); updated §4.1 status board to match actual file states and added D4, D11, D12; changed "gap claim" to "gap hypothesis" in §6 and §10 for consistency with problem_framing v2.1; clarified §8 Reviewer row; added §13 clause anticipating the falsification merge | Ken Ira Lacson Talingting |

---

*This charter governs the project. It must be amended deliberately, not eroded by convenience.*
