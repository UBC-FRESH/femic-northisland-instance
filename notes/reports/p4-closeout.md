# Phase close-out report: P4 baseline, targets, and web UI

Phase: P4 baseline, targets, and web UI
Parent issue: #23
Pull request: queued, `feature/p4-baseline-ui` into `main`
Evidence head: `fe445cd`
Report commit: the commit that adds this report
Date: 2026-10-21
Status: queued for approval. Not merged.

## Recommendation

1. Squash-merge the Phase 4 pull request, and delete `feature/p4-baseline-ui`.
2. Close parent issue #23 with a closeout comment that cites the merge commit.
3. Launch P5 for clean-checkout verification and release notes.

Settings changes: none.

## 1. Objectives and acceptance

| Criterion | Evidence | Status |
| --- | --- | --- |
| Baseline run | `runtime/baseline`, 51,289 blocks, 100 years | met |
| Target report | two provisional targets, both `met` | met |
| UI geometry and service | `runtime/fragments.geojson`, `/health` ok on 8014 | met |
| Map and target verification | headless browser, 51,289 blocks, no console errors | met |

## 2. Workflow compliance

- Parent #23 existed before `feature/p4-baseline-ui`.
- Child #24 to #27 are linked as sub-issues.
- Evidence is in `notes/reference/ws4-baseline.md`.

## 3. Gate evidence

- `python scripts/dashboard.py`: all gates GREEN.
- Baseline harvest by decade: 10.7M, 2.4M, 4.4M, 0.16M m3.
- Targets: product 1,063,908.30 vs 1,000,000; feature 6,885,994.52 vs 5,000,000.
- UI: 51,289 blocks, 4,746 treated in period 2, two met targets.

## 4. CI evidence

CI runs on the pull request head.

## 5. Deviations

| Deviation | Cause | Remedy |
| --- | --- | --- |
| Baseline is front-loaded | Clearcut-at-age-60 replay | Recorded as a smoke baseline, not an optimized schedule |
| Targets are provisional | No reviewed policy set yet | Recorded as demonstration targets |
| Browser emitted WebGL performance warnings | Headless GPU readback | No application errors; accepted |

## 6. Next phase

P5 verifies the full workflow from a clean checkout, records the release notes,
and names the remaining TIPSY and target-policy gaps.

## 7. Decision

- [ ] Approve as written.
- [ ] Approve with the changes stated here: <changes>.
