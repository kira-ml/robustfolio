# Reviewer's guide

**Version:** 1.0
**Status:** Active — communication artifact, not a contract.
**Purpose:** A thirty-minute path through the repository for someone who wants to
check the claims rather than read everything.

## The path

| Minutes | Read | Question it answers |
|---|---|---|
| 0–5 | [`../README.md`](../README.md) front, [`positioning.md`](positioning.md), paper abstract | What is claimed, and at what evidence level? |
| 5–10 | [`evaluation_protocol.md`](evaluation_protocol.md) §5–6, then [`published-run/decisions.csv`](published-run/decisions.csv) | What was fixed, and what did the gates return? |
| 10–15 | [`../src/robustfolio/backtest.py`](../src/robustfolio/backtest.py) `run_method` and `run_harness` | How is one rebalance built, without lookahead? |
| 15–20 | [`../src/robustfolio/report.py`](../src/robustfolio/report.py) `decision_table` | How do eight gates become one verdict? |
| 20–25 | [`../notes/paired_inference_2026-11-04.md`](../notes/paired_inference_2026-11-04.md), [`../notes/country_sample_result_2026-11-05.md`](../notes/country_sample_result_2026-11-05.md) | Why did the test fail, and did the result replicate? |
| 25–30 | `python scripts/demo_the_check.py`, then `verify_release.py` with a snapshot you independently hold | Does the check refuse a wrong verdict? With a supplied snapshot, does the table reproduce? |

## Claims and their falsifiers

| Claim | Evidence | What would falsify it |
|---|---|---|
| The rule was fixed before the run | Protocol v2.4, decision log, dated freeze | A threshold or comparator changed after the run |
| `M2` failed three of eight gates | `decisions.csv` | A gate value or verdict that does not match the arithmetic |
| The gate could not see a 0.20 effect | Power note: 0.478 observed, 0.72 true, 24% power | A recomputation showing 80% power at 0.20 |
| A 0.20 advantage is excluded | Paired interval [−0.011, +0.147] | An upper bound at or above 0.20 |
| The edge did not replicate | Country `decisions.csv`: `M2` below `B1` | `M2` above `B1` with an interval excluding zero |
| Decisions reproduce exactly **when a snapshot archive is supplied** | `verify_release.py` | Any decision-bearing quantity differing |
| The first sample is exploratory | Finding F26 | Evidence that the test ran blind |

## Three commands

```bash
python -m pytest -q                      # the full suite; no snapshot needed
python scripts/demo_the_check.py         # watch the verifier refuse a tampered verdict
python scripts/verify_release.py --archive <your snapshot archive> --run docs/published-run
```

The snapshot is **not distributed**. The third command only runs end to end if
you independently hold an archive. Without one, use the first two commands and
inspect the committed tables in `docs/published-run/`.

## What to be suspicious of

- The first sample is **exploratory and non-confirmatory**; the hypotheses are
  untested, not falsified.
- Survivorship is argued by construction; the in-sample test is vacuous.
- One asset family, one period, flat costs, no market impact.
- The snapshot is a 2026 vendor's revised history, not what a trader saw.
- The snapshot is **not distributed**, so exact end-to-end reproduction requires
  your own licensed copy; the committed tables are the public record.
- The country sample is current-listed; its survivorship remains.

A reviewer who reads only the result and not these five lines has read a different
paper.
