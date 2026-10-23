#!/usr/bin/env python3
"""Build a deterministic baseline harvest schedule from a ws4 dataset.

Every eligible block is harvested once with the declared treatment when it
reaches the target age. The schedule is driven by the 0-based treatment
``offset``: offset 0 is the first simulation year, and a block already at or
beyond the target age is entered at offset 0. Period 0 is the zero-length
pre-simulation snapshot and is never a treatment slot.

The baseline also supports a retention policy. Blocks whose compilation
features belong to a retained AU are removed from the harvest schedule and
remain in the dataset as retained/unmanaged stands.
"""

from __future__ import annotations

import argparse
import json
from collections.abc import Sequence
from pathlib import Path

import pandas as pd


def load_retention_aus(path: Path) -> tuple[str, ...]:
    """Read the retained AU labels from a retention JSON file.

    Parameters
    ----------
    path : pathlib.Path
        JSON object with a ``retain_aus`` list of model AU labels.

    Returns
    -------
    tuple of str
        Unique retained AU labels in file order.
    """
    payload = json.loads(path.read_text(encoding="utf-8"))
    raw_aus = payload.get("retain_aus")
    if not isinstance(raw_aus, list):
        raise ValueError(f"{path} must contain a 'retain_aus' list")
    aus = tuple(dict.fromkeys(str(value).strip() for value in raw_aus if str(value).strip()))
    if not aus:
        raise ValueError(f"{path} must name at least one retained AU")
    return aus


def _retained_block_ids(
    *,
    dataset: Path,
    retain_aus: Sequence[str],
) -> set[int]:
    """Return block ids with at least one feature in a retained AU.

    Parameters
    ----------
    dataset : pathlib.Path
        Compiled ws4 dataset directory with ``features.parquet`` and
        ``fragments.parquet``.
    retain_aus : sequence of str
        Model AU labels such as ``CWH_CW_L``.

    Returns
    -------
    set of int
        Blocks to remove from the harvest schedule.
    """
    if not retain_aus:
        return set()

    features = pd.read_parquet(dataset / "features.parquet")
    fragments = pd.read_parquet(dataset / "fragments.parquet")
    required_features = {"track_id", "label"}
    required_fragments = {"track_id", "block_id"}
    if not required_features.issubset(features.columns):
        raise ValueError("features.parquet is missing track_id or label")
    if not required_fragments.issubset(fragments.columns):
        raise ValueError("fragments.parquet is missing track_id or block_id")

    mask = features["label"].str.startswith("feature.Area.og1.") & ~features["label"].str.endswith(
        ".total"
    )
    au_rows = features.loc[mask, ["track_id", "label"]].copy()
    if au_rows.empty:
        raise ValueError("features.parquet has no feature.Area.og1 AU labels")
    au_rows["au_label"] = au_rows["label"].str.replace("feature.Area.og1.", "", regex=False)
    au_by_track = au_rows.drop_duplicates("track_id").set_index("track_id")["au_label"]
    known_aus = set(au_by_track.unique())
    unknown = set(retain_aus) - known_aus
    if unknown:
        raise ValueError(f"unknown retained AU labels: {sorted(unknown)}")

    fragment_aus = fragments.loc[:, ["track_id", "block_id"]].copy()
    fragment_aus["au_label"] = fragment_aus["track_id"].map(au_by_track)
    retained = fragment_aus[fragment_aus["au_label"].isin(retain_aus)]
    if retained.empty:
        raise ValueError("no blocks matched the retained AU labels")
    return set(retained["block_id"].astype(int))


def build_schedule(
    *,
    dataset: Path,
    target_age: int,
    treatment: str,
    retain_aus: Sequence[str] = (),
) -> tuple[pd.DataFrame, dict[str, object]]:
    """Return a block schedule and a compact summary.

    Parameters
    ----------
    dataset : pathlib.Path
        Compiled ws4 dataset directory containing ``blocks.parquet`` and the
        feature/fragment tables used by the retention filter.
    target_age : int
        Age in years at which each eligible block is harvested.
    treatment : str
        Treatment code to apply, normally ``CC``.
    retain_aus : sequence of str, optional
        Model AU labels to remove from the harvest schedule.

    Returns
    -------
    tuple of (pandas.DataFrame, dict)
        The schedule with ``block_id``, ``treatment``, and ``offset`` columns,
        and a JSON-ready summary.
    """
    blocks = pd.read_parquet(dataset / "blocks.parquet")
    required = {"block_id", "offset", "area_ha"}
    missing = required.difference(blocks.columns)
    if missing:
        raise ValueError(f"blocks.parquet is missing columns: {sorted(missing)}")
    if target_age <= 0:
        raise ValueError("target_age must be positive")

    grouped = (
        blocks.groupby("block_id", as_index=False)
        .agg(offset=("offset", "min"), area_ha=("area_ha", "sum"))
        .sort_values("block_id")
    )
    source_block_count = len(grouped)
    source_area_ha = float(grouped["area_ha"].sum())
    retained_blocks = _retained_block_ids(
        dataset=dataset,
        retain_aus=retain_aus,
    )
    retained = grouped[grouped["block_id"].astype(int).isin(retained_blocks)]
    if retained_blocks:
        grouped = grouped[~grouped["block_id"].astype(int).isin(retained_blocks)]
    grouped["offset"] = (target_age - grouped["offset"]).clip(lower=0).astype(int)
    grouped["treatment"] = treatment
    schedule = grouped.loc[:, ["block_id", "treatment", "offset"]].copy()
    schedule["block_id"] = schedule["block_id"].astype(int)

    summary: dict[str, object] = {
        "dataset": str(dataset),
        "target_age": target_age,
        "treatment": treatment,
        "retain_aus": list(dict.fromkeys(retain_aus)),
        "source_block_count": source_block_count,
        "block_count": len(schedule),
        "retained_block_count": len(retained),
        "source_area_ha": round(source_area_ha, 4),
        "area_ha": round(float(grouped["area_ha"].sum()), 4),
        "retained_area_ha": round(float(retained["area_ha"].sum()), 4),
        "offset_min": int(schedule["offset"].min()) if len(schedule) else None,
        "offset_max": int(schedule["offset"].max()) if len(schedule) else None,
    }
    return schedule, summary


def main() -> None:
    """Write the baseline schedule and its summary."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--dataset", type=Path, required=True)
    parser.add_argument("--out", type=Path, required=True)
    parser.add_argument("--target-age", type=int, default=60)
    parser.add_argument("--treatment", default="CC")
    parser.add_argument(
        "--retention-config",
        type=Path,
        help="Optional JSON retention policy with a retain_aus list.",
    )
    parser.add_argument(
        "--retain-au",
        action="append",
        default=[],
        dest="retain_aus",
        help="Model AU label to retain; repeat for multiple AUs.",
    )
    args = parser.parse_args()
    retain_aus = list(args.retain_aus)
    if args.retention_config is not None:
        retain_aus.extend(load_retention_aus(args.retention_config))
    schedule, summary = build_schedule(
        dataset=args.dataset,
        target_age=args.target_age,
        treatment=args.treatment,
        retain_aus=tuple(dict.fromkeys(retain_aus)),
    )
    args.out.parent.mkdir(parents=True, exist_ok=True)
    schedule.to_csv(args.out, index=False)
    summary_path = args.out.with_suffix(".summary.json")
    summary_path.write_text(
        json.dumps(summary, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    print(json.dumps(summary, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
