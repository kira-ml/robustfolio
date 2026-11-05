#import "generated/paired.typ": paired
#import "generated/cap_sweep.typ": cap-sweep
#import "generated/country.typ": country
#import "generated/numbers.typ": sourced, verdicts, psr-bar, headline-bps, n-assets, n-months, n-folds, n-solves

#let accent = rgb("#1f5c99")
#let red = rgb("#9c3527")
#let amber = rgb("#b07a1e")
#let green = rgb("#2f7d4f")
#let muted = rgb("#6b6b6b")
#let ink = rgb("#1a1a1a")
#let paper = rgb("#f7f5f0")
#let rule = rgb("#d8d5cd")

#let fmt(x, digits) = {
  let s = str(calc.round(x, digits: digits))
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

#let pct(x, digits) = fmt(x * 100, digits) + "%"
#let signed(x, digits) = if x >= 0 { "+" + fmt(x, digits) } else { fmt(x, digits) }

#let eyebrow(x) = text(size: 9pt, fill: muted, tracking: 1.2pt)[#x]
#let footer = place(bottom + left, text(size: 8pt, fill: muted)[github.com/kira-ml/robustfolio · exploratory, non-confirmatory · not investment advice])
// The country sample was pre-registered, so it is confirmatory for that sample; the
// project as a whole remains exploratory because the correction came from the first one.
#let footer-registered = place(bottom + left, text(size: 8pt, fill: muted)[github.com/kira-ml/robustfolio · pre-registered sample · confirmatory for that sample · not investment advice])
#let card(body) = block(width: 100%, fill: white, stroke: 0.6pt + rule, inset: 12pt, radius: 5pt, body)
#let takeaway(body) = place(
  bottom + left,
  dy: -34pt,
  block(width: 100%, fill: accent, inset: 9pt, radius: 4pt)[
    #text(fill: white, size: 11.5pt, weight: "bold", body)
  ],
)

#set page(width: 540pt, height: 675pt, margin: 38pt, fill: paper)
#set text(font: "Libertinus Serif", size: 14pt, fill: ink, lang: "en")
#set par(justify: false, leading: 0.65em, spacing: 0.9em)

#let m2 = paired.methods.M2
#let m1 = paired.methods.M1
#let cs-m1 = cap-sweep.m1
#let cs-m2 = cap-sweep.m2
#let c-b1 = country.rows.filter(r => r.id == "B1").first()
#let c-b3 = country.rows.filter(r => r.id == "B3").first()
#let c-m1 = country.rows.filter(r => r.id == "M1").first()
#let c-m2 = country.rows.filter(r => r.id == "M2").first()
#let c-d1 = country.decisions.filter(d => d.id == "M1").first()
#let c-d2 = country.decisions.filter(d => d.id == "M2").first()

// 1 -------------------------------------------------------------------------
#v(23pt)
#eyebrow[ROBUSTFOLIO · AN OPEN-SOURCE PORTFOLIO BENCHMARK]
#v(14pt)
#text(size: 24pt, weight: "bold")[My own test rejected my best method.]
#v(4pt)
#text(size: 24pt, weight: "bold", fill: red)[It couldn't see a win that size.]
#v(14pt)
#text(size: 12pt, fill: muted)[I built an open-source benchmark: seven ways to build a portfolio, #n-assets US ETFs, #n-months months, after trading costs, one rule fixed before the run. Then I re-read the result with the test the design was built for, and ran it on a market I had never seen.]
#v(14pt)
#table(
  columns: (1.25fr, 2.35fr, auto),
  align: (left, left, right),
  inset: (x: 4pt, y: 8pt),
  stroke: none,
  [the bar], rect(width: (paired.bar / 0.8) * 100%, height: 20pt, fill: ink), [#fmt(paired.bar, 2)],
  [what the test needed], rect(width: (m2.psr-mde / 0.8) * 100%, height: 20pt, fill: red), [#fmt(m2.psr-mde, 2)],
)
#v(5pt)
#text(size: 9.5pt, fill: muted)[The test's 80% detection threshold, in net excess Sharpe: return above cash per unit of risk, after trading costs. An improvement at the bar would usually be missed.]
#v(16pt)
#card[
  #text(size: 11pt, weight: "bold")[What this is]
  #v(3pt)
  #text(size: 11.5pt)[A benchmark for portfolio methods: seven constructions, one decision rule, and a test suite that checks the evaluation itself. Not a trading strategy, and not investment advice.]
  #v(7pt)
  #text(size: 11pt, weight: "bold")[Why it matters]
  #v(3pt)
  #text(size: 11.5pt)[A model can be built correctly and still be judged by a test that cannot see its effect. That is the failure this project exists to catch — and the first one it caught was mine.]
]
#takeaway[The edge didn't survive a new market. The lesson did.]
#footer

