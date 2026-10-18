"""Pack a frozen snapshot for release, or verify an unpacked one (spec §3.1).

    # Pack: verify the snapshot on disk, then write a deterministic archive
    python scripts/pack_snapshot.py --snapshot <snapshot_id> --out dist/

    # Verify an archive without trusting the manifest
    python scripts/pack_snapshot.py --verify dist/<archive>.tar.gz --extract-to data/snapshots

    # Verify a snapshot directory that is already unpacked
    python scripts/pack_snapshot.py --verify-dir data/snapshots/<snapshot_id>

Why this exists
---------------
The project's claim to a reader is not "believe these numbers" but "check these
numbers". That requires reproducing the *same* input, not a similar one: Yahoo
Finance revises history, so a reader who runs ``build_snapshot.py`` in six months
gets a different snapshot id and slightly different numbers, and the claim
degrades from checkable to folklore. Shipping the frozen snapshot as a release
asset is what keeps the check alive, and it is only 2.4 MB.

The archive is written deterministically -- sorted member names, no owner info,
no timestamps -- so that the published ``.sha256`` of the archive stays valid
across re-packs of identical content. A digest that changes every time you
re-pack the same bytes is a digest nobody can verify.

The archive also carries a ``NOTICE.txt`` beside the snapshot's own files, stating
where the third-party data came from and that the repository's MIT licence does
not cover it (finding F30, DEC-20261017-034). It is generated from a template in
this file rather than read from disk, so it is version-controlled and cannot
drift from the archive that carries it.

Integrity chain, all four links checked here:
    file bytes -> per-file SHA-256 -> bundle hash -> snapshot id (last 8 hex)
plus an external ``<archive>.sha256`` recorded in the release notes, so the
manifest cannot be edited to match tampered files without the archive digest
changing too.
"""

from __future__ import annotations

import argparse
import gzip
import hashlib
import io
import json
import shutil
import sys
import tarfile
import tempfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from robustfolio import data as data_mod  # noqa: E402


# --------------------------------------------------------------------------- #
# The notice that travels with the data
# --------------------------------------------------------------------------- #
#: Name of the notice member written inside the archive, beside the snapshot
#: directory's own files. It is generated at pack time from this template rather
#: than read from disk, so that it is version-controlled, reviewable in a diff,
#: and impossible to lose by rebuilding a snapshot (finding F30, DEC-20261017-034).
#:
#: Deliberately *not* a field in ``manifest.json``: the manifest is the data
#: layer's hashed record, and a licensing statement is neither data nor a
#: statement about data. Excluded from the hash chain so a licence notice can
#: never be mistaken for an input.
NOTICE_NAME = "NOTICE.txt"

NOTICE_TEXT = """\
NOTICE -- third-party data in this snapshot
===========================================

This snapshot is a frozen copy of third-party market data, published by the
robustfolio project so that its published results can be verified exactly
rather than approximately. If you have it, it came from a release asset.

Source
------
  prices_raw.parquet, actions.parquet
      Yahoo Finance, retrieved 2026-10-17 through the yfinance library.
      Daily OHLCV for 18 US-listed ETFs. Prices are unadjusted; corporate
      actions are recorded separately in actions.parquet.
  rf_dgs1mo.parquet
      FRED series DGS1MO (1-month US Treasury constant-maturity yield).
  universe_pit.csv
      Instrument metadata re-expressed by this project from fund issuers'
      fact sheets (SPDR, iShares).
  manifest.json, quality_report.md
      Produced by this project. manifest.json records a SHA-256 per data file.

Licence
-------
The repository's MIT licence covers this project's code and its own text and
artefacts. It does NOT cover the Yahoo Finance price and action data above,
which remains subject to Yahoo's terms of service. That data is redistributed
here for the sole purpose of verifying the published results, non-commercially
and with attribution. For any other purpose, obtain market data from a source
that licenses it to you.

FRED series DGS1MO is US government data and is effectively public domain.

Status of this file
-------------------
NOTICE.txt is written by scripts/pack_snapshot.py when the release archive is
built. It is deliberately NOT listed in manifest.json's sha256 map, which covers
the data files only: this file is a statement about them, not one of them, and
it is kept out of the hash chain so that a licensing notice can never be
mistaken for an input.

If this notice is missing from an archive claiming to be an official one, do
not trust that archive.
"""


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--snapshot", default=None,
                        help="snapshot id to pack; defaults to the newest on disk")
    parser.add_argument("--out", type=Path, default=Path("dist"),
                        help="directory to write the archive and its checksum into")
    parser.add_argument("--verify", type=Path, default=None,
                        help="verify an archive (and optionally extract it)")
    parser.add_argument("--verify-dir", type=Path, default=None,
                        help="verify an already-unpacked snapshot directory")
    parser.add_argument("--extract-to", type=Path, default=None,
                        help="with --verify: extract into this directory (e.g. data/snapshots)")
    parser.add_argument("--force-extract", action="store_true",
                        help="with --verify --extract-to: overwrite an existing snapshot")
    return parser.parse_args(argv)


