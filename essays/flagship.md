# I tried to break my own result before I published it

*Four defences against fooling yourself, one that failed, and a null I can stand behind.*

---

I spent most of this project trying to falsify my own result. The result held up. My *claim* about
it did not — twice, in two consecutive runs of a check I had written specifically to catch it.

Here is the one that still stings. I pre-registered a confirmatory test. Hypothesis, metric,
threshold, decision rule — written down and dated before any data was touched, which is the entire
point of pre-registration. Then I built the report generator: the thing that turns a run into a table
a stranger can check. To validate it end to end I had to run it on the frozen configuration, and the
frozen configuration *is* the confirmatory configuration. So the answer to my confirmatory test was on
my screen, in a file I was diffing, before the test ran.

That is the defence that failed. It was not a bug and it was not carelessness; it was two things I
wanted in direct tension, and I chose to be able to check my numbers. More on that at the end, because
it is the part I would most want someone to push on.

The same day, a defence I assumed could not fail did. The README claimed the repository reproduces its
published table *bit-for-bit*. I added a continuous-integration step that could actually test that
claim — and the claim failed. I fixed it, and the next run failed harder. What came out of that is
the most useful thing in the repository, and it is not a number: it is the distinction between what a
check can prove exactly and what it can only bound.

## What I was actually testing

One question, framed so that a wrong answer to it is still worth something:

> Does a robust, turnover-aware portfolio construction method beat a plain one out-of-sample, net of
> transaction costs — once you adjust for having tried more than one?

The domain is a worked example, not the payload. Eighteen US ETFs on a point-in-time universe, 168
out-of-sample months, fourteen non-overlapping folds, 1,176 optimiser solves. Five baselines and two
treatments; each treatment differs from the plain sample-covariance MVO baseline in exactly one
component: `M1` swaps the sample covariance for a shrinkage estimate; `M2` swaps the sample mean for a
Black–Litterman posterior.

The thing that decides is a *conjunction*, and that is a design choice worth defending. A candidate
must clear both bars against the **best baseline** — a net Sharpe advantage of at least 0.20, *and* a
probabilistic Sharpe ratio of at least 0.95. Not either. Requiring only significance gets you a
statistically clean effect too small to care about; requiring only materiality gets you a big number
you cannot distinguish from luck. Requiring both is the minimum that resists being gamed, because each
one alone is a target you can hit by choosing the wrong thing to measure.

And the answer is **no**. The best baseline is `B3` — plain sample-covariance, sample-mean MVO, which is
the method the project set out to critique — at a net Sharpe of 0.7896, 90% interval [0.331, 1.318]. The
strongest candidate, `M2`, reaches 0.8538 with interval [0.426, 1.369]. That is +0.064 against a 0.20
bar, and a PSR of 0.587 against a 0.95 bar. Both candidates return **FAILURE**.

Two disclosures, stated once and meant: this run is **exploratory and non-confirmatory**, so it may not
be cited for or against any hypothesis; and the confirmatory slot is **empty**, for the reason in the
opening. Nothing here is investment advice, and no absolute return claim is made anywhere — the metric
is net *excess* Sharpe, and every number below carries the interval and the cost level it was measured
at.

That is the domain. Everything interesting is in the four defences.

## Defence 1 — freeze before looking

Pre-registration is usually described as a virtue. It is better understood as a mechanism, and like any
mechanism its value is exactly the set of things it makes impossible.

It makes it impossible to move the bar after seeing the number. Impossible to swap the benchmark for one
that flatters the candidate. Impossible to quietly drop a method that embarrassed you. The protocol, the
method spec, the thresholds and the decision rule are versioned files that were frozen and dated before
the run; where a reading was ambiguous, it is disclosed rather than resolved in whichever direction helps
(findings **F24** and **F25**: two readings were under-specified, and the F25 one — fold wins counted on
net Sharpe, the concentration clause on the per-fold mean return difference — *is what produces this
verdict*, so it is stated in the claims policy rather than chosen after the fact).

There is a subtler payoff, and for anyone who works on panels it is the useful part. The standard worry
with testing several things is multiple testing, and the standard fix is a correction. But if you fire
exactly once, the correction is inert: with one pre-registered comparison the deflated Sharpe ratio
collapses to the probabilistic one. What remains binding is not the correction — it is the **choice of
benchmark**. My candidates both *pass* a deflated Sharpe test against zero (p = 0.0032 and 0.0017) and
both *fail* the probabilistic test against the best baseline (0.495 and 0.587). If I had reported the
headline number and stopped, I would have reported a pass. The benchmark is the finding, and
pre-registration is what stopped me from choosing it afterwards.

## Defence 2 — prove no leakage mechanically

