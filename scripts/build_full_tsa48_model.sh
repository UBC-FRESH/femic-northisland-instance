#!/usr/bin/env bash
# Build the full TSA 48 ws4 model after `femic run` has produced the upstream
# bundle and checkpoint. The NICC intersection and K3Z are flags on the full
# model, and the full/NICC/outside runs are simulated separately so the parts
# reconcile exactly.
set -euo pipefail

INSTANCE_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$INSTANCE_ROOT"

RUN_ID="${RUN_ID:-tsa48_full_20261021}"
CHECKPOINT="${CHECKPOINT:-data/ria_vri_vclr1p_checkpoint8.feather}"
PATCHWORKS_OUT="${PATCHWORKS_OUT:-output/patchworks_tsa48_full}"
MODEL_DIR="${MODEL_DIR:-runtime/tsa48_full}"
TARGET_AGE="${TARGET_AGE:-60}"
YEARS="${YEARS:-100}"

mkdir -p "$MODEL_DIR" "$MODEL_DIR/parts" "$MODEL_DIR/schedules" "$MODEL_DIR/runs" "$MODEL_DIR/evidence"

python -m femic export patchworks \
  --tsa 48 \
  --bundle-dir data/model_input_bundle \
  --checkpoint "$CHECKPOINT" \
  --output-dir "$PATCHWORKS_OUT"

python -m ws4.cli build \
  --xml "$PATCHWORKS_OUT/forestmodel.xml" \
  --fragments "$PATCHWORKS_OUT/fragments/fragments.shp" \
  --out "$MODEL_DIR/matrix"

python scripts/flag_parts.py \
  --fragments "$PATCHWORKS_OUT/fragments/fragments.shp" \
  --nicc data/source/aoi/nicc_district.gpkg \
  --k3z data/source/aoi/k3z_tenure.gpkg \
  --out-dir "$MODEL_DIR/parts" \
  --dataset "$MODEL_DIR/matrix"

python -m ws4.cli validate --dataset "$MODEL_DIR/matrix"

python scripts/build_part_schedules.py \
  --dataset "$MODEL_DIR/matrix" \
  --out-dir "$MODEL_DIR/schedules" \
  --target-age "$TARGET_AGE"

python scripts/build_part_datasets.py \
  --dataset "$MODEL_DIR/matrix" \
  --parts "$MODEL_DIR/parts/block_parts.csv" \
  --out-dir "$MODEL_DIR"

for part in full nicc outside; do
  dataset="$MODEL_DIR/matrix"
  if [ "$part" != "full" ]; then
    dataset="$MODEL_DIR/matrix_$part"
  fi
  python -m ws4.cli validate --dataset "$dataset"
  python -m ws4.cli simulate \
    --dataset "$dataset" \
    --schedule "$MODEL_DIR/schedules/$part.csv" \
    --out "$MODEL_DIR/runs/$part" \
    --years "$YEARS"
  python -m ws4.cli report \
    --run "$MODEL_DIR/runs/$part" \
    --targets config/targets.tsa48_full.yaml
done

python scripts/report_part_accounting.py \
  --runs "$MODEL_DIR/runs" \
  --out "$MODEL_DIR/evidence/account_values_by_part.csv"

python scripts/report_tsr_benchmark.py \
  --dataset "$MODEL_DIR/matrix" \
  --part-datasets "$MODEL_DIR" \
  --runs "$MODEL_DIR/runs" \
  --schedules "$MODEL_DIR/schedules" \
  --out "$MODEL_DIR/evidence/tsr_benchmark.csv"

python scripts/prepare_ws4_ui.py \
  --fragments "$PATCHWORKS_OUT/fragments/fragments.shp" \
  --out "$MODEL_DIR/fragments.geojson" \
  --parts "$MODEL_DIR/parts/block_parts.csv"

echo "full TSA 48 model built under $MODEL_DIR"
