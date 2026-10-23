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

## Working Linux and Wine lane

The earlier SIBEC and RESULTS attempts did not fail because TIPSY cannot run
here. They used a system `xvfb-run` and a legacy Wine prefix, and the RESULTS
input wrote planted densities as decimals such as `416.7`. BatchTIPSY parses
those columns as `Integer`, so it opened a hidden .NET dialog and waited.

The documented `tsa29mini` lane works on this host:

- scratch Wine prefix with Wine Mono 9.0.0;
- userspace Xvfb built from extracted Ubuntu packages and string-patched to
  `/tmp/xkb`;
- direct `wine TIPSYbtc.exe /TSR <input> <output> <error>`.

After rounding planted densities to integers, the 12-AU North Island input ran
in about ten seconds with `exit_code=0`, 12 output rows, and zero error rows.
The exact recipe is in `runbooks/tipsy-btc-linux-wine.md`.

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

The accepted candidate uses the RESULTS species and density with the model
PSPL/VDYP site-index mapping, the TSA 48 15% OAF 1, and OAF 2 of 5% (12.5% for
CWH_FD). Gross TIPSY volume divided by VDYP volume, mean over ages 60, 80, 100,
and 120:

| Model AU | Stratum | SI | TIPSY / VDYP gross | TIPSY / VDYP merchantable |
| --- | --- | ---: | ---: | ---: |
| 21000 | CWH_HW L | 11.6 | 0.89 | 0.70 |
| 22000 | CWH_HW M | 18.4 | 1.13 | 1.00 |
| 23000 | CWH_HW H | 27.6 | 1.38 | 1.23 |
| 21001 | CWH_CW L | 7.9 | 0.46 | 0.23 |
| 22001 | CWH_CW M | 12.0 | 0.80 | 0.65 |
| 23001 | CWH_CW H | 18.3 | 1.15 | 1.01 |
| 21002 | CWH_YC L | 7.0 | 0.71 | 0.27 |
| 22002 | CWH_YC M | 9.7 | 1.18 | 0.82 |
| 23002 | CWH_YC H | 13.0 | 1.30 | 1.09 |
| 21003 | CWH_FD L | 23.0 | 2.12 | 1.72 |
| 22003 | CWH_FD M | 28.4 | 1.56 | 1.26 |
| 23003 | CWH_FD H | 33.6 | 1.47 | 1.17 |

Eight of twelve AUs meet or beat VDYP on gross volume. CWH_HW L (0.89),
CWH_CW L (0.46) and M (0.80), and CWH_YC L (0.71) remain below. A leading-species-only variant raises CWH_YC L from
0.71 to 0.92 and CWH_CW M from 0.80 to 0.87, but CWH_CW L stays near 0.53. That
points to the low CWH_CW L site index or the VDYP curve in that AU, not to the
BatchTIPSY runtime.

The AU-wise comparison is in
`config/tsr/tipsy_au_results_vdyp_comparison.csv`. The ws4 bundle, matrix,
baseline run, targets, and UI geometry were rebuilt from this lane. Both
provisional targets are met.

## Visual inspection

The 12-AU contact sheet is `plots/tipsy_vdyp_northisland_12au.png`; individual
panels are `plots/tipsy_vdyp_northisland-<AU>.png`. These are generated build
artifacts and are not tracked. Red panels mark the four AUs that remain below
VDYP on mean gross volume over ages 60-120.

The model THLB area by AU is in `config/tsr/thlb_area_by_au.csv`. The four
problem AUs cover 9,142 ha of the 28,558 ha model-flagged THLB (32.0%). For
context, they cover 165,368 ha of the 442,452 ha compiled model stand area
(37.4%). The model THLB flag is narrower than the TSR Table 4 current THLB
benchmark; the two denominators should not be mixed.

## Base-model retention decision

The v0.2.0 base model retains `CWH_CW_L` and `CWH_YC_L` and keeps harvesting
`CWH_HW_L` and `CWH_CW_M`. The two retained AUs are the weakest managed curves
and contribute negligible long-run volume; retaining all four would remove
32.0% of model THLB and reduce the 100-year average to 79.3% of the pro-rated
AAC. The accepted policy and scenario evidence are in
`notes/reference/retention-decision.md` and `notes/adr/0001-retain-low-yield-aus.md`.
