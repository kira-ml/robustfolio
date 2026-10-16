# Evaluation Protocol: robustfolio

**Version:** 2.2
**Status:** Draft — Phase A and Phase C merges applied; pending owner confirmation of `[PROPOSED]` values and freeze
**Owner:** Ken Ira Lacson Talingting
**Created:** 2026-10-14 (as `success_metrics_and_evaluation_protocol.md`)
**Last Updated:** 2026-10-15
**Supersedes:** `success_metrics_and_evaluation_protocol.md` v1.1 and `falsification_and_kill_criteria.md` v1.1 (merged per execution TODO item B1); `project_charter.md` §6–9 (relocated per DEC-20261015-017, Phase A); `benchmark_and_baseline_spec.md`, `data_contract_and_point_in_time_policy.md`, `cost_model_and_frictions.md`, and `experiment_registry_and_preregistration.md` (spec sections) merged per DEC-20261015-018, Phase C
**Related:** [`problem_framing.md`](problem_framing.md), [`scope_and_non_goals.md`](scope_and_non_goals.md), [`risk_register_and_premortem.md`](risk_register_and_premortem.md), [`decision_log.md`](decision_log.md)

> **Merge note.** Per DEC-20261015-017 (Phase A) and DEC-20261015-018 (Phase C), this document has absorbed the project charter's §6–9 as §8; the baseline spec as §4; the data contract as §5.4; the cost model as §5.5; and the registry rules as §12. The registry *ledger* lives in `decision_log.md` Appendix A. All external references in the body have been redirected to the internal sections. Remaining external references are to documents that are retained in the 6-doc set: `problem_framing.md`, `scope_and_non_goals.md`, `risk_register_and_premortem.md`, and `decision_log.md`.

---

## 0. Purpose of This Document

This document defines, **before any experiment is run**:

1. Exactly how success and failure will be measured.
2. What claims the project makes and how each could be falsified.
3. What evidence triggers a kill, pivot, or stop-and-report.
4. How multiple-testing adjustment and uncertainty are handled.
5. How goalpost-moving, sunk-cost continuation, and complexity-creep-as-rescue are prevented.

This is the project's **evaluation and enforcement contract**. It owns the measurement instrument (§§2–7, 12–15), the governance rules that fire when measurement returns a verdict (§§8–11), and the merged spec sections that previously lived in separate documents (§4 baselines, §5.4 data contract, §5.5 cost model, §12 registry rules).

**Once frozen, this document may not be modified after seeing experimental results.** Any modification requires a decision log entry and a version bump, and the modification must be justified by a pre-existing protocol flaw, not by an inconvenient result.

---

## 1. Evaluation Philosophy

Six principles govern every measurement decision in this project.

1. **Net-of-cost, out-of-sample, multiple-testing-aware.** Gross Sharpe, in-sample Sharpe, and unadjusted p-values are diagnostic only. They are never the basis for a success claim.
2. **Pre-registration before execution.** Every experiment is registered with its hypothesis, parameters, metrics, and decision rule before it runs.
3. **Report the full distribution, not the point estimate.** Confidence intervals, sensitivity bands, and failure modes are reported alongside every headline number.
4. **Every claim must have a test that could prove it wrong.** If no such test exists, the claim is not part of the project's scientific content and may not be reported as a finding.
5. **Failure to falsify is not proof.** A method that survives its tests is "not yet falsified," not "correct." Reporting language must reflect this.
6. **Negative results are first-class outputs.** A falsified hypothesis is a successful experiment. A project that ends with a clean negative result has succeeded by its own definition (see [`problem_framing.md`](problem_framing.md) §13).

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

**Freeze-session note (DEC-20261015-015, finding 1).** The Phase 1 code computed "gross Sharpe" without subtracting the risk-free rate, while computing "net Sharpe" with it. As frozen, both gross and net Sharpe must use the same \( R_f \) convention, defined in §5.5.5. The freeze session must resolve this finding before Status flips to `Frozen`.

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

The primary metric is always reported relative to baselines, not in isolation. This section owns the baseline set, its mathematical definitions, and the fair-comparison rules. It absorbs content previously in `benchmark_and_baseline_spec.md` (per DEC-20261015-018, Phase C).

### 4.1 Baseline philosophy

Three principles govern baseline selection and implementation.

1. **Baselines are the null hypothesis.** A robust method is only interesting if it beats the strongest, simplest, fairest null. Weak baselines are a form of self-deception.
2. **Simple beats sophisticated.** If a complex method cannot beat 1/N, the complexity is not justified (DeMiguel, Garlappi, & Uppal, 2009).
3. **Reproducible without ambiguity.** Any researcher with the same data and cost model must be able to regenerate the baseline results. No magic constants, no undocumented choices.

A robust method that beats sample MVO but loses to 1/N has not solved the problem. A robust method that beats 1/N net of costs, after multiple-testing adjustment, has.

### 4.2 Baseline set

The MVP baseline set is fixed. Each baseline must be implemented, tested, and reported in every method comparison.

| ID | Baseline | Family | Uses expected returns? | Rationale |
|----|----------|--------|----------------------|-----------|
| **B1** | Equal weight (1/N) | Naive | No | Strongest simple prior (DeMiguel et al., 2009) |
| **B2** | Risk parity (equal risk contribution) | Risk-based | No | Practitioner default; robust to return error |
| **B3** | Sample mean-variance optimization | Classical | Yes | The method being critiqued |
| **B4** | Minimum variance | Risk-based | No | Robust to return error; classical alternative |
| **B5** | Turnover-penalized MVO (L1) | Robust | Yes | Simplest turnover-aware method |

**Extensions** (not in MVP; require a pre-registered experiment): inverse-volatility weights; hierarchical risk parity (López de Prado, 2016); equal risk budget with return views; shrinkage covariance + minimum variance; Black-Litterman.

### 4.3 Common definitions

All baselines share the following conventions.

- **Universe:** as defined in §5.4.2.
- **Rebalance frequency:** monthly (last trading day of the month).
- **Estimation window:** `[PROPOSED: 36 months rolling]` for B2, B3, B4, B5. B1 uses no estimation.
- **Constraints:** fully invested, long-only, no leverage.
  - \( \sum_i w_i = 1 \)
  - \( w_i \ge 0 \)
  - \( w_i \le w_{\max} \) where \( w_{\max} = \text{[PROPOSED: 0.30]} \)
