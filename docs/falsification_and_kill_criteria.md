# Falsification and Kill Criteria: robustfolio

**Version:** 1.1
**Status:** Draft — pending owner confirmation of proposed thresholds; freeze before first experiment
**Owner:** Ken Ira Lacson Talingting
**Created:** 2026-10-14
**Last Updated:** 2026-10-15
**Supersedes:** 1.0
**Related:** [`problem_framing.md`](problem_framing.md), [`project_charter.md`](project_charter.md), [`success_metrics_and_evaluation_protocol.md`](success_metrics_and_evaluation_protocol.md), [`experiment_registry_and_preregistration.md`](experiment_registry_and_preregistration.md), [`decision_log.md`](decision_log.md), [`risk_register_and_premortem.md`](risk_register_and_premortem.md)

> **Note on future consolidation.** Per the execution TODO item B1, this document is scheduled to merge into [`success_metrics_and_evaluation_protocol.md`](success_metrics_and_evaluation_protocol.md). When that merge happens, this document will be retired and its content (hypotheses, triggers, sunk-cost firewall, freeze rules) will live in the merged protocol. Until then, this document is the source of truth for falsification tests and kill/pivot triggers.

---

## 0. Purpose of This Document

This document defines, **before any experiment is run**:

1. What claims `robustfolio` makes and how each could be **falsified**.
2. What evidence would trigger a **kill** (stop the project), **pivot** (change the framing), or **stop-and-report** (conclude with a documented negative result).
3. What **time-based** and **evidence-based** triggers force a decision.
4. How to prevent **goalpost-moving**, **sunk-cost continuation**, and **complexity creep as rescue**.

This is the enforcement document. The charter establishes authority and the taxonomy of decisions (Kill, Pivot, Stop-and-report, Continue — see [`project_charter.md`](project_charter.md) §7). The evaluation protocol establishes measurement. This document establishes **the decision rules that fire when measurement returns a verdict**.

**Once frozen, this document may not be modified after seeing experimental results.** Any change requires a decision log entry with a rationale that a skeptical external reviewer would accept.

---

## 1. Falsification Philosophy

The project is falsificationist, not confirmationist. This has three operational consequences:

1. **Every claim must have a test that could prove it wrong.** If no such test exists, the claim is not part of the project's scientific content and may not be reported as a finding.
2. **Failure to falsify is not proof.** A method that survives its tests is "not yet falsified," not "correct." Language in reporting must reflect this.
3. **Negative results are first-class outputs.** A falsified hypothesis is a successful experiment. A project that ends with a clean negative result has succeeded by its own definition (see [`project_charter.md`](project_charter.md) §1).

Every hypothesis below has the form: *"Under protocol P, method M beats baseline B on metric m by at least δ."* The corresponding falsification is: *"Under protocol P, M does not beat B on m by δ, after adjustment."*

---

## 2. Hypotheses and Falsification Tests

Hypotheses are grouped by family. Each family shares a multiple-testing correction (see [`success_metrics_and_evaluation_protocol.md`](success_metrics_and_evaluation_protocol.md) §7).

### Family H1 — Estimation error is the binding constraint

| ID | Hypothesis | Falsification test | Kill/pivot on falsification |
|----|-----------|-------------------|------------------------------|
| H1.1 | Sample MVO produces extreme weights relative to 1/N | Max absolute weight > `[PROPOSED: 0.40]` in ≥ 1 fold | If not, the framing premise is weak; document and re-evaluate problem |
| H1.2 | Sample MVO has higher turnover than 1/N | Annualized turnover ratio > `[PROPOSED: 2.0]` | If not, turnover is not the problem; revisit |
| H1.3 | Estimation error, not optimization, drives instability | Shrinkage covariance reduces weight dispersion vs sample covariance | If not, revisit root-cause model in [`problem_framing.md`](problem_framing.md) §5 |

**Family kill trigger:** If H1.1 and H1.2 both fail on the primary dataset, the problem framing is falsified. Pivot or stop before Phase 2.

### Family H2 — Robust methods improve net performance

