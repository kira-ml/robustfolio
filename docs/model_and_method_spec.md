# Model and Method Specification: robustfolio

**Version:** 1.0
**Status:** Draft — written 2026-10-17 (execution TODO item C2). This document must be `Frozen` (item C3) before Gate 1 may be entered.
**Owner:** Ken Ira Lacson Talingting
**Created:** 2026-10-17
**Last Updated:** 2026-10-17
**Related:** [`evaluation_protocol.md`](evaluation_protocol.md) (v2.4, Frozen — the measurement contract), [`scope_and_non_goals.md`](scope_and_non_goals.md) (v1.4, Active — the scope authority), [`problem_framing.md`](problem_framing.md), [`risk_register_and_premortem.md`](risk_register_and_premortem.md), [`decision_log.md`](decision_log.md)

> **What this document is.** The frozen evaluation protocol defines *what counts as success*. This document defines *exactly what gets computed* to produce those numbers: the methods, estimators, optimizers, walk-forward harness, cost application, and metric formulas. It is the artifact that DEC-20261017-019 finding F7 (metric implementations) was deferred to.
>
> **What this document is not.** It owns no scope (that is [`scope_and_non_goals.md`](scope_and_non_goals.md) §6) and no threshold (§§6, 7, 12, 13 of the protocol). No number in this document is a new success criterion; every threshold here is quoted from the protocol with a source tag.

---

## 0. Authority, conflict resolution, and status

Three documents meet here. The rule is fixed and directional:

| Question | Authority | This document's role |
|----------|-----------|----------------------|
| Is method *M* in scope (MVP vs extension)? | [`scope_and_non_goals.md`](scope_and_non_goals.md) (§6) | Operationalize the MVP set; never widen it |
| What counts as success; which thresholds; which metrics must be reported? | [`evaluation_protocol.md`](evaluation_protocol.md) (§§2–7, 12–13) | Implement exactly; never redefine or relax |
| How is each method/estimator/optimizer/metric computed? | **This document** | Define precisely enough to be reproduced |

If this document and the protocol disagree on a *value*, the protocol wins. If this document and scope disagree on *classification*, scope wins. A disagreement is a defect in this document, not a licence to pick.

**Status discipline.** This is `Draft`. Items marked `[OPEN]` must be resolved before `Frozen` (C3). `[OPEN]` items are spec-level implementation choices that the protocol and scope deliberately left to this document; they are not scope or threshold changes.

**Resolution of finding F9 (logged DEC-20261017-022).** The frozen protocol §4.2 previously listed "shrinkage covariance + minimum variance" and "Black-Litterman" as *extensions*, while [`scope_and_non_goals.md`](scope_and_non_goals.md) §3.4/§3.5 mark them `MVP`. Scope §6 makes scope authoritative on classification. MVP therefore includes the shrinkage-covariance and Bayesian-return **robust methods**, and §4.2 of the protocol now points to scope §4 for the extension list (protocol v2.3 → v2.4; a §16 pre-result correction). This is required for Family H2 to be testable: H2.1 and H2.2 are Phase 2 hypotheses, and an "extension" cannot run until Gate 4.

---

## 1. Method set and identifier scheme

Two kinds of object exist: **baselines** (the null; protocol §4.2, IDs `B1`–`B5`) and **robust methods** (the treatments; IDs `M1`, `M2`, …). A method is fully specified by the triple *(expected-return estimator, covariance estimator, constructor)*. Baselines and robust methods differ in exactly one component wherever they are compared (protocol §4.6; resolves DEC-20261017-019 F4).

| ID | Name | μ estimator | Σ estimator | Constructor | Role | Hypothesis |
|----|------|-------------|-------------|-------------|------|------------|
| **B1** | Equal weight (1/N) | none | none | w = 1/N | Primary benchmark (protocol §4.4) | H1.1, H1.2, H2.4 |
| **B2** | Risk parity (ERC) | none | sample | ERC | Practitioner default | H2.4 |
| **B3** | Sample MVO | sample mean | sample | MVO | The critique target | H1.1, H2.1–H2.4 |
| **B4** | Minimum variance | none | sample | min-var | Classical robust alternative | H2.4 |
| **B5** | Turnover-penalized MVO (L1) | sample mean | sample | MVO + L1 | Strongest simple robust baseline | H2.3, H2.4 |
| **M1** | Shrinkage-covariance MVO | sample mean | **Ledoit-Wolf** | MVO | Shrinkage treatment | **H2.1** |
| **M2** | Bayesian (Black-Litterman) MVO | **B-L posterior** | sample | MVO | Bayesian-return treatment | **H2.2** |

