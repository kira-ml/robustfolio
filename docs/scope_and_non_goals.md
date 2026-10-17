# Scope and Non-Goals: robustfolio

**Version:** 1.4
**Status:** Active — owner-activated 2026-10-17 (DEC-20261017-021); v1.4 clarifies the MVP robust-method set (DEC-20261017-022)
**Owner:** Ken Ira Lacson Talingting
**Created:** 2026-10-14
**Last Updated:** 2026-10-17
**Supersedes:** 1.3 (activation at the protocol freeze; `[PROPOSED]` defaults confirmed) and earlier
**Related:** [`problem_framing.md`](problem_framing.md), [`evaluation_protocol.md`](evaluation_protocol.md), [`decision_log.md`](decision_log.md), [`risk_register_and_premortem.md`](risk_register_and_premortem.md)

---

## 0. Purpose of This Document

This document is the **authoritative definition of what `robustfolio` is and is not**. It exists to:

1. Establish a single source of truth for scope.
2. Prevent scope creep by defining explicit boundaries.
3. Define the tri-level structure: **Core MVP**, **Extensions**, and **Out of Scope**.
4. Specify the amendment process for changing scope.
5. Resolve conflicts between other documents that mention scope.

Any document that disagrees with this one on scope is either outdated or wrong. When in conflict, this document wins unless this document is itself amended.

---

## 1. Scope Philosophy

Three principles govern scope decisions.

1. **Narrow by default, widen deliberately.** Every additional asset class, method, or frequency multiplies the surface area for bugs and overfitting. The default answer to "should we add X?" is no.
2. **MVP is what completes a loop.** The MVP must be able to run a full walk-forward, net-of-cost, multiple-testing-adjusted evaluation on at least one baseline and one robust method. Nothing else is required to demonstrate or falsify the project's hypothesis.
3. **Extensions are earned, not assumed.** An extension enters scope only if the MVP is complete and the extension is justified by a pre-registered hypothesis in [`evaluation_protocol.md`](evaluation_protocol.md) §12.

A scope that grows without amendment is scope creep, even if each addition looks reasonable in isolation. [Systems]

---

## 2. Tri-Level Scope Structure

Scope is defined at three levels. The distinction matters because different levels have different rules for what is allowed.

| Level | Definition | Change process |
|-------|-----------|----------------|
| **Core MVP** | Required to complete Phase 1–4 | Locked once this document is Active |
| **Extensions** | Optional, only after MVP; require pre-registered hypothesis | Added via amendment + decision log entry |
| **Out of Scope** | Explicitly excluded; requires an amendment to this document and `evaluation_protocol.md` §8 | Amendment + version bump + decision log entry |

Everything not listed in Core MVP or Extensions is Out of Scope by default.

---

## 3. Core MVP

The MVP is the minimum sufficient implementation to test the project's primary hypothesis ([`problem_framing.md`](problem_framing.md) §1). It is frozen when this document becomes Active.

### 3.1 Universe

| Dimension | MVP value |
|-----------|-----------|
| Asset class | US-listed ETFs spanning equity, fixed income, commodities, real estate |
| Candidate universe size | Point-in-time candidate list, target 15–25 liquid ETFs (reconstructed per [`evaluation_protocol.md`](evaluation_protocol.md) §5.4.7) |
| Minimum history at backtest start | 60 months (frozen in [`evaluation_protocol.md`](evaluation_protocol.md) §5.4.2) |
| Currency | USD only |
| Instrument type | Long-only, unlevered ETFs |
| Delisted assets | Retained through delisting date; delisting return included |

### 3.2 Data

| Dimension | MVP value |
|-----------|-----------|
| Frequency | Daily prices, monthly decisions |
| Source | Per [`evaluation_protocol.md`](evaluation_protocol.md) §5.4.1 |
| Point-in-time discipline | Mandatory per [`evaluation_protocol.md`](evaluation_protocol.md) §5.4.3 |
| Risk-free rate | 1-month T-bill, FRED DGS1MO (per §5.4.1 and §5.5.5) |

### 3.3 Rebalance

| Dimension | MVP value |
|-----------|-----------|
| Frequency | Monthly |
| Rebalance date | Last trading day of the month |
| Execution | Close of rebalance date |
| Signal timing | Data through close of rebalance date |

