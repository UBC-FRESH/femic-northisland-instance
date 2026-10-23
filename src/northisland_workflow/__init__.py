"""FreshForge provider for the North Island ws4 model-build workflow.

The provider wraps ws4's command-line build, validation, simulation, and reporting
surfaces. It keeps the workflow document declarative while every model-producing
step remains an inspectable command with a resolved artifact path.

FreshForge is an optional development dependency. Import this module only through
the ``freshforge.providers`` entry point, or call :func:`provider_factory` from a
process where FreshForge is installed.
"""

from __future__ import annotations

import subprocess
import sys
from collections.abc import Callable
from dataclasses import dataclass
from pathlib import Path
from typing import Any

PROVIDER_ID = "northisland.ws4"
PROVIDER_VERSION = "0.2.0"

CommandRunner = Callable[[tuple[str, ...], Path], subprocess.CompletedProcess[str]]


@dataclass(frozen=True)
class _NodeContract:
    """Declarative contract for one provider node type."""

    id: str
    name: str
    description: str
    inputs: tuple[str, ...] = ()
    outputs: tuple[str, ...] = ()
    parameters: tuple[str, ...] = ()
    artifacts: tuple[str, ...] = ()


_NODE_CONTRACTS: tuple[_NodeContract, ...] = (
    _NodeContract(
        id="post_tipsy",
        name="Build post-TIPSY model-input bundle",
        description="Run FEMIC Stage 01b and assemble the public model-input bundle.",
        inputs=("compiled_upstream",),
        outputs=("model_input_bundle",),
        parameters=("instance_root", "run_config", "tsa", "run_id"),
        artifacts=("manifest",),
    ),
    _NodeContract(
        id="build_dataset",
        name="Build ws4 dataset",
        description="Compile a ForestModel XML recipe and fragment inventory into a ws4 matrix.",
        outputs=("dataset",),
        parameters=("instance_root", "xml", "fragments", "out"),
        artifacts=("manifest",),
    ),
    _NodeContract(
        id="validate_dataset",
        name="Validate ws4 dataset",
        description="Validate a compiled ws4 dataset against its manifest and schema invariants.",
        inputs=("dataset",),
        outputs=("validated_dataset",),
        parameters=("instance_root", "dataset"),
    ),
    _NodeContract(
        id="build_baseline_schedule",
        name="Build baseline schedule",
        description=(
            "Build a deterministic clearcut-at-target-age schedule from the dataset blocks."
        ),
        inputs=("validated_dataset",),
        outputs=("schedule",),
        parameters=("instance_root", "dataset", "out", "target_age", "retention_config"),
        artifacts=("schedule", "summary"),
    ),
    _NodeContract(
        id="simulate",
        name="Simulate ws4 schedule",
        description="Replay a schedule over the compiled dataset and write a run directory.",
        inputs=("schedule",),
        outputs=("run",),
        parameters=("instance_root", "dataset", "schedule", "out", "years"),
        artifacts=("run",),
    ),
    _NodeContract(
        id="report",
        name="Report ws4 run",
        description="Write the account summary and target status for a simulated run.",
        inputs=("run",),
        outputs=("report",),
        parameters=("instance_root", "run", "targets"),
        artifacts=("summary", "targets"),
    ),
    _NodeContract(
        id="prepare_ui",
        name="Prepare ws4 UI assets",
        description=(
            "Dissolve the fragment geometry to block features and write a web-ready GeoJSON."
        ),
        inputs=("run",),
        outputs=("ui_assets",),
        parameters=("instance_root", "fragments", "out"),
        artifacts=("geometry",),
    ),
)


class NorthIslandWs4Provider:
    """FreshForge provider for the North Island ws4 workflow."""

    def __init__(self, command_runner: CommandRunner | None = None) -> None:
        self._command_runner = command_runner or _default_command_runner

    def metadata(self) -> Any:
        """Return FreshForge provider metadata."""
        return _provider_metadata()

    def validate_node(self, node: Any, node_type: Any, *, location: str) -> tuple[Any, ...]:
        """Validate one node's declared inputs, outputs, parameters, and artifacts."""
        return _validate_contract_node(node, node_type, location=location)

    def run_node(self, node: Any, node_type: Any, *, context: Any) -> Any:
        """Execute one ws4 workflow node and return provider-owned outputs."""
        builders = _command_builders()
        builder = builders.get(str(node_type.id))
        result_type, run_status = _freshforge_run_result_types()
        diagnostic, severity = _freshforge_diagnostic_types()
        if builder is None:
            return result_type(
                status=run_status.FAILED,
                diagnostics=(
                    diagnostic(
                        severity=severity.ERROR,
                        code="northisland.ws4.execution.unsupported",
                        message=f"No execution hook for node type '{node_type.id}'.",
                        location=f"nodes.{node.id}",
                    ),
                ),
            )
        try:
            command, cwd = builder(node)
        except ValueError as exc:
            return result_type(
                status=run_status.FAILED,
                diagnostics=(
                    diagnostic(
                        severity=severity.ERROR,
                        code="northisland.ws4.parameters.invalid",
                        message=str(exc),
                        location=f"nodes.{node.id}.parameters",
                    ),
                ),
            )

        completed = self._command_runner(command, cwd)
        data: dict[str, Any] = {
            "command": list(command),
            "cwd": str(cwd),
            "returncode": completed.returncode,
        }
        if completed.stdout:
            data["stdout"] = completed.stdout
        if completed.stderr:
            data["stderr"] = completed.stderr
        diagnostics: tuple[Any, ...] = ()
        if completed.returncode != 0:
            diagnostics = (
                diagnostic(
                    severity=severity.ERROR,
                    code="northisland.ws4.command.failed",
                    message=(
                        f"ws4 command for node '{node.id}' exited with "
                        f"return code {completed.returncode}."
                    ),
                    location=f"nodes.{node.id}",
                ),
            )
        outputs = node.outputs if isinstance(node.outputs, dict) else {}
        return result_type(
            status=run_status.SUCCESS if completed.returncode == 0 else run_status.FAILED,
            outputs=outputs,
            artifacts=_resolved_artifacts(node, cwd),
            diagnostics=diagnostics,
            data=data,
        )


