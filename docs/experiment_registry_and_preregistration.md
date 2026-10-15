# Experiment Registry and Preregistration: robustfolio

**Version:** 1.0  
**Status:** Draft — pending owner confirmation of proposed defaults; freeze before first experiment  
**Owner:** Ken Ira Lacson Talingting  
**Created:** 2026-10-14  
**Last Updated:** 2026-10-14  
**Supersedes:** None  
**Related:** [`problem_framing.md`](problem_framing.md), [`project_charter.md`](project_charter.md), [`evaluation_protocol.md`](evaluation_protocol.md), [`data_contract_and_point_in_time_policy.md`](data_contract_and_point_in_time_policy.md), [`cost_model_and_frictions.md`](cost_model_and_frictions.md), [`benchmark_and_baseline_spec.md`](benchmark_and_baseline_spec.md), [`decision_log.md`](decision_log.md)

---

## 0. Purpose of This Document

This document defines:

1. What counts as an experiment.
2. What must be recorded **before** an experiment runs.
3. How the registry is structured, versioned, and frozen.
4. How the multiple-testing denominator is computed.
5. How results are recorded, interpreted, and linked to decisions.
6. How amendments, re-runs, and invalidations are handled.
7. How exploratory work is separated from confirmatory work.

It is the **contract** between intention and execution. An experiment that is not pre-registered is not eligible to support a success claim (see `evaluation_protocol.md` §1, principle 2).

**Once frozen, the format and rules of this document may not be modified after seeing experimental results.** Any change requires a decision log entry and a version bump.

---

## 1. Preregistration Philosophy

Three principles govern all experiment registration.

1. **Lock before you look.** Every hypothesis, parameter, metric, and decision rule is recorded before the experiment runs. If it is not written down beforehand, it is exploratory.
2. **The denominator is honest.** The number of registered trials is the multiple-testing denominator. Hiding trials is scientific misconduct, including self-deception.
3. **Negative results are entries too.** A failed experiment is recorded with the same rigor as a successful one. It contributes to the denominator and to the learning loop.

A result obtained from an unregistered run is a hypothesis, not a finding. It may motivate a new pre-registered experiment but cannot be reported as evidence.

---

## 2. What Counts as an Experiment

An **experiment** is any run that produces a metric on which a decision or claim will be based.

This includes:

- Any comparison of a robust method against any baseline.
- Any sensitivity analysis whose result will be reported.
- Any hyperparameter selection whose outcome affects a reported metric.
- Any re-run of a prior experiment with any change in data, code, or parameters.

An experiment does **not** include:

- Unit tests, integration tests, or leakage tests (these are infrastructure, not findings).
- Exploratory data analysis, unless its output will be reported as a result.
- Debugging runs whose outputs are discarded.
- Sanity checks that do not produce a reported metric.

**Rule:** If you will report the number, it is an experiment. If you would not report it, do not call it one.

---

## 3. Registry Structure

> **Note:** The following are **proposed conservative defaults**. Confirm or replace before freezing.

### 3.1 Storage format

`[PROPOSED]`: Two files.

- `docs/experiment_registry_and_preregistration.md` — this document (rules and index).
- `experiments/registry.md` — the append-only log of registrations, results, and decisions.

Alternative: one file with two sections. Owner to confirm.

### 3.2 Registration ID format

`[PROPOSED]`: `EXP-<family>-<YYYYMMDD>-<nnn>`

Example: `EXP-H2-20261020-001` = first experiment in family H2, registered on 2026-10-20.

Family codes:

- `H1` — Estimation error is the binding constraint.
- `H2` — Robust methods improve net performance.
- `H3` — Improvements are robust, not artifacts.
- `H4` — The gap claim is real.
- `X` — Exploratory (not eligible for success claims).

### 3.3 Immutability

Once a registration is created:

