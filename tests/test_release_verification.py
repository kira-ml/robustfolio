"""The verifier's own comparison logic, which is now a load-bearing claim.

``scripts/verify_release.py`` is the command the README invites a stranger to run.
Its comparison was "tolerance exactly zero" until CI disagreed twice: once on one
column by 4.2e-17 (F33) and once on thirteen columns by 4.698e-12 (F34). The fix
splits the claim -- decisions exact, measurements bounded -- and this file tests
the split rather than the numbers, using synthetic tables so the tests are
hermetic and run on a fresh clone.

The property that matters: a difference far too small to change any decision must
pass, and a difference large enough to change one must fail.
"""

from __future__ import annotations

import sys
from pathlib import Path

import numpy as np
import pandas as pd
import pytest

REPO_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO_ROOT / "scripts"))

import verify_release as vr  # noqa: E402


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

    That is four orders of magnitude below the six decimals the report prints, and
    nine orders below the tightest threshold any decision uses. It must pass, and
    the verifier must still say what it saw rather than rounding to 'exact'.
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
    """
    assert vr.TOLERANCE == 1e-9
    assert 4.698e-12 * 10 < vr.TOLERANCE
    assert vr.TOLERANCE < 1e-4
    assert set(vr.EXACT_COLUMNS) == {"rebalances", "folds", "headline_cost_bps"}


def test_the_headline_metric_is_the_one_the_decision_rules_use() -> None:
    """If §2's deciding metric were renamed, the exact ranking check would go blind."""
    from robustfolio import report as reporting

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
