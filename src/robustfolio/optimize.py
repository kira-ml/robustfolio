"""Convex constructors (spec §5): the mean-variance family, minimum variance, risk parity.

Three properties this module has deliberately, each a reaction to a specific
defect in the Phase 1 code:

1. **No fallback portfolio (spec §5.7).** A solve that is not *accepted* raises
   :class:`SolverFailure` and aborts the run. Phase 1 substituted equal weights
   on any solver failure, which would have hidden solver failures *inside* the
   results (DEC-20261015-016, risk R-E01). There is no code path here that
   returns a portfolio the solver did not produce.

2. **A solver-independent optimality certificate (spec §5.6).** The mandated
   solver is ``cvxpy`` + ``CLARABEL``. CLARABEL does not report a duality gap
   (`problem.solver_stats.extra_stats` is ``None``), so the spec's "duality gap
   <= 1e-7" cannot be read off it. Every solve is instead certified by a KKT
   residual computed **from the primal solution alone** -- stationarity, dual
   feasibility and complementary slackness, with no reliance on the solver's own
   dual variables or sign conventions. See :func:`_mvo_residual`. This deviation
   from the letter of §5.6 is recorded as finding F17.

3. **Uniform constraints (spec §5.1).** The same ``1'w = 1`` and the same box
   ``0 <= w_i <= w_max`` apply to every constructor, including B1 and B2
   (DEC-20261017-019 F1: the Phase 1 harness applied the cap to some methods and
   not others, which made the comparison unfair).

Risk parity (B2) needs more than a QP and is documented separately at
:func:`risk_parity`.
"""

from __future__ import annotations

from dataclasses import dataclass, field

import cvxpy as cp
import numpy as np
import pandas as pd

from .config import ACCEPT_TOL, DIAGONAL_LOADING, GAMMA, SOLVER_TOL, W_MAX

__all__ = [
    "SolverFailure",
    "Solution",
    "mean_variance",
    "minimum_variance",
    "risk_parity",
]


class SolverFailure(RuntimeError):
    """A solve was not accepted. Deliberately fatal -- see spec §5.7 and risk R-E01."""


@dataclass(frozen=True)
class Solution:
    """A weight vector together with the evidence that it is the optimum.

    The certificate fields are what the harness logs per fold; they are the
    artefact that distinguishes "the solver said optimal" from "the solution
    satisfies the optimality conditions".
    """

    weights: pd.Series
    objective: float
    status: str
    max_violation: float
    residual: float
    formulation: str = ""
    meta: dict = field(default_factory=dict)

    def __post_init__(self) -> None:
        if not np.all(np.isfinite(self.weights.to_numpy(dtype=float))):
            raise SolverFailure("accepted solution contains non-finite weights")


# --------------------------------------------------------------------------- #
# Shared validation
# --------------------------------------------------------------------------- #

def _check_inputs(mu: pd.Series, cov: pd.DataFrame, max_weight: float) -> tuple[np.ndarray, np.ndarray, list[str]]:
    if not isinstance(cov, pd.DataFrame):
        raise TypeError("cov must be a pandas DataFrame")
    if not cov.index.equals(cov.columns):
        raise ValueError("cov must have identical row and column labels")
    names = list(cov.index)
    n = len(names)
    if n == 0:
        raise ValueError("empty universe")
    if not isinstance(mu, pd.Series):
        raise TypeError("mu must be a pandas Series")
    if list(mu.index) != names:
        raise ValueError(
            "mu and cov labels disagree; the method set requires one column "
            "ordering (spec §4, lexicographic)"
        )
    if not (0.0 < max_weight <= 1.0):
        raise ValueError(f"max_weight must lie in (0, 1], got {max_weight}")
    # Spec §2 feasibility note: the cap is feasible iff N * w_max >= 1. An
    # infeasible configuration is a hard error, never a silent renormalisation.
    if n * max_weight < 1.0 - 1e-12:
        raise SolverFailure(
            f"infeasible configuration: N * w_max = {n} * {max_weight} = "
            f"{n * max_weight:.6f} < 1 (spec §2)"
        )
    sigma = cov.to_numpy(dtype=float)
    if sigma.shape != (n, n):
        raise ValueError(f"cov must be square {n}x{n}, got {sigma.shape}")
    if not np.all(np.isfinite(sigma)):
        raise ValueError("cov contains non-finite entries")
    return mu.to_numpy(dtype=float), sigma, names


