"""The synthetic end-to-end path is the reproducible demo for a fresh clone.

It does not reproduce the published sample. It exercises the real snapshot
layout, the walk-forward harness, all seven methods, the report builder, and the
written run directory without the restricted vendor data.
"""

from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

import run_synthetic_demo as demo  # noqa: E402


def test_synthetic_demo_runs_the_whole_pipeline(tmp_path: Path) -> None:
    result = demo.run_demo(tmp_path, bootstrap=False)
    run = result["run"]
    written = result["written"]

    assert len(run.outcomes) == 7
    assert len(run.decisions) == 2
    for name in ("manifest", "outcomes", "decisions", "report"):
        assert name in written, f"{name} was not written"

    assert (tmp_path / "outcomes.csv").exists()
    assert (tmp_path / "decisions.csv").exists()
    assert (tmp_path / "report.md").exists()
    assert (tmp_path / "manifest.json").exists()

    # run_demo() raises if any residual exceeds the frozen acceptance threshold;
    # reaching this point means the synthetic solves also passed the certificate.
