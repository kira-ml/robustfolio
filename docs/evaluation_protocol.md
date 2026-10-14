# Evaluation Protocol: robustfolio

**Version:** 2.0
**Status:** Draft — pending owner confirmation of proposed thresholds; freeze before first experiment
**Owner:** Ken Ira Lacson Talingting
**Created:** 2026-10-14 (as `success_metrics_and_evaluation_protocol.md`)
**Last Updated:** 2026-10-15
**Supersedes:** `success_metrics_and_evaluation_protocol.md` v1.1 and `falsification_and_kill_criteria.md` v1.1 (merged per execution TODO item B1)
**Related:** [`problem_framing.md`](problem_framing.md), [`project_charter.md`](project_charter.md), [`scope_and_non_goals.md`](scope_and_non_goals.md), [`data_contract_and_point_in_time_policy.md`](data_contract_and_point_in_time_policy.md), [`cost_model_and_frictions.md`](cost_model_and_frictions.md), [`benchmark_and_baseline_spec.md`](benchmark_and_baseline_spec.md), [`experiment_registry_and_preregistration.md`](experiment_registry_and_preregistration.md), [`risk_register_and_premortem.md`](risk_register_and_premortem.md)

---

## 0. Purpose of This Document

This document defines, **before any experiment is run**:

1. Exactly how success and failure will be measured.
2. What claims the project makes and how each could be falsified.
3. What evidence triggers a kill, pivot, or stop-and-report.
4. How multiple-testing adjustment and uncertainty are handled.
5. How goalpost-moving, sunk-cost continuation, and complexity-creep-as-rescue are prevented.

This is the project's **evaluation and enforcement contract**. It absorbs the content that previously lived in two separate documents. The charter establishes authority and the taxonomy of decisions (see [`project_charter.md`](project_charter.md) §7); this document establishes the measurement instrument and the decision rules that fire when measurement returns a verdict.

**Once frozen, this document may not be modified after seeing experimental results.** Any modification requires a decision log entry and a version bump, and the modification must be justified by a pre-existing protocol flaw, not by an inconvenient result.

---

## 1. Evaluation Philosophy

Six principles govern every measurement decision in this project.

1. **Net-of-cost, out-of-sample, multiple-testing-aware.** Gross Sharpe, in-sample Sharpe, and unadjusted p-values are diagnostic only. They are never the basis for a success claim.
2. **Pre-registration before execution.** Every experiment is registered with its hypothesis, parameters, metrics, and decision rule before it runs.
3. **Report the full distribution, not the point estimate.** Confidence intervals, sensitivity bands, and failure modes are reported alongside every headline number.
4. **Every claim must have a test that could prove it wrong.** If no such test exists, the claim is not part of the project's scientific content and may not be reported as a finding.
5. **Failure to falsify is not proof.** A method that survives its tests is "not yet falsified," not "correct." Reporting language must reflect this.
6. **Negative results are first-class outputs.** A falsified hypothesis is a successful experiment. A project that ends with a clean negative result has succeeded by its own definition (see [`project_charter.md`](project_charter.md) §1).

A result that is statistically significant but economically trivial is not success.
A result that is economically large but statistically fragile is not success.
Success requires both, under the frozen protocol, after costs and multiple-testing adjustment.

Every hypothesis in §7 has the form: *"Under protocol P, method M beats baseline B on metric m by at least δ."* The corresponding falsification is: *"Under protocol P, M does not beat B on m by δ, after adjustment."*

---

## 2. Primary Metric

**Primary metric:** Net-of-cost out-of-sample Sharpe ratio (annualized).

**Definition:**

\[
\text{Net Sharpe} = \frac{\mathbb{E}[R_{\text{net}}] - R_f}{\sigma(R_{\text{net}})} \cdot \sqrt{12}
\]

where \( R_{\text{net}} = R_{\text{gross}} - c(\Delta w) \) is the monthly net return after transaction costs, \( R_f \) is the risk-free rate, and \( \sigma \) is the standard deviation of monthly net returns.

**Why this metric:** It is the standard risk-adjusted return measure, directly comparable to published benchmarks, and sensitive to both return degradation and volatility increase. It penalizes cost drag through the numerator.

