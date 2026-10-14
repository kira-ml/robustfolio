# robustfolio — Execution TODO

**Version:** 1.0
**Status:** Active — execute in order
**Owner:** Ken Ira Lacson Talingting
**Created:** 2026-10-15
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

## Phase A — Stop the bleeding (do these first, ~2 hours total)

These items are pure consistency fixes. They remove redundancy that will
otherwise drift and cost you more time later. No new thinking required.

- [ ] **A1. Fix `README.md` to reflect reality.**
  - Problem: README lists 20 documents, 15 of which do not exist, and marks
    statuses that contradict the actual files (e.g., says charter is "Planned"
    while the actual file is Version 1.1 Draft).
  - Action: rewrite the status board to list only the 12 files that exist,
    with statuses matching the actual file headers.
  - Unblocks: nothing directly, but a wrong status board is worse than none.

- [ ] **A2. Execute the scope supersession.**
  - Problem: `scope_and_non_goals.md` says it supersedes
    `problem_framing.md` §10 and `project_charter.md` §5, but both still
    contain scope content.
  - Action:
    - Delete `problem_framing.md` §10, replace with a one-line pointer to
      `scope_and_non_goals.md`.
    - Delete `project_charter.md` §5, replace with a one-line pointer.
  - Unblocks: removes scope drift risk.

- [ ] **A3. Execute the evaluation-contract supersession.**
  - Problem: the evaluation contract (primary metric, baselines, protocol,
    success, falsification) appears in `problem_framing.md` §9,
    `success_metrics_and_evaluation_protocol.md` §2–6, and
    `falsification_and_kill_criteria.md` §2.
  - Action: delete `problem_framing.md` §9, replace with a pointer to
    `success_metrics_and_evaluation_protocol.md`.
  - Unblocks: removes threshold-drift risk.

- [ ] **A4. Execute the pre-mortem supersession.**
  - Problem: `problem_framing.md` §12 duplicates a subset of
    `risk_register_and_premortem.md` §4.
  - Action: delete `problem_framing.md` §12, replace with a pointer.
  - Unblocks: removes risk-register drift risk.

- [ ] **A5. Execute the kill/pivot taxonomy supersession.**
  - Problem: the taxonomy is defined in `project_charter.md` §7 and again in
    `falsification_and_kill_criteria.md` §3, which says "these match charter
    §7 but add operational precision."
  - Action: keep the taxonomy in `project_charter.md` §7. Replace
    `falsification_and_kill_criteria.md` §3 with a pointer to charter §7.
    Keep §4 (project-level triggers) in the falsification doc — that content
    is unique.
  - Unblocks: removes taxonomy drift risk.

- [ ] **A6. Execute the cost-level supersession.**
  - Problem: cost levels appear in
    `success_metrics_and_evaluation_protocol.md` §5.5,
    `cost_model_and_frictions.md` §3.3, and `scope_and_non_goals.md` §3.8.
  - Action: keep the cost levels in `cost_model_and_frictions.md` §3.3.
    Replace the other two with pointers.
  - Unblocks: removes cost-level drift risk.

- [ ] **A7. Verify the merges did not break cross-references.**
  - Action: search the docs/ folder for references to the deleted sections.
    Update each to point to the new single source.
  - Unblocks: cross-reference integrity.

---

## Phase B — Consolidate governance (do after A, ~4 hours)

These items merge governance documents that currently overlap. This is the
change that reduces your file count from 12 to roughly 8.

- [ ] **B1. Merge `falsification_and_kill_criteria.md` into
      `success_metrics_and_evaluation_protocol.md`.**
  - Rationale: hypotheses, thresholds, and kill triggers belong in one
    document. Splitting them across two files, plus a taxonomy copy in the
    charter, requires three files to answer "what happens if H2.4 fails?"
  - Action: create `evaluation_protocol.md` containing:
    - metrics and thresholds (from protocol §2–6)
    - hypotheses and falsification tests (from falsification §2)
    - kill/pivot/stop triggers (from falsification §4–6)
    - sunk-cost firewall (from falsification §7)
    - freeze rules (from protocol §11)
  - Retire the old two files. Keep them as `_v1_archived` if you want a
    historical record, but they are not the source of truth.
  - Unblocks: single source of truth for the evaluation contract.

