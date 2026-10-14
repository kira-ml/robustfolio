# robustfolio — Execution TODO

**Version:** 1.1
**Status:** Active — Phase A/B partially executed 2026-10-15
**Owner:** Ken Ira Lacson Talingting
**Created:** 2026-10-15
**Last Updated:** 2026-10-15
**Purpose:** Close the structural gaps identified in the documentation review,
reduce redundant documentation, and unblock Phase 1 (first experiment).

**Rule:** After this TODO is complete, the next artifact is *code*, not markdown.

---

## 0. How to use this list

- Items are ordered by dependency, not by importance.
- `[ ]` = not started. `[~]` = in progress. `[x]` = done. `[-]` = declined (with reason).
- Every item names the artifact it changes and the artifact it unblocks.
- If an item requires a decision, the decision is stated explicitly, not implied.
- Do not add items to this list. If you discover a new task, it goes into
  `decision_log.md` as an entry, not into this file.

---

## Progress snapshot (2026-10-15)

- **A2–A6:** done (via `problem_framing.md` v2.2).
- **B1:** done — `evaluation_protocol.md` v2.0 exists.
- **F1–F4:** done in exploratory form — Phase 1 experiment ran; H1.1 and H1.2
  not falsified; results in `results/phase1_results.csv`.
- **Deferred/cancelled by owner decision (2026-10-15):** the target doc set is
  being reduced to ~5 files, not 8–9. Phase B/C/D/E are therefore re-scoped.
  See "Open decision" at bottom.

---

## Phase A — Stop the bleeding

- [ ] **A1. Fix `README.md` to reflect reality.** Not done.
- [x] **A2. Execute the scope supersession.** Done via v2.2.
- [x] **A3. Execute the evaluation-contract supersession.** Done via v2.2.
- [x] **A4. Execute the pre-mortem supersession.** Done via v2.2.
- [x] **A5. Execute the kill/pivot taxonomy supersession.** Done via v2.2.
- [x] **A6. Execute the cost-level supersession.** Done via v2.2.
- [ ] **A7. Verify the merges did not break cross-references.** Partially —
  dead links remain in several docs; will be resolved by the merge.

---

## Phase B — Consolidate governance

- [x] **B1. Merge `falsification_and_kill_criteria.md` into
      `success_metrics_and_evaluation_protocol.md`.** Done — new file is
      `evaluation_protocol.md` v2.0. Old files deleted.
- [ ] **B2. Tighten `project_charter.md`.** Pending re-scope — the plan now is
      to delete the charter, not tighten it (mission → problem_framing;
      gates/decision rights → README or decision_log).
- [ ] **B3. Tighten `scope_and_non_goals.md`.** Pending.
- [ ] **B4. Verify the new file set is internally consistent.** Pending the
      larger merge.

---

## Phase C — Write the missing substance

- [ ] **C1. Decide the three open method choices.**
- [ ] **C2. Write `model_and_method_spec.md`.**
- [ ] **C3. Freeze the method spec.**

*(Re-scope note: if the doc set collapses to 5 files, the method spec may
become a section of the evaluation protocol or the problem framing, not a
standalone file.)*

---

## Phase D — Close the open decisions

- [ ] **D1. Extract every `[PROPOSED]` value into one table.**
- [ ] **D2. Confirm or replace each value.**
- [ ] **D3. Freeze the evaluation protocol, data contract, and cost model.**

---

## Phase E — Write the remaining referenced documents

- [~] **E1. `decision_log.md`** — exists with seed entries; needs a real entry
      for Phase 1's parameter choices (60/0.40/1.0/0.1).
- [ ] **E2. `reproducibility_and_environment.md`** — write when needed.
- [ ] **E3. `results_reporting_and_claims_policy.md`** — write before Phase 4.
- [-] **E4. `roadmap_and_phase_gates.md`** — declined.
- [ ] **E5. `architecture_decision_records/`** — create when needed.
- [-] **E6. `glossary.md`** — declined for now.
- [ ] **E7. `open_source_and_license_policy.md`** — write before public release.

---

## Phase F — Run the first experiment

- [x] **F1. Implement the data ingestion pipeline.** Done — `src/robustfolio/data.py`.
- [x] **F2. Implement baseline B1 (1/N) and baseline B3 (sample MVO).** Done,
      plus four additional methods.
- [x] **F3. Implement the walk-forward harness with cost model.** Done —
      `src/robustfolio/backtest.py`. Note: used 60-month train window, not 36.
- [x] **F4. Run the H1.1 and H1.2 falsification tests.** Done. Both not
      falsified. See `problem_framing.md` §14 and `results/phase1_results.csv`.
- [ ] **F5. Log the experiment in the registry before running it.** Not done —
      Phase 1 ran as an exploratory smoke test without a registry entry. This
      is a decision-log item, not a TODO item.

---

## Explicitly not on this list (and why)

- Do not write another governance document.
- Do not write extension specs.
- Do not build a general framework.
- Do not tune hyperparameters before F4.
- Do not add a new method to rescue a failing result.

---

## Open decision (2026-10-15)

The owner has decided to reduce the doc set to ~5 foundational files instead of
8–9. This supersedes the "Definition of done" below. The revised target:

```
README.md
docs/problem_framing.md
docs/scope_and_non_goals.md
docs/evaluation_protocol.md      ← absorbs baselines, cost, data, registry rules
docs/decision_log.md
```

Files to merge or delete: `benchmark_and_baseline_spec.md`,
`cost_model_and_frictions.md`, `data_contract_and_point_in_time_policy.md`,
`experiment_registry_and_preregistration.md`, `risk_register_and_premortem.md`,
`project_charter.md`.

Merge estimated at 4–6 hours. Not urgent. Execute when next session begins.

---

## Definition of done for this TODO

*(Superseded by the Open Decision above. Retained for historical reference.)*

1. `README.md` reflects the actual file set. (A1)
2. Supersessions are executed; no content is duplicated across documents. (A2–A7)
3. `evaluation_protocol.md` is the single evaluation contract. (B1)
4. `project_charter.md` is one page of governance. (B2)
5. `model_and_method_spec.md` exists and is Frozen. (C2, C3)
6. All `[PROPOSED]` values are confirmed or replaced. (D1–D3)
7. First experiment (F1–F5) has run and its result is recorded. (F1–F5)

---

## Revision history

| Date | Version | Change | Author |
|------|---------|--------|--------|
| 2026-10-15 | 1.0 | Initial execution TODO | Ken Ira Lacson Talingting |
| 2026-10-15 | 1.1 | Marked A2–A6, B1, F1–F4 complete; noted deferred/re-scoped items; added Open Decision on 5-doc target | Ken Ira Lacson Talingting |
