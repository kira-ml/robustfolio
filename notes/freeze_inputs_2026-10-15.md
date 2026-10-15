# Freeze Inputs — 2026-10-15

**Owner:** Ken Ira Lacson Talingting
**Purpose:** Carry inputs from tonight's code review, diagnostic, and reading into the protocol-freeze session. **Not a Tier 0 document. Not a contract. Not a decision.**
**Consumed by:** `evaluation_protocol.md` §18 freeze session
**Supersedes:** nothing
**Superseded by:** the frozen `evaluation_protocol.md` itself

This file exists because the gap between "I discovered something" and "I froze the protocol" is where findings get lost, re-litigated, or silently dropped. It carries them forward verbatim.

---

## 1. DSR inputs from the Bailey & López de Prado (2014) paper

The DSR formula (Eq. 2) requires five inputs beyond the selected strategy's SR:

| Input | Definition | Source in robustfolio | Status |
|---|---|---|---|
| `N` | Number of **independent** trials | `experiment_registry_and_preregistration.md` — count of EXPERIMENT entries | Undefined. Only 1 entry exists (DEC-20261015-012, exploratory). |
| `V[{SR_n}]` | Variance of SR across trials | Per-trial SR must be recorded in the registry | Registry template must capture per-trial SR. Not yet verified. |
| `T` | Sample length | Walk-forward OOS length: 168 months in Phase 1 | Defined for Phase 1; freeze must fix for Phase 2. |
| `γ₃` | Skew of selected strategy's returns | `evaluation_protocol.md` §3 secondary metric | Defined. |
| `γ₄` | Raw kurtosis (fisher=False) | §3 secondary metric | Defined. |

**N is not raw trial count.** The paper (Appendix 3, Eq. 9) defines the implied number of independent trials as `N̂ = ρ̂ + (1 − ρ̂) M`, where `ρ̂` is the average pairwise correlation of trial returns. If trials are highly correlated (same universe, same period, same estimator family), raw `M` overstates `N̂` and the DSR test becomes too conservative.

**Decision required at freeze:** Does §12.1 use raw `M` or `N̂`? Paper-faithful answer is `N̂`. Raw `M` is defensible only if the protocol states why it deviates from the source.

**Open item for §12.1:** The registry template must record, per trial:
- method name
- parameter configuration
- OOS return series (net)
- SR (for `V[{SR_n}]`)
- verdict
- date registered
- date executed

If the current template does not capture OOS returns or per-trial SR, it must be amended before Phase 2, not after.

---

## 2. §6.1 clarification — two distinct tests

`evaluation_protocol.md` §6.1 currently reads:

> A robust method is statistically significant if:
> - Deflated Sharpe ratio p-value < 0.05, AND
> - Probabilistic Sharpe ratio > 0.95 against the best baseline.

These are two different tests with two different null hypotheses, and the protocol does not currently state which threshold PSR uses.

- **DSR** = PSR with the rejection threshold set to `SR_0`, the expected maximum Sharpe under N independent trials. `DSR > 0.95` means "95% confident the strategy's true SR exceeds the multiple-testing-adjusted threshold."
- **PSR vs baseline** = PSR with the rejection threshold set to `SR_baseline`. `PSR > 0.95` means "95% confident the strategy's true SR exceeds the baseline's SR."

The protocol must state explicitly that the PSR test in §6.1 uses `SR* = SR_best_baseline`, not `SR* = 0`. Otherwise the two bullets are the same test written twice, or the second bullet is undefined.

**Decision required at freeze:** state the threshold for each test explicitly. Both tests are legitimate; they answer different questions.

---

## 3. §5.2 / §5.3 — walk-forward and cross-validation

**The question:** Does robustfolio use walk-forward only, or walk-forward plus purged k-fold for hyperparameter selection?

**What Phase 1 actually did:** `backtest.py` implements rolling walk-forward. `train = returns.iloc[start - 60 : start]` ends strictly before `test = returns.iloc[start : start + 12]`. There is **no leakage in the walk-forward structure**. But there is **no purging or embargo**, because none is needed in strict walk-forward — there is no overlap between train and test folds.

**What §5.3 currently says:** `evaluation_protocol.md` §5.3 describes purged k-fold with an embargo, citing López de Prado (2018) Ch. 7. This is a different validation structure from walk-forward.