- The **pre-registration section** is frozen and may not be edited.
- The **results section** is appended after execution.
- The **conclusion section** is appended after analysis.
- The **decision section** is appended after the decision is made.

Amendments are separate entries that reference the original. The original is never modified.

### 3.4 Append-only rule

The registry is append-only. No entry is deleted. Invalidated experiments are marked as `INVALIDATED` with a reference to the invalidation reason.

---

## 4. Preregistration Template

Every experiment registration must include all fields below before execution.

```markdown
### EXP-<family>-<YYYYMMDD>-<nnn>

**Status:** REGISTERED | RUNNING | COMPLETED | INVALIDATED | ARCHIVED  
**Registered:** YYYY-MM-DD  
**Family:** H1 | H2 | H3 | H4 | X  
**Related hypotheses:** (from falsification doc)  
**Related decision triggers:** (from falsification doc)  

#### 1. Hypothesis

- **Statement:** (one sentence, falsifiable)
- **Direction:** (e.g., "Method M's net Sharpe > baseline B's net Sharpe")
- **Effect size of interest:** (minimum economically meaningful difference)
- **Prior:** (prior probability that the hypothesis is true, with justification)

#### 2. Methods compared

- **Baselines:** (list of baseline IDs from `benchmark_and_baseline_spec.md`)
- **Candidate methods:** (list of method IDs from `model_and_method_spec.md`)

#### 3. Parameters

- **Universe:** (reference to data contract §3)
- **Snapshot ID:** (SHA-256 of snapshot bundle)
- **Estimation window:** 
- **Rebalance frequency:** 
- **Cost levels:** (list of κ values)
- **Constraints:** (w_max, long-only, fully invested)
- **Method-specific parameters:** (γ, λ, shrinkage intensity, etc.)
- **Random seeds:** (if any stochastic component)

#### 4. Evaluation protocol

- **Protocol version:** (reference to success metrics doc version)
- **Primary metric:** (as defined in protocol §2)
- **Secondary metrics:** (as defined in protocol §3)
- **Statistical test:** (deflated Sharpe, probabilistic Sharpe, or both)
- **Confidence level:** 
- **Multiple-testing family size at registration:** (count of prior trials in this family + 1)

#### 5. Decision rule

- **Success condition:** (what result would confirm the hypothesis)
- **Failure condition:** (what result would falsify the hypothesis)
- **Ambiguous condition:** (if any, what would count as inconclusive)
- **Action on success:** 
- **Action on failure:** 
- **Action on ambiguity:** 

#### 6. Cost and time estimate

- **Compute budget estimate:** 
- **Wall-clock estimate:** 
- **Data volume:** 

#### 7. What would invalidate this experiment

- (List of conditions from data contract §11, cost model §8, and falsification doc §4)

#### 8. Pre-registration signature

- **Author:** 
- **Date:** 
- **Git commit at registration:** 
- **Registry version at registration:** 
```

The `Status` field is the only field that may change in the pre-registration section, and only to reflect progression, never to revise content.

---

## 5. Results Template

Appended only after the experiment completes. Never edited.

```markdown
#### 9. Results

**Run date:** YYYY-MM-DD  
**Git commit at run:**   
**Snapshot ID used:**   
**Wall-clock time:**   
**Compute cost:**   

**Primary metric:**

| Method | Net Sharpe (10 bps) | 90% CI | Deflated Sharpe p-value |
|--------|---------------------|--------|--------------------------|
| ...    | ...                 | ...    | ...                      |

**Secondary metrics:**

| Method | Turnover | Max DD | CVaR 95% | Cost drag | Calibration |
|--------|----------|--------|----------|-----------|-------------|
| ...    | ...      | ...    | ...      | ...       | ...         |

**Sensitivity across cost levels:**

| Method | 0 bps | 5 bps | 10 bps | 20 bps | 50 bps |
|--------|-------|-------|--------|--------|--------|
| ...    | ...   | ...   | ...    | ...    | ...    |

**Walk-forward fold results:**

| Fold | Period | Method | Net Sharpe | Turnover |
|------|--------|--------|-----------|----------|
| ...  | ...    | ...    | ...       | ...      |

**Calibration checks:**

- [ ] Time-travel test passed
- [ ] Survivorship test passed
- [ ] Adjusted-price test passed
- [ ] Universe reconstruction test passed
- [ ] Determinism test passed

**Anomalies:** (any unexpected behavior, bugs found, deviations)
```