- [ ] **B2. Tighten `project_charter.md`.**
  - Action: after A5 and A3, the charter should contain only:
    - mission, vision, primary objective
    - deliverables
    - non-goals (pointer to scope doc)
    - phase gates
    - kill/pivot/stop *authority* (not taxonomy)
    - decision rights
    - resource constraints
    - definition of done
  - Target length: one page of governance, not five.
  - Unblocks: charter becomes readable in 5 minutes.

- [ ] **B3. Tighten `scope_and_non_goals.md`.**
  - Action: it's currently good. After A2, it's the single source. Verify
    it contains no duplicates of the evaluation protocol or the cost model.
  - Unblocks: nothing, but keeps the file lean.

- [ ] **B4. Verify the new file set is internally consistent.**
  - Action: search for any remaining cross-document duplication.
  - Unblocks: confidence that the doc set is stable.

---

## Phase C — Write the missing substance (do after B, ~6-8 hours)

This is the actual gap. Right now, half your cross-references point at
`model_and_method_spec.md`, which does not exist.

- [ ] **C1. Decide the three open method choices.**
  - **D1. Shrinkage target.** Ledoit-Wolf 2004 (constant-correlation) or
    Ledoit-Wolf 2003 (identity). Recommendation: constant-correlation.
  - **D2. Black-Litterman views.** Use no views for MVP (prior mean +
    covariance as posterior)? Recommendation: yes, defer views to extension.
  - **D3. Risk parity solver.** Spinu (2013) coordinate descent, scipy
    minimize on log-barrier, or Newton on the fixed point. Recommendation:
    Spinu, for the convergence guarantee.
  - Action: write the three decisions into `decision_log.md`.
  - Unblocks: C2.

- [ ] **C2. Write `model_and_method_spec.md`.**
  - Required sections:
    1. Method ID registry (M-SC, M-LW, M-RP, etc.) — every other document
       references these.
    2. Covariance estimators: sample, Ledoit-Wolf (variant, target, intensity
       rule).
    3. Expected return estimators: sample mean, equal/none, Black-Litterman
       (prior, no views for MVP).
    4. Optimizers: MVO QP, min-variance QP, risk parity, L1-penalized QP
       (reformulated with auxiliary variables).
    5. Penalty alignment: how λ relates to κ, in what units, when they can
       diverge.
    6. Solver and tolerance: which solver (recommend Clarabel or OSQP),
       convergence criterion, failure behavior.
    7. Per-method test fixtures: a known input → a hand-computed output, so
       each method is verifiable.
  - Target length: 2,000–3,000 words of real content.
  - Unblocks: Phase 1 code.

- [ ] **C3. Freeze the method spec.**
  - Action: confirm every method choice. Bump to Frozen. Add revision row.
  - Unblocks: implementation.

---

## Phase D — Close the open decisions (do after C, ~2 hours)

You currently have ~46 `[PROPOSED]` values scattered across 7 documents.
You cannot freeze what you cannot see.

- [ ] **D1. Extract every `[PROPOSED]` value into one table.**
  - Action: create `open_decisions.md` (or add a section to the charter)
    listing every proposed value, its document and section, and a
    recommendation.
  - Unblocks: freezing.

- [ ] **D2. Confirm or replace each value.**
  - Action: for each proposed value, write "confirmed" or a replacement.
    Record in `decision_log.md`.
  - Unblocks: the protocol, data contract, and cost model can be frozen.

- [ ] **D3. Freeze the evaluation protocol, data contract, and cost model.**
  - Action: bump each to Frozen. Add revision rows.
  - Unblocks: Phase 1 experiments can now be legally run under your own
    rules.

---

## Phase E — Write the remaining referenced documents (do after D, or skip)

These are referenced by other docs but are not urgent. Do them when they
block something, not before.

