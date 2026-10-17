"""Report generation and the §6 decision rules (spec §8, protocol §6).

Spec §8 requires **a single command** that regenerates the report, and an
immutable ``manifest.json`` per run recording the snapshot, the git commit, the
protocol version, the config, the seeds, and the environment. Protocol §14.1 then
fixes what must appear, and §14.2 fixes what may never be claimed. This module is
the place where those two constraints meet, so it is deliberately opinionated:

**Every headline number carries its uncertainty.** Net Sharpe is reported at all
five §5.5.3 cost levels, with a stationary-bootstrap interval at the headline
level, because a bare point estimate of a Sharpe from 168 months invites a
precision the data does not support (protocol §13.1, §14.1 item 5).

**The decision rule is computed, not narrated.** §6.1-§6.4 are a conjunction of
sixteen comparisons; a report that states the verdict without showing each
comparison cannot be checked by its reader. :func:`decision_table` returns one
row per candidate with every comparison as its own boolean column, and the
markdown report shows them.

**Gross numbers are labelled diagnostic everywhere they appear.** §7.1 requires a
gross Sharpe, §14.2 forbids any claim based on it, and §7.5 only makes sense if
gross and net share the same ``r_f``. Gross Sharpe is therefore carried in the
tables in a column whose name says so.

Two protocol clauses are **not** implemented here, and the report says so rather
than filling the gap with a plausible number:

* §6.3's "advantage" is not pinned to a metric. The "holds in >= 60% of folds"
  clause reads the **primary metric** (§2: only net Sharpe may decide whether a
  method beats a baseline), while "no single fold accounts for more than 40% of
  the total advantage" needs an **additive** decomposition, which a Sharpe is
  not. Both are computed: fold wins by net Sharpe, concentration by mean monthly
  net excess return. Recorded as **finding F25**.
* §7.8's calibration is implemented for the **return** half only. The volatility
  half has no defined realisation at a one-month horizon. Recorded as **finding
  F24**.
"""

from __future__ import annotations

import json
import platform
import subprocess
import sys
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path

import numpy as np
import pandas as pd

from . import metrics, stats
from .backtest import BacktestResult, METHOD_IDS
from .config import (
    BOOTSTRAP_BLOCK_MEAN,
    BOOTSTRAP_REPS,
    CI_LEVEL_DECISION,
    CI_LEVEL_REPORT,
    COST_HEADLINE_BPS,
    COST_LEVELS_BPS,
    DSR_FAMILY_SIZE,
    DSR_PVALUE_MAX,
    ESTIMATION_WINDOW,
    MATERIALITY_DRAWDOWN_SLACK,
    MATERIALITY_SHARPE_GAP,
    MATERIALITY_TURNOVER_MULTIPLE,
    PSR_MIN,
    ROBUSTNESS_COST_LEVELS,
    ROBUSTNESS_FOLD_FRACTION,
    ROBUSTNESS_FOLD_SHARE_MAX,
    SEED,
)

__all__ = [
    "BASELINE_IDS",
    "CANDIDATE_IDS",
    "PROTOCOL_VERSION",
    "SPEC_VERSION",
    "CALIBRATION_TARGET",
    "Decision",
    "Report",
    "build_report",
    "calibration_table",
    "decision_table",
    "design_diagnostics",
    "fold_table",
    "manifest",
    "outcome_table",
]

#: Spec §7.8 / protocol §3 target range for empirical coverage.
CALIBRATION_TARGET = (0.80, 1.00)

#: Protocol §4.2's baseline set. B5 is a baseline *and* the H2.3 treatment, so it
#: is in this set; the candidates below are what the project claims.
BASELINE_IDS = ("B1", "B2", "B3", "B4", "B5")

#: The methods whose claims the §6.4 success test evaluates (H2.1, H2.2).
CANDIDATE_IDS = ("M1", "M2")

#: Protocol §4.4 / §7: H2.3 compares the penalised and unpenalised MVO.
H23_TREATMENT, H23_CONTROL = "B5", "B3"

PROTOCOL_VERSION = "2.4"
SPEC_VERSION = "1.1"


# --------------------------------------------------------------------------- #
# Manifest
# --------------------------------------------------------------------------- #

def _git_commit() -> str:
    """The commit the numbers came from, or a loud placeholder.

    A report whose code revision is unknown is not reproducible, so this is
    recorded rather than optional (protocol §12.4 item 8, spec §10.3).
    """
    try:
        out = subprocess.run(
            ["git", "rev-parse", "HEAD"],
            capture_output=True, text=True, check=True, cwd=Path(__file__).resolve().parents[2],
        )
        return out.stdout.strip()
    except Exception:  # noqa: BLE001 - a report must still be writable outside a repo
        return "UNKNOWN"


def manifest(snapshot_id: str, *, extras: dict | None = None) -> dict:
    """The run manifest of spec §8, including the frozen seeds and versions."""
    payload = {
        "generated_utc": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "snapshot_id": snapshot_id,
        "git_commit": _git_commit(),
        "protocol_version": PROTOCOL_VERSION,
        "spec_version": SPEC_VERSION,
        "seed": SEED,
        "bootstrap": {
            "method": "stationary block bootstrap (Politis & Romano 1994)",
            "mean_block_months": BOOTSTRAP_BLOCK_MEAN,
            "replications": BOOTSTRAP_REPS,
            "ci_level_report": CI_LEVEL_REPORT,
            "ci_level_decision": CI_LEVEL_DECISION,
        },
        "cost_levels_bps": list(COST_LEVELS_BPS),
        "headline_cost_bps": COST_HEADLINE_BPS,
        "dsr_family_size": DSR_FAMILY_SIZE,
        "method_ids": list(METHOD_IDS),
        "baseline_ids": list(BASELINE_IDS),
        "candidate_ids": list(CANDIDATE_IDS),
        "environment": {
            "python": sys.version.split()[0],
            "platform": platform.platform(),
            "numpy": np.__version__,
            "pandas": pd.__version__,
        },
        "scope": (
            "EXPLORATORY (DEC-20261015-012): this run is non-confirmatory and may "
            "not be cited for or against any hypothesis."
        ),
    }
    if extras:
        payload.update(extras)
    return payload