#pagebreak()

// 2 -------------------------------------------------------------------------
#eyebrow[THE PROBLEM]
#v(10pt)
#text(size: 23pt, weight: "bold")[Portfolio construction is an estimation problem.]
#v(10pt)
#text(size: 12.5pt)[The standard method estimates average returns and correlations from history, then picks the portfolio with the best trade-off between return and risk. The estimates are noisy. The optimizer can load on assets that looked good by chance. With #n-assets assets and 60 months of history, there are more parameters than independent observations; regularization — shrinking noisy estimates — is the standard response.]
#v(8pt)
#text(size: 12.5pt)[The project asks a narrow question: do “robust” methods — a shrinkage covariance (which pulls noisy correlations toward a simpler estimate), a Black–Litterman mean (which blends the historical average with a prior) — beat a plain baseline out of sample, after costs, once you account for having tried more than one method?]
#v(12pt)
#card[
  #text(size: 11pt, weight: "bold")[Why it matters]
  #v(3pt)
  #text(size: 11.5pt)[A better estimator is only useful if it survives the noise, the costs, and the decision. That is what the benchmark tests.]
]
#takeaway[This is a question about evidence, not a pitch for a strategy.]
#footer

#pagebreak()

// 3 -------------------------------------------------------------------------
#eyebrow[WHAT I BUILT]
#v(10pt)
#text(size: 23pt, weight: "bold")[A benchmark, not a backtest.]
#v(8pt)
#text(size: 12pt)[A backtest is a model of a market. A benchmark tests whether the model's edge survives data it has not seen — and whether the test could see the edge at all.]
#v(10pt)
#set text(size: 11.5pt)
#table(
  columns: (1.15fr, 2.55fr),
  align: (left, left),
  inset: 5pt,
  stroke: none,
  [*The engine*], [A walk-forward test: re-estimate each month on the previous 60 months, then test the next month. #n-months out-of-sample months in #n-folds non-overlapping folds.],
  [*The universe*], [#n-assets US ETFs across equity, bonds, commodities and real estate; eligibility rules applied at each date.],
  [*The methods*], [Five standard baselines plus two variants that change one assumption in the standard mean-variance model.],
  [*The apparatus*], [A pre-registered decision rule, a leakage test suite, a numerical check that the optimizer solved the problem, and a reproduction check.],
)
#set text(size: 14pt)
#v(10pt)
#text(size: 11pt, fill: muted)[#n-solves optimizer solves; every one checked numerically. The code and the frozen data snapshot are public.]
#v(6pt)
#text(size: 11pt, fill: muted)[*What it is not:* a live system, a forecast, or a claim of alpha. One asset family, one period, flat costs.]
#takeaway[The benchmark is the deliverable, not just the headline number.]
#footer

#pagebreak()

// 4 -------------------------------------------------------------------------
#eyebrow[HOW I JUDGED IT]
#v(10pt)
#text(size: 23pt, weight: "bold")[One metric, one rule, fixed before the run.]
#v(12pt)
#text(size: 12.5pt)[*Net excess Sharpe:* return above cash, after #headline-bps bps (0.10%) one-way trading costs, divided by volatility. A summary of the path, not a forecast.]
#v(8pt)
#text(size: 12.5pt)[*The rule:* a method had to beat the best baseline by at least #fmt(paired.bar, 2) net Sharpe, clear the significance tests (the edge is unlikely to be luck), and pass five more checks on turnover, drawdown, cost levels, folds and concentration.]
#v(12pt)
#card[
  #text(size: 11pt, weight: "bold")[Why both tests]
  #v(3pt)
  #text(size: 11.5pt)[Significance alone admits tiny effects. Size alone admits noise. Requiring both, plus robustness, is what makes a null informative.]
]
#takeaway[The rule was written before the run. The run is exploratory because the planned blind test was compromised.]
#footer

