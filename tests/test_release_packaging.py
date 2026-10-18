"""The release chain must be checkable, so it is checked here.

These tests cover ``scripts/pack_snapshot.py`` and the integrity chain it asserts:

    file bytes -> per-file SHA-256 -> bundle hash -> snapshot id -> archive digest

They are hermetic: they build a *tiny* synthetic snapshot rather than using the
frozen one, so they run on a fresh clone with no data and no network. The finance
is tested elsewhere; what is tested here is that the thing a reader runs to check
our numbers cannot pass while being wrong.

The regression that motivated the last test is worth stating plainly, because it
is the reason this file exists at all: the first draft of the packer recomputed
the bundle hash from ``manifest.json``'s full ``sha256`` map, which lists five
files, while the snapshot id's hash is derived from four (the quality report is
excluded, because it embeds the snapshot id). That draft rejected every valid
snapshot -- a verifier that fails on correct input is more dangerous than none,
because it teaches people to ignore it. Finding F27.
"""

from __future__ import annotations

import json
import sys
import tarfile
from pathlib import Path

import pandas as pd
import pytest

REPO_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO_ROOT / "scripts"))

from pack_snapshot import (  # noqa: E402
    NOTICE_NAME,
    NOTICE_TEXT,
    VerificationError,
    _archive_digest,
    pack,
    unpack,
    verify_snapshot_dir,
)
from robustfolio import data as dm  # noqa: E402

SNAPSHOT_ID = "yahoo-synthetic-2000-01-01_2001-12-31-2002-01-01-abcdef01"


def _write_snapshot(root: Path, *, mutate: dict[str, bytes] | None = None) -> Path:
    """Build a minimal snapshot whose manifest is internally consistent."""
    path = root / SNAPSHOT_ID
    path.mkdir(parents=True)

    index = pd.date_range("2000-01-01", periods=14, freq="D")
    pd.DataFrame({"close": range(14)}, index=index).to_parquet(path / dm.PRICE_FILE)
    pd.DataFrame({"dividends": [0.0] * 14}, index=index).to_parquet(path / dm.ACTIONS_FILE)
    pd.DataFrame({"dgs1mo": [0.01] * 14}, index=index).to_parquet(path / dm.RF_FILE)
    (path / dm.UNIVERSE_FILE).write_text("ticker\nSYN\n", encoding="utf-8")
    (path / dm.QUALITY_FILE).write_text("# synthetic\n", encoding="utf-8")

    if mutate:
        for name, blob in mutate.items():
            (path / name).write_bytes(blob)

    digests = dm.snapshot_digests(path)
    bundle = dm.bundle_hash({name: digests[name] for name in dm.BUNDLE_FILES})
    manifest = {
        "schema_version": 1,
        "snapshot_id": path.name,
        "hash8": bundle[:8],
        "sha256": digests,
        "bundle_sha256": bundle,
    }
    (path / dm.MANIFEST_FILE).write_text(json.dumps(manifest, indent=2), encoding="utf-8")
    return path


@pytest.fixture()
def snapshot_dir(tmp_path: Path) -> Path:
    return _write_snapshot(tmp_path)


# --------------------------------------------------------------------------- #
# The chain holds on a good snapshot
# --------------------------------------------------------------------------- #

def test_valid_snapshot_verifies(snapshot_dir: Path) -> None:
    result = verify_snapshot_dir(snapshot_dir)
    assert result["bundle_sha256"] == json.loads(
        (snapshot_dir / dm.MANIFEST_FILE).read_text(encoding="utf-8")
    )["bundle_sha256"]


def test_bundle_hash_covers_four_files_not_five(snapshot_dir: Path) -> None:
    """F27: the five-file map is exactly what a naive verifier would use."""
    manifest = json.loads((snapshot_dir / dm.MANIFEST_FILE).read_text(encoding="utf-8"))
    recorded = manifest["sha256"]
    assert len(recorded) == len(dm.SNAPSHOT_FILES) == 5
    assert set(dm.BUNDLE_FILES) == set(recorded) - {dm.QUALITY_FILE}

    # The wrong set produces a different bundle hash, which is why the naive
    # verifier rejected every snapshot instead of silently accepting a bad one.
    assert dm.bundle_hash(recorded) != manifest["bundle_sha256"]
    assert dm.bundle_hash({n: recorded[n] for n in dm.BUNDLE_FILES}) == manifest["bundle_sha256"]


