"""Leakage suite -- evaluation_protocol.md section 5.4.8.

Before any experiment runs:

1. **Time-travel test:** for random timestamps, verify no field used at t
   contains values knowable only after t.
2. **Survivorship test:** verify the universe at t includes assets that
   delisted after t.
3. **Adjusted-price test:** verify point-in-time adjusted prices do not
   incorporate corporate actions with ex-dates after t.
4. **Universe reconstruction test:** verify membership at t matches archived
   evidence.
5. **Determinism test:** same snapshot + same code -> identical output.

Any failing test blocks the experiment.

Tests run against a hermetic synthetic snapshot (which contains a real split and
real dividends, so each test has power) and, where the assertion is about the
actual data, against the newest immutable snapshot on disk.

Two protocol facts are asserted here rather than assumed:

* Section 5.4.8 test 2 is **vacuous in-sample** -- no confirmed candidate
  delisted between 2012-06 and 2026-05 (notes/pit_universe_2026-10-17.md
  section 5). The test skips with that reason and re-activates automatically if
  the universe ever gains a delisting.
* Section 5.4.8 test 1's power is demonstrated by a negative control: a future
  dividend *does* change a naive whole-sample result, so immunity to it is not
  vacuous.
"""

from __future__ import annotations

import numpy as np
import pandas as pd
import pytest

from robustfolio import data as dm

from conftest import (
    CCC_FIRST_ELIGIBLE,
    SPLIT_DATE,
    SYNTHETIC_TICKERS,
    make_snapshot,
    with_actions,
)

#: Seed for the random-timestamp draws (spec section 11, O7: SEED = 20261017).
SEED = 20261017


def _derived(snapshot: dm.Snapshot, t) -> dict:
    """Every value the pipeline would use at t, in one comparable bundle."""
    return {
        "adjusted_prices": snapshot.adjusted_prices(t),
        "monthly_returns": snapshot.monthly_total_returns(cutoff=t),
        "eligible": sorted(snapshot.eligible(t)),
        "price_at": snapshot.price_at(t),
        "adv_3m": snapshot.adv_3m(t),
        "history_months": snapshot.history_months(t),
    }


def _assert_same(a: dict, b: dict, context: str) -> None:
    for key in a:
        left, right = a[key], b[key]
        if isinstance(left, pd.DataFrame):
            pd.testing.assert_frame_equal(left, right, obj=context + ":" + key)
        elif isinstance(left, pd.Series):
            pd.testing.assert_series_equal(left, right, obj=context + ":" + key)
        else:
            assert left == right, f"{context}:{key} differs: {left!r} != {right!r}"


# --------------------------------------------------------------------------- #
# 1. Time-travel test
# --------------------------------------------------------------------------- #

def test_1_time_travel_synthetic(synthetic_snapshot, month_ends):
    """Full snapshot and its truncation agree at random timestamps."""
    rng = np.random.default_rng(SEED)
    draw = [month_ends[i] for i in rng.choice(len(month_ends), size=12, replace=False)]
    for t in sorted(draw):
        _assert_same(
            _derived(synthetic_snapshot, t),
            _derived(synthetic_snapshot.truncated(t), t),
            context=f"truncation@{t.date()}",
        )


def test_1_time_travel_real(real_snapshot):
    """Same check on the real snapshot (protocol section 5.4.8 item 1)."""
    rng = np.random.default_rng(SEED)
    ends = real_snapshot.monthly_prices().index
    ends = ends[ends >= pd.Timestamp("2012-06-30")]
    assert len(ends) > 24, "expected a multi-year monthly record"
    draw = [ends[i] for i in rng.choice(len(ends), size=8, replace=False)]
    for t in sorted(draw):
        _assert_same(
            _derived(real_snapshot, t),
            _derived(real_snapshot.truncated(t), t),
            context=f"real-truncation@{t.date()}",
        )


def test_1_time_travel_power_control():
    """A leak would be detected: a future dividend changes a naive result.

    ``t`` sits mid-month; the injected dividend's ex-date is after ``t`` but
    inside the same month. A pipeline that ignored ``t`` would fold it in.
    """
    base = make_snapshot()
    t = pd.Timestamp("2019-06-14")
    injected = pd.concat(
        [
            base.actions,
            pd.DataFrame(
                [{"ticker": "BBB", "ex_date": pd.Timestamp("2019-06-20"),
                  "kind": "dividend", "value": 5.0}]
            ),
        ],
        ignore_index=True,
    )
    patched = with_actions(base, injected)

    leaky = patched.monthly_total_returns()          # ignores the cutoff
    pit_clean = patched.monthly_total_returns(cutoff=t)
    pit_base = base.monthly_total_returns(cutoff=t)

    month = pd.Timestamp("2019-06-30")
    assert not np.isclose(leaky.loc[month, "BBB"], pit_clean.loc[month, "BBB"]), (
        "power control failed: injecting a post-t future dividend did not change "
        "the naive result, so the time-travel test cannot detect leakage"
    )
    pd.testing.assert_series_equal(pit_clean.loc[month], pit_base.loc[month])


