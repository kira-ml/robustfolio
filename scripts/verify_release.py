"""Verify a published run against its release archive (the "check me" command).

    python scripts/verify_release.py --archive dist/<archive>.tar.gz --run results/<run_id>/

Extracts the frozen snapshot from the release archive into a temporary directory,
re-runs all seven methods, rebuilds both published tables, and compares them against
the run's ``outcomes.csv`` and ``decisions.csv``. Exits non-zero if a *decision*
differs -- including a §6.4 verdict -- or if a metric differs by more than
:data:`TOLERANCE`.

Both tables are compared because they fail differently. The metrics are
measurements and may move by the platform noise in :data:`TOLERANCE`; the verdict is
a decision and may not move at all. Until DEC-20261018-041 only ``outcomes.csv`` was
compared, and the *ranking* of net Sharpe was standing in for the verdict -- which
agrees here and need not in general, since §6.1-§6.4 decide with a conjunction of
gates that no single ranking represents.

Why this is a script and not a paragraph in the README
------------------------------------------------------
Because the two ways to get this wrong are both silent, and both produce a
plausible number (findings F27, F28):

1. ``pandas.read_csv`` is **lossy by one ULP** at its default settings. Reading
   the published ``outcomes.csv`` with defaults returns ``0.1820065203183531``
   where the file contains ``0.18200652031835318``; ``float_precision="high"``
   is also lossy. Only ``float_precision="round_trip"`` is exact. A verifier
   that reads with defaults reports a mismatch on a perfectly good artifact.
2. The bundle hash covers four files, not the five that ``manifest.json``
   lists. A verifier that recomputes the bundle from the manifest's full hash
   map rejects every valid snapshot.

It also asserts something of a different kind: that the archive still **carries its
notice** (finding F30). That is a compliance property rather than a numerical one,
but it fails the same way -- silently, on a re-pack, with the data still looking
fine and the licence claim no longer attached to it.

Both of those were wrong in the first draft of this file's predecessor, and both
produced numbers that looked like findings. A claim that can be checked only by
re-deriving the checker's own bugs is not a checkable claim, so the check is
shipped as code with its tolerances stated -- and the tolerance itself is the
third thing this file learned the hard way (findings F33, F34). The claim is split
in two: everything decision-bearing is compared exactly, and the continuous
metrics are compared against a documented bound, with the observed difference
always printed. See :data:`TOLERANCE` for why the bound is not zero.
"""

from __future__ import annotations

import argparse
import sys
import tempfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
sys.path.insert(0, str(Path(__file__).resolve().parent))

import pandas as pd  # noqa: E402
import numpy as np  # noqa: E402

from pack_snapshot import (  # noqa: E402
    NOTICE_NAME,
    NOTICE_TEXT,
    VerificationError,
    _archive_digest,
    unpack,
)
from robustfolio import backtest  # noqa: E402
from robustfolio import data as data_mod  # noqa: E402
from robustfolio import report as reporting  # noqa: E402

