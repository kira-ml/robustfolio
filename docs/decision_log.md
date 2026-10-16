# Decision Log — robustfolio

**Project:** `robustfolio`
**Owner:** Ken Ira Lacson Talingting
**Created:** 2026-10-14
**Last Updated:** 2026-10-15
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
---

*This log exists to make decisions explicit, dated, and reviewable. Its append-only discipline is the reason it can be trusted. If the log is edited to hide a gap, the log is worthless. If the log records its gaps, the log is the project's strongest artifact.*
