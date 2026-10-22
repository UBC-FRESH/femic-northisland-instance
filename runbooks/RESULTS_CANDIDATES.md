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
- The BatchTIPSY run on the RESULTS input did not produce
  `04_output-northisland.csv` within five minutes under Wine. The completed
  managed/VDYP comparison remains the median-VDYP-SI variant.

## 4. Promotion gate

Before this lane replaces the accepted input:

1. Resolve the free-growing density and species mix, rather than using total
   stems per hectare.
2. Run BatchTIPSY to completion and show that the managed curve meets or beats
   VDYP at the same site index, or record the gap as a known limitation.
3. Review the thin AUs and decide whether to borrow a neighbouring AU, widen the
   SI class, or keep the median-VDYP-SI curve.
4. Update `config/tsr/tipsy_au_mapping.csv` and the FreshForge workflow only
   after the comparison is accepted.
