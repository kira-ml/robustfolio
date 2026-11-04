"""Paired inference for the robustfolio run (exploratory, 2026-11-04).

The registered §6.1 significance gate is a *level* probabilistic Sharpe ratio
(PSR): the candidate's Sharpe against the best baseline's observed Sharpe. It
ignores the fact that the two return series are almost the same portfolio, so it
throws away most of the comparison's power. This script computes the paired
alternative on the same run, without changing anything the frozen protocol
decided:

* paired annualised Sharpe difference and its stationary-bootstrap interval,
* P(delta > 0) and a one-sided p-value,
* an equivalence decision against the materiality bar,
* the registered PSR gate's own required delta / power, and
* the DSR p-value at family sizes 1, 2 and 7.

It writes ``paired_inference.json`` and ``paired_inference.md`` beside the run.
The frozen verdict is not recomputed and is not changed: this is a reading of
the same evidence through the test the design diagnostic said would decide
H2.4, and it is labelled exploratory because the data have already been seen.

    python scripts/paired_inference.py --run results/<run>

The run directory must contain ``net_excess_returns.csv`` (the primary metric's
input, one column per method) and ``outcomes.csv`` / ``decisions.csv`` (the
published tables). Create one with ``scripts/run_experiment.py``.
"""

from __future__ import annotations

import argparse
import json
import math
import sys
from dataclasses import asdict, dataclass
from pathlib import Path

import numpy as np
import pandas as pd
from scipy import stats as sps

REPO_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO_ROOT / "src"))

from robustfolio import stats  # noqa: E402
from robustfolio.config import (  # noqa: E402
    BOOTSTRAP_BLOCK_MEAN,
    BOOTSTRAP_REPS,
    MATERIALITY_SHARPE_GAP,
    SEED,
)

PERIODS_PER_YEAR = 12
PSR_BAR = 0.95


# --------------------------------------------------------------------------- #
# The paired statistic
# --------------------------------------------------------------------------- #

def annualized_sharpe(values: np.ndarray) -> float:
    """Annualised Sharpe of a monthly excess-return vector (no rf: already excess)."""
    values = np.asarray(values, dtype=float)
    if values.size < 2:
        return float("nan")
    sd = float(values.std(ddof=1))
    if sd == 0.0 or not np.isfinite(sd):
        return float("nan")
    return float(values.mean() / sd * math.sqrt(PERIODS_PER_YEAR))


@dataclass(frozen=True)
class PairedResult:
    """One candidate-versus-baseline paired comparison."""

    method: str
    baseline: str
    n: int
    rho: float
    candidate_net_sharpe: float
    baseline_net_sharpe: float
    point_delta_sr: float
    ci90_low: float
    ci90_high: float
    ci95_low: float
    ci95_high: float
    p_positive: float
    p_one_sided: float
    p_exceeds_bar: float
    equivalence: str
    psr_registered: float
    psr_required_delta: float
    psr_mde_80: float
    psr_power_at_bar: float
    psr_power_at_bar_simulated: float
    dsr_p: dict[str, float]
    fold_min_delta: float
    fold_max_delta: float
    folds_positive: int
    folds_total: int


def _paired_draws(
    candidate: np.ndarray,
    baseline: np.ndarray,
    *,
    reps: int,
    mean_block: float,
    seed: int,
) -> np.ndarray:
    """Paired stationary-bootstrap draws of the annualised Sharpe difference.

    Both series are resampled with the *same* positional indices, which is the
    whole point: the comparison keeps the common variation and removes it from
    the standard error. Resampling each series independently would answer a
    different question and would be far less powerful.
    """
    n = len(candidate)
    if len(baseline) != n:
        raise ValueError("candidate and baseline must have the same length")
    indices = stats.stationary_bootstrap_indices(
        n, mean_block=mean_block, reps=reps, seed=seed
    )
    c = np.asarray(candidate, dtype=float)[indices]
    b = np.asarray(baseline, dtype=float)[indices]
    with np.errstate(invalid="ignore", divide="ignore"):
        sr_c = c.mean(axis=1) / c.std(axis=1, ddof=1) * math.sqrt(PERIODS_PER_YEAR)
        sr_b = b.mean(axis=1) / b.std(axis=1, ddof=1) * math.sqrt(PERIODS_PER_YEAR)
    return sr_c - sr_b