# --------------------------------------------------------------------------- #
# Per-method metrics
# --------------------------------------------------------------------------- #

def _excess(net: pd.Series, rf: pd.Series | None) -> pd.Series:
    if rf is None:
        return net.dropna()
    return (net - rf.reindex(net.index)).dropna()


def _interval_columns(interval: stats.BootstrapInterval, prefix: str) -> dict:
    """Flatten a bootstrap interval into `<prefix>_ci_*` columns.

    The prefix is a parameter because these columns are merged into the same row
    for four different statistics; building the names at the call site is what
    stops two statistics' intervals from overwriting each other.
    """
    return {
        f"{prefix}_ci_low": interval.low,
        f"{prefix}_ci_high": interval.high,
        f"{prefix}_ci_level": interval.level,
        f"{prefix}_ci_reps": interval.reps,
        f"{prefix}_ci_block": interval.mean_block,
        f"{prefix}_ci_seed": interval.seed,
        f"{prefix}_ci_n": interval.n_usable,
    }


def outcome_table(
    results: dict[str, BacktestResult],
    *,
    rf: pd.Series | None = None,
    cost_levels: tuple[int, ...] = COST_LEVELS_BPS,
    headline_bps: int = COST_HEADLINE_BPS,
    bootstrap: bool = True,
) -> pd.DataFrame:
    """One row per method: §14.1's mandatory disclosures, at the headline cost.

    Net Sharpe at **every** cost level is reported (item 1); the headline level
    additionally gets a bootstrap interval for net Sharpe, turnover, drawdown and
    CVaR (§13.1). ``DSR``/``PSR`` need a benchmark, so they are not here -- see
    :func:`decision_table`.
    """
    rows: dict[str, dict] = {}
    for method, result in results.items():
        net = result.net_returns(headline_bps)
        gross = result.gross_returns
        excess = _excess(net, rf)
        row: dict = {
            "rebalances": int(len(result.weights)),
            "folds": int(result.folds.nunique()),
            "headline_cost_bps": int(headline_bps),
            "net_sharpe": metrics.sharpe(net, rf),
            "gross_sharpe_diagnostic": metrics.sharpe(gross, rf),
            "cost_drag": metrics.cost_drag(gross, net, rf),
            "turnover_annualized": result.annualized_turnover(),
            "max_drawdown": metrics.max_drawdown(net),
            "cvar95": metrics.cvar(net),
            "skew": metrics.skew_kurt(net)[0],
            "kurtosis": metrics.skew_kurt(net)[1],
            "autocorr1": metrics.autocorr1(net),
            "mean_monthly_net_excess": float(excess.mean()) if len(excess) else float("nan"),
        }
        for level in cost_levels:
            row[f"net_sharpe_{level}bps"] = metrics.sharpe(result.net_returns(level), rf)
        if bootstrap:
            # Common random numbers: every call reseeds from the same SEED and the
            # same sample length, so the intervals share their block structure.
            row.update(_interval_columns(
                stats.bootstrap_ci(excess, metrics.sharpe), "net_sharpe"))
            row.update(_interval_columns(
                stats.bootstrap_ci(result.turnover, metrics.annualized_turnover), "turnover"))
            row.update(_interval_columns(
                stats.bootstrap_ci(net, metrics.max_drawdown), "max_drawdown"))
            row.update(_interval_columns(
                stats.bootstrap_ci(net, metrics.cvar), "cvar95"))
        rows[method] = row
    frame = pd.DataFrame.from_dict(rows, orient="index")
    frame.index.name = "method"
    return frame


# --------------------------------------------------------------------------- #
# §6.3 fold table
# --------------------------------------------------------------------------- #

def fold_table(
    result: BacktestResult,
    baseline: BacktestResult,
    *,
    rf: pd.Series | None = None,
    cost_bps: int = COST_HEADLINE_BPS,
) -> pd.DataFrame:
    """Per-fold comparison of one method against one baseline (protocol §6.3).

    Two advantage measures, because §6.3's two clauses need different things:

    * ``advantage_sharpe`` -- the primary metric (§2), used for "holds in >= 60%
      of folds". Computed within each fold, so it is a 12-month Sharpe and
      therefore noisy by construction; that noise is the reason the gate is 9 of
      14 rather than all 14.
    * ``advantage_return`` -- per-fold mean monthly net excess return difference,
      used for the concentration clause. A Sharpe has no additive decomposition
      across folds; a mean return does, and folds are equal length, so the fold
      shares are shares of the same total.

    Finding F25 records that §6.3 does not say which of these "advantage" means.
    """
    if not result.folds.equals(baseline.folds):
        raise ValueError("method and baseline folds are not the same calendar")
    net = result.net_returns(cost_bps)
    base_net = baseline.net_returns(cost_bps)
    method_excess = _excess(net, rf)
    base_excess = _excess(base_net, rf)

    rows: dict[int, dict] = {}
    for fold in sorted(result.folds.unique()):
        mask = result.folds == fold
        this = method_excess[method_excess.index.isin(net.index[mask])]
        that = base_excess[base_excess.index.isin(base_net.index[mask])]
        rows[int(fold)] = {
            "fold": int(fold),
            "months": int(mask.sum()),
            "net_sharpe": metrics.sharpe(net[mask], rf),
            "baseline_net_sharpe": metrics.sharpe(base_net[mask], rf),
            "advantage_sharpe": metrics.sharpe(net[mask], rf) - metrics.sharpe(base_net[mask], rf),
            "net_return_mean": float(this.mean()) if len(this) else float("nan"),
            "baseline_return_mean": float(that.mean()) if len(that) else float("nan"),
            "advantage_return": (
                float(this.mean()) - float(that.mean()) if len(this) and len(that) else float("nan")
            ),
        }
    frame = pd.DataFrame.from_dict(rows, orient="index")
    frame.index.name = "fold"
    return frame


