# Essays

These are the written deliverables of [`robustfolio`](../README.md), published alongside the code so that
every claim in them can be checked against the repository that made it.

| # | Essay | Audience | Length |
|---|---|---|---|
| 1 | [`flagship.md`](flagship.md) — *I tried to break my own result before I published it* | General technical | ~2,800 words |
| 2 | [`cut-quant.md`](cut-quant.md) — *A pre-registered null on robust portfolio construction* | Quant research / systematic investing | ~1,100 words |
| 3 | [`cut-ml-ds.md`](cut-ml-ds.md) — *Four defences against fooling yourself* | ML / data science engineering | ~1,600 words |

**Read the flagship first.** It leads with the method, uses the finance result as its worked example, and
ends with the toolkit. The two cuts are not summaries: the quant cut adds the benchmark-choice argument,
the turnover inversion and the effective-bets diagnostic; the ML/DS cut strips the domain and states the
four defences generically, with the solver and library failures as its evidence.

## What every piece is subject to

The claims rules are [E3, a draft](../docs/results_reporting_and_claims_policy.md) — the reporting template
and the operational form of protocol §14.2. In brief, and binding on all three essays:

- The run is **exploratory and non-confirmatory**; it may not be cited for or against any hypothesis. No
  confirmatory test exists (finding F26, DEC-20261017-034), so the hypotheses are **untested, not
  falsified**.
- **Net excess Sharpe only.** No absolute return, no "beats the market", no investable framing. Cumulative
  net excess return is a metric's input path, not a return stream.
- Gross Sharpe appears only as a labelled diagnostic beside the net figure.
- No p-value without its benchmark — here the DSR/PSR contrast *is* the finding.
- No superiority claim without its interval; no claim from a single cost level or a single fold.
- Findings describe **this implementation**, not upstream library bugs: F19 and F28 document upstream
  behaviour working as specified.

## The check, rather than the summary

The number the essays report is reproducible from the frozen release archive. Rather than trust the
prose, run the command that tests it:

```bash
python scripts/verify_release.py --archive <the release asset> --run docs/published-run
```

It compares every **decision-bearing** quantity exactly — method set, rebalances, folds, headline cost
level, the ranking by net Sharpe, and the selected baseline — and the continuous metrics within a
documented `1e-9`, printing the observed worst difference on every run. If it prints anything other than
`EXACT` or `WITHIN`, the essays are wrong and the check is right.
