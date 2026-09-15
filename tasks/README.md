# DCSE Task Queue & Delegation Layer

The canonical delegation package and task packets reside in `dcse/tasks/`.

## Quick Commands
- **View Task Queue:** `python -m dcse tasks`
- **Inspect Specific Task:** `python -m dcse tasks --id <ID>` (e.g. `python -m dcse tasks --id T-002`)
- **Run Regression Suite:** `python -m dcse test`
- **Run Benchmark Against Baseline:** `python -m dcse bench --against dcse/baseline.json`
- **View Rule Inventory:** `python -m dcse inventory`

For detailed executor instructions, rule lifecycle staging, and report formatting, refer directly to `dcse/tasks/README.md`.
