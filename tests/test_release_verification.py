"""The verifier's own comparison logic, which is now a load-bearing claim.

``scripts/verify_release.py`` is the command the README invites a stranger to run.
Its comparison was "tolerance exactly zero" until CI disagreed twice: once on one
column by 4.2e-17 (F33) and once on thirteen columns by 4.698e-12 (F34). The fix
splits the claim -- decisions exact, measurements bounded -- and this file tests
the split rather than the numbers, using synthetic tables so the tests are
hermetic and run on a fresh clone. One test reads the committed
``docs/published-run/decisions.csv`` instead, because its subject *is* that artifact:
whether the verifier's hand-written list of exact columns still covers the fields the
generator actually writes.

The property that matters: a difference far too small to change any decision must
pass, and a difference large enough to change one must fail.
"""

from __future__ import annotations

import math
import sys
from pathlib import Path

import numpy as np
import pandas as pd
import pytest

REPO_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO_ROOT / "scripts"))

import verify_release as vr  # noqa: E402
from robustfolio import report as reporting  # noqa: E402


def _table(**overrides: float) -> pd.DataFrame:
    """Seven methods with the published shape: five baselines, two candidates."""
    base = {
        "rebalances": 168.0,
        "folds": 14.0,
        "headline_cost_bps": 10.0,
        "net_sharpe": 0.5,
        "turnover_annualized": 0.4,
        "cvar95": -0.05,
    }
    base.update(overrides)
    net = {
        "B1": 0.5482, "B2": 0.4519, "B3": 0.7896, "B4": 0.1820, "B5": 0.7843,
        "M1": 0.7860, "M2": 0.8538,
    }
    rows = {}
    for method, sharpe in net.items():
        row = dict(base)
        row["net_sharpe"] = sharpe
        rows[method] = row
    return pd.DataFrame.from_dict(rows, orient="index")


def test_an_identical_table_is_exact() -> None:
    published = _table()
    worst, offenders, problems = vr.compare(published.copy(), published)
    assert worst == 0.0
    assert offenders == []
    assert problems == []


def test_platform_noise_passes_and_is_reported_as_a_number() -> None:
    """4.698e-12 is what two platforms actually disagreed by (F34).

    That is seven orders of magnitude below the four decimals the report prints, and
    the tolerance is ~200x it while still five orders below them. Both of those
    ratios are asserted by
    ``test_the_tolerance_is_a_documented_constant_not_a_hidden_one`` rather than
    trusted to this sentence. It must pass, and the verifier must still say what it
    saw rather than rounding to 'exact'.
    """
    published = _table()
    recomputed = published.copy()
    recomputed.loc["M2", "net_sharpe"] += 4.698e-12
    recomputed.loc["B3", "turnover_annualized"] += 4.307e-12

    worst, offenders, problems = vr.compare(recomputed, published)

    assert worst == pytest.approx(4.698e-12, rel=1e-3)
    assert offenders == []
    assert problems == []


def test_a_difference_that_could_change_a_verdict_fails() -> None:
    """The §6.2 materiality bar is 0.20 Sharpe; the §6.1 bar is PSR 0.95.

    Anything near those is a different result, not a rounding difference, and the
    tolerance must not absorb it.
    """
    published = _table()
    recomputed = published.copy()
    recomputed.loc["M2", "net_sharpe"] += 1e-6

    worst, offenders, problems = vr.compare(recomputed, published)

    assert worst == pytest.approx(1e-6)
    assert offenders == ["net_sharpe"]
    assert problems == []


def test_a_changed_rebalance_count_fails_even_when_every_metric_is_within_tolerance() -> None:
    """The discrete checks are what the tolerance cannot excuse."""
    published = _table()
    recomputed = published.copy()
    recomputed["rebalances"] = 167.0
    recomputed["net_sharpe"] = published["net_sharpe"]  # every metric unchanged

    worst, offenders, problems = vr.compare(recomputed, published)

    assert worst == 0.0, "the only difference is the count itself"
    assert offenders == [], "and it is not a tolerance question"
    assert any("rebalances" in problem for problem in problems)


def test_a_changed_ranking_fails() -> None:
    """§6.3 counts fold wins by rank; a reordering is a different decision."""
    published = _table()
    recomputed = published.copy()
    recomputed.loc["B4", "net_sharpe"] = 0.95

    _, offenders, problems = vr.compare(recomputed, published)

    assert offenders == ["net_sharpe"]
    assert any("ranking" in problem for problem in problems)


