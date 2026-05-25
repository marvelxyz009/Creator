"""Backward-compat shim for the early Milestone 1 implementation.

The real implementation now lives in `orchestrator.workflows.manual_mode`,
which handles all 5 scene-generation agents through a single registry-driven
driver. This module re-exports the scene-director-specific API used by the
older tests in `test_scene_director_manual.py`.

New code should call `manual_mode.prepare_agent_prompt` and
`manual_mode.validate_agent_output` directly.
"""

from __future__ import annotations

from pathlib import Path

from orchestrator.core.config import Config
from orchestrator.workflows.manual_mode import (
    AGENT_SPECS,
    PrepareResult,
    ValidateResult,
    prepare_agent_prompt,
    print_prepare_summary,
    print_validate_summary,
    validate_agent_output,
)

# Re-exports for test back-compat (old tests import these names).
__all__ = [
    "PrepareResult",
    "ValidateResult",
    "prepare_scene_director",
    "validate_scene_director_output",
    "print_prepare_summary",
    "print_validate_summary",
]


def prepare_scene_director(sample_dir: Path, config: Config) -> PrepareResult:
    """Compat wrapper: prepare-agent for scene-director only."""
    return prepare_agent_prompt(
        agent_id="scene-director",
        sample_dir=sample_dir,
        config=config,
        prior_outputs={},   # scene-director has no priors
    )


def validate_scene_director_output(
    sample_dir: Path, input_path: Path, config: Config
) -> ValidateResult:
    """Compat wrapper: validate-agent-output for scene-director only."""
    return validate_agent_output(
        agent_id="scene-director",
        sample_dir=sample_dir,
        input_path=input_path,
        config=config,
    )
