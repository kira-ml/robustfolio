# v1.1 — the country sample, the correction, and the brief

> **Data archive removed (2026-11-06).** The snapshot archive and its checksum are no longer distributed: the upstream Yahoo Finance and FRED terms do not permit redistribution. The repository continues to publish the code, tables, figures, and digests needed to inspect the result. See [`data_licenses.md`](data_licenses.md) and [`open_source_and_license_policy.md`](open_source_and_license_policy.md) (v1.2).

> **Claim correction (2026-11-08).** The country sample was originally labeled confirmatory. The protocol file was last written after the results, and both were committed together; the repository cannot establish that the freeze preceded execution. The sample is now reported as a pre-specified external replication, not a confirmatory test. See [`audit_2026-11-08.md`](../notes/audit_2026-11-08.md) and [`release-notes-v1.1.1.md`](release-notes-v1.1.1.md).

**Released:** 2026-11-06
**Tag:** `v1.1`
**Status:** the first sample remains exploratory and non-confirmatory; the
country sample is a pre-specified external replication, not a confirmatory test.

## What this release adds

- **A pre-specified country-ETF sample.** 18 current-listed iShares MSCI
  country ETFs, 2005-07 to 2026-06, 252 months in 21 folds, the same seven
  methods and the same 0.20 bar. The best baseline changed from `B3` to equal
  weight (`B1`): 0.3527 against `M2` 0.3193 and `M1` 0.2710. The treatment
  edge did not replicate; the lesson about comparators did.
- **The power correction.** The registered PSR gate is a level test: it needed
  an observed gap of 0.478 to certify a 0.20 bar, and its 80%-power threshold
  was 0.72. On the paired test `M2` is +0.064 [−0.011, +0.147], so a 0.20
  advantage is excluded and the null survives the repair of the test.
- **The communication layer.** A thesis-first README, `docs/positioning.md`,
  a two-page research brief, and an eight-slide carousel. The paper and the
  published tables are unchanged in substance.
- **Citation metadata.** `CITATION.cff`, so the repository can be cited.

## Evidence status

| Claim | Status |
|---|---|
| Single-factor comparison (first sample) | Exploratory, non-confirmatory |
| Power audit | Verified arithmetic on the published series |
| Country-ETF replication | External replication; protocol dated 2026-11-05, freeze not independently verified (corrected 2026-11-08) |
| Universal, live, or alpha claim | Not made |

The hypotheses of the first sample are **untested, not falsified**: the
registered test was executed without the blindness its registration required
(finding F26).

## What is published

| Document | File |
|---|---|
| Working paper | `essays/robustfolio-working-paper.pdf` |
| Carousel | `essays/robustfolio-carousel.pdf` |
| Research brief | `essays/robustfolio-research-brief.pdf` |

The country snapshot is **not distributed**. It remains an internal research
artefact for the reasons in [`data_licenses.md`](data_licenses.md): the upstream
Yahoo Finance terms prohibit automated collection and redistribution without
express permission, and FRED's terms prohibit archiving FRED content or providing
it to third parties. Its identity is recorded so a reader can tell which input
produced the tables:

```
sha256  d8bf3b43603f192c77b0a4e0f26223c64e70dce2aed17fb2ba2fe67f47a572ef
bundle  269a45651ec04755b7954e8e99db7dc15f6bee92d4fe5a5e0707a67ce95de26c
size    1.89 MB (archive, no longer distributed)
```

The archive digest identifies the *distribution* (data plus `NOTICE.txt`); the
bundle hash identifies the *data*. They are deliberately different (finding F31).

## Reproducibility

The code, the frozen configuration, and the committed tables remain available.
The first sample's reference tables are in `docs/published-run/`; the country
sample's numbers are reported in the paper and the brief.

`scripts/verify_release.py` compares a fresh run against the reference tables,
but it needs a snapshot archive to do so. Because the archives are not
redistributed, a third party cannot run that exact end-to-end check from this
repository alone. The comparison logic and the reference tables remain
inspectable, and the limitation is stated rather than hidden. The first
sample's archive was removed from `v1.0.0` at the same time.

## Limits

One asset family, one period, flat costs, no market impact. The country sample
is current-listed, so survivorship remains. The numbers belong to their
samples, not to markets in general. Not investment advice.