**Design rule.** M1 differs from B3 *only* in Σ; M2 differs from B3 *only* in μ. This is what makes H2.1 and H2.2 single-factor tests rather than confounded comparisons.

**Not in MVP** (extensions per scope §4; require a pre-registered experiment and Gate 4): inverse-volatility weights, hierarchical risk parity, PCA factor covariance, CVaR optimization, L2 turnover penalty, equal-risk-budget-with-views, tuned-λ variants, market-impact-enabled variants. The Phase 1 script's `inverse_vol` method stays in the codebase only as an extension candidate and **must not appear in the MVP comparison table** (DEC-20261017-019 F2).

---

## 2. Shared configuration (frozen values, cited not redefined)

Every method uses these values. They are read from the protocol; this table exists so the implementation has one source of truth in code.

| Parameter | Value | Source |
|-----------|-------|--------|
| Universe | point-in-time candidate list, target 15–25 US ETFs | protocol §5.4.2, §5.4.7; scope §3.1 |
| Minimum history at entry | 60 consecutive months | protocol §5.4.2 |
| Eligibility | ≥ 60 months history **and** trailing-3-month ADV > $5M **and** valid positive price | protocol §5.4.2 |
| Estimation window | 60 months, **rolling**, re-estimated monthly | protocol §5.2 |
| Test window / step | 12 months / 12 months, non-overlapping | protocol §5.2 |
| Rebalance | monthly, last trading day | protocol §5.4.3, §5.5.4 |
| Constraints | Σw = 1; 0 ≤ w_i ≤ `w_max` = 0.30, **uniform across all methods** | protocol §4.3 |
| Risk aversion | γ = 10 (B3, B5, M1, M2) | protocol §4.3 |
| Turnover penalty | λ = κ = 0.001 (monthly return per unit one-way turnover) | protocol §4.4 B5, §5.5.6 |
| Cost levels κ | 0, 5, 10 (**headline**), 20, 50 bps one-way | protocol §5.5.3 |
| Risk-free rate | 1-month T-bill; forward-fill ≤ 1 month then FRED `DGS1MO`; **never zero** | protocol §5.4.6, §5.5.5 |
| R_f convention | same series for gross and net Sharpe | protocol §2, §5.5.5 |
| Execution | signals through close of *t−1*; execute at that close; hold month *t* | protocol §5.5.4 |
| Bootstrap | stationary block, mean block 6, B = 2000, 90% reporting / 95% decision | protocol §13.1 |

**Feasibility note.** The cap is feasible for every method because N · `w_max` ≥ 1 for any candidate universe of size N ≥ 4 (target ≥ 15). The implementation asserts this at startup; an infeasible configuration is a hard error, not a silent fallback (contrast the Phase 1 SLSQP fallback, DEC-20261015-016).

---

## 3. Data pipeline (point-in-time)

Implements protocol §5.4. The data layer is the only place vendor specifics may appear (protocol §5.4.1).

### 3.1 Snapshot contract

A snapshot is immutable and lives under `data/snapshots/<snapshot_id>/` with `<snapshot_id> = <source>-<asset_class>-<start>_<end>-<retrieval_date>-<hash8>` (protocol §5.4.9). It contains:

```
data/snapshots/<snapshot_id>/
  prices_raw.parquet        # unadjusted OHLC/close, one column per ticker
  actions.parquet           # splits + dividends with ex-dates
  rf_dgs1mo.parquet         # 1-month T-bill yield, or a manifest-flagged BIL proxy with an explicit warning
  universe_pit.csv          # candidate membership: ticker, first_eligible, last_eligible, source_note
  quality_report.md         # imputations, flagged outliers, actions applied, unresolved issues
  manifest.json             # source URLs, retrieval timestamp, SHA-256 of each file + bundle
```