**The gap:** §5.3 has no defined role if §5.2 is the only validation structure. Either:
- **Option A:** §5.3 applies only to Phase 2 hyperparameter selection, if Phase 2 uses it. Walk-forward remains the sole evaluation structure.
- **Option B:** §5.3 is deleted. Walk-forward only. Hyperparameter selection, if any, uses a validation split purged from test.
- **Option C:** §5.3 is retained but explicitly marked `[DEFERRED — not applied to walk-forward]`.

**Decision required at freeze:** pick one. Do not leave §5.3 ambiguous.

**§5.2 window length (36 vs 60):** `[PROPOSED: 36 months]` in the protocol. Phase 1 used 60. `TODO.md` F3 already flagged the mismatch. The freeze must reconcile. Options:
- Freeze at 60 (Phase 1's number), amend `[PROPOSED]`.
- Freeze at 36, treat Phase 1 as a 60-month variant.
- Freeze at both, and declare window length a swept dimension for Phase 2.

There is **no canonical source** for the choice. It is a judgment call. Record the reasoning.

---

## 4. §12.3, §13.1, §5.2 — explicit non-sources

Three `[PROPOSED]` values are grounded in convention, not in a specific cited paper. The freeze should mark these as such, so a future auditor is not surprised.

| Value | Current proposal | Source |
|---|---|---|
| §12.3 FDR level | `q = 0.10` | Convention (BH 1995 uses 0.05 in examples; genomics uses 0.10). Not from DSR. |
| §13.1 block length | 6 months | `T^(1/3)` heuristics for block bootstrap. Not from DSR. Politis & Romano (1994) is the origin for the method, not the block length. |
| §5.2 window / test / step | 36 / 12 / 12 | Judgment. No canonical source. |

The freeze should state that these are default heuristics chosen by the owner, subject to sensitivity testing in Phase 2. Not derived from a paper.

---

## 5. DSR-input observations from Phase 1 diagnostic (2026-10-15)

Diagnostic run: `scripts/dsr_inputs_phase1.py`. Output: `notes/dsr_inputs_phase1.json`.

**Not an experiment. Not registered. Not a confirmatory result. See DEC-20261015-012, -015.**

Summary of the JSON:

| Observation | Value | What it means for §12.1 |
|---|---|---|
| `M` raw trials | 6 | Phase 1 methods. |
| Average pairwise correlation `ρ̂` | 0.648 | High — same universe, same period, three of six use the same covariance estimator. |
| Implied independent trials `N̂` | 2.76 | The paper-faithful count for Phase 1. |
| `V[{SR_n}]` (monthly SR) | 0.00123 | Small — methods cluster around similar SR. |
| Skew range across methods | −0.61 to +0.18 | Sign flips between baseline family and regularized family. |
| Raw kurtosis range | 3.04 to 4.70 | Baselines are fat-tailed; optimizers are not. |

**The three observations that matter:**

1. **M=6 collapses to N̂≈2.76.** The six methods are highly correlated trials. If §12.1 uses raw M, the DSR test is too conservative for Phase 1's structure. If §12.1 uses N̂, the test is calibrated to the paper's definition. **This is the decision §12.1 must make.**

2. **Skew flips sign between families.** Baselines (EW, inverse_vol, sample_mvo) have negative skew; regularized methods (unconstrained_mvo, ledoit_wolf, turnover_penalized) have positive skew. In Eq. 2's denominator, `1 − γ₃·SR + (γ₄−1)/4·SR²`, this penalizes the baselines more than the regularized methods. The test is therefore not neutral across the two families.

3. **Kurtosis differs materially.** EW and inverse_vol have raw kurtosis 4.64 and 4.70. The MVO variants cluster at 3.0–3.8. Same direction of effect as observation 2.

**Firewall — read before the freeze session:**

> **DSR values are not computed in this file. The freeze session will compute them only after N, V[{SR_n}], and the §6.1 dual-test specification are fixed.**
>
> Computing DSR first, seeing the numbers, and then deciding what N should mean is a goalpost-move. The paper defines the inputs. The freeze defines what robustfolio uses. The order is fixed.

The JSON at `notes/dsr_inputs_phase1.json` contains the raw inputs. Do not open it inside `evaluation_protocol.md` and start tuning thresholds against it. Read it once at the start of the freeze session, write the frozen definition of `N` and `V[{SR_n}]` into §12.1, and only then compute DSR.

---

## 6. What this file does not authorize

- No new methods.
- No new experiments.
- No new data sources.
- No source-file changes to `src/`.
- No edits to `evaluation_protocol.md` before the freeze session.
- No DSR calculations before §12.1 is specified.
- No registry entries.

This file is input. The freeze is judgment. The two are separate sessions.

---

**End of freeze inputs.**