# --------------------------------------------------------------------------- #
# §7.8 calibration
# --------------------------------------------------------------------------- #

def calibration_table(
    results: dict[str, BacktestResult],
    *,
    headline_bps: int = COST_HEADLINE_BPS,
    window: int = ESTIMATION_WINDOW,
    level: float = CI_LEVEL_REPORT,
) -> pd.DataFrame:
    """Empirical coverage of next-month return intervals per method (§7.8, §3).

    **The reading, stated because §7.8 does not pin it (finding F24).** At each
    rebalance ``t`` the trailing window is the method's own previous ``window``
    months of **net portfolio** returns, a ``level`` prediction interval is formed
    from it by the stationary bootstrap, and the realised value checked against it
    is the *next* month's net return. The alternative reading -- asset returns
    over the estimation window re-weighted by ``w(t)`` -- is not used, because it
    would silently mix a gross-weight projection with net realisations.

    Consequence the reader must not miss: the number below is a property of the
    method's **realised return distribution**, not evidence that its covariance or
    return forecast was right. §7.8's second half (a prediction interval for next
    month's *volatility*) is not implemented and no coverage is reported for it:
    at a one-month horizon there is no sample over which a monthly volatility is
    realised, so any number would be a definition rather than a measurement.
    """
    rows: dict[str, dict] = {}
    for method, result in results.items():
        net = result.net_returns(headline_bps).dropna()
        values = net.to_numpy(dtype=float)
        index = net.index
        lows: list[float] = []
        highs: list[float] = []
        realised: list[float] = []
        stamps: list[pd.Timestamp] = []
        for i in range(window, len(values)):
            low, high = stats.prediction_interval(values[i - window:i], level=level)
            if not (np.isfinite(low) and np.isfinite(high)):
                continue
            lows.append(low)
            highs.append(high)
            realised.append(float(values[i]))
            stamps.append(index[i])
        coverage, hits, usable = stats.calibration_coverage(
            pd.Series(lows, index=stamps, dtype=float),
            pd.Series(highs, index=stamps, dtype=float),
            pd.Series(realised, index=stamps, dtype=float),
        )
        rows[method] = {
            "window_months": int(window),
            "level": float(level),
            "months_evaluated": int(usable),
            "hits": int(hits),
            "coverage": coverage,
            "target_low": CALIBRATION_TARGET[0],
            "target_high": CALIBRATION_TARGET[1],
            "in_target_range": bool(
                np.isfinite(coverage) and CALIBRATION_TARGET[0] <= coverage <= CALIBRATION_TARGET[1]
            ),
        }
    frame = pd.DataFrame.from_dict(rows, orient="index")
    frame.index.name = "method"
    return frame


# --------------------------------------------------------------------------- #
# §6.3 detectability / finding F15
# --------------------------------------------------------------------------- #

def design_diagnostics(
    results: dict[str, BacktestResult],
    decisions: pd.DataFrame,
    *,
    rf: pd.Series | None = None,
    headline_bps: int = COST_HEADLINE_BPS,
) -> pd.DataFrame:
    """Correlation between each candidate and the best baseline (finding F15).

    DEC-20261017-028 resolved F15 as reading (a): ``rho`` is reported in a
    **design/detectability** appendix and is **not** added to the registered
    metric set, so no registration is amended and the DSR family size stays
    ``N = 1``. This function is that appendix's data.

    Why it is worth reporting at all: the two methods' return series overlap
    almost completely (they differ in one input), so the *paired* difference
    carries far less noise than either level, and the power of the comparison is
    governed by ``rho`` rather than by ``T``. The design diagnostic measured the
    paired test as reaching 80% power for the §6.2 threshold at ``rho >= 0.98``;
    the realised ``rho`` is what says whether that regime is the one actually in
    force. ``se_difference`` is the standard error of the mean paired difference,
    which is the quantity the power statement is about.

    ``rho`` is a property of the sample, not a result. It is deliberately kept
    out of :func:`outcome_table` so that no downstream reader mistakes it for a
    registered metric.
    """
    rows: dict[str, dict] = {}
    for method, decision_row in decisions.iterrows():
        baseline = str(decision_row["baseline"])
        candidate_returns = _excess(results[method].net_returns(headline_bps), rf)
        baseline_returns = _excess(results[baseline].net_returns(headline_bps), rf)
        paired = pd.DataFrame(
            {"candidate": candidate_returns, "baseline": baseline_returns}
        ).dropna()
        n = int(len(paired))
        if n < 3:
            rho = float("nan")
            se = float("nan")
        else:
            rho = float(paired["candidate"].corr(paired["baseline"]))
            difference = paired["candidate"] - paired["baseline"]
            se = float(difference.std(ddof=1) / np.sqrt(n))
        rows[method] = {
            "baseline": baseline,
            "n_paired_months": n,
            "rho": rho,
            "mean_paired_difference": (
                float((paired["candidate"] - paired["baseline"]).mean()) if n else float("nan")
            ),
            "se_difference": se,
            "is_registered_metric": False,
        }
    frame = pd.DataFrame.from_dict(rows, orient="index")
    frame.index.name = "method"
    return frame


