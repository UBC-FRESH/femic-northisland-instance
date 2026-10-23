# P5 closeout: TSR metadata, TIPSY curves, and the v0.2.0 base model

Parent issue: #29
Branch: `feature/p5-tsr-metadata`
Status: complete
Date: 2026-10-23

## 1. Scope

P5 moved the North Island instance from a provisional VDYP-transform managed
curve to a public-data BatchTIPSY lane, then locked a base model with an explicit
retention policy. The work covers:

- TSA 48 TSR document extraction and the full THLB net-down ladder;
- AU-wise TIPSY parameter mapping and public RESULTS species/density;
- a working Linux and Wine BatchTIPSY lane;
- managed/VDYP comparison for all 12 AUs;
- the retention decision and rebuilt baseline;
- the v0.2.0 release surface.

## 2. What changed

- Added the public RESULTS candidate workflow in
  `scripts/build_results_tipsy_inputs.py` and documented it in
  `runbooks/RESULTS_CANDIDATES.md`.
- Added the working BatchTIPSY Linux recipe in
  `runbooks/tipsy-btc-linux-wine.md` and the `scripts/tipsybtc-wine.sh`
  wrapper.
- Fixed the RESULTS input density type. BatchTIPSY parses planted density as
  `Integer`; decimal values raised a hidden .NET dialog.
- Rebuilt the managed curves from RESULTS species/density and the model
  PSPL/VDYP site index.
- Compared managed TIPSY with VDYP for all 12 AUs in
  `config/tsr/tipsy_au_results_vdyp_comparison.csv`.
- Added `config/retention.json` and the `--retention-config` schedule filter.
- Retained `CWH_CW_L` and `CWH_YC_L`; kept `CWH_HW_L` and `CWH_CW_M`
  harvestable.
- Rebuilt the model-input bundle, ws4 matrix, baseline, targets, and UI.
- Bumped the instance version to 0.2.0 and added `RELEASE_NOTES.md`.

## 3. Evidence

### Managed/VDYP

Eight of twelve AUs meet or beat VDYP on gross volume. The four below are
documented in `notes/reference/tipsy-vs-vdyp.md` and
`config/tsr/tipsy_au_results_vdyp_comparison.csv`.

### Retention

| Scenario | THLB remaining | 100-yr average | Share of pro-rated AAC |
| --- | ---: | ---: | ---: |
| Harvest all AUs | 28,557.9 ha | 176,955 m3/yr | 100.4% |
| Retain CWH_CW_L + CWH_YC_L | 26,840.3 ha | 173,553 m3/yr | 98.4% |
| Retain CWH_HW_L + CWH_CW_M | 21,133.3 ha | 143,228 m3/yr | 81.2% |
| Retain all four | 19,415.7 ha | 139,825 m3/yr | 79.3% |

The accepted policy is the two-AU retention. The pro-rated AAC is
1,096,000 * 28,557.9 / 177,505 = 176,330 m3/yr.

### Accepted baseline

- Scheduled blocks: 46,321
- Scheduled area: 390,438.4 ha
- Retained blocks: 4,968
- Retained total stand area: 52,013.6 ha
- Retained model THLB: 1,717.6 ha
- Remaining model THLB: 26,840.3 ha
- First decade managed volume: 10,384,983 m3
- 100-year managed volume: 17,355,255 m3
- 100-year average: 173,553 m3/yr
- Provisional targets: both met

## 4. Decision

Retain `CWH_CW_L` and `CWH_YC_L`, keep `CWH_HW_L` and `CWH_CW_M` in the
harvest schedule. The full decision record is
`notes/adr/0001-retain-low-yield-aus.md`; the working analysis is
`notes/reference/retention-decision.md`; the public explanation is
`docs/retention-policy.rst`.

## 5. Gates and release

- `python scripts/dashboard.py`: GREEN.
- `python -m freshforge validate` passes for the 10-node full workflow and the
  7-node downstream workflow.
- PR #36 merged to `main` as `34c6f65` after CI run 39903434345 passed.
- Docs run 39903434346 built with warnings as errors and deployed Pages after
  Pages was enabled for GitHub Actions. Site:
  https://ubc-fresh.github.io/femic-northisland-instance/
- v0.2.0 release:
  https://github.com/UBC-FRESH/femic-northisland-instance/releases/tag/v0.2.0

## 6. Commits

- `d07e263` and earlier: TSR extraction, RESULTS lane, BatchTIPSY lane, charts,
  THLB table, and NICC land-base/UI work.
- This closeout adds the retention policy, base-model rebuild, notes, Sphinx
  pages, version bump, and release notes.

## 7. Residual risks

- The baseline is a one-pass schedule, not a sustained-yield optimization.
- The pro-rated AAC uses the model THLB share of the TSR THLB and is an
  approximation.
- The retained AUs still hold old first-growth volume that is not liquidated.
- The managed TIPSY curves for the retained AUs remain in the bundle as
  provenance and are not scheduled.