**Known limitations:** Sharpe ratio is sensitive to non-normality, autocorrelation, and the choice of sample period. It is not a complete description of performance. This is why secondary metrics exist.

**Decision use:** The primary metric is the *only* metric allowed to determine whether a robust method beats a baseline. All other metrics are diagnostic or constraint-checking.

---

## 3. Secondary Metrics

These are reported for every method. None of them alone determines success, but together they establish whether the primary metric result is credible.

| Metric | Definition | Purpose | Constraint |
|--------|-----------|---------|------------|
| **Annualized turnover** | Sum of absolute weight changes per year, one-way | Cost driver and capacity constraint | Must be reported; no hard cap, but see §6.2 |
| **Maximum drawdown** | Largest peak-to-trough decline in cumulative net return | Tail risk | Must be reported |
| **CVaR (95%)** | Expected shortfall in worst 5% of months | Tail risk | Must be reported |
| **Cost drag** | Annualized gross Sharpe minus annualized net Sharpe | Direct measure of friction impact | Must be reported |
| **Calibration** | Coverage of 90% confidence intervals for returns and volatility | Model honesty | Target: 80–100% empirical coverage |
| **Deflated Sharpe ratio** | Sharpe adjusted for multiple testing | Overfitting defense | Used for significance test |
| **Probabilistic Sharpe ratio** | Probability that true Sharpe exceeds a benchmark | Significance test | Reported alongside deflated Sharpe |
| **Skewness and kurtosis** | Higher moments of net return distribution | Non-normality diagnostic | Must be reported |
| **Autocorrelation (lag 1)** | Serial correlation of monthly net returns | Smoothing / staleness diagnostic | Must be reported |

---

## 4. Baselines

The primary metric is always reported relative to baselines, not in isolation. Baselines are defined in [`benchmark_and_baseline_spec.md`](benchmark_and_baseline_spec.md). At minimum:

| # | Baseline | Rationale |
|---|----------|-----------|
| B1 | 1/N equal weight | Strongest simple prior; DeMiguel et al. (2009) |
| B2 | Risk parity | Robust to return errors; common practitioner default |
| B3 | Sample mean-variance optimization | The method being critiqued |
| B4 | Minimum variance | Robust to return errors |
| B5 | Turnover-penalized MVO (L1) | The simplest turnover-aware robust method |

**A robust method must be compared against all five baselines** in every experiment that claims improvement.

---

## 5. Evaluation Protocol

### 5.1 Data splits

| Split | Purpose | Rule |
|-------|---------|------|
| **Training** | Estimate parameters | Ends strictly before test period; point-in-time |
| **Validation** | Select hyperparameters, if any | Purged and embargoed; never overlapping test |
| **Test** | Evaluate final method | Never used for any selection decision |

### 5.2 Walk-forward

- **Procedure:** Rolling or expanding estimation window; fixed test window; step forward in time; repeat.
- **Estimation window:** `[PROPOSED: 36 months rolling]`. Owner to confirm.
- **Test window:** `[PROPOSED: 12 months]`. Owner to confirm.
- **Step size:** `[PROPOSED: 12 months]`. Owner to confirm.
- **Rebalance frequency:** Monthly (baseline).
- **No overlap** between training and test returns.

### 5.3 Purged cross-validation and embargo

- For any hyperparameter selection, use purged k-fold CV with an embargo between training and test folds.
- **Purge:** Remove training observations whose label window overlaps the test window.
- **Embargo:** `[PROPOSED: 1 month]` gap between training and test. Owner to confirm.
- Reference: López de Prado (2018), *Advances in Financial Machine Learning*, Ch. 7.

### 5.4 Point-in-time discipline

- All estimates at time \( t \) use only information available at or before \( t \).
- No survivorship bias: include delisted securities as they existed.
- No lookahead in corporate actions, index membership, or pricing.
- Any violation invalidates the experiment. See [`data_contract_and_point_in_time_policy.md`](data_contract_and_point_in_time_policy.md).

### 5.5 Cost sensitivity (moved)

