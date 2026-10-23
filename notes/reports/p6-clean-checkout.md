# P6.1 clean-checkout downstream verification

Phase: P6 verify and release
Task: P6.1 verify the clean-checkout downstream build (#38)
Parent issue: #37
Date: 2026-10-23
Status: downstream lane verified; full public-data upstream lane remains a recorded gap.

## What was verified

A fresh clone of `UBC-FRESH/femic-northisland-instance` at `8156773` was built
with the recorded FEMIC model-input bundle and the recorded checkpoint. The
clean checkout contained no compiled matrix, baseline run, or UI geometry before
the run.

This verifies the downstream FEMIC-to-ws4 lane. It does **not** re-run the
public-data VDYP/TIPSY compilation; that lane needs a materialized
`FEMIC_EXTERNAL_DATA_ROOT` and remains P6.2.

## Inputs

The clean clone used the recorded bundle and checkpoint from the release
checkout:

| Input | SHA-256 |
| --- | --- |
| `data/model_input_bundle/au_table.csv` | `41856e2e85433fd239f1442a0cf8ff8c573bfaff166507d69a5bb497931673a2` |
| `data/model_input_bundle/curve_table.csv` | `852b7d385a1bf7a2585d410f8f8ead0c5cd53661fffa77a8ec73b7ec6ff45f54` |
| `data/model_input_bundle/curve_points_table.csv` | `16ecc29112b1ccae7e02c01cac185ec4b9ebf0c9fae809e5d20c163f3ace4c7f` |
| `data/ria_vri_vclr1p_checkpoint8.feather` | `eef4dd8ed1c4ed408c6163ecc7240633f58435e53fd6c10d53ef914afb88b3ef` |

## Commands

```bash
git clone https://github.com/UBC-FRESH/femic-northisland-instance.git
cd femic-northisland-instance
# copy the recorded bundle and checkpoint into data/
export PYTHONPATH="$PWD/src:$PWD/scripts"
python -m freshforge validate workflows/freshforge/northisland_ws4_from_bundle.yaml
python -m freshforge run workflows/freshforge/northisland_ws4_from_bundle.yaml \
  --workdir . --namespace p6/nicc --json
python scripts/dashboard.py
```

## Result

- Workflow: **7/7 nodes success**, 0 warnings, 0 errors.
- Matrix: 56,187 blocks / 442,451.9975 ha.
- Baseline schedule: 46,321 blocks, target age 60, offsets 0-30.
- Retained AUs: `CWH_CW_L`, `CWH_YC_L`.
- Retained blocks: 4,968; retained stand area: 52,013.5878 ha.
- Retained THLB: 1,717.5959 ha; remaining model THLB: 26,840.3499 ha.
- 100-year managed volume: 17,355,254.55 m3.
- 100-year average: 173,552.55 m3/yr.
- Pro-rated AAC: 176,330.29 m3/yr; realized share: 98.4247%.
- Targets: both provisional targets **met**.
- Dashboard: **GREEN**.
- Both FreshForge workflows validate.

These values match the v0.2.0 release evidence within rounding.

## Remaining gap

The full public-data upstream lane (VDYP/BatchTIPSY -> model-input bundle) was
not re-run because `FEMIC_EXTERNAL_DATA_ROOT` is not materialized in this
checkout. P6.2 must either materialize the public data and run
`northisland_model_build` from a clean clone, or record that lane as deferred.