@dataclass(frozen=True)
class PairedDelta:
    """A compact paired comparison for a caller that only needs the interval."""

    point: float
    ci_low: float
    ci_high: float
    p_positive: float
    p_one_sided: float
    n: int
    rho: float


def paired_delta_ci(
    candidate: pd.Series,
    baseline: pd.Series,
    *,
    level: float = 0.90,
    reps: int = BOOTSTRAP_REPS,
    mean_block: float = BOOTSTRAP_BLOCK_MEAN,
    seed: int = SEED,
) -> PairedDelta:
    """Paired annualised Sharpe difference and its percentile interval.

    This is the reusable piece of :func:`analyse`: the same positional
    resampling, the same common-random-number seed, and the same definition of
    the statistic. The cap sweep calls it so it cannot grow a second, subtly
    different paired test.
    """
    paired = pd.concat(
        [candidate.rename("candidate"), baseline.rename("baseline")], axis=1
    ).dropna()
    a = paired["candidate"].to_numpy(dtype=float)
    b = paired["baseline"].to_numpy(dtype=float)
    draws = _paired_draws(a, b, reps=reps, mean_block=mean_block, seed=seed)
    finite = draws[np.isfinite(draws)]
    tail = (1.0 - float(level)) / 2.0 * 100.0
    low, high = np.percentile(finite, [tail, 100.0 - tail])
    return PairedDelta(
        point=annualized_sharpe(a) - annualized_sharpe(b),
        ci_low=float(low),
        ci_high=float(high),
        p_positive=float((finite > 0).mean()),
        p_one_sided=float((finite <= 0).mean()),
        n=len(a),
        rho=float(np.corrcoef(a, b)[0, 1]),
    )


def _equivalence(ci_low: float, ci_high: float, bar: float) -> str:
    """Three-way decision from a 90% interval and a materiality bar.

    The 90% two-sided interval is the 5% one-sided test. If the whole interval
    is below the bar, a materially large advantage is excluded; if the whole
    interval is above it, a materially large advantage is supported; otherwise
    the data cannot tell. This is deliberately not a binary pass/fail: "no
    evidence" and "evidence of no material effect" are different objects.
    """
    if not (np.isfinite(ci_low) and np.isfinite(ci_high)):
        return "UNDEFINED"
    if ci_high < bar:
        return "NOT_MATERIAL"
    if ci_low > bar:
        return "MATERIAL"
    return "INCONCLUSIVE"


