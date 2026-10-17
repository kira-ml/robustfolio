"""Conformance tests for the engine core (spec §4, §5).

These are the tests that make two claims checkable rather than asserted:

* the optimizer returns what it says it returns -- the constraints hold and the
  solution satisfies the KKT conditions (spec §5.6);
* a solve that is not clean fails loudly instead of silently substituting a
  portfolio (spec §5.7, DEC-20261015-016, risk R-E01).

The certificate tests deliberately do **not** trust the solver. An analytic
interior solution is derived by hand for a diagonal covariance, and the residual
is checked to be zero there and non-zero when that solution is perturbed. That
is what pins the sign conventions in `optimize._mvo_residual`, which would
otherwise be a silent source of false "accepted" verdicts.
"""

from __future__ import annotations

import numpy as np
import pandas as pd
import pytest

from robustfolio import estimators, optimize
from robustfolio.config import GAMMA, W_MAX

NAMES = ["A", "B", "C", "D", "E"]


def diagonal_cov(variances, names=NAMES) -> pd.DataFrame:
    return pd.DataFrame(np.diag(variances), index=names, columns=names)


@pytest.fixture
def correlated_cov() -> pd.DataFrame:
    rng = np.random.default_rng(7)
    factors = rng.normal(scale=0.03, size=(240, 3))
    loadings = np.array(
        [[1.0, 0.0, 0.0], [0.9, 0.2, 0.0], [0.2, 1.0, 0.1],
         [0.0, 0.3, 0.9], [0.5, 0.5, 0.5]]
    )
    returns = factors @ loadings.T + rng.normal(scale=0.01, size=(240, 5))
    frame = pd.DataFrame(returns, columns=NAMES)
    return frame.cov()


# --------------------------------------------------------------------------- #
# Estimators (spec §4)
# --------------------------------------------------------------------------- #

def test_sample_cov_is_unbiased(correlated_cov):
    """Spec §4.2 pins ddof=1, 'matching pandas.DataFrame.cov'."""
    assert list(correlated_cov.index) == NAMES


def test_sample_cov_uses_ddof_one():
    values = np.array([[1.0, 2.0], [2.0, 4.0], [4.0, 8.0]])
    frame = pd.DataFrame(values, columns=["x", "y"])
    assert np.isclose(estimators.sample_cov(frame).loc["x", "x"], np.var(values[:, 0], ddof=1))


def test_ledoit_wolf_intensity_is_a_probability(correlated_cov):
    delta = estimators.ledoit_wolf_shrinkage(
        _returns_from_cov_target(correlated_cov)
    )
    assert 0.0 <= delta <= 1.0


def test_ledoit_wolf_shrinks_off_diagonals():
    returns = _returns_with_strong_correlation()
    sample = estimators.sample_cov(returns)
    shrunk = estimators.ledoit_wolf_cov(returns)
    off = ~np.eye(len(returns.columns), dtype=bool)
    assert np.abs(shrunk.to_numpy()[off]).mean() < np.abs(sample.to_numpy()[off]).mean()
    # the target is constant-variance, so the diagonal is shrunk toward a
    # common value: the spread of the diagonal must not increase
    assert shrunk.to_numpy().diagonal().std() <= sample.to_numpy().diagonal().std()


def test_black_litterman_is_exactly_halfway(correlated_cov):
    """Spec §4.5: mu_BL = (Pi + mu_hat)/2, and tau cancels identically."""
    mu = pd.Series(np.linspace(0.001, 0.005, len(NAMES)), index=NAMES)
    prior = estimators.equilibrium_returns(correlated_cov, gamma=GAMMA)
    posterior = estimators.black_litterman_returns(mu, correlated_cov, gamma=GAMMA)
    assert np.allclose(posterior, 0.5 * (prior + mu))
    # tau does not appear: the reduction is exact, not approximated
    assert np.allclose(posterior, np.asarray(0.5 * (prior + mu)))
    # M2 must differ from B3 in mu only -- the covariances are the same object
    assert estimators.sample_cov(_returns_with_strong_correlation()).shape == correlated_cov.shape


