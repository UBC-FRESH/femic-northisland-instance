# TIPSY vs VDYP after the TFL 6 adaptation

## Setup

- TIPSY input species and density: nearest TFL 6 MP10 Table 29 future-managed
  candidate rows.
- OAF 1: **0.85** (the TSA 48 data package documents a 15% OAF 1).
- OAF 2: 0.95, or 0.875 for the CWH_FD AUs.
- Site index: **median VDYP output SI** for each TSA 48 AU.
- Genetic worth: TSA 48 data package Table 45 (Cw 4.33, Fd 7.63, Hw 5.20,
  Ss 2.00).
- TIPSY runtime: BatchTIPSY Composer under Wine, with Wine Mono installed.

The adapted parameters are in
`config/tsr/tipsy_au_tfl6_tsa48_adapted.csv`.

## Result

Gross TIPSY volume divided by VDYP volume, mean over ages 60, 80, 100, and 120:

| Model AU | Stratum | SI | TIPSY / VDYP (gross) |
| --- | --- | ---: | ---: |
| 21000 | CWH_HW L | 12.0 | 0.52 |
| 22000 | CWH_HW M | 18.3 | 0.71 |
| 23000 | CWH_HW H | 27.9 | 1.04 |
| 21001 | CWH_CW L | 8.0 | 0.27 |
| 22001 | CWH_CW M | 11.9 | 0.45 |
| 23001 | CWH_CW H | 17.7 | 0.68 |
| 21002 | CWH_YC L | 7.1 | 0.40 |
| 22002 | CWH_YC M | 9.6 | 0.57 |
| 23002 | CWH_YC H | 12.6 | 0.72 |
| 21003 | CWH_FD L | 23.4 | 1.75 |
| 22003 | CWH_FD M | 28.4 | 1.43 |
| 23003 | CWH_FD H | 33.4 | 1.38 |

Using merchantable TIPSY volume instead of gross volume makes the Hw/Cw/Yc
ratios lower, not higher.

## Interpretation

The prediction holds: after the TFL 6 adaptation and the TSA 48 15% OAF 1, the
managed TIPSY curves for western hemlock, western redcedar, and yellow-cedar are
**below** the unmanaged VDYP curves at the same age. Only coastal Douglas-fir and
high-site western hemlock meet or beat VDYP.

Likely causes:

- the TFL 6 species mixes are RESULTS-derived for TFL 6, not TSA 48;
- the mixed-species TIPSY average includes slow secondary species (Ba, Cy);
- the median VDYP SI is a back-calculated inventory SI, not necessarily the
  potential site index the TSA 48 managed-stand method used;
- TIPSY merchantable and gross outputs use a different utilization and
  decay/waste/breakage basis than the VDYP smooth curves.

## Next candidates to test

1. Leading-species-only mixes (Hw 100, Cw 100, Yc 100, Fd 100) with the same
   median VDYP SI.
2. The TSA 48 SIBEC/PSPL SI by species instead of the AU median.
3. The RESULTS-derived species and density lane described below.

Until one of those closes the gap, the TFL 6 adaptation should be treated as a
diagnostic, not as the accepted managed-curve lane.

## SIBEC SI attempt

A second variant used the TFL 6 species and density, the TSA 48 15% OAF 1, and
the SIBEC/PSPL site index per species from the FEMIC run. BatchTIPSY under Wine
started but did not produce `04_output-northisland.csv` within ten minutes; the
run was stopped. The SIBEC SI route is therefore not yet a working lane in this
runtime. The median-VDYP-SI variant remains the only completed managed/VDYP
comparison.

## RESULTS reverse-engineering workflow

The public RESULTS layers can supply the missing AU-wise TIPSY inputs without the
unpublished `tsa48_tipsy_input` workbook. Candidate layers:

| Layer | Use |
| --- | --- |
| `WHSE_FOREST_VEGETATION.RSLT_OPENING_SVW` | opening identity, harvest date, area, BEC |
| `WHSE_FOREST_VEGETATION.RSLT_PLANTING_SVW` | planted species, density, seedlot, genetic worth, planting date |
| `WHSE_FOREST_VEGETATION.RSLT_FOREST_COVER_INV_SVW` | free-growing inventory attributes |
| `WHSE_FOREST_VEGETATION.RSLT_FOREST_COVER_SILV_SVW` | silviculture status and stocking |
| `WHSE_FOREST_VEGETATION.RSLT_FOREST_COVER_SPECIES_SVW` | free-growing species composition and density |
| `WHSE_FOREST_VEGETATION.RSLT_STANDARDS_UNITS_SVW` | standards-unit context |
| `WHSE_FOREST_VEGETATION.RSLT_ACTIVITY_TREATMENT_SVW` | treatment history and timing |

Workflow:

1. Fetch TSA 48-scoped subsets with WFS/OpenMaps or the BCGW custom download.
2. Join each opening to planting, free-growing species, and activity records.
3. Derive planted and natural species composition, density, regeneration delay,
   genetic worth, and free-growing species mix.
4. Aggregate to the model AU keys (BEC zone/subzone + leading species + SI class).
5. Replace the TFL 6 candidate species and density in `03_input` with the
   RESULTS-derived values.
6. Run BatchTIPSY and compare managed versus VDYP again.

This path is fully public and reproducible, and it matches the TSA 48 data
package method, which states that managed-stand inputs come from RESULTS.

## RESULTS candidate run

The candidate workflow is implemented in
`scripts/build_results_tipsy_inputs.py`, with the exact fetch and aggregation
commands in `runbooks/RESULTS_CANDIDATES.md`. The first run used
`RSLT_OPENING_SVW`, `RSLT_PLANTING_SVW`, and `RSLT_FOREST_COVER_INV_SVW`,
fetched by `femic data bcdc-fetch` for the AOI envelope. The separate
`RSLT_FOREST_COVER_SPECIES_SVW` package is attribute-only and exposes no WFS
resource, so the inventory layer's `I_SPECIES_CODE_*` and
`I_SPECIES_PERCENT_*` fields supply the free-growing species mix.

The aggregate assigns an opening by leading species and by the nearest model AU
median site index. It wrote `config/tsr/tipsy_au_results_candidates.csv` for all
12 AUs from 4,198 openings. Three AUs are thin: CWH_CW L has 4 openings, CWH_YC
L has 21, and CWH_YC M has 11; their density comes from a single planting record
and is labelled `planting_single`. For the other AUs, `median_density` is the
median planting-derived density from RESULTS. `median_total_stems` is retained
separately because `I_TOTAL_STEMS_PER_HA` includes natural ingress and is not a
planted density.

The BatchTIPSY run with the RESULTS input did not produce
`04_output-northisland.csv` within five minutes under Wine. A second run with a
leading-species-only input (Hw, Cw, Yc, or Fd at 1,200 stems per hectare with the
RESULTS site index) also did not complete. The failure is therefore at the
TIPSY runtime boundary, not only in the species mix. The completed managed/VDYP
comparison remains the median-VDYP-SI variant, and the RESULTS table is a
candidate diagnostic rather than the accepted lane.