# --------------------------------------------------------------------------- #
# §6 decision rules
# --------------------------------------------------------------------------- #

@dataclass(frozen=True)
class Decision:
    """The outcome of §6.1-§6.4 for one candidate against the best baseline."""

    method: str
    baseline: str
    verdict: str
    rows: pd.DataFrame
    folds: pd.DataFrame

    @property
    def passed(self) -> dict[str, bool]:
        record = self.rows.iloc[0]
        return {
            key.removeprefix("pass_"): bool(record[key])
            for key in self.rows.columns
            if key.startswith("pass_")
        }


def _best_baseline_id(outcomes: pd.DataFrame, baseline_ids: tuple[str, ...] = BASELINE_IDS) -> str:
    """The baseline with the highest headline net Sharpe (protocol §6.1, §6.2)."""
    present = [b for b in baseline_ids if b in outcomes.index]
    if not present:
        raise ValueError("no baseline methods present in the outcomes table")
    return str(outcomes.loc[present, "net_sharpe"].astype(float).idxmax())


def decision_table(
    results: dict[str, BacktestResult],
    outcomes: pd.DataFrame,
    *,
    rf: pd.Series | None = None,
    headline_bps: int = COST_HEADLINE_BPS,
    cost_levels: tuple[int, ...] = COST_LEVELS_BPS,
    family_size: int = DSR_FAMILY_SIZE,
    candidate_ids: tuple[str, ...] = CANDIDATE_IDS,
) -> tuple[pd.DataFrame, dict[str, Decision]]:
    """Evaluate §6.1-§6.4 for every candidate against the best baseline.

    Returns the one-row-per-candidate table and the per-candidate detail (the
    fold table and the fully-labelled comparison row) so a reader can check each
    of the sixteen comparisons rather than trust a verdict.
    """
    best_id = _best_baseline_id(outcomes)
    best = results[best_id]
    best_net_sharpe = float(outcomes.loc[best_id, "net_sharpe"])

    rows: list[dict] = []
    detail: dict[str, Decision] = {}

    for method in candidate_ids:
        if method not in results:
            continue
        result = results[method]
        net = result.net_returns(headline_bps)
        excess = _excess(net, rf)

        # --- §6.1 statistical significance ---------------------------------- #
        psr = stats.psr(excess, stats.annualized_to_per_period(best_net_sharpe))
        deflated = stats.dsr(excess, family_size=family_size)
        pass_psr = bool(np.isfinite(psr) and psr > PSR_MIN)
        pass_dsr = bool(np.isfinite(deflated) and stats.dsr_pvalue(deflated) < DSR_PVALUE_MAX)

        # --- §6.2 economic materiality -------------------------------------- #
        sharpe_gap = float(outcomes.loc[method, "net_sharpe"]) - best_net_sharpe
        pass_gap = bool(sharpe_gap >= MATERIALITY_SHARPE_GAP)
        turnover_ratio = (
            float(outcomes.loc[method, "turnover_annualized"])
            / float(outcomes.loc[best_id, "turnover_annualized"])
        )
        pass_turnover = bool(turnover_ratio <= MATERIALITY_TURNOVER_MULTIPLE)
        mdd_slack = float(outcomes.loc[method, "max_drawdown"]) - float(
            outcomes.loc[best_id, "max_drawdown"]
        )
        pass_mdd = bool(mdd_slack >= -MATERIALITY_DRAWDOWN_SLACK)

        # --- §6.3 robustness ------------------------------------------------ #
        cost_wins = int(sum(
            float(outcomes.loc[method, f"net_sharpe_{level}bps"])
            > float(outcomes.loc[best_id, f"net_sharpe_{level}bps"])
            for level in cost_levels
        ))
        pass_cost_levels = bool(cost_wins >= ROBUSTNESS_COST_LEVELS)

        folds = fold_table(result, best, rf=rf, cost_bps=headline_bps)
        fold_wins = int((folds["advantage_sharpe"] > 0).sum())
        fold_target = int(np.ceil(ROBUSTNESS_FOLD_FRACTION * len(folds)))
        pass_folds = bool(fold_wins >= fold_target)

        advantages = folds["advantage_return"].astype(float)
        total = float(advantages.sum())
        if np.isfinite(total) and total > 0:
            max_share = float((advantages / total).max())
            pass_share = bool(max_share <= ROBUSTNESS_FOLD_SHARE_MAX)
        else:
            # No positive total advantage: the concentration clause is vacuous,
            # and saying "pass" would let a losing method through on a technicality.
            max_share = float("nan")
            pass_share = False

        statistical = pass_psr and pass_dsr
        material = pass_gap and pass_turnover and pass_mdd
        robust = pass_cost_levels and pass_folds and pass_share
        if statistical and material and robust:
            verdict = "SUCCESS"
        elif (statistical and material) or robust:
            verdict = "PARTIAL"
        else:
            verdict = "FAILURE"

        rows.append({
            "method": method,
            "baseline": best_id,
            "baseline_net_sharpe": best_net_sharpe,
            "net_sharpe": float(outcomes.loc[method, "net_sharpe"]),
            "psr": psr,
            "psr_benchmark": best_net_sharpe,
            "psr_threshold": PSR_MIN,
            "pass_psr": pass_psr,
            "dsr": deflated,
            "dsr_pvalue": stats.dsr_pvalue(deflated),
            "dsr_family_size": family_size,
            "dsr_threshold": DSR_PVALUE_MAX,
            "dsr_v_is_convention": family_size == 1,
            "pass_dsr": pass_dsr,
            "sharpe_gap": sharpe_gap,
            "sharpe_gap_threshold": MATERIALITY_SHARPE_GAP,
            "pass_sharpe_gap": pass_gap,
            "turnover_ratio": turnover_ratio,
            "turnover_ratio_max": MATERIALITY_TURNOVER_MULTIPLE,
            "pass_turnover": pass_turnover,
            "drawdown_slack": mdd_slack,
            "drawdown_slack_min": -MATERIALITY_DRAWDOWN_SLACK,
            "pass_drawdown": pass_mdd,
            "cost_levels_won": cost_wins,
            "cost_levels_required": ROBUSTNESS_COST_LEVELS,
            "pass_cost_levels": pass_cost_levels,
            "folds_won": fold_wins,
            "folds_required": fold_target,
            "pass_folds": pass_folds,
            "max_fold_share": max_share,
            "max_fold_share_limit": ROBUSTNESS_FOLD_SHARE_MAX,
            "pass_fold_share": pass_share,
            "statistical": statistical,
            "material": material,
            "robust": robust,
            "verdict": verdict,
        })
        detail[method] = Decision(
            method=method, baseline=best_id, verdict=verdict,
            rows=pd.DataFrame([rows[-1]]), folds=folds,
        )

    frame = pd.DataFrame(rows).set_index("method") if rows else pd.DataFrame()
    return frame, detail