def test_equilibrium_returns_uses_equal_weight_reference(correlated_cov):
    pi = estimators.equilibrium_returns(correlated_cov, gamma=GAMMA)
    expected = GAMMA * correlated_cov.to_numpy() @ np.full(len(NAMES), 1 / len(NAMES))
    assert np.allclose(pi.to_numpy(), expected)


def test_estimators_reject_nan():
    frame = pd.DataFrame(np.ones((5, 2)), columns=["x", "y"])
    frame.iloc[0, 0] = np.nan
    with pytest.raises(ValueError, match="NaN"):
        estimators.sample_cov(frame)


def test_equal_weight_is_exact():
    frame = pd.DataFrame(np.ones((10, 4)), columns=list("abcd"))
    assert np.allclose(estimators.equal_weight(frame).to_numpy(), 0.25)


def test_estimators_are_independent_of_the_frames_memory_layout():
    """Finding F19: the same values must give bit-identical estimates.

    ``DataFrame.mean()`` and ``DataFrame.cov()`` reduce along the frame block's
    strides, and ``pandas`` leaves that block in whichever order the last
    mutation produced. Two frames with identical values but different layout
    therefore gave ULP-different estimates, which would falsify spec §5.4.8's
    bit-identical determinism and -- worse -- would let a leakage test report a
    floating-point artefact of its own perturbation as leaked information.
    """
    rng = np.random.default_rng(7)
    values = rng.normal(scale=0.05, size=(60, 6))
    index = pd.date_range("2007-01-31", periods=60, freq="ME")
    columns = list("ABCDEF")

    canonical = pd.DataFrame(values.copy(), index=index, columns=columns)
    # A deliberately Fortran-ordered frame holding exactly the same values.
    fortran = pd.DataFrame(np.asfortranarray(values), index=index, columns=columns, copy=False)

    assert np.array_equal(canonical.to_numpy(), fortran.to_numpy())
    # If this fails the setup no longer differs in layout, so the test below
    # would pass vacuously and the trigger would need re-deriving.
    assert canonical.to_numpy().flags["C_CONTIGUOUS"]
    assert not fortran.to_numpy().flags["C_CONTIGUOUS"]

    pd.testing.assert_series_equal(
        estimators.sample_mean(canonical), estimators.sample_mean(fortran), check_exact=True
    )
    pd.testing.assert_frame_equal(
        estimators.sample_cov(canonical), estimators.sample_cov(fortran), check_exact=True
    )
    pd.testing.assert_series_equal(
        estimators.inverse_vol(canonical), estimators.inverse_vol(fortran), check_exact=True
    )


def test_sample_cov_reproduces_pandas_bit_for_bit_on_contiguous_input():
    """The F19 fix is a determinism fix, not a numerical deviation (spec §4.2)."""
    rng = np.random.default_rng(11)
    frame = pd.DataFrame(rng.normal(scale=0.04, size=(60, 5)), columns=NAMES)
    assert estimators.sample_cov(frame).to_numpy().tobytes() == frame.cov().to_numpy().tobytes()
    assert estimators.sample_mean(frame).to_numpy().tobytes() == frame.mean().to_numpy().tobytes()


# --------------------------------------------------------------------------- #
# Optimizer: constraints and the feasibility contract (spec §5.1, §5.6, §2)
# --------------------------------------------------------------------------- #

def test_all_constructors_satisfy_the_common_constraint_set(correlated_cov):
    mu = _returns_with_strong_correlation().mean()
    solutions = {
        "B3": optimize.mean_variance(mu, correlated_cov),
        "B4": optimize.minimum_variance(correlated_cov),
        "B5": optimize.mean_variance(
            mu, correlated_cov, w_prev=estimators.equal_weight(_returns_with_strong_correlation()),
            turnover_penalty=0.001,
        ),
        "M1": optimize.mean_variance(mu, estimators.ledoit_wolf_cov(_returns_with_strong_correlation())),
        "B2": optimize.risk_parity(correlated_cov),
    }
    for name, solution in solutions.items():
        w = solution.weights.to_numpy()
        assert np.isclose(w.sum(), 1.0, atol=1e-9), name
        assert (w >= -1e-9).all(), name
        assert (w <= W_MAX + 1e-9).all(), name
        assert solution.max_violation <= optimize.ACCEPT_TOL, name
        assert solution.residual <= optimize.ACCEPT_TOL, name


