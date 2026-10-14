# Problem Framing: Robust, Turnover-Aware Portfolio Rebalancing

**Version:** 2.1
**Status:** Foundational, falsifiable problem contract
**Project:** `robustfolio`
**License:** MIT (see repository root)

---

## 0. Purpose

This document defines the real-world problem that `robustfolio` exists to investigate. It is not a project plan, feature list, or solution specification. It is a falsifiable problem contract grounded in fundamentals, causal reasoning, practical constraints, and out-of-sample evaluation.

Its purpose is to:

- Establish a shared understanding of the problem.
- Identify who experiences it and what decisions it affects.
- Explain why it matters in practice.
- Document current approaches and their limitations.
- Point to the authoritative sources for scope, evaluation, and risk.
- Provide a falsifiable basis for evaluating whether the project succeeds.

Read this before writing code, selecting models, or running backtests.

**Scope note.** This document does not define scope, evaluation protocol, or risk register. Those live in:

- Scope: [`scope_and_non_goals.md`](scope_and_non_goals.md)
- Evaluation: [`success_metrics_and_evaluation_protocol.md`](success_metrics_and_evaluation_protocol.md)
- Risk: [`risk_register_and_premortem.md`](risk_register_and_premortem.md)
- Kill/pivot triggers: [`falsification_and_kill_criteria.md`](falsification_and_kill_criteria.md)

This document answers only: *what is the problem, and what is the causal model?*

---

## 1. Problem Statement

In systematic investing, portfolio construction methods that rely on historical estimates of expected returns and covariance are highly sensitive to estimation error. Under realistic frictions such as transaction costs, this sensitivity produces unstable portfolio weights, excessive turnover, and degraded net-of-cost out-of-sample performance.

More precisely:

- Mean-variance optimization can amplify small input errors into large weight changes (Michaud, 1989).
- Historical means are noisy and often dominate covariance errors in portfolio optimization (Chopra & Ziemba, 1993).
- Many textbook and open-source treatments ignore or under-model transaction costs, which erode net returns and constrain capacity.
- Common remedies—constraints, shrinkage, turnover penalties—are often applied ad hoc, without systematic comparison or reproducible evaluation.
- Multiple testing across strategies can make the best in-sample result look better than it is out-of-sample.

The core problem is not that mean-variance optimization is mathematically wrong. It is that naive application treats noisy historical estimates as known parameters and ignores or under-models the cost of acting on those estimates.

### Formal decision problem

Given:

- An investable universe \( U \) of liquid assets.
- Historical data available up to time \( t \).
- A transaction cost model \( c(\Delta w) \).
- A risk model \( \Sigma \) and return estimate \( \mu \).
- Constraints on weights, turnover, leverage, and risk.

Choose a rebalancing policy \( \pi \) that maximizes expected net risk-adjusted return over a horizon:

\[
\max_{\pi} \mathbb{E}\left[ U(R_{\text{net}}) \mid \mathcal{F}_t \right]
\]

where \( R_{\text{net}} = R_{\text{gross}} - \text{costs} \), and \( U \) is a risk-adjusted utility such as net Sharpe ratio, expected shortfall-adjusted return, or a multi-period objective.

The decision problem is therefore not "find the optimal portfolio." It is:

> **How should a systematic investor construct and rebalance a portfolio to maximize net risk-adjusted return while controlling turnover, estimation error, and multiple-testing risk?**

---

## 2. Stakeholders and Decisions Affected

| Stakeholder | Context | Decision Affected | Value at Stake |
|---|---|---|---|
| Quantitative researcher | Designing allocation methods | Choice of estimator, optimizer, rebalancing rule | Research credibility, strategy robustness |
| Portfolio manager | Managing multi-asset portfolios | Rebalancing frequency, trade list, risk budget | Net returns, drawdown, capacity |
| Risk manager | Monitoring portfolio risk | Risk decomposition, stress testing | Tail risk, capital adequacy |
| Systematic fund | Running live strategies | Turnover control, cost budgeting | Transaction costs, slippage, capacity |
| Student / independent researcher | Building reproducible tools | Method selection, evaluation design | Learning, portfolio quality, career signaling |

The primary decision this project supports:

> **How should a systematic investor construct and rebalance a portfolio to maximize net risk-adjusted return while controlling turnover and estimation error?**

---

## 3. Why This Problem Matters

### 3.1 Economic Significance

- Transaction costs are real. A strategy with a modest gross Sharpe and high turnover can lose a material fraction of its risk-adjusted edge once costs are applied. The magnitude depends on turnover, cost per trade, and return volatility; it is not a constant. This is exactly what the project measures.
- Estimation error causes real capital to be misallocated and can lead to drawdowns that impair compounding.
- Capacity constraints mean even successful strategies degrade as assets under management grow.

### 3.2 Practical Relevance

- Many open-source portfolio optimization libraries focus on in-sample optimization or ignore costs entirely.
- Many student and research projects report gross Sharpe ratios without realistic cost assumptions, leading to overconfidence and non-reproducible claims.
- Practitioners need transparent, reproducible benchmarks to compare methods.

### 3.3 Base Rates and Prior Evidence

