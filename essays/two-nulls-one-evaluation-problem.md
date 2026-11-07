# Two nulls, one evaluation problem

**What a failed method and a stopped project taught me about testing portfolio ideas**

*Ken Ira Lacson Talingting · November 2026*

Most portfolio research asks whether a method works. These two projects asked a less comfortable question: **can the evaluation itself support the claim being made?** One project tested seven portfolio constructions against a frozen decision rule. The other tested whether an ML uncertainty layer improves a distributionally robust portfolio, then stopped two follow-up versions before they could touch the holdout.

Both produced nulls. They are not the same kind of null, and that is the point. The interesting failure in each case was not the model. It was the instrument.

---

## Two designs, one question

| | **Robustfolio** | **Epistemic DRO** |
|---|---|---|
| Question | Do robust portfolio methods beat plain baselines under a frozen protocol? | Does ML epistemic uncertainty improve a DRO mean-CVaR portfolio, net of costs, out of sample? |
| Design | 7 methods, 18 US ETFs, 168 out-of-sample months, 14 folds, 1,176 certified solves | 72 ETFs; three pre-registered attempts; v2/v3 stopped before the 2025–2026 holdout |
| Verdict | Both treatments fail the frozen decision rule | H1 tail improvement fails; H2 non-inferiority passes; H3 ablation fails |
| Status | Exploratory US sample; confirmatory country replication | Methods study; holdout untouched |

The designs share a discipline rather than a codebase: point-in-time eligibility, walk-forward evaluation, net-of-cost returns, a pre-declared comparator, and a written rule for what counts as success. They also share the same uncomfortable outcome. The method was not the binding constraint.

---

## The first null: a win too small for the test to see

Robustfolio compared five baselines and two treatments on 18 US ETFs over 168 months. The best baseline was `B3`, plain sample-covariance, sample-mean MVO — the method the project set out to critique. The best treatment, `M2`, earned a net Sharpe of 0.8538 against `B3`'s 0.7896. That is a gap of **+0.064**.

The frozen rule required a **0.20** materiality bar and a probabilistic Sharpe ratio of **0.95** against the best baseline. `M2`'s PSR was **0.587**. Both candidates returned **FAILURE**.

The tempting reading is that the method failed. The more useful reading is that the test could not have succeeded. The registered PSR gate is a *level* test: it needed an observed gap of about **0.478** to certify a 0.20 effect, and its 80%-power minimum detectable effect was about **0.72**. The paired test, which the gate does not use, was powered to separate roughly 0.13–0.20; there `M2` was **+0.064 [−0.011, +0.147]**, with a 90% upper bound that rules out a 0.20 advantage.

So the result is narrower than either "the method works" or "the method fails." The data are consistent with a small advantage, and inconsistent with a material one. The US sample remains **exploratory**, because the registered confirmatory test's answer was observed before it ran (finding F26). The hypotheses are **untested, not falsified**.

The country replication made the evaluation problem visible from another direction. On 18 country ETFs over 252 months, the best baseline changed from sample MVO to **equal weight**, and the treatment edge did not replicate. The comparator was not a fixed feature of the world. It was a property of the sample.

---

## The second null: a model that calibrated but did not inform

Epistemic DRO asked whether uncertainty from an ML return model could improve the tail-risk/return trade-off of a mean-CVaR portfolio. The v1 result was mixed in a way that is easy to misread:

- **H1 failed.** The uncertainty-aware portfolio did not achieve lower drawdown or CVaR than the point-estimate DRO and mean-variance comparators, net of costs.
- **H2 passed**, but only as a **non-inferiority** test: net Sharpe was not materially worse than the best baseline.
- **H3 failed.** The ablation did not attribute a tail-risk improvement to the uncertainty layer.

The descriptive numbers show why the non-inferiority result is not a victory lap. The reduced `M1` had a net Sharpe of 0.816, max drawdown of −0.242, and CVaR95 of −0.083. The point-estimate DRO `B5` had 0.798, −0.243, and −0.084. Equal weight `B1` had 0.673, −0.266, and −0.098. The uncertainty layer neither improved the tail nor damaged returns enough to fail the non-inferiority bar. That is a valid methods result, not an investable edge.

