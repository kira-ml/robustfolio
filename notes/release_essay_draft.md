# Release essay — working draft (not a Tier 0 document)

**Status:** skeleton. Working input, not a contract. **F26 and E7 are both closed** (DEC-20261017-034); the remaining gate before publication is the release itself, plus E3.
**Baseline for v1.0.0:** the release packaging chain (DEC-20261017-032) and the first end-to-end run
(`EXP-X-20261017-003`), both exploratory.

---

## 1. The shape of the piece

**Lead with the method. Illustrate with the domain. Back it with the toolkit.**

The finance result is a clean null on an unusually well-defended experiment. That is a *good*
worked example and a *bad* headline: "robust portfolio methods don't beat sample MVO on ETFs" is
interesting to perhaps a few thousand people and reads as a negative result to everyone else. The
transferable claim is the one that survives outside finance:

> I ran a pre-registered experiment, and I spent most of the effort trying to break my own result
> before believing it. Here are the four defences that worked, the one that failed, and the
> numbers that came out.

That claim is checkable by the reader — the repository ships the checker — which is the whole point.

### Title options (avoid "portfolio" and "backtest" in the flagship)

1. **"I tried to break my own result before I published it"** — plain, first-person, describes the
   method rather than the domain.
2. **"Pre-registration is not enough: four defences against fooling yourself"** — declares the
   payload up front; slightly more seminar-ish.
3. **"The verification you haven't verified"** — the thesis in five words, derived from F27/F28.
4. **"An honest null, and the machinery that makes it honest"** — closest to what actually happened;
   risks reading as a negative result.

*Recommendation:* 1 for the flagship, 3 for the technical cross-post. 1 leads with the process and
lets the null arrive as evidence, which is the right order.

---

## 2. Verified numbers the piece may cite

Everything here is checked against `README.md` / `outcomes.csv` / the decision log. **Do not
re-derive any of these while writing; copy them.**

| Claim | Value | Source |
|---|---|---|
| Out-of-sample months / folds / solves | 168 / 14 / 1,176 | `report.meta`, `certify_engine.py` |
| Worst engine certificate residual | `1.49e-11` vs `1e-7` acceptance | `certify_engine.py` |
| Best baseline (`B3`) net Sharpe @10 bps | 0.7896, 90% CI [0.331, 1.318] | `outcomes.csv` |
| `M2` (the strongest candidate) | 0.8538, 90% CI [0.426, 1.369] | `outcomes.csv` |
| `M2` advantage over `B3` | +0.064, bar 0.20 (§6.2) | `decisions.csv` |
| `M2` PSR against `B3` | 0.587, bar 0.95 (§6.1) | `decisions.csv` |
| DSR p-values (`M1`, `M2`) vs **zero** | 0.0032, 0.0017 | `outcomes.csv` |
| Correlation with best baseline | ρ = 0.9845 (`M1`), 0.9856 (`M2`) | `design.csv` |
| Paired differences | +0.4% and +0.6% per year | `design.csv` |
| Snapshot archive | 1.67 MB, SHA-256 `7a3fc209…` | `pack_snapshot.py` |
| Reproduction check | `EXACT`, max abs diff `0.000e+00`, 18 columns | `verify_release.py` |
| CI | regenerates **and** verifies bit-for-bit against `docs/published-run/outcomes.csv`, pinned to the archive digest | `ci.yml` |
| Suite | 159 passed, 1 skipped | `pytest -q` |

### Claims this piece may **not** make (protocol §14.2)

- No absolute return, no "beats the market", no investable framing. Cumulative net excess return is
  a metric's input path, not a return stream.
- No gross Sharpe as a headline; it is labelled diagnostic in the artefacts and must stay that way.
- No in-sample numbers presented as evidence.
- No p-value without its benchmark. The DSR/PSR contrast **is** the finding; quoting one alone
  inverts it.
- No superiority claim without the interval.
- No single-cost-level claim. Costs are swept; 10 bps is the headline, not the only level.
- **The word "confirmatory" appears only inside the F26 disclosure.** F26 is resolved by
  re-designation (DEC-20261017-034): the registered confirmatory test's answer was observed before it
  ran, so it is **executed (non-confirmatory)** and **no confirmatory test now exists**. The public
  description is **"pre-registered, mechanically evaluated, non-confirmatory"**, and the hypotheses
  are **untested, not falsified** — the frozen rule returns failure for both candidates either way,
  but it was never applied blind, and this piece will not call it a test.

---

## 3. Section plan