# --------------------------------------------------------------------------- #
# 2. Survivorship test
# --------------------------------------------------------------------------- #

def test_2_survivorship_is_vacuous_in_sample(real_snapshot):
    """A universe of still-listed instruments cannot exercise this test.

    Recorded, not hidden: every confirmed candidate traded throughout the
    sample (notes/pit_universe_2026-10-17.md section 5), so there is no
    delisting return to verify. If that ever changes, this test fails on
    purpose rather than passing vacuously.
    """
    universe = real_snapshot.universe
    delisted = universe[universe["last_eligible"].astype(str).str.strip() != ""]
    if delisted.empty:
        pytest.skip(
            "section 5.4.8 test 2 is vacuous in-sample: no confirmed candidate "
            "delisted between 2012-06 and 2026-05 (protocol section 5.4.5). "
            "Survivorship is argued by construction, not measured."
        )
    raise AssertionError(
        "the universe now contains a delisting; implement the survivorship "
        "check (membership through the delisting date + delisting return) "
        "before running any experiment"
    )


def test_2_survivorship_mechanism_is_wired():
    """The delisting path works even though it is unexercised in-sample."""
    universe = pd.DataFrame(
        [
            {"ticker": "AAA", "first_eligible": "2014-01-01", "last_eligible": "", "source_note": "s"},
            {"ticker": "BBB", "first_eligible": "2014-01-01", "last_eligible": "2019-12-31", "source_note": "s"},
            {"ticker": "CCC", "first_eligible": CCC_FIRST_ELIGIBLE, "last_eligible": "", "source_note": "s"},
        ]
    )
    snapshot = make_snapshot(universe=universe)
    assert "BBB" in snapshot.members_at("2019-06-30")
    assert "BBB" not in snapshot.members_at("2020-06-30")
    assert snapshot.listed_until("BBB") == pd.Timestamp("2019-12-31")
    assert snapshot.listed_until("AAA") is None


# --------------------------------------------------------------------------- #
# 3. Adjusted-price test
# --------------------------------------------------------------------------- #

def test_3_split_does_not_leak_a_spurious_return(synthetic_snapshot):
    """BBB halves on its ex-date; the split-adjusted return must not jump."""
    returns = synthetic_snapshot.monthly_total_returns()
    split_month = (SPLIT_DATE + pd.offsets.MonthEnd(0))
    assert abs(returns.loc[split_month, "BBB"]) < 0.10, (
        "a -50% raw price halves at the split but the adjusted return jumps: "
        "the split factor was not applied"
    )


def test_3_future_actions_do_not_affect_past(synthetic_snapshot):
    """Injected post-t splits and dividends leave every value <= t untouched."""
    t = pd.Timestamp("2019-06-30")
    injected = pd.concat(
        [
            synthetic_snapshot.actions,
            pd.DataFrame(
                [
                    {"ticker": "BBB", "ex_date": pd.Timestamp("2020-03-02"),
                     "kind": "split", "value": 3.0},
                    {"ticker": "BBB", "ex_date": pd.Timestamp("2020-05-15"),
                     "kind": "dividend", "value": 9.0},
                ]
            ),
        ],
        ignore_index=True,
    )
    patched = with_actions(synthetic_snapshot, injected)

    pd.testing.assert_frame_equal(
        patched.monthly_total_returns(cutoff=t),
        synthetic_snapshot.monthly_total_returns(cutoff=t),
    )
    pd.testing.assert_frame_equal(
        patched.adjusted_prices(t), synthetic_snapshot.adjusted_prices(t)
    )


def test_3_adjusted_prices_use_only_known_actions(real_snapshot):
    """Recomputing with actions truncated at t reproduces adjusted_prices(t)."""
    for t in (pd.Timestamp("2013-06-28"), pd.Timestamp("2019-03-29")):
        truncated = real_snapshot.actions[real_snapshot.actions["ex_date"] <= t]
        expected = real_snapshot.adjusted_prices(t)
        recomputed = with_actions(real_snapshot, truncated).adjusted_prices(t)
        pd.testing.assert_frame_equal(expected, recomputed)


def test_3_dividend_branch_is_exercised(real_snapshot):
    """The dividend half of the adjustment is real, not assumed."""
    dividends = real_snapshot.actions[real_snapshot.actions["kind"] == "dividend"]
    splits = real_snapshot.actions[real_snapshot.actions["kind"] == "split"]
    assert len(dividends) > 0, "no dividends in the snapshot: return construction untested"
    if splits.empty:
        pytest.skip(
            "no splits in the confirmed universe: the split branch of section "
            "5.4.8 test 3 is unexercised on real data (covered by the synthetic "
            "fixture instead)"
        )


