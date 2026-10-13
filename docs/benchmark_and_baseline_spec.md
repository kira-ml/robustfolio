# Benchmark and Baseline Specification: robustfolio

**Version:** 1.0  
**Status:** Draft — pending owner confirmation of proposed defaults; freeze before method comparison  
**Owner:** Ken Ira Lacson Talingting  
**Created:** 2026-10-14  
**Last Updated:** 2026-10-14  
**Supersedes:** None  
**Related:** [`problem_framing.md`](problem_framing.md), [`project_charter.md`](project_charter.md), [`success_metrics_and_evaluation_protocol.md`](success_metrics_and_evaluation_protocol.md), [`falsification_and_kill_criteria.md`](falsification_and_kill_criteria.md), [`data_contract_and_point_in_time_policy.md`](data_contract_and_point_in_time_policy.md), [`cost_model_and_frictions.md`](cost_model_and_frictions.md), [`model_and_method_spec.md`](model_and_method_spec.md)

---

## 0. Purpose of This Document

This document defines **exactly which baselines are used, how each is computed, and what behavior is expected from each**.

Its purpose is to:

1. Fix the competitor set before any robust method is implemented.
2. Specify each baseline mathematically so it is reproducible without ambiguity.
3. Pre-register expected behavior so results can be interpreted against priors.
4. Prevent the failure mode of using weak baselines to manufacture success.
5. Prevent the failure mode of using unreproducible baselines that no third party can verify.

It is the **contract** between "a robust method wins" and "a robust method wins against a fair comparison set." A result that beats a weak or biased baseline is not a result.

**Once frozen, this document may not be modified after seeing experimental results.** Adding or weakening baselines after results is a form of goalpost-moving.

---

## 1. Baseline Philosophy

Three principles govern baseline selection and implementation.

1. **Baselines are the null hypothesis.** A robust method is only interesting if it beats the strongest, simplest, fairest null. Weak baselines are a form of self-deception.
2. **Simple beats sophisticated.** If a complex method cannot beat 1/N, the complexity is not justified. This is the base rate from DeMiguel, Garlappi, & Uppal (2009).
3. **Reproducible without ambiguity.** Any researcher with the same data and cost model must be able to regenerate the baseline results. No magic constants, no undocumented choices.

A robust method that beats sample MVO but loses to 1/N has not solved the problem. A robust method that beats 1/N net of costs, after multiple-testing adjustment, has.

---

## 2. Baseline Set

The MVP baseline set is fixed. Each baseline must be implemented, tested, and reported in every method comparison.

| ID | Baseline | Family | Uses expected returns? | Rationale |
|----|----------|--------|----------------------|-----------|
| **B1** | Equal weight (1/N) | Naive | No | Strongest simple prior (DeMiguel et al., 2009) |
| **B2** | Risk parity (equal risk contribution) | Risk-based | No | Practitioner default; robust to return error |
| **B3** | Sample mean-variance optimization | Classical | Yes | The method being critiqued |
| **B4** | Minimum variance | Risk-based | No | Robust to return error; classical alternative |
| **B5** | Turnover-penalized MVO (L1) | Robust | Yes | Simplest turnover-aware method |

**Extensions** (not in MVP, require pre-registered experiment):

- Inverse volatility weights.
- Hierarchical risk parity (López de Prado, 2016).
- Equal risk budget with return views.
- Shrinkage covariance + minimum variance.
- Black-Litterman.

Extensions are not baselines until the owner adds them via amendment.

---

## 3. Common Definitions

All baselines share the following conventions, inherited from the other Tier 0 documents.

- **Universe:** as defined in `data_contract_and_point_in_time_policy.md` §3.
- **Rebalance frequency:** monthly (§4.1 of cost model).
- **Estimation window:** `[PROPOSED: 36 months rolling]` for B2, B3, B4, B5. B1 uses no estimation.
- **Constraints:** fully invested, long-only, no leverage.
  - \( \sum_i w_i = 1 \)
  - \( w_i \ge 0 \)
  - \( w_i \le w_{\max} \) where \( w_{\max} = \text{[PROPOSED: 0.30]} \)