def _psr_gate(
    candidate: pd.Series,
    baseline_sr_annualized: float,
    bar: float,
    *,
    reps: int,
    mean_block: float,
    seed: int,
) -> tuple[float, float, float, float, float]:
    """The registered PSR gate's number, and what it needs to fire.

    Returns ``(registered_psr, required_delta, mde_80, power_at_bar_analytic,
    power_at_bar_simulated)``. ``required_delta`` is the annualised Sharpe gap
    at which the *observed* PSR reaches 0.95. The 80% MDE is the true gap that
    gives an 80% chance of crossing it. The simulated power resamples the
    baseline's own monthly returns (with a mean shift), so it keeps the sample's
    skew and fat tails instead of assuming normality.
    """
    r = candidate.dropna().astype(float)
    n = len(r)
    sr_m = float(r.mean() / r.std(ddof=1))
    g3 = float(sps.skew(r, bias=False))
    g4 = float(sps.kurtosis(r, fisher=False, bias=False))
    denominator = 1.0 - g3 * sr_m + (g4 - 1.0) / 4.0 * sr_m * sr_m
    if denominator <= 0.0:
        raise ValueError("PSR denominator is non-positive")

    z95 = float(sps.norm.ppf(PSR_BAR))
    required = z95 * math.sqrt(denominator) / math.sqrt(n - 1) * math.sqrt(PERIODS_PER_YEAR)
    mde80 = (z95 + float(sps.norm.ppf(0.80))) * math.sqrt(denominator) / math.sqrt(
        n - 1
    ) * math.sqrt(PERIODS_PER_YEAR)
    sr_ann = sr_m * math.sqrt(PERIODS_PER_YEAR)
    se_ann = math.sqrt((PERIODS_PER_YEAR + 0.5 * sr_ann * sr_ann) / n)
    power_analytic = float(1.0 - sps.norm.cdf((required - bar) / se_ann))

    # Simulated power: shift the baseline's own returns to a true gap of `bar`,
    # then ask how often the registered gate would cross 0.95.
    baseline = r  # the candidate's own distribution is the closest proxy here
    shift = bar / math.sqrt(PERIODS_PER_YEAR) * float(baseline.std(ddof=1))
    indices = stats.stationary_bootstrap_indices(
        n, mean_block=mean_block, reps=reps, seed=seed
    )
    draws = baseline.to_numpy(dtype=float)[indices] + shift
    sr_draw = draws.mean(axis=1) / draws.std(axis=1, ddof=1)
    sr_baseline = baseline_sr_annualized / math.sqrt(PERIODS_PER_YEAR)
    z = (sr_draw - sr_baseline) * math.sqrt(n - 1) / math.sqrt(denominator)
    power_simulated = float((sps.norm.cdf(z) > PSR_BAR).mean())

    registered = float(
        stats.psr(r, stats.annualized_to_per_period(baseline_sr_annualized))
    )
    return registered, required, mde80, power_analytic, power_simulated


def _dsr_sensitivity(
    candidate: pd.Series,
    outcomes: pd.DataFrame,
    family_sizes: tuple[int, ...],
) -> dict[str, float]:
    """DSR p-values when the trial family is counted 1, 2 or all 7 ways.

    ``N = 1`` is the frozen convention, not an adjustment: it reduces the DSR to
    a PSR against zero. The other rows are a robustness check on the caption's
    "after paying for the number of trials" phrasing, not a protocol change.
    """
    trial_sharpes = outcomes["net_sharpe"].astype(float) / math.sqrt(PERIODS_PER_YEAR)
    variance = float(trial_sharpes.var(ddof=1))
    out: dict[str, float] = {}
    for n_trials in family_sizes:
        sr0 = stats.expected_max_sharpe(variance, n_trials)
        out[str(n_trials)] = float(stats.dsr_pvalue(stats.psr(candidate, sr0)))
    return out


def _leave_one_fold_out(
    candidate: pd.Series,
    baseline: pd.Series,
    *,
    fold_months: int = 12,
) -> tuple[float, float, int, int]:
    """Recompute delta SR dropping each 12-month fold, one at a time.

    The frozen concentration gate reads a share of the total advantage; this
    asks the more direct question: does the sign survive removing any single
    fold? It is a diagnostic, not a replacement for §6.3.
    """
    n = len(candidate)
    folds = np.arange(n) // fold_months
    total = int(folds.max()) + 1
    deltas = []
    for fold in range(total):
        keep = folds != fold
        deltas.append(
            annualized_sharpe(candidate.to_numpy()[keep])
            - annualized_sharpe(baseline.to_numpy()[keep])
        )
    finite = [d for d in deltas if np.isfinite(d)]
    return (
        float(min(finite)) if finite else float("nan"),
        float(max(finite)) if finite else float("nan"),
        int(sum(d > 0 for d in finite)),
        len(finite),
    )


# --------------------------------------------------------------------------- #
# Run-level analysis
# --------------------------------------------------------------------------- #

