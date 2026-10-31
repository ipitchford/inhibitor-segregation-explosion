# Replay receipt

**Date:** 31 October 2026. **Runner:** the shared local research queue, macOS arm64; CPython 3.11 via uv; NumPy 2.3.5 pinned in `uv.lock`.

| Run | Mode | Result |
|---|---|---|
| `run_checks.py` (exact checks, standard library) | normal, `-B` | PASS, exact match with `verification/results.json` |
| same | `-O -B` | PASS, identical (no `assert` statements) |
| `run_checks.py --full` (estimator, quick and full enclosure) | `uv run --frozen` | PASS within tolerance; full enclosure inside the published intervals for s0 = 2, 3, 4 |
| `negative_controls.py` | normal and `-O` | 4 of 4 corruptions rejected in both modes |

Each run used a temporary copy of the package; retained outputs and the package tree were unchanged. The publication gate repeats this replay from a fresh extraction of the frozen archive; its log is retained privately with the publication receipts. During review (31 October 2026) every script of the original research bundle was also replayed from a fresh extraction and reproduced its recorded outputs bit for bit.
