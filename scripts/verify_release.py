"""Verify a published run against its release archive (the "check me" command).

    python scripts/verify_release.py --archive dist/<archive>.tar.gz --run results/<run_id>/

Extracts the frozen snapshot from the release archive into a temporary directory,
re-runs all seven methods, rebuilds the metric table, and compares it against the
run's ``outcomes.csv``. Exits non-zero on any mismatch.

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

Both of those were wrong in the first draft of this file's predecessor, and both
produced numbers that looked like findings. A claim that can be checked only by
re-deriving the checker's own bugs is not a checkable claim, so the check is
shipped as code with its tolerances stated.
"""

from __future__ import annotations

import argparse
import sys
import tempfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
sys.path.insert(0, str(Path(__file__).resolve().parent))

import pandas as pd  # noqa: E402

from pack_snapshot import VerificationError, _archive_digest, unpack  # noqa: E402
from robustfolio import backtest  # noqa: E402
from robustfolio import data as data_mod  # noqa: E402
from robustfolio import report as reporting  # noqa: E402

#: Exact-zero tolerance. The claim is bit-for-bit reproduction of the published
#: floats, not "close enough": if a re-run differs at all, the artefact no longer
#: describes what produced it and a reader deserves to know.
TOLERANCE = 0.0


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--archive", type=Path, required=True,
                        help="release snapshot archive (.tar.gz)")
    parser.add_argument("--run", type=Path, required=True,
                        help="published run directory containing outcomes.csv")
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

    published = _load_published(Path(args.run) / "outcomes.csv")

    def reproduce(snapshot_dir: Path) -> pd.DataFrame:
        data_mod.SNAPSHOTS_DIR = Path(snapshot_dir)
        ids = data_mod.list_snapshots()
        if not ids:
            raise VerificationError(f"no snapshot inside {snapshot_dir}")
        snapshot = data_mod.load_snapshot(ids[0], verify=True)
        results = {m: backtest.run_method(snapshot, m) for m in backtest.METHOD_IDS}
        kwargs = {"rf": snapshot.rf_monthly(), "bootstrap": False}
        if args.headline_bps is not None:
            kwargs["headline_bps"] = args.headline_bps
        return reporting.outcome_table(results, **kwargs)

    if args.keep is not None:
        args.keep.mkdir(parents=True, exist_ok=True)
        snapshot_dir = unpack(args.archive, args.keep, force=True)
        recomputed = reproduce(snapshot_dir.parent)
    else:
        with tempfile.TemporaryDirectory() as tmp:
            snapshot_dir = unpack(args.archive, Path(tmp))
            recomputed = reproduce(Path(tmp))

    shared = [c for c in recomputed.columns if c in published.columns]
    compared = published.loc[recomputed.index, shared].astype(float)
    diff = (recomputed[shared].astype(float) - compared).abs()

    worst = diff.max().max()
    print(f"methods      : {len(recomputed)}")
    print(f"columns      : {len(shared)}")
    print(f"max abs diff : {worst:.3e}")
    print()

    offenders = diff.max().loc[lambda s: s > TOLERANCE].sort_values(ascending=False)
    if len(offenders):
        print("MISMATCH on the following columns:", file=sys.stderr)
        for column, value in offenders.items():
            print(f"  {column}: {value:.3e}", file=sys.stderr)
        print(
            "\nThe archive no longer reproduces the published run. Either the "
            "snapshot is not the one the run used, or the code has changed since "
            "the run was published. Both invalidate the run.",
            file=sys.stderr,
        )
        return 1

    print("EXACT: the release archive reproduces every published metric bit-for-bit.")
    print("(The frozen seed, the frozen tolerance and the immutable snapshot are what")
    print(" make this an equality rather than an approximation.)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
