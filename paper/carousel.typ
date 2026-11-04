#import "generated/paired.typ": paired
#import "generated/cap_sweep.typ": cap-sweep
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
#let card(body) = block(fill: white, stroke: 0.6pt + rule, inset: 12pt, radius: 5pt, body)
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

// 1 -------------------------------------------------------------------------
#v(20pt)
#eyebrow[ROBUSTFOLIO · AN OPEN-SOURCE PORTFOLIO BENCHMARK]
#v(12pt)
#text(size: 27pt, weight: "bold")[I set the bar at #fmt(paired.bar, 2).]
#v(2pt)
#text(size: 27pt, weight: "bold", fill: red)[My own test needed #fmt(m2.psr-mde, 2).]
#v(12pt)
#text(size: 12pt, fill: muted)[I built a benchmark that compares seven ways to build a portfolio across #n-assets US ETFs over #n-months months, after trading costs, under a rule fixed before the run. The best one still failed the rule.]
#v(14pt)
#card[
  #text(size: 11pt, weight: "bold")[What this is]
  #v(3pt)
  #text(size: 11.5pt)[An open-source research project on portfolio construction: how to spread money across assets when historical estimates are noisy. It is not a trading strategy or investment advice.]
  #v(5pt)
  #text(size: 11.5pt)[The short version: the portfolio was not clearly better, and the test was too weak to detect the improvement I said would matter.]
]
#v(16pt)
#table(
  columns: (1.25fr, 2.35fr, auto),
  align: (left, left, right),
  inset: 4pt,
  stroke: none,
  [the bar], rect(width: (paired.bar / 0.8) * 100%, height: 12pt, fill: ink), [#fmt(paired.bar, 2)],
  [the test needed], rect(width: (m2.psr-mde / 0.8) * 100%, height: 12pt, fill: red), [#fmt(m2.psr-mde, 2)],
)
#v(4pt)
#text(size: 9.5pt, fill: muted)[The test's 80% detection threshold, in net excess Sharpe. A real #fmt(paired.bar, 2) improvement would usually be missed.]
#takeaway[The result is a correction of the test, not a win for the portfolio.]
#footer

#pagebreak()

// 2 -------------------------------------------------------------------------
#eyebrow[THE PROBLEM]
#v(10pt)
#text(size: 23pt, weight: "bold")[Portfolio construction is an estimation problem.]
#v(10pt)
#text(size: 12.5pt)[The standard method estimates average returns and correlations from history, then picks the portfolio with the best trade-off between return and risk. The estimates are noisy. The optimizer can load on assets that looked good by chance.]
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
#text(size: 23pt, weight: "bold")[It finished first. It still failed.]
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
#takeaway[The original test was not wrong. It was answering a different question.]
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
#eyebrow[THE MECHANISM TEST]
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
#takeaway[The mechanism test did not support the shrinkage explanation. It did show the cap binding the mean treatment.]
#footer

#pagebreak()

// 10 ------------------------------------------------------------------------
#eyebrow[WHAT THIS SHOWS]
#v(14pt)
#text(size: 24pt, weight: "bold")[The benchmark itself is the result.]
#v(10pt)
#text(size: 12.5pt)[*The headline number was not enough.* The test, the benchmark and the decision rule decide what a number means.]
#v(6pt)
#text(size: 12.5pt)[*The correction is a better test on the same data,* not a new strategy.]
#v(6pt)
#text(size: 12.5pt)[*A real test needs a new sample,* registered before I look at it.]
#v(12pt)
#card[
  #text(size: 11.5pt, weight: "bold")[What I would check in my own work]
  #v(3pt)
  #text(size: 11.5pt)[Before trusting a metric, ask what decision it is supposed to support. A test can be rigorous and still answer the wrong question.]
]
#takeaway[Code, paper and the reproduction check: github.com/kira-ml/robustfolio]
#footer