def _load_if_needed(sigma: np.ndarray, label: str) -> tuple[np.ndarray, dict]:
    """Add ``eps * I`` when the matrix is not numerically positive definite.

    Spec §5.3/§5.5 say "diagonal loading ``eps I``, ``eps = 1e-6``, if
    ``Sigma_hat`` is near-singular". The *threshold* for "near-singular" is not
    pinned anywhere; this implementation applies loading exactly when the
    smallest eigenvalue is non-positive, which is the minimal reading and the
    point at which the algorithms are otherwise undefined (``ln`` and the
    quadratic form). The decision is logged either way so it can never be
    silent. A broader threshold would be a new unpinned value and is left to the
    owner.
    """
    eig_min = float(np.linalg.eigvalsh((sigma + sigma.T) / 2.0).min())
    applied = eig_min <= 0.0
    if applied:
        sigma = sigma + DIAGONAL_LOADING * np.eye(sigma.shape[0])
    return sigma, {
        "eig_min": eig_min,
        "diagonal_loading_applied": applied,
        "diagonal_loading": DIAGONAL_LOADING if applied else 0.0,
    }


def _solved(problem: cp.Problem, n: int, *, label: str) -> None:
    """Run the solver and reject anything that is not cleanly solved (spec §5.6).

    The tolerances are passed explicitly rather than left at the solver's
    defaults; see ``config.SOLVER_TOL`` and finding F17. Without them the
    acceptance residual is not attainable and every solve would be rejected.
    """
    try:
        problem.solve(
            solver=cp.CLARABEL,
            tol_gap_abs=SOLVER_TOL,
            tol_gap_rel=SOLVER_TOL,
            tol_feas=SOLVER_TOL,
        )
    except Exception as exc:  # noqa: BLE001 - re-raised with the fold's identity
        raise SolverFailure(f"{label}: solver raised {type(exc).__name__}: {exc}") from exc
    if problem.status not in (cp.OPTIMAL, cp.OPTIMAL_INACCURATE):
        raise SolverFailure(f"{label}: solver status {problem.status!r}, not optimal")


def _max_violation(problem: cp.Problem) -> float:
    """Worst constraint violation, vector constraints included.

    ``Constraint.violation()`` returns a scalar for scalar constraints and an
    array for vector ones, so it cannot be passed straight to ``float``.
    """
    worst = 0.0
    for constraint in problem.constraints:
        violation = constraint.violation()
        if violation is None:
            continue
        values = np.atleast_1d(np.asarray(violation, dtype=float))
        if values.size:
            worst = max(worst, float(np.nanmax(np.abs(values))))
    return worst


# --------------------------------------------------------------------------- #
# Optimality certificate, from the primal solution alone
# --------------------------------------------------------------------------- #

