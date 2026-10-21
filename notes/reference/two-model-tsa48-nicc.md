# Full TSA 48 and NICC-overlap models

Status: build in progress on `feature/full-tsa48`.

## The two models

1. **Full TSA 48 benchmark model** (`runtime/tsa48_full/matrix`)
   - Boundary: full North Island TSA 48 (`data/source/aoi/tsa48_full.gpkg`).
   - Every block carries a `part` flag (`nicc` or `outside`) and a `k3z` flag.
   - Purpose: benchmark the ws4 wood supply against the published TSA 48 AAC and
     THLB, then split the AAC between the NICC overlap and the rest of the TSA.

2. **NICC-overlap + K3Z model** (`runtime/matrix`, served on port 8014)
   - Boundary: TSA 48 intersected with the North Island - Central Coast
     Natural Resource District, plus the K3Z community forest.
   - Purpose: the student/MSFM model for NICF planning, including the proposed
     8,000 ha NICF expansion.

## Reference numbers

From the North Island TSA Timber Supply Review Data Package, July 2020,
Table 4 and section 7.1.1:

| Quantity | Value |
| --- | ---: |
| TSA boundary area | 2,426,749 ha |
| Ocean removed | 677,289 ha |
| Gross land area | 1,749,460 ha |
| Section 8 decision area | 714,726 ha |
| Current THLB | 177,505 ha |
| Current AAC | 1,248,100 m³/yr |

The NICC intersection is 1,083,003.66 ha gross. The published AAC and THLB are
for the whole TSA, which is why the full-TSA model is the benchmark and the
NICC-only model cannot use those numbers directly.

## Part accounting

The full model's `part` flag is in `blocks.parquet` and `fragments.parquet`, and
in the UI GeoJSON properties. Because ws4 reports state/area accounts over the
dataset fragments rather than the scheduled blocks, the accounting views are
separate filtered datasets:

- `runtime/tsa48_full/matrix_nicc`
- `runtime/tsa48_full/matrix_outside`

Each is a valid ws4 matrix with the same tracks, curves, treatments, and
products; only the fragment/block tables are filtered. Simulating the full,
NICC, and outside schedules against the matching dataset makes every account
reconcile exactly (`full = nicc + outside`).

Evidence files:

- `runtime/tsa48_full/evidence/account_values_by_part.csv`
- `runtime/tsa48_full/evidence/account_values_by_part_reconciliation.csv`
- `runtime/tsa48_full/evidence/tsr_benchmark.csv`

## Reproduction

```bash
export FEMIC_EXTERNAL_DATA_ROOT=/path/to/femic-public-data/data
python -m femic run --run-config config/run_profile.tsa48_full.yaml
scripts/build_full_tsa48_model.sh
./serve_tsa48_full.sh   # port 8015
```
