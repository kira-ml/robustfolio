# Power and effective bets — design diagnostics — 2026-10-17

**Status:** Design diagnostic. **Not an experiment and not a registry entry** (see §0).
**Version:** 1.1
**Owner:** Ken Ira Lacson Talingting
**Authority:** [`evaluation_protocol.md`](../docs/evaluation_protocol.md) §4.3, §5.2, §6.1–§6.3, §12.2, §13.1; [`model_and_method_spec.md`](../docs/model_and_method_spec.md) §1
**Reproduce:** `python scripts/diagnostics_power.py --json results/diagnostics_power.json --figure results/diagnostics_power.png`
**Snapshot:** `yahoo-usetf-2007-01-01_2026-09-30-2026-10-17-2ad06139`
**Recorded by:** DEC-20261017-028 — this note is an input; the diagnostics are ruled **not an experiment and not a registry entry** (§0), and finding **F15** is resolved (§6).

---

## 0. What this is, and what it is not

Protocol §12.2 defines an experiment as "any run that produces a metric on which a decision or claim will be based." This note produces **no portfolio, no strategy return series, and no performance metric**. Every number is a property of the data (the eigen-spectrum of the covariance) or of the test design (the power of the registered tests). The results would be identical if M1 and M2 had never been proposed.

It therefore:

* is **not** a registry entry and does **not** count toward any multiple-testing denominator;
* cannot be cited for or against H1, H2, or H3;
* exists to answer two questions that must be settled **before** a Test D result can be interpreted at all — otherwise a null result is indistinguishable from an underpowered test, which is the §12.10 exploratory failure mode wearing a confirmatory label.

It corrects a claim made in the strategy discussion on the same date (§7).

---

## 1. The universe contains 3–5 independent bets, not 18

Eighteen correlated asset-class ETFs are not eighteen bets. The eigen-spectrum of the correlation matrix over the frozen out-of-sample window (168 months) says how many there really are.

| Measure | Value | Reading |
|---|---|---|
| Market factor share (`λ₁/Σλ`) | 0.505 | half of all variance is one direction |
| Variance explained by 1 … 6 factors | 51 / 73 / 82 / 86 / 89 / 91 % | needs 6 factors for 90% |
| Participation ratio `N_part = (Σλ)²/Σλ²` | **3.14** | ~3 effective directions |
| Entropy effective rank `N_ent = exp(−Σp ln p)` | **5.03** | ~5 effective directions |
| Condition number `cond(corr)` | 1,704 | |

The gap between `N_part` (3.1) and `N_ent` (5.0) is itself informative: a few large directions dominate the *variance*, while several small ones carry the *diversity*. Both are far below 18.

The same measurement on each fold's **60-month estimation window** — exactly what an optimizer sees — is stable:

| Measure | min | median | max |
|---|---|---|---|
| `N_part` (corr) | 2.45 | 3.38 | 3.91 |
| `N_ent` (corr) | 4.13 | 5.06 | 5.71 |
| top factor share | 0.39 | 0.44 | 0.61 |
| `cond(Σ)` | 649 | 1,215 | 12,426 |

---

## 2. The near-singularity is real structure, not a short sample

A natural objection: with 18 assets and 168 observations, a small eigenvalue may just be sampling noise. The Marchenko–Pastur law says where the eigenvalues of an **independent** panel of this shape would sit:

* band for an independent 18 × 168 panel: **[0.452, 1.762]**
* observed: **12 of the 18** sample eigenvalues fall *below* the lower edge
* the smallest eigenvalue is **0.0053** — the edge is **85×** that value

An independent panel does not produce this. The panel's near-singularity is genuine correlation structure, which means:

1. **The H1 premise is supported by the data, not assumed.** The sample covariance cannot be inverted safely; naive MVO is *forced* to blow up. (This is now evidence, not framing.)
2. The offending direction has essentially no variance, so any procedure that inverts `Σ` amplifies it — which is precisely the mechanism shrinkage is designed to damp.

---

## 3. What the registered tests can actually detect

### 3(a) The level test is fine. The differences are the problem.

The level test asks "is this strategy's Sharpe different from zero?" (protocol §6.1). Minimum detectable effect at 80% power, one-sided 5%, with `T = 168`:

| | value |
|---|---|
| MDE (annualised Sharpe) | **≈ 0.67** |
| AR(1) of monthly asset returns | median −0.040, max 0.208; first principal component −0.099 |
| first principal component | skew +0.52, Pearson kurtosis 4.54 (3.0 = normal) |

