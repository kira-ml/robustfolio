# Positioning

**Version:** 1.0
**Status:** Active
**Last Updated:** 2026-11-06

This file is the one-page answer to "what is this project, and why should anyone care?"
It is a communication artifact, not a contract: it binds nothing and changes no protocol.

## One sentence

A pre-registered evaluation benchmark for portfolio construction, with a published power
audit and an out-of-sample replication.

## Thesis

In portfolio research, the binding constraint is usually the **evaluation**, not the method.
The comparator, the test's power, and the sample decide the verdict more than the strategy
does.

The project is the evidence for that thesis, not a search for a better portfolio.

## Audience

- **Researchers** who evaluate portfolio methods and need a design that can fail.
- **Data scientists** who build evaluation harnesses and want the statistical failure modes
  made explicit.
- **Allocators and practitioners** who read backtests and want to know what a number can
  and cannot support.

Not written for retail investors, and not investment advice.

## Three contributions

| # | Contribution | Evidence status |
|---|---|---|
| 1 | A **single-factor registered comparison**: seven constructions on 18 US ETFs over 168 months, where each treatment differs from the baseline in exactly one component. | Verified, exploratory |
| 2 | A **power audit of the registered gate**: it required an observed gap of 0.478 to certify a 0.20 bar, and had about 24% power at 0.20. | Verified |
| 3 | A **pre-registered out-of-sample replication** on 18 country ETFs: the best baseline changed from sample MVO to equal weight, and the treatment edge did not replicate. | Confirmatory for that sample |

Supporting apparatus: a leakage suite, a KKT certificate on every solve, and a reproduction
check that compares decisions exactly and measurements within a documented bound.

## What it does not claim

- Not a live trading system, not a forecast, not a claim of alpha.
- Not a confirmatory test of the first sample: the registered test was executed without
  blindness (finding F26), so the hypotheses are untested, not falsified.
- Not universal: one asset family, one period, flat costs, no market impact.
- Not "no effect": the supported sentence is "not materially better than the best baseline".

## Why it matters

A backtest can be well built and still be judged by a test that cannot see the effect it was
designed to detect. This project makes that failure visible, quantifies it, and then runs the
same test on a sample that did not inform the design. The reusable output is the evaluation
discipline: pre-register the rule, audit its power, choose the comparator mechanically, and
replicate on fresh territory.

## Proof points

- `M2` 0.8538 vs `B3` 0.7896: a gap of +0.064 against a 0.20 bar.
- PSR against `B3`: 0.587 against 0.95. DSR against zero: p = 0.0017. Same series, different
  reference point.
- Paired: +0.064, 90% interval [−0.011, +0.147]; a 0.20 advantage is excluded.
- Country sample: `B1` 0.3527, `M2` 0.3193, `M1` 0.2710.
- Reproduction: 1,176 solves, zero numerical rejections; decisions exact, measurements
  within 1e-9.

## How to verify

- Paper: `essays/robustfolio-working-paper.pdf`
- Brief: `essays/robustfolio-research-brief.pdf`
- Protocol: `docs/evaluation_protocol.md`
- Test correction: `notes/paired_inference_2026-11-04.md`
- Replication: `notes/confirmatory_country_etfs_2026-11-05.md`
- Reproduction: `scripts/verify_release.py` and `docs/published-run/README.md`