### 3.4 Covariance estimators

| Estimator | Status |
|-----------|--------|
| Sample covariance | MVP |
| Ledoit-Wolf shrinkage | MVP |

### 3.5 Expected return estimators

| Estimator | Status |
|-----------|--------|
| Sample mean | MVP (for B3, B5) |
| Equal / none | MVP (for B1, B2, B4) |
| Black-Litterman | MVP — no-views (equilibrium-prior) variant, defined in [`model_and_method_spec.md`](model_and_method_spec.md) §4.5 |

### 3.6 Optimizers / constructors

| Method | MVP status |
|--------|------------|
| Equal weight (1/N) | MVP |
| Risk parity (ERC) | MVP |
| Sample MVO | MVP |
| Minimum variance | MVP |
| Turnover-penalized MVO (L1) | MVP |

**MVP methods (the full set).** The five constructors above define the baselines **B1–B5**. The MVP *robust methods* are the single-factor treatments built on them: **M1** = Ledoit-Wolf shrinkage covariance + sample-mean MVO (tests H2.1); **M2** = sample covariance + Bayesian/Black-Litterman posterior returns (tests H2.2). Both are defined exactly in [`model_and_method_spec.md`](model_and_method_spec.md) §1. The §3.4 Ledoit-Wolf estimator and the §3.5 Black-Litterman estimator were **not** promoted to the baseline set — the baseline set stays B1–B5 — but they are MVP *robust-method* components, not extensions. This is the clarification of finding F9 (DEC-20261017-022).

### 3.7 Turnover penalties

| Penalty | MVP status |
|---------|------------|
| L1 (proportional to trade size) | MVP |
| L2 (quadratic) | Extension |

### 3.8 Evaluation

| Component | MVP status |
|-----------|------------|
| Walk-forward | MVP |
| Purged cross-validation + embargo | MVP |
| Net-of-cost Sharpe at all cost levels | MVP (cost levels defined in [`evaluation_protocol.md`](evaluation_protocol.md) §5.5.3) |
| Deflated Sharpe ratio | MVP |
| Probabilistic Sharpe ratio | MVP |
| Block bootstrap confidence intervals | MVP |
| Cost sensitivity bands | MVP (levels defined in [`evaluation_protocol.md`](evaluation_protocol.md) §5.5.3) |

### 3.9 Reporting

| Component | MVP status |
|-----------|------------|
| Gross vs net, in-sample vs OOS labels | MVP |
| Confidence intervals | MVP |
| Sensitivity analysis | MVP |
| Negative-result reporting | MVP |
| Reproducible report generation | MVP |

**MVP completion criterion:** A single command produces a reproducible report comparing all MVP baselines and at least one MVP robust method, across all cost levels, with all MVP metrics, on the MVP universe.

---

## 4. Extensions

Extensions are permitted only after MVP completion and require a pre-registered hypothesis. They are not in scope by default.

> **Confirmed at activation (2026-10-17).** Extension prioritization is fixed; adding an extension still requires the §4.3 entry criteria.

### 4.1 Tier A extensions (low cost, high value)

| Extension | Justification | Cost |
|-----------|--------------|------|
| PCA factor covariance | Alternative to Ledoit-Wolf; tests whether dimensionality reduction matters | Low |
| CVaR optimization | Tests robustness of turnover-aware methods under a tail-risk objective | Low-mid |
| L2 turnover penalty | Compares L1 vs L2 in cost alignment | Low |
| Inverse-volatility weights | Simple baseline complement to risk parity | Low |
| Hierarchical risk parity | Modern alternative; tests clustering-based robustness | Mid |

### 4.2 Tier B extensions (higher cost, useful but not required)

| Extension | Justification | Cost |
|-----------|--------------|------|
| Multi-period optimization | Tests whether dynamic optimization beats single-period | High |
| Regime detection | Tests whether regime-conditional allocation helps net of costs | High |
| Alternative rebalancing frequencies (quarterly, biweekly) | Tests sensitivity to rebalance cadence | Mid |
| Additional asset classes (international ETFs, sector ETFs) | Tests generality | Mid-high |
| Simplified market impact model | Tests whether cost-aware optimization survives nonlinear costs | Mid |

### 4.3 Extension entry criteria

For any extension to enter scope:

