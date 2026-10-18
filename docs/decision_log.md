# Decision Log — robustfolio

**Project:** `robustfolio`
**Owner:** Ken Ira Lacson Talingting
**Created:** 2026-10-14
**Version:** 1.16
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
| DEC-20261017-024 | 2026-10-17 | GOVERNANCE | ACTIVE | Confirm the point-in-time candidate universe (18 ETFs); accept the residual survivorship limitation |
| DEC-20261017-025 | 2026-10-17 | GOVERNANCE | ACTIVE | Build the immutable PIT snapshot; pass the §5.4.8 leakage suite; record findings F10–F12 |
| DEC-20261017-026 | 2026-10-17 | GOVERNANCE | ACTIVE | Confirm F10/F11 (rf conventions); register Test B and Test D; raise F13 (DSR trial count) and F14 (Test C period) |
| DEC-20261017-027 | 2026-10-17 | GOVERNANCE | ACTIVE | Resolve F13 (N = 1 confirmed) and F14 (Test C windows {36, 60} at the frozen anchor); register Test C |
| DEC-20261017-028 | 2026-10-17 | GOVERNANCE | ACTIVE | Rule the design diagnostics non-experimental; resolve F15 (report rho, no amendment); retract the "underpowered" claim |
| DEC-20261017-029 | 2026-10-17 | GOVERNANCE | ACTIVE | Resolve F16/F17/F18 (solver acceptance, Ledoit-Wolf ddof, initial w-minus); record the engine-core certificate and its near-miss |
| DEC-20261017-030 | 2026-10-17 | GOVERNANCE | ACTIVE | Land the walk-forward harness (spec 6); record findings F19-F23 (layout determinism, certificate nu, redundant L1 bound, risk-parity acceptance bypass, certification-evidence divergence) |
| DEC-20261017-031 | 2026-10-17 | GOVERNANCE | ACTIVE | Land the reporting layer (spec 7-8): metrics, inference, report, one reproducible command; record findings F24-F26 and the first exploratory end-to-end result |

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

### DEC-20261017-024

**Date:** 2026-10-17
**Type:** GOVERNANCE
**Status:** ACTIVE
**Authority:** Owner
**Related docs:** `notes/pit_universe_2026-10-17.md` (v1.0, Confirmed — confirmed by this entry), `notes/pit_candidates_2026-10-17.csv`, `evaluation_protocol.md` (v2.4, Frozen §5.4.2/§5.4.7), `model_and_method_spec.md` (v1.1, Frozen §3.3/§3.4), `scope_and_non_goals.md` (v1.4, §3.1), `docs/README.md` (v1.6), `risk_register_and_premortem.md` (v1.3), `notes/tests_BCD_spec_2026-10-17.md`, DEC-20261017-020, DEC-20261017-021, DEC-20261017-023
**Related risks:** R-D02, R-S02

**Context:**
Gate 1 entry (`evaluation_protocol.md` §8.4) requires the point-in-time candidate universe list (§5.4.7) and a passing §5.4.8 leakage suite. DEC-20261017-023 closed the documentation half and left exactly those two. This entry records the reconstruction and owner confirmation of the **candidate list** — the first of the two, and the last object that needed a decision rather than an execution.

**Decision:**
1. **Candidate universe confirmed at 18 instruments**, anchored at the backtest start (2012-06) with an inception cut-off of 2007-05-31: `SPY` `MDY` `IWM` `EFA` `EEM` `VNQ` `RWX` `GLD` `SLV` `DBC` `SHY` `IEF` `TLT` `LQD` `AGG` `TIP` `HYG` `MBB`. One liquid representative per bucket — equity 5, real estate 2, commodities 3, fixed income 8 — inside §5.4.2's 15–25 target. Inception dates are verified from issuer fact sheets and SEC EDGAR N-1A filings.
2. **The anchor is derived, not chosen.** §13.1's frozen bootstrap note (\(T = 168\) months) plus §4.3's 60-month window and §5.2's walk-forward force a 228-month record, 2007-06 … 2026-05: backtest start **2012-06**, first estimation window 2007-06 … 2012-05, inception cut-off **2007-05-31**. The competing reading (anchor = the 2007-06 data start → inception ≤ 2002-06) excludes every fixed-income, commodity, and real-estate instrument in scope — the earliest, `TLT`/`IEF`/`SHY`/`LQD`, launched 2002-07-22 — and is therefore unsatisfiable; resolved by satisfiability. Membership is invariant to a ±1-month anchor shift (nearest inception: `HYG`, 2007-04-04).
3. **O1 applied.** No cash / T-bill proxy: Phase 1's `BIL` is dropped; duration-bearing Treasuries stay. The Phase 1 `DEFAULT_UNIVERSE` in `src/robustfolio/data.py` therefore no longer matches the candidate list — a Gate 1/2 code change, not a documentation change (DEC-20261015-015).
4. **The residual survivorship limitation is accepted as documented.** The inception screen is objective; the in-scope closure record 2012–2026 is thin (closures are dominated by sub-$100 M, thematic, leveraged, and ETN products, all out of scope). The §5.4.8.2 survivorship test is therefore **vacuous in-sample** — exactly what §5.4.5 already anticipates ("no candidate delists in-sample"). The bias is **argued, not measured**: per §5.4.7 every result stays universe-conditional and the §5.4.7 downgrade clause is held in reserve. The owner declined the archived-PIT-screen upgrade (§5.4.1 forbids paid data without budget approval).
5. **No Tier-0 value changed.** The universe count is delegated by protocol §5.4.2 ("target 15–25") and scope §3.1, so no protocol, spec, or scope version bump is required.
6. **No `src/` or `scripts/` change.**

**Alternatives considered:**
- **Anchor at the data start (2007-06, inception ≤ 2002-06).** Rejected — unsatisfiable for the four required asset classes.
- **Trim fixed income to 16 (drop `AGG` and `MBB`).** Rejected — aggregate and MBS are distinct buckets (MBS adds prepayment risk) and 18 stays inside the target.
- **Phase 1 core only (14, ex-`BIL`).** Rejected — drops the size (`MDY`), aggregate, MBS, and silver buckets. The §4.3 \( \gamma \) derivation survives either way, since the sleeve structure and its collinearity are preserved.
- **Upgrade to archived 2007/2012 AUM+ADV screens.** Rejected by the owner — a paid source for a bounded, documented residual.
- **Assert the list is survivorship-free.** Rejected — that is the R-D02 failure mode: an unmeasured bias asserted away.

