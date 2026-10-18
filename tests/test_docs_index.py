"""Documentation integrity, checked mechanically rather than by inspection.

The project's stated failure mode is a document that *looks* authoritative and is
not. Two version numbers live in two places each, and both had already drifted
before this file existed:

* ``docs/README.md``'s own ``**Version:**`` header against the last row of its
  revision history. It read 1.12 while the history's last row was 1.13 -- the
  same drift that the 1.13 row itself reports having fixed for 1.11 (finding F29).
* the status board's ``Version``/``Status`` columns against each document's own
  ``**Version:**``/``**Status:**`` header. This one is worse than cosmetic: if the
  board says a contract is *Frozen* at 2.4 while the contract says *Draft*, the
  freeze itself is ambiguous, and every "the protocol is frozen" claim in the
  repository rests on that word.

A rule kept by discipline drifts. A rule kept by a test does not. So both are
tests, and they parse the real files rather than a copy of them.
"""

from __future__ import annotations

import re
from pathlib import Path

import pytest

DOCS = Path(__file__).resolve().parents[1] / "docs"
INDEX = DOCS / "README.md"

VERSION_LINE = re.compile(r"^\*\*Version:\*\*\s*([0-9][0-9.]*)\s*$", re.MULTILINE)
STATUS_LINE = re.compile(r"^\*\*Status:\*\*\s*(.+?)\s*$", re.MULTILINE)
#: A revision-history row: | date | version | ... |
REVISION_ROW = re.compile(r"^\|\s*\d{4}-\d{2}-\d{2}\s*\|\s*([0-9][0-9.]*)\s*\|", re.MULTILINE)
#: A status-board row: | # | [`doc.md`](doc.md) | version | status | ...
BOARD_ROW = re.compile(
    r"^\|\s*\d+\s*\|\s*\[`(?P<name>[^`]+)`\]\((?P<path>[^)]+)\)\s*\|"
    r"\s*(?P<version>[^|]*?)\s*\|\s*(?P<status>[^|]*?)\s*\|",
    re.MULTILINE,
)


def _version(text: str) -> str | None:
    match = VERSION_LINE.search(text)
    return match.group(1) if match else None


def _normalise(value: str) -> str:
    """Strip emphasis and footnote markers so `**Frozen**` == `Frozen`."""
    return re.sub(r"[*`~^]", "", value).strip()


def _status_token(value: str) -> str:
    """The single word a status header leads with.

    Documents expand their status into a sentence ("Frozen -- owner-confirmed
    2026-10-17 at v2.3 ..."). Only the leading token is compared: the comparison
    that matters is *Frozen* versus *Draft*, because a contract the board calls
    frozen while the contract calls itself a draft is an ambiguous freeze. The
    rest of the sentence is prose and is allowed to differ.
    """
    head = re.split(r"[(\u2014\u2013,;]", _normalise(value))[0]
    return head.strip().strip(".").lower()


def test_index_version_matches_its_revision_history() -> None:
    text = INDEX.read_text(encoding="utf-8")
    header = _version(text)
    assert header is not None, "docs/README.md has no **Version:** line"

    rows = REVISION_ROW.findall(text)
    assert rows, "docs/README.md has no revision-history rows"

    highest = max(rows, key=lambda v: tuple(int(p) for p in v.split(".")))
    assert header == highest, (
        f"docs/README.md header says {header} but its revision history ends at "
        f"{highest}; bump them together or derive one from the other"
    )

    # A history that goes backwards is a history nobody can date a decision from.
    keys = [tuple(int(p) for p in v.split(".")) for v in rows]
    assert keys == sorted(keys), f"revision history is not monotonic: {rows}"


def test_the_prose_count_of_active_documents_matches_the_board() -> None:
    """The sentence above the board said *seven* while the board listed *eight*.

    It had said seven since E7 was added as row 8 -- the same class of error this
    file already exists to catch (finding F29: a value written down twice drifts),
    except with a count instead of a version. The repair is not a careful count; it
    is to stop keeping the number by hand and count it here, where the table is.
    """
    words = {
        "one": 1, "two": 2, "three": 3, "four": 4, "five": 5, "six": 6,
        "seven": 7, "eight": 8, "nine": 9, "ten": 10, "eleven": 11, "twelve": 12,
    }
    text = INDEX.read_text(encoding="utf-8")
    match = re.search(
        r"The active documentation set is \*\*([a-z]+)\*\* files", text
    )
    assert match, (
        "the sentence stating how many active documents there are has changed shape; "
        "either restore the countable form or update this test with it"
    )

    stated = words[match.group(1)]
    board = BOARD_ROW.findall(text)
    assert stated == len(board), (
        f"the index says the active set is {stated} ({match.group(1)}) files "
        f"but the board lists {len(board)}"
    )


def test_status_board_agrees_with_each_document() -> None:
    board = list(BOARD_ROW.finditer(INDEX.read_text(encoding="utf-8")))
    assert board, "no status-board rows parsed; the table format changed"

    checked = 0
    problems: list[str] = []
    for match in board:
        row = match.groupdict()
        target = (DOCS / row["path"]).resolve()
        if not target.exists():
            problems.append(f"{row['name']}: link target does not exist ({row['path']})")
            continue
        if target.suffix != ".md":
            continue

        text = target.read_text(encoding="utf-8")
        version = _version(text)
        status_match = STATUS_LINE.search(text)
        status = _normalise(status_match.group(1)) if status_match else None

        if version is None:
            problems.append(f"{row['name']}: no **Version:** header")
            continue

        if version != row["version"].strip():
            problems.append(
                f"{row['name']}: board says {row['version'].strip()}, document says {version}"
            )
        # Status is compared case-insensitively and only on the frozen/active/draft
        # vocabulary; a footnote marker would otherwise pass a *Frozen* claim.
        if status is not None and _status_token(row["status"]) != _status_token(status):
            problems.append(
                f"{row['name']}: board says {_normalise(row['status'])}, document says {status}"
            )
        checked += 1

    assert not problems, "documentation index disagrees with its documents:\n  " + "\n  ".join(problems)
    assert checked >= 5, f"only {checked} documents cross-checked; the board should list the set"


@pytest.mark.parametrize("name", ["evaluation_protocol.md", "model_and_method_spec.md"])
def test_frozen_contracts_say_frozen(name: str) -> None:
    """A frozen contract is the premise of every claim in the repository."""
    text = (DOCS / name).read_text(encoding="utf-8")
    match = STATUS_LINE.search(text)
    assert match is not None, f"{name} has no status header"
    assert "frozen" in match.group(1).lower(), (
        f"{name} is not marked Frozen but the project treats it as such"
    )
