"""The paired-inference reading is computed, not asserted.

Three properties matter here:

1. **Identical series have zero difference**, and the paired bootstrap must say
   so rather than manufacture noise from two resamplings of the same data.
2. **A constant shift is detected**, so the test has power in the direction it
   claims to measure.
3. **The equivalence column is three-way**, because collapsing it to pass/fail
   would reintroduce the exact confusion the note exists to remove.

The run-level test uses a small synthetic panel, not the frozen snapshot: the
snapshot is not distributed, and a unit test must not depend on it.
"""

from __future__ import annotations

import sys
from pathlib import Path

import numpy as np
import pandas as pd

REPO_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO_ROOT / "scripts"))

import paired_inference as paired  # noqa: E402


def _series(seed: int = 7, n: int = 120) -> pd.Series:
    rng = np.random.default_rng(seed)
    return pd.Series(rng.normal(0.004, 0.03, size=n))


def test_identical_series_have_zero_paired_difference():
    a = _series()
    draws = paired._paired_draws(
        a.to_numpy(), a.to_numpy(), reps=200, mean_block=6, seed=1
    )
    assert np.allclose(draws, 0.0)
    assert paired.annualized_sharpe(a.to_numpy()) == paired.annualized_sharpe(a.to_numpy())


def test_a_constant_shift_is_detected():
    baseline = _series(seed=11)
    candidate = baseline + 0.002
    draws = paired._paired_draws(
        candidate.to_numpy(), baseline.to_numpy(), reps=200, mean_block=6, seed=1
    )
    assert np.nanmean(draws) > 0.0
    assert np.nanmean(draws > 0) > 0.95


def test_equivalence_is_three_way():
    assert paired._equivalence(0.00, 0.19, 0.20) == "NOT_MATERIAL"
    assert paired._equivalence(0.21, 0.35, 0.20) == "MATERIAL"
    assert paired._equivalence(0.10, 0.30, 0.20) == "INCONCLUSIVE"


def test_analyse_returns_the_documented_shape():
    rng = np.random.default_rng(20261104)
    n = 48
    index = pd.date_range("2020-01-31", periods=n, freq="ME")
    base = pd.Series(rng.normal(0.004, 0.03, size=n), index=index)
    frame = pd.DataFrame(
        {
            "B1": base + rng.normal(0.0, 0.001, size=n),
            "B3": base,
            "M1": base + rng.normal(0.0, 0.002, size=n),
            "M2": base + rng.normal(0.0005, 0.002, size=n),
        }
    )
    outcomes = pd.DataFrame(
        {"net_sharpe": {"B1": 0.4, "B3": 0.5, "M1": 0.5, "M2": 0.6}}
    )
    decisions = pd.DataFrame(
        {"baseline": {"M1": "B3", "M2": "B3"}}
    )
    payload = paired.analyse(
        frame, outcomes, decisions, bar=0.20, reps=200, seed=1
    )
    assert payload["n_months"] == n
    assert payload["comparator"]["best"] == "B3"
    assert set(payload["methods"]) == {"M1", "M2"}
    for row in payload["methods"].values():
        assert row["equivalence"] in {"MATERIAL", "NOT_MATERIAL", "INCONCLUSIVE"}
        assert 0.0 <= row["p_positive"] <= 1.0
        assert row["ci90_low"] <= row["ci90_high"]
        assert set(row["dsr_p"]) == {"1", "2", "7"}


def test_markdown_quotes_the_computed_numbers():
    rng = np.random.default_rng(3)
    n = 48
    index = pd.date_range("2020-01-31", periods=n, freq="ME")
    base = pd.Series(rng.normal(0.004, 0.03, size=n), index=index)
    frame = pd.DataFrame({"B3": base, "M2": base + rng.normal(0.001, 0.002, size=n)})
    outcomes = pd.DataFrame({"net_sharpe": {"B3": 0.5, "M2": 0.6}})
    decisions = pd.DataFrame({"baseline": {"M2": "B3"}})
    payload = paired.analyse(frame, outcomes, decisions, bar=0.20, reps=100, seed=1)
    text = paired.render_markdown(payload)
    row = payload["methods"]["M2"]
    assert f"{row['point_delta_sr']:+.4f}" in text
    assert f"{row['ci90_low']:+.4f}" in text
    assert "NOT_MATERIAL" in text or "INCONCLUSIVE" in text or "MATERIAL" in text