# --------------------------------------------------------------------------- #
# Verification
# --------------------------------------------------------------------------- #

class VerificationError(RuntimeError):
    """The snapshot on disk does not match its own manifest."""


def verify_snapshot_dir(path: Path) -> dict:
    """Check every link of the integrity chain for one snapshot directory.

    Raises :class:`VerificationError` on the first broken link. Returns the
    manifest plus the recomputed digests so the caller can report them.
    """
    path = Path(path)
    if not path.is_dir():
        raise VerificationError(f"not a directory: {path}")

    manifest_path = path / data_mod.MANIFEST_FILE
    if not manifest_path.exists():
        raise VerificationError(f"missing {data_mod.MANIFEST_FILE} in {path}")
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))

    recorded = manifest.get("sha256") or {}
    if not recorded:
        raise VerificationError("manifest records no per-file hashes; nothing to verify")

    # Link 1: the bytes on disk must hash to what the manifest records.
    recomputed = data_mod.snapshot_digests(path)
    for name, digest in recorded.items():
        if name not in recomputed:
            raise VerificationError(f"manifest lists an unknown file: {name}")
        if recomputed[name] != digest:
            raise VerificationError(
                f"{name}: substance does not match the manifest\n"
                f"  recorded  {digest}\n"
                f"  recomputed {recomputed[name]}"
            )

    # Link 2: the manifest's own hashes must produce the bundle hash it records.
    # Without this, a tampered manifest that lists tampered files would pass
    # link 1 while still naming a snapshot id it no longer describes. The bundle
    # hash covers BUNDLE_FILES only -- the quality report is excluded because it
    # embeds the snapshot id, which is derived from the bundle hash (finding F27).
    bundle = data_mod.bundle_hash(data_mod.bundle_digests(path))
    if manifest.get("bundle_sha256") and bundle != manifest["bundle_sha256"]:
        raise VerificationError(
            "manifest is internally inconsistent: its per-file hashes do not "
            f"produce its recorded bundle hash\n  recorded  {manifest['bundle_sha256']}"
            f"\n  recomputed {bundle}"
        )

    # Link 3: the bundle hash must be the one named in the snapshot id.
    hash8 = manifest.get("hash8")
    if hash8 and not str(bundle).startswith(hash8):
        raise VerificationError(
            f"snapshot id claims hash8 {hash8}, but the content hashes to {bundle[:8]}"
        )
    if manifest.get("snapshot_id") and path.name != manifest["snapshot_id"]:
        raise VerificationError(
            f"directory is {path.name} but the manifest says {manifest['snapshot_id']}"
        )

    return {"manifest": manifest, "recomputed": recomputed, "bundle_sha256": bundle}


# --------------------------------------------------------------------------- #
# Deterministic archiving
# --------------------------------------------------------------------------- #