- [ ] **E1. `decision_log.md`** — create the log file with one entry
      (the method choices from C1).
- [ ] **E2. `reproducibility_and_environment.md`** — write when you first
      set up the Python environment, not before.
- [ ] **E3. `results_reporting_and_claims_policy.md`** — write before Phase
      4 (reporting), not before.
- [ ] **E4. `roadmap_and_phase_gates.md`** — decline. The charter §6 already
      contains this. Update the README to remove the reference.
- [ ] **E5. `architecture_decision_records/`** — create the folder when you
      make your first irreversible technical decision, not before.
- [ ] **E6. `glossary.md`** — decline for now. Add terms if a reader is
      confused, not speculatively.
- [ ] **E7. `open_source_and_license_policy.md`** — write before public
      release, not before.

---

## Phase F — Run the first experiment (do after D, ~1-2 days of work)

**This is the point of the entire project.** Do not write more documentation
after this item.

- [ ] **F1. Implement the data ingestion pipeline (C1 from charter).**
  - Minimal: fetch raw prices + corporate actions for the candidate universe,
    store as a snapshot, compute point-in-time adjusted prices.
  - Do not build a general framework. Fetch only what the first experiment
    needs.

- [ ] **F2. Implement baseline B1 (1/N) and baseline B3 (sample MVO).**
  - Two methods. Nothing more.
  - Unit test each against a hand-computed fixture (from C2 §7).

- [ ] **F3. Implement the walk-forward harness with cost model.**
  - Rolling 36-month estimation, 12-month test, step 12 months.
  - Apply costs at 10 bps on drifted weights.
  - Compute net Sharpe.

- [ ] **F4. Run the H1.1 and H1.2 falsification tests.**
  - H1.1: does sample MVO produce max absolute weight > 0.40 in ≥ 1 fold?
  - H1.2: does sample MVO have annualized turnover ratio > 2.0?
  - If both fail: the problem framing is falsified. Pivot or stop. Write
    the result into the registry and the decision log.
  - If either holds: the problem framing survives Phase 1. Proceed to
    Phase 2 (robust methods).

- [ ] **F5. Log the experiment in the registry before running it.**
  - Use the pre-registration template. Include the snapshot hash, git
    commit, and family-size count.

---

## Explicitly not on this list (and why)

- **Do not write another governance document.** Nine governance docs
  governing three substance docs is already inverted. Adding another
  widens the gap.
- **Do not write extension specs.** L2 penalty, PCA factor, HRP,
  multi-period optimization — all out of MVP scope. Their time is Phase 5,
  if it comes.
- **Do not build a general framework.** Fetch what F1 needs. Refactor later,
  when you have a working loop and know what the abstractions should be.
- **Do not tune hyperparameters before F4.** The first experiment tests
  whether the premise is real, not whether a method wins.
- **Do not add a new method to rescue a failing result.** This is the
  sunk-cost failure mode you documented in `falsification_and_kill_criteria.md`
  §7 and `risk_register_and_premortem.md` R-P02. Honor your own rules.

---

## Definition of done for this TODO

This TODO is complete when all of the following are true:

1. `README.md` reflects the actual file set. (A1)
2. Supersessions are executed; no content is duplicated across documents.
   (A2–A7)
3. `falsification_and_kill_criteria.md` is merged into
   `success_metrics_and_evaluation_protocol.md`, now named
   `evaluation_protocol.md`. (B1)
4. `project_charter.md` is one page of governance. (B2)
5. `model_and_method_spec.md` exists and is Frozen. (C2, C3)
6. All `[PROPOSED]` values are confirmed or replaced; the evaluation
   protocol, data contract, and cost model are Frozen. (D1–D3)
7. The first experiment (F1–F5) has run and its result is recorded in the
   registry.

**After this TODO is complete, you will have 8–9 markdown files, one of
which is a method spec. The next artifact after that is code.**

---

## Revision history

| Date | Version | Change | Author |
|------|---------|--------|--------|
| 2026-10-15 | 1.0 | Initial execution TODO | Ken Ira Lacson Talingting |