- **Risk aversion:** \( \gamma = \text{[PROPOSED: 5]} \) for B3 and B5.
- **Covariance estimator:** sample covariance unless otherwise specified.
- **Expected return estimator:** sample mean (arithmetic, monthly) for B3 and B5.
- **Cost model:** proportional \( \kappa \) bps per one-way turnover, per `cost_model_and_frictions.md` §3.
- **Execution:** close of rebalance date.
- **Point-in-time:** all inputs satisfy `data_contract_and_point_in_time_policy.md` §4.

**Fair comparison rule:** All baselines must be evaluated under the same protocol. Deviations must be documented and justified in the experiment registry. Any asymmetric treatment of a baseline vs a robust method invalidates the comparison.

---

## 4. Baseline Specifications

### 4.1 B1 — Equal weight (1/N)

**Definition:**

\[
w_i = \frac{1}{N}, \quad \forall i \in U_t
\]

where \( U_t \) is the eligible universe at rebalance date \( t \).

**Inputs:** None. No estimation.

**Optimization:** None.

**Turnover:** Determined entirely by drifted weights and universe changes.

**Expected behavior (prior):**

- Low turnover relative to optimizing methods, because weights drift slowly.
- Moderate Sharpe; historically competitive with sample MVO out-of-sample (DeMiguel et al., 2009).
- No concentration in any single asset.
- Loses to risk-based methods in high-volatility regimes if the universe has mixed risk profiles.

**Role in this project:** The primary benchmark. A robust method that cannot beat 1/N net of costs has not demonstrated practical value.

**Falsification relevance:** If no robust method beats B1 net of costs, the project's primary objective (charter §3) is likely falsified (see `falsification_and_kill_criteria.md` §4 K1).

---

### 4.2 B2 — Risk parity (equal risk contribution)

**Definition:**

Solve for weights \( w \) such that each asset contributes equally to portfolio volatility:

\[
w_i \cdot (\Sigma w)_i = w_j \cdot (\Sigma w)_j, \quad \forall i, j
\]

subject to:

\[
\sum_i w_i = 1, \quad w_i \ge 0, \quad w_i \le w_{\max}
\]

**Inputs:**

- \( \Sigma \): sample covariance, `[PROPOSED: 36 months rolling]`.
- No expected returns.

**Optimization:** Convex. Solved via standard risk-budgeting algorithm (Spinu, 2013; or scipy-based iterative solver). Fallback: iterative proportional risk allocation.

**Turnover:** Driven by covariance changes and weight drift.

**Expected behavior (prior):**

- Lower volatility than 1/N when the universe mixes high- and low-vol assets.
- Similar or higher Sharpe than 1/N.
- Higher turnover than 1/N due to covariance re-estimation.
- Sensitive to covariance estimation error in high dimensions.

**Role in this project:** The strongest risk-based competitor. A robust method that cannot beat risk parity net of costs has limited practical relevance.

**Implementation note:** If the covariance matrix is near-singular, apply diagonal loading (add \( \epsilon I \) with \( \epsilon = \text{[PROPOSED: 1e-6]} \)) before solving. Document the loading in the experiment registry.

---

### 4.3 B3 — Sample mean-variance optimization (MVO)

**Definition:**

\[
\max_w \ w^\top \mu - \frac{\gamma}{2} w^\top \Sigma w
\]

subject to:

\[
\sum_i w_i = 1, \quad w_i \ge 0, \quad w_i \le w_{\max}
\]

**Inputs:**

- \( \mu \): sample mean of monthly returns over `[PROPOSED: 36 months rolling]`.
- \( \Sigma \): sample covariance over the same window.
- \( \gamma = \text{[PROPOSED: 5]} \).

**Optimization:** Quadratic program. Solved via standard QP solver. Document the solver and tolerance in the experiment registry.

**Turnover:** Typically high. Sample means change materially month to month, producing large weight changes.

**Expected behavior (prior):**

