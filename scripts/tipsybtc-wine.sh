#!/usr/bin/env bash
# Run TIPSYbtc.exe under Wine on Linux.
#
# Copy this file into the BTC install directory before calling
# `femic tipsy run-btc --btc-exe <install>/tipsybtc-wine.sh`.
# FEMIC copies the install directory, so the wrapper and TIPSYbtc.exe stay
# together in the staged copy.
set -euo pipefail

if [[ -z "${FEMIC_BTC_WINEPREFIX:-}" ]]; then
  echo "FEMIC_BTC_WINEPREFIX must point at the scratch Wine prefix." >&2
  exit 2
fi

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
export WINEPREFIX="${FEMIC_BTC_WINEPREFIX}"
export DISPLAY="${FEMIC_BTC_DISPLAY:-:99}"
export WINEDEBUG="${WINEDEBUG:--all}"

exec wine "${SCRIPT_DIR}/TIPSYbtc.exe" "$@"