def provider_factory() -> NorthIslandWs4Provider:
    """Return the provider instance for FreshForge entry-point discovery."""
    return NorthIslandWs4Provider()


def _provider_metadata() -> Any:
    node_type_metadata, provider_metadata = _freshforge_metadata_types()
    return provider_metadata(
        id=PROVIDER_ID,
        version=PROVIDER_VERSION,
        name="North Island ws4 provider",
        description=(
            "Instance-owned FreshForge nodes for the North Island ws4 build, "
            "baseline simulation, reporting, and UI asset preparation."
        ),
        node_types=tuple(
            node_type_metadata(
                id=contract.id,
                name=contract.name,
                description=contract.description,
                inputs=contract.inputs,
                outputs=contract.outputs,
                parameters=contract.parameters,
                artifacts=contract.artifacts,
            )
            for contract in _NODE_CONTRACTS
        ),
    )


def _validate_contract_node(node: Any, node_type: Any, *, location: str) -> tuple[Any, ...]:
    diagnostic, severity = _freshforge_diagnostic_types()
    diagnostics: list[Any] = []
    diagnostics.extend(
        _missing_key_diagnostics(
            diagnostic=diagnostic,
            severity=severity,
            required=tuple(node_type.inputs),
            actual=node.inputs,
            field_name="inputs",
            location=location,
        )
    )
    diagnostics.extend(
        _missing_key_diagnostics(
            diagnostic=diagnostic,
            severity=severity,
            required=tuple(node_type.outputs),
            actual=node.outputs,
            field_name="outputs",
            location=location,
        )
    )
    diagnostics.extend(
        _missing_key_diagnostics(
            diagnostic=diagnostic,
            severity=severity,
            required=tuple(node_type.parameters),
            actual=node.parameters,
            field_name="parameters",
            location=location,
        )
    )
    artifacts = node.artifacts if isinstance(node.artifacts, dict) else {}
    diagnostics.extend(
        _missing_key_diagnostics(
            diagnostic=diagnostic,
            severity=severity,
            required=tuple(node_type.artifacts),
            actual=artifacts,
            field_name="artifacts",
            location=location,
        )
    )
    diagnostics.extend(
        _empty_parameter_diagnostics(
            diagnostic=diagnostic,
            severity=severity,
            parameters=node.parameters,
            required=tuple(node_type.parameters),
            location=location,
        )
    )
    return tuple(diagnostics)


def _command_builders() -> dict[str, Callable[[Any], tuple[tuple[str, ...], Path]]]:
    return {
        "post_tipsy": _build_post_tipsy_command,
        "build_dataset": _build_dataset_command,
        "validate_dataset": _build_validate_command,
        "build_baseline_schedule": _build_schedule_command,
        "simulate": _build_simulate_command,
        "report": _build_report_command,
        "prepare_ui": _build_prepare_ui_command,
    }


def _build_post_tipsy_command(node: Any) -> tuple[tuple[str, ...], Path]:
    command = list(
        _python(
            "-m",
            "femic",
            "tsa",
            "post-tipsy",
            "--instance-root",
            _parameter(node, "instance_root"),
            "--run-config",
            _parameter(node, "run_config"),
            "--tsa",
            _parameter(node, "tsa"),
            "--run-id",
            _parameter(node, "run_id"),
        )
    )
    return tuple(command), _instance_root(node)


def _build_dataset_command(node: Any) -> tuple[tuple[str, ...], Path]:
    return (
        _python(
            "-m",
            "ws4.cli",
            "build",
            "--xml",
            _parameter(node, "xml"),
            "--fragments",
            _parameter(node, "fragments"),
            "--out",
            _parameter(node, "out"),
        ),
        _instance_root(node),
    )


