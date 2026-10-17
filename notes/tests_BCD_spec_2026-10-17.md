# Tests B / C / D — Specification — 2026-10-17

**Owner:** Ken Ira Lacson Talingting
**Purpose:** Define the three diagnostics that `problem_framing.md` §14 and DEC-20261015-012 reference but never specify (DEC-20261017-019 finding F6). Test B isolates the **cap artifact**, Test C the **window artifact**, and Test D is the **confirmatory** evaluation.
**Not a Tier 0 document. Not a contract.** These are pre-registration inputs: the actual registrations are appended to `decision_log.md` Appendix A *after* `evaluation_protocol.md` is frozen.
**Logged by:** DEC-20261017-020.
**Companion input:** [`freeze_worksheet_2026-10-17.md`](freeze_worksheet_2026-10-17.md).

**Precondition:** none of these tests may run before (a) `evaluation_protocol.md` is `Frozen`, (b) the §5.4.8 leakage suite passes, and (c) the test is registered in Appendix A. Running any of them earlier repeats the DEC-20261015-012 error.

---

## 0. The question they answer

Phase 1 (exploratory) observed that Ledoit-Wolf shrinkage and turnover-penalized MVO underperformed even unpenalized sample MVO on net Sharpe. Its open question:

> Is that underperformance a **box-cap artifact** (Test B), a **window-length artifact** (Test C), or a **real effect** (Test D)?

DEC-20261017-019 F1 sharpens the question: Phase 1's baselines were not subject to the same constraints as the optimizers, so the comparison itself was not like-for-like. Tests B and C are therefore *characterization* runs. Test D is the *decision*.

---

## 1. Common configuration

| Parameter | Value | Source |
|-----------|-------|--------|
| Universe | the frozen MVP universe (15 ETFs) | freeze worksheet §3 |
| Period | full history available from the point-in-time snapshot | §5.4 |
| Data | point-in-time adjusted, from the frozen raw+actions reconstruction | §5.4.1 |
| Rebalance | monthly | §3.3 |
| Walk-forward | rolling estimation window; 12-month test; 12-month step | §5.2 |
| Cost levels | the five §5.5.3 levels (0/5/10/20/50 bps), headline at 10 bps | §5.5.3 |
| Methods (all tests) | B1 (1/N), B2 (risk parity), B3 (sample MVO), B4 (min variance), B5 (penalized MVO, λ=κ) | §4.2 |
| Robust methods (Test D only) | shrinkage-covariance MVO, Ledoit-Wolf, and the §4.2 robust candidates | §4.2 / §7 H2 |
| Constraint rule | `w_max` applied **uniformly to every method** | freeze worksheet §2 (fixes F1) |
| Random seeds | fixed and recorded per §12.4 | §12.4 |

**All three tests use identical data, period, cost model, and constraint handling.** Any deviation invalidates the comparison (§4.6).

---

## 2. Test B — Cap sensitivity (artifact test)

**Hypothesis (H3-family diagnostic):** the Phase 1 underperformance of shrinkage/penalty methods is an artifact of the cap being applied only to the optimizers.

**Design.** Sweep `w_max ∈ {0.20, 0.30, 0.40, 1.00}` (1.00 = uncapped). Everything else fixed at the common configuration (`test window 12`, `step 12`, window 60, κ = 10 bps, λ = κ). Apply the cap **uniformly** in every arm, including B1 and B2.

**Output.** For each cap value, the net-Sharpe ranking of all methods, and specifically:
- `ΔB = SR_net(penalty/shrinkage method) − SR_net(B3)` at each cap;
- `Δbase = SR_net(B1) − SR_net(best optimizer)` at each cap.

**Decision rule.**
- If `ΔB < 0` for every cap **and** `Δbase` widens monotonically as the cap loosens → the Phase 1 underperformance is **not** a cap artifact; escalate to Test C.
- If `ΔB < 0` **only** at loose/no cap and reverses at tight caps → the underperformance is **a cap artifact**; the framing's remedy hypothesis is not falsified by Phase 1.
- If `ΔB` changes sign with cap in a non-monotone way → the result is **cap-fragile**; report as unresolved and do not proceed to a confirmatory claim without a new hypothesis.

**Family:** X (exploratory). **Trials:** 4 arms, all reported. Does not count toward the H2/H3 denominator.

---

## 3. Test C — Window sensitivity (artifact test)

