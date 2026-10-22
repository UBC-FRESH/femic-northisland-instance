# TSR metadata extraction and TIPSY mapping

## Documents

| Cycle | Document | Source |
| --- | --- | --- |
| TSR_2020 | North Island TSA Timber Supply Review Data Package | BC TSR FTP |
| TSR_2022 | North Island TSA Discussion Paper | BC TSR assets |
| TSR_2024 | AAC Rationale for North Island TSA | BC TSR assets |

The FEMIC TSR workflow (`index`, `fetch`, `extract`) produced 413 candidate facts
for TSA 48:

| Fact family | Count |
| --- | ---: |
| `au_definition_candidate` | 5 |
| `source_layer_candidate` | 71 |
| `thlb_reference` | 254 |
| `tipsy_input_candidate` | 80 |
| `document_metadata` | 3 |

The canonical discovery artifacts stay under the FEMIC checkout. The reviewed
instance surface is `config/tsr/`.

## Full THLB net-down ladder

The reviewed backbone is the 2020 data package Table 4, page 25. The 2022
Discussion Paper Table 5 updates some values. The full ladder is transcribed in
`config/tsr/thlb_netdown.recipe.yaml`.

| Stage | Factor | Unique area excluded (ha) |
| --- | --- | ---: |
| GLB | North Island TSA boundary area | 2,426,749 |
| GLB -> AFLB | Ocean | 677,289 |
| GLB -> AFLB | Non-provincial lands | 244,982 |
| GLB -> AFLB | Not managed within TSA AAC | 789,755 |
| AFLB | Section 8 Decision Area | 714,726 |
| AFLB -> LHLB | Non-forest | 184,783 |
| AFLB -> LHLB | Roads, trails, landings | 7,386 |
| AFLB | Analysis forest land base (AFLB) | 522,557 |
| AFLB -> LHLB | Provincial parks & reserves | 137,685 |
| AFLB -> LHLB | Recreation sites | 8,067 |
| AFLB -> LHLB | Recreation trails | 33 |
| LHLB -> THLB | Inoperable | 72,256 |
| LHLB -> THLB | Terrain stability | 38,715 |
| LHLB -> THLB | Sites with low growing potential | 58,401 |
| LHLB -> THLB | Problem forest types | 249 |
| LHLB -> THLB | Landscape-level biodiversity - OGMA | 13,996 |
| LHLB -> THLB | Stand-level biodiversity - WTRA | 759 |
| LHLB -> THLB | Wildlife habitat areas | 1,568 |
| LHLB -> THLB | Ungulate winter range | 314 |
| LHLB -> THLB | Riparian reserves & management areas | 9,155 |
| LHLB -> THLB | Archaeological sites | 1,892 |
| LHLB -> THLB | PSP & research installations | 708 |
| LHLB -> THLB | Karst | 1,254 |
| THLB | Current timber harvesting land base | 177,505 |
| Future | Future WTRA | 9,609 |
| Future | Future roads | TBD |

The 2022 Discussion Paper Table 5 reports the same ladder with updated values
for terrain stability, low growing potential, problem forest types, OGMA,
WTRA, WHA, UWR, riparian, archaeological, PSP, and karst. The rationale's final
determination adjusts the harvest level rather than the land-base ladder.

## TIPSY AU-wise parameters

The data package documents the managed-stand method on pages 61-64:

- model: BatchTipsy Composer version 5.0 (Dec 20, 2019)
- site index: Provincial Site Productivity Layer v7.0, SIBEC-based
- tree improvement: area-weighted genetic worth from RESULTS/SPAR
- OAF 1: standard 15% reduction
- OAF 2: standard 5%; increased to 12.5% for existing and future managed
  Douglas-fir in `CWHmm1`, `xm1`, and `xm2`
- regeneration: RESULTS opening-level planted and natural species composition,
  density, genetic worth, planting delay, and planted percent
- future managed stands: species composition from BEC zone/subzone, site index
  from PSPL by species

The TSR also cites `TIPSY input table - tsa48_tipsy_input` on page 69. That
table is **not in the public PDF**, not in the TSR FTP directory, and not in the
BC Data Catalogue. The exact per-AU species/density workbook is therefore a
published-data blocker.

The reviewed mapping in `config/tsr/tipsy_au_mapping.csv` combines:

- TSR-sourced constants: OAF1 15%, OAF2 5% or 12.5%, genetic worth Cw 4.33,
  Fd 7.63, Hw 5.20, Ss 2.00, one-year regeneration delay, merchantability
  DBH 12.5/17.5 cm, top DIB 10/15 cm, stump 30 cm, slab 10/15 cm cedar;
- model-sourced per-AU values: species mix, density 1200, and site index from
  the FEMIC VDYP/PSPL run.

`config/tipsy/northisland.yaml` now carries one rule per model AU
(`source_managed_local_au_id` 21000-23003) plus a fallback.

## Evidence

- `config/tsr/overlay.yaml`
- `config/tsr/source_layers.recipe.yaml`
- `config/tsr/thlb_netdown.recipe.yaml`
- `config/tsr/tipsy_au_mapping.csv`
- `config/tipsy/northisland.yaml`

## Blocker

The exact `tsa48_tipsy_input` workbook is not published with the TSR package.
Until it is supplied, per-AU species composition and density remain
model-derived, while the TSR constants are adopted. Accepted BatchTIPSY output
is still required before the managed-curve lane is production-ready.
