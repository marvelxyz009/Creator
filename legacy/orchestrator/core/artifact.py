"""Artifact IO: read and write YAML/Markdown artifacts.

Artifacts are the framework's IPC format. Every agent input and output is a
YAML or Markdown file. This module is the only place the orchestrator touches
the filesystem for artifact reads/writes.
"""

from __future__ import annotations

import logging
from pathlib import Path
from typing import Any

import yaml

logger = logging.getLogger(__name__)


# ─── Read ─────────────────────────────────────────────────────────────────────

def read_yaml(path: Path) -> dict[str, Any]:
    """Load a YAML file into a dict. Raises FileNotFoundError if missing."""
    if not path.exists():
        raise FileNotFoundError(f"Artifact not found: {path}")
    with path.open("r", encoding="utf-8") as fh:
        data = yaml.safe_load(fh)
    if data is None:
        return {}
    if not isinstance(data, dict):
        raise ValueError(f"Expected YAML dict at top level: {path} (got {type(data).__name__})")
    return data


def read_markdown(path: Path) -> str:
    """Load a Markdown file as a string."""
    if not path.exists():
        raise FileNotFoundError(f"Markdown artifact not found: {path}")
    return path.read_text(encoding="utf-8")


def read_optional_yaml(path: Path) -> dict[str, Any] | None:
    """Read a YAML file if it exists; return None otherwise. Use sparingly."""
    if not path.exists():
        return None
    return read_yaml(path)


# ─── Write ────────────────────────────────────────────────────────────────────

def write_yaml(path: Path, data: dict[str, Any]) -> None:
    """Write a dict as YAML to `path`. Creates parent dirs."""
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as fh:
        yaml.safe_dump(
            data,
            fh,
            sort_keys=False,
            allow_unicode=True,
            default_flow_style=False,
            indent=2,
        )
    logger.debug("Wrote YAML artifact: %s", path)


def write_markdown(path: Path, content: str) -> None:
    """Write a string as Markdown to `path`. Creates parent dirs."""
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")
    logger.debug("Wrote Markdown artifact: %s", path)


# ─── Sample inspection (used by `inspect-sample` CLI) ─────────────────────────

def inspect_sample(sample_dir: Path) -> int:
    """Print a sample's tree and check for required inputs. Returns CLI exit code."""
    if not sample_dir.exists():
        print(f"ERROR: sample directory does not exist: {sample_dir}")
        return 1

    print(f"Sample: {sample_dir}")
    inputs_dir = sample_dir / "inputs"
    outputs_dir = sample_dir / "outputs"

    print(f"  inputs/  : {'exists' if inputs_dir.exists() else 'MISSING'}")
    if inputs_dir.exists():
        for entry in sorted(inputs_dir.rglob("*")):
            if entry.is_file():
                print(f"    {entry.relative_to(sample_dir)}")

    print(f"  outputs/ : {'exists' if outputs_dir.exists() else '(none — fresh sample)'}")
    if outputs_dir.exists():
        for entry in sorted(outputs_dir.rglob("*")):
            if entry.is_file():
                print(f"    {entry.relative_to(sample_dir)}")

    return 0 if inputs_dir.exists() else 1
