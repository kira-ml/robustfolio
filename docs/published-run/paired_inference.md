# Paired inference - exploratory

**Status:** EXPLORATORY - same data, post-hoc reading; not a confirmatory test  
**Sample:** 168 months; paired stationary bootstrap, 2000 reps, mean block 6, seed 20261017  
**Materiality bar:** 0.20 annualised net Sharpe  
**Comparator:** `B3` (0.7896); next is `B5` at 0.7843, a margin of 0.0053.

| Method | delta SR | 90% paired CI | P(delta>0) | one-sided p | P(delta>bar) | equivalence | registered PSR | gate requires | gate power @ bar |
|---|---:|---:|---:|---:|---:|---|---:|---:|---:|
| `M1` | -0.0036 | [-0.0964, +0.0800] | 0.487 | 0.512 | 0.000 | **NOT_MATERIAL** | 0.495 | 0.474 | 0.190 |
| `M2` | +0.0642 | [-0.0113, +0.1467] | 0.917 | 0.083 | 0.004 | **NOT_MATERIAL** | 0.587 | 0.478 | 0.241 |

`equivalence` reads the 90% paired interval against the bar: `NOT_MATERIAL` means the whole interval is below the bar, so a materially large advantage is excluded at the 5% one-sided level; `MATERIAL` means it is above; `INCONCLUSIVE` means it straddles. This is a three-way reading, not a replacement for the frozen verdict.

The `registered PSR` column is the §6.1 gate as written: a **level** test of the candidate against the baseline's observed Sharpe. `gate requires` is the gap at which that gate would fire; `gate power @ bar` is the simulated chance it fires when the true gap equals the materiality bar. The paired columns use the same months and preserve their common variation.
