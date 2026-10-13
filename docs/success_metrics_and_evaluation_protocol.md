# Success Metrics and Evaluation Protocol: robustfolio

**Version:** 1.0  
**Status:** Draft — pending owner confirmation of proposed thresholds; freeze before first experiment  
**Owner:** Ken Ira Lacson Talingting  
**Created:** 2026-10-14  
**Last Updated:** 2026-10-14  
**Supersedes:** None  
**Related:** [`problem_framing.md`](problem_framing.md), [`project_charter.md`](project_charter.md), [`falsification_and_kill_criteria.md`](falsification_and_kill_criteria.md), [`data_contract_and_point_in_time_policy.md`](data_contract_and_point_in_time_policy.md), [`cost_model_and_frictions.md`](cost_model_and_frictions.md), [`benchmark_and_baseline_spec.md`](benchmark_and_baseline_spec.md), [`experiment_registry_and_preregistration.md`](experiment_registry_and_preregistration.md)

---

## 0. Purpose of This Document

This document defines **exactly how success and failure will be measured** for `robustfolio`, before any experiment is run.

Its purpose is to:

- Prevent moving goalposts after seeing results.
- Define the primary metric, secondary metrics, and their decision thresholds.
- Specify the evaluation protocol: data splits, walk-forward, purged cross-validation, embargo.
- Specify how multiple testing is adjusted.
- Specify how confidence intervals and statistical significance are computed.
- Specify what counts as "materially better" than baselines.
- Specify what must be reported, in what form, and with what caveats.

**This document does not define the problem** (see `problem_framing.md`), the project contract (see `project_charter.md`), or the kill thresholds (see `falsification_and_kill_criteria.md`). It defines the measurement instrument.

**Once frozen, this document may not be modified after seeing experimental results.** Any modification requires a decision log entry and a version bump, and the modification must be justified by a pre-existing protocol flaw, not by an inconvenient result.

---

## 1. Evaluation Philosophy

Three principles govern every measurement decision in this project:

1. **Net-of-cost, out-of-sample, multiple-testing-aware.** Gross Sharpe, in-sample Sharpe, and unadjusted p-values are diagnostic only. They are never the basis for a success claim.
2. **Pre-registration before execution.** Every experiment is registered with its hypothesis, parameters, metrics, and decision rule before it runs. See `experiment_registry_and_preregistration.md`.
3. **Report the full distribution, not the point estimate.** Confidence intervals, sensitivity bands, and failure modes are reported alongside every headline number.

A result that is statistically significant but economically trivial is not success.  
A result that is economically large but statistically fragile is not success.  
Success requires both, under the frozen protocol, after costs and multiple-testing adjustment.

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
| **Annualized turnover** | Sum of absolute weight changes per year, one-way | Cost driver and capacity constraint | Must be reported; no hard cap, but see Section 6 |
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

The primary metric is always reported relative to baselines, not in isolation. Baselines are defined in `benchmark_and_baseline_spec.md`. At minimum:

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
- Any violation invalidates the experiment. See `data_contract_and_point_in_time_policy.md`.

### 5.5 Cost sensitivity

Every method is evaluated at multiple cost levels:

| Level | Cost per trade | Purpose |
|-------|----------------|---------|
| Zero | 0 bps | Diagnostic only; not a success criterion |
| Low | 5 bps | Best-case realistic |
| Baseline | 10 bps | Primary cost assumption |
| High | 20 bps | Stress case |
| Extreme | 50 bps | Robustness boundary |

**Primary metric is reported at 10 bps.** Other levels are reported as sensitivity bands. A robust method is one whose advantage survives across cost levels.

---

## 6. Materiality and Decision Thresholds

> **Note:** The following thresholds are **proposed conservative defaults**. They define what "materially better" means. The owner must confirm or replace them before freezing this document.

### 6.1 Statistical significance

A robust method is statistically significant if:

- **Deflated Sharpe ratio p-value < 0.05** *(proposed)*, AND
- **Probabilistic Sharpe ratio > 0.95** *(proposed)* against the best baseline.

### 6.2 Economic materiality

A robust method is economically material if:

- **Net Sharpe improvement over best baseline ≥ 0.20** *(proposed)* at 10 bps, AND
- **Turnover is not more than 2× the best baseline's turnover** *(proposed)*, AND
- **Maximum drawdown is not worse than the best baseline's drawdown by more than 5 percentage points** *(proposed)*.

### 6.3 Robustness

A robust method is robust if:

- Its advantage over the best baseline holds at **≥ 3 of 5 cost levels**, AND
- Its advantage holds in **≥ 60% of walk-forward folds** *(proposed)*, AND
- No single fold accounts for more than 40% of the total advantage *(proposed)*.

### 6.4 Success definition

A method is **successful** if it satisfies **all** of:

1. Statistical significance (6.1), AND
2. Economic materiality (6.2), AND
3. Robustness (6.3), AND
4. No violation of point-in-time discipline or cost model.

**Partial success** is defined as satisfying 1 and 2 but failing 3, or vice versa. Partial success is reported as such, not as success.

**Failure** is defined as failing 1 or 2, or having a violation in 4.

---

## 7. Multiple Testing Adjustment

Every experiment is logged in `experiment_registry_and_preregistration.md`. The number of registered trials is the multiple-testing denominator.