| ID | Hypothesis | Falsification test | Kill/pivot on falsification |
|----|-----------|-------------------|------------------------------|
| H2.1 | Shrinkage covariance beats sample covariance on net Sharpe | Evaluation protocol §6 success criteria met | If not, drop shrinkage from the claim set |
| H2.2 | Bayesian expected returns beat historical mean on net Sharpe | Same criteria | If not, drop Bayesian returns |
| H2.3 | Turnover penalty improves net Sharpe vs unpenalized MVO | Same criteria | If not, drop turnover penalty |
| H2.4 | At least one robust method beats the best baseline on net Sharpe | Same criteria | **Project-level trigger — see §4** |

**Family kill trigger:** If H2.1–H2.3 all fail, the project's method claims are falsified. Pivot to diagnostic tool or stop-and-report.

### Family H3 — Improvements are robust, not artifacts

| ID | Hypothesis | Falsification test | Kill/pivot on falsification |
|----|-----------|-------------------|------------------------------|
| H3.1 | Improvement survives at 3+ cost levels | Evaluation protocol §6.3 | If not, downgrade claim to "cost-level-specific" |
| H3.2 | Improvement survives in 60%+ of walk-forward folds | Same | If not, claim is not robust; report as fragile |
| H3.3 | Improvement survives multiple-testing adjustment | Deflated Sharpe p-value | If not, claim is not statistically defensible; report as exploratory |

**Family kill trigger:** If H3.3 fails for all methods, the project cannot claim method superiority. Pivot to diagnostic benchmark.

### Family H4 — The gap hypothesis is real

| ID | Hypothesis | Falsification test | Kill/pivot on falsification |
|----|-----------|-------------------|------------------------------|
| H4.1 | No open-source tool reproduces this exact comparison | R1 tool scan identifies no equivalent | If equivalent exists, pivot to replication or extension |
| H4.2 | Published work does not already answer the question | R1 literature scan | If answered, pivot to replication or extension |

**Family kill trigger:** If H4.1 or H4.2 fails, the gap hypothesis is falsified. Update [`problem_framing.md`](problem_framing.md) §4.1 and pivot.

---

## 3. Kill / Pivot / Stop Definitions (moved)

The taxonomy of decisions — **Kill**, **Pivot**, **Stop-and-report**, **Continue** — and their authority are defined authoritatively in:

> [`project_charter.md`](project_charter.md) §7

They are not duplicated here. The charter's hard rules (no phase exceeds its time-box without a decision log entry; primary-objective failure forces Stop-and-report rather than added complexity; new methods require pre-registered hypotheses; kill requires a decision log entry) are enforced by the triggers in §4–§7 of this document.

This stub is retained to preserve cross-references.

---

## 4. Project-Level Kill Triggers

These are the conditions under which the project as a whole must decide to kill, pivot, or stop-and-report. Each is a **hard trigger**: the decision cannot be deferred.

### K1 — Primary objective falsified

**Trigger:** After Phase 3 evaluation, no robust method satisfies [`success_metrics_and_evaluation_protocol.md`](success_metrics_and_evaluation_protocol.md) §6.4 (statistical significance + economic materiality + robustness).

**Decision:** Stop-and-report. The project's primary hypothesis is falsified.

**Not permitted:** Adding new methods, relaxing thresholds, or extending the evaluation to find a positive result.

**Rationale:** The charter §7 Hard Rule 2 already says this. This document makes it enforceable.

### K2 — Problem framing falsified

**Trigger:** H1.1 and H1.2 both fail on the primary dataset, before Phase 2.

**Decision:** Kill or pivot to a diagnostic-benchmark framing.

**Not permitted:** Proceeding to Phase 2 on the assumption that "the problem must be real."

### K3 — Gap hypothesis falsified

**Trigger:** R1 identifies an existing tool or paper that reproduces the planned comparison with equivalent rigor.

**Decision:** Kill or pivot to replication or extension.

**Not permitted:** Proceeding to build a less rigorous version of something that exists.

### K4 — Time budget exhausted

