#import "generated/numbers.typ": *

// ---------------------------------------------------------------------------
// Formatting helpers. Every number below comes from generated/numbers.typ;
// this file contains the argument and no measurement.
// ---------------------------------------------------------------------------

#let fmt(x, digits) = {
  let s = str(calc.round(x, digits: digits))
  // `calc.round(40.0, digits: 0)` stringifies as "40." in this Typst version.
  if s.len() > 0 and s.at(s.len() - 1) == "." { s = s.slice(0, s.len() - 1) }
  let parts = s.split(".")
  let out = if parts.len() == 1 {
    if digits == 0 { s } else { s + "." + "000000".slice(0, digits) }
  } else {
    let have = parts.at(1).len()
    if have < digits { s + "000000".slice(0, digits - have) } else { s }
  }
  out.replace("-", "−")
}

#let ci(low, high) = "[" + fmt(low, 3) + ", " + fmt(high, 3) + "]"
#let pct(x, digits) = fmt(x * 100, digits) + "%"

#let id-cell(r) = if r.candidate or r.id == best { strong(r.id) } else { r.id }
#let pass-cell(ok) = if ok {
  text(fill: rgb("#1c6b3c"), weight: "bold")[pass]
} else {
  text(fill: rgb("#9c3527"), weight: "bold")[fail]
}

#let max-gap = calc.max(..verdicts.map(v => v.gap))
#let min-dsr = calc.min(..verdicts.map(v => v.dsr))
#let max-dsr = calc.max(..verdicts.map(v => v.dsr))

// Named records rather than positions: the tables' row order is a property of
// the run, and prose that indexes it would break silently if it changed.
#let v1 = verdicts.filter(v => v.id == "M1").first()
#let v2 = verdicts.filter(v => v.id == "M2").first()
#let b3 = rows.filter(r => r.id == best).first()
#let b5 = rows.filter(r => r.id == "B5").first()
#let top = rows.first()

// ---------------------------------------------------------------------------
// Page and type
// ---------------------------------------------------------------------------

#set document(
  title: "The benchmark is the binding constraint",
  author: "Ken Ira Lacson Talingting",
  keywords: ("pre-registration", "portfolio construction", "reproducibility", "null result"),
)

#set page(
  paper: "a4",
  margin: (top: 24mm, bottom: 24mm, x: 25mm),
  footer: context [
    #set text(size: 7.5pt, fill: luma(115))
    #grid(
      columns: (1fr, auto),
      [github.com/kira-ml/robustfolio],
      align(right)[#counter(page).display("1")],
    )
  ],
)

#set text(font: "New Computer Modern", size: 10.5pt, lang: "en", hyphenate: true)
#set par(justify: true, leading: 0.70em, spacing: 1.05em)

#set heading(numbering: "1.1")
#show heading.where(level: 1): it => block(above: 1.6em, below: 0.55em)[
  #set text(size: 13pt, weight: "bold")
  #it
  #v(-0.35em)
  #line(length: 100%, stroke: 0.4pt + luma(165))
]
#show heading.where(level: 2): it => block(above: 1.5em, below: 0.40em)[
  #set text(size: 11pt, weight: "bold")
  #it
]

#set figure(numbering: "1")
#set table(stroke: none, inset: (x: 4pt, y: 3.2pt))
#set list(spacing: 0.55em)
#set enum(spacing: 0.55em)

#show figure: set block(spacing: 1.5em)
#show figure.caption: it => block(width: 100%, above: 0.45em)[
  #set text(size: 8.8pt)
  #set par(justify: false, leading: 0.55em)
  // Left, not centred: a centred caption indents its first line to wherever the
  // longest line happens to start, so two tables side by side begin differently.
  #align(left, it)
]
#show table: set text(hyphenate: false)

// ---------------------------------------------------------------------------
// Front matter
// ---------------------------------------------------------------------------

#align(center)[
  #text(size: 20pt, weight: "bold")[The benchmark is the binding constraint]
  #v(0.30em)
  #text(size: 11pt)[
    A registered comparison of seven portfolio constructions, four defences against
    fooling yourself, and a reproduction claim that was wrong twice
  ]
  #v(0.95em)
  #text(size: 10pt)[Ken Ira Lacson Talingting]
  #v(0.10em)
  #text(size: 8.5pt, fill: luma(100))[Working paper · October 2026]
]