def test_infeasible_cap_is_a_hard_error():
    """Spec §2: N * w_max < 1 is a hard error, never a silent renormalisation."""
    mu = pd.Series([0.01, 0.01, 0.01], index=list("abc"))
    cov = diagonal_cov([0.01, 0.01, 0.01], names=list("abc"))
    with pytest.raises(optimize.SolverFailure, match="infeasible"):
        optimize.mean_variance(mu, cov, max_weight=0.30)


def test_mismatched_labels_are_rejected(correlated_cov):
    mu = pd.Series(np.full(len(NAMES), 0.01), index=list(reversed(NAMES)))
    with pytest.raises(ValueError, match="labels"):
        optimize.mean_variance(mu, correlated_cov)


def test_turnover_penalty_requires_an_explicit_initial_portfolio(correlated_cov):
    """Finding F18: the initial w^- is unpinned, so it may not be defaulted."""
    mu = _returns_with_strong_correlation().mean()
    with pytest.raises(ValueError, match="F18"):
        optimize.mean_variance(mu, correlated_cov, turnover_penalty=0.001)


def test_determinism(correlated_cov):
    """Spec §5.4.8: identical inputs must give bit-identical weights."""
    mu = _returns_with_strong_correlation().mean()
    first = optimize.mean_variance(mu, correlated_cov).weights
    second = optimize.mean_variance(mu, correlated_cov).weights
    assert first.equals(second)
    assert optimize.risk_parity(correlated_cov).weights.equals(
        optimize.risk_parity(correlated_cov).weights
    )


def test_no_silent_fallback_when_acceptance_fails(correlated_cov, monkeypatch):
    """Spec §5.7. Phase 1 returned 1/N here; the rewrite must raise."""
    mu = _returns_with_strong_correlation().mean()
    monkeypatch.setattr(optimize, "ACCEPT_TOL", 0.0)
    with pytest.raises(optimize.SolverFailure, match="residual|violation"):
        optimize.mean_variance(mu, correlated_cov)


def test_a_solver_that_says_optimal_still_has_to_pass_the_certificate(
    correlated_cov, monkeypatch
):
    """Finding F17: ``status='optimal'`` is the solver's claim, not evidence.

    The failure mode this check exists to catch is a solver that reports success
    at a point which does not satisfy the optimality conditions -- the case
    measured on the frozen universe is CLARABEL returning ``optimal`` with a KKT
    residual of 1.2e-4. The error must therefore name the self-report, or the
    log reads like an ordinary solver crash rather than a disagreement.
    """
    mu = _returns_with_strong_correlation().mean()
    monkeypatch.setattr(optimize, "ACCEPT_TOL", 0.0)
    with pytest.raises(optimize.SolverFailure, match=r"solver reported 'optimal'"):
        optimize.mean_variance(mu, correlated_cov)


def test_solutions_carry_the_solver_self_report(correlated_cov):
    """The results must record the claim *and* the check, so they can disagree."""
    mu = _returns_with_strong_correlation().mean()
    solution = optimize.mean_variance(mu, correlated_cov)
    assert solution.meta["solver_status"] == "optimal"
    assert isinstance(solution.meta["solver_iterations"], int)
    assert solution.meta["solver_iterations"] >= 1