def analyse(
    returns: pd.DataFrame,
    outcomes: pd.DataFrame,
    decisions: pd.DataFrame,
    *,
    bar: float = MATERIALITY_SHARPE_GAP,
    reps: int = BOOTSTRAP_REPS,
    mean_block: float = BOOTSTRAP_BLOCK_MEAN,
    seed: int = SEED,
    family_sizes: tuple[int, ...] = (1, 2, 7),
) -> dict:
    """Compute every paired diagnostic for every candidate in the decision table."""
    baseline = str(decisions["baseline"].iloc[0])
    best_sr = float(outcomes.loc[baseline, "net_sharpe"])
    baseline_returns = returns[baseline].dropna().astype(float)
    results: dict[str, PairedResult] = {}

    for method in decisions.index:
        candidate = returns[str(method)].dropna().astype(float)
        paired = pd.concat(
            [candidate.rename("candidate"), baseline_returns.rename("baseline")], axis=1
        ).dropna()
        a = paired["candidate"].to_numpy()
        b = paired["baseline"].to_numpy()
        n = len(a)

        draws = _paired_draws(
            a, b, reps=reps, mean_block=mean_block, seed=seed
        )
        finite = draws[np.isfinite(draws)]
        point = annualized_sharpe(a) - annualized_sharpe(b)
        ci90 = np.percentile(finite, [5.0, 95.0])
        ci95 = np.percentile(finite, [2.5, 97.5])
        p_positive = float((finite > 0).mean())
        p_one_sided = float((finite <= 0).mean())
        p_exceeds = float((finite > bar).mean())

        psr, required, mde80, power_a, power_s = _psr_gate(
            candidate,
            best_sr,
            bar,
            reps=reps,
            mean_block=mean_block,
            seed=seed,
        )
        dsr_p = _dsr_sensitivity(candidate, outcomes, family_sizes)
        fold_min, fold_max, folds_pos, folds_total = _leave_one_fold_out(
            candidate, baseline_returns
        )

        results[str(method)] = PairedResult(
            method=str(method),
            baseline=baseline,
            n=n,
            rho=float(np.corrcoef(a, b)[0, 1]),
            candidate_net_sharpe=float(outcomes.loc[method, "net_sharpe"]),
            baseline_net_sharpe=best_sr,
            point_delta_sr=float(point),
            ci90_low=float(ci90[0]),
            ci90_high=float(ci90[1]),
            ci95_low=float(ci95[0]),
            ci95_high=float(ci95[1]),
            p_positive=p_positive,
            p_one_sided=p_one_sided,
            p_exceeds_bar=p_exceeds,
            equivalence=_equivalence(float(ci90[0]), float(ci90[1]), bar),
            psr_registered=psr,
            psr_required_delta=required,
            psr_mde_80=mde80,
            psr_power_at_bar=power_a,
            psr_power_at_bar_simulated=power_s,
            dsr_p=dsr_p,
            fold_min_delta=fold_min,
            fold_max_delta=fold_max,
            folds_positive=folds_pos,
            folds_total=folds_total,
        )

    ranked = outcomes.loc[[b for b in outcomes.index if b.startswith("B")], "net_sharpe"]
    ranked = ranked.sort_values(ascending=False)
    second = str(ranked.index[1]) if len(ranked) > 1 else None
    comparator = {
        "best": baseline,
        "best_sr": best_sr,
        "second": second,
        "second_sr": float(ranked.iloc[1]) if second else float("nan"),
        "margin": float(best_sr - ranked.iloc[1]) if second else float("nan"),
    }

    return {
        "status": "EXPLORATORY - same data, post-hoc reading; not a confirmatory test",
        "bar": float(bar),
        "n_months": int(len(baseline_returns)),
        "reps": int(reps),
        "mean_block": float(mean_block),
        "seed": int(seed),
        "comparator": comparator,
        "methods": {k: asdict(v) for k, v in results.items()},
    }


# --------------------------------------------------------------------------- #
# Rendering
# --------------------------------------------------------------------------- #