Cost levels, the primary cost assumption, and sensitivity bands are defined authoritatively in:

> [`cost_model_and_frictions.md`](cost_model_and_frictions.md) §3.3

They are not duplicated here. Every method is evaluated at all cost levels defined in that document. The primary metric is reported at the baseline cost level defined there (currently 10 bps). A robust method is one whose advantage survives across cost levels.

---

## 6. Materiality and Decision Thresholds

> **Note:** The following thresholds are **proposed conservative defaults**. They define what "materially better" means. The owner must confirm or replace them before freezing this document.

### 6.1 Statistical significance

A robust method is statistically significant if:

- **Deflated Sharpe ratio p-value < 0.05** *(proposed)*, AND
- **Probabilistic Sharpe ratio > 0.95** *(proposed)* against the best baseline.

### 6.2 Economic materiality

A robust method is economically material if:

- **Net Sharpe improvement over best baseline ≥ 0.20** *(proposed)* at the baseline cost level, AND
- **Turnover is not more than 2× the best baseline's turnover** *(proposed)*, AND
- **Maximum drawdown is not worse than the best baseline's drawdown by more than 5 percentage points** *(proposed)*.

### 6.3 Robustness

A robust method is robust if:

- Its advantage over the best baseline holds at **≥ 3 of the cost levels defined in [`cost_model_and_frictions.md`](cost_model_and_frictions.md) §3.3**, AND
- Its advantage holds in **≥ 60% of walk-forward folds** *(proposed)*, AND
- No single fold accounts for more than 40% of the total advantage *(proposed)*.

### 6.4 Success definition

A method is **successful** if it satisfies **all** of:

1. Statistical significance (§6.1), AND
2. Economic materiality (§6.2), AND
3. Robustness (§6.3), AND
4. No violation of point-in-time discipline or cost model.

**Partial success** is defined as satisfying 1 and 2 but failing 3, or vice versa. Partial success is reported as such, not as success.

**Failure** is defined as failing 1 or 2, or having a violation in 4.

---

## 7. Hypotheses and Falsification Tests

Hypotheses are grouped by family. Each family shares a multiple-testing correction (see §12).

### Family H1 — Estimation error is the binding constraint

| ID | Hypothesis | Falsification test | Kill/pivot on falsification |
|----|-----------|-------------------|------------------------------|
| H1.1 | Sample MVO produces extreme weights relative to 1/N | Max absolute weight > `[PROPOSED: 0.40]` in ≥ 1 fold | If not, the framing premise is weak; document and re-evaluate problem |
| H1.2 | Sample MVO has higher turnover than 1/N | Annualized turnover ratio > `[PROPOSED: 2.0]` | If not, turnover is not the problem; revisit |
| H1.3 | Estimation error, not optimization, drives instability | Shrinkage covariance reduces weight dispersion vs sample covariance | If not, revisit root-cause model in [`problem_framing.md`](problem_framing.md) §5 |

**Family kill trigger:** If H1.1 and H1.2 both fail on the primary dataset, the problem framing is falsified. Pivot or stop before Phase 2. See §8 K2.

### Family H2 — Robust methods improve net performance

| ID | Hypothesis | Falsification test | Kill/pivot on falsification |
|----|-----------|-------------------|------------------------------|
| H2.1 | Shrinkage covariance beats sample covariance on net Sharpe | §6 success criteria met | If not, drop shrinkage from the claim set |
| H2.2 | Bayesian expected returns beat historical mean on net Sharpe | Same criteria | If not, drop Bayesian returns |
| H2.3 | Turnover penalty improves net Sharpe vs unpenalized MVO | Same criteria | If not, drop turnover penalty |
| H2.4 | At least one robust method beats the best baseline on net Sharpe | Same criteria | **Project-level trigger — see §8 K1** |

**Family kill trigger:** If H2.1–H2.3 all fail, the project's method claims are falsified. Pivot to diagnostic tool or stop-and-report.

### Family H3 — Improvements are robust, not artifacts