# --------------------------------------------------------------------------- #
# 4. Universe reconstruction test
# --------------------------------------------------------------------------- #

def test_4_membership_matches_archived_list(real_snapshot):
    """Membership at t is a subset of the archived candidate list, by date."""
    universe = real_snapshot.universe
    assert 15 <= len(universe) <= 25, "protocol section 5.4.2 requires 15-25 candidates"
    first = dict(zip(universe["ticker"], pd.to_datetime(universe["first_eligible"])))

    ends = real_snapshot.monthly_prices().index
    ends = ends[(ends >= pd.Timestamp("2012-06-30")) & (ends <= pd.Timestamp("2026-05-31"))]
    rng = np.random.default_rng(SEED)
    sample = [ends[i] for i in rng.choice(len(ends), size=10, replace=False)]

    for t in sorted(sample):
        members = real_snapshot.members_at(t)
        eligible = real_snapshot.eligible(t)
        assert set(eligible) <= set(members), f"{t.date()}: eligible outside membership"
        for ticker in members:
            assert first[ticker] <= t, f"{t.date()}: {ticker} listed before it existed"


def test_4_nobody_is_a_member_before_its_first_eligible_date(real_snapshot):
    for row in real_snapshot.universe.itertuples(index=False):
        before = pd.Timestamp(row.first_eligible) - pd.Timedelta(days=1)
        assert row.ticker not in real_snapshot.members_at(before)


def test_4_frozen_anchor_universe_is_complete(real_snapshot):
    """At the frozen backtest start every candidate is eligible.

    The anchor (2012-06) is derived, not chosen: protocol section 13.1's T = 168
    months, section 4.3's 60-month window and section 5.2's walk-forward force a
    228-month record (DEC-20261017-024). If a candidate is not yet eligible
    here, the anchor is wrong or the candidate list is wrong -- both block
    Gate 1.
    """
    anchor = pd.Timestamp("2012-06-29")
    eligible = set(real_snapshot.eligible(anchor))
    expected = set(real_snapshot.tickers)
    assert eligible == expected, (
        f"not eligible at the frozen anchor {anchor.date()}: "
        f"{sorted(expected - eligible)}"
    )


# --------------------------------------------------------------------------- #
# 5. Determinism test
# --------------------------------------------------------------------------- #

def test_5_same_snapshot_same_output(real_snapshot_id):
    left = dm.load_snapshot(real_snapshot_id)
    right = dm.load_snapshot(real_snapshot_id)
    pd.testing.assert_frame_equal(left.adjusted_prices(), right.adjusted_prices())
    pd.testing.assert_frame_equal(left.monthly_total_returns(), right.monthly_total_returns())
    pd.testing.assert_series_equal(left.rf_monthly(), right.rf_monthly())


def test_5_snapshot_is_byte_immutable(real_snapshot_id):
    """Manifest SHA-256 digests must match the files on disk (section 5.4.9)."""
    snapshot = dm.load_snapshot(real_snapshot_id, verify=True)
    assert snapshot.manifest["sha256"], "snapshot carries no integrity hashes"
    for name, digest in snapshot.manifest["sha256"].items():
        assert dm.sha256_file(snapshot.path / name) == digest


# --------------------------------------------------------------------------- #
# Risk-free series (protocol section 5.4.6, 5.5.5)
# --------------------------------------------------------------------------- #

def test_rf_is_never_zero_filled(real_snapshot):
    """The loader must never *invent* a zero; genuine vendor zeros are allowed.

    DGS1MO printed 0.00 on some 2015 days, so a plain "rf > 0" assertion would
    be wrong. The protocol forbids *substituting* zero for a missing rate
    (section 5.4.6), which is what this checks.
    """
    observed = (
        real_snapshot.rf_daily.set_index("date")["dgs1mo"].sort_index().resample("ME").last()
    )
    assert observed.notna().all(), (
        "a month has no DGS1MO observation; the loader would have had to impute it"
    )

    rf = real_snapshot.rf_monthly()
    assert len(rf) > 100, "expected a multi-year monthly rf series"
    assert rf.notna().all()
    assert (rf >= 0).all(), "a negative 1-month T-bill rate is impossible in this window"
    assert (rf < 0.02).all(), "monthly rf implausibly large: the conversion is wrong"

    for ts in rf.index[rf == 0.0]:
        prior = ts - pd.offsets.MonthEnd(1)
        assert observed.get(prior, float("nan")) == 0.0, (
            f"{ts.date()}: zero risk-free rate with no matching vendor zero"
        )
