#import "generated/paired.typ": paired
#import "generated/country.typ": country
#import "generated/numbers.typ": psr-bar, headline-bps, n-assets, n-months, n-folds, n-solves

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
#let footer = context [
  #place(bottom + left, text(size: 8pt, fill: muted)[github.com/kira-ml/robustfolio · exploratory, non-confirmatory · not investment advice])
  #place(bottom + right, text(size: 8pt, fill: muted)[#counter(page).display("1") / 8])
]
// The country sample is a pre-specified external replication, not a confirmatory test:
// the protocol's freeze is not independently verified. The project as a whole remains
// exploratory because the correction came from the first sample.
#let footer-registered = context [
  #place(bottom + left, text(size: 8pt, fill: muted)[github.com/kira-ml/robustfolio · external replication · not confirmatory · not investment advice])
  #place(bottom + right, text(size: 8pt, fill: muted)[#counter(page).display("1") / 8])
]
#let card(body) = block(width: 100%, fill: white, stroke: 0.6pt + rule, inset: 12pt, radius: 5pt, body)
#let takeaway(body) = place(
  bottom + left,
  dy: -34pt,
  block(width: 100%, fill: accent, inset: 9pt, radius: 4pt)[
    #text(fill: white, size: 11.5pt, weight: "bold", body)
  ],
)

#set page(width: 540pt, height: 675pt, margin: 38pt, fill: paper)
#set document(
  title: "Robustfolio: testing seven ways to build a portfolio",
  author: "Ken Ira Lacson Talingting",
)
#set text(font: "Libertinus Serif", size: 14pt, fill: ink, lang: "en")
#set par(justify: false, leading: 0.65em, spacing: 0.9em)

#let m2 = paired.methods.M2
#let m1 = paired.methods.M1
#let n-params = n-assets * (n-assets + 1) / 2 + n-assets
#let c-m1 = country.rows.filter(r => r.id == "M1").first()
#let c-m2 = country.rows.filter(r => r.id == "M2").first()
#let c-d1 = country.decisions.filter(d => d.id == "M1").first()
#let c-d2 = country.decisions.filter(d => d.id == "M2").first()

// 1 -------------------------------------------------------------------------
#v(22pt)
#eyebrow[ROBUSTFOLIO · AN OPEN-SOURCE PORTFOLIO BENCHMARK]
#v(14pt)
#text(size: 24pt, weight: "bold")[My own test rejected my best method.]
#v(4pt)
#text(size: 24pt, weight: "bold", fill: red)[It couldn't see a win that size.]
#v(14pt)
#text(size: 12.5pt, fill: muted)[I built an open-source benchmark: seven ways to build a portfolio, #n-assets US ETFs, #n-months months, after trading costs, one rule fixed before the run. Then I re-read the result with the test the design was built for, and ran it on a market I had never seen.]
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
#v(14pt)
#card[
  #text(size: 11pt, weight: "bold")[What this is]
  #v(3pt)
  #text(size: 12pt)[A benchmark for portfolio methods: seven constructions, one decision rule, and a test suite that checks the evaluation itself. Not a trading strategy, and not investment advice.]
]
#takeaway[The edge didn't survive a new market. The lesson did.]
#footer

#pagebreak()

// 2 -------------------------------------------------------------------------
#eyebrow[THE PROBLEM]
#v(10pt)
#text(size: 23pt, weight: "bold")[Portfolio construction is an estimation problem.]
#v(10pt)
#text(size: 13pt)[The standard method estimates average returns and correlations from history, then picks the portfolio with the best trade-off between return and risk. The estimates are noisy: mean–variance needs #n-params parameters, and the estimation window gives it 60 months of data.]
#v(10pt)
#table(
  columns: (1fr, 1fr),
  align: (left, left),
  stroke: none,
  inset: 0pt,
  [#text(size: 34pt, weight: "bold")[#n-params] #text(size: 11pt, fill: muted)[parameters]], [#text(size: 34pt, weight: "bold")[60] #text(size: 11pt, fill: muted)[months]],
)
#v(10pt)
#text(size: 13pt)[Regularization — shrinking noisy estimates — is the standard response. Whether it helps is an empirical question, not a mathematical one.]
#v(8pt)
#text(size: 13pt)[The question: do the “robust” versions — a shrinkage covariance, a Black–Litterman mean — beat a plain baseline out of sample, after costs, once you account for having tried more than one method?]
#takeaway[A portfolio is a set of assumptions. The market does not have to share them.]
#footer

