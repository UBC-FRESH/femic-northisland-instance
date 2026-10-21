#!/usr/bin/env python3
"""Build the North Island model AOI from public BC boundary layers.

The Basecamp email thread defines the AOI as the part of TSA 48 that lies in
the North Island - Central Coast Natural Resource District, plus the community
forest agreement (CFA). The script clips the TSA to the district, adds any
active CFA polygons that touch the result, and writes one reviewed GeoPackage.

The ArcGIS REST sources are public. The output is a small tracked boundary
artifact, so a rebuild does not require a network connection after the first
run.
"""

from __future__ import annotations

import argparse
import io
import json
from pathlib import Path
from typing import Any

import geopandas as gpd
import requests
from shapely.geometry import mapping, shape

TSA_QUERY = (
    "https://maps.gov.bc.ca/arcgis/rest/services/whse/"
    "bcgw_pub_whse_admin_boundaries/MapServer/78/query"
)
DISTRICT_QUERY = (
    "https://maps.gov.bc.ca/arcgis/rest/services/whse/"
    "bcgw_pub_whse_admin_boundaries/MapServer/58/query"
)
TENURE_QUERY = (
    "https://maps.gov.bc.ca/arcgis/rest/services/whse/bcgw_pub_whse_forest_tenure/MapServer/8/query"
)


def fetch_geojson(url: str, params: dict[str, str]) -> gpd.GeoDataFrame:
    """Fetch an ArcGIS REST query as a GeoDataFrame in EPSG:3005.

    Parameters
    ----------
    url : str
        ArcGIS REST query endpoint.
    params : dict of str to str
        Query parameters. The function forces GeoJSON, geometry, and EPSG:3005.

    Returns
    -------
    geopandas.GeoDataFrame
        The returned features with their attributes.
    """
    query = {**params, "returnGeometry": "true", "outSR": "3005", "f": "geojson"}
    response = requests.get(url, params=query, timeout=180)
    response.raise_for_status()
    frame = gpd.read_file(io.StringIO(response.text))
    return frame.set_crs("EPSG:3005", allow_override=True)


def build_aoi(
    tsa: gpd.GeoDataFrame,
    district: gpd.GeoDataFrame,
    tenure: gpd.GeoDataFrame,
) -> gpd.GeoDataFrame:
    """Clip the TSA to the district and add intersecting community forests.

    Parameters
    ----------
    tsa : geopandas.GeoDataFrame
        TSA polygon or polygons. The caller filters to TSA 48.
    district : geopandas.GeoDataFrame
        Natural resource district polygon or polygons.
    tenure : geopandas.GeoDataFrame
        Community forest agreement polygons to add back.

    Returns
    -------
    geopandas.GeoDataFrame
        One dissolved AOI polygon with source counts and area in hectares.

    Raises
    ------
    ValueError
        When an input is empty or the intersection is empty.
    """
    for name, frame in (("tsa", tsa), ("district", district), ("tenure", tenure)):
        if frame.empty:
            raise ValueError(f"{name} input is empty")
    clipped = gpd.overlay(tsa, district, how="intersection", keep_geom_type=True)
    if clipped.empty:
        raise ValueError("TSA and district do not intersect")
    geometry = clipped.geometry.union_all()
    touching = tenure[tenure.intersects(geometry)]
    if not touching.empty:
        geometry = geometry.union(touching.geometry.union_all())
    return gpd.GeoDataFrame(
        {
            "aoi_name": ["northisland"],
            "tsa_count": [len(tsa)],
            "district_count": [len(district)],
            "cfa_count": [len(touching)],
            "area_ha": [round(float(geometry.area) / 10000.0, 2)],
            "geometry": [shape(mapping(geometry))],
        },
        crs="EPSG:3005",
    )


def write_aoi(aoi: gpd.GeoDataFrame, out: Path) -> dict[str, Any]:
    """Write the AOI GeoPackage and return a JSON-ready summary.

    Parameters
    ----------
    aoi : geopandas.GeoDataFrame
        One-row AOI frame from :func:`build_aoi`.
    out : Path
        Destination GeoPackage path.

    Returns
    -------
    dict
        Summary with the destination, layer name, area, and bounds.
    """
    out.parent.mkdir(parents=True, exist_ok=True)
    layer = "northisland_aoi"
    aoi.to_file(out, layer=layer, driver="GPKG")
    bounds = [round(float(value), 3) for value in aoi.total_bounds]
    return {
        "path": str(out),
        "layer": layer,
        "crs": "EPSG:3005",
        "area_ha": float(aoi["area_ha"].iloc[0]),
        "cfa_count": int(aoi["cfa_count"].iloc[0]),
        "bounds": bounds,
    }


def main() -> None:
    """Fetch the public layers, build the AOI, and write the tracked artifact."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--out",
        type=Path,
        default=Path("data/source/aoi/northisland_aoi.gpkg"),
    )
    args = parser.parse_args()

    tsa = fetch_geojson(TSA_QUERY, {"where": "TSA_NUMBER='48'", "outFields": "*"})
    district = fetch_geojson(
        DISTRICT_QUERY,
        {"where": "ORG_UNIT='DNI'", "outFields": "*"},
    )
    tenure = fetch_geojson(
        TENURE_QUERY,
        {
            "where": "FOREST_FILE_ID LIKE 'K%' AND LIFE_CYCLE_STATUS_CODE='ACTIVE'",
            "outFields": "*",
        },
    )
    aoi = build_aoi(tsa, district, tenure)
    summary = write_aoi(aoi, args.out)
    summary_path = args.out.with_suffix(".summary.json")
    summary_path.write_text(
        json.dumps(summary, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    print(json.dumps(summary, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
