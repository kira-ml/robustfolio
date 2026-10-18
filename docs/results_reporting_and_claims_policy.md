# Results Reporting and Claims Policy — robustfolio

**Version:** 1.0
**Status:** **Frozen**
**Frozen:** 2026-10-18 (DEC-20261018-040; draft at DEC-20261018-039)
**Owner:** Ken Ira Lacson Talingting
**Created:** 2026-10-18
**Subordinate to:** [`evaluation_protocol.md`](evaluation_protocol.md) §14 (Frozen). Where this document and §14 disagree, §14 wins.

Two questions, and only two: **how is a result reported**, so that a reader can find every mandatory
disclosure without trusting the author's summary of it; and **what may be claimed from it**, so that a
true sentence cannot be built out of a number that does not support it. It is written because a claim
is the cheapest thing in a project to overstate and the most expensive to retract — and because these
rules previously lived in four places (protocol §14.2, §5 of the licence policy, the F26 relabelling, and
the README's limitations), which is one place too many. On freeze, the licence policy's §5 was reduced to
a pointer here, as it said it would be.

**Every rule below carries one of two marks, and the distinction is load-bearing.** `[§14]` — a
restatement of a rule already frozen in the protocol, which wins any conflict. `[E3]` — this document's
own rule: binding since v1.0, and revised only by a new entry in `decision_log.md`. While this document
was a draft each of its rules carried `[PROPOSED]`, binding nothing until the owner confirmed it, and §8
records the act that removed that status. A policy that quietly acquires authority it was never granted
is the same failure as a claim that quietly outruns its number.

---

## 1. Precedence

- `[§14]` Protocol §14.1 (required disclosures) and §14.2 (forbidden claims) bind on every public
  artefact. This document may **operationalise** them and may **not** weaken them. Any conflict
  resolves to the protocol.
- `[E3]` "Public artefact" means: this README, anything in `docs/`, `notes/` or `essays/`, a release
  note, an issue, a pull request, **a public post**, or a message sent to a reviewer. Working notes are
  not governed, but they are quoted, so they are written as if they were.
- `[E3]` A rule here is enforced by a check where a check is possible, and by a disclosure where it is
  not. An unenforceable rule is written down as a rule with its enforcement gap named, rather than as
  an aspiration that reads like a guarantee.

## 2. The reporting template: §14.1's nine disclosures, and where they live

`[§14]` the nine disclosures. `[E3]` the mapping to artefacts, which is checkable column by column and
**binds every experiment reported after this freeze**: a row with nothing to report is recorded as empty
with the reason, rather than omitted.

| # | §14.1 requires | artefact | field, exactly | how a reader checks it |
|---|---|---|---|---|
| 1 | gross and net Sharpe at every cost level (§5.5.3) | `outcomes.csv` | `net_sharpe_{0,5,10,20,50}bps`, `net_sharpe`, `gross_sharpe_diagnostic`, `headline_cost_bps`, `cost_drag` | re-run; compare |
| 2 | in-sample and out-of-sample, clearly labelled | — | every performance number here is computed on the **out-of-sample** stream (first OOS month 2012-06-30); none is in-sample | the first OOS date is in the run's `folds_*.csv` |
| 3 | turnover, drawdown, CVaR, cost drag | `outcomes.csv` | `turnover_annualized`, `max_drawdown`, `cvar95`, `cost_drag` | re-run; compare |
| 4 | deflated Sharpe and probabilistic Sharpe | `decisions.csv` | `psr`, `psr_benchmark`, `psr_threshold`, `dsr`, `dsr_pvalue`, `dsr_family_size`, `dsr_v_is_convention` | the benchmark is a **column**, not a footnote |
| 5 | confidence intervals for all headline metrics | `outcomes.csv` | `net_sharpe_ci_low/high/level/reps/block/seed/n`, and the same for turnover, drawdown and CVaR | a CI without its method is a number with a rumour attached, so the method, replication count, block length and seed are column names |
| 6 | number of trials in the family, and the adjustment | `decisions.csv`, `manifest.json` | `dsr_family_size` (= 1), `design.csv` | with `N = 1` the deflation is inert — DSR ≡ PSR against zero — so **the binding constraint is the benchmark, not the correction**, which is why row 4 matters more here than row 6 |
| 7 | data period, universe, exclusions | `manifest.json`, `universe_pit.csv` | snapshot id; `first_eligible`, `last_eligible`, `source_note` | the ADV floor binds on `RWX`, and an exclusion that binds is disclosed where it binds |
| 8 | protocol deviations, with justification | `decision_log.md` | the `F`-series findings | the live one: spec §5.6's solver-tolerance sentence is contradicted by the implementation and is deferred to the next versioned revision |
| 9 | limitations and known failure modes | `report.md`, `README.md` | "Limitations" | a limitation with a number attached beats a limitation with an adjective attached |

`[E3]` If a future experiment reports in-sample numbers, the label goes in the **field name**, not in a
paragraph: a reader who sorts a table must not be able to lose the label.

## 3. Status vocabulary

`[§14]` These tokens already bind; they are collected here because a claim is read in the context of
the status it carries.

| token | means | may be cited for or against a hypothesis? |
|---|---|---|
| `EXPLORATORY` | non-confirmatory (DEC-20261015-012). Everything this project has published to date | **no** |
| `EXECUTED (NON-CONFIRMATORY)` | a pre-registered test run without the blindness its own registration required (F26, DEC-20261017-034). Same execution as `EXP-X-20261017-003`, a second label | **no** |
| `CONFIRMATORY` | reserved | only after the registration rule below is satisfied |

`[§14]` For an `EXECUTED (NON-CONFIRMATORY)` test the verdict is `FAILURE` and the hypothesis is
**untested, not falsified**. The public phrasing is fixed: *"pre-registered, mechanically evaluated,
non-confirmatory"*. Relabelling an execution cannot rescue a hypothesis, and the distinction is stated
rather than implied (DEC-20261017-034 item 3).

`[E3]` `CONFIRMATORY` may be used only for a test that was registered **blind**, against a sample that
did not exist when the registration was written, with the design not selected by any observed result —
and the artefact must name the sample in the same sentence. A registration whose sample already exists is
exploratory no matter when it was written down.

`[E3]` The word "confirmatory" appears in a public artefact only inside a disclosure that says which of
the three senses above is meant. It is never used as a modifier of "result".

## 4. Forbidden claims, operationalised

`[§14]` §14.2's list, with the compliant form and the specific failure each one prevents:

| forbidden | why it is the tempting failure | the compliant form |
|---|---|---|
| any absolute return claim, "beats the market" | the return series exists and can be plotted | net **excess** Sharpe, with its interval and its cost level, labelled exploratory. Cumulative net excess return is a metric's input path, not a return stream |
| any claim from gross Sharpe | it is larger | `gross_sharpe_diagnostic` is labelled diagnostic, appears only beside the net figure, and is legitimate only as a decomposition (`cost_drag = SR_gross − SR_net` under the same rf) |
| any claim from in-sample performance | in-sample numbers are always better | no in-sample performance is reported (§2 row 2) |
| any claim from an unadjusted p-value | a p-value quoted alone is the most credible-looking way to say nothing | every p-value is quoted **with its benchmark**, which is a column (`psr_benchmark`) rather than a recollection. Here the contrast *is* the finding: PSR's benchmark is the best baseline, DSR's is zero, and quoting one without the other inverts the result |
| any superiority claim without an interval | point estimates are what get remembered | every headline number carries `_ci_low`/`_ci_high` and the interval's method |
| any single-fold or single-cost-level claim | the best fold, or the free cost level, is easy to find | fold counts carry their denominator and the concentration clause; costs are swept, and 10 bps is the headline rather than the only level |

`[E3]` Four additions, each learned from a specific defect in this repository rather than imported from
good practice:

1. **A reproduction claim names the command that shows it and what that command prints.** A claim whose
   check does not exist is not made (F32: the README's own command returned 404).
2. **A reproduction claim is stated at the strength the check actually has.** "Decisions exact,
   measurements within a documented bound, observed value printed" — not "bit-for-bit", which was false
   twice (F33, F34).
3. **A mechanism is not a result.** A finding about how the numbers behave (a kernel, a parser, a
   tolerance) is described as a property of this implementation, never as a property of the world.
4. **A number is not quoted from a table without naming the table's status.** Every number quoted from
   `docs/published-run/outcomes.csv` carries "exploratory and non-confirmatory".

## 5. Quoting a number

`[E3]` Quoting a number is encouraged, provided it is quoted **with its interval, its cost level and its
exploratory status**. No metric here may be presented as a return, a forecast, or a recommendation.

## 6. Findings describe this implementation, not upstream libraries

`[E3]` Findings in `docs/decision_log.md` describe **this project's implementation and readings**, not
defects in `cvxpy`, `scikit-learn`, `pandas` or any other upstream library. F19 and F28 document upstream
behaviour that is working as specified; they must not be cited as upstream bugs. Where a finding *is*
about an upstream defect, it is reported upstream first and cited here only afterwards.

## 7. What this document does not do

`[E3]` It does not decide whether the null result is interesting — that is the narrative's job, subject to
§4 — and it does not require that a result be interesting before it can be reported. It does not govern
the internal working notes. It does not turn a bounded measurement into a guarantee: §4 item 2 is the rule
that keeps the reproduction claim inside its check.

## 8. The freeze record

`[§14]` Nothing in this document bound before 2026-10-18. It was written as a draft in which every rule was
marked `[PROPOSED]`, and the five values below were confirmed by the owner in one act rather than chosen
silently (DEC-20261018-040). The right-hand column is what the document now says, and it is the row that
would be checked if a reader ever doubted whether a rule here was granted or assumed.

| # | value | confirmed as |
|---|---|---|
| P1 | this document is a governed document, not an unregistered note | governed: board row 9, versioned, frozen like the protocol. The licence policy's §5 reduced to a pointer, so the claim rules exist in one place |
| P2 | `CONFIRMATORY` requires a blind registration against a sample that did not yet exist | §3, final two entries |
| P3 | the §2 template binds future experiments | §2: a row with nothing to report is recorded as empty with a reason, not omitted |
| P4 | a public post is a governance event for §4 | §1: "public artefact" includes a public post |
| P5 | the two shorter cuts of the flagship essay are governed by §4 identically to the long one | claimed in `essays/README.md`: no cut may say what the long form may not |

`[E3]` Two specification readings were confirmed in the same act, because they decide published claims
and had until then been disclosed rather than settled. They are recorded here as cross-references; they
are implemented in the report and the decision log, not in this document:

- **F24** (§7.8's calibration does not define what is predicted): the **return** half is implemented
  under a stated reading — the trailing window is the method's own previous 60 months of net portfolio
  returns, the interval is formed by the stationary bootstrap, and the realisation is the next month's net
  return (coverage 81.5–87.0%). The **volatility half is not implemented**, and no coverage number is
  reported for it, because at a one-month horizon no monthly volatility is realised and any number would
  be a definition rather than a measurement.
- **F25** (§6.3's "advantage" is not pinned to a metric): fold wins are counted on **net Sharpe**, the
  §2 primary metric, while the concentration clause uses the **per-fold mean monthly net excess return
  difference**, because a Sharpe is not additive and the clause requires an additive decomposition. This
  reading is load-bearing: in the published run the concentration clause is the binding one for `M2` at
  51.3%, so **this reading produces the published `FAILURE` verdict**.

## 9. Review trigger

- **Protocol §14 is revised** → this document is revised in the same act, or dies. A policy that restates
  a contract is only as good as its fidelity to the contract.
- **A public claim is disputed** → the resolution is recorded in `decision_log.md`, and if the dispute
  has force the rule here is amended rather than the claim defended.
- **A rule here is found to be unenforceable** → it is rewritten with the gap named (§1), because a rule
  that reads like a guarantee while relying on discipline is the failure mode this repository keeps
  finding in its own claims.
- **A future experiment cannot fill a §2 row** → that is a finding about the template, not a licence to
  omit the row: the empty row is recorded with its reason, and if the gap recurs the template moves to
  v1.1 with the change recorded.
- **The frozen flag itself is doubted** → the check is `tests/test_docs_index.py`, which compares this
  document's own `**Version:**`/`**Status:**` header against the status board. A freeze that two files
  disagree about is not a freeze.