def _mvo_residual(
    w: np.ndarray,
    mu: np.ndarray,
    sigma: np.ndarray,
    risk_aversion: float,
    penalty: float,
    base: np.ndarray | None,
    cap: float,
    tol: float = ACCEPT_TOL,
) -> tuple[float, dict]:
    """KKT residual for the mean-variance family.

    The problem is a **maximisation**:

        max_w  mu'w - (gamma/2) w'Sw - penalty * |w - base|_1
        s.t.   1'w = 1,  0 <= w <= cap

    For a maximisation the KKT system takes the multipliers of the ``g(w) <= 0``
    constraints *subtracted* -- stationarity of

        L = f(w) - nu (1'w - 1) + lo'w - hi' (w - cap),     lo, hi >= 0

    gives, with ``g = mu - gamma S w`` and ``s_i`` a subgradient of
    ``|w_i - base_i|``,

        g_i - penalty * s_i = nu - lo_i + hi_i

    with complementary slackness ``lo_i w_i = 0`` and ``hi_i (cap - w_i) = 0``.
    Hence:

    * interior: ``g_i - penalty s_i == nu``
    * at the cap: ``g_i - penalty s_i >= nu`` (``hi_i`` is the excess)
    * at the floor: ``g_i - penalty s_i <= nu`` (``lo_i`` is the deficit)

    **Sign errors here are invisible**: a flipped ``nu`` turns a certificate into
    a rubber stamp, and a flipped convention is exactly the mistake this function
    first contained. The convention is pinned by checking the residual against an
    analytic interior optimum *and* against a point known to be optimal by direct
    search -- see ``tests/test_conformance.py``.

    For a convex QP the conditions are sufficient, so a small residual *is* a
    certificate of optimality. Nothing here touches the solver's own dual
    variables, which removes any dependence on their sign convention and on the
    solver used (the mandated solver exposes no duality gap -- finding F17).

    ``nu`` is recovered from the indices where both box constraints are inactive
    and the absolute-value term is smooth; the median is used so one
    misclassified index cannot move it. ``tol`` classifies a variable as being at
    a bound: it is the run acceptance tolerance, because a primal solution is
    only certified to that accuracy, so a weight 2e-8 inside the cap *is* at the
    cap for certificate purposes. If no smooth interior index exists the residual
    is computed with ``nu = 0`` and will normally fail -- a loud failure is
    correct (spec §5.7), but this certificate assumes at least one such index,
    which holds for any universe of size >= 4 under the frozen cap.
    """
    n = len(w)
    g = mu - risk_aversion * (sigma @ w)

    if penalty > 0.0:
        base = np.zeros(n) if base is None else np.asarray(base, dtype=float)
        d = w - base
        at_kink = np.abs(d) <= tol
        s_fixed = np.where(d > 0.0, 1.0, np.where(d < 0.0, -1.0, 0.0))
    else:
        at_kink = np.zeros(n, dtype=bool)
        s_fixed = np.zeros(n)

    at_lo = w <= tol
    at_hi = w >= cap - tol
    interior = ~(at_lo | at_hi)
    smooth = interior & ~at_kink

    a = g - penalty * s_fixed
    nu = float(np.median(a[smooth])) if smooth.any() else 0.0

    residual = np.zeros(n)
    fixed = ~at_kink

    # interior: g_i - penalty s_i == nu
    m = interior & fixed
    residual[m] = np.abs(a[m] - nu)
    # interior, at the kink of |.|: any s in [-1, 1] is allowed
    m = interior & at_kink
    residual[m] = np.maximum(0.0, np.abs(g[m] - nu) - penalty)

    # at the cap: need g_i - penalty s_i >= nu, slack is hi_i
    m = at_hi & fixed
    residual[m] = np.maximum(0.0, nu - a[m])
    m = at_hi & at_kink
    residual[m] = np.maximum(0.0, nu - g[m] - penalty)

    # at the floor: need g_i - penalty s_i <= nu, slack is lo_i
    m = at_lo & fixed
    residual[m] = np.maximum(0.0, a[m] - nu)
    m = at_lo & at_kink
    residual[m] = np.maximum(0.0, g[m] - penalty - nu)

    value = float(np.max(residual)) if n else 0.0
    return value, {
        "nu": nu,
        "n_interior": int(interior.sum()),
        "n_at_cap": int(at_hi.sum()),
        "n_at_floor": int(at_lo.sum()),
    }


# --------------------------------------------------------------------------- #
# Mean-variance family (B3, B5, M1, M2, and the B3 uncapped diagnostic)
# --------------------------------------------------------------------------- #

def mean_variance(
    mu: pd.Series,
    cov: pd.DataFrame,
    *,
    w_prev: pd.Series | None = None,
    turnover_penalty: float = 0.0,
    max_weight: float = W_MAX,
    risk_aversion: float = GAMMA,
    label: str = "MVO",
) -> Solution:
    """``max_w  mu'w - (gamma/2) w'Sw - penalty * ||w - w_prev||_1`` s.t. §5.1.

    Solved as a convex QP with auxiliary variables ``u_i >= +-(w_i - w_prev_i)``,
    never by subgradient descent (spec §5.4; the Phase 1 SLSQP path used both a
    subgradient and an equal-weight fallback, DEC-20261015-016).

    Instantiations (spec §5.4):

    ==========  ==============  ============  ====================  ========
    Method      mu              Sigma         penalty               w_prev
    ==========  ==============  ============  ====================  ========
    B3          sample          sample        0                     --
    B5          sample          sample        kappa = 0.001         drifted
    M1          sample          Ledoit-Wolf   0                     --
    M2          B-L posterior   sample        0                     --
    ==========  ==============  ============  ====================  ========

    ``max_weight=1.0`` reproduces the H1.1 uncapped diagnostic; that output is a
    diagnostic, never a baseline, and is excluded from the comparison table and
    from any cost or Sharpe claim (protocol §7 H1.1; DEC-20261017-020 N2).
    """
    mu_v, sigma, names = _check_inputs(mu, cov, max_weight)
    n = len(names)
    base = None
    if turnover_penalty > 0.0:
        if w_prev is None:
            # The initial w^- at the first rebalance of a run is not pinned by
            # the protocol or the spec (finding F18). Refusing here rather than
            # defaulting keeps the choice visible in the caller and logged in
            # the run, instead of buried in a library default. Resolved as
            # "start flat" (w^- = 0) by DEC-20261017-029; the harness reads
            # config.INITIAL_HOLDING_MODE and passes the zeros.
            raise ValueError(
                "turnover_penalty > 0 requires w_prev: the initial w^- is not "
                "pinned by the protocol or spec (finding F18), so it must be "
                "supplied explicitly by the caller and recorded"
            )
        if list(w_prev.index) != names:
            raise ValueError("w_prev labels disagree with the covariance labels")
        base = w_prev.to_numpy(dtype=float)

    w = cp.Variable(n)
    objective = mu_v @ w - (risk_aversion / 2.0) * cp.quad_form(w, cp.psd_wrap(sigma))
    constraints = [cp.sum(w) == 1.0, w >= 0.0, w <= max_weight]
    if turnover_penalty > 0.0:
        u = cp.Variable(n, nonneg=True)
        constraints += [u >= w - base, u >= -(w - base)]
        objective = objective - turnover_penalty * cp.sum(u)

    problem = cp.Problem(cp.Maximize(objective), constraints)
    _solved(problem, n, label=label)

    w_val = np.asarray(w.value, dtype=float).ravel()
    violation = _max_violation(problem)
    residual, meta = _mvo_residual(
        w_val, mu_v, sigma, risk_aversion, turnover_penalty, base, max_weight
    )
    _accept(label, violation, residual)
    return Solution(
        weights=pd.Series(w_val, index=names),
        objective=float(problem.value),
        status=problem.status,
        max_violation=violation,
        residual=residual,
        formulation="l1_epigraph" if turnover_penalty > 0.0 else "quadratic",
        meta=meta,
    )


