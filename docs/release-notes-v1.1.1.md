# v1.1.1 — claim correction and DOI archive

**Released:** 2026-11-08
**Tag:** `v1.1.1`
**Status:** Compliance and claim-correction patch. No research result changed.

## Why this release exists

The `v1.1` release labeled the country-ETF sample **confirmatory**. A pre-publication audit found that the repository cannot establish that the protocol was frozen before execution:

- the country results were written at **2026-11-05 19:51:35**;
- the protocol file was last written at **20:08:45**;
- both were committed together at **20:09:27**;
- the “confirmatory” label was added at **20:15:08**.

The protocol file was created before the snapshot, but its final content was written after the results. No earlier copy, commit, dangling object, editor-history entry, or cloud copy exists. The sample is therefore a **pre-specified external replication**, not a confirmatory test. The numbers, tables, methods, and verdicts are unchanged.

Full evidence: [`notes/audit_2026-11-08.md`](../notes/audit_2026-11-08.md).

## What changed

- Country status changed from **Confirmatory** to **External replication; protocol dated 2026-11-05, freeze not independently verified** everywhere it appeared: README, paper, brief, carousel, positioning, release notes, country README, result note, protocol note, synthesis, and outreach notes.
- Version `1.1.1` in `pyproject.toml`, `robustfolio.__version__`, and `CITATION.cff`.
- Audit note added.
- A test now pins the country label so the old claim cannot reappear silently.

No return, metric, verdict, method, cost, or solver changed. The US end-to-end check remains **EXACT**; the country sample reproduces exactly with its own runner.

## What is published

- Code, tests, documentation, project-authored tables, figures, and PDFs.
- No third-party market data. The Yahoo Finance prices and corporate actions and the FRED `DGS1MO` series are not included and are not redistributed.
- No snapshot archive is attached to this release.

## DOI

A DOI draft is private; it is not part of this release until the claim correction and external review gates are complete. Do not publish the earlier `v1.1.0` draft.

## Tag note

The `v1.1` tag points to the pre-correction tree and is not moved. Use `v1.1.1` or the corrected DOI archive. The `v1.1` release body carries a pointer to this release.

## Limits

This is a methods study, not a trading system. No alpha claim, no live deployment, no investment advice. The country sample is current-listed and not survivorship-free. Exact end-to-end reproduction requires independently obtained data.
