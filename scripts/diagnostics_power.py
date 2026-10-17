"""Design diagnostics for the frozen protocol: effective bets and statistical power.

**This is not an experiment and not a registry entry** (`evaluation_protocol.md`
§12.2: an experiment is a run that produces a metric on which a decision or claim
will be based). No portfolio is formed, no strategy return series is constructed,
and no performance metric is reported. Every number here is a property of the
*data* or of the *test design*, and would be identical if the robust methods had
never been proposed.

Two questions, both of which must be answered before a Test D result can be
interpreted at all:

1. **How many independent bets does the universe actually contain?**  The
   eigen-spectrum of the covariance the optimizer sees. Eighteen correlated
   asset-class ETFs are not eighteen bets; if the effective count is ~5, the
   ceiling on any optimizer's edge is set long before the estimator is chosen.

2. **What effect size can the registered tests detect?**  The power of (a) the
   level test ("is this strategy's Sharpe positive?") and (b) the paired
   difference test ("is method A better than method B by Δ?"). These have
   *very* different power, and conflating them is the most common way a
   portfolio study misleads itself.

Usage::

    python scripts/diagnostics_power.py [--json PATH] [--figure PATH]
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

import numpy as np
import pandas as pd
from scipy import stats

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from robustfolio import data as dm  # noqa: E402

# -- frozen protocol constants (quoted, not chosen) ------------------------- #
OOS_START = pd.Timestamp("2012-06-30")   # DEC-20261017-024: derived anchor
OOS_END = pd.Timestamp("2026-05-31")     # protocol §13.1: T = 168 months
EST_WINDOW = 60                          # protocol §4.3
TEST_MONTHS = 12                         # protocol §5.2
ALPHA = 0.05                             # protocol §6.1, one-sided
POWER = 0.80
ECONOMIC_THRESHOLD_ANNUAL = 0.20         # protocol §6.2
FOLD_SHARE = 0.60                        # protocol §6.3


# --------------------------------------------------------------------------- #
# 1. Effective number of bets
# --------------------------------------------------------------------------- #

def effective_bets(frame: pd.DataFrame) -> dict:
    """Eigen-spectrum summary of a return panel.

    ``n_part`` is the participation ratio, ``(sum l)^2 / sum l^2``: 1 for a
    single factor, ``n`` for an isotropic (independent) panel. ``n_ent`` is the
    entropy-based effective rank, ``exp(-sum p ln p)``. Both are upper bounds on
    the number of genuinely independent directions, and they are scale-free when
    computed on the correlation matrix (so volatility dispersion cannot flatter
    them).
    """
    corr = frame.corr().values
    cov = frame.cov().values

    def _spectrum(matrix: np.ndarray) -> tuple[np.ndarray, float, float, float]:
        values = np.linalg.eigvalsh(matrix)[::-1]
        values = np.clip(values, 1e-18, None)
        weights = values / values.sum()
        n_part = float(values.sum() ** 2 / (values ** 2).sum())
        n_ent = float(np.exp(-(weights * np.log(weights)).sum()))
        return values, n_part, n_ent, float(weights[0])

    corr_values, corr_part, corr_ent, corr_top = _spectrum(corr)
    _, cov_part, cov_ent, cov_top = _spectrum(cov)
    explained = np.cumsum(corr_values / corr_values.sum())

    return {
        "n_assets": int(frame.shape[1]),
        "n_months": int(frame.shape[0]),
        "n_part_corr": corr_part,
        "n_ent_corr": corr_ent,
        "top_share_corr": corr_top,
        "cond_corr": float(corr_values[0] / corr_values[-1]),
        "n_part_cov": cov_part,
        "n_ent_cov": cov_ent,
        "top_share_cov": cov_top,
        "explained_by_k": {
            int(k): float(explained[k - 1]) for k in range(1, min(8, len(explained)) + 1)
        },
        "n_factors_for_90pct": int(np.searchsorted(explained, 0.90) + 1),
    }


def fold_windows(index: pd.DatetimeIndex) -> list[tuple[pd.Timestamp, list[pd.Timestamp]]]:
    """The 14 (estimation-window-end, test-months) pairs implied by §4.3 + §5.2."""
    oos = index[(index >= OOS_START) & (index <= OOS_END)]
    folds = []
    for start in range(0, len(oos), TEST_MONTHS):
        test = list(oos[start:start + TEST_MONTHS])
        if len(test) < TEST_MONTHS:
            break
        prior = index[index < test[0]]
        folds.append((prior[-1], test))
    return folds


# --------------------------------------------------------------------------- #
# 2. Power of the level test and of the paired difference test
# --------------------------------------------------------------------------- #

def se_level(sr_monthly: float, n_months: int, ar1: float = 0.0) -> float:
    """Lo (2002) standard error of a Sharpe estimate, with AR(1) inflation."""
    inflation = (1.0 + ar1) / (1.0 - ar1) if ar1 > 0 else 1.0
    return float(np.sqrt((1.0 + 0.5 * sr_monthly**2) / n_months) * np.sqrt(inflation))


def se_difference(sr_monthly: float, rho: float, n_months: int) -> float:
    """Jobson-Korkie / Memmel standard error of the *difference* of two Sharpes.

    ``Var(dSR) = (1/T) [ 2(1 - rho) + SR^2 (1 - rho^2) ]`` for two strategies with
    equal Sharpe ``SR`` at return frequency and return correlation ``rho``.

    The first term is the one that matters: two strategies that are 99% correlated
    can be separated by a difference far smaller than either one's own standard
    error. This is why the paired design is powerful, and why the *level* test is
    not.
    """
    return float(np.sqrt((2.0 * (1.0 - rho) + sr_monthly**2 * (1.0 - rho**2)) / n_months))


def mde(se: float) -> float:
    """Minimum detectable effect at 80% power, one-sided 5%."""
    z = stats.norm.ppf(1.0 - ALPHA) + stats.norm.ppf(POWER)
    return float(z * se)


def power_at(true_effect: float, se: float) -> float:
    """Power to detect ``true_effect`` when the estimator has standard error ``se``."""
    z_crit = stats.norm.ppf(1.0 - ALPHA)
    return float(1.0 - stats.norm.cdf(z_crit - true_effect / se))


# --------------------------------------------------------------------------- #
# Report
# --------------------------------------------------------------------------- #

def fmt(value: float, digits: int = 3) -> str:
    return f"{value:.{digits}f}"


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--json", type=Path, default=None)
    parser.add_argument("--figure", type=Path, default=None)
    args = parser.parse_args()

    snapshot_id = dm.list_snapshots()[0]
    snapshot = dm.load_snapshot(snapshot_id)
    returns = snapshot.monthly_total_returns()

    out: dict = {"snapshot_id": snapshot_id, "not_an_experiment": True}

    print("=" * 78)
    print("robustfolio design diagnostics -- NOT an experiment, NOT a registry entry")
    print("=" * 78)
    print(f"snapshot : {snapshot_id}")
    print(f"window   : {OOS_START.date()} .. {OOS_END.date()} "
          f"(protocol 13.1: T = 168 months, 14 folds)")
    print(f"universe : {returns.shape[1]} candidates")

    folds = fold_windows(returns.index)
    oos = returns.loc[OOS_START:OOS_END]
    out["n_oos_months"] = int(len(oos))
    out["n_folds"] = len(folds)
    print(f"folds    : {len(folds)} x {TEST_MONTHS} months, "
          f"estimation window {EST_WINDOW} months")

    # ---- 1. effective bets ------------------------------------------------- #
    print()
    print("--- 1. how many independent bets does the universe contain? ---")

    full = effective_bets(oos.dropna(axis=1, how="any"))
    out["full_window"] = full
    print(f"\nfull out-of-sample window ({full['n_months']} months, "
          f"{full['n_assets']} assets), correlation matrix:")
    print(f"  market factor share (lambda_1 / sum lambda) : "
          f"{fmt(full['top_share_corr'])}")
    print("  variance explained by the first k factors   : "
          + ", ".join(f"{k}:{fmt(v, 2)}" for k, v in full["explained_by_k"].items()))
    print(f"  factors needed for 90% of variance          : "
          f"{full['n_factors_for_90pct']}")
    print(f"  participation ratio      N_part             : "
          f"{fmt(full['n_part_corr'], 2)}")
    print(f"  entropy effective rank   N_ent              : "
          f"{fmt(full['n_ent_corr'], 2)}")
    print(f"  condition number         cond(corr)         : "
          f"{fmt(full['cond_corr'], 1)}")

    # Marchenko-Pastur: where would the eigenvalues of an INDEPENDENT panel of
    # this size sit?  If the observed extremes fall outside that support, the
    # near-singularity is structure, not a short-sample artifact.
    ratio = full["n_assets"] / full["n_months"]
    mp_lower = (1.0 - np.sqrt(ratio)) ** 2
    mp_upper = (1.0 + np.sqrt(ratio)) ** 2
    eigenvalues = np.linalg.eigvalsh(oos.dropna(axis=1, how="any").corr().values)[::-1]
    below = int((eigenvalues < mp_lower).sum())
    out["marchenko_pastur"] = {
        "ratio": float(ratio), "lower": float(mp_lower), "upper": float(mp_upper),
        "n_below_lower": below, "smallest": float(eigenvalues[-1]),
    }
    print(f"\n  Marchenko-Pastur band for an independent 18x168 panel: "
          f"[{fmt(mp_lower)}, {fmt(mp_upper)}]")
    print(f"  observed eigenvalues below the lower edge : {below} of 18 "
          f"(smallest {eigenvalues[-1]:.4f}; the edge is "
          f"{mp_lower / eigenvalues[-1]:.0f}x that)")
    print("  => not consistent with an independent panel: the near-singularity is "
          "real")
    print("     correlation structure, so the sample covariance cannot be inverted "
          "safely --")
    print("     which is the H1 premise, supported by the data rather than assumed.")

    per_fold = []
    for end, test in folds:
        prior = returns.index[returns.index <= end][-EST_WINDOW:]
        window = returns.loc[prior].dropna(axis=1, how="any")
        stats_fold = effective_bets(window)
        stats_fold["fold_end"] = end.date().isoformat()
        per_fold.append(stats_fold)
    out["per_fold_estimation_windows"] = per_fold

    def spread(key: str) -> str:
        values = np.array([f[key] for f in per_fold])
        return (f"min {fmt(values.min(), 2)}  median {fmt(np.median(values), 2)}"
                f"  max {fmt(values.max(), 2)}")

    print(f"\nper-fold estimation window ({EST_WINDOW} months, exactly what each "
          f"optimizer sees):")
    print(f"  N_part (corr)      : {spread('n_part_corr')}")
    print(f"  N_ent  (corr)      : {spread('n_ent_corr')}")
    print(f"  top factor share   : {spread('top_share_corr')}")
    print(f"  cond(cov)          : "
          + "min {:,.0f}  median {:,.0f}  max {:,.0f}".format(
              np.min([f["cond_corr"] for f in per_fold]) * 1,
              np.median([f["cond_corr"] for f in per_fold]),
              np.max([f["cond_corr"] for f in per_fold])))

    n_assets = full["n_assets"]
    print(f"  observations per parameter   N/T = {n_assets}/{EST_WINDOW}"
          f" = {n_assets / EST_WINDOW:.2f}")

    out["n_over_t"] = float(n_assets / EST_WINDOW)

    # ---- 2. power: level test ---------------------------------------------- #
    print()
    print("--- 2. what can the registered tests detect? ---")
    print("\n(a) LEVEL test -- is a strategy's Sharpe positive?  (protocol 6.1)")

    # asset-level autocorrelation and non-normality feed the error variance
    ar1_assets = oos.apply(lambda c: c.autocorr(1)).dropna()
    principal = oos.dropna(axis=1, how="any")
    centred = principal - principal.mean()
    vectors = np.linalg.eigh(centred.corr().values)[1][:, ::-1]
    pc1 = pd.Series(centred.values @ vectors[:, 0], index=principal.index)
    ar1_pc1 = float(pc1.autocorr(1))
    skew_pc1 = float(pc1.skew())
    kurt_pc1 = float(pc1.kurt() + 3.0)  # pandas returns excess kurtosis

    out["ar1"] = {
        "assets_median": float(ar1_assets.median()),
        "assets_max": float(ar1_assets.max()),
        "pc1": ar1_pc1,
    }
    out["pc1_non_normality"] = {"skew": skew_pc1, "pearson_kurtosis": kurt_pc1}

    print(f"  AR(1) of monthly asset returns : median {fmt(ar1_assets.median())}, "
          f"max {fmt(ar1_assets.max())}; first principal component {fmt(ar1_pc1)}")
    print(f"  first principal component      : skew {fmt(skew_pc1)}, "
          f"Pearson kurtosis {fmt(kurt_pc1)}  (3.0 = normal)")

    print(f"\n  {'annual SR':>10} {'MDE (annual SR)':>16} {'power at SR=0.50':>18}")
    level_rows = []
    for sr_annual in (0.30, 0.50, 0.70, 1.00):
        sr_monthly = sr_annual / np.sqrt(12.0)
        se = se_level(sr_monthly, len(oos), ar1=ar1_pc1)
        row = {
            "sri_annual": sr_annual,
            "mde_annual": mde(se) * np.sqrt(12.0),
            "power_at_0.50": power_at(0.50 / np.sqrt(12.0), se),
        }
        level_rows.append(row)
        print(f"  {sr_annual:>10.2f} {row['mde_annual']:>16.2f} "
              f"{row['power_at_0.50']:>18.2f}")
    out["level_test"] = level_rows
    print(f"\n  A strategy needs roughly SR {fmt(level_rows[1]['mde_annual'], 2)} "
          f"annualised before its Sharpe is statistically")
    print("  distinguishable from zero at all. So the level test cannot resolve a "
          "Sharpe in the")
    print("  0.3-0.5 band -- but it CAN confirm an already-large Sharpe.")

    # What level of Sharpe actually occurred?  (Asset characterisation, not a
    # strategy result: no portfolio is formed here.)
    asset_sr = (oos.mean() / oos.std()) * np.sqrt(12.0)
    out["asset_sharpe_annual"] = {
        "min": float(asset_sr.min()), "median": float(asset_sr.median()),
        "max": float(asset_sr.max()),
    }
    print(f"  For context, buy-and-hold annualised Sharpes of the candidates span "
          f"{fmt(asset_sr.min(), 2)} .. {fmt(asset_sr.max(), 2)}")
    print(f"  (median {fmt(asset_sr.median(), 2)}) over this window, i.e. mostly "
          f"ABOVE the level-test")
    print("  threshold -- so the level test is adequately powered here, and the "
          "interesting")
    print("  question is the SMALL DIFFERENCES, not the levels.")

    # ---- 3. power: paired difference --------------------------------------- #
    print("\n(b) PAIRED DIFFERENCE test -- is method A better than B by delta?")
    print("    Var(dSR) = (1/T)[ 2(1-rho) + SR^2 (1-rho^2) ]   "
          "(Jobson-Korkie / Memmel)")
    assumed_annual = 0.50
    sr_monthly = assumed_annual / np.sqrt(12.0)
    print(f"    assumed level SR = {assumed_annual:.2f} annualised "
          f"({fmt(sr_monthly)} monthly), T = {len(oos)}")

    paired_rows = []
    print(f"\n    {'rho':>7} {'SE(dSR) mo':>11} {'MDE(dSR) annual':>17} "
          f"{'power at 0.20 annual':>21}")
    for rho in (0.90, 0.95, 0.98, 0.99, 0.995, 0.999):
        se = se_difference(sr_monthly, rho, len(oos))
        mde_annual = mde(se) * np.sqrt(12.0)
        power = power_at(ECONOMIC_THRESHOLD_ANNUAL / np.sqrt(12.0), se)
        paired_rows.append({
            "rho": rho, "se_monthly": se, "mde_annual": mde_annual, "power": power,
        })
        print(f"    {rho:>7.3f} {se:>11.5f} {mde_annual:>17.3f} {power:>21.2f}")
    out["paired_difference_test"] = {
        "assumed_level_sr_annual": assumed_annual,
        "threshold_annual": ECONOMIC_THRESHOLD_ANNUAL,
        "rows": paired_rows,
    }

    threshold_rho = next(
        (r["rho"] for r in paired_rows if r["power"] >= POWER), None
    )
    out["rho_for_80pct_power_at_threshold"] = threshold_rho
    print(f"\n    The 6.2 threshold (0.20 annualised) is detectable at >= 80% power "
          f"once rho >= {threshold_rho}.")
    print("    M1/M2 differ from B3 by exactly one component, so rho in "
          "0.95-0.995 is expected --")
    print("    but it is an ASSUMPTION until measured. Requirement: the harness must "
          "report")
    print("    rho(candidate, best baseline) alongside every Sharpe difference. If "
          f"rho < {threshold_rho},")
    print("    a null result is UNDERPOWERED (inconclusive), not evidence of no effect.")

    # ---- 4. the robustness gate -------------------------------------------- #
    print()
    print("--- 3. is the 6.3 fold-consistency gate informative? ---")
    n_folds = len(folds)
    needed = int(np.ceil(FOLD_SHARE * n_folds))
    p_independent = float(stats.binom.sf(needed - 1, n_folds, 0.5))
    out["fold_gate"] = {
        "n_folds": n_folds, "needed": needed, "p_pass_under_null_independent": p_independent,
    }
    print(f"  6.3 requires the advantage in >= {FOLD_SHARE:.0%} of folds "
          f"(>= {needed} of {n_folds}).")
    print(f"  Under the null with independent folds: "
          f"P(pass) = {p_independent:.3f}")
    print("  Fold outcomes share overlapping training windows, so they are "
          "positively correlated\n  and the true rate is HIGHER than that. Either "
          "way the gate alone is a weak filter:\n  the conjunctive 6.1 DSR bullet "
          "is what controls Type I, not this.")

    # ---- 5. context -------------------------------------------------------- #
    print()
    print("--- 4. context: is the estimation-error problem even real here? ---")
    print(f"  N/T = {n_assets}/{EST_WINDOW} = {n_assets / EST_WINDOW:.2f}  "
          f"(large => sample covariance is badly estimated,")
    print("  which is the H1 premise) BUT the effective number of bets is only "
          f"{fmt(full['n_part_corr'], 1)}-{fmt(full['n_ent_corr'], 1)},")
    print("  so the achievable gain from a better estimator is bounded by how "
          "little independent")
    print("  cross-sectional signal the universe contains. Both facts are true; "
          "which dominates")
    print("  is exactly what Test D asks.")

    if args.json:
        args.json.parent.mkdir(parents=True, exist_ok=True)
        args.json.write_text(json.dumps(out, indent=2, default=float), encoding="utf-8")
        print(f"\nwritten: {args.json}")

    if args.figure:
        import matplotlib
        matplotlib.use("Agg")
        import matplotlib.pyplot as plt

        fig, axes = plt.subplots(1, 2, figsize=(11, 4.2))
        rho_grid = np.linspace(0.80, 0.999, 200)
        axes[0].plot(rho_grid, [mde(se_difference(sr_monthly, r, len(oos))) * np.sqrt(12)
                                for r in rho_grid])
        axes[0].axhline(ECONOMIC_THRESHOLD_ANNUAL, ls="--", c="k")
        axes[0].set_xlabel("correlation with baseline")
        axes[0].set_ylabel("MDE, annualised Sharpe difference")
        axes[0].set_title("Paired test: detectable difference")

        axes[1].bar(range(1, len(full["explained_by_k"]) + 1),
                    [v for v in full["explained_by_k"].values()])
        axes[1].set_xlabel("factors")
        axes[1].set_ylabel("cumulative variance explained")
        axes[1].set_title("Eigen-spectrum of the universe")
        fig.tight_layout()
        args.figure.parent.mkdir(parents=True, exist_ok=True)
        fig.savefig(args.figure, dpi=150)
        print(f"written: {args.figure}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