A Sharpe must reach roughly **0.67** before it is statistically distinguishable from zero. Monthly returns are mildly *negatively* autocorrelated (median −0.04), so the Lo (2002) autocorrelation inflation is ~1.0, not a penalty.

For context — and this is asset characterisation, not a strategy result — buy-and-hold annualised Sharpes of the 18 candidates span **0.06 to 1.09** (median 0.45) over this window. Most sit *above* the level-test threshold, so the level test is adequately powered here, and **the interesting question is the small differences, not the levels.**

### 3(b) The paired difference test — the one that decides H2.4

The §6.2 threshold is a **net Sharpe improvement of 0.20** over the best baseline. Whether that is detectable depends almost entirely on how correlated the candidate is with the baseline. Jobson–Korkie / Memmel:

```
Var(ΔSR) = (1/T)[ 2(1−ρ) + SR²(1−ρ²) ]
```

For an assumed level Sharpe of 0.50 annualised (0.144 monthly), `T = 168`:

| ρ (candidate vs baseline) | SE(ΔSR) monthly | MDE(ΔSR) annualised | power at the 0.20 threshold |
|---|---|---|---|
| 0.900 | 0.0348 | 0.300 | 0.50 |
| 0.950 | 0.0246 | 0.212 | 0.76 |
| **0.980** | 0.0156 | **0.134** | **0.98** |
| 0.990 | 0.0110 | 0.095 | 1.00 |
| 0.995 | 0.0078 | 0.067 | 1.00 |
| 0.999 | 0.0035 | 0.030 | 1.00 |

**The §6.2 threshold is detectable at ≥ 80% power once ρ ≥ 0.98.**

Two consequences:

* The paired design is *far* more powerful than the level test — a 0.20 difference is resolvable even though a 0.50 Sharpe level is not. This is not a trick; it is why M1 and M2 are specified to differ from B3 by exactly one component. **The minimal-difference design is what buys the statistical power**, and it should be presented that way in the writeup.
* Power is therefore **conditional on an unmeasured quantity**. ρ in 0.95–0.995 is *expected*, not known. If ρ turns out to be 0.90, the power at the threshold is 0.50 — a coin flip — and a null result must be reported as **underpowered**, not as evidence of no effect.

### 3(c) The deflated-Sharpe non-normality term

With `γ₃ = 0.52`, `γ₄ = 4.54` on the market factor, the DSR denominator `√(1 − γ₃·SR + (γ₄−1)/4 · SR²)` evaluates to **0.971** at the monthly level — a ~3% *favourable* adjustment (the positive skew term dominates the fat-tail term). This is computed on the **market factor**; a long-only optimized portfolio typically carries *negative* skew (crash risk), which pushes the term the other way. The harness must compute this on the actual strategy returns, not on this proxy. With `N = 1` the DSR's selection deflation is minimal, so the binding statistical constraint is power (§3b), not Type I.

---

## 4. The §6.3 fold-consistency gate is a weak filter

§6.3 requires the advantage to hold in ≥ 60% of folds (≥ 9 of 14). Under the null, fold outcomes are coin flips, so:

**P(≥ 9 of 14 | p = 0.5) = 0.212.**

Roughly one null experiment in five passes the gate on its own. Folds share overlapping *training* windows (the 12-month *test* windows do not overlap), so fold outcomes are positively correlated, which pushes the true rate **higher** than 0.212 rather than lower.

This is not a Type-I hole: §6.4 is a conjunction and the §6.1 DSR bullet carries the 5% control. It does mean the gate is close to **non-binding as a discriminator** — it removes little that the DSR test has not already removed. Worth stating plainly, because a reader will otherwise read "robust in 9 of 14 folds" as stronger evidence than it is.

---

## 5. The tension this leaves, stated precisely

Two opposing facts, both now measured:

* **The estimation problem is large.** `N/T = 18/60 = 0.30` observations per parameter, the sample covariance is genuinely near-singular (§2), and the smallest eigenvalue sits 85× below the noise floor. There is real, correctable estimation error — shrinkage *should* help.
* **The prize is small.** The universe carries only 3–5 independent bets (§1). There is little independent cross-sectional structure for a better estimator to uncover; 1/N already captures most of what is there.