- **Risk aversion:** \( \gamma = \text{[PROPOSED: 5]} \) for B3 and B5.
- **Covariance estimator:** sample covariance unless otherwise specified.
- **Expected return estimator:** sample mean (arithmetic, monthly) for B3 and B5.
- **Cost model:** proportional \( \kappa \) bps per one-way turnover, per §5.5.
- **Execution:** close of rebalance date (§5.5.4).
- **Point-in-time:** all inputs satisfy §5.4.3.

### 4.4 Baseline specifications

**B1 — Equal weight (1/N).** \( w_i = 1/N \) for all \( i \in U_t \). No inputs, no optimization. Turnover determined entirely by drifted weights and universe changes. Role: the primary benchmark. A robust method that cannot beat 1/N net of costs has not demonstrated practical value. Falsification relevance: if no robust method beats B1 net of costs, the primary objective is likely falsified (see §8.6 K1).

**B2 — Risk parity (equal risk contribution).** Solve for \( w \) such that \( w_i (\Sigma w)_i = w_j (\Sigma w)_j \) for all \( i,j \), subject to \( \sum w_i = 1 \), \( w_i \ge 0 \), \( w_i \le w_{\max} \). Inputs: sample covariance, 36 months rolling. Convex; solved via standard risk-budgeting algorithm (Spinu, 2013) or scipy-based iterative solver. Implementation note: diagonal loading \( \epsilon I \) with \( \epsilon = \text{[PROPOSED: 1e-6]} \) if \( \Sigma \) is near-singular.

**B3 — Sample mean-variance optimization (MVO).** \( \max_w \ w^\top \mu - \frac{\gamma}{2} w^\top \Sigma w \) subject to constraints above. Inputs: sample mean and covariance over 36 months rolling. QP; document solver and tolerance. The critique target. Demonstrating that B3 fails out-of-sample is expected and serves as a baseline sanity check, not as a novel finding. **Caveat:** if B3 does *not* show extreme weights or high turnover on the primary dataset, the problem framing premise is weakened. This is a Phase 1 exit criterion.

**B4 — Minimum variance.** \( \min_w \ w^\top \Sigma w \) subject to constraints. Equivalent to MVO with \( \mu = 0 \). Inputs: sample covariance, 36 months rolling. Diagonal loading as in B2.

**B5 — Turnover-penalized MVO (L1).** \( \max_w \ w^\top \mu - \frac{\gamma}{2} w^\top \Sigma w - \lambda \| w - w^- \|_1 \) subject to constraints. Inputs: \( \mu \), \( \Sigma \), \( \gamma \) as in B3; \( \lambda = \text{[PROPOSED: equal to baseline \( \kappa \) = 10 bps = 0.001 in monthly return units]} \); \( w^- \) = drifted weights from the previous period (see §5.5.5). Convex QP with auxiliary variables \( u_i \ge |w_i - w_i^-| \). The strongest simple robust baseline. Any robust method that does not beat B5 net of costs is not adding practical value beyond a simple penalty.

**Freeze-session note (DEC-20261015-015, finding 2).** In Phase 1, `TURNOVER_PENALTY = 0.1` was scale-dominated: it was ~2× the return term and ~20× the risk term in the monthly objective. The Phase 1 result is a statement about λ=0.1 specifically, not about turnover penalties as a class. The freeze session must specify a principled λ, either λ = κ or a documented alternative, and state the units.

### 4.5 Expected behavior (priors)

| Baseline | Expected turnover | Expected net Sharpe rank | Expected drawdown | Sensitivity to estimation error |
|----------|-------------------|--------------------------|-------------------|-------------------------------|
| B1 (1/N) | Low | Mid | Low-mid | None |
| B2 (Risk parity) | Mid | Mid-high | Low | Low-mid |
| B3 (Sample MVO) | High | Low | High | High |
| B4 (Min variance) | Mid | Mid-high | Low | Mid |
| B5 (Turnover-penalized MVO) | Low-mid | Mid-high | Mid | Mid |

These priors are testable. If Phase 1 results contradict them, update the model of the problem, not the priors.

### 4.6 Fair comparison rules

1. **Same universe.** All baselines use the same eligible universe at each rebalance date.
2. **Same data.** All baselines use the same point-in-time snapshot.
3. **Same cost model.** All baselines incur costs under the same model, \( \kappa \), and execution timing.
4. **Same constraints.** Weight bounds, leverage, and long-only constraints are identical.
5. **Same evaluation.** Walk-forward folds, cost levels, and metrics are identical.
6. **Same estimation window** where applicable. Deviations documented and justified.
7. **Same reporting.** Gross and net Sharpe, turnover, drawdown, cost drag at all cost levels.
8. **No silent parameter tuning.** Any parameter change from the frozen defaults requires a pre-registered experiment.

### 4.7 What invalidates a baseline comparison

- A baseline was implemented with a different cost model, universe, or constraint set than the robust method.
- A baseline's hyperparameters were tuned on test data.
- A baseline was reported only at cost levels that flattered it — or that flattered the robust method.
- A baseline's weights were not properly constrained.
- A baseline's covariance matrix was regularized while the robust method's was not (or vice versa) without documentation.
- A baseline was silently dropped from the comparison because of poor results.
- A baseline result was not reproducible from the frozen snapshot and code version.

Invalidated comparisons are documented, not deleted.

### 4.8 Reporting requirements

Every baseline result must report: baseline ID and name; exact inputs used (estimation window, covariance estimator, \( \gamma \), \( \lambda \), \( w_{\max} \)); solver and convergence status; gross Sharpe, net Sharpe at each cost level, turnover, drawdown, cost drag; confidence intervals for Sharpe and turnover; any deviation from frozen defaults with justification; implementation notes affecting interpretation.

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

**Freeze-session note (DEC-20261015-015, finding 4d).** The Phase 1 harness used an expanding-within-test training set (`train + test.iloc[:t]`), which is neither pure rolling nor pure expanding. The freeze session must specify which convention is adopted and adjust this subsection accordingly.

### 5.3 Purged cross-validation and embargo

- For any hyperparameter selection, use purged k-fold CV with an embargo between training and test folds.
- **Purge:** Remove training observations whose label window overlaps the test window.
- **Embargo:** `[PROPOSED: 1 month]` gap between training and test. Owner to confirm.
- Reference: López de Prado (2018), *Advances in Financial Machine Learning*, Ch. 7.

### 5.4 Data contract and point-in-time discipline

This section owns the data contract. It absorbs content previously in `data_contract_and_point_in_time_policy.md` (per DEC-20261015-018, Phase C).

**Three data principles:**

