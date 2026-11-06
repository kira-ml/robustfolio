# Open Source and License Policy — robustfolio

**Version:** 1.2
**Status:** **Frozen**
**Frozen:** 2026-10-17 (see DEC-20261017-033 for the draft, DEC-20261017-034 for the confirmations)
**Revised:** 2026-10-18, v1.0 → 1.1 — §5 reduced to a pointer at DEC-20261018-040. **2026-11-06, v1.1 → 1.2 — §2 rewritten: third-party data is not redistributed (DEC-20261106-042). This supersedes the v1.1 disposition that permitted publishing the archive with a NOTICE.**
**Owner:** Ken Ira Lacson Talingting
**Created:** 2026-10-17

Two questions, and only two: **what may a reader do with this repository**, and **what may this project publish**. It is written before the first public release rather than after, because the second question changes what gets *uploaded*, not merely what gets said — and because the snapshot, which the verification chain depends on, is not the project's to publish.

---

## 1. Code

The code — `src/`, `scripts/`, `tests/`, and the markdown in `docs/` and `notes/` — is **MIT** licensed, per [`../LICENSE`](../LICENSE). Inbound contributions are accepted under the same terms (no CLA), which is the standard MIT in/out arrangement and the one that adds the least friction.

MIT is the right choice here rather than a copyleft licence because the artefact's value is that people can **check** it. A licence that discourages reuse of the checker would defeat the point.

---

## 2. Data — the part that is not the code

The pipeline reads third-party data. **No third-party data files are redistributed by this repository or by its releases.** MIT covers the code and the project's own text and artefacts; it does not cover the data, and this project cannot grant rights it does not hold. Derived tables (`outcomes.csv`, `decisions.csv`, `cap_sweep.csv`, `paired_inference.json`, `country-sample/` tables, and `results/phase1_results.csv`) are published as project-authored statistics; they contain no raw observations and inherit the data's provenance.

| Component | Source | Redistribution status |
|---|---|---|
| `prices_raw.parquet`, `actions.parquet` | Yahoo Finance via `yfinance`, retrieved 2026-10-17 | **Not redistributed.** Yahoo's terms restrict automated collection and do not grant a redistribution right. |
| `rf_dgs1mo.parquet` | FRED series `DGS1MO` | **Not redistributed.** The underlying series is US government data, but FRED's service terms separately prohibit storing, caching, archiving, or providing FRED content to third parties. |
| `universe_pit.csv` | ETF issuers' fact sheets (SPDR, iShares, …) | The snapshot copy is not redistributed. The public candidate list contains tickers and eligibility dates, not prices. |
| `manifest.json`, `quality_report.md` | This project | Covered by MIT. |
| Everything derived from the above (`outcomes.csv`, `decisions.csv`, findings, figures) | This project | Covered by MIT as project authorship, **but inherits the data's provenance**. The derived tables contain statistics, not raw observations. |

**Disposition — do not redistribute. Confirmed 2026-11-06 (DEC-20261106-042), superseding the v1.1 disposition.** Rationale:

1. **A notice is not a licence.** v1.1 published the archive on the theory that a non-commercial verification copy with attribution was permissible. A terms review found no redistribution grant from either Yahoo or FRED. Non-commercial purpose and attribution do not create permission.
2. **The narrower reading is the defensible one.** The project's value is that it documents its own limits. Publishing data it has no right to publish would undercut that claim more than losing exact reproduction does.
3. **The archive is not the claim.** The claim is that the code, the frozen configuration, and the published tables can be inspected. Exact end-to-end reproduction was the strongest supporting check, not the result itself.

**What changed.** On 2026-11-06 the snapshot archives and checksums were deleted from the `v1.0.0` and `v1.1` releases, and both release bodies were corrected. The local archives remain only for the owner's verification; they are gitignored and must not be uploaded again without a written permission that covers redistribution. [`data_licenses.md`](data_licenses.md) records each file, its terms, and the disposition.

**The NOTICE.** `scripts/pack_snapshot.py` still writes a **`NOTICE.txt`** member into a locally packed archive, generated deterministically from a template in that script. It now states that the archive is **not for redistribution** and records the source and retrieval date. It is a provenance statement, not a licence.

