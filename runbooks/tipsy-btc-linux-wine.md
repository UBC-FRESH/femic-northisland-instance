# Runbook: BatchTIPSY under Wine on Linux

This is the working Linux lane for `TIPSYbtc.exe /TSR`. It is the same recipe
used by the UBC-FRESH `tsa29mini` replant run: a scratch Wine prefix with
Wine Mono 9.0.0, a userspace Xvfb with patched xkb paths, and a direct
`wine TIPSYbtc.exe /TSR <input> <output> <error>` call.

Do not use the system `xvfb-run` or a copied legacy Wine prefix as the
decision-making lane. Those paths can start BatchTIPSY and then leave it
waiting on a hidden .NET dialog. The symptom is a `Microsoft .NET Framework`
window, or a process that sits after the `Database:` line in `Log*.txt`.

## One-time setup

```bash
I=<instance-root>
BTC=<known-good-tipsy-4.7-btc-install>
SCRATCH=$I/tipsy_io/scratch
mkdir -p "$SCRATCH"/{work,btc_install}
cp -a "$BTC"/* "$SCRATCH/btc_install/"
cp "$I/scripts/tipsybtc-wine.sh" "$SCRATCH/btc_install/"
chmod +x "$SCRATCH/btc_install/tipsybtc-wine.sh"
```

Create the Wine prefix and install Wine Mono. `TIPSYbtc.exe` is a 64-bit .NET
assembly.

```bash
export WINEPREFIX=$SCRATCH/wineprefix-mono
export WINEARCH=win64
export WINEDEBUG=-all
wineboot -u
curl -sL -o "$SCRATCH/wine-mono-9.0.0-x86.msi" \
  https://dl.winehq.org/wine/wine-mono/9.0.0/wine-mono-9.0.0-x86.msi
WINMSI="Z:$(echo "$SCRATCH/wine-mono-9.0.0-x86.msi" | sed 's|/|\\|g')"
wine msiexec /i "$WINMSI" /qn
```

Stage a userspace Xvfb. BatchTIPSY creates windows even in `/TSR` mode, and the
packaged Xvfb resolves xkb data through compiled-in paths.

```bash
mkdir -p "$SCRATCH/xvfb/debs" "$SCRATCH/xvfb/rootfs"
cd "$SCRATCH/xvfb/debs"
apt-get download xvfb libxfont2 xserver-common x11-xkb-utils xkb-data
cd ..
for deb in debs/*.deb; do dpkg -x "$deb" rootfs; done

rm -rf /tmp/xkb
mkdir -p /tmp/xkb/out /tmp/xkb/share
cp rootfs/usr/bin/Xvfb /tmp/xkb/Xvfb-patched
cp rootfs/usr/bin/xkbcomp /tmp/xkb/xkbcomp
chmod +x /tmp/xkb/Xvfb-patched /tmp/xkb/xkbcomp
ln -sfn "$SCRATCH/xvfb/rootfs/usr/share/X11/xkb" /tmp/xkb/share/xkb
python - <<'PY'
from pathlib import Path
path = Path("/tmp/xkb/Xvfb-patched")
data = path.read_bytes()
for old, new in (
    (b"/usr/bin\x00", b"/tmp/xkb\x00"),
    (b"/usr/share/X11/xkb", b"/tmp/xkb/share/xkb"),
    (b"/var/lib/xkb/", b"/tmp/xkb/out/"),
):
    if len(old) != len(new) or old not in data:
        raise SystemExit(f"unexpected Xvfb path string: {old!r}")
    data = data.replace(old, new)
path.write_bytes(data)
PY
```

## Run BatchTIPSY

```bash
I=<instance-root>
SCRATCH=$I/tipsy_io/scratch
rm -f /tmp/.X99-lock /tmp/.X11-unix/X99
LD_LIBRARY_PATH=$SCRATCH/xvfb/rootfs/usr/lib/x86_64-linux-gnu \
  /tmp/xkb/Xvfb-patched :99 -screen 0 1024x768x24 -nolisten tcp &
XVFB_PID=$!
sleep 2

cd "$SCRATCH/work"
cp "$I/data/03_input-northisland.csv" .
export DISPLAY=:99
export WINEPREFIX=$SCRATCH/wineprefix-mono
export WINEDEBUG=-all
wine "$SCRATCH/btc_install/TIPSYbtc.exe" /TSR \
  03_input-northisland.csv 04_output-northisland.csv 04_error-northisland.csv

kill "$XVFB_PID"
```

A successful run exits `0`, writes one output row per input feature, and writes
a header-only error file. A 12-row North Island run takes about ten seconds.

## Run through FEMIC

Copy `scripts/tipsybtc-wine.sh` into the BTC install, then:

```bash
export FEMIC_BTC_WINEPREFIX=$SCRATCH/wineprefix-mono
export FEMIC_BTC_DISPLAY=:99
python -m femic tipsy run-btc data/03_input-northisland.csv \
  --btc-exe "$SCRATCH/btc_install/tipsybtc-wine.sh" \
  --scratch-dir "$SCRATCH/femic-run" \
  --output-csv data/04_output-northisland.csv \
  --error-csv data/04_error-northisland.csv \
  --run-id northisland_tipsy_results
```

FEMIC copies the install, patches `TimberSupply.rpt` with the vetted TSR
preset, runs the wrapper, and writes `tipsy_io/logs/btc_manifest-*.json`.

## Input contract

BatchTIPSY parses the density columns as integers. A value such as `416.7`
raises:

```text
Input string '416.7' is not valid.
Couldn't find a valid type from string "416.7" to type "Integer".
```

`scripts/build_results_tipsy_inputs.py` rounds planted densities to integers
and writes the CSV as `int64`. Site-index columns may remain decimal.

## Acceptance checks

- `exit_code=0` and no lingering `TIPSYbtc.exe`.
- `04_error-*.csv` has zero data rows.
- Output has one row per input feature and the expected age columns.
- Managed gross yield is compared with the VDYP curve at the same AU.
