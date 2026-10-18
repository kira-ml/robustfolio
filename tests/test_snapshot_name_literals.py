"""One name, written down in four places, is four chances to get it wrong.

The frozen snapshot is identified by a string built from a tickers label, a window
start, a window end, a retrieval date and a content hash, joined by a rule the
builder knows and a human does not:

    yahoo-usetf-2007-01-01_2026-09-30-2026-10-17-2ad06139
              ^tickers ^start  ^end       ^retrieved ^hash8

One underscore. Not two, and not where intuition puts the second one. The name is
quoted by hand in the README's reproduction command, in the CI workflow, and in a
document, and a single wrong separator makes `curl` return 404 while looking
exactly as plausible as the right one. That is finding **F32**, and this file is
the fix: the literals are compared against each other and -- when the frozen
snapshot is on disk -- against the filesystem, which is the only authority for
whether a name exists.

On a fresh clone the filesystem check skips and this is a consistency check. CI is
not a fresh clone: it fetches the release asset, so there the same tests compare
the literals to a real archive. The cheap check runs everywhere; the strong check
runs where it can.
"""

from __future__ import annotations

import re
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
CI_YML = ROOT / ".github" / "workflows" / "ci.yml"
README = ROOT / "README.md"
PUBLISHED_RUN = ROOT / "docs" / "published-run" / "README.md"
SNAPSHOTS_DIR = ROOT / "data" / "snapshots"

#: Literals that are legitimately not the live snapshot id -- an old id quoted in
#: a historical record, say. Empty, and meant to stay that way: every entry has to
#: be justified to a reader who wonders why a name in the repo is not the name.
ALLOWED_LITERALS: frozenset[str] = frozenset()

#: Assembled from fragments so that this file does not itself contain a literal
#: snapshot name for the scan below to trip over.
_NAME_RE = re.compile(r"yahoo" + r"-usetf-[0-9a-z_\-]+")

_SCANNED_SUFFIXES = {".md", ".py", ".yml", ".yaml", ".toml", ".cfg", ".txt", ".csv", ".json"}
_SKIPPED_PARTS = {".git", ".venv", "__pycache__", ".pytest_cache", "dist", "results", "build"}


def _ci_env() -> dict[str, str]:
    text = CI_YML.read_text(encoding="utf-8")
    env: dict[str, str] = {}
    for key in ("RELEASE_TAG", "SNAPSHOT_ASSET", "SNAPSHOT_ID", "ARCHIVE_SHA256"):
        match = re.search(rf"^\s*{key}:\s*(\S+)\s*$", text, re.MULTILINE)
        assert match, f"{key} is no longer defined in {CI_YML.name}; this test is now blind"
        env[key] = match.group(1)
    return env


def _scan() -> list[tuple[Path, int, str]]:
    found: list[tuple[Path, int, str]] = []
    for path in sorted(ROOT.rglob("*")):
        if not path.is_file() or path.suffix.lower() not in _SCANNED_SUFFIXES:
            continue
        if any(part in _SKIPPED_PARTS for part in path.relative_to(ROOT).parts):
            continue
        try:
            text = path.read_text(encoding="utf-8")
        except (UnicodeDecodeError, OSError):
            continue
        for line_no, line in enumerate(text.splitlines(), 1):
            for value in _NAME_RE.findall(line):
                found.append((path, line_no, value))
    return found


def test_the_archive_name_is_built_from_the_snapshot_id() -> None:
    """The two literals in the workflow have to describe the same object.

    This is the check that catches a separator typo in either one: the asset name
    is not independently typed, it is the id with a prefix and a suffix.
    """
    env = _ci_env()
    assert env["SNAPSHOT_ASSET"] == f"robustfolio-snapshot-{env['SNAPSHOT_ID']}.tar.gz"


def test_every_quoted_snapshot_name_is_the_same_name() -> None:
    """Four hand-written copies of one name is three too many; they must agree."""
    reference = _ci_env()["SNAPSHOT_ID"]
    bad = [(path, line, value) for path, line, value in _scan()
           if value != reference and value not in ALLOWED_LITERALS]

    if bad:
        report = "\n".join(
            f"  {path.relative_to(ROOT)}:{line}\n    found [{value}]\n    want  [{reference}]"
            for path, line, value in bad
        )
        pytest.fail(
            "snapshot name literals do not match the workflow's SNAPSHOT_ID "
            "(finding F32 -- one wrong separator is a 404 that looks plausible):\n"
            + report
        )


def test_the_readme_downloads_the_asset_that_exists() -> None:
    """The README's reproduction command is the one thing a reader runs first."""
    asset = _ci_env()["SNAPSHOT_ASSET"]
    text = README.read_text(encoding="utf-8")
    match = re.search(r"^ASSET=(\S+)$", text, re.MULTILINE)
    assert match, "the README no longer sets ASSET= before its curl; this test is blind"
    assert match.group(1) == asset, (
        "the README's ASSET does not match the workflow's SNAPSHOT_ASSET; "
        "a reader following the README would get a 404"
    )


def test_the_named_snapshot_is_the_one_on_disk() -> None:
    """The literals are checked against a real directory, not against each other.

    Skipped on a fresh clone, where there is nothing to compare to -- but present
    in CI, which fetches the archive, and locally, where the snapshot was built.
    """
    directories = [p.name for p in SNAPSHOTS_DIR.iterdir() if p.is_dir()] if SNAPSHOTS_DIR.is_dir() else []
    if not directories:
        pytest.skip("no frozen snapshot on disk: the literals can only be checked for consistency")

    assert len(directories) == 1, f"expected one frozen snapshot, found {directories}"
    assert directories[0] == _ci_env()["SNAPSHOT_ID"], (
        "the workflow names a snapshot that is not the one on disk -- so the literal "
        "is wrong, or the snapshot was rebuilt without updating the literal"
    )


def test_the_published_run_names_the_frozen_snapshot() -> None:
    """The document that tells a reader what to verify against must name it right."""
    reference = _ci_env()["SNAPSHOT_ID"]
    text = PUBLISHED_RUN.read_text(encoding="utf-8")
    names = set(_NAME_RE.findall(text))
    assert names == {reference}, f"docs/published-run/README.md names {names}, not {reference}"
