# Country sample 2 — protocol (freeze not independently verified)

**Version:** 1.1
**Status:** **Pre-specified protocol; the repository does not independently establish that its final content was frozen before execution.** The sample is reported as an external replication, not a confirmatory test. See [`audit_2026-11-08.md`](audit_2026-11-08.md).
**Created:** 2026-11-05
**Owner:** Ken Ira Lacson Talingting
**Reproduce:** `python scripts/run_country_sample.py`
**Snapshot:** `yahoo-countryetf-1998-01-01_2026-09-30-2026-11-05-269a4565`

**Claim-status note (2026-11-08).** The protocol file was created at 19:49:16 on 2026-11-05, before the snapshot at 19:49:50. However, it was last written at 20:08:45, after the country results at 19:51:35; the protocol and results were committed together at 20:09:27. The repository therefore cannot establish that the final protocol content was frozen before execution. The sample is retained as a pre-specified external replication. The original protocol text below is preserved.

---

## 0. What this is

The first sample (18 US multi-asset ETFs, 2012-06 to 2026-05) produced a null and a
correction. The correction said the registered significance test was a level test, while the
design was a paired comparison. This note records a **new sample** on which that corrected
test is applied once. The protocol document is dated 2026-11-05; its freeze before execution
is not independently verified.

The sample is different in three ways:

- **Cross-section:** 18 country equity ETFs, not 18 US multi-asset ETFs.
- **Period:** 2005-07 to 2026-06, 252 months, including the 2008 crisis.
- **Regime:** a different set of drawdowns, correlations and rate environments.

It is a test of **external validity**, not another pass over the same 168 months.

**What has been seen.** Only data coverage: first/last dates, row counts, dividend and split
counts. No return, Sharpe, ranking, or backtest has been computed on this sample. The protocol
document predates the snapshot, but its final content was written after the results; the
freeze is not independently verified.

---

## 1. Hypothesis

**H2.1 (shrinkage).** On this sample, the Ledoit–Wolf shrinkage-covariance MVO (`M1`) beats the
best baseline on net excess Sharpe by at least the materiality bar, with a paired 95% lower
confidence bound above zero, and passes the robustness gates.

**H2.2 (Black–Litterman).** On this sample, the Black–Litterman mean MVO (`M2`) beats the best
baseline on the same terms.

**H2.4 (at least one).** At least one of `M1` or `M2` succeeds under the rule. Both are
reported regardless.

Direction: positive. Effect size of interest: **0.20** net excess Sharpe, the same bar as the
first sample. Prior: no strong directional prior; country equity is a different cross-section
and the 2008 regime is different, so the result is genuinely open.

---

## 2. Data and sample

| Item | Value |
|---|---|
| Universe | 18 iShares MSCI country ETFs (list in `notes/pit_candidates_country_2026-11-05.csv`) |
| First eligible | 2005-06-30 |
| Out-of-sample period | 2005-07-01 to 2026-06-30 |
| Out-of-sample months | 252 |
| Folds | 21 non-overlapping 12-month folds |
| Estimation window | 60 months, rolling, re-estimated monthly |
| Rebalance | monthly, last trading day |
| Costs | 10 bps one-way headline; 0/5/10/20/50 bps reported |
| Constraints | fully invested, long only, `w_i <= 0.30` |
| Data source | Yahoo Finance via the frozen snapshot builder; FRED `DGS1MO` |
| Price basis | raw unadjusted + point-in-time corporate actions, as in the first sample |

**Point-in-time eligibility only.** Each fund enters at `first_eligible`; it is absent before
that date. The list is **current-listed**: no in-scope country ETF in this list delisted during
the sample. The survivorship limitation is therefore present and disclosed, not measured. The
result is conditional on this list.

**Why 2005-07.** The 60-month window ending 2005-06 is available for every fund (the latest
history starts in 2000-06). The last complete 12-month fold ends 2026-06. The snapshot carries
data through 2026-09-30, so no partial month enters a return.

---

## 3. Methods

The method set, estimators, optimizer, constraints and cost application are the same as the
first sample:

- `B1` equal weight
- `B2` risk parity (ERC)
- `B3` sample-covariance, sample-mean MVO
- `B4` minimum variance
- `B5` turnover-penalised MVO, `lambda = kappa = 0.001`
- `M1` `B3` with a Ledoit–Wolf covariance
- `M2` `B3` with a Black–Litterman mean

No new methods. No tuning. No fallback solver.

---

## 4. Primary metric and comparator

**Primary metric:** net excess Sharpe at 10 bps one-way costs, annualised.

**Comparator:** the best baseline by net excess Sharpe, selected mechanically from `B1`–`B5`
after the run. Its identity is an output; the definition is fixed here.

**Paired test.** The candidate and the comparator are compared month by month on the same 252
months. The statistic is the annualised Sharpe difference; the interval is a stationary
block bootstrap (2,000 replications, mean block 6 months, seed 20261017). The significance
gate is the **5th percentile of the paired bootstrap distribution above zero** — the 95%
one-sided lower confidence bound. This replaces the level PSR gate from protocol v2.4. The
level PSR and the DSR are reported as diagnostics, not as gates.

**Why this is the correction.** The first sample showed that a level test can require an
effect of about 0.72 to notice a 0.20 difference. The paired test uses the common variation
between two nearly identical portfolios and is the test the minimal-difference design was
built for.

---

## 5. Decision rule

For each candidate, against the best baseline:

1. **Significance:** paired bootstrap 5th percentile > 0 (95% one-sided).
2. **Materiality:** point net Sharpe gap ≥ 0.20.
3. **Turnover:** candidate turnover ≤ 2× the baseline's.
4. **Drawdown:** candidate max drawdown no worse than the baseline's by more than 5
   percentage points.
5. **Cost levels:** candidate beats the baseline at ≥ 3 of the 5 reported cost levels.
6. **Folds:** candidate beats the baseline in ≥ 60% of the 21 folds.
7. **Concentration:** no single fold contributes more than 40% of the total advantage.
8. **Discipline:** no point-in-time, cost-model, or solver violation.

**Success** = all eight. **Partial** = significance + materiality, or robustness, but not both.
**Failure** = otherwise. Every candidate is reported; no best-of selection.

**Multiple testing.** Two candidates, both reported. DSR at family size 2 is reported as a
diagnostic. No claim is made from a selected subset.

---

## 6. What would invalidate the sample

- Any leakage test failure from the existing suite.
- A solver rejection under the frozen 1e-7 certificate; a failed arm is reported as
  incomplete, not tolerated.
- A different universe, period, cost level, or constraint set from the table above.
- Any performance-dependent change to the hypothesis, threshold, or method set.

---

## 7. What this can and cannot show

It can examine whether the corrected paired rule and the two treatments replicate on a different
cross-section and period. It cannot make the original sample confirmatory, remove the
current-listed survivorship limitation, or establish that a result generalises beyond country
equity ETFs. A null here is a valid result; a positive result is a replication with the same
caveats, not a trading recommendation.

---

## 8. Revision history

| Version | Date | Change |
|---|---|---|
| 1.0 | 2026-11-05 | Pre-specified country-ETF sample, 2005-07 to 2026-06; paired significance gate; same 0.20 bar and robustness gates. |
| 1.1 | 2026-11-08 | Claim-status correction: the protocol's final content was written after the results; the freeze is not independently verified. The sample is reported as an external replication, not a confirmatory test. |