def test_a_changed_best_baseline_fails() -> None:
    """§6.1/§6.2 benchmark every candidate against the best baseline.

    If the rule selects a different one, no candidate is being compared to the
    same thing -- even if every number is within a rounding error of the old one.
    """
    published = _table()
    recomputed = published.copy()
    recomputed.loc["B5", "net_sharpe"] = 0.81  # above B3

    _, _, problems = vr.compare(recomputed, published)

    assert any("best baseline" in problem for problem in problems)


def test_a_changed_method_set_fails() -> None:
    published = _table()
    recomputed = published.drop(index="B4")

    worst, offenders, problems = vr.compare(recomputed, published)

    assert worst == float("inf")
    assert offenders == []
    assert any("method set" in problem for problem in problems)


def test_the_tolerance_is_a_documented_constant_not_a_hidden_one() -> None:
    """A tolerance that floats is a tolerance nobody can audit.

    It must stay well above the platform noise it exists to absorb (4.7e-12) and
    well below any quantity a decision is made on (the tightest is 0.20).

    The *margin* below the printed precision is derived here from the tolerance and
    the report's own printed precision rather than restated. It had been written
    into six artefacts and three had drifted: "six orders" where the ratio is five,
    "six decimals" where the report prints four, and one instance wrapped across a
    line break so that no text search could find it at all. A margin with three
    variants is a number written down twice (F29), so this test is its one home.
    """
    assert vr.TOLERANCE == 1e-9
    assert 4.698e-12 * 10 < vr.TOLERANCE
    assert vr.TOLERANCE < 1e-4
    assert set(vr.EXACT_COLUMNS) == {"rebalances", "folds", "headline_cost_bps"}

    printed = 10.0 ** -reporting.PRINTED_DECIMALS
    margin = math.log10(printed / vr.TOLERANCE)
    assert round(margin) == 5, (
        f"the tolerance is {margin:.1f} orders below the "
        f"{reporting.PRINTED_DECIMALS} printed decimals, but every artefact that "
        "states the margin says five"
    )
    assert round(math.log10(printed / 4.698e-12)) == 7, (
        "the worst cross-platform difference (F34) is seven orders below the printed "
        "precision, as the verifier's comments say"
    )
    assert 100 < vr.TOLERANCE / 4.698e-12 < 1000, "described as ~200x the measured noise"


def test_the_headline_metric_is_the_one_the_decision_rules_use() -> None:
    """If §2's deciding metric were renamed, the exact ranking check would go blind."""
    assert vr.HEADLINE_METRIC in reporting.CANDIDATE_IDS or vr.HEADLINE_METRIC == "net_sharpe"
    assert vr.HEADLINE_METRIC == "net_sharpe", (
        "protocol §2 makes net Sharpe the deciding metric; the verifier's ranking "
        "and best-baseline checks read this name"
    )


def test_blank_columns_are_ignored_rather_than_failed() -> None:
    """The verifier compares the intersection, so a richer published table is fine."""
    published = _table()
    published["net_sharpe_ci_low"] = np.nan  # only produced with bootstrap=True
    recomputed = _table()

    worst, offenders, problems = vr.compare(recomputed, published)

    assert worst == 0.0
    assert offenders == []
    assert problems == []


# --------------------------------------------------------------------------- #
# The verdict table: the half of the claim that arrives with decisions.csv
# --------------------------------------------------------------------------- #

def _decisions() -> pd.DataFrame:
    """Two candidates with the published verdict shape (a subset of the 35 fields).

    The values are M1/M2's published ones so a reader can line this fixture up with
    ``docs/published-run/decisions.csv``, but nothing below depends on them: the
    subject is the exact/bounded split, not the numbers.
    """
    rows = {
        "M1": {
            "baseline": "B3",
            "dsr_family_size": 1, "dsr_v_is_convention": True,
            "cost_levels_won": 2, "cost_levels_required": 2,
            "folds_won": 6, "folds_required": 6,
            "pass_psr": False, "pass_dsr": True, "pass_sharpe_gap": False,
            "pass_turnover": False, "pass_drawdown": True,
            "pass_cost_levels": True, "pass_folds": True, "pass_fold_share": True,
            "statistical": False, "material": False, "robust": False,
            "verdict": "FAILURE",
            "psr": 0.49498722172115786,
            "dsr_pvalue": 0.0031928282918427486,
            "sharpe_gap": -0.0036218597549328687,
            "max_fold_share": 0.505,
            "turnover_ratio": 0.895,
        },
        "M2": {
            "baseline": "B3",
            "dsr_family_size": 1, "dsr_v_is_convention": True,
            "cost_levels_won": 2, "cost_levels_required": 2,
            "folds_won": 10, "folds_required": 6,
            "pass_psr": False, "pass_dsr": True, "pass_sharpe_gap": False,
            "pass_turnover": True, "pass_drawdown": True,
            "pass_cost_levels": True, "pass_folds": True, "pass_fold_share": False,
            "statistical": False, "material": False, "robust": False,
            "verdict": "FAILURE",
            "psr": 0.5874181993286492,
            "dsr_pvalue": 0.0016589151882665178,
            "sharpe_gap": 0.06422889810101624,
            "max_fold_share": 0.513,
            "turnover_ratio": 0.981,
        },
    }
    return pd.DataFrame.from_dict(rows, orient="index")


