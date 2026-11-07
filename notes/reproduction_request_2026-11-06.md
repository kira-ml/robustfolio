# Independent check request

**Date:** 2026-11-06 (updated 2026-11-08)
**Goal:** one independent check of the code, the published tables, or both before 2026-12-04.

The point is a check, not an endorsement. A mismatch is the interesting outcome and
is reported the same way as a match.

**What changed on 2026-11-06.** The snapshot archive is no longer distributed: the
Yahoo and FRED terms do not permit redistribution (DEC-20261106-042). An exact
end-to-end reproduction therefore requires the reviewer to obtain the data
independently. The request below is scoped to what a reviewer can actually run
without receiving restricted data.

**Update 2026-11-07.** Two hermetic checks were added, and the requested scope is
unchanged. `scripts/run_synthetic_demo.py` exercises the real data layout, harness,
all seven methods, and the report builder on a deterministic synthetic panel with a
split and dividends; it is explicitly not a reproduction of the published sample.
The verifier's mutation suite now requires a failure for every exact field, method
order, count, cost level, ranking, baseline, notice, gate, flag, and verdict.

**Update 2026-11-08 — claim correction.** The country sample is now labeled a
pre-specified external replication, not a confirmatory test. The protocol file was
last written after the results, and both were committed together; the repository
cannot establish that the freeze preceded execution. The correction is recorded in
[`audit_2026-11-08.md`](audit_2026-11-08.md) and `DEC-20261108-044`. The reviewer is
asked to attack this label specifically: if the correction is too generous, say so;
if it is still too strong, say that too.

## The message

Send as-is, personalise the first line.

> Hi [name] — I built a pre-registered benchmark for portfolio construction, and I am
> looking for one independent check rather than an endorsement. I recently corrected
> my own country-sample claim: the protocol was not independently verifiable as
> frozen before execution, so it is now labeled an external replication, not a
> confirmatory test. The code and the published tables are public; the market-data
> snapshot is not redistributed for licensing reasons, so the check is either a
> code/claims review or, if you already have independently licensed data, a run
> against your own snapshot. The hermetic checks take a few minutes. If something
> disagrees — especially the corrected label — that is the useful outcome, and I will
> report it either way. Would you take a look?
> <link to the repository, `notes/audit_2026-11-08.md`, and the reviewer's guide>

## What they run without any market data

```bash
git clone https://github.com/kira-ml/robustfolio.git && cd robustfolio
python -m pip install -e ".[dev]"
python -m pytest -q
python scripts/run_synthetic_demo.py --out /tmp/synthetic-demo
python scripts/demo_the_check.py
python scripts/certify_engine.py
```

These exercise the synthetic end-to-end path, the leakage suite, the
release-packaging integrity tests, the snapshot-name checks, the verifier's own
exact/bounded split and mutation suite, the generated paper and cards, and the
engine certificate. They do not reproduce the published numbers, because the input
is not present.

## If they independently hold a snapshot

They can run the comparison against their own archive:

```bash
python scripts/verify_release.py --archive <their snapshot archive> --run docs/published-run
```

Do **not** send them an archive. The project does not redistribute it, and a
reviewer's own data-access terms are theirs to satisfy.

## What to send back

- Operating system, Python version, and whether the install was clean.
- Which check they ran: the hermetic suite, a code/claims review, or a snapshot
  comparison.
- For the suite: pass/fail counts and any failure text.
- For a snapshot comparison: the final line (`EXACT`, `WITHIN`, or a mismatch) and,
  if a mismatch, which quantity differed — not the whole log.
- For a review: the claim that did not survive, and the evidence.

## Log

| Date | Person | Check | Result | Notes |
|---|---|---|---|---|
| | | | | |
| | | | | |

## Rules

- Ask for a check, not a quote.
- Do not explain the expected answer first; offer the protocol link after the run.
- Do not send the snapshot archive.
- Report a mismatch in the README; do not rerun until it matches.
- Two checks, then stop. More is a hobby, not validation.