1. **Point-in-time or nothing.** Every value used at time \( t \) must have been available at time \( t \). Retroactive values (backfilled, restated, survivor-filtered) are not permitted in estimation or evaluation.
2. **Reproducible from raw.** Every derived dataset must be reconstructible from raw snapshots plus documented transformation code. No manual edits, no undocumented joins.
3. **Honest about limits.** Where public data cannot satisfy point-in-time requirements, the limitation is documented and the affected claims are downgraded, not hidden.

#### 5.4.1 Allowed sources

| Purpose | Source | Access | Point-in-time quality |
|---------|--------|--------|----------------------|
| Adjusted daily prices | `[PROPOSED: Yahoo Finance via yfinance]` | Free | Retroactive; must be reconstructed (§5.4.4) |
| Raw daily prices | `[PROPOSED: Yahoo Finance via yfinance]` | Free | Real-time at retrieval; reliable after snapshot |
| Corporate actions | `[PROPOSED: Yahoo Finance / Stooq]` | Free | Reasonable for large-cap |
| Risk-free rate (1-month T-bill) | `[PROPOSED: FRED DGS1MO]` | Free | Point-in-time |
| ETF / equity metadata | `[PROPOSED: Yahoo Finance / SEC EDGAR]` | Free | Reasonable |
| Universe definition | `[PROPOSED: fixed historical candidate list + delisted members]` | Free / manual | Must be reconstructed point-in-time |

**Forbidden sources:** any source whose historical values are retroactively adjusted without a raw alternative; any source whose free tier has undocumented revision history; any source whose TOS prohibits research use; any proprietary or paid data without explicit budget approval.

**Vendor lock-in mitigation:** all ingestion code isolates vendor-specific logic behind an adapter. Swapping sources must not require rewriting estimation or evaluation code.

#### 5.4.2 Universe definition

- **Asset class:** `[PROPOSED: US-listed ETFs spanning equity, fixed income, commodities, real estate]`.
- **Candidate universe size:** `[PROPOSED: 15–25 liquid ETFs]`.
- **Minimum history at backtest start:** `[PROPOSED: 5 years]`.
- **Currency:** USD only.
- **Instrument type:** long-only, unlevered ETFs.
- **Delisted handling:** any candidate that delisted during the backtest is retained up to its delisting date, then excluded. Delisting returns are included.

**Eligibility at time \( t \)** using only information available at \( t \):

1. It is a member of the candidate universe at \( t \).
2. It has at least `[PROPOSED: 36 months]` of consecutive valid price history ending at \( t \).
3. Its average daily dollar volume over trailing `[PROPOSED: 3 months]` exceeds `[PROPOSED: $5 million]`.
4. Its price at \( t \) is positive and not flagged as erroneous (§5.4.6).

Universe expansions require a §8 amendment and a new pre-registered experiment. Silent expansion invalidates results.

#### 5.4.3 Point-in-time rules

**At time \( t \), the following may be used:** prices, returns, and volumes observed at or before \( t \); corporate action information known at or before \( t \); universe membership as defined at or before \( t \).

**The following may not be used:** any value computed using future prices, future universe membership, or future corporate actions; any revised or restated historical value that was not the value available at \( t \); any index membership assigned after \( t \).

Weights at \( t \) use only information available at or before \( t \). Execution is at the close of \( t \) or open of \( t+1 \), fixed consistently across methods (§5.5.4). Return at \( t+1 \) uses prices between \( t \) and \( t+1 \); costs applied at \( t \) based on weight change from \( t-1 \) to \( t \). No future information enters the return calculation.

#### 5.4.4 Adjusted-price reconstruction

Free price sources typically provide **retroactively adjusted** prices. Using them naively is a form of lookahead.

**Required procedure:**

1. Retrieve **raw unadjusted close prices**; store as a snapshot.
2. Retrieve **corporate action history** (splits, dividends); store as a snapshot.
3. At evaluation time \( t \), compute adjusted prices using only corporate actions with ex-dates ≤ \( t \).
4. Use the point-in-time adjusted series for return computation.

If raw unadjusted series is unavailable, adjusted series may be used only if the adjustment methodology is documented, the bias is acknowledged as a limitation, and affected claims are downgraded to "exploratory" in reporting.

#### 5.4.5 Corporate actions

| Action | Handling |
|--------|----------|
| Stock split | Adjust historical prices and shares point-in-time; do not adjust weights (splits are value-neutral) |
| Cash dividend | Add to return on ex-date; do not adjust price retroactively for return calculation |
| Special dividend | Treated as cash dividend; document and flag |
| Merger / acquisition | Asset removed at effective date; terminal value added to returns |
| Delisting | Asset removed at delisting date; delisting return added (assume `[PROPOSED: -100%]` if unavailable, flag as limitation) |
| Ticker change | Reconciled in metadata; same asset |
| ETF inception | Asset enters only after inception and eligibility rules are satisfied |

Any action not covered above must be documented before use.

#### 5.4.6 Missing data and outliers

| Case | Policy |
|------|--------|
| Isolated missing day | Forward-fill up to `[PROPOSED: 3 consecutive days]`; mark as imputed |
| Extended gap (> 3 days) | Treat asset ineligible for the gap window; exclude from rebalance |
| Missing risk-free rate | Use last observed value; flag |
| Missing corporate action | Halt; reconcile before proceeding |

Price jumps not explained by corporate actions are flagged and reviewed. Volume spikes not explained by events are flagged but retained. Manual overrides require a decision log entry and a data-quality note in the snapshot.

**Freeze-session note (DEC-20261015-015, finding 4c).** The Phase 1 code substituted zero for missing risk-free rate months via `.fillna(0.0)`. The freeze session must specify the missing-rf policy explicitly, replacing silent substitution.

Every snapshot has a companion quality report listing: missing values imputed, outliers flagged, corporate actions applied, universe membership changes, unresolved issues.

#### 5.4.7 Survivorship bias prevention

1. The candidate list is defined **as of the backtest start date**, not as of today.
2. Assets that delisted during the backtest remain in the universe until their delisting date.
3. Delisting returns are included.
4. No asset is dropped from the candidate list because it no longer exists today.
5. The candidate list must be reconstructed from point-in-time evidence (archived ETF screens, historical fund lists, SEC filings).

If point-in-time universe membership cannot be reconstructed, the limitation is documented and affected claims are downgraded.

#### 5.4.8 Leakage tests

Before any experiment runs:

1. **Time-travel test:** for random timestamps, verify no field used at \( t \) contains values knowable only after \( t \).
2. **Survivorship test:** verify the universe at \( t \) includes assets that delisted after \( t \).
3. **Adjusted-price test:** verify point-in-time adjusted prices do not incorporate corporate actions with ex-dates after \( t \).
4. **Universe reconstruction test:** verify membership at \( t \) matches archived evidence.
5. **Determinism test:** same snapshot + same code → identical output.

