# robustfolio

**Does a robust, turnover-aware portfolio construction method beat a plain one out-of-sample, net of transaction costs — once you adjust for having tried more than one?**

This repository is the benchmark that answers that question under a pre-registered, frozen evaluation protocol. It is built to produce an *honest* answer rather than a favourable one: the hypothesis, the metrics, the thresholds, and the decision rule were all fixed and dated before the results were computed, and a clean "no" is a successful outcome here.

[![protocol](https://img.shields.io/badge/protocol-v2.4%20frozen-blue)](docs/evaluation_protocol.md)
[![spec](https://img.shields.io/badge/spec-v1.1%20frozen-blue)](docs/model_and_method_spec.md)
[![license](https://img.shields.io/badge/license-MIT-green)](LICENSE)

---

## Result

> **Exploratory, non-confirmatory** (DEC-20261015-012). These numbers may not be cited for or against any hypothesis. The registered confirmatory test (`EXP-H2-20261017-001`) has not been executed; see [Limitations](#limitations) and findings F24–F26.

**Neither robust method was successful under the frozen decision rule.** Over 168 out-of-sample months on a point-in-time universe of 18 US ETFs, the best baseline was `B3` — plain sample-covariance, sample-mean MVO, the method the project set out to critique.

| Method | Net Sharpe @ 10 bps | 90% bootstrap CI | Gross (diagnostic only) |
|---|---|---|---|
| `B1` equal weight (1/N) | 0.5482 | [0.153, 1.002] | 0.5527 |
| `B2` risk parity (ERC) | 0.4519 | [0.017, 0.974] | 0.4592 |
| **`B3` sample MVO — best baseline** | **0.7896** | [0.331, 1.318] | 0.8151 |
| `B4` minimum variance | 0.1820 | [-0.253, 0.751] | 0.1953 |
| `B5` turnover-penalised MVO | 0.7843 | [0.316, 1.316] | 0.7926 |
| `M1` shrinkage-covariance MVO | 0.7860 | [0.327, 1.298] | 0.8077 |
| `M2` Bayesian (Black–Litterman) MVO | **0.8538** | [0.426, 1.369] | 0.8791 |

Net Sharpe is the **only** metric allowed to decide whether a method beats a baseline (protocol §2). `M2`'s advantage over `B3` is **+0.064** against a materiality bar of **0.20** (§6.2), and its probabilistic Sharpe ratio against `B3` is **0.587** against a bar of **0.95** (§6.1). Both candidates therefore return **FAILURE** under §6.4 — `M1` at −0.004 and `M2` at +0.064.

The part worth reading closely: both candidates *pass* the deflated Sharpe p-value (0.0032 and 0.0017), because the DSR is measured against a **zero** benchmark. They fail the PSR, because that is measured against the **best baseline**. §6.1 requires both, and the first run is a live demonstration of why.

**This is not an underpowered null.** The candidates' return series correlate with the best baseline at ρ = 0.9845 and 0.9856, which is inside the region where the design diagnostic found the paired comparison adequately powered for the §6.2 threshold. The paired differences are +0.4% and +0.6% a year. The effect is absent, not invisible.

The deliverable is the **apparatus**, not the number: a leakage-tested walk-forward engine, a numerical certificate, a pre-registered decision rule, and a report that prints the comparison it failed on.

---

## Reproduce it

```bash
git clone https://github.com/kira-ml/robustfolio.git && cd robustfolio
python -m pip install -e .

# 1. Build an immutable point-in-time snapshot from the tracked universe definition.
#    Downloads daily prices + corporate actions from Yahoo Finance and freezes them.
python scripts/build_snapshot.py --end 2026-09-30 --retrieval-date 2026-10-17

# 2. Regenerate the headline number and every table behind it.
python scripts/run_experiment.py --out results/run       # defaults to the newest snapshot on disk

# 3. Verify the engine and the leakage discipline independently.
python scripts/certify_engine.py                          # 7 methods x 168 rebalances, KKT certificate
python -m pytest -q                                       # 134 passed, 1 skipped
```

Step 2 writes `manifest.json` (snapshot id, git commit, protocol and spec versions, seed, environment), `outcomes.csv`, `decisions.csv`, `calibration.csv`, `design.csv`, `folds_<M>.csv`, and `report.md`.

Yahoo Finance revises history. The snapshot is immutable once built and every snapshot is identified by a content hash, so a rebuild with a different retrieval date is a **different** snapshot and may produce slightly different numbers. The frozen snapshot behind the table above is `yahoo-usetf-2007-01-01_2026-09-30-2026-10-17-2ad06139`.

---

## What is built

| Component | State |
|---|---|
| Evaluation protocol | **Frozen** v2.4 — metrics, thresholds, hypotheses, registry rules, firewalls |
| Method spec | **Frozen** v1.1 — estimators, optimizer, harness, metric definitions |
| Universe | 18 US ETF candidates, point-in-time eligibility (17–18 eligible at each rebalance), anchored 2012-06 |
| Methods | 5 baselines (`B1`–`B5`) + 2 robust treatments (`M1`, `M2`), differing in exactly one component from `B3` |
| Walk-forward harness | 60-month rolling estimation, 12-month non-overlapping test blocks, monthly rebalance, 168 OOS months / 14 folds |
| Optimizer | CVXPY + CLARABEL, **no fallback path**, every rebalance certified by a primal KKT residual against a frozen tolerance |
| Engine certificate | 7 methods × 168 rebalances = **1,176 solves, zero rejections**; worst KKT residual `1.49e-11` vs `1e-7` acceptance |
| Leakage suite | protocol §5.4.8 — 14 pass, 1 recorded skip (the survivorship test is vacuous in-sample; see below) |
| Tests | 134 passed, 1 skipped |

---

## Limitations

These are the honest ones, not a disclaimer. The full list is in the report and in [`docs/decision_log.md`](docs/decision_log.md).

- **The headline run is exploratory.** It is not pre-registered as confirmatory and cannot be cited for or against any hypothesis (DEC-20261015-012). Worse, validating the report generator required executing the frozen configuration, so the registered confirmatory test's answer has already been observed — **it would now be a reproduction, not a blind test** (finding F26).
- **168 out-of-sample months and 18 ETF candidates** (17–18 eligible at any rebalance). This sample can separate roughly a 0.13–0.20 net Sharpe difference between these highly correlated strategies, and not much less.
- **The cost model is a flat 10 bps with no market impact, capacity, taxes, or regime dependence.** Costs cannot reach the optimizer: each rebalance is solved once and every cost level is derived from that single turnover series, so a cost level cannot influence the weights it prices.
- **Survivorship is argued by construction, not measured.** The survivorship test (§5.4.8 test 2) is vacuous in-sample: no confirmed candidate delisted between 2012-06 and 2026-05 (§5.4.5).
- **Data provenance is Yahoo Finance**, frozen into an immutable snapshot with a quality report. It is not an institutional point-in-time vendor feed.
- **Two specification readings are disclosed, not silent.** §7.8 leaves the object of its prediction interval undefined, so only the *return* half is reported (coverage 81.5–87.0%); the volatility half is deliberately **not** implemented. §6.3's "advantage" is not pinned to a metric, so fold wins use net Sharpe and the concentration clause uses per-fold mean return — **and that reading decides the verdict here** (findings F24, F25).
- **Not investment advice, and not a claim of tradable alpha.** Nothing here is a live trading system, and no absolute return claim is made (protocol §14.2).

---

## Documentation

The contracts live in [`docs/`](docs/) and are the authority: **if this README and the docs disagree, the docs win.**

- [`docs/evaluation_protocol.md`](docs/evaluation_protocol.md) — frozen metrics, thresholds, hypotheses, registry and firewalls
- [`docs/model_and_method_spec.md`](docs/model_and_method_spec.md) — frozen method, estimator, optimizer and metric definitions
- [`docs/problem_framing.md`](docs/problem_framing.md) · [`docs/scope_and_non_goals.md`](docs/scope_and_non_goals.md)
- [`docs/risk_register_and_premortem.md`](docs/risk_register_and_premortem.md) — how this project fails
- [`docs/decision_log.md`](docs/decision_log.md) — every governance decision, the experiment registry, and findings F1–F26

---

## License

MIT. See [`LICENSE`](LICENSE).

*Robust*, because the binding constraint in practice is rarely sophistication and usually robustness to estimation error, non-stationarity, and frictions. *Folio*, because the object of study is the portfolio, not the signal.
