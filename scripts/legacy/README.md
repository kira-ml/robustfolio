# Legacy scripts

These scripts are preserved for provenance, not maintenance.

They were written for Phase 1, before the current `Snapshot` API replaced the
old `load_monthly_returns` loader and before `backtest.run_method` replaced the
old `walk_forward` entry point. They do **not** run against the current package;
`diagnose_slsqp.py`, `phase1_experiment.py`, and `dsr_inputs_phase1.py` all call
`backtest.walk_forward`, which no longer exists.

They are kept because the historical decision log and the Phase 1 result refer to
them. Do not use them for new runs, and do not cite them as a current reproduction
path. The current entry points are:

- `scripts/build_snapshot.py`
- `scripts/run_experiment.py`
- `scripts/run_country_sample.py`
- `scripts/verify_release.py`

`results/phase1_results.csv` is a historical Phase 1 record; it is not regenerated
by the current code.
