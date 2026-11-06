# v1.1 — the country sample, the correction, and the brief

**Released:** 2026-11-06
**Tag:** `v1.1`
**Status:** the first sample remains exploratory and non-confirmatory; the
country sample is confirmatory for that sample.

## What this release adds

- **A pre-registered country-ETF sample.** 18 current-listed iShares MSCI
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
| Country-ETF replication | Confirmatory for that sample |
| Universal, live, or alpha claim | Not made |

The hypotheses of the first sample are **untested, not falsified**: the
registered test was executed without the blindness its registration required
(finding F26).

## Assets

| Asset | File |
|---|---|
| Working paper | `essays/robustfolio-working-paper.pdf` |
| Carousel | `essays/robustfolio-carousel.pdf` |
| Research brief | `essays/robustfolio-research-brief.pdf` |
| Country snapshot | `robustfolio-snapshot-yahoo-countryetf-1998-01-01_2026-09-30-2026-11-05-269a4565.tar.gz` |

Country snapshot digest:

```
SHA-256  d8bf3b43603f192c77b0a4e0f26223c64e70dce2aed17fb2ba2fe67f47a572ef
size     1.89 MB
bundle   269a45651ec04755b7954e8e99db7dc15f6bee92d4fe5a5e0707a67ce95de26c
```

The archive digest identifies the *distribution* (data plus `NOTICE.txt`); the
bundle hash identifies the *data*. They are deliberately different (finding
F31). The first sample's archive remains on the `v1.0.0` release and is
unchanged.

## Reproduce

First sample, from the `v1.0.0` archive:

```bash
ASSET=robustfolio-snapshot-yahoo-usetf-2007-01-01_2026-09-30-2026-10-17-2ad06139.tar.gz
curl -LO "https://github.com/kira-ml/robustfolio/releases/download/v1.0.0/$ASSET"
python scripts/verify_release.py --archive "$ASSET" --run docs/published-run
```

Country sample:

```bash
SNAP=yahoo-countryetf-1998-01-01_2026-09-30-2026-11-05-269a4565
python scripts/pack_snapshot.py --verify "robustfolio-snapshot-$SNAP.tar.gz" --extract-to data/snapshots
python scripts/run_country_sample.py --snapshot "$SNAP" --out results/country_sample
```

Decisions are compared exactly; measurements within 1e-9, with the observed
difference printed.

## Limits

One asset family, one period, flat costs, no market impact. The country sample
is current-listed, so survivorship remains. The numbers belong to their
samples, not to markets in general. Not investment advice.
