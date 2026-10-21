# Phase close-out report: P0 Bootstrap

Phase: P0 Bootstrap
Parent issue: #1
Pull request: queued, `feature/p0-bootstrap` into `main`
Evidence head: `fbe4884`
Report commit: the commit that adds this report
Date: 2026-10-21
Status: queued for approval. Not merged.

## Recommendation

Approve these actions. The agent carries them out in this order, and reads back each result.

1. Squash-merge the Phase 0 pull request, and delete `feature/p0-bootstrap`.
2. Close parent issue #1 with a closeout comment that cites the merge commit.
3. Launch P1: create its branch, set the phase statuses in `ROADMAP.md`, create its child issues, and start P1.1.

Settings changes: none.

## 1. Objectives and acceptance

| Criterion | Evidence | Status |
| --- | --- | --- |
| Adapt the seed contract and project identity | `91344ff`; `README.md`, `AGENTS.md`, `ROADMAP.md`, `notes/reference/aoi.md` | met |
| Add the FEMIC instance configuration and AOI boundary | `1c5aa20`; `data/source/aoi/northisland_aoi.gpkg`, 1,083,003.66 ha | met |
| Add the FreshForge provider and model-build workflow | `a62d397`; 11 nodes; `freshforge validate` and `plan` pass | met |
| Verify the dashboard and web UI path | `47153cc`; dashboard GREEN, 160 tests; UI command in `README.md` | met with a stated limit: the UI smoke waits for the first matrix and baseline in P4 |
| No generated runtime or model output tracked | `.gitignore` and `git status` | met |

## 2. Workflow compliance

- Parent issue #1 existed before `feature/p0-bootstrap`.
- Child issues #2 to #5 are linked as sub-issues of #1.
- Commits start with task IDs: `P0.1` to `P0.4`.
- Roadmap, changelog, notes, and issue state moved with the work.
- Approval gates: the maintainer approved repository creation in the session; no tag, release, or settings change was made.

## 3. Gate evidence

`python scripts/dashboard.py` on `47153cc`:

```text
GATE                STATUS   SECONDS
lint                GREEN
format              GREEN
types               GREEN
tests               GREEN
validator           GREEN
docs                GREEN
OVERALL: GREEN. Every gate passed.
```

`python -m pytest -q`: 160 passed, 95.68 percent branch coverage of `scripts/`.

`python -m freshforge validate workflows/freshforge/northisland_model_build.yaml`:
validation passed with 11 nodes.

`python -m freshforge plan workflows/freshforge/northisland_model_build.yaml`:
the plan lists all 11 nodes in dependency order.

## 4. CI evidence

| Run ID | Head commit | Conclusion | Notes |
| --- | --- | --- | --- |
| 39649466430 | `fbe4884` | success | Quality gates, dashboard summary, and pre-commit parity all pass |

The first run on the seed head failed because CI did not install the public-data
runtime dependencies. `fbe4884` adds pandas, pyarrow, geopandas, shapely,
requests, and the matching type stubs to `requirements-dev.txt`, and the run is
green.

## 5. Deviations

| Deviation | Cause | Remedy |
| --- | --- | --- |
| The Basecamp CLI was not on `PATH` | Installed under `~/.local/bin` | Used the absolute CLI path for read-only discovery |
| Wine was absent | Host prerequisite for the bundled 32-bit VDYP7 console | Installed `wine64` and `wine32:i386`; recorded as a host prerequisite |
| The provisional TSA-only run was stopped | The email AOI is TSA clipped to NICC, not the whole TSA | Replaced it with the custom AOI before any model output was accepted |
| BatchTIPSY is absent | The first lane uses `vdyp_transform` | Recorded as a release blocker; replace with accepted TIPSY output before release |

## 6. Next phase

P1 confirms the CFA interpretation, materializes the public data root, and
validates the AOI and source manifests. Recommended default: treat K3Z as the CFA
unless the attached map shows a different file.

## 7. Decision

- [ ] Approve as written.
- [ ] Approve with the changes stated here: <changes>.