Any failing test blocks the experiment.

#### 5.4.9 Snapshots and versioning

A **snapshot** is an immutable bundle of: raw source files; retrieval timestamp; source identifiers and URLs; SHA-256 hash of the bundle; companion quality report. Stored under `data/snapshots/<snapshot_id>/` and never modified.

Naming: `<source>-<asset_class>-<start>_<end>-<retrieval_date>-<hash8>`.

Every derived dataset records: the snapshot ID it derives from; the transformation code version (git commit); a hash of the output.

Snapshots are append-only. Corrections create a new snapshot; old ones are retained.

**Freeze-session note (DEC-20261015-015, finding 4a).** The Phase 1 cache returns stale data if the cache file exists and is stale. The freeze session must specify a cache invalidation policy (or declare this out of scope for Phase 2).

#### 5.4.10 What invalidates a result

- Point-in-time violation in any field.
- Survivorship bias in universe construction.
- Undocumented corporate action adjustment.
- Use of retroactively adjusted prices without point-in-time reconstruction.
- Manual edit of a raw value without a decision log entry.
- Snapshot mismatch between estimation and evaluation.
- Failing leakage test not resolved before running.
- Missing data imputation beyond §5.4.6 without disclosure.

Invalidated results are documented, not deleted.

### 5.5 Cost model and frictions

This section owns the cost model. It absorbs content previously in `cost_model_and_frictions.md` (per DEC-20261015-018, Phase C).

**Three cost principles:**

1. **Costs are certain; rebalancing benefits are not.** A rebalance pays cost today for an uncertain future benefit. The model must make this asymmetry explicit.
2. **Simple, conservative, transparent.** A fixed-bps model is preferred over a complex impact model. Where the model is wrong, it should err toward overestimating costs.
3. **Sensitivity over precision.** We do not know the true cost. Results are reported across a range of cost levels; a robust method is one whose advantage survives across the range.

#### 5.5.1 Scope

| Friction | Modeled? | Notes |
|----------|----------|-------|
| Commissions | Yes | Fixed bps per trade |
| Bid-ask spread | Yes | Fixed bps per trade; separable |
| Slippage | Yes | Fixed bps per trade, conservative |
| Market impact | Simplified, optional | Size-dependent term, off by default |
| Tax | No | Documented as limitation |
| Financing / borrow | No | Long-only, no leverage |
| FX | No | USD-only universe |
| Operational overhead | No | Not a per-trade friction |

**Out of scope (explicitly):** realistic impact curves (Almgren-Chriss, square-root); order book dynamics; intraday execution modeling; tax optimization; short-selling borrow costs; custody fees, fund expense ratios; capacity constraints from AUM.

#### 5.5.2 Cost formula

For each asset \( i \) at rebalance time \( t \):

\[
\text{Trade}_i(t) = |w_i(t) - w_i(t^-)| \cdot \text{AUM}
\]
\[
c_i(t) = \kappa \cdot |w_i(t) - w_i(t^-)|
\]
\[
C(t) = \sum_i c_i(t)
\]
\[
R_{\text{net}}(t) = R_{\text{gross}}(t) - C(t)
\]

**Turnover at \( t \) (one-way, portfolio-level):** \( \text{Turnover}(t) = \sum_i |w_i(t) - w_i(t^-)| \).

Annualized turnover = sum of monthly turnover over 12 months. **One-way** throughout. Any two-way usage must be labeled.

**Freeze-session note (DEC-20261015-015, finding 4b).** The Phase 1 code contained a dead `metrics.annualized_turnover` function using a different turnover definition than `realized_turnover`. The freeze session must ensure a single canonical turnover definition is used in Phase 2 code, and this subsection's formula is that definition.

#### 5.5.3 Cost parameter \( \kappa \)

| Cost level | \( \kappa \) (one-way bps) | Purpose |
|------------|---------------------------|---------|
| Zero | 0 | Diagnostic only |
| Low | 5 | Best-case realistic |
| Baseline | 10 | Primary cost assumption |
| High | 20 | Stress case |
| Extreme | 50 | Robustness boundary |

**Baseline \( \kappa = 10 \) bps** is the primary assumption. All headline results at this level. Other levels reported as sensitivity bands.

**Optional size-dependent term (off by default):** \( c_i(t) = \kappa \cdot |\Delta w_i| + \lambda \cdot \text{ADV-ratio}_i \cdot |\Delta w_i|^{3/2} \). If enabled, documented in the registry and reported separately, not mixed into the baseline.

#### 5.5.4 Execution timing

- **Rebalance frequency:** monthly.
- **Rebalance date:** last trading day of the month.
- **Signal computation:** based on data through the close of the rebalance date.
- **Execution price:** `[PROPOSED: close of the rebalance date]`.
- **Cost application:** costs applied at the rebalance date, deducted from that period's return.

The choice must be consistent across all methods and documented in every registry entry.

#### 5.5.5 Drifted weights and risk-free rate convention

Between rebalances, weights drift:

\[
w_i(t^-) = \frac{w_i(t-1) \cdot (1 + r_i(t))}{\sum_j w_j(t-1) \cdot (1 + r_j(t))}
\]

This must be computed correctly. A common bug is to treat pre-rebalance weights as equal to post-rebalance weights from the prior period, which understates turnover and costs. See `risk_register_and_premortem.md` R-C01.

**Risk-free rate convention (freeze-session input).** For all Sharpe ratios, gross and net, \( R_f \) is the 1-month T-bill yield as observed at \( t \), converted to a monthly rate. The same \( R_f \) series is used for both gross and net Sharpe. `Cost drag` is defined as the difference between gross Sharpe and net Sharpe under the *same* \( R_f \) convention. This resolves DEC-20261015-015 finding 1.

#### 5.5.6 Cost-aware vs cost-penalized

Two distinct approaches:

1. **Cost-aware:** model costs explicitly and subtract from returns.
2. **Cost-penalized:** add a penalty term to the objective, which indirectly controls turnover.

Both are in scope. Each must be labeled clearly. A method that is cost-aware but uses cost-penalized language (or vice versa) is mislabeled and will be flagged.

For the turnover-penalized objective \( \max_w \ w^\top \mu - \frac{\gamma}{2} w^\top \Sigma w - \lambda \| w - w^- \|_1 \), under the proportional cost model \( \lambda = \kappa \) aligns the penalty with the actual cost. In practice \( \lambda \) may be tuned above \( \kappa \). The units of \( \lambda \) are monthly return per unit of one-way turnover.

#### 5.5.7 Sensitivity analysis

