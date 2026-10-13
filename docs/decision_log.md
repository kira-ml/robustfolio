# Decision Log: robustfolio

**Version:** 1.0  
**Status:** Active — this log is used from the moment the first Tier 0 document is written  
**Owner:** Ken Ira Lacson Talingting  
**Created:** 2026-10-14  
**Last Updated:** 2026-10-14  
**Supersedes:** None  
**Related:** [`README.md`](README.md), [`project_charter.md`](project_charter.md), [`problem_framing.md`](problem_framing.md), [`success_metrics_and_evaluation_protocol.md`](success_metrics_and_evaluation_protocol.md), [`falsification_and_kill_criteria.md`](falsification_and_kill_criteria.md), [`data_contract_and_point_in_time_policy.md`](data_contract_and_point_in_time_policy.md), [`cost_model_and_frictions.md`](cost_model_and_frictions.md), [`benchmark_and_baseline_spec.md`](benchmark_and_baseline_spec.md), [`experiment_registry_and_preregistration.md`](experiment_registry_and_preregistration.md), [`risk_register_and_premortem.md`](risk_register_and_premortem.md), [`scope_and_non_goals.md`](scope_and_non_goals.md)

---

## 0. Purpose of This Document

This document is the **append-only log of material decisions** made during the `robustfolio` project.

Its purpose is to:

1. Preserve the **reasoning** behind decisions, not just the decision itself.
2. Make **sunk-cost fallacy** harder by documenting why a path was chosen and what would change it.
3. Provide an **audit trail** for anyone (including the owner) asking "why is this the way it is?"
4. Feed the **learning loop**: every closed decision is an opportunity to update priors.
5. Prevent **silent drift**: any change to a frozen document is recorded here.

A decision not logged is a decision that will be forgotten, second-guessed, or reversed without reflection.

**This log is not frozen.** It grows with the project. Its *rules* and *format* are stable; its contents accumulate.

---

## 1. What Counts as a Decision

Log anything that materially affects the project's direction, claims, or reproducibility.

### 1.1 Must log

- Any change to a Frozen document (§11 of most contracts).
- Any scope change (promotion, demotion, extension entry).
- Any pivot, kill, or stop-and-report decision.
- Any phase-gate outcome.
- Any change to a baseline, metric, cost model, or data contract.
- Any new experiment that is not routine (i.e., beyond the MVP set).
- Any materialized risk with a non-trivial response.
- Any reversal of a prior decision.
- Any "continue unchanged" decision after a trigger fired.

### 1.2 Do not log

- Routine implementation details (variable naming, file structure).
- Debugging sessions with no lasting effect.
- Exploratory work that produced no reportable result.
- Minor documentation typo fixes.

**Rule of thumb:** if you would want to be able to defend it six months from now, log it.

---

## 2. Entry Format

Every entry follows the same structure. Fields marked *optional* may be omitted for small decisions.

```markdown
## DEC-<YYYYMMDD>-<nnn>

**Date:** YYYY-MM-DD  
**Type:** SCOPE | METHOD | PROTOCOL | GOVERNANCE | DATA | COST | BASELINE | EXPERIMENT | PIVOT | KILL | STOP | RISK  
**Status:** ACTIVE | SUPERSEDED | REVERSED  
**Authority:** Owner  
**Related docs:** (links)  
**Related experiments:** (EXP-IDs, if any)  
**Related risks:** (R-IDs, if any)  

**Context:**  
One paragraph. What situation prompted this decision.

**Decision:**  
What was decided, stated as a single clear choice.

**Alternatives considered:**  
- Alternative A — rejected because …  
- Alternative B — rejected because …

**Rationale:**  
Why this decision, grounded in the Core Mental Models where relevant.

**Reversibility:** Easy | Moderate | Hard  
**Revisit trigger:**  
What observable event would cause this decision to be revisited.

*Optional for larger decisions:*

**Expected value assessment:**  
Probability-weighted reasoning if relevant.

**Pre-mortem:**  
How this decision could fail, and how that would be detected.
```

---

## 3. Rules of the Log