---

## 6. Conclusion Template

Appended after analysis. Never edited.

```markdown
#### 10. Conclusion

**Verdict:** CONFIRMED | FALSIFIED | INCONCLUSIVE | INVALIDATED  
**Effect size observed:**   
**Effect size vs. pre-registered interest threshold:**   
**Statistical significance:**   
**Economic materiality:** (per protocol §6.2)  
**Robustness:** (per protocol §6.3)  

**Interpretation:** (2–4 sentences, no hedging beyond what the evidence supports)

**Threats to validity:** (list)

**Links to update:**
- [ ] `evaluation_protocol.md` §7 (hypothesis status)
- [ ] `decision_log.md` (decision entry)
- [ ] `risk_register_and_premortem.md` (if new failure mode observed)
- [ ] `problem_framing.md` (if framing affected)
```

---

## 7. Decision Template

Appended after the decision is made. Never edited.

```markdown
#### 11. Decision

**Decision:** CONTINUE | PIVOT | KILL | STOP-AND-REPORT  
**Authority:** Owner  
**Date:** YYYY-MM-DD  
**Rationale:** (2–4 sentences)  
**Next experiment:** (EXP-ID, or "none")  
**Decision log entry:** (link)  
```

---

## 8. Multiple-Testing Denominator

The multiple-testing denominator is the number of **registered confirmatory trials** in a family up to and including the current trial.

### 8.1 Rules

1. Every registration in family H1–H4 counts toward the denominator.
2. Exploratory registrations (family X) do not count, but they also cannot support success claims.
3. Invalidated experiments still count. Invalidating an experiment does not erase it from history.
4. Amendments count as new trials if they change any parameter, metric, or decision rule.
5. Re-runs with identical parameters and code count as one trial.

### 8.2 Reporting

Every result must report:

- The current family size \( N \).
- The deflated Sharpe adjustment applied.
- The FDR-adjusted p-value, if the FDR rule from protocol §7.3 is applied.

### 8.3 Freezing the denominator

Once Phase 3 begins (evaluation), the denominator for the H2 and H3 families is frozen. Additional trials in these families are not permitted without a decision log entry justifying why they do not constitute goalpost-moving.

---

## 9. Amendments and Re-runs

### 9.1 Amendment

An **amendment** changes a registered experiment before it runs, or adds a new trial after a prior one completed.

Amendments require:

- A new registration ID.
- A reference to the original.
- A one-sentence justification.
- A pre-registration of any changed fields.
- A decision log entry if the amendment is motivated by a prior result.

**Amendments made after seeing the result of the original are new trials, not clarifications.**

### 9.2 Re-run

A **re-run** re-executes the same experiment with the same parameters and code. Re-runs:

- Do not create a new registry entry.
- Record the new run date, environment, and outcome in the existing entry.
- Count as one trial for multiple-testing purposes.

### 9.3 What triggers a re-run vs an amendment

| Change | Re-run | Amendment |
|--------|--------|-----------|
| Hardware | ✅ | |
| Compute time | ✅ | |
| Git commit (non-parameter) | ✅ | |
| Random seed | | ✅ |
| Any parameter | | ✅ |
| Metric definition | | ✅ |
| Decision rule | | ✅ |
| Data snapshot | | ✅ |
| Baseline set | | ✅ |

---

## 10. Exploratory Work

### 10.1 Definition

