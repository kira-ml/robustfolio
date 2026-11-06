#set document(
  title: "What a Backtest Can Prove",
  author: "Ken Ira Lacson Talingting",
)

#set page(
  paper: "a4",
  margin: (x: 20mm, y: 18mm),
  footer: context align(center)[
    #text(size: 8pt, fill: luma(120))[#counter(page).display("1") / 2]
  ],
)

#set text(font: "New Computer Modern", size: 10.5pt, lang: "en")
#set par(justify: true, leading: 0.72em, spacing: 1.0em)

#let accent = rgb("#1f5c99")
#let muted = luma(105)
#let rule = line(length: 100%, stroke: 0.5pt + luma(180))
#let eyebrow(x) = text(size: 8.5pt, fill: muted, tracking: 1.4pt)[#x]

// ---------------------------------------------------------------------------
// Page 1
// ---------------------------------------------------------------------------

#eyebrow[ROBUSTFOLIO · RESEARCH BRIEF]
#v(10pt)
#text(size: 26pt, weight: "bold")[What a Backtest Can Prove]
#v(6pt)
#text(size: 12.5pt, fill: luma(70))[
  A pre-registered benchmark for portfolio construction, with a power audit
  and an out-of-sample replication.
]
#v(10pt)
#rule
#v(6pt)
#text(size: 9pt, fill: muted)[Ken Ira Lacson Talingting · November 2026]

#v(12pt)

#text(size: 11.5pt, weight: "bold", fill: accent)[The question]
#v(2pt)
#text(size: 10.5pt)[
  Does a "robust" portfolio method beat a plain one, out of sample, after trading
  costs, once you account for having tried more than one? The project fixes the
  decision rule before the run, and then asks a second question that most
  backtests never ask: *could the rule see the effect it was testing for?*
]

#v(10pt)

#text(size: 11.5pt, weight: "bold", fill: accent)[What was built]
#v(2pt)
#list(
  [Seven constructions on 18 US ETFs over 168 months (June 2012 to May 2026);
    five baselines, two treatments, 1,176 rebalances, 10 bps one-way costs.],
  [A decision rule fixed before the run: a 0.20 net Sharpe bar, a 0.95
    probabilistic Sharpe ratio against the best baseline, a 0.05 deflated-Sharpe
    p-value, and five robustness checks.],
  [An evaluation apparatus: a leakage suite, a KKT certificate on every solve,
    and a reproduction check that compares decisions exactly and measurements
    within a documented bound.],
)

#v(10pt)

#text(size: 11.5pt, weight: "bold", fill: accent)[Three findings]
#v(4pt)

#table(
  columns: (auto, 1fr),
  align: (left, left),
  stroke: none,
  column-gutter: 10pt,
  inset: (x: 0pt, y: 5pt),
  [#text(size: 22pt, weight: "bold", fill: accent)[1]], [
    *The comparator decides.* The same return series passes the deflated
    Sharpe test against _zero_ (p = 0.0017) and fails the probabilistic Sharpe
    test against the best baseline (0.587 against 0.95). With one registered
    comparison, the multiple-testing correction is inert. What binds is the
    benchmark.
  ],
  [#text(size: 22pt, weight: "bold", fill: accent)[2]], [
    *The gate could not see the bar.* The registered level test required an
    observed gap of 0.478 to certify a 0.20 effect; its 80%-power threshold was
    0.72, and its power at 0.20 was about 24%. On the paired test the estimate
    is +0.064 [−0.011, +0.147]: a 0.20 advantage is excluded, and the null
    survives the repair of the test.
  ],
  [#text(size: 22pt, weight: "bold", fill: accent)[3]], [
    *The edge did not replicate.* A pre-registered country-ETF sample (18 funds,
    252 months, 21 folds) changed the best baseline from sample MVO to equal
    weight. Equal weight returned 0.3527, `M2` 0.3193, `M1` 0.2710. The
    benchmark lesson replicated; the treatment edge did not.
  ],
)

#v(8pt)
#text(size: 9.5pt, fill: muted)[
  `M2` is not shown to be materially better than the best baseline, and a 0.20
  advantage is excluded. That is the supported sentence. "No effect" is not.
]