#v(0.9em)

#block(
  width: 100%,
  fill: luma(246),
  stroke: 0.5pt + luma(200),
  inset: 9pt,
)[
  #set text(size: 9pt)
  #set par(leading: 0.62em)
  *Status: EXPLORATORY AND NON-CONFIRMATORY.* The registered test was executed without the
  blindness its registration required, so this run may not be cited for or against either
  hypothesis: the hypotheses are *untested, not falsified*. The verdict the frozen rule
  returns is quoted below for completeness; it is not a test of anything. The description
  this work asks to be held to is _pre-registered, mechanically evaluated,
  non-confirmatory_. Net *excess* Sharpe only, at stated costs, with intervals; no absolute
  return claim; nothing here is an investable return.
]

#v(0.9em)

#block(inset: (left: 7pt, right: 7pt))[
  #set text(size: 9.6pt)
  #set par(leading: 0.64em)
  *Abstract.* This paper compares #n-methods constructions for spreading a portfolio across
  #n-assets US equity, bond, commodity and real-estate ETFs over #n-months out-of-sample
  months. Two
  of them are treatments, and each differs from a sample-covariance, sample-mean
  mean--variance baseline (`B3`) in exactly one component: `M1` replaces the sample
  covariance with a Ledoit--Wolf shrinkage estimate; `M2` replaces the sample mean with a
  Black--Litterman posterior. The decision rule was fixed before the run and is a
  conjunction — a net excess Sharpe advantage of at least #fmt(gap-bar, 2) over the best
  baseline, a probabilistic Sharpe ratio of at least #fmt(psr-bar, 2) against that same
  baseline, and six robustness gates — not a ranking. Both treatments fail. The larger
  advantage, #fmt(max-gap, 3) against a bar of #fmt(gap-bar, 2), is a point estimate whose
  interval overlaps the baseline's, and it belongs to the treatment that changes the mean
  rather than the covariance. The same two strategies clear a deflated-Sharpe test against
  zero at p = #fmt(min-dsr, 4) and #fmt(max-dsr, 4), which places the binding constraint in
  the declared benchmark rather than in the multiple-testing correction. Because validating
  the reporting layer required running the frozen configuration first, no blind test exists:
  the run is exploratory and the hypotheses are untested, not falsified. The paper's second
  subject is the instrument — what a reproduction check can prove, and what it cannot.
]

#v(0.6em)

// ---------------------------------------------------------------------------
// 1
// ---------------------------------------------------------------------------

= The question

Robust portfolio construction is usually sold as a cure for estimation error. The argument is
old and sound [1]: a mean--variance optimiser treats estimated means and covariances as if
they were known, so it loads on the assets whose estimates are most optimistic, and the
portfolio it produces is often worse out of sample than equal weight [2]. The proposed cures
— shrink the covariance [3], put a prior on the mean [4] — are well motivated. The evidence
offered for them is usually a backtest in which the cured portfolio has a higher Sharpe ratio.

This paper takes that last step seriously. A higher number is not evidence unless four things
hold: the comparison changes one thing; the rule that would reject the improvement was fixed
before the result was seen; the improvement is large enough to matter; and the numbers can be
checked by someone who does not trust the author. The first three are design choices. The
fourth is an engineering one, and it is the one this project spent most of its effort on.

The result here is a null. Two treatments that differ from a mean--variance baseline in
exactly one component each — a shrinkage covariance and a Black--Litterman mean — produce no
net excess Sharpe advantage large enough to clear a bar fixed in advance, on a sample
powered to detect an effect at that bar. Both fail the registered rule. Neither is rescued by
a cost sweep or by the fold structure, and the intervals do not separate them from the
baseline.

Four things are contributed, and only the first is a result:

+ a single-factor registered comparison, in which each treatment differs from the baseline in
  one component, so a difference is attributable to that component rather than to a bundle;
+ evidence that under a single registered comparison the deflation machinery is inert, and
  the *declared benchmark* is what decides the test — which makes fixing the comparator a
  statistical requirement rather than bookkeeping;
