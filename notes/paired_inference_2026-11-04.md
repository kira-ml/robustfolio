# Paired inference — a correction to the reading, not to the verdict

**Version:** 1.0
**Status:** **Exploratory.** Same data, post-hoc reading. Not a confirmatory test, not a protocol amendment.
**Created:** 2026-11-04
**Owner:** Ken Ira Lacson Talingting
**Reproduce:** `python scripts/paired_inference.py --run results/<run>`
**Run:** `EXP-X-20261017-003` — 168 months, 18 US ETFs, 7 methods, 10 bps one-way
**Related:** [`evaluation_protocol.md`](../docs/evaluation_protocol.md) §6.1–§6.4; [`power_and_effective_bets_2026-10-17.md`](power_and_effective_bets_2026-10-17.md) §3(b); [`published-run/decisions.csv`](../docs/published-run/decisions.csv)

---

## 0. What this note is

The published run says both treatments **FAILURE** under §6.4. That verdict is not
changed here, and the frozen protocol is not edited. What changes is the
*interpretation* of why they fail.

The design diagnostic in `power_and_effective_bets_2026-10-17.md` §3(b) says the
**paired** difference test is the one that decides H2.4, and that it reaches 80%
power for a 0.20 net-Sharpe gap once ρ ≥ 0.98. The realised ρ is 0.9845 (M1) and
0.9856 (M2), inside that regime.

But the registered §6.1 gate is not that test. It is a **level** probabilistic
Sharpe ratio: the candidate's Sharpe against the best baseline's *observed*
Sharpe. It ignores the pairing, so it discards most of the comparison's power.
This note computes the paired test on the same return series and reports both.

The distinction matters because the two tests disagree about what the data show,
and one of them answers the question the project asked.

---

## 1. Result

Paired stationary bootstrap, 2,000 replications, mean block 6 months, seed
20261017. `delta SR` is the annualised net excess Sharpe difference;
`P(delta > 0)` is the bootstrap probability the candidate is better.

| Candidate | delta SR | 90% paired CI | P(delta > 0) | one-sided p | P(delta > 0.20) | equivalence | registered PSR |
|---|---:|---:|---:|---:|---:|---|---:|
| `M1` | -0.0036 | [-0.0964, +0.0800] | 0.487 | 0.512 | 0.000 | **NOT_MATERIAL** | 0.495 |
| `M2` | +0.0642 | [-0.0113, +0.1467] | 0.917 | 0.083 | 0.004 | **NOT_MATERIAL** | 0.587 |

Reading the rows:

- **`M2` is probably a little better, but not by enough to matter.** The point
  estimate is positive and the paired probability is 0.917, but the 90% interval
  includes zero, so it is not established at the 5% level. The correct sentence
  is not "no better"; it is "not shown to be 0.20 better, and the data are
  consistent with a small positive effect."
- **The 0.20 bar is excluded, not merely missed.** The 90% upper bound is 0.147,
  below 0.20. The three-way equivalence column therefore says
  `NOT_MATERIAL`: a materially large advantage is ruled out at the 5% one-sided
  level. This is stronger than a failure to reject.
- **`M1` is a genuine zero.** The interval is centred on zero, and
  `P(delta > 0.20) = 0.000`.

The paired interval is roughly **twelve times narrower** than the interval on
either level. That is the whole value of pairing two almost-identical portfolios.

---

## 2. The gate the project actually registered

The §6.1 gate requires `PSR > 0.95` against the baseline's observed Sharpe. For
these return series, the *observed* gap needed to cross that bar is:

| Candidate | gate requires (observed delta) | 80%-power MDE (true delta) | power at a true 0.20 |
|---|---:|---:|---:|
| `M1` | 0.474 | 0.717 | 0.19 |
| `M2` | 0.478 | 0.723 | 0.24 |

The 80% MDE is about **0.72**, not 0.13–0.20. A true 0.20 improvement would fail
the registered gate roughly three times out of four. That is the sense in which
the published null is not informative about the bar the project said it cared
about: the gate, not the data, is the binding constraint.

This is the same failure the project is built to catch — a claim broader than the
mechanism underneath it. The paper's sentence "a sample powered to detect an
effect at that bar" is true of the paired test and false of the registered gate.
This note is the correction.

---

## 3. Secondary checks

**Multiple testing.** `DSR_FAMILY_SIZE = 1` is the frozen convention, not an
adjustment: it reduces the DSR to a PSR against zero. Counting the family
honestly gives:

| Family size | `M1` DSR p | `M2` DSR p |
|---|---:|---:|
| 1 (registered) | 0.0032 | 0.0017 |
| 2 (two candidates) | 0.0112 | 0.0063 |
| 7 (all methods) | **0.0613** | 0.0389 |

`M2` survives the 7-method count; `M1` does not. The published sentence should
therefore read "with one registered comparison, deflation has almost nothing to
remove", not "after paying for the number of trials" without qualification.

**Fold fragility.** Dropping each 12-month fold in turn leaves `M2`'s paired
difference positive in **14 of 14** leave-one-out samples (worst +0.029); `M1`
is positive in 2 of 14. The frozen concentration gate (one fold contributing
51.3%) is a magnitude test, not a sign test; the sign of `M2`'s advantage does
not depend on the best fold. Both statements belong in the v2.

**Comparator margin.** `B3` beats `B5` by **0.0053**, not "not close". `M1` is
+0.0016 against `B5` and -0.0036 against `B3`; its sign depends on which
baseline is chosen. The verdict does not change, but the paper's "the choice is
not close" should be corrected.

---

## 4. What this does and does not change

**Does not change:** the frozen §6.4 verdict (`FAILURE` for both candidates),
the protocol, the published tables, or the confirmatory status. The run remains
exploratory and the confirmatory slot remains empty.

**Does change:** the reason. The candidates do not fail because the data are
silent. `M2` fails because its advantage, while plausibly positive, is too small
to clear the pre-registered materiality bar — and the data exclude that bar. The
registered gate also could not have detected a 0.20 effect most of the time, so
"failed the significance gate" is not the same as "no effect".

---

## 5. Limitations

- **Same data, already seen.** This is a post-hoc reading. It cannot be
  confirmatory, and it does not fill the empty confirmatory slot.
- **Bootstrap, not a new sample.** The paired interval assumes the monthly
  dependence is captured by a 6-month stationary block; a different block length
  or a wild bootstrap would move the third decimal.
- **The power figures are approximations.** The analytic MDE uses the candidate's
  own skew and kurtosis; the simulated power resamples the candidate's returns
  with a mean shift. They agree on the order of magnitude (0.19–0.24 at a true
  0.20), which is enough to establish the gate is far below 80% power.
- **The 0.20 bar remains a judgement.** Nothing here argues it should be lower.
  The point is only that the test and the bar must be calibrated to each other.

---

## 6. What would change the verdict

A genuinely confirmatory test needs a **new sample** — a different asset class,
or a period that does not yet exist — registered before the data do, with a
decision rule that uses the paired test and an equivalence margin. The current
sample can support the statement "not materially better than the best baseline";
it cannot support "better" or "no effect".

---

## 7. Revision history

| Version | Date | Change |
|---|---|---|
| 1.0 | 2026-11-04 | Initial exploratory note: paired inference, equivalence, gate power, DSR sensitivity, fold and comparator checks. |