# --------------------------------------------------------------------------- #
# The archive round-trips and is deterministic
# --------------------------------------------------------------------------- #

def test_pack_is_deterministic(snapshot_dir: Path, tmp_path: Path) -> None:
    first = tmp_path / "one.tar.gz"
    second = tmp_path / "two.tar.gz"
    digest_a, listing = pack(snapshot_dir, first)
    digest_b, _ = pack(snapshot_dir, second)

    assert digest_a == digest_b
    assert listing == "\n".join(
        sorted([p.name for p in snapshot_dir.iterdir() if p.is_file()] + [NOTICE_NAME])
    )


def test_archive_digest_is_stable_across_process_runs(snapshot_dir: Path, tmp_path: Path) -> None:
    """A published digest must survive a re-pack, so ``mtime`` cannot leak in.

    The mtimes here are deliberately perturbed; the digest must not move.
    """
    archive = tmp_path / "run.tar.gz"
    baseline, _ = pack(snapshot_dir, archive)

    import os
    import time

    touched = snapshot_dir / dm.PRICE_FILE
    os.utime(touched, (time.time() + 4242, time.time() + 4242))

    again = tmp_path / "run2.tar.gz"
    repeat, _ = pack(snapshot_dir, again)
    assert _archive_digest(archive) == baseline == repeat


def test_unpack_verifies_and_places_the_snapshot(snapshot_dir: Path, tmp_path: Path) -> None:
    archive = tmp_path / "snap.tar.gz"
    pack(snapshot_dir, archive)

    destination = tmp_path / "restored"
    restored = unpack(archive, destination)

    assert restored.name == SNAPSHOT_ID
    assert dm.snapshot_digests(restored) == dm.snapshot_digests(snapshot_dir)
    assert not list(destination.glob(".unpack-*")), "staging directory was left behind"


# --------------------------------------------------------------------------- #
# The notice travels with the data (finding F30)
# --------------------------------------------------------------------------- #

def test_archive_carries_the_notice(snapshot_dir: Path, tmp_path: Path) -> None:
    """F30: the data must not travel without the statement that MIT is not its licence."""
    archive = tmp_path / "snap.tar.gz"
    pack(snapshot_dir, archive)

    with tarfile.open(archive, "r:gz") as tar:
        assert f"{SNAPSHOT_ID}/{NOTICE_NAME}" in tar.getnames()
        member = tar.extractfile(f"{SNAPSHOT_ID}/{NOTICE_NAME}")
        assert member is not None
        text = member.read().decode("utf-8")

    assert text == NOTICE_TEXT, "the notice in the archive is not the notice in the source"
    assert "Yahoo" in text and "MIT" in text, "the notice must name the source and the licence"
    assert "does NOT cover" in text


def test_notice_travels_out_of_the_archive_with_the_data(
    snapshot_dir: Path, tmp_path: Path
) -> None:
    """A notice a reader has to fetch separately is one that gets separated."""
    archive = tmp_path / "snap.tar.gz"
    pack(snapshot_dir, archive)

    restored = unpack(archive, tmp_path / "restored")

    notice = restored / NOTICE_NAME
    assert notice.exists(), "the notice did not survive extraction"
    assert notice.read_text(encoding="utf-8") == NOTICE_TEXT


def test_notice_is_not_in_the_hash_chain(snapshot_dir: Path) -> None:
    """The notice is a statement *about* the data, not an input to it.

    If it ever entered ``manifest.json``'s map, the bundle hash would move with a
    purely editorial change and the snapshot id would stop naming its data.
    """
    before = dm.snapshot_digests(snapshot_dir)
    bundle_before = dm.bundle_hash({n: before[n] for n in dm.BUNDLE_FILES})

    (snapshot_dir / NOTICE_NAME).write_text("a notice that drifted", encoding="utf-8")

    assert dm.snapshot_digests(snapshot_dir) == before
    assert dm.bundle_hash({n: before[n] for n in dm.BUNDLE_FILES}) == bundle_before