Every method is evaluated across the 5 cost levels in §5.5.3.

1. **Primary result** at 10 bps.
2. **Sensitivity band** across 0–50 bps.
3. **Break-even cost** at which the method loses its advantage over the best baseline.
4. **Monotonicity check:** does net Sharpe decline monotonically with cost? Non-monotonicity signals a bug or artifact.

A robust method has a break-even cost above the baseline assumption (10 bps) and ideally above the stress case (20 bps).

#### 5.5.8 Limitations (explicit)

Fixed bps is not reality. No market impact curve. No intraday dynamics. No capacity model. No regime dependence. No tax. These limitations bound the claims. Claims about real-world profitability beyond the modeled frictions must be explicitly qualified.

#### 5.5.9 What invalidates a net-of-cost result

- Costs were not applied to drifted weights (§5.5.5).
- Different cost levels were applied inconsistently across methods.
- Turnover was reported two-way but compared against a one-way cost model.
- The cost parameter \( \kappa \) differs across methods without justification.
- The execution price assumption differs across methods.
- Cost-penalized and cost-aware methods were compared without labeling.
- Sensitivity analysis was skipped or reported selectively.
- Market impact was included in one method but not in the baseline without disclosure.

Invalidated results are documented, not deleted.

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

- Its advantage over the best baseline holds at **≥ 3 of the cost levels defined in §5.5.3**, AND
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

**Family kill trigger:** If H1.1 and H1.2 both fail on the primary dataset, the problem framing is falsified. Pivot or stop before Phase 2. See §8.6 K2.

### Family H2 — Robust methods improve net performance

| ID | Hypothesis | Falsification test | Kill/pivot on falsification |
|----|-----------|-------------------|------------------------------|
| H2.1 | Shrinkage covariance beats sample covariance on net Sharpe | §6 success criteria met | If not, drop shrinkage from the claim set |
| H2.2 | Bayesian expected returns beat historical mean on net Sharpe | Same criteria | If not, drop Bayesian returns |
| H2.3 | Turnover penalty improves net Sharpe vs unpenalized MVO | Same criteria | If not, drop turnover penalty |
| H2.4 | At least one robust method beats the best baseline on net Sharpe | Same criteria | **Project-level trigger — see §8.6 K1** |

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

**Family kill trigger:** If H4.1 or H4.2 fails, the gap hypothesis is falsified. Update [`problem_framing.md`](problem_framing.md) §4.1 and pivot. See §8.6 K3.

---

## 8. Project-Level Governance and Kill Triggers

This section absorbs content previously in `project_charter.md` §6–9 (relocated per DEC-20261015-017). It owns the decision taxonomy, decision rights, time-boxes, phase gates, and project-level kill triggers.

### 8.1 Decision taxonomy and authority

| Category | Meaning | Authority |
|----------|---------|-----------|
| **Kill** | Stop the project; archive findings | Owner |
| **Pivot** | Change the problem framing or deliverable (e.g., diagnostic tool instead of method superiority) | Owner |
| **Stop-and-report** | Conclude with a documented negative result | Owner |
| **Continue** | Proceed to next phase | Owner |

**Hard rules:**

1. No phase may exceed its time-box (§8.3) without a decision log entry.
2. If no robust method satisfies §6.4 after Phase 3, the project must pivot to Stop-and-report rather than add complexity.
3. Adding a new method to rescue a failing result requires a pre-registered hypothesis and a new experiment entry (§12).
4. The owner may kill the project at any time. A decision log entry is still required, even if the justification is simply "owner decision." This preserves the learning loop and prevents silent abandonment.

### 8.2 Decision rights

| Role | Holder | Responsibility |
|------|--------|----------------|
| **Owner / Decision-maker** | Ken Ira Lacson Talingting | Final authority on scope, gates, kill/pivot, and claims |
| **Reasoning partner** | LLM (Core Mental Models OS) | Challenge assumptions, surface failure modes, apply models, flag anti-patterns |
| **Reviewer** | None (no third-party reviewer; self-review plus reasoning-partner challenge) | Sanity-check evaluation protocol and claims before release |
| **Informed** | Open-source users, readers of the repo | Consume results and documentation |

**Escalation:** If the reasoning partner identifies a violation of the evaluation protocol, kill criteria, or anti-patterns, it must flag it. The owner decides. Silence is not consent.

### 8.3 Time-boxes

> **Note:** The values below are proposed conservative defaults for a solo, part-time independent researcher. Confirm or replace each value before freezing.

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

**Risk of ruin:** Low. The project risks time, not capital or reputation, provided claims are framed honestly and phase gates are enforced.

### 8.4 Phase gates

A phase cannot begin until the prior gate is passed. Gates are enforced by the owner, not by momentum.

| Phase | Name | Entry Criteria | Exit Criteria (Go) | No-Go Action |
|-------|------|----------------|--------------------|--------------|
| 0 | Problem Validation | Tier 0 documentation Active or Frozen | R1 complete and documents a scan of ≥10 relevant open-source tools, papers, or repositories, explicitly stating which part of the gap hypothesis remains uncovered; registry, data contract, cost model, baseline spec, and evaluation protocol drafted | Narrow problem or stop |
| 1 | Data & Baselines | Gate 0 passed; data contract, cost model, baseline spec frozen; method spec frozen | C1, C2, C3 work; R2 shows MVO instability is real | Fix data/cost contract or stop |
| 2 | Robust Methods | Gate 1 passed | C4 implemented and unit-tested; no leakage | Reduce method scope |
| 3 | Evaluation | Gate 2 passed | C5 complete; R3 produced; multiple-testing adjusted | Extend evaluation or narrow claims |
| 4 | Reporting & Release | Gate 3 passed | C6 complete; R4 written; repo reproducible from scratch | Release as negative result or diagnostic tool |
| 5 | Extensions (optional) | Gate 4 passed and primary objective met OR clearly framed | Extension scoped and justified by priors | Do not start |

**Gate discipline:** A gate may be passed with a documented negative result. It may not be passed by relaxing the evaluation protocol after seeing results.

### 8.5 Governance cadence

| Cadence | Activity | Output |
|---------|----------|--------|
| Before each experiment | Pre-register hypothesis, parameters, metrics, decision rule | Entry in the registry (§12, `decision_log.md` Appendix A) |
| After each experiment | Record result, update priors, decide next action | Registry entry + decision log entry if material |
| At each phase gate | Review exit criteria; decide go/no-go/pivot/kill | Decision log entry |
| Monthly | Review §8, status board, risk register | Updated docs |
| On surprise or failure | Update risk register and decision log; revisit priors | Updated docs |

