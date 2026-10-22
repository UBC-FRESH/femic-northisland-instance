# RESULTS-derived TIPSY candidates

This runbook rebuilds the public RESULTS candidate table used to replace the
unpublished TSA 48 `tsa48_tipsy_input` workbook. The lane is a diagnostic
candidate, not an accepted managed-yield input, until BatchTIPSY completes and
the managed/VDYP comparison is reviewed.

## 1. Fetch the public layers

Run from the instance root. The bbox is the EPSG:3005 envelope of the tracked
North Island AOI.

```bash
BBOX=$(python -c "import geopandas as gpd; g=gpd.read_file('data/source/aoi/northisland_aoi.gpkg'); print(','.join(str(v) for v in g.total_bounds))")
python -m femic data bcdc-fetch \
  --instance-root . \
  --bbox "$BBOX" \
  --output-format gpkg \
  --download-root data/downloads/bcdc \
  WHSE_FOREST_VEGETATION.RSLT_OPENING_SVW \
  WHSE_FOREST_VEGETATION.RSLT_PLANTING_SVW \
  WHSE_FOREST_VEGETATION.RSLT_FOREST_COVER_INV_SVW
```

`WHSE_FOREST_VEGETATION.RSLT_FOREST_COVER_SPECIES_SVW` is an attribute-only
catalogue package with no WFS resource. The aggregation therefore reads the
`I_SPECIES_CODE_1..5` and `I_SPECIES_PERCENT_1..5` fields in
`RSLT_FOREST_COVER_INV_SVW`.

## 2. Aggregate to model AUs

```bash
python scripts/build_results_tipsy_inputs.py
```

This writes `config/tsr/tipsy_au_results_candidates.csv`. Each row is keyed by
`stratum_code` and `si_level` and carries the opening count, median site index,
median total stems per hectare, opening-weighted species mix, genetic worth, and
the TSA 48 OAF 1/OAF 2 values.

To create a candidate TIPSY input without overwriting the accepted input:

```bash
python scripts/build_results_tipsy_inputs.py \
  --tipsy-input /tmp/03_input-northisland-results.csv
```

## 3. What the first run found

- 4,198 openings were assigned across all 12 model AUs.
- Three AUs are thin: `CWH_CW` L has 4 openings, `CWH_YC` L has 21, and
  `CWH_YC` M has 11. Their `median_density` comes from a single planting record
  and is labelled `planting_single`.
- `median_density` uses the planting-derived density where RESULTS has a planting
  record. It does not use `I_TOTAL_STEMS_PER_HA`, which includes natural ingress
  and is retained only as `median_total_stems` for comparison.
- BatchTIPSY now runs through the documented Linux and Wine lane in
  `runbooks/tipsy-btc-linux-wine.md`: scratch Wine prefix with Wine Mono 9.0.0,
  userspace patched Xvfb, and a direct `wine TIPSYbtc.exe /TSR` call. The
  earlier hangs were the system `xvfb-run`/legacy prefix and decimal density
  values that BatchTIPSY parses as `Integer`.
- The 12-AU RESULTS input completes with `exit_code=0`, 12 output rows, and zero
  error rows. The accepted candidate uses the RESULTS species and density with
  the model PSPL/VDYP site-index mapping.
- Nine of twelve AUs meet or beat VDYP on gross volume. CWH_CW L and M and
  CWH_YC L remain below; that is a site-index/curve interpretation gap, not a
  runtime failure.

## 4. Promotion gate

Before this lane replaces the accepted input:

1. Review the low CWH_CW L and M and CWH_YC L gross-volume ratios against the
   VDYP curves and decide whether the site-index transfer or the VDYP curve is
   the weak link.
2. Review the thin AUs and decide whether to borrow a neighbouring AU or widen
   the SI class.
3. Update `config/tsr/tipsy_au_mapping.csv` and the FreshForge workflow when the
   comparison is accepted.