#: Absolute tolerance for the continuous metrics. It is not zero, and that needs
#: justifying rather than asserting -- it was zero until CI disagreed twice.
#:
#: The original claim was "tolerance exactly zero". It held on the machine that
#: produced the table. It held on the first CI runner, which mismatched on one
#: column by 4.2e-17 (finding F33). On the next runner it mismatched on thirteen
#: columns, the worst by 4.698e-12 (finding F34). There are two causes and neither
#: is a bug in this repository:
#:
#:   1. The estimator's covariance is a matrix product, evaluated by a BLAS kernel
#:      that OpenBLAS selects from the CPU's features **at run time**. Two machines
#:      may therefore disagree in the last bits of Sigma-hat (F33 found the same
#:      mechanism in a single metric). Thread count is not the cause: running this
#:      whole pipeline on one machine with one BLAS thread and with four produces
#:      byte-identical tables, checked.
#:   2. A quadratic program is solved only to its solver's tolerance. The frozen
#:      ``SOLVER_TOL`` is 1e-14, so the optimal portfolio is defined to about that
#:      much, and a 1e-16 difference in the input reappears in the weights at
#:      ~1e-12. Asking for bit-for-bit equality of a solver's output across CPUs
#:      asks for something the artefact never had.
#:
#: So the claim is split, and the stronger half is the half that matters:
#:
#:   * every **decision-bearing** quantity is compared **exactly** -- the method
#:     set and its order, the rebalance and fold counts, the headline cost level,
#:     the ranking by net Sharpe, and which baseline the §6.1/§6.2 rule selects;
#:   * the continuous metrics are compared within ``TOLERANCE``, and the observed
#:     worst-case difference is printed on every run rather than hidden.
#:
#: 1e-9 is about 200x the worst difference measured across two platforms, and five
#: orders of magnitude below the four decimals at which any of these numbers is
#: quoted or compared. It is loose enough to survive a runtime-chosen kernel and
#: far too tight to survive a changed estimator, cost model or window -- which is
#: what a verifier is for.
#:
#: The margin is stated in *exactly one* runnable place and derived from the two
#: constants it relates (``TOLERANCE`` and ``report.PRINTED_DECIMALS``), asserted by
#: tests/test_release_verification.py. It was previously restated in six artefacts,
#: and three of them had drifted to the wrong order of magnitude, which is the F29
#: failure mode -- a value written down twice drifts -- applied to prose.
TOLERANCE = 1e-9

#: Counts and labels rather than measurements. A different rebalance count or
#: headline cost level is a different experiment, not a rounding difference.
EXACT_COLUMNS = ("rebalances", "folds", "headline_cost_bps")

#: The fields of ``decisions.csv`` that *are* the verdict. The eight ``pass_*``
#: booleans are §6.1-§6.4's individual gates, the three summary flags are the
#: statistical/material/robust conjunction, and ``verdict`` is the sentence the
#: README publishes. Comparing these against a tolerance would be treating a
#: decision as if it were a measurement, so they are compared exactly: a verdict
#: that changes is a different result no matter how little the statistics moved.
#:
#: This is the half of the claim that was missing until DEC-20261018-041. The
#: verifier compared the metrics and the *ranking*, and the ranking was standing in
#: for the verdict -- which happens to agree here and need not in general, because
#: §6.1-§6.4 decide with a conjunction that the ranking does not represent.
#:
#: The candidate identity is not in this tuple because it is the table's *index*;
#: :func:`compare_decisions` compares the index separately and exactly.
DECISION_EXACT_COLUMNS = (
    "baseline",
    "dsr_family_size",
    "dsr_v_is_convention",
    "pass_psr",
    "pass_dsr",
    "pass_sharpe_gap",
    "pass_turnover",
    "pass_drawdown",
    "pass_cost_levels",
    "pass_folds",
    "pass_fold_share",
    "cost_levels_won",
    "cost_levels_required",
    "folds_won",
    "folds_required",
    "statistical",
    "material",
    "robust",
    "verdict",
)

#: The metric the §6.1/§6.2 rules rank methods by, and therefore a decision
#: rather than a measurement.
HEADLINE_METRIC = "net_sharpe"


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--archive", type=Path, required=True,
                        help="release snapshot archive (.tar.gz)")
    parser.add_argument("--run", type=Path, required=True,
                        help="published run directory: outcomes.csv and decisions.csv")
    parser.add_argument("--expect-sha256", default=None,
                        help="digest quoted in the release notes; the archive must match it")
    parser.add_argument("--headline-bps", type=int, default=None,
                        help="headline cost level; defaults to the frozen value")
    parser.add_argument("--keep", type=Path, default=None,
                        help="extract the snapshot here instead of a temporary directory")
    return parser.parse_args(argv)


def _load_published(path: Path) -> pd.DataFrame:
    """Read a published table without the default parser's ULP-level loss."""
    return pd.read_csv(path, index_col=0, float_precision="round_trip")