### 8.6 Project-level kill triggers

These are the conditions under which the project as a whole must decide to kill, pivot, or stop-and-report. Each is a **hard trigger**: the decision cannot be deferred. The taxonomy and authority are defined in §8.1.

#### K1 — Primary objective falsified

**Trigger:** After Phase 3 evaluation, no robust method satisfies §6.4 (statistical significance + economic materiality + robustness).

**Decision:** Stop-and-report. The project's primary hypothesis is falsified.

**Not permitted:** Adding new methods, relaxing thresholds, or extending the evaluation to find a positive result.

**Rationale:** §8.1 Hard Rule 2 already says this. This section makes it enforceable.

#### K2 — Problem framing falsified

**Trigger:** H1.1 and H1.2 both fail on the primary dataset, before Phase 2.

**Decision:** Kill or pivot to a diagnostic-benchmark framing.

**Not permitted:** Proceeding to Phase 2 on the assumption that "the problem must be real."

#### K3 — Gap hypothesis falsified

**Trigger:** R1 identifies an existing tool or paper that reproduces the planned comparison with equivalent rigor.

**Decision:** Kill or pivot to replication or extension.

**Not permitted:** Proceeding to build a less rigorous version of something that exists.

#### K4 — Time budget exhausted

**Trigger:** Total time budget from §8.3 is reached, regardless of where the project is.

**Decision:** Stop-and-report with whatever is complete. If results are not yet available, report as "incomplete — no conclusion."

**Not permitted:** Silent time-box extension. Any extension requires an amendment to §8.3 with a decision log entry.

#### K5 — Phase time-box exhausted without gate pass

**Trigger:** Any phase exceeds its time-box from §8.3 without passing its gate.

**Decision:** Kill the phase or pivot the phase goal. Do not roll over into the next phase.

**Not permitted:** Continuing into the next phase "in parallel" or "just to keep momentum."

#### K6 — Data or cost contract broken

**Trigger:** Any experiment in Phase 1 or later reveals a violation of §5.4 (data contract) or §5.5 (cost model) that cannot be corrected without invalidating prior results.

**Decision:** Halt evaluation. Fix the contract. Re-run affected experiments or kill.

**Not permitted:** Reporting results from invalidated experiments as findings.

#### K7 — Cumulative invalidation

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
| Diagnostic benchmark | K1 or H3.3 fails for all methods | Deliver the framework and negative result as the contribution | Update `problem_framing.md`, §8 |
| Replication study | K3 | Reproduce an existing result to validate the framework | Update scope and this protocol |
| Narrower method scope | H2.x fails for a specific method | Drop that method; keep the family | Update baseline list in §4 |
| Narrower universe | H1.x fails on one asset class but holds on another | Restrict to the asset class where the effect is real | Update §5.4 |
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
3. The owner elects to stop for any reason (per §8.1 Hard Rule 4), OR
4. Two or more pivot attempts have failed.

**Stop-and-report deliverable:**

- A written conclusion: positive, negative, or mixed, with explicit language about what was and was not tested.
- All Tier 0 documentation in its final state.
- The full experiment registry, including failed and invalidated experiments.
- The decision log documenting the stop.
- Reproducible code and data acquisition instructions.

**Stop-and-report is not failure.** It is the correct outcome when the evidence does not support the claim. It is reported with the same care as a positive result.

---

## 12. Experiment Registry and Multiple Testing Adjustment

This section owns registry *rules* and multiple-testing adjustment. It absorbs content previously in `experiment_registry_and_preregistration.md` (per DEC-20261015-018, Phase C). The registry *ledger* lives in `decision_log.md` Appendix A.

### 12.1 Preregistration philosophy

1. **Lock before you look.** Every hypothesis, parameter, metric, and decision rule is recorded before the experiment runs. If it is not written down beforehand, it is exploratory.
2. **The denominator is honest.** The number of registered trials is the multiple-testing denominator. Hiding trials is scientific misconduct, including self-deception.
3. **Negative results are entries too.** A failed experiment is recorded with the same rigor as a successful one.

A result obtained from an unregistered run is a hypothesis, not a finding.

### 12.2 What counts as an experiment

An **experiment** is any run that produces a metric on which a decision or claim will be based. This includes comparisons of robust methods against baselines, reported sensitivity analyses, hyperparameter selection affecting a reported metric, and re-runs with any change in data, code, or parameters.

It does **not** include unit/integration/leakage tests, exploratory data analysis unless reported, debugging runs whose outputs are discarded, or sanity checks that do not produce a reported metric.

**Rule:** If you will report the number, it is an experiment.

### 12.3 Registry structure

- **Storage:** rules in this section; ledger in `decision_log.md` Appendix A.
- **ID format:** `EXP-<family>-<YYYYMMDD>-<nnn>`. Family codes: `H1`, `H2`, `H3`, `H4`, `X` (exploratory).
- **Immutability:** pre-registration section frozen on creation; results, conclusion, and decision sections appended. Amendments are separate entries referencing the original.
- **Append-only:** no entry is deleted. Invalidated experiments marked `INVALIDATED` with reason.

### 12.4 Preregistration template

Every registration must include all fields below before execution:

- **Status, Registered date, Family, Related hypotheses, Related decision triggers.**
- **1. Hypothesis:** statement (one sentence, falsifiable); direction; effect size of interest; prior probability with justification.
- **2. Methods compared:** baselines (B-IDs from §4); candidate methods (M-IDs).
- **3. Parameters:** universe; snapshot ID (SHA-256); estimation window; rebalance frequency; cost levels; constraints; method-specific parameters; random seeds.
- **4. Evaluation protocol:** protocol version; primary metric; secondary metrics; statistical test; confidence level; multiple-testing family size at registration (count of prior trials in this family + 1).
- **5. Decision rule:** success condition; failure condition; ambiguous condition; action on each.
- **6. Cost and time estimate:** compute budget; wall-clock; data volume.
- **7. What would invalidate this experiment.**
- **8. Pre-registration signature:** author; date; git commit at registration; registry version at registration.

The `Status` field is the only field that may change in the pre-registration section, and only to reflect progression.

### 12.5 Results, conclusion, and decision templates

Appended after execution, analysis, and decision respectively. Never edited.

**Results:** run date; git commit; snapshot ID; wall-clock; compute cost; primary metric table (net Sharpe at 10 bps, 90% CI, deflated Sharpe p-value); secondary metrics table (turnover, max DD, CVaR 95%, cost drag, calibration); sensitivity across cost levels; walk-forward fold results; calibration checkboxes (time-travel, survivorship, adjusted-price, universe reconstruction, determinism); anomalies.

