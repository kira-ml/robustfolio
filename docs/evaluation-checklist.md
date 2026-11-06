# Evaluation checklist for portfolio backtests

**Version:** 1.0
**Status:** Active — communication artifact, not a contract.
**Purpose:** Eight questions to ask before trusting a backtest. Each is paired with
the failure it catches and with how this project answers it.

A backtest is an experiment in time. These are the questions I would ask of my own
work; they are also the questions that found this project's central defect.

## 1. Was the decision rule fixed before the run?

**Why.** Otherwise the threshold can move to the result.
**Catches.** HARKing, post-hoc threshold selection, "we meant 0.15 all along".
**Here.** Protocol v2.4 was frozen before the run. The rule is a conjunction of
eight gates, and the verdict is computed by code, not chosen by hand.

## 2. Is the comparator chosen mechanically?

**Why.** The benchmark decides the verdict more than the method does.
**Catches.** Choosing a weak baseline after seeing the results.
**Here.** "Best of five baselines by net Sharpe", selected by code: `B3` in the
first sample, `B1` in the country sample.

## 3. What effect could the test actually detect?

**Why.** A null from an underpowered test is not evidence of absence.
**Catches.** The level-versus-paired confusion; a significance gate that cannot
see the materiality bar.
**Here.** The registered PSR gate needed an observed gap of 0.478, a true effect
of 0.72 for 80% power, and had about 24% power at 0.20.

## 4. Is the edge larger than the costs and turnover it requires?

**Why.** A gross edge can disappear net.
**Catches.** Ignoring commissions, spreads, turnover, capacity.
**Here.** Costs are 10 bps one-way and reported at five levels; the country
treatments traded about three times the baseline.

## 5. Is the evaluation time-ordered and leakage-free?

**Why.** Future information inflates every metric.
**Catches.** Lookahead, survivorship, preprocessing leakage.
**Here.** Weights at month *t* use only months before *t*; eligibility is
point-in-time; a leakage suite runs. The survivorship test is vacuous in-sample
and is recorded as a skip, not a pass.

## 6. Can a stranger reproduce the table?

**Why.** An unreproducible number is a claim, not evidence.
**Catches.** Hidden state, version drift, silent data revisions.
**Here.** A frozen snapshot with SHA-256; decisions compared exactly, measurements
within 1e-9, and the observed difference printed on every run.

## 7. Did it survive a sample that did not inform the design?

**Why.** In-sample selection is the default explanation for a good result.
**Catches.** Overfitting to one universe, period, or cost model.
**Here.** A pre-registered country-ETF sample. The treatment edge did not
replicate, and that is reported as the result.

## 8. What is the strongest sentence the evidence supports, and what does it not?

**Why.** Scope is part of the claim.
**Catches.** "No effect", "works live", "beats the market".
**Here.** "`M2` is not shown to be materially better than the best baseline, and a
0.20 advantage is excluded." Not "`M2` has no edge."

---

If a backtest cannot answer question 3 or question 6, it is not ready to be
believed, regardless of its Sharpe.