- A large fraction of published factor or portfolio strategies fail out-of-sample after costs (Harvey, Liu, & Zhu, 2016).
- Simple equal-weight (1/N) often outperforms complex optimization out-of-sample in historical studies (DeMiguel, Garlappi, & Uppal, 2009).
- These findings are priors, not universal laws. They suggest robustness is often the binding constraint, but the project should test where and why they hold.

---

## 4. Current Approaches and Their Limitations

| Approach | Description | Strengths | Limitations |
|---|---|---|---|
| Sample mean-variance optimization | Use historical means and covariance | Theoretically optimal if inputs are known | Extreme weights, high turnover, poor out-of-sample |
| Constraints (box, turnover) | Impose weight bounds | Simple, effective | Ad hoc, no principled choice of bounds |
| Shrinkage covariance | Ledoit-Wolf, factor models | Reduces covariance noise | Ignores expected return error |
| Bayesian expected returns | Black-Litterman, priors | Bayesian, intuitive | Requires view specification, still sensitive |
| Robust optimization | Optimize against worst-case inputs | Explicitly models uncertainty | Can be conservative, computationally heavier |
| Resampling / bootstrap | Simulate input uncertainty | Reduces overfitting | Can be slow, model-dependent |
| Risk parity | Equal risk contribution | Robust, no expected returns | Ignores return forecasts, can underperform |
| Turnover penalty | Add L1/L2 penalty to objective | Directly controls turnover | Requires tuning, may distort allocation |
| Multi-period optimization | Optimize over horizon with costs | Theoretically sound | Computationally heavy, model-dependent |

### 4.1 Hypothesized gap

**Hypothesis, not established fact.** No reproducible, open-source benchmark currently exists that systematically compares robust estimation, Bayesian expected returns, and turnover-aware optimization under realistic costs, walk-forward evaluation, and multiple-testing-aware metrics.

This is stated as a hypothesis to be tested, not as an assertion. It is the claim the project must validate in Phase 0 before proceeding. The test is a literature and tool scan; the failure mode is that an equivalent benchmark already exists, in which case the project pivots to replication or extension (see [`falsification_and_kill_criteria.md`](falsification_and_kill_criteria.md) §4 K3 and the Phase 0 gate in [`project_charter.md`](project_charter.md) §6).

---

## 5. Root Causes

Reduce the problem to its irreducible components:

1. **Uncertainty.** Future returns and covariances are unknown. Any estimate is a random variable with error.
2. **Optimization amplifies error.** The mean-variance objective is a quadratic function of inputs; small input errors can produce large weight changes.
3. **Frictions.** Trading costs real resources. Every rebalance trades off expected improvement against certain cost.
4. **Non-stationarity.** Return distributions change over time. Historical estimates may not represent the future.
5. **Multiple testing.** Researchers test many strategies; the best in-sample result is likely overfit.
6. **Objective mismatch.** Optimizing gross return or in-sample Sharpe can produce poor net-of-cost out-of-sample performance.

Any solution must address these fundamentals explicitly.

---

## 6. Causal Model

A simplified causal view of the problem:

```text
Historical Data ──► Covariance/Mean Estimates ──► Optimizer ──► Extreme/Unstable Weights
       │                   ▲                                      │
       │                   │                                      ▼
       └── Non-stationarity ┘                              High Turnover
                                                                  │
                                                                  ▼
                                                          Transaction Costs
                                                                  │
                                                                  ▼
                                                            Net Return ↓
```

**Key causal paths:**

- Historical data → noisy estimates → optimizer → unstable weights.
- Unstable weights → high turnover → costs → lower net returns.
- Non-stationarity → estimates become stale → further errors.
- Multiple testing → overfit strategy selection → inflated expectations → poor live performance.

**Assumptions:**

- Transaction costs are modeled as a function of turnover, initially fixed bps per trade.
- Market impact is out of scope for the core problem.
- Rebalancing is periodic, initially monthly.
- The investable universe is liquid and available point-in-time.

**Confounders and complications:**

- Market regime changes can affect both estimation error and transaction costs.
- Volatility clusters can make covariance estimates stale.
- Liquidity varies over time, so fixed cost assumptions are an approximation.
- Capacity constraints may matter at larger AUM.

**Interventions that could change outcomes:**

- Improve estimates: shrinkage, Bayesian priors, factor models.
- Constrain optimization: turnover penalty, weight bounds, risk budgets.
- Reduce rebalancing frequency.
- Model costs directly in the objective.
- Use walk-forward evaluation to detect overfitting.

This project intervenes primarily through improved estimation and turnover-aware optimization.

---

## 7. Systems View

Feedback loops, delays, and bottlenecks:

- **Reinforcing loop:** High turnover → high costs → lower returns → pressure to rebalance more to recover → higher turnover.
- **Balancing loop:** Turnover penalty → lower turnover → lower costs → higher net returns.
- **Delay:** Costs are incurred immediately; benefits of rebalancing may take months to materialize.
- **Bottleneck:** Estimation error and objective misspecification are primary bottlenecks. No amount of optimization can overcome bad inputs or a gross-return-only objective.
- **Leverage point:** Covariance shrinkage, Bayesian expected returns, and turnover penalties are high-leverage interventions because they directly address the bottleneck.

