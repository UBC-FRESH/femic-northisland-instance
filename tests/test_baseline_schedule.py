"""Tests for the deterministic baseline schedule builder."""

from __future__ import annotations

import json
import sys
from pathlib import Path

import pandas as pd
import pytest

from build_baseline_schedule import build_schedule, load_retention_aus, main


def test_build_schedule_uses_age_offsets(tmp_path: Path) -> None:
    """A block reaches the target age after the difference in years."""
    dataset = tmp_path / "dataset"
    dataset.mkdir()
    pd.DataFrame(
        {
            "block_id": [1, 1, 2],
            "track_id": [10, 11, 12],
            "offset": [20, 20, 80],
            "area_ha": [5.0, 2.0, 9.0],
        }
    ).to_parquet(dataset / "blocks.parquet", index=False)

    schedule, summary = build_schedule(
        dataset=dataset,
        target_age=60,
        treatment="CC",
    )

    assert schedule.to_dict("records") == [
        {"block_id": 1, "treatment": "CC", "offset": 40},
        {"block_id": 2, "treatment": "CC", "offset": 0},
    ]
    assert summary["block_count"] == 2
    assert summary["area_ha"] == 16.0
    assert summary["offset_min"] == 0
    assert summary["offset_max"] == 40


def test_build_schedule_rejects_missing_columns(tmp_path: Path) -> None:
    """A dataset without the required block and age columns is rejected."""
    dataset = tmp_path / "dataset"
    dataset.mkdir()
    pd.DataFrame({"block_id": [1]}).to_parquet(dataset / "blocks.parquet", index=False)

    with pytest.raises(ValueError, match="missing columns"):
        build_schedule(dataset=dataset, target_age=60, treatment="CC")


def test_build_schedule_rejects_non_positive_target_age(tmp_path: Path) -> None:
    """The target age must be positive."""
    dataset = tmp_path / "dataset"
    dataset.mkdir()
    pd.DataFrame(
        {
            "block_id": [1],
            "track_id": [10],
            "offset": [0],
            "area_ha": [1.0],
        }
    ).to_parquet(dataset / "blocks.parquet", index=False)

    with pytest.raises(ValueError, match="target_age"):
        build_schedule(dataset=dataset, target_age=0, treatment="CC")


def _write_retention_dataset(dataset: Path) -> None:
    """Write a tiny dataset with two retained AUs and one harvestable AU."""
    dataset.mkdir()
    pd.DataFrame(
        {
            "block_id": [1, 2, 3],
            "track_id": [10, 11, 12],
            "offset": [0, 20, 0],
            "area_ha": [5.0, 7.0, 3.0],
        }
    ).to_parquet(dataset / "blocks.parquet", index=False)
    pd.DataFrame(
        {
            "track_id": [10, 11, 12],
            "label": [
                "feature.Area.og1.CWH_CW_L",
                "feature.Area.og1.CWH_HW_L",
                "feature.Area.og1.CWH_YC_L",
            ],
            "curve_id": [1, 2, 3],
        }
    ).to_parquet(dataset / "features.parquet", index=False)
    pd.DataFrame(
        {
            "fragment_id": [1, 2, 3],
            "block_id": [1, 2, 3],
            "track_id": [10, 11, 12],
            "area_ha": [5.0, 7.0, 3.0],
            "age": [100, 40, 100],
        }
    ).to_parquet(dataset / "fragments.parquet", index=False)


def test_load_retention_aus_reads_json(tmp_path: Path) -> None:
    """The retention policy is read from the documented JSON shape."""
    path = tmp_path / "retention.json"
    path.write_text(json.dumps({"retain_aus": ["CWH_CW_L", "CWH_YC_L"]}))

    assert load_retention_aus(path) == ("CWH_CW_L", "CWH_YC_L")


def test_load_retention_aus_rejects_empty_policy(tmp_path: Path) -> None:
    """A retention policy without AUs is a blocking input error."""
    path = tmp_path / "retention.json"
    path.write_text(json.dumps({"retain_aus": []}))

    with pytest.raises(ValueError, match="at least one"):
        load_retention_aus(path)


def test_build_schedule_removes_retained_au_blocks(tmp_path: Path) -> None:
    """Blocks in retained AUs leave the harvest schedule."""
    dataset = tmp_path / "dataset"
    _write_retention_dataset(dataset)

    schedule, summary = build_schedule(
        dataset=dataset,
        target_age=60,
        treatment="CC",
        retain_aus=("CWH_CW_L", "CWH_YC_L"),
    )

    assert schedule.to_dict("records") == [{"block_id": 2, "treatment": "CC", "offset": 40}]
    assert summary["source_block_count"] == 3
    assert summary["block_count"] == 1
    assert summary["retained_block_count"] == 2
    assert summary["retained_area_ha"] == 8.0
    assert summary["area_ha"] == 7.0


def test_build_schedule_rejects_unknown_retained_au(tmp_path: Path) -> None:
    """An AU label that does not exist in the dataset is rejected."""
    dataset = tmp_path / "dataset"
    _write_retention_dataset(dataset)

    with pytest.raises(ValueError, match="unknown retained AU"):
        build_schedule(
            dataset=dataset,
            target_age=60,
            treatment="CC",
            retain_aus=("CWH_CW_H",),
        )


def test_main_writes_retention_schedule(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    """The CLI wires the retention policy into the written schedule."""
    dataset = tmp_path / "dataset"
    _write_retention_dataset(dataset)
    policy = tmp_path / "retention.json"
    policy.write_text(json.dumps({"retain_aus": ["CWH_CW_L", "CWH_YC_L"]}))
    out = tmp_path / "schedule.csv"
    monkeypatch.setattr(
        sys,
        "argv",
        [
            "build_baseline_schedule.py",
            "--dataset",
            str(dataset),
            "--out",
            str(out),
            "--retention-config",
            str(policy),
        ],
    )

    main()

    schedule = pd.read_csv(out)
    assert schedule["block_id"].tolist() == [2]
    summary = json.loads(out.with_suffix(".summary.json").read_text())
    assert summary["retained_block_count"] == 2