Then the project did something a model-search pipeline rarely does: it tested whether the next experiment deserved to exist. Version 2's uncertainty features passed the pre-holdout gate only **65.4%** of the time, below the 80% bar, despite good conformal coverage (**89.9%** validation, **85.9%** development test). Version 3's conditional sigma passed only **43.0%** of the time. Its calibration was superficially excellent — mean sigma **0.0429** against mean realized absolute return **0.0430** — but the correlation was only **0.284**, and the decile spread was **0.0376**. Calibration was not information.

Both versions stopped before the holdout. That decision is the project's most distinctive result.

---

## The evaluation problem

The two projects point at the same four lessons.

### 1. The comparator chooses the question

A method that beats equal weight has demonstrated something different from a method that beats sample MVO. Robustfolio's best baseline changed when the sample changed. Epistemic DRO's H2 is explicitly a comparison against the best baseline, which is why a non-inferiority pass cannot be reported as a win. The comparator must be chosen before the result is seen, and reported with the result. Otherwise "the method failed" may only mean "the benchmark was strong."

### 2. Power is part of the result

A gate that cannot detect a 0.20 effect is not evidence that no 0.20 effect exists. Robustfolio's level PSR gate needed roughly 0.48 observed. Epistemic DRO's 80% MI gate had **zero power** at a 20% R² signal in its synthetic power study; the pooled alternative had full power there. Both are statements about the instrument, not about the strategy. The minimum detectable effect and the observed interval belong next to every verdict.

### 3. A gate has error rates too

Epistemic DRO's gate study is the clearest example. Under an iid pooled test, **20 of 21** signals passed; under a block-aware null, **3 of 21** did. The v2 and v3 sigma signals did not survive. A later effect-size audit found that survivors' IC confidence intervals included zero and that trailing volatility dominated the conditional sigma. The original gate was not merely strict or lenient; it was answering a different question from the one the holdout would have asked. Dependence, multiple testing, and effect size have to be designed into the gate, not discovered after it fails.

### 4. The holdout is a budget, not a formality

Epistemic DRO stopped v2 and v3 before spending the 2025–2026 holdout, which remains untouched. Robustfolio's US confirmatory slot is empty because the registered test was executed non-blind while validating the report generator. One project preserved its ability to learn later; the other documented exactly how that ability is lost. A holdout is valuable only if the evidence that precedes it is strong enough to justify the spend — and only if the spend is actually blind.

---

## What I would do next

Not another model on the same data. Not a v4. Not a new Robustfolio method.

The next study, if there is one, should start from a genuinely new sample or a period that does not yet exist, and it should pre-register:

1. **The comparator rule**, including what happens if the best baseline changes.
2. **The minimum effect size** that would change a decision.
3. **The power calculation** for the gate, in that effect-size unit.
4. **A dependence-aware null** and a multiple-testing correction.
5. **One use of the holdout**, with the stopping rule written before the data arrive.

That is a 2027 decision, not a November one. The November deliverable is the reusable instrument: the evaluation checklist, the leakage suite, the certified solver, the gate study, and the discipline to stop.

---

## What this does not say

Neither project claims alpha, market-beating performance, investability, or live readiness. Robustfolio's US sample is exploratory and its hypotheses are untested; its country sample is confirmatory only for that sample. Epistemic DRO is a methods study on a current-listed ETF universe, not a survivorship-free production backtest; H2 is a non-inferiority pass, not evidence of superiority. Its gate and effect-size study is a **post-hoc methods audit**, not a new experiment. Neither project used the 2025–2026 holdout. Nothing here is investment advice.

The two nulls are useful because the evaluation was designed to make them informative. That is the part worth reusing.

---

**Code and papers**

- Robustfolio: [github.com/kira-ml/robustfolio](https://github.com/kira-ml/robustfolio) · [working paper](https://github.com/kira-ml/robustfolio/blob/main/essays/robustfolio-working-paper.pdf)
- Epistemic DRO: [github.com/kira-ml/epistemic-dro](https://github.com/kira-ml/epistemic-dro) · [working paper](https://github.com/kira-ml/epistemic-dro/blob/main/paper/mini_paper.pdf)
