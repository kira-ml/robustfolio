# A pre-registered null on robust portfolio construction — and why the benchmark is the binding constraint

*The domain-specific cut. Assumes you know what an MVO is.*

---

**Exploratory and non-confirmatory.** The run below may not be cited for or against any hypothesis: the
registered confirmatory test was executed without the blindness its registration required, so no
confirmatory test exists and the hypotheses are **untested, not falsified**. Net *excess* Sharpe only; no
absolute return claim; all costs and intervals stated. The code, the published tables, and the check
are public. The input snapshot is **not** redistributed -- the upstream Yahoo and FRED terms prohibit
it -- so exact end-to-end reproduction requires independently obtained data.

## The experiment

Eighteen US ETFs on a point-in-time universe (point-in-time *eligibility*, not point-in-time data — the
prices are what a 2026 source holds for 2012 today). 168 out-of-sample months, fourteen 12-month folds,
1,176 optimiser solves, a 60-month rolling estimation window re-estimated monthly, monthly rebalance.
Net Sharpe at a headline 10 bps one-way cost, with the cost levels swept rather than chosen.

Five baselines and two treatments. The two treatments each differ from the plain sample-covariance,
sample-mean MVO baseline (`B3`) in **exactly one component**: `M1` swaps the sample covariance for a
shrinkage estimate; `M2` swaps the sample mean for a Black–Litterman posterior. Everything else —
universe, window, optimiser, cap, costs — is shared, so a difference is attributable to the component
that changed and not to a bundle of choices.

The decision rule is a conjunction against the **best baseline**: net Sharpe advantage ≥ **0.20** *and* a
probabilistic Sharpe ratio ≥ **0.95**. Both, not either.

## The result

| | Net Sharpe @10 bps | 90% CI | Turnover (annualised) |
|---|---|---|---|
| `B1` equal weight | 0.5482 | [0.153, 1.002] | 0.39 |
| `B2` risk parity | 0.4519 | [0.017, 0.974] | 0.34 |
| **`B3` sample MVO — best baseline** | **0.7896** | [0.331, 1.318] | **2.12** |
| `B4` minimum variance | 0.1820 | [−0.253, 0.751] | 0.43 |
| `B5` turnover-penalised MVO | 0.7843 | [0.316, 1.316] | 0.73 |
| `M1` shrinkage-covariance MVO | 0.7860 | [0.327, 1.298] | 1.92 |
| `M2` Bayesian (Black–Litterman) MVO | **0.8538** | [0.426, 1.369] | 2.14 |

`M2`'s advantage over `B3` is **+0.064** against a 0.20 bar; its PSR against `B3` is **0.587** against a
0.95 bar. Both candidates return **FAILURE** (`M1` at −0.004). Every interval overlaps `B3`'s. One
disclosure on the verdict: §6.3's "advantage" is not pinned to a metric, and the confirmed reading —
fold wins on net Sharpe, the concentration clause on the per-fold mean return difference — is the
binding one for `M2` (51.3%), so a *stated reading*, not the arithmetic alone, produces that `FAILURE`.

The materiality bar does the work here, and that is the point of having one. A 0.064 improvement in net
Sharpe on a strategy that carries *more* turnover than the baseline is not a result you could act on even
if it were statistically clean. The **paired** comparison is powered to separate roughly 0.13–0.20
between strategies correlated at ρ ≈ 0.985; it gives `M2` +0.064 [−0.011, +0.147] and `M1` −0.004
[−0.096, +0.080]. `M2` is plausibly a little better, but the interval includes zero and both are far
below 0.20. The effect is **small**, not absent — and the registered level test is a different, much
less powerful test.

## Why the benchmark, not the correction, is the binding constraint

Here is the part I would carry to another project. Both candidates **pass** the deflated Sharpe test
against zero — p = 0.0032 and 0.0017. Both **fail** the probabilistic Sharpe test against the best
baseline — 0.495 and 0.587. Same strategies, same return series, opposite conclusions, and the only
difference is what each statistic is measured against.

That is not a paradox, it is the whole question. With exactly one pre-registered comparison, the
multiple-testing correction is *inert*: the deflated Sharpe ratio collapses to the probabilistic one, and
the deflation machinery you carefully specified never fires. What remains binding is which benchmark you
declared in advance. Firing once substitutes for a correction, but only if you also fix the reference
point before you look — because the benchmark is the one input to the test that you choose, and after the
fact there is always a flattering one.

## The turnover inversion

The motivating story for robust construction is usually that it wins by **trading less**. Here it
inverts. `B3`, the plain sample MVO that the project set out to critique, carries 2.12 annualised
turnover and wins anyway on net Sharpe at the headline cost. `B5`, the turnover-penalised baseline,
cuts turnover by roughly two thirds — to 0.73 — and lands a hair *below* `B3` at 0.7843. The
two robust treatments do not trade less: `M2` carries slightly more turnover than the baseline
(2.14 versus 2.12), and `M1` carries about 9% less (1.92).

So in this sample, turnover-penalisation bought a real reduction in trading and did not buy an improvement
in net Sharpe, while the highest-turnover method was the best performer. That is a legitimate outcome and
it is the kind of thing a single headline number would have hidden; I only saw it because the table
reports turnover next to the metric it is supposed to protect.

## A diagnostic hypothesis (not a result)

Eighteen assets, but the **effective number of independent bets is small**: a participation ratio of about
3.1 and an entropy-based count of about 5.0 out of 18. The correlation matrix has condition number ≈ 1.7e3,
and twelve of the eighteen eigenvalues fall **below the lower edge** of the Marchenko–Pastur band for an
independent panel of this shape ([0.452, 1.762]) — the smallest at 0.0053, which is 85× below that edge.
The estimation problem is large and genuinely near-singular (18 assets on a 60-month window).

If that is the right reading, then shrinkage has almost no noise to bite on — there is very little
independent information to shrink toward a prior — and the uniform 30% position cap is doing **more
regularisation than the estimator is**. That would explain why `M1` (shrinkage) lands at essentially
`B3`, and why the only candidate with a different *mean* (`M2`) is the only one that separates at all.

It is testable, and I have now tested it. **Update, 2026-11-04:** the cap sweep across 0.20, 0.30, 0.40
and 1.00 does **not** support the shrinkage version of this hypothesis. `M1 − B3` remains within
noise of zero across the cap grid; the point estimate is positive at the 40% cap (+0.010), but its
interval includes zero and it is far below the bar. The cap does not rescue shrinkage. It does show the cap binding the
Black–Litterman treatment, whose advantage grows with the cap but remains below the materiality bar.
The tidy story failed its own test; the result is in `notes/cap_sweep_shrinkage_2026-11-04.md`.

## What to check

The reproduction claim is deliberately split, because a solver's output is defined only to its
tolerance: **decisions** (method set, rebalances, folds, headline cost level, ranking, selected
baseline, and the eight §6.4 gates with the verdict itself) are compared exactly and fail the build on
any difference, while the continuous quantities are compared within a documented `1e-9` and the
observed worst difference — `4.698e-12` on the CI runner — is printed on every run rather than the
bound being quoted. Clone the repository and run `verify_release.py` against a snapshot archive if you
independently have one; the archive itself is not distributed. If it prints anything other than
`EXACT` or `WITHIN`, tell me.
