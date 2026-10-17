# robustfolio

> A reproducible, open-source benchmark for turnover-aware, robust portfolio rebalancing — with honest net-of-cost out-of-sample results and documented negative findings.

**Status:** Phase 0 — Problem Validation, closing. The Tier 0 documentation set is consolidated to six files and the evaluation protocol is pending freeze. An exploratory Phase 1 smoke test exists and is explicitly non-confirmatory (DEC-20261015-012).

[![Phase](https://img.shields.io/badge/phase-0%20problem%20validation-blue)]()
[![License](https://img.shields.io/badge/license-MIT-green)](LICENSE)
[![Status](https://img.shields.io/badge/status-pre--alpha-lightgrey)]()

---

## What This Is

`robustfolio` investigates a specific, practical problem in systematic investing:

> Portfolio construction methods that rely on historical estimates of expected returns and covariance are highly sensitive to estimation error. Under realistic transaction costs, this sensitivity produces unstable weights, excessive turnover, and degraded net-of-cost out-of-sample performance.

The project builds a **reproducible benchmark** that:

- Compares robust, turnover-aware portfolio construction methods against strong, simple baselines.
- Evaluates everything **net of transaction costs** and **out-of-sample**, using walk-forward validation.
- Adjusts for **multiple testing** using deflated Sharpe and probabilistic Sharpe.
- Reports **negative results** with the same rigor as positive ones.

The project's primary objective is falsifiable:

> Determine whether any robust, turnover-aware method delivers materially better net-of-cost out-of-sample risk-adjusted return than simple baselines, after adjusting for multiple testing.

A clean negative result — a well-documented "no, it doesn't" — is a **successful outcome** by this project's definition. Inflated positive results are not.

---

## Why It Matters

Most portfolio optimization libraries optimize in-sample or ignore costs entirely. Many student and research projects report gross Sharpe ratios without realistic cost assumptions. Practitioners need transparent, reproducible benchmarks to compare methods.

The base rates are sobering:

- A large fraction of published factor and portfolio strategies fail out-of-sample after costs.
- Simple equal-weight (1/N) often outperforms complex optimization out-of-sample.
- Robustness, not sophistication, is usually the binding constraint.

This project treats those findings as **priors to be tested**, not as universal laws.

---

## What This Project Is NOT

Explicitly out of scope. Reading this list is itself a project survival mechanism.

- Not a high-frequency or intraday trading system.
- Not an options, futures, or derivatives toolkit.
- Not a live trading or execution engine.
- Not a proprietary alpha research platform.
- Not a general-purpose backtesting framework for all asset classes.
- Not a commercial portfolio optimizer.
- Not a market-timing or wealth-management tool.
- Not a place to make absolute return claims.

If the benchmark is useful, those are separate projects built on top of it — not part of it.

---

## Current Status

**Phase 0 — Problem Validation.**

The Tier 0 documentation set has been consolidated from twelve files to six (DEC-20261015-017, DEC-20261015-018). The evaluation protocol is drafted and **pending freeze**; the freeze is the binding constraint on Phase 1.

An **exploratory Phase 1 smoke test** ran on 2026-10-15. It exercised the walk-forward harness end to end, but it was not pre-registered and is **non-confirmatory** (DEC-20261015-012). Its numbers may be used to scope diagnostics only; they may not be cited for or against any hypothesis.

| Artifact | Status |
|----------|--------|
| Tier 0 documentation set (6 files) | Consolidated; protocol pending freeze |
| Exploratory walk-forward harness | Exists (non-confirmatory) |
| Data ingestion pipeline (point-in-time) | Not started — harness uses adjusted Yahoo data |
| MVP baselines (B1–B5) | Partial — B1, B3, B5 only; B2 and B4 missing |
| Robust method implementations | Not started |
| Evaluation metrics (DSR, PSR, CVaR, CIs) | Not started |
| Public release | Not started |

The next milestone is **freezing `docs/evaluation_protocol.md`**, the gated entry to Phase 1: Data and Baselines.

---

## Documentation

All project contracts, protocols, and decision records live in [`docs/`](docs/). The active set is six files:

- [`docs/README.md`](docs/README.md) — Documentation index and status board
- [`docs/problem_framing.md`](docs/problem_framing.md) — The real problem, stakeholders, causal model
- [`docs/scope_and_non_goals.md`](docs/scope_and_non_goals.md) — What is and is not in scope
- [`docs/evaluation_protocol.md`](docs/evaluation_protocol.md) — Metrics, baselines, data contract, cost model, registry rules, governance
- [`docs/risk_register_and_premortem.md`](docs/risk_register_and_premortem.md) — Failure modes and pre-mortem
- [`docs/decision_log.md`](docs/decision_log.md) — Why the project is the way it is (and the experiment registry, Appendix A)

Working inputs that are **not** contracts live in [`notes/`](notes/).

The docs are versioned. Frozen documents may not be modified after seeing experimental results without a decision log entry and a version bump.

---

## Operating Principles

These principles govern every decision in the project. They are not marketing — they are enforcement mechanisms.

1. **Falsification before optimization.** Every claim must have a test that could prove it wrong.
2. **Point-in-time or nothing.** No lookahead, no survivorship bias, no retroactive adjustments.
3. **Net of cost, out of sample, multiple-testing aware.** Gross, in-sample, and unadjusted numbers are diagnostic only.
4. **Pre-register before running.** Every experiment is registered with its hypothesis and decision rule before execution.
5. **Negative results are first-class.** A clean "no" is a successful outcome.
6. **Kill decisions are free.** Continuing past the evidence is the actual failure mode.
7. **Narrow by default.** Scope grows only by amendment, never by drift.

If these read like constraints rather than values, that is deliberate. They exist because the alternative has been tried many times and usually fails.

---

## Roadmap (Phase Gates)

The project proceeds through gated phases. Each gate is a go/no-go decision. A phase cannot begin until the previous gate is passed.

| Phase | Name | Entry criteria | Exit criteria |
|-------|------|----------------|---------------|
| 0 | Problem Validation | Charter active | Literature and tool scan complete; Tier 0 contracts drafted |
| 1 | Data & Baselines | Contracts frozen | Data pipeline works; baselines reproduce; MVO instability confirmed |
| 2 | Robust Methods | Gate 1 passed | Robust methods implemented and unit-tested; no leakage |
| 3 | Evaluation | Gate 2 passed | Walk-forward results with multiple-testing adjustment |
| 4 | Reporting & Release | Gate 3 passed | Reproducible report; honest conclusion; public release |
| 5 | Extensions (optional) | Gate 4 passed and justified | Scoped, pre-registered extension |

A gate may be passed with a documented **negative** result. It may not be passed by relaxing the evaluation protocol after seeing results.

---

## Repository Structure

```
robustfolio/
├── README.md                       ← you are here
├── LICENSE                         ← MIT
├── pyproject.toml                  ← package metadata
├── requirements.txt                ← Phase 1 dependencies (unpinned)
├── docs/                           ← the 6-file contract set
│   ├── README.md                   ← documentation index and status board
│   ├── problem_framing.md
│   ├── scope_and_non_goals.md
│   ├── evaluation_protocol.md
│   ├── risk_register_and_premortem.md
│   └── decision_log.md
├── notes/                          ← non-contract working inputs (freeze inputs, DSR inputs)
├── src/robustfolio/                ← exploratory walk-forward implementation
├── scripts/                        ← Phase 1 experiment and diagnostics
├── data/                           ← local cache and (planned) snapshots — git-ignored
└── results/                        ← experiment outputs
```

`tests/` (unit, integration, leakage) does not exist yet; it is required by the Phase 1 gate and will be added before any confirmatory experiment.

---

## Getting Started

**There is nothing to install yet.** The project is in Phase 0; the Python package in `src/robustfolio/` is an exploratory harness, not a released tool.

Read the documentation in this order:

1. [`docs/problem_framing.md`](docs/problem_framing.md) — what problem is being solved
2. [`docs/scope_and_non_goals.md`](docs/scope_and_non_goals.md) — what is and is not in scope
3. [`docs/evaluation_protocol.md`](docs/evaluation_protocol.md) — how success is measured and what would falsify it
4. [`docs/risk_register_and_premortem.md`](docs/risk_register_and_premortem.md) — how the project fails

If you want to contribute to the documentation phase, open an issue.

---

## Contributing

Contribution guidelines will be added in `docs/open_source_and_license_policy.md` before Phase 4.

For now:

- **Issues are welcome** for factual errors, unclear documentation, or questions about the problem framing.
- **Pull requests to frozen documents** require a decision log entry explaining why the change is not goalpost-moving.
- **Pull requests to draft documents** are welcome but should reference the relevant decision log entry or issue.
- **Contributions that add scope** (new asset classes, new methods, new frequencies) require a charter amendment; they will not be accepted as drive-by PRs.

The project's discipline is intentional. Contributions that weaken it will be declined with a rationale, not silently.

---

## License

MIT. See [`LICENSE`](LICENSE).

---

## Citation

A citation will be provided once a public release exists. Until then, please link to this repository.

---

## Why "robustfolio"

*Robust* because the binding constraint in practice is usually not sophistication but robustness to estimation error, non-stationarity, and frictions. *Folio* because the object of study is the portfolio, not the signal.

The name is a reminder of what the project is actually about.

---

*This README is the front door. The real project lives in [`docs/`](docs/). If this README and the docs ever disagree, the docs win.*