+ a reproduction protocol that splits the claim in two: decisions compared exactly,
  measurements compared within a bound, with the observed difference printed on every run;
+ a reported null, with the rule that produced it, the reading it depends on, and the
  circumstances under which it would have said otherwise.

What this is not: a claim of tradable alpha, a confirmatory test, or a survey. The sample is
one universe, one period, one cost model, and the hypotheses remain untested.

// ---------------------------------------------------------------------------
// 2
// ---------------------------------------------------------------------------

= Design

== Universe and sample

The universe is #n-assets US-listed ETFs spanning equity, fixed income, commodities and real
estate. Membership is reconstructed from a date-stamped candidate list in which each fund
carries the date from which it is eligible, so no instrument enters before it existed. This
is point-in-time *eligibility*, not point-in-time *data*: the prices are what a 2026 vendor
holds for 2012 today, and price history is revised. The distinction is not repaired here and
it is not small.

Rebalancing is monthly, on the last trading day. The estimation window is 60 months, rolling
and re-estimated every month; test windows are twelve months and do not overlap. Portfolios
are fully invested and long only, with a uniform 30% cap on any position, and the
mean--variance constructions share a risk aversion of 10. Costs are charged one way at a
headline #headline-bps basis points, and the run reports every metric at
#cost-levels.map(c => str(c)).join(", ") basis points so that the headline is a choice among
reported levels rather than a number selected after the fact.

The sample begins with the first eligible month, in mid-2012, and ends in September 2026:
#n-months monthly rebalances in #n-folds non-overlapping twelve-month folds, and #n-solves
optimiser solves across the #n-methods constructions.

== Seven constructions

Five are baselines and two are treatments. The treatments are single-factor by construction:
`M1` is `B3` with the sample covariance replaced by a Ledoit--Wolf shrinkage estimate; `M2`
is `B3` with the sample mean replaced by a Black--Litterman posterior. Universe, window,
optimiser, constraints, costs and rebalancing are shared. A difference between a treatment and
`B3` is therefore attributable to the one component that changed — and that minimal-difference
design is also what buys the statistical power, because the paired comparison of two
almost-identical return series is far more sensitive than the comparison of either to zero.

#figure(
  table(
    columns: (auto, 1.25fr, 1.05fr, 1fr),
    align: (left, left, left, left),
    inset: (x: 5pt, y: 4pt),
    table.hline(stroke: 0.8pt),
    table.header([ID], [Construction], [Differs from `B3` in], [Role]),
    table.hline(stroke: 0.4pt),
    [*B1*], [Equal weight], [no optimiser], [Primary benchmark],
    [*B2*], [Risk parity], [equal risk contribution], [Practitioner default],
    [*B3*], [Sample MVO], [—], [Critique target],
    [*B4*], [Minimum variance], [no mean], [Robust alternative],
    [*B5*], [Turnover-penalised MVO], [an L1 penalty], [Robust baseline],
    [*M1*], [Shrinkage-covariance MVO], [the covariance], [Treatment, H2.1],
    [*M2*], [Black--Litterman MVO], [the mean], [Treatment, H2.2],
    table.hline(stroke: 0.8pt),
  ),
  caption: [The seven constructions. `M1` and `M2` each change one component of `B3`, so a
    difference between a treatment and the baseline is attributable to that component; nothing
    else differs, including the constraints and the cost model. `B3` was the best baseline in
    this run.],
) <tab-methods>

== The decision rule

The registered rule is a conjunction of eight gates, applied to the best baseline rather than
to zero:

+ a probabilistic Sharpe ratio against the best baseline of at least #fmt(psr-bar, 2) —
  the probability that the candidate's Sharpe exceeds the baseline's;
+ a deflated-Sharpe p-value of at most #fmt(dsr-bar, 2)\;
+ a net excess Sharpe advantage over the best baseline of at least #fmt(gap-bar, 2)\;
+ a turnover ratio against the baseline of at most #fmt(turnover-limit, 2)\;
+ a drawdown slack of at least #fmt(drawdown-min, 3)\;
+ a win at #cost-required of the #n-cost-levels cost levels;
+ a win in at least #folds-required of the #n-folds folds;
+ no single fold contributing more than #pct(fold-limit, 0) of the advantage.

