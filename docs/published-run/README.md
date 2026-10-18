# Published run — `outcomes.csv` and `decisions.csv`

**Version:** 1.3
**Status:** Frozen
**Created:** 2026-10-18
**Last Updated:** 2026-10-18

These are the **published tables** from the first end-to-end run of the reporting layer,
`EXP-X-20261017-003`, computed from the frozen snapshot
`yahoo-usetf-2007-01-01_2026-09-30-2026-10-17-2ad06139`: the seven methods' `outcomes.csv`, and the
`decisions.csv` table that states what the §6.1–§6.4 rules *concluded* from it.

They are committed, in full, for one reason: **they make the reproduction claim a standing guarantee
instead of a one-off.** `scripts/verify_release.py` compares freshly computed tables against reference
tables. Without a committed reference, that check can only ever be run by a person who already has a
run directory — so CI could regenerate the numbers but never say whether they were *the same* numbers.
Now it can, and the repository's own CI runs it against the release archive:

```bash
python scripts/verify_release.py \
    --archive <the release asset> \
    --run docs/published-run \
    --expect-sha256 <the digest quoted in the release notes>
```

Expect either **`EXACT`, max abs diff `0.000e+00`** (the machine agreed to the last bit) or
**`WITHIN 1e-09`** with the observed difference printed (it did not, and the difference is smaller
than the arithmetic can be pinned down to). Both exit zero. A difference of half a rebalance, a
different cost level, a reordered ranking, a different benchmark baseline or **a different verdict**
exits non-zero in either case, because no tolerance applies to a decision.

## Why the verdict table is committed as well

`decisions.csv` is the second half of the published set (DEC-20261018-041), and it is worth stating
why it is pinned here rather than regenerated like the other companion files.

The verifier's first version compared the metrics and the *ranking*. The ranking was standing in for
the verdict, and those are not the same object. §6.1–§6.4 do not decide on a ranking; they decide on a
**conjunction of gates** — `pass_psr`, `pass_dsr`, `pass_sharpe_gap`, `pass_turnover`,
`pass_drawdown`, `pass_cost_levels`, `pass_folds`, `pass_fold_share`, then the `statistical`,
`material` and `robust` summary flags — and a candidate can lead the ranking and still fail the
conjunction. In this run the two happen to agree. There is no reason they must.

So the table that carries the verdict is now published, and every field of it that *is* a decision is
compared exactly, `verdict` included. That closes the strongest form of the claim this repository
makes. Not "the metrics are stable", but **the answer is the same**.

## What reproduces exactly, and what reproduces to a bound

This section used to be called "the equality is a property of the arithmetic, not of the machine",
and it used to claim tolerance exactly zero against a pinned digest on two platforms. **Both of those
claims were falsified by the check itself**, which is the single most useful thing that has happened
to this repository's claims so far.

**First failure (finding F33, DEC-20261018-037).** One column, `autocorr1`, was `4.163e-17` away —
about three units in the last place — while the other seventeen columns matched bit-for-bit.
`autocorr1` went through `np.corrcoef`, which reaches a BLAS `ddot`/`dgemm` kernel, and OpenBLAS
selects its kernel at *runtime* from the CPU's feature set, so the same bytes and the same Python
produced different last bits on a different CPU. It is now computed with an exactly-rounded summation
(`math.fsum` over the departures, plus the primitives IEEE-754 requires to be correctly rounded), so
every rounding step is defined by the standard rather than chosen by a kernel — and it is slightly
*more* accurate for it. Regenerating the table after that fix moved exactly one column, in its last
three bits, and no headline number; the diff is recorded in that decision. That fix is still correct
and still wanted.

**Second failure (finding F34, DEC-20261018-038).** On the next runner, **thirteen** of the eighteen
columns moved, the worst by `4.698e-12`. This one is not a defect and cannot be fixed the same way:

1. The estimator's covariance is a matrix product evaluated by a runtime-chosen BLAS kernel, so two
   machines can disagree in the last bits of `Sigma-hat`. Thread count is ruled out by experiment:
   the whole pipeline run with one BLAS thread and with four produces byte-identical tables here.
2. A quadratic program is solved **only to its solver's tolerance**. The frozen `SOLVER_TOL` is
   `1e-14`, so the optimal portfolio is defined to about that much, and a `1e-16` difference in the
   input reappears in the weights at `~1e-12`. Asking for a solver's output to be bit-for-bit equal
   across CPUs asks for a property the artefact never had.

The honest conclusion is not "the numbers are approximate, so widen the tolerance". It is that
**exactness was never the right claim for the measurements, and always the right claim for the
decisions.** So the verifier splits them:

- **Compared exactly.** The method set and its order, `rebalances`, `folds`, the headline cost level,
  the ranking of methods by net Sharpe, and which baseline the §6.1/§6.2 rules select — and every
  decision-bearing field of `decisions.csv`: the candidate set and its order, the selected baseline,
  the eight `pass_*` gates, the three summary flags, and the `verdict` itself. Any difference fails
  the build. These are discrete, they are what the experiment is *for*, and a `1e-12` wobble cannot
  move them.
- **Compared within `1e-9`.** The continuous quantities in both tables — the metrics, and the
  statistics the verdict was computed from (`psr`, `dsr_pvalue`, `sharpe_gap`, `max_fold_share`, the
  turnover ratio and the drawdown slack). That constant is 200× the worst cross-platform difference
  measured and five orders of magnitude below the four decimals at which any of these numbers is
  quoted or compared — loose enough to survive a runtime-chosen kernel, and far too tight to survive
  a changed estimator, cost model, threshold or window, which is what a verifier is for. The observed
  worst difference is printed on every run, so a reader sees the bound being spent rather than being
  told it exists.

The margin in the paragraph above is the only place it is stated in prose on purpose. It is derived
from two constants (`verify_release.TOLERANCE` and `report.PRINTED_DECIMALS`) and asserted by
`tests/test_release_verification.py`, because it had previously been written into six artefacts and
three of them had drifted to the wrong order of magnitude.

## Why this is not circular

The tables are a *record of an output*, not an input. Nothing in the pipeline reads them; the code
re-derives every number from the price panel in the archive. A mismatch is therefore information
about the code or the archive, never about these files — which is what makes them usable as a check.

## What it is not

**Exploratory and non-confirmatory.** These are the numbers of `EXP-X-20261017-003`, which was
executed to validate the report generator. They may not be cited for or against any hypothesis
(finding **F26**, `decision_log.md` DEC-20261017-034), and that includes the `verdict` column: it is
the output of the frozen decision rules applied to an exploratory run, not a confirmatory test of
`H2.1` or `H2.2`. The files are here to make a check runnable, not to be a result.

The other companion files a full run produces (`calibration.csv`, `design.csv`, `folds_*.csv`,
`net_excess_returns.csv`, `manifest.json`, `report.md`) are deliberately **not** committed: they are
regenerated by one command, and `results/` ignores run directories for that reason. The two files
pinned here are the tables the verifier compares against.
