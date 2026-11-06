# TODO

**Updated:** 2026-11-06
**Status:** Working checklist. Not a governance document, not a contract.
**Authority:** decisions live in [`docs/decision_log.md`](docs/decision_log.md). The old `TODO.md` was retired into its Appendix B; this file is the execution view of the current plan, not a revival of that ledger.

**Current constraint:** independent review and citability under a **no-redistribution** data policy. The evidence is already at the ceiling; the gaps are a DOI and one independent check. The snapshot cannot be a public release asset: the Yahoo and FRED terms do not permit it (DEC-20261106-042).

**State at this update**

- `main` at `3affad1` before the compliance remediation; the remediation commit follows.
- Tests: 246 passed, 1 skipped (the vacuous survivorship test) after the remediation.
- Live carousel: <https://www.linkedin.com/feed/update/urn:li:activity:7524101151596937216/> (posted 2026-11-05).
- Previous post: <https://www.linkedin.com/feed/update/urn:li:activity:7520351295396933632/>.
- Artifacts: paper 10 pages, carousel 8 slides, research brief 2 pages, positioning doc.

---

## Now — this week

- [x] **Stop redistributing third-party data.** Done 2026-11-06.
  - Deleted both snapshot assets from the `v1.0.0` and `v1.1` releases; corrected both bodies.
  - `docs/open_source_and_license_policy.md` → v1.2; `docs/data_licenses.md` created.
  - README, paper, essays, published-run notes, packaging notice, verifier text, external-check request, and CI corrected.
  - Decision: `DEC-20261106-042`.
- [ ] **Put the research brief in the first comment** of the live post, or send it to five specific people.
  - Done when: five sends logged below, or the comment is edited.
  - Do not post it as a new feed item.
- [ ] **Record the carousel's 7-day numbers** on 2026-11-12: impressions, comments, profile views, link clicks.
  - Done when: the numbers are in the log below.
  - Decision rule: fewer than ~500 impressions and no substantive comment means the constraint is distribution, not format.
- [x] **Write `CITATION.cff`** at the repository root. Done 2026-11-06.
  - Version `1.1.0`; matches the `v1.1` tag.
- [x] **Draft the `v1.1` release notes**: the country sample, the correction, the brief. Done: [`docs/release-notes-v1.1.md`](docs/release-notes-v1.1.md).

## Next — weeks 2–4: make it citable

- [x] **Tag `v1.1`.** Done with this commit; pushed with the branch.
- [x] **Create the GitHub release from `v1.1`.** Done 2026-11-06; published and marked latest.
- [ ] **Archive to Zenodo and mint a DOI.**
  - Owner action: Zenodo, link the GitHub repo or upload the archive.
  - Done when: DOI appears in the README, the paper, and the brief.
- [x] **Package the country snapshot locally.** Done: `dist/robustfolio-snapshot-yahoo-countryetf-1998-01-01_2026-09-30-2026-11-05-269a4565.tar.gz` plus `.sha256`; 1.89 MB. **Not published** — retained for local verification only.
- [x] **Withdraw the country snapshot from the release.** Done 2026-11-06: the asset and its checksum were deleted, and the release body now states why. Do not re-upload without written permission.
- [ ] **One-command check, without the data.** A fresh clone runs the hermetic suite and rebuilds the paper from the committed tables.
  - Done when: a reviewer completes the route in [`docs/reviewers-guide.md`](docs/reviewers-guide.md) in under thirty minutes.
- [ ] **Add the DOI to the paper's first page** and rebuild the PDF.
  - Done when: the committed paper shows the DOI.

## Weeks 5–8: the reusable instrument

- [x] **Evaluation checklist** — eight questions any portfolio backtest should answer.
  - One page, public: [`docs/evaluation-checklist.md`](docs/evaluation-checklist.md), linked from the README.
- [x] **Reviewer's guide** — what to check, in what order, and what would falsify each claim: [`docs/reviewers-guide.md`](docs/reviewers-guide.md).
- [ ] **Technical note 1** — the power audit: 0.478 observed / 0.72 true / 24% power at 0.20.
  - Done when: published as a note or a post.
- [ ] **Next LinkedIn post** — the checklist card, not a summary of the same result.
  - Timing: 5–7 days after the carousel, or when its impressions plateau.
  - Hook: "Most backtests are underpowered. Mine was."
  - Done when: posted, with the carousel and paper in the first comment.

## Weeks 9–12: external validation

- [ ] **Two independent checks.**
  - Use [`notes/reproduction_request_2026-11-06.md`](notes/reproduction_request_2026-11-06.md); ask two people to run the hermetic suite and review one claim, or to compare against a snapshot they independently hold.
  - Do **not** send an archive: the project does not distribute it.
  - Done when: two external checks are recorded, and a "Checks" section is in the README.
- [ ] **One venue submission.**
  - See [`notes/venue_and_talk_plan_2026-11-06.md`](notes/venue_and_talk_plan_2026-11-06.md): SSRN first, arXiv if endorsed.
  - Done when: submitted, with the DOI and the replication included.
- [ ] **One talk.**
  - Twelve-minute outline is in the same note.
  - Done when: delivered, slides posted.

## Backlog / optional

- [ ] Do not re-upload a snapshot without a written redistribution permission. Treat this as a standing non-goal, not a task.
- [ ] Update or retire `notes/outreach_package.md` (stale LinkedIn drafts).
- [ ] Personal study guide (outside the repository; not a public artifact).
- [ ] Add a `docs/reproductions.md` page when the first external run lands.

## Blocked on the owner

- Zenodo DOI — account and archive. The archive must contain only redistributable material; do not upload a snapshot with Yahoo/FRED data.
- LinkedIn comment, DMs, and the next post.
- External check asks and the venue submission.

## Non-goals — do not do

- Do not delete or repost the live carousel.
- Do not publish the study guide as a flagship artifact.
- Do not add methods, datasets, or experiments. The evidence is at the ceiling.
- Do not chase impressions or likes.
- Do not claim "first" or "novel" without a literature check.

---

## Log

| Date | Item | Result |
|---|---|---|
| 2026-11-05 | Carousel posted | 8 slides, document post live |
| 2026-11-05 | First comment | Code, paper, notes, previous post |
| 2026-11-06 | Positioning + README front + brief | Committed `3260a0c` |
| 2026-11-06 | Full suite | 246 passed, 1 skipped |
| 2026-11-06 | `CITATION.cff` + release notes | v1.1 prep |
| 2026-11-06 | Country snapshot packaged | 1.89 MB, SHA `d8bf3b43…72ef` |
| 2026-11-06 | Tag `v1.1` | Pushed with the branch |
| 2026-11-06 | Evaluation checklist + reviewer's guide | Published in `docs/` |
| 2026-11-06 | Reproduction request + venue/talk plan | Notes ready |
| 2026-11-06 | v1.1 release + snapshot | Published, asset digest verified — **later withdrawn** |
| 2026-11-06 | Draft + checksum hygiene | Draft removed; checksum attached as `.txt`, content verified |
| 2026-11-06 | **Compliance remediation** | Both snapshot assets deleted from `v1.0.0`/`v1.1`; policy v1.2; `data_licenses.md`; notices and all public reproduction claims corrected. `DEC-20261106-042` |
| 2026-11-06 | Post-remediation suite | 246 passed, 1 skipped; archive verification `EXACT`, `M1 FAILURE / M2 FAILURE` |
| 2026-11-12 | Carousel 7-day numbers | Pending |
