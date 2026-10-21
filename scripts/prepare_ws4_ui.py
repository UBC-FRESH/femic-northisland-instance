#!/usr/bin/env python3
"""Prepare block geometry for the ws4 web UI from FEMIC fragment geometry.

FEMIC exports one polygon per fragment. The ws4 dataset keys its schedule by
block, so the UI geometry is dissolved to one feature per block and carries a
``block_id`` field that matches ``blocks.parquet``.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path

import geopandas as gpd


def _block_column(frame: gpd.GeoDataFrame) -> str:
    for candidate in ("BLOCK", "block", "block_id", "BLOCK_ID"):
        if candidate in frame.columns:
            return candidate
    raise ValueError("fragment geometry needs one of BLOCK, block, block_id, or BLOCK_ID")


def prepare_ui_geometry(
    *,
    fragments: Path,
    out: Path,
) -> dict[str, object]:
    """Dissolve fragment geometry to blocks and write a GeoJSON file.

    Parameters
    ----------
    fragments : Path
        Fragment shapefile or GeoPackage exported by FEMIC.
    out : Path
        Destination GeoJSON path.

    Returns
    -------
    dict
        A JSON-ready summary with the source, block count, and CRS.
    """
    frame = gpd.read_file(fragments)
    if frame.empty:
        raise ValueError(f"fragment geometry is empty: {fragments}")
    block_column = _block_column(frame)
    frame[block_column] = frame[block_column].astype(int)
    blocks = frame[[block_column, "geometry"]].dissolve(by=block_column).reset_index()
    blocks = blocks.rename(columns={block_column: "block_id"})
    blocks["block_id"] = blocks["block_id"].astype(int)
    out.parent.mkdir(parents=True, exist_ok=True)
    blocks.to_file(out, driver="GeoJSON")
    return {
        "source": str(fragments),
        "out": str(out),
        "block_count": len(blocks),
        "crs": str(frame.crs) if frame.crs is not None else None,
    }


def main() -> None:
    """Write the UI geometry and print its summary."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--fragments", type=Path, required=True)
    parser.add_argument("--out", type=Path, required=True)
    args = parser.parse_args()
    summary = prepare_ui_geometry(fragments=args.fragments, out=args.out)
    print(json.dumps(summary, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