**Trigger:** Total time budget from [`project_charter.md`](project_charter.md) §9 is reached, regardless of where the project is.

**Decision:** Stop-and-report with whatever is complete. If results are not yet available, report as "incomplete — no conclusion."

**Not permitted:** Silent time-box extension. Any extension requires a charter amendment with decision log entry.

### K5 — Phase time-box exhausted without gate pass

**Trigger:** Any phase exceeds its time-box from [`project_charter.md`](project_charter.md) §9 without passing its gate.

**Decision:** Kill the phase or pivot the phase goal. Do not roll over into the next phase.

**Not permitted:** Continuing into the next phase "in parallel" or "just to keep momentum."

### K6 — Data or cost contract broken

**Trigger:** Any experiment in Phase 1 or later reveals a violation of [`data_contract_and_point_in_time_policy.md`](data_contract_and_point_in_time_policy.md) or [`cost_model_and_frictions.md`](cost_model_and_frictions.md) that cannot be corrected without invalidating prior results.

**Decision:** Halt evaluation. Fix the contract. Re-run affected experiments or kill.

**Not permitted:** Reporting results from invalidated experiments as findings.

### K7 — Cumulative invalidation

**Trigger:** `[PROPOSED: 3]` or more experiments in the same family are invalidated for protocol reasons.

**Decision:** Kill the family. If the invalidations span families, kill the project.

**Rationale:** Repeated invalidation signals the protocol itself is not workable, not that the methods are failing.

---

## 5. Pivot Criteria

A pivot is permitted only under the following conditions. Every pivot requires a decision log entry with a version bump.

| Pivot | Trigger | New framing | Requires |
|-------|---------|-------------|----------|
| Diagnostic benchmark | K1 or H3.3 fails for all methods | Deliver the framework and negative result as the contribution | Update `problem_framing.md`, `project_charter.md` |
| Replication study | K3 | Reproduce an existing result to validate the framework | Update scope and evaluation protocol |
| Narrower method scope | H2.x fails for a specific method | Drop that method; keep the family | Update evaluation protocol baseline list |
| Narrower universe | H1.x fails on one asset class but holds on another | Restrict to the asset class where the effect is real | Update data contract |
| Shorter horizon | Long-horizon results are unstable | Restrict claim to monthly rebalancing only | Update evaluation protocol |

**Forbidden pivots:**

- "Add more data" to rescue a failed result.
- "Try a different metric" to find significance.
- "Extend the test window" to accumulate more evidence of the same period.
- "Add another method" without a pre-registered hypothesis and a fresh experiment entry.

---

## 6. Stop-and-Report Criteria

Stop-and-report is the correct decision when:

1. K1 fires (primary objective falsified), OR
2. The project reaches its total time budget without a positive result, OR
3. The owner elects to stop for any reason (per [`project_charter.md`](project_charter.md) §7 Hard Rule 4), OR
4. Two or more pivot attempts have failed.

**Stop-and-report deliverable:**

- A written conclusion: positive, negative, or mixed, with explicit language about what was and was not tested.
- All Tier 0 documentation in its final state.
- The full experiment registry, including failed and invalidated experiments.
- The decision log documenting the stop.
- Reproducible code and data acquisition instructions.

**Stop-and-report is not failure.** It is the correct outcome when the evidence does not support the claim. It is reported with the same care as a positive result.

---

## 7. Sunk Cost Firewall

The most likely failure mode of this project is not a bad method. It is **continuing past the evidence out of sunk cost**.

Rules to prevent it:

1. **Time budgets are hard stops.** Once a phase time-box is exhausted, no work in that phase continues. A decision log entry is required to move on.
2. **No work in a new phase while a gate is unresolved.** Parallel progress is scope creep.
3. **Effort already spent is never a reason to continue.** Only evidence of future value is.
4. **A kill decision is free.** The owner can kill at any time. The project's identity does not depend on finishing.
5. **"Almost there" is not evidence.** If the last experiment failed the success criteria, the next experiment needs a fresh pre-registered hypothesis.