def test_an_identical_verdict_table_is_exact() -> None:
    published = _decisions()
    worst, offenders, problems = vr.compare_decisions(published.copy(), published)

    assert worst == 0.0
    assert offenders == []
    assert problems == []


def test_a_statistic_inside_the_verdict_table_may_move() -> None:
    """psr and dsr_pvalue are measurements; platform noise must not fail them."""
    published = _decisions()
    recomputed = published.copy()
    recomputed.loc["M2", "psr"] += 4.698e-12
    recomputed.loc["M1", "dsr_pvalue"] += 4.2e-17

    worst, offenders, problems = vr.compare_decisions(recomputed, published)

    assert worst == pytest.approx(4.698e-12, rel=1e-3)
    assert offenders == []
    assert problems == []


def test_a_statistic_beyond_tolerance_fails() -> None:
    published = _decisions()
    recomputed = published.copy()
    recomputed.loc["M1", "psr"] -= 0.01

    worst, offenders, problems = vr.compare_decisions(recomputed, published)

    assert offenders == ["psr"]
    assert problems == []


def test_a_flipped_verdict_fails_however_little_the_statistics_moved() -> None:
    """The one comparison that must never be made with a tolerance.

    Both candidates pass the DSR and fail the PSR, so a reader checking only the
    metric table would call this a pass. If an archive reproduces every statistic
    and reports the opposite verdict, the archive is wrong -- the *result* changed,
    not the measurement.
    """
    published = _decisions()
    recomputed = published.copy()
    recomputed.loc["M2", "verdict"] = "SUCCESS"

    worst, offenders, problems = vr.compare_decisions(recomputed, published)

    assert worst == 0.0
    assert offenders == []
    assert any("VERDICT differs" in problem for problem in problems)


def test_a_gate_contradicting_its_own_statistic_still_fails() -> None:
    """A gate is compared as a decision, never recomputed from the metrics.

    ``pass_fold_share`` is False here while ``max_fold_share`` is 0.513 against a
    0.50 limit. Recomputing the gate from the metric would silently agree with the
    archive; comparing the gate catches an archive that disagrees with itself.
    """
    published = _decisions()
    recomputed = published.copy()
    recomputed.loc["M2", "pass_fold_share"] = True

    worst, offenders, problems = vr.compare_decisions(recomputed, published)

    assert worst == 0.0
    assert offenders == []
    assert any("pass_fold_share differs" in problem for problem in problems)


def test_a_changed_candidate_set_fails() -> None:
    published = _decisions()
    recomputed = published.iloc[[0]]

    worst, offenders, problems = vr.compare_decisions(recomputed, published)

    assert worst == float("inf")
    assert any("candidate set" in problem for problem in problems)


def test_every_boolean_in_the_published_verdict_table_is_compared_exactly() -> None:
    """A boolean in decisions.csv is a decision, and the list is hand-written.

    ``DECISION_EXACT_COLUMNS`` is maintained by hand while the table is generated, so
    the two can drift: a new gate added to the artifact would be compared within a
    tolerance without anyone noticing. So the booleans are *derived* from the
    committed artifact's dtypes rather than listed a second time here.
    """
    path = REPO_ROOT / "docs" / "published-run" / "decisions.csv"
    published = pd.read_csv(path, index_col=0, float_precision="round_trip")

    booleans = [c for c in published.columns if pd.api.types.is_bool_dtype(published[c])]
    assert booleans, "the published verdict table carries its gates as booleans"

    missing = [c for c in booleans if c not in vr.DECISION_EXACT_COLUMNS]
    assert missing == [], f"boolean decision fields compared within a tolerance: {missing}"
    assert "verdict" in vr.DECISION_EXACT_COLUMNS, "the published sentence itself"

    extra = [c for c in vr.DECISION_EXACT_COLUMNS if c not in published.columns]
    assert extra == [], f"the verifier compares fields the artifact does not carry: {extra}"