1. **Append-only.** Entries are never deleted. Corrections are new entries that reference the old one.
2. **Immutable.** Once written, an entry's Context, Decision, Alternatives, and Rationale are frozen.
3. **Status updates allowed.** The `Status` field may change to `SUPERSEDED` or `REVERSED`, with a reference to the superseding entry.
4. **Material changes to Frozen documents require an entry.** No exceptions.
5. **Every kill, pivot, and stop produces an entry.** Even if the justification is "owner decision."
6. **Every materialized risk with a response produces an entry.** Even if the response is "continue."
7. **Every phase-gate outcome produces an entry.** Even if the outcome is "proceed as planned."
8. **Every entry has a stable ID.** IDs are never reused. `DEC-YYYYMMDD-NNN`, incrementing per day.
9. **Cross-reference by ID, not position.** "See DEC-20261015-002," never "see the entry above."

---

## 4. Entry Index

> Newest first. This index is regenerated whenever the log is updated. Entries themselves are appended in chronological order in §5.

| ID | Date | Type | Summary | Status |
|----|------|------|---------|--------|
| DEC-20261014-011 | 2026-10-14 | SCOPE | MVP universe: 15–25 US ETFs | ACTIVE |
| DEC-20261014-010 | 2026-10-14 | BASELINE | Baseline set B1–B5 | ACTIVE |
| DEC-20261014-009 | 2026-10-14 | COST | Baseline κ = 10 bps | ACTIVE |
| DEC-20261014-008 | 2026-10-14 | PROTOCOL | Deflated Sharpe as primary multiple-testing adjustment | ACTIVE |
| DEC-20261014-007 | 2026-10-14 | PROTOCOL | Walk-forward: 36-month rolling, 12-month test | ACTIVE |
| DEC-20261014-006 | 2026-10-14 | METHOD | Turnover penalty: L1 = κ alignment | ACTIVE |
| DEC-20261014-005 | 2026-10-14 | DATA | Point-in-time price reconstruction required | ACTIVE |
| DEC-20261014-004 | 2026-10-14 | GOVERNANCE | Falsification before optimization | ACTIVE |
| DEC-20261014-003 | 2026-10-14 | SCOPE | Monthly rebalancing baseline | ACTIVE |
| DEC-20261014-002 | 2026-10-14 | METHOD | Adopt Core Mental Models OS as reasoning framework | ACTIVE |
| DEC-20261014-001 | 2026-10-14 | GOVERNANCE | Adopt falsificationist project structure | ACTIVE |

---

## 5. Entries

> Entries are appended in chronological order. Newest at the bottom. Never insert in the middle.

---

### DEC-20261014-001

**Date:** 2026-10-14  
**Type:** GOVERNANCE  
**Status:** ACTIVE  
**Authority:** Owner  
**Related docs:** [`project_charter.md`](project_charter.md), [`problem_framing.md`](problem_framing.md)  
**Related risks:** R-P01, R-P02, R-S05  

**Context:**  
Before any code, the project needed a governance structure that would prevent silent failure, false positives, and goalpost-moving.

**Decision:**  
Adopt a falsificationist project structure with frozen Tier 0 contracts: evaluation protocol, kill criteria, data contract, cost model, baseline spec, and experiment registry.

**Alternatives considered:**  
- Ad-hoc research notebook — rejected: no reproducibility, no protection against p-hacking.  
- Lightweight docs — rejected: insufficient defense against the known failure modes of portfolio research.  
- Full academic paper outline — rejected: over-formal for a solo project; slows execution.

**Rationale:**  
[First Principles] [Inversion] The failure modes of portfolio research are well known: overfitting, lookahead, cost ignorance, multiple testing. A falsificationist structure addresses each explicitly and forces the owner to confront them before, not after, seeing results.

**Reversibility:** Hard  
**Revisit trigger:** If the structure proves too heavy to sustain and blocks Phase 1 progress, downgrade to a lighter structure with an explicit decision entry.

---

### DEC-20261014-002

**Date:** 2026-10-14  
**Type:** METHOD  
**Status:** ACTIVE  
**Authority:** Owner  
**Related docs:** All Tier 0 docs  
**Related risks:** R-H03 (blind spots)  

**Context:**  
Solo research is prone to blind spots, sunk-cost reasoning, and confirmation bias. A reasoning framework is needed to surface these.

**Decision:**  
Adopt the Core Mental Models OS as the reasoning framework for all substantive decisions in this project.

**Alternatives considered:**  
- No framework — rejected: leaves failure modes invisible.  
- Informal checklist — rejected: too weak to enforce; drifts under pressure.

**Rationale:**  
[Systems] [Inversion] An explicit framework, applied consistently and labeled in docs, makes reasoning auditable. It also establishes a role (reasoning partner) that can challenge the owner's decisions.