**Anti-pattern to flag:** The owner saying "let me just try one more thing" after a failed gate. This is the sunk-cost failure mode. The reasoning partner must flag it.

---

## 8. Decision Process

When a trigger fires, follow this sequence:

1. **Recognize.** The trigger is identified by the owner or the reasoning partner.
2. **Log the trigger.** Add an entry to `decision_log.md` with: date, trigger, evidence, options considered.
3. **Evaluate options.** Kill, pivot, stop-and-report, or continue — with explicit expected value reasoning.
4. **Decide.** The owner decides. No decision is a decision to continue, which must be logged.
5. **Act.** Update affected documents. Bump versions. Notify informed parties.
6. **Update priors.** Record what was learned in `decision_log.md` and, if relevant, in [`problem_framing.md`](problem_framing.md) or the evaluation protocol.

**Time-box for decisions:** `[PROPOSED: 1 week]` from trigger recognition to decision. Beyond this, the project is drifting.

---

## 9. When This Document Conflicts With Others

| Conflict | Resolution |
|----------|------------|
| Charter vs this document | The charter owns the decision *taxonomy* (§7) and *authority* (§8). This document owns the *triggers* that fire on those categories. If they conflict on a trigger, this document wins until amended. If they conflict on a category, the charter wins. |
| Evaluation protocol vs this document | The evaluation protocol defines measurement; this document defines decisions on that measurement. They must agree on thresholds. |
| Problem framing vs this document | This document may falsify the problem framing. When it does, [`problem_framing.md`](problem_framing.md) must be updated. |
| Owner intuition vs this document | This document wins until amended via decision log. |
| Scope vs this document | [`scope_and_non_goals.md`](scope_and_non_goals.md) owns scope. This document's pivot criteria (§5) that change scope (e.g., narrower universe) require a scope amendment, not just a decision log entry. |

---

## 10. Model Tags Applied

- **[Inversion]** — Defined what would falsify every claim before running any experiment.
- **[Experimental]** — Hypothesis-test pairs; family-wise multiple-testing control; invalidation rules.
- **[Bayesian]** — Thresholds framed as evidence updates; priors revisited after each trigger.
- **[Systems]** — Trigger-response cadence; escalation path; version control.
- **[Expected Value]** — Sunk-cost firewall; opportunity cost acknowledged; kill is free.
- **[Learning Loop]** — Every trigger logged; priors updated; pivot history preserved.

---

## 11. Owner Action Checklist Before Freezing

Before setting Status to `Frozen`, confirm or replace every `[PROPOSED]` value:

- [ ] Section 2, H1.1: extreme-weight threshold
- [ ] Section 2, H1.2: turnover ratio threshold
- [ ] Section 4, K7: cumulative invalidation count
- [ ] Section 8: decision time-box

Also confirm:

- [ ] Section 4 triggers are consistent with your charter time-boxes ([`project_charter.md`](project_charter.md) §9)
- [ ] Section 5 forbidden pivots are acceptable to you
- [ ] Section 7 sunk cost firewall rules are acceptable
- [ ] The decision authority in Section 8 matches [`project_charter.md`](project_charter.md) §8
- [ ] Section 9 conflict resolution is consistent with the charter's own conflict rule

Once confirmed, bump to Version 1.2, set Status to `Frozen`, and add a revision history row.

---

## 12. Revision History

| Date | Version | Change | Author |
|------|---------|--------|--------|
| 2026-10-14 | 1.0 | Initial falsification and kill criteria | Ken Ira Lacson Talingting |
| 2026-10-15 | 1.1 | Replaced §3 (Kill/Pivot/Stop Definitions) with pointer to charter §7 (A5); changed "gap claim" to "gap hypothesis" in §2 H4 and §4 K3 for consistency with problem_framing v2.1; updated §9 conflict table to clarify taxonomy vs trigger ownership; added note on future consolidation into evaluation protocol (B1); updated cross-references to full paths | Ken Ira Lacson Talingting |

---

*This document exists to make stopping easy and continuing honest. If it is not enforced, the project is not falsificationist.*
