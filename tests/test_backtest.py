"""Harness conformance tests (spec §6).

The central test here is
:func:`test_month_t_weight_uses_no_month_t_return`. It is mechanical, not
attitudinal: it perturbs one month's return and checks that the weight formed
*at* that month is bit-identical while the weight formed at the *next* month
changes. That two-sided result is what distinguishes "the code looks
lookahead-free" from "the code is lookahead-free", and it fails the moment the
training window is widened by one month -- the exact defect found in Phase 1
(protocol §5.2, DEC-20261015-015 finding 4d).
"""

from __future__ import annotations

import numpy as np
import pandas as pd
import pytest

from robustfolio import backtest
from robustfolio.backtest import drift_weights, run_harness

ASSETS = ["A", "B", "C", "D", "E"]
START = pd.Timestamp("2007-01-31")


def synthetic_returns(n_months: int = 80, columns=ASSETS, seed: int = 0) -> pd.DataFrame:
    rng = np.random.default_rng(seed)
    index = pd.date_range(START, periods=n_months, freq="ME")
    values = rng.normal(scale=0.03, size=(n_months, len(columns)))
    return pd.DataFrame(values, index=index, columns=columns)


def all_eligible(t) -> list[str]:
    return list(ASSETS)


def window(index, first: int, last: int):
    return index[first], index[last]


# --------------------------------------------------------------------------- #
# §6.1 the loop's shape
# --------------------------------------------------------------------------- #

def test_rebalance_months_are_contiguous_and_within_the_requested_window():
    returns = synthetic_returns()
    start, end = window(returns.index, 60, 79)
    result = run_harness(returns, all_eligible, method="B1", start=start, end=end)
    assert len(result.weights) == 20
    assert result.weights.index[0] == start
    assert result.weights.index[-1] == end
    assert list(result.gross_returns.index) == list(result.weights.index)
    assert list(result.turnover.index) == list(result.weights.index)


def test_a_window_with_too_little_history_is_refused():
    returns = synthetic_returns(n_months=80)
    start = returns.index[30]  # only 30 prior months
    with pytest.raises(ValueError, match="prior months"):
        run_harness(returns, all_eligible, method="B1", start=start, end=returns.index[79])


def test_an_empty_eligible_universe_is_refused():
    returns = synthetic_returns()
    start, end = window(returns.index, 60, 70)
    with pytest.raises(ValueError, match="no eligible assets"):
        run_harness(returns, lambda t: [], method="B1", start=start, end=end)


def test_an_eligible_asset_outside_the_return_frame_is_refused():
    returns = synthetic_returns()
    start, end = window(returns.index, 60, 70)
    with pytest.raises(ValueError, match="absent from the return frame"):
        run_harness(returns, lambda t: ASSETS + ["ZZZ"], method="B1", start=start, end=end)


# --------------------------------------------------------------------------- #
# §6.1 folds
# --------------------------------------------------------------------------- #

def test_folds_are_non_overlapping_blocks_of_twelve():
    returns = synthetic_returns(n_months=108)
    start, end = window(returns.index, 60, 107)
    result = run_harness(returns, all_eligible, method="B1", start=start, end=end)
    assert len(result.folds) == 48
    counts = result.folds.value_counts().sort_index()
    assert list(counts.index) == [0, 1, 2, 3]
    assert set(counts.to_numpy()) == {12}
    # no month appears in two folds
    assert result.folds.index.is_unique


def test_fold_returns_compound_the_net_return_within_each_fold():
    """The §6.3 fold gate counts folds that beat a baseline, so it needs a
    per-fold number; compounding is the only aggregation invariant to how a fold
    is decomposed into months."""
    returns = synthetic_returns(n_months=96)
    start, end = window(returns.index, 60, 95)
    result = run_harness(returns, all_eligible, method="B1", start=start, end=end)
    folds = result.fold_returns(10.0)
    assert list(folds.index) == [0, 1, 2]
    net = result.net_returns(10.0)
    for fold in folds.index:
        block = net[result.folds == fold]
        assert len(block) == 12
        assert np.isclose(float(folds.loc[fold]), float((1.0 + block).prod() - 1.0))