| ID | Hypothesis | Falsification test | Kill/pivot on falsification |
|----|-----------|-------------------|------------------------------|
| H3.1 | Improvement survives at 3+ cost levels | §6.3 | If not, downgrade claim to "cost-level-specific" |
| H3.2 | Improvement survives in 60%+ of walk-forward folds | Same | If not, claim is not robust; report as fragile |
| H3.3 | Improvement survives multiple-testing adjustment | Deflated Sharpe p-value | If not, claim is not statistically defensible; report as exploratory |

**Family kill trigger:** If H3.3 fails for all methods, the project cannot claim method superiority. Pivot to diagnostic benchmark.

### Family H4 — The gap hypothesis is real

| ID | Hypothesis | Falsification test | Kill/pivot on falsification |
|----|-----------|-------------------|------------------------------|
| H4.1 | No open-source tool reproduces this exact comparison | R1 tool scan identifies no equivalent | If equivalent exists, pivot to replication or extension |
| H4.2 | Published work does not already answer the question | R1 literature scan | If answered, pivot to replication or extension |

**Family kill trigger:** If H4.1 or H4.2 fails, the gap hypothesis is falsified. Update [`problem_framing.md`](problem_framing.md) §4.1 and pivot. See §8 K3.

---

## 8. Project-Level Kill Triggers

These are the conditions under which the project as a whole must decide to kill, pivot, or stop-and-report. Each is a **hard trigger**: the decision cannot be deferred. The taxonomy and authority (Kill, Pivot, Stop-and-report, Continue) are defined in [`project_charter.md`](project_charter.md) §7.

### K1 — Primary objective falsified

**Trigger:** After Phase 3 evaluation, no robust method satisfies §6.4 (statistical significance + economic materiality + robustness).

**Decision:** Stop-and-report. The project's primary hypothesis is falsified.

**Not permitted:** Adding new methods, relaxing thresholds, or extending the evaluation to find a positive result.

**Rationale:** The charter §7 Hard Rule 2 already says this. This section makes it enforceable.

### K2 — Problem framing falsified

**Trigger:** H1.1 and H1.2 both fail on the primary dataset, before Phase 2.

**Decision:** Kill or pivot to a diagnostic-benchmark framing.

**Not permitted:** Proceeding to Phase 2 on the assumption that "the problem must be real."

### K3 — Gap hypothesis falsified

**Trigger:** R1 identifies an existing tool or paper that reproduces the planned comparison with equivalent rigor.

**Decision:** Kill or pivot to replication or extension.

**Not permitted:** Proceeding to build a less rigorous version of something that exists.

### K4 — Time budget exhausted

**Trigger:** Total time budget from [`project_charter.md`](project_charter.md) §9 is reached, regardless of where the project is.

**Decision:** Stop-and-report with whatever is complete. If results are not yet available, report as "incomplete — no conclusion."

**Not permitted:** Silent time-box extension. Any extension requires a charter amendment with decision log entry.

### K5 — Phase time-box exhausted without gate pass

**Trigger:** Any phase exceeds its time-box from [`project_charter.md`](project_charter.md) §9 without passing its gate.

**Decision:** Kill the phase or pivot the phase goal. Do not roll over into the next phase.

**Not permitted:** Continuing into the next phase "in parallel" or "just to keep momentum."

### K6 — Data or cost contract broken

**Trigger:** Any experiment in Phase 1 or later reveals a violation of [`data_contract_and_point_in_time_policy.md`](data_contract_and_point_in_time_policy.md) or [`cost_model_and_frictions.md`](cost_model_and_frictions.md) that cannot be corrected without invalidating prior results.

**Decision:** Halt evaluation. Fix the contract. Re-run affected experiments or kill.

**Not permitted:** Reporting results from invalidated experiments as findings.

### K7 — Cumulative invalidation

**Trigger:** `[PROPOSED: 3]` or more experiments in the same family are invalidated for protocol reasons.

**Decision:** Kill the family. If the invalidations span families, kill the project.

**Rationale:** Repeated invalidation signals the protocol itself is not workable, not that the methods are failing.

---

## 9. Sunk Cost Firewall

The most likely failure mode of this project is not a bad method. It is **continuing past the evidence out of sunk cost**.

Rules to prevent it:

1. **Time budgets are hard stops.** Once a phase time-box is exhausted, no work in that phase continues. A decision log entry is required to move on.
2. **No work in a new phase while a gate is unresolved.** Parallel progress is scope creep.
3. **Effort already spent is never a reason to continue.** Only evidence of future value is.
4. **A kill decision is free.** The owner can kill at any time. The project's identity does not depend on finishing.
5. **"Almost there" is not evidence.** If the last experiment failed the success criteria, the next experiment needs a fresh pre-registered hypothesis.

**Anti-pattern to flag:** The owner saying "let me just try one more thing" after a failed gate. This is the sunk-cost failure mode. The reasoning partner must flag it.

**Hard rule:** A pivot is not a rescue. A pivot must be justified by a falsified hypothesis, not by an inconvenient result. If the pivot looks like "add another method to fix the last failure," it is scope creep wearing a pivot costume.

---

## 10. Pivot Criteria

A pivot is permitted only under the following conditions. Every pivot requires a decision log entry with a version bump.

| Pivot | Trigger | New framing | Requires |
|-------|---------|-------------|----------|
| Diagnostic benchmark | K1 or H3.3 fails for all methods | Deliver the framework and negative result as the contribution | Update `problem_framing.md`, `project_charter.md` |
| Replication study | K3 | Reproduce an existing result to validate the framework | Update scope and this protocol |
| Narrower method scope | H2.x fails for a specific method | Drop that method; keep the family | Update baseline list in this protocol |
| Narrower universe | H1.x fails on one asset class but holds on another | Restrict to the asset class where the effect is real | Update data contract |
| Shorter horizon | Long-horizon results are unstable | Restrict claim to monthly rebalancing only | Update this protocol |

**Forbidden pivots:**

- "Add more data" to rescue a failed result.
- "Try a different metric" to find significance.
- "Extend the test window" to accumulate more evidence of the same period.
- "Add another method" without a pre-registered hypothesis and a fresh experiment entry.

---

## 11. Stop-and-Report Criteria

Stop-and-report is the correct decision when:

1. K1 fires (primary objective falsified), OR
2. The project reaches its total time budget without a positive result, OR
3. The owner elects to stop for any reason (per [`project_charter.md`](project_charter.md) §7 Hard Rule 4), OR
4. Two or more pivot attempts have failed.

**Stop-and-report deliverable:**

- A written conclusion: positive, negative, or mixed, with explicit language about what was and was not tested.
- All Tier 0 documentation in its final state.
- The full experiment registry, including failed and invalidated experiments.
- The decision log documenting the stop.
- Reproducible code and data acquisition instructions.

**Stop-and-report is not failure.** It is the correct outcome when the evidence does not support the claim. It is reported with the same care as a positive result.

---

## 12. Multiple Testing Adjustment

Every experiment is logged in [`experiment_registry_and_preregistration.md`](experiment_registry_and_preregistration.md). The number of registered trials is the multiple-testing denominator.

### 12.1 Deflated Sharpe Ratio

Deflated Sharpe adjusts for:

- Number of trials \( N \).
- Non-normality of returns (skewness, kurtosis).
- Length of the sample.
- Variance of the Sharpe estimates across trials.

Reference: Bailey & López de Prado (2014).

### 12.2 Pre-registration rules

- Every hypothesis, parameter set, and metric is registered **before** execution.
- Post-hoc metric changes invalidate the trial for the purposes of success claims.
- Exploratory analyses are allowed and reported separately as "exploratory, not confirmatory."

### 12.3 Family-wise error control

- Trials are grouped by hypothesis family (H1–H4 in §7).
- Within a family, apply Benjamini-Hochberg FDR control at `[PROPOSED: q = 0.10]`. Owner to confirm.
- Report both raw and adjusted p-values.

---

## 13. Confidence Intervals and Estimation

All headline metrics are reported with uncertainty quantification.

### 13.1 Method

- **Bootstrap:** Stationary block bootstrap for Sharpe, turnover, and drawdown confidence intervals.
- **Block length:** `[PROPOSED: 6 months]`. Owner to confirm.
- **Replications:** `[PROPOSED: 2000]`. Owner to confirm.
- **Confidence level:** 90% for reporting; 95% for decision thresholds.

