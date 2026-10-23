#!/usr/bin/env python
"""Write the North Island AOI polygon as the web map's non-forest underlay.

The block layer covers forest only. Drawing the gross AOI beneath it keeps the gaps in the
inventory (non-forest, water, roads) from reading as missing map data.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path

import geopandas as gpd


def main() -> None:
    """Write the AOI polygon as a GeoJSON underlay.

    Returns
    -------
    None
        The GeoJSON is written to the requested output path.
    """
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--aoi", type=Path, required=True, help="AOI polygon (GPKG or SHP)")
    parser.add_argument("--out", type=Path, required=True, help="Output GeoJSON")
    args = parser.parse_args()

    frame = gpd.read_file(args.aoi)
    if frame.empty:
        raise SystemExit(f"{args.aoi} has no features")
    frame = frame[["geometry"]].copy()
    args.out.parent.mkdir(parents=True, exist_ok=True)
    frame.to_file(args.out, driver="GeoJSON")
    document = json.loads(args.out.read_text(encoding="utf-8"))
    print(
        json.dumps(
            {
                "out": str(args.out),
                "features": len(document.get("features", [])),
                "crs": str(frame.crs),
                "bytes": args.out.stat().st_size,
            }
        )
    )


if __name__ == "__main__":
    main()