# --------------------------------------------------------------------------- #
# The report object
# --------------------------------------------------------------------------- #

@dataclass
class Report:
    """Everything one run produces, ready to write (spec §8)."""

    manifest: dict
    outcomes: pd.DataFrame
    decisions: pd.DataFrame
    folds: dict[str, pd.DataFrame]
    calibration: pd.DataFrame | None = None
    design: pd.DataFrame | None = None
    net_excess_returns: pd.DataFrame | None = None
    notes: list[str] = field(default_factory=list)

    def write(self, directory: Path) -> dict[str, Path]:
        """Write ``manifest.json``, the CSV tables, and ``report.md``."""
        directory = Path(directory)
        directory.mkdir(parents=True, exist_ok=True)
        written: dict[str, Path] = {}

        manifest_path = directory / "manifest.json"
        manifest_path.write_text(json.dumps(self.manifest, indent=2) + "\n", encoding="utf-8")
        written["manifest"] = manifest_path

        tables = {"outcomes": self.outcomes, "decisions": self.decisions}
        if self.net_excess_returns is not None:
            # Published so that the headline figure, and any statistic a reader
            # prefers to ours, can be computed from the run directory alone
            # rather than by re-running the harness. It holds net *excess*
            # returns, because that is the series the primary metric is defined
            # on (spec §2): a figure drawn from anything else would illustrate a
            # different quantity from the one in the table above it. ``to_csv``
            # writes float64 at full round-tripping precision; the trap is on
            # the *reader* side, where ``pandas.read_csv`` defaults to a parser
            # that is lossy by one ULP (finding F28). Read it with
            # ``float_precision="round_trip"`` to compare, not to plot.
            tables["net_excess_returns"] = self.net_excess_returns
        if self.calibration is not None:
            tables["calibration"] = self.calibration
        if self.design is not None:
            tables["design"] = self.design
        for name, frame in tables.items():
            path = directory / f"{name}.csv"
            frame.to_csv(path)
            written[name] = path

        for method, frame in self.folds.items():
            path = directory / f"folds_{method}.csv"
            frame.to_csv(path)
            written[f"folds_{method}"] = path

        report_path = directory / "report.md"
        report_path.write_text(self.to_markdown(), encoding="utf-8")
        written["report"] = report_path
        return written

    def to_markdown(self) -> str:
        return _render(self)