*Why not `manifest.json`* — DEC-20261017-033 originally required the notice in "the archive's own manifest", and DEC-20261017-034 changed that deliberately. `manifest.json` is the data layer's hashed record; a licensing statement is neither data nor a statement about data, and putting it there would place a mutable editorial statement inside the artefact the integrity chain reads. A sibling `NOTICE.txt` is reviewable in git, travels with extraction, and cannot drift from the snapshot on disk.

**Consequences, stated as a degradation.** Without the exact input, "one command regenerates the number" becomes "one command regenerates the code path; the number was produced by an input the reader does not have." The verifier and the committed tables remain, so the comparison is still inspectable, but a third party cannot run it end to end from this repository alone. That is worse than the v1.1 arrangement, and it is documented as worse in the README, the paper, and [`published-run/README.md`](published-run/README.md) rather than quietly dropped.

**Rejected alternatives.** Publishing the archive with a NOTICE (the v1.1 disposition) is rejected: a notice cannot supply a missing licence. Publishing only the derived monthly series is rejected for the same reason: it is still derived from the same restricted content, and it would not reproduce the daily→monthly aggregation, the corporate-action application, or the point-in-time eligibility. Publishing nothing at all is rejected because the code, tables, and identity digests remain useful and publishable.

**Reversibility:** the disposition is revocable if the owner obtains a written redistribution permission or a licensed substitute. Any such change requires a new `decision_log.md` entry. The default is **do not redistribute**.

---

## 3. What this project does not publish

- **No live signals, no positions, no investment advice.** The output is an evaluation, not a strategy.
- **No claim of tradable alpha, and no absolute-return framing** (protocol §14.2).
- **No confirmatory language while finding F26 is open.** The registered confirmatory test's answer has already been observed, so the honest description is "pre-registered, mechanically evaluated, non-confirmatory".
- **No personal data.** There is none in the pipeline: the inputs are public market data and public fund metadata.

---

## 4. Contributions

**Confirmed 2026-10-17 (DEC-20261017-034):** issues and pull requests are welcome; no CLA and no DCO sign-off. A contribution must, at minimum:

1. keep `pytest -q` green (including the leakage suite and the packaging-integrity tests);
2. not change a frozen value — a threshold, a seed, a metric definition, the cost model, or a registered hypothesis — without a `decision_log.md` entry, because those values are what make the numbers quotable;
3. state, if it changes a result, **which** result changed and by how much.

Findings are welcome. This project publishes its own defects (F1–F34) on the view that a documented defect is evidence about the method rather than an embarrassment; a report that a specific finding is wrong is treated the same way.

---

## 5. Attribution and what a reader may claim

**Reduced to a pointer on 2026-10-18** (DEC-20261018-040), as this section's own review trigger said it would be. The claim rules stated here in v1.0 now live in exactly one place:

- [`results_reporting_and_claims_policy.md`](results_reporting_and_claims_policy.md) — **§5** (quoting a number: with its interval, its cost level and its exploratory status; no metric presented as a return, a forecast or a recommendation) and **§6** (findings describe this project's implementation, not defects in upstream libraries, and F19 and F28 must not be cited as upstream bugs).

Protocol §14.2 remains the authority and E3 operationalises it; nothing is stated there that is not either a restatement of §14 or a rule E3 identifies as its own.

---

## 6. Review trigger

- Both dispositions confirmed 2026-10-17 → **v1.0 Frozen**.
- **Fired 2026-11-06:** a terms review found that neither Yahoo nor FRED grants a redistribution right. §2 was re-examined, the archive assets were removed from the `v1.0.0` and `v1.1` releases, and the disposition became **do not redistribute** at v1.2 (DEC-20261106-042).
- Yahoo, FRED, or an ETF issuer changes its terms, or any third party objects to a published artefact → §2 is re-examined and the disposition revisited, with the outcome recorded in `decision_log.md`.
- The owner obtains written permission, or a licensed data substitute, that permits redistribution → §2 may be revisited; the default remains **do not redistribute** until that permission exists.
- A contribution-model dispute arises → §4 revisited.
- `results_reporting_and_claims_policy.md` (E3) is written → §5 is reduced to a pointer, so that the claim rules exist in exactly one place. **Fired 2026-10-18**: E3 was written, frozen at v1.0, and §5 reduced to a pointer (DEC-20261018-040).
