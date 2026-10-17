# Decision Log — robustfolio

**Project:** `robustfolio`
**Owner:** Ken Ira Lacson Talingting
**Created:** 2026-10-14
**Last Updated:** 2026-10-17
**Purpose:** Immutable record of every governance, experiment, and pivot decision in the project. Entries are append-only. Supersession is by a new entry, not by editing an old one.

---

## Format

Each entry uses the following fields:

- **Date** — calendar date of the decision
- **Type** — GOVERNANCE / EXPERIMENT / PIVOT / KILL / STOP
- **Status** — ACTIVE / SUPERSEDED / REVERTED
- **Authority** — Owner (sole authority on this project)
- **Related docs** — files that this decision constrains or is constrained by
- **Related risks** — R-IDs from `risk_register_and_premortem.md`
- **Context** — what was happening and why a decision was needed
- **Decision** — what was decided
- **Alternatives considered** — what was rejected and why
- **Rationale** — mental models applied and reasoning
- **Reversibility** — Soft / Hard / Irreversible
- **Revisit trigger** — conditions under which this decision is reopened
- **Expected value assessment** — probabilistic view, where applicable
- **Pre-mortem** — how this decision fails in 6 weeks

## Conventions

1. Entries are append-only. Editing an old entry is forbidden; supersede it with a new entry that references it.
2. Historical references to files that have since been merged or deleted are preserved as-written. The `Related docs` field in an old entry reflects the state of the repo when the entry was written, not the current state.
3. Every confirmatory experiment that runs must have a pre-registration entry in Appendix A of this file **and** a decision-log entry here. If a run was not pre-registered, it is logged here as exploratory and is non-confirmatory. *(Updated by DEC-20261015-017: the registry ledger is now Appendix A of this file, superseding the standalone `experiment_registry_and_preregistration.md`. Registry *rules* relocate to `evaluation_protocol.md` §12 in Phase C.)*
4. When a TODO item is a governance decision (e.g., changing the target file set), it is logged here, not in `TODO.md`.
5. The multiple-testing denominator for `evaluation_protocol.md` §12 is the count of confirmatory EXPERIMENT entries in this log. Exploratory entries (Type: EXPERIMENT (exploratory)) do not count.

---

## Index

| ID | Date | Type | Status | Title |
|----|------|------|--------|-------|
| DEC-20261014-000 | 2026-10-14 | GOVERNANCE | ACTIVE | Establish falsificationist structure and Tier 0 docs before code |
| DEC-20261015-012 | 2026-10-15 | EXPERIMENT (exploratory) | ACTIVE | Phase 1 smoke test logged as exploratory, non-confirmatory |
| DEC-20261015-013 | 2026-10-15 | GOVERNANCE | ACTIVE | Adopt 5-doc target set; gate merges on taxonomy relocation |
| DEC-20261015-014 | 2026-10-15 | GOVERNANCE | ACTIVE | Retract unrecoverable seed entries 001–011; resolve multiple-testing denominator |
| DEC-20261015-015 | 2026-10-15 | GOVERNANCE | ACTIVE | Record code-review findings as freeze-session inputs |
| DEC-20261015-016 | 2026-10-15 | GOVERNANCE | ACTIVE | Close finding 3 of 015 — zero SLSQP fallbacks in Phase 1 |
| DEC-20261015-017 | 2026-10-15 | GOVERNANCE | ACTIVE | Execute Phase A relocations; adopt 6-doc target set |
| DEC-20261015-018 | 2026-10-15 | GOVERNANCE | ACTIVE | Execute Phase C spec merges; retire source files |
| DEC-20261017-019 | 2026-10-17 | GOVERNANCE | ACTIVE | Record audit findings (fair-comparison defect, baseline-set mismatch, parameter drift) as freeze-session inputs; repair doc integrity |
| DEC-20261017-020 | 2026-10-17 | GOVERNANCE | ACTIVE | Define Tests B/C/D (resolves F6); produce freeze worksheet; record findings N1–N3 |
| DEC-20261017-021 | 2026-10-17 | GOVERNANCE | ACTIVE | Freeze `evaluation_protocol.md` v2.3; activate scope v1.3 and risk register v1.2; extend R1 scan to 16 items |
| DEC-20261017-022 | 2026-10-17 | GOVERNANCE | ACTIVE | Write `model_and_method_spec.md` v1.0 Draft (C2); resolve finding F9 (MVP robust-method classification) |
| DEC-20261017-023 | 2026-10-17 | GOVERNANCE | ACTIVE | Freeze `model_and_method_spec.md` v1.1 (C3); resolve open items O1–O7 |

**Gap note (001–011):** Resolved by DEC-20261015-014. The seed entries referenced in DEC-20261014-000 were not written and are not recoverable. They are treated as never having existed in this log.

**Supersession note (DEC-20261015-013):** The 5-doc target set adopted in DEC-20261015-013 is superseded by the 6-doc target set adopted in DEC-20261015-017. The three preconditions and the sequencing rule in 013 remain in force. Only the target count and the risk-register home decision are superseded.

---

## Entries

---

### DEC-20261014-000

**Date:** 2026-10-14
**Type:** GOVERNANCE
**Status:** ACTIVE
**Authority:** Owner
**Related docs:** `problem_framing.md`, `project_charter.md`, `scope_and_non_goals.md`, `success_metrics_and_evaluation_protocol.md`, `falsification_and_kill_criteria.md`, `data_contract_and_point_in_time_policy.md`, `cost_model_and_frictions.md`, `benchmark_and_baseline_spec.md`, `experiment_registry_and_preregistration.md`, `risk_register_and_premortem.md`
**Related risks:** R-P02, R-P03, R-P04, R-H02

**Context:**
Day 1 of `robustfolio`. The project exists because of a strategic goal: build a portfolio-quality research project that demonstrates quantitative reasoning, reproducibility discipline, and honest interpretation, for the purpose of attracting research and industry opportunities. The owner is a 20-year-old ML major with two years of hands-on experience.

The immediate decision on Day 1 was not "what will the project do?" but "what failure modes does it need to defend against before any code is written?" The answer was informed by reading DeMiguel, Garlappi, and Uppal (2009), Chopra and Ziemba (1993), Michaud (1989), and Harvey, Liu, and Zhu (2016) — the foundational critiques of naive portfolio optimization and the multiple-testing problems that make most published strategies fail out-of-sample.

**Decision:**
Establish the project as a falsificationist research effort with frozen Tier 0 documentation prior to any code, and adopt the Core Mental Models OS as the reasoning framework. Produce ten Tier 0 documents in one day to force the reasoning to be explicit before implementation begins. Subsequent code will be written against these contracts, not before them.

**Alternatives considered:**
- **Ad-hoc research notebook** — rejected. No reproducibility, no pre-registration, no protection against p-hacking. This is the base-rate failure mode for solo quant projects.
- **Lightweight docs (one README + one notebook)** — rejected. Insufficient defense against the specific failure modes the literature documents (multiple testing, lookahead, cost ignorance).
- **Full academic paper outline** — rejected. Over-formal for a solo 4–6 week project; the paper format requires peer review and an advisor. A blog post + reproducible repo is the correct format at this stage.
- **Start coding immediately, document later** — rejected. Documentation written after results exist tends to rationalize the results rather than constrain them. This is the exact pattern the project exists to avoid.

**Rationale:**
[First Principles] [Inversion] [Systems] The failure modes of portfolio research are well-documented and well-known: overfitting, lookahead bias, cost underestimation, multiple testing, goalpost-moving. Each has a standard defense, and each defense requires being in place *before* the experiment, not after. Ten documents in one day is aggressive, but the alternative — writing them piecemeal as the project proceeds — is how the defenses get weakened by convenience.

The specific decision to write the *evaluation protocol* and *falsification and kill criteria* before any code is the load-bearing one. It forces the owner to specify, in advance, what would make them stop, what would count as failure, and what would count as success. That is the single most effective defense against confirmation bias in solo research.

**Reversibility:** Hard (documentation contracts are hard to unwind without invalidating prior work)

**Revisit trigger:**
If by end of Week 1 the documentation effort has consumed more time than the code effort, and no experiment has run, the falsificationist structure is failing its own purpose (which is to accelerate honest work, not to substitute for it). In that case, downgrade to a lighter structure with an explicit decision entry — not a silent abandonment.

**Expected value assessment:**
- Probability the discipline holds and produces an honest result: 70%.
- Probability the docs become churn and delay the experiment: 25%.
- Probability the project is abandoned in Week 2–4 despite the structure: 5%.

The failure modes are visible in real time via the update trigger above. That is the defense.

**Pre-mortem:**
Six weeks from Day 1, this decision has failed in one of two ways. Either (a) the documents have proliferated to 14+ files with contradictory cross-references, becoming a substitute for actual work — the doc-churn failure mode — or (b) the documents are correct but no experiment has been run, no finding exists, and the project has no empirical content. Both are detectable from the update trigger and the `evaluation_protocol.md` §9 sunk-cost firewall. Both are correctable by treating the "stop writing docs, run the experiment" rule as binding.

**Outcome (Day 1, 2026-10-14):**

Ten Tier 0 documents written:

1. `problem_framing.md` v2.0 — problem statement, causal model, references
2. `project_charter.md` v1.1 — mission, deliverables, phase gates
3. `scope_and_non_goals.md` v1.0 — MVP, extensions, out-of-scope
4. `success_metrics_and_evaluation_protocol.md` v1.0 — metrics, thresholds, walk-forward
5. `falsification_and_kill_criteria.md` v1.0 — hypotheses, triggers, sunk-cost firewall
6. `data_contract_and_point_in_time_policy.md` v1.0 — sources, point-in-time rules
7. `cost_model_and_frictions.md` v1.0 — cost model, drifted weights, sensitivity
8. `benchmark_and_baseline_spec.md` v1.0 — B1–B5, fair comparison rules
9. `experiment_registry_and_preregistration.md` v1.0 — registry rules, templates
10. `risk_register_and_premortem.md` v1.0 — RPN-scored risks, pre-mortem scenarios

Plus `decision_log.md` (this file) and `README.md` (index).

All ten docs written. Seed entries 001–011 referenced for the eleven foundational decisions (see gap note in Index). No code written. Consistent with the plan.

**Day 1 open risk:** the doc set is already larger than what a solo 4–6 week project typically sustains. This will be tested in Week 1. If the docs are not consistently maintained, they become the failure mode rather than the defense.

---

### DEC-20261015-012

**Date:** 2026-10-15
**Type:** EXPERIMENT (exploratory)
**Status:** ACTIVE
**Authority:** Owner
**Related docs:** `problem_framing.md` (§7, §11, §14), `evaluation_protocol.md` (§0, §1, §7 H1.1/H1.2, §12.2, §15), `experiment_registry_and_preregistration.md`, DEC-20261014-000
**Related risks:** R-P02, R-P03, R-P04, R-H02

**Context:**
Phase 1 smoke test ran 2026-10-15 before `evaluation_protocol.md` reached Frozen status. The run implemented the walk-forward harness and evaluated six methods on 15 liquid US ETFs over 232 months (2007-06 to 2026-09). Parameters: 60-month rolling train, 12-month test, 12-month step, monthly rebalance, long-only, box cap 0.40 (unconstrained where noted), 10 bps per unit turnover.

