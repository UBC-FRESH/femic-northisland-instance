"""Tests for the North Island AOI builder."""

from __future__ import annotations

from pathlib import Path

import geopandas as gpd
import pytest
from shapely.geometry import box

from build_aoi import build_aoi, write_aoi


def _frame(geometry: list[object], crs: str = "EPSG:3005") -> gpd.GeoDataFrame:
    return gpd.GeoDataFrame(
        {"name": [f"f{i}" for i in range(len(geometry))]}, geometry=geometry, crs=crs
    )


def test_build_aoi_clips_to_district_and_adds_cfa() -> None:
    """The AOI is the TSA/district intersection plus an adjacent CFA."""
    tsa = _frame([box(0, 0, 1000, 1000)])
    district = _frame([box(0, 0, 1000, 500)])
    cfa = _frame([box(1000, 0, 1200, 200)])

    aoi = build_aoi(tsa, district, cfa)

    assert len(aoi) == 1
    assert aoi.crs is not None
    assert aoi["cfa_count"].iloc[0] == 1
    assert aoi["area_ha"].iloc[0] == pytest.approx(54.0, rel=0.01)
    assert aoi.total_bounds[2] == 1200


def test_build_aoi_ignores_distant_cfa() -> None:
    """A CFA that does not touch the clipped TSA is not added."""
    tsa = _frame([box(0, 0, 1000, 1000)])
    district = _frame([box(0, 0, 1000, 500)])
    cfa = _frame([box(2000, 0, 2200, 200)])

    aoi = build_aoi(tsa, district, cfa)

    assert aoi["cfa_count"].iloc[0] == 0
    assert aoi.total_bounds[2] == 1000


def test_build_aoi_rejects_empty_inputs() -> None:
    """An empty TSA is a blocking input error."""
    with pytest.raises(ValueError, match="tsa"):
        build_aoi(_frame([]), _frame([box(0, 0, 100, 100)]), _frame([box(0, 0, 100, 100)]))


def test_write_aoi_round_trips(tmp_path: Path) -> None:
    """The written GeoPackage has the named layer and summary fields."""
    aoi = _frame([box(0, 0, 1000, 500)])
    aoi["aoi_name"] = "northisland"
    aoi["cfa_count"] = 1
    aoi["area_ha"] = 50.0
    out = tmp_path / "aoi.gpkg"

    summary = write_aoi(aoi, out)

    assert out.is_file()
    assert summary["layer"] == "northisland_aoi"
    assert summary["area_ha"] == 50.0
    assert summary["cfa_count"] == 1
