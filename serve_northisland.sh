#!/usr/bin/env bash
# Serve the North Island ws4 model on loopback.
set -euo pipefail

INSTANCE_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PORT="${PORT:-8014}"
DATASET="${DATASET:-$INSTANCE_ROOT/runtime/matrix}"
RUNS="${RUNS:-$INSTANCE_ROOT/runtime}"
GEOMETRY="${GEOMETRY:-$INSTANCE_ROOT/runtime/fragments.geojson}"
TARGETS="${TARGETS:-$INSTANCE_ROOT/config/targets.yaml}"

cd "$INSTANCE_ROOT"
exec python -m ws4.cli serve \
  --dataset "$DATASET" \
  --runs "$RUNS" \
  --geometry "$GEOMETRY" \
  --targets "$TARGETS" \
  --crs EPSG:3005 \
  --allow-runs \
  --allow-agent \
  --agent-cwd "$INSTANCE_ROOT" \
  --host 127.0.0.1 \
  --port "$PORT"