| § | Section | Words | Job |
|---|---|---|---|
| 1 | The hook: my own validation step destroyed my confirmatory test | 250 | Earn attention with a specific, embarrassing, true story. |
| 2 | What I was actually testing | 300 | Frame the question and the pre-registered rule. Enough for a quant reader, skimmable for everyone else. |
| 3 | Defence 1 — freeze before looking | 300 | Pre-registration as a mechanism, not a virtue. Include the rule that was frozen and what it forbade. |
| 4 | Defence 2 — prove no leakage mechanically | 350 | The leakage suite, and why "we reviewed the code" is not a defence. |
| 5 | Defence 3 — certify the numerics | 400 | F19 (memory layout / ULP), F20 (the certificate rejected 7 provably optimal solutions), F23 (the certification script was certifying a different problem). The strongest section. |
| 6 | Defence 4 — significance **and** materiality **and** robustness | 300 | The sixteen-comparison conjunction, and the DSR-passes/PSR-fails demonstration. |
| 7 | The defence that failed: F26 | 350 | The honest centrepiece. A lobe of the design (independent validation of the report generator) was in direct tension with another lobe (blindness of the confirmatory test). I chose validation, and I'm saying so. |
| 8 | The result | 250 | The null, with intervals. Frame as: the effect is absent, not invisible (ρ ≈ 0.985, power shown). Plus the diagnostic that explains it (effective bets ≈ 3–5 of 18; 12 of 18 eigenvalues below the MP edge). |
| 9 | What a reader can do with this | 200 | The four defences as a checklist; the check-me command; "use it on your own panel". |
| — | What I'd do differently | 150 | Includes: run the report generator on a *different* snapshot to preserve Test D's blindness. |

**Total ≈ 2,850 words.** Trim §2 and §8 in the draft pass.

---

## 4. The two derivative cuts

### Cut A — quant / systematic investing (~1,200 words)

Domain-specific, assumes the reader knows what an MVO is. Keep §2, §5, §6, §8; compress §1 to two
sentences; drop §9. Add:

- The **benchmark-choice** point: with `N = 1` the deflation is inert, so `DSR = PSR` against zero.
  The binding constraint is *which* benchmark, not the multiple-testing correction. Pre-registration
  substitutes for multiple-testing correction when you fire exactly once.
- The **diagnostic hypothesis** (label it as a hypothesis, not a result): with effective bets ≈ 3 and
  `cond(Σ̂) ≈ 1.7e3`, shrinkage has little to bite on and a uniform 30% cap is a *stronger*
  regulariser than the estimator. What would test it: relax the cap and compare shrinkage across cap
  levels. Do not state it as established — state it as what the diagnostics suggest and what would
  falsify it. This connects to the abandoned Test B (cap sweep) and is the single most interesting
  technical thread in the project.
- The **turnover** observation: `B3` carries 2.12 annualised turnover and still wins on net Sharpe at
  the headline cost, which is the opposite of the motivating story.

### Cut B — ML / data science (~1,200 words)

Strip the finance entirely. Keep §1, §3, §4, §5, §6, §9. Translate:

- "portfolio" → "model", "asset" → "feature", "rebalance" → "refit", "net Sharpe" → "held-out metric".
- The four defences, stated generically: (1) freeze before looking; (2) prove the absence of leakage
  mechanically, not by inspection; (3) certify the numerics so a solver or library failure cannot
  masquerade as a result; (4) require significance **and** materiality **and** robustness together,
  because each alone is a Goodhart target.
- F19's lesson generalised: **your results depended on memory layout.** A library's reduction over a
  non-contiguous frame gave ULP-different answers, which in a leakage test is indistinguishable from
  actual leakage. The fix is a contiguity guarantee, and the test that pins it is the valuable
  artefact.
- F27/F28 as the sharpest stories for this audience: both bugs were in *my verifier*, both produced
  plausible numbers, and one of them was a library default (`pd.read_csv`) lying by one ULP.

---

## 5. Distribution (after v1.0.0 is cut)

1. **Direct outreach first, 10–20 named people.** Ask for critique of a specific section, not for a
   job and not for a share. Expected conversion is 10–50× public posting; the point is substantive
   conversation, not reach.
2. **Public posts second:** the flagship on a platform that renders links, the two cuts as separate
   posts on their own merits rather than as "a summary of my essay".
3. **The metric to watch is not stars, likes or impressions.** It is: *did at least one person whose
   work I respect engage substantively?* Any other number is a Goodhart target in a project whose
   entire thesis is that Goodhart targets are how honest work decays.
4. **Lead with the check-me command.** The one-line invitation should be "clone it and run
   `verify_release.py`; if it prints anything other than `EXACT`, tell me" — that is a claim nobody
   else in the conversation is making, and it puts the falsification burden on the artefact.

---

## 6. Open items before anything is published

- [x] **F26 closed** — re-designated **executed (non-confirmatory)**, no replacement test registered (DEC-20261017-034).
- [x] **E7** — `docs/open_source_and_license_policy.md` v1.0 **Frozen**; the archive carries its own `NOTICE.txt` (DEC-20261017-035).
- [ ] **E3** — `docs/results_reporting_and_claims_policy.md`, "must be written before Phase 4"; governs what may be claimed. Not a hard gate — protocol §14.2 already governs the claims — but the natural single home for the rules these pieces cite.
- [ ] Snapshot uploaded as a release asset and the digest quoted in the release notes.
- [ ] Tag `v1.0.0`, cut the Release.
- [ ] Re-read every public artefact against §14.2 **after** the release exists, since the release notes are themselves an artefact.