1. MVP is complete (Phase 4 gate passed, per [`evaluation_protocol.md`](evaluation_protocol.md) §8.4).
2. A pre-registered hypothesis exists in the experiment registry ([`decision_log.md`](decision_log.md) Appendix A, rules in [`evaluation_protocol.md`](evaluation_protocol.md) §12).
3. The extension does not violate any non-goal in §5.
4. A decision log entry is created with rationale and prior expected value.
5. This document is amended with a version bump.

**Extensions that do not meet these criteria are out of scope, regardless of how promising they look.** [Inversion]

---

## 5. Out of Scope

Explicitly excluded. Adding any of these requires an amendment to this document and to [`evaluation_protocol.md`](evaluation_protocol.md) §8, not merely a scope amendment.

### 5.1 Asset classes and instruments

- High-frequency or intraday trading.
- Options, futures, swaps, or any derivative instrument.
- Short positions or leverage.
- Cryptocurrencies.
- Individual corporate bonds or credit instruments.
- Private markets, real assets, or illiquid instruments.
- FX trading as a standalone strategy.

### 5.2 Frequencies and horizons

- Intraday signals.
- Weekly or daily rebalancing as a primary frequency.
- Multi-decade horizon studies.

### 5.3 Data and signals

- Proprietary alpha signals.
- Alternative data (satellite, text, sentiment).
- Factor timing or macro forecasting.
- Machine-learning return predictors beyond standard estimators (e.g., neural nets for μ).

### 5.4 Execution and infrastructure

- Live trading or execution systems.
- Broker integration.
- Realistic market impact modeling (Almgren-Chriss or order-book models).
- Capacity constraints as a function of AUM.
- Tax-aware optimization.

### 5.5 Claims and products

- Beating the market or maximizing absolute return.
- Market timing.
- Wealth management advice.
- A commercial portfolio optimizer.
- A general-purpose backtesting framework for all asset classes.

### 5.6 Governance

- Multi-user collaboration features.
- Public API for third parties.
- Enterprise deployment.

**Reading this list carefully is itself a project survival mechanism.** Most solo projects fail because they quietly drift into one of these territories. [Inversion]

---

## 6. Scope Conflict Resolution

Other documents in `docs/` mention scope. This section defines how conflicts are resolved.

| Conflicting document | Resolution |
|---------------------|-----------|
| [`problem_framing.md`](problem_framing.md) §10 | Now a stub pointing here. No conflict. |
| [`evaluation_protocol.md`](evaluation_protocol.md) §4.2 | Baseline set is defined there; whether each is MVP or extension is defined here. |
| [`evaluation_protocol.md`](evaluation_protocol.md) §5.5.3 | Cost levels are defined there. Scope marks cost sensitivity as MVP; the numeric levels are that section's authority. |
| [`evaluation_protocol.md`](evaluation_protocol.md) §8 | Phase gates and time-boxes are defined there. Scope does not override them. |
| Any new document | Must not contradict this document. If it does, either this document or the new document is wrong. |

**Rule:** Scope questions are answered here, not in the other documents. Other documents may *reference* scope but may not *define* it.

---

## 7. Scope Creep Detection

Signals that scope is creeping, and the correct response.

| Signal | Interpretation | Response |
|--------|---------------|----------|
| A new method appears in code before Phase 2 gate | Silent scope expansion | Halt; register experiment or remove method |
| A new asset class appears in a backtest | Out-of-scope universe | Halt; revert or amend this document and §5 of [`evaluation_protocol.md`](evaluation_protocol.md) §5.4 |
| A new metric appears in a report | Undisclosed scope change | Report as exploratory; register future trial |
| A new frequency appears in comparison | Out-of-scope frequency | Remove; if pursued, register as extension |
| The "MVP" section of a report describes more than the MVP here | Definition drift | Freeze report; compare against this document |
| The owner says "let me just add..." | Classic scope creep | Apply §4.3 entry criteria or decline |

**Rule:** Any of these signals is a decision log entry, even if the decision is to decline the change. Silent scope drift is a project-level risk (see [`risk_register_and_premortem.md`](risk_register_and_premortem.md) R-P03).

---

## 8. What Causes This Document to Change

