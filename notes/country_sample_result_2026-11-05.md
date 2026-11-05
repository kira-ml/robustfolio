# New-sample result — country ETFs, 2005–2026

**Version:** 1.0
**Status:** **Pre-registered new sample, executed.** Confirmatory for this sample; the broader project remains exploratory because the corrected test was derived from the first sample.
**Created:** 2026-11-05
**Pre-registration:** [`confirmatory_country_etfs_2026-11-05.md`](confirmatory_country_etfs_2026-11-05.md)
**Snapshot:** `yahoo-countryetf-1998-01-01_2026-09-30-2026-11-05-269a4565`
**Tables:** [`../docs/published-run/country-sample/`](../docs/published-run/country-sample/)
**Reproduce:** `python scripts/run_country_sample.py --out results/country_sample`

---

## 1. What was run

The pre-registered new sample: 18 current-listed iShares MSCI country ETFs, 2005-07 to
2026-06, 252 months, 21 non-overlapping folds, 60-month rolling window, monthly rebalance,
10 bps one-way costs, 30% position cap, same seven methods and optimizer as the first sample.

The significance gate is the corrected one: the **5th percentile of the paired bootstrap
Sharpe difference above zero** (95% one-sided). The level PSR and the DSR are reported as
diagnostics, not as gates. The materiality bar is still **0.20** net excess Sharpe.

No performance was inspected before the protocol was frozen. Only data coverage was checked.

---

## 2. Result

| Method | Net excess Sharpe | Turnover | Max drawdown |
|---|---:|---:|---:|
| **B1 equal weight** | **0.3527** | 0.83 | −58.3% |
| B2 risk parity | 0.3423 | 0.86 | −57.1% |
| B5 turnover-penalised | 0.2919 | 1.40 | −59.2% |
| B3 sample MVO | 0.2797 | 2.54 | −57.8% |
| B4 minimum variance | 0.2715 | 1.76 | −50.3% |
| M1 shrinkage | 0.2710 | 2.43 | −58.5% |
| M2 Black–Litterman | 0.3193 | 2.48 | −57.6% |

The best baseline is **B1 (1/N)**, not B3.

### Candidate decisions, against B1

| Candidate | Paired delta | 90% interval | P(delta > 0) | Gap | Turnover ratio | Cost levels won | Folds won | Verdict |
|---|---:|---:|---:|---:|---:|---:|---:|---|
| M1 | −0.0817 | [−0.1746, +0.0290] | 0.116 | −0.0817 | 2.93× | 0 / 5 | 10 / 21 | **FAILURE** |
| M2 | −0.0334 | [−0.1253, +0.0748] | 0.312 | −0.0334 | 2.99× | 0 / 5 | 11 / 21 | **FAILURE** |

Both 90% upper bounds are below 0.20. At the 5% one-sided level, the data **exclude a
material 0.20 advantage** over 1/N for both candidates. The point estimates are negative, and
both treatments trade about three times as much as 1/N. The turnover gate alone would reject
them.

The concentration clause is not applicable in the usual sense because the total advantage is
negative; the method already fails on significance, materiality, cost levels, folds and
turnover. It is recorded as `NaN` rather than a pass, because a losing method should not pass
a concentration test on a technicality.

---

## 3. What it means

**The treatment advantage did not replicate. The benchmark lesson did.**

In the first sample, B3 (plain sample MVO) was the best baseline, and M2 was slightly better
than B3 while still failing the 0.20 bar. In the country-ETF sample, **1/N is the best
baseline**, and M2 is below it. A treatment can look better than B3 and still lose to the
simplest portfolio in the room.

That is the project's thesis, stated more sharply: **the comparator is doing the work.** The
first sample's B3 was a property of that universe, not a law. On a different universe and
period, the benchmark changes, and the treatment ranking changes with it.

The corrected test also behaves as intended. The paired test does not rescue the treatments;
it reports a negative point estimate with an interval whose upper bound is below the
materiality bar. The level PSR/DSR diagnostics do not support a positive edge either. The
result is not "the test was too weak"; it is "the effect is not there, against this
benchmark."

**The original result was not a hidden win.** It was a small, universe-conditional edge over
B3 that disappeared when the comparator became 1/N. The correction made the test honest; the
new sample made the external validity honest.

---

## 4. Limitations

- **Current-listed country ETFs.** No in-scope delisting in the sample; the survivorship
  limitation is present and disclosed, not measured. The result is conditional on this list.
- **One asset class and period.** Country equity, 2005–2026, including the 2008 crisis. This
  is a different sample, not a universal test.
- **Yahoo price history is revised.** The snapshot pins what the vendor held at retrieval; it
  is not a perfect point-in-time reconstruction of what a trader saw.
- **Flat 10 bps cost.** No market impact, capacity, taxes, or regime-dependent costs. The
  treatments' ~3× turnover relative to 1/N makes this limitation material.
- **Confirmatory for this sample, not for the original hypothesis in general.** The corrected
  test was derived from the first sample; this sample is unseen, but the broader project is
  still exploratory in the strict sense.

---

## 5. What would change the conclusion

A different universe with delisted funds, a capacity-aware cost model, a different asset class,
or a period that does not yet exist. The result would also change if a treatment beat 1/N with
a paired lower bound above zero and a gap at or above 0.20; it did not here.

The one-line summary:

> **On a new sample, the robust treatments still failed — and this time the benchmark was
> 1/N, not sample MVO. The treatment advantage did not replicate; the benchmark lesson did.**
