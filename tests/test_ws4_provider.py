"""Tests for the instance-owned FreshForge provider command contracts."""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

import pytest

from northisland_workflow import (
    NorthIslandWs4Provider,
    _build_dataset_command,
    _build_post_tipsy_command,
    _build_simulate_command,
    provider_factory,
)


@dataclass
class _FakeNode:
    id: str
    parameters: dict[str, Any]
    inputs: dict[str, Any] = field(default_factory=dict)
    outputs: dict[str, Any] = field(default_factory=dict)
    artifacts: dict[str, Any] = field(default_factory=dict)


def test_build_dataset_command_resolves_instance_root(tmp_path: Path) -> None:
    """The build command runs from the instance root and names the recipe inputs."""
    node = _FakeNode(
        id="build",
        parameters={
            "instance_root": str(tmp_path),
            "xml": "output/forestmodel.xml",
            "fragments": "output/fragments.shp",
            "out": "runtime/matrix",
        },
    )

    command, cwd = _build_dataset_command(node)

    assert cwd == tmp_path
    assert command[1:4] == ("-m", "ws4.cli", "build")
    assert command[-6:] == (
        "--xml",
        "output/forestmodel.xml",
        "--fragments",
        "output/fragments.shp",
        "--out",
        "runtime/matrix",
    )


def test_simulate_command_includes_optional_topology(tmp_path: Path) -> None:
    """Topology is passed only when the workflow declares it."""
    node = _FakeNode(
        id="simulate",
        parameters={
            "instance_root": str(tmp_path),
            "dataset": "runtime/matrix",
            "schedule": "runtime/schedule.csv",
            "out": "runtime/baseline",
            "years": 100,
            "topology": "runtime/topology.csv",
        },
    )

    command, cwd = _build_simulate_command(node)

    assert cwd == tmp_path
    assert command[-2:] == ("--topology", "runtime/topology.csv")
    assert "--years" in command
    assert "100" in command


def test_post_tipsy_command_uses_the_instance_run_config(tmp_path: Path) -> None:
    """The post-TIPSY node calls the FEMIC seam in the instance working directory."""
    node = _FakeNode(
        id="post_tipsy",
        parameters={
            "instance_root": str(tmp_path),
            "run_config": "config/run_profile.northisland.yaml",
            "tsa": "48",
            "run_id": "northisland_20261021",
        },
    )

    command, cwd = _build_post_tipsy_command(node)

    assert cwd == tmp_path
    assert command[1:5] == ("-m", "femic", "tsa", "post-tipsy")
    assert "--tsa" in command
    assert "48" in command


def test_provider_factory_returns_provider() -> None:
    """The entry point returns the provider class."""
    assert isinstance(provider_factory(), NorthIslandWs4Provider)


def test_missing_parameter_is_reported() -> None:
    """A missing required parameter fails before a command is built."""
    node = _FakeNode(id="build", parameters={"instance_root": "."})
    with pytest.raises(ValueError, match="requires parameter 'xml'"):
        _build_dataset_command(node)
