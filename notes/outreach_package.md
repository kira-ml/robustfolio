# Outreach and publication package (working notes — not governed until posted)

Once posted or sent, the text below is a **public artefact** under
[E3 §1 and §4](../docs/results_reporting_and_claims_policy.md): the essays' rules apply to the message
text itself, not only to the document it links to. That is why every draft here carries the
non-confirmatory disclosure and the net-excess phrasing, even the one-liners.

**Order matters: direct outreach first, public posts second.** Direct outreach converts 10–50× better,
and the point of both is the same — *did someone whose work I respect engage substantively with a
specific claim?* Not impressions, not likes, not stars. Those are the Goodhart target; substantive
engagement by a competent sceptic is the measure.

---

## 1. The one-paragraph version (for a cold DM or an intro)

> I've just published a pre-registered evaluation of robust portfolio construction on 18 US ETFs — the
> answer is a null, and that's not the interesting part. The interesting part is that my own
> reproduction claim failed twice, caught both times by a check I'd written to test it, and what came
> out of that is a cleaner way to state what a numerical result actually guarantees. Everything is
> reproducible from a frozen archive, and there's a script that checks it rather than a summary that
> asserts it. I'd value a critique of one specific section — [SECTION]. No ask beyond that.

Rule: name **one specific section** you want attacked. A vague "let me know what you think" gets
"looks great".

## 2. Two DM variants

**Quant research / systematic investing:**

> You've written about [specific thing]. I've published a pre-registered null on robust portfolio
> construction (18 US ETFs, 168 OOS months, 14 folds, net excess Sharpe @10bps). The result is
> unremarkable; the part I think you'd find worth attacking is the claim that with one pre-registered
> comparison the multiplicity correction is *inert*, so the binding constraint becomes the choice of
> baseline — both my candidates pass a DSR against zero and fail a PSR against the best baseline. If
> that reframing is wrong, I'd rather know before more people read it. The specific section is
> `essays/cut-quant.md` §"Why the benchmark, not the correction, is the binding constraint".

**ML / data science engineering:**

> A question about verification rather than models. I wrote that my pipeline reproduces its published
> table bit-for-bit, then added a check that could test it — and it failed, twice. Once because a BLAS
> kernel picks its summation order at run time from CPU features; once because a solver's output is a
> property of (data, code, machine), not (data, code), and my tolerance didn't say so. The repair was
> to split the claim: decisions exact, measurements bounded, observed difference printed.
> `essays/cut-ml-ds.md` is the write-up. I'd like the case where this split is *insufficient* —
> because I suspect there is one.

## 3. Public posts

### 3a. LinkedIn (long)

> I spent most of this project trying to falsify my own result. The result held up. My claim about
> how well I had verified it did not — twice, in two consecutive runs of a check I wrote to test it.
>
> The question I set out to answer: does a robust, turnover-aware portfolio construction method beat a
> plain one out-of-sample, net of transaction costs — once you adjust for having tried more than one?
> I pre-registered the hypothesis, the metrics, the thresholds and the decision rule before any data
> was touched, because a clean "no" is a successful outcome for a design like this.
>
> The answer is no. Best baseline (plain sample MVO) net excess Sharpe 0.79 at the 10 bps headline cost,
> 90% CI [0.33, 1.32]; best candidate 0.85, 90% CI [0.43, 1.37] — a gap of +0.06 against a
> pre-registered bar of 0.20, and
> the design was powered to separate 0.13–0.20. The effect is absent, not invisible.
>
> Here is what I actually learned, and it is not about portfolios:
>
> 1. I claimed my repository reproduces its published table bit-for-bit. It failed its first real run —
>    one metric out by 4.2e-17, because a BLAS kernel chooses its own summation order at run time.
> 2. I fixed that. The next run failed harder — thirteen metrics, up to 4.7e-12, on an identical
>    environment. The cause was that a quadratic program is solved only to its tolerance. **A number
>    produced by a solver is a property of (data, code, machine), not (data, code).**
> 3. So the claim is split rather than softened: every *decision-bearing* quantity compared exactly —
>    method set, rebalances, folds, ranking, selected baseline — and the continuous metrics within a
>    documented 1e-9, with the observed difference printed on every run. That claim has now survived
>    being tested after failing twice.
> 4. And the defence that failed was the one I was proudest of: to validate the report generator
>    end-to-end I had to run the frozen configuration — which was the confirmatory configuration. The
>    registered test was executed without its required blindness, so it is re-designated
>    non-confirmatory and the hypotheses are **untested, not falsified**. I won't call it a test in
>    order to have a result.
>
> Everything is exploratory and non-confirmatory, the metric is net *excess* Sharpe, and no absolute
> return claim is made anywhere. The archive is frozen, and there is a script that checks the numbers
> rather than a summary that asserts them — if it prints anything other than EXACT or WITHIN, the
> essays are wrong and the check is right.
>
> Link in the comments. I'd rather be told where this is wrong than told it looks good.

### 3b. LinkedIn / X (short)

> My reproduction claim failed twice — caught both times by a check I wrote to test it.
>
> Cause 1: a BLAS kernel picks its summation order at run time from CPU features.
> Cause 2: a solver's output is a property of (data, code, machine), not (data, code).
>
> So I stopped claiming "bit-for-bit" and split it: decisions compared exactly, measurements bounded,
> observed difference printed on every run.
>
> The underlying experiment is a pre-registered null on robust portfolio construction — net excess
> Sharpe, exploratory and non-confirmatory, no absolute return claim. The write-up is about the
> verification, not the portfolio. If the exact/bounded split is wrong for your setting, I want that
> counterexample.

## 4. Who to contact (categories; names are the owner's call)

Aim for 10–20 people, weighted to people who have *publicly written* about the thing you're claiming —
those are the ones whose critique is worth having, and the ones most likely to reply to a specific,
checkable question.

- **Numerical / reproducibility-adjacent**: people who write about determinism, BLAS/LAPACK behaviour,
  or reproducible research in Python — the F33/F34 split is directly their subject.
- **Backtest-critique / deflated-Sharpe** authors — they will attack the DSR-vs-PSR reframing, which is
  the claim most worth attacking.
- **Shrinkage / robust-estimation** people — the effective-bets diagnostic (`N_part ≈ 3.1`,
  12 of 18 eigenvalues below the Marchenko–Pastur lower edge) is a hypothesis aimed squarely at them.
- **ML/DS verification and testing** practitioners — the "my verifier was the bug three times" thread.
- One or two people with **no finance background** — the flagship is written for them, and if they can't
  follow the argument, the argument is wrong.

What to ask, in one line: *"Which of these four defences is the weakest, and what's the smallest change
that would break it?"*

## 5. What success looks like (and is not)

| not the measure | the measure |
|---|---|
| impressions, likes, stars | has one competent sceptic restated a claim of yours accurately, then attacked it? |
| "great project!" | has someone found a case the exact/bounded split does not cover? |
| a job offer | has the F25 reading been challenged, so the verdict is either defended or corrected? |

The one outcome that would be a genuine failure: nobody checks, everyone is nice, and the claims go
uncorrected.
