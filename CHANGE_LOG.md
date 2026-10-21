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