**Rationale:**
[First Principles] The anchor was derived from the frozen window arithmetic rather than picked, so the list needs no arbitrary date decision.
[Inversion] The survivorship question was attacked by asking what *should* be missing (delisted members) instead of asserting completeness; the honest answer — nothing in scope — is recorded as an argument, not a measurement.
[Experimental] The list is fixed before any result exists, so membership cannot be tuned to outcomes.
[Goodhart's Law] Confirming a "clean" universe is worth little unless the residual is stated; the note records both.

**Reversibility:** Soft. The list is a data artifact; a change requires a new decision-log entry. The anchor *reading* is recorded and could be restated without changing membership.

**Revisit trigger:**
An archived screen surfaces an in-scope ETF available at 2007-06 that later liquidated → add the member, exercise §5.4.5's delisting default, and re-run the §5.4.8.2 test. Or the harness's first-fold month moves the cut-off across an inception date (it does not, given `HYG`'s margin).

**Expected value assessment:**
- Probability the confirmed list is implementable in the snapshot with no membership change: high (~90%).
- Probability an in-scope, large, liquid, non-leveraged ETF available at 2007-06 later liquidated and is missing: low (~10–15%) — the in-scope closure record is thin but not exhaustively audited.
- Probability the residual later proves economically material for the out-of-sample comparisons: low (~10%), since all candidates are large and liquid throughout.
- Probability Gate 1 is now blocked only on the leakage suite: high (~95%).

**Pre-mortem:**
Six weeks from now this entry has failed in one of three ways. (a) The candidate list is expanded mid-backtest to chase a result — detectable by diffing the snapshot's `universe_pit.csv` against this entry. (b) A cash proxy reappears in the universe (e.g. `BIL` smuggled back in via the Phase 1 `DEFAULT_UNIVERSE`) — detectable by grepping the snapshot universe for §3.4's excluded tickers. (c) The "no in-scope delisting" finding is cited as proof the design is survivorship-free — detectable by checking that the note's §5 residual is quoted alongside it. All three are the failure modes this record exists to prevent.

---

### DEC-20261017-025

**Date:** 2026-10-17
**Type:** GOVERNANCE
**Status:** ACTIVE
**Authority:** Owner
**Related docs:** `notes/snapshot_and_leakage_evidence_2026-10-17.md` (v1.0, Evidence record — recorded by this entry), `src/robustfolio/data.py`, `scripts/build_snapshot.py`, `tests/test_leakage_suite.py`, `tests/conftest.py`, `evaluation_protocol.md` (v2.4, Frozen §5.4.8/§5.4.9/§8.4), `model_and_method_spec.md` (v1.1, Frozen §3), `notes/pit_candidates_2026-10-17.csv`, `docs/README.md` (v1.7), DEC-20261015-015, DEC-20261017-021, DEC-20261017-024
**Related risks:** R-D02, R-S02, R-E01, R-M05

**Context:**
DEC-20261017-024 confirmed the candidate list and left exactly one Gate 1 blocker: the §5.4.8 leakage suite, which could not run because no immutable snapshot existed. This entry records the snapshot builder, the point-in-time reader, the suite, and its pass. It is the **first `src/` / `scripts/` change since the freeze** (DEC-20261015-015 forbade pre-freeze code changes; the freeze completed in DEC-20261017-021, so the restriction no longer binds).

**Decision:**
1. **Snapshot built.** `yahoo-usetf-2007-01-01_2026-09-30-2026-10-17-2ad06139`, bundle SHA-256 `2ad06139…d707`: 18 candidates, 4,966 daily rows, 2,294 corporate actions (2 splits, 2,292 dividends), 4,941 `DGS1MO` observations. The window ends on the last **complete** month so no partial month enters a return.
2. **The §5.4.8 leakage suite passes: 14 passed, 1 skipped.** Items 1, 3, 4, 5 pass against real data; item 2 skips as **vacuous in-sample** (§5.4.5), with the mechanism verified separately so the check re-activates if the universe changes. No failing test → the Phase 1 experiment is unblocked.
3. **PIT contract implemented** per spec §3.1–§3.4 and protocol §5.4: `load_snapshot` never reaches the network and vendor specifics are isolated in one block; `Snapshot.truncated(t)` is the operational form of §5.4.3; splits back-adjust prices while cash dividends enter the return on the ex-date (§5.4.5); eligibility per §5.4.2; the risk-free rate is never zero-filled (§5.4.6); snapshots are append-only and hash-pinned (§5.4.9).
4. **Two conventions are not pinned by the frozen documents** and are therefore recorded as findings and defaulted, not silently chosen: **F10** `RF_ANNUAL_TO_MONTHLY = "geometric"` (`(1+y)^(1/12)-1`; alternative `y/12`), and **F11** `RF_ALIGN = "prior_month"` (the yield observed at the close of `t-1` prices month `t`; alternative is the literal §5.5.5 "observed at `t`"). Both set a value inside every net Sharpe ratio. The owner is asked to confirm or override; until then the defaults stand and are stamped into every snapshot manifest.
5. **F12 recorded.** The §5.4.2 `ADV > $5M` floor is binding on `RWX`, whose dollar volume falls from $15–28 M (2012–2020) to $0.99 M (2026). The **eligible** set is 18 for 2012-06…2021-11 and 17 thereafter. The frozen rule is working as written; the consequence — a time-varying investable set and a real, costed divestment — is recorded for the owner before Gate 2. No decision is required to proceed.
6. **Pre-mortem item (b) of DEC-20261017-024 is closed in code.** The Phase 1 `DEFAULT_UNIVERSE` (which contained `BIL`) is renamed `PHASE1_UNIVERSE` and quarantined under a `LEGACY` banner; nothing on the confirmatory path can reach it. The confirmatory universe is the snapshot's `universe_pit.csv` only.
7. **No Tier-0 contract value changed.** The protocol, spec, and scope are not amended; no version bump.

**Alternatives considered:**
- **Hold the leakage suite until the full Phase 2 rewrite.** Rejected — §5.4.8 blocks experiments, and the suite is the cheapest way to falsify the data layer *before* any result exists.
- **Treat the §5.5.5 conversion as obvious and skip the finding.** Rejected — that silently fixes a value inside every net Sharpe ratio; the standing rule (F1–F9 precedent) is that frozen-value gaps are surfaced, not absorbed.
- **Drop `RWX` from the candidate list so the universe stays 18.** Rejected — that is membership tuning after observing data. The list is fixed by DEC-20261017-024; eligibility is applied by the frozen rule, not negotiated.
- **Use the Phase 1 shortcut (`auto_adjust=True` adjusted closes).** Rejected — protocol §5.4.4/§5.4.10 make retroactively adjusted prices an invalidation. Raw unadjusted prices plus ex-post corporate actions is the frozen two-tier contract.
- **Register Tests B/C/D in Appendix A now that a snapshot ID exists.** Deferred, not rejected — §12.4's precondition is met, but the registrations belong with the harness that runs them, not with the data layer.

**Rationale:**
[First Principles] The suite is a falsifier for the data layer, and it earned its keep: two real defects (month-end prices read from *raw* rather than split-adjusted closes — worth a spurious −49 % month; and a genuine `DGS1MO` 0.00 misread as a forbidden zero-substitution) were caught before any number was computed, which is exactly when they are cheapest.
[Inversion] Rather than assert the snapshot is leak-free, the suite constructs the leak — a dividend with an ex-date after `t` **does** change a naive whole-sample result — and shows the pipeline is immune to it. A test that cannot fail proves nothing.
[Baseline-first] The cheapest satisfiable data (Yahoo raw + FRED) was made to meet the frozen contract before any paid source was considered (§5.4.1).
[Probabilistic] The derived anchor is now confirmed by data, not only by window arithmetic: all 18 candidates are eligible at 2012-06-29 and **none** is eligible in the 65 preceding months.

**Reversibility:** Soft for the code; hard for the snapshot. Snapshots are append-only, so the `…-2ad06139` bundle is never modified — a corrected retrieval creates a new snapshot ID and this entry remains the record of what was used.

**Revisit trigger:**
The owner confirms or overrides F10/F11 → the constants change and a new snapshot is built (the manifest stamps the conventions, so a mixed pair is detectable). Or Yahoo/FRED restates history → new snapshot. Or the §5.4.8.2 test activates (a candidate delists) → implement the survivorship check before any further run.

**Expected value assessment:**
- Probability the suite would have passed without the two defects having been fixed: low (~15 %); the split branch is exercised by real `EEM` (3:1) and `SLV` (10:1) 2008 splits.
- Probability F10/F11 are immaterial to the H2 comparison (both methods share one `R_f`): high (~95 %).
- Probability F12 changes a test outcome materially: low (~10 %); it does change the investable set for 48 of 172 OOS months, so it must stay visible.
- Probability the snapshot reproduces byte-for-byte on a fresh retrieval: moderate (~60 %) — vendor series are restated over time, which is precisely why the values are pinned and a new retrieval yields a new ID.

**Pre-mortem:**
Six weeks from now this entry has failed in one of four ways. (a) The suite is re-run against a *live cache* rather than the snapshot, so it validates nothing — detectable by asserting `load_snapshot` is the harness's only data entry point. (b) F10/F11 are quietly frozen by usage before the owner confirms them — detectable by diffing the constants against this entry and the manifest. (c) A later `src/` change re-introduces `auto_adjust=True` or a `BIL` cash proxy — detectable by grepping the confirmatory path for `PHASE1_UNIVERSE` and `auto_adjust`. (d) F12's shrinking universe is cited as "a 17-asset universe" with no note that it was 18 — detectable by requiring the note's §4 table alongside any universe count.

---

### DEC-20261017-026

**Date:** 2026-10-17
**Type:** GOVERNANCE
**Status:** ACTIVE
**Authority:** Owner
**Related docs:** `notes/snapshot_and_leakage_evidence_2026-10-17.md` (v1.1, confirmed by this entry), `notes/tests_BCD_spec_2026-10-17.md`, `evaluation_protocol.md` (v2.4, Frozen §6, §12.4, §12.6, §12.9), `model_and_method_spec.md` (v1.1, Frozen §1, §2), `docs/README.md` (v1.8), DEC-20261015-014, DEC-20261015-015, DEC-20261017-024, DEC-20261017-025
**Related risks:** R-M01, R-M02, R-D05, R-P01, R-S02

**Context:**
DEC-20261017-025 closed both Gate 1 data blockers and left two risk-free conventions (F10, F11) awaiting owner confirmation. Protocol §12.4 requires a snapshot ID in every registration, and had none until that entry; so the Tests B/C/D registrations — deferred by DEC-20261017-020 and by DEC-20261017-025's alternative list — became writable for the first time. This entry records the confirmations and the first two registrations, and reports two findings that block the third.

**Decision:**
1. **F10 confirmed: `RF_ANNUAL_TO_MONTHLY = "geometric"`** (`(1+y/100)^(1/12)-1`).
   **F11 confirmed: `RF_ALIGN = "prior_month"`** (the yield observed at the close of `t-1` prices month `t`, consistent with §5.5.4).
   Both were the implemented defaults, so **no code change and no new snapshot** — the built snapshot's manifest already stamps the confirmed conventions. Both findings are closed.
2. **Test B registered** — `EXP-X-20261017-001` in Appendix A. Family **X**, so it does **not** count toward any denominator (§12.6.2). Cap sweep `w_max ∈ {0.20, 0.30, 0.40, 1.00}`, applied uniformly in every arm, everything else at the common configuration.
3. **Test D registered** — `EXP-H2-20261017-001` in Appendix A. Family **H2/H3**, **counts**. Family size at registration **N = 1** (zero prior confirmatory trials in the family per DEC-20261015-014 + 1; §12.6.1).
4. **Test C is *not* registered.** It cannot be pre-registered honestly yet — see **F14**.
5. **Findings raised:**
   - **F13 — the DSR trial count for a multi-method registration is not pinned.** §12.6 fixes the *family denominator* (registered confirmatory trials = 1 here, per DEC-20261015-014), but §12.7's DSR also needs the number of trials from which the reported maximum was selected. Test D reports the best of **two** candidate methods (`M1`, `M2`) against five baselines. Registering with `N = 1` follows the frozen rules literally; if the owner intends `M1`/`M2` to be separate trials, the registration must be **amended before execution** (§12.9 permits pre-run amendment via a new registration ID; §12.11 invalidates only post-execution edits). Flagged because §12.11 makes a wrong family-size count fatal to the adjustment.
   - **F14 — Test C's window sweep has no common evaluation period.** The spec (Tests B/C/D §1) requires all arms to share an identical period. With data starting 2007-01 and a rolling estimation window, the first feasible out-of-sample month is 2010-06 (36-month window), 2012-06 (60), and 2017-06 (120). The three arms are therefore **not comparable as written**, and the 120-month arm discards five years of the sample relative to the frozen protocol. Two options, both with a cost: (a) hold every arm to the common window 2017-06…2026-05 (108 months, 9 folds) — comparable, but abandons 2012-06…2017-05 for a diagnostic that exists to characterise the *frozen* 60-month setting; or (b) let each arm run its own period and report them as three separate diagnostics rather than one comparison — no information lost, but the "window artifact" question is then answered by three mutually non-comparable numbers. **Owner decision required before Test C is registered.**
6. **No Tier-0 contract value changed; no protocol, spec, or scope amendment.** Test B and Test D registrations are ledger entries, not contracts.

**Alternatives considered:**
- **Fold the F10/F11 confirmation into DEC-20261017-025.** Rejected — entries are append-only and 025 recorded the findings as *outstanding*; a confirmation is a new act, not an edit of the old one.
- **Register Test C at the 2017-06 common window without asking.** Rejected — it silently discards five years of the frozen protocol's evaluation period to serve an exploratory diagnostic, which is exactly the kind of parameter choice that should be the owner's.
- **Register Test D with `N = 2` (two candidate methods).** Rejected for the registration as written — the frozen rules define the denominator as *registered confirmatory trials* (§12.6), and DEC-20261015-014 defines those as confirmatory EXPERIMENT entries in this log. Recorded as F13 so the choice is the owner's, not an accident of the registration.
- **Defer all three registrations until the Phase 2 harness exists.** Rejected — §12.1 is "lock before you look"; a registration written after the code exists is a registration written by someone who has already seen how it runs.

**Rationale:**
[First Principles] A registration's only value is that it was written while the outcome was still unknown. The snapshot ID and the frozen thresholds were the last missing inputs; with both present, deferring further would erode the lock.
[Inversion] The failure mode is not "a missing registration" but "a registration whose parameters were chosen after the sweep" — so Tests B and C are registered **before** any harness exists, and the firewall (§5 of the spec) is quoted in the entry itself.
[Goodhart's Law] F13 is recorded rather than resolved because resolving it conveniently (N = 1) is the direction that makes success easier to declare. The owner should be the one to accept that.
[Systems] F14 surfaced only because the registrations were written before the code: the window sweep's period-misalignment is invisible in prose and unavoidable in a run.

**Reversibility:** Soft. Registrations are append-only ledger entries; Test D's `N` may be amended before execution under §12.9 (new registration ID). F10/F11 are confirmed values in code and in the manifest of an append-only snapshot — a later change requires a new snapshot and a new entry.

**Revisit trigger:**
The owner answers F13 → Test D's registration is amended before execution (or left as `N = 1`). The owner answers F14 → Test C is registered, or the Tests B/C/D spec is amended at its §3. The Phase 2 harness becomes runnable → execution may begin only with a completed registration for every reported metric (§12.2).

**Expected value assessment:**
- Probability the confirmed F10/F11 values are the ones used in the confirmatory run: high (~99%) — they are already in code and stamped in the manifest.
- Probability `N = 1` is the value the owner intends after reading F13: high (~70%) — it follows the frozen rules literally; the remaining ~30% is the `M1`/`M2`-as-two-trials reading.
- Probability the owner chooses a common period and Test C loses the 2012-06…2017-05 stretch: moderate (~50%).
- Probability Test B or Test D must be amended before execution: moderate (~40%) — both are written against a harness that does not yet exist, so a parameter will likely need restating rather than changing.

**Pre-mortem:**
Six weeks from now this entry has failed in one of four ways. (a) Test D is executed with `N = 1` while `M1` and `M2` were effectively two searches — detectable by checking whether the results section reports a best-of-several selection and whether F13 was answered. (b) Test C is registered at whichever period produced the more striking window story — detectable by checking the registration predates the run and that its period rule is the one recorded here, not a later choice. (c) The registrations are quietly edited after a run to match what was run — detectable because the pre-registration fields are immutable (§12.3) and the ledger is append-only. (d) The Phase 2 harness is built and run without amending the registrations at all, so the numbers reported are for an unregistered configuration — detectable by diffing the harness's frozen config against the entries' field 3.

---

### DEC-20261017-027

**Date:** 2026-10-17
**Type:** GOVERNANCE
**Status:** ACTIVE
**Authority:** Owner
**Related docs:** `evaluation_protocol.md` (v2.4, Frozen §5.2, §12.6, §12.7, §12.9), `notes/tests_BCD_spec_2026-10-17.md` (§3 amended, §9 addendum), `decision_log.md` Appendix A (`EXP-X-20261017-002`), `docs/README.md` (v1.9), DEC-20261015-014, DEC-20261017-026
**Related risks:** R-M01, R-M02, R-E04, R-S02

**Context:**
DEC-20261017-026 registered Test B and Test D and raised two findings that blocked the third registration. Both are questions of *measurement*, not of data: neither could be settled by reading the frozen documents, and both were raised with the convenient answer (N = 1; a period chosen to make the sweep work) separated from the correct one. The owner has answered both.

**Decision:**
1. **F13 resolved: `N = 1` confirmed.** The DSR trial count for `EXP-H2-20261017-001` is 1, per §12.6 and DEC-20261015-014 (the denominator is the count of registered **confirmatory trials**, of which Test D is the first). Reporting the best of `M1`/`M2` is a *reporting* choice within one registration, not two trials. **The registration stands exactly as written — no amendment is required**, so the risk that §12.11 attaches to a corrected family size is closed.
2. **F14 resolved: Test C runs windows `{36, 60}` over the frozen out-of-sample period 2012-06 … 2026-05.** The 120-month arm is **dropped**, not deferred. Both arms therefore share an identical period, satisfying the B/C/D spec §1 "identical period" rule exactly, and remain comparable with Tests B and D. The 60-month arm reproduces Test D's `B3`/`B5` configuration under the same data and period, giving a free internal consistency check.
3. **Rationale for dropping rather than relocating the 120-month arm.** A 120-month estimation window needs 120 months of history before its first out-of-sample month. The confirmed universe's latest inception is `HYG` (2007-04), so the earliest possible first OOS month is 2017-06 and the arm exists only by moving the whole of Test C five years later than the frozen protocol. That is not a free choice: it would make Test C's evidence base different from the protocol's for a diagnostic whose entire purpose is to characterise the *frozen* 60-month setting. A defect removed by discarding the defective arm is preferable to a deviation carried for an exploratory result.
4. **The spec's §3 decision rule is amended** for two arms (persists at both → not a window artifact; only at 60 → artifact; only at 36 → inverted, Phase 1 not reproduced). Recorded in the B/C/D spec §9 and restated verbatim in the registration's field 5.
5. **Test C registered** — `EXP-X-20261017-002`, family **X** (§12.6.2: non-counting, 2 arms, both reported).
6. **Limitation recorded.** Two arms cannot distinguish a monotone window trend from a threshold effect, and the 36-month arm sits below the frozen 60-month recommendation, so the sweep tests sensitivity *downward* only. The window sweep is therefore weaker evidence than a three-arm sweep would have been; the condition-number diagnostic in the same entry carries the complementary part of the answer. This is stated so that a later reader does not read a two-point "not a window artifact" verdict as strong.
7. **No Tier-0 contract value changed.** §5.2's frozen 60-month window is untouched; only an exploratory diagnostic's arm list changed.

**Alternatives considered:**
- **Relocate all three arms to the common window 2017-06…2026-05** (keeps the 120-month arm; arms mutually comparable). Rejected — abandons 2012-06…2017-05 and makes Test C's period differ from Tests B/D and from the frozen protocol, for a purely exploratory verdict.
- **Report three separate single-arm diagnostics over their own maximal periods.** Rejected — no comparable number answers the question the test exists to answer; the closest of the three options to the §12.10 exploratory failure mode.
- **Keep the 120-month arm and let its OOS start later than the others.** Rejected — this is option 1 by another name, and it makes the arms non-comparable, which §1 forbids.
- **Set `N = 2` for Test D to be conservative.** Rejected — §12.6 and DEC-20261015-014 define the denominator as registered confirmatory trials; adopting 2 would inflate the denominator to buy conservatism, which is the same error as deflating it to buy significance. If a two-candidate selection needs its own correction, that is a *method* finding (a §12.7 definition gap), not a denominator change — and it is recorded as such in F13's closure below.
- **Leave Test C unregistered indefinitely.** Rejected — an unregistered diagnostic that later informs anything is a §12.10 violation waiting to happen.

**Rationale:**
[Inversion] Both findings were settled by asking which error the *frozen rules* were written to prevent: F13 by refusing to trade a denominator for convenience in either direction, F14 by refusing to carry a deviation that exists only to keep a weak arm alive.
[First Principles] The universe's 2007 inception is a hard constraint, not a preference. A 120-month window at a 2012-06 anchor is arithmetically impossible, so the choice was never "which window" but "which period" — and the protocol already owns the period.
[Goodhart's Law] Test C is exploratory and cannot support a success claim; its only failure mode is being *cited* as if it could. Making it explicitly weaker (two arms, an inverted verdict available, a recorded limitation) reduces that risk rather than raising it.
[Information Theory] Discarding the infeasible arm removes a parameter whose value would have been determined by an unrelated constraint, which is noise dressed as a dimension.

**Reversibility:** Soft. Test C is append-only and unexecuted; dropping the 120-month arm is a decision about a registration, not about data or code. If the universe is ever extended with a pre-2007 instrument, a *new* registration can add the arm at the frozen anchor.

**Revisit trigger:**
An amended or extended universe makes a 120-month window feasible at the 2012-06 anchor → register a new Test C with three arms rather than editing this one. Or Test C returns a "window artifact" verdict at 60 months → the §5.2 window recommendation is reopened (a protocol matter, per §16), not silently accepted. Or Test D's results show the `M1`/`M2` selection mattered → open the §12.7 definition gap as a method finding.

**Expected value assessment:**
- Probability `N = 1` is the value ultimately used in the confirmatory DSR: high (~90%) — now owner-confirmed rather than merely registered.
- Probability Test C's two-arm sweep produces a decisive verdict (artifact / not) rather than an ambiguous one: moderate (~50%); the recorded limitation anticipates the ambiguous case.
- Probability the dropped 120-month arm would have changed Test C's verdict had it been feasible: low-to-moderate (~30%).
- Probability the 60-month arm reproduces Test D's `B3` numbers exactly: high (~95%) — same snapshot, same window, same cap, same cost model; a mismatch would indicate a harness defect, which is the point of the check.

**Pre-mortem:**
Six weeks from now this entry has failed in one of four ways. (a) Test C's two-point sweep is cited as "the window artifact was ruled out" — detectable by checking the limitation in point 6 is quoted alongside any such claim. (b) The dropped 120-month arm is quietly reintroduced during implementation because it is easy once a longer history is fetched — detectable by diffing the harness's arm list against the registration. (c) `N = 1` is revisited *after* Test D's results are known — detectable because §12.9 permits pre-run amendment only, and this entry records the confirmation date. (d) The restated decision rule for two arms is applied with "all three windows" language left in the code or the report — detectable by grepping the harness and report text for the three-arm phrasing.

---

### DEC-20261017-028

**Date:** 2026-10-17
**Type:** GOVERNANCE
**Status:** ACTIVE
**Authority:** Owner
**Related docs:** `notes/power_and_effective_bets_2026-10-17.md` (v1.0 → v1.1, recorded by this entry), `scripts/diagnostics_power.py`, `evaluation_protocol.md` (v2.4, Frozen §4.3, §6.1–§6.3, §12.2, §12.6.4, §12.9, §13.1), `decision_log.md` Appendix A, `docs/README.md` (v1.10), DEC-20261017-026, DEC-20261017-027
**Related risks:** R-M01, R-M02, R-E04, R-S02

**Context:**
DEC-20261017-027 completed the registry. The next question was whether the registered tests can detect the effect they exist to detect. That question needed no model and no harness — only the eigen-spectrum of the covariance and the sampling theory of Sharpe *differences* — so it was answered before any experiment ran, which is the point. It also changed a conclusion reached in discussion earlier the same day, so it is recorded rather than left in chat.

**Decision:**
1. **Ruling (§12.2): the design diagnostics are not an experiment and not a registry entry.** `scripts/diagnostics_power.py` forms no portfolio, produces no strategy return series and reports no performance metric; every number is a property of the data or of the test design, and the values would be identical if `M1`/`M2` had never been proposed. It cannot be cited for or against H1–H3 and does not count toward any denominator. Recorded so that a later reader cannot mistake it for an unregistered run.
2. **`notes/power_and_effective_bets_2026-10-17.md` v1.0 adopted as a design input** (v1.1 as of this entry).
3. **F15 raised and resolved — reading (a): design diagnostic, no amendment.** ρ(candidate, best baseline) must be reported in the **design/detectability appendix** accompanying any Test D result, and a null result with ρ < 0.98 at the §6.2 threshold is labelled **UNDERPOWERED / inconclusive**, not negative. It is **not** added to the registered metric set: §12.6.4's "any … metric" is read as protecting the decision-relevant metrics, and ρ cannot support or defeat a claim. `EXP-H2-20261017-001` is therefore **not amended** and its family size stays **N = 1**.
4. **A correction is recorded.** The claim made in discussion that the project is "underpowered for a 0.2 Sharpe claim" is **retracted** as too pessimistic: the paired design detects the §6.2 threshold at ≥ 80% power for ρ ≥ 0.98, and the level test's ≈ 0.67 requirement is cleared by the candidates' realised Sharpes (0.06–1.09, median 0.45). The design is silent only about improvements below ≈ 0.13.
5. **Three measured facts are recorded as inputs to the problem framing and to the eventual writeup:**
   - the universe carries **`N_part` 3.14 / `N_ent` 5.03** independent directions overall, stable per fold at 2.45–3.91 / 4.13–5.71, with the market factor at 50.5% of variance and 6 factors needed for 90%;
   - **12 of the 18** sample eigenvalues fall below the Marchenko–Pastur lower edge (0.452) for an *independent* 18 × 168 panel, the smallest being **85× below it** — so the H1 premise is **supported by the data rather than assumed**;
   - under the null the §6.3 fold gate passes **21.2%** of the time (≥ 9 of 14, independent folds; higher with the positive fold correlation), so it is a **weak discriminator** and must not be presented as independent evidence.
6. **No frozen document is amended.** The ρ requirement lands in a design appendix, not in the spec's §8 reporting interface. `evaluation_protocol.md` (v2.4), `model_and_method_spec.md` (v1.1) and `scope_and_non_goals.md` (v1.4) are unchanged. If ρ is later wanted inside the *required* report, that is a separate versioned spec amendment.

**Alternatives considered:**
- **Treat ρ as a registered secondary metric and amend pre-run (reading b).** Rejected — §12.6.4 read literally raises the denominator to N = 2 for adding a statistic that can only make the report *more* honest, so the more transparent the reporting the higher the bar. Recorded because the reading is defensible and its perversity is the reason it was rejected, not because it is unreasonable.
- **Leave ρ unreported.** Rejected — a null would then be published without its power caveat, and an underpowered test would read as evidence of no effect. That is the §12.10 failure mode wearing a confirmatory label.
- **Put ρ into the Frozen spec's §8 reporting interface.** Deferred, not rejected — it would require a versioned amendment to a Frozen document for a statistic that is not decision-bearing. Revisit if ρ ever enters a decision rule.
- **Omit the retraction because the claim was only made in conversation.** Rejected — the log records retractions elsewhere (DEC-20261015-014), and an analysis whose errors are not logged is not an analysis.
- **Build the diagnostics inside the Phase 2 harness.** Rejected — it would have delayed the one output that is independent of how Test D lands, and it would put the diagnostic inside the thing it is meant to check.

**Rationale:**
[First Principles] The decisive quantities — the eigen-spectrum of Σ and the sampling variance of a Sharpe difference — are properties of the data and of the test, not of any method. They were therefore computable before the harness existed, and being computable early is what makes them useful.
[Inversion] The failure mode is not an uninformative result but an **uninterpretable** one: a null that cannot be distinguished from an underpowered test. ρ is the quantity that separates them.
[Bayesian Updating] The earlier claim was updated by its own arithmetic and the update is recorded. A project that demands calibrated uncertainty from its model must apply the same standard to its own prose.
[Goodhart's Law] Reading (b) makes success harder to declare *and* easier to look rigorous — the shape of a rule that gets worked around. Reading (a) leaves the restriction where the protocol put it (decision-relevant metrics) and adds the diagnostic outside it.
[Baselines and Opportunity Cost] The whole diagnostic is one script and one note with no model, and it yields a result that survives either Test D outcome. That is a better return per unit of effort than any further protocol work.

**Reversibility:** Soft. The §12.2 ruling and the F15 resolution are append-only. If ρ is later wanted inside the required report, a versioned spec amendment supersedes point 6 without disturbing anything else.

**Revisit trigger:**
Test D returns a null with ρ < 0.98 → the result is labelled underpowered and the §6.2 threshold, not the method, becomes the finding. Or Test D returns ρ < 0.95 → the minimal-difference design did not deliver the expected correlation and the power assumption in the registration's field 4 is revisited on new evidence. Or ρ enters a decision rule → point 6's deferral expires.

**Expected value assessment:**
- Probability ρ lands ≥ 0.98 for the best candidate/baseline pair: moderate (~60%) — the one-component difference makes high correlation likely but not certain.
- Probability the effective-bets figure (3–5 directions, not 18 assets) changes how a reader interprets the eventual result: high (~85%).
- Probability the Marchenko–Pastur comparison was necessary to establish the H1 premise rather than assert it: high (~80%).
- Probability the fold gate proves decision-relevant despite the 0.212 null rate: low (~15%).

**Pre-mortem:**
Six weeks from now this entry has failed in one of four ways. (a) Test D is reported without ρ, so a null is read as "no effect" — detectable by checking that the design appendix accompanies the result. (b) The 21.2% fold-gate rate is quoted as if it implicated the DSR adjustment — detectable because the two are conjunctive and only §6.1 controls Type I. (c) The effective-bets figure is quoted as "the universe has 3 assets" rather than "3–5 effective directions among 18 candidates" — detectable by requiring the candidate count to travel with the effective count. (d) The diagnostic is quietly re-run with a different ρ assumption until the power looks good — detectable because the assumption is written down in the note's §3(b) and changing it is an amendment.

### DEC-20261017-029

**Date:** 2026-10-17
**Type:** GOVERNANCE
**Status:** ACTIVE
**Authority:** Owner
**Related docs:** `model_and_method_spec.md` (v1.1, Frozen, §1, §4.2, §4.3, §5.1, §5.3, §5.6, §5.7), `evaluation_protocol.md` (v2.4, Frozen, §4.3, §4.4, §5.4.8), `src/robustfolio/config.py`, `src/robustfolio/estimators.py`, `src/robustfolio/optimize.py`, `tests/test_conformance.py`, `scripts/certify_engine.py`, DEC-20261015-016, DEC-20261017-019
**Related risks:** R-E01, R-E04

**Context:**
The Phase 2 rewrite began with the engine core (estimators and constructors) rather than with the harness, because every defect in this project's history lived at the estimator/optimizer/backtest boundary: the SLSQP fallback (DEC-20261015-016), the expanding window inside the test period, and the fair-comparison defect where the cap was applied to some methods and not others (DEC-20261017-019). Implementing §5.6's acceptance test literally then exposed three values the frozen documents cannot supply, and one defect in the new code.

The defect is recorded first because it is the one that nearly went unnoticed. The optimality certificate was written with the multipliers of the `g(w) <= 0` constraints *added*, which is correct for a minimisation and wrong for a maximisation. The sign error would not have changed any weight, any turnover figure or any Sharpe ratio: it would only have turned the certificate into a rubber stamp that accepted whatever the solver returned. It was caught by a test that checks the residual against a hand-derived interior optimum and against a point known to be optimal by direct search. Recorded because a project whose central claim is "we verify the optimiser" cannot leave the verification's own near-miss unlogged.

**Decision:**
1. **F16 resolved -- reading (a): keep `sklearn` as specified.** M1's Σ is the sklearn Ledoit-Wolf estimate, whose base empirical covariance uses `ddof=0`, while §4.2 pins the sample covariance to `ddof=1`. M1 therefore differs from B3 by the shrinkage *and* by a factor `T/(T-1)` in the base (about 1.7% at `T = 60`). The discrepancy is documented in `estimators.py`, quantified, and left in place. It is deliberately **not** silently rescaled: the spec names the sklearn estimator, and a correction applied without a versioned amendment would be a larger violation of §1's design rule than the confound it removes.
2. **F17 resolved -- reading (a): explicit tolerance, KKT residual in place of the duality gap.** §5.6 requires three things that cannot all hold. (i) It pins "Tolerance: solver defaults"; on the frozen universe the defaults return a KKT residual of about `1.2e-4`, three orders of magnitude above the required `1e-7`, so the default reading rejects every fold. (ii) It requires a "duality gap <= 1e-7"; CLARABEL does not expose one (`solver_stats.extra_stats` is `None`). The operating point is fixed at `SOLVER_TOL = 1e-14`, which delivers `1.9e-12`; `1e-16` is *worse* (`4.4e-6`, because the solver degrades to `optimal_inaccurate`). `ACCEPT_TOL = 1e-7` remains the binding acceptance test, and the duality gap is replaced by a KKT residual computed from the primal solution alone. For a convex QP these conditions are sufficient, so it is an equivalent certificate, and being solver-independent it is a stronger one than the quantity it replaces.
3. **F18 resolved -- reading (a): the out-of-sample period starts flat.** The initial `w^-` at the first rebalance (2012-06) is unpinned. It is fixed at `w^- = 0`: the strategy begins from cash, the first rebalance buys 100% and pays one month of the 10 bps headline cost, and every method pays the same entry cost so the comparison stays fair. Under `w >= 0` this makes B5's L1 penalty exactly constant at that rebalance, so B5's first month equals unpenalised MVO -- which is correct, since there is no prior holding to penalise. `optimize.mean_variance` continues to **raise** when `turnover_penalty > 0` is passed without an explicit `w_prev`; the value is supplied by the caller and logged, never defaulted inside the library.
4. **Evidence recorded.** `scripts/certify_engine.py`, against the frozen snapshot: **168 rebalances x 6 solver-backed methods = 1008 solves, zero failures**; worst KKT residual `2.97e-11` (B4), `3400x` inside the acceptance tolerance; max constraint violation `7.8e-15`; `cond(Sigma_hat)` `1.30e4` to `6.09e5`; universe 17-18 assets; zero estimation windows skipped. Test suite: 37 passed, 1 known skip (the §5.4.8 item 2 vacuity recorded in DEC-20261017-025).
5. **The cap genuinely binds for B2, and this is a finding in its own right.** Risk parity was box-constrained on **154 of 168** rebalances. The §5.3 log-barrier formulation carries no `1'w = 1` constraint -- the scale is set by the balance between the quadratic and the barrier -- so the cap cannot be applied to the unnormalised solution, whose normalisation factor is about 30x here. The implementation pushes the cap through the normalisation by a convex homotopy (bisect the unnormalised cap level until the normalised maximum equals `w_max`, each step a convex coordinate descent). Had this been implemented as a naive cap on the unnormalised weights, B2's baseline would have been an infeasible portfolio in 92% of Test D's months, and the error would have looked like a result.
6. **No frozen document is amended by this entry.** The three resolutions are implementation decisions *within* §5.6's intent, and F16 and F18 concern values the documents do not state. The one place where the implementation now contradicts a frozen sentence is §5.6's "Tolerance: solver defaults", which this entry supersedes in practice. Correcting the sentence is a versioned spec amendment and is deferred to the next spec revision rather than made unilaterally here.

**Alternatives considered:**
- **F17, keep solver defaults and loosen the acceptance tolerance to what they deliver (about `1e-3`).** Rejected -- it makes §5.6's acceptance clause nearly vacuous, which is the opposite of its stated purpose, and it would license exactly the unverified solves the clause exists to reject.
- **F17, report the residual relative to the problem's natural gradient scale.** Rejected for now, not refuted. It is scale-robust and would have the same effect, but it changes the meaning of the `1e-7` threshold and therefore needs its own confirmation; the absolute form was confirmed instead.
- **F17, solve the dual and compute a literal duality gap.** Rejected -- it doubles the solves, and the gap would then be limited by the accuracy of *both* primal and dual, so it is a weaker certificate than a primal-only KKT residual at the same cost.
- **F16, rescale sklearn's output by `T/(T-1)` so M1 differs from B3 in exactly one component.** Deferred, not refuted: it is arguably what §1 intends, but it requires amending a Frozen section to make the code match the design rule, and the confound it removes is 1.7% on the covariance's scale while the treatment (shrinkage at `delta` up to 0.99) moves it by orders of magnitude.
- **F18, start already invested at `1/N`.** Rejected -- it assumes a holding the out-of-sample period never established, and it exempts every method from an entry cost the first month actually incurs.
- **Leave the three findings as in-code comments only.** Rejected -- an unpinned value chosen in a docstring is a silent choice with better manners. The F1-F15 precedent is that these are raised for ruling.
- **Silently fix the certificate's sign error and not mention it.** Rejected -- see Context. The near-miss is the most informative thing that happened in this work package.

**Rationale:**
[First Principles] The spec's acceptance clause is a claim about the *solution*, not about the solver's self-report. Once that is read plainly, "solver defaults" cannot be load-bearing, because the defaults demonstrably do not produce a solution that passes the clause. Reading the clause as binding and the tolerance as instrumental resolves the conflict in the only direction that preserves the clause's purpose.
[Inversion] The failure mode here is not a wrong weight, it is a *false certificate*: an acceptance check that passes on every input is indistinguishable from a correct one until the day it is not. Both the sign error and the "solver defaults" conflict are instances of the same failure shape, and both were found by asking what would have to be true for the check to be wrong.
[Baselines and Opportunity Cost] `1e-14` rather than `1e-12` cost nothing (22 s for 1008 solves) and moved the worst residual from `5.6e-7`, a factor of 5 inside the threshold, to `3.0e-11`, a factor of 3400. Optimum-seeking at that margin is free.
[Goodhart's Law] A tolerance chosen to make the acceptance test pass is a quantity being measured becoming a target. It is defensible only because the *direction* was fixed first (tighter is better) and the chosen value is near the point where the solver starts to degrade, not at the loosest value that passes.
[LLN / Sample Complexity] 1008 certified solves across 168 rebalances and 14 folds is the evidence that the operating point is not tuned to one window. One certified fold would have proved nothing.

**Reversibility:** Soft. Points 1-3 are implementation-level and can be revised by a later entry without touching a frozen document. Point 6 is explicitly deferred, so the spec's §5.6 text is to be corrected at the next versioned revision.

**Revisit trigger:**
Any rebalance fails to certify at `SOLVER_TOL = 1e-14` in any later run -> the operating point is re-opened and the failing fold is examined before any tolerance is moved. Or the next spec revision is opened -> §5.6's "Tolerance: solver defaults" sentence is corrected there. Or a reviewer argues that M1's `T/(T-1)` base factor exceeds the shrinkage treatment in the M1-vs-B3 comparison -> F16's deferral expires and the estimator is amended.

**Expected value assessment:**
- Probability the certificate would have accepted a genuinely wrong solution at some point without the analytic test: moderate (~40%) -- the sign error survived a full writing pass and only failed once a known-optimal point was checked against it.
- Probability the "solver defaults" reading would have been implemented literally by a careful reader of §5.6: high (~70%) -- the sentence is unambiguous, and it is wrong.
- Probability B2's cap binds under the frozen configuration: ~100% (measured: 154 of 168).
- Probability the naive unnormalised cap would have been the first implementation attempted: high (~75%) -- it is the obvious reading and it is wrong by a factor of about 30 in scale.
- Probability a reviewer notices F16's confound without it being recorded: low (~20%).

**Pre-mortem:**
Six weeks from now this entry has failed in one of four ways. (a) `SOLVER_TOL = 1e-14` is treated as a frozen constant and a fold fails on new data with no one remembering it was chosen empirically -- detectable because the measured table is in `config.py` next to the value. (b) M1's `T/(T-1)` confound is described in the write-up as "shrinkage only" -- detectable by checking the estimator's docstring against the claim. (c) §5.6 still reads "Tolerance: solver defaults" and a future reader takes the spec over the code -- detectable by grepping the spec for the sentence before any milestone. (d) The certificate's sign convention is copied into the walk-forward harness with the same inversion -- detectable because the analytic test lives in the suite, not in the function.

---

### DEC-20261017-030

**Date:** 2026-10-17
**Type:** GOVERNANCE
**Status:** ACTIVE
**Authority:** Owner
**Related docs:** `model_and_method_spec.md` (v1.1, Frozen, §4.2, §5.4, §5.6, §6.1-§6.4), `evaluation_protocol.md` (v2.4, Frozen, §5.5, §13.1), `src/robustfolio/backtest.py`, `src/robustfolio/estimators.py`, `src/robustfolio/optimize.py`, `src/robustfolio/config.py`, `tests/test_backtest.py`, `tests/test_conformance.py`, `scripts/certify_engine.py`, DEC-20261017-029
**Related risks:** R-E01, R-E04

**Context:**
The walk-forward harness (spec §6) is the second half of the engine. Writing it, and then making `scripts/certify_engine.py` certify *it* rather than a re-implementation of it, exposed one specification-conformance gap and four defects. They share a shape: each is a check or an optimisation that *looked* right and would have produced a plausible wrong answer rather than an error. None changes a frozen value or a frozen method definition.

The conformance gap is the plainest. `optimize.risk_parity`'s uncapped branch returned a `Solution` without ever calling `_accept`. On the frozen universe the cap binds on 154 of 168 rebalances, so the branch is rare -- and for the other 14, neither of §5.6's two acceptance checks ran at all. A failure there could only ever have been silent.

**Decision:**
1. **The harness lands (spec §6).** `src/robustfolio/backtest.py` implements §6.1-§6.4 as one monthly loop per method: a strictly trailing 60-month estimation window re-estimated monthly, the eligible set *at t*, drift applied before the universe change, and turnover computed over the full candidate universe so a leaver's closing trade is counted. The cost model (§5.5) cannot reach the optimiser -- each rebalance is solved once and every cost level is derived from that one turnover series -- because otherwise a cost level could influence the weights it is supposed to price. Folds are 12-month blocks of the rebalance index, so the §6.3 gate reads them without re-deriving the calendar.
2. **F19 recorded -- estimator determinism depends on the frame's memory layout.** pandas' `DataFrame.mean()`/`.cov()` reduce along the block's strides, and a frame can end up Fortran-ordered (a `frame.loc[row] = scalar` assignment is enough), so two logically identical frames returned estimates differing in the last ULP. That would falsify §5.4.8's bit-identical-determinism requirement and let a leakage test report its own floating-point perturbation as leaked information. Fixed by returning `np.ascontiguousarray(...)` from `estimators._as_matrix`; verified bit-identical to the pinned pandas definitions, so **no spec deviation**.
3. **F20 resolved -- the certificate's `nu` recovery was wrong for a case that is not hypothetical.** `_mvo_residual` recovered the sum multiplier `nu` by taking a median over the *smooth interior* indices, falling back to `nu = 0` when that set is empty. The set is empty whenever the turnover penalty makes *holding* optimal, because then every weight sits on the `|.|` kink at once. That fallback rejected **seven** optimal B5 rebalances with residuals up to `1.5e-3`; CLARABEL, SCS and OSQP agreed on the objective there to `1e-10` and no feasible pairwise exchange improved it. Replaced by an exact interval formulation: each index bounds `nu` from one or both sides (interior pins it, a kink contributes a band of width `2*kappa`, floor and cap bound it one-sided), the KKT system is satisfiable iff the largest lower bound does not exceed the smallest upper bound, and the residual is half the width of that empty interval -- the min-max stationarity violation over all admissible `nu`. It needs no subset to be non-empty. The docstring's earlier claim that a smooth interior index "holds for any universe of size >= 4 under the frozen cap" is **false** and is retracted.
4. **F21 resolved -- a redundant constraint changed the answer.** `mean_variance` declared the L1 auxiliary variable `u = cp.Variable(n, nonneg=True)`. The constraints `u >= w - base` and `u >= -(w - base)` already imply `u >= |w - base| >= 0`, so the bound is mathematically redundant -- but it adds a row to CLARABEL's constraint matrix and changes its path. With it, rebalance **B5 2015-01-31** returns `optimal_inaccurate` after 12 iterations at a point `2.8e-11` *below* the optimum (KKT residual `5.1e-7`); without it, the identical problem solves to `optimal` in 15 iterations with KKT residual `0`. The bound is removed. This is a fix inside the formulation §5.4 pins, which specifies the *constraints* rather than the variable declaration, so it is **not** a spec deviation.
5. **F22 recorded -- the risk-parity acceptance bypass (§5.6).** Fixed by calling `_accept` on the uncapped branch as well. §5.6's "either check failing aborts the run" now holds on all 168 rebalances for all seven methods.
6. **F23 recorded -- the certification evidence came from a different problem.** `scripts/certify_engine.py` rebuilt the rebalance loop itself and passed B5 a constant equal-weight initial holding, while production passes the *drifted* holding. It therefore certified an optimisation problem the project never runs, and missed F20's and F21's failures entirely: it reported B5 clean at `3.8e-12` while production was rejecting rebalances. The script now drives `backtest.run_method` and reports that run's diagnostics, and it asserts the protocol §13.1 structure (168 rebalances, 14 folds, one shared calendar across methods). Evidence the artifact under test did not produce is not evidence.
7. **`construct` now labels every solve with its rebalance date.** A rejected solve previously read only `MVO`, so the failing month had to be recovered by re-running with a patched harness; it now reads `B5 2015-01-31: ...`. A diagnosability fix, not a behaviour change.
8. **`SOLVER_TOL = 1e-14` is re-confirmed on the whole universe.** Evidence: **7 methods x 168 rebalances = 1176 solves, zero rejections**, worst residual `1.49e-11` -- a factor of ~6700 inside the acceptance tolerance. The tolerance does not map monotonically to achieved accuracy: `1e-12` leaves 15 rebalances over acceptance, `1e-13` and `1e-14` leave 0, and `1e-15` / `1e-16` leave 41 / 132. The measured table in `config.py` is updated from the earlier single-fold figures to these whole-run figures. Note also that **B5 self-reports `optimal_inaccurate` on 62 of 168 rebalances while all 168 certify** -- the reverse of the F17 disagreement, and the strongest available argument that the certificate, not the self-report, must be the binding test.
9. **No frozen document is amended.** F19-F23 are implementation-level. Point 4 touches a formulation the spec pins only at the level of the constraints, and the change keeps those constraints exactly.

**Alternatives considered:**
- **F20, widen the certificate's kink tolerance until the seven rebalances passed.** Rejected outright -- the classification tolerance *is* the acceptance tolerance, and loosening it to make a check pass is the Goodhart failure the check exists to prevent. The interval formulation makes the case pass because the point is optimal, with no tolerance moved.
- **F20, keep `nu = 0` and treat the rejections as an acceptable false-positive rate.** Rejected -- a certificate that rejects provably optimal points is not a conservative certificate, it is a broken one, and it would have blocked every B5 result.
- **F21, keep `nonneg=True` and instead raise `SOLVER_TOL` or loosen `ACCEPT_TOL` so 2015-01-31 passed.** Rejected -- the point is genuinely `2.8e-11` below the optimum; the right response to a solver returning a suboptimal point is to stop asking it to, not to lower the bar.
- **F21, accept the failure and run B5 with the rebalance excluded.** Rejected -- B5 is a baseline the comparison needs, and an objective error of `2.8e-11` is not the threat §5.6 guards against. Excluding a rebalance would also silently change the cost series.
- **F22/F23, leave both and note them.** Rejected -- F22 leaves an acceptance check that never runs on 8% of rebalances, and F23 leaves the project's primary evidence artifact unverifiable. Both are the "check that cannot fail" shape.
- **Certify by running the harness *and* keeping the standalone sweep.** Rejected -- two certificates that can disagree is worse than one that is right, and that disagreement is what hid F20 and F21.
- **Not record F19-F23 because none of them changes a headline number.** Rejected -- F20 and F21 each changed the weights at concrete rebalances, and the record's value is that the next reader can tell a fix that repairs a certificate from one that weakens it.

**Rationale:**
[First Principles] All five are the same question at different layers: does this check fail when the thing it checks is wrong? The risk-parity branch never asked it, the certificate asked it with a broken `nu`, the formulation asked it with a redundant constraint, and the certification script asked it of a different problem.
[Inversion] The failure mode is a *plausible* wrong answer, not an exception. Of the seven B5 failures that started this, six were certificate artifacts (rejecting optimal points), one was a genuinely suboptimal point, and all seven were reported identically. Only reading the whole residual vector rather than aborting at the first separates mechanisms that a first-failure abort makes indistinguishable.
[Baselines First] B5 is a baseline. Had F21 gone unfixed, the honest options were "no B5" or "relaxed acceptance" -- both damage the comparison the project exists to make. Removing a redundant constraint is free.
[Goodhart's Law] Three of the proposed fixes here were "move the threshold". All were rejected; the two accepted fixes make the *computation* right and leave every threshold untouched.
[LLN / Sample Complexity] 168 rebalances and 14 folds is what turned "B5 fails" into a distribution over failing months, which is what exposed two distinct mechanisms behind seven superficially identical failures.
[Opportunity Cost] Driving the existing harness from the certification script deleted the duplicated rebalance loop from it and made the evidence artifact self-consistent -- less code, stronger claim.

**Reversibility:** Soft. Points 1, 4, 6 and 7 are code-level. Point 2 is required by a frozen determinism requirement. Points 3 and 5 make an acceptance check match its own specification.

**Revisit trigger:**
Any rebalance fails to certify in a later run -> the failing month is dissected before any tolerance or formulation is touched, since F20 and F21 would both have been "fixed" wrongly by moving a number. Or a reviewer shows the interval certificate accepting a point that is not a KKT point -> the classification tolerance (`tol = ACCEPT_TOL`) is re-examined, because the certificate is exact only if the classification is. Or the next spec revision opens -> §5.6's "Tolerance: solver defaults" sentence, deferred by DEC-20261017-029, is corrected there.

**Expected value assessment:**
- Probability the smooth-interior fallback would have blocked the Phase 1 run before anyone diagnosed it: high (~80%) -- it failed on 7 of 168 B5 rebalances and the harness aborts on the first.
- Probability the failure would have been "fixed" by loosening `ACCEPT_TOL` had the evidence been only the residual number: moderate (~50%) -- `5.1e-7` looks like a tolerance problem.
- Probability `nonneg=True` would be written by any competent implementer of the L1 epigraph: high (~70%) -- it is the obvious way to declare `u`.
- Probability a weight vector `3.4e-5` off the optimum would have been noticed without the certificate: low (~15%) -- the objective error was `2.8e-11` and the cost impact is `~4e-8`.
- Probability the standalone certification script's divergence would have been caught by a reader of its clean-looking output: low (~20%).
- Probability the 62 `optimal_inaccurate` self-reports indicate a real problem: low (~10%) -- all 62 certify at `<= 2.1e-12`.

**Pre-mortem:**
Six weeks from now this entry has failed in one of four ways. (a) B5's worst residual of `2.1e-12` is quoted as evidence that B5 solves more accurately than B4 (`1.5e-11`), when the two are different problems -- detectable by checking that any cross-method accuracy claim uses the same formulation. (b) The interval certificate is described as "the KKT residual" without noting that at a kink the stationarity condition is a band of width `2*kappa`, so a point within `kappa` of the true multiplier is indistinguishable -- detectable by grepping the certificate's docstring for the band. (c) `scripts/certify_engine.py` drifts back into re-implementing the loop after a future refactor -- detectable because it must call `backtest.run_method`. (d) The new `results/*.json` exclusion hides the next artifact that *should* have been kept -- detectable because every committed evidence table is named in a decision-log entry.

---

### DEC-20261017-031

**Date:** 2026-10-17
**Type:** GOVERNANCE
**Status:** ACTIVE
**Authority:** Owner
**Related docs:** `model_and_method_spec.md` (v1.1, Frozen, §7.1-§7.11, §8, §9), `evaluation_protocol.md` (v2.4, Frozen, §2, §3, §6.1-§6.4, §7, §12.2, §12.6, §13.1, §14), `src/robustfolio/metrics.py`, `src/robustfolio/stats.py`, `src/robustfolio/report.py`, `scripts/run_experiment.py`, `tests/test_metrics.py`, `tests/test_stats.py`, `tests/test_report.py`, DEC-20261017-029, DEC-20261017-030
**Related risks:** R-E01, R-E04

**Context:**
The reporting layer is the last piece of the execution path. Spec §7 fixes the metric registry, spec §8 requires *one command* that regenerates the report plus an immutable run manifest, and protocol §14 fixes what must be disclosed. Three things had to be settled before it could be written.

First, §7.2 states plainly that the Phase 1 `metrics.annualized_turnover` is deleted: it derived turnover from `weights.diff()`, which treats the pre-rebalance weight as the previous *post*-rebalance weight and therefore ignores drift. `src/robustfolio/metrics.py` was a 1,339-byte Phase 1 stub containing exactly that function.

Second, §8's "one command" implies that every number a reader sees is produced by a path that has been exercised, not by a notebook. The reporting layer therefore had to consume `BacktestResult.net_returns(bps)` / `.turnover` / `.folds` rather than re-derive any of them: a report that recomputes the metric it reports is a second implementation of the metric.

Third, protocol §6.1-§6.4 is a conjunction of sixteen comparisons. A verdict is only checkable if each comparison is shown, so the decision rule is computed into a table rather than narrated into prose.

**Decision:**
1. **The metric registry lands (spec §7.1-§7.7).** `metrics.py` is rewritten with one function per metric and one definition each: `sharpe` (§7.1), `annualized_turnover` (§7.2), `max_drawdown` (§7.3), `cvar` (§7.4), `cost_drag` (§7.5), `skew_kurt` (§7.6), `autocorr1` (§7.7). The dead Phase 1 function is **deleted** as §7.2 requires. `sharpe` and `cost_drag` take `r_f` as an argument and never treat a missing series as zero (protocol §5.4.6), and both legs of `cost_drag` receive the *same* `r_f` (§7.5, protocol §2). `BacktestResult.annualized_turnover` now delegates to `metrics.annualized_turnover`, so the formula `12 * mean` exists once. **Turnover takes the harness's drifted per-month series, never a weight frame**, because drift is computed in exactly one place (risk R-C01) and a weight frame is what invited the defect §7.2 deletes.
2. **The inference layer lands (spec §7.8-§7.11).** `stats.py` implements PSR in per-period Sharpe units with a single conversion function (`annualized_to_per_period`) so the `sqrt(12)` cannot slip inside an inverse normal; DSR per §7.10 with the family variance from `config.DSR_FAMILY_SIZE`; the stationary block bootstrap (Politis-Romano geometric blocks, mean 6 months, 2,000 replications, `config.SEED`) in a fully vectorised form; and the calibration primitives. `psr` **raises** when its denominator's argument is non-positive rather than returning a `nan` or a clipped value: a fabricated p-value is worse than an aborted run, and this number gates §6.1.
3. **The report and the single command land (spec §8, protocol §14).** `report.py` builds the per-method disclosure table (net Sharpe at all five cost levels with 90% bootstrap intervals at the headline level, gross Sharpe labelled diagnostic, cost drag, turnover, drawdown, CVaR, skew, kurtosis, lag-1 autocorrelation), the sixteen-comparison decision table, the per-fold table, and the calibration table. `scripts/run_experiment.py` runs all seven methods and writes `<out>/manifest.json`, `outcomes.csv`, `decisions.csv`, `calibration.csv`, `folds_<M>.csv`, and `report.md`. The runner re-asserts the protocol §13.1 structure (168 rebalances, 14 folds) and the §5.6 certificate on the results it is about to report, and exits non-zero if either fails.
4. **F24 recorded -- §7.8's calibration does not define what is being predicted.** "A 90% prediction interval for the next month's return and for volatility" leaves both the object of the interval (asset returns or the portfolio's) and the realisation of a one-month *volatility* unspecified. The **return** half is implemented under a stated reading: at each rebalance the trailing window is the method's own previous 60 months of **net portfolio** returns, the interval is formed by the stationary bootstrap, and the realisation is the **next** month's net return. The **volatility half is not implemented** and no coverage number is reported for it: at a one-month horizon there is no sample over which a monthly volatility is realised, so any number would be a definition rather than a measurement. The reading is stated in the report, in the manifest, and in the module docstring. **Owner decision requested.**
5. **F25 recorded -- §6.3's "advantage" is not pinned to a metric, and its two clauses need different properties.** "Its advantage holds in >= 60% of walk-forward folds" reads naturally as the **primary metric** (§2: only net Sharpe may decide whether a method beats a baseline), so fold wins are counted on net Sharpe. "No single fold accounts for more than 40% of the total advantage" requires an **additive** decomposition, which a Sharpe is not: the concentration clause therefore uses the per-fold mean monthly net excess return difference. Both readings are reported. This matters rather than being bookkeeping: in the first run below the concentration clause is the **binding** one for `M2` (51.3%), so the reading decides the verdict. **Owner decision requested.**
6. **F26 recorded -- the reporting layer's validation consumed Test D's blind look.** The report generator can only be validated end-to-end on the frozen configuration, so the first run of `scripts/run_experiment.py` necessarily produced the confirmatory configuration's result before `EXP-H2-20261017-001` was executed. The mitigation is that the hypothesis, parameters, metrics and decision rule were all frozen *before* the look (§12.1) and the decision rule is mechanical, so observing the number cannot change the rule. What it does change is the *status* of Test D: executing it now would be a **reproduction and formal record**, not a blind test. Nothing may be amended on the strength of this look (§12.9). **Owner decision requested** -- disclose and proceed, re-designate Test D, or register a genuinely new confirmatory test with an honestly counted denominator.
7. **The DSR at `N = 1` is a convention, not a formula limit, and this is recorded rather than assumed.** §7.10 defines `SR_0 = sqrt(V)[(1-gamma) Phi^-1(1 - 1/N) + gamma Phi^-1(1 - 1/(N e))]`. At `N = 1` the first term is `Phi^-1(0) = -inf`, so the *formula* diverges; §7.10's frozen note specifies the value directly instead -- `V` = the analytic estimator variance `(1 + SR_hat^2/2)/T`, "`SR_0` approximately 0 ... reduces the DSR to a PSR against zero". Implemented as the note (`SR_0 = 0.0` exactly, the expected maximum of a single mean-zero draw), because the formula's answer (`DSR = 0`) would reject every method merely for having run once. This is a pinned convention, so it is **not** an owner choice; the §7.10 wording is deferred to the next versioned spec revision, as F17's §5.6 sentence was.
8. **Three implementation defects were caught by the new tests before any result was produced.**
   - `sharpe` and `per_period_sharpe` returned astronomically large values on a constant series: summing many copies of a value that is not exactly representable leaves the computed mean one ulp off, so `std(ddof=1)` comes back `~1e-19` rather than `0` and the guard `std == 0` does not fire. A constant 1%/month series produced a Sharpe of `2.3e16`. The degeneracy guard now tests the series' **range** (`max == min`), which is exact for the genuine case and inert on real data.
   - The first draft of `metrics.autocorr1`'s docstring asserted that `pandas.Series.autocorr(1)` subtracts the whole-series mean and therefore differs from §7.7's `corr(r_t, r_{t-1})`. That is **false**: pandas implements `autocorr` as `self.corr(self.shift(lag))`, i.e. exactly the paired Pearson correlation. The claim is retracted and the test now pins **equality** with pandas, which is the useful check.
   - The report's "break-even vs best baseline" column collapsed a non-monotone cost profile into a single threshold, printing "<= 50 bps" for `B5`, which is *behind* the best baseline at 0, 5 and 10 bps and *ahead* at 20 and 50. The column now **lists** the cost levels at which a method leads.
9. **The first end-to-end exploratory run is recorded, and it is non-confirmatory.** Snapshot `yahoo-usetf-2007-01-01_2026-09-30-2026-10-17-2ad06139`; 18 tickers; 168 rebalances; 14 folds; 1,176 solves; certificate clean (worst residual inside acceptance, as in DEC-20261017-030). Headline net Sharpe at 10 bps: **best baseline `B3` (sample MVO) 0.7896** [90% CI 0.331, 1.318]; `B5` 0.7843; `M1` 0.7860 [0.327, 1.298]; `M2` 0.8538 [0.426, 1.369]. `M2` leads the best baseline by **+0.064** net Sharpe (the §6.2 bar is 0.20) and its PSR against that baseline is **0.587** (the §6.1 bar is 0.95), so **both candidates return FAILURE under §6.4**. DSR p-values are 0.0032 (`M1`) and 0.0017 (`M2`) -- the contrast with the PSR column is the point of §6.1's two bullets: against a *zero* benchmark both look strong; against the *best baseline* neither is distinguishable from it. Calibration coverage of next-month return intervals is 81.5%-87.0% for all seven methods, inside §3's 80-100% target. The design/detectability appendix gives `rho(M1, B3) = 0.9845` and `rho(M2, B3) = 0.9856`, so the paired comparison was powered for the §6.2 threshold and the null is not an artefact of low power. **This is an exploratory run under §12.10 and fires nothing:** K1 belongs to Test D, and see F26.
10. **Finding F15's design/detectability appendix is implemented**, which was a decided item the first pass of this work package had missed. DEC-20261017-028 resolved F15 as reading (a): `rho(candidate, best baseline)` is reported in a **design/detectability** appendix, **not** added to the registered metric set, so no registration is amended and the DSR family size stays `N = 1`. `report.design_diagnostics` computes `rho`, the paired sample size, the mean paired difference and its standard error, and `design.csv` plus report section 7 carry them with an explicit \"not a registered metric\" label and a manifest flag. It is worth reporting because the power of the comparison is governed by the correlation of the *differences*, not by `T`, and the design diagnostic found a paired test reaching 80% power for the §6.2 threshold only at `rho >= 0.98`. **Measured here: `rho(M1, B3) = 0.9845`, `rho(M2, B3) = 0.9856`** -- inside that regime. That matters for how the null must be read: the comparison *was* adequately powered (MDE ~0.13 net Sharpe at this correlation), so the FAILURE verdicts are a statement about the effect being absent, not about the test being unable to see it. The point estimates agree: the mean paired differences are `+0.00031` (`M1`) and `+0.00047` (`M2`) per month, i.e. about `+0.4%` and `+0.6%` a year.\n11. **The CSV artefacts do not carry a column duplicating their index.** `outcomes.csv`, `calibration.csv` and `design.csv` were being written with both a `method` index and a `method` column; the column was removed (it was unused by the renderer and by every test). `decisions.csv` was already clean.\n12. **No frozen document is amended.** Points 4-6 are ambiguity records, point 7 is a deferred wording fix, and points 1-3 and 8 are implementation.

**Alternatives considered:**
- **F24, leave calibration unimplemented and note it.** Rejected -- protocol §3 requires calibration coverage for every method, and leaving a frozen requirement blank is worse than implementing the defensible reading with the reading stated.
- **F24, implement the volatility half on a definitional convention.** Rejected -- it would report a number whose value is fixed by a definition rather than by the data, which is indistinguishable from a fabricated result to every downstream reader.
- **F24, implement the asset-return reading (re-weight the estimation window by `w(t)`).** Rejected for now -- it mixes a gross-weight projection with net realisations, and the portfolio-return reading is the one the report can compute from what the harness already produced.
- **F25, report both clauses on net Sharpe.** Rejected -- the concentration clause would have no denominator, since per-fold Sharpes do not sum to anything.
- **F25, report both clauses on mean monthly return.** Rejected for the fold-count clause -- §2 makes net Sharpe the only metric allowed to decide whether a method beats a baseline, and the clause is a statement about the comparison.
- **F25/F24, record the readings only in the code.** Rejected -- both change what a reader concludes from the report, and both are decisions a reviewer would expect to see dated.
- **Point 8b, quietly fix the docstring.** Rejected -- a docstring that states a false fact about a dependency is exactly the kind of thing that gets propagated into a methods section.
- **Point 8a, treat the astronomical Sharpe as acceptable because no real series is constant.** Rejected -- the same ulp mechanism fires on any nearly-degenerate series, and the failure mode is a plausible enormous number rather than an error.
- **F26, do not run the report before Test D to preserve its blindness.** Rejected as impossible -- the reporting layer cannot be validated on a different configuration than the frozen one, and shipping an unvalidated report generator would be a larger risk than the loss of blindness. The loss is disclosed rather than hidden.
- **F26, silently proceed to Test D.** Rejected -- a confirmatory test whose answer was already observed is not confirmatory, and the record has to say so.

**Rationale:**
[First Principles] Each of F24, F25 and F26 is the same question: what exactly is the quantity the frozen document names? §7.8 names a prediction interval without naming its object; §6.3 names an "advantage" whose two clauses require incompatible properties; §12.1 names a blind test that the build order makes impossible to keep blind. None is a numerical gap, and all three would have been resolved silently by any implementation.
[Inversion] The failure mode in each case is a *number that looks fine*. A calibration coverage of 0.83 computed against asset returns would read identically to one computed against portfolio returns; a 51.3% concentration computed on Sharpe differences would read identically to one computed on returns; a re-run of a known answer would read identically to a blind test. The remedy is to state the reading where the number is produced.
[Baselines First] The first run's best baseline is the plainest method in the set -- sample-covariance, sample-mean MVO (`B3`). That is the outcome the project's design predicts, and it is why the baseline set has to be part of the report rather than a footnote: a robust method that does not beat `B3` has not earned its complexity.
[Probabilistic Claims] The `M2` result is the honest shape of this project's likely finding: a point estimate `+0.064` ahead of the best baseline, with a 90% interval `[0.426, 1.369]` against that baseline's `[0.331, 1.318]` -- almost entirely overlapping. The interval, not the point estimate, is what the report leads with.
[Goodhart's Law] §6.1's two bullets are a Goodhart defence and the first run demonstrates it: `M1` and `M2` clear the DSR (p = 0.003, 0.002) *and* fail the PSR (0.495, 0.587). A rule that used only the DSR -- the multiple-testing-adjusted one, i.e. the one that looks stricter -- would have declared a winner here.
[LLN / Sample Complexity] 168 months cannot separate 0.79 from 0.85. The decision rule's 0.20 gap is not conservative; it is approximately what this sample can detect, which is the reason it is the bar.
[Opportunity Cost] Building the report before firing Test D cost Test D's blindness (F26). Building it after would have meant writing the report generator against a result nobody could check, and the generator is the artifact the résumé claim rests on.
[Path Dependence] The Phase 1 stub's `annualized_turnover` would have been inherited by any implementer who trusted the existing module. §7.2's instruction to delete it is the reason the new `metrics.py` was written rather than extended.

**Reversibility:** Soft. Points 1-3 and 8 are code-level. Points 4-6 are disclosed readings, reversible by owner decision (F25 changes a verdict only in the concentration clause; F24's volatility half can be added once its object is defined). Point 7 is a deferred wording fix with no behavioural freedom.

**Revisit trigger:**
Owner resolves F24 or F25 -> the report's reading is updated and the entry is superseded in part. Owner resolves F26 -> Test D's status is restated in Appendix A. The next versioned spec revision opens -> §7.10's `N = 1` wording, §7.8's calibration object, and protocol §6.3's "advantage" are corrected there. Or a later run's verdict differs between the two F25 readings -> the concentration clause is re-examined before any conclusion is drawn from it.

**Expected value assessment:**
- Probability a reader would have taken the calibration coverage as evidence about the forecasts rather than about the return distribution, had the reading not been stated: high (~75%).
- Probability the two F25 readings give the same verdict on a candidate near the §6.2 threshold: moderate (~40%) in general; in this run they already differ, because the concentration clause decides `M2`.
- Probability `B3` being the best baseline would have been reported without the baseline table: low, since §6.1 fixes it -- but the *identity* of the best baseline being the plainest method is the finding, and it needed the table to be visible.
- Probability the constant-series Sharpe would have reached a report had the test not been written: low (~10%) -- no real return series is exactly constant, but the guard was the natural thing to write and the natural guard does not work.
- Probability the pandas `/autocorr` claim would have been copied into a write-up: moderate (~35%) -- it is the kind of sentence that reads as diligence.
- Probability F26's loss of blindness changes Test D's conclusion: low (~15%) -- the decision rule is mechanical and was frozen first, so the look cannot move the rule. Its cost is to the *claim* of confirmatoriness, not to the arithmetic.

**Pre-mortem:**
Six weeks from now this entry has failed in one of four ways. (a) The calibration coverage is quoted as "the models are well calibrated" when it only says the method's own return distribution covered the next month -- detectable by checking that any calibration claim names the F24 reading. (b) `M2`'s +0.064 is cited as a positive result because the DSR p-value was 0.0017 -- detectable by grepping for whether a PSR number appears beside it, since §6.1 requires both. (c) The concentration clause's 51.3% is treated as a property of `M2` rather than of the F25 reading -- detectable by checking that the clause is always reported with its metric. (d) Test D is reported as confirmatory despite F26 -- detectable because the Appendix A entry must carry the F26 disclosure.

---

### DEC-20261017-032

**Date:** 2026-10-17
**Type:** GOVERNANCE
**Status:** ACTIVE
**Authority:** Owner
**Related docs:** `docs/README.md` (v1.14), `decision_log.md` (v1.7), `src/robustfolio/data.py`, `src/robustfolio/report.py`, `scripts/build_snapshot.py`, `scripts/pack_snapshot.py` (new), `scripts/verify_release.py` (new), `scripts/make_figures.py` (new), `tests/test_release_packaging.py` (new), `tests/test_docs_index.py` (new), `.github/workflows/ci.yml` (new), DEC-20261017-025, DEC-20261017-031
**Related risks:** R-E01, R-E04

**Context:**
The execution path was complete after DEC-20261017-031 and the résumé bar was met on paper: *one command regenerates the number*. It was not yet met in substance. A reader who clones the repository and runs `scripts/build_snapshot.py` does **not** reproduce the published number, because Yahoo revises history — the rebuilt snapshot gets a different content hash, a different snapshot id, and slightly different prices. "Check these numbers" would quietly have become "trust these numbers", which is the one thing this project cannot afford to be.

So the frozen snapshot has to ship. At 2.43 MB it fits inside a release asset, which raised a second question that turned out to be the real work: if the artefact *is* the deliverable, then the integrity chain around the artefact needs to be the most trustworthy code in the repository — and the only way to know that is to have it catch an error, which means deliberately trying to break it.

Two attempts to verify the artefact were made, and **both were wrong in ways that produced plausible numbers**. Neither error was in the artefact. That is the whole finding: a verification you have not verified is not a verification, and this project's claim rests on the verification.

**Decision:**
1. **The bundle hash gets one definition, in the data layer, and the two file sets are named.** `build_snapshot.py` had the four bundle files spelled out inline while `data.SNAPSHOT_FILES` listed five; `_bundle_hash` was a second copy of the same formula. Both are gone: `data.bundle_hash(hashes)` is the single definition, called by the builder and by the packer, and the sets are explicit as `BUNDLE_FILES` (four) and `SNAPSHOT_FILES` (five). This is finding **F27** (point 7).
2. **`scripts/pack_snapshot.py` packs and verifies a snapshot.** It checks the whole chain, writes a **deterministic** `tar.gz` (sorted members, `mtime` pinned to the epoch, no gzip timestamp or filename, fixed mode) plus an external `<archive>.sha256`, and supports `--verify` / `--verify-dir` / `--extract-to`. Determinism is not decoration: the release publishes the archive's digest, and a digest that changes when nothing changed cannot be checked. Extraction is **staged**: unpack to a temporary directory inside the destination, verify, and only then move into place, so a failed verification cannot leave a half-written snapshot behind. Absolute paths and `..` members are refused before anything is written, and an existing snapshot is never overwritten without `--force-extract`, because snapshots are append-only.
3. **`scripts/verify_release.py` is the "check me" command.** It verifies the archive against the digest quoted in the release notes, extracts the snapshot to a temporary directory, re-runs all seven methods, rebuilds the metric table, and asserts equality against the run's `outcomes.csv` at tolerance **exactly zero**. Zero, not `1e-9`: the claim is that the artefact is exact, and a tolerance loose enough to absorb a real discrepancy would also have absorbed both of the errors below.
4. **The run directory publishes `net_excess_returns.csv`.** The monthly net **excess** return series of every method at the headline cost, which is precisely the series the primary metric is defined on (protocol §2). The figure, and any statistic a reader prefers to ours, can now be computed from the run directory alone rather than by re-running the harness. It is an **auxiliary disclosure, not a registered metric**: no registration is amended, `N = 1` is unchanged, and the manifest, the report and the CSV all say so.
5. **`scripts/make_figures.py` draws the two headline figures from the run directory alone** — cumulative net excess return with its drawdown, and the primary metric with its bootstrap interval. The exploratory/confirmatory label is read from the run's own `manifest.json` rather than passed in or assumed, and an unreadable manifest is labelled `STATUS-NOT-STATED` rather than defaulted to either. Protocol §14.2's prohibitions are enforced by construction: every figure states the cost level it is net of, the axis is labelled as a multiple of 1.0 rather than a return, and the footer says "not an investable return".
6. **CI is green on a fresh clone by design, and complete once the release exists.** `tests/conftest.py` already skips data-dependent tests with an explanatory reason, so a clone with no data passes; the workflow attempts to fetch the frozen snapshot from the release assets, and when that succeeds it *also* runs the full suite and the one-command regeneration, with certification on, so a solver failure breaks the build rather than appearing as a result. A single Python version is used deliberately: the environment is frozen (the bootstrap seed and `SOLVER_TOL` are part of the result), so a second interpreter would test a configuration nobody quotes numbers from.
7. **F27 -- the bundle hash covers four files; `manifest.json` lists five.** The quality report is excluded because it embeds the snapshot id, which is derived from the bundle hash — including it would be circular. The name does not say so, and the first packer recomputed the bundle from the manifest's full `sha256` map, obtained a different value, and **rejected every valid snapshot**. A verifier that fails on correct input is worse than no verifier, because it teaches people to ignore it. Fixed by naming both sets in `data.py` and pinning the distinction with a regression test.
8. **F28 -- `pandas.read_csv` is lossy by one ULP at its default settings.** It returns `0.1820065203183531` where `outcomes.csv` contains `0.18200652031835318`. `float_precision="high"` is also lossy; only `float_precision="round_trip"` is exact. `pandas.DataFrame.to_csv` writes full round-tripping precision, so the **artefact is exact and the reader was wrong**: the first comparison of the extracted archive against the published table reported a mismatch of `8.3e-17` on `B4` and would have been filed as a reproducibility failure. The trap is recorded where it bites — in the verification script's docstring, in the writer's comment, and in the report's notes — and the comparison is shipped as code so that no reader has to rediscover it.
9. **F29 -- the documentation index had drifted in two places, and duplicated state is now maintained by a test rather than by discipline.** `docs/README.md`'s own `**Version:**` header read `1.12` while its revision history ended at `1.13` — the same drift the `1.13` row itself reports fixing for `1.11`. Separately, the status board asserted version `1.6` for `decision_log.md`, which declared no version at all, so the board's claim about that file could not be checked against the file. Both are fixed, and `tests/test_docs_index.py` now asserts four invariants mechanically: the index header equals its own last revision row; the revision history is monotonic; every status-board row's version and status agree with the document it names (status compared on its leading token, so a *Frozen* claim cannot hide behind prose); and both frozen contracts say *Frozen*.
10. **Nothing is pushed, no release is cut, and no public material may use confirmatory language.** F24, F25 and F26 remain open owner decisions from DEC-20261017-031, and F26 in particular forbids "confirmatory" while the confirmatory configuration's answer has already been observed. The packaging work is what makes the release *possible*; it does not make it *permitted*.

**Evidence:**
- Archive: `robustfolio-snapshot-yahoo-usetf-2007-01-01_2026-09-30-2026-10-17-2ad06139.tar.gz`, **1.67 MB**, SHA-256 `28e1d9073844d43be2b256bc7b1ba6c6cf4d050e50703472e206d5ca4052f11e`, **identical** across two independent packs and after perturbing the members' `mtime`.
- `verify_release.py` against the archive and the `EXP-X-20261017-003` run directory: **`EXACT`, max abs difference `0.000e+00` over 18 published columns, 7 methods re-run from the extracted snapshot.**
- Tests: **150 passed, 1 skipped** (the skip is the vacuous §5.4.8 in-sample delisting test, unchanged). New: 12 packaging tests, 4 documentation-integrity tests.
- `pack_snapshot.py --verify-dir` on the frozen snapshot reports the four-link chain intact, with the bundle hash equalling the snapshot id's 8 hex characters.

**Alternatives considered:**
- **Commit the snapshot to git.** Rejected -- a 2.4 MB binary blob is permanent in history for an artefact that is regenerable from a script, and it would make the repository the source of truth for something whose truth is the digest.
- **Rebuild the snapshot during verification.** Rejected -- this is the failure mode the whole exercise exists to prevent; a rebuilt snapshot is a different input, so the comparison would be a coincidence rather than a check.
- **`zip` instead of a deterministic `tar.gz`.** Rejected -- embedded timestamps and unspecified member order make the archive digest unstable, at which point the published digest cannot be verified and the chain has a broken link.
- **Loosen `verify_release.py`'s tolerance, e.g. to `1e-12`.** Rejected -- both of the bugs found here were in the verifier, and a tolerance loose enough to hide one of them would have been chosen *because* it hid one of them. Zero is what makes exactness a claim rather than a hope.
- **Document the pandas `float_precision` trap in the README instead of shipping a script.** Rejected -- a paragraph cannot be run, and the trap produces a plausible number sentinel rather than an error.
- **Publish raw net returns instead of net excess returns.** Rejected -- the figure would then illustrate a different quantity from the table above it, which is exactly the inconsistency the registered metric (§2) exists to prevent.
- **Make the data-dependent tests fail instead of skip.** Rejected -- a CI that is red until a 1.67 MB asset is downloaded teaches people to ignore CI, and the honest signal ("this check did not run") is already available as a skip reason.
- **Test on a matrix of Python versions.** Rejected -- the frozen environment is part of the result; a second interpreter tests a configuration from which no number is quoted.
- **Enforce the documentation index by review.** Rejected -- it had already drifted twice, once immediately after a fix for the same drift. This is `[Path Dependence]` in miniature: the remedy for a rule kept by memory is to stop keeping it by memory.

**Rationale:**
[First Principles] "Reproduce the number" has a hidden quantifier. It does not mean *compute a similar number*; it means *compute the same number from the same input*. Everything in this entry follows from taking that literally: the input must ship, its digest must be stable enough to publish, and the comparison must be exact enough to fail when it should.
[Inversion] Ask what would make this project *look* verified while not being verified, and both findings appear immediately. A verifier that rejects every valid snapshot gets deleted or its tolerance loosened; a verifier that reads with a lossy parser reports a mismatch on a good artefact and gets dismissed as noise. In both cases the response is to weaken the check, which is how a verification programme dies -- not from a missed bug, but from crying wolf once too often.
[Baselines First] The plain verification baseline is "same bytes in, same bytes out". Both errors were deviations from that baseline introduced by a convenient tool (`findall`-style convenience, a default parser), and both were caught only because the expected answer was known to 17 digits.
[Probabilistic Claims] The published claim is now conditional and checkable: *given archive digest X, the run reproduces the published table exactly*. A reader who shows a different result has a specific, falsifiable disagreement -- wrong archive, or changed code -- rather than a vague one about environment.
[Goodhart's Law] The release will be judged by impressions, stars and inboxes, none of which measure whether the verification works. The counter is to make the check-me command the *most* prominent artefact and the cheapest thing to run, so that the measure that is easy to fake (attention) is not the measure that is easy to satisfy.
[Code vs Prose] Both F28 and the pandas trap are the same shape: knowledge that is true, important, and useless when written down, because the failure is silent. The response is to move the knowledge into something executable. The same argument applies to the documentation index (point 9): a version kept in two places will drift, so the agreement is asserted by a test.
[Opportunity Cost] The snapshot asset and figures were chosen over drafting the flagship essay, because they are strictly enabling: the essay quotes the digest and shows the figure, so writing it first would have meant writing it twice.
[Path Dependence] The four-file/five-file asymmetry has been in the snapshot format since DEC-20261017-025 and was invisible until someone tried to verify it from the outside. An artefact's internal consistency is not tested by the code that produces it; only a second, independent consumer tests it.

**Reversibility:** Soft. All of it is code and tooling. The snapshot itself, its digest and the archive are immutable once published, and the readings/decisions recorded by DEC-20261017-031 (F24/F25/F26) are untouched by this entry.

**Revisit trigger:**
A release is cut -> the CI workflow's `RELEASE_TAG`/`SNAPSHOT_ASSET` are updated to the published asset, `verify_release.py` is re-run against it, and the digest is re-quoted. A new snapshot is built -> a new id and digest, and the board, the archive name and the CI variables are updated together. `pandas` changes its default `float_precision` behaviour -> the F28 note is re-verified (the new test pins the behaviour, so such a change breaks the suite rather than silently changing a verdict). F24, F25 or F26 is resolved -> the release may proceed, and the wording of every public artefact is re-checked against §14.2 before it does.

**Expected value assessment:**
- Probability a reader (or a future run) reproduces a *different* number from the archived snapshot with unchanged code: very low (<2%) -- the archive is content-addressed and the comparison is exact.
- Probability the F28 pandas trap would have been filed as a reproducibility failure had the archive not been checked by hand first: high (~70%) -- the first two comparisons both misfired, and the natural next step is a bug report against the snapshot rather than against the reader.
- Probability the F27 defect (a verifier rejecting valid snapshots) would have been noticed from the code alone: low (~15%) -- it is only visible by running the verifier on a correct snapshot.
- Probability the documentation-index drift would have been found by review in the next month: low (~20%) -- it had just recurred immediately after a fix for the same drift, which is what a rule-with-no-mechanism looks like.
- Probability a release is cut without the F26 constraint being re-read: moderate (~40%) -- the packaging work is the last technical item in the release plan, and the temptation is to treat "it's finished" as "it's permitted". Mitigated by point 10 being explicit and by the manifest's `scope` field, which the figures read rather than assume.

**Pre-mortem:**
Six weeks from now this entry has failed in one of four ways. (a) The snapshot asset was uploaded but the digest was never quoted where a reader would find it, so the chain's fourth link is decorative -- detectable by asking `verify_release.py --expect-sha256` to fail on a deliberately wrong digest, which it does, and by checking that the release notes carry the number. (b) CI's `continue-on-error` download failure was mistaken for a passing full run, so the workflow reads green while the reproduction step silently never ran -- detectable because the "Confirm the snapshot is the frozen one" step is gated on the same output, so a job showing `Tests` green *and* no certification step ran has been masked. (c) The figures were published from a re-run rather than from the committed run directory, so the figure and the table describe two different runs -- detectable because `make_figures.py` takes a run directory and prints the run name into the figure footer. (d) `net_excess_returns.csv` is described somewhere as a registered metric or as investable returns -- detectable by grepping for "net_excess_returns" outside the auxiliary-disclosure wording, and by checking that no figure's footer has lost the "not an investable return" clause.

---

### DEC-20261017-033

**Date:** 2026-10-18
**Type:** GOVERNANCE
**Status:** ACTIVE
**Authority:** Owner
**Related docs:** `open_source_and_license_policy.md` (v1.0, Draft — new), `docs/README.md` (v1.15), `decision_log.md` (v1.8), `LICENSE`, DEC-20261017-032
**Related risks:** R-E01

**Context:**
Appendix B item **E7** recorded `open_source_and_license_policy.md` as "must be written before public release", and DEC-20261017-032 built the release chain that makes a public release imminent. Writing the policy was therefore a precondition, not a nicety.

Writing it surfaced something the release plan had not accounted for. The project's most load-bearing output is now the **frozen snapshot archive** — the artefact that makes "one command regenerates the number" exactly true rather than approximately true. That archive contains Yahoo Finance daily prices. The `LICENSE` is MIT and covers the *code*; it does not, and cannot, cover third-party market data. A policy that simply said "MIT" would have been a licence claim about data the project does not own, published in the same breath as an upload of that data.

**Decision:**
1. **`open_source_and_license_policy.md` is written as v1.0 Draft** and registered as the eighth active document; E7 is removed from the "Not yet written" list (the same treatment `model_and_method_spec.md` received at `docs/README.md` v1.4). It answers exactly two questions — what a reader may do with the repository, and what this project may publish — and deliberately does not become a general governance document.
2. **The licence is split explicitly by artefact class.** MIT covers `src/`, `scripts/`, `tests/`, `docs/`, `notes/`, and everything the project itself authors. It does **not** cover the snapshot archive's Yahoo-sourced price and action files, which remain governed by Yahoo's terms. FRED `DGS1MO` is US government data, effectively public domain, and is recorded separately. Everything derived from the data inherits the data's provenance even though the project authored it.
3. **F30 raised — the archive is a redistribution, and the release plan assumed it was not.** Publishing the snapshot is the *only* way the project's central claim stays true, and it is also a redistribution of roughly 4,966 daily rows × 18 instruments of third-party data. The disposition is a **`[PROPOSED]` owner decision**, not something this entry can settle: **(a)** publish the archive with a NOTICE (recommended), **(b)** publish only the derived series, or **(c)** publish no data and the digest alone. The `[PROPOSED]` recommendation is **(a)**, on the grounds that (b) would verify the arithmetic while leaving the analyst's actual work unverified, and (c) would leave the digest meaningless. If (a) is confirmed, the source, retrieval date, and the fact that MIT does not cover the data must appear in the README, the release notes, *and* the archive's manifest. The disposition is revocable, and the consequence of revoking it is documented in advance as a *degradation* of the verification path rather than quietly dropped.
4. **Contributions: `[PROPOSED]` issues and PRs, no CLA, no DCO.** A contribution must keep the suite green, must not change a frozen value without a decision-log entry, and must state which result changed and by how much if it changes one. Recorded because "MIT inbound = MIT outbound" is the arrangement with the least friction and the least scope for a contributor to be surprised.
5. **Attribution rule: findings describe this implementation, not upstream libraries.** F19 and F28 both document upstream behaviour that is working as specified; they must not be cited as `cvxpy` or `pandas` bugs. This is a small clause with a large failure mode: a mis-cited finding becomes someone else's bug report.
6. **F26 remains unresolved and this entry does not resolve it.** The recommendation presented for the owner is to **re-designate `EXP-H2-20261017-001` as EXECUTED (NON-CONFIRMATORY)** and record its execution as the *same* run as `EXP-X-20261017-003` — one execution, one record, two labels, no duplicated numbers — and to **not** register a replacement confirmatory test now. Reasoning under the framework is in the Rationale below. **Owner decision requested.**

**Alternatives considered:**
- **One licence for everything, stated as "MIT".** Rejected -- it would be a false claim about third-party data, made in the same document that publishes it. A licence statement is cheap to write and expensive to be wrong about.
- **Publish the derived monthly series only (F30 option b).** Rejected as the *primary* disposition -- it would verify the metric arithmetic while leaving the corporate-action application, the daily-to-monthly aggregation, and the point-in-time eligibility by date unverified, i.e. it would verify the easy half.
- **Publish nothing but the digest (F30 option c).** Rejected -- an unverifiable digest is theatre; the whole chain exists so that a reader can check rather than trust.
- **Silently publish the archive, since everyone does.** Rejected -- "widely done" is the cargo-cult reasoning the framework's first model names explicitly, and the project's differentiation is precisely that it does not do things because they are common.
- **Fold licensing into `scope_and_non_goals.md` rather than adding an eighth document.** Considered and rejected -- E7 names this document specifically, and licence terms are not scope; but the document is kept to one page to avoid growing the doc set for its own sake.
- **Let E7 wait until after the release.** Rejected -- it is the last recorded precondition, and its §2 changes *what is uploaded*, not merely what is said.

**Rationale:**
[First Principles] *What is the artefact?* Not a strategy and not a data product: a **verifiable evaluation**, whose value is entirely a function of whether a stranger can check it. The licence follows from that. MIT for the checker, because a checker people cannot reuse is not a checker; a NOTICE for the data, because the project does not own it.
[Inversion] Ask how this release fails *silently and catastrophically*, and the archive's provenance is the answer: it would fail by publishing third-party data under a licence that does not cover it, with nobody noticing until someone notices. That is a category of failure that the project's whole apparatus — leakage tests, certificates, zero-tolerance reproduction — was not pointed at, because every one of those checks is about *the arithmetic* being right, and this is about *the claim* being right.
[Goodhart] The release's success will be measured in attention, and attention is trivially separable from correctness. Worse, the project has a subtler version of the same trap: its quality metric is "did the apparatus work", and a **null result flatters the apparatus**. If the answer had been yes, the same code would have been called rigorous for different reasons. The guardrail is that the checks must be *sign-independent*: the leakage suite, the KKT certificate and the zero-tolerance reproduction check would each have returned the same pass had `M2` won. That is worth saying out loud in the write-up, because it is the difference between rigour and a narrative that happens to end well.
[Map is Not the Territory] The point-in-time discipline in this project covers **eligibility**: which instruments existed and were tradeable at each rebalance. It does **not** cover **data**: the prices in a 2026 snapshot for 2012 are Yahoo's *current* history for that period, which has been revised, and are not the prices a trader would have seen. "Point-in-time" here therefore means point-in-time *universe*, not point-in-time *data*. This is stated in the limitations and should be stated more precisely than it currently is.
[Ergodicity] The framework's sixth model warns that an ensemble-average good system can still be destroyed by a tail event, and the metric set here is a mean-and-dispersion set: Sharpe, CVaR, drawdown, skew. There is no survival criterion. The live evidence is in this run — `M2` has the best metric and `B2` (risk parity) has the lowest drawdown, so the "on average" winner is not the over-time survivor. Recorded as an open question about the metric set rather than a defect, because §2 fixes the primary metric and this entry may not amend it.
[Second-Order Thinking] Publishing creates obligations that outlive the post: a stale snapshot, a CI variable pinned to a release tag, a link that rots. DEC-20261017-032's digest plus `verify_release.py` are what make staleness *detectable* rather than *silent*, which is the difference between a maintenance task and a slow-motion falsehood.
[Path Dependence] F26 is itself a path-dependence artefact of build order, and the reusable lesson is exactly one rule: **validate a pipeline against a throwaway configuration, never the registered one.** That rule is why no replacement confirmatory test should be registered in a hurry — a test designed after seeing the answer is a test designed by the answer.
[Law of Large Numbers] The decision to re-designate rather than replace Test D follows from sample size, not from modesty: a genuinely blind replacement would need a *new sample* (a different asset class, or a period that has not happened yet), and a four-month extension has no power. Promising a confirmatory test that cannot exist for years is worse than stating plainly that this evaluation is non-confirmatory and checkable.

**Reversibility:** Soft. The document is Draft; both `[PROPOSED]` items are one-line changes if rejected. The archive's disposition is revocable by deleting an asset. Nothing frozen is touched, and no result changes.

**Revisit trigger:**
Owner confirms both `[PROPOSED]` items -> `open_source_and_license_policy.md` goes to v1.0 Frozen. Owner resolves F26 -> Appendix A's ledger entry for `EXP-H2-20261017-001` is restated, and the release may proceed under §14.2. Yahoo, FRED or an issuer changes terms, or a third party objects -> §2 of the policy is re-examined and the outcome recorded here. `results_reporting_and_claims_policy.md` (E3) is written -> policy §5 is reduced to a pointer so the claim rules exist in one place. The metric set is ever revisited -> the Ergodicity note above becomes a concrete proposal with §2 unchanged.

**Expected value assessment:**
- Probability a reader would have assumed MIT covered the snapshot archive, absent an explicit split: high (~85%) -- "the repo is MIT" is the default reading, and it is wrong here.
- Probability the archive is objected to by the rights holder and must come down: low (~5%) -- daily prices of large publicly listed ETFs, non-commercial, attributed, for verification.
- Probability a mis-cited finding is filed as an upstream bug report if the attribution clause is absent: moderate (~30%) -- F28 is a `pandas` default behaving as documented, which reads like a bug out of context.
- Probability a confirmatory replacement test registered now would be honestly blind: very low (<5%) -- the design would be selected by an answer already known.
- Probability the ergodicity gap matters to a reader's decision: low for *this* release (~10%), but the observation that the metric-set winner is not the drawdown-minimiser is high (~75%) to be noticed by a quant reviewer, and it is better raised by the author than received as a criticism.

**Pre-mortem:**
Six weeks from now this entry has failed in one of four ways. (a) The archive was uploaded with the NOTICE in the README but not in the archive's own manifest, so the data travels with no statement attached -- detectable by opening the asset's `manifest.json` and finding the source and the licence note. (b) A bare licence word ("MIT", "open source") was written somewhere beside a data file, collapsing the split this entry exists to make -- detectable by grepping for the licence word near `prices_raw` or `universe_pit`. (c) F26 was quietly forgotten in the release rush and something public said "confirmatory" -- detectable by grepping the published artefacts for that word and requiring that it appear only inside the F26 disclosure. (d) The ergodicity note was read as a finding rather than as an observation about the metric set, and §2 was amended on its strength without an owner decision -- detectable because §2 is frozen and any amendment would need a decision entry that this one is not.

---



### DEC-20261017-034

**Date:** 2026-10-18
**Type:** GOVERNANCE
**Status:** ACTIVE
**Authority:** Owner
**Related docs:** `open_source_and_license_policy.md` (v1.0 **Frozen** — was Draft at DEC-20261017-033), `docs/README.md` (v1.16), `decision_log.md` (v1.9), `evaluation_protocol.md` §12.1/§12.9/§12.10, Appendix A entry `EXP-H2-20261017-001`, `scripts/pack_snapshot.py`
**Related risks:** R-E01

**Context:**
DEC-20261017-033 presented three owner decisions: how to resolve **F26**, and two `[PROPOSED]` items in the new licence policy. The owner confirmed all three on 2026-10-17. This entry records the resolutions, and one deviation from DEC-033's own wording that executing them made necessary.

**Decision:**

1. **F26 is resolved by re-designation, not by repair.** `EXP-H2-20261017-001` (Test D) is marked **EXECUTED (NON-CONFIRMATORY)** and its execution is recorded as the **same run** as `EXP-X-20261017-003` — one execution, one record, two labels, no duplicated numbers. Repair was not available: the reporting layer could only be validated end-to-end on the frozen configuration, so the confirmation's answer was observed before the test ran, and no subsequent act restores prospective blindness.

2. **The registered confirmatory slot in family H2/H3 is now spent and empty.** No replacement test is registered. **K1 does not fire** — it belongs to a confirmatory test and none was executed blind — so H2.4 is **untested**, not falsified, and the honest public description is **"pre-registered, mechanically evaluated, non-confirmatory"**. This is a weaker claim than a passed test and a *stronger* one than a backtest, and it is the accurate one.

3. **The relabelling cannot be used to rescue the hypothesis, and the ledger says so in the entry itself.** The §6.4 verdict is `FAILURE` for both candidates either way. What changed is *which entry carries the verdict*, not the verdict. This is recorded inside the ledger entry rather than left for a sceptical reader to reconstruct, because a reader who discovers it unaided will reasonably suspect the opposite.

4. **`open_source_and_license_policy.md` is frozen at v1.0.** Both `[PROPOSED]` items are confirmed: **(a)** publish the snapshot archive with a NOTICE (F30), and the contribution model as **issues and PRs, no CLA and no DCO**, with the three contribution conditions as written.

5. **Deviation from DEC-20261017-033, recorded rather than absorbed.** DEC-033 required the NOTICE to appear in "the README, the release notes, *and* the archive's own manifest". The third is **changed** to a **`NOTICE.txt` member inside the archive**, generated from a template held in the packaging script. Reason: `manifest.json` is the *data layer's own hashed record*, and a licensing statement is neither data nor a statement about data; putting it there would place a mutable editorial statement inside the artefact the integrity chain reads. A sibling `NOTICE.txt` is reviewable in git, travels with extraction, and is generated deterministically so it cannot drift from the snapshot on disk. The README and the release notes carry the text as originally required. **This is a deliberate, reasoned deviation, not a silent one**, which is the only reason it is acceptable.

6. **What a valid confirmatory test would require — stated as a condition, not promised as a plan.** A **new sample**: a different asset class, or a period that does not yet exist. The design must not be selected by the observed result, and the denominator must be counted honestly at registration. No such test is registered now, and registering one in a hurry would be worse than not having one, because a test designed after the answer is known is a test designed by the answer.

**Alternatives considered:**
- **Disclose and execute Test D as registered (DEC-033 option B).** Rejected. It re-runs a known configuration, adds no information, and its only distinctive feature is the risk of being read as confirmatory. The formal record it would create is already created by `EXP-X-20261017-003`.
- **Register a new confirmatory test now (DEC-033 option C).** Rejected for the reason in item 6: the only samples available are unpowered (a four-month extension) or contaminated (the same data, already seen).
- **Call the result a *failed* confirmatory test, since the rule returns FAILURE.** Tempting and rejected. It would let the project keep the word "confirmatory" if the answer had been favourable and drop it because the answer was not — which is precisely the selection effect the freeze exists to prevent. The label must not depend on the sign of the result.
- **Amend §6.4's thresholds so the observed gap qualifies.** Rejected categorically (§8.1 Hard Rule 2, §12.9). Recorded only because it is the failure mode this whole apparatus exists to prevent.
- **Delete the exploratory run's numbers from the public material to avoid the awkwardness.** Rejected. The numbers are reproducible from a frozen snapshot by a published command; suppressing them would replace an honest null with an unverifiable one.

**Rationale:**
[First Principles] *What is the artefact?* An evaluation whose value is that a stranger can check it. Blindness is a property of *how* a number was obtained; checkability is a property of *whether* it can be verified. F26 destroyed the first here. It did not touch the second, because the rule is frozen, mechanical, and publicly re-runnable to **tolerance zero** (DEC-20261017-032). The project should therefore say exactly which of the two it has, rather than borrowing the prestige of the one it lost.
[Inversion] Ask what the *dishonest* version of this resolution looks like: relabel an inconvenient result as non-confirmatory, escape K1, and quietly keep quoting the number. The defence is not that the relabelling is disinterested — it is not, and the entry says so — but that **it cannot change the verdict**, and that a reader can verify the frozen rule's output themselves. A defence a reader can check beats an assertion of good faith.
[Goodhart] The project's quality metric is "did the apparatus work", and a **null result flatters the apparatus**. If `M2` had cleared the bar the same code would have been praised for different reasons. The checks must be shown to be **sign-independent** — the leakage suite, the KKT certificate and the zero-tolerance reproduction would each have returned the same verdict had `M2` won — because otherwise "rigour" is a story that happens to end well.
[Path Dependence] F26 is an artefact of build order, and it compresses to one reusable rule: **validate a pipeline against a throwaway configuration, never the registered one.** Recorded here as the generalisable lesson, since it is the only part of this entry that is worth anything to someone else.
[Second-Order Thinking] Publishing a non-confirmatory null invites the reading "he ran it, did not like the answer, and demoted it". The only durable answer is to have said so first, in the ledger, in the author's own words — which is cheaper than being asked.

**Reversibility:** Soft. Item 1 is a status restatement and item 5 is a file placement; both are matters of record, not code. Nothing frozen is amended: §6.4, §12.1 and the registered parameters are untouched, and no result changes.

**Revisit trigger:**
A genuinely new sample becomes available and a confirmatory test can be registered blind -> this entry's item 6 is satisfied and a new registration is appended. A reader disputes the relabelling -> item 3's reasoning is the answer, and if the dispute has force, a new entry restates the conclusion rather than editing this one. `results_reporting_and_claims_policy.md` (E3) is written -> the "non-confirmatory" phrasing rule moves there and E7 §5 becomes a pointer.

**Expected value assessment:**
- Probability a careful reader would have inferred the F26 label problem from the artefacts unaided: moderate (~35%) -- the registry says REGISTERED and the run says exploratory, which is a visible seam.
- Probability that disclosing it in the author's own words costs credibility rather than gaining it: low (~15%). The framework's own failure mode here is understating a defect and being caught; overstating it is recoverable.
- Probability a future reader needs item 6 (what a valid test requires) to judge the project fairly: high (~75%) -- the natural question is "so will you test it properly?", and "no, and here is why not yet" is a better answer than a promise.
- Probability the NOTICE placement matters (item 5): low for licensing outcome (~10%), high for reviewability (~80%) -- a `NOTICE.txt` in the diff can be read; a licence field inside a generated manifest is easy to miss.

**Pre-mortem:**
Six weeks from now this entry has failed in one of three ways. (a) A public artefact says "confirmatory", or says "the confirmatory test failed" -- detectable by grepping the published material for the word and requiring it to appear only inside the F26 disclosure. (b) The registry index says RE-DESIGNATED but the entry's own Conclusion section still reads as though K1 fired, so two parts of the same ledger disagree -- detectable by reading the index row and the entry's Decision line together. (c) Item 5's deviation was implemented by editing `manifest.json` after all, so the archive's hashed record carries an editorial licence statement -- detectable by opening the published `manifest.json` and finding no `license`/`notice` key of this kind.

---

### DEC-20261017-035

**Date:** 2026-10-18
**Type:** IMPLEMENTATION
**Status:** ACTIVE
**Authority:** Owner (implements DEC-20261017-033 and DEC-20261017-034)
**Related docs:** `open_source_and_license_policy.md` §2 (v1.0 Frozen), `scripts/pack_snapshot.py`, `scripts/verify_release.py`, `tests/test_release_packaging.py`, `README.md`, `docs/README.md` (v1.17), `decision_log.md` (v1.10)
**Related risks:** R-E01

**Context:**
DEC-20261017-034 confirmed that the release archive is published with a NOTICE, and that the notice lives in a `NOTICE.txt` member rather than as a field in `manifest.json`. This entry records the implementation — including one property that only became visible once it was built.

**Decision:**

1. **`scripts/pack_snapshot.py` generates the notice.** It defines `NOTICE_TEXT` and writes `NOTICE_NAME` (`NOTICE.txt`) into the archive at `{snapshot_id}/NOTICE.txt`, from that template, deterministically: sorted member order, `mtime` pinned to the epoch, mode 0644, so the archive digest stays reproducible. A file of that name **stored in the snapshot directory is refused** with an explicit error, so the template is the single source of the notice and a stale on-disk copy cannot drift from the archive that carries it.

2. **`scripts/verify_release.py` asserts it before re-running anything.** An archive that lost its notice fails loudly instead of publishing a data dump with no statement attached. This is a **compliance property, not a numerical one** — it fails the same way the numerical bugs did, silently, on a re-pack, with the data still looking fine.

3. **The archive was re-packed.** Archive digest **`28e1d907…` → `7a3fc209…`**; size unchanged at 1.67 MB. **The bundle hash did not move** (`2ad0613913df9065b62ba2291abc391402c1eb13d36937ba8c2bbc09d637d707`) and the snapshot id did not change.

4. **Finding F31 recorded — the archive digest is not the snapshot id.** The archive digest identifies the **distribution** (data + notice); the bundle hash and snapshot id identify the **data**. Because the notice is deliberately outside the hash chain, adding a purely editorial file moved one identity and not the other. Both are correct — and that is precisely the hazard: a reader who reads the published digest as the snapshot's identity will conclude the snapshot changed, or will treat the digest as covering the data when it also covers the notice. **Mitigation:** the README's reproduction block now states what the digest is *of* and prints the bundle hash beside it.

5. **Re-verification with the notice check active:** `archive sha 7a3fc209…`, `notice NOTICE.txt present, unchanged`, `methods 7`, `columns 18`, `max abs diff 0.000e+00` → **`EXACT`**.

**Alternatives considered:**
- **Store `NOTICE.txt` under `data/snapshots/<id>/`.** Rejected — `data/` is git-ignored, so the notice would live in a regenerable directory: version-controlled by nothing, invisible in a diff, and absent from any snapshot a user rebuilds. The whole point of the notice is that it cannot be lost, and putting it outside git is how it would be lost.
- **Add a `license` field to `manifest.json`.** Rejected at DEC-20261017-034 and rejected again in implementation: the manifest is the data layer's hashed record.
- **Keep the notice only in the README and the release notes.** Rejected — the failure mode the notice exists to prevent is the data being redistributed *away from* its statement. A notice that stays in the repository does not travel inside the tarball.
- **Fold the notice into the hash chain so one identity covers everything.** Rejected — it would make an editorial change to a licence statement alter the snapshot's id, i.e. make a licensing statement part of the data. Two identities, clearly named, is the right structure; F31 is the name.

**Rationale:**
[First Principles] The archive has two jobs — being data, and being *a redistribution of someone else's data* — and those jobs have different identities. Collapsing them is what produces F31's confusion; naming them is the fix.
[Inversion] Ask how the notice gets lost: not by malice but by being a file somebody must remember to add. Generating it from a template makes forgetting it impossible; asserting it in the verifier makes losing it loud.
[Baselines] The simplest thing that works is a text file generated by the packer — no schema change, no dependency, no service. The elaborated alternative (a licence field inside the hashed record) is strictly worse.
[Goodhart] The tempting measure is "the licence policy is written", which a document satisfies. The one that matters is "the data cannot travel without its statement", which only the archive carrying it satisfies — so it is now checked mechanically rather than believed.

**Reversibility:** Soft. The notice is a template, the verifier's assertion is one function, and `manifest.json` is untouched.

**Revisit trigger:**
Yahoo, FRED or an issuer changes terms, or a third party objects → the notice text and the archive's disposition are revisited per `open_source_and_license_policy.md` §6. **The notice text is ever edited → the archive digest moves and must be re-quoted in the release notes, while the bundle hash and the snapshot id must *not* move; if they do, F31's separation has been broken and the change is not what it claims to be.**

**Expected value assessment:**
- Probability a reader would otherwise have taken the published digest as the snapshot's identity: **high (~70%)** — it is the only hash in the README, and the asset name calls it a content hash.
- Probability the notice would be omitted from a future re-pack without the verifier assertion: **moderate (~40%)** — it exists only because a script generates it.
- Probability the "store it in `data/`" alternative would have been lost: **very high (~90%)** — `data/` is git-ignored and rebuilt by script.

**Pre-mortem:**
Three ways this fails later. **(a)** The release notes quote `28e1d907…` from an earlier draft — detectable by comparing the published notes against `dist/*.sha256`. **(b)** Someone re-packs with a different `pack_snapshot.py` so the notice text differs and `verify_release.py` now rejects a "valid" archive — that is the intended behaviour, and any change to the notice must move the digest with it. **(c)** F31 is read as a defect to be fixed by *merging* the two hashes — detectable at review, since merging them requires the notice to be inside `manifest.json`'s map, which item 1 forbids.

---

### DEC-20261018-036

**Date:** 2026-10-18
**Type:** IMPLEMENTATION
**Status:** ACTIVE
**Authority:** Owner (implements the CI change agreed at DEC-20261017-034)
**Related docs:** `README.md`, `.github/workflows/ci.yml`, `docs/published-run/README.md`, `tests/test_snapshot_name_literals.py` (new), `docs/README.md` (v1.19), `decision_log.md` (v1.12)
**Related risks:** R-E01

**Context:**
Making CI verify bit-for-bit rather than merely regenerate required `verify_release.py` to compare against a committed reference table, and that required the frozen snapshot to be named in one more place. Before adding it, every literal in the repository that quotes the snapshot id was checked against the filesystem rather than against the other literals. Four were wrong. One of them is **published**: the README's reproduction command, whose `curl` returns 404 for any reader who follows it.

The wrong form is a single character — an extra underscore where the window end meets the retrieval date, `2026-09-30_2026-10-17` instead of `2026-09-30-2026-10-17`. It came from an earlier summary of this project and every later copy inherited it. While investigating, a **fresh hand-typed copy in the workflow was wrong in exactly the same way within minutes**, which is the finding: the defect is hand-typing, not the typo.

**Decision:**

1. **Finding F32 recorded.** The snapshot id is quoted by hand in the README, the CI workflow, and a document; a wrong separator is indistinguishable from the right one by reading, and fails as a 404. Load-bearing fact for the record: **the release is unaffected** — the published asset was named by `pack_snapshot.py` from the filesystem, so its name was always correct, its digest is unchanged, and CI's committed `SNAPSHOT_ID` was correct. The defect was confined to documentation and to one envelope variable that had not yet been exercised.

2. **All four literals corrected**, and the corrected README command checked by running it, not by reading it.

3. **`tests/test_snapshot_name_literals.py` added** — five checks: the archive name is *derived* from the id rather than compared to it; every quoted literal equals the workflow's `SNAPSHOT_ID`; the README's `ASSET` equals the workflow's `SNAPSHOT_ASSET`; the id equals the snapshot directory on disk when one is present; and the new `docs/published-run` document names the frozen snapshot. On a fresh clone this is a consistency check; in CI — which fetches the archive — it is checked against a real directory.

4. **The guard was shown to fail.** Reintroducing the bad separator fails **4 of the 5** tests. A check that has never been seen to fail is decoration.

5. **`docs/published-run/outcomes.csv` is committed** as the published metric table (4,777 bytes), and CI runs `verify_release.py --archive <fetched asset> --run docs/published-run --expect-sha256 <pinned digest>`. The workflow therefore compares a freshly computed table against the published one at tolerance zero — which is what the README claimed and previously did not do.

6. **A skipped end-to-end check now announces itself.** The fetch step keeps `continue-on-error: true` (a fresh clone and a pre-release repository have nothing to fetch, and a red CI teaches people to ignore CI) but emits a `::warning::` annotation naming exactly what was skipped.

**Alternatives considered:**
- **Fix the four literals and stop.** Rejected: the same mistake was made twice inside the hour, the second time by an agent that had just written the first fix.
- **Have the README derive the asset name from the release page rather than set `ASSET=`.** Rejected as the primary fix — a copy-pasteable command is worth more to a reader — but the literal is now enforced rather than trusted.
- **Make the fetch step fail when the asset cannot be fetched.** Rejected for the reason the workflow's own header gives: before a release exists there is nothing to fetch, and a CI that is red on a fresh clone is a CI people learn to ignore. A visible warning is the honest middle.
- **Exempt the workflow's `SNAPSHOT_ID` from the naming test because CI checks it anyway.** Rejected: CI is precisely where it matters, and the step that would catch it sits behind the `continue-on-error` fetch.
- **Rename the snapshot to match the typo.** Rejected without discussion: the id is content-derived and embedded in the published asset name and the archive manifest.

**Rationale:**
[First Principles] An identifier that a human retypes is hand-entered data, and the filesystem already knows the answer. The fix is not care, it is derivation, plus a test for the places where derivation is not possible.
[Map is Not the Territory] The four literals agreed with each other's *shape* and disagreed with the thing itself. Comparing copies to copies would have found nothing; the defect was found only by comparing to the filesystem.
[Inversion] Ask how a 404 stays invisible: it is wrapped in `continue-on-error`, and the step it feeds is one whose absence looks like success. So the second half of the fix is making the skip announce itself.
[Goodhart] The tempting measure is "the README has a reproduction command". The measure that matters is "the command works", knowable only by running it against the thing it names.
[Path Dependence] The wrong form came from an early summary and was inherited by every later copy. Cheap to fix now, expensive to keep, which is the argument for one authoritative source and a test rather than for proofreading.

**Reversibility:** Soft. Four literals, one new test file, one workflow step, one committed CSV.

**Revisit trigger:**
A genuinely different snapshot id appears in the repository (e.g. after a rebuild) -> the literal goes into the test's allowlist with a reason, rather than the test being loosened. A second snapshot exists on disk -> the "exactly one" assertion becomes a loop over the snapshots actually present. The release asset is renamed -> the warning annotation says so, and the name is fixed at its source of truth: the filesystem.

**Expected value assessment:**
- Probability a reader would have hit the 404 before anything else: **high (~60%)** — it is the first command in the reproduction block, and the block is the repository's central claim.
- Probability the class recurs without a test: **high (~70%)**, evidenced by a repeat within the same hour.
- Probability the committed reference table catches a real regression: **moderate** — it fires on any change to the pipeline's arithmetic, which is the point, and will be annoying exactly once.
- Residual risk, stated rather than hidden: a wrong asset name is still a warning and not a failure. Accepted because the alternative is a CI that is red on every fresh clone; mitigated because the name is now pinned by a test rather than by attention.

**Pre-mortem:**
Three ways this fails later. **(a)** Someone silences the naming test by allowlisting a literal with no reason — detectable because the allowlist is a short, commented set that a reviewer must read. **(b)** CI shows a warning nobody reads, and the end-to-end half quietly stops running for months — detectable by checking that a recent run shows the step that re-runs every method and compares against `docs/published-run` as having *run*, rather than as skipped. (This bullet originally quoted that step's name verbatim; DEC-20261018-038 renamed the step, so the detection procedure now describes it instead of quoting it — the same lesson as this entry: an identifier written down twice drifts, so write it down once and check it against the thing itself.) **(c)** The committed reference table is regenerated from a buggy run, making the check agree with the bug — detectable because the digest of the archive is pinned separately, so the table and the archive cannot drift together without the pinned digest also changing.

---

### DEC-20261018-037

**Date:** 2026-10-18
**Type:** IMPLEMENTATION
**Status:** ACTIVE
**Authority:** Owner (fixes what the CI check added at DEC-20261018-036 found)
**Related docs:** `src/robustfolio/metrics.py`, `tests/test_metrics.py`, `README.md`, `docs/published-run/outcomes.csv`, `docs/published-run/README.md`, `docs/README.md` (v1.20), `decision_log.md` (v1.13)
**Related risks:** R-E01

**Context:**
The workflow step added at DEC-20261018-036 re-runs every method from the release archive and compares the result to the committed published table at tolerance **exactly zero**. It ran on commit `6040f7e` and **failed** (run 39132731808):

```
MISMATCH on the following columns:
  autocorr1: 4.163e-17
max abs diff : 4.163e-17
columns      : 18
```

Seventeen of the eighteen columns the verifier compares matched **bit-for-bit** across Windows and the Linux runner. The eighteenth, §7.7's lag-1 autocorrelation, was three units in the last place out.

**Root cause, established rather than guessed.** `metrics.autocorr1` ended in `float(np.corrcoef(current, lagged)[0, 1])`. `np.corrcoef` builds on `np.cov`, which builds on the BLAS `ddot`/`dgemm` kernels, and OpenBLAS picks its kernel **at runtime** from the CPU's feature set. A reduction whose *order of summation* depends on the answering CPU is not required to give the same last bits. Nothing was wrong with the archive, the data, or the metric's logic: the arithmetic was under-specified, and a check that asserts equality found the place where that mattered.

**Decision:**

1. **Finding F33 recorded.** *A claim of bit-for-bit reproduction is a claim about arithmetic, not about the data — and it silently depends on run-time CPU dispatch in the linear-algebra layer.* This is the same family as F2 and F19 (implementation detail masquerading as a stronger property than it is), but located in a dependency rather than in this repository's code.

2. **`metrics.autocorr1` no longer goes through BLAS.** It is computed by a new `metrics._pearson_exact`, which uses `math.fsum` for the means and for the sums and otherwise uses only operations IEEE-754 *requires* to be correctly rounded: subtraction, multiplication, division, square root. Every rounding step is therefore defined by the standard, so the result is bit-identical on any conforming platform. It is also the more accurate of the two formulations, because a vectorised dot product is not required to be correctly rounded.

3. **The published table was regenerated, and the diff of that regeneration is the evidence rather than the assertion.** All 46 columns compared; **exactly one changed** — `autocorr1`, worst case `9.714e-17` (B3). **No headline number moved**, so every figure quoted in the ledger remains valid, and the change is invisible at the three decimals the report prints.

4. **Two mechanical guards added** (`tests/test_metrics.py`). `test_autocorr1_does_not_go_through_a_blas_reduction` parses the module's call graph and asserts that nothing named `corrcoef` is *called* — a value test cannot guard this, since the formulations differ by less than any tolerance worth writing down, and it is deliberate that the guard reads calls rather than text so that the module may still document `corrcoef`. `test_pearson_exact_is_the_correctly_rounded_correlation` checks the new path against an exact-rational reference computed with `fractions.Fraction`, so it does not agree with the implementation merely by reusing its arithmetic.

5. **The residual limitation is stated, not papered over.** The estimator's covariance (`np.cov`), the conditioning diagnostic (`np.linalg.cond`, `eigvalsh`) and the solver's own linear algebra still run inside BLAS/LAPACK. Their last-bit behaviour is not this repository's to define. What is claimed is what has been checked: tolerance exactly zero, against a pinned archive digest, on two platforms.

> **Corrected 2026-10-18, DEC-20261018-038 — within the hour, by this entry's own check.** The last sentence above was false the moment it was tested again. The next CI runner mismatched **thirteen** of the eighteen columns, the worst by `4.698e-12`, and no amount of arithmetic specification in this repository would have prevented it: the cause named in this very item (runtime-chosen BLAS kernels, plus a solver whose own tolerance defines the optimal point) is exactly what produced the difference, amplified by the solver from `1e-16` to `1e-12`.
>
> Item 1's *diagnosis* stands and was correct: a bit-for-bit claim is a claim about arithmetic, and it silently depended on runtime CPU dispatch. Item 5's *conclusion* — that the residual could be disclosed while the strong claim was still made — did not survive. The corrected claim is not weaker, it is better aimed: **decisions exact, measurements bounded**, with the bound measured rather than asserted. See DEC-20261018-038 for the split and for why "exactly zero" was the wrong property to want from a solver's output.

6. **The release is unaffected.** The archive, its digest `7a3fc209…`, the bundle hash and the snapshot id are all unchanged; the fix is in the code that *reads* the archive and in a table that lives in the repository.

**Alternatives considered:**
- **Relax the verifier to a tolerance (e.g. 1e-15) and keep the existing wording.** Rejected: it would convert a discovered defect into a permanent caveat, and it would weaken the one check in this repository that can distinguish "the code still runs" from "the code produces the same numbers". The tolerance is exactly zero *because* that distinction is the point.
- **Leave the comparison exact but exclude `autocorr1` as a diagnostic column.** Rejected as a first resort: it treats a symptom. The column's value was in fact reproducible; only its *computation* was not, and that is fixable in five lines. It remains available as a fallback if a genuinely unfixable column ever appears.
- **Compute the whole estimator path without BLAS.** Rejected: an 18x18 covariance and the solver's linear algebra would have to be hand-rolled, adding more risk than the dependence removes, and correctness of those routines is *better* served by LAPACK than by this repository. Cheap where it is cheap, stated where it is not.
- **Weaken the README claim instead of the arithmetic** ("reproduces to within floating-point tolerance"). Rejected for the same reason as the first alternative, and because the sentence had been true on the development machine for hours; the failure was the most useful thing the new check produced.
- **Keep the fix local and skip the essay hook.** Recorded as a poor use of the finding: this is the clearest concrete instance the project has of "a claim nobody could test was softer than it sounded, and the moment it became testable it was false".

**Rationale:**
[First Principles] "Reproduces bit-for-bit" is a statement about summation order. Summation order inside a BLAS kernel is chosen at runtime by `DYNAMIC_ARCH` dispatch. So the claim was not merely unverified, it was not *entailed* by anything the repository had written down.
[Map is Not the Territory] The map said "tolerance exactly zero, therefore exact"; the territory said seventeen columns. No amount of re-reading the map would have found it.
[Inversion] How does a reproduction claim become false without anyone doing anything wrong? Let a dependency make a choice the standard permits, and put the claim in a place where only one platform can see it. Both halves are removed: the arithmetic is now fully specified, and a second platform now runs the check on every push.
[Goodhart] The tempting measure is "the verifier passes". The measure that matters is "the verifier passes on another machine, at zero tolerance". Chasing the first would have ended in a tolerance parameter.
[Path Dependence] The choice of `np.corrcoef` was made when it looked like the clearest transcription of §7.7's formula. It *is* the clearest transcription; it is simply not a *specified* one. Cheap to replace, expensive to leave.

**Reversibility:** Soft. One metric function, two tests, one regenerated table. Reverting would restore a known, documented, platform-dependent defect.

**Revisit trigger:**
The verifier fails again on a different column -> the next BLAS/LAPACK dependence has surfaced, and the diagnosis starts from the same question: is the *arithmetic* specified, or merely conventional? A column whose value cannot be made platform-independent -> it becomes the first entry in a documented exception list, and the README says why. Python or numpy gains a documented determinism guarantee for the relevant reductions -> the hand-rolled reduction could be replaced by a simpler call.

**Expected value assessment:**
- Probability the new check would find something on its first real run: **observed, 1.0** — it did, within one commit of being added. That is the strongest evidence available that the check was worth adding, and it is evidence of the kind this project has repeatedly found: the interesting failures arrive the moment a claim becomes testable.
- Probability a consumer of these numbers is affected by the `autocorr1` change: **negligible** — it is a diagnostic, it moved in the 17th digit, and the report prints three decimals.
- Probability the class recurs elsewhere: **moderate**, because the covariance and the solver still sit on BLAS; disclosed above rather than estimated away.
- Residual risk: the guards test the *mechanism* on this platform, not cross-platform equality. The cross-platform evidence is the CI run, which is per-push. Stated.

**Pre-mortem:**
Three ways this fails later. **(a)** Someone "simplifies" `_pearson_exact` back to `np.corrcoef` because it looks like reinvention — detectable because the guard names `corrcoef` and the docstring says why. **(b)** A future column becomes platform-dependent and the response is to add a tolerance, quietly retiring the zero-tolerance claim — detectable because the claim is written in three places and a tolerance parameter would have to be added to `verify_release.py`, which is a visible diff. **(c)** `math.fsum` on a long series becomes a performance problem in some future, larger experiment — measurable, and the fallback (pairwise summation with a fixed block order) is a known alternative rather than an unknown one.

---

### DEC-20261018-038

**Date:** 2026-10-18
**Type:** IMPLEMENTATION
**Status:** ACTIVE
**Authority:** Owner (fixes what the CI check added at DEC-20261018-036 found, twice)
**Related docs:** `scripts/verify_release.py`, `tests/test_release_verification.py`, `src/robustfolio/report.py`, `README.md`, `docs/published-run/README.md`, `.github/workflows/ci.yml`, `notes/release_essay_draft.md`, `docs/README.md` (v1.21), `decision_log.md` (v1.14)
**Related risks:** R-E01

**Context:**
DEC-20261018-037 was pushed as `65a0c82`. The workflow step added at DEC-20261018-036 — "re-run every method from the release archive and compare against the committed table" — ran again and **failed again** (run 39134078120), this time on **thirteen** of the eighteen columns:

```
MISMATCH on the following columns:
  kurtosis: 4.698e-12                net_sharpe_10bps: 2.837e-12
  turnover_annualized: 4.307e-12     net_sharpe: 2.837e-12
  gross_sharpe_diagnostic: 2.875e-12 net_sharpe_20bps: 2.799e-12
  net_sharpe_0bps: 2.875e-12         net_sharpe_50bps: 2.682e-12
  net_sharpe_5bps: 2.856e-12         skew: 5.979e-13
                                     autocorr1: 1.052e-13
                                     cvar95: 6.642e-14
                                     max_drawdown: 3.442e-15
```

DEC-20261018-037 had fixed one metric's arithmetic and written, in its item 5, that the residual (BLAS and LAPACK inside the estimator and the solver) was *disclosed*. That sentence was falsified within the hour by the check it described. It is corrected in place above.

**What was established, rather than assumed:**

1. **Not the environment.** The two runs' install lines were parsed as sets — 51 packages in each, **symmetric difference empty** (`numpy 2.2.6`, `scipy`, `clarabel 0.11.1`, `cvxpy 1.7.5`, `pandas 2.3.3`, all identical). The runner image is identical too (`ubuntu24/20261012.334.1`). The only difference the record shows is the machine: `GitHub Actions 1000000268` versus `GitHub Actions 1000000269`.
2. **Not thread count.** The whole pipeline was run locally with `OPENBLAS_NUM_THREADS=1` and `OPENBLAS_NUM_THREADS=4`. The two tables are byte-identical to each other **and** to the published table. Whatever varies between those two runners, it is not how many threads BLAS chose.
3. **The divergence is in the weights, not in the reporting.** `turnover_annualized` is a function of the portfolio weights alone — it does not touch the return series — and it moved by `4.307e-12`. So the two runs solved to slightly different portfolios, and the metric differences are downstream of that.
4. **The magnitude says "solver", not "last bit".** A last bit at these magnitudes is `1e-16`. The largest
   difference is `4.698e-12` — four orders of magnitude larger — consistent with a `1e-16` perturbation of
   the covariance matrix being amplified by an optimiser whose acceptance tolerance is the frozen
   `SOLVER_TOL = 1e-14`. (This item said the differences were "`1e-13` to `1e-12`" until the thirteen
   values were read back off the log; the smallest is `3.4e-15`. The corrected form states the largest,
   because that is the quantity the argument turns on.)

**Finding F34.** *A number produced by a solver is a property of (data, code, machine), not of (data, code).* Where a computation contains an iterative optimiser, its output is defined only to the solver's tolerance; any claim about its exact digits is a claim about one run, not about the result. This is the same family as F33 one level up: F33 was a claim about arithmetic that turned out to be a claim about a dependency's runtime behaviour, and F34 is a claim about a *result* that turned out to be a claim about a *run*.

**Decision:**

1. **The verifier's claim is split rather than widened.** `scripts/verify_release.py` now separates what is exact from what is measured:
   - **Exact** (any difference fails the build): the method set and its order, `rebalances`, `folds`, the headline cost level, the **ranking** of the methods by net Sharpe, and **which baseline** the §6.1/§6.2 rules select. These are discrete, they are what the experiment is for, and a `1e-12` wobble cannot move them.
   - **Within `TOLERANCE`** (documented constant, `1e-9`): the continuous metrics. The observed worst difference is printed on every run, so the bound is spent in public rather than asserted.
   The failure messages now distinguish the two cases, because they mean different things: a decision mismatch says *this is a different experiment*, while a tolerance breach says *this is a different result*.
2. **`TOLERANCE = 1e-9`, justified by measurement rather than convenience.** It is ~200x the worst cross-platform difference measured (`4.698e-12`) and **five** orders of magnitude below the four decimals at which any of these numbers is quoted or compared. (Five, not six: this sentence said "six" until it was checked against the exponent it names — a hand-written margin is a claim, and it was the same class of error as the one this entry is about, one paragraph over.) It is loose enough to absorb a runtime-chosen kernel and far too tight to absorb a changed estimator, cost model or window. The derivation is in the constant's comment, where the next person will look.
3. **The comparison was extracted as a pure function (`compare`) and covered by ten hermetic tests** (`tests/test_release_verification.py`), built on synthetic tables so they run on a fresh clone. They assert the properties that matter, not the numbers: platform noise (`4.698e-12`) passes; a change of `1e-6` — the scale of a real estimator bug — fails; a changed rebalance count, a reordered ranking, or a different best baseline fails **even though every metric is within tolerance**. A test also pins `TOLERANCE` and the exact-column set, so the constant cannot drift silently.
4. **The F33 fix is kept and its description is not overstated.** `autocorr1`'s exactly-rounded summation removes a genuine platform dependence at no cost and makes the metric layer exactly reproducible *given the same inputs*. What it does not do — and what DEC-037's wording implied it did — is make the whole pipeline platform-independent.
5. **Every public claim is corrected in place, in the same commit.** `README.md` (the reproduction block's comment, the reference-table paragraph, the CI status row), `docs/published-run/README.md` (rewritten — its previous section was titled "the equality is a property of the arithmetic, not of the machine" and is now titled "what reproduces exactly, and what reproduces to a bound"), and `ci.yml` (the step name and its header comment). Leaving a sentence the check has just falsified is the drift F29 named, one document over.
6. **The manifest now records the part of the environment that varies between identical machines** (`report._blas_context`): the BLAS build and its `DYNAMIC_ARCH` ceiling, the thread-control variables, the core count, and the processor. When this happened, the record could not say why, and the answer had to be found by re-running the pipeline under a forced thread count. A record that does not name what varies cannot explain a difference in what it records.
7. **The release is unaffected.** The archive, its digest `7a3fc209…`, the bundle hash and the snapshot id are unchanged: the change is in a script that *reads* the archive, in the record a run writes about itself, and in prose.

**Alternatives considered:**
- **Widen the tolerance silently and keep the wording.** Rejected. This is the failure mode the finding is about: the claim would again be a property of the environment it was tested in, and the next failure would be discovered by a stranger rather than by CI.
- **Set the tolerance at `1e-6` "to be safe".** Rejected: safety from false alarms bought by losing the ability to detect a real one is not safety. `1e-9` keeps four orders of margin over the measured noise and still catches every change that matters.
- **Make the covariance deterministic (replace `np.cov` with a specified reduction, as F33 did for `autocorr1`) and keep the zero-tolerance claim.** Rejected as the *fix for this decision*, and recorded as the natural follow-up. It removes one of the two suspected sources and cannot address the other (the solver's own tolerance is not this repository's to define). It would also change every published number in the 16th digit and require regeneration plus re-verification, for a property — cross-platform bit equality of a solver's output — that is not what the artefact is for. If exact cross-platform equality ever becomes a requirement, this is the first thing to try, and the verifier's split makes the attempt measurable: the `max abs diff` line would report whether it worked.
- **Drop the comparison and keep "one command regenerates the number".** Rejected: that is exactly the weaker claim DEC-20261018-036 existed to replace. The exact half — decisions — is the half with the value, and it survives intact.
- **Compare only decisions, with no metric comparison at all.** Rejected: a changed cost model can move net Sharpe by `1e-3` while leaving the ranking identical. The bounded comparison is what catches that, and it is now the only thing that would.
- **Commit `decisions.csv` and compare the decision table exactly.** Deferred, not rejected. The current exact checks derive the decision-bearing quantities from the published table itself (ranking, best baseline), which needs no extra artefact. If the §6 rules ever gain a quantity that the table does not imply, this becomes the natural next step — recorded here so that it is a remembered option rather than a re-derivation.

**Rationale:**
[First Principles] What is the artefact? A set of numbers **and the decisions drawn from them**. The decisions are discrete and must be exact; the numbers are continuous and are defined only to the solver's tolerance. The original claim conflated the two and took the strength of the first for the second.
[Map is Not the Territory] The map said "tolerance exactly zero"; the territory said `4.698e-12`. This is the second time in two commits that the same class of error fired (F33, F34), and when a class fires twice the response has to change the class. The class is: *a claim whose truth is a property of the environment in which it was tested.* The repair is not a better instance of the claim; it is a claim that names its environment.
[Inversion] How does this fail from here? By making the check green. Every such failure mode is a widening of `TOLERANCE` until a real regression fits inside it, and each widening is locally reasonable. The defence is structural: a bound derived from a measurement, printed on every run, pinned by a test, and paired with an exact comparison that no bound can touch.
[Goodhart] "CI is green" is the proxy; "the same result reproduces on another machine" is the goal. A tolerance bought to make the proxy true is the textbook substitution. The chosen bound is 200x the noise and `1e-6` of the published precision, so a change large enough to matter cannot hide inside it.
[Probabilistic Claims] The claim is now quantitative and two-sided: *decisions identical; measurements within `1e-9`, worst observed `4.698e-12`.* A reader can falsify either half with one command, and neither half borrows the other's strength.
[Order and Path Dependence] Had the first CI runner been the second one, the claim would have started at `1e-9`, `autocorr1`'s defect would have been invisible, and F33 would not exist. Two runs were needed to separate two causes that a single failure conflates. This is a real limit on the method: **two machines is not a sample.** The bound is empirical, and the revisit trigger says so rather than implying a population guarantee.

**Reversibility:** Soft. One script, one test file, one diagnostic field in the manifest, and prose. Reverting restores a claim that is known false on at least one machine out of three observed.

**Outcome (2026-10-18, same day).** CI run 39136157646 on `089541f` — a *third* distinct machine, `GitHub Actions 1000000270` — ran the reworked comparison end to end and passed:

```
notice       : NOTICE.txt present, unchanged
methods      : 7
columns      : 18
max abs diff : 4.698e-12
tolerance    : 1e-09
WITHIN 1e-09: ... every decision-bearing quantity ... is identical.
```

Three things are worth recording rather than celebrating. First, the verifier printed the **observed** difference, not the bound: a reader of the log sees `4.698e-12`, not "within tolerance". Second, the value is **identical** to the worst difference on the failing run, which suggests a stable platform difference rather than random variation — so the bound was set above a quantity that repeats. Third, and stated against interest: this run's machine agrees with the *failing* run's machine while the *first* run's machine agreed with Windows on seventeen of eighteen columns. The evidence base is three machines; it establishes that the difference exists, that it is bounded and reproducible, and that it does not move any decision. It does **not** establish which kernel differs, and no entry here should be read as claiming otherwise.

**Revisit trigger:**
CI fails on the measurement comparison with a *large* difference (`> 1e-8`) -> this is not kernel noise; treat it as a genuine reproduction failure and look for a changed estimator or a changed window before touching the constant. CI fails on the measurement comparison with a small difference (`~1e-12`) on a third distinct hardware configuration -> the empirical bound was too tight, **measure again and raise it with the measurement recorded**, never silently. A decision-bearing quantity appears in the published table as a continuous column -> add it to the exact checks (`EXACT_COLUMNS` or a new exact comparison), because a probability that is compared with a tolerance is a decision that can move. Exact cross-platform equality becomes a requirement (a reviewer asks for it) -> attempt the deterministic covariance named above, with the `max abs diff` line as the metric. `np.show_config`'s shape changes -> `_blas_context` degrades to `"unavailable"` rather than failing a run, which the test allows for by pinning the keys only.

**Expected value assessment:**
- Probability the check would find something on its second run: **1.0, observed**. Two runs, two failures, both real, both in a sentence written within the prior hour. A check that has produced two correct falsifications of its author's own claims in two attempts is the single most valuable thing in this repository, and the reason is structural rather than lucky: the claims were written *before* the check existed.
- Probability a consumer of these numbers is affected by any of this: **zero to one part in `1e-12`**. The published table moved in one diagnostic column's last bits; the headline numbers were untouched; the release is byte-identical.
- Probability the same class appears again in a different form: **high**, because the class is "the claim is broader than the mechanism". Declared, with the trigger above.
- Residual risk: the bound is empirical and rests on three machines. Stated rather than smoothed over.

**Pre-mortem:**
Three ways this fails later. **(a)** Someone raises `TOLERANCE` to silence a red build — detectable because the constant is asserted by a test, documented in a comment that gives its derivation, and named in the README and in `docs/published-run/README.md`; a change is a visible diff in four places rather than a quiet edit in one. **(b)** A future decision rule moves onto a continuous quantity (a probability rather than a ranking) and the exact half silently stops covering it — detectable because `HEADLINE_METRIC` is asserted by a test, and because this entry's revisit trigger names the case. **(c)** A reader concludes that "within `1e-9`" means the numbers are soft — answerable with one command, which prints the actual difference (`0.000e+00` on the reference machine) rather than the bound, and with the release digest pinned so the comparison cannot drift with the input.

---

### DEC-20261018-039

**Date:** 2026-10-18
**Type:** GOVERNANCE
**Status:** ACTIVE (the document it introduces is a **Draft** and binds nothing)
**Authority:** Owner (freeze deferred; see item 5)
**Related docs:** `docs/results_reporting_and_claims_policy.md` (v0.1, Draft), `docs/README.md` (v1.23), `tests/test_docs_index.py`, `notes/release_essay_draft.md`
**Related risks:** R-G01

**Context:**
Protocol §14 says "Every experiment result is reported in a standard format. See `results_reporting_and_claims_policy.md` for the full template (to be written before Phase 4)"; Appendix B item **E3** carries it as pending; and two frozen documents promise to reduce to a pointer once it exists (E7 §5, and DEC-20261017-034's non-confirmatory phrasing rule). The rules themselves already bind — §14.2 is frozen — but they live in four places, and a rule that lives in four places is a rule that will be quoted from whichever copy flatters the claim.

**Decision:**

1. **E3 is written, as a Draft.** `docs/results_reporting_and_claims_policy.md` v0.1, `**Status:** Draft`, registered on the status board as row 9 so that the board's own cross-check covers it. It binds nothing until the owner confirms it (item 5), and its purpose is stated in its opening: two questions — how a result is reported, and what may be claimed from it.
2. **Every rule in it is marked `[frozen]` or `[PROPOSED]`, with the `[frozen]` ones naming their source.** This is the document's central design choice rather than a formatting one. A policy that quietly acquires authority it was never granted is the same failure as a claim that outruns its number, and this project has spent the day finding that failure twice (F33, F34). A reader can therefore tell at a glance what is a restatement of a binding rule and what is a proposal.
3. **The reporting template maps §14.1's nine disclosures to exact fields** (§2), because "the disclosures are reported" is a claim, and a claim is worth what its checkable form is worth. The mapping surfaced one fact worth naming: `psr_benchmark` is a **column**, so "no p-value without its benchmark" is enforced mechanically rather than remembered — which matters more here than the multiple-testing correction, because with `N = 1` the deflation is inert and the benchmark *is* the finding.
4. **§4 operationalises §14.2's six prohibitions with the compliant form for each**, plus four additions each tied to a defect this repository actually had: a reproduction claim names its command (F32), is stated at the strength its check has (F33/F34), distinguishes a mechanism from a result, and never quotes a table without naming the table's status. §3 fixes the status vocabulary, including that an `EXECUTED (NON-CONFIRMATORY)` verdict is `FAILURE` while the hypothesis remains **untested, not falsified**.
5. **Freeze is deferred, and the five open values are collected as one decision-ready table (§8, P1–P5)** rather than scattered through the text. They are: whether E3 becomes a governed document; whether `CONFIRMATORY` requires a blind registration against a sample that does not yet exist; whether the template binds future experiments or describes this run; whether a public post is a governance event for §4; and whether the two shorter cuts of the flagship essay are governed identically. **Per the standing rule, no value has been chosen silently.**
6. **A drift was found while adding the board row, and the fix is structural.** The sentence above the status board said the active documentation set was *seven* files while the board listed *eight*, and had said so since E7 became row 8 — in the same document whose revision history reports fixing exactly that class of error (**F29**: a value written down twice drifts). The count is now **counted against the table** by a new test rather than kept by hand, which is F32's lesson ("derive identifiers, do not retype them") applied to a number.

**Alternatives considered:**
- **Write E3 as a section of the protocol instead of a document.** Rejected: the protocol is Frozen at v2.4, and amending it to add a reporting template would be a versioned contract revision for material that is operational rather than definitional.
- **Write E3 and mark it Frozen now.** Rejected on the project's own rule: write and freeze are separate acts, and freeze requires owner confirmation. A document that declares itself frozen without that confirmation is the ambiguity `tests/test_docs_index.py` exists to prevent.
- **Skip E3 for v1, since §14.2 already governs claims and Phase 4 is not reached.** Rejected, narrowly: the flagship essay and its two cuts will cite these rules, and citing four documents is worse than citing one. But the *reason* it is safe to write now is that it binds nothing — which is also why it is a Draft.
- **Fold the `[PROPOSED]` items into the document body without marking them.** Rejected: that is how an unconfirmed value acquires authority.
- **Fix the board's prose count by writing "nine" carefully.** Rejected as the repair of a symptom: the count had already drifted once, and the class is fixed by counting it where the table is.

**Rationale:**
[First Principles] What is a claims policy for? To make it impossible to state something true-looking that the numbers do not support. That means its rules must be *checkable where possible* and *explicitly marked* where they are not — which is why §2 maps disclosures to columns and §1 says an unenforceable rule is written with its enforcement gap named.
[Map is Not the Territory] The document distinguishes what binds from what is proposed because the map here is partly aspirational. Saying so is what keeps the map usable.
[Goodhart] The tempting measure of a policy is that it exists. The measure that matters is whether a reader can tell which sentences are binding, and whether the binding ones are checkable. §2 and the `[frozen]`/`[PROPOSED]` marking are both aimed at that, not at completeness.
[Path Dependence] The rules accumulated in four places because each was written when it was needed — §14.2 in the protocol, the licence policy's §5 for the release, DEC-034 for the relabelling. Consolidating them creates a single point of failure in exchange for a single point of truth, which is only acceptable if the consolidation is faithful; hence §9's rule that a revision of §14 revises this document in the same act or kills it.
[Inversion] How does E3 make things worse? By becoming a document people cite *instead of* the protocol. §1's precedence rule is the whole defence: §14 wins any conflict, and this document may not weaken it.

**Reversibility:** Trivial. One unregistered-feeling document, one board row, one test. Deleting it restores the status quo ante with no decision unmade, because nothing in it binds.

**Revisit trigger:**
Owner confirms P1–P5 -> the document goes to **v1.0 Frozen**, E7 §5 and DEC-034's phrasing rule reduce to pointers, and the freeze is recorded in a new entry. P1 rejected -> the document is withdrawn and its rules stay where they are; §9 records that the duplication is accepted. Protocol §14 revised -> this document is revised in the same act or deleted. A contested public claim is resolved by a rule not found here -> §4 gains the rule, or the document is shown to be incomplete and says so.

**Expected value assessment:**
- Probability the essays cite this document rather than §14.2 directly: **high** — and that is the value, provided the precedence rule is respected, because a single citable home is what stops the four copies from being quoted selectively.
- Probability an open value (P1–P5) is resolved wrongly by this document acting as if confirmed: **low by construction**, because none of them is asserted as a rule and all five are collectable in one table.
- Probability the marking discipline (frozen vs proposed) survives contact with future edits: **moderate** — the risk is that a later editor writes a rule in the flat voice the other documents use. The mitigation is the opening paragraph, which explains *why* the marking exists rather than merely requiring it.

**Pre-mortem:**
Three ways this fails later. **(a)** E3 is cited as authority for a claim that only §14 governs — detectable because §1 states the precedence and the first thing a dispute would check is the protocol. **(b)** The `[PROPOSED]` markers are stripped when the document is frozen without confirming P1–P5 — detectable because freezing is recorded in a new entry that must name each confirmation. **(c)** It becomes a tenth document nobody reads, and the four original copies are quoted again — detectable by the board row's "Draft" status persisting without a freeze decision, which is a visible unresolved state rather than a silent one.

---

### DEC-20261018-040

**Date:** 2026-10-18
**Type:** GOVERNANCE
**Status:** ACTIVE
**Authority:** Owner (all five values and both readings confirmed by the owner, not inferred)
**Related docs:** `docs/results_reporting_and_claims_policy.md` (v1.0, **Frozen**), `docs/open_source_and_license_policy.md` (v1.1), `docs/README.md` (v1.24), `essays/`, `tests/test_docs_index.py`
**Related risks:** R-G01

**Context:**
DEC-20261018-039 wrote E3 as a Draft in which every rule was marked `[PROPOSED]` — binding nothing — and collected the five open values as P1–P5 in one table. The three essays were then written against it and cite it, which is the moment the choice had to be made: publish an essay that cites a *draft*, or freeze the document it cites. The owner chose to freeze first. Two specification readings (F24, F25) had also been **disclosed rather than settled** since DEC-20261017-031, and one of them decides a published claim, so they were put to the same act.

**Decision:**

1. **E3 is frozen at v1.0** and is a governed document: status-board row 9, versioned, cross-checked against its own header by `tests/test_docs_index.py` like every other board row. The check that a *freeze* is real is that the board and the document agree about the word.
2. **The draft's marking is replaced, not deleted.** Every rule now carries `[§14]` — a restatement of a rule already frozen in the protocol, which wins any conflict — or `[E3]` — this document's own rule, binding since v1.0 and revisable only by a new entry here. The `[PROPOSED]` marker is gone because the proposals are resolved, and §8 is now the **freeze record**: the five values with what was confirmed, so that a reader can tell a granted rule from an assumed one without taking the document's word for it.
3. **All five values confirmed as proposed.** P1 (governed document); P2 (`CONFIRMATORY` requires a blind registration against a sample that did not exist when the registration was written, named in the same sentence); P3 (the §2 template binds future experiments — an empty row is recorded with its reason, never omitted); P4 (**a public post is a public artefact**, so §4 governs the post text and not merely the document it links to); P5 (the two shorter cuts are governed identically to the flagship, so no cut may say what the long form may not).
4. **F24 and F25 are confirmed as readings, in the same act.** F24: the calibration's **return** half is implemented (trailing 60 months of the method's own net portfolio returns, stationary bootstrap, next month's net return as the realisation; coverage 81.5–87.0%) and the **volatility** half is deliberately not implemented, because at a one-month horizon no monthly volatility is realised and any figure would be a definition rather than a measurement. F25: fold wins are counted on **net Sharpe** (§2's primary metric) while the concentration clause uses the **per-fold mean monthly net excess return difference**, because the clause needs an additive decomposition and a Sharpe is not one. **F25 is load-bearing and is recorded as such: the concentration clause is the binding one for `M2` at 51.3%, so this reading — not the arithmetic — is what produces the published `FAILURE` verdict.** Confirming it freezes the verdict as published; the alternative was to leave a published result resting on an unconfirmed interpretation.
5. **The licence policy's §5 is reduced to a pointer, and E7 goes to v1.1.** E7's own review trigger said this would happen when E3 was written ("§5 is reduced to a pointer, so that the claim rules exist in exactly one place"), and the trigger is now marked fired. §5's two rules — quoting a number with its interval, cost level and exploratory status; and findings describing this implementation rather than upstream library defects — exist in E3 §5 and §6.
6. **Nothing that affects the release changed.** The `NOTICE.txt` in the archive is generated by the packaging code and pinned by `tests/test_release_packaging.py` against the archive member; it is not read from E7's prose. The archive, its digest, the bundle hash, the snapshot id and the published table are untouched. This is a documentation act and can be reversed without re-publishing anything.

**Alternatives considered:**
- **Publish while E3 is a draft.** Rejected by the owner. A reader checking "what are the claim rules" would be sent to a document that says it binds nothing, which is weaker than protocol §14 alone, and it would make the essays cite a document with less authority than the essays claim for it.
- **Freeze E3 with the `[PROPOSED]` markers left in place as history.** Rejected: a marker describes a status, and a frozen rule marked "binds nothing until confirmed" is an internal contradiction that the board's cross-check cannot resolve. The §8 record preserves the same information in the form a reader can act on.
- **Keep E7 §5 as it stands and let the duplication persist.** Rejected: E7 promised the reduction, and the four-copies problem was the reason E3 exists.
- **Amend E7 by deletion rather than reduction.** Rejected: a section that silently disappears from a frozen document is indistinguishable from an edit someone did not want to explain. A pointer says where the rule went.
- **Leave F24/F25 open and note in the essays that a reading decides the verdict.** Rejected: honest but unstable. An interpretation that decides a published conclusion should be settled before the conclusion is published as settled.
- **Re-open F25 and re-derive the verdict on the other reading.** Rejected, and worth stating why: the alternative reading (concentration on fold-wise Sharpe differences) is not better defined than the chosen one — a Sharpe is not additive, which is the whole reason §6.3's clause is ambiguous — so the change would trade a stated reading for an unstated one. The ambiguity is disclosed (F25), which is the remedy the protocol provides for an under-specified threshold.

**Rationale:**
[First Principles] *What is a frozen policy for?* To let a reader tell which sentences bind. The `[§14]`/`[E3]` marking answers "does this overrule the protocol?" and the §8 record answers "was this granted?" — the two questions a policy's authority actually rests on.
[Map is Not the Territory] The document's authority was a claim about the document, and until the confirmation act it was false. §8 is the map of the act.
[Inversion] How does freezing E3 make the project worse? By creating one more place where a claim can be *thought* to be checked — so §9 names the check that verifies the freeze itself (the board cross-check), and §2 keeps the mapping column-by-column rather than asserting coverage.
[Goodhart] The tempting measure of a claims policy is that it exists and is frozen; the measure that matters is whether a disputed sentence can be resolved by pointing at a rule. The two-category marking and the §8 record are what make pointing possible.
[Probabilistic Claims] F25's confirmation makes the published verdict conditional on a *named* reading, in public, where the alternative was a verdict that quietly depended on one.
[Order and Path Dependence] The essays were written first, which forced the decision now rather than later — and the draft state is what made it safe to write them first, because nothing they cited bound anything until this act.

**Reversibility:** Soft and cheap in the sense that matters. E3 can be revised by a new entry; the readings can be re-opened, which would change the published verdict and require correcting the README, the essays and this log in one act. The release is unaffected either way.

**Revisit trigger:**
A future experiment cannot fill a §2 row → the row is recorded empty with its reason, and if the gap recurs the template moves to v1.1 with the change recorded. A disputed public claim resolves to a rule not found in E3 → §4 gains the rule, or the document is shown incomplete, with the outcome recorded here. Protocol §14 revised → E3 is revised in the same act or dies (§9). F25 re-opened → the verdict on both candidates is re-derived and every artefact that states it is corrected together, because a verdict that changes on a reading must change everywhere it is quoted.

**Expected value assessment:**
- Probability a reader can now determine whether a given claim rule binds: **high** — the marking is mechanical and the board cross-check is a test, not a habit.
- Probability the freeze changes any number: **zero**. Documentation only; the archive, digest and published table are untouched and the notice is code-generated.
- Probability F25 is challenged: **moderate** — it is the natural place to attack the verdict — and the answer is now a named, disclosed reading rather than a re-derivation. That is the whole benefit of settling it.
- Residual risk: E7 v1.1 is a revision to a Frozen document, and revisions to frozen documents are how contracts drift. Mitigated by the change being a *reduction* to a pointer whose two rules remain in E3, and by the version bump being visible on the board.

**Pre-mortem:**
Three ways this fails later. **(a)** A reader cites E7 §5 for a rule that has moved and finds a pointer — the intended outcome, since the pointer names the destination. **(b)** The §8 record drifts out of agreement with the rules it describes — detectable because the record names the rule and the section, so changing one without the other is a visible inconsistency in a document read top to bottom. **(c)** E3 acquires authority over something the protocol owns — detectable because every restatement is marked `[§14]` and §1 states the precedence, so the check is a diff against §14 rather than a reading.

---

## Appendix A — Experiment Registry (Ledger)

This appendix is the append-only ledger of pre-registered experiments. Registry *rules* (what counts as an experiment, ID format, denominator rules, invalidation rules) live in `evaluation_protocol.md` §12 and, until Phase C completes, in `experiment_registry_and_preregistration.md`. This appendix holds the *entries*.

**Status of this appendix:** Scaffolded in Phase A (per DEC-20261015-017). Populated in Phase C after the freeze. The Phase 1 exploratory run is recorded below as a pointer only; its substantive record is DEC-20261015-012.

**Rule:** No entry is edited. Registrations, results, conclusions, and decisions are appended in order. Invalidations are marked in place with a reference to the invalidation rule in `evaluation_protocol.md` §12.

### Index

| EXP-ID | Date | Family | Status | Title |
|--------|------|--------|--------|-------|
| EXP-H1-20261015-001 | 2026-10-15 | X (exploratory) | ARCHIVED | Phase 1 smoke test (retroactively logged per DEC-20261015-012) |
| EXP-X-20261017-001 | 2026-10-17 | X (exploratory) | REGISTERED | Test B — cap-sensitivity sweep (cap-artifact diagnostic) |
| EXP-X-20261017-002 | 2026-10-17 | X (exploratory) | REGISTERED | Test C — window sensitivity, windows {36, 60} (window-artifact diagnostic) |
| EXP-H2-20261017-001 | 2026-10-17 | H2 / H3 (confirmatory) | RE-DESIGNATED — EXECUTED (NON-CONFIRMATORY) | Test D — evaluation of the robust methods (H2.4); N = 1 at registration; blindness lost to F26, so it does not count (DEC-20261017-034) |
| EXP-X-20261017-003 | 2026-10-17 | X (exploratory) | EXECUTED (non-confirmatory) | First end-to-end run of the reporting layer — report-generator validation on the frozen configuration (see F26) |

### EXP-H1-20261015-001

**Status:** ARCHIVED
**Registered:** 2026-10-15 (retroactively, as a pointer; the substantive record predates this scaffold)
**Family:** X (exploratory — non-confirmatory)
**Related decision log entry:** DEC-20261015-012

**Note:** This entry exists so the ledger is non-empty and so future readers can trace the Phase 1 exploratory run through the correct index. It does not carry a full pre-registration template because it was not pre-registered. It is not a finding. It does not count toward any multiple-testing denominator.

**No further entries exist as of 2026-10-15.** The first confirmatory registration will be appended after `evaluation_protocol.md` reaches `Frozen`.

**Superseded in part (2026-10-17, DEC-20261017-026 / -027).** The protocol is `Frozen` and the first registrations are appended below: `EXP-X-20261017-001` (Test B, exploratory), `EXP-X-20261017-002` (Test C, exploratory, windows {36, 60}), and `EXP-H2-20261017-001` (Test D, confirmatory, N = 1). Test C's window sweep was reduced from {36, 60, 120} to {36, 60} by finding F14 (DEC-20261017-027): the 120-month arm has no feasible start at the frozen anchor, since the universe did not exist before 2007.

### EXP-X-20261017-001

**Status:** REGISTERED (not executed)
**Registered date:** 2026-10-17
**Family:** X (exploratory — **non-counting**; §12.6.2)
**Related hypotheses:** H3-family diagnostic (cap artifact). Companion to `EXP-H2-20261017-001`.
**Related decision triggers:** §4.3 `w_max`; resolves audit finding F1. Not a §8.6 kill trigger.
**Related decision log entry:** DEC-20261017-020 (spec), DEC-20261017-026 (this registration)

**1. Hypothesis.** The Phase 1 underperformance of the shrinkage and turnover-penalized methods, relative to unpenalized sample MVO, is an artifact of the box cap having been applied only to the optimizers.
*Direction:* if the artifact is real, `ΔB` (penalized/shrinkage minus `B3`) reverses sign as the cap loosens and the cap is applied uniformly.
*Effect size of interest:* a sign change in `ΔB` between the tightest and loosest arm.
*Prior probability:* moderate (~40%). Phase 1 applied the cap unevenly, so the artifact is plausible, but Phase 1 also changed the window, `γ`, and cost treatment at once, so the cap is not the only candidate.
*Falsifiable:* yes — a pre-committed decision rule on `ΔB` and `Δbase` (field 5).

**2. Methods compared.** Baselines `B1` (1/N), `B2` (risk parity), `B3` (sample MVO), `B4` (min variance), `B5` (turnover-penalized MVO, λ = κ). No robust methods (Test D owns those). Cap applied **uniformly to every method including `B1` and `B2`** (fixes audit finding F1).

**3. Parameters.**
| Parameter | Value |
|---|---|
| Universe | the snapshot's `universe_pit.csv` — 18 confirmed candidates (DEC-20261017-024); eligible 18 → 17 after 2021-11 (F12) |
| Snapshot ID (SHA-256) | `yahoo-usetf-2007-01-01_2026-09-30-2026-10-17-2ad06139` (`2ad0613913df9065b62ba2291abc391402c1eb13d36937ba8c2bbc09d637d707`) |
| Data | point-in-time adjusted, raw + corporate actions (protocol §5.4.1) |
| Estimation window | 60 months, rolling, re-estimated monthly (§5.2) |
| Test window / step | 12 months / 12 months, non-overlapping (§5.2) |
| Out-of-sample period | 2012-06 … 2026-05 (168 months, 14 folds) |
| Rebalance | monthly, last trading day (§5.5.4) |
| **Swept parameter** | `w_max ∈ {0.20, 0.30, 0.40, 1.00}` (1.00 = uncapped), applied uniformly in every arm |
| Constraints | Σw = 1; 0 ≤ w_i ≤ `w_max` |
| Cost levels | 0 / 5 / 10 / 20 / 50 bps; headline 10 bps (§5.5.3) |
| Turnover penalty | λ = κ = 0.001 monthly (uniform with `B5`) |
| γ | 10 (`B3`, `B5`) |
| Random seeds | `SEED = 20261017` (spec §11 O6/O7); no other stochastic component |
| Solver | `cvxpy` / `CLARABEL` convex QP, no fallback (F1, F3) |

**4. Evaluation protocol.** Protocol `evaluation_protocol.md` **v2.4 (Frozen)**; method spec **v1.1 (Frozen)**.
*Primary metric:* net Sharpe at 10 bps. *Secondary:* `ΔB`, `Δbase`, turnover, max drawdown, CVaR 95%, cost drag.
*Statistical test:* **descriptive only.** DSR and PSR are reported for information but carry no decision weight: family X cannot support success claims (§12.6.2, §12.10).
*Confidence level:* 90% block-bootstrap intervals.
*Multiple-testing family size at registration:* **N/A** — family X does not count (§12.6.2). 4 arms, **all reported**.

**5. Decision rule.**
- `ΔB < 0` at **every** cap **and** `Δbase` widens monotonically as the cap loosens → the underperformance is **not** a cap artifact; escalate to Test C.
- `ΔB < 0` **only** at loose/no cap and reverses at tight caps → **cap artifact**; the framing's remedy hypothesis is not falsified by Phase 1.
- `ΔB` changes sign with cap non-monotonically → **cap-fragile**; report as unresolved and do not proceed to a confirmatory claim without a new hypothesis.
- **In all three cases:** if an arm reveals a configuration where a robust method meets §6.4, that configuration is **not** adopted. It becomes the hypothesis for a **new, separately pre-registered** experiment, with the Test B arms (4) counted as prior trials in that experiment's denominator (Tests B/C/D spec §5, rules 1–3).

**6. Cost and time estimate.** Compute: 4 arms × 14 folds × 5 methods; cap-constrained convex QPs are small (≤ 18 assets) and solve in well under a second each. Estimated wall-clock: **under 10 minutes** single-threaded on the development machine, plus one snapshot read. Data volume: the snapshot's parquet files (~2 MB).

**7. What would invalidate this experiment.** Any §12.11 condition; additionally: an arm whose cap is not applied uniformly; a differing OOS period, universe, cost model, or constraint handling between arms (Tests B/C/D spec §1 — "any deviation invalidates the comparison"); use of the arms to select Test D's configuration (firewall §5).

**8. Pre-registration signature.** Author: Ken Ira Lacson Talingting. Date: 2026-10-17. Git commit at registration: `1b71e13` (the code state this registration was written against). Registry version at registration: `decision_log.md` v1.3, Appendix A scaffold.

**Results:** pending execution.
**Conclusion:** pending.
**Decision:** pending.

---

### EXP-X-20261017-002

**Status:** REGISTERED (not executed)
**Registered date:** 2026-10-17
**Family:** X (exploratory — **non-counting**; §12.6.2)
**Related hypotheses:** H3-family diagnostic (window artifact). Companion to `EXP-H2-20261017-001`.
**Related decision triggers:** §5.2 estimation window. Not a §8.6 kill trigger.
**Related decision log entries:** DEC-20261017-020 (spec), DEC-20261017-026 (F14 raised), DEC-20261017-027 (F14 resolved; this registration)

**1. Hypothesis.** The Phase 1 underperformance of the shrinkage and turnover-penalized methods is specific to the **60-month** estimation window.
*Direction:* the underperformance is absent (or reverses) at a shorter window.
*Effect size of interest:* a sign change in `ΔB` (penalized/shrinkage minus `B3`) between the 36- and 60-month arms.
*Prior probability:* moderate (~40%). Phase 1's instability is consistent with a short, noisy estimation window, but Phase 1 also changed the cap and the cost treatment at the same time.
*Falsifiable:* yes — pre-committed decision rule on `ΔB` across the two arms (field 5).

**2. Methods compared.** Baselines `B1` (1/N), `B2` (risk parity), `B3` (sample MVO), `B4` (min variance), `B5` (turnover-penalized MVO, λ = κ). No robust methods (Test D owns those).

**3. Parameters.**
| Parameter | Value |
|---|---|
| Universe | the snapshot's `universe_pit.csv` — 18 confirmed candidates; eligible 18 → 17 after 2021-11 (F12) |
| Snapshot ID (SHA-256) | `yahoo-usetf-2007-01-01_2026-09-30-2026-10-17-2ad06139` (`2ad0613913df9065b62ba2291abc391402c1eb13d36937ba8c2bbc09d637d707`) |
| Data | point-in-time adjusted, raw + corporate actions (§5.4.1) |
| **Swept parameter** | rolling estimation window `∈ {36, 60}` months |
| **Period rule (F14)** | **both arms share the identical out-of-sample period 2012-06 … 2026-05** (168 months, 14 folds), so the arms are directly comparable and consistent with Tests B and D. The 120-month arm is **dropped**: the universe did not exist before 2007, so a 120-month window has no feasible start at the frozen anchor (DEC-20261017-027). |
| Test window / step | 12 months / 12 months, non-overlapping (§5.2) |
| Rebalance | monthly, last trading day (§5.5.4) |
| Constraints | Σw = 1; 0 ≤ w_i ≤ **0.30** — the frozen value, held fixed across arms so the window is the only varying factor (§4.3) |
| Cost levels | 0 / 5 / 10 / 20 / 50 bps; headline 10 bps (§5.5.3) |
| Turnover penalty | λ = κ = 0.001 monthly |
| γ | 10 (`B3`, `B5`) |
| Random seeds | `SEED = 20261017` (spec O6/O7); no other stochastic component |
| Solver | `cvxpy` / `CLARABEL` convex QP, no fallback |

**4. Evaluation protocol.** Protocol **v2.4 (Frozen)**; method spec **v1.1 (Frozen)**.
*Primary metric:* net Sharpe at 10 bps, per arm. *Secondary:* `ΔB` per arm; net-Sharpe ranking per arm; **condition number of the sample covariance** at each window (the dispersion diagnostic, which is the same question the window sweep asks — see the B/C/D spec §9).
*Statistical test:* **descriptive only.** Family X cannot support success claims (§12.6.2, §12.10).
*Confidence level:* 90% block-bootstrap intervals.
*Multiple-testing family size at registration:* **N/A** — family X does not count. 2 arms, **both reported**.

**5. Decision rule (restated for two arms; DEC-20261017-027).** The spec's original rule was written for three windows and is amended here to match the two feasible arms:
- Underperformance present at **both** 36 and 60 months → **not** a window artifact; the frozen window stands.
- Underperformance present at **60 months only** → **window artifact**; the §5.2 60-month recommendation is called into question and the window becomes a swept dimension for a re-frozen protocol.
- Underperformance present at **36 months only** → report as **inverted**: the effect is not attributable to the longer window, and the Phase 1 observation is not reproduced.
- **In every case:** if an arm reveals a configuration where a robust method meets §6.4, that configuration is **not** adopted; it becomes the hypothesis for a new, separately pre-registered experiment, with the Test C arms (2) counted as prior trials in that experiment's denominator (B/C/D spec §5, rules 1–3).

**6. Cost and time estimate.** 2 arms × 14 folds × 5 methods. Smaller than Test B. Estimated wall-clock: **under 10 minutes** single-threaded, plus one snapshot read.

**7. What would invalidate this experiment.** Any §12.11 condition; additionally: the two arms using different out-of-sample periods, universes, cost models, or caps (B/C/D spec §1); the cap varying with the window; use of the arms to select Test D's configuration (firewall §5).

**8. Pre-registration signature.** Author: Ken Ira Lacson Talingting. Date: 2026-10-17. Git commit at registration: `ca4364c`. Registry version at registration: `decision_log.md` v1.3, Appendix A with the §12.4 template.

**Results:** pending execution.
**Conclusion:** pending.
**Decision:** pending.

---

### EXP-H2-20261017-001

**Status:** **RE-DESIGNATED — EXECUTED (NON-CONFIRMATORY)**, 2026-10-17 (finding F26; DEC-20261017-034). The registration below is unchanged — hypothesis, parameters, metrics, decision rule and denominator are exactly as pre-registered.
**Registered date:** 2026-10-17
**Family:** H2 / H3 (**confirmatory slot — does not count**; the registration was confirmatory, the execution was not blind, so it contributes nothing to any denominator, §12.10 by analogy)
**Related hypotheses:** H2.1, H2.2, H2.3, **H2.4**; H3.1, H3.2, H3.3.
**Related decision triggers:** **§8.6 K1** (if no method is successful, the primary objective is falsified → stop-and-report).
**Related decision log entries:** DEC-20261017-023 (spec freeze), DEC-20261017-025 (snapshot), DEC-20261017-026 (this registration)

**1. Hypothesis (H2.4).** Under the frozen protocol, at least one robust method beats the best baseline on net Sharpe after costs and multiple-testing adjustment, per §6.4.
*Direction:* positive — at least one of `M1`, `M2` exceeds the best of `B1`–`B5`.
*Effect size of interest:* net Sharpe improvement over the best baseline **≥ 0.20** (§6.2).
*Prior probability:* low-to-moderate (~30%). Phase 1 (exploratory, non-confirmatory — DEC-20261015-012) found shrinkage and penalized MVO *underperforming* on net Sharpe; the frozen protocol is fairer than Phase 1's comparison (uniform cap, identical data), which cuts both ways.
*Falsifiable:* yes — §6.4's four conditions are all fixed in advance, and failure triggers K1.

**2. Methods compared.** Baselines `B1`–`B5` (§4.2). Robust candidates `M1` (Ledoit-Wolf shrinkage covariance + sample-mean MVO; differs from `B3` **only** in Σ) and `M2` (sample covariance + no-views Bayesian/Black-Litterman posterior MVO, ½(Π + μ̂); differs from `B3` **only** in μ). Both are MVP components per scope §3.4/§3.5 (finding F9, DEC-20261017-022).

**3. Parameters.**
| Parameter | Value |
|---|---|
| Universe | the snapshot's `universe_pit.csv` — 18 confirmed candidates; eligible 18 → 17 after 2021-11 (F12) |
| Snapshot ID (SHA-256) | `yahoo-usetf-2007-01-01_2026-09-30-2026-10-17-2ad06139` (`2ad0613913df9065b62ba2291abc391402c1eb13d36937ba8c2bbc09d637d707`) |
| Data | point-in-time adjusted, raw + corporate actions (§5.4.1) |
| Estimation window | 60 months, rolling, re-estimated monthly (§5.2) — **the frozen value**, not whichever arm won Test C |
| Test window / step | 12 months / 12 months (168 OOS months, 14 folds) |
| Rebalance | monthly, last trading day (§5.5.4) |
| Constraints | Σw = 1; 0 ≤ w_i ≤ **0.30**, uniform across **all** methods (§4.3, fixes F1) |
| Risk aversion | γ = 10 (`B3`, `B5`, `M1`, `M2`) |
| Turnover penalty | λ = κ = 0.001 monthly (`B5`) |
| Cost levels | 0 / 5 / 10 / 20 / 50 bps; headline 10 bps (§5.5.3) |
| Risk-free rate | `DGS1MO`, geometric monthly conversion, prior-month alignment (confirmed F10/F11, DEC-20261017-026); same `R_f` for gross and net |
| Shrinkage target (`M1`) | `sklearn` Ledoit-Wolf, identity target (spec O2) |
| Solver | `cvxpy` / `CLARABEL`; acceptance = max constraint violation ≤ 1e-7 **and** duality gap ≤ 1e-7; **no fallback** (spec O4, F1/F3) |
| Random seeds | `SEED = 20261017` (spec O7); block bootstrap uses the same seed |
| H1.1 treatment | `H1.1` tests the **uncapped** optimizer (decoupled from the capped `B3`); reported as a separate treatment |

**4. Evaluation protocol.** Protocol `evaluation_protocol.md` **v2.4 (Frozen)**; method spec **v1.1 (Frozen)**.
*Primary metric:* net Sharpe at the baseline cost level (10 bps).
*Secondary metrics:* gross Sharpe; turnover; maximum drawdown; CVaR 95%; cost drag; per-fold net Sharpe; DSR and PSR; calibration (return + volatility, one-month horizon, 80–100% coverage).
*Statistical test:* §6.1 — **DSR p-value < 0.05** with `SR* = SR_0` (expected maximum under `N` trials) **and PSR > 0.95** vs `SR* = SR_best baseline`; both required. §12.8 — Benjamini-Hochberg FDR at **q = 0.10** within family H2/H3.
*Confidence level:* 90% block-bootstrap CIs (§13).
*Multiple-testing family size at registration:* **N = 1** — zero prior confirmatory trials in family H2/H3 + 1 (§12.6; the denominator is the count of confirmatory EXPERIMENT entries per DEC-20261015-014). **See finding F13** (DEC-20261017-026): `N = 1` follows the frozen rules literally; if `M1` and `M2` are to be counted as separate trials it must be amended **before execution** (§12.9).

**5. Decision rule (§6.4).** A method is **successful** only if **all four** hold: statistical significance (§6.1), economic materiality (§6.2: net Sharpe improvement ≥ 0.20 *and* turnover ≤ 2× the best baseline *and* max drawdown no worse than the best baseline by > 5 pp), robustness (§6.3: advantage at ≥ 3 cost levels *and* in ≥ 60% of folds *and* no fold contributing > 40% of the advantage), and no PIT/cost violation.
- **Success condition:** ≥ 1 method satisfies all four → H2.4 confirmed; proceed to Phase 3.
- **Failure condition:** no method satisfies all four → **K1 fires: stop-and-report.** The primary objective is falsified.
- **Ambiguous condition:** a method satisfies some but not all → report as `INCONCLUSIVE`; it is not a success.
- **Action in every case:** no method may be added and no threshold relaxed to rescue the result (§8.6 K1, §8.1 Hard Rule 2).

**6. Cost and time estimate.** Compute: 14 folds × 7 methods × 5 cost levels; each fold solves a small (≤ 18-asset) convex QP per method. Estimated wall-clock: **under 30 minutes** single-threaded, plus one snapshot read.

**7. What would invalidate this experiment.** Any §12.11 condition; additionally: any §5.4 field not traceable to the snapshot; a failing §5.4.8 leakage test; a differing universe, cost model, or constraint handling between methods (§4.6); the configuration being taken from a Test B or Test C arm (firewall, Tests B/C/D spec §5); a `B3` that is capped while the comparable `M1`/`M2` is not (F1 regression).

**8. Pre-registration signature.** Author: Ken Ira Lacson Talingting. Date: 2026-10-17. Git commit at registration: `1b71e13`. Registry version at registration: `decision_log.md` v1.3, Appendix A scaffold.

**Results:** Executed 2026-10-17 as **`EXP-X-20261017-003` — one execution, one record, two labels** (DEC-20261017-034). The run is logged in full under that entry and is deliberately not duplicated here. Snapshot `yahoo-usetf-2007-01-01_2026-09-30-2026-10-17-2ad06139`; the §3 parameters above, unchanged; 168 rebalances, 14 folds, 1,176 solves, §5.6 certificate clean.

**Conclusion:** **Not a confirmation, and no H2.4 statement is made.** Under the frozen §6.4 rule the verdict is **FAILURE** for both candidates. `M2` net Sharpe **0.8538** against the best baseline `B3` **0.7896** is a gap of **+0.064** against the registered **≥ 0.20** bar; `M1` is **−0.004**. PSR **0.587** and **0.495** against the registered **0.95** bar. The §6.3 concentration clause is independently binding — `M2`'s largest fold contributes **51.3%** of its advantage. **K1 does not fire**: K1 belongs to a confirmatory test, and this execution was not blind. The primary objective is therefore **untested**, not falsified.

Two things make the relabelling honest rather than a way out, and both are recorded here rather than left for a reader to notice. **(1)** It changes *which entry carries the verdict*, not the verdict: the §6.4 outcome is `FAILURE` either way, so nothing is rescued by relabelling it. **(2)** The hypothesis, parameters, metrics, thresholds, decision rule and denominator were frozen before the number was seen and the rule is mechanical, so the observation cannot have moved the verdict even though it destroyed the blindness.

**Decision:** Re-designated **EXECUTED (NON-CONFIRMATORY)** per DEC-20261017-034. **No replacement confirmatory test is registered** — see that entry for what a valid one would require. Nothing in this entry may be cited for or against H2.4.

---

### EXP-X-20261017-003

**Status:** EXECUTED (2026-10-17) — **exploratory, non-confirmatory, non-counting** (§12.10)
**Family:** X (exploratory — does not count toward any multiple-testing denominator, §12.6.2)
**Related hypotheses:** none. No hypothesis was tested and none may be cited for or against.
**Related decision log entry:** DEC-20261017-031

**Purpose.** Validate the reporting layer end to end (spec §8's single command) on the frozen configuration: `scripts/run_experiment.py` over all seven methods of spec §1, producing the report, the decision table, the fold tables, and the calibration table. This is a **software validation artifact**, not a test of H2.4.

**What ran.** Snapshot `yahoo-usetf-2007-01-01_2026-09-30-2026-10-17-2ad06139`; the frozen parameters of `EXP-H2-20261017-001` §3, with no arm selected by any Test B or Test C sweep (the firewall of the B/C/D spec §5 is not engaged: no sweep has been run). 168 rebalances, 14 folds, 1,176 solves, §5.6 certificate clean, protocol §13.1 structure asserted by the runner.

**Numbers produced (recorded so they cannot be presented as new).**

| Method | Net Sharpe (10 bps) | 90% CI | Turnover (ann.) | Max DD |
|---|---|---|---|---|
| `B1` | 0.5482 | [0.1531, 1.0018] | 0.391 | -0.181 |
| `B2` | 0.4519 | [0.0167, 0.9739] | 0.340 | -0.134 |
| `B3` | **0.7896** | [0.3311, 1.3176] | 2.120 | -0.184 |
| `B4` | 0.1820 | [-0.2532, 0.7506] | 0.430 | -0.109 |
| `B5` | 0.7843 | [0.3159, 1.3160] | 0.729 | -0.198 |
| `M1` | 0.7860 | [0.3269, 1.2980] | 1.920 | -0.180 |
| `M2` | 0.8538 | [0.4255, 1.3687] | 2.141 | -0.176 |

`B3` is the best baseline. `M1` and `M2` each return **FAILURE** under §6.4: the net-Sharpe improvement over `B3` is `-0.004` and `+0.064` (bar 0.20), and the PSR against `B3` is 0.495 and 0.587 (bar 0.95). The DSR p-values, 0.0032 and 0.0017, pass -- against a *zero* benchmark. Fold wins are 6 of 14 (`M1`) and 10 of 14 (`M2`); the §6.3 concentration clause fails both (50.5% and 51.3% of the total advantage in one fold -- see finding F25). Calibration coverage of next-month return intervals is 81.5%-87.0%, inside §3's target.

**Conclusion.** The reporting layer reproduces its own numbers from one command and the frozen seed, and the decision rule evaluates. **No hypothesis statement follows from this entry.** It does not fire K1, which belongs to `EXP-H2-20261017-001`.

**Disclosure (finding F26, DEC-20261017-031).** This run executed the configuration `EXP-H2-20261017-001` is registered on, so Test D's answer has been observed before Test D was executed. Everything Test D relies on -- hypothesis, parameters, metrics, decision rule, denominator -- was frozen *before* this look (protocol §12.1), and the rule is mechanical, so the observation cannot alter the rule. It does mean Test D's execution would be a **reproduction and formal record rather than a blind test**, and that **nothing may be amended on the strength of this look** (§12.9). Owner decision pending.

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
| E7 | `open_source_and_license_policy.md` | Closed — v1.0 Draft | Written before public release as required; two `[PROPOSED]` items await owner confirmation (data-redistribution disposition — finding F30 — and the contribution model). DEC-20261017-033 |
| F5 | Log the experiment in the registry before running it | Open | **Closed** — DEC-20261015-012 + Appendix A pointer `EXP-H1-20261015-001` |

**Note on F1–F4 of the source TODO (F1–F4 in "Phase F").** Those items (implement data pipeline, baselines, walk-forward harness, run H1.1/H1.2) were marked done in exploratory form. Their completion is recorded in DEC-20261015-012; DEC-20261017-019 qualifies it (the harness was completed but does not implement the protocol's baseline set or constraint rules).

**Open items from this appendix that are on the critical path:** C1 → C2 → C3 (method spec), and D1 → D2 → D3 (the freeze). These are the same items named as the binding constraint in DEC-20261015-017.

**Update 2026-10-17 (DEC-20261017-021).** The freeze closed: **D1** (the worksheet was produced), **D2** (every value was confirmed or replaced), **D3** (the protocol, data contract, and cost model are `Frozen` at v2.3), **C1** (the open method choices were decided — 60-month window, `w_max` 0.30 uniform, γ = 10, λ = κ), **A7** (the last dead cross-reference, F5d, was fixed in `docs/README.md`), **B3** (scope activated at v1.3), and **B4** (the audit and freeze reconciled the file set). Still open: **C2** and **C3** (write and freeze the method spec), **E2** (`reproducibility_and_environment.md`), **E3** (`results_reporting_and_claims_policy.md`), **E5** (`architecture_decision_records/`), **E7** (`open_source_and_license_policy.md`). The method-spec half (C2 → C3) is now the binding constraint on Gate 1.

**Update 2026-10-17 (DEC-20261017-022).** **C2** closed — `model_and_method_spec.md` v1.0 `Draft` written; it absorbs finding F7. Finding **F9** (MVP robust-method classification: protocol §4.2 vs scope §3.4/§3.5) resolved in scope's favour; `evaluation_protocol.md` §4.2 corrected at v2.4 (a §16 pre-result change) and `scope_and_non_goals.md` clarified at v1.4. **C3 remains open** and is now gated on the spec's `[OPEN]` items O1, O2, O4–O7. The remaining appendix items open on the critical path are C3 and, for Gate 1, the point-in-time candidate list (protocol §5.4.7).

**Update 2026-10-17 (DEC-20261017-023).** **C3** closed — `model_and_method_spec.md` v1.0 `Draft` → **v1.1 `Frozen`**; all six `[OPEN]` items resolved (spec §11). The **documentation half of Gate 1 is complete**. Gate 1 entry now requires only the point-in-time candidate universe list (protocol §5.4.7) and the §5.4.8 leakage suite. The remaining appendix items still open are **E2** (`reproducibility_and_environment.md`), **E3** (`results_reporting_and_claims_policy.md`), **E5** (`architecture_decision_records/`), and **E7** (`open_source_and_license_policy.md`) — none on the Gate 1 critical path.

**Update 2026-10-17 (DEC-20261017-024).** The **point-in-time candidate universe list** (protocol §5.4.7) is reconstructed and confirmed — `notes/pit_universe_2026-10-17.md` v1.0, 18 instruments, anchored at the backtest start 2012-06. One of the two remaining Gate 1 items is closed; the **§5.4.8 leakage suite** is now the only Gate 1 blocker. No Tier-0 value changed (the universe count is delegated by protocol §5.4.2 and scope §3.1).

**Update 2026-10-17 (DEC-20261017-025).** The **§5.4.8 leakage suite passes** (14 passed, 1 skipped as vacuous in-sample) against the first immutable snapshot, `yahoo-usetf-2007-01-01_2026-09-30-2026-10-17-2ad06139`. **Both Gate 1 data blockers are now closed**; the Phase 1 experiment is unblocked. Findings **F10** (rf annual-to-monthly conversion) and **F11** (rf observation month) are surfaced for owner confirmation; **F12** records that the §5.4.2 liquidity floor is binding on `RWX`, so the eligible set declines from 18 to 17 after 2021-11. This is the first `src/` / `scripts/` change since the freeze. The remaining appendix items still open are unchanged and off the critical path: **E2**, **E3**, **E5**, **E7**. The next critical-path work is registering Tests B/C/D in Appendix A (protocol §12.4 — now unblocked, since a snapshot ID exists) and rewriting `src/` to conform to protocol v2.4 + spec v1.1.

**Update 2026-10-17 (DEC-20261017-026).** **F10 and F11 confirmed as recorded** (`geometric`, `prior_month`) — no code change, so no new snapshot. The first registrations are written: `EXP-X-20261017-001` (Test B, family X, non-counting) and `EXP-H2-20261017-001` (Test D, family H2/H3, counting, **N = 1**). **Test C is not registered**: finding **F14** — the window sweep {36, 60, 120} has no common evaluation period (first feasible OOS 2010-06 / 2012-06 / 2017-06), so its arms are not comparable and the spec's "identical period" rule cannot be met without an owner decision. Finding **F13** — whether a single registration that reports the best of several candidate methods (`M1`, `M2`) should carry `N = 1` or `N = 2` in the DSR — is recorded for the owner; it must be amended before execution if changed (§12.9).

**Update 2026-10-17 (DEC-20261017-027).** Both findings are closed. **F13:** `N = 1` is **owner-confirmed**, so `EXP-H2-20261017-001` stands exactly as registered and the §12.11 family-size risk is closed. **F14:** Test C runs windows **{36, 60}** over the frozen 2012-06…2026-05 period; the **120-month arm is dropped** because the universe did not exist before 2007, so a 120-month window has no feasible start at the frozen anchor. The spec's three-arm decision rule is restated for two arms, and the reduced strength of a two-point sweep is recorded as a limitation. **Test C registered** as `EXP-X-20261017-002` (family X, 2 arms, both reported). All three Tests B/C/D are now pre-registered; none has been executed. No Tier-0 value changed.

**Update 2026-10-17 (DEC-20261017-028).** Design diagnostics, run before any experiment and recorded as **not an experiment and not a registry entry** (protocol §12.2): `notes/power_and_effective_bets_2026-10-17.md` v1.0 (v1.1 by the entry) plus `scripts/diagnostics_power.py`. Measured: the 18 candidates carry only **3–5 independent directions** (`N_part` 3.14 / `N_ent` 5.03; per-fold 2.45–3.91 / 4.13–5.71) rather than 18; **12 of 18** sample eigenvalues fall below the Marchenko–Pastur lower edge (0.452) for an independent 18 × 168 panel, the smallest by **85×**, so the H1 premise is **supported by the data rather than assumed**; and the §6.3 fold gate passes **21.2%** of the time under the null (≥ 9 of 14). **Finding F15 raised and resolved (reading a)**: ρ(candidate, best baseline) is reported in a **design/detectability appendix**, not added to the registered metric set, so `EXP-H2-20261017-001` is **not amended** and keeps **N = 1**. The earlier claim that the project is "underpowered for a 0.2 Sharpe claim" is **retracted** — the paired design detects the §6.2 threshold at ≥ 80% power for ρ ≥ 0.98. No frozen document amended; the remaining appendix items still open are unchanged (**E2**, **E3**, **E5**, **E7**).

**Update 2026-10-17 (DEC-20261017-029).** The Phase 2 rewrite's **engine core** lands (commit `e59a55e`): `src/robustfolio/config.py` (new, the single source of truth for frozen values), `estimators.py` and `optimize.py` rewritten, `tests/test_conformance.py` (23 cases), `scripts/certify_engine.py`. `optimize.py` is `cvxpy` + `CLARABEL` with **no fallback path** (spec §5.7) and a **primal-only KKT certificate** in place of the duality gap CLARABEL does not expose. Evidence: **168 rebalances x 6 solver-backed methods = 1,008 solves, zero failures**, worst residual `2.97e-11`, `cond(Sigma_hat)` `1.30e4`–`6.09e5`. Risk parity's cap binds on **154 of 168** rebalances. Three findings resolved: **F16** (sklearn Ledoit-Wolf `ddof=0` vs spec §4.2 `ddof=1` — left as specified, quantified, not rescaled); **F17** (spec §5.6's "solver defaults" cannot deliver its own 1e-7 acceptance, so `SOLVER_TOL = 1e-14` is set explicitly and the unexposed duality gap is replaced); **F18** (initial `w^- = 0`, the period starts flat). One defect in the new code is recorded: the certificate's multipliers were first added rather than subtracted — correct for a minimisation and wrong for a maximisation — which would have accepted whatever the solver returned, and was caught by the analytic test. The one place the implementation now contradicts a frozen sentence is spec §5.6's "Tolerance: solver defaults", superseded in practice by this entry and **deferred to the next versioned spec revision** rather than amended unilaterally. The walk-forward harness (`backtest.py`) is **not yet rewritten**. No Tier-0 value changed; the remaining appendix items still open are unchanged (**E2**, **E3**, **E5**, **E7**).

**Update 2026-10-17 (DEC-20261017-030).** The **walk-forward harness** (spec §6) lands (`src/robustfolio/backtest.py`, `tests/test_backtest.py`) and `scripts/certify_engine.py` is rewritten to certify the harness rather than a re-implementation of it. The rewritten engine now certifies the entire frozen run: **7 methods x 168 rebalances = 1176 solves, zero rejections**, worst residual `1.49e-11`; B5's worst residual fell from `5.1e-7` to `2.1e-12`. Five findings are recorded, all implementation-level: **F19** (estimator results depended on the frame's memory layout, fixed by a contiguity guarantee -- no spec deviation); **F20** (the certificate's `nu` fallback wrongly rejected seven optimal B5 rebalances, replaced by an exact interval formulation); **F21** (a redundant `nonneg=True` bound on the L1 auxiliary variable was making CLARABEL return a point `2.8e-11` below the optimum at one rebalance, removed); **F22** (risk parity's uncapped branch never ran the §5.6 acceptance checks -- 14 of 168 B2 rebalances were silently uncertified); and **F23** (the certification script had been certifying a *different* B5 problem, which is why F20 and F21 were invisible to it). `SOLVER_TOL = 1e-14` is re-confirmed on the whole run and its evidence table in `config.py` is updated from single-fold to whole-run figures. No frozen document is amended; the remaining appendix items still open are unchanged (**E2**, **E3**, **E5**, **E7**).

**Update 2026-10-17 (DEC-20261017-031).** The **reporting layer** (spec §7-§8) lands: `metrics.py` rewritten to the §7.1-§7.7 registry (the Phase 1 `annualized_turnover`, whose `weights.diff()` basis §7.2 explicitly deletes, is **removed**, and `BacktestResult.annualized_turnover` now delegates to the single canonical formula), a new `stats.py` (PSR, DSR with the frozen `N = 1` convention, the stationary block bootstrap, the §7.8 calibration primitives), a new `report.py` (the §14 disclosure table, the sixteen-comparison §6.1-§6.4 decision table with every comparison as its own pass/fail column, the per-fold table, and the calibration table), and `scripts/run_experiment.py` -- **one command** that writes `manifest.json`, `outcomes.csv`, `decisions.csv`, `calibration.csv`, `folds_<M>.csv` and `report.md`, re-asserting the §5.6 certificate and the §13.1 structure on what it reports. Three findings are recorded, all **ambiguity or status records rather than numerical ones**, and all three are **open owner decisions**: **F24** -- §7.8 does not define the object of its prediction interval or the realisation of a one-month volatility, so the **return half** is implemented under a stated reading (the method's own trailing 60 months of net portfolio returns, checked against the next month's net return) and the **volatility half is not implemented at all** rather than filled with a definition; **F25** -- §6.3's "advantage" is not pinned to a metric, and its two clauses need different properties, so fold wins are counted on net Sharpe (§2) and the concentration clause uses per-fold mean monthly net excess return, both reported -- and the reading **decides the verdict**, since the concentration clause is the binding one for `M2` (51.3%); **F26** -- validating the report generator required executing the frozen configuration, so `EXP-H2-20261017-001`'s answer was observed before Test D ran, which does not move the mechanical (frozen) decision rule but does make Test D a reproduction rather than a blind test. The first end-to-end run is logged as **`EXP-X-20261017-003`** (family X, executed, **non-counting**): `B3` is the best baseline at net Sharpe **0.7896** [0.3311, 1.3176], `M2` **0.8538** [0.4255, 1.3687], `M1` **0.7860**; both candidates return **FAILURE** under §6.4. Three implementation defects were caught by the new tests before any number was reported (a constant series producing a Sharpe of `2.3e16` under the natural `std == 0` guard; a **false docstring claim** that pandas' `.autocorr(1)` uses a whole-series mean; and a "break-even" column that misdescribed a non-monotone cost profile). No frozen document is amended; the remaining appendix items still open are unchanged (**E2**, **E3**, **E5**, **E7**).

**Update 2026-10-17 (DEC-20261017-032).** The **release packaging chain** lands: the frozen snapshot packs into a **deterministic 1.67 MB** `tar.gz` with an external `.sha256` (`scripts/pack_snapshot.py`), `scripts/verify_release.py` re-runs all seven methods against the snapshot *extracted from that archive* and asserts equality with the published table at tolerance **zero** (`EXACT`, max abs diff `0.000e+00`, 18 columns), the run directory publishes `net_excess_returns.csv`, `scripts/make_figures.py` draws the two headline figures from the run directory alone, and a `CI` workflow runs the hermetic suite on a fresh clone and — once the release asset exists — the full suite plus the one-command regeneration with certification on. Findings **F27** (the bundle hash is derived from **four** files while `manifest.json` lists **five**, so a verifier that recomputes it from the manifest's own map rejects every valid snapshot), **F28** (`pandas.read_csv`'s default parser — and `float_precision="high"` — is **lossy by one ULP**, so a verifier reading the published table with defaults reports a mismatch on a correct artefact), and **F29** (`docs/README.md`'s own version header had drifted behind its revision history, and the status board asserted a version for `decision_log.md` that the file did not declare) are recorded. Both F27 and F28 were **errors in the verifier, not in the artefact**, which is the entry's point. Two appendix items are now on the release critical path: **E7** (`open_source_and_license_policy.md`, "must be written before public release") is the **only** item standing between a finished artefact and a publishable one, and **E3** (`results_reporting_and_claims_policy.md`) governs what may be claimed when it is published. The other appendix items still open are unchanged (**E2**, **E5**). **Nothing has been pushed and no release has been cut**; F24–F26 remain open owner decisions, so no public material may use confirmatory language.

**Update 2026-10-17 (DEC-20261017-033).** **E7 closes**: `open_source_and_license_policy.md` is written as **v1.0 Draft** and registered as the eighth active document, removed from "Not yet written". It separates the licence by artefact class — **MIT for the code**, and explicitly **not** for the Yahoo-sourced snapshot archive — because the release chain the previous entry built uploads third-party data that MIT cannot cover. Finding **F30** is raised: publishing the archive is a **redistribution**, which the release plan had assumed it was not, so the disposition is a `[PROPOSED]` **owner** decision — publish the archive with a NOTICE (recommended), publish only the derived series, or publish the digest alone. The contribution model is `[PROPOSED]` (issues and PRs, no CLA), and an **attribution clause** records that findings describe this implementation, not `cvxpy` or `pandas` defects, since F19 and F28 document upstream behaviour working as specified. The **F26** recommendation is presented and deliberately **not** resolved: re-designate `EXP-H2-20261017-001` as **EXECUTED (NON-CONFIRMATORY)**, record its execution as the *same* run as `EXP-X-20261017-003` (one execution, one record, two labels), and register **no** replacement confirmatory test now, because a test designed after the answer is known is a test designed by the answer. **Owner decisions requested on F26 and on the two `[PROPOSED]` items.** Nothing pushed; no release cut.

**Update 2026-10-17 (DEC-20261017-034).** Both requests are answered. **F26:** `EXP-H2-20261017-001` is re-designated **EXECUTED (NON-CONFIRMATORY)**; its execution is the *same run* as `EXP-X-20261017-003` (one execution, one record, two labels), **no replacement confirmatory test is registered**, and because K1 belongs to a confirmatory test, K1 **does not fire** — H2.4 is **untested, not falsified**. Family H2/H3 now holds a spent, empty confirmatory slot. The entry states, in the ledger rather than in a reader's reconstruction, why this cannot be used to rescue the hypothesis: the §6.4 verdict is `FAILURE` for both candidates either way, so the relabelling changed *which entry carries the verdict*, not the verdict. **E7:** `open_source_and_license_policy.md` is **v1.0 Frozen** with both `[PROPOSED]` items confirmed — publish the snapshot archive with a NOTICE, and accept contributions as issues and PRs with no CLA. One deliberate deviation from DEC-033's own wording is recorded: the NOTICE lives in a **`NOTICE.txt` member inside the archive**, generated by `scripts/pack_snapshot.py`, rather than as a field in `manifest.json`, because the manifest is the data layer's hashed record and a licensing statement is not data. **Nothing pushed; no release cut; the release now has no open governance gate.**

**Update 2026-10-17 (DEC-20261017-035).** The NOTICE is **implemented**, not merely decided. `scripts/pack_snapshot.py` generates a deterministic `NOTICE.txt` member inside the archive from a version-controlled template in that script, and **refuses** a copy stored in the snapshot directory so the template stays the single source. `scripts/verify_release.py` asserts the notice is present and unchanged *before* it re-runs the seven methods, so an archive that lost its notice fails loudly instead of publishing third-party data with no statement attached. **The archive digest moved (`28e1d907…` → `7a3fc209…`) while the bundle hash and snapshot id did not**, which is the property that keeps `manifest.json` a record about data rather than a place to editorialise — and which is now named as **finding F31**: the archive digest identifies the *distribution*, the snapshot id identifies the *data*, and the README says so where a reader meets the digest. Re-verification with the notice check active: `EXACT`, max abs diff `0.000e+00`, 18 columns. Four new packaging tests.**

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
| 2026-10-17 | Added DEC-20261017-024 (point-in-time candidate universe confirmed — 18 ETFs anchored 2012-06; residual survivorship limitation accepted as documented). Updated Appendix B with the DEC-024 update note. | Ken Ira Lacson Talingting |
| 2026-10-17 | Added DEC-20261017-025 (immutable PIT snapshot built; §5.4.8 leakage suite passes — 14 passed, 1 vacuous skip; findings F10–F12 recorded; Gate 1 data blockers closed). Created `notes/snapshot_and_leakage_evidence_2026-10-17.md`; added the snapshot builder, the PIT reader and the leakage suite to `src/`/`scripts/`/`tests/`. Updated Appendix B with the DEC-025 update note. | Ken Ira Lacson Talingting |
| 2026-10-17 | Added DEC-20261017-026 (F10/F11 confirmed as recorded; first registry entries: `EXP-X-20261017-001` Test B and `EXP-H2-20261017-001` Test D, N = 1; findings F13 and F14 raised — Test C not registered). Introduced the §12.4 pre-registration template in Appendix A; updated Appendix A index and the scaffold note, and Appendix B with the DEC-026 update note. | Ken Ira Lacson Talingting |
| 2026-10-17 | Added DEC-20261017-027 (F13 resolved — N = 1 owner-confirmed, Test D stands as registered; F14 resolved — Test C windows {36, 60} at the frozen 2012-06…2026-05 period, 120-month arm dropped as infeasible; `EXP-X-20261017-002` Test C registered). Updated Appendix A index and scaffold note, Appendix B note, and the B/C/D spec §9 addendum. All three Tests B/C/D now pre-registered; none executed. | Ken Ira Lacson Talingting |
| 2026-10-17 | Added DEC-20261017-028 (design diagnostics ruled non-experimental under §12.2; effective-bets and power figures recorded; F15 raised and resolved — report ρ in a design appendix, no amendment, `N = 1` unchanged; the "underpowered" claim retracted). Created `notes/power_and_effective_bets_2026-10-17.md` and `scripts/diagnostics_power.py`. Updated the Appendix B note. No frozen document amended. | Ken Ira Lacson Talingting |
| 2026-10-17 | Added DEC-20261017-029 (engine core: estimators/optimizers rewritten with a primal-only KKT certificate; F16/F17/F18 raised and resolved; the certificate's own sign defect recorded). Updated the Appendix B note. `docs/README.md` to v1.11. | Ken Ira Lacson Talingting |
| 2026-10-17 | Added DEC-20261017-030 (walk-forward harness lands; findings F19-F23 recorded — layout-dependent estimator results, the certificate's `nu` fallback, a redundant L1 auxiliary bound, the risk-parity acceptance bypass, and the certification script's divergence from production; `SOLVER_TOL` re-confirmed on 1176 solves). Updated the evidence table in `config.py`, the Appendix B note, and `.gitignore`. | Ken Ira Lacson Talingting |
| 2026-10-17 | Added DEC-20261017-031 (reporting layer lands — `metrics.py` rewritten to spec §7.1-§7.7 with the Phase 1 turnover definition deleted, new `stats.py` and `report.py`, and the single command `scripts/run_experiment.py`; findings F24 (calibration object / volatility half), F25 (§6.3 "advantage" metric) and F26 (the report's validation consumed Test D's blind look) recorded as open owner decisions; first end-to-end run logged as `EXP-X-20261017-003`, exploratory and non-counting, with `B3` the best baseline and both candidates returning FAILURE). Updated the Appendix A index and ledger, the Appendix B note, and `docs/README.md`. | Ken Ira Lacson Talingting |
| 2026-10-17 | Added DEC-20261017-032 (release packaging chain: the frozen snapshot packs into a deterministic 1.67 MB release archive with an external `.sha256`; `scripts/verify_release.py` re-runs the harness against the extracted archive and asserts equality with the published table at tolerance zero; the run directory publishes `net_excess_returns.csv`; `scripts/make_figures.py` draws both headline figures; a `CI` workflow runs the fresh-clone suite and, when the release asset exists, the full reproduction). Findings **F27** (the bundle hash covers four files, not the five `manifest.json` lists — the first verifier rejected every valid snapshot), **F28** (`pandas.read_csv`'s default parser is lossy by one ULP) and **F29** (`docs/README.md`'s version header had drifted behind its own history, and the status board asserted a version for this file that this file did not declare) recorded. Added `tests/test_release_packaging.py`, `tests/test_docs_index.py`, and a `**Version:**` header to this file so the status board's claim about it is checkable. Nothing pushed; no release cut; F24-F26 remain open, so no public confirmatory language. `docs/README.md` to v1.14. | Ken Ira Lacson Talingting |
| 2026-10-17 | Added DEC-20261017-033 (**E7 closed**: `open_source_and_license_policy.md` v1.0 Draft written and registered as the eighth active document — MIT for code, explicitly **not** for the Yahoo-sourced snapshot archive). Finding **F30** raised: the published archive is a redistribution of third-party market data, so its disposition is a `[PROPOSED]` owner decision (publish with a NOTICE, recommended). The contribution model is `[PROPOSED]`; an attribution clause is added so F19/F28 are not read as upstream bugs. The **F26** recommendation (re-designate Test D as non-confirmatory, do not register a replacement) is presented as an owner decision and **not** resolved by this entry. `docs/README.md` to v1.15. | Ken Ira Lacson Talingting |
| 2026-10-17 | Added DEC-20261017-034 (**F26 resolved**: `EXP-H2-20261017-001` re-designated **EXECUTED (NON-CONFIRMATORY)**, its execution recorded as the *same run* as `EXP-X-20261017-003`, no replacement confirmatory test registered, and K1 not fired — so H2.4 is **untested rather than falsified**. The Appendix A index row, the entry's status, family line, Results, Conclusion and Decision are restated, and the reason the relabelling cannot rescue the hypothesis is recorded *inside the entry*. **E7 closed**: `open_source_and_license_policy.md` frozen at v1.0 with both `[PROPOSED]` items confirmed. The NOTICE placement deviates deliberately from DEC-033's wording — a `NOTICE.txt` member in the archive instead of a field in `manifest.json` — and the deviation is recorded rather than absorbed). `docs/README.md` to v1.16, `decision_log.md` to v1.9. | Ken Ira Lacson Talingting |
| 2026-10-17 | Added DEC-20261017-035 (the NOTICE implemented: `pack_snapshot.py` generates a deterministic `NOTICE.txt` member from a version-controlled template and refuses an on-disk copy; `verify_release.py` asserts the notice is present and unchanged before re-running the methods, so an archive that lost it fails loudly instead of publishing data with no statement attached. Archive digest `28e1d907…` → **`7a3fc209…`**, bundle hash and snapshot id **unmoved**. **Finding F31** recorded — the archive digest identifies the *distribution* and the snapshot id identifies the *data*, and an editorial addition moves one but not the other; the README now states what the digest is of. Four new packaging tests. Re-verification with the notice check active: `EXACT`, max abs diff `0.000e+00`, 18 columns). `docs/README.md` to v1.17, `decision_log.md` to v1.10. | Ken Ira Lacson Talingting |
| 2026-10-18 | Corrected the **Date** field of DEC-20261017-033/034/035 from 2026-10-17 to 2026-10-18. The entries carried the previous day forward by inertia across local midnight; their commit timestamps (`4541cc8`, `1444f3f`, `7e4067b`) are all 2026-10-18 and are the independent evidence — the record was checked against git, not against itself. The **IDs are deliberately not renamed**: an identifier has to stay stable, renaming would break references in `docs/README.md`, `open_source_and_license_policy.md`, `notes/` and this file's own text, and the Date field is the field that carries the date. DEC-20261017-032 is left at 2026-10-17 because its work straddles the boundary (`33dabdb`, 2026-10-18 00:35). **No entry content changed** — no decision, claim, result or reason. | Ken Ira Lacson Talingting |
| 2026-10-18 | Added DEC-20261018-036 (**finding F32**: the snapshot id was quoted by hand in four places and one carried a wrong separator — an extra underscore where the window end meets the retrieval date — so the README's own reproduction command returned **404** for any reader who followed it. Found by checking the literals against the filesystem rather than against each other; a fresh hand-typed copy in the workflow was wrong the same way within minutes, which is the real finding. All four corrected; `tests/test_snapshot_name_literals.py` added (five checks, shown to fail 4-of-5 when the defect is reintroduced); CI's optional fetch step now emits a warning naming what it skipped instead of failing silently, and `docs/published-run/outcomes.csv` is committed so the workflow can verify bit-for-bit rather than merely regenerate. **The release itself is unaffected**: the published asset name and digest were always correct). `docs/README.md` to v1.19. | Ken Ira Lacson Talingting |
| 2026-10-18 | Added DEC-20261018-037 (**finding F33**: the bit-for-bit comparison added one commit earlier *failed on its first real run* — CI run 39132731808, `autocorr1: 4.163e-17`, max abs diff `4.163e-17` over 18 columns, the other seventeen exact. `np.corrcoef` reaches a BLAS kernel that OpenBLAS selects from the CPU's features at run time, so the archive reproduced exactly on Windows and not on the runner. `autocorr1` now uses an exactly-rounded summation (`math.fsum` plus only the primitives IEEE-754 requires to be correctly rounded), which is bit-identical anywhere and slightly more accurate. **The published table was regenerated and the diff is the evidence**: 46 columns compared, exactly one changed (`autocorr1`, worst `9.714e-17`), no headline number moved. Two guards added — one parses the call graph so a revert to `corrcoef` fails, one checks the new path against an exact-rational reference. Residual limits — `np.cov`, `np.linalg` and the solver still sit on BLAS/LAPACK — are recorded rather than papered over. The archive, its digest and the snapshot id are unchanged). `docs/README.md` to v1.20. | Ken Ira Lacson Talingting |
| 2026-10-18 | Added DEC-20261018-038 (**finding F34**: the CI comparison failed a **second** time, on the next runner, on **thirteen** of eighteen columns, worst `4.698e-12` — and it was right again. Environment ruled out by parsing both runs' install lines as sets: 51 packages each, symmetric difference empty, identical runner image `ubuntu24/20261012.334.1`; the only difference is the machine (`GitHub Actions 1000000268` vs `…269`). Thread count ruled out by experiment: the pipeline run locally at one and at four BLAS threads gives byte-identical tables, both equal to the published one. Divergence located in the **weights** (`turnover_annualized` is a function of weights only and moved by `4.307e-12`), at `1e-13`–`1e-12` rather than `1e-16`, i.e. a `1e-16` covariance difference amplified by a solver whose own tolerance is the frozen `1e-14`. **F34:** a number produced by a solver is a property of *(data, code, machine)*, not of *(data, code)* — so the verifier's claim is **split rather than widened**: method set, rebalances, folds, headline cost level, the ranking by net Sharpe and the selected baseline are compared **exactly** and fail the build on any difference, while the continuous metrics are compared within a documented `1e-9` (~200x the measured noise, `1e-6` of the published precision) and the observed worst difference is printed on every run. `compare()` extracted as a pure function with **10 hermetic tests** (platform noise passes; `1e-6` fails; a changed count, ranking or baseline fails even with every metric in tolerance; the constant is pinned). DEC-037's item-5 claim corrected in place with a marker, DEC-036's pre-mortem no longer quotes a step name it can drift from, every public claim corrected in the same commit, and the run manifest now records the BLAS build, its `DYNAMIC_ARCH` ceiling, the thread controls and the machine shape (`report._blas_context`) so the next such difference is diagnosable from the artefact. Release unaffected: archive, digest, bundle hash and snapshot id unchanged. `docs/README.md` to v1.21. | Ken Ira Lacson Talingting |
| 2026-10-18 | Added DEC-20261018-039 (**E3** written): `results_reporting_and_claims_policy.md` v0.1 (Draft), the claims policy protocol §14 promises — §2 maps §14.1's nine disclosures to exact field names (`psr_benchmark` is a *column*, so "no p-value without its benchmark" is enforced mechanically), §3 fixes the status vocabulary (`EXECUTED (NON-CONFIRMATORY)` returns `FAILURE` while the hypothesis is **untested, not falsified**), §4 operationalises §14.2 plus four additions each tied to a real defect, and §8 collects the five open values as one decision-ready table. Every rule marked `[PROPOSED]` or as a restatement. The status board's prose count said *seven* while the table listed *eight* → now **checked against the table** by `tests/test_docs_index.py`. **Back-filled:** this revision row was omitted when the version was bumped to 1.15. | Ken Ira Lacson Talingting |
| 2026-10-18 | **Corrected DEC-20261018-038's own numbers** after reading the claims back against the artefacts (the same defect had reached the README, `docs/published-run/README.md` and the essays): "**six** orders of magnitude below the four decimals" where the true margin is **five** (`1e-9` against `1e-4`), and an "`1e-13` to `1e-12`" range where the observed spread is `3.442e-15` to `4.698e-12`. Each corrected form now states the quantity the argument turns on. **Back-filled:** the correction was made without a revision row. | Ken Ira Lacson Talingting |
| 2026-10-18 | Added DEC-20261018-040 (**E3 frozen at v1.0**): all five open values (**P1**–**P5**) and the two specification readings (**F24**, **F25**) confirmed by the owner in a single act rather than inferred. The draft's marking is replaced — `[§14]` (a restatement of a rule already frozen in the protocol, which wins any conflict) versus `[E3]` (this document's own rule, binding since v1.0) — and **§8 becomes the freeze record**, so a reader can tell a granted rule from an assumed one. **F25 is load-bearing and is now recorded as such:** the concentration clause binds for `M2` at 51.3%, so a *reading*, not the arithmetic, produces the published `FAILURE` verdict. The licence policy's §5 reduced to a pointer (its own review trigger, now marked fired) and E7 goes to v1.1. Documentation only: the archive, its digest, the bundle hash, the snapshot id and the published table are untouched, and the `NOTICE.txt` is code-generated and test-pinned. | Ken Ira Lacson Talingting |

---

*This log exists to make decisions explicit, dated, and reviewable. Its append-only discipline is the reason it can be trusted. If the log is edited to hide a gap, the log is worthless. If the log records its gaps, the log is the project's strongest artifact.*