### 13.2 Why block bootstrap

Monthly portfolio returns exhibit autocorrelation and volatility clustering. IID bootstrap understates uncertainty. Block bootstrap preserves local dependence structure.

---

## 14. Reporting Requirements

Every experiment result is reported in a standard format. See [`results_reporting_and_claims_policy.md`](results_reporting_and_claims_policy.md) for the full template (to be written before Phase 4).

### 14.1 Mandatory disclosures

Every result must report:

1. Gross and net Sharpe at every cost level defined in [`cost_model_and_frictions.md`](cost_model_and_frictions.md) §3.3.
2. In-sample and out-of-sample metrics, clearly labeled.
3. Turnover, drawdown, CVaR, cost drag.
4. Deflated Sharpe and probabilistic Sharpe.
5. Confidence intervals for all headline metrics.
6. Number of trials in the family, and the adjustment applied.
7. Data period, universe, and any exclusions.
8. Any protocol deviations, with justification.
9. Limitations and known failure modes.

### 14.2 Forbidden claims

The following are never allowed without explicit qualification:

- "Beats the market" or any absolute return claim.
- Any claim based on gross Sharpe.
- Any claim based on in-sample performance.
- Any claim based on unadjusted p-values.
- Any claim of superiority without confidence intervals.
- Any claim based on a single walk-forward fold or a single cost level.

### 14.3 Decision process when a trigger fires

When a trigger from §8 fires, follow this sequence:

1. **Recognize.** The trigger is identified by the owner or the reasoning partner.
2. **Log the trigger.** Add an entry to `decision_log.md` with: date, trigger, evidence, options considered.
3. **Evaluate options.** Kill, pivot, stop-and-report, or continue — with explicit expected value reasoning.
4. **Decide.** The owner decides. No decision is a decision to continue, which must be logged.
5. **Act.** Update affected documents. Bump versions. Notify informed parties.
6. **Update priors.** Record what was learned in `decision_log.md` and, if relevant, in [`problem_framing.md`](problem_framing.md) or this protocol.

**Time-box for decisions:** `[PROPOSED: 1 week]` from trigger recognition to decision. Beyond this, the project is drifting.

---

## 15. What Would Invalidate a Result

A result is invalidated (not merely weakened) if any of the following occurred:

- Lookahead bias in data or estimation.
- Survivorship bias in universe construction.
- Post-hoc metric or threshold changes.
- Undisclosed trials contributing to multiple-testing inflation.
- Cost model inconsistent with [`cost_model_and_frictions.md`](cost_model_and_frictions.md).
- Point-in-time violation in corporate actions, pricing, or index membership.
- Test period overlap with training period beyond the allowed embargo.
- An experiment ran before its registration was complete.
- The decision rule was changed after seeing results.

Invalidated results are documented, not deleted. They inform the learning loop.

---

## 16. Protocol Freeze Rules

Once this document is `Frozen`:

1. Metrics cannot be added, removed, or redefined to change the outcome.
2. Thresholds in §§6, 7, 12, and 13 cannot be relaxed.
3. Cost levels defined in [`cost_model_and_frictions.md`](cost_model_and_frictions.md) §3.3 cannot be changed without amending that document, which in turn requires the same discipline.
4. A change is permitted only if:
   - A protocol flaw is discovered **before** seeing results, AND
   - The change is documented in the decision log with rationale, AND
   - The version is bumped, AND
   - Affected experiments are re-run and re-registered.
5. Any change made **after** seeing results requires a full decision log entry explaining why the change is not goalpost-moving. The owner must be able to defend this to a skeptical external reviewer.

**Conflict resolution with other documents:**