**Reversibility:** Easy  
**Revisit trigger:** If model tags become ritual rather than useful, simplify to a smaller core set.

---

### DEC-20261014-003

**Date:** 2026-10-14  
**Type:** SCOPE  
**Status:** ACTIVE  
**Authority:** Owner  
**Related docs:** [`scope_and_non_goals.md`](scope_and_non_goals.md), [`cost_model_and_frictions.md`](cost_model_and_frictions.md)  

**Context:**  
Rebalancing frequency materially affects turnover and cost sensitivity. The project needs a baseline frequency.

**Decision:**  
Monthly rebalancing is the baseline frequency. Other frequencies (weekly, quarterly) are extensions.

**Alternatives considered:**  
- Quarterly — rejected: too few observations for turnover to differentiate methods.  
- Weekly — rejected: unrealistic for retail and inflates costs without adding insight.  
- Multiple frequencies in MVP — rejected: scope creep.

**Rationale:**  
[First Principles] [Systems] Monthly is the standard practitioner frequency for ETF portfolios, produces enough rebalancing events to test turnover behavior, and keeps the data pipeline simple.

**Reversibility:** Easy  
**Revisit trigger:** If monthly turnover turns out to be dominated by drift rather than signal, revisit with quarterly.

---

### DEC-20261014-004

**Date:** 2026-10-14  
**Type:** GOVERNANCE  
**Status:** ACTIVE  
**Authority:** Owner  
**Related docs:** [`falsification_and_kill_criteria.md`](falsification_and_kill_criteria.md)  

**Context:**  
The most common failure in quantitative research is confirmationism: running experiments until something looks significant, then reporting it.

**Decision:**  
Falsification and kill criteria are defined before any experiment is run, and the project must be willing to conclude with a documented negative result.

**Alternatives considered:**  
- Define criteria after piloting — rejected: this is p-hacking with extra steps.  
- Define criteria informally — rejected: informal criteria are reinterpreted under pressure.

**Rationale:**  
[Inversion] [Experimental] Writing the falsification criteria first forces the owner to specify what would change their mind, which is the only reliable defense against post-hoc rationalization.

**Reversibility:** Hard  
**Revisit trigger:** None. This is a foundational commitment.

---

### DEC-20261014-005

**Date:** 2026-10-14  
**Type:** DATA  
**Status:** ACTIVE  
**Authority:** Owner  
**Related docs:** [`data_contract_and_point_in_time_policy.md`](data_contract_and_point_in_time_policy.md)  
**Related risks:** R-D01, R-D02  

**Context:**  
Free price sources (yfinance, Stooq) retroactively adjust prices for corporate actions. Naive use introduces lookahead.

**Decision:**  
Point-in-time adjusted prices must be reconstructed from raw prices and corporate actions. If reconstruction is not feasible for a given source, affected claims are downgraded to exploratory.

**Alternatives considered:**  
- Use `auto_adjust=True` — rejected: silent lookahead, the exact failure mode the project is meant to avoid.  
- Assume bias is small — rejected: unquantified bias is worse than no result.  
- Downgrade all claims from the start — rejected: unnecessary if reconstruction is feasible.

**Rationale:**  
[Inversion] [Systems] This is the single most common silent corruption in retail backtesting. Requiring reconstruction makes the corruption visible.

**Reversibility:** Moderate  
**Revisit trigger:** If reconstruction proves infeasible in Phase 1, downgrade affected claims per data contract §4.4 and log the change.

---

### DEC-20261014-006

**Date:** 2026-10-14  
**Type:** METHOD  
**Status:** ACTIVE  
**Authority:** Owner  
**Related docs:** [`cost_model_and_frictions.md`](cost_model_and_frictions.md), [`benchmark_and_baseline_spec.md`](benchmark_and_baseline_spec.md)  

**Context:**  
The L1 turnover penalty has a parameter λ. The cost model has a parameter κ. Misalignment between them means the penalized baseline (B5) is not actually cost-aware.

**Decision:**  
Set λ = κ by default. This aligns the penalty with the actual cost in return units. Any deviation requires a pre-registered experiment.

**Alternatives considered:**  
- Tune λ on a validation set — rejected: introduces a hyperparameter that invites overfitting.  
- Set λ > κ for conservatism — rejected: not principled; the penalty should reflect actual cost.  
- Ignore alignment — rejected: renders B5 meaningless as a cost-aware baseline.