def minimum_variance(
    cov: pd.DataFrame,
    *,
    max_weight: float = W_MAX,
    label: str = "B4",
) -> Solution:
    """``min_w w'Sw`` s.t. §5.1 (spec §5.5).

    Equivalent to §5.4 with ``mu = 0``; ``gamma`` is inert, so it is fixed at 1
    and never exposed, to stop a caller "tuning" a parameter that cannot matter.
    """
    zero_mu = pd.Series(np.zeros(cov.shape[0]), index=list(cov.index))
    return mean_variance(
        zero_mu,
        cov,
        turnover_penalty=0.0,
        max_weight=max_weight,
        risk_aversion=1.0,
        label=label,
    )


# --------------------------------------------------------------------------- #
# Risk parity (B2)
# --------------------------------------------------------------------------- #

def _ccd_risk_budgeting(
    sigma: np.ndarray,
    budgets: np.ndarray,
    cap: float | None = None,
    tol: float = 1e-13,
    max_iter: int = 50_000,
) -> np.ndarray:
    """Cyclically-coordinate-descent risk budgeting (spec §5.3).

    Solves, in the **unnormalised** scale,

        min_{w > 0}  1/2 w'Sw - sum_i b_i ln w_i     s.t. w_i <= cap

    by Spinu (2013) / Griveau-Billion, Richard & Roncalli (2013) coordinate
    descent. For coordinate *i*, stationarity of the objective is

        S_ii w_i^2 + (sum_{j != i} S_ij w_j) w_i - b_i = 0

    and the update takes the positive root, clipped at ``cap``. The unnormalised
    solution satisfies ``w_i (Sw)_i = b_i`` exactly for every uncapped ``i``;
    normalising multiplies every risk contribution by the same positive
    constant, so relative risk contributions -- the thing risk parity is *about*
    -- are preserved.

    Returns the unnormalised vector. The caller normalises.
    """
    n = sigma.shape[0]
    w = np.full(n, 1.0 / n, dtype=float)
    for _ in range(max_iter):
        w_prev = w.copy()
        for i in range(n):
            a = sigma[i, i]
            if a <= 0.0:
                raise SolverFailure(f"risk parity: non-positive variance for asset {i}")
            b = float(sigma[i] @ w) - a * w[i]
            wi = (-b + np.sqrt(b * b + 4.0 * a * budgets[i])) / (2.0 * a)
            if cap is not None and wi > cap:
                wi = cap
            w[i] = wi
        if np.max(np.abs(w - w_prev)) <= tol * max(1.0, float(np.max(w))):
            return w
    raise SolverFailure("risk parity: coordinate descent did not converge")


def _erc_residual(w: np.ndarray, sigma: np.ndarray, cap: float, tol: float = 1e-7) -> float:
    """Max pairwise difference of risk contributions among *uncapped* assets.

    Spec §5.3: "max_{i,j} |RC_i - RC_j| < 1e-8 among uncapped assets". The
    tolerance applied here is the run acceptance tolerance, not the tighter
    convergence target, because this is the check that *certifies* the solve.
    """
    rc = w * (sigma @ w)
    uncapped = w < cap - tol
    if uncapped.sum() < 2:
        return 0.0
    values = rc[uncapped]
    return float(values.max() - values.min())