The run was executed as an exploratory smoke test — to verify the pipeline end-to-end and to check whether H1.1 and H1.2 had any signal at all — and was not registered in `experiment_registry_and_preregistration.md` before execution. Under `evaluation_protocol.md` §12.2, an unregistered run is not confirmatory evidence. Under §15, results from unregistered runs are exploratory.

The parameter choices (60-month window, 0.40 cap, 1.0 turnover penalty, 0.1 = 10 bps cost) were made during harness implementation, not pre-registered. They are recorded here retroactively to prevent silent tuning.

**Decision:**
Treat Phase 1 as exploratory, non-confirmatory. The results in `results/phase1_results.csv` and `problem_framing.md` §14 may be used for diagnostic purposes only — specifically, to scope Tests B/C/D — and may not be cited as evidence for or against any hypothesis in `evaluation_protocol.md` §7 families H1–H4.

Specifically:

- H1.1 and H1.2 are **not falsified**, not confirmed. The observation that sample MVO produces extremal weights (capped max 0.400, unconstrained max 0.599) and ~7.5× the turnover of 1/N is a diagnostic signal, not a finding.
- The observation that Ledoit-Wolf shrinkage and turnover-penalized MVO underperform unpenalized sample MVO on net Sharpe is **not a finding**. It is a signal that the 60/0.40/10bps configuration is not the configuration in which the remedy hypothesis holds — if it holds at all.

**Alternatives considered:**
- **Treat Phase 1 as confirmatory.** Rejected. Violates `evaluation_protocol.md` §12.2 (pre-registration before execution) and §1 principle 1 (gross and exploratory metrics are diagnostic only). Accepting it would erode the protocol's first freeze.
- **Discard Phase 1 entirely and re-run after freeze.** Rejected. The pipeline works; discarding verified code is waste. Marking the result exploratory preserves the code and its diagnostic value while removing the claim.
- **Retroactively register Phase 1 with back-dated parameters.** Rejected. Retroactive registration is not registration. This is the exact goalpost-moving pattern the protocol exists to prevent.
- **Silently keep the Phase 1 numbers without disclosure.** Rejected. Silent inheritance is the failure mode; this entry exists to cut the inheritance path.

**Rationale:**
[Inversion] [Bayesian] The failure mode is not "Phase 1 was wrong." The failure mode is "Phase 1 was unregistered, and later decisions quietly inherit its results." Logging the run as exploratory — with the parameter choices recorded — converts an ambiguous artifact into a named, bounded, disclosed artifact.

[First Principles] A registered experiment is one whose hypothesis, parameters, metrics, and decision rule existed before the result. Phase 1 had none of these. The honest label is what the protocol says it is.