def test_certificate_accepts_the_no_trade_optimum_where_every_weight_is_a_kink():
    """Finding F20.

    When the turnover penalty makes *holding* the drifted portfolio optimal, every
    weight sits exactly on the ``|.|`` kink at once, so there is no smooth
    interior index from which to read the sum multiplier ``nu``. The earlier
    certificate fell back to ``nu = 0`` there and rejected seven optimal B5
    rebalances on the frozen universe with residuals up to 1.5e-3, while CLARABEL,
    SCS and OSQP agreed on the objective to 1e-10 and no feasible exchange
    improved it. The residual is not a warning sign to be tolerated; it was wrong.

    Construction: with equal expected returns and an equal-variance diagonal
    covariance, the unpenalised capped optimum is the equal-weighted portfolio.
    Any positive turnover penalty therefore makes "do not trade" exactly optimal,
    so the solution equals the initial holding and every weight is a kink.
    """
    names = ["A", "B", "C", "D"]
    cov = diagonal_cov([0.04] * 4, names=names)
    mu = pd.Series([0.05] * 4, index=names)

    base = optimize.mean_variance(mu, cov).weights
    assert (base > 1e-6).all() and (base < W_MAX - 1e-6).all(), "need an interior optimum"

    solution = optimize.mean_variance(mu, cov, w_prev=base, turnover_penalty=0.001)

    assert np.allclose(solution.weights.to_numpy(), base.to_numpy(), atol=1e-9)
    assert solution.meta["n_at_kink"] == 4
    # Every box-interior index is simultaneously a kink, so the certificate's
    # "smooth interior" set -- the only source the old version had for nu -- is
    # empty here, which is exactly what made it fall back to nu = 0.
    assert solution.meta["n_interior"] == 4
    assert solution.meta["n_at_floor"] == 0
    assert solution.meta["n_at_cap"] == 0
    assert solution.residual <= 1e-7


def test_certificate_rejects_a_point_that_has_traded_off_the_kink():
    """The mirror of the test above: the kink band must not become a rubber stamp.

    At a kink the stationarity condition is a band of width 2*penalty, so a point
    within it is indistinguishable from optimal. But a weight that has moved *off*
    the kink is held to the smooth condition, which pins the multiplier exactly.
    A perturbation must therefore be rejected, with a residual of the same order as
    the perturbation's gradient effect -- this is the check that stops the F20 fix
    from having traded one broken certificate for another.
    """
    names = ["A", "B", "C", "D"]
    sigma = np.diag([0.04] * 4)
    mu = np.array([0.05] * 4)
    base = np.array([0.25] * 4)
    penalty, cap, gamma = 0.001, W_MAX, 10.0

    # Exactly on the kink: certified, with no smooth interior index to read nu from.
    residual, meta = optimize._mvo_residual(base, mu, sigma, gamma, penalty, base, cap)
    assert meta["n_at_kink"] == 4
    assert residual <= optimize.ACCEPT_TOL

    # Traded 1e-4 off the kink in two directions: the smooth condition binds.
    traded = base.copy()
    traded[0] += 1e-4
    traded[1] -= 1e-4
    residual, meta = optimize._mvo_residual(traded, mu, sigma, gamma, penalty, base, cap)
    assert meta["n_at_kink"] == 2
    assert residual > optimize.ACCEPT_TOL


def test_risk_parity_uncapped_branch_is_accepted_too(monkeypatch):
    """Spec §5.6. The uncapped branch used to return without calling ``_accept``.

    On the frozen universe the cap binds for B2 in 154 of 168 rebalances, so the
    remaining 14 were never acceptance-checked -- a failure could only be silent.
    """
    names = [f"A{i}" for i in range(8)]
    cov = diagonal_cov([0.04] * 8, names=names)  # equal risk -> 1/8 each, cap loose

    solution = optimize.risk_parity(cov)
    assert solution.formulation == "erc"  # the uncapped branch
    assert solution.residual <= 1e-7

    monkeypatch.setattr(optimize, "_erc_residual", lambda *args, **kwargs: 1.0)
    with pytest.raises(optimize.SolverFailure, match="residual"):
        optimize.risk_parity(cov)


# --------------------------------------------------------------------------- #
# Optimizer: optimality
# --------------------------------------------------------------------------- #

def test_minimum_variance_matches_the_analytic_solution_for_diagonal_covariance():
    variances = np.array([0.02, 0.021, 0.022, 0.023, 0.024])
    cov = diagonal_cov(variances)
    analytic = (1.0 / variances) / (1.0 / variances).sum()
    solution = optimize.minimum_variance(cov)
    assert np.allclose(solution.weights.to_numpy(), analytic, atol=1e-7)