# --------------------------------------------------------------------------- #
# §6.3 drift
# --------------------------------------------------------------------------- #

def test_drift_matches_the_formula():
    weights = pd.Series([0.5, 0.3, 0.2], index=["x", "y", "z"])
    realized = pd.Series([0.10, -0.05, 0.02], index=["x", "y", "z"])
    grown = weights * (1.0 + realized)
    expected = grown / grown.sum()
    assert np.allclose(drift_weights(weights, realized), expected)


def test_drift_preserves_the_unit_sum():
    rng = np.random.default_rng(4)
    weights = pd.Series(rng.dirichlet(np.ones(7)), index=list("abcdefg"))
    realized = pd.Series(rng.normal(scale=0.05, size=7), index=list("abcdefg"))
    assert np.isclose(float(drift_weights(weights, realized).sum()), 1.0)


def test_drift_refuses_a_missing_prior_return():
    weights = pd.Series([0.5, 0.5], index=["x", "y"])
    realized = pd.Series([0.01, np.nan], index=["x", "y"])
    with pytest.raises(ValueError, match="prior month's return"):
        drift_weights(weights, realized)


def test_drift_refuses_a_collapsed_denominator():
    weights = pd.Series([0.5, 0.5], index=["x", "y"])
    realized = pd.Series([-1.0, -1.0], index=["x", "y"])
    with pytest.raises(ValueError, match="collapsed"):
        drift_weights(weights, realized)


# --------------------------------------------------------------------------- #
# §6.4 turnover, cost and gross return -- against the definitions, not the code
# --------------------------------------------------------------------------- #

def test_first_rebalance_starts_flat_and_pays_a_full_entry():
    """Finding F18 / DEC-20261017-029: w^- = 0, so the entry trade is 100%."""
    returns = synthetic_returns()
    start, end = window(returns.index, 60, 70)
    result = run_harness(returns, all_eligible, method="B1", start=start, end=end)
    assert np.allclose(result.drift.iloc[0].to_numpy(), 0.0)
    assert np.isclose(float(result.turnover.iloc[0]), 1.0)


def test_turnover_is_the_absolute_difference_from_the_drifted_book():
    returns = synthetic_returns()
    start, end = window(returns.index, 60, 75)
    result = run_harness(returns, all_eligible, method="B1", start=start, end=end)
    recomputed = (result.weights - result.drift).abs().sum(axis=1)
    assert np.allclose(result.turnover.to_numpy(), recomputed.to_numpy())


def test_gross_return_is_the_weight_vector_times_the_realised_returns():
    returns = synthetic_returns()
    start, end = window(returns.index, 60, 75)
    result = run_harness(returns, all_eligible, method="B1", start=start, end=end)
    for t in result.weights.index:
        expected = float(result.weights.loc[t] @ returns.loc[t])
        assert np.isclose(float(result.gross_returns.loc[t]), expected)


def test_net_return_is_gross_minus_the_turnover_cost():
    returns = synthetic_returns()
    start, end = window(returns.index, 60, 75)
    result = run_harness(returns, all_eligible, method="B1", start=start, end=end)
    net = result.net_returns(10.0)
    expected = result.gross_returns - 0.001 * result.turnover
    assert np.allclose(net.to_numpy(), expected.to_numpy())
    assert np.allclose(result.net_returns(0.0).to_numpy(), result.gross_returns.to_numpy())