Both are true, and they pull in opposite directions. **Which dominates is exactly what Test D asks** — and this note cannot answer it. What the note *can* say is what Test D will be capable of showing: a difference of ≥ 0.20 at ≥ 80% power, or nothing. It cannot resolve a true improvement of, say, 0.10, and it must not be reported as though it had.

---

## 6. Finding F15 — a Sharpe difference is uninterpretable without ρ

**Raised by this note; resolved by DEC-20261017-028 — reading (a) adopted: reported as a design diagnostic, no amendment, `N = 1` unchanged.**

Test D's power depends on ρ, the return correlation between each robust candidate and the best baseline. It is *not* currently a registered output. Without it, a null result cannot be distinguished from an underpowered one — which is the difference between "we tested it and it failed" and "we could not have told either way."

**F15.** Test D must report ρ(candidate, best baseline) alongside every Sharpe difference. If a null result arrives with ρ < 0.98 at the §6.2 threshold, it is **UNDERPOWERED / inconclusive**, not negative.

Governance question this raises: is restating a reported statistic an "amendment" under §12.9 / §12.6.4 ("amendments count as new trials if they change any parameter, **metric**, or decision rule")? Two readings:

* **(a) Design diagnostic, no amendment.** ρ is a detectability input reported in a design appendix, the same class of object as the numbers in this note — it cannot support or defeat a claim, so it does not change the registered metric set. Denominator stays `N = 1`. *Recommended.*
* **(b) Registered secondary metric, pre-run amendment.** Treated literally: adding a reported metric changes the metric set, so it is an amendment, which under §12.6.4 counts as a new trial and raises the denominator to `N = 2` — making success *harder* for adding a diagnostic that only makes the report more honest.

Reading (b) has the perverse property that the more transparent the reporting, the higher the bar. Surfaced rather than resolved for that reason. **Resolution (DEC-20261017-028): reading (a).** ρ is reported in the design/detectability appendix and is not added to the registered metric set, so `EXP-H2-20261017-001` is not amended and keeps `N = 1`. If ρ is later wanted inside the *required* report, that is a separate versioned amendment to `model_and_method_spec.md` §8.

---

## 7. Correction to the earlier verbal claim

In the strategy discussion on 2026-10-17 it was argued that the project is "underpowered for a 0.2 Sharpe claim." **That was too pessimistic and the calculation corrects it:**

* the **paired** difference test detects the §6.2 threshold at ≥ 80% power for ρ ≥ 0.98, which the minimal-difference design makes likely;
* what is genuinely hard is the **level** test, which needs a Sharpe of ≈ 0.67 — but the assets' realised Sharpes in this window (up to 1.09) mostly clear that bar anyway.

The correct statement is narrower and more useful: **the design is powered for the economic threshold provided ρ is high, and the test is silent about improvements below ~0.13.** Recorded here because the earlier claim was made with confidence it had not earned — the model applied to the project must also be applied to the project's own analysis.

---

## 8. Limitations of this diagnostic

1. **Asymptotic and normal.** The power figures use Lo (2002) / Jobson–Korkie asymptotic standard errors. `T = 168` is moderate; the non-normality correction (§3c) is computed on a proxy series.
2. **ρ is assumed, not measured.** This is the whole point of F15. The reported MDEs are conditional on the ρ in each row.
3. **Fold correlation is unquantified.** §4 gives the independent-folds bound and asserts the true rate is higher; the magnitude is not estimated.
4. **No strategy is formed.** By design (§0). These numbers cannot substitute for Test D, only frame it.
5. **The level-test context (§3a) uses buy-and-hold asset Sharpes**, which are not strategies and are not registered; they appear only to establish that the level test is not the binding constraint.

---

## 9. Revision history

| Version | Date | Change | Author |
|---------|------|--------|--------|
| 1.0 | 2026-10-17 | Initial design diagnostics: effective bets (`N_part` 3.14, `N_ent` 5.03, MP comparison), level-test MDE ≈ 0.67, paired-difference power table, fold-gate null rate 0.212. Finding F15 raised. Corrected the earlier "underpowered" claim. | Ken Ira Lacson Talingting |
| 1.1 | 2026-10-17 | Recorded by DEC-20261017-028 as an input: diagnostics ruled non-experimental under §12.2, and F15 resolved — ρ reported in a design appendix, no amendment, `N = 1` unchanged. Header and §6 updated; no measured value changed. | Ken Ira Lacson Talingting |
