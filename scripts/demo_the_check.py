"""Show that the release check can fail, and that it declines to fail for noise.

    python scripts/demo_the_check.py

CI re-runs the whole experiment from the release archive and compares the result to
the committed tables, so the check *passing* is observed on every push. It has also
been seen *rejecting* -- twice, on platform noise (F33, F34) -- but the half of the
comparison added in DEC-20261018-041 has never refused anything: the verdict table
is compared exactly, and no run has ever disagreed with it. A comparison that has
never refused anything is a comparison that might not be able to refuse, which is
the argument that puts a positive control beside the margin test in
``tests/test_onepager.py``.

This feeds the two comparison functions three tables that disagree with the
published ones and prints what each call returned:

1. a headline measurement moved by 0.01   -> caught, and the column named
2. a verdict flipped FAILURE -> SUCCESS   -> caught, with every statistic untouched
3. a measurement moved by 1e-12           -> not caught, correctly

The third matters as much as the first two. A verifier that fails on platform noise
is unusable, and one that tolerates a changed decision is worthless; the split
between them *is* the claim the project makes, and this is that claim executed
rather than described.

Exit status is 0 only if all three behave as stated, so running the demo is also a
test of the check. It writes nothing: the tampering happens on in-memory copies,
because a demo that edited ``docs/published-run/`` would destroy the artefact it
exists to protect.
"""

from __future__ import annotations

import sys
from pathlib import Path

import pandas as pd

REPO_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(Path(__file__).resolve().parent))

import verify_release as verifier  # noqa: E402

PUBLISHED = REPO_ROOT / "docs" / "published-run"

#: A difference a person could call "the same result" and be wrong about.
MEASURABLE = 0.01

#: The scale of the difference two machines actually produced (F34 measured 4.698e-12).
NOISE = 1e-12


def _load(path: Path) -> pd.DataFrame:
    """Read at full precision; the default parser is lossy by an ULP (F28)."""
    return pd.read_csv(path, index_col=0, float_precision="round_trip")


def _bump(table: pd.DataFrame, delta: float, *, metric: str) -> pd.DataFrame:
    """The same table with the strongest method's headline measurement moved."""
    changed = table.copy()
    method = changed[metric].astype(float).idxmax()
    changed.loc[method, metric] = float(changed.loc[method, metric]) + delta
    return changed


def _report(number: int, title: str, *, caught: bool, expected: bool,
            worst: float, offenders: list[str], problems: list[str]) -> bool:
    if problems:
        detail = "; ".join(problems)
    elif offenders:
        detail = f"{', '.join(offenders)} beyond the bound (worst {worst:.3e})"
    else:
        detail = f"worst {worst:.3e}, inside the bound"
    print(f"{number}. {title}")
    print(f"   result : {'caught' if caught else 'passed'}")
    print(f"   detail : {detail}")
    if caught is not expected:
        print(f"   ^ expected the check to {'catch' if expected else 'accept'} this")
    return caught is expected


def main(argv: list[str] | None = None) -> int:
    del argv                                  # no options: the tables are the argument
    outcomes = _load(PUBLISHED / "outcomes.csv")
    decisions = _load(PUBLISHED / "decisions.csv")
    metric = verifier.HEADLINE_METRIC

    print(f"published : {PUBLISHED.relative_to(REPO_ROOT).as_posix()} (read only; the copies below are in memory)")
    print(f"tolerance : {verifier.TOLERANCE:.0e} on measurements, exact on decisions")
    print()

    results = []

    worst, offenders, problems = verifier.compare(
        _bump(outcomes, MEASURABLE, metric=metric), outcomes
    )
    results.append(_report(
        1, f"a headline measurement moved by {MEASURABLE}",
        caught=bool(offenders or problems), expected=True,
        worst=worst, offenders=offenders, problems=problems,
    ))

    strongest = decisions["sharpe_gap"].astype(float).idxmax()
    original = str(decisions.loc[strongest, "verdict"])
    if original == "SUCCESS":
        print(f"premise broken: {strongest} is already SUCCESS, so there is nothing to flip")
        return 1
    flipped = decisions.copy()
    flipped.loc[strongest, "verdict"] = "SUCCESS"
    worst, offenders, problems = verifier.compare_decisions(flipped, decisions)
    results.append(_report(
        2, f"the verdict for {strongest} flipped {original} -> SUCCESS",
        caught=bool(offenders or problems), expected=True,
        worst=worst, offenders=offenders, problems=problems,
    ))

    worst, offenders, problems = verifier.compare(
        _bump(outcomes, NOISE, metric=metric), outcomes
    )
    results.append(_report(
        3, f"a headline measurement moved by {NOISE:g} (platform noise)",
        caught=bool(offenders or problems), expected=False,
        worst=worst, offenders=offenders, problems=problems,
    ))

    print()
    if all(results):
        print("All three behaved as documented: a changed decision is refused, a changed")
        print("measurement is refused, and the noise two machines produce is absorbed.")
    else:
        print("The check did NOT behave as documented, so the claim it supports is wrong.")
    print()
    print("What this does not show: that the pipeline computes these numbers. It shows")
    print("that the comparison refuses a table that disagrees. CI re-runs the pipeline;")
    print("this exercises the comparison it hands the result to.")

    return 0 if all(results) else 1


if __name__ == "__main__":
    raise SystemExit(main())