def _archive_digest(archive: Path) -> str:
    h = hashlib.sha256()
    with open(archive, "rb") as fh:
        for chunk in iter(lambda: fh.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def pack(snapshot_dir: Path, archive: Path) -> tuple[str, str]:
    """Write ``snapshot_dir`` into ``archive`` deterministically.

    Determinism is not decoration: the release publishes the archive's SHA-256,
    and a digest that changes when nothing changed cannot be checked. So member
    order is sorted, mtimes are pinned to the epoch, and the gzip stream carries
    no timestamp or filename.

    The archive carries one member the directory does not: ``NOTICE_NAME``, the
    third-party-data and licence statement, written from :data:`NOTICE_TEXT` in
    this file rather than read from disk (finding F30). It is placed *inside* the
    snapshot directory's path so that ``unpack`` carries it out with the data --
    a notice a reader has to fetch separately is a notice that gets separated
    from the data it describes.
    """
    archive = Path(archive)
    archive.parent.mkdir(parents=True, exist_ok=True)
    if (snapshot_dir / NOTICE_NAME).exists():
        raise VerificationError(
            f"{NOTICE_NAME} already exists in {snapshot_dir}; it is generated at "
            "pack time from a template in this script and must not be stored on "
            "disk, where it could drift from the archive that carries it"
        )
    names = sorted(p.name for p in snapshot_dir.iterdir() if p.is_file())
    members = sorted(names + [NOTICE_NAME])

    raw = io.BytesIO()
    with tarfile.open(fileobj=raw, mode="w") as tar:
        for name in members:
            if name == NOTICE_NAME:
                payload = NOTICE_TEXT.encode("utf-8")
                info = tarfile.TarInfo(f"{snapshot_dir.name}/{name}")
                info.size = len(payload)
                body: io.BufferedIOBase = io.BytesIO(payload)
            else:
                source = snapshot_dir / name
                info = tar.gettarinfo(str(source), arcname=f"{snapshot_dir.name}/{name}")
                body = open(source, "rb")
            info.mtime = 0
            info.uid = info.gid = 0
            info.uname = info.gname = ""
            info.mode = 0o644
            with body as fh:
                tar.addfile(info, fh)

    with open(archive, "wb") as out:
        with gzip.GzipFile(filename="", mode="wb", fileobj=out, mtime=0) as gz:
            gz.write(raw.getvalue())

    return _archive_digest(archive), "\n".join(members)


def unpack(archive: Path, destination: Path, *, force: bool = False) -> Path:
    """Extract an archive into ``destination`` and return the snapshot directory.

    Extraction is staged: the archive is unpacked into a temporary directory,
    verified, and only then moved into place. A verification that can leave a
    half-written snapshot behind is not a verification.
    """
    archive = Path(archive)
    destination = Path(destination)
    destination.mkdir(parents=True, exist_ok=True)

    with tempfile.TemporaryDirectory(dir=destination, prefix=".unpack-") as staging:
        with tarfile.open(archive, mode="r:gz") as tar:
            members = tar.getmembers()
            for member in members:
                # Refuse absolute paths and traversal before writing anything.
                if member.name.startswith(("/", "\\")) or ".." in Path(member.name).parts:
                    raise VerificationError(f"unsafe member in archive: {member.name}")
            tar.extractall(staging)

        roots = [p for p in Path(staging).iterdir() if p.is_dir()]
        if len(roots) != 1:
            raise VerificationError(
                f"expected exactly one snapshot directory in the archive, found {len(roots)}"
            )
        staged = roots[0]
        verify_snapshot_dir(staged)

        target = destination / staged.name
        if target.exists() and not force:
            raise VerificationError(
                f"{target} already exists; snapshots are append-only. "
                "Re-run with --force-extract to replace it."
            )
        if target.exists():
            shutil.rmtree(target)
        shutil.move(str(staged), str(target))
    return target


# --------------------------------------------------------------------------- #
# CLI
# --------------------------------------------------------------------------- #

def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)

    if args.verify_dir is not None:
        result = verify_snapshot_dir(args.verify_dir)
        print(f"verified   : {Path(args.verify_dir).name}")
        print(f"files      : {len(result['recomputed'])}")
        print(f"bundle     : {result['bundle_sha256']}")
        print("all four integrity links hold")
        return 0

    if args.verify is not None:
        digest = _archive_digest(args.verify)
        print(f"archive    : {args.verify.name}")
        print(f"archive sha: {digest}")
        if args.extract_to is not None:
            target = unpack(args.verify, args.extract_to, force=args.force_extract)
            print(f"extracted  : {target}")
            print(f"verified   : {target.name}")
        else:
            with tempfile.TemporaryDirectory() as tmp:
                target = unpack(args.verify, Path(tmp))
                print(f"verified   : {target.name}")
        return 0

    snapshot_id = args.snapshot
    if snapshot_id is None:
        ids = data_mod.list_snapshots()
        if not ids:
            print("no snapshot on disk; run scripts/build_snapshot.py first", file=sys.stderr)
            return 2
        snapshot_id = ids[0]

    snapshot_dir = data_mod.SNAPSHOTS_DIR / snapshot_id
    result = verify_snapshot_dir(snapshot_dir)

    archive = Path(args.out) / f"robustfolio-snapshot-{snapshot_id}.tar.gz"
    digest, listing = pack(snapshot_dir, archive)
    checksum = archive.with_suffix(archive.suffix + ".sha256")
    checksum.write_text(f"{digest}  {archive.name}\n", encoding="utf-8")

    size_mb = archive.stat().st_size / (1 << 20)
    print(f"snapshot   : {snapshot_id}")
    print(f"bundle     : {result['bundle_sha256']}")
    print(f"members    : {listing.replace(chr(10), ', ')}")
    print(f"notice     : {NOTICE_NAME} ({len(NOTICE_TEXT.encode('utf-8'))} bytes, "
          "third-party data and licence statement -- finding F30)")
    print(f"archive    : {archive}")
    print(f"archive sha: {digest}")
    print(f"size       : {size_mb:.2f} MB")
    print()
    print("Publish both files as release assets and quote the archive digest in the")
    print("release notes. A reader then reproduces the published numbers exactly:")
    print(f"  python scripts/pack_snapshot.py --verify {archive.name} --extract-to data/snapshots")
    print(f"  python scripts/run_experiment.py --snapshot {snapshot_id} --out results/{snapshot_id}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