| Conflict | Resolution |
|----------|------------|
| Charter vs this document (taxonomy, authority) | The charter owns the decision taxonomy and authority ([`project_charter.md`](project_charter.md) §7–8). |
| Charter vs this document (thresholds, triggers) | This document owns thresholds and triggers. If they conflict on a trigger, this document wins until amended. |
| Problem framing vs this document | This document may falsify the problem framing. When it does, [`problem_framing.md`](problem_framing.md) must be updated. |
| Scope vs this document | [`scope_and_non_goals.md`](scope_and_non_goals.md) owns scope. Pivots that change scope (§10) require a scope amendment, not just a decision log entry. |
| Cost model vs this document | [`cost_model_and_frictions.md`](cost_model_and_frictions.md) owns cost levels. This document references them. |
| Owner intuition vs this document | This document wins until amended via decision log. |

---

## 17. Model Tags Applied

- **[First Principles]** — Reduced success to a single primary metric with supporting diagnostics.
- **[Experimental]** — Pre-registration, walk-forward, purged CV, embargo, falsification.
- **[Bayesian]** — Confidence intervals, probabilistic Sharpe, calibration, priors revisited after each trigger.
- **[Inversion]** — Invalidation rules (§15), forbidden claims (§14.2), freeze rules (§16), sunk-cost firewall (§9).
- **[Systems]** — Cost sensitivity bands, multiple-testing family control, trigger-response cadence.
- **[Expected Value]** — Materiality thresholds define economically meaningful improvement; sunk-cost firewall; kill is free.
- **[Information Theory]** — Compressed to decisions, thresholds, and rules; no filler.
- **[Learning Loop]** — Every trigger logged; priors updated; pivot history preserved.

---

## 18. Owner Action Checklist Before Freezing

Before setting Status to `Frozen`, confirm or replace every `[PROPOSED]` value:

**Measurement protocol:**

- [ ] §5.2: estimation window, test window, step size
- [ ] §5.3: embargo length
- [ ] §6.1: significance thresholds
- [ ] §6.2: materiality thresholds
- [ ] §6.3: robustness thresholds
- [ ] §12.3: FDR level
- [ ] §13.1: block length, replications

**Falsification and triggers:**

- [ ] §7 H1.1: extreme-weight threshold
- [ ] §7 H1.2: turnover ratio threshold
- [ ] §8 K7: cumulative invalidation count
- [ ] §14.3: decision time-box

**Cross-document consistency:**

- [ ] §8 triggers are consistent with your charter time-boxes ([`project_charter.md`](project_charter.md) §9)
- [ ] §10 forbidden pivots are acceptable to you
- [ ] §9 sunk cost firewall rules are acceptable
- [ ] §14.3 decision authority matches [`project_charter.md`](project_charter.md) §8
- [ ] §16 conflict resolution is consistent with the charter's own conflict rule
- [ ] Cost levels confirmed in [`cost_model_and_frictions.md`](cost_model_and_frictions.md) §11, not here

Once confirmed, bump to Version 2.1, set Status to `Frozen`, and add a revision history row.

---

## 19. Revision History

| Date | Version | Change | Author |
|------|---------|--------|--------|
| 2026-10-14 | 1.0 | Initial protocol (`success_metrics_and_evaluation_protocol.md`) | Ken Ira Lacson Talingting |
| 2026-10-14 | 1.0 | Initial falsification and kill criteria (`falsification_and_kill_criteria.md`) | Ken Ira Lacson Talingting |
| 2026-10-15 | 1.1 | Protocol: replaced §5.5 cost levels with pointer to cost model doc (A6) | Ken Ira Lacson Talingting |
| 2026-10-15 | 1.1 | Falsification: replaced §3 taxonomy with pointer to charter §7 (A5); changed "gap claim" to "gap hypothesis" | Ken Ira Lacson Talingting |
| 2026-10-15 | 2.0 | Merged the two documents into a single `evaluation_protocol.md` (B1). Structure: metrics (§§2–4) → protocol (§5) → thresholds (§6) → hypotheses (§7) → triggers (§8) → firewalls (§§9–11) → adjustment and uncertainty (§§12–13) → reporting and invalidation (§§14–15) → freeze rules (§16). Consolidated the two owner checklists into one (§18) and the two revision histories into one (§19). | Ken Ira Lacson Talingting |

---

*This protocol governs what counts as success and when the project stops. It must be frozen before experiments and defended against erosion. If it is not enforced, the project is not falsificationist.*