def test_notice_stored_on_disk_is_refused(snapshot_dir: Path, tmp_path: Path) -> None:
    """The template is the single source of the notice; a copy on disk could drift."""
    (snapshot_dir / NOTICE_NAME).write_text("a stale copy", encoding="utf-8")
    with pytest.raises(VerificationError, match="must not be stored on disk"):
        pack(snapshot_dir, tmp_path / "snap.tar.gz")


# --------------------------------------------------------------------------- #
# Every link of the chain fails loudly when broken
# --------------------------------------------------------------------------- #

def test_tampered_file_is_rejected(snapshot_dir: Path) -> None:
    (snapshot_dir / dm.RF_FILE).write_bytes(b"tampered")
    with pytest.raises(VerificationError, match="substance does not match"):
        verify_snapshot_dir(snapshot_dir)


def test_missing_file_is_rejected(snapshot_dir: Path) -> None:
    (snapshot_dir / dm.ACTIONS_FILE).unlink()
    with pytest.raises(dm.SnapshotError):
        verify_snapshot_dir(snapshot_dir)


def test_manifest_that_matches_tampered_files_is_rejected(snapshot_dir: Path) -> None:
    """The attack link 1 alone cannot catch: rewrite a file *and* its hash.

    Per-file hashing would pass; the bundle hash is derived from the whole map,
    so the recomputed bundle stops matching the recorded one and the snapshot id
    stops describing the content.
    """
    manifest_path = snapshot_dir / dm.MANIFEST_FILE
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))

    blob = b"quietly different bytes"
    (snapshot_dir / dm.RF_FILE).write_bytes(blob)
    manifest["sha256"][dm.RF_FILE] = dm.sha256_file(snapshot_dir / dm.RF_FILE)
    manifest_path.write_text(json.dumps(manifest, indent=2), encoding="utf-8")

    with pytest.raises(VerificationError, match="internally inconsistent"):
        verify_snapshot_dir(snapshot_dir)


def test_snapshot_id_disagreeing_with_content_is_rejected(snapshot_dir: Path) -> None:
    manifest_path = snapshot_dir / dm.MANIFEST_FILE
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    manifest["hash8"] = "00000000"
    manifest_path.write_text(json.dumps(manifest, indent=2), encoding="utf-8")

    with pytest.raises(VerificationError, match="hash8"):
        verify_snapshot_dir(snapshot_dir)


def test_directory_name_disagreeing_with_manifest_is_rejected(snapshot_dir: Path, tmp_path: Path) -> None:
    renamed = snapshot_dir.with_name("yahoo-synthetic-renamed")
    snapshot_dir.rename(renamed)
    with pytest.raises(VerificationError, match="directory is"):
        verify_snapshot_dir(renamed)


def test_unsafe_archive_member_is_refused(tmp_path: Path) -> None:
    """Extraction must refuse traversal before writing anything to disk."""
    import io as _io
    import tarfile

    hostile = tmp_path / "hostile.tar.gz"
    payload = b"pwned"
    with tarfile.open(hostile, mode="w:gz") as tar:
        info = tarfile.TarInfo(name="../escaped.txt")
        info.size = len(payload)
        tar.addfile(info, _io.BytesIO(payload))

    destination = tmp_path / "out"
    with pytest.raises(VerificationError, match="unsafe member"):
        unpack(hostile, destination)
    assert not (tmp_path / "escaped.txt").exists()


def test_extract_refuses_to_overwrite(snapshot_dir: Path, tmp_path: Path) -> None:
    archive = tmp_path / "snap.tar.gz"
    pack(snapshot_dir, archive)
    destination = tmp_path / "restored"
    unpack(archive, destination)
    with pytest.raises(VerificationError, match="append-only"):
        unpack(archive, destination)