A **confirmatory run reads a snapshot, never the live cache**. The development cache is content-addressed by `(source, tickers, date-range, retrieval params)` (protocol §5.4.9; resolves DEC-20261015-015 finding 4a). Interface: `data.load_snapshot(snapshot_id) -> Snapshot`, where every downstream function takes a `Snapshot` and cannot reach the network.

### 3.2 Point-in-time adjusted prices

```
adjusted_prices(snapshot, t):
    raw      = snapshot.prices_raw.loc[:t]
    actions  = snapshot.actions[ex_date <= t]          # ONLY actions known at t
    return make_adjustments(raw, actions)              # split factor + dividend reinvestment
```

Rules (protocol §5.4.4, §5.4.5): splits adjust historical prices/shares point-in-time and do **not** adjust weights; cash dividends are added to the return on the ex-date and do not retroactively change price returns; mergers/delistings terminate the series with a terminal/delisting return; ticker changes are reconciled in metadata. Adjusting with any action whose ex-date is after *t* is the leakage the §5.4.8 test blocks.

### 3.3 Eligibility

```
eligible(t) = {i : i in universe_pit(t)
                    and history_months(i, ending t) >= 60
                    and adv_3m(i, t) > 5e6
                    and price(i, t) > 0 and not flagged_erroneous(i, t)}
```

The eligible set is recomputed at every rebalance; a universe change is a state change carried into the drifted-weight and turnover computation (§6.3). Missing data follow protocol §5.4.6: forward-fill ≤ 3 consecutive days, else the asset is ineligible for the gap window (not filled).

### 3.4 Risk-free rate

Monthly `rf_t` = the 1-month T-bill yield observed at *t*, converted to a monthly rate. Missing months are forward-filled ≤ 1 month, then the FRED `DGS1MO` value is used directly. **Zero is never substituted** (protocol §5.4.6; resolves DEC-20261015-015 finding 4c). The same `rf` series feeds gross and net Sharpe (§7.1).

> `[OPEN] O1` — The Phase 1 universe included `BIL` as a cash proxy. A near-zero-volatility instrument is degenerate for risk parity (§5.3) and for the mean-variance scale. The point-in-time candidate list (Gate 1 data task) must state explicitly whether a cash/T-bill proxy is a candidate, and the answer is recorded here before C3.

---

## 4. Estimators

All estimators take a `T × N` matrix of monthly **simple** returns over the estimation window and return μ (`N`-vector) and/or Σ (`N × N`). Columns are sorted lexicographically; no estimator may see data after *t*.

### 4.1 Sample mean

\[ \hat\mu_i = \frac{1}{T}\sum_{t} r_{it} \]

Arithmetic mean of monthly simple returns. Used by B3, B5, M1.

### 4.2 Sample covariance

\[ \hat\Sigma = \frac{1}{T-1}\sum_t (r_t - \hat\mu)(r_t - \hat\mu)^\top \]

Unbiased (`ddof=1`), matching `pandas.DataFrame.cov`. Used by B2, B3, B4, B5, M2. Condition number is logged per fold (diagnostic for Test C; risk R-E04).

### 4.3 Ledoit-Wolf shrinkage covariance

\[ \hat\Sigma_{LW} = (1-\delta)\,\hat\Sigma + \delta\,\hat F, \qquad \delta \in [0,1] \]

`[OPEN] O2` — the shrinkage **target** must be stated explicitly because "Ledoit-Wolf" names several estimators. MVP choice: the `sklearn.covariance.LedoitWolf` estimator (Ledoit & Wolf, 2004), whose target is \(\hat F = \bar\sigma^2 I\) with \(\bar\sigma^2 = \operatorname{tr}(\hat\Sigma)/N\), and whose intensity \(\delta\) is the analytic optimum. The constant-correlation target (Ledoit & Wolf, 2003) is a registered variant, not MVP. The chosen target and the fitted \(\delta\) (per fold) are recorded in the results. Used by M1.

### 4.4 Equilibrium (reverse-optimized) excess returns

The Black-Litterman prior:

\[ \Pi = \gamma\,\hat\Sigma\,w_{\text{ref}}, \qquad w_{\text{ref}} = \tfrac{1}{N}\mathbf{1} \]

