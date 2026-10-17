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

#: Confidence levels: 90% for reporting, 95% for decision thresholds
#: (protocol §13.1). Two constants because the protocol really does use two.
CI_LEVEL_REPORT = 0.90
CI_LEVEL_DECISION = 0.95

#: Registered multiple-testing family size for the confirmatory family
#: (protocol §12.6; finding F13 resolved as N = 1 by DEC-20261017-027).
DSR_FAMILY_SIZE = 1

#: Euler-Mascheroni constant, as named in the DSR definition (spec §7.10).
EULER_MASCHERONI = 0.5772156649015329

# --- decision thresholds (protocol §6; confirmed at freeze) ----------------- #

#: §6.1 statistical significance: DSR p-value below this, with SR* = SR_0...
DSR_PVALUE_MAX = 0.05

#: ...and PSR above this, with SR* = the best baseline's observed Sharpe.
PSR_MIN = 0.95

#: §6.2 economic materiality: minimum net-Sharpe improvement over the best
#: baseline at the headline cost level.
MATERIALITY_SHARPE_GAP = 0.20

#: §6.2: turnover may not exceed this multiple of the best baseline's.
MATERIALITY_TURNOVER_MULTIPLE = 2.0

#: §6.2: maximum drawdown may not be worse than the best baseline's by more
#: than this, in absolute return terms (5 percentage points).
MATERIALITY_DRAWDOWN_SLACK = 0.05

#: §6.3 robustness: the advantage must hold at this many of the five §5.5.3
#: cost levels.
ROBUSTNESS_COST_LEVELS = 3

#: §6.3: and in this fraction of walk-forward folds (>= 60% of 14 folds = 9),
#: and no single fold may contribute more than this fraction of the total
#: advantage.
ROBUSTNESS_FOLD_FRACTION = 0.60
ROBUSTNESS_FOLD_SHARE_MAX = 0.40

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
#: reading rejects every fold. The accuracy actually achieved is a function of
#: this tolerance, and *not* monotonically:
#:
#:   ==========  ===========  ==================  ==================
#:   tol         status       worst residual      over acceptance tol
#:   ==========  ===========  ==================  ==================
#:   1e-8        optimal      1.2e-4              (solver defaults)
#:   1e-12       optimal      7.9e-7              15 of 1176
#:   1e-13       optimal      1.1e-8              0
#:   1e-14       optimal      1.5e-11             0   <- used
#:   1e-15       optimal      1.1e-4              41
#:   1e-16       optimal      5.4e-3              132
#:   ==========  ===========  ==================  ==================
#:
#: The 1e-8 row is the solver default, measured on the first fold. Every other row
#: is the whole frozen run -- 7 methods x 168 rebalances = 1176 solves -- measured
#: by ``scripts/certify_engine.py`` *after* the certificate fixes (findings F20 and
#: F21). The non-monotonicity is the point: 1e-13 is three orders of magnitude
#: worse than 1e-14 in the worst case, and both 1e-15 and 1e-16 are far worse than
#: 1e-12. Asking the solver to be more exact is not how exactness is obtained.
#:
#: 1e-14 is the operating point: zero rejections across all 1176 solves and a worst
#: residual four orders of magnitude inside the acceptance threshold, while going
#: tighter *decreases* accuracy because the solver gives up and returns
#: ``optimal_inaccurate``. The spec's intent -- that the residual check binds -- is
#: honoured; the explicit tolerance is the only way to honour it. Both this and the
#: "duality gap" substitution are **finding F17**, resolved as reading (a) by
#: DEC-20261017-029.
SOLVER_TOL = 1e-14
