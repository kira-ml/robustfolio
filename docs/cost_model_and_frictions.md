# Cost Model and Frictions: robustfolio

**Version:** 1.0  
**Status:** Draft — pending owner confirmation of proposed defaults; freeze before first backtest  
**Owner:** Ken Ira Lacson Talingting  
**Created:** 2026-10-14  
**Last Updated:** 2026-10-14  
**Supersedes:** None  
**Related:** [`problem_framing.md`](problem_framing.md), [`project_charter.md`](project_charter.md), [`success_metrics_and_evaluation_protocol.md`](success_metrics_and_evaluation_protocol.md), [`data_contract_and_point_in_time_policy.md`](data_contract_and_point_in_time_policy.md), [`falsification_and_kill_criteria.md`](falsification_and_kill_criteria.md), [`benchmark_and_baseline_spec.md`](benchmark_and_baseline_spec.md)

---

## 0. Purpose of This Document

This document defines **exactly how trading frictions are modeled** in every experiment. It specifies:

1. What frictions are in scope and what is out of scope.
2. The cost model formula and its parameters.
3. Execution timing assumptions.
4. How costs enter the objective function and the performance measurement.
5. Sensitivity ranges used for robustness checks.
6. What invalidates a net-of-cost result.

It is the **contract** between turnover and reported performance. Without it, "net-of-cost" is unmeasurable. Violations invalidate results (see `falsification_and_kill_criteria.md` §4 K6).

**Once frozen, this document may not be modified after seeing experimental results.** Any change requires a decision log entry and a version bump.

---

## 1. Frictions Philosophy

Three principles govern all cost decisions:

1. **Costs are certain; rebalancing benefits are not.** A rebalance pays cost today for an uncertain future benefit. The model must make this asymmetry explicit.
2. **Simple, conservative, transparent.** A fixed-bps model is preferred over a complex impact model. Where the model is wrong, it should be wrong in the conservative direction (overestimate costs, not underestimate).
3. **Sensitivity over precision.** We do not know the true cost. We report results across a range of cost levels, and a robust method is one whose advantage survives across the range.

A strategy that only works at zero cost is not a strategy. A strategy whose advantage shrinks monotonically with costs but survives at realistic levels is honest.

---

## 2. Scope

### 2.1 In scope

| Friction | Modeled? | Notes |
|----------|----------|-------|
| Commissions | Yes | Fixed bps per trade |
| Bid-ask spread | Yes | Fixed bps per trade; can be separated |
| Slippage | Yes | Fixed bps per trade, conservative |
| Market impact | Simplified | Included only as an optional size-dependent term |
| Tax | No | Out of scope; documented as limitation |
| Financing / borrow | No | Long-only, no leverage in MVP |
| Foreign exchange | No | USD-denominated universe only |
| Operational overhead | No | Not a per-trade friction |

### 2.2 Out of scope (explicitly)

- Realistic market impact curves (Almgren-Chriss, square-root, etc.).
- Order book dynamics.
- Intraday execution modeling.
- Tax optimization.
- Short-selling borrow costs.
- Custody fees, fund expense ratios (documented separately if relevant).
- Capacity constraints from AUM.

These exclusions are intentional. They keep the project feasible and focused on the core problem. Any attempt to add them requires a charter amendment and a new experiment.

---

## 3. Cost Model

### 3.1 Base model — proportional cost

For each asset \( i \) at rebalance time \( t \), the traded notional is:

\[
\text{Trade}_i(t) = |w_i(t) - w_i(t^-)| \cdot \text{AUM}
\]

where \( w_i(t^-) \) is the post-return weight from the previous period (drifted weight) and \( w_i(t) \) is the target weight.

The proportional cost for asset \( i \) at time \( t \) is:

\[
c_i(t) = \kappa \cdot |w_i(t) - w_i(t^-)|
\]

where \( \kappa \) is the one-way cost rate in basis points per unit of turnover.

Total portfolio cost at time \( t \):

\[
C(t) = \sum_i c_i(t)
\]

Net return:

\[
R_{\text{net}}(t) = R_{\text{gross}}(t) - C(t)
\]

### 3.2 Turnover definition

Turnover at time \( t \) (one-way, portfolio-level):

\[
\text{Turnover}(t) = \sum_i |w_i(t) - w_i(t^-)|
\]

