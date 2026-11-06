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
- [ ] **Write `CITATION.cff`** at the repository root.
  - Done when: valid file, author and title match the paper, README links it.
- [ ] **Draft the `v1.1` release notes**: the country sample, the correction, the brief.
  - Done when: notes are ready to paste into the GitHub release UI.

## Next — weeks 2–4: make it citable

- [ ] **Tag `v1.1` and create the GitHub release.**
  - Owner action: GitHub web UI (`gh` CLI is not installed).
  - Done when: release exists with the notes.
- [ ] **Archive to Zenodo and mint a DOI.**
  - Owner action: Zenodo, link the GitHub repo or upload the archive.
  - Done when: DOI appears in the README, the paper, and the brief.
- [ ] **Release the country snapshot** (or a derived package if the licence prevents redistribution).
  - Use `scripts/pack_snapshot.py`; attach the `.sha256`; keep the NOTICE.
  - Done when: the asset is on the release and the reproduction note is updated.
  - Why: the most interesting result is currently the least reproducible.
- [ ] **One-command reproduction** and CI badge.
  - Done when: a fresh clone reproduces one published table in under ten minutes.
- [ ] **Add the DOI to the paper's first page** and rebuild the PDF.
  - Done when: the committed paper shows the DOI.

## Weeks 5–8: the reusable instrument

- [ ] **Evaluation checklist** — six questions any portfolio backtest should answer.
  - One page, public, linked from the README.
  - Done when: it exists and someone outside the project has used it.
- [ ] **Reviewer's guide** — what to check, in what order, and what would falsify each claim.
- [ ] **Technical note 1** — the power audit: 0.478 observed / 0.72 true / 24% power at 0.20.
  - Done when: published as a note or a post.
- [ ] **Next LinkedIn post** — the checklist card, not a summary of the same result.
  - Timing: 5–7 days after the carousel, or when its impressions plateau.
  - Hook: "Most backtests are underpowered. Mine was."
  - Done when: posted, with the carousel and paper in the first comment.

## Weeks 9–12: external validation

- [ ] **Two independent reproductions.**
  - Ask two practitioners or researchers to run one published table; record the result in an issue or a PR.
  - Done when: two external runs are recorded, and a "Reproductions" section is in the README.
- [ ] **One venue submission.**
  - SSRN, arXiv q-fin, or a workshop.
  - Done when: submitted, with the DOI and the replication included.
- [ ] **One talk.**
  - University seminar or local quant meetup.
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
| 2026-11-12 | Carousel 7-day numbers | Pending |