def test_the_cost_level_cannot_reach_the_weights():
    """§5.5.6 fixes B5's penalty at kappa = 0.001; the §5.5.3 sweep is ex-post.

    So the harness is solved once and every cost level reuses one weight path.
    If a cost level could move a weight, this project's cost sweep would be
    measuring the cost level instead of the method.
    """
    returns = synthetic_returns()
    start, end = window(returns.index, 60, 75)
    result = run_harness(returns, all_eligible, method="B5", start=start, end=end)
    weights = result.weights.copy()
    zero = result.net_returns(0.0)
    assert result.weights.equals(weights), "net_returns() must not mutate or re-solve"
    assert np.allclose(zero.to_numpy(), result.gross_returns.to_numpy())
    # the drag is linear in the level, which is only true if the weights held
    drag_ten = float((result.gross_returns - result.net_returns(10.0)).sum())
    drag_fifty = float((result.gross_returns - result.net_returns(50.0)).sum())
    assert drag_ten > 0.0
    assert np.isclose(drag_fifty, 5.0 * drag_ten, rtol=1e-12)


# --------------------------------------------------------------------------- #
# §6.3 universe changes
# --------------------------------------------------------------------------- #

def test_a_leaving_asset_is_traded_to_zero_and_that_trade_is_counted():
    returns = synthetic_returns()
    start, end = window(returns.index, 60, 79)
    leaves_at = returns.index[71]

    def eligible(t):
        return [a for a in ASSETS if not (a == "E" and t >= leaves_at)]

    result = run_harness(returns, eligible, method="B1", start=start, end=end)
    assert result.weights.loc[leaves_at, "E"] == 0.0
    # the leaver still carried its drifted weight into the month it left
    assert result.drift.loc[leaves_at, "E"] > 0.0
    # so closing it out is charged, and it is charged exactly once
    assert np.isclose(
        float(result.turnover.loc[leaves_at]),
        float(np.abs(result.weights.loc[leaves_at] - result.drift.loc[leaves_at]).sum()),
    )
    # it stays at zero afterwards and never drifts back
    after = result.weights.index[result.weights.index > leaves_at]
    assert (result.weights.loc[after, "E"] == 0.0).all()


def test_a_new_entrant_starts_from_zero():
    returns = synthetic_returns()
    start, end = window(returns.index, 60, 79)
    joins_at = returns.index[66]
    universe = ASSETS + ["F"]
    # extend the frame with a sixth column, eligible only from `joins_at`
    returns = returns.copy()
    returns["F"] = np.linspace(-0.01, 0.01, len(returns))

    def eligible(t):
        return universe if t >= joins_at else ASSETS

    result = run_harness(returns, eligible, method="B1", start=start, end=end)
    assert result.weights.loc[joins_at, "F"] > 0.0
    assert result.drift.loc[joins_at, "F"] == 0.0


# --------------------------------------------------------------------------- #
# The no-lookahead proof (protocol §5.5.4)
# --------------------------------------------------------------------------- #

def test_month_t_weight_uses_no_month_t_return():
    """Perturb one month; that month's weight must not move, the next must.

    Run with B3, whose weights genuinely depend on the training window, so the
    test cannot pass vacuously the way it would for B1's fixed 1/N.
    """
    returns = synthetic_returns()
    target = returns.index[65]
    start, end = window(returns.index, 60, 70)

    baseline = run_harness(returns, all_eligible, method="B3", start=start, end=end)

    shocked = returns.copy()
    shocked.loc[target] = shocked.loc[target] * 100.0
    after = run_harness(shocked, all_eligible, method="B3", start=start, end=end)

    # month t's weight is formed from months < t only
    pd.testing.assert_series_equal(
        baseline.weights.loc[target], after.weights.loc[target], check_exact=True
    )
    # ... but the *next* month's weight does see it, because its window includes t.
    # If this assertion fails the test above is vacuous, so it is not optional.
    assert not np.allclose(
        baseline.weights.loc[returns.index[66]].to_numpy(),
        after.weights.loc[returns.index[66]].to_numpy(),
    )
    # and the realised return of month t does move, as it must
    assert not np.isclose(
        float(baseline.gross_returns.loc[target]), float(after.gross_returns.loc[target])
    )


