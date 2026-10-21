# FEMIC North Island Instance

Public FEMIC and ws4 model instance for the North Island Timber Supply Area AOI.
FEMIC rebuilds the inventory and yield curves from public BC data; ws4 compiles
the resulting model and serves it in a local web UI.

## Status

Phase 0 (bootstrap) is active. The public AOI boundary, FEMIC profile, and the
FreshForge workflow exist. The first full VDYP/TIPSY build and ws4 baseline run
are the next executable lane. `ROADMAP.md` is the plan of record, and the GitHub
issues carry the live state.

## AOI

The Basecamp email thread defines the AOI as TSA 48 clipped to the North Island
- Central Coast Natural Resource District, with the community forest agreement
added back. The tracked boundary is
`data/source/aoi/northisland_aoi.gpkg` (EPSG:3005, layer `northisland_aoi`,
1,083,003.66 ha). See `notes/reference/aoi.md` for the quote, sources, and
review checkpoints.

## Model-build chain

```text
public BC data (VRI, TSA, district, tenure)
  -> femic prep validate-case / geospatial-preflight
  -> femic run (VDYP natural curves + managed curve transform)
  -> femic tsa post-tipsy (model-input bundle)
  -> femic export patchworks (ForestModel XML + fragments)
  -> ws4 build + validate (canonical matrix)
  -> ws4 baseline schedule + simulate + report
  -> ws4 prepare UI geometry + serve
```

The Patchworks XML/fragments pair is an interchange artifact for ws4. Patchworks
is not the runtime lane for this instance.

## Reproduce the build with FreshForge

FreshForge is the workflow of record. Each node is a recorded command with an
artifact path.

```bash
python -m pip install -e .
python -m freshforge validate workflows/freshforge/northisland_model_build.yaml
python -m freshforge plan workflows/freshforge/northisland_model_build.yaml
export FEMIC_EXTERNAL_DATA_ROOT=/path/to/femic-public-data/data
python -m freshforge run workflows/freshforge/northisland_model_build.yaml \
  --workdir runtime/freshforge \
  --namespace northisland/model-build \
  --json
```

The public data root must contain `bc/tsa/FADM_TSA.gdb`,
`bc/vri/2025/VEG_COMP_LYR_R1_POLY_2025.gdb`, and the matching VDYP input
geodatabase. The `femic-public-data` submodule is the canonical source.

VDYP7 runs under Wine on Linux. The repository carries the VDYP executable; the
host needs `wine` and `wine32`. The first lane uses the VDYP-transform managed
curve mode, so it does not require BatchTIPSY. Replace that lane with accepted
TIPSY output before release.

## Web UI

```bash
./serve_northisland.sh
```

`PORT=...` overrides the default `8014`. The script passes `--crs EPSG:3005`,
`--allow-runs`, and `--allow-agent`, with the agent working directory set to the
instance root.

The service binds loopback only. ws4 has no authentication; do not expose it
without a trusted proxy. The geometry is EPSG:3005 and MapLibre projects it to
WGS84 in the browser.

## Repository map

| Path | Purpose |
| --- | --- |
| `AGENTS.md` | Agent operating contract and project-specific rules |
| `ROADMAP.md` | Phases, tasks, and GitHub issue map |
| `CHANGE_LOG.md` | Dated narrative of changes |
| `config/` | FEMIC run profile, rebuild spec, TIPSY scaffold, Patchworks export config |
| `data/source/aoi/` | Tracked public AOI boundary and review summary |
| `src/northisland_workflow/` | FreshForge provider and ws4 command contracts |
| `workflows/freshforge/` | The model-build workflow of record |
| `scripts/` | AOI build, baseline schedule, UI geometry, workflow validator |
| `docs/` | Sphinx site and RTFM surface |
| `notes/` | AOI decision, ADRs, and close-out reports |
| `tests/` | Unit and contract tests |

## Public-data boundary

This repository is public. Do not add raw MKRF cost or revenue spreadsheets,
private tenure data, credentials, or machine-specific paths. The model uses
published BC data and public cost/price bases.

## License

MIT. See `LICENSE`.