γ = 10 (protocol §4.3); the equal-weight reference is used because the MVP has no market-capitalisation weights. \(\Pi\) is in monthly excess-return units.

### 4.5 Bayesian (Black-Litterman) posterior — no subjective views

The MVP B-L variant uses the **data view** (the sample mean) as the only view. With the view matrix \(P = I\), view returns \(Q = \hat\mu\), prior covariance \(\tau\hat\Sigma\), and view uncertainty \(\Omega = \tau\hat\Sigma\) (Black-Litterman, 1992, original \(\Omega \propto P\Sigma P^\top\)):

\[ \hat\mu_{BL} = \left[(\tau\hat\Sigma)^{-1} + (\tau\hat\Sigma)^{-1}\right]^{-1}\left[(\tau\hat\Sigma)^{-1}\Pi + (\tau\hat\Sigma)^{-1}Q\right] = \tfrac{1}{2}\left(\Pi + \hat\mu\right) \]

with \(\tau = 1/T\). The closed form is stated because it removes any solver/tuning ambiguity: **M2 shrinks the sample mean exactly halfway toward the equilibrium prior.** No subjective views are permitted in MVP; a view-bearing B-L is an extension (scope §4.3). Used by M2 (with the sample covariance).

> The honest characterisation of M2 is "Bayesian shrinkage of the sample mean toward the equilibrium prior", which is the no-views reduction of Black-Litterman. Reporting language must say so (no "alpha from views").

---

## 5. Constructors and optimizers

### 5.1 Common constraint set

\[ \mathbf{1}^\top w = 1, \qquad 0 \le w_i \le w_{\max} = 0.30 \quad \forall i \]

Applied **uniformly to every method, including B1 and B2** (protocol §4.3; resolves DEC-20261017-019 F1). Every constructor returns a feasible weight vector or raises; no constructor substitutes a different portfolio on failure.

### 5.2 B1 — Equal weight

\(w_i = 1/N\). No inputs, no solver. If N · `w_max` < 1, infeasible (§2).

### 5.3 B2 — Risk parity (equal risk contribution)

Risk contribution \(\mathrm{RC}_i(w) = w_i(\hat\Sigma w)_i\), equalised subject to §5.1. Primary algorithm: cyclically-coordinate-descent risk budgeting (Spinu, 2013; Griveau-Billion, Richard, & Roncalli, 2013), which solves

\[ \min_{w>0}\ \tfrac{1}{2}w^\top\hat\Sigma w - \tfrac{1}{N}\sum_i \ln w_i \quad\Longrightarrow\quad w_i(\hat\Sigma w)_i = 1/N \ \forall i, \]

then normalises \(w\) to sum 1. **Box-constraint handling.** The cap can bind (a low-volatility asset wants a large ERC weight). When it does, B2 is re-solved as a box-constrained risk-budgeting problem — minimise \(\sum_i\big(\mathrm{RC}_i(w) - w^\top\hat\Sigma w/N\big)^2\) subject to §5.1 — whose solution equals the ERC solution when the cap is inactive (Bai, Scheinberg, & Tütüncü, 2016). Diagonal loading \(\epsilon I\), \(\epsilon = 10^{-6}\), if \(\hat\Sigma\) is near-singular. Convergence check: \(\max_{i,j}|\mathrm{RC}_i - \mathrm{RC}_j| < 10^{-8}\) among uncapped assets (protocol §4.4 B2). Both formulations are logged per fold.

### 5.4 B3, B5, M1, M2 — Mean-variance family

\[ \max_{w}\ w^\top\mu - \tfrac{\gamma}{2}w^\top\Sigma w - \lambda\sum_i u_i \quad\text{s.t.}\quad \mathbf{1}^\top w = 1,\ 0 \le w \le w_{\max},\ u_i \ge |w_i - w_i^-| \]

Solved as a **convex quadratic program with auxiliary variables** \(u_i \ge w_i - w_i^-\) and \(u_i \ge -(w_i - w_i^-)\), never by subgradient descent (protocol §4.4 B5; resolves DEC-20261015-015 finding 2). Instantiation:

| Method | μ | Σ | λ | \(w^-\) |
|--------|---|---|---|--------|
| B3 | sample | sample | 0 | — |
| B5 | sample | sample | κ = 0.001 | drifted weights (§6.3) |
| M1 | sample | Ledoit-Wolf | 0 | — |
| M2 | B-L posterior | sample | 0 | — |