---

## 8. Uncertainty and Calibration

All estimates in this problem are probabilistic:

- **Prior:** Equal weight (1/N) is a robust prior that assumes no information.
- **Likelihood:** Historical data provides evidence about means and covariances, but with high noise.
- **Posterior:** Shrinkage and Bayesian estimators combine prior and likelihood to produce more stable estimates.
- **Calibration:** We must track whether confidence intervals for returns and risk are accurate.

The project treats all estimates as probabilistic and evaluates methods by out-of-sample calibration and net performance, not just point estimates.

---

## 9. Evaluation Contract (moved)

The evaluation contract — baselines, primary and secondary metrics, walk-forward protocol, success criteria, falsification criteria, and cost sensitivity levels — is defined authoritatively in:

> [`success_metrics_and_evaluation_protocol.md`](success_metrics_and_evaluation_protocol.md)

It is not duplicated here. Changes to evaluation thresholds or metrics are made in that document, not in this one. This stub is retained to preserve cross-references from other documents.

---

## 10. Scope and Boundaries (moved)

The authoritative definition of scope — Core MVP, extensions, and out-of-scope items — is:

> [`scope_and_non_goals.md`](scope_and_non_goals.md)

Scope is not duplicated here. Any conflict between this document and the scope document is resolved in favor of the scope document. This stub is retained to preserve cross-references.

---

## 11. Problem Validation Criteria

Before building the full solution, validate that the problem is real and worth solving. These are the Phase 1 gates, distinct from the Phase 0 gates in the charter.

1. **Literature and tool scan.** Covered by the Phase 0 gate in [`project_charter.md`](project_charter.md) §6. This section does not duplicate it.
2. **Simple experiments show sample MVO produces extreme weights and high turnover on the primary dataset.** This is the Phase 1 empirical gate (see also `falsification_and_kill_criteria.md` H1.1 and H1.2).
3. **Baselines such as 1/N and risk parity are robust and often competitive, confirming robustness is a key challenge.**
4. **A minimal turnover penalty reduces turnover without destroying net performance in preliminary tests.**
5. **The gap hypothesis in §4.1 is not falsified by the Phase 0 scan.** See [`falsification_and_kill_criteria.md`](falsification_and_kill_criteria.md) §4 K3.

If these criteria are not met, narrow, pivot, or stop per the kill/pivot triggers.

---

## 12. Failure Modes / Pre-Mortem (moved)

The failure-mode table and pre-mortem belong to the risk register, which is the living source of truth for this content:

> [`risk_register_and_premortem.md`](risk_register_and_premortem.md)

This section previously contained a strict subset of that register and would have drifted. It is not duplicated here. This stub is retained to preserve cross-references.

---

## 13. Value and Trade-offs

- **If successful:** A reusable open-source tool, a rigorous research contribution, and strong career signaling.
- **If unsuccessful:** A well-documented negative result and a validated backtesting framework.
- **Opportunity cost:** Time spent here is not spent on pure signal research, a backtesting toolkit, or regime detection.
- **Risk of ruin:** Low. The project risks time, not capital or reputation, provided claims are framed honestly. Phase gates limit wasted effort.

---

## 14. Feedback and Revision

- **Feedback source:** Out-of-sample results, sensitivity analyses, peer review, open-source issues.
- **Update trigger:** If baselines dominate all robust methods, reframe the problem as a diagnostic tool.
- **Iteration:** Revisit this document after baseline implementation and after the evaluation phase.
- **Learning loop:** Every major experiment should update priors about which interventions actually improve net risk-adjusted return.

---

## 15. References

- Bailey, D. H., & López de Prado, M. (2014). The Deflated Sharpe Ratio.
- Chopra, V. K., & Ziemba, W. T. (1993). The Effect of Errors in Means, Variances, and Covariances on Optimal Portfolio Choice.
- DeMiguel, V., Garlappi, L., & Uppal, R. (2009). Optimal Versus Naive Diversification.
- Harvey, C. R., Liu, Y., & Zhu, H. (2016). … and the Cross-Section of Expected Returns.
- Ledoit, O., & Wolf, M. (2004). A Well-Conditioned Estimator for Large-Dimensional Covariance Matrices.
- Markowitz, H. (1952). Portfolio Selection.
- Michaud, R. O. (1989). The Markowitz Optimization Enigma.

---

## 16. Revision History

| Date | Version | Change | Author |
|------|---------|--------|--------|
| 2026-10-13 | 1.0 | Initial problem framing | Ken Ira Lacson Talingting |
| 2026-10-14 | 2.0 | Expanded to full falsifiable problem contract | Ken Ira Lacson Talingting |
| 2026-10-15 | 2.1 | Qualified §3.1 Sharpe-erosion example; inverted §4 gap claim from assertion to hypothesis (§4.1); moved §9 (evaluation), §10 (scope), §12 (pre-mortem) to their authoritative documents and left stubs; trimmed §11 items 1 and 5 to pointers; added revision history | Ken Ira Lacson Talingting |

---

**End of problem framing.**