Annualized turnover is the sum of monthly turnover over 12 months. Both one-way and two-way definitions exist; this project uses **one-way** throughout. Any use of two-way must be labeled.

### 3.3 Cost parameter \( \kappa \)

> **Note:** The following values are **proposed conservative defaults**. Confirm or replace before freezing.

| Cost level | \( \kappa \) (one-way bps) | Purpose |
|------------|---------------------------|---------|
| Zero | 0 | Diagnostic only |
| Low | 5 | Best-case realistic |
| Baseline | 10 | Primary cost assumption |
| High | 20 | Stress case |
| Extreme | 50 | Robustness boundary |

**Baseline \( \kappa = 10 \) bps** is the primary assumption. All headline results are reported at this level. Other levels are reported as sensitivity bands.

### 3.4 Optional size-dependent term

If the owner wishes to include a simplified market impact term, it takes the form:

\[
c_i(t) = \kappa \cdot |\Delta w_i| + \lambda \cdot \text{ADV-ratio}_i \cdot |\Delta w_i|^{3/2}
\]

where `ADV-ratio` is the trade notional divided by average daily volume. This term is **off by default** in MVP. If enabled, it must be documented in the experiment registry and reported as a separate result, not mixed into the baseline.

---

## 4. Execution Timing Assumptions

Timing affects both returns and costs. The following are fixed across all methods.

### 4.1 Rebalance schedule

- Rebalance frequency: monthly (baseline).
- Rebalance date: last trading day of the month.
- Signal computation: based on data through the close of the rebalance date.

### 4.2 Execution price

`[PROPOSED]`: Execution at the **close of the rebalance date**. Alternative: open of the next trading day.

Rationale: close-of-day execution is simpler, matches monthly rebalance conventions, and avoids an extra day of price uncertainty. The choice must be consistent across all methods and documented in every experiment registry entry.

### 4.3 Cost application

Costs are applied at the rebalance date, deducted from that period's return:

\[
R_{\text{net}}(t) = R_{\text{gross}}(t) - \sum_i \kappa \cdot |w_i(t) - w_i(t^-)|
\]

### 4.4 Drifted weights

Between rebalances, weights drift with returns. The pre-rebalance weight \( w_i(t^-) \) is:

\[
w_i(t^-) = \frac{w_i(t-1) \cdot (1 + r_i(t))}{\sum_j w_j(t-1) \cdot (1 + r_j(t))}
\]

This must be computed correctly. A common bug is to treat pre-rebalance weights as equal to post-rebalance weights from the prior period, which understates turnover and costs.

---

## 5. Cost-Aware Objective Function

### 5.1 Baseline objective

The unpenalized mean-variance objective:

\[
\max_w \ w^\top \mu - \frac{\gamma}{2} w^\top \Sigma w
\]

ignores costs entirely. This is the critique target.

### 5.2 Turnover-penalized objective

The penalized objective:

\[
\max_w \ w^\top \mu - \frac{\gamma}{2} w^\top \Sigma w - \lambda \| w - w^- \|_1
\]

where \( \lambda \) is the turnover penalty in return units and \( \| \cdot \|_1 \) is the L1 norm.

**Equivalence to cost model:**

Under the proportional cost model, \( \lambda = \kappa \) aligns the penalty with the actual cost in return units. In practice, \( \lambda \) may be tuned above \( \kappa \) to account for uncertainty, market impact, or model risk.

### 5.3 L2 penalty variant

The L2 variant:

\[
\max_w \ w^\top \mu - \frac{\gamma}{2} w^\top \Sigma w - \lambda \| w - w^- \|_2^2
\]

is included as an extension. L2 penalizes large trades more than small trades, which is a different economic assumption from proportional cost. Reporting must label which penalty is used.

### 5.4 Cost-aware vs cost-penalized

Two distinct approaches exist:

1. **Cost-aware:** Model costs explicitly and subtract them from returns.
2. **Cost-penalized:** Add a penalty term to the objective, which indirectly controls turnover.

Both are in scope. Each must be labeled clearly. A method that is cost-aware but uses cost-penalized language (or vice versa) is mislabeled and will be flagged in review.

---

## 6. Sensitivity Analysis

Every method is evaluated across the 5 cost levels in §3.3. Reporting requirements:

1. **Primary result** at 10 bps.
2. **Sensitivity band** across 0–50 bps.
3. **Break-even cost** at which the method loses its advantage over the best baseline.
4. **Monotonicity check:** Does net Sharpe decline monotonically with cost? Non-monotonicity signals a bug or an artifact.

A robust method has a break-even cost above the baseline assumption (10 bps) and, ideally, above the stress case (20 bps).

---

## 7. Cost Model Limitations

Explicitly acknowledged:

- **Fixed bps is not reality.** Real costs vary by asset, size, time of day, and market conditions.
- **No market impact curve.** Large trades in illiquid assets will be underestimated.
- **No intraday dynamics.** Execution at close ignores intraday price paths.
- **No capacity model.** AUM is not varied in MVP; all results are per-unit-notional.
- **No regime dependence.** Costs are assumed constant across volatility regimes.
- **No tax.** After-tax performance is not measured.

These limitations do not invalidate the model, but they bound the claims. Any claim about real-world profitability beyond the modeled frictions must be explicitly qualified.

---

## 8. What Invalidates a Net-of-Cost Result

An experiment's net-of-cost result is invalidated if any of the following occurred:

- Costs were not applied to drifted weights (§4.4).
- Different cost levels were applied inconsistently across methods.
- Turnover was reported as two-way but compared against a one-way cost model.
- The cost parameter \( \kappa \) differs across methods without justification.
- The execution price assumption differs across methods.
- Cost-penalized and cost-aware methods were compared without labeling.
- Sensitivity analysis was skipped or reported selectively (e.g., only at the level that flattered the method).
- Market impact was included in one method but not in the baseline without disclosure.

Invalidated results are documented and not deleted.

---

## 9. Reporting Requirements

Every experiment result must report:

1. Cost model used (proportional, optional impact, or both).
2. \( \kappa \) at each cost level, with primary level flagged.
3. Execution timing assumption.
4. Gross Sharpe and net Sharpe at each cost level.
5. Turnover (one-way, annualized).
6. Cost drag (gross Sharpe minus net Sharpe, annualized).
7. Break-even cost vs the best baseline.
8. Monotonicity check result.
9. Any optional features enabled or disabled.

See `success_metrics_and_evaluation_protocol.md` §9 for the general reporting template.

---

## 10. Model Tags Applied

- **[First Principles]** — Reduced frictions to a proportional cost model with explicit parameters.
- **[Inversion]** — Defined invalidation rules and limitation acknowledgments before defining success.
- **[Experimental]** — Fixed execution timing, sensitivity bands, monotonicity checks, pre-registration.
- **[Systems]** — Turnover-penalty vs cost-aware distinction; drifted weight computation; objective alignment.
- **[Bayesian]** — Sensitivity ranges propagate into claim confidence; break-even cost as decision input.
- **[Information Theory]** — Compressed to formula, parameters, and rules; no filler.

---

## 11. Owner Action Checklist Before Freezing

Before setting Status to `Frozen`, confirm or replace every `[PROPOSED]` value:

- [ ] Section 3.3: confirm baseline \( \kappa \) and cost level set
- [ ] Section 3.4: decide whether to include size-dependent impact term in MVP (default: off)
- [ ] Section 4.1: confirm rebalance frequency and date
- [ ] Section 4.2: confirm execution price assumption (close vs next open)
- [ ] Section 5.2: confirm whether \( \lambda = \kappa \) or a tuned value will be used
- [ ] Section 5.3: decide whether L2 penalty is in MVP or extension
- [ ] Section 6: confirm sensitivity analysis is mandatory in every experiment

Also confirm:

- [ ] The cost levels in §3.3 are consistent with the evaluation protocol §5.5.
- [ ] The execution timing assumption is consistent with the data contract §4.3.
- [ ] You accept the limitations in §7 and will qualify claims accordingly.

Once confirmed, bump to Version 1.1, set Status to `Frozen`, and add a revision history row.

---

## 12. Revision History

| Date | Version | Change | Author |
|------|---------|--------|--------|
| 2026-10-14 | 1.0 | Initial cost model and frictions document | Ken Ira Lacson Talingting |

---

*This document exists to make "net-of-cost" a measurement rather than a claim. A strategy whose edge disappears at realistic costs is a strategy whose edge is not real.*
