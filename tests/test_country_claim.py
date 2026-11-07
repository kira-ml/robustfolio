"""The country sample's corrected claim must not silently revert.

The v1.1 label was "confirmatory". The audit found that the country results were
written at 19:51:35, the protocol file was last written at 20:08:45, and both were
committed together. The repository cannot establish that the protocol was frozen
before execution, so the sample is a pre-specified external replication.

These are source-level assertions on purpose: the PDFs are rebuilt from these files
by the paper/brief/carousel tests, and a claim that only exists in a generated PDF
would be harder to correct.
"""

from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def _read(relative: str) -> str:
    return (ROOT / relative).read_text(encoding="utf-8")


def test_protocol_note_is_not_labeled_confirmatory() -> None:
    text = _read("notes/confirmatory_country_etfs_2026-11-05.md")
    assert "freeze not independently verified" in text
    assert "Pre-registered and frozen before execution" not in text
    assert "Confirmatory sample 2" not in text


def test_result_note_is_an_external_replication() -> None:
    text = _read("notes/country_sample_result_2026-11-05.md")
    assert "not labeled confirmatory" in text
    assert "Confirmatory for this sample" not in text


def test_country_readme_is_not_labeled_confirmatory() -> None:
    text = _read("docs/published-run/country-sample/README.md")
    assert "not labeled confirmatory" in text
    assert "Confirmatory for this sample" not in text
    assert "Claim-status note (2026-11-08)" in text


def test_public_readme_states_the_correction() -> None:
    text = _read("README.md")
    assert "not labeled confirmatory" in text
    assert "confirmatory for that sample" not in text.lower()
    assert "notes/audit_2026-11-08.md" in text


def test_positioning_uses_the_external_label() -> None:
    text = _read("docs/positioning.md")
    assert "External replication; protocol dated 2026-11-05" in text
    assert "Confirmatory for that sample" not in text


def test_paper_does_not_claim_a_confirmatory_country_sample() -> None:
    text = _read("paper/paper.typ")
    assert "pre-specified external replication" in text
    assert "confirmatory for that sample" not in text.lower()


def test_brief_does_not_claim_a_confirmatory_country_sample() -> None:
    text = _read("essays/brief.typ")
    assert "freeze not independently verified" in text
    assert "[Replication], [Confirmatory]" not in text


def test_carousel_footer_does_not_claim_confirmatory() -> None:
    text = _read("paper/carousel.typ")
    assert "external replication" in text
    assert "not confirmatory" in text
    assert "confirmatory for that sample" not in text.lower()


def test_synthesis_uses_the_corrected_label() -> None:
    text = _read("essays/two-nulls-one-evaluation-problem.md")
    assert "not labeled confirmatory" in text
    assert "confirmatory country replication" not in text


def test_v1_1_1_release_notes_record_the_correction() -> None:
    text = _read("docs/release-notes-v1.1.1.md")
    assert "not a confirmatory test" in text
    assert "No research result changed" in text