"We reviewed the backtest and it doesn't leak" is a claim about code, and reading code is not a proof.
So leakage is not argued here; it is a suite of tests, each one an executable definition of a specific
way a walk-forward backtest can see the future: no look-ahead in the eligible set, no peeking at the
test block, costs that cannot reach the optimiser that prices them.

The sharpest example of why inspection fails is a bug in my own estimator layer. Two logically identical
data frames returned covariance estimates differing in the last bit — because pandas reduces along a
block's *strides*, and a single `frame.loc[row] = value` assignment is enough to leave a frame in
Fortran order. That matters far more than it sounds. My leakage suite includes a bit-identical
determinism requirement, and under that requirement a floating-point wobble caused by my own memory
layout is **indistinguishable from leaked information**. The test would have reported my own numerical
noise as a leak. The fix is one explicit contiguity guarantee; the durable artefact is the test that
pins it.

And a test can pass for the wrong reason, which has to be said out loud. One test in the suite is
**vacuous**: no instrument in my universe delisted during the sample, so the survivorship test has
nothing to bite on. It is recorded as a skip with the reason, not as a pass. A green check with no
power behind it is worse than a red one, because it buys silence.

## Defence 3 — certify the numerics

This is where the project spent most of its effort, and it is where the best story is, so I have kept it
in full.

Every one of the 1,176 rebalances is checked against a primal KKT residual, and no rebalance is allowed
to fall back to a different solver. The result: 1,176 solves, zero rejections, worst residual 1.49e-11
against an acceptance tolerance of 1e-7 — about 6,700 times inside the bar. On its own that sentence is
almost worthless, because it describes the final state. What makes it worth something is the three
separate occasions on which **the certificate itself was wrong**:

- It recovered a Lagrange multiplier by taking a median over the "smooth interior" and falling back to
  zero when that set was empty — which happens exactly when the turnover penalty makes *holding* optimal.
  That fallback rejected **seven provably optimal solutions**, with residuals up to 1.5e-3, while three
  independent solvers agreed on the objective to 1e-10.
- A redundant constraint — `nonneg=True` on an auxiliary variable already implied to be non-negative by
  its own defining constraints — added a row to the solver's constraint matrix and changed its path. With
  it, one rebalance solved to `optimal_inaccurate` at a point 2.8e-11 *below* the optimum. Mathematically
  equivalent, numerically not.
- Most embarrassing of all: **the script doing the certifying was solving a different problem.** It
  rebuilt the rebalance loop by hand and passed one method a constant equal-weight starting holding,
  where production passes the *drifted* holding. It reported that method clean while production was
  rejecting rebalances. Evidence the artefact under test did not produce is not evidence.

Then the claim I would have bet on failed too.

I wrote that the repository reproduces its published table bit-for-bit, and added a check that could test
it against the frozen release archive. The first run of that check failed by `4.2e-17` on exactly one of
eighteen columns. The cause was not my code's logic: that metric reached a BLAS kernel that OpenBLAS
chooses *at run time* from the CPU's features, so the summation order had never actually been specified.
I replaced it with a summation whose every rounding step is defined by the IEEE-754 standard, which is
bit-identical anywhere and slightly *more* accurate. I measured the cost of that fix rather than
asserting it: regenerate the table, diff all 46 columns — exactly one moved, in its last three bits, and
no headline number moved.

The next run failed **harder**. Thirteen of the eighteen columns moved, the worst by `4.698e-12`.

I ruled out the boring explanations instead of assuming them. The two runs installed an identical set of
51 packages (parsed as sets; symmetric difference empty) on an identical runner image. Not dependency
drift. Thread count? I ran the whole pipeline locally with one BLAS thread and with four: byte-identical
tables, both matching the published one. Not threading. Then the diagnosis fell out of a single column —
`turnover_annualized` moved, and it is a function of the portfolio weights *alone*. The two machines had
solved to slightly different portfolios, and the metric differences were downstream of that. And the
magnitude said which layer was responsible: a rounding error at these magnitudes is `1e-16`, and the
largest difference was `4.698e-12` — four orders of magnitude bigger — a `1e-16` difference in the
covariance matrix, amplified by an optimiser whose own acceptance tolerance is `1e-14`.

That is not a bug that can be fixed, and pretending otherwise would have been the mistake. **A number
produced by a solver is a property of the data, the code *and the machine*, not just the first two.** The
solve is defined only to the solver's tolerance, so "the number" was never as solid as the table it sat
in.

So the repair was not to widen a tolerance and keep the wording. It was to notice that I had been making
two different claims and dressing them identically:

- **Decisions are exact.** Which methods ran, how many rebalances, how many folds, the headline cost
  level, the ranking by net Sharpe, which baseline the rules select. These are discrete, they are what
  the experiment is *for*, and a `1e-12` wobble cannot move them. Any difference fails the build.