**Hypothesis:** the Phase 1 underperformance is specific to the 60-month estimation window.

**Design.** Sweep the rolling estimation window `∈ {36, 60, 120}` months. Cap fixed at the **frozen** value, window-independent. Everything else fixed.

**Output.** Net-Sharpe ranking and `ΔB` per window, plus a dispersion diagnostic (condition number of the sample covariance at each window).

**Decision rule.**
- If the underperformance persists at all three windows → **not** a window artifact.
- If it appears only at 60 months → **window artifact**; the freeze worksheet's 60-month recommendation is called into question and the window becomes a swept dimension for a re-frozen protocol.
- If results are non-monotone in window → **window-fragile**; report as unresolved.

**Family:** X (exploratory). **Trials:** 3 arms, all reported.

---

## 4. Test D — Confirmatory evaluation

**Hypothesis (H2.4):** under the frozen protocol, at least one robust method beats the best baseline on net Sharpe after costs and multiple-testing adjustment, per §6.4.

**Design.** Run the full frozen protocol once, at the frozen configuration (window, cap, λ fixed by the freeze — **not** whichever arm won Tests B/C; see §5). Report B1–B5, the robust methods, at all five cost levels, with DSR, PSR, block-bootstrap CIs, CVaR, turnover, drawdown, and cost drag.

**Decision rule (§6.4).** A method succeeds only if all four hold: statistical significance (§6.1), economic materiality (§6.2), robustness (§6.3), and no PIT/cost violation. If **no** method satisfies §6.4, **K1 fires: stop-and-report** — the primary objective is falsified. No method may be added, and no threshold relaxed, to rescue the result (§8.6 K1, §8.1 Hard Rule 2).

**Family:** H2 / H3. **Counts** toward the multiple-testing denominator.

---

## 5. Firewall — the selection trap

Tests B and C each sweep parameters. The failure mode this section prevents is running the sweeps, noticing that configuration *X* produces a positive result, and then reporting Test D at configuration *X*.

**Rules:**

1. **Test D runs only at the configuration frozen by the freeze session.** Its window, cap, and λ are read from the frozen `evaluation_protocol.md`, not from Tests B/C.
2. **If a B/C arm reveals a configuration where a robust method meets §6.4**, that configuration is **not** adopted. It becomes the hypothesis for a **new, separately pre-registered** experiment at that configuration.
3. When that new experiment is registered, **the B/C arms count as prior trials** in its multiple-testing denominator. Sweeping 4 caps and 3 windows to find one that works, then reporting it, is 7 (or more) trials, not 1.
4. **All arms are reported**, including those where the framing's prediction fails. Selective reporting is the §12.10 exploratory failure mode.

**Rationale** `[Goodhart's Law]` `[Inversion]`: the sweep is a search over configurations. If the search result is reported as a confirmatory finding, the metric has been gamed through the search itself. Rule 1 makes the frozen configuration independent of the search; rule 3 makes the search honest about its cost.

---

## 6. Worked example of the firewall

Suppose Test B finds that at `w_max = 0.40` the turnover-penalized method beats B3, while at 0.30 it does not. The correct output is:

> "At the frozen cap of 0.30, the penalized method does not beat B3 (ΔB = −0.04). Under a looser cap (0.40), it does (ΔB = +0.02). The difference is attributable to the constraint set, not to the penalty."

It is **not** "the penalized method beats MVO." If the `0.40` arm is to be pursued, it requires a new registration at `w_max = 0.40` with the Test B arms entered as prior trials.

---

## 7. Dependencies on the freeze

- Test B depends on the §4.3 `w_max` recommendation and resolves F1.
- Test C depends on the §5.2 window recommendation.
- Test D cannot be registered until §12.1 (N), §6.1 (DSR/PSR thresholds), and §5.5.5 (rf convention) are frozen.
- Tests B and C cannot run until §5.4 (data contract) is frozen and the §5.4.8 leakage suite passes — they measure net Sharpe, which is only meaningful on point-in-time data.

---

## 8. What this file does not authorize

- No runs before the freeze.
- No new methods, data sources, or cost levels beyond those listed.
- No use of Test B or C to select Test D's configuration.
- No registry entries (these are the specs the entries will reference).

This file defines the tests. The freeze decides the configuration. The registry records the runs. The three are separate.

---

**End of Tests B/C/D specification.**
