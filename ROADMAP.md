# FEMIC North Island Instance Roadmap

This roadmap is the plan of record and the issue tracker map for the North Island
instance. Keep it in step with the GitHub issues, `CHANGE_LOG.md`, and `notes/`.
`scripts/check_workflow.py` parses the phase headers, status lines, and checkboxes
below, so keep their format.

Every phase starts as `planned` with `Parent issue: TBD`. Activate a phase only
after its parent issue exists and the maintainer approves it.

## Issue Tracker Map

| Phase | Parent issue | Branch | Status |
| --- | --- | --- | --- |
| P0 Bootstrap | #1 | `feature/p0-bootstrap` | complete |
| P1 AOI and public data | #7 | `feature/p1-aoi-public-data` | complete |
| P2 FEMIC upstream build | #12 | `feature/p2-femic-upstream` | complete |
| P3 ws4 model build | #18 | `feature/p3-ws4-model` | complete |
| P4 Baseline, targets, and web UI | #23 | `feature/p4-baseline-ui` | pr-open |
| P5 Verify and release | TBD | `feature/p5-verify-release` | planned |
| P6 Operate and maintain | TBD | `feature/p6-operate` | planned |

## Lifecycle Map

| Stage | Phases | Exit criteria |
| --- | --- | --- |
| Scope and design | P0, P1 | The AOI, sources, and public/private boundary are recorded and validated |
| Build | P2, P3 | FEMIC compiles the inputs and ws4 builds and validates the matrix |
| Verify | P4, P5 | The baseline run, target report, and web UI are inspected and reproducible |
| Release and deploy | P5 | A reviewed release names the exact artifacts and their provenance |
| Operate and maintain | P6 | Review cadence, incoming changes, and retirement are recorded |
| Retire | P6 (procedure) | Archive notice, final changelog entry, and issues closed |

## Conventions

- A phase is `P<n>`. A task is `P<n>.<m>`. A subtask is a checklist item inside
  the task's issue body. Three levels at most.
- Status values are `planned`, `active`, `pr-open`, `complete`, and `deferred`.
- A phase becomes `complete` only after its pull request merges to `main` and its
  parent issue closes.

## Phase 0: Bootstrap

Parent issue: #1
Branch: `feature/p0-bootstrap`
Status: complete

Goal: make the repository a self-describing, reproducible FEMIC and ws4 instance
for the North Island AOI.

- [x] P0.1 Adapt the seed contract and project identity (#2)
- [x] P0.2 Add the FEMIC instance configuration and AOI boundary (#3)
- [x] P0.3 Add the FreshForge provider and model-build workflow (#4)
- [x] P0.4 Verify the green dashboard and local web UI path (#5)

Acceptance criteria:

- `python scripts/dashboard.py` is green.
- `python -m freshforge validate` and `plan` pass for
  `workflows/freshforge/northisland_model_build.yaml`.
- The committed AOI GeoPackage has one EPSG:3005 polygon and the reviewed area.
- No generated runtime or model output is tracked.

## Phase 1: AOI and public data

Parent issue: #7
Branch: `feature/p1-aoi-public-data`
Status: complete

Goal: confirm the Basecamp AOI decision, materialize the public data root, and
verify the boundary and source layers.

- [x] P1.1 Confirm the CFA interpretation with the thread and map (#8)
- [x] P1.2 Materialize the public VRI, VDYP, TSA, and district layers (#9)
- [x] P1.3 Validate the AOI area, bounds, and source checksums (#10)

Acceptance criteria:

- The AOI decision names the exact clip and add-back layers.
- `femic prep validate-case` passes against the materialized public data root.
- The boundary and source manifests are recorded.

## Phase 2: FEMIC upstream build

Parent issue: #12
Branch: `feature/p2-femic-upstream`
Status: complete

Goal: compile natural and managed yield inputs for the AOI with FEMIC.

- [x] P2.1 Run the VDYP curve build and inspect the curve diagnostics (#13)
- [x] P2.2 Build the post-TIPSY model-input bundle (#14)
- [x] P2.3 Export the ForestModel XML and fragments for ws4 (#15)
- [x] P2.4 Record the accepted runtime boundary and any deferred TIPSY gap (#16)

Acceptance criteria:

- The run manifest, curve tables, bundle tables, and XML/fragments exist.
- The model-input QA checks pass or have a recorded blocker.
- The export has the expected block and area counts.

## Phase 3: ws4 model build

Parent issue: #18
Branch: `feature/p3-ws4-model`
Status: complete

Goal: compile the FEMIC export into a canonical ws4 dataset and validate it.

- [x] P3.1 Build the ws4 matrix from the exported XML and fragments (#19)
- [x] P3.2 Validate the dataset manifest and schema invariants (#20)
- [x] P3.3 Inspect block, curve, treatment, and account coverage (#21)

Acceptance criteria:

- `python -m ws4.cli build` and `validate` pass.
- The dataset has positive managed area and no orphan block joins.
- The manifest records the XML and fragment inputs.

## Phase 4: Baseline, targets, and web UI

Parent issue: #23
Branch: `feature/p4-baseline-ui`
Status: pr-open

Goal: produce the first baseline schedule and target report, then serve the model
in the ws4 web UI.

- [x] P4.1 Build and simulate the baseline schedule (#24)
- [x] P4.2 Write the first target set and report (#25)
- [x] P4.3 Prepare the UI geometry and launch the loopback service (#26)
- [x] P4.4 Verify map rendering, target display, and run switching (#27)

Acceptance criteria:

- The baseline run has a harvest and growing-stock summary.
- The target report distinguishes met and unmet rows.
- The web UI renders the AOI and the baseline run with `--crs EPSG:3005`.

## Phase 5: Verify and release

Parent issue: TBD
Branch: `feature/p5-verify-release`
Status: planned

Goal: verify the full workflow from a clean checkout and publish the reviewed
instance artifacts.

- [ ] P5.1 Run the full workflow from a clean checkout
- [ ] P5.2 Record the release notes and known gaps
- [ ] P5.3 Tag and publish after approval

Acceptance criteria:

- A clean checkout reproduces the matrix and baseline run.
- The release names the exact commit, data root, and runtime versions.
- No private data or generated model output is tracked.

## Phase 6: Operate and maintain

Parent issue: TBD
Branch: `feature/p6-operate`
Status: planned

Goal: keep the instance current and retire it cleanly when needed.

- [ ] P6.1 Set a review cadence and record the first review
- [ ] P6.2 Triage source-layer, runtime, and AOI changes
- [ ] P6.3 Record the retirement procedure

Acceptance criteria:

- The review cadence is held once and recorded.
- Incoming changes have a disposition.

## Detailed Next Steps Notes

1. Phase 0 is active on `feature/p0-bootstrap`, parent issue #1. Its child tasks
   are #2 to #5.
2. The AOI is TSA 48 clipped to the NICC district, with the community forest
   agreement added back. See `notes/reference/aoi.md`.
3. The first model execution uses `managed_curve_mode: vdyp_transform` and does
   not require BatchTIPSY. Replace it with accepted TIPSY output before release.
4. Run FreshForge from the instance root with `FEMIC_EXTERNAL_DATA_ROOT` set to
   the materialized public data tree.