Every threshold is read from the published verdict table rather than restated by hand, and
@tab-gates prints the rule gate by gate for both candidates.

Significance alone admits improvements too small to act on; materiality alone admits noise.
Requiring both, plus robustness across cost levels and folds, is what makes a null
informative: a candidate that fails has failed at the bar the design was built to detect, not
at an arbitrary one. Two caveats belong with the rule rather than in a footnote. The fold gate
is weak: if folds were coin flips, #pct(sourced.fold-null-rate, 1) of null experiments would pass it
on their own, and the folds share overlapping training windows, so the true rate is higher.
And the materiality gate is a decision about the world, not a statement about noise: it says
an improvement is too small to act on, which is why the bar is stated in the units the
decision is made in.

== What was fixed before the run

The registration fixed the hypotheses — H2.1, that a shrinkage covariance beats the sample
covariance on net Sharpe, and H2.2, that a Black--Litterman posterior beats the historical
mean — together with the metric, the thresholds, the headline cost level, the fold structure
and the conjunction above. It also fixed the comparator *mechanically*: the rule names the
best baseline, where "best" is defined as the highest net Sharpe among the five baselines.
The identity of that baseline is an output of the run, but the definition that selects it is
not, so the comparator cannot be chosen by hand after the answer is known. @sec-benchmark
argues that this distinction carries most of the weight; @sec-limits records what it does not
settle.

What the registration did not fix, because it could not, is the order in which the reporting
layer and the test would run. @sec-failed is about that.

// ---------------------------------------------------------------------------
// 3
// ---------------------------------------------------------------------------

= Results

== The null

@tab-results and @fig-intervals report the same estimates. `B3`, the plain
sample-covariance, sample-mean optimiser that the project set out to critique, is the best
baseline at #fmt(b3.point, 4). `M2` has the highest point
estimate of any construction, #fmt(top.point, 4),
an advantage of #fmt(max-gap, 3). That is below the #fmt(gap-bar, 2) bar. `M1` lands on `B3`:
its advantage is #fmt(v1.gap, 3), which is to say none.