**Conclusion:** verdict (CONFIRMED / FALSIFIED / INCONCLUSIVE / INVALIDATED); effect size observed; effect size vs pre-registered threshold; statistical significance; economic materiality; robustness; interpretation (2–4 sentences); threats to validity; links to update (§7, `decision_log.md`, `risk_register_and_premortem.md` if new failure mode, `problem_framing.md` if framing affected).

**Decision:** CONTINUE / PIVOT / KILL / STOP-AND-REPORT; authority; date; rationale (2–4 sentences); next experiment (EXP-ID or "none"); decision log entry link.

### 12.6 Multiple-testing denominator

The denominator is the number of **registered confirmatory trials** in a family up to and including the current trial.

1. Every registration in family H1–H4 counts.
2. Exploratory registrations (family X) do not count and cannot support success claims.
3. Invalidated experiments still count.
4. Amendments count as new trials if they change any parameter, metric, or decision rule.
5. Re-runs with identical parameters and code count as one trial.

Every result must report the current family size \( N \), the deflated Sharpe adjustment applied, and the FDR-adjusted p-value.

**Freezing:** once Phase 3 begins, the denominator for H2 and H3 is frozen. Additional trials require a decision log entry justifying why they do not constitute goalpost-moving.

### 12.7 Deflated Sharpe ratio

Adjusts for: number of trials \( N \); non-normality of returns (skewness, kurtosis); length of sample; variance of Sharpe estimates across trials. Reference: Bailey & López de Prado (2014).

### 12.8 Family-wise error control

- Trials are grouped by hypothesis family (H1–H4 in §7).
- Within a family, apply Benjamini-Hochberg FDR control at `[PROPOSED: q = 0.10]`. Owner to confirm.
- Report both raw and adjusted p-values.

### 12.9 Amendments and re-runs

**Amendment** changes a registered experiment before it runs, or adds a new trial after a prior one completed. Requires a new registration ID, reference to the original, one-sentence justification, pre-registration of changed fields, and (if motivated by a prior result) a decision log entry.

**Re-run** re-executes with same parameters and code. Does not create a new registry entry; records the new run date, environment, and outcome in the existing entry. Counts as one trial.

Re-run triggers: hardware, compute time, non-parameter git commit. Amendment triggers: random seed, any parameter, metric definition, decision rule, data snapshot, baseline set.

### 12.10 Exploratory work

**Definition:** any analysis whose result is not pre-registered.

**Rules:** must be labeled `EXPLORATORY` in every artifact; may motivate new pre-registered experiments; may not support success claims; must be reported in a separate section of any publication; existence must be disclosed when reporting confirmatory results.

The failure mode being prevented: running many unregistered variants, finding one that "works," and pre-registering it retroactively.

### 12.11 What invalidates an experiment

- The experiment ran before the registration was complete.
- Fields in the pre-registration section were edited after execution.
- The results section reports a metric not in the pre-registration.
- The decision rule was changed after seeing results.
- A family-size count in the registration was wrong and cannot be corrected without invalidating the adjustment.
- The experiment was not registered at all but is reported as a finding.
- A trial was suppressed from the denominator.

Invalidation does not delete the entry. It marks it `INVALIDATED` with a reason and a reference to the relevant rule.

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

Every experiment result is reported in a standard format. See `results_reporting_and_claims_policy.md` for the full template (to be written before Phase 4).

### 14.1 Mandatory disclosures

Every result must report:

1. Gross and net Sharpe at every cost level defined in §5.5.3.
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

When a trigger from §8.6 fires, follow this sequence:

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
- Cost model inconsistent with §5.5.
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
3. Cost levels defined in §5.5.3 cannot be changed without amending this document, which requires the same discipline.
4. A change is permitted only if:
   - A protocol flaw is discovered **before** seeing results, AND
   - The change is documented in the decision log with rationale, AND
   - The version is bumped, AND
   - Affected experiments are re-run and re-registered.
5. Any change made **after** seeing results requires a full decision log entry explaining why the change is not goalpost-moving. The owner must be able to defend this to a skeptical external reviewer.

**Conflict resolution with other documents:**

| Conflict | Resolution |
|----------|------------|
| Taxonomy, authority, time-boxes, phase gates vs any document | This document §8 owns the decision taxonomy, decision rights, time-boxes, and phase gates. |
| Thresholds and triggers vs any document | This document §§6–8 owns thresholds and triggers. |
| Baselines vs any document | This document §4 owns the baseline set and fair-comparison rules. |
| Data contract vs any document | This document §5.4 owns the data contract. |
| Cost levels vs any document | This document §5.5 owns the cost model and cost levels. |
| Registry format and rules vs any document | This document §12 owns registry rules. The registry ledger lives in `decision_log.md` Appendix A. |
| Problem framing vs this document | This document may falsify the problem framing. When it does, [`problem_framing.md`](problem_framing.md) must be updated. |
| Scope vs this document | [`scope_and_non_goals.md`](scope_and_non_goals.md) owns scope. Pivots that change scope (§10) require a scope amendment, not just a decision log entry. |
| Risk register vs this document | [`risk_register_and_premortem.md`](risk_register_and_premortem.md) is a living document owned by itself. Its R-IDs are referenced from this document but not defined here. |
| Owner intuition vs this document | This document wins until amended via decision log. |

---

## 17. Model Tags Applied

- **[First Principles]** — Reduced success to a single primary metric with supporting diagnostics.
- **[Experimental]** — Pre-registration, walk-forward, purged CV, embargo, falsification.
- **[Bayesian]** — Confidence intervals, probabilistic Sharpe, calibration, priors revisited after each trigger.
- **[Inversion]** — Invalidation rules (§15), forbidden claims (§14.2), freeze rules (§16), sunk-cost firewall (§9).
- **[Systems]** — Cost sensitivity bands, multiple-testing family control, trigger-response cadence, phase gates (§8.4).
- **[Expected Value]** — Materiality thresholds define economically meaningful improvement; sunk-cost firewall; kill is free.
- **[Information Theory]** — Compressed to decisions, thresholds, and rules; no filler.
- **[Learning Loop]** — Every trigger logged; priors updated; pivot history preserved.

---

## 18. Owner Action Checklist Before Freezing

Before setting Status to `Frozen`, confirm or replace every `[PROPOSED]` value:

**Measurement protocol:**

- [ ] §5.2: estimation window, test window, step size
- [ ] §5.2: walk-forward convention (pure rolling vs expanding-within-test — resolves DEC-20261015-015 finding 4d)
- [ ] §5.3: embargo length
- [ ] §6.1: significance thresholds
- [ ] §6.2: materiality thresholds
- [ ] §6.3: robustness thresholds
- [ ] §12.8: FDR level
- [ ] §13.1: block length, replications