def test_certificate_is_zero_at_an_analytic_interior_optimum_and_positive_elsewhere():
    """Pins the sign conventions of the KKT residual without trusting the solver.

    For a diagonal covariance and the box inactive, the mean-variance optimum is
    ``w = (1/gamma) * Sigma^-1 (mu - nu 1)`` with
    ``nu = (1' Sigma^-1 mu - gamma) / (1' Sigma^-1 1)``.
    """
    variances = np.array([0.02, 0.021, 0.022, 0.023, 0.024])
    mu_values = np.array([0.010, 0.009, 0.008, 0.007, 0.006])
    cov = diagonal_cov(variances)
    mu = pd.Series(mu_values, index=NAMES)

    inv = np.diag(1.0 / variances)
    ones = np.ones(len(NAMES))
    nu = (ones @ inv @ mu_values - GAMMA) / (ones @ inv @ ones)
    w_star = inv @ (mu_values - nu) / GAMMA

    assert np.isclose(w_star.sum(), 1.0), "the analytic case must be feasible"
    assert w_star.max() < W_MAX, "the analytic case must have an inactive box"

    sigma = cov.to_numpy()
    residual_star, _ = optimize._mvo_residual(w_star, mu_values, sigma, GAMMA, 0.0, None, W_MAX)
    assert residual_star < 1e-12

    perturbed = w_star.copy()
    perturbed[0] -= 0.02
    perturbed[1] += 0.02
    residual_bad, _ = optimize._mvo_residual(perturbed, mu_values, sigma, GAMMA, 0.0, None, W_MAX)
    assert residual_bad > 1e-4

    solution = optimize.mean_variance(mu, cov)
    assert np.allclose(solution.weights.to_numpy(), w_star, atol=1e-7)
    assert solution.residual < 1e-9, "the solver's own solution must certify clean"


def test_certificate_detects_a_cap_violation():
    """With equal expected returns the mean-variance optimum is minimum variance.

    ``mu'w = mu * 1'w`` is constant on the feasible set, so the risk term decides
    alone -- which makes this an independent analytic check of the same
    certificate on a *capped* problem, where the first-order conditions are
    inequalities rather than equalities.
    """
    variances = np.array([0.02, 0.021, 0.022, 0.023, 0.024])
    mu = pd.Series(np.full(len(NAMES), 0.01), index=NAMES)
    solution = optimize.mean_variance(mu, diagonal_cov(variances))
    analytic = (1.0 / variances) / (1.0 / variances).sum()
    assert np.allclose(solution.weights.to_numpy(), analytic, atol=1e-7)
    assert solution.residual < 1e-9
    assert solution.weights.max() < W_MAX, "the box must stay inactive here"

    capped = optimize.mean_variance(mu, diagonal_cov(variances), max_weight=0.21)
    assert np.isclose(capped.weights.max(), 0.21, atol=1e-7)
    assert capped.residual < 1e-9, "the certificate must hold with a binding cap"


# --------------------------------------------------------------------------- #
# Turnover penalty (B5, spec §5.4)
# --------------------------------------------------------------------------- #

def test_turnover_penalty_pulls_toward_the_previous_portfolio(correlated_cov):
    returns = _returns_with_strong_correlation()
    mu = returns.mean()
    w_prev = pd.Series([0.5, 0.5, 0.0, 0.0, 0.0], index=NAMES)
    unpenalised = optimize.mean_variance(mu, correlated_cov, w_prev=w_prev, turnover_penalty=0.0)
    penalised = optimize.mean_variance(mu, correlated_cov, w_prev=w_prev, turnover_penalty=0.01)
    assert (
        np.abs(penalised.weights - w_prev).sum()
        < np.abs(unpenalised.weights - w_prev).sum()
    )
    assert penalised.residual < 1e-8


