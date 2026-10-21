# Phase close-out report: P3 ws4 model build

Phase: P3 ws4 model build
Parent issue: #18
Pull request: queued, `feature/p3-ws4-model` into `main`
Evidence head: `d2b7405`
Report commit: the commit that adds this report
Date: 2026-10-21
Status: queued for approval. Not merged.

## Recommendation

1. Squash-merge the Phase 3 pull request, and delete `feature/p3-ws4-model`.
2. Close parent issue #18 with a closeout comment that cites the merge commit.
3. Launch P4 for the baseline, targets, and web UI verification.

Settings changes: none.

## 1. Objectives and acceptance

| Criterion | Evidence | Status |
| --- | --- | --- |
| Build the ws4 matrix | `d2b7405`; `runtime/matrix/manifest.json` | met |
| Validate the dataset | `Dataset is valid` | met |
| Inspect coverage | `notes/reference/ws4-build.md` | met |

## 2. Workflow compliance

- Parent #18 existed before `feature/p3-ws4-model`.
- Child #19 to #21 are linked as sub-issues.
- The downstream FreshForge workflow validates and plans with 7 nodes.

## 3. Gate evidence

- `python scripts/dashboard.py`: all gates GREEN.
- `ws4 build`: exit 0.
- `ws4 validate`: `Dataset is valid`.
- Matrix: 56,187 blocks and fragments, 9,612 tracks, 2,156 curves, 5,930 treatments, 442,451.9975 ha block area.
- Managed/unmanaged at year 0: 285,579.4582 / 413,894.0517 ha.

## 4. CI evidence

CI runs on the pull request head.

## 5. Deviations

| Deviation | Cause | Remedy |
| --- | --- | --- |
| Schedule block count (51,289) is lower than the blocks table (56,187) | Split managed/unmanaged portions share a block id | The schedule builder groups by block; recorded in the build note |

## 6. Next phase

P4 runs the baseline simulation, records the target report, and verifies the
loopback web UI with the AOI geometry.

## 7. Decision

- [ ] Approve as written.
- [ ] Approve with the changes stated here: <changes>.
