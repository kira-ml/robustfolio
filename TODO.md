# TODO

**Updated:** 2026-11-06
**Status:** Working checklist. Not a governance document, not a contract.
**Authority:** decisions live in [`docs/decision_log.md`](docs/decision_log.md). The old `TODO.md` was retired into its Appendix B; this file is the execution view of the current plan, not a revival of that ledger.

**Current constraint:** external validation and citability, not content. The evidence is already at the ceiling; the gaps are a DOI, a released snapshot, and one independent reproduction.

**State at this update**

- `main` at `3260a0c`, clean and synced.
- Tests: 246 passed, 1 skipped (the vacuous survivorship test).
- Live carousel: <https://www.linkedin.com/feed/update/urn:li:activity:7524101151596937216/> (posted 2026-11-05).
- Previous post: <https://www.linkedin.com/feed/update/urn:li:activity:7520351295396933632/>.
- Artifacts: paper 10 pages, carousel 8 slides, research brief 2 pages, positioning doc.

---

## Now — this week

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
- [x] **Package the country snapshot.** Done: `dist/robustfolio-snapshot-yahoo-countryetf-1998-01-01_2026-09-30-2026-11-05-269a4565.tar.gz` plus `.sha256`; 1.89 MB; SHA `d8bf3b43…72ef`.
- [x] **Attach the country snapshot to the release.** Done 2026-11-06; GitHub reports the asset at 1,980,519 bytes with digest `sha256:d8bf3b43…72ef`.
- [ ] **One-command reproduction** and CI badge.
  - Done when: a fresh clone reproduces one published table in under ten minutes.
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

- [ ] **Two independent reproductions.**
  - Use [`notes/reproduction_request_2026-11-06.md`](notes/reproduction_request_2026-11-06.md); ask two people to run one table.
  - Done when: two external runs are recorded, and a "Reproductions" section is in the README.
- [ ] **One venue submission.**
  - See [`notes/venue_and_talk_plan_2026-11-06.md`](notes/venue_and_talk_plan_2026-11-06.md): SSRN first, arXiv if endorsed.
  - Done when: submitted, with the DOI and the replication included.
- [ ] **One talk.**
  - Twelve-minute outline is in the same note.
  - Done when: delivered, slides posted.

## Backlog / optional

- [ ] Pack the country snapshot if the release route is chosen later.
- [ ] Update or retire `notes/outreach_package.md` (stale LinkedIn drafts).
- [ ] Personal study guide (outside the repository; not a public artifact).
- [ ] Add a `docs/reproductions.md` page when the first external run lands.

## Blocked on the owner

- GitHub release and assets — web UI, not the CLI.
- Zenodo DOI — account and archive.
- LinkedIn comment, DMs, and the next post.
- External reproduction asks and the venue submission.

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
| 2026-11-12 | Carousel 7-day numbers | Pending |