**B3 uncapped diagnostic.** H1.1 tests the **uncapped** optimizer (`w_max = 1`), reported as a separate diagnostic treatment, never as a baseline (protocol §7 H1.1; resolves DEC-20261017-020 N2). Its weights are excluded from the MVP comparison table and from any cost/Sharpe claim.

### 5.5 B4 — Minimum variance

\(\min_w\ w^\top\Sigma w\) subject to §5.1 (equivalent to §5.4 with μ = 0; γ is inert). Inputs: sample covariance. Diagonal loading as in B2.

### 5.6 Solver specification

- **Solver:** `cvxpy` (≥ 1.4) with the `CLARABEL` conic/QP solver; deterministic, no licence, no randomness. `scipy.optimize.minimize` + SLSQP is **removed** — the L1 objective is non-smooth and the Phase 1 SLSQP path used a subgradient plus an equal-weight fallback (protocol §4.4 B5; risk R-E01).
- **Acceptance:** a fold is accepted only if the solver returns `optimal` or `optimal_inaccurate` **and** the KKT residual / constraint violation check passes at 1e-7. Any other status aborts the run with the fold identified. No silent fallbacks (contrast Phase 1's `np.ones(n)/n` fallback).
- **Tolerance:** solver defaults; the residual check in §5.6 is the binding acceptance test.
- **Determinism:** identical inputs must give bit-identical weights (protocol §5.4.8 determinism test).

> `[OPEN] O4` — the exact residual-check formula (max constraint violation and duality gap) is recorded before C3.

### 5.7 Fallback policy

There is no fallback portfolio. A non-accepted fold is a hard error that blocks the run (risk R-E01). This is deliberate: the Phase 1 silent fallback would have masked solver failures inside the results.

---

## 6. Walk-forward harness

Implements protocol §5.2, §5.5.4, §5.5.5.

### 6.1 Fold generation

Rolling: at fold *k*, the estimation window is months \([k,\;k+60)\) and the test window is \([k+60,\;k+72)\); *k* advances by 12. Weights are **re-estimated monthly** inside the test window using only the trailing 60 months. The Phase 1 convention that trained on `concat(train, test.iloc[:t])` (expanding within test) is **forbidden** (protocol §5.2; resolves DEC-20261015-015 finding 4d).

### 6.2 Monthly loop (no-lookahead)

```
for t in range(estimation_window, len(months)):
    train = returns.iloc[t-60 : t]        # months strictly before t
    w_t   = constructor(train, w_prev_t_minus)      # uses no month-t return
    r_gross[t] = w_t · returns.iloc[t]
    w_prev_t_minus, to_t, cost_t = apply_cost(w_prev, w_t, returns.iloc[t-1])   # §6.3–6.4
```

The invariant: a method's month-*t* weight uses no month-*t* return (protocol §5.5.4 no-lookahead rule).

### 6.3 Drifted weights

Before computing turnover at *t*, book weights are drifted by the realised return of month *t−1*:

\[ w_i(t^-) = \frac{w_i(t-1)\,(1 + r_i(t-1))}{\sum_j w_j(t-1)\,(1 + r_j(t-1))} \]

Implemented once and reused by every caller (protocol §5.5.5; risk R-C01, R-C04). Universe changes at *t* (an asset becoming eligible/ineligible) are applied to the drifted vector before the trade vector is formed: a new entrant starts at 0, a leaver is traded to 0.

### 6.4 Cost application

\[ \text{Turnover}(t) = \sum_i |w_i(t) - w_i(t^-)|, \qquad C(t) = \kappa\sum_i |w_i(t) - w_i(t^-)|, \qquad R_{\text{net}}(t) = R_{\text{gross}}(t) - C(t) \]

One-way throughout; the cost is charged at the rebalance and deducted from the following period's return (protocol §5.5.2, §5.5.4). The single canonical turnover definition (§7.2) is used here.

### 6.5 Determinism

Seeds are set once per run and recorded in the manifest (protocol §12.4). The only stochastic component is the bootstrap (§7.11); estimators and solvers are deterministic. The §5.4.8 determinism test (same snapshot + same code → identical output) is run before any confirmatory run.

---

## 7. Metrics (implements finding F7)

All metrics are computed on the out-of-sample monthly net-return series unless stated. Every metric below is listed in protocol §§2–3 or §§13 and is reported per protocol §14.1.

### 7.1 Sharpe ratio (gross and net)

\[ \text{SR} = \frac{\operatorname{mean}(r - r_f)}{\operatorname{std}(r - r_f,\ \text{ddof}=1)}\sqrt{12} \]

The **same `r_f` series** is used for gross and net (protocol §2, §5.5.5; resolves DEC-20261015-015 finding 1). `r_f` is never zero-substituted (§3.4).

### 7.2 Turnover (canonical)

\[ \text{Turnover}_{\text{ann}} = 12 \cdot \operatorname{mean}_t \sum_i |w_i(t) - w_i(t^-)| \]

One-way, annualized (protocol §5.5.2; resolves DEC-20261015-015 finding 4b). The dead `metrics.annualized_turnover` (Phase 1) is **deleted**; only this definition exists in the rewrite.

### 7.3 Maximum drawdown

\[ W_t = \prod_{s \le t}(1 + r_{\text{net},s}), \qquad \text{MDD} = \min_t\left(\frac{W_t}{\max_{s\le t} W_s} - 1\right) \]

Reported as a negative number.

### 7.4 CVaR (95%)

With \(r_{(1)} \le \dots \le r_{(T)}\) the ascending net monthly returns and \(k = \lceil 0.05\,T\rceil\):

\[ \text{CVaR}_{95} = \frac{1}{k}\sum_{j=1}^{k} r_{(j)} \]

Mean of the worst 5% of months; reported as a monthly return. Protocol §3 requires it for every method.

### 7.5 Cost drag

\(\text{Cost drag} = \text{SR}_{\text{gross}} - \text{SR}_{\text{net}}\) under the **same** `r_f` (protocol §2).

### 7.6 Skewness and kurtosis

Sample skewness \(\gamma_3 = m_3/m_2^{3/2}\) and **non-excess** kurtosis \(\gamma_4 = m_4/m_2^{2}\), both bias-corrected (`scipy.stats.skew`/`kurtosis`, `bias=False`; kurtosis `fisher=False`). These exact values feed the PSR/DSR denominators (§7.9–7.10), so definitional consistency matters.

### 7.7 Lag-1 autocorrelation

\(\rho_1 = \operatorname{corr}(r_t, r_{t-1})\) on net monthly returns. Large positive \(\rho_1\) is the smoothing/staleness diagnostic (protocol §3; risk of smoothed weights).

### 7.8 Calibration

For each rebalance, using the trailing window and the block bootstrap, form a 90% prediction interval for the next month's return and for volatility; report **empirical coverage** = fraction of rebalances whose realised value falls inside. Target 80–100% (protocol §3). Coverage is reported per method.

> `[OPEN] O5` — the exact calibration protocol (return interval only, or return and volatility; single-month horizon) is fixed before C3; the operationalisation above is the recommendation.

### 7.9 Probabilistic Sharpe ratio (PSR)

Benchmark \(SR^*\) in **per-period** units (annual \(\to\) per-period: \(\div\sqrt{12}\)). With \(T\) observations:

\[ \text{PSR}(SR^*) = \Phi\!\left(\frac{(\hat{SR} - SR^*)\sqrt{T-1}}{\sqrt{1 - \gamma_3\hat{SR} + \tfrac{\gamma_4 - 1}{4}\hat{SR}^2}}\right) \]

References: Bailey & López de Prado (2012). Decision use (protocol §6.1): \(SR^* = SR_{\text{best baseline}}\), threshold PSR > 0.95.

### 7.10 Deflated Sharpe ratio (DSR)

The DSR is PSR evaluated at the expected maximum Sharpe under \(N\) trials:

\[ SR_0 = \sqrt{V}\,\Big[(1-\gamma)\,\Phi^{-1}\!\big(1-\tfrac{1}{N}\big) + \gamma\,\Phi^{-1}\!\big(1-\tfrac{1}{Ne}\big)\Big], \qquad \text{DSR} = \text{PSR}(SR_0) \]

where \(\gamma \approx 0.5772156649\) is the Euler–Mascheroni constant, \(e\) is Euler's number, \(N\) is the registered family size (protocol §12.6), and \(V = \operatorname{Var}(\hat{SR}_n)\) is the variance of the per-period Sharpe estimates **across the family's trials**. Decision use (protocol §6.1): DSR p-value \(= 1 - \text{DSR} < 0.05\). Reference: Bailey & López de Prado (2014).

> **V when \(N = 1\).** \(V\) is undefined from a single trial. Specified convention: for \(N \ge 2\), \(V\) = sample variance (`ddof=1`) of the family's per-period trial Sharpes; for \(N = 1\), \(V = (1 + \tfrac{1}{2}\hat{SR}^2)/T\), the asymptotic variance of the Sharpe estimator, which gives \(SR_0 \approx 0\) and reduces the DSR to a PSR against zero. `[OPEN] O6` — confirm this convention before C3.

### 7.11 Block-bootstrap confidence intervals

Stationary block bootstrap (Politis & Romano, 1994): geometric block lengths with mean \(L = 6\) months, \(B = 2000\) replications, percentile intervals — 90% for reporting, 95% for decisions (protocol §13.1). Computed for Sharpe, turnover, maximum drawdown, and CVaR. Seed: `numpy.random.default_rng(SEED)` with `SEED` fixed and recorded in the manifest. `[OPEN] O7` — seed value fixed before C3.

### 7.12 Metric registry

| Metric | Function | Used for | Source |
|--------|----------|----------|--------|
| Net Sharpe (annualized) | `sharpe` | **primary metric** | protocol §2 |
| Gross Sharpe | `sharpe` | diagnostic only | protocol §2, §14.2 |
| Turnover (annualized, one-way) | `turnover` | constraint check | protocol §3, §5.5.2 |
| Maximum drawdown | `max_drawdown` | tail risk | protocol §3 |
| CVaR 95% | `cvar` | tail risk | protocol §3 |
| Cost drag | `cost_drag` | friction impact | protocol §3 |
| Skewness, kurtosis | `skew_kurt` | non-normality | protocol §3, §7.6 |
| Lag-1 autocorrelation | `autocorr1` | smoothing | protocol §3 |
| Calibration coverage | `calibration` | model honesty | protocol §3 |
| PSR / DSR | `psr`, `dsr` | significance | protocol §6.1, §12.7 |
| Block-bootstrap CI | `bootstrap_ci` | uncertainty | protocol §13.1 |

---

## 8. Reporting interface

This document specifies *how numbers are produced and labelled*, not the reporting policy (that is `results_reporting_and_claims_policy.md`, to be written before Phase 4). The MVP completion criterion (scope §3.9) requires **a single command** that regenerates the report:

```
python scripts/run_experiment.py --snapshot <snapshot_id> --config <frozen config> --out results/<run_id>/
```

Each run writes an immutable `manifest.json` (snapshot ID, git commit, protocol version, config, seeds, environment) and the result tables (net Sharpe at all five cost levels with CIs, DSR/PSR, turnover, drawdown, CVaR, cost drag, per-fold results). Gross/in-sample/unadjusted numbers are labelled diagnostic (protocol §14.2).

---

## 9. Module layout and dependencies

Implementation lands in the Phase 2 rewrite. Proposed layout (subject to ADR at first irreversible choice):

| Module | Responsibility |
|--------|----------------|
| `src/robustfolio/data.py` | snapshot reader, PIT adjusted-price reconstruction, eligibility, rf loader, adapter isolation |
| `src/robustfolio/estimators.py` | `sample_mean`, `sample_cov`, `ledoit_wolf_cov`, `equilibrium_returns`, `black_litterman_returns`, `equal_weight` |
| `src/robustfolio/optimize.py` | convex-QP MVO family (§5.4), minimum variance (§5.5), risk parity (§5.3), solver acceptance (§5.6) |
| `src/robustfolio/backtest.py` | walk-forward harness (§6), drifted weights, cost application |
| `src/robustfolio/metrics.py` | §§7.1–7.8 |
| `src/robustfolio/stats.py` *(new)* | PSR, DSR, block bootstrap, calibration (§§7.8–7.11) |
| `src/robustfolio/report.py` *(new)* | report generation, manifest (§8) |
| `scripts/run_experiment.py` *(new)* | the single reproducible command |

**Dependency change:** add `cvxpy>=1.4` (with `CLARABEL`) to `requirements.txt`; keep `scikit-learn` for `LedoitWolf`; `statsmodels` is **not** required (PSR/DSR implemented directly); `matplotlib`/`pyarrow` retained.

---

## 10. Reproducibility and determinism

1. Same snapshot + same git commit + same config → identical output (protocol §5.4.8).
2. Solver path is deterministic (§5.6); the only randomness is the bootstrap, seeded and recorded (§7.11).
3. Every derived artefact records the snapshot ID, transformation-code commit, and an output hash (protocol §5.4.9).
4. The Phase 1 caveat applies: the Phase 1 run (DEC-20261015-012) is **exploratory and non-confirmatory**; none of its numbers may be cited for or against any hypothesis, and no Phase 1 parameter (γ = 1.0, `w_max` = 0.40, λ = 0.1, expanding window, `.fillna(0.0)` rf, `auto_adjust=True`) survives into a confirmatory run.

---

## 11. Open items to resolve before freeze (C3)

| ID | Item | Recommendation |
|----|------|----------------|
| O1 | Does the PIT candidate list include a cash/T-bill proxy? (affects B2 cap, MVO scale) | Decide at universe reconstruction; record here |
| O2 | Ledoit-Wolf shrinkage target | `sklearn` identity target; constant-correlation as a variant |
| O4 | Exact solver acceptance residual formula | max constraint violation ≤ 1e-7 and duality gap ≤ 1e-7 |
| O5 | Calibration protocol detail | return + volatility, one-month horizon |
| O6 | \(V\) (DSR) when \(N=1\) | analytic estimator variance \((1+\tfrac12\hat{SR}^2)/T\) |
| O7 | Bootstrap seed value | fixed constant recorded in the manifest |

**Freeze (C3) requires:** every `[OPEN]` resolved, the frozen config reproduced by `scripts/run_experiment.py` on the MVP universe, and a decision-log entry with a version bump. Gate 1 entry additionally requires the point-in-time candidate list (§3.1 O1) and the §5.4.8 leakage suite passing.

---

## 12. Model tags applied

- **[First Principles]** — one method = (μ, Σ, constructor); H2.1/H2.2 are single-factor tests by construction.
- **[Inversion]** — the no-fallback policy (§5.7), the F9 conflict resolution (§0), and the O-items exist to stop the spec from hiding a defect inside a "reasonable default".
- **[Information Theory]** — closed forms where possible (§4.5) to remove solver ambiguity; every metric has one definition.
- **[Systems]** — estimator → constructor → harness → metrics → report, with a single source of truth for each frozen value (§2).
- **[Learning Loop]** — the F7 deferral and the F9 conflict are closed by reference, not by silence.

---

## 13. Revision History

| Date | Version | Change | Author |
|------|---------|--------|--------|
| 2026-10-17 | 1.0 | Initial `model_and_method_spec.md` (TODO C2). Defines the MVP method set (B1–B5, M1 shrinkage-covariance MVO for H2.1, M2 Bayesian/B-L MVO for H2.2) and fixes the F9 classification conflict in favour of scope §3.4/§3.5 (logged DEC-20261017-022; protocol §4.2 corrected to v2.4). Absorbs DEC-20261017-019 finding F7: exact implementations of Sharpe (single-\(R_f\)), canonical turnover, maximum drawdown, CVaR 95%, cost drag, skewness/kurtosis, lag-1 autocorrelation, calibration, PSR, DSR, and stationary block-bootstrap CIs. Specifies the convex-QP MVO family (auxiliary L1 variables, CLARABEL, no fallback), risk-parity CCD with box handling, the rolling-60 walk-forward harness with drifted-weight cost application, and the module/dependency plan (`cvxpy` added). Status `Draft`; `[OPEN]` O1, O2, O4–O7 remain. | Ken Ira Lacson Talingting |

---

*This document exists so that two people implementing the frozen protocol would produce the same numbers. If it leaves a choice that changes a result, it has failed and the choice must be moved into the spec.*