#figure(
  table(
    columns: (1.0fr, 1.35fr, 1.55fr, 1.0fr, 1.15fr),
    align: (left, right, right, right, right),
    table.hline(stroke: 0.8pt),
    table.header(
      [Method], [Net excess Sharpe], [#(ci-level)% interval], [Turnover], [Max drawdown],
    ),
    table.hline(stroke: 0.4pt),
    ..rows.map(r => (
      id-cell(r),
      [#fmt(r.point, 4)],
      [#ci(r.low, r.high)],
      [#fmt(r.turnover, 2)],
      [#pct(r.drawdown, 1)],
    )).flatten(),
    table.hline(stroke: 0.8pt),
  ),
  caption: [Net excess Sharpe at the #headline-bps bps one-way headline cost, with a
    #(ci-level)% stationary-bootstrap interval (#ci-reps replications, mean block
    #fmt(ci-block, 0) months), annualised turnover, and maximum drawdown of the net excess
    series. Candidates are bold. Exploratory and non-confirmatory: no confirmatory test
    exists, and these numbers may not be cited for or against either hypothesis.],
) <tab-results>

#figure(
  image("generated/intervals.png", width: 100%),
  caption: [The same seven estimates as intervals. The shaded band is the distance the
    materiality gate requires — #fmt(gap-bar, 2) of net excess Sharpe to the right of
    #(best) — so a candidate clears it only if its dot sits to the right of the band.
    Intervals overlap for every pair of constructions. Exploratory and non-confirmatory.],
) <fig-intervals>

The intervals are the result, and the ordering is not. Every construction's #(ci-level)%
interval overlaps the interval for `B3`, most of them by a wide margin, so the table's ordering by point
estimate is a ranking of estimates rather than a separation of strategies. The two treatments
carry as much turnover as the baseline or more.

Both treatments fail the rule. @tab-gates shows why, and the failures are not marginal:
`M2` passes five of the eight gates and fails three, `M1` passes three and fails five. The
gate that decides both is the probabilistic Sharpe ratio, where they score
#fmt(v1.psr, 3) and #fmt(v2.psr, 3) against a bar of
#fmt(psr-bar, 2). The concentration gate also fails for both: even where an advantage exists,
it lives in a single fold — #pct(v1.fold-share, 1) for `M1` and
#pct(v2.fold-share, 1) for `M2`, against a #pct(fold-limit, 0) limit.

`M2` is worth a second look, because it is the case where a careless report would have found
a win. It leads the ranking, wins #v2.cost-won of the #n-cost-levels cost levels
and #v2.folds-won of the #n-folds folds, and clears the deflated-Sharpe gate. It
still fails on the two gates that ask whether the advantage is *worth having*: the gap and
the probability that the gap is real. That is the conjunction working as designed — the
robustness gates are satisfied and the materiality gate is not, so the answer is no.

One reading is load-bearing and is disclosed rather than buried. The protocol requires the
advantage to hold across folds but does not pin "advantage" to a metric. The reading used
here — fold wins measured on net Sharpe, the concentration clause measured on the per-fold
mean-return difference — is the reading that decides the verdict for `M2`, because the concentration
gate fails at #pct(v2.fold-share, 1). Whether a different reading would change
the verdict is a computation that has not been run, and this paper does not claim it would.
The verdict is therefore the output of a stated reading, not of the arithmetic alone.

#figure(
  table(
    columns: (1fr, auto, auto),
    align: (left, center, center),
    table.hline(stroke: 0.8pt),
    table.header([Gate], [#v1.id], [#v2.id]),
    table.hline(stroke: 0.4pt),
    ..(
      (
        (key: "psr", label: [PSR against the best baseline, at least #fmt(psr-bar, 2)]),
        (key: "dsr", label: [Deflated-Sharpe p-value, at most #fmt(dsr-bar, 2)]),
        (key: "gap", label: [Net Sharpe gap over the best baseline, at least #fmt(gap-bar, 2)]),
        (key: "turnover", label: [Turnover ratio, at most #fmt(turnover-limit, 2)]),
        (key: "drawdown", label: [Drawdown slack, at least #fmt(drawdown-min, 3)]),
        (key: "cost", label: [Cost levels won, at least #cost-required of #n-cost-levels]),
        (key: "folds", label: [Folds won, at least #folds-required of #n-folds]),
        (key: "share", label: [Largest fold share, at most #pct(fold-limit, 0)]),
      ).map(spec => (
        [#spec.label],
        pass-cell(v1.gates.at(spec.key)),
        pass-cell(v2.gates.at(spec.key)),
      )).flatten()
    ),
    table.hline(stroke: 0.4pt),
    [Passed], [#v1.passed of 8], [#v2.passed of 8],
    [Verdict], strong(v1.verdict), strong(v2.verdict),
    table.hline(stroke: 0.8pt),
  ),
  caption: [The registered conjunction. A candidate passes only if all eight gates pass.
    `M2` clears the statistical gate, the robustness gates and the concentration clause's
    siblings, and fails the two gates that ask whether the advantage is large enough to
    matter.],
) <tab-gates>

== The benchmark, not the correction, is the binding constraint
<sec-benchmark>

Both treatments clear the deflated-Sharpe test against zero: p = #fmt(v1.dsr, 4)
and #fmt(v2.dsr, 4). Both fail the probabilistic Sharpe test against `B3`:
#fmt(v1.psr, 3) and #fmt(v2.psr, 3). Same return series, opposite
conclusions, and the only difference is what each statistic is measured against.

That is not a paradox. With exactly one registered comparison the family size is one, so the
selection deflation is inert: the deflated Sharpe ratio and the probabilistic Sharpe ratio
differ only in their reference point, zero in one case and `B3` in the other. The machinery
the project specified to correct for multiple testing never fires, because with one test there
is nothing to correct. What remains binding is the benchmark — the one input to the test that
the analyst chooses, and the input for which, after the fact, there is always a flattering
value.

Both p-values answer "is this strategy's Sharpe greater than zero", not "is it better than the
baseline". A reader who takes p = #fmt(min-dsr, 4) as evidence of improvement has answered a
question nobody asked. This is the sentence the project exists to make difficult to skip.

== The cost sweep, and the turnover inversion

@tab-sweep reports the same metric at each of the #n-cost-levels cost levels. Across them the
advantage of `M2` over `B3` moves between #fmt(v2.sweep-low, 3) and
#fmt(v2.sweep-high, 3)\; the advantage of `M1` between
#fmt(v1.sweep-low, 3) and #fmt(v1.sweep-high, 3). The bar is
#fmt(gap-bar, 2) at every level. Sweeping costs does not make a null true, but a conclusion
that reversed between two adjacent cost levels would not be worth an interval, and this one
does not reverse.

#figure(
  table(
    columns: (auto,) * (n-cost-levels + 1),
    align: (left,) + (center,) * n-cost-levels,
    table.hline(stroke: 0.8pt),
    table.header(table.cell(colspan: 1)[Method], ..cost-levels.map(c => [#c bps])),
    table.hline(stroke: 0.4pt),
    ..rows.map(r => (
      id-cell(r),
      ..r.sweep.map(v => [#fmt(v, 4)]),
    )).flatten(),
    table.hline(stroke: 0.8pt),
  ),
  caption: [Net excess Sharpe at each reported one-way cost level. The headline level is
    #headline-bps bps. Exploratory and non-confirmatory.],
) <tab-sweep>

The usual story for robust construction is that it wins by trading less. Here it inverts.
`B3` carries #fmt(b3.turnover, 2) annualised turnover and
still leads on net excess Sharpe at the headline cost, while `B5`, the turnover-penalised
baseline, cuts turnover to #fmt(b5.turnover, 2) and lands
below `B3`. The two treatments carry as much turnover as the baseline or more. In this sample,
turnover penalisation bought a real reduction in trading and did not buy an improvement in net
Sharpe, while the highest-turnover construction was the best performer. That is a legitimate
outcome, and it is the kind of thing a single headline number would have hidden.

== A diagnostic hypothesis, labelled as one

Eighteen assets are not eighteen bets. On the frozen window the effective number of
independent directions is #fmt(sourced.n-part, 2) by participation ratio and
#fmt(sourced.n-ent, 2) by entropy — far below #n-assets. The near-singularity is structural
rather than a short-sample artefact: for an independent panel of this shape the
Marchenko--Pastur band would be [#fmt(sourced.mp-low, 3), #fmt(sourced.mp-high, 3)], and
#fmt(sourced.mp-below, 0) of the #n-assets eigenvalues fall below the lower edge, the smallest at
#fmt(sourced.smallest-eig, 4), about #fmt(sourced.edge-ratio, 0) times below it [8].

If that is the right reading, shrinkage has little independent noise to bite on, and the
uniform 30% cap is doing more regularisation than the estimator is. That would explain why
`M1` lands on `B3`, and why `M2` — the only treatment that changes the mean rather than the
covariance — is the only one that moves the point estimate at all. It is a hypothesis and it
is labelled as one: the cap sweep that would test it, across four values of the cap, was
registered and has never been run.

// ---------------------------------------------------------------------------
// 4
// ---------------------------------------------------------------------------

= The defence that failed
<sec-failed>

Four defences were built before the result was read. Freeze the metric, thresholds and decision
rule before looking, so the comparator cannot be chosen after the answer is known. Prove the
absence of leakage mechanically, with a test suite rather than a code review — including one
test recorded as vacuous rather than passed. Certify the numerics: every rebalance's KKT
residual checked against a frozen tolerance, #n-solves solves with zero rejections and a worst
residual of #sourced.kkt-worst against a #sourced.kkt-bar bar. And require significance,
materiality and robustness together rather than any one of them.

Three of the four held. The first failed, and it failed for the most ordinary of reasons: the
reporting layer had to be validated before any result could be read, and the only
configuration that could validate it was the frozen one — which was the registered one.

State that precisely, because the difference between an accident and a design failure matters.
The registration required that the confirmatory test be executed blind: the analyst must not
know the answer when the test runs. Validating the generator required re-running the harness on
the frozen configuration and reading its table. The frozen configuration is the confirmatory
configuration. So the answer was on screen, in a file being diffed, before the test ran.
Nothing was edited; no threshold moved; the rules that ran were the ones written down. The
blindness was gone.

The consequence is not cosmetic. A test that was not blind is not a confirmatory test, and
blindness cannot be restored to a sample whose answer has been seen. The run is therefore
exploratory and non-confirmatory, and the hypotheses are *untested, not falsified* — a
distinction the project's claims policy fixes in advance, precisely so that a result like this
one cannot later be relabelled into support. The registered rule's verdict stands as an output
of the rule, and is not evidence about H2.1 or H2.2 in either direction.

What survives is the design, the numbers and the disclosure. What does not survive is any
claim that either hypothesis has been tested. A confirmatory statement would need a sample that
does not yet exist, registered before it does.

// ---------------------------------------------------------------------------
// 5
// ---------------------------------------------------------------------------

= Reproduction: what a check can prove

The numbers in this paper are checkable because the repository ships the frozen archive and a
verifier that recomputes both tables from it. That instrument makes a stronger claim than "the
code runs": it compares. The claim it made first was too strong, and the check itself falsified
it twice.

== Two failures

The original claim was exact equality — the same bytes and the same code produce the same
table, on any machine. The first run of the comparison found one column, an autocorrelation,
differing by #sourced.blas-diff: three units in the last place. The cause was not the
arithmetic but the kernel. The correlation went through a BLAS routine whose implementation is
selected at run time from the CPU's feature set, so the same expression rounded differently on
a different CPU. The fix was to compute that column with exactly-rounded summation, so that
every rounding step is defined by IEEE-754 rather than chosen by a kernel.

The second run failed harder: thirteen of the eighteen columns moved, the worst by
#sourced.worst-diff. That one is not a defect and cannot be fixed the same way. The covariance
is a matrix product evaluated by a runtime-chosen kernel, and a quadratic program is solved
only to its tolerance — a perturbation of one part in $10^16$ in the input reappears in the
weights at about $10^(-12)$. Asking a solver's output to be bit-for-bit equal across machines
asks for a property the artefact never had.

== The split

The response was not to widen the tolerance until the check passed. It was to notice that the
claim had been about two different kinds of object. Decisions are discrete: which methods ran,
how many rebalances and folds, the headline cost level, the ranking, the selected baseline, the
eight gates and the verdict. Measurements are continuous: the metrics and the statistics the
verdict was computed from. The first set is compared exactly, and any difference fails the
build. The second is compared within #sourced.tolerance, and the difference actually observed
is printed on every run rather than the bound being quoted. The bound is roughly two hundred
times the worst cross-machine difference measured, and five orders of magnitude below the
precision at which these numbers are reported.

That split is this section's methodological claim, and it generalises beyond this project: a
reproduction claim should be stated separately for the objects that cannot wobble and the
objects that can. "It reproduces" is not one claim.

== A check that can be seen refusing

A check that has never failed is untested. This one has failed twice on real data, and the
repository also ships a demonstration that tampers with in-memory copies of the published
tables to show the refusal working: a measurement moved by 0.01 is refused and the column
named; a verdict flipped from `FAILURE` to `SUCCESS`, with every statistic untouched, is
refused with `VERDICT differs`; and a difference of $10^(-12)$, the scale a different machine
produces, is absorbed, because a check that fails on platform noise is useless. The first two
are the behaviour that matters and the third is what makes the check usable.

One limit remains, and it is worth stating rather than leaving to be found. No real run has
ever disagreed with the published verdict, so the verdict-refusal path is demonstrated
synthetically and not on a genuine disagreement.

// ---------------------------------------------------------------------------
// 6
// ---------------------------------------------------------------------------

= Limitations and what would change the verdict
<sec-limits>

*The sample.* One universe of #n-assets funds, one period of #n-months out-of-sample months in
#n-folds folds, one asset-class family. The design can separate a net excess Sharpe difference
of roughly #fmt(sourced.paired-mde-980, 2) to #fmt(sourced.paired-mde-950, 2) between these
highly correlated strategies, and it is silent about smaller effects. The null is therefore
"no effect at or above the bar", not "no effect". A true improvement of half the bar would not
have been detected here and must not be reported as though it had been.

*The comparator.* The rule compares against the best baseline, identified mechanically after
the run. The definition is fixed and the identity is not, which is weaker than naming the
comparator in the registration. In this sample `B3` was the best baseline by a margin
#fmt(b3.point - b5.point, 4)
over the next one, so the choice is not close; that is a fact about this run, not a property of
the design.

*The cost model.* A flat one-way cost with no market impact, capacity, taxes or regime
dependence. Costs cannot reach the optimiser: each rebalance is solved once and every cost
level is derived from that single turnover series, so a cost level cannot influence the weights
it prices. A capacity-constrained version would likely penalise the two high-turnover
treatments, which would make the null stronger rather than weaker — but that is an argument,
not a measurement.

*The reading.* One clause of the rule is not pinned to a metric, and the reading used here
decides one candidate's verdict. A different reading is a different computation; it has not
been run, and the paper does not claim it would change the result.

*The status.* No confirmatory test exists, so nothing here is evidence for or against H2.1 or
H2.2. This is the binding limitation: the other four qualify a null, and this one says the null
is not a test.

What would change the verdict: a confirmatory replication on a sample that did not exist when
it was registered, with the same rule and the same bar; a cap sweep that isolates how much of
the regularisation comes from the constraint rather than the estimator; a wider universe; and a
cost model with impact. An effect at or above the bar, with an interval that excludes the
baseline, would also do it — and would be the outcome the design was built to detect.

// ---------------------------------------------------------------------------
// 7
// ---------------------------------------------------------------------------

= Reproducing this paper

Every number in @tab-results, @tab-sweep and @tab-gates, and in @fig-intervals, is read from
`docs/published-run/` by `scripts/build_paper.py`. The paper's source contains no typed
measurement, and a test checks that by searching it for the values in the tables. To check the
tables against the release archive:

```bash
python scripts/verify_release.py \
    --archive <the release asset> \
    --run docs/published-run \
    --expect-sha256 <the digest quoted in the release notes>
```

The verifier exits zero on `EXACT` or `WITHIN #sourced.tolerance`, and non-zero on any
difference in a decision, including the verdict. To regenerate this document:

```bash
python scripts/build_paper.py
```

If the verifier reports anything other than those two outcomes, that is the interesting result.

#heading(numbering: none)[References]

#set enum(numbering: n => "[" + str(n) + "]")
#set par(hanging-indent: 1.4em)

+ Michaud, R. O. (1989). The Markowitz optimization enigma: is "optimized" optimal?
  _Financial Analysts Journal_, 45(1), 31--42.

+ DeMiguel, V., Garlappi, L., and Uppal, R. (2009). Optimal versus naive diversification: how
  inefficient is the 1/N portfolio strategy? _Review of Financial Studies_, 22(5),
  1915--1953.

+ Ledoit, O., and Wolf, M. (2004). Honey, I shrunk the sample covariance matrix.
  _Journal of Portfolio Management_, 30(4), 110--119.

+ Black, F., and Litterman, R. (1992). Global portfolio optimization. _Financial Analysts
  Journal_, 48(5), 28--43.

+ Bailey, D. H., and López de Prado, M. (2012). The Sharpe ratio efficient frontier.
  _Journal of Risk_, 15(2), 3--44.

+ Bailey, D. H., and López de Prado, M. (2014). The deflated Sharpe ratio: correcting for
  selection bias, backtest overfitting, and non-normality. _Journal of Portfolio Management_,
  40(5), 94--107.

+ Politis, D. N., and Romano, J. P. (1994). The stationary bootstrap. _Journal of the American
  Statistical Association_, 89(428), 1303--1313.

+ Marchenko, V. A., and Pastur, L. A. (1967). Distribution of eigenvalues for some sets of
  random matrices. _Mathematics of the USSR-Sbornik_, 1(4), 457--483.

+ Arnott, R., Harvey, C. R., and Markowitz, H. (2019). A backtesting protocol in the era of
  machine learning. _Journal of Financial Data Science_, 1(1), 64--74.