**Rationale:**  
[First Principles] [Experimental] Alignment between penalty and cost is the minimal requirement for B5 to be a fair comparison to robust cost-aware methods.

**Reversibility:** Easy  
**Revisit trigger:** If λ = κ produces degenerate behavior (e.g., no rebalancing at all), register a new experiment to explore tuned λ.

---

### DEC-20261014-007

**Date:** 2026-10-14  
**Type:** PROTOCOL  
**Status:** ACTIVE  
**Authority:** Owner  
**Related docs:** [`success_metrics_and_evaluation_protocol.md`](success_metrics_and_evaluation_protocol.md)  

**Context:**  
Walk-forward windows trade off estimation accuracy against test sample size. Too short overfits; too long reduces fold count.

**Decision:**  
Walk-forward uses a 36-month rolling estimation window, 12-month test window, and 12-month step size.

**Alternatives considered:**  
- 60-month estimation — rejected: too few folds; expensive for a short ETF history.  
- 24-month estimation — rejected: covariance estimates too noisy.  
- Expanding window — rejected: loses regime adaptivity; rolling is more realistic for practitioner methods.

**Rationale:**  
[Bayesian] [Experimental] 36 months gives a reasonable covariance estimate for 15–25 assets, and 12-month test windows yield multiple independent folds. Twelve-month steps give non-overlapping test periods.

**Reversibility:** Moderate  
**Revisit trigger:** If folds are too few or the results are dominated by one fold, revisit window lengths. Log the change.

---

### DEC-20261014-008

**Date:** 2026-10-14  
**Type:** PROTOCOL  
**Status:** ACTIVE  
**Authority:** Owner  
**Related docs:** [`success_metrics_and_evaluation_protocol.md`](success_metrics_and_evaluation_protocol.md), [`falsification_and_kill_criteria.md`](falsification_and_kill_criteria.md)  

**Context:**  
Multiple testing in portfolio research is severe. A method that looks significant without adjustment may be noise.

**Decision:**  
Deflated Sharpe ratio (Bailey & López de Prado, 2014) is the primary multiple-testing adjustment. Probabilistic Sharpe is reported alongside. Family-wise FDR control at q = 0.10 is applied within hypothesis families.

**Alternatives considered:**  
- Bonferroni — rejected: too conservative for a family of highly correlated trials.  
- No adjustment — rejected: unacceptable in a project that explicitly critiques overfitting.  
- Only probabilistic Sharpe — rejected: does not account for the number of trials.

**Rationale:**  
[Bayesian] [Experimental] Deflated Sharpe accounts for trial count, sample length, and non-normality. It is the standard in this domain.

**Reversibility:** Hard (protocol)  
**Revisit trigger:** None without a decision log entry justifying the change before, not after, results.

---

### DEC-20261014-009

**Date:** 2026-10-14  
**Type:** COST  
**Status:** ACTIVE  
**Authority:** Owner  
**Related docs:** [`cost_model_and_frictions.md`](cost_model_and_frictions.md)  

**Context:**  
Net-of-cost results depend on the assumed cost per trade. The project needs a primary cost assumption.

**Decision:**  
Baseline κ = 10 bps one-way per trade. Sensitivity evaluated at 0, 5, 10, 20, 50 bps.

**Alternatives considered:**  
- 5 bps — rejected: too optimistic for mixed ETF universe including less liquid categories.  
- 20 bps — rejected: too pessimistic for liquid large-cap ETFs; would overstate cost drag.  
- 10 bps with sensitivity band — chosen: conservative, defensible, and stress-tested.

**Rationale:**  
[Expected Value] [Systems] 10 bps is a reasonable mid-point for liquid ETFs, and the sensitivity band makes claims robust to the assumption rather than dependent on it.

**Reversibility:** Moderate  
**Revisit trigger:** If broker/venue actual costs become known and differ materially, revisit.

---

### DEC-20261014-010

**Date:** 2026-10-14  
**Type:** BASELINE  
**Status:** ACTIVE  
**Authority:** Owner  
**Related docs:** [`benchmark_and_baseline_spec.md`](benchmark_and_baseline_spec.md)  

**Context:**  
The comparison set determines what "beats baselines" means. Weak or cherry-picked baselines produce meaningless success.

