# Change Log

Newest entries last. Each milestone gets a dated entry that matches the roadmap status and the GitHub issue comments.

## 2026-10-21

- Created FEMIC North Island Instance from the UBC-FRESH dev workflow seed. The agent contract, roadmap, docs skeleton, and validator came from the seed. Every phase is planned, and no parent issues exist yet.

## 2026-10-21

- Created `femic-northisland-instance` from the UBC-FRESH dev workflow seed and
  opened P0 parent issue #1 with child tasks #2 to #5.
- Recorded the Basecamp AOI decision in `notes/reference/aoi.md`: TSA 48 clipped
  to the North Island - Central Coast Natural Resource District, with the
  community forest agreement added back. The tracked AOI is
  `data/source/aoi/northisland_aoi.gpkg`, 1,083,003.66 ha in EPSG:3005.
- Added the FEMIC run profile, rebuild spec, Patchworks export config, and a
  provisional TIPSY scaffold. The first lane uses `vdyp_transform` managed
  curves and does not require BatchTIPSY.
- Added the instance-owned `northisland.ws4` FreshForge provider with build,
  validate, post-TIPSY, baseline schedule, simulate, report, and UI geometry
  nodes. The workflow validates and plans with 11 nodes.
- Added the AOI, baseline schedule, and UI geometry scripts with tests. The local
  suite passes 160 tests and the full dashboard is green.
- Installed Wine and Wine32 on the host so the bundled VDYP7 console executable
  can run on Linux. This is a host prerequisite, not a repository artifact.
- Closed P0.1 to P0.3 and queued P0.4. `python scripts/dashboard.py` reports all
  gates GREEN with 160 tests. `freshforge validate` and `plan` pass for the
  11-node workflow. Generated AOI, VDYP, and runtime outputs remain untracked.
- Merged Phase 0 as `e853651`, closed parent issue #1, and launched Phase 1 on
  `feature/p1-aoi-public-data` with parent #7 and tasks #8 to #10.
- Completed P1.1 to P1.3 on `feature/p1-aoi-public-data`. The Basecamp overview
  map confirms the TSA and NICC district geometry but does not label the CFA;
  K3Z remains the only active community forest touching the clipped TSA. Added
  `scripts/check_public_data.py` and the portable
  `data/source/public_data_manifest.json`. The dashboard is GREEN.
- Merged Phase 1 as `b13f957` and launched Phase 2 on
  `feature/p2-femic-upstream` with parent #12 and tasks #13 to #16.
- Completed the P2 upstream build. The corrected auto-sampling run covers all 12
  AUs, writes the model-input bundle, and exports 51,289 fragments and 49 curves.
  `freshforge validate` passes for the 10-node full workflow and the 7-node
  downstream workflow.
- Merged Phase 2 as `f5dd1cb` (squash of PR #17) and launched Phase 3 on
  `feature/p3-ws4-model` with parent #18 and tasks #19 to #21. The downstream
  FreshForge workflow builds and validates the ws4 matrix.
- Completed the P3 ws4 build. `ws4 build` and `validate` pass; the matrix has
  56,187 blocks/fragments, 2,156 curves, 5,930 treatments, and 442,451.9975 ha
  of block area.
- Merged Phase 3 as `f4fea9e` and launched Phase 4 on `feature/p4-baseline-ui`
  with parent #23 and tasks #24 to #27. The baseline run and the loopback web UI
  are verified.
- Completed P4: baseline simulated, two provisional targets met, and the ws4 UI
  verified with 51,289 blocks on loopback port 8014.
- Merged Phase 4 as `2558f9c`. The North Island model builds end to end and the
  ws4 UI is live on `127.0.0.1:8014` with 51,289 blocks and two met targets.
- Launched Phase 5 on `feature/p5-tsr-metadata` with parent #29 and tasks #30 to
  #35. The phase uses the FEMIC TSR document-metadata workflows to extract the
  TSA 48 data-package structure, the full THLB net-down ladder, and AU-wise
  TIPSY parameters.
- Completed P5.1 to P5.4. Extracted 413 TSA 48 TSR candidate facts from the 2020
  data package, 2022 discussion paper, and 2024 rationale; built the reviewed
  overlay and source-layer recipe; transcribed the full Table 4 THLB net-down
  ladder; and mapped all 12 model AUs to TSR-sourced OAF2, genetic-worth, and
  regeneration constants. The exact published `tsa48_tipsy_input` workbook is
  not available and remains the TIPSY blocker.

## 2026-10-22

- Added the public RESULTS candidate lane for AU-wise TIPSY inputs. The fetch
  covers `RSLT_OPENING_SVW`, `RSLT_PLANTING_SVW`, and
  `RSLT_FOREST_COVER_INV_SVW`; the separate forest-cover-species package is
  attribute-only and exposes no WFS resource, so the inventory species columns
  are used instead.
- Added `scripts/build_results_tipsy_inputs.py`, its unit tests, and
  `runbooks/RESULTS_CANDIDATES.md`. The first run assigned 4,198 openings across
  all 12 model AUs and wrote `config/tsr/tipsy_au_results_candidates.csv`.
  Density comes from RESULTS planting records; the three thin AUs use a single
  planting record and are labelled `planting_single`.
- BatchTIPSY still did not produce `04_output-northisland.csv` within five
  minutes under Wine with the RESULTS input. The RESULTS table remains a
  diagnostic candidate, not the accepted managed-curve lane.
- `python scripts/dashboard.py` is GREEN with 189 tests and 96.47 percent branch
  coverage of `scripts/`.

## 2026-10-22

- Corrected the earlier P5.5 conclusion. BatchTIPSY does run under Wine on this
  host through the documented `tsa29mini` lane: a scratch Wine prefix with Wine
  Mono 9.0.0, a userspace Xvfb patched to `/tmp/xkb`, and a direct
  `wine TIPSYbtc.exe /TSR` call. The earlier failures came from the system
  `xvfb-run`/legacy prefix path, not from TIPSY itself.
- Added `runbooks/tipsy-btc-linux-wine.md` and
  `scripts/tipsybtc-wine.sh` with the working recipe and the FEMIC wrapper
  contract.
- Fixed `scripts/build_results_tipsy_inputs.py` so planted densities are
  integers. BatchTIPSY parses those columns as `Integer`; a value such as
  `416.7` raised a hidden .NET conversion dialog.
- The 12-AU RESULTS input now completes with `exit_code=0`, 12 output rows, and
  zero error rows. Eight of twelve AUs meet or beat VDYP on gross volume;
  CWH_HW L, CWH_CW L and M, and CWH_YC L remain below and are documented as a site-index
  and curve-interpretation gap.
- Updated `config/tipsy/northisland.yaml` to the RESULTS species and density.
  Rebuilt the model-input bundle (696 curves), ws4 matrix (56,187
  blocks/fragments), baseline run, target report, and UI geometry. Both
  provisional targets are met.
- `python scripts/dashboard.py` is GREEN.
- Marked P5.5 complete: the managed-curve lane now carries the reviewed RESULTS
  parameters, the ws4 dataset validates, and both provisional targets are met.
  The low CWH_CW L and M and CWH_YC L gross-volume ratios remain documented
  review items for P5.6.

## 2026-10-22 - Offset clock and UI geometry

- Rebuilt the NICC baseline on the 0-based offset clock; both provisional targets remain met.
- Reduced the UI polygon simplification from 100 m to 10 m.