- An amendment to §8 of [`evaluation_protocol.md`](evaluation_protocol.md) that changes the mission or non-goals.
- A decision to promote an extension into the MVP (unusual; requires justification).
- A decision to demote an MVP item to an extension (also unusual; requires justification).
- A validated finding that an out-of-scope item is actually required for the MVP loop.

Any change:

1. Requires a decision log entry.
2. Requires a version bump.
3. Requires updating all documents that reference scope.
4. Must not weaken the phase-gate discipline established in [`evaluation_protocol.md`](evaluation_protocol.md) §8.4.

---

## 9. Model Tags Applied

- **[First Principles]** — Reduced scope to the minimum sufficient implementation to test the primary hypothesis.
- **[Inversion]** — Defined out-of-scope items and scope-creep signals before defining MVP success.
- **[Information Theory]** — Consolidated overlapping scope definitions into one authoritative source; superseded duplicates.
- **[Systems]** — Tri-level structure, entry criteria for extensions, conflict-resolution rules, creep-detection signals.
- **[Learning Loop]** — Scope changes feed the decision log; creep signals feed the risk register.

---

## 10. Owner Action Checklist Before Activating

Before setting Status to `Active`:

- [x] Section 3.1: confirm asset class, universe size, and minimum history
- [x] Section 3.4–3.7: confirm which methods are MVP vs extension
- [x] Section 4.1–4.2: confirm or reorder the extension tiers
- [x] Section 5: confirm the out-of-scope list is complete and acceptable
- [x] Section 6: confirm other documents reference this one and do not redefine scope

Also confirm:

- [x] You accept that everything not in Core MVP or Extensions is out of scope by default.
- [x] You accept the extension entry criteria (§4.3).
- [x] You accept the scope-creep detection signals (§7) and will act on them.
- [x] Cost levels are confirmed in [`evaluation_protocol.md`](evaluation_protocol.md) §5.5.3, not here.
- [x] `problem_framing.md` §10 is a stub pointing here (completed 2026-10-15).

**Activated 2026-10-17.** Version 1.3; Status `Active`.

---

## 11. Revision History

| Date | Version | Change | Author |
|------|---------|--------|--------|
| 2026-10-14 | 1.0 | Initial scope and non-goals document | Ken Ira Lacson Talingting |
| 2026-10-15 | 1.1 | Replaced §3.8 cost-level row with pointer to cost model doc §3.3 (A6); updated §6 conflict table to reflect supersessions; updated §10 checklist to reflect completed supersessions; added revision history | Ken Ira Lacson Talingting |
| 2026-10-15 | 1.2 | Updated all cross-references to retired documents per DEC-20261015-018: `project_charter.md`, `benchmark_and_baseline_spec.md`, `success_metrics_and_evaluation_protocol.md`, `falsification_and_kill_criteria.md`, `cost_model_and_frictions.md`, and `experiment_registry_and_preregistration.md` redirected to `evaluation_protocol.md` sections. §3.2 point-in-time reference redirected to §5.4.3. §4.3 registry reference redirected to `decision_log.md` Appendix A and `evaluation_protocol.md` §12. §6 conflict table rewritten. §8 charter reference redirected to §8 of the protocol. No scope content changed. | Ken Ira Lacson Talingting |
| 2026-10-17 | 1.3 | **Activated** at the protocol freeze (DEC-20261017-021). §3.1 `[PROPOSED]` defaults confirmed and aligned with the frozen protocol (universe = point-in-time list per §5.4.7; minimum history 60 months). §4 note de-proposed. §10 activation checklist completed. Status `Draft` → `Active`. | Ken Ira Lacson Talingting |
| 2026-10-17 | 1.4 | Clarified the MVP method set (finding F9, DEC-20261017-022). §3.5 Black-Litterman row reworded to "MVP — no-views (equilibrium-prior) variant" and pointed at `model_and_method_spec.md` §4.5. Added a §3.6 note naming the MVP robust methods (M1 shrinkage MVO, M2 Bayesian/B-L MVO) and stating they are MVP components, not the baseline set (B1–B5). Resolves the scope-vs-protocol-§4.2 contradiction in scope's favour (scope §6). No MVP/extension status changed. | Ken Ira Lacson Talingting |

---

*This document exists to keep the project small enough to finish and honest enough to trust. Scope is a constraint, not a wish list.*