def _check_notice(snapshot_dir: Path) -> None:
    """An archive without its notice is not the archive the release published.

    Finding F30 / DEC-20261017-034: the notice states that the third-party market
    data is *not* covered by the repository's MIT licence. It is deliberately kept
    out of ``manifest.json``'s hash map -- it is a statement about the data, not an
    input to it -- which also makes it cheap to lose. So its presence is asserted
    here rather than assumed, and a re-pack that dropped it fails loudly instead of
    publishing a data dump with no statement attached.
    """
    notice = snapshot_dir / NOTICE_NAME
    if not notice.exists():
        raise VerificationError(
            f"{NOTICE_NAME} is missing from the snapshot. This archive redistributes "
            "third-party data and must carry the statement about it (finding F30); "
            "an archive without it is not the one the release published."
        )
    if notice.read_text(encoding="utf-8") != NOTICE_TEXT:
        raise VerificationError(
            f"{NOTICE_NAME} in the archive differs from the template in "
            "pack_snapshot.py. The notice is generated, never stored on disk, so a "
            "difference means the archive was built by different code."
        )
    print(f"notice       : {NOTICE_NAME} present, unchanged")


def compare(
    recomputed: pd.DataFrame,
    published: pd.DataFrame,
    *,
    tolerance: float = TOLERANCE,
) -> tuple[float, list[str], list[str]]:
    """Classify a re-run against the published table.

    Returns ``(worst_absolute_difference, columns_beyond_tolerance,
    exact_comparisons_that_failed)``. The split is the whole point of the
    function: *which* method won, over how many rebalances, at which cost level,
    and against which benchmark are not approximate quantities, so they are
    compared exactly; the measurements behind them are approximate, so they are
    compared against a documented bound.
    """
    problems: list[str] = []

    if list(recomputed.index) != list(published.index):
        problems.append(
            f"method set or order differs: {list(recomputed.index)} vs {list(published.index)}"
        )
        return float("inf"), [], problems

    shared = [column for column in recomputed.columns if column in published.columns]
    published = published.loc[recomputed.index, shared]
    # Counts and labels are *checked exactly* below, so they are deliberately not
    # also measured against a tolerance: that would let a different experiment
    # pass as a rounding difference.
    numeric = [
        c for c in shared
        if pd.api.types.is_numeric_dtype(recomputed[c]) and c not in EXACT_COLUMNS
    ]

    if numeric:
        diff = (recomputed[numeric].astype(float) - published[numeric].astype(float)).abs()
        worst = float(diff.max().max())
        offenders = [column for column in diff.columns if float(diff[column].max()) > tolerance]
    else:
        worst, offenders = 0.0, []

    for column in EXACT_COLUMNS:
        if column in shared and not np.array_equal(
            recomputed[column].to_numpy(), published[column].to_numpy()
        ):
            problems.append(
                f"{column} differs: {recomputed[column].tolist()} vs {published[column].tolist()}"
            )

    if HEADLINE_METRIC in shared:
        order_new = list(recomputed[HEADLINE_METRIC].astype(float).sort_values(ascending=False).index)
        order_pub = list(published[HEADLINE_METRIC].astype(float).sort_values(ascending=False).index)
        if order_new != order_pub:
            problems.append(
                f"ranking by {HEADLINE_METRIC} differs: {order_new} vs {order_pub}"
            )

        baselines = [b for b in reporting.BASELINE_IDS if b in recomputed.index]
        if baselines:
            best_new = max(baselines, key=lambda b: float(recomputed.loc[b, HEADLINE_METRIC]))
            best_pub = max(baselines, key=lambda b: float(published.loc[b, HEADLINE_METRIC]))
            if best_new != best_pub:
                problems.append(
                    f"best baseline differs: {best_new} vs {best_pub}. Every candidate "
                    "would be compared against a different benchmark, which is a "
                    "different experiment, not a rounding difference."
                )

    return worst, offenders, problems


