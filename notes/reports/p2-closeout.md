# Phase close-out report: P2 FEMIC upstream build

Phase: P2 FEMIC upstream build
Parent issue: #12
Pull request: queued, `feature/p2-femic-upstream` into `main`
Evidence head: `d286bde`
Report commit: the commit that adds this report
Date: 2026-10-21
Status: queued for approval. Not merged.

## Recommendation

1. Squash-merge the Phase 2 pull request, and delete `feature/p2-femic-upstream`.
2. Close parent issue #12 with a closeout comment that cites the merge commit.
3. Launch P3 and continue into the ws4 build and UI verification.

Settings changes: none.

## 1. Objectives and acceptance

| Criterion | Evidence | Status |
| --- | --- | --- |
| VDYP curves for all four strata | 12 AUs: CWH_HW/L/M/H, CWH_CW/L/M/H, CWH_YC/L/M/H, CWH_FD/L/M/H | met with a stated limit: auto sampling |
| Post-TIPSY model-input bundle | `data/model_input_bundle/au_table.csv` has 12 rows | met; `femic run` assembles the bundle, so the separate post-TIPSY node was removed |
| ForestModel XML and fragments | export: 12 AUs, 49 curves, 51,289 fragments | met |
| Runtime boundary recorded | `notes/reference/vdyp-runtime.md`, `docs/model-build.rst` | met |

## 2. Workflow compliance

- Parent #12 existed before `feature/p2-femic-upstream`.
- Child #13 to #16 are linked as sub-issues.
- Commits start with task IDs.
- The full FreshForge workflow validates and plans with 10 nodes after the redundant post-TIPSY node was removed.

## 3. Gate evidence

- `python scripts/dashboard.py`: all gates GREEN.
- `femic run`: exit 0; `vdyp_results` covers all four strata.
- Export: `patchworks export completed tsa=['northisland'] au=12 fragments=51289 curves=49`.
- `python -m freshforge validate workflows/freshforge/northisland_model_build.yaml`: 10 nodes.
- `python -m freshforge validate workflows/freshforge/northisland_ws4_from_bundle.yaml`: 7 nodes.

## 4. CI evidence

CI runs on the pull request head.

## 5. Deviations

| Deviation | Cause | Remedy |
| --- | --- | --- |
| The first `all` sampling run timed out | The VDYP console batch timeout is 30 s | Switched to `vdyp_sampling_mode: auto` with `vdyp_two_pass_rebin: false` |
| The standalone post-TIPSY node failed on artifact names | The legacy pipeline uses `tsanorthisland` names, while the bundle path uses `northisland` | Removed the redundant node; `femic run` already writes the bundle |
| Body harvest is front-loaded | Baseline is a clearcut-at-age-60 replay, not an optimized schedule | Recorded as a baseline limitation; P4 targets and search are separate |

## 6. Next phase

P3 compiles the exported XML/fragments into ws4, validates the matrix, and records the dataset evidence. The downstream FreshForge workflow already exercises those nodes.

## 7. Decision

- [ ] Approve as written.
- [ ] Approve with the changes stated here: <changes>.