[Goodhart's Law] The temptation to keep "H1.1 and H1.2 confirmed" in `problem_framing.md` §14 is the temptation to let an exploratory number stand in for a confirmatory one. The label must match the protocol, not the wish.

**Reversibility:** Soft. The entry can be superseded if Tests B/C/D later produce a confirmatory result under a frozen protocol. It cannot be deleted — the record is the point.

**Revisit trigger:**
After Tests B/C/D are pre-registered, executed, and logged, and after `evaluation_protocol.md` reaches Frozen. At that point, if the sensitivity sweep produces a configuration in which a robust method beats the best baseline per §6.4, a new confirmatory experiment is registered and Phase 1 becomes its diagnostic predecessor. If not, the diagnostic-benchmark pivot (K1/K3, §10) applies.

**Expected value assessment:**
- Probability the exploratory disclosure prevents a later goalpost-move: high (~85%). Once the parameters are named in the log, they cannot be silently changed without a visible contradiction.
- Probability Phase 1's diagnostic signal is later confirmed by Tests B/C/D: not estimable from Phase 1 alone. This is exactly what Tests B/C/D exist to resolve. Assigning a probability now would itself be an unregistered prior.
- Probability the entry is skipped and Phase 1 gets cited as confirmatory anyway: low, contingent on this entry existing. Hence this entry.

**Pre-mortem:**
Six weeks from now this entry has failed in one of two ways. Either (a) Phase 1's numbers appear in a claim without the "exploratory" qualifier — the label-without-teeth failure mode; or (b) the entry is treated as a verdict rather than a deferral, and Tests B/C/D are skipped on the reasoning that "Phase 1 already answered it" — the premature-closure failure mode. Both are detectable: (a) by grepping `problem_framing.md` §14 and `evaluation_protocol.md` §7 for "confirmed" language attached to Phase 1; (b) by confirming that Tests B/C/D have a registry entry before any Phase 2 work begins.

---

### DEC-20261015-013

**Date:** 2026-10-15
**Type:** GOVERNANCE
**Status:** ACTIVE (partially SUPERSEDED by DEC-20261015-017 — see Supersession note in Index)
**Authority:** Owner
**Related docs:** `TODO.md` (Open Decision, Definition of done), `README.md`, `problem_framing.md`, `evaluation_protocol.md`, `project_charter.md`, `benchmark_and_baseline_spec.md`, `cost_model_and_frictions.md`, `data_contract_and_point_in_time_policy.md`, `experiment_registry_and_preregistration.md`, `risk_register_and_premortem.md`, `scope_and_non_goals.md`
**Related risks:** R-P02, R-P03, R-P04, R-H02

**Context:**
`TODO.md` records an owner decision (2026-10-15) to reduce the doc set from the current 12 files (9 Tier 0 + `decision_log.md` + `README.md` + `TODO.md`) to ~5 foundational files. The stated target is:

```
README.md
docs/problem_framing.md
docs/scope_and_non_goals.md
docs/evaluation_protocol.md      ← absorbs baselines, cost, data, registry rules
docs/decision_log.md
```

That decision supersedes `TODO.md`'s own "Definition of done" (items 4 and 5). By the TODO's own rule — "Do not add items to this list. If you discover a new task, it goes into `decision_log.md`" — a change of this scope is a decision-log entry, not a TODO footnote. This entry records it.

The decision was reached in the context of the Phase 1 finding and the pivot risk it created. It is not a response to Phase 1's results — the motivation is doc-set reduction independent of any experimental outcome — but it must be logged before it becomes entangled with Phase 1's resolution (DEC-20261015-012).

**Decision:**
Adopt a 5-doc target set as the intended end-state of the documentation phase. Execute the merges only after:

1. DEC-20261015-012 (Phase 1 exploratory status) is in the log.
2. The charter's decision taxonomy and authority (`project_charter.md` §7–8, referenced by `evaluation_protocol.md` §16) has been relocated to `evaluation_protocol.md` §8 **before** `project_charter.md` is deleted.
3. A home for the experiment registry (running log, not spec) and the risk register (R-IDs, not spec) has been designated. Candidate homes: `decision_log.md` for the registry ledger; `problem_framing.md` §12 for the risk register. If no home is acceptable, keep both as separate non-Tier-0 files — a running log is not a contract and cannot merge into a frozen protocol.

Merges not gated by these three conditions (`benchmark_and_baseline_spec.md` → `evaluation_protocol.md` §4; `cost_model_and_frictions.md` → §5.5; `data_contract_and_point_in_time_policy.md` → §5.4) may proceed whenever the owner elects, and are not on the critical path for today.

**Alternatives considered:**
- **Keep all 12 files.** Rejected. DEC-20261014-000's pre-mortem named doc proliferation as a failure mode; the file count is not the issue but the maintenance surface is. Consolidation is directionally correct.
- **Merge immediately, including charter and registry.** Rejected. `evaluation_protocol.md` §16 says "The charter owns the decision taxonomy and authority." Deleting the charter before moving the taxonomy self-references a deleted file and breaks the conflict-resolution table. The registry is a ledger, not a spec; merging it into a frozen protocol makes the protocol a mutable log, which destroys the freeze.
- **Pause everything until the doc set is 5 files.** Rejected. That treats the doc count as the goal. The binding constraint is the Phase 1 disclosure and the freeze; the merge is downstream.
- **Fold the decision into `TODO.md` and skip the log entry.** Rejected. That is the TODO's own rule being violated. The Open Decision supersedes the TODO's completion criteria; supersessions of the TODO by the TODO cannot be recorded in the TODO.

**Rationale:**
[First Principles] A governance decision that changes the target file set changes what "done" means. That is definitional, not executional. Definitional changes belong in the decision log.

[Systems] The charter, registry, and risk register are not merely docs; each holds IDs and cross-references (R-P02, R-P03, R-P04, R-H02 in the Day 1 entry; the conflict-resolution table in `evaluation_protocol.md` §16). Deleting without relocating the IDs leaves dangling references. The three preconditions above are exactly the three dangling-reference risks.

[Goodhart's Law] "5 files" is a metric. If it becomes the goal, coverage is sacrificed to hit it. The correct test is coverage-preservation, not file count. The three preconditions are the coverage check.

**Reversibility:** Hard. Deleted docs are recoverable from git history but their cross-references are not automatically restored. Revisit triggers below bound the damage.

**Revisit trigger:**
If any `[PROPOSED]` value in `evaluation_protocol.md` §18 becomes unreachable after a merge — i.e., its source doc is deleted and the value is not relocated — the merge is reversed for that doc. If any R-ID named in DEC-20261014-000 or DEC-20261015-012 dangles after `risk_register_and_premortem.md` is deleted, the merge is reversed for that doc. If the target-doc set is not reached by end of Week 2 and no experiment has run in the interim, the merge is deferred to after the protocol freeze — the constraint is the freeze, not the file count. *(Target updated from 5 to 6 by DEC-20261015-017.)*

**Expected value assessment:**
- Probability the target doc set is reached without loss of coverage: moderate (~60%). The three preconditions are the reason it is not lower.
- Probability a merge introduces a dangling cross-reference that takes >1 hour to notice and fix: moderate (~40%) if executed without the preconditions; low (~10%) if executed after them.
- Probability the merge delays the freeze past Week 2: low (~20%) if the three non-critical merges are deferred until after the freeze; high (~60%) if the merge is attempted first.

The EV of "merge first, freeze second" is lower than "freeze first, merge second" because the merge is reversible-in-principle but the freeze is the binding constraint on Phase 2.

**Pre-mortem:**
Six weeks from now this entry has failed if the doc set is at target count and `evaluation_protocol.md` is not Frozen — consolidation achieved at the cost of the freeze. That is the count-as-goal failure mode, visible from the Status field of `evaluation_protocol.md`. The entry has also failed if the doc set is at target count and one of R-P02/R-P03/R-P04/R-H02 appears in the log without a register entry defining it — coverage traded for count, visible by grepping the log for R-IDs and confirming each resolves.

---

### DEC-20261015-014

**Date:** 2026-10-15
**Type:** GOVERNANCE
**Status:** ACTIVE
**Authority:** Owner
**Related docs:** `decision_log.md` (Index gap note; DEC-20261014-000 Outcome), `evaluation_protocol.md` §12 (multiple-testing denominator), `experiment_registry_and_preregistration.md`
**Related risks:** R-P02, R-P03, R-P04, R-H02

**Context:**
DEC-20261014-000 records in its Outcome block that "seed entries 001–011 [were] logged for the eleven foundational decisions" on Day 1. A full-file audit on 2026-10-15 finds no such entries in `decision_log.md`. The file contains DEC-20261014-000, DEC-20261015-012, and DEC-20261015-013 only. The claim in `000` is therefore unsubstantiated.

Under `evaluation_protocol.md` §12, the count of EXPERIMENT entries in this log is the multiple-testing denominator. If any of the missing 001–011 entries were EXPERIMENT type, the denominator is undercounted. If all eleven were GOVERNANCE type, the denominator is unaffected but the record is still incomplete.

**Decision:**
Declare seed entries 001–011 **not written and not recoverable**. They are treated as never having existed in this log.

This has the following consequences:

1. The claim in DEC-20261014-000's Outcome block — "seed entries 001–011 logged for the eleven foundational decisions" — is **retracted**. The line is superseded by this entry, not edited in place, per the append-only convention.
2. The eleven "foundational decisions" referenced are, as of this entry, undocumented. Where they are load-bearing (the falsificationist structure, the ten-doc Tier 0 set, the adoption of the Core Mental Models OS), their content is preserved in the prose of DEC-20261014-000. Where they are not (individual parameter choices, minor doc-level decisions), they are dropped.
3. The multiple-testing denominator in `evaluation_protocol.md` §12 is confirmed as zero EXPERIMENT entries prior to DEC-20261015-012. No correction is required.
4. The Index gap note in this file is resolved and may be removed in the next file normalization.

**Alternatives considered:**
- **Back-fill entries 001–011 from memory.** Rejected. Reconstructed decisions are not contemporaneous records. Back-filling them with any label short of "reconstructed" would create false provenance. Back-filling them with an explicit "reconstructed" label adds eleven low-value entries for decisions already captured in DEC-20261014-000's prose.
- **Leave the gap open and continue.** Rejected. `evaluation_protocol.md` §12's denominator cannot be validated against an open question. The gap must be closed either way.
- **Delete the "seed entries 001–011" line from `000`.** Rejected. Entries are append-only. Editing history to remove a gap is the failure mode this log exists to prevent.
- **Treat the eleven as SUPERSEDED by `000`.** Rejected. `000` is dated 2026-10-14 and cannot supersede entries of the same date it claims to summarize. The relationship is undefined, not supersession.

**Rationale:**
[Inversion] The failure mode is not "eleven decisions were made informally." The failure mode is "a reference to eleven entries appears in the log, the entries do not exist, and downstream counts (multiple-testing denominator) inherit the reference." Logging the absence closes the inheritance path.

[First Principles] A decision log is a set of dated, atomic records. A reference to records that do not exist is not a record. Retraction is the correct operation; back-fill is not.

[Goodhart's Law] The eleven entries were likely never written because "log eleven entries" was a target on Day 1 and was satisfied in prose instead. This entry exists to prevent the same pattern from recurring: future counts of logged decisions must correspond to actual entries, not to narrative claims of entries.

**Reversibility:** Hard. If the entries are later found in a different file, this entry is superseded by a new entry that migrates them. It cannot be edited.

**Revisit trigger:**
If any of the eleven foundational decisions is later cited as the basis for a Phase 2+ action, and the citation cannot be traced to DEC-20261014-000 or a later entry, this gap is reopened and the citation is treated as unsupported.

**Expected value assessment:**
- Probability the eleven entries exist elsewhere in the repository: low (~10%). The folder audit on 2026-10-15 found no candidate file.
- Probability the gap, left open, later produces an uncounted experiment in the multiple-testing denominator: low (~5%), because no experiments were run on 2026-10-14 or 2026-10-15 other than Phase 1 (now logged as DEC-20261015-012).
- Probability this entry becomes load-bearing for a future audit: moderate (~40%). A public-release or peer-review audit will encounter the "seed entries 001–011" line in `000` and require a resolution. This entry is that resolution.

**Pre-mortem:**
Six weeks from now this entry has failed if (a) the "seed entries 001–011" line in `000` is later discovered to refer to a real file, and this entry's retraction has to be reversed — provenance damage, since retraction then reversal looks like the log is unsure of its own contents; or (b) a future entry cites one of the eleven foundational decisions as a live constraint, and this entry's "dropped" clause is read as license to disregard it. Both are detectable: (a) by keeping the file audit log; (b) by the revisit trigger above.

---

### DEC-20261015-015

**Date:** 2026-10-15
**Type:** GOVERNANCE
**Status:** ACTIVE
**Authority:** Owner
**Related docs:** `decision_log.md` (DEC-20261015-012), `evaluation_protocol.md` (§2, §3, §5.2, §15), `problem_framing.md` §14, source files reviewed: `metrics.py`, `backtest.py`, `optimize.py`, `estimators.py`, `data.py`, `phase1_experiment.py`
**Related risks:** R-P02, R-P03, R-P04, R-H02

**Context:**
A §15 invalidation review of the Phase 1 source on 2026-10-15 produced four findings that affect the protocol freeze. None invalidates Phase 1's status as exploratory. All four are inputs to the freeze session, recorded here so they are not lost between now and then.

**Findings:**

1. **Gross Sharpe is not a Sharpe ratio.** `phase1_experiment.py` calls `annualized_sharpe(gross_returns)` without `rf_monthly`, and `annualized_sharpe(net_returns, rf_monthly=rf)` with it. Reported "gross Sharpe" is a raw return-to-vol ratio; reported "net Sharpe" is a true Sharpe. `cost_drag = gross_sharpe - net_sharpe` therefore conflates transaction cost with the risk-free rate. Order of magnitude: BIL averaged ~10–15 bps/month over 2007–2026, so gross Sharpe is overstated by roughly 0.1–0.2 relative to net. This does not affect H1.1 or H1.2, which use `max_abs_weight` and `realized_turnover`. It affects the §14 table's "Gross Sharpe" and "Cost drag" columns, which are mislabeled.

2. **The turnover penalty was scale-dominated, not tested.** `TURNOVER_PENALTY = 0.1`. Objective terms in monthly units at typical values: `mu'w` ≈ 0.005, `½ w'Σw` ≈ 0.0005, `λ‖Δw‖₁` at λ=0.1 and ‖Δw‖₁ ≈ 0.1 → ≈ 0.01. The penalty is ~2× the return term and ~20× the risk term. The optimizer effectively minimizes ‖w − w_prev‖₁ with MVO as a small perturbation. The Phase 1 conclusion "turnover penalty underperforms unpenalized MVO" is therefore a statement about λ=0.1 specifically, not about turnover penalties as a class. §7 H2.3 was not tested. DEC-20261015-012's wording ("not a finding") understates this — the correct statement is "the penalty as implemented is scale-dominated and uninformative."

3. **Silent SLSQP fallback to equal weight.** `optimize.py` returns `np.ones(n)/n` on any SLSQP failure, without a counter, log, or raise. If `ledoit_wolf_mvo` or `turnover_penalized_mvo` failed on a material fraction of folds, the reported performance is contaminated by 1/N, the best-performing baseline. Direction of bias unknown. The Phase 1 failure rate must be disclosed before the freeze, or the affected method must be flagged as contaminated.

4. **Minor, non-invalidating.** (a) `data.py` cache returns stale data if the cache file exists and is stale; reproducibility risk. (b) `metrics.annualized_turnover` is dead code with a different turnover definition than `realized_turnover`; latent inconsistency. (c) `rf_monthly.reindex(r.index).fillna(0.0)` silently substitutes zero rf for missing months. (d) `_rebalance` uses an expanding-within-test training set (`train + test.iloc[:t]`), which is neither pure rolling nor pure expanding; §5.2 does not describe this convention.

**Decision:**
Record the four findings as freeze-session inputs. No code changes are authorized before the freeze, except the SLSQP failure-rate disclosure in finding 3, which may be performed as a diagnostic re-run without modifying any source file.

**Alternatives considered:**
- **Fix the code now.** Rejected. The freeze decides what the metrics should measure. Fixing `annualized_sharpe` before the freeze has decided whether gross Sharpe remains a reported metric would be action before resolution — the §9 anti-pattern.
- **Amend DEC-20261015-012 to incorporate finding 2.** Rejected. Entries are append-only. Finding 2 is recorded here and referenced by the freeze session; 012's original wording stands as the record of what was decided on its date.
- **Defer all four findings to the freeze session without logging.** Rejected. The gap between tonight and the freeze session is where findings get lost.

**Rationale:**
[Inversion] The failure mode is not "the code has bugs." It is "the code-review findings are discovered, discussed, and forgotten before the freeze session, and the freeze proceeds on the assumptions the review was supposed to challenge." Logging them now closes that path.

[Theory of Constraints] The constraint is the freeze. These four findings are the freeze's inputs. They are not a work queue.

**Reversibility:** Soft. Findings may be superseded by the freeze session's own decisions.

**Revisit trigger:** The freeze session must address all four findings — resolve, defer with rationale, or declare out of scope — before the protocol status changes from `Draft` to `Frozen`.

**Expected value assessment:**
- Probability a finding is lost between tonight and the freeze session without this entry: high (~70%).
- Probability at least one finding changes a `[PROPOSED]` value or a §3 metric definition: high (~80%).
- Probability the SLSQP failure rate materially contaminates a Phase 1 method: not estimable without the diagnostic run.

**Pre-mortem:**
Six weeks from now this entry has failed if the freeze session is completed and none of the four findings is reflected in the frozen protocol or in a superseding entry. Detectable by diffing the frozen `evaluation_protocol.md` §2, §3, §5.2 against this entry.

---

### DEC-20261015-016

**Date:** 2026-10-15
**Type:** GOVERNANCE
**Status:** ACTIVE
**Authority:** Owner
**Related docs:** `decision_log.md` DEC-20261015-015 (finding 3), `evaluation_protocol.md` §15
**Related risks:** R-P02, R-P03, R-P04, R-H02

**Context:**
DEC-20261015-015 finding 3 flagged a silent SLSQP fallback in `optimize.py` that substitutes equal weight on convergence failure, with unknown failure rate across Phase 1 folds. The diagnostic authorized by that entry was run on 2026-10-15 via `scripts/diagnose_slsqp.py`, which detects fallbacks by exact-equality against `1/n` across all assets.

**Result:**

| Method | Fallbacks | Total rebalances | Rate |
|---|---|---|---|
| `sample_mvo` | 0 | 168 | 0.0% |
| `unconstrained_sample_mvo` | 0 | 168 | 0.0% |
| `ledoit_wolf_mvo` | 0 | 168 | 0.0% |
| `turnover_penalized_mvo` | 0 | 168 | 0.0% |

**Decision:**
Close finding 3 of DEC-20261015-015 as a non-issue. The SLSQP fallback branch was not exercised in Phase 1. Phase 1's reported numbers for `ledoit_wolf_mvo` and `turnover_penalized_mvo` are not contaminated by equal-weight substitution.

**Alternatives considered:**
- **Add a persistent failure counter to `optimize.py` and re-run.** Rejected. The exact-equality detector is sufficient given the near-impossibility of the optimizer converging to identical weights for 15 heterogeneous assets under active constraints. A persistent counter is a Phase 2 code change, which DEC-20261015-015 forbids.
- **Leave finding 3 open into the freeze.** Rejected. It is now resolved.

**Rationale:**
[Inversion] The failure mode was "Phase 1's shrinkage/penalty numbers are partly 1/N in disguise." The diagnostic rules this out.

[Theory of Constraints] This was the last open invalidation risk from the code review. The freeze now proceeds with all four 015 findings either resolved (3), deferred to freeze (1, 2), or non-invalidating (4).

**Reversibility:** Soft.

**Revisit trigger:** If Phase 2's walk-forward harness or optimizer is modified, re-run the diagnostic before any confirmatory experiment.

**Expected value assessment:**
- Probability the diagnostic misses a real fallback: low (~5%). The exact-equality check is conservative.
- Probability a Phase 2 optimizer change reintroduces silent fallbacks without this entry: moderate (~40%) if the fallback branch is not removed; low if it is.

**Pre-mortem:**
Six weeks from now this entry has failed if the optimizer is modified and the fallback branch is exercised in a Phase 2 run without a diagnostic. Detectable by grepping Phase 2 output for exactly-equal weights.

---

### DEC-20261015-017

**Date:** 2026-10-15
**Type:** GOVERNANCE
**Status:** ACTIVE
**Authority:** Owner
**Related docs:** `decision_log.md` (DEC-20261015-013), `evaluation_protocol.md` (§8, §16, §18), `project_charter.md` (source, retired), `experiment_registry_and_preregistration.md` (source, retained until Phase C), `risk_register_and_premortem.md` (retained), `TODO.md` (absorbed later), `benchmark_and_baseline_spec.md`, `cost_model_and_frictions.md`, `data_contract_and_point_in_time_policy.md`
**Related risks:** R-P02, R-P04

**Context:**
DEC-20261015-013 committed the project to a consolidated doc set and named three preconditions before executing merges, plus a sequencing rule (freeze first, merge second). This entry executes the Phase A relocations and records the file-set decision.

**Decision:**
Adopt a **6-doc target set** (superseding the 5-doc target in DEC-20261015-013). The risk register cannot be merged into a frozen contract without collapsing the spec/ledger distinction that DEC-20261015-013 itself invokes. It is retained as a standalone living document.

**Target set (6 files):**

1. `README.md`
2. `problem_framing.md`
3. `scope_and_non_goals.md`
4. `evaluation_protocol.md` — absorbs charter §6–9 (Phase A), baselines, cost, data, registry rules (Phase C)
5. `decision_log.md` — absorbs registry ledger as Appendix A (Phase A scaffold; Phase C populate), TODO open items (Phase C)
6. `risk_register_and_premortem.md` — retained

**Retired files, deleted after relocation is verified:**

- `project_charter.md` — §6–9 relocated to `evaluation_protocol.md` §8 in Phase A; remainder relocated to `problem_framing.md` / `scope_and_non_goals.md` in Phase C.
- `benchmark_and_baseline_spec.md` — Phase C.
- `cost_model_and_frictions.md` — Phase C.
- `data_contract_and_point_in_time_policy.md` — Phase C.
- `experiment_registry_and_preregistration.md` — Phase C (rules → `evaluation_protocol.md` §12; ledger → this file's Appendix A).
- `TODO.md` — Phase C (open items → this file's Appendix B).

**Sequencing:** Phase A (charter §6–9 relocation into `evaluation_protocol.md` §8; homes designated for registry ledger and risk register; this entry logged) executes before freeze. Phase C (baseline/cost/data/registry merges; source-file deletion) executes after freeze. Both phases logged here.

**Alternatives considered:**
- **5-doc target (per DEC-20261015-013).** Superseded. Merging the risk register into the protocol or problem framing is the category error DEC-20261015-013 §2 names for the registry. The register is a living document with its own re-scoring cadence; the protocol is a frozen contract.
- **Delete charter without relocating §6–9.** Rejected. `evaluation_protocol.md` §16 self-referenced "the charter owns the taxonomy." Deleting without relocation creates a self-reference to a deleted file. Phase A resolves this.
- **Merge first, freeze second.** Rejected. DEC-20261015-013's own EV assessment: freeze is the binding constraint.
- **Defer both phases until after freeze.** Rejected for Phase A. The freeze checklist (§18) needs §8 in place; leaving the charter as the taxonomy owner means freezing a protocol that references an about-to-be-retired document.

**Rationale:**
[First Principles] File count is a proxy for maintenance surface. Coverage is the goal. 6 files with preserved coverage beats 5 files with a broken spec/ledger distinction.
[Inversion] The failure mode is not "12 files." It is "self-referencing deleted files" and "living registers absorbed into frozen contracts."
[Systems] The charter, registry, and risk register hold cross-references (R-IDs, K-triggers, EXP-IDs) that other files depend on. Relocation before deletion preserves the reference graph.

**Reversibility:** Hard. Deleted files are recoverable from git; cross-references are not automatically restored.

**Revisit trigger:** If the 6-file set is not reached by end of Week 2 and no experiment has run in the interim, defer Phase C until after the freeze. Freeze is the binding constraint. If `risk_register_and_premortem.md` is later found to need frozen status (e.g., to gate a phase), re-evaluate the retention decision.

**Expected value assessment:**
- P(6-file set reached without coverage loss): ~75%.
- P(Phase C delays freeze past Week 2): ~15% if sequenced after freeze; ~50% if attempted first.

**Pre-mortem:**
Six weeks from now this entry has failed if (a) `evaluation_protocol.md` §8 exists but §12 and §§5.4–5.5 do not, leaving a half-merged protocol; or (b) the risk register is deleted anyway without the coverage check. Detectable by grepping the remaining files for retired filenames — zero matches expected after Phase C.

---
### DEC-20261015-018

**Date:** 2026-10-15
**Type:** GOVERNANCE
**Status:** ACTIVE
**Authority:** Owner
**Related docs:** `decision_log.md` (DEC-20261015-017, DEC-20261015-013), `evaluation_protocol.md` (§4, §5.4, §5.5, §12, §16, §19), `benchmark_and_baseline_spec.md` (source, retired), `cost_model_and_frictions.md` (source, retired), `data_contract_and_point_in_time_policy.md` (source, retired), `experiment_registry_and_preregistration.md` (source, retired), `TODO.md` (source, retired), `README.md`, `scope_and_non_goals.md` (retained)
**Related risks:** R-P02, R-P04

**Context:**
DEC-20261015-017 executed Phase A (charter §6–9 relocation) and designated the 6-doc target set. This entry executes Phase C: the spec merges of the baseline, cost, data, and registry-rules documents into `evaluation_protocol.md`, and the absorption of `TODO.md` open items into `decision_log.md` Appendix B.

**Decision:**
Execute the Phase C merges as drafted. Specifically:

1. `benchmark_and_baseline_spec.md` → `evaluation_protocol.md` §4 (baselines).
2. `data_contract_and_point_in_time_policy.md` → `evaluation_protocol.md` §5.4 (data contract).
3. `cost_model_and_frictions.md` → `evaluation_protocol.md` §5.5 (cost model).
4. `experiment_registry_and_preregistration.md` rules → `evaluation_protocol.md` §12; its ledger → `decision_log.md` Appendix A (already scaffolded in DEC-20261015-017).
5. `TODO.md` open items → `decision_log.md` Appendix B.
6. `README.md` status board updated to reflect the 6-doc set.
7. `scope_and_non_goals.md` retained; its cross-references updated to point at `evaluation_protocol.md` §5.5 for cost levels (was `cost_model_and_frictions.md` §3.3).

Source files deleted after relocation is verified: `benchmark_and_baseline_spec.md`, `cost_model_and_frictions.md`, `data_contract_and_point_in_time_policy.md`, `experiment_registry_and_preregistration.md`, `TODO.md`.

**Alternatives considered:**
- **Keep source files as historical artifacts.** Rejected. The 6-doc target exists precisely to retire them. Git history preserves the originals.
- **Merge into `problem_framing.md` instead of `evaluation_protocol.md`.** Rejected. These are all evaluation-contract specs; the protocol is their natural home.
- **Merge the registry *ledger* into the protocol alongside the rules.** Rejected. Same category error as before: a frozen contract cannot host a mutable log.
- **Defer Phase C until after the freeze.** Rejected by sequencing inversion. DEC-20261015-017 already committed to freeze first, merge second. This entry records the merge as **prepared**, not executed, pending the freeze. Its Status remains ACTIVE but the merge blocks are not applied until the protocol's Status flips to `Frozen`.

**Rationale:**
[First Principles] The spec docs each own one slice of the evaluation contract. Consolidating them into one file reduces the maintenance surface without changing what is evaluated.
[Systems] Cross-references from the protocol into the source docs become internal section refs. The reference graph is preserved, not broken.
[Goodhart's Law] File count is not the goal. Coverage preservation is. The revision history of the protocol records what was absorbed from where; git history preserves the full source content.

**Reversibility:** Hard. Deleted files are recoverable from git; cross-references are not automatically restored.

**Revisit trigger:** If any `[PROPOSED]` value in `evaluation_protocol.md` §18 becomes unreachable after a merge — i.e., its source doc is deleted and the value is not relocated — the merge is reversed for that doc. If any of the absorbed sections reads as a summary rather than the full rule, the merge is incomplete and the source doc is restored.

**Expected value assessment:**
- P(all four spec merges preserve coverage without a gap): ~85%. The source content is compact and self-contained.
- P(the merge delays the freeze): ~10%, conditional on merging being done *after* the freeze, as planned. If done before, ~50%.

**Pre-mortem:**
Six weeks from now this entry has failed if (a) `evaluation_protocol.md` §12 exists in rules-only form and the ledger in Appendix A is empty, leaving experiments un-logged; or (b) `scope_and_non_goals.md` still points at `cost_model_and_frictions.md` §3.3 after that file was deleted. Both are detectable by grepping the surviving files for the retired filenames — zero matches expected.

### DEC-20261017-019

**Date:** 2026-10-17
**Type:** GOVERNANCE
**Status:** ACTIVE
**Authority:** Owner
**Related docs:** `decision_log.md` (DEC-20261015-012, -015, -016, -017, -018), `evaluation_protocol.md` (§3, §4.2, §4.3, §4.6, §4.7, §5.2, §5.4.4, §5.4.8, §5.4.9, §7, §13, §18), `problem_framing.md` §14, `README.md`, `docs/README.md`, `docs/TODO.md` (retired; absorbed into Appendix B), source files reviewed: `data.py`, `estimators.py`, `optimize.py`, `backtest.py`, `metrics.py`, `scripts/phase1_experiment.py`
**Related risks:** R-P01, R-P04, R-S02, R-C01

**Context:**
A full documentation-and-source audit on 2026-10-17 (docs set, `src/robustfolio/`, `scripts/`, `results/`, git history) produced findings that bear on the pending freeze. This entry records them so they are not lost between the audit and the freeze session, in the same mode as DEC-20261015-015. None of them changes Phase 1's exploratory status (DEC-20261015-012). Findings F1, F2, F3, F4 are **new**; F5–F7 are documentation-integrity items; F8 is carried forward from DEC-20261015-015 finding 4.

**Findings:**

1. **F1 — Fair-comparison constraint defect.** In `backtest.py`, `equal_weight` and `inverse_vol` return weights that bypass the box constraint entirely (`max_weight` is not applied), while every MVO variant is capped at 0.40. In Phase 1, `inverse_vol` reached `max_abs_weight = 0.858` against an MVO cap of 0.40. This violates `evaluation_protocol.md` §4.6 rule 4 ("same constraints") and is exactly the §4.7 invalidation condition "a baseline's weights were not properly constrained." Consequence: the Phase 1 comparison is not like-for-like — the capped MVO family was denied concentration capacity that `inverse_vol` was allowed, and `inverse_vol` is the row most affected (max weight 0.858, and the largest gross-to-net gap). `equal_weight` is unaffected: 1/15 ≈ 0.067 sits inside any cap. The distortion flatters `inverse_vol`, not `1/N`.
2. **F2 — Baseline-set mismatch and a scope signal.** `evaluation_protocol.md` §4.2 fixes the MVP baseline set as B1 (1/N), **B2 (risk parity)**, B3 (sample MVO), **B4 (minimum variance)**, B5 (turnover-penalized MVO). The code implements B1, B3, and B5. **B2 and B4 are not implemented.** Conversely, `inverse_vol` — listed in §4.2 as an *extension*, not MVP — *is* implemented. This is simultaneously two missing MVP baselines and the §7 scope-creep signal "a new method appears in code before the Phase 2 gate."
3. **F3 — Parameter drift between protocol proposals and code.** Code values vs `[PROPOSED]` protocol values: risk aversion γ = 1.0 vs 5; `w_max` = 0.40 vs 0.30; estimation window = 60 months vs 36; turnover penalty λ = 0.1 vs the proposed λ = κ. Freezing §4.3 and §5.2 without reconciling these would freeze numbers the code does not produce.
4. **F4 — Confounded MVO variants.** `_rebalance` passes the L1 turnover penalty to `unconstrained_sample_mvo` but a penalty of 0.0 to `sample_mvo`. The two MVO variants therefore differ on **two** dimensions at once — box cap *and* turnover penalty — so neither isolates the effect of the constraint or the penalty. (This compounds DEC-20261015-015 finding 2.)
5. **F5 — Documentation-integrity defects (partly repaired today).** (a) Root `README.md` was stale: it claimed "no production code yet," reported every artifact as "Not started," and linked to seven deleted documents; repaired in this session. (b) `decision_log.md` Index omitted the DEC-20261015-018 row; repaired in this session. (c) `decision_log.md` referenced an Appendix B that was never created after `docs/TODO.md` was retired; created in this session. (d) `docs/README.md` claims `model_and_method_spec.md` is "referenced by `evaluation_protocol.md` §4 and §12"; the protocol contains no such reference. (d) is **not** repaired and is assigned to the `model_and_method_spec.md` work item.
6. **F6 — Tests B/C/D are undefined.** `problem_framing.md` §14 and DEC-20261015-012 reference "Tests B/C/D" eight times as the planned resolution of the cap-artifact / window-artifact / real-effect question, but they are specified nowhere. They cannot be pre-registered after the freeze until they are defined. F1 and F3 make this more urgent, not less: the Phase 1 signal that B/C/D were meant to interpret is itself potentially a constraint artifact.
7. **F7 — Metric-implementation gap.** `evaluation_protocol.md` §3 requires CVaR, calibration, deflated Sharpe, probabilistic Sharpe, skewness, kurtosis, and lag-1 autocorrelation; §13 requires block-bootstrap confidence intervals. None of these is implemented in `metrics.py`. The current harness reports Sharpe, turnover, max drawdown, and max weight only.
8. **F8 — Point-in-time and snapshot gap.** `data.py` retrieves retroactively adjusted prices (`auto_adjust=True`) with a local Parquet cache and no immutable snapshot, so §5.4.4 (adjusted-price reconstruction) and §5.4.9 (snapshots) are unsatisfied. This is disclosed as a Phase 1 caveat, but it means the §5.4 data contract as written is not currently satisfiable by the repository.

**Decision:**
Record F1–F8 as freeze-session inputs. No changes to `src/` or `scripts/` are authorized before the freeze (DEC-20261015-015 remains in force). The documentation-integrity repairs in F5(a)–(c) were performed in this session because they are documentation-only and touch no measured artifact.

The freeze session must, for each finding, resolve it, defer it with a stated rationale, or declare it out of scope, before `evaluation_protocol.md` status flips from `Draft` to `Frozen`. F1, F2, and F3 in particular change what a faithful freeze of §4.3 and §5.2 must say; F6 must be resolved before any post-freeze experiment registration.

**Alternatives considered:**
- **Fix `src/` now (apply `max_weight` to all methods, add B2 and B4, correct γ and window).** Rejected. Same reasoning as DEC-20261015-015: the freeze decides what the metrics and constraints should be. Changing measured behavior before that decision is action before resolution.
- **Fold F1–F4 into DEC-20261015-015 by editing it.** Rejected. Entries are append-only; supersession is by a new entry.
- **Defer F1–F8 to the freeze session without logging them.** Rejected. This is the exact "findings discovered, discussed, and forgotten before the freeze" path that DEC-20261015-015 exists to close.
- **Treat F1 as invalidating Phase 1 retroactively.** Rejected. Phase 1 is already labelled exploratory and non-confirmatory; F1 narrows the interpretation of an already-non-confirmatory artifact, it does not un-invalidate anything.

**Rationale:**
[Inversion] The failure mode this entry prevents is a freeze that proceeds on the assumption that Phase 1's code implements the protocol's own baseline set and constraint rules. It does not. The freeze would then have been calibrated against a comparison that `evaluation_protocol.md` §4.7 itself calls invalid.
[Goodhart's Law] "Get the protocol frozen" is a process metric. Its proxy risk is freezing a contract the code cannot satisfy (F2, F8) or that misdescribes the code (F1, F3). The purpose is a satisfiable, honest contract, not a status field reading `Frozen`.
[First Principles] A baseline comparison is only meaningful if the treatments differ solely in the dimension under study. F1, F3, and F4 each break that condition.

**Reversibility:** Soft. Findings may be superseded by the freeze session's decisions. The F5 documentation repairs are themselves reversible via git.

**Revisit trigger:**
The freeze session must address F1–F8. If the freeze completes and none of F1–F8 is reflected in the frozen protocol or in a superseding entry, this entry has failed (detectable by diffing the frozen `evaluation_protocol.md` §3, §4.2, §4.3, §5.2, §5.4 against this entry). If Tests B/C/D are registered before F6 is resolved, the registration is invalid.

**Expected value assessment:**
- Probability at least one of F1–F4 changes a frozen `[PROPOSED]` value or a §4 constraint rule: high (~85%).
- Probability F1 materially affects the interpretation of the Phase 1 diagnostic: high — `inverse_vol` is the method with the largest observed max weight (0.858) and the largest gross-to-net gap, so the artifact lands on a headline row.
- Probability F5-class documentation drift recurs without a checklist item: moderate (~40%) unless the freeze checklist (§18) is extended to include a cross-reference integrity check.

**Pre-mortem:**
Six weeks from now this entry has failed if (a) `evaluation_protocol.md` is `Frozen` while `inverse_vol` still bypasses the box constraint (F1) or while B2/B4 remain unimplemented but listed as MVP (F2); or (b) `docs/README.md` still asserts that `model_and_method_spec.md` is referenced by the protocol (F5d) after the method spec is written. Both are detectable by grepping the code for `max_weight` call-sites and by grepping the protocol for `model_and_method_spec`.

### DEC-20261017-020

**Date:** 2026-10-17
**Type:** GOVERNANCE
**Status:** ACTIVE
**Authority:** Owner
**Related docs:** `decision_log.md` (DEC-20261015-012, -015, -017, -018, DEC-20261017-019), `evaluation_protocol.md` (§4.2, §5.2, §7, §8.4, §18), `problem_framing.md` (§4.1, §14), `scope_and_non_goals.md` §4.3, `notes/freeze_worksheet_2026-10-17.md` (new), `notes/tests_BCD_spec_2026-10-17.md` (new)
**Related risks:** R-S02, R-S03, R-D02, R-P01

**Context:**
DEC-20261017-019 recorded finding F6: "Tests B/C/D" are referenced eight times in `problem_framing.md` §14 and DEC-20261015-012 as the planned resolution of the cap-artifact / window-artifact / real-effect question, but were specified nowhere. The freeze worksheet (TODO item D1) was also outstanding. This entry records the production of both artifacts and three further findings surfaced while producing them.

**Decision:**
1. **F6 is resolved.** Tests B, C, and D are specified in `notes/tests_BCD_spec_2026-10-17.md`, with a common configuration, per-test decision rules, family assignment (B and C: family X, exploratory, non-counting; D: families H2/H3, counting), and a selection firewall that prevents a B/C sweep from choosing Test D's configuration.
2. **The freeze worksheet is produced** at `notes/freeze_worksheet_2026-10-17.md`. It restates every `[PROPOSED]` value in `evaluation_protocol.md` §18 and every finding from DEC-20261015-015 and DEC-20261017-019 with a recommended value, rationale, and source tag.
3. **The recommendations in the worksheet are proposals, not decisions.** They become binding only when the owner confirms them at the freeze session. This entry freezes none of them.
4. **Three new findings (N1–N3) are recorded** as additional freeze-session inputs.

**Findings (new):**

- **N1 — Gate 0 is not met as written.** `evaluation_protocol.md` §8.4 requires the R1 scan to document "≥10 relevant open-source tools, papers, or repositories." The Phase 0 scan (`problem_framing.md` §4.1) names four (`cvxportfolio`, `PyPortfolioOpt`, `Riskfolio-Lib`, `skfolio`). Under the protocol's own exit criteria, Gate 0 has not been passed. *Recommendation:* extend the scan to ≥10 rather than relax the criterion — the criterion is the defense against a false gap claim (§8.6 K3, R-S03).
- **N2 — H1.1 is unreachable under an enforced cap.** If the freeze adopts a uniform `w_max = 0.30` (freeze worksheet §2, resolving F1), then no method's maximum weight can exceed 0.40, and H1.1's test — "max absolute weight > 0.40 in ≥1 fold" — cannot be satisfied by any capped model. H1.1 must be redefined to test the **uncapped** sample MVO, with the capped variant reported as a separate treatment. Without this, the framing's primary premise check fails for a definitional reason, not an empirical one.
- **N3 — The fixed universe is survivorship-biased.** `data.py`'s 15-ticker universe consists of instruments alive *today*, which is exactly R-D02's escalation trigger ("universe membership matches today's live tickers exactly"). §5.4.7 requires a point-in-time candidate list. All 15 incepted before 2007 and none delisted in-sample, so the contract's delisting rules are never exercised and the universe carries an unquantified upward bias. *Recommendation:* reconstruct a point-in-time candidate list, or explicitly downgrade affected claims to universe-conditional and record the limitation in §5.4.7.

**Alternatives considered:**
- **Freeze the protocol in this session using the worksheet.** Rejected. The worksheet is input; the freeze is judgment; they are separate sessions (`freeze_inputs_2026-10-15.md` §6). The owner has not yet confirmed the values.
- **Leave Tests B/C/D undefined and defer to the freeze.** Rejected. Tests B and C are themselves diagnostics that inform the freeze's window and cap choices; defining them earlier is what lets the freeze reconcile F1 and F3 coherently.
- **Fold N1–N3 into DEC-20261017-019.** Rejected. Entries are append-only; 019 was written before these findings existed.
- **Treat the worksheet recommendations as decided.** Rejected. Nothing is frozen until §18 is signed; treating proposals as decided is the Goodhart failure mode the worksheet's own header warns against.

**Rationale:**
[First Principles] A freeze decision requires the complete set of decisions to be visible in one place with their dependencies. The worksheet makes the §18 checklist decision-ready instead of a list of unchecked boxes.
[Inversion] N2 is the clearest instance: adding a constraint (the cap) silently disables the very hypothesis (H1.1) the constraint-set change was meant to make fair. The failure is definitional, and it was invisible until the cap rule and the H1.1 threshold were read together.
[Goodhart's Law] "Get the protocol frozen" is a process metric. Freezing unsatisfiable contracts (F8) or unreachable hypotheses (N2) satisfies the metric while defeating its purpose. The worksheet exists to surface both before the status flips.

**Reversibility:** Soft. Both artifacts are working inputs; the freeze session may revise or discard any recommendation, and the Tests B/C/D specification may be re-scoped there.

**Revisit trigger:**
At the freeze session: every recommendation must be accepted, replaced, or declined with a reason; F6's specification must be confirmed or revised before any post-freeze registration references it; N1 must be resolved (scan extended or criterion amended) before Gate 0 is declared passed.

**Expected value assessment:**
- Probability the worksheet reduces freeze-session time by consolidating §18 into one sheet: high (~80%).
- Probability at least one worksheet recommendation is revised at the freeze: high (~70%) — expected, and the reason recommendations are not decisions.
- Probability N2 would have caused a spurious H1.1 failure had it not been caught: moderate (~50%) if the cap is adopted uniformly and H1.1 is left unchanged.
- Probability N3 is left unresolved and every result carries an unquantified survivorship bias: moderate (~40%) without an explicit freeze-session decision.

**Pre-mortem:**
Six weeks from now this entry has failed if (a) the worksheet's recommendations are quoted as decided values while §18 is still unsigned; or (b) Tests B and C have run and one of their arms was used to select Test D's configuration, defeating the firewall in `tests_BCD_spec_2026-10-17.md` §5. (a) is detectable by checking `evaluation_protocol.md` Status against any citation of a worksheet value; (b) is detectable by confirming that Test D's registered window and cap equal the frozen §5.2/§4.3 values.

### DEC-20261017-021

**Date:** 2026-10-17
**Type:** GOVERNANCE
**Status:** ACTIVE
**Authority:** Owner
**Related docs:** `evaluation_protocol.md` (v2.3, Frozen), `scope_and_non_goals.md` (v1.3, Active), `risk_register_and_premortem.md` (v1.2, Active), `problem_framing.md` (v2.4), `README.md` (root), `docs/README.md` (v1.3), `notes/freeze_worksheet_2026-10-17.md`, `notes/tests_BCD_spec_2026-10-17.md`, DEC-20261015-015, DEC-20261015-016, DEC-20261015-017, DEC-20261015-018, DEC-20261017-019, DEC-20261017-020
**Related risks:** R-P01, R-P04, R-D01, R-D02, R-C02, R-S02

**Context:**
DEC-20261017-020 produced the freeze worksheet and defined Tests B/C/D. This entry is the freeze session itself: the owner confirmed the worksheet's recommendations, and the resulting values were written into `evaluation_protocol.md`. The freeze of the evaluation protocol is the binding constraint the whole Phase 0 has been structured around (DEC-20261015-017), and DEC-20261015-015 and DEC-20261017-019 had accumulated open findings that had to be resolved before the status could flip.

**Decision:**
Freeze and activate the documentation set, and resolve the accumulated freeze-session inputs.

1. **`evaluation_protocol.md` v2.3 — Status `Frozen`.** Every `[PROPOSED]` value confirmed or replaced; all inline freeze-session notes resolved. The full decision table with rationale and source tags is `notes/freeze_worksheet_2026-10-17.md` §0 and §13.
2. **`scope_and_non_goals.md` v1.3 — Status `Active`.** The §10 activation checklist was completed; §3.1 defaults were aligned with the frozen protocol.
3. **`risk_register_and_premortem.md` v1.2 — Status `Active`.** Ratings confirmed; the §8 materialization log opened with R-D01 (adjusted-price ingestion, finding F8) and R-D02 (survivorship universe, finding N3).
4. **`problem_framing.md` v2.4.** The §4.1 Phase 0 scan was extended from 4 to 16 items, satisfying the §8.4 Gate 0 exit criterion (finding N1).
5. **No `src/` or `scripts/` change.** DEC-20261015-015's pre-freeze source freeze held to the end.

**Key frozen values (full list in the worksheet §0/§13):**

- Estimation window **60 months rolling**, re-estimated monthly; test 12; step 12. §5.3 scoped to hyperparameter selection only (embargo 1 month).
- `w_max = 0.30` applied **uniformly to every method** (fixes F1); `γ = 10`, scale-verified against a ≈12.3 balance point (replaces the §4.3-proposed 5 and the code's 1.0); `λ = κ = 0.001` (replaces the scale-dominated 0.1).
- Data contract re-frozen as the **satisfiable two-tier** path: raw unadjusted + corporate actions + SHA-256 snapshots; 60-month eligibility; a required point-in-time candidate list; a missing-rf policy that never substitutes zero; a content-addressed cache with confirmatory runs reading snapshots (fixes F8, satisfies §5.4.7).
- Execution convention made explicit (signals through close t−1; hold month t); single `R_f` for gross and net Sharpe; H1.1 redefined to test the **uncapped** optimizer (fixes N2); Gate 0 exit requires the ≥10-item R1 scan (fixes N1).

**Alternatives considered:**
- **Freeze §5.4 as aspirational (vendor-grade PIT required).** Rejected. It is not satisfiable at the $0 data budget and would fire K6 on the first confirmatory run. The two-tier path keeps the point-in-time rule intact at $0.
- **Amend the Gate 0 criterion instead of extending the scan.** Rejected. Lowering a gate criterion at the moment of passing it is goalpost-moving (Goodhart). Extending the scan satisfies the criterion on its own terms.
- **Keep γ = 5 (proposed) or γ = 1.0 (code).** Rejected. γ = 1.0 makes B3 a strawman baseline (R-S02, fake wins); the scale check showed the balance point is ≈12.3, so γ = 10 is the representative choice.
- **Freeze only the measurement protocol and defer §5.4.** Rejected by the owner. A half-frozen protocol would leave Gate 1's entry criteria unmet and invite a second freeze.
- **Leave F5(d) (the false `model_and_method_spec.md` reference) to the method-spec work item.** Rejected. It is a documentation-only defect; it was fixed in this session rather than carried.
- **Wait for the method spec before freezing the protocol.** Rejected. The method spec is the *next* artifact (C2/C3); the protocol is the constraint it must satisfy, not the reverse.

**Rationale:**
[Theory of Constraints] The freeze was the binding constraint on every downstream phase. Resolving the accumulated findings first (DEC-20261015-015, DEC-20261017-019, DEC-20261017-020) is what made the freeze a decision rather than a status flip.
[Inversion] N2 was the load-bearing catch: enforcing the uniform cap would have made H1.1 unreachable by construction. H1.1 now tests the uncapped optimizer, so the framing's premise check is empirical again.
[First Principles] A baseline comparison is only meaningful if the treatments differ solely in the dimension under study. F1 (constraint asymmetry), F3 (parameter drift), and F4 (confounded variants) each broke that condition; the frozen values restore it.
[Goodhart's Law] The freeze is a process metric; its value is a satisfiable, honest contract, not the string `Frozen`. The two rejection alternatives above exist to keep the status field honest.

**Reversibility:** Hard. The protocol is now `Frozen`; §16 permits changes only for a pre-existing protocol flaw, documented in the decision log with a version bump, and post-result changes require an external-review defense. Findings may still be superseded by later entries.

**Revisit trigger:**
Any change to a frozen value requires a §16 amendment and a decision-log entry. Tests B/C/D may reveal that the 60-month window or the 0.30 cap is the wrong configuration; if so, that is a new pre-registered experiment (per the firewall in `notes/tests_BCD_spec_2026-10-17.md` §5), not an edit to the frozen protocol. Gate 1 cannot be entered until the method spec (§ C2/C3) is written and the point-in-time candidate list exists (§5.4.7).

**Expected value assessment:**
- Probability the freeze unblocks Phase 1 within the Phase 0 time-box: high (~85%). The remaining Phase 0 items are the method spec and the environment doc.
- Probability at least one frozen value is revised by a later §16 amendment: moderate (~40%) — expected; the window and cap are explicitly swept dimensions in Tests B/C/D.
- Probability the N2 fix prevents a spurious H1.1 failure: high (~90%), conditional on the uniform cap being implemented.
- Probability the survivorship requirement (N3) is under-scoped and the PIT list proves hard to reconstruct: moderate (~45%). If so, the fallback is a documented universe-conditional downgrade, not a silent one.

**Pre-mortem:**
Six weeks from now this entry has failed in one of three ways. (a) The protocol reads `Frozen` but the Phase 2 code still bypasses the box constraint for some methods (F1) or implements the expanding-within-test convention (§5.2) — detectable by grepping `src/` for `max_weight` call-sites and for `test.iloc[:t]`. (b) A frozen value was changed after seeing a result without a §16 amendment — detectable by diffing `evaluation_protocol.md` against this entry's date. (c) The Phase 1 numbers are cited as confirmatory evidence for the now-frozen thresholds — detectable by grepping reports for "confirmed" language attached to Phase 1. All three are the failure modes the freeze exists to prevent.

---

### DEC-20261017-022

**Date:** 2026-10-17
**Type:** GOVERNANCE
**Status:** ACTIVE
**Authority:** Owner
**Related docs:** `model_and_method_spec.md` (v1.0, Draft — new), `evaluation_protocol.md` (v2.4, Frozen), `scope_and_non_goals.md` (v1.4, Active), `docs/README.md` (v1.4), `notes/tests_BCD_spec_2026-10-17.md`, `notes/freeze_worksheet_2026-10-17.md`, DEC-20261015-015, DEC-20261017-019, DEC-20261017-020, DEC-20261017-021
**Related risks:** R-S02, R-E01, R-E04, R-M05, R-C02

**Context:**
DEC-20261017-021 froze the protocol and activated scope and the risk register, leaving the method spec (todo C2, then C3) as the binding constraint on Gate 1 (§8.4). Writing the spec surfaced a contradiction the freeze had not resolved: the frozen protocol §4.2 listed "shrinkage covariance + minimum variance" and "Black-Litterman" as **extensions**, while the Active `scope_and_non_goals.md` §3.4/§3.5 mark them **MVP**. Scope §6 makes scope authoritative on MVP-vs-extension classification, but the two documents had never been reconciled, and the freeze worksheet settled only the *baseline* set (B1–B5). This is finding **F9**.

F9 is load-bearing, not cosmetic. Hypotheses H2.1 ("shrinkage covariance beats sample covariance") and H2.2 ("Bayesian expected returns beat historical mean") are **Family H2 — Phase 2**. Extensions cannot run until Gate 4 (scope §4.3). Under the protocol's reading, Phase 2's own hypotheses would be unreachable — structurally identical to finding N2 (an unreachable H1.1), which the freeze had to fix.

**Decision:**
1. **`model_and_method_spec.md` v1.0 — `Draft`** is written (todo C2 complete). It defines the MVP method set, the estimators, the optimizers/solvers, the walk-forward harness, the cost application, and the exact metric implementations. It absorbs DEC-20261017-019 finding **F7** (CVaR, DSR, PSR, skewness, kurtosis, lag-1 autocorrelation, stationary block-bootstrap CIs).
2. **F9 resolved in scope's favour** (scope §6). Shrinkage covariance and Black-Litterman are MVP **robust-method** components. `evaluation_protocol.md` §4.2 was corrected: the hard-coded extension list is replaced by a pointer to scope §3–§4 (protocol v2.3 → **v2.4**; a §16 **pre-result** correction — no experiment had run against v2.3 and no measurement value changed). `scope_and_non_goals.md` v1.3 → **v1.4** clarifies §3.5 and names the MVP robust methods.
3. **MVP method set fixed.** Baselines **B1–B5** (unchanged, protocol §4.2). Robust methods: **M1** = Ledoit-Wolf shrinkage covariance + sample-mean MVO (tests H2.1; differs from B3 only in Σ); **M2** = sample covariance + Bayesian/Black-Litterman posterior returns (tests H2.2; differs from B3 only in μ). M2's no-views B-L has the closed form \(\hat\mu_{BL} = \tfrac12(\Pi + \hat\mu)\), removing solver ambiguity.
4. **Implementation decisions recorded in the spec** (all are implementation-level, not scope or threshold): convex-QP MVO family with auxiliary L1 variables solved by `cvxpy`/`CLARABEL`, **no fallback** (replaces the Phase 1 SLSQP subgradient path and its equal-weight fallback); Ledoit-Wolf via the `sklearn` identity target; risk-parity via CCD with a box-constrained least-squares extension when the cap binds; rolling-60 walk-forward with a single drifted-weight function; the canonical turnover and single-\(R_f\) conventions. `cvxpy` is added to `requirements.txt`.
5. **Open items O1, O2, O4–O7** (`model_and_method_spec.md` §11) must be resolved before the spec is frozen (C3). C3 is **not** performed in this entry: writing and freezing are separate acts (the DEC-20261015-015 / §18 discipline), and the owner has not yet reviewed v1.0.

**Alternatives considered:**
- **Protocol wins — shrinkage and B-L stay extensions.** Rejected. It makes H2.1 and H2.2 untestable until Gate 4, i.e. it makes two Phase 2 hypotheses unreachable. It also contradicts scope §3.4/§3.5, which the freeze activated as authoritative.
- **Middle path — shrinkage is MVP, B-L deferred.** Rejected by the owner. It leaves H2.2 untestable and re-opens the classification for a second time.
- **Reconcile only in the method spec; leave protocol §4.2 as written.** Rejected. A contradiction left inside a `Frozen` document will be read differently by different readers; the spec cannot be the authority on a value the protocol owns.
- **Freeze the method spec now (C3 in the same act).** Rejected. The spec must be read before it is frozen, and O1–O7 remain open; freezing it now would lock in silently-defaulted choices. The write/freeze separation is the same discipline that produced the protocol freeze.
- **Fold F9 into DEC-20261017-021.** Rejected. Entries are append-only; 021 recorded the freeze, which did not contain this finding.

**Rationale:**
[First Principles] A method is the triple (μ, Σ, constructor). M1 differs from B3 only in Σ and M2 only in μ, so H2.1 and H2.2 are single-factor tests rather than confounded comparisons (protocol §4.6; F4).
[Theory of Constraints] Gate 1's binding constraint was the method spec; F9 was a latent blocker *inside* that constraint, which is exactly why writing the artifact surfaced it.
[Inversion] The failure mode is a spec that reads as compliant while quietly making a hypothesis unreachable. Managing the MVP/extension boundary explicitly is the fix; leaving §4.2 uncorrected would let a future reader claim MVP compliance while never running H2.1/H2.2.
[Information Theory] Closed forms (the B-L posterior) and a single source of truth for each frozen value (§2 of the spec) remove decisions that could otherwise drift between implementation and protocol.

**Reversibility:** Soft for the spec (it is `Draft`). The protocol §4.2 correction is a §16 pre-result change and may itself be superseded by a later entry; the freeze record in §18 is preserved unchanged as the v2.3 snapshot.

**Revisit trigger:**
The C3 freeze of `model_and_method_spec.md`; resolution of O1–O7; and, if the point-in-time candidate list (O1) includes a cash/T-bill proxy, the B2 cap handling and the MVO scale in §5.3/§5.4 must be revisited before C3. A future change to the MVP method set is a scope amendment (scope §4.3), not an edit to this entry.

**Expected value assessment:**
- Probability the spec is freezeable (C3) after resolving O1–O7 within the Phase 0/1 time-box: high (~85%).
- Probability at least one O-item changes a metric convention (rather than confirming the recommendation): moderate (~30%) — the DSR \(V\)-when-\(N=1\) convention (O6) and the calibration operationalisation (O5) are the least settled.
- Probability the F9 correction prevents a Phase 2 dead-end: high (~90%).
- Probability the PIT list includes a cash proxy and reopens B2's cap handling: moderate (~35%), conditional on the universe reconstruction.

**Pre-mortem:**
Six weeks from now this entry has failed in one of three ways. (a) The spec is frozen with an `[OPEN]` item silently defaulted — detectable by grepping `model_and_method_spec.md` for `[OPEN]`. (b) The v2.4 §4.2 correction is cited as a post-result change — detectable by comparing the DEC date with the first confirmatory run date (no run predates it). (c) The Phase 2 code diverges from §5/§6 of the spec — detectable by testing each constructor against the spec's formulation and the no-fallback policy. All three are caught by the §12.4 pre-registration template, which requires the spec version and git commit at registration.

---

### DEC-20261017-023

**Date:** 2026-10-17
**Type:** GOVERNANCE
**Status:** ACTIVE
**Authority:** Owner
**Related docs:** `model_and_method_spec.md` (v1.1, Frozen — frozen by this entry), `evaluation_protocol.md` (v2.4, Frozen), `scope_and_non_goals.md` (v1.4, Active), `docs/README.md` (v1.5), DEC-20261015-015, DEC-20261017-019, DEC-20261017-020, DEC-20261017-021, DEC-20261017-022
**Related risks:** R-E01, R-E04, R-M05, R-C02, R-S02

**Context:**
DEC-20261017-022 wrote `model_and_method_spec.md` as `Draft` v1.0 with six `[OPEN]` items (O1, O2, O4–O7), deliberately leaving the freeze (todo C3) as a separate act. C3 was the last documentation item on the Gate 1 critical path. This entry is the C3 freeze session: the owner confirmed the resolutions, and the status flips.

**Decision:**
1. **`model_and_method_spec.md` v1.0 → v1.1 — Status `Frozen`** (item C3 complete). All six `[OPEN]` items resolved and recorded in the spec §11:
   - **O1** — **No cash/T-bill proxy** in the candidate universe. The universe holds risky ETFs only; the risk-free asset is modelled separately (§3.4), and a near-zero-volatility instrument degenerates the ERC and mean-variance scale. Duration-bearing treasuries (e.g. `SHY` and longer) stay eligible. This is universe composition delegated by `scope_and_non_goals.md` §3.1 — **not** a scope change.
   - **O2** — Ledoit-Wolf target = the `sklearn` identity target (Ledoit & Wolf, 2004); constant-correlation (2003) is a registered variant.
   - **O4** — Solver acceptance: `optimal`/`optimal_inaccurate` **and** max constraint violation ≤ 1e-7 **and** duality gap ≤ 1e-7; otherwise a hard error.
   - **O5** — Calibration: one-month horizon; 90% bootstrap prediction intervals for next-month return **and** volatility; coverage target 80–100%.
   - **O6** — DSR \(V\) when \(N = 1\): analytic estimator variance \((1 + \tfrac12\hat{SR}^2)/T\); for \(N \ge 2\), the sample variance (`ddof=1`) of the family's per-period trial Sharpes.
   - **O7** — Bootstrap seed `SEED = 20261017`, recorded in the run manifest.
2. **Correction to v1.0's stated C3 conditions.** v1.0 listed "the frozen configuration reproduced by `scripts/run_experiment.py` on the MVP universe" as a C3 condition. That inverts the code/spec dependency — the code is the *subject* of the spec, not its precondition — so it is removed from C3 and reassigned to Gate 1/2. The point-in-time candidate list and the §5.4.8 leakage suite are **Gate 1 entry** items (protocol §8.4), not C3 items.
3. **Gate 1 documentation half complete.** Gate 1 entry still requires the point-in-time candidate list (protocol §5.4.7) and the §5.4.8 leakage suite to be built and to pass. Those are now the only unblocked Gate 1 items.
4. **No `src/` or `scripts/` change.** The spec remains the constraint the Phase 2 rewrite must satisfy.

**Alternatives considered:**
- **Freeze v1.0 as written, carrying the `[OPEN]` items into Phase 2.** Rejected. It would lock silent defaults into a `Frozen` document and violate the spec's own §11 ("every `[OPEN]` resolved"). The whole point of listing them was that they must not default silently.
- **Resolve O1 by deferring to the PIT reconstruction.** Rejected. The cash-proxy question is decidable on principle now — the risk-free leg is modelled separately and a near-zero-volatility instrument breaks the ERC/MVO scale — so leaving it open would block B2's implementation for no gain.
- **Bump to v2.0 instead of v1.1.** Rejected. The change is the resolution of the draft's own open items, not a redesign of the method set or metrics.
- **Fold C3 into DEC-20261017-022.** Rejected. Entries are append-only, and DEC-022 explicitly recorded that C3 was not performed there; writing and freezing are separate acts.

**Rationale:**
[Theory of Constraints] C3 was the last documentation blocker on Gate 1; with it frozen, the project's remaining Gate 1 work is data, not documents.
[First Principles] O1 was resolved from principle (the risk-free asset is not a portfolio asset; near-zero volatility degenerates the optimizer) rather than by an arbitrary pick.
[Inversion] Freezing forced a literal check of v1.0's own stated freeze conditions, which exposed that one of them (run-reproduction) inverted the dependency — a defect that would have blocked C3 indefinitely had it not been corrected.
[Goodhart's Law] The value of the `Frozen` status is that the definitions are fixed before any result exists, not the string itself; resolving the items first is what makes the status honest.

**Reversibility:** Hard. The spec is `Frozen`; a change requires a decision-log entry and a version bump on the DEC-20261017-023 discipline. Findings may still be superseded by later entries.

**Revisit trigger:**
If Gate 1/2 implementation shows a specification is not implementable as written (most likely the box-constrained risk-parity formulation, §5.3, or the solver acceptance test, §5.6), that is a §16-style amendment to this document, logged and version-bumped — not a silent code deviation. If the point-in-time reconstruction cannot exclude a cash proxy, O1 is revisited before the first confirmatory run.

**Expected value assessment:**
- Probability the spec is implementable as written without amendment: high (~75%). The risk-parity box formulation (§5.3) is the least certain element.
- Probability at least one frozen definition (a metric convention, or the risk-parity formulation) is amended during the Phase 2 build: moderate (~35%) — expected for a first freeze of a spec this detailed, provided each amendment is logged.
- Probability Gate 1 is now blocked only on data (the PIT list), not documentation: high (~90%).

**Pre-mortem:**
Six weeks from now this entry has failed in one of three ways. (a) The Phase 2 code silently deviates from a frozen definition (e.g. an equal-weight fallback reappears, or λ ≠ κ) — detectable by testing each constructor against §5 and grepping `src/` for fallback patterns. (b) The O1 cash-proxy rule is contradicted by the actual PIT list — detectable by checking the candidate list against §3.4. (c) A frozen metric definition (most likely DSR `V`, O6) is changed after seeing Test D's result — detectable by diffing `model_and_method_spec.md` against this entry's date. All three are the failure modes the freeze exists to prevent.

---

## Appendix A — Experiment Registry (Ledger)

This appendix is the append-only ledger of pre-registered experiments. Registry *rules* (what counts as an experiment, ID format, denominator rules, invalidation rules) live in `evaluation_protocol.md` §12 and, until Phase C completes, in `experiment_registry_and_preregistration.md`. This appendix holds the *entries*.

**Status of this appendix:** Scaffolded in Phase A (per DEC-20261015-017). Populated in Phase C after the freeze. The Phase 1 exploratory run is recorded below as a pointer only; its substantive record is DEC-20261015-012.

**Rule:** No entry is edited. Registrations, results, conclusions, and decisions are appended in order. Invalidations are marked in place with a reference to the invalidation rule in `evaluation_protocol.md` §12.

### Index

| EXP-ID | Date | Family | Status | Title |
|--------|------|--------|--------|-------|
| EXP-H1-20261015-001 | 2026-10-15 | X (exploratory) | ARCHIVED | Phase 1 smoke test (retroactively logged per DEC-20261015-012) |

### EXP-H1-20261015-001

**Status:** ARCHIVED
**Registered:** 2026-10-15 (retroactively, as a pointer; the substantive record predates this scaffold)
**Family:** X (exploratory — non-confirmatory)
**Related decision log entry:** DEC-20261015-012

**Note:** This entry exists so the ledger is non-empty and so future readers can trace the Phase 1 exploratory run through the correct index. It does not carry a full pre-registration template because it was not pre-registered. It is not a finding. It does not count toward any multiple-testing denominator.

**No further entries exist as of 2026-10-15.** The first confirmatory registration will be appended after `evaluation_protocol.md` reaches `Frozen`.

---

## Appendix B — Absorbed Items from Retired `docs/TODO.md`

This appendix is the migration record for the open items in `docs/TODO.md` (v1.1, retired per DEC-20261015-018 item 5; source preserved in git history). It exists so that retiring the TODO did not silently drop its unfinished work. It is a **migration record, not a task list**: like the rest of this log, it is append-only, and new tasks are recorded as new decision entries, not added here.

**Dispositions:**

- **closed** — the item is done or superseded; no further action.
- **open** — the item is still live; its home is named.
- **declined** — the owner decided against it, with the reason preserved from the source.

| TODO ID | Item | Status at retirement | Home now |
|---------|------|----------------------|----------|
| A1 | Fix `README.md` to reflect reality | Open | **Closed** — root `README.md` reconciled 2026-10-17 (DEC-20261017-019, F5a) |
| A7 | Verify merges did not break cross-references | Partial | **Closed** — F5(a)–(c) repaired (DEC-20261017-019); F5(d) (the false `model_and_method_spec.md` reference in `docs/README.md`) fixed at the freeze (DEC-20261017-021, `docs/README.md` v1.3) |
| B2 | Tighten `project_charter.md` | Superseded | Closed — charter retired (DEC-20261015-017/-018); content relocated to `evaluation_protocol.md` §8, `problem_framing.md`, `scope_and_non_goals.md` |
| B3 | Tighten `scope_and_non_goals.md` | Open | **Closed** — activated v1.3 (DEC-20261017-021); §3.5/§3.6 clarified at v1.4 (DEC-20261017-022) |
| B4 | Verify the new file set is internally consistent | Open | Open — partially addressed by this session's audit (DEC-20261017-019) |
| C1 | Decide the three open method choices | Open | **Closed** — freeze worksheet (§0/§13); 60-month window, `w_max` 0.30 uniform, γ = 10, λ = κ (DEC-20261017-021) |
| C2 | Write `model_and_method_spec.md` | Open | **Closed** — `model_and_method_spec.md` v1.0 Draft written 2026-10-17 (DEC-20261017-022); absorbs F7 |
| C3 | Freeze the method spec | Open | **Closed** — `model_and_method_spec.md` v1.1 `Frozen`; all `[OPEN]` items resolved (DEC-20261017-023) |
| D1 | Extract every `[PROPOSED]` value into one table | Open | **Closed** — freeze worksheet produced (DEC-20261017-021) |
| D2 | Confirm or replace each value | Open | **Closed** — all values confirmed/replaced at the freeze session (DEC-20261017-021) |
| D3 | Freeze the evaluation protocol, data contract, and cost model | Open | **Closed** — `evaluation_protocol.md` Frozen at v2.3; v2.4 is a §16 §4.2 correction only (DEC-20261017-022) |
| E1 | `decision_log.md` entry for Phase 1 parameter choices | In progress | **Closed** — DEC-20261015-012 |
| E2 | `reproducibility_and_environment.md` | Open | Open — written when the Python environment is first set up |
| E3 | `results_reporting_and_claims_policy.md` | Open | Open — must be written before Phase 4 |
| E4 | `roadmap_and_phase_gates.md` | Declined | Closed — declined in source; not re-opened |
| E5 | `architecture_decision_records/` | Open | Open — created at the first irreversible architectural decision |
| E6 | `glossary.md` | Declined | Closed — declined in source; not re-opened |
| E7 | `open_source_and_license_policy.md` | Open | Open — must be written before public release |
| F5 | Log the experiment in the registry before running it | Open | **Closed** — DEC-20261015-012 + Appendix A pointer `EXP-H1-20261015-001` |

**Note on F1–F4 of the source TODO (F1–F4 in "Phase F").** Those items (implement data pipeline, baselines, walk-forward harness, run H1.1/H1.2) were marked done in exploratory form. Their completion is recorded in DEC-20261015-012; DEC-20261017-019 qualifies it (the harness was completed but does not implement the protocol's baseline set or constraint rules).

**Open items from this appendix that are on the critical path:** C1 → C2 → C3 (method spec), and D1 → D2 → D3 (the freeze). These are the same items named as the binding constraint in DEC-20261015-017.

**Update 2026-10-17 (DEC-20261017-021).** The freeze closed: **D1** (the worksheet was produced), **D2** (every value was confirmed or replaced), **D3** (the protocol, data contract, and cost model are `Frozen` at v2.3), **C1** (the open method choices were decided — 60-month window, `w_max` 0.30 uniform, γ = 10, λ = κ), **A7** (the last dead cross-reference, F5d, was fixed in `docs/README.md`), **B3** (scope activated at v1.3), and **B4** (the audit and freeze reconciled the file set). Still open: **C2** and **C3** (write and freeze the method spec), **E2** (`reproducibility_and_environment.md`), **E3** (`results_reporting_and_claims_policy.md`), **E5** (`architecture_decision_records/`), **E7** (`open_source_and_license_policy.md`). The method-spec half (C2 → C3) is now the binding constraint on Gate 1.

**Update 2026-10-17 (DEC-20261017-022).** **C2** closed — `model_and_method_spec.md` v1.0 `Draft` written; it absorbs finding F7. Finding **F9** (MVP robust-method classification: protocol §4.2 vs scope §3.4/§3.5) resolved in scope's favour; `evaluation_protocol.md` §4.2 corrected at v2.4 (a §16 pre-result change) and `scope_and_non_goals.md` clarified at v1.4. **C3 remains open** and is now gated on the spec's `[OPEN]` items O1, O2, O4–O7. The remaining appendix items open on the critical path are C3 and, for Gate 1, the point-in-time candidate list (protocol §5.4.7).

**Update 2026-10-17 (DEC-20261017-023).** **C3** closed — `model_and_method_spec.md` v1.0 `Draft` → **v1.1 `Frozen`**; all six `[OPEN]` items resolved (spec §11). The **documentation half of Gate 1 is complete**. Gate 1 entry now requires only the point-in-time candidate universe list (protocol §5.4.7) and the §5.4.8 leakage suite. The remaining appendix items still open are **E2** (`reproducibility_and_environment.md`), **E3** (`results_reporting_and_claims_policy.md`), **E5** (`architecture_decision_records/`), and **E7** (`open_source_and_license_policy.md`) — none on the Gate 1 critical path.

---

## Revision history

| Date | Change | Author |
|------|--------|--------|
| 2026-10-14 | Initial file. DEC-20261014-000 recorded; entries 001–011 referenced. | Ken Ira Lacson Talingting |
| 2026-10-15 | Added DEC-20261015-012 (Phase 1 exploratory status) and DEC-20261015-013 (5-doc target governance). | Ken Ira Lacson Talingting |
| 2026-10-15 | File normalized: added header, format section, conventions, index, gap note for 001–011, and this revision history. No entry content was altered. | Ken Ira Lacson Talingting |
| 2026-10-15 | Added DEC-20261015-014 (retraction of unrecoverable seed entries 001–011); resolved index gap note; removed the now-obsolete 001–011 index row. | Ken Ira Lacson Talingting |
| 2026-10-15 | Added DEC-20261015-015 (code-review findings as freeze-session inputs). | Ken Ira Lacson Talingting |
| 2026-10-15 | Added DEC-20261015-016 (SLSQP fallback diagnostic — finding 3 of 015 closed). | Ken Ira Lacson Talingting |
| 2026-10-15 | Added DEC-20261015-017 (Phase A relocations; 6-doc target). Added Appendix A (Experiment Registry Ledger) scaffold with EXP-H1-20261015-001 pointer. Fixed Index table formatting (gap note moved below table). Added Supersession note for DEC-20261015-013. Updated Conventions 3 and 5 to reflect registry relocation and exploratory non-counting. | Ken Ira Lacson Talingting |
| 2026-10-15 | Added DEC-20261015-018 (Phase C spec merges; source-file retirement). Added this row. | Ken Ira Lacson Talingting |
| 2026-10-17 | Added DEC-20261017-019 (audit findings F1–F8 as freeze-session inputs; documentation-integrity repairs). Added the missing DEC-20261015-018 Index row. Created Appendix B (absorbed items from retired `docs/TODO.md`). | Ken Ira Lacson Talingting |
| 2026-10-17 | Added DEC-20261017-020 (Tests B/C/D defined — resolves F6; freeze worksheet produced; findings N1–N3). | Ken Ira Lacson Talingting |
| 2026-10-17 | Added DEC-20261017-021 (freeze executed: `evaluation_protocol.md` v2.3 Frozen; `scope_and_non_goals.md` v1.3 Active; `risk_register_and_premortem.md` v1.2 Active; R1 scan extended in `problem_framing.md` v2.4). Updated Appendix B dispositions note. | Ken Ira Lacson Talingting |
| 2026-10-17 | Added DEC-20261017-022 (`model_and_method_spec.md` v1.0 Draft — C2; finding F9 resolved in scope's favour; protocol v2.4 §4.2 correction; scope v1.4). Updated Appendix B rows C1/C2/C3/D1/D2/D3/B3 to current state and added the DEC-022 update note. | Ken Ira Lacson Talingting |
| 2026-10-17 | Added DEC-20261017-023 (`model_and_method_spec.md` v1.1 Frozen — C3; all `[OPEN]` items O1, O2, O4–O7 resolved; v1.0's run-reproduction freeze condition corrected). Updated Appendix B row C3 and added the DEC-023 update note. | Ken Ira Lacson Talingting |
---

*This log exists to make decisions explicit, dated, and reviewable. Its append-only discipline is the reason it can be trusted. If the log is edited to hide a gap, the log is worthless. If the log records its gaps, the log is the project's strongest artifact.*
