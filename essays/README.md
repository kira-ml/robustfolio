# Essays

These are the written deliverables of [`robustfolio`](../README.md), published alongside the code so that
every claim in them can be checked against the repository that made it.

| # | Essay | Audience | Length |
|---|---|---|---|
| 1 | [`flagship.md`](flagship.md) — *I tried to break my own result before I published it* | General technical | ~2,800 words |
| 2 | [`cut-quant.md`](cut-quant.md) — *A pre-registered null on robust portfolio construction* | Quant research / systematic investing | ~1,100 words |
| 3 | [`cut-ml-ds.md`](cut-ml-ds.md) — *Four defences against fooling yourself* | ML / data science engineering | ~1,600 words |
| 4 | [`robustfolio-working-paper.pdf`](robustfolio-working-paper.pdf) — *The benchmark is the binding constraint* | Research / systematic investing | 10 pages |
| 5 | [`robustfolio-carousel.pdf`](robustfolio-carousel.pdf) — *My own test rejected my best method. It couldn't see a win that size.* | LinkedIn / general technical | 8 slides |
| 6 | [`robustfolio-research-brief.pdf`](robustfolio-research-brief.pdf) — *What a backtest can prove* | Recruiters / research leads / collaborators | 2 pages |

**The research brief.** [`robustfolio-research-brief.pdf`](robustfolio-research-brief.pdf) — *What a backtest can
prove*: two pages for a recruiter, a research lead, or a collaborator. It states the thesis, the three
contributions with their evidence status, the method in one paragraph, the sentence the result supports,
and the links to verify it. It is written to be read in five minutes and checked in ten. The source is
[`brief.typ`](brief.typ); every number is one of the published ones.

**The one-page version.** [`one-pager.pdf`](one-pager.pdf) — *I tried to break my own result before I
published it*: the four defences, the one that failed, and the null underneath, on one sheet. It carries
the project name and its subject above that title, because the title is a hook and a sheet read away
from the post still has to say which project it belongs to. It is not a
hand-made graphic. `python scripts/make_onepager.py` redraws it from the published tables, and
`tests/test_onepager.py` checks that its numbers are the published ones, that the disclosure the policy
requires is on it, that no block crosses the margin, and that it still fits on one page. A number typed
into a post has nothing to notice it drifting; this one has a test.

**The carousel.** [`robustfolio-carousel.pdf`](robustfolio-carousel.pdf) — *My own test rejected my best
method. It couldn't see a win that size.*: eight slides for a LinkedIn document post. It opens on the
test's blind spot, then sets out the problem, the benchmark built to address it, the result and the flaw
behind it, before the correction and the new sample. It defines net excess Sharpe and the decision rule in
plain language, then shows the 0.8538, the +0.064 gap, the 0.20 bar, the paired 0.917 and the bound the
data support. It is written for a non-specialist audience without dropping the technical specifics: 18
ETFs, 168 months, 1,176 solves, a leakage suite, a numerical check and a reproduction check. The cap sweep
is reported in one line on the correction slide: it did not rescue shrinkage, and it did bind the
Black–Litterman treatment. The final act reports the pre-registered country-ETF sample: 18 country ETFs,
2005–2026, 252 months; the best baseline is 1/N, both treatments underperform it, and the treatment
advantage does not replicate. It is drawn in Typst from `paper/generated/paired.typ` and
`paper/generated/country.typ`; `python scripts/build_paper.py` rebuilds it and
`tests/test_carousel.py` checks the slide count, the rendered numbers and the source.
`robustfolio-carousel-cover.png` is the 4:5 cover for a single-image post. The mechanism note is
[`notes/cap_sweep_shrinkage_2026-11-04.md`](../notes/cap_sweep_shrinkage_2026-11-04.md); the new
sample is [`notes/country_sample_result_2026-11-05.md`](../notes/country_sample_result_2026-11-05.md).

**Read the flagship first.** It leads with the method, uses the finance result as its worked example, and
ends with the toolkit. The two cuts are not summaries: the quant cut adds the benchmark-choice argument,
the turnover inversion and the effective-bets diagnostic; the ML/DS cut strips the domain and states the
four defences generically, with the solver and library failures as its evidence.

**The long version.** [`robustfolio-working-paper.pdf`](robustfolio-working-paper.pdf) — *The benchmark is
the binding constraint*: the argument at length, single column, A4, with the decisions, the cost sweep, the
turnover inversion and the design diagnostic in one place. It is generated the same way the one-pager is.
`python scripts/build_paper.py` writes every measurement the paper quotes into `paper/generated/numbers.typ`
from `docs/published-run/`, and `paper/paper.typ` interpolates from it — the prose types no number of its
own. [`tests/test_paper.py`](../tests/test_paper.py) rebuilds the PDF and fails if a table value is missing
from the rendered text, if a measurement appears in the source, or if a claim the policy prohibits appears
anywhere in the document. The title is the paper's actual finding: with one registered comparison, the
deflation machinery has nothing to correct, and the benchmark is what decides the verdict. The paper
also reports the post-hoc cap sweep: it does not rescue shrinkage, and the mean treatment's
cap-conditional advantage remains below the bar. The country-ETF sample is the external-validity
test: the best baseline is 1/N, both treatments underperform it, and the treatment advantage does
not replicate. Its values are generated into `paper/generated/country.typ` from
`docs/published-run/country-sample/`; the prose types none of them.

## What every piece is subject to

The claims rules are [**E3, frozen at v1.0**](../docs/results_reporting_and_claims_policy.md) — the reporting
template and the operational form of protocol §14.2, with every rule marked `[§14]` (a restatement of the
frozen protocol, which wins any conflict) or `[E3]` (the policy's own rule). In brief, and binding on all
three essays:

- The run is **exploratory and non-confirmatory**; it may not be cited for or against any hypothesis. No
  confirmatory test exists (finding F26, DEC-20261017-034), so the hypotheses are **untested, not
  falsified**.
- **Net excess Sharpe only.** No absolute return, no "beats the market", no investable framing. Cumulative
  net excess return is a metric's input path, not a return stream.
- Gross Sharpe appears only as a labelled diagnostic beside the net figure.
- No p-value without its benchmark — here the DSR/PSR contrast *is* the finding.
- No superiority claim without its interval; no claim from a single cost level or a single fold.
- **The verdict rests on a named reading.** §6.3's "advantage" is not pinned to a metric; the confirmed
  reading (fold wins on net Sharpe, the concentration clause on the per-fold mean return difference) is
  what produces `FAILURE` for `M2`, and E3 §8 records it as load-bearing rather than leaving it implicit.
- Findings describe **this implementation**, not upstream library bugs: F19 and F28 document upstream
  behaviour working as specified.

## The check, rather than the summary

The number the essays report can be checked against the frozen snapshot, but the snapshot is **not
distributed**: the Yahoo and FRED terms do not permit redistribution. A reader who independently holds
the archive can run the command that tests it:

```bash
python scripts/verify_release.py --archive <path to your snapshot archive> --run docs/published-run
```

It compares every **decision-bearing** quantity exactly — method set, rebalances, folds, headline cost
level, the ranking by net Sharpe, the selected baseline, and — from the published verdict table — each
of the eight §6.1–§6.4 gates and the `verdict` itself — and the continuous quantities within a
documented `1e-9`, printing the observed worst difference on every run. If it prints anything other than
`EXACT` or `WITHIN`, the essays are wrong and the check is right. The licence record is
[`../docs/data_licenses.md`](../docs/data_licenses.md).
