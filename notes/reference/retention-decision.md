# Retention decision for the NICC base model

Status: accepted for the v0.2.0 base model
Date: 2026-10-23
Decision record: `notes/adr/0001-retain-low-yield-aus.md`

## Question

Should the NICC base model keep managing the four AUs whose second-growth TIPSY
curves are below VDYP? If not, which ones should be retained, and what happens
to THLB and the pro-rated AAC?

## Curve evidence

The accepted managed curves use public RESULTS species and density with the
model PSPL/VDYP site index, TSA 48 OAF 1 of 15%, and OAF 2 of 5% or 12.5% for
CWH_FD. The AU-wise comparison is
`config/tsr/tipsy_au_results_vdyp_comparison.csv`.

| AU | Gross TIPSY / VDYP | Merchantable / VDYP | THLB ha | Result |
| --- | ---: | ---: | ---: | --- |
| CWH_HW_L | 0.89 | 0.70 | 4,312.6 | below, but material volume |
| CWH_CW_M | 0.80 | 0.65 | 3,112.0 | below, but material volume |
| CWH_CW_L | 0.46 | 0.23 | 1,497.2 | lowest yield, negligible volume |
| CWH_YC_L | 0.71 | 0.27 | 220.4 | lowest yield, negligible volume |

The ratios are means over ages 60, 80, 100, and 120. CWH_HW_L crosses above
VDYP at later ages on gross volume, but its 60-120 mean remains below 1.0.

## Scenario method

The base dataset was compiled with the accepted managed curves. For each
retention scenario, blocks whose feature labels place them in the selected AU
were removed from the deterministic clearcut-at-age-60 schedule. The retained
stands stay in the dataset with their VDYP curves. The simulation horizon was
100 years.

This is a schedule-level scenario, not a formal sustained-yield optimization.
The pro-rated AAC is the 2024 TSA 48 AAC of 1,096,000 m3/yr scaled by the model
THLB share of the TSR current THLB:

```text
1,096,000 * 28,557.9 / 177,505 = 176,330 m3/yr
```

## Results

| Scenario | THLB remaining | Retained THLB | 100-year managed volume | 100-year average | % of pro-rated AAC |
| --- | ---: | ---: | ---: | ---: | ---: |
| Harvest all AUs | 28,557.9 ha | 0.0 ha | 17,695,542 m3 | 176,955 m3/yr | 100.4% |
| Retain CWH_CW_L + CWH_YC_L | 26,840.3 ha | 1,717.6 ha | 17,355,255 m3 | 173,553 m3/yr | **98.4%** |
| Retain CWH_HW_L + CWH_CW_M | 21,133.3 ha | 7,424.6 ha | 14,322,767 m3 | 143,228 m3/yr | 81.2% |
| Retain all four | 19,415.7 ha | 9,142.2 ha | 13,982,479 m3 | 139,825 m3/yr | 79.3% |

The first 10-year period is dominated by old-growth liquidation. In the
accepted two-AU retention scenario it is 10,384,983 m3, or about 1.038M m3/yr;
that is above the pro-rated AAC and is not the right long-run comparison. The
100-year average is the stable comparison because the baseline schedule harvests
every eligible block once and then stops.

## Decision

Retain **CWH_CW_L** and **CWH_YC_L**, and keep harvesting **CWH_HW_L** and
**CWH_CW_M**.

The two retained AUs are the ones where the managed curve is clearly weak and
the long-run volume contribution is negligible. Retaining them removes only
1,717.6 ha, or 6.0% of model THLB, and keeps the 100-year average at 98.4% of
the pro-rated AAC. Retaining the other two as well would remove 32.0% of THLB
and drop the average to 79.3% of the pro-rated AAC, which is too large a loss
for a base model.

## Implementation

`config/retention.json` records the retained and harvested AUs and the scenario
evidence. The baseline schedule builder reads it with:

```bash
python scripts/build_baseline_schedule.py \
  --dataset runtime/matrix \
  --out runtime/baseline_schedule.csv \
  --target-age 60 \
  --retention-config config/retention.json
```

The FreshForge `build_baseline_schedule` node passes
`retention_config: config/retention.json` in both the full and downstream
workflows. The accepted baseline is written to `runtime/baseline` and served by
the ws4 UI.

## Accepted baseline readout

- Scheduled blocks: 46,321
- Scheduled area: 390,438.4 ha
- Retained blocks: 4,968
- Retained total stand area: 52,013.6 ha
- Retained model THLB: 1,717.6 ha
- Remaining model THLB: 26,840.3 ha
- First decade managed volume: 10,384,983 m3
- 100-year managed volume: 17,355,255 m3
- 100-year average: 173,553 m3/yr
- Pro-rated AAC: 176,330 m3/yr
- Share of pro-rated AAC: 98.4%
- Provisional targets: both met

## Risks and limitations

- The retained AUs still contain old first-growth volume. Retaining them forgoes
  that near-term volume; the base model does not attempt to liquidate it.
- The pro-rated AAC uses the model THLB share of the TSR THLB. The model THLB
  flag is narrower than the TSR benchmark, so the ratio is an approximation.
- The baseline is a one-pass schedule. A sustained-yield optimization is still
  required before the value can be treated as a policy AAC.
- The managed TIPSY curves for the retained AUs remain in the bundle as
  provenance. They are not scheduled and do not contribute to the baseline.
  A later cleanup can remove them from the bundle.
- The four-AU and two-AU results depend on the current RESULTS species/density
  and the PSPL/VDYP site-index mapping. Revisit the decision if either changes.
