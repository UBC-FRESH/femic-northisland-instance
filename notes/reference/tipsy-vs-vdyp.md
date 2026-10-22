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
3. The unpublished `tsa48_tipsy_input` workbook, if it can be supplied.

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
