"""Frozen configuration values.

`model_and_method_spec.md` §2 says these values are *read from the protocol* and
that the table exists "so the implementation has one source of truth in code".
This module is that single source. Nothing here may be changed without a
decision-log entry that amends the protocol or the spec.

Every value carries its source so a reader can check it without leaving the file.
"""

from __future__ import annotations

# --- method-set parameters ------------------------------------------------- #

#: Risk aversion for the mean-variance family (protocol §4.3).
GAMMA = 10.0

#: Per-asset cap, applied uniformly to every method including B1 and B2
#: (protocol §4.3; DEC-20261017-019 F1).
W_MAX = 0.30

#: Turnover penalty for B5, in monthly return per unit of one-way turnover
#: (protocol §4.4 B5, §5.5.6). lambda = kappa.
TURNOVER_PENALTY = 0.001

#: Cost levels in basis points, one-way (protocol §5.5.3). The headline is 10.
COST_LEVELS_BPS = (0, 5, 10, 20, 50)
COST_HEADLINE_BPS = 10

# --- walk-forward window --------------------------------------------------- #

#: Estimation window in months; rolling, re-estimated monthly (protocol §5.2).
ESTIMATION_WINDOW = 60

#: Test window and step in months, non-overlapping (protocol §5.2).
TEST_WINDOW = 12
STEP = 12

#: Initial holding at the first rebalance of a run (finding F18, resolved by
#: DEC-20261017-029). The out-of-sample period starts flat, so ``w^- = 0``: the
#: first rebalance buys 100% and pays one month of the headline cost. Every
#: method pays the same entry cost, so the comparison stays fair. Under
#: ``w >= 0`` the L1 penalty is then exactly constant at that rebalance, so B5's
#: first month equals unpenalised MVO -- which is correct, because there is no
#: prior holding to penalise. ``optimize.mean_variance`` still refuses a
#: ``turnover_penalty > 0`` call with no explicit ``w_prev``: the harness reads
#: this constant and passes the zeros, so the choice is logged, never defaulted.
INITIAL_HOLDING_MODE = "flat"

# --- universe / eligibility ------------------------------------------------ #

#: Minimum consecutive months of history at entry (protocol §5.4.2).
MIN_HISTORY_MONTHS = 60

#: Trailing-3-month average dollar volume floor, USD (protocol §5.4.2).
ADV_FLOOR_USD = 5e6

#: Forward-fill limit for daily gaps, in days (protocol §5.4.6).
MAX_FFILL_DAYS = 3

# --- statistics ------------------------------------------------------------ #

#: Bootstrap seed (spec §7.11; resolves O7). Recorded in every run manifest.
SEED = 20261017

#: Stationary-block-bootstrap mean block length in months (protocol §13.1).
BOOTSTRAP_BLOCK_MEAN = 6

#: Bootstrap replications (protocol §13.1).
BOOTSTRAP_REPS = 2000

# --- solver acceptance ----------------------------------------------------- #

#: Acceptance tolerance: max constraint violation and the optimality residual
#: must both be at or below this (spec §5.6, resolving O4).
ACCEPT_TOL = 1e-7

#: Diagonal loading applied to a covariance that is not numerically positive
#: definite (spec §5.3, §5.5).
DIAGONAL_LOADING = 1e-6

#: Solver tolerances passed to CLARABEL.
#:
#: Spec §5.6 says two things that cannot both hold: "**Tolerance:** solver
#: defaults", and "a fold is accepted only if ... the KKT residual / constraint
#: violation check passes at 1e-7" (the O4 note adds "duality gap <= 1e-7"). On
#: the frozen universe CLARABEL's *defaults* return a point whose KKT residual is
#: ~1.2e-4 -- three orders of magnitude above the required 1e-7 -- so the default
#: reading rejects every fold. The residual is a pure function of this tolerance:
#:
#:   ==========  ==================  ===================
#:   tol         solver status       KKT residual
#:   ==========  ==================  ===================
#:   1e-8        optimal             1.2e-4   (defaults)
#:   1e-10       optimal             4.4e-6
#:   1e-12       optimal             5.6e-7
#:   1e-14       optimal             1.9e-12  <- used
#:   1e-16       optimal_inaccurate  4.4e-6   (degrades)
#:   ==========  ==================  ===================
#:
#: 1e-14 is the operating point: it clears the acceptance threshold by ~5 orders
#: of magnitude, while going tighter *decreases* accuracy because the solver gives
#: up and returns ``optimal_inaccurate``. The spec's intent -- that the residual
#: check binds -- is honoured; the explicit tolerance is the only way to honour
#: it. Both this and the "duality gap" substitution are **finding F17**, resolved
#: as reading (a) by DEC-20261017-029.
SOLVER_TOL = 1e-14