def render_markdown(payload: dict) -> str:
    """A compact, checkable table; no number is typed by hand."""
    bar = payload["bar"]
    lines = [
        "# Paired inference - exploratory",
        "",
        f"**Status:** {payload['status']}  ",
        f"**Sample:** {payload['n_months']} months; paired stationary bootstrap, "
        f"{payload['reps']} reps, mean block {payload['mean_block']:g}, seed {payload['seed']}  ",
        f"**Materiality bar:** {bar:.2f} annualised net Sharpe  ",
        f"**Comparator:** `{payload['comparator']['best']}` "
        f"({payload['comparator']['best_sr']:.4f}); next is "
        f"`{payload['comparator']['second']}` at "
        f"{payload['comparator']['second_sr']:.4f}, a margin of "
        f"{payload['comparator']['margin']:.4f}.",
        "",
        "| Method | delta SR | 90% paired CI | P(delta>0) | one-sided p | P(delta>bar) | equivalence | registered PSR | gate requires | gate power @ bar |",
        "|---|---:|---:|---:|---:|---:|---|---:|---:|---:|",
    ]
    for method, row in payload["methods"].items():
        lines.append(
            f"| `{method}` | {row['point_delta_sr']:+.4f} | "
            f"[{row['ci90_low']:+.4f}, {row['ci90_high']:+.4f}] | "
            f"{row['p_positive']:.3f} | {row['p_one_sided']:.3f} | "
            f"{row['p_exceeds_bar']:.3f} | **{row['equivalence']}** | "
            f"{row['psr_registered']:.3f} | {row['psr_required_delta']:.3f} | "
            f"{row['psr_power_at_bar_simulated']:.3f} |"
        )
    lines += [
        "",
        "`equivalence` reads the 90% paired interval against the bar: "
        "`NOT_MATERIAL` means the whole interval is below the bar, so a materially "
        "large advantage is excluded at the 5% one-sided level; `MATERIAL` means it "
        "is above; `INCONCLUSIVE` means it straddles. This is a three-way reading, "
        "not a replacement for the frozen verdict.",
        "",
        "The `registered PSR` column is the §6.1 gate as written: a **level** test "
        "of the candidate against the baseline's observed Sharpe. `gate requires` is "
        "the gap at which that gate would fire; `gate power @ bar` is the simulated "
        "chance it fires when the true gap equals the materiality bar. The paired "
        "columns use the same months and preserve their common variation.",
    ]
    return "\n".join(lines) + "\n"


def load_run(run_dir: Path) -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    returns = pd.read_csv(run_dir / "net_excess_returns.csv", index_col=0, parse_dates=True)
    outcomes = pd.read_csv(run_dir / "outcomes.csv", index_col=0)
    decisions = pd.read_csv(run_dir / "decisions.csv", index_col=0)
    return returns, outcomes, decisions


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--run", type=Path, required=True, help="run directory")
    parser.add_argument(
        "--bar",
        type=float,
        default=MATERIALITY_SHARPE_GAP,
        help="materiality bar (annualised net Sharpe); default from config",
    )
    parser.add_argument("--reps", type=int, default=BOOTSTRAP_REPS)
    args = parser.parse_args(argv)

    returns, outcomes, decisions = load_run(args.run)
    payload = analyse(
        returns, outcomes, decisions, bar=args.bar, reps=args.reps
    )
    out_json = args.run / "paired_inference.json"
    out_md = args.run / "paired_inference.md"
    out_json.write_text(json.dumps(payload, indent=2), encoding="utf-8")
    out_md.write_text(render_markdown(payload), encoding="utf-8")
    print(f"wrote {out_json}")
    print(f"wrote {out_md}")
    for method, row in payload["methods"].items():
        print(
            f"  {method}: delta {row['point_delta_sr']:+.4f} "
            f"[{row['ci90_low']:+.4f}, {row['ci90_high']:+.4f}] "
            f"P>0 {row['p_positive']:.3f}  {row['equivalence']}  "
            f"registered PSR {row['psr_registered']:.3f}"
        )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