def compare_decisions(
    recomputed: pd.DataFrame,
    published: pd.DataFrame,
    *,
    tolerance: float = TOLERANCE,
) -> tuple[float, list[str], list[str]]:
    """Classify a re-run's verdict table against the published one.

    Same contract as :func:`compare`, and the same split, but this is the half that
    says what the run *found*. A candidate's verdict is a decision, so the fields
    that carry it are compared exactly; the statistics those fields were computed
    from are compared within the documented bound, because they are measurements.

    The two halves are deliberately not merged into one comparison: a metric that
    moved by ``1e-12`` must not be able to fail this, and a ``verdict`` that flipped
    must not be able to pass it however small the statistics that produced it.
    """
    problems: list[str] = []

    if list(recomputed.index) != list(published.index):
        problems.append(
            f"candidate set or order differs: {list(recomputed.index)} vs "
            f"{list(published.index)}"
        )
        return float("inf"), [], problems

    shared = [column for column in recomputed.columns if column in published.columns]
    published = published.loc[recomputed.index, shared]

    numeric = [
        c for c in shared
        if c not in DECISION_EXACT_COLUMNS
        and pd.api.types.is_numeric_dtype(recomputed[c])
        and pd.api.types.is_numeric_dtype(published[c])
    ]
    if numeric:
        diff = (recomputed[numeric].astype(float) - published[numeric].astype(float)).abs()
        worst = float(diff.max().max())
        offenders = [c for c in diff.columns if float(diff[c].max()) > tolerance]
    else:
        worst, offenders = 0.0, []

    for column in shared:
        if column not in DECISION_EXACT_COLUMNS:
            continue
        left = recomputed[column].tolist()
        right = published[column].tolist()
        if left != right:
            label = "VERDICT" if column == "verdict" else column
            problems.append(f"{label} differs: {left} vs {right}")

    return worst, offenders, problems


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)

    # -- link 4: the archive must match the digest the release published ------- #
    digest = _archive_digest(args.archive)
    print(f"archive      : {args.archive.name}")
    print(f"archive sha  : {digest}")

    expected = args.expect_sha256
    sidecar = args.archive.with_suffix(args.archive.suffix + ".sha256")
    if expected is None and sidecar.exists():
        expected = sidecar.read_text(encoding="utf-8").split()[0]
        print(f"expected sha : {expected}  (from {sidecar.name})")
    if expected is not None and expected.strip().lower() != digest:
        print("\nMISMATCH: the archive does not match the published digest", file=sys.stderr)
        return 1

    run_dir = Path(args.run)
    published = _load_published(run_dir / "outcomes.csv")
    decisions_path = run_dir / "decisions.csv"
    if not decisions_path.exists():
        print(
            f"\nMISSING: {decisions_path} is not there, so the verdicts cannot be "
            "compared.\nA published run is outcomes.csv *and* decisions.csv "
            "(DEC-20261018-041). The verdict is a decision; checking the metrics that "
            "were computed to support a sentence, while skipping the sentence, leaves "
            "the most decision-bearing quantity in the run unexamined.",
            file=sys.stderr,
        )
        return 1
    published_decisions = _load_published(decisions_path)

    def reproduce(snapshot_dir: Path) -> tuple[pd.DataFrame, pd.DataFrame]:
        data_mod.SNAPSHOTS_DIR = Path(snapshot_dir)
        ids = data_mod.list_snapshots()
        if not ids:
            raise VerificationError(f"no snapshot inside {snapshot_dir}")
        snapshot = data_mod.load_snapshot(ids[0], verify=True)
        results = {m: backtest.run_method(snapshot, m) for m in backtest.METHOD_IDS}
        kwargs = {"rf": snapshot.rf_monthly(), "bootstrap": False, "calibration_window": False}
        if args.headline_bps is not None:
            kwargs["headline_bps"] = args.headline_bps
        # One path, not two: ``build_report`` is what ``run_experiment.py`` calls to
        # write the published CSVs, so the check cannot drift from the writer.
        run = reporting.build_report(results, snapshot_id=ids[0], **kwargs)
        return run.outcomes, run.decisions

    if args.keep is not None:
        args.keep.mkdir(parents=True, exist_ok=True)
        snapshot_dir = unpack(args.archive, args.keep, force=True)
        _check_notice(snapshot_dir)
        recomputed, recomputed_decisions = reproduce(snapshot_dir.parent)
    else:
        with tempfile.TemporaryDirectory() as tmp:
            snapshot_dir = unpack(args.archive, Path(tmp))
            _check_notice(snapshot_dir)
            recomputed, recomputed_decisions = reproduce(Path(tmp))

    worst, offenders, exact_problems = compare(recomputed, published)
    d_worst, d_offenders, d_problems = compare_decisions(
        recomputed_decisions, published_decisions
    )

    verdicts = (
        " / ".join(f"{m} {v}" for m, v in recomputed_decisions["verdict"].items())
        if "verdict" in recomputed_decisions.columns else "not reported"
    )

    shared = [column for column in recomputed.columns if column in published.columns]
    print(f"methods      : {len(recomputed)}")
    print(f"columns      : {len(shared)}")
    print(f"verdicts     : {verdicts}  ({len(recomputed_decisions)} candidates)")
    print(f"max abs diff : {max(worst, d_worst):.3e}")
    print(f"tolerance    : {TOLERANCE:.0e}")
    print()

    if exact_problems or d_problems:
        print("DECISION MISMATCH -- these are exact quantities, not measurements:", file=sys.stderr)
        for problem in exact_problems + d_problems:
            print(f"  {problem}", file=sys.stderr)
        print(
            "\nThe archive no longer produces the published *decisions*, which no "
            "amount of floating-point slack can excuse: the method set, the window, "
            "the cost level, the ranking, the benchmark and the §6.4 verdict are all "
            "discrete. Either the snapshot is not the one the run used, or the code "
            "has changed since the run was published.",
            file=sys.stderr,
        )
        return 1

    if offenders or d_offenders:
        print("MISMATCH beyond tolerance on the following columns:", file=sys.stderr)
        for column in offenders:
            value = float((recomputed[column].astype(float) - published.loc[recomputed.index, column].astype(float)).abs().max())
            print(f"  {column}: {value:.3e}", file=sys.stderr)
        for column in d_offenders:
            value = float(
                (
                    recomputed_decisions[column].astype(float)
                    - published_decisions.loc[recomputed_decisions.index, column].astype(float)
                ).abs().max()
            )
            print(f"  decisions.{column}: {value:.3e}", file=sys.stderr)
        print(
            f"\nThe archive no longer reproduces the published run: at least one metric "
            f"is more than {TOLERANCE:.0e} away, which is far outside the "
            "runtime-kernel differences this tolerance exists to absorb (findings "
            "F33/F34). Either the snapshot is not the one the run used, or the code "
            "has changed since the run was published. Both invalidate the run.",
            file=sys.stderr,
        )
        return 1

    if worst == 0.0 and d_worst == 0.0:
        print("EXACT: the release archive reproduces every published metric bit-for-bit,")
        print(f"and every decision-bearing quantity is identical -- including the verdict")
        print(f"on both candidates ({verdicts}).")
        print("(The frozen seed, the frozen tolerance and the immutable snapshot are what")
        print(" make this an equality rather than an approximation -- on this machine.)")
    else:
        print(f"WITHIN {TOLERANCE:.0e}: the archive reproduces every published metric to {max(worst, d_worst):.3e}")
        print("on this machine, and every decision-bearing quantity -- the method set, the")
        print("window, the cost level, the ranking, the benchmark baseline and the verdict")
        print(f"({verdicts}) -- is identical.")
        print("The residual is not slack in the claim: it is a BLAS kernel chosen from the")
        print("CPU's features at run time, amplified by the solver's own tolerance. See")
        print("finding F34 in docs/decision_log.md for how this bound was measured.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
