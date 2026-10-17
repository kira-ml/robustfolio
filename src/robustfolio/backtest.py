"""Walk-forward harness (spec §6).

Implements the no-lookahead monthly loop of §6.2, the drifted-weight recursion
of §6.3, and the cost application of §6.4. Three properties are deliberate:

1. **Month *t*'s weight uses no month-*t* return** (§6.2). The estimation window
   is ``months[months < t][-60:]`` -- strictly before *t*. This is checkable
   mechanically rather than by inspection: perturbing a single month's return
   must leave that month's weight bit-identical and must change the *next*
   month's weight. ``tests/test_backtest.py::test_month_t_weight_uses_no_month_t_return``
   does exactly that, which is what makes the no-lookahead claim evidence
   rather than an assurance.

2. **One drift implementation, one turnover definition** (§6.3, §7.2).
   :func:`drift_weights` is the only place the recursion is written, and every
   caller reuses it (risk R-C01, R-C04). Turnover has exactly two callers and
   one formula; the Phase 1 ``metrics.annualized_turnover`` is not resurrected.

3. **The cost level cannot reach the optimizer.** Turnover depends on the
   weights and the weights depend on the trailing window, not on the cost level
   -- §5.5.6 fixes B5's penalty at ``kappa = 0.001`` independently of the
   §5.5.3 sweep. So the harness is solved once and net returns are produced at
   any cost level from the same turnover series (:meth:`BacktestResult.net_returns`).
   Solving five times would be five times the work for one answer, and would
   invite the cost level to leak into a method.

The harness is deliberately decoupled from the snapshot: :func:`run_harness`
takes a return frame and an eligibility callable, so the leakage tests can drive
it with synthetic data and an adversarial return series. :func:`run_method` is
the thin snapshot adapter.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Callable

import numpy as np
import pandas as pd

from . import estimators, optimize
from .config import (
    ESTIMATION_WINDOW,
    GAMMA,
    INITIAL_HOLDING_MODE,
    TEST_WINDOW,
    TURNOVER_PENALTY,
    W_MAX,
)

__all__ = [
    "METHOD_IDS",
    "BacktestResult",
    "construct",
    "drift_weights",
    "run_harness",
    "run_method",
]

#: The method set of spec §1: five baselines and two robust methods.
METHOD_IDS = ("B1", "B2", "B3", "B4", "B5", "M1", "M2")

#: Frozen out-of-sample period (protocol §13.1). Selected by month, so the
#: comparison is robust to whether the data layer labels by month start or end.
OOS_START = pd.Timestamp("2012-06-01")
OOS_END = pd.Timestamp("2026-05-31")


@dataclass(frozen=True)
class BacktestResult:
    """A monthly out-of-sample weight path and everything derived from it.

    ``gross_returns`` and ``turnover`` are the primitives; net returns are a
    function of the cost level, not a stored field, because the weights do not
    depend on it (see the module docstring).
    """

    method: str
    weights: pd.DataFrame
    drift: pd.DataFrame
    gross_returns: pd.Series
    turnover: pd.Series
    folds: pd.Series
    diagnostics: pd.DataFrame = field(default_factory=pd.DataFrame)

    # -- derived ----------------------------------------------------------- #

    def cost_drag(self, cost_bps: float) -> pd.Series:
        """``C(t) = kappa * sum_i |w_i(t) - w_i(t^-)|`` (spec §6.4), one-way."""
        kappa = float(cost_bps) / 10_000.0
        return kappa * self.turnover

    def net_returns(self, cost_bps: float) -> pd.Series:
        """``R_net(t) = R_gross(t) - C(t)`` (spec §6.4)."""
        return self.gross_returns - self.cost_drag(cost_bps)

    def annualized_turnover(self) -> float:
        """§7.2: ``12 * mean_t turnover_t``, one-way, from the single canonical series."""
        if self.turnover.empty:
            return float("nan")
        return float(12.0 * self.turnover.mean())

    def fold_returns(self, cost_bps: float = 10.0) -> pd.Series:
        """Net return compounded within each fold, indexed by fold id.

        The §6.3 fold gate counts folds that beat a baseline; that test needs a
        per-fold number, and compounding is the only aggregation that is
        invariant to the decomposition of a fold into months.
        """
        net = self.net_returns(cost_bps)
        return net.groupby(self.folds).apply(lambda x: float((1.0 + x).prod() - 1.0))


# --------------------------------------------------------------------------- #
# §6.3 Drifted weights
# --------------------------------------------------------------------------- #

def drift_weights(weights: pd.Series, realized_returns: pd.Series) -> pd.Series:
    """Book weights after one month of realised returns (spec §6.3).

        w_i(t^-) = w_i(t-1) (1 + r_i(t-1)) / sum_j w_j(t-1) (1 + r_j(t-1))

    The denominator cannot vanish for a long-only portfolio with positive
    growth, but it is checked rather than assumed: a collapsed denominator would
    otherwise produce inf/nan weights that propagate into turnover and the cost
    line as a plausible number.
    """
    w = weights.astype(float)
    r = realized_returns.reindex(w.index)
    if r.isna().any():
        missing = list(r.index[r.isna()])
        raise ValueError(f"drift needs the prior month's return for every holding; missing {missing}")
    grown = w * (1.0 + r)
    total = float(grown.sum())
    if not np.isfinite(total) or total <= 0.0:
        raise ValueError(f"drift denominator collapsed to {total!r}")
    return grown / total


# --------------------------------------------------------------------------- #
# Constructor dispatch
# --------------------------------------------------------------------------- #

def construct(
    method: str,
    train: pd.DataFrame,
    *,
    w_prev: pd.Series | None = None,
    max_weight: float = W_MAX,
    turnover_penalty: float = TURNOVER_PENALTY,
    risk_aversion: float = GAMMA,
    label: str | None = None,
) -> tuple[pd.Series, dict]:
    """Build the target weights for one method on one estimation window.

    ``train`` holds only the assets eligible at the rebalance date, with
    lexicographically sorted columns (spec §4). Returns the weight vector and a
    diagnostics record for that rebalance.

    ``label`` is threaded into the optimizer so that a rejected solve identifies
    *which* rebalance it came from. Without it every failure reads ``MVO`` and the
    failing month has to be recovered by re-running with a patched harness.
    """
    if train.shape[1] == 0:
        raise ValueError(f"{method}: empty eligible universe")
    if train.isna().any().any():
        raise ValueError(f"{method}: estimation window contains gaps")

    call_label = method if label is None else label

    if method == "B1":
        # Arithmetic, no solver, so no certificate and no self-report to record.
        return estimators.equal_weight(train), {
            "formulation": "arithmetic",
            "residual": 0.0,
            "max_violation": 0.0,
            "solver_status": None,
            "solver_iterations": None,
        }

    cov = estimators.sample_cov(train)
    diagnostics = {"cond": float(np.linalg.cond(cov.to_numpy()))}

    if method == "B2":
        solution = optimize.risk_parity(cov, max_weight=max_weight, label=call_label)
    elif method == "B3":
        solution = optimize.mean_variance(
            estimators.sample_mean(train), cov,
            max_weight=max_weight, risk_aversion=risk_aversion, label=call_label,
        )
    elif method == "B4":
        solution = optimize.minimum_variance(cov, max_weight=max_weight, label=call_label)
    elif method == "B5":
        if w_prev is None:
            raise ValueError("B5 requires w_prev: the turnover penalty is defined against it")
        solution = optimize.mean_variance(
            estimators.sample_mean(train), cov,
            w_prev=w_prev, turnover_penalty=turnover_penalty,
            max_weight=max_weight, risk_aversion=risk_aversion, label=call_label,
        )
    elif method == "M1":
        lag = train.shape[0]
        diagnostics["shrinkage"] = estimators.ledoit_wolf_shrinkage(train)
        diagnostics["ddof_ratio"] = lag / (lag - 1.0)  # finding F16
        solution = optimize.mean_variance(
            estimators.sample_mean(train), estimators.ledoit_wolf_cov(train),
            max_weight=max_weight, risk_aversion=risk_aversion, label=call_label,
        )
    elif method == "M2":
        solution = optimize.mean_variance(
            estimators.black_litterman_returns(
                estimators.sample_mean(train), cov, gamma=risk_aversion
            ),
            cov, max_weight=max_weight, risk_aversion=risk_aversion, label=call_label,
        )
    else:
        raise ValueError(f"unknown method {method!r}; expected one of {METHOD_IDS}")

    diagnostics["residual"] = solution.residual
    diagnostics["max_violation"] = solution.max_violation
    diagnostics["formulation"] = solution.formulation
    # What the solver said about itself, next to what the certificate found.
    diagnostics["solver_status"] = solution.meta.get("solver_status", solution.status)
    diagnostics["solver_iterations"] = solution.meta.get("solver_iterations")
    return solution.weights, diagnostics


# --------------------------------------------------------------------------- #
# §6.1-§6.4 The monthly loop
# --------------------------------------------------------------------------- #

def run_harness(
    returns: pd.DataFrame,
    eligible: Callable[[pd.Timestamp], list[str]],
    *,
    method: str,
    start: pd.Timestamp = OOS_START,
    end: pd.Timestamp = OOS_END,
    estimation_window: int = ESTIMATION_WINDOW,
    max_weight: float = W_MAX,
    turnover_penalty: float = TURNOVER_PENALTY,
    risk_aversion: float = GAMMA,
) -> BacktestResult:
    """Run one method across the out-of-sample period, monthly.

    ``returns`` is a ``T x N`` frame of monthly simple returns over the full
    candidate universe. ``eligible(t)`` returns the assets available at month
    *t*; the harness never reads a return dated after *t* when forming *t*'s
    weights.
    """
    if method not in METHOD_IDS:
        raise ValueError(f"unknown method {method!r}; expected one of {METHOD_IDS}")

    months = pd.DatetimeIndex(returns.index).sort_values()
    if months.has_duplicates:
        raise ValueError("returns index has duplicate months")
    returns = returns.loc[months]
    universe = list(returns.columns)

    rebalances = months[(months >= pd.Timestamp(start)) & (months <= pd.Timestamp(end))]
    if len(rebalances) == 0:
        raise ValueError(f"no rebalance months in [{start}, {end}]")

    prior_history = months[months < rebalances[0]]
    if len(prior_history) < estimation_window:
        raise ValueError(
            f"the first rebalance {rebalances[0].date()} has only {len(prior_history)} "
            f"prior months; {estimation_window} are required (spec §6.1)"
        )

    # Finding F18: the period starts flat, so the first rebalance trades from 0.
    if INITIAL_HOLDING_MODE != "flat":
        raise NotImplementedError(f"INITIAL_HOLDING_MODE={INITIAL_HOLDING_MODE!r} is not implemented")
    previous = pd.Series(0.0, index=universe)

    weight_rows: dict[pd.Timestamp, pd.Series] = {}
    drift_rows: dict[pd.Timestamp, pd.Series] = {}
    gross: dict[pd.Timestamp, float] = {}
    turnover: dict[pd.Timestamp, float] = {}
    diagnostics: dict[pd.Timestamp, dict] = {}

    for position, t in enumerate(rebalances):
        window = months[months < t][-estimation_window:]
        members = sorted(eligible(t))
        if not members:
            raise ValueError(f"no eligible assets at {t.date()}; the harness will not hold cash")
        missing = [name for name in members if name not in returns.columns]
        if missing:
            raise ValueError(f"eligible assets absent from the return frame at {t.date()}: {missing}")

        train = returns.loc[window, members]

        # --- §6.3 drift, then the universe change -------------------------- #
        # A new entrant is already 0 in `previous` (the universe is fixed at the
        # candidate list), and a leaver keeps its drifted weight here so the
        # trade that closes it out is counted in turnover.
        drift = previous.copy()
        if position > 0:
            drift = drift_weights(previous, returns.loc[rebalances[position - 1]])
        w_prev_members = drift.reindex(members).fillna(0.0)

        # --- §6.2 constructor: strictly trailing window, no month-t return -- #
        weights, record = construct(
            method,
            train,
            w_prev=w_prev_members,
            max_weight=max_weight,
            turnover_penalty=turnover_penalty,
            risk_aversion=risk_aversion,
            label=f"{method} {t.date().isoformat()}",
        )
        weights = weights.reindex(members).astype(float)

        target = pd.Series(0.0, index=universe)
        target[members] = weights.to_numpy()

        # --- §6.4 turnover and cost, over the full universe ---------------- #
        turnover[t] = float(np.abs(target - drift).sum())

        realized = returns.loc[t].reindex(members)
        if realized.isna().any():
            bad = list(realized.index[realized.isna()])
            raise ValueError(f"{t.date()}: eligible asset has no realised return {bad}")
        gross[t] = float(weights.to_numpy() @ realized.to_numpy())

        weight_rows[t] = target
        drift_rows[t] = drift
        diagnostics[t] = {"n_assets": len(members), **record}
        previous = target

    index = pd.DatetimeIndex(list(weight_rows))
    fold_ids = pd.Series(np.arange(len(index)) // TEST_WINDOW, index=index, name="fold")

    return BacktestResult(
        method=method,
        weights=pd.DataFrame(weight_rows).T.reindex(columns=universe),
        drift=pd.DataFrame(drift_rows).T.reindex(columns=universe),
        gross_returns=pd.Series(gross, name="gross").reindex(index),
        turnover=pd.Series(turnover, name="turnover").reindex(index),
        folds=fold_ids,
        diagnostics=pd.DataFrame(diagnostics).T.reindex(index),
    )


def run_method(snapshot, method: str, **kwargs) -> BacktestResult:
    """Snapshot adapter: :func:`run_harness` against an immutable PIT snapshot."""
    return run_harness(
        snapshot.monthly_total_returns(),
        snapshot.eligible,
        method=method,
        **kwargs,
    )