- Extreme weights: concentration in a few assets, often at the \( w_{\max} \) bound.
- High turnover, high cost drag.
- Poor net-of-cost out-of-sample Sharpe.
- Occasionally high in-sample Sharpe; this is the failure mode being critiqued.

**Role in this project:** The critique target. Demonstrating that B3 fails out-of-sample is expected and serves as a baseline sanity check, not as a novel finding.

**Caveat:** If B3 *does not* show extreme weights or high turnover on the primary dataset, the problem framing premise (`problem_framing.md` §1) is weakened. This is a Phase 1 exit criterion.

---

### 4.4 B4 — Minimum variance

**Definition:**

\[
\min_w \ w^\top \Sigma w
\]

subject to:

\[
\sum_i w_i = 1, \quad w_i \ge 0, \quad w_i \le w_{\max}
\]

**Inputs:**

- \( \Sigma \): sample covariance, `[PROPOSED: 36 months rolling]`.
- No expected returns.

**Optimization:** Quadratic program (equivalent to MVO with \( \mu = 0 \) and a normalization constraint). Solved via standard QP solver.

**Turnover:** Driven by covariance changes; lower than B3.

**Expected behavior (prior):**

- Lower realized volatility than 1/N and B3.
- Sharpe competitive with or better than B3 out-of-sample.
- Concentrated in low-volatility assets; may underweight high-return assets.
- Turnover lower than B3 but not negligible.

**Role in this project:** The classical risk-based benchmark. B4 and B2 serve as complementary risk-based comparisons: B4 minimizes variance; B2 equalizes risk contributions.

**Implementation note:** Guard against singular \( \Sigma \) with diagonal loading as in B2.

---

### 4.5 B5 — Turnover-penalized MVO (L1)

**Definition:**

\[
\max_w \ w^\top \mu - \frac{\gamma}{2} w^\top \Sigma w - \lambda \| w - w^- \|_1
\]

subject to:

\[
\sum_i w_i = 1, \quad w_i \ge 0, \quad w_i \le w_{\max}
\]

**Inputs:**

- \( \mu \), \( \Sigma \), \( \gamma \) as in B3.
- \( \lambda \): turnover penalty, `[PROPOSED: equal to baseline \( \kappa \) = 10 bps = 0.001 in monthly return units]`.
- \( w^- \): drifted weights from the previous period (see `cost_model_and_frictions.md` §4.4).

**Optimization:** Convex QP with L1 penalty. Reformulated with auxiliary variables \( u_i \ge |w_i - w_i^-| \) as a standard QP.

**Turnover:** Directly penalized. Should be materially lower than B3, at the cost of some in-sample fit.

**Expected behavior (prior):**

- Turnover significantly lower than B3.
- Net Sharpe higher than B3 at realistic costs.
- May match or exceed B4 on net Sharpe.
- Sensitive to \( \lambda \) choice.

**Role in this project:** The simplest turnover-aware method. Any robust method that does not beat B5 net of costs is not adding practical value beyond a simple penalty.

**Implementation note:** B5 is the closest thing to a robust method in the baseline set. It is deliberately included so that more sophisticated robust methods are compared against a simple, strong alternative — not just against naive MVO.

---

## 5. Expected Behavior Summary

Pre-registered priors, to be checked against Phase 1 results.

| Baseline | Expected turnover | Expected net Sharpe rank | Expected drawdown | Sensitivity to estimation error |
|----------|-------------------|--------------------------|-------------------|-------------------------------|
| B1 (1/N) | Low | Mid | Low-mid | None |
| B2 (Risk parity) | Mid | Mid-high | Low | Low-mid |
| B3 (Sample MVO) | High | Low | High | High |
| B4 (Min variance) | Mid | Mid-high | Low | Mid |
| B5 (Turnover-penalized MVO) | Low-mid | Mid-high | Mid | Mid |

These priors are testable. If Phase 1 results contradict them, update the model of the problem, not the priors.

---

## 6. Fair Comparison Rules

These rules ensure no baseline is inadvertently advantaged or disadvantaged.

