# Phase close-out report: P1 AOI and public data

Phase: P1 AOI and public data
Parent issue: #7
Pull request: queued, `feature/p1-aoi-public-data` into `main`
Evidence head: the commit before this report
Report commit: the commit that adds this report
Date: 2026-10-21
Status: queued for approval. Not merged.

## Recommendation

Approve these actions.

1. Squash-merge the Phase 1 pull request, and delete `feature/p1-aoi-public-data`.
2. Close parent issue #7 with a closeout comment that cites the merge commit.
3. Launch P2: create its branch, set the phase statuses, create its child issues,
   and start the FEMIC upstream build.

Settings changes: none.

## 1. Objectives and acceptance

| Criterion | Evidence | Status |
| --- | --- | --- |
| Confirm the CFA interpretation | #8; overview map; `notes/reference/aoi.md` | met with a limit: the map does not label the CFA, so K3Z is the public-tenure match |
| Record the public data root | #9; `notes/reference/public-data.md`; `data/source/public_data_manifest.json` | met |
| Validate the AOI and source checksums | #10; `scripts/build_aoi.py`; `scripts/check_public_data.py`; `femic prep validate-case` | met |

## 2. Workflow compliance

- Parent issue #7 existed before `feature/p1-aoi-public-data`.
- Child issues #8 to #10 are linked as sub-issues.
- Commits start with task IDs.
- Approval gates: no tag, release, or settings change.

## 3. Gate evidence

`python scripts/dashboard.py`: all gates GREEN.

`python -m pytest -q`: passes with the 95 percent branch coverage gate.

`femic prep validate-case --run-config config/run_profile.northisland.yaml`:
passed with the custom AOI boundary and the materialized public data root.

`python scripts/check_public_data.py`: four required geodatabases present, key
tables hashed, manifest written.

## 4. CI evidence

CI runs on the pull request head. The local dashboard is the evidence head above.

## 5. Deviations

| Deviation | Cause | Remedy |
| --- | --- | --- |
| The attached image is only the sender logo | The map is the `north_island_tsa_48.pdf` attachment | Rendered the PDF and inspected the overview map |
| The map does not label the CFA | It is a TSA overview map, not a tenure map | Recorded K3Z as the only active community forest match and kept the caveat |

## 6. Next phase

P2 runs the FEMIC upstream build through FreshForge. Recommended default: use the
materialized public data root from `FEMIC_EXTERNAL_DATA_ROOT`, keep
`managed_curve_mode: vdyp_transform` for the first lane, and record the TIPSY gap
as a release blocker.

## 7. Decision

- [ ] Approve as written.
- [ ] Approve with the changes stated here: <changes>.
