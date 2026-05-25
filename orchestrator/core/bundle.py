"""Context bundles: tailored inputs an agent receives for a single invocation.

Mirrors prompts/shared/context-contract.md. The orchestrator's contract with
every agent is: starvation by default, inclusion must be justified. This
module assembles bundles per agent contract.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import Any


@dataclass
class Bundle:
    """A typed context bundle for a single agent invocation.

    Mirrors the YAML structure described in prompts/shared/context-contract.md.
    Serializable to YAML for inclusion in run reports.
    """

    for_agent: str
    task_id: str
    pinned_artifacts: dict[str, Any] = field(default_factory=dict)
    """Map of artifact-ref → loaded data (or only-the-fields-this-agent-needs)."""

    graph_queries: list[dict[str, Any]] = field(default_factory=list)
    """List of {description, result} entries. Result is computed against memory graph."""

    recent_canon: list[dict[str, Any]] = field(default_factory=list)
    """Per-scene voice-continuity windows: {scene, window, content}."""

    constraints: dict[str, Any] = field(default_factory=dict)
    """Constraints the agent must honor: {rules: [R1, ...], additional: '...'}"""

    revision_directive: str | None = None
    """Set only on re-runs. Supersedes default behavior for this invocation."""

    budget_tokens: int = 6000

    def to_dict(self) -> dict[str, Any]:
        """Return a YAML-serializable dict."""
        return {
            "for_agent": self.for_agent,
            "task_id": self.task_id,
            "budget_tokens": self.budget_tokens,
            "pinned_artifacts": self.pinned_artifacts,
            "graph_queries": self.graph_queries,
            "recent_canon": self.recent_canon,
            "constraints": self.constraints,
            "revision_directive": self.revision_directive,
        }


class BundleAssembler:
    """Builds Bundles for specific agent invocations.

    Each agent's prompt template lists `required_inputs` and `graph_queries` in
    its frontmatter / structure. The assembler reads those declarations and
    builds a Bundle that satisfies them — pinning only the named fields, not
    the whole artifact.

    MVP scope: the assembler hard-codes input rules per agent. A future version
    will parse the prompt template's structured frontmatter to drive assembly
    automatically.
    """

    def __init__(self, sample_dir: Path):
        self.sample_dir = sample_dir

    def assemble_for_scene_director(self, task_id: str) -> Bundle:
        """Assemble the bundle for [scene-director] from samples/<sample>/inputs/."""
        from orchestrator.core.artifact import read_yaml

        inputs = self.sample_dir / "inputs"
        return Bundle(
            for_agent="scene-director",
            task_id=task_id,
            pinned_artifacts={
                "theme.yaml": read_yaml(inputs / "theme.yaml"),
                "world.yaml": read_yaml(inputs / "world.yaml"),
                "characters/mira.yaml": read_yaml(inputs / "characters" / "mira.yaml"),
                "characters/tomas.yaml": read_yaml(inputs / "characters" / "tomas.yaml"),
                "plot_beat.yaml": read_yaml(inputs / "plot_beat.yaml"),
                "memory_graph_excerpt.yaml": read_yaml(inputs / "memory_graph_excerpt.yaml"),
            },
            constraints={
                "rules": ["R1", "R2", "R3", "R4", "R5", "R6", "R7"],
                "additional": "Honor scene-schema invariants: turn, theme_touch, residue.graph_writes required.",
            },
            budget_tokens=8000,
        )

    def assemble_for_symbolism_tracker(
        self, task_id: str, scene_blueprint: dict[str, Any]
    ) -> Bundle:
        """Assemble bundle for [symbolism-tracker] (audit mode)."""
        from orchestrator.core.artifact import read_yaml

        inputs = self.sample_dir / "inputs"
        return Bundle(
            for_agent="symbolism-tracker",
            task_id=task_id,
            pinned_artifacts={
                "theme.yaml": read_yaml(inputs / "theme.yaml"),
                "scene_blueprint": scene_blueprint,
                "memory_graph_excerpt.yaml": read_yaml(inputs / "memory_graph_excerpt.yaml"),
            },
            constraints={"rules": ["R6"]},
            budget_tokens=4000,
        )

    def assemble_for_dialogue_specialist(
        self, task_id: str, scene_blueprint: dict[str, Any]
    ) -> Bundle:
        """Assemble bundle for [dialogue-specialist]."""
        from orchestrator.core.artifact import read_yaml

        inputs = self.sample_dir / "inputs"
        return Bundle(
            for_agent="dialogue-specialist",
            task_id=task_id,
            pinned_artifacts={
                "scene_blueprint": scene_blueprint,
                "characters/mira.yaml": read_yaml(inputs / "characters" / "mira.yaml"),
                "characters/tomas.yaml": read_yaml(inputs / "characters" / "tomas.yaml"),
                "memory_graph_excerpt.yaml": read_yaml(inputs / "memory_graph_excerpt.yaml"),
            },
            constraints={"rules": ["R1", "R3", "R4", "R5", "R7", "R8"]},
            budget_tokens=6000,
        )

    def assemble_for_anti_ai_editor(
        self, task_id: str, draft: str, scene_blueprint: dict[str, Any]
    ) -> Bundle:
        """Assemble bundle for [anti-ai-editor]."""
        from orchestrator.core.artifact import read_yaml

        inputs = self.sample_dir / "inputs"
        return Bundle(
            for_agent="anti-ai-editor",
            task_id=task_id,
            pinned_artifacts={
                "draft_under_edit": draft,
                "scene_blueprint": scene_blueprint,
                "characters/mira.yaml": read_yaml(inputs / "characters" / "mira.yaml"),
                "characters/tomas.yaml": read_yaml(inputs / "characters" / "tomas.yaml"),
            },
            constraints={"rules": ["R1", "R8", "R9", "R10"]},
            budget_tokens=8000,
        )

    def assemble_for_continuity_auditor(
        self, task_id: str, draft: str, scene_blueprint: dict[str, Any]
    ) -> Bundle:
        """Assemble bundle for [continuity-auditor]."""
        from orchestrator.core.artifact import read_yaml

        inputs = self.sample_dir / "inputs"
        return Bundle(
            for_agent="continuity-auditor",
            task_id=task_id,
            pinned_artifacts={
                "draft_under_audit": draft,
                "scene_blueprint": scene_blueprint,
                "memory_graph_snapshot": read_yaml(inputs / "memory_graph_excerpt.yaml"),
            },
            constraints={"rules": ["R5"]},
            budget_tokens=4000,
        )