def risk_parity(
    cov: pd.DataFrame,
    *,
    max_weight: float = W_MAX,
    label: str = "B2",
) -> Solution:
    """Equal-risk-contribution portfolio subject to §5.1 (spec §5.3).

    **Why this is not a QP.** The log-barrier formulation

        min_{w > 0}  1/2 w'Sw - (1/N) sum_i ln w_i     [then normalise]

    pins the risk contributions to ``1/N`` each, but it has no ``1'w = 1``
    constraint: the scale is set by the balance between the quadratic and the
    barrier. Imposing ``1'w = 1`` on that problem does *not* give equal risk
    contributions, and capping the unnormalised ``w`` is meaningless because the
    normalisation factor is ~30x here (the unnormalised solution satisfies
    ``w'Sw = 1``, i.e. its sum is large).

    The cap therefore has to be pushed through the normalisation. The solution
    used is a convex homotopy: bisect on the *unnormalised* cap level ``k`` until
    the normalised maximum equals ``w_max``. Each step of the bisection is a
    convex problem solved by coordinate descent, so the whole procedure is
    deterministic and convex at every step, and the result is the constrained
    minimum of the least-squares risk-budgeting problem named in §5.3 -- among
    uncapped assets the risk contributions are equal, and the capped ones sit
    exactly on the bound. Which of the two formulations was used is reported in
    ``formulation`` and logged per fold.

    The bisection exists because the cap genuinely binds for this universe:
    ``SHY`` (1-3y Treasuries) wants far more than 30% of an equal-risk portfolio.
    """
    _, sigma, names = _check_inputs(
        pd.Series(np.zeros(cov.shape[0]), index=list(cov.index)), cov, max_weight
    )
    sigma, load_meta = _load_if_needed(sigma, label)
    n = len(names)
    budgets = np.full(n, 1.0 / n)

    raw = _ccd_risk_budgeting(sigma, budgets)
    w = raw / raw.sum()
    if float(w.max()) <= max_weight + 1e-12:
        return Solution(
            weights=pd.Series(w, index=names),
            objective=float(w @ sigma @ w),
            status="optimal",
            max_violation=max(0.0, float(w.max()) - max_weight),
            residual=_erc_residual(w, sigma, max_weight),
            formulation="erc",
            meta={**load_meta, "cap": float(raw.max())},
        )

    # The cap binds: find the unnormalised cap level whose normalised maximum
    # is exactly w_max. m(k) is non-decreasing in k (a looser cap on the raw
    # vector loosens the normalised maximum), with m(0+) = 1/N and
    # m(k_raw_max) = the uncapped normalised maximum.
    k_hi = float(raw.max())

    def normalised_max(k: float) -> float:
        r = _ccd_risk_budgeting(sigma, budgets, cap=k)
        return float(r.max() / r.sum())

    k_lo = k_hi
    for _ in range(200):
        k_lo *= 0.5
        if normalised_max(k_lo) <= max_weight:
            break
    else:
        raise SolverFailure(f"{label}: could not bracket the cap level")

    for _ in range(200):
        k_mid = 0.5 * (k_lo + k_hi)
        if normalised_max(k_mid) <= max_weight:
            k_lo = k_mid
        else:
            k_hi = k_mid
        if k_hi - k_lo <= 1e-15 * max(1.0, k_hi):
            break

    raw = _ccd_risk_budgeting(sigma, budgets, cap=k_hi)
    w = raw / raw.sum()
    violation = max(0.0, float(w.max()) - max_weight)
    residual = _erc_residual(w, sigma, max_weight)
    _accept(label, violation, residual)
    return Solution(
        weights=pd.Series(w, index=names),
        objective=float(w @ sigma @ w),
        status="optimal",
        max_violation=violation,
        residual=residual,
        formulation="erc_box_constrained",
        meta={
            **load_meta,
            "cap_level_raw": k_hi,
            "n_at_cap": int((w >= max_weight - 1e-7).sum()),
            "n_bisection_note": "normalised maximum pinned to w_max",
        },
    )


# --------------------------------------------------------------------------- #
# Acceptance
# --------------------------------------------------------------------------- #

def _accept(label: str, violation: float, residual: float) -> None:
    """Spec §5.6 acceptance. Either check failing aborts the run."""
    if violation > ACCEPT_TOL:
        raise SolverFailure(
            f"{label}: max constraint violation {violation:.3e} > {ACCEPT_TOL:.0e}"
        )
    if residual > ACCEPT_TOL:
        raise SolverFailure(
            f"{label}: optimality residual {residual:.3e} > {ACCEPT_TOL:.0e} "
            "(stationarity / dual feasibility / complementary slackness)"
        )
