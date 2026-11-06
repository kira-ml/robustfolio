# Contributing

Issues and pull requests are welcome. The project is a research artefact, so a
change is judged by whether it keeps the published result checkable rather than
by whether it adds a feature.

## Before you change anything

```bash
python -m pip install -e ".[dev,paper]"
python -m pytest -q
```

The suite is hermetic: it does not need the frozen snapshot, a network
connection, or the local archive. The snapshot itself is not distributed; see
[`docs/data_licenses.md`](docs/data_licenses.md).

## Rules

1. Keep `pytest -q` green.
2. Do not change a frozen threshold, seed, metric definition, cost model, or
   hypothesis without a `docs/decision_log.md` entry.
3. If a change moves a result, state which result moved and by how much.
4. Do not commit raw market data, credentials, or a snapshot archive.
5. Findings are welcome. A report that a specific finding is wrong is treated
   the same way as a report that a result is wrong.