#pagebreak()

// ---------------------------------------------------------------------------
// Page 2
// ---------------------------------------------------------------------------

#text(size: 11.5pt, weight: "bold", fill: accent)[Method, in one paragraph]
#v(2pt)
#text(size: 10.5pt)[
  Each month, weights are estimated on the previous 60 months and held for one
  month; the 168 months form 14 non-overlapping 12-month folds. The rule is a
  conjunction: a 0.20 net Sharpe gap, a 0.95 PSR against the best baseline, a
  0.05 deflated-Sharpe p-value, and five robustness checks on turnover,
  drawdown, cost levels, folds, and concentration. Long-only, 30% cap, 10 bps
  one-way.
]

#v(10pt)

#text(size: 11.5pt, weight: "bold", fill: accent)[Evidence level]
#v(4pt)

#table(
  columns: (1.4fr, 1.0fr, 2.1fr),
  align: (left, left, left),
  stroke: none,
  column-gutter: 8pt,
  inset: (x: 0pt, y: 4pt),
  table.hline(stroke: 0.5pt),
  table.header([Claim], [Status], [Why]),
  table.hline(stroke: 0.3pt),
  [Single-factor comparison], [Exploratory], [First sample; the registered test ran without its required blindness],
  [Power audit], [Verified], [Arithmetic on the published return series],
  [Replication], [Confirmatory], [Registered before it ran; the new sample did not inform the design],
  [Universal, live, or alpha claim], [Not made], [One asset family, one period, flat costs, no impact],
  table.hline(stroke: 0.5pt),
)

#v(10pt)

#text(size: 11.5pt, weight: "bold", fill: accent)[What it does not claim]
#v(2pt)
#list(
  [Not a live trading system, a forecast, or a claim of alpha.],
  [Not a confirmatory test of the first sample: the hypotheses are untested,
    not falsified.],
  [Not "no effect": the data are consistent with a small improvement and exclude
    a material one.],
  [Not universal: one asset family, one period, current-listed country funds in
    the replication.],
)

#v(10pt)

#text(size: 11.5pt, weight: "bold", fill: accent)[Why it matters]
#v(2pt)
#text(size: 10.5pt)[
  A backtest can be rigorous and still answer the wrong question. The project
  makes that failure visible, quantifies it, and then runs the same test on a
  sample that did not inform the design. The reusable output is a discipline:
  pre-register the rule, audit its power, choose the comparator mechanically,
  and replicate on fresh territory.
]

#v(10pt)

#text(size: 11.5pt, weight: "bold", fill: accent)[Verify]
#v(2pt)
#table(
  columns: (1.3fr, 3fr),
  align: (left, left),
  stroke: none,
  inset: (x: 0pt, y: 3pt),
  [Repository], [#link("https://github.com/kira-ml/robustfolio")[github.com/kira-ml/robustfolio]],
  [Working paper], [#link("https://github.com/kira-ml/robustfolio/blob/main/essays/robustfolio-working-paper.pdf")[essays/robustfolio-working-paper.pdf]],
  [Protocol], [#link("https://github.com/kira-ml/robustfolio/blob/main/docs/evaluation_protocol.md")[docs/evaluation_protocol.md]],
  [Power correction], [#link("https://github.com/kira-ml/robustfolio/blob/main/notes/paired_inference_2026-11-04.md")[notes/paired_inference_2026-11-04.md]],
  [Replication], [#link("https://github.com/kira-ml/robustfolio/blob/main/notes/confirmatory_country_etfs_2026-11-05.md")[notes/confirmatory_country_etfs_2026-11-05.md]],
)

#v(8pt)
#text(size: 9.5pt, fill: muted)[
  Reproduce the published tables with `python scripts/verify_release.py --archive <asset> --run docs/published-run`.
  Decisions are compared exactly; measurements within 1e-9, with the observed difference printed.
]

#v(14pt)
#rule
#v(4pt)
#text(size: 8.5pt, fill: muted)[
  Personal research communication, not investment advice. The project is not a
  trading system, and no absolute return claim is made.
]
