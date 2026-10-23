# FEMIC North Island Instance

Public FEMIC and ws4 model instance for the North Island Timber Supply Area AOI.
FEMIC rebuilds the inventory and yield curves from public BC data; ws4 compiles
the resulting model and serves it in a local web UI. This repository is
tracked in `femic` as the `external/femic-northisland-instance` submodule.

## Runtime lane

**ws4 is the primary runtime.** The Patchworks XML/fragments pair is an
interchange input to `ws4 build`; Patchworks itself is reference-only. The
NICC model is the student/MSFM lane for the TSA 48 ∩ NICC + K3Z area. Its
full-TSA benchmark sibling is
**[`UBC-FRESH/femic-tsa48-instance`](https://github.com/UBC-FRESH/femic-tsa48-instance)**
(port 8016). That repository carries the full-TSA benchmark, the NICC
intersection as a `part` flag, and the current `≈214,544 m3/yr` NICC harvest
reference.

The two repositories are deliberately related but **independent datasets and
runtimes**. Either can be used alone. See
`notes/reference/related-instances.md` for the shared-input and scope contract.

## Status

v0.2.0 is the locked NICC base model. The public AOI boundary, FEMIC upstream
build, BatchTIPSY managed curves, ws4 matrix, retention schedule, baseline run,
and loopback web UI are verified. The baseline retains `CWH_CW_L` and
`CWH_YC_L` and keeps the other ten AUs harvestable; the 100-year average carries
98.4% of the pro-rated AAC. `ROADMAP.md` is the plan of record, and the GitHub
issues carry the live state. See `docs/retention-policy.rst` and
`notes/reference/retention-decision.md`.

## AOI

The Basecamp email thread defines the AOI as TSA 48 clipped to the North Island
- Central Coast Natural Resource District, with the community forest agreement
added back. The tracked boundary is
`data/source/aoi/northisland_aoi.gpkg` (EPSG:3005, layer `northisland_aoi`,
1,083,003.66 ha). See `notes/reference/aoi.md` for the quote, sources, and
review checkpoints.

## First build

- AOI: 1,083,003.66 ha (TSA 48 clipped to NICC, CFA added back).
- FEMIC: 12 AUs across CWH_HW, CWH_CW, CWH_YC, and CWH_FD at L/M/H.
- Export: 51,289 fragments, 696 curves.
- ws4 matrix: 56,187 blocks/fragments, 5,930 treatments.
- Baseline: 46,321 scheduled blocks after retaining `CWH_CW_L` and `CWH_YC_L`.
- Managed harvest: 173,553 m3/yr over 100 years, 98.4% of the 176,330 m3/yr
  pro-rated AAC.
- Targets: ten NICC reference floors (214,544 m3/yr) plus the growing-stock smoke target; reference run meets all.
- UI: 51,289 blocks, MapLibre, `http://127.0.0.1:8014/`.

## Model-build chain

```text
public BC data (VRI, TSA, district, tenure)
  -> femic prep validate-case / geospatial-preflight
  -> femic run (VDYP curves, managed transform, model-input bundle)
  -> femic export patchworks (ForestModel XML + fragments)
  -> ws4 build + validate (canonical matrix)
  -> ws4 baseline schedule + simulate + report
  -> ws4 prepare UI geometry + serve
```

The Patchworks XML/fragments pair is an interchange artifact for ws4. Patchworks
is not the runtime lane for this instance and is retained only as reference
evidence for comparison and rebuild provenance.

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

If the inspected FEMIC bundle already exists, the downstream workflow starts at
the XML/fragments export:

```bash
python -m freshforge run workflows/freshforge/northisland_ws4_from_bundle.yaml \
  --workdir runtime/freshforge \
  --namespace northisland/ws4 \
  --json
```

The public data root must contain `bc/tsa/FADM_TSA.gdb`,
`bc/vri/2025/VEG_COMP_LYR_R1_POLY_2025.gdb`, and the matching VDYP input
geodatabase. The `femic-public-data` submodule is the canonical source.

VDYP7 runs under Wine on Linux. The repository carries the VDYP executable; the
host needs `wine` and `wine32`. BatchTIPSY also runs under Wine through the
scratch-prefix, Wine Mono, and userspace-Xvfb lane in
`runbooks/tipsy-btc-linux-wine.md`. The accepted managed lane uses public RESULTS
species and density with the model PSPL/VDYP site index; the AU-wise comparison
is in `config/tsr/tipsy_au_results_vdyp_comparison.csv`.

## Web UI

```bash
python scripts/prepare_land_base.py \
  --aoi data/source/aoi/northisland_aoi.gpkg \
  --out runtime/land_base.geojson
./serve_northisland.sh
```

`PORT=...` overrides the default `8014`. The script passes `--crs EPSG:3005`,
the exact block geometry, the AOI land-base underlay, `--allow-runs`, and
`--allow-agent`, with the agent working directory set to the instance root.

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