def build_report(
    results: dict[str, BacktestResult],
    *,
    snapshot_id: str,
    rf: pd.Series | None = None,
    cost_levels: tuple[int, ...] = COST_LEVELS_BPS,
    headline_bps: int = COST_HEADLINE_BPS,
    family_size: int = DSR_FAMILY_SIZE,
    bootstrap: bool = True,
    calibration_window: bool = True,
) -> Report:
    """Compute the whole report from a set of completed backtests."""
    missing = [m for m in METHOD_IDS if m not in results]
    if missing:
        raise ValueError(f"report needs every method; missing {missing}")
    outcomes = outcome_table(
        results, rf=rf, cost_levels=cost_levels, headline_bps=headline_bps, bootstrap=bootstrap
    )
    decisions, detail = decision_table(
        results, outcomes, rf=rf, headline_bps=headline_bps,
        cost_levels=cost_levels, family_size=family_size,
    )
    folds = {method: decision.folds for method, decision in detail.items()}
    calibration = (
        calibration_table(results, headline_bps=headline_bps)
        if calibration_window
        else None
    )
    design = design_diagnostics(results, decisions, rf=rf, headline_bps=headline_bps)
    net_excess_returns = pd.DataFrame(
        {
            method: _excess(result.net_returns(headline_bps), rf)
            for method, result in results.items()
        }
    ).sort_index()
    return Report(
        manifest=manifest(
            snapshot_id,
            extras={
                "family_size": family_size,
                "cost_levels_bps": list(cost_levels),
                "calibration": {
                    "reported": bool(calibration_window),
                    "reading": (
                        "trailing window = the method's own previous 60 months of net "
                        "portfolio returns; realised value = the next month's net return "
                        "(finding F24). The volatility half of spec 7.8 is not implemented."
                    ),
                    "window_months": ESTIMATION_WINDOW,
                },
                "design_diagnostics": {
                    "is_registered_metric": False,
                    "note": (
                        "rho(candidate, best baseline) is reported per finding F15 "
                        "(DEC-20261017-028) as a design/detectability diagnostic. It is "
                        "not a registered metric and no registration is amended by it."
                    ),
                },
            },
        ),
        outcomes=outcomes,
        decisions=decisions,
        folds=folds,
        calibration=calibration,
        design=design,
        net_excess_returns=net_excess_returns,
        notes=[
            "F15/design: rho(candidate, best baseline) is reported in the design/"
            "detectability table and is NOT a registered metric; the DSR family size "
            "stays N = 1 and no registration is amended.",
            "F24: §7.8 calibration is reported for the next-month RETURN only, under the "
            "reading stated in the manifest. The volatility half has no realisation "
            "defined at a one-month horizon; it is not implemented and no coverage "
            "number is reported for it.",
            "F25: §6.3's 'advantage' is not pinned to a metric. Fold wins use net "
            "Sharpe (the primary metric, §2); the concentration clause uses per-fold "
            "mean monthly net excess return because a Sharpe has no additive "
            "decomposition across folds. The two readings can decide the verdict "
            "differently, and in this run the concentration clause is the binding one.",
            "DSR with the registered family size N = 1 evaluates PSR at SR_0 = 0 by "
            "the frozen O6 convention (spec §7.10); the general formula has no "
            "finite N = 1 limit.",
            "Auxiliary artefact: net_excess_returns.csv holds the monthly net excess "
            "portfolio return series of every method at the headline cost -- the exact "
            "series the primary metric is defined on, so the headline figure and any "
            "statistic a reader prefers can be recomputed from the run directory alone. "
            "It is a disclosure, not a registered metric. Compare it with "
            "float_precision='round_trip' -- pandas' default parser is lossy by one ULP "
            "(finding F28).",
        ],
    )


# --------------------------------------------------------------------------- #
# Rendering
# --------------------------------------------------------------------------- #

def _fmt(value: object, digits: int = 4) -> str:
    if value is None:
        return "n/a"
    try:
        number = float(value)  # type: ignore[arg-type]
    except (TypeError, ValueError):
        return str(value)
    if not np.isfinite(number):
        return "n/a"
    return f"{number:.{digits}f}"


def _fmt_pct(value: object) -> str:
    try:
        number = float(value)  # type: ignore[arg-type]
    except (TypeError, ValueError):
        return "n/a"
    if not np.isfinite(number):
        return "n/a"
    return f"{100.0 * number:.1f}%"