**Decision:**  
Baseline set is B1 (1/N), B2 (risk parity), B3 (sample MVO), B4 (min variance), B5 (turnover-penalized MVO, L1).

**Alternatives considered:**  
- B1–B3 only — rejected: omits risk-based competitors (B2, B4) and the strong robust simple baseline (B5).  
- Add Black-Litterman as baseline — rejected: it is a robust method candidate, not a baseline; belongs in method set.  
- Add HRP as baseline — rejected: same reason; extension candidate.

**Rationale:**  
[First Principles] [Inversion] B1, B3, B4 cover the historical spectrum. B2 and B5 ensure that any robust method must beat genuinely strong, simple alternatives, not only the critique target.

**Reversibility:** Moderate  
**Revisit trigger:** If R1 tool scan reveals a standard baseline missing from the set, add it via amendment before Phase 3.

---

### DEC-20261014-011

**Date:** 2026-10-14  
**Type:** SCOPE  
**Status:** ACTIVE  
**Authority:** Owner  
**Related docs:** [`scope_and_non_goals.md`](scope_and_non_goals.md)  

**Context:**  
The MVP universe determines estimation error magnitude, covariance conditioning, and realism of results.

**Decision:**  
MVP universe is 15–25 liquid US-listed ETFs spanning equity, fixed income, commodities, and real estate, with at least 5 years of history at backtest start.

**Alternatives considered:**  
- 5–10 ETFs — rejected: too small for covariance estimation to be interesting; MVO looks artificially stable.  
- 50+ ETFs — rejected: estimation error dominates in unrealistic ways; too close to the "dimensionality curse" failure mode the project critiques.  
- Multi-country ETFs — rejected: introduces FX and timezone complexity; out of scope.

**Rationale:**  
[First Principles] [Systems] 15–25 assets is the sweet spot where sample covariance is meaningfully noisy but not hopeless, and where MVO's instability is genuinely observable.

**Reversibility:** Moderate  
**Revisit trigger:** If Phase 1 shows MVO is not unstable at this universe size, revisit. That would falsify H1.1 and require a pivot.

---

## 6. How This Log Feeds Other Documents

| Document | Uses the log for |
|----------|-----------------|
| `project_charter.md` | Amendments to mission, scope, phase gates |
| `success_metrics_and_evaluation_protocol.md` | Any change to metrics or thresholds |
| `falsification_and_kill_criteria.md` | Every kill, pivot, stop, and materialized trigger |
| `data_contract_and_point_in_time_policy.md` | Any change to data sources or point-in-time rules |
| `cost_model_and_frictions.md` | Any change to κ, execution, or cost model |
| `benchmark_and_baseline_spec.md` | Addition or removal of baselines |
| `experiment_registry_and_preregistration.md` | Amendments to pre-registered experiments; denominator changes |
| `risk_register_and_premortem.md` | Materialized risks and their responses |
| `scope_and_non_goals.md` | Extension entry, MVP promotions/demotions, charter amendments |

Any of the above documents can link to `DEC-YYYYMMDD-NNN` for the reasoning behind a specific choice.

---

## 7. Model Tags Applied

- **[Information Theory]** — Compressed decision-making to a stable format and consistent IDs; eliminated narrative sprawl.
- **[Learning Loop]** — Every closed decision becomes an opportunity to update priors; the log is the memory of the project.
- **[Inversion]** — Pre-mortem field for larger decisions asks "how could this fail?" before the decision is acted on.
- **[Systems]** — Append-only structure, cross-references, status field, index regeneration.
- **[Bayesian]** — Optional expected value assessment and revisit triggers update beliefs when evidence arrives.

---

## 8. Owner Action Checklist Before Use

- [ ] Confirm or amend the seed entries in §5.
- [ ] Confirm the entry format in §2 is usable for your workflow.
- [ ] Confirm the rules in §3 are acceptable.
- [ ] Add this file to the README index and status board.
- [ ] Link to this file from every Tier 0 document that references "the decision log."

Once confirmed, bump to Version 1.1, keep Status `Active`, and add a revision history row.

---

## 9. Revision History

| Date | Version | Change | Author |
|------|---------|--------|--------|
| 2026-10-14 | 1.0 | Initial decision log with seed entries derived from Tier 0 documents | Ken Ira Lacson Talingting |

---

*This log exists so that the project can remember why it is the way it is. A decision not logged is a decision waiting to be silently reversed.*
