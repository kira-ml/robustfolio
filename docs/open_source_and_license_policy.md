# Open Source and License Policy — robustfolio

**Version:** 1.0
**Status:** Draft — awaiting owner confirmation of two `[PROPOSED]` dispositions
**Owner:** Ken Ira Lacson Talingting
**Created:** 2026-10-17

Two questions, and only two: **what may a reader do with this repository**, and **what may this project publish**. It is written before the first public release rather than after, because the second question changes what gets *uploaded*, not merely what gets said — and because the snapshot asset, which the whole verification chain depends on, is not the project's to license.

---

## 1. Code

The code — `src/`, `scripts/`, `tests/`, and the markdown in `docs/` and `notes/` — is **MIT** licensed, per [`../LICENSE`](../LICENSE). Inbound contributions are accepted under the same terms (no CLA), which is the standard MIT in/out arrangement and the one that adds the least friction.

MIT is the right choice here rather than a copyleft licence because the artefact's value is that people can **check** it. A licence that discourages reuse of the checker would defeat the point.

---

## 2. Data — the part that is not the code

The repository's most load-bearing output is a **frozen snapshot archive**, published as a release asset so that a reader can reproduce the published numbers exactly rather than approximately (DEC-20261017-032). That archive contains third-party data, and **the MIT licence does not cover it**:

| Component | Source | Status |
|---|---|---|
| `prices_raw.parquet`, `actions.parquet` | Yahoo Finance via `yfinance` | Third-party market data. Yahoo's terms govern use and restrict redistribution. |
| `rf_dgs1mo.parquet` | FRED series `DGS1MO` (US Treasury) | US federal government data; effectively public domain. |
| `universe_pit.csv` | ETF issuers' fact sheets (SPDR, iShares, …) | Instrument metadata, derived and re-expressed by this project. |
| `manifest.json`, `quality_report.md` | This project | Covered by MIT. |
| Everything derived from the above (`outcomes.csv`, `net_excess_returns.csv`, findings, figures) | This project | Covered by MIT, **but inherits the data's provenance**. |

**The tension is real and should be stated rather than resolved silently.** The archive is a redistribution of roughly 4,966 daily rows × 18 instruments of Yahoo-sourced prices. It is also the *only* way the project's central claim stays true: without the exact input, "one command regenerates the number" degrades into "one command generates a similar number", which is the failure the release chain exists to prevent.

**`[PROPOSED]` disposition (a) — publish the archive, with a NOTICE.** Rationale:

1. The data is factual daily prices of publicly listed ETFs, of the kind widely republished, used here non-commercially and with attribution.
2. The purpose is verification of published results, not the distribution of a data product.
3. Deleting the archive would remove the one property that distinguishes this project from every unverifiable backtest.

**Required if (a) is confirmed**, and enforced by review rather than by hope: the README, the release notes, and the archive's own manifest must each state the **source**, the **retrieval date**, that **Yahoo's terms govern the data and MIT does not cover it**, and that the asset exists **to verify the published results**.

**Rejected alternatives.** Publishing only the derived monthly series (option b) is smaller and more defensible, but it would not reproduce the daily→monthly aggregation, the corporate-action application, or the point-in-time eligibility by date — i.e. it would verify the arithmetic while leaving the analyst's actual work unverified. Publishing nothing (option c) leaves the digest meaningless.

**Reversibility:** the asset is deletable and the disposition is revocable. If the owner, Yahoo, or any third party objects, the asset comes down and the verification path degrades to a published digest plus a rebuild instruction — which is *worse, and will be documented as worse* in the README, rather than quietly dropped.

---

## 3. What this project does not publish

- **No live signals, no positions, no investment advice.** The output is an evaluation, not a strategy.
- **No claim of tradable alpha, and no absolute-return framing** (protocol §14.2).
- **No confirmatory language while finding F26 is open.** The registered confirmatory test's answer has already been observed, so the honest description is "pre-registered, mechanically evaluated, non-confirmatory".
- **No personal data.** There is none in the pipeline: the inputs are public market data and public fund metadata.

---

## 4. Contributions

**`[PROPOSED]`:** issues and pull requests are welcome; no CLA and no DCO sign-off. A contribution must, at minimum:

1. keep `pytest -q` green (including the leakage suite and the packaging-integrity tests);
2. not change a frozen value — a threshold, a seed, a metric definition, the cost model, or a registered hypothesis — without a `decision_log.md` entry, because those values are what make the numbers quotable;
3. state, if it changes a result, **which** result changed and by how much.

Findings are welcome. This project publishes its own defects (F1–F29) on the view that a documented defect is evidence about the method rather than an embarrassment; a report that a specific finding is wrong is treated the same way.

---

## 5. Attribution and what a reader may claim

Quoting a number is fine, and encouraged, provided it is quoted **with its interval, its cost level, and its exploratory status**. The full prohibitions live in protocol §14.2 and, once written, in `results_reporting_and_claims_policy.md` (Appendix B item **E3**). No metric here may be presented as a return, a forecast, or a recommendation.

Findings recorded in `docs/decision_log.md` describe **this project's implementation and readings**, not defects in `cvxpy`, `scikit-learn`, `pandas`, or any other upstream library. Two of them (F19, F28) document behaviour of upstream code that is working as specified; they must not be cited as upstream bugs.

---

## 6. Review trigger

- Owner confirms both `[PROPOSED]` dispositions → **v1.0 Frozen**.
- Yahoo, FRED, or an ETF issuer changes its terms, or any third party objects to the archive → §2 is re-examined and the asset's disposition revisited, with the outcome recorded in `decision_log.md`.
- A contribution-model dispute arises → §4 revisited.
- `results_reporting_and_claims_policy.md` (E3) is written → §5 is reduced to a pointer, so that the claim rules exist in exactly one place.