**Baselines (§4):**

- [ ] §4.3: estimation window (36 months) and \( w_{\max} \) (0.30)
- [ ] §4.3: \( \gamma \) (5)
- [ ] §4.4 B2: risk parity solver and diagonal loading
- [ ] §4.4 B5: \( \lambda \) baseline and L1 formulation; **resolves DEC-20261015-015 finding 2**
- [ ] §4.2: baseline set (B1–B5) confirmed; no extensions promoted

**Data contract (§5.4):**

- [ ] §5.4.1: data sources and access method
- [ ] §5.4.2: candidate universe size and minimum history
- [ ] §5.4.2: eligibility thresholds (history, dollar volume)
- [ ] §5.4.5: delisting return assumption
- [ ] §5.4.6: forward-fill limit; **resolves DEC-20261015-015 finding 4c** (missing rf policy)
- [ ] §5.4.9: snapshot naming convention; **resolves DEC-20261015-015 finding 4a** (cache invalidation policy)

**Cost model (§5.5):**

- [ ] §5.5.3: baseline \( \kappa \) and cost level set
- [ ] §5.5.1: decide whether size-dependent impact term is in MVP (default: off)
- [ ] §5.5.4: execution price assumption (close vs next open)
- [ ] §5.5.6: whether \( \lambda = \kappa \) or a tuned value will be used
- [ ] §5.5.5: risk-free rate convention for gross and net Sharpe; **resolves DEC-20261015-015 finding 1** (gross Sharpe definition)

**Governance (§8):**

- [ ] §8.3: time-boxes (per-week, total, per-phase)
- [ ] §8.4: phase gate exit criteria are usable as written

**Falsification and triggers:**

- [ ] §7 H1.1: extreme-weight threshold
- [ ] §7 H1.2: turnover ratio threshold
- [ ] §8.6 K7: cumulative invalidation count
- [ ] §14.3: decision time-box

**Cross-document consistency:**

- [ ] §8.6 triggers are consistent with the time-boxes in §8.3
- [ ] §9 sunk cost firewall rules are acceptable
- [ ] §10 forbidden pivots are acceptable
- [ ] §14.3 decision authority matches §8.2
- [ ] §16 conflict resolution is internally consistent

**Open freeze-session inputs (DEC-20261015-015):**

- [ ] Finding 1 resolved (gross Sharpe definition) — §2 note, §5.5.5
- [ ] Finding 2 resolved (turnover penalty scale) — §4.4 B5, §5.5.6
- [ ] Finding 4a resolved (cache staleness) — §5.4.9
- [ ] Finding 4b resolved (duplicate turnover function) — §5.5.2
- [ ] Finding 4c resolved (missing rf substitution) — §5.4.6
- [ ] Finding 4d resolved (walk-forward convention) — §5.2

Once confirmed, bump to Version 2.3, set Status to `Frozen`, and add a revision history row.

---

## 19. Revision History

| Date | Version | Change | Author |
|------|---------|--------|--------|
| 2026-10-14 | 1.0 | Initial protocol (`success_metrics_and_evaluation_protocol.md`) | Ken Ira Lacson Talingting |
| 2026-10-14 | 1.0 | Initial falsification and kill criteria (`falsification_and_kill_criteria.md`) | Ken Ira Lacson Talingting |
| 2026-10-15 | 1.1 | Protocol: replaced §5.5 cost levels with pointer to cost model doc (A6) | Ken Ira Lacson Talingting |
| 2026-10-15 | 1.1 | Falsification: replaced §3 taxonomy with pointer to charter §7 (A5); changed "gap claim" to "gap hypothesis" | Ken Ira Lacson Talingting |
| 2026-10-15 | 2.0 | Merged the two documents into a single `evaluation_protocol.md` (B1). Structure: metrics (§§2–4) → protocol (§5) → thresholds (§6) → hypotheses (§7) → triggers (§8) → firewalls (§§9–11) → adjustment and uncertainty (§§12–13) → reporting and invalidation (§§14–15) → freeze rules (§16). Consolidated the two owner checklists into one (§18) and the two revision histories into one (§19). | Ken Ira Lacson Talingting |
| 2026-10-15 | 2.1 | Phase A relocations per DEC-20261015-017. §8 retitled "Project-Level Governance and Kill Triggers" and expanded to absorb `project_charter.md` §6–9: §8.1 taxonomy, §8.2 decision rights, §8.3 time-boxes, §8.4 phase gates, §8.5 governance cadence, §8.6 kill triggers. All references to `project_charter.md` removed or redirected to §8. §16 conflict table rewritten. §18 checklist updated to reference §8 instead of the charter, and expanded with the DEC-20261015-015 findings 1, 2, 4 as freeze-session inputs. §10 pivot table "Requires" column updated. §11 stop-and-report reference updated to §8.1 Hard Rule 4. §1 principle 6 reference updated to `problem_framing.md` §13. | Ken Ira Lacson Talingting |
| 2026-10-15 | 2.2 | Phase C spec merges per DEC-20261015-018. §4 replaced with full baseline section (from `benchmark_and_baseline_spec.md`): philosophy, baseline set, common definitions, per-baseline specifications, priors, fair-comparison rules, invalidation rules, reporting requirements. §5.4 replaced with full data contract (from `data_contract_and_point_in_time_policy.md`): sources, universe, point-in-time rules, adjusted-price reconstruction, corporate actions, missing data, survivorship, leakage tests, snapshots, invalidation rules. §5.5 replaced with full cost model (from `cost_model_and_frictions.md`): scope, formula, \( \kappa \) levels, execution timing, drifted weights, cost-aware vs cost-penalized, sensitivity, limitations, invalidation rules. §12 replaced with full registry rules and multiple-testing adjustment (from `experiment_registry_and_preregistration.md`): philosophy, definition, structure, templates, denominator, deflated Sharpe, FDR control, amendments, exploratory rules, invalidation. §16 conflict table rewritten to reflect internal ownership. §18 checklist expanded with subsection checklists for §4, §5.4, §5.5, and explicit freeze-session inputs mapped to DEC-20261015-015 findings. Freeze-session notes added inline at §2, §4.4 B5, §5.2, §5.4.6, §5.4.9, §5.5.2, §5.5.5. Status remains `Draft`; freeze is the next step. | Ken Ira Lacson Talingting |

---

*This protocol governs what counts as success and when the project stops. It must be frozen before experiments and defended against erosion. If it is not enforced, the project is not falsificationist.*