def test_uncapped_diagnostic_is_actually_uncapped(correlated_cov):
    """H1.1's uncapped optimizer is a diagnostic, not a baseline (DEC-20261017-020 N2)."""
    vars_ = np.array([0.02, 0.021, 0.022, 0.023, 0.024])
    # a concentrated expected-return vector, so the capped and uncapped
    # problems genuinely differ
    mu = pd.Series([0.04, 0.005, 0.005, 0.005, 0.005], index=NAMES)
    solution = optimize.mean_variance(mu, diagonal_cov(vars_), max_weight=1.0)
    assert solution.weights.max() > W_MAX, "the cap must genuinely be lifted"
    assert np.isclose(solution.weights.sum(), 1.0)
    assert solution.residual < 1e-8
    capped = optimize.mean_variance(mu, diagonal_cov(vars_), max_weight=W_MAX)
    assert np.isclose(capped.weights.max(), W_MAX, atol=1e-7)
    assert capped.weights.max() < solution.weights.max()
    assert capped.residual < 1e-8


# --------------------------------------------------------------------------- #
# Risk parity (B2, spec §5.3)
# --------------------------------------------------------------------------- #

def test_risk_parity_is_inverse_volatility_for_uncorrelated_assets():
    # volatilities chosen so the inverse-volatility solution stays inside the
    # cap; otherwise this is testing the capped path, which the next test does
    vols = np.array([0.04, 0.045, 0.05, 0.055])
    cov = diagonal_cov(vols ** 2, names=list("abcd"))
    solution = optimize.risk_parity(cov)
    expected = (1.0 / vols) / (1.0 / vols).sum()
    assert expected.max() < W_MAX, "the uncapped path must be the one exercised"
    assert solution.formulation == "erc"
    assert np.allclose(solution.weights.to_numpy(), expected, atol=1e-6)


def test_risk_parity_equalises_risk_contributions(correlated_cov):
    solution = optimize.risk_parity(correlated_cov)
    w = solution.weights.to_numpy()
    sigma = correlated_cov.to_numpy()
    rc = w * (sigma @ w)
    assert np.ptp(rc) < 1e-7
    assert solution.residual < optimize.ACCEPT_TOL


def test_risk_parity_handles_a_binding_cap():
    """A low-volatility asset wants far more than w_max; SHY does this for real."""
    vols = np.array([0.005, 0.04, 0.04, 0.04, 0.04])
    cov = diagonal_cov(vols ** 2)
    solution = optimize.risk_parity(cov)
    w = solution.weights.to_numpy()
    assert solution.formulation == "erc_box_constrained"
    assert np.isclose(w.max(), W_MAX, atol=1e-6)
    assert (w <= W_MAX + 1e-9).all()
    assert np.isclose(w.sum(), 1.0, atol=1e-12)
    # the remaining assets share the residual risk budget equally
    rest = np.sort(w[1:])
    assert np.allclose(rest, rest[0], atol=1e-6)
    # and the certification still holds among the uncapped assets
    assert solution.residual < optimize.ACCEPT_TOL


def test_risk_parity_cap_does_not_bind_for_an_equal_volatility_universe():
    cov = diagonal_cov(np.full(5, 0.04 ** 2))
    solution = optimize.risk_parity(cov)
    assert solution.formulation == "erc"
    assert np.allclose(solution.weights.to_numpy(), 1.0 / 5)


# --------------------------------------------------------------------------- #
# Synthetic helpers
# --------------------------------------------------------------------------- #

def _returns_with_strong_correlation() -> pd.DataFrame:
    rng = np.random.default_rng(11)
    market = rng.normal(scale=0.03, size=(240, 1))
    idiosyncratic = rng.normal(scale=0.01, size=(240, 5))
    values = market + idiosyncratic
    return pd.DataFrame(values, columns=NAMES)


def _returns_from_cov_target(cov: pd.DataFrame) -> pd.DataFrame:
    rng = np.random.default_rng(3)
    return pd.DataFrame(
        rng.multivariate_normal(np.zeros(len(cov)), cov.to_numpy(), size=120),
        columns=list(cov.index),
    )