def test_a_shocked_future_month_cannot_move_an_earlier_weight():
    """The other direction: no weight may depend on a return dated after it."""
    returns = synthetic_returns()
    start, end = window(returns.index, 60, 74)
    baseline = run_harness(returns, all_eligible, method="B3", start=start, end=end)

    shocked = returns.copy()
    shocked.loc[returns.index[74]] = 50.0
    after = run_harness(shocked, all_eligible, method="B3", start=start, end=end)

    pd.testing.assert_frame_equal(
        baseline.weights.loc[: returns.index[73]],
        after.weights.loc[: returns.index[73]],
        check_exact=True,
    )


# --------------------------------------------------------------------------- #
# Determinism (spec §5.4.8)
# --------------------------------------------------------------------------- #

def test_the_harness_is_deterministic():
    returns = synthetic_returns()
    start, end = window(returns.index, 60, 72)
    first = run_harness(returns, all_eligible, method="B3", start=start, end=end)
    second = run_harness(returns, all_eligible, method="B3", start=start, end=end)
    assert first.weights.equals(second.weights)
    assert first.gross_returns.equals(second.gross_returns)
    assert first.turnover.equals(second.turnover)


# --------------------------------------------------------------------------- #
# Diagnostics the harness must carry for the reporting layer
# --------------------------------------------------------------------------- #

def test_diagnostics_carry_the_certificate_and_the_condition_number():
    returns = synthetic_returns()
    start, end = window(returns.index, 60, 68)
    result = run_harness(returns, all_eligible, method="B3", start=start, end=end)
    assert list(result.diagnostics.index) == list(result.weights.index)
    for column in ("n_assets", "cond", "residual", "max_violation", "formulation",
                   "solver_status", "solver_iterations"):
        assert column in result.diagnostics.columns
    assert (result.diagnostics["residual"].astype(float) <= 1e-7).all()
    assert (result.diagnostics["n_assets"] == len(ASSETS)).all()
    # The solver's self-report is recorded next to the certificate, so a
    # disagreement between them is visible in the results (finding F17).
    assert (result.diagnostics["solver_status"] == "optimal").all()
    assert result.diagnostics["solver_iterations"].notna().all()


def test_m1_diagnostics_record_the_ledoit_wolf_intensity_and_the_ddof_gap():
    """Spec §4.3 requires delta per fold; finding F16 requires the ddof gap visible."""
    returns = synthetic_returns()
    start, end = window(returns.index, 60, 66)
    result = run_harness(returns, all_eligible, method="M1", start=start, end=end)
    delta = result.diagnostics["shrinkage"].astype(float)
    assert ((delta >= 0.0) & (delta <= 1.0)).all()
    ratio = result.diagnostics["ddof_ratio"].astype(float)
    assert np.allclose(ratio, 60.0 / 59.0)


def test_unknown_methods_are_refused():
    returns = synthetic_returns()
    start, end = window(returns.index, 60, 65)
    with pytest.raises(ValueError, match="unknown method"):
        run_harness(returns, all_eligible, method="B9", start=start, end=end)
    with pytest.raises(ValueError, match="unknown method"):
        backtest.construct("B9", returns.iloc[:60])


def test_every_registered_method_runs_end_to_end():
    returns = synthetic_returns()
    start, end = window(returns.index, 60, 70)
    for method in backtest.METHOD_IDS:
        result = run_harness(returns, all_eligible, method=method, start=start, end=end)
        weights = result.weights.iloc[1:]
        assert np.allclose(weights.sum(axis=1), 1.0, atol=1e-9), method
        assert (weights.to_numpy() >= -1e-9).all(), method
        assert (weights.to_numpy() <= 0.30 + 1e-9).all(), method
        assert result.net_returns(10.0).notna().all(), method