#pagebreak()

// 3 -------------------------------------------------------------------------
#eyebrow[WHAT I BUILT]
#v(10pt)
#text(size: 23pt, weight: "bold")[A benchmark, not a backtest.]
#v(8pt)
#text(size: 12.5pt)[A backtest is a model of a market. A benchmark tests whether the model's edge survives data it has not seen — and whether the test could see the edge at all.]
#v(10pt)
#table(
  columns: (1.15fr, 2.55fr),
  align: (left, left),
  inset: 5pt,
  stroke: none,
  [*The engine*], [A walk-forward test: re-estimate each month on the previous 60 months, then test the next. #n-months out-of-sample months in #n-folds folds.],
  [*The universe*], [#n-assets US ETFs across equity, bonds, commodities and real estate; eligibility rules applied at each date.],
  [*The methods*], [Five standard baselines plus two variants that change one assumption in the standard mean-variance model.],
  [*The apparatus*], [A decision rule fixed before the run, a leakage test suite, a numerical check, and a reproduction check.],
)
#v(10pt)
#table(
  columns: (1fr, 1fr),
  align: (left, left),
  stroke: none,
  inset: 0pt,
  [#text(size: 30pt, weight: "bold")[#n-solves] #text(size: 10.5pt, fill: muted)[optimizer solves]], [#text(size: 30pt, weight: "bold")[0] #text(size: 10.5pt, fill: muted)[numerical rejections]],
)
#v(6pt)
#text(size: 10.5pt, fill: muted)[Not a live system, a forecast, or a claim of alpha.]
#takeaway[Then I fixed the rule that would decide it.]
#footer

#pagebreak()

// 4 -------------------------------------------------------------------------
#eyebrow[THE RESULT]
#v(12pt)
#text(size: 23pt, weight: "bold")[First on the metric. Failed on the decision.]
#v(8pt)
#text(size: 44pt, weight: "bold")[#fmt(m2.candidate-sr, 4)]
#v(2pt)
#text(size: 12pt, fill: muted)[net excess Sharpe at #headline-bps bps one-way costs — the highest of the seven]
#v(12pt)
#text(size: 12.5pt)[The rule, fixed before the run: beat the best baseline by #fmt(paired.bar, 2), clear the significance test, and pass five robustness checks.]
#v(8pt)
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
#v(8pt)
#table(
  columns: (1.1fr, 2.4fr, auto),
  align: (left, left, right),
  inset: 4pt,
  stroke: none,
  [the gap], rect(width: (m2.delta / 0.24) * 100%, height: 9pt, fill: green), [#fmt(m2.delta, 3)],
  [the bar], rect(width: (paired.bar / 0.24) * 100%, height: 9pt, fill: ink), [#fmt(paired.bar, 2)],
)
#v(10pt)
#text(size: 12.5pt, fill: red, weight: "bold")[A ranking and a verdict are different objects.]
#takeaway[The number that failed said more about the test than the method.]
#footer

#pagebreak()

// 5 -------------------------------------------------------------------------
#eyebrow[THE FLAW]
#v(10pt)
#text(size: 23pt, weight: "bold")[The bar was #fmt(paired.bar, 2). The test needed #fmt(m2.psr-mde, 2).]
#v(10pt)
#text(size: 13pt)[A test has a detection threshold: the smallest true effect it can reliably notice. This one needed about #fmt(m2.psr-mde, 2) for an 80% chance; the bar was #fmt(paired.bar, 2). A real #fmt(paired.bar, 2) improvement would usually have been missed.]
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
#text(size: 12.5pt)[*The candidate scored #fmt(m2.psr, 3) against a #fmt(psr-bar, 2) bar.* A failing score is not evidence of absence: at the bar, the test would usually have failed.]
#v(10pt)
#card[
  #text(size: 11pt, weight: "bold")[What went wrong]
  #v(3pt)
  #text(size: 12pt)[The test compared the candidate's Sharpe with the baseline's observed Sharpe. The design was built for a paired comparison.]
]
#takeaway[A test can be rigorous and still answer the wrong question.]
#footer

#pagebreak()

// 6 -------------------------------------------------------------------------
#eyebrow[THE CORRECTION]
#v(10pt)
#text(size: 23pt, weight: "bold")[The same data, the right test.]
#v(6pt)
#text(size: 44pt, weight: "bold", fill: accent)[#fmt(m2.p-positive, 3)]
#v(2pt)
#text(size: 12pt, fill: muted)[probability M2 beats B3 on a paired resampling test]
#v(10pt)
#table(
  columns: (1.2fr, auto),
  align: (left, right),
  inset: 4pt,
  stroke: none,
  [*Sharpe gap*], [#signed(m2.delta, 3)],
  [*90% range*], [#fmt(m2.ci-low, 3) to #fmt(m2.ci-high, 3)],
  [*p-value*], [#fmt(m2.p-one-sided, 3)],
)
#v(8pt)
#text(size: 12pt)[The two strategies hold almost the same portfolio (ρ = #fmt(m2.rho, 3)), so a month-by-month comparison is far more sensitive than comparing each to zero.]
#v(8pt)
#text(size: 13pt, fill: red, weight: "bold")[NOT MATERIAL — #fmt(m2.ci-high, 3) < #fmt(paired.bar, 2).]
#v(3pt)
#text(size: 11.5pt)[The 90% upper bound is below the advantage the study was designed to detect.]
#v(6pt)
#text(size: 10.5pt, fill: muted)[A post-hoc cap sweep did not rescue shrinkage; the gap remains far below the #fmt(paired.bar, 2) bar and its interval includes zero.]
#takeaway[The result is a bound, not a shrug.]
#footer

#pagebreak()

// 7 -------------------------------------------------------------------------
#eyebrow[THE NEW SAMPLE]
#v(10pt)
#text(size: 23pt, weight: "bold")[A new market. A different winner.]
#v(4pt)
#text(size: 12pt, fill: muted)[#country.n-assets country ETFs · 2005–2026 · #country.n-months months · #country.n-folds folds. The best baseline changed from B3 to B1.]
#v(10pt)
#table(
  columns: (auto, 1fr),
  align: (left, right),
  inset: (x: 4pt, y: 5pt),
  stroke: none,
  [*Method*], [*Net Sharpe*],
  ..country.rows.map(r => (
    [#r.id], [#fmt(r.net, 4)]
  )).flatten(),
)
#v(6pt)
#text(size: 8.5pt, fill: muted)[B1 equal weight · B2 risk parity · B3 sample MVO · B4 minimum variance · B5 turnover-penalised · M1 shrinkage · M2 Black–Litterman.]
#v(8pt)
#text(size: 12pt)[*M2 vs B1:* #signed(c-d2.delta, 3) [#fmt(c-d2.low, 3), #fmt(c-d2.high, 3)]. *M1 vs B1:* #signed(c-d1.delta, 3) [#fmt(c-d1.low, 3), #fmt(c-d1.high, 3)]. Both upper bounds are below #fmt(paired.bar, 2); 0 of 5 cost levels; about #fmt(c-d2.turnover-ratio, 1)× the turnover.]
#v(8pt)
#text(size: 12.5pt, weight: "bold")[The benchmark lesson replicated. The treatment advantage did not.]
#takeaway[The edge depended on the market. The lesson did not.]
#footer-registered

#pagebreak()

// 8 -------------------------------------------------------------------------
#eyebrow[WHAT THIS SHOWS]
#v(14pt)
#text(size: 24pt, weight: "bold")[The benchmark is the binding constraint.]
#v(10pt)
#text(size: 12.5pt)[*First sample:* the top number failed the rule — #signed(m2.delta, 3) against #fmt(paired.bar, 2).]
#v(6pt)
#text(size: 12.5pt)[*Second sample:* equal weight beat both treatments.]
#v(6pt)
#text(size: 12.5pt)[*The correction:* the same data, read with the test the design was built for.]
#v(6pt)
#text(size: 12.5pt)[*The limit:* every number here belongs to its sample, not to markets in general.]
#v(6pt)
#text(size: 12.5pt)[*The apparatus:* a pre-registered rule, a power audit, and a failed replication on the record.]
#v(12pt)
#card[
  #text(size: 11pt, weight: "bold")[What I would carry into the next study]
  #v(4pt)
  #text(size: 11.5pt)[— Fix the decision rule before the data.]
  #v(3pt)
  #text(size: 11.5pt)[— Audit the test's power, not only the strategy's return.]
  #v(3pt)
  #text(size: 11.5pt)[— Replicate on a sample that did not inform the design.]
]
#takeaway[Code, paper and the reproduction check: github.com/kira-ml/robustfolio]
#footer