def _build_validate_command(node: Any) -> tuple[tuple[str, ...], Path]:
    return (
        _python(
            "-m",
            "ws4.cli",
            "validate",
            "--dataset",
            _parameter(node, "dataset"),
        ),
        _instance_root(node),
    )


def _build_schedule_command(node: Any) -> tuple[tuple[str, ...], Path]:
    command = [
        *_python(
            "scripts/build_baseline_schedule.py",
            "--dataset",
            _parameter(node, "dataset"),
            "--out",
            _parameter(node, "out"),
            "--target-age",
            _parameter(node, "target_age"),
        )
    ]
    _append_option(command, node, "retention_config", "--retention-config")
    return tuple(command), _instance_root(node)


def _build_simulate_command(node: Any) -> tuple[tuple[str, ...], Path]:
    command = [
        *_python(
            "-m",
            "ws4.cli",
            "simulate",
            "--dataset",
            _parameter(node, "dataset"),
            "--schedule",
            _parameter(node, "schedule"),
            "--out",
            _parameter(node, "out"),
            "--years",
            _parameter(node, "years"),
        )
    ]
    _append_option(command, node, "topology", "--topology")
    return tuple(command), _instance_root(node)


def _build_report_command(node: Any) -> tuple[tuple[str, ...], Path]:
    command = [
        *_python(
            "-m",
            "ws4.cli",
            "report",
            "--run",
            _parameter(node, "run"),
        )
    ]
    _append_option(command, node, "targets", "--targets")
    return tuple(command), _instance_root(node)


def _build_prepare_ui_command(node: Any) -> tuple[tuple[str, ...], Path]:
    return (
        _python(
            "scripts/prepare_ws4_ui.py",
            "--fragments",
            _parameter(node, "fragments"),
            "--out",
            _parameter(node, "out"),
        ),
        _instance_root(node),
    )


def _python(*args: str) -> tuple[str, ...]:
    return (sys.executable, *args)


def _instance_root(node: Any) -> Path:
    return Path(_parameter(node, "instance_root")).resolve()


def _parameter(node: Any, key: str) -> str:
    value = node.parameters.get(key)
    if value is None:
        raise ValueError(f"ws4 node '{node.id}' requires parameter '{key}'.")
    if isinstance(value, str):
        if not value.strip():
            raise ValueError(f"ws4 node '{node.id}' parameter '{key}' must be nonempty.")
        return value
    return str(value)


def _optional_parameter(node: Any, key: str) -> str | None:
    value = node.parameters.get(key)
    if value is None:
        return None
    if isinstance(value, str):
        return value if value.strip() else None
    return str(value)


def _append_option(command: list[str], node: Any, key: str, option: str) -> None:
    value = _optional_parameter(node, key)
    if value is not None:
        command.extend([option, value])


def _default_command_runner(
    command: tuple[str, ...], cwd: Path
) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        list(command),
        cwd=cwd,
        check=False,
        capture_output=True,
        text=True,
    )


def _resolved_artifacts(node: Any, root: Path) -> dict[str, Any]:
    artifacts = node.artifacts if isinstance(node.artifacts, dict) else {}
    resolved: dict[str, Any] = {}
    for key, value in artifacts.items():
        if isinstance(value, (str, Path)):
            path = Path(value)
            resolved[key] = str(path if path.is_absolute() else root / path)
        else:
            resolved[key] = value
    return resolved


def _missing_key_diagnostics(
    *,
    diagnostic: Any,
    severity: Any,
    required: tuple[str, ...],
    actual: dict[str, Any],
    field_name: str,
    location: str,
) -> tuple[Any, ...]:
    return tuple(
        diagnostic(
            severity=severity.ERROR,
            code=f"northisland.ws4.{field_name}.missing",
            message=f"ws4 node requires {field_name} key '{key}'.",
            location=f"{location}.{field_name}.{key}",
        )
        for key in required
        if key not in actual
    )


def _empty_parameter_diagnostics(
    *,
    diagnostic: Any,
    severity: Any,
    parameters: dict[str, Any],
    required: tuple[str, ...],
    location: str,
) -> tuple[Any, ...]:
    diagnostics: list[Any] = []
    for key in required:
        value = parameters.get(key)
        if isinstance(value, str) and not value.strip():
            diagnostics.append(
                diagnostic(
                    severity=severity.ERROR,
                    code="northisland.ws4.parameters.empty",
                    message=f"ws4 node parameter '{key}' must be nonempty.",
                    location=f"{location}.parameters.{key}",
                )
            )
    return tuple(diagnostics)


def _freshforge_metadata_types() -> tuple[Any, Any]:
    from freshforge.providers import NodeTypeMetadata, ProviderMetadata

    return NodeTypeMetadata, ProviderMetadata


def _freshforge_diagnostic_types() -> tuple[Any, Any]:
    from freshforge.records import Diagnostic, DiagnosticSeverity

    return Diagnostic, DiagnosticSeverity


def _freshforge_run_result_types() -> tuple[Any, Any]:
    from freshforge.records import ProviderRunResult, RunStatus

    return ProviderRunResult, RunStatus
