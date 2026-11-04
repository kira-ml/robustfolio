# Cap sweep — is the 30% cap doing the regularisation?

**Version:** 1.1
**Status:** **Exploratory, completed.** Post-hoc mechanism test on the same data. Not confirmatory, not a protocol amendment, and not a rescue of the frozen verdict.
**Created:** 2026-11-04
**Owner:** Ken Ira Lacson Talingting
**Reproduce:** `python scripts/cap_sweep.py`
**Snapshot:** `yahoo-usetf-2007-01-01_2026-09-30-2026-10-17-2ad06139`
**Related:** `notes/tests_BCD_spec_2026-10-17.md` §2 (registered Test B, which excludes M1/M2); `notes/paired_inference_2026-11-04.md`; `essays/flagship.md` §"The result, read properly"

---

## 0. What this is, and what it is not

The first run's null has a mechanistic explanation in the essay, labelled there as a
hypothesis: with only 3–5 effective bets, a near-singular covariance, and a uniform 30%
position cap, the cap is doing more regularisation than the shrinkage estimator. If that
is true, the value of shrinkage should appear when the cap is relaxed and the optimiser
has more room to exploit estimation error.

This note pre-declares the test of that mechanism. It is **exploratory** because the same
data have already been seen; it cannot confirm or falsify H2.1, and it does not change the
frozen 0.30 verdict. Its only job is to separate two explanations for the same null:

- **cap explanation:** M1's advantage over B3 grows as the cap loosens;
- **no-signal explanation:** M1's advantage stays at or below zero at every cap.

The essay already names the test, so running it is not a new hypothesis invented after the
fact. It is the check the write-up asked for.

---

## 1. Design

| Item | Value |
|---|---|
| Universe | the frozen snapshot's 18 candidates (17–18 eligible at a rebalance) |
| Period | 2012-06 to 2026-05, 168 out-of-sample months, 14 folds |
| Window | 60 months, rolling, re-estimated monthly |
| Rebalance | monthly, last trading day |
| Cost | 10 bps one-way (headline); the paired comparison uses net excess returns |
| Caps | `w_max ∈ {0.20, 0.30, 0.40, 1.00}` (1.00 = uncapped) |
| Methods | `B1`, `B2`, `B3`, `B4`, `M1`, `M2` |
| `B5` | attempted; the 0.40 arm failed the frozen 1e-7 KKT certificate at 2014-08-31 (residual 2.571e-7). Reported as **incomplete**, not imputed |
| Test | paired stationary block bootstrap of the annualised net excess Sharpe difference, 2,000 reps, mean block 6, seed 20261017 |
| Primary comparison | `M1 − B3` (shrinkage) at each cap; `M2 − B3` (Black–Litterman) as a secondary |
| Secondary output | net Sharpe, turnover, maximum weight, number of held assets, paired 90% CI |

**Why B1 and B2 are in the table.** They are cap-invariant in construction (1/N is below
0.20; risk parity is capped but not optimised against returns). They are the controls: if
the cap sweep moves them, the sweep is measuring something other than the intended
mechanism.

**Why the 0.30 arm is included.** It is the frozen configuration. It must reproduce the
published M1/M2/B3 numbers; if it does not, the sweep is not comparable to the headline run.

---

## 2. Decision rule, fixed before the extended arms are run

All four caps and both treatments are reported. No arm is selected as the headline.

- **SUPPORTED (cap explanation).** `ΔSR(M1 − B3) ≤ 0` at 0.30 **and** `ΔSR(M1 − B3) > 0` at
  1.00, with the 90% paired interval at 1.00 excluding zero. The cap is doing the work the
  shrinkage estimator was supposed to do.
- **NOT SUPPORTED (no-signal explanation).** `ΔSR(M1 − B3) ≤ 0` at every cap. The cap is not
  the reason; the estimator has nothing to add on this universe.
- **CAP-FRAGILE / INCONCLUSIVE.** Any other pattern: a sign change without a separating
  interval, a non-monotone path, or an arm that cannot be certified. Report it as
  unresolved; do not pick the cap that tells the better story.

The same rule is applied to `M2 − B3` as a secondary, with no claim if the two disagree.

---

## 3. Firewall — the selection trap

1. The frozen 0.30 result is not replaced by a looser-cap result. The headline remains the
   0.30 null.
2. If a loose cap makes M1 or M2 clear the §6.2 bar, that is a **new hypothesis** requiring
   a new pre-registered experiment at that cap, with these eight arms counted as prior
   trials. It is not "M1 wins".
3. Every arm is reported, including B5's failure and any cap where the ranking reverses.
4. The cap is a **constraint**, not a strategy parameter. Choosing 1.00 after seeing the
   result would be the same error as choosing a benchmark after seeing the result.

---

## 4. What would invalidate an arm

- The 0.30 arm does not reproduce the published B3/M1/M2 net Sharpes to within the
  documented 1e-9.
- A solver arm cannot pass the frozen 1e-7 certificate. It is reported as incomplete, and
  the tolerance is **not** widened to include it.
- The eligible universe or cost level differs from the frozen run.
- A cap is silently dropped because it produced an inconvenient sign.