1. **Same universe.** All baselines use the same eligible universe at each rebalance date.
2. **Same data.** All baselines use the same point-in-time snapshot.
3. **Same cost model.** All baselines incur costs under the same model, \( \kappa \), and execution timing.
4. **Same constraints.** Weight bounds, leverage, and long-only constraints are identical across baselines.
5. **Same evaluation.** Walk-forward folds, cost levels, and metrics are identical.
6. **Same estimation window** (where applicable). Deviations must be documented and justified.
7. **Same reporting.** Each baseline is reported with gross Sharpe, net Sharpe, turnover, drawdown, and cost drag at all cost levels.
8. **No silent parameter tuning.** Any parameter change from the frozen defaults requires a pre-registered experiment.

**Violation of any rule invalidates the comparison.** Documented in `falsification_and_kill_criteria.md` §4 K6.

---

## 7. What Invalidates a Baseline Comparison

A baseline comparison is invalidated if any of the following occurred:

- A baseline was implemented with a different cost model, universe, or constraint set than the robust method.
- A baseline's hyperparameters were tuned on test data.
- A baseline was reported only at cost levels that flattered it.
- A baseline was reported only at cost levels that flattered the robust method.
- A baseline's weights were not properly constrained (e.g., leverage or short exposure allowed).
- A baseline's covariance matrix was regularized while the robust method's was not (or vice versa) without documentation.
- A baseline was silently dropped from the comparison because of poor results.
- A baseline result was not reproducible from the frozen snapshot and code version.

Invalidated comparisons are documented and not deleted.

---

## 8. Reporting Requirements

Every baseline result must report:

1. Baseline ID and name.
2. Exact inputs used (estimation window, covariance estimator, \( \gamma \), \( \lambda \), \( w_{\max} \)).
3. Solver and convergence status.
4. Gross Sharpe, net Sharpe at each cost level, turnover, drawdown, cost drag.
5. Confidence intervals for Sharpe and turnover.
6. Any deviation from the frozen defaults, with justification.
7. Any implementation notes affecting interpretation.

See `success_metrics_and_evaluation_protocol.md` §9 and `results_reporting_and_claims_policy.md` for the full template.

---

## 9. Model Tags Applied

- **[First Principles]** — Reduced baselines to their mathematical definitions, inputs, and constraints.
- **[Inversion]** — Defined invalidation conditions and fair-comparison rules before defining success.
- **[Experimental]** — Pre-registered priors and falsifiable behavior; frozen parameters.
- **[Systems]** — Consistent constraints, cost model, and evaluation across baselines.
- **[Bayesian]** — Priors stated and testable; contradictions update the model.
- **[Information Theory]** — Compressed to definitions, rules, and expected behavior; no filler.

---

## 10. Owner Action Checklist Before Freezing

Before setting Status to `Frozen`, confirm or replace every `[PROPOSED]` value:

- [ ] Section 3: confirm estimation window (36 months) and \( w_{\max} \) (0.30)
- [ ] Section 3: confirm \( \gamma \) (5)
- [ ] Section 4.2: confirm risk parity solver and diagonal loading
- [ ] Section 4.5: confirm \( \lambda \) baseline (10 bps) and L1 formulation
- [ ] Section 2: confirm the baseline set (B1–B5) and decide if any extensions are promoted
- [ ] Section 5: confirm priors are acceptable starting beliefs

Also confirm:

- [ ] You accept that B3 is a critique target, not a competitor to "win" against.
- [ ] You accept the fair comparison rules in §6.
- [ ] You accept that B5 is a strong baseline and any robust method must beat it, not only B3.
- [ ] You are prepared to implement all five baselines and unit-test them before Phase 2.

Once confirmed, bump to Version 1.1, set Status to `Frozen`, and add a revision history row.

---

## 11. Revision History

| Date | Version | Change | Author |
|------|---------|--------|--------|
| 2026-10-14 | 1.0 | Initial benchmark and baseline specification | Ken Ira Lacson Talingting |

---

*This document exists to make "a robust method wins" a meaningful claim. A method that beats only weak baselines has beaten nothing. A method that beats strong baselines has earned the claim.*