#pagebreak()

// 5 -------------------------------------------------------------------------
#eyebrow[THE RESULT]
#v(12pt)
#text(size: 23pt, weight: "bold")[First on the metric. Failed on the decision.]
#v(8pt)
#text(size: 44pt, weight: "bold")[#fmt(m2.candidate-sr, 4)]
#v(2pt)
#text(size: 12pt, fill: muted)[net excess Sharpe — the highest of the seven]
#v(14pt)
#table(
  columns: (1fr, auto),
  align: (left, right),
  inset: 5pt,
  stroke: none,
  [*Gap over the best baseline*], [#signed(m2.delta, 3)],
  [*Materiality bar*], [#fmt(paired.bar, 2)],
  [*Original test (probability edge is real)*], [#fmt(m2.psr, 3) of #fmt(psr-bar, 2)],
  [*Checks failed*], [3 of 8],
)
#v(10pt)
#table(
  columns: (1.1fr, 2.4fr, auto),
  align: (left, left, right),
  inset: 4pt,
  stroke: none,
  [the gap], rect(width: (m2.delta / 0.24) * 100%, height: 9pt, fill: green), [#fmt(m2.delta, 3)],
  [the bar], rect(width: (paired.bar / 0.24) * 100%, height: 9pt, fill: ink), [#fmt(paired.bar, 2)],
)
#v(12pt)
#text(size: 12pt, fill: red, weight: "bold")[A ranking and a verdict are different objects.]
#takeaway[The number is a summary of one path, not a return you could spend.]
#footer

#pagebreak()

// 6 -------------------------------------------------------------------------
#eyebrow[THE FLAW]
#v(10pt)
#text(size: 23pt, weight: "bold")[The bar was #fmt(paired.bar, 2). The test needed #fmt(m2.psr-mde, 2).]
#v(10pt)
#text(size: 12.5pt)[A test has a detection threshold: the smallest true effect it can reliably notice. This one needed about #fmt(m2.psr-mde, 2) to have an 80% chance of noticing it. The bar was #fmt(paired.bar, 2). A real #fmt(paired.bar, 2) improvement would have been missed most of the time.]
#v(12pt)
#table(
  columns: (1.1fr, 2.4fr, auto),
  align: (left, left, right),
  inset: 4pt,
  stroke: none,
  [the bar], rect(width: (paired.bar / 0.8) * 100%, height: 9pt, fill: ink), [#fmt(paired.bar, 2)],
  [the test], rect(width: (m2.psr-mde / 0.8) * 100%, height: 9pt, fill: red), [#fmt(m2.psr-mde, 2)],
)
#v(10pt)
#card[
  #text(size: 11pt, weight: "bold")[What went wrong]
  #v(3pt)
  #text(size: 11.5pt)[The original test compared the candidate's Sharpe with the baseline's observed Sharpe. The design was built for a paired comparison. The test was measuring a different question.]
]
#takeaway[A test can be rigorous and still answer the wrong question.]
#footer

#pagebreak()

// 7 -------------------------------------------------------------------------
#eyebrow[THE CORRECTION]
#v(10pt)
#text(size: 23pt, weight: "bold")[The same data, the right test.]
#v(8pt)
#text(size: 44pt, weight: "bold", fill: accent)[#fmt(m2.p-positive, 3)]
#v(2pt)
#text(size: 12pt, fill: muted)[probability M2 beats B3 on a paired resampling test]
#v(14pt)
#table(
  columns: (1.2fr, auto),
  align: (left, right),
  inset: 5pt,
  stroke: none,
  [*Sharpe gap*], [#signed(m2.delta, 3)],
  [*90% range*], [#fmt(m2.ci-low, 3) to #fmt(m2.ci-high, 3)],
  [*p-value*], [#fmt(m2.p-one-sided, 3)],
  [*Original test*], [#fmt(m2.psr, 3)],
)
#v(12pt)
#text(size: 12pt)[The two strategies hold almost the same portfolio (ρ = #fmt(m2.rho, 3)), so comparing them month by month is far more sensitive than comparing each to zero.]
#takeaway[Pairing is what turns a noisy comparison into a usable one.]
#footer

#pagebreak()

// 8 -------------------------------------------------------------------------
#eyebrow[THE READING]
#v(10pt)
#text(size: 23pt, weight: "bold")[The data exclude a #fmt(paired.bar, 2) advantage.]
#v(6pt)
#text(size: 44pt, weight: "bold", fill: red)[#fmt(m2.ci-high, 3) < #fmt(paired.bar, 2)]
#v(2pt)
#text(size: 12pt, fill: muted)[the 90% upper bound is below the materiality bar]
#v(14pt)
#card[
  #text(size: 12pt, weight: "bold", fill: red)[NOT MATERIAL]
  #v(3pt)
  #text(size: 12pt)[M2 is plausibly a little better. It is not materially better — not enough to justify the extra complexity. The data exclude the #fmt(paired.bar, 2) improvement the study was designed to detect.]
]
#v(10pt)
#text(size: 11.5pt, fill: muted)[This is a bounded result: material, not material, or undecided. Here it is not material.]
#takeaway[The result is a bound, not a shrug.]
#footer

#pagebreak()

// 9 -------------------------------------------------------------------------
#eyebrow[WHY IT FAILED]
#v(10pt)
#text(size: 22pt, weight: "bold")[The cap did not rescue shrinkage.]
#v(6pt)
#text(size: 12pt, fill: muted)[I thought the 30% position cap was doing the job of keeping the portfolio simple, which would explain why the shrinkage method added nothing. I tested it.]
#v(10pt)
#table(
  columns: (auto, 1.15fr, 1.15fr),
  align: (right, right, right),
  inset: 4pt,
  stroke: none,
  [*Position limit*], [*Shrinkage*], [*Black–Litterman*],
  [#fmt(cs-m1.at(0).cap, 2)], [#signed(cs-m1.at(0).delta, 3) (#fmt(cs-m1.at(0).low, 3), #fmt(cs-m1.at(0).high, 3))], [#signed(cs-m2.at(0).delta, 3) (#fmt(cs-m2.at(0).low, 3), #fmt(cs-m2.at(0).high, 3))],
  [#fmt(cs-m1.at(1).cap, 2)], [#signed(cs-m1.at(1).delta, 3) (#fmt(cs-m1.at(1).low, 3), #fmt(cs-m1.at(1).high, 3))], [#signed(cs-m2.at(1).delta, 3) (#fmt(cs-m2.at(1).low, 3), #fmt(cs-m2.at(1).high, 3))],
  [#fmt(cs-m1.at(2).cap, 2)], [#signed(cs-m1.at(2).delta, 3) (#fmt(cs-m1.at(2).low, 3), #fmt(cs-m1.at(2).high, 3))], [#signed(cs-m2.at(2).delta, 3) (#fmt(cs-m2.at(2).low, 3), #fmt(cs-m2.at(2).high, 3))],
  [#fmt(cs-m1.at(3).cap, 2)], [#signed(cs-m1.at(3).delta, 3) (#fmt(cs-m1.at(3).low, 3), #fmt(cs-m1.at(3).high, 3))], [#signed(cs-m2.at(3).delta, 3) (#fmt(cs-m2.at(3).low, 3), #fmt(cs-m2.at(3).high, 3))],
)
#v(8pt)
#text(size: 11.5pt)[*Shrinkage: not supported.* The gap stays at or below zero; every interval includes zero.]
#v(4pt)
#text(size: 11.5pt)[*Black–Litterman: depends on the cap.* The gap grows as the cap loosens, but remains below #fmt(paired.bar, 2). The looser cap also means larger positions: the largest holding rises from #fmt(cs-m2.at(1).maxw, 2) to #fmt(cs-m2.at(3).maxw, 2).]
#v(6pt)
#text(size: 10.5pt, fill: muted)[Post-hoc, and reported as post-hoc: this tests an explanation for the null, not a new hypothesis.]
#takeaway[The mechanism test did not support the shrinkage explanation. It did show the cap binding the mean treatment.]
#footer

#pagebreak()

// 10 ------------------------------------------------------------------------
#eyebrow[THE NEW SAMPLE]
#v(10pt)
#text(size: 22pt, weight: "bold")[A new market. A different winner.]
#v(4pt)
#text(size: 11.5pt, fill: muted)[#country.n-assets country ETFs · 2005–2026 · #country.n-months months · #country.n-folds folds. The best baseline was equal weight (B1), not sample MVO (B3).]
#v(10pt)
#table(
  columns: (auto, 1.2fr, 1fr),
  align: (right, right, right),
  inset: 3.5pt,
  stroke: none,
  [*Method*], [*Net Sharpe*], [*Turnover*],
  ..country.rows.map(r => (
    [#r.id], [#fmt(r.net, 4)], [#fmt(r.turnover, 2)]
  )).flatten(),
)
#v(6pt)
#text(size: 8.5pt, fill: muted)[B1 equal weight · B2 risk parity · B3 sample MVO · B4 minimum variance · B5 turnover-penalised · M1 shrinkage · M2 Black–Litterman.]
#v(8pt)
#text(size: 11pt)[*M2 vs B1:* #signed(c-d2.delta, 3) [#fmt(c-d2.low, 3), #fmt(c-d2.high, 3)]. *M1 vs B1:* #signed(c-d1.delta, 3) [#fmt(c-d1.low, 3), #fmt(c-d1.high, 3)]. Both upper bounds are below #fmt(paired.bar, 2); both won 0 of 5 cost levels; both traded about #fmt(c-d2.turnover-ratio, 1)× the baseline.]
#v(8pt)
#card[
  #text(size: 11.5pt, weight: "bold")[What replicated — and what did not]
  #v(3pt)
  #text(size: 11.5pt)[The benchmark lesson replicated: the best baseline changed from B3 to B1. The treatment advantage did not.]
]
#takeaway[The edge depended on the market. The lesson did not.]
#footer-registered

#pagebreak()

// 11 ------------------------------------------------------------------------
#eyebrow[WHAT THIS SHOWS]
#v(14pt)
#text(size: 24pt, weight: "bold")[The benchmark is the binding constraint.]
#v(8pt)
#text(size: 12pt)[What you compare against decides the verdict. The metric is a summary; the benchmark is the decision.]
#v(10pt)
#text(size: 12pt)[*First sample:* the top number failed the rule — #signed(m2.delta, 3) against #fmt(paired.bar, 2).]
#v(5pt)
#text(size: 12pt)[*Second sample:* equal weight beat both treatments.]
#v(5pt)
#text(size: 12pt)[*The correction:* the same data, read with the test the design was built for.]
#v(5pt)
#text(size: 12pt)[*The limit:* every number here belongs to its sample, not to markets in general.]
#v(12pt)
#block(width: 100%)[
  #card[
    #text(size: 11pt, weight: "bold")[What I would carry into the next study]
    #v(4pt)
    #text(size: 11.5pt)[— Fix the decision rule before the data.]
    #v(3pt)
    #text(size: 11.5pt)[— Audit the test's power, not only the strategy's return.]
    #v(3pt)
    #text(size: 11.5pt)[— Replicate on a sample that did not inform the design.]
  ]
]
#takeaway[Code, paper and the reproduction check: github.com/kira-ml/robustfolio]
#footer
