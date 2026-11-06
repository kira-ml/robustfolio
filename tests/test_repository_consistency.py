"""Cross-file consistency that is easy to drift and cheap to check.

The package version and the citation version are two copies of one fact; the
committed CSV headers are a third kind of copy, where a duplicated index name
looks like a normal column until someone tries to parse it.
"""

from __future__ import annotations

import csv
import re
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]


def _pyproject_version() -> str:
    text = (ROOT / "pyproject.toml").read_text(encoding="utf-8")
    match = re.search(r'^version = "([^"]+)"$', text, re.MULTILINE)
    assert match, "pyproject.toml has no version"
    return match.group(1)


def _citation_version() -> str:
    text = (ROOT / "CITATION.cff").read_text(encoding="utf-8")
    match = re.search(r'^version: "([^"]+)"$', text, re.MULTILINE)
    assert match, "CITATION.cff has no version"
    return match.group(1)


def _package_version() -> str:
    import robustfolio

    return robustfolio.__version__


def test_package_and_citation_versions_agree() -> None:
    versions = {
        "pyproject.toml": _pyproject_version(),
        "CITATION.cff": _citation_version(),
        "robustfolio.__version__": _package_version(),
    }
    assert len(set(versions.values())) == 1, versions


def _public_csvs() -> list[Path]:
    paths = sorted((ROOT / "docs" / "published-run").rglob("*.csv"))
    paths += sorted((ROOT / "notes").glob("*.csv"))
    phase1 = ROOT / "results" / "phase1_results.csv"
    if phase1.exists():
        paths.append(phase1)
    return paths


@pytest.mark.parametrize("path", _public_csvs(), ids=lambda p: str(p.relative_to(ROOT)))
def test_committed_csv_headers_are_unique(path: Path) -> None:
    with path.open(newline="", encoding="utf-8") as handle:
        header = next(csv.reader(handle))
    assert len(header) == len(set(header)), f"duplicate column in {path.name}: {header}"
