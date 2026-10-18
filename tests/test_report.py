"""Report generation and the §6 decision rules.

These tests drive :mod:`robustfolio.report` with hand-built
:class:`~robustfolio.backtest.BacktestResult` objects rather than the snapshot, so
the decision rule can be exercised on *known* inputs. A decision rule that is only
ever tested by running it on real data is a decision rule nobody has checked: the
verdict it produces there is one sample, and the clauses that failed could have
failed for the wrong reason.

The synthetic constructions are deliberately exact. A candidate whose returns are
its baseline's returns plus a constant has a known Sharpe gap, a known fold-by-fold
advantage, and a known concentration, so the §6.2 and §6.3 clauses have answers
that were computed before the code ran.
"""

from __future__ import annotations

import json

import numpy as np
import pandas as pd
import pytest

from robustfolio import report as reporting
from robustfolio.backtest import METHOD_IDS, BacktestResult
from robustfolio.config import COST_LEVELS_BPS

N_MONTHS = 168
N_FOLDS = 14
MONTHS_PER_FOLD = N_MONTHS // N_FOLDS


def make_result(
    method: str,
    *,
    alpha: float = 0.005,
    sigma: float = 0.04,
    turnover: float = 0.10,
    seed: int = 0,
    n: int = N_MONTHS,
) -> BacktestResult:
    """A synthetic monthly backtest with a known mean and known constant turnover.

    ``alpha`` is the mean monthly gross return and the draw is a function of
    ``seed`` alone, so two results built with the same ``seed`` differ by exactly
    ``alpha`` month for month. That is what makes the fold-by-fold advantage of the
    tests below computable in advance.
    """
    rng = np.random.default_rng(seed)
    index = pd.date_range("2012-06-30", periods=n, freq="ME")
    gross = pd.Series(rng.normal(alpha, sigma, n), index=index)
    turn = pd.Series(np.full(n, float(turnover)), index=index)
    folds = pd.Series(np.arange(n) // (n // N_FOLDS), index=index, dtype=int)
    weights = pd.DataFrame({"A": 0.5, "B": 0.5}, index=index)
    return BacktestResult(
        method=method,
        weights=weights,
        drift=weights.copy(),
        gross_returns=gross,
        turnover=turn,
        folds=folds,
    )


def make_results(**alphas: float) -> dict[str, BacktestResult]:
    """Every method of spec §1, each with its own mean return."""
    return {
        method: make_result(method, alpha=alphas.get(method, 0.005))
        for method in METHOD_IDS
    }


# --------------------------------------------------------------------------- #
# Outcome table
# --------------------------------------------------------------------------- #

def test_outcome_table_covers_every_method_and_cost_level():
    outcomes = reporting.outcome_table(make_results(), bootstrap=False)

    assert list(outcomes.index) == list(METHOD_IDS)
    for level in COST_LEVELS_BPS:
        assert f"net_sharpe_{level}bps" in outcomes.columns
    for column in ("net_sharpe", "gross_sharpe_diagnostic", "cost_drag", "turnover_annualized",
                   "max_drawdown", "cvar95", "skew", "kurtosis", "autocorr1"):
        assert column in outcomes.columns


def test_net_sharpe_declines_with_the_cost_level():
    outcomes = reporting.outcome_table(
        {"B1": make_result("B1", turnover=0.25)}, bootstrap=False
    )

    series = [float(outcomes.loc["B1", f"net_sharpe_{level}bps"]) for level in COST_LEVELS_BPS]

    assert series == sorted(series, reverse=True), "net Sharpe must fall as costs rise"
    assert series[0] > series[-1]


def test_gross_sharpe_is_above_net_sharpe_and_cost_drag_is_the_difference():
    outcomes = reporting.outcome_table({"B1": make_result("B1", turnover=0.25)}, bootstrap=False)

    row = outcomes.loc["B1"]

    assert row["gross_sharpe_diagnostic"] > row["net_sharpe"]
    assert row["cost_drag"] == pytest.approx(
        row["gross_sharpe_diagnostic"] - row["net_sharpe"], rel=1e-10
    )


def test_headline_net_sharpe_equals_the_ten_bps_column():
    outcomes = reporting.outcome_table({"B1": make_result("B1")}, bootstrap=False)

    assert outcomes.loc["B1", "net_sharpe"] == pytest.approx(
        outcomes.loc["B1", "net_sharpe_10bps"], rel=1e-12
    )


def test_bootstrap_columns_appear_only_when_requested():
    without = reporting.outcome_table({"B1": make_result("B1")}, bootstrap=False)
    forced = reporting.outcome_table({"B1": make_result("B1")}, bootstrap=True)

    assert "net_sharpe_ci_low" not in without.columns
    assert "net_sharpe_ci_low" in forced.columns
    assert forced.loc["B1", "net_sharpe_ci_low"] <= forced.loc["B1", "net_sharpe"]
    assert forced.loc["B1", "net_sharpe_ci_high"] >= forced.loc["B1", "net_sharpe"]
    assert forced.loc["B1", "net_sharpe_ci_reps"] == 2000
    assert forced.loc["B1", "net_sharpe_ci_seed"] == reporting.SEED


# --------------------------------------------------------------------------- #
# Fold table
# --------------------------------------------------------------------------- #

def test_fold_table_advantage_is_exact_when_the_paths_differ_by_a_constant():
    """Same seed -> the same draw, so the advantage is the known constant."""
    baseline = make_result("B1", alpha=0.005, seed=0)
    candidate = make_result("M1", alpha=0.020, seed=0)

    folds = reporting.fold_table(candidate, baseline)

    assert list(folds["months"]) == [MONTHS_PER_FOLD] * N_FOLDS
    expected = 0.020 - 0.005
    assert folds["advantage_return"].to_numpy() == pytest.approx(expected, rel=1e-12)
    assert (folds["advantage_sharpe"] > 0).all()


def test_fold_table_reports_a_negative_advantage_when_the_candidate_is_worse():
    baseline = make_result("B1", alpha=0.020, seed=0)
    candidate = make_result("M1", alpha=0.005, seed=0)

    folds = reporting.fold_table(candidate, baseline)

    assert (folds["advantage_return"] < 0).all()
    assert (folds["advantage_sharpe"] < 0).all()


def test_fold_table_refuses_a_baseline_on_a_different_calendar():
    candidate = make_result("M1", n=N_MONTHS)
    baseline = make_result("B1", n=N_MONTHS - 12)

    with pytest.raises(ValueError, match="same calendar"):
        reporting.fold_table(candidate, baseline)


# --------------------------------------------------------------------------- #
# Decision rule
# --------------------------------------------------------------------------- #

def test_best_baseline_is_the_one_with_the_highest_net_sharpe():
    results = make_results(B1=0.002, B2=0.009, B3=0.004, B4=0.001, B5=0.003)
    outcomes = reporting.outcome_table(results, bootstrap=False)

    decisions, _ = reporting.decision_table(results, outcomes)

    assert set(decisions["baseline"]) == {"B2"}


def test_a_candidate_identical_to_the_baseline_fails_everything():
    """No gap, no edge at any cost level, no fold wins: a FAILURE by construction."""
    results = make_results()
    outcomes = reporting.outcome_table(results, bootstrap=False)

    decisions, _ = reporting.decision_table(results, outcomes)

    row = decisions.loc["M2"]
    assert row["sharpe_gap"] == pytest.approx(0.0, abs=1e-12)
    assert not row["pass_sharpe_gap"]
    assert not row["pass_psr"]
    assert int(row["cost_levels_won"]) == 0
    assert int(row["folds_won"]) == 0
    assert row["verdict"] == "FAILURE"


def test_a_candidate_clearly_ahead_satisfies_every_clause():
    """M1 has a known +1.5%/month constant edge over five identical baselines.

    Every §6 clause is decidable in advance: the Sharpe gap is
    ``0.015/sigma*sqrt(12)``, the edge holds in all 14 folds, at all five cost
    levels, and no fold carries more than 1/14 of it. The tolerance on the gap is
    10% because ``sigma`` here is the *realised* draw's dispersion, which differs
    from the nominal 0.04 by about ``1/sqrt(2T)`` -- the clause outcomes, not the
    gap's third digit, are what this test is checking.
    """
    results = make_results(M1=0.020)
    outcomes = reporting.outcome_table(results, bootstrap=False)

    decisions, detail = reporting.decision_table(results, outcomes)

    row = decisions.loc["M1"]
    expected_gap = 0.015 / 0.04 * np.sqrt(12)
    assert row["sharpe_gap"] == pytest.approx(expected_gap, rel=0.1)
    assert row["verdict"] == "SUCCESS", row.to_dict()
    assert row["pass_psr"] and row["pass_dsr"]
    assert row["pass_sharpe_gap"] and row["pass_turnover"] and row["pass_drawdown"]
    assert int(row["cost_levels_won"]) == len(COST_LEVELS_BPS)
    assert int(row["folds_won"]) == N_FOLDS
    assert row["max_fold_share"] <= 0.40
    assert detail["M1"].folds.shape[0] == N_FOLDS


def test_a_candidate_ahead_by_less_than_the_materiality_threshold_is_partial_only():
    """A +0.05 Sharpe edge: real enough to win every fold, far too small to clear
    §6.1's PSR bar against the best baseline or §6.2's 0.20 gap."""
    results = make_results(M1=0.005 + 0.05 * 0.04 / np.sqrt(12))
    outcomes = reporting.outcome_table(results, bootstrap=False)

    decisions, _ = reporting.decision_table(results, outcomes)

    row = decisions.loc["M1"]
    assert row["sharpe_gap"] == pytest.approx(0.05, rel=0.1)
    assert row["sharpe_gap"] < reporting.MATERIALITY_SHARPE_GAP
    assert not row["pass_sharpe_gap"]
    assert not row["pass_psr"], "the benchmark is the best baseline, not zero"
    assert row["pass_dsr"], "against a zero benchmark the edge is still real"
    assert not row["statistical"]
    assert not row["material"]
    assert row["robust"], "it wins every fold and every cost level"
    assert row["verdict"] == "PARTIAL"


def test_a_baseline_missing_from_the_table_is_an_error():
    results = make_results()
    del results["B5"]
    outcomes = reporting.outcome_table(results, bootstrap=False)

    decisions, _ = reporting.decision_table(results, outcomes)

    assert "B5" not in set(decisions["baseline"])


def test_decisions_cover_the_registered_candidates_only():
    outcomes = reporting.outcome_table(make_results(), bootstrap=False)
    decisions, _ = reporting.decision_table(make_results(), outcomes)

    assert list(decisions.index) == list(reporting.CANDIDATE_IDS)


# --------------------------------------------------------------------------- #
# Manifest and rendering
# --------------------------------------------------------------------------- #

def test_manifest_records_the_things_a_reproduction_needs():
    payload = reporting.manifest("some-snapshot-id")

    for key in ("generated_utc", "snapshot_id", "git_commit", "protocol_version",
                "spec_version", "seed", "bootstrap", "environment", "dsr_family_size"):
        assert key in payload
    assert payload["snapshot_id"] == "some-snapshot-id"
    assert payload["bootstrap"]["replications"] == 2000
    assert "EXPLORATORY" in payload["scope"]


def test_the_manifest_records_what_decides_the_last_bits():
    """Finding F34: two machines, one image, the same 51 packages, `4.698e-12` apart.

    The record could not have explained that, because it did not record the part
    of the environment that differs between two machines with identical software:
    the BLAS build and the kernel it dispatches to at run time from the CPU's
    features. A field that records only what is already identical is decoration.
    """
    payload = reporting.manifest("some-snapshot-id")
    context = payload["environment"]["blas_context"]

    assert context["cpu_count"] >= 1
    assert "OPENBLAS_NUM_THREADS" in context["thread_controls"]
    assert set(context["blas"]) == {"name", "version", "build_configuration"}


def test_build_report_refuses_an_incomplete_method_set():
    results = make_results()
    del results["M2"]

    with pytest.raises(ValueError, match="needs every method"):
        reporting.build_report(results, snapshot_id="x", bootstrap=False)


def test_report_writes_every_artefact_and_labels_itself_exploratory(tmp_path):
    run = reporting.build_report(
        make_results(M1=0.020), snapshot_id="snap", bootstrap=False
    )

    written = run.write(tmp_path)

    assert set(written) >= {"manifest", "outcomes", "decisions", "report", "folds_M1", "calibration", "design"}
    payload = json.loads((tmp_path / "manifest.json").read_text(encoding="utf-8"))
    assert payload["snapshot_id"] == "snap"
    assert payload["git_commit"]
    assert payload["calibration"]["reported"] is True
    assert "F24" in payload["calibration"]["reading"]

    text = (tmp_path / "report.md").read_text(encoding="utf-8")
    assert "EXPLORATORY" in text
    assert "diagnostic only" in text
    assert "SUCCESS" in text and "FAILURE" in text
    assert "Monotonic: every method's net Sharpe declines with cost." in text
    assert "F24" in text and "F25" in text
    assert "Calibration of next-month return intervals" in text

    outcomes = pd.read_csv(tmp_path / "outcomes.csv", index_col=0)
    assert list(outcomes.index) == list(METHOD_IDS)
    decisions = pd.read_csv(tmp_path / "decisions.csv", index_col=0)
    assert list(decisions.index) == list(reporting.CANDIDATE_IDS)
    folds = pd.read_csv(tmp_path / "folds_M1.csv", index_col=0)
    assert len(folds) == N_FOLDS
    calibration = pd.read_csv(tmp_path / "calibration.csv", index_col=0)
    assert list(calibration.index) == list(METHOD_IDS)
    assert (calibration["level"] == 0.90).all()
    design = pd.read_csv(tmp_path / "design.csv", index_col=0)
    assert list(design.index) == list(reporting.CANDIDATE_IDS)
    assert not design["is_registered_metric"].any()
    assert payload["design_diagnostics"]["is_registered_metric"] is False


def test_report_marks_a_non_monotonic_cost_profile_as_a_bug_signal(tmp_path):
    """§5.5.7 item 4: rising net Sharpe with cost is a bug signal, not a finding."""
    results = make_results()
    sabotage = make_result("B1", alpha=0.005, turnover=-0.10)  # negative turnover
    results["B1"] = sabotage
    run = reporting.build_report(results, snapshot_id="snap", bootstrap=False)

    text = run.to_markdown()

    assert "NON-MONOTONIC" in text


def test_report_renders_with_bootstrap_intervals(tmp_path):
    run = reporting.build_report(
        make_results(M1=0.020), snapshot_id="snap", bootstrap=True, family_size=1
    )
    text = run.to_markdown()

    assert "90% CI" in text
    assert "[1." in text or "[-" in text  # an interval, not just a point


# --------------------------------------------------------------------------- #
# §7.8 calibration wiring
# --------------------------------------------------------------------------- #

def test_calibration_table_reports_coverage_with_all_of_its_inputs():
    frame = reporting.calibration_table({"B1": make_result("B1")}, window=60)

    row = frame.loc["B1"]
    assert row["window_months"] == 60
    assert row["months_evaluated"] == N_MONTHS - 60
    assert row["level"] == pytest.approx(0.90)
    assert row["coverage"] == pytest.approx(row["hits"] / row["months_evaluated"])
    assert 0.5 <= row["coverage"] <= 1.0, "a stationary series must roughly cover"
    assert (row["target_low"], row["target_high"]) == reporting.CALIBRATION_TARGET


def test_calibration_table_evaluates_nothing_before_a_full_window():
    frame = reporting.calibration_table({"B1": make_result("B1")}, window=N_MONTHS)

    assert int(frame.loc["B1", "months_evaluated"]) == 0
    assert np.isnan(float(frame.loc["B1", "coverage"]))
    assert not frame.loc["B1", "in_target_range"]


def test_calibration_table_is_reproducible_from_the_frozen_seed():
    first = reporting.calibration_table({"B1": make_result("B1")}, window=60)
    second = reporting.calibration_table({"B1": make_result("B1")}, window=60)

    assert first.loc["B1", "coverage"] == second.loc["B1", "coverage"]
    assert int(first.loc["B1", "hits"]) == int(second.loc["B1", "hits"])


def test_calibration_can_be_switched_off():
    run = reporting.build_report(
        make_results(),
        snapshot_id="snap",
        bootstrap=False,
        calibration_window=False,
    )

    assert run.calibration is None
    assert "Calibration" not in run.to_markdown()
    assert run.manifest["calibration"]["reported"] is False


# --------------------------------------------------------------------------- #
# Finding F15 design / detectability table
# --------------------------------------------------------------------------- #

def test_design_table_reports_rho_and_the_paired_difference():
    results = make_results(M1=0.020)
    outcomes = reporting.outcome_table(results, bootstrap=False)
    decisions, _ = reporting.decision_table(results, outcomes)

    frame = reporting.design_diagnostics(results, decisions)

    assert list(frame.index) == list(reporting.CANDIDATE_IDS)
    row = frame.loc["M1"]
    assert row["baseline"] == decisions.loc["M1", "baseline"]
    assert row["n_paired_months"] == N_MONTHS
    assert -1.0 <= row["rho"] <= 1.0
    # The candidate is the baseline plus a known constant edge, so the two series
    # are perfectly correlated and the paired difference has no dispersion.
    assert row["rho"] == pytest.approx(1.0, abs=1e-9)
    assert row["mean_paired_difference"] == pytest.approx(0.015, rel=1e-9)
    assert row["se_difference"] == pytest.approx(0.0, abs=1e-15)


def test_design_table_marks_itself_as_not_a_registered_metric():
    results = make_results()
    outcomes = reporting.outcome_table(results, bootstrap=False)
    decisions, _ = reporting.decision_table(results, outcomes)

    frame = reporting.design_diagnostics(results, decisions)

    assert not frame["is_registered_metric"].any()
    text = reporting.build_report(results, snapshot_id="snap", bootstrap=False).to_markdown()
    assert "Design and detectability" in text
    assert "Not a registered metric" in text