### 7.1 Deflated Sharpe Ratio

Deflated Sharpe adjusts for:

- Number of trials \( N \).
- Non-normality of returns (skewness, kurtosis).
- Length of the sample.
- Variance of the Sharpe estimates across trials.

Reference: Bailey & López de Prado (2014).

### 7.2 Pre-registration rules

- Every hypothesis, parameter set, and metric is registered **before** execution.
- Post-hoc metric changes invalidate the trial for the purposes of success claims.
- Exploratory analyses are allowed and reported separately as "exploratory, not confirmatory."

### 7.3 Family-wise error control

- Trials are grouped by hypothesis family.
- Within a family, apply Benjamini-Hochberg FDR control at `[PROPOSED: q = 0.10]`. Owner to confirm.
- Report both raw and adjusted p-values.

---

## 8. Confidence Intervals and Estimation

All headline metrics are reported with uncertainty quantification.

### 8.1 Method

- **Bootstrap:** Stationary block bootstrap for Sharpe, turnover, and drawdown confidence intervals.
- **Block length:** `[PROPOSED: 6 months]`. Owner to confirm.
- **Replications:** `[PROPOSED: 2000]`. Owner to confirm.
- **Confidence level:** 90% for reporting; 95% for decision thresholds.

### 8.2 Why block bootstrap

Monthly portfolio returns exhibit autocorrelation and volatility clustering. IID bootstrap understates uncertainty. Block bootstrap preserves local dependence structure.

---

## 9. Reporting Requirements

Every experiment result is reported in a standard format. See `results_reporting_and_claims_policy.md` for the full template.

### 9.1 Mandatory disclosures

Every result must report:

1. Gross and net Sharpe at all 5 cost levels.
2. In-sample and out-of-sample metrics, clearly labeled.
3. Turnover, drawdown, CVaR, cost drag.
4. Deflated Sharpe and probabilistic Sharpe.
5. Confidence intervals for all headline metrics.
6. Number of trials in the family, and the adjustment applied.
7. Data period, universe, and any exclusions.
8. Any protocol deviations, with justification.
9. Limitations and known failure modes.

### 9.2 Forbidden claims

The following are never allowed without explicit qualification:

- "Beats the market" or any absolute return claim.
- Any claim based on gross Sharpe.
- Any claim based on in-sample performance.
- Any claim based on unadjusted p-values.
- Any claim of superiority without confidence intervals.
- Any claim based on a single walk-forward fold or a single cost level.

---

## 10. What Would Invalidate a Result

A result is invalidated (not merely weakened) if any of the following occurred:

- Lookahead bias in data or estimation.
- Survivorship bias in universe construction.
- Post-hoc metric or threshold changes.
- Undisclosed trials contributing to multiple-testing inflation.
- Cost model inconsistent with `cost_model_and_frictions.md`.
- Point-in-time violation in corporate actions, pricing, or index membership.
- Test period overlap with training period beyond the allowed embargo.

Invalidated results are documented, not deleted. They inform the learning loop.

---

## 11. Protocol Freeze Rules

Once this document is `Frozen`:

1. Metrics cannot be added, removed, or redefined to change the outcome.
2. Thresholds in Sections 6, 7, and 8 cannot be relaxed.
3. Cost levels in Section 5.5 cannot be changed.
4. A change is permitted only if:
   - A protocol flaw is discovered **before** seeing results, AND
   - The change is documented in the decision log with rationale, AND
   - The version is bumped, AND
   - Affected experiments are re-run and re-registered.
5. Any change made **after** seeing results requires a full decision log entry explaining why the change is not goalpost-moving. The owner must be able to defend this to a skeptical external reviewer.

---

## 12. Model Tags Applied

- **[First Principles]** — Reduced success to a single primary metric with supporting diagnostics.
- **[Experimental]** — Pre-registration, walk-forward, purged CV, embargo, falsification.
- **[Bayesian]** — Confidence intervals, probabilistic Sharpe, calibration.
- **[Inversion]** — Section 10 (invalidation), Section 9.2 (forbidden claims), Section 11 (freeze rules).
- **[Systems]** — Cost sensitivity bands, multiple-testing family control.
- **[Expected Value]** — Materiality thresholds define economically meaningful improvement.
- **[Information Theory]** — Compressed to decisions, thresholds, and rules; no filler.

---

## 13. Owner Action Checklist Before Freezing

Before setting Status to `Frozen`, confirm or replace every `[PROPOSED]` value:

- [ ] Section 5.2: estimation window, test window, step size
- [ ] Section 5.3: embargo length
- [ ] Section 6.1: significance thresholds
- [ ] Section 6.2: materiality thresholds
- [ ] Section 6.3: robustness thresholds
- [ ] Section 7.3: FDR level
- [ ] Section 8.1: block length, replications
- [ ] Section 5.5: cost levels (confirm 0/5/10/20/50 bps or replace)

Once confirmed, bump to Version 1.1, set Status to `Frozen`, and add a revision history row.

---

## 14. Revision History

| Date | Version | Change | Author |
|------|---------|--------|--------|
| 2026-10-14 | 1.0 | Initial protocol | Ken Ira Lacson Talingting |

---

*This protocol governs what counts as success. It must be frozen before experiments and defended against erosion.*