def _render(report: Report) -> str:
    outcomes = report.outcomes
    decisions = report.decisions
    lines: list[str] = []

    lines.append("# robustfolio run report")
    lines.append("")
    lines.append(f"**Snapshot:** `{report.manifest['snapshot_id']}`  ")
    lines.append(f"**Git commit:** `{report.manifest['git_commit']}`  ")
    lines.append(
        f"**Protocol:** v{report.manifest['protocol_version']} (frozen) · "
        f"**Spec:** v{report.manifest['spec_version']} (frozen)  "
    )
    lines.append(
        f"**Generated:** {report.manifest['generated_utc']} · "
        f"**Seed:** {report.manifest['seed']} · "
        f"**Family size N:** {report.manifest['dsr_family_size']}"
    )
    lines.append("")
    lines.append(
        "> **EXPLORATORY.** This run is non-confirmatory (DEC-20261015-012). "
        "None of these numbers may be cited for or against any hypothesis."
    )
    lines.append("")

    # -- headline table ------------------------------------------------------ #
    lines.append("## 1. Headline metric (protocol §2, §14.1)")
    lines.append("")
    lines.append(
        "Net Sharpe is the **only** metric that may decide whether a method beats a "
        "baseline (§2). Gross Sharpe is listed for the cost-drag decomposition and is "
        "**diagnostic only** (§14.2)."
    )
    lines.append("")
    lines.append(
        "| Method | Net Sharpe | 90% CI | Gross Sharpe (diagnostic) | Cost drag | "
        "Turnover (ann.) | Max DD | CVaR 95% |"
    )
    lines.append("|---|---|---|---|---|---|---|---|")
    for method, row in outcomes.iterrows():
        ci = "n/a"
        low, high = row.get("net_sharpe_ci_low"), row.get("net_sharpe_ci_high")
        if low is not None and np.isfinite(float(low)):
            ci = f"[{_fmt(low)}, {_fmt(high)}]"
        lines.append(
            f"| `{method}` | {_fmt(row['net_sharpe'])} | {ci} | "
            f"{_fmt(row['gross_sharpe_diagnostic'])} | {_fmt(row['cost_drag'])} | "
            f"{_fmt(row['turnover_annualized'])} | {_fmt(row['max_drawdown'])} | "
            f"{_fmt(row['cvar95'])} |"
        )
    lines.append("")

    # -- cost sensitivity ---------------------------------------------------- #
    lines.append("## 2. Cost sensitivity (protocol §5.5.7, §14.1)")
    lines.append("")
    cost_levels = [c for c in report.manifest["cost_levels_bps"]]
    header = " | ".join(f"{c} bps" for c in cost_levels)
    lines.append(f"| Method | {header} | Ahead of the best baseline at |")
    lines.append("|---" * (len(cost_levels) + 2) + "|")
    best_id = str(decisions["baseline"].iloc[0]) if len(decisions) else None
    for method, row in outcomes.iterrows():
        values = " | ".join(_fmt(row[f"net_sharpe_{c}bps"]) for c in cost_levels)
        ahead = "n/a"
        if best_id is not None:
            # The levels are listed rather than summarised as one threshold: a
            # method that trails at low cost and leads at high cost is not
            # "break-even at 50 bps", and calling it that would misdescribe which
            # side of the comparison it is on. B5 is exactly that method here.
            best_values = {c: float(outcomes.loc[best_id, f"net_sharpe_{c}bps"]) for c in cost_levels}
            own = {c: float(row[f"net_sharpe_{c}bps"]) for c in cost_levels}
            above = [c for c in cost_levels if own[c] > best_values[c]]
            ahead = ", ".join(str(c) for c in above) if above else "never"
        lines.append(f"| `{method}` | {values} | {ahead} |")
    lines.append("")
    lines.append(
        "**Monotonicity check (§5.5.7 item 4).** Net Sharpe must decline as the cost "
        "level rises. A violation is a bug signal, not a finding."
    )
    lines.append("")
    violations: list[str] = []
    for method, row in outcomes.iterrows():
        series = [float(row[f"net_sharpe_{c}bps"]) for c in cost_levels]
        for left, right, low_c, high_c in zip(series, series[1:], cost_levels, cost_levels[1:]):
            if right > left + 1e-12:
                violations.append(f"`{method}` rises from {low_c} to {high_c} bps")
    lines.append(
        "Monotonic: every method's net Sharpe declines with cost."
        if not violations
        else "**NON-MONOTONIC:** " + "; ".join(violations)
    )
    lines.append("")

    # -- secondary diagnostics ---------------------------------------------- #
    lines.append("## 3. Secondary diagnostics (protocol §3, §14.1)")
    lines.append("")
    lines.append("| Method | Skew | Kurtosis | Lag-1 autocorr | Mean monthly net excess | Rebalances | Folds |")
    lines.append("|---|---|---|---|---|---|---|")
    for method, row in outcomes.iterrows():
        lines.append(
            f"| `{method}` | {_fmt(row['skew'], 3)} | {_fmt(row['kurtosis'], 3)} | "
            f"{_fmt(row['autocorr1'], 3)} | {_fmt(row['mean_monthly_net_excess'], 6)} | "
            f"{int(row['rebalances'])} | {int(row['folds'])} |"
        )
    lines.append("")

    # -- decisions ----------------------------------------------------------- #
    lines.append("## 4. Decision rule (protocol §6.1–§6.4)")
    lines.append("")
    if len(decisions) == 0:
        lines.append("No candidate methods in this run.")
    else:
        lines.append(
            f"Best baseline: **`{best_id}`** at net Sharpe "
            f"{_fmt(decisions['baseline_net_sharpe'].iloc[0])}. All comparisons below "
            "are against it."
        )
        lines.append("")
        lines.append("| Clause | Requirement | " + " | ".join(f"`{m}`" for m in decisions.index) + " |")
        lines.append("|---|---" + "|---" * len(decisions) + "|")
        first = decisions.iloc[0]

        lines.append(
            f"| §6.1 PSR | > {first['psr_threshold']:.2f} vs best baseline | "
            + " | ".join(
                f"{_fmt(r['psr'])} {'PASS' if r['pass_psr'] else 'FAIL'}"
                for _, r in decisions.iterrows()
            )
            + " |"
        )
        lines.append(
            f"| §6.1 DSR p-value | < {first['dsr_threshold']:.2f} (N = {int(first['dsr_family_size'])}) | "
            + " | ".join(
                f"{_fmt(r['dsr_pvalue'])} {'PASS' if r['pass_dsr'] else 'FAIL'}"
                for _, r in decisions.iterrows()
            )
            + " |"
        )
        lines.append(
            f"| §6.2 net-Sharpe gap | ≥ {first['sharpe_gap_threshold']:.2f} | "
            + " | ".join(
                f"{_fmt(r['sharpe_gap'])} {'PASS' if r['pass_sharpe_gap'] else 'FAIL'}"
                for _, r in decisions.iterrows()
            )
            + " |"
        )
        lines.append(
            f"| §6.2 turnover ratio | ≤ {first['turnover_ratio_max']:.2f}× baseline | "
            + " | ".join(
                f"{_fmt(r['turnover_ratio'], 3)}× {'PASS' if r['pass_turnover'] else 'FAIL'}"
                for _, r in decisions.iterrows()
            )
            + " |"
        )
        lines.append(
            f"| §6.2 drawdown slack | ≥ {first['drawdown_slack_min']:.2f} | "
            + " | ".join(
                f"{_fmt(r['drawdown_slack'])} {'PASS' if r['pass_drawdown'] else 'FAIL'}"
                for _, r in decisions.iterrows()
            )
            + " |"
        )
        lines.append(
            f"| §6.3 cost levels won | ≥ {int(first['cost_levels_required'])} of "
            f"{len(cost_levels)} | "
            + " | ".join(
                f"{int(r['cost_levels_won'])} {'PASS' if r['pass_cost_levels'] else 'FAIL'}"
                for _, r in decisions.iterrows()
            )
            + " |"
        )
        lines.append(
            f"| §6.3 folds won | ≥ {int(first['folds_required'])} of "
            f"{int(outcomes['folds'].iloc[0])} | "
            + " | ".join(
                f"{int(r['folds_won'])} {'PASS' if r['pass_folds'] else 'FAIL'}"
                for _, r in decisions.iterrows()
            )
            + " |"
        )
        lines.append(
            f"| §6.3 max fold share | ≤ {first['max_fold_share_limit']:.2f} of total advantage | "
            + " | ".join(
                f"{_fmt_pct(r['max_fold_share'])} {'PASS' if r['pass_fold_share'] else 'FAIL'}"
                for _, r in decisions.iterrows()
            )
            + " |"
        )
        lines.append(
            "| §6.1 statistical | PSR **and** DSR | "
            + " | ".join(
                ("PASS" if r["statistical"] else "FAIL") for _, r in decisions.iterrows()
            )
            + " |"
        )
        lines.append(
            "| §6.2 material | all three clauses | "
            + " | ".join(("PASS" if r["material"] else "FAIL") for _, r in decisions.iterrows())
            + " |"
        )
        lines.append(
            "| §6.3 robust | all three clauses | "
            + " | ".join(("PASS" if r["robust"] else "FAIL") for _, r in decisions.iterrows())
            + " |"
        )
        lines.append(
            "| **§6.4 verdict** | success / partial / failure | "
            + " | ".join(f"**{r['verdict']}**" for _, r in decisions.iterrows())
            + " |"
        )
    lines.append("")

    # -- calibration ---------------------------------------------------------- #
    if report.calibration is not None and len(report.calibration):
        frame = report.calibration
        lines.append("## 5. Calibration of next-month return intervals (protocol §3, spec §7.8)")
        lines.append("")
        lines.append(
            "Target coverage 80–100% at the stated interval level. **Reading (F24):** the "
            "trailing window is the method's own previous 60 months of net portfolio "
            "returns and the realised value is the *next* month's net return, so this "
            "measures whether the method's return distribution is calibrated — not "
            "whether its covariance or return forecast was right. The volatility half "
            "of §7.8 is not implemented."
        )
        lines.append("")
        lines.append("| Method | Window | Level | Months evaluated | Coverage | Hits | In target |")
        lines.append("|---|---|---|---|---|---|---|")
        for method, row in frame.iterrows():
            lines.append(
                f"| `{method}` | {int(row['window_months'])} | {_fmt_pct(row['level'])} | "
                f"{int(row['months_evaluated'])} | {_fmt_pct(row['coverage'])} | "
                f"{int(row['hits'])} | {'yes' if row['in_target_range'] else '**no**'} |"
            )
        lines.append("")

    # -- fold detail --------------------------------------------------------- #
    lines.append("## 6. Walk-forward folds (protocol §6.3, §14.1 item 5)")
    lines.append("")
    for method, frame in report.folds.items():
        baseline = str(decisions.loc[method, "baseline"])
        lines.append(f"### `{method}` vs best baseline `{baseline}`")
        lines.append("")
        lines.append("| Fold | Months | Net Sharpe | Baseline | Advantage (Sharpe) | Advantage (mean monthly return) |")
        lines.append("|---|---|---|---|---|---|")
        for _, row in frame.iterrows():
            lines.append(
                f"| {int(row['fold'])} | {int(row['months'])} | {_fmt(row['net_sharpe'])} | "
                f"{_fmt(row['baseline_net_sharpe'])} | {_fmt(row['advantage_sharpe'])} | "
                f"{_fmt(row['advantage_return'], 6)} |"
            )
        lines.append("")

    # -- design / detectability (finding F15) -------------------------------- #
    if report.design is not None and len(report.design):
        frame = report.design
        lines.append("## 7. Design and detectability (finding F15, DEC-20261017-028)")
        lines.append("")
        lines.append(
            "**Not a registered metric.** `rho` is the Pearson correlation of the candidate's "
            "and the best baseline's net monthly excess returns. It is reported because the two "
            "series are produced by nearly the same estimator, so the comparison's power is "
            "governed by the correlation of their *differences*, not by the length of the "
            "sample; the design diagnostic found a paired test reaching 80% power for the §6.2 "
            "threshold at `rho >= 0.98`. `se_difference` is the standard error of the mean "
            "paired difference. No registration is amended and the DSR family size stays `N = 1`."
        )
        lines.append("")
        lines.append("| Candidate | Baseline | Paired months | rho | Mean paired difference | SE of difference |")
        lines.append("|---|---|---|---|---|---|")
        for method, row in frame.iterrows():
            lines.append(
                f"| `{method}` | `{row['baseline']}` | {int(row['n_paired_months'])} | "
                f"{_fmt(row['rho'])} | {_fmt(row['mean_paired_difference'], 6)} | "
                f"{_fmt(row['se_difference'], 6)} |"
            )
        lines.append("")

    # -- honest limitations -------------------------------------------------- #
    lines.append("## 8. Limitations, deviations, and open items (protocol §14.1 items 8–9)")
    lines.append("")
    for note in report.notes:
        lines.append(f"- {note}")
    lines.append(
        "- The Phase 1 caveat applies: this is an exploratory run. The frozen "
        "confirmatory experiment (Test D, `EXP-H2-20261017-001`) has not yet been "
        "executed."
    )
    lines.append(
        f"- Frictions are a fixed {report.manifest['headline_cost_bps']} bps flat model "
        "with no market impact, capacity, tax, or regime dependence (protocol §5.5.8)."
    )
    lines.append(
        "- §7.8's calibration coverage targets 80–100%; the volatility half is not "
        "implemented (F24), so this run cannot claim to have met §3's calibration "
        "requirement in full."
    )
    lines.append("")
    return "\n".join(lines)