Exploratory work is any analysis whose result is not pre-registered.

### 10.2 Rules

1. Exploratory work must be labeled `EXPLORATORY` in every artifact.
2. Exploratory results may motivate new pre-registered experiments.
3. Exploratory results may not support success claims.
4. Exploratory results must be reported in a separate section of any publication.
5. The existence of exploratory work must be disclosed when reporting confirmatory results.

### 10.3 Why this matters

The failure mode being prevented: running many unregistered variants, finding one that "works," and then pre-registering it retroactively. This is p-hacking with extra steps. Labeling and disclosure is the defense.

---

## 11. Registry Hygiene

### 11.1 Append-only log

- The registry is a running log. New entries are appended, never inserted.
- Every entry has a stable ID. IDs are never reused.
- Cross-references use IDs, not positions.

### 11.2 Versioning

- The registry format (this document) is versioned.
- The registry content (the log) is not versioned; it accumulates.
- Git history provides the audit trail.

### 11.3 Backups

- The registry lives in the repository and is committed with code.
- Snapshots are referenced by hash from the registry, not embedded in it.

### 11.4 Review cadence

- Before each phase gate, the registry is reviewed for completeness.
- Missing entries are a gate failure, not a clerical issue.

---

## 12. What Invalidates an Experiment

An experiment's registration is invalidated if any of the following occurred:

- The experiment ran before the registration was complete.
- Fields in the pre-registration section were edited after execution.
- The results section reports a metric not in the pre-registration.
- The decision rule was changed after seeing results.
- A family-size count in the registration was wrong and the error cannot be corrected without invalidating the multiple-testing adjustment.
- The experiment was not registered at all but is reported as a finding.
- A trial was suppressed from the denominator.

Invalidation does not delete the entry. It marks it `INVALIDATED` with a reason and a reference to the relevant invalidation rule.

---

## 13. Model Tags Applied

- **[Experimental]** — Pre-registration, frozen parameters, append-only log, invalidation rules.
- **[Inversion]** — Defined what invalidates an experiment before defining success.
- **[Bayesian]** — Priors, effect sizes of interest, and denominator discipline.
- **[Systems]** — Registry structure, multiple-testing families, phase-gate review.
- **[Learning Loop]** — Results, conclusions, and decisions all feed back into the registry.
- **[Information Theory]** — Compressed to fields, rules, and checklists; no filler.

---

## 14. Owner Action Checklist Before Freezing

Before setting Status to `Frozen`, confirm or replace every `[PROPOSED]` value:

- [ ] Section 3.1: confirm storage format (two files vs one)
- [ ] Section 3.2: confirm ID format and family codes
- [ ] Section 4: confirm pre-registration fields are complete and usable
- [ ] Section 8: confirm multiple-testing denominator rules
- [ ] Section 9.3: confirm re-run vs amendment triggers
- [ ] Section 10: confirm exploratory work rules

Also confirm:

- [ ] You accept that every reported metric requires a registration.
- [ ] You accept that the registry is append-only.
- [ ] You accept that exploratory results cannot support success claims.
- [ ] You accept that invalidated experiments remain in the log.
- [ ] You accept the phase-gate review of registry completeness.

Once confirmed, bump to Version 1.1, set Status to `Frozen`, and add a revision history row.

---

## 15. Revision History

| Date | Version | Change | Author |
|------|---------|--------|--------|
| 2026-10-14 | 1.0 | Initial experiment registry and preregistration document | Ken Ira Lacson Talingting |
| 2026-10-15 | 1.1 | Updated cross-references after `success_metrics_and_evaluation_protocol.md` and `falsification_and_kill_criteria.md` were merged into `evaluation_protocol.md`. No content changed. | Ken Ira Lacson Talingting |

---

*This document exists to make pre-registration enforceable. An unregistered result is not a finding. A registered result that was edited is not a finding. The registry is the audit trail of what was actually tested.*
