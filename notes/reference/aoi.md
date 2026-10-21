# North Island AOI

Status: accepted for the first model build
Source: Basecamp FRST 558 inbox forward, "North Island Timber Supply Area", 2026-10-21
Original sender: Ione (ibhecate@gmail.com)

## Decision

The model AOI is:

> the North Island (formerly Vancouver Island portion of the Kingcome TSA), now
> the portion of the NI TSA that is found within the District of North Island -
> Central Coast (only on Vancouver Island) ... clip the area to the NICC District
> (and add back in the CFA).

Operational rule:

1. Start with TSA 48, the North Island Timber Supply Area.
2. Clip to the North Island - Central Coast Natural Resource District (`ORG_UNIT = DNI`).
3. Add back the community forest agreement polygons that touch the clipped area.

The email also supplied the 2020 TSR data package and a 2024 determination PDF.
Those documents are context, not geometry inputs.

## Public geometry sources

| Layer | Source | Selection |
| --- | --- | --- |
| TSA | BCGW `WHSE_ADMIN_BOUNDARIES.FADM_TSA`, ArcGIS REST layer 78 | `TSA_NUMBER = '48'` |
| District | BCGW `WHSE_ADMIN_BOUNDARIES` Natural Resource Districts, ArcGIS REST layer 58 | `ORG_UNIT = 'DNI'` |
| Community forest | BCGW `WHSE_FOREST_TENURE.FTEN_MANAGED_LICENCE_POLY_SVW`, ArcGIS REST layer 8 | active `K*` file that intersects the clipped TSA |
| Data warehouse reference | <https://www.arcgis.com/home/item.html?id=b3fdfae29f304708b084c2cff9db7cd9> | TSA view supplied in the thread |

`scripts/build_aoi.py` implements the rule. The tracked artifact is
`data/source/aoi/northisland_aoi.gpkg`, layer `northisland_aoi`, EPSG:3005.

## Review checkpoints

| Check | Value |
| --- | --- |
| TSA 48 gross area | 2,441,910.93 ha |
| NICC district gross area | 7,499,969.72 ha |
| TSA 48 inside NICC | 1,083,003.66 ha |
| Community forest polygons touching the result | 3 (K3Z, 2,391.51 ha) |
| Final AOI area | 1,083,003.66 ha |
| Final AOI bounds (EPSG:3005) | 740950.574, 542039.840, 988579.684, 688552.175 |

The community forest is already inside the TSA/NICC intersection, so adding it
does not change the dissolved area. It is still unioned into the boundary so a
future TSA revision cannot silently drop it.

## Open review point

The original email says "add back in the CFA" without naming the file. The
public tenure layer returns only K3Z, the North Island Community Forest, as an
active community forest touching the clipped TSA. The attached overview map
labels the black North Island TSA boundary, the red NICC district boundary, and
the dark-gray Section 8 decision area, but it does not label the CFA. Treat K3Z
as the CFA until the sender or a more detailed tenure map confirms a different
file.