---

## 5. What this can and cannot show

It can show whether the shrinkage null is **cap-conditional** on this universe. It cannot
show that shrinkage works in general, that a looser cap is investable (a 1.00 cap can
concentrate the portfolio and raise turnover), or that the 0.30 protocol was wrong. A
positive result at 1.00 would be a mechanism finding and a hypothesis for a new sample, not
a licence to change the frozen rule.

---

## 6. Result (appended 2026-11-04)

The 0.30 arm reproduces the published B3/M1/M2 net Sharpes exactly
(0.789583, 0.785962, 0.853812), so the sweep is comparable to the headline run.
The paired differences are annualised net-excess Sharpe; the intervals are 90%
stationary-bootstrap intervals over the same 168 months.

| Cap | `M1 − B3` | 90% CI | `M2 − B3` | 90% CI | `B5 − B3` |
|---:|---:|---:|---:|---:|---:|
| 0.20 | −0.0154 | [−0.1065, +0.0727] | +0.0486 | [−0.0311, +0.1404] | −0.0455 |
| 0.30 | −0.0036 | [−0.0964, +0.0800] | +0.0642 | [−0.0113, +0.1467] | −0.0053 |
| 0.40 | +0.0100 | [−0.0843, +0.0972] | +0.1192 | [+0.0370, +0.2058] | **not certifiable** |
| 1.00 | −0.0033 | [−0.0955, +0.0832] | +0.1376 | [+0.0445, +0.2372] | **not certifiable** |

Net Sharpe by cap (B1 is cap-invariant below 0.20; B4 is the min-variance control):

| Cap | B1 | B2 | B3 | B4 | M1 | M2 |
|---:|---:|---:|---:|---:|---:|---:|
| 0.20 | 0.5482 | 0.4608 | 0.7176 | 0.2536 | 0.7022 | 0.7662 |
| 0.30 | 0.5482 | 0.4519 | 0.7896 | 0.1820 | 0.7860 | 0.8538 |
| 0.40 | 0.5482 | 0.4514 | 0.7701 | 0.1379 | 0.7801 | 0.8894 |
| 1.00 | 0.5482 | 0.4438 | 0.7678 | 0.0527 | 0.7645 | 0.9054 |

**The pre-declared shrinkage condition is not met.** `M1 − B3` is negative at
0.30 and negative at 1.00, and every interval includes zero. The cap does not
explain why shrinkage looked useless; loosening it does not turn M1 into a
winner. On this sample, the no-signal explanation survives and the cap
explanation does not.

**The secondary result is different.** `M2 − B3` grows monotonically with the
cap: +0.049 at 0.20, +0.064 at 0.30, +0.119 at 0.40, +0.138 at 1.00. At 0.40
and 1.00 the paired interval excludes zero. The cap was binding the
Black–Litterman treatment, not the shrinkage treatment. But the point estimate
at 1.00 is **0.138, still below the 0.20 materiality bar**, and the 1.00 interval
extends to 0.237, so the materiality question is inconclusive rather than
cleared. The cap is part of the M2 story; it is not a rescue.

**Two caveats that travel with the M2 row.** A looser cap buys the Sharpe with
concentration: M2's maximum weight rises from 0.30 at the frozen cap to 0.80 at
1.00, and its held-asset count falls from 5.8 to 4.0. B3 at 1.00 holds a single
asset (maximum weight 1.00). A 1.00 cap is a diagnostic, not an investable
recommendation. And `B5` cannot be certified at 0.40 or 1.00: the frozen 1e-7
KKT certificate rejects the 2014-08-31 and 2015-12-31 rebalances at residuals
2.571e-7 and 1.226e-6. Those arms are reported as incomplete; the tolerance was
not widened.

---

## 7. What this changes, and what it does not

**Changes:** the essay's mechanism hypothesis — that the 30% cap is doing the
regularisation and shrinkage has nothing left to bite on — is **not supported**
on this sample. The M1 null is not a cap artifact. The cap does bind M2's
advantage, but even at the loosest cap the advantage is below the bar the study
set.

**Does not change:** the frozen 0.30 verdict, the published tables, or the
confirmatory status. The sweep is exploratory, the same data have been seen, and
the 0.40/1.00 arms are not a new strategy recommendation. If the cap-conditional
M2 result is worth pursuing, it requires a new pre-registered experiment at a
named cap, on a new sample, with these eight arms counted as prior trials.

The honest one-line summary is: **the tidy mechanism story failed, and the
secondary mechanism is real but too small to clear the bar.** That is a better
result than a story that fits.

---

## 8. Revision history

| Version | Date | Change |
|---|---|---|
| 1.0 | 2026-11-04 | Initial pre-declaration. The B1–B5 arms at 0.20/0.30 were observed during the failed Test B attempt; the M1/M2 extension is the new question. Disclosed rather than presented as blind. |
| 1.1 | 2026-11-04 | Results appended. The 0.30 arm reproduces the published metrics; the shrinkage cap hypothesis is not supported; the M2 advantage grows with the cap but remains below 0.20; B5 at 0.40/1.00 is not certifiable and is reported as incomplete. |
