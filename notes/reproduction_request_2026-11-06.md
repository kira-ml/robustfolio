# Reproduction request

**Date:** 2026-11-06
**Goal:** two independent runs of one published table before 2026-12-04.

The point is a check, not an endorsement. A mismatch is the interesting outcome and
is reported the same way as a match.

## The message

Send as-is, personalise the first line.

> Hi [name] — I built a pre-registered benchmark for portfolio construction, and I am
> looking for one independent check rather than an endorsement. The first sample ships
> as a 1.67 MB archive; one command re-runs seven methods and compares the result to
> the published table. It takes about ten minutes. If it disagrees, that is the useful
> outcome, and I will report it either way. Would you run it?
> <link to the v1.0.0 release and its SHA-256>

## What they run

```bash
ASSET=robustfolio-snapshot-yahoo-usetf-2007-01-01_2026-09-30-2026-10-17-2ad06139.tar.gz
curl -LO "https://github.com/kira-ml/robustfolio/releases/download/v1.0.0/$ASSET"
python -m pip install -e .
python scripts/verify_release.py --archive "$ASSET" --run docs/published-run
```

## What to send back

- Operating system, Python version, and whether the install was clean.
- The final line: `EXACT`, `WITHIN`, or a mismatch, with the maximum absolute
  difference.
- If a mismatch: which quantity differed, not the whole log.

## Log

| Date | Person | Result | Notes |
|---|---|---|---|
| | | | |
| | | | |

## Rules

- Ask for a check, not a quote.
- Do not explain the expected answer first; offer the protocol link after the run.
- Report a mismatch in the README; do not rerun until it matches.
- Two runs, then stop. More is a hobby, not validation.