- **Measurements are bounded.** The continuous metrics are compared against a documented `1e-9` — about
  200 times the worst cross-platform difference I measured, and five orders of magnitude below the four
  decimals any of these numbers is ever quoted at. The observed worst difference is printed on every
  run, so the bound is spent in public rather than asserted.

The check now runs on every push. It prints the difference it actually saw — `4.698e-12` — rather than
the bound it was allowed, and reports that every decision is identical. That is the only claim in this
project that has been falsified twice and then survived: the third machine to run it differed on the
measurements by exactly the amount the bound had been set to absorb, and agreed on everything that
decides.

## Defence 4 — significance *and* materiality *and* robustness

The four defences exist because each of the previous three can be satisfied while the conclusion is still
wrong. Overfitting is not the only way to fool yourself. You also fool yourself by optimising the
decision rule, so the rule is a conjunction (as above), and by reporting the fold that worked, so fold
wins carry their denominator and a concentration clause.

The live demonstration is the one worth keeping: both candidates pass the p-value test against zero and
fail the significance test against the benchmark. Two honest statistics, pointed at two different
questions, disagreeing — and the protocol says you must answer both. A single number would have hidden
the entire finding.

## The defence that failed

Now the part I would want a reader to attack.

The conflict was real. The report generator is the artefact the whole "check these numbers" claim rests
on: a table, produced from an immutable snapshot, that a stranger can regenerate. Validating it end to
end requires executing the frozen configuration — because that is the configuration being reported. But
the frozen configuration *is* the confirmatory configuration. Validating the generator and blinding the
confirmatory test were mutually exclusive, and I did not see that until I had already chosen.

I chose the generator. So the registered test is re-designated **executed (non-confirmatory)**: the
execution happened, the numbers are real, and it was not blind. No confirmatory test now exists. The
hypotheses are **untested, not falsified** — the frozen rule returns failure for both candidates either
way, but it was never applied blind, and I am not going to call it a test in order to have a result.

What a valid one would need, concretely: a **new sample**. A different asset class, or a period that does
not yet exist, registered before the data does. Blindness cannot be restored once lost, and a
re-designation does not repair it — it just names it correctly.

## The result, read properly

Here is why the null is worth more than a shrug. The candidates' return series correlate with the best
baseline at ρ = 0.9845 and 0.9856, and the paired differences are +0.4% and +0.6% per year. This design
was powered to separate a net Sharpe difference of roughly 0.13 to 0.20 between strategies this
correlated, and the observed gaps are 0.064 and −0.004. Every interval overlaps the baseline's. So the
effect is **absent, not invisible** — which is a much stronger statement than "not significant".

The diagnostics explain why, and I will label this as what it is: a hypothesis, not a result. Eighteen
assets, but an effective number of independent bets of only about 3 to 5 — measured by participation
ratio and by entropy — with a correlation matrix condition number around 1.7e3, and twelve of the eighteen
eigenvalues below the lower edge of the Marchenko–Pastur band for a panel of this shape (the smallest sits
85× below that edge). In that regime shrinkage has very little noise to bite on,
and the uniform 30% position cap is doing more regularisation than the estimator is. It is testable:
relax the cap and compare shrinkage across cap levels. It is also, plausibly, the most interesting thing
this project has produced, and it is exactly the kind of tidy story that a null is supposed to prevent me
from believing, which is why it is labelled a hypothesis.

## What a reader can do with this

The four defences transfer to any panel you already work on, and none of them needs a portfolio:

1. **Freeze before looking.** Write the decision rule where you cannot reach it, and date it.
2. **Prove the absence of leakage mechanically.** "We reviewed it" is not a defence. And record the tests
   that are vacuous rather than letting them pass.
3. **Certify the numerics.** A solver failure or a library reduction can masquerade as a finding, and the
   certificate is a piece of software too — mine was wrong three times.
4. **Require significance, materiality and robustness together.** Any one alone is a target.

And the check I would ask you to run: clone the repository, run `verify_release.py` against the release
archive, and tell me if it prints anything other than `EXACT` or `WITHIN`. That claim puts the
falsification burden on the artefact rather than on my summary of it, which is the only kind of claim
worth making in public.

## What I would do differently

Validate the report generator on a **different** snapshot, so the confirmatory configuration stays
unexecuted. Write down the *reproduction* claim only after the check that tests it exists — I wrote
"bit-for-bit" first and discovered what it meant second, twice. And state every claim at the strength its
check actually has, from the beginning: exactly where it is exact, bounded where it is bounded, and with
the measured number printed rather than the tolerance quoted.
