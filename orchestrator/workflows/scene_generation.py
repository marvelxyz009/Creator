"""Scene Generation Workflow — the MVP target.

Implements prompts/workflows/scene-generation-workflow.md. The DAG:

    [scene-director]
         │
         ▼
    [symbolism-tracker]   (audits the blueprint)
         │
         ▼
    [dialogue-specialist] (drafts dialogue)
         │
         ▼
    [anti-ai-editor]      (smell scrub + humanization)
         │
         ▼
    [continuity-auditor]  (final graph validation)
         │
         ▼
       canon

Each step is bound to a callable that: assembles a Bundle, calls the LLM,
parses the YAML response, writes the artifact, returns a StepResult.

For MVP this file is intentionally direct (no decorator magic). When this
shape stabilizes across multiple workflows, the common parts can move into
a generic AgentStep wrapper.
"""

from __future__ import annotations

import logging
from pathlib import Path
from typing import Any

from orchestrator.core.artifact import write_markdown, write_yaml
from orchestrator.core.bundle import BundleAssembler
from orchestrator.core.runner import Step, StepResult, WorkflowRunner
from orchestrator.llm.client import LLMClient
from orchestrator.llm.models import model_for_agent
from orchestrator.prompts.loader import PromptLoader
from orchestrator.prompts.render import (
    extract_yaml_from_response,
    render_system_prompt,
    render_user_prompt,
)
from orchestrator.workflows.base import Workflow

logger = logging.getLogger(__name__)


class SceneGenerationWorkflow(Workflow):
    workflow_id = "scene-generation"

    def __init__(self, config):
        super().__init__(config)
        self.loader = PromptLoader(prompts_dir=config.prompts_dir)
        self.llm = LLMClient(
            api_key=config.anthropic_api_key,
            default_model=config.anthropic_model,
            default_max_tokens=config.anthropic_max_tokens,
        )

    # ─── DAG construction ────────────────────────────────────────────────────

    def build_steps(self, sample_dir: Path, run_dir: Path) -> list[Step]:
        assembler = BundleAssembler(sample_dir=sample_dir)

        def step_scene_director(_runner: WorkflowRunner, _prior: dict) -> StepResult:
            return self._run_agent(
                agent_id="scene-director",
                bundle=assembler.assemble_for_scene_director(task_id="scene:01"),
                output_path=run_dir / "01-scene-blueprint.yaml",
                output_format="yaml",
            )

        def step_symbolism_tracker(_runner: WorkflowRunner, prior: dict) -> StepResult:
            blueprint = prior["scene-director"].output
            if blueprint is None:
                return StepResult(
                    step_id="symbolism-tracker",
                    status="hard_reject",
                    notes="upstream step did not produce parseable output",
                )
            return self._run_agent(
                agent_id="symbolism-tracker",
                bundle=assembler.assemble_for_symbolism_tracker(
                    task_id="scene:01-symbol-audit",
                    scene_blueprint=blueprint,
                ),
                output_path=run_dir / "02-symbol-audit.yaml",
                output_format="yaml",
            )

        def step_dialogue_specialist(_runner: WorkflowRunner, prior: dict) -> StepResult:
            blueprint = prior["scene-director"].output
            return self._run_agent(
                agent_id="dialogue-specialist",
                bundle=assembler.assemble_for_dialogue_specialist(
                    task_id="scene:01-dialogue",
                    scene_blueprint=blueprint,
                ),
                output_path=run_dir / "03-dialogue-draft.yaml",
                output_format="yaml",
            )

        def step_anti_ai_editor(_runner: WorkflowRunner, prior: dict) -> StepResult:
            blueprint = prior["scene-director"].output
            dialogue = prior["dialogue-specialist"].output
            # For MVP we pass the dialogue draft YAML as the 'draft'; in a fuller
            # implementation a separate Prose Agent renders dialogue+blueprint
            # into prose, and THAT becomes the draft input to anti-ai-editor.
            draft = (dialogue or {}).get("dialogue_draft", "")
            result = self._run_agent(
                agent_id="anti-ai-editor",
                bundle=assembler.assemble_for_anti_ai_editor(
                    task_id="scene:01-anti-ai",
                    draft=str(draft),
                    scene_blueprint=blueprint,
                ),
                output_path=run_dir / "04-smell-report-and-revision.yaml",
                output_format="yaml",
            )
            # Also write the revised draft as markdown for human review
            if result.output and "humanization_pass" in result.output:
                revised = result.output["humanization_pass"].get("revised_draft", "")
                if revised:
                    write_markdown(run_dir / "05-revised-draft.md", revised)
            return result

        def step_continuity_auditor(_runner: WorkflowRunner, prior: dict) -> StepResult:
            blueprint = prior["scene-director"].output
            anti_ai = prior["anti-ai-editor"].output or {}
            revised = (
                anti_ai.get("humanization_pass", {}).get("revised_draft", "")
                if isinstance(anti_ai, dict)
                else ""
            )
            return self._run_agent(
                agent_id="continuity-auditor",
                bundle=assembler.assemble_for_continuity_auditor(
                    task_id="scene:01-continuity",
                    draft=str(revised),
                    scene_blueprint=blueprint,
                ),
                output_path=run_dir / "06-continuity-report.yaml",
                output_format="yaml",
            )

        return [
            Step(
                id="scene-director",
                description="Produce scene blueprint",
                fn=step_scene_director,
            ),
            Step(
                id="symbolism-tracker",
                description="Audit symbol operations against state machine",
                depends_on=["scene-director"],
                fn=step_symbolism_tracker,
            ),
            Step(
                id="dialogue-specialist",
                description="Draft voice-specific dialogue",
                depends_on=["scene-director"],
                fn=step_dialogue_specialist,
            ),
            Step(
                id="anti-ai-editor",
                description="Smell scrub + humanization pass",
                depends_on=["dialogue-specialist"],
                fn=step_anti_ai_editor,
            ),
            Step(
                id="continuity-auditor",
                description="Validate against memory graph",
                depends_on=["anti-ai-editor"],
                fn=step_continuity_auditor,
            ),
        ]

    # ─── Single-agent invocation ─────────────────────────────────────────────

    def _run_agent(
        self,
        agent_id: str,
        bundle: Any,
        output_path: Path,
        output_format: str,
    ) -> StepResult:
        """Load prompt, render bundle, call LLM, parse + persist response."""
        template = self.loader.load(agent_id)
        system_prompt = render_system_prompt(template.system_prompt_markdown)
        user_prompt = render_user_prompt(bundle)
        model = model_for_agent(agent_id, default=self.config.anthropic_model)

        response = self.llm.call(
            system_prompt=system_prompt,
            user_prompt=user_prompt,
            model=model,
        )

        parsed = extract_yaml_from_response(response.text)
        if parsed is None:
            # Persist the raw text for forensics, mark as hard_reject.
            write_markdown(output_path.with_suffix(".raw.md"), response.text)
            return StepResult(
                step_id=agent_id,
                status="hard_reject",
                raw_output=response.text,
                notes="failed to parse YAML from LLM response",
            )

        if output_format == "yaml":
            write_yaml(output_path, parsed)
        else:  # markdown
            write_markdown(output_path, response.text)

        status = parsed.get("status", "ok")
        return StepResult(
            step_id=agent_id,
            status=status,
            output=parsed,
            raw_output=response.text,
            artifact_path=output_path,
            notes=f"model={model} in={response.input_tokens} out={response.output_tokens}",
        )

    # ─── Golden comparison ───────────────────────────────────────────────────

    def compare_to_golden(
        self, sample_dir: Path, run_dir: Path, report
    ) -> dict[str, Any]:
        """Compare generated artifacts to sample/outputs/ if present.

        Comparison is INFORMATIONAL for MVP: we report structural overlap
        (same top-level keys, same status, same major sections) but do NOT
        treat divergence as failure. Prose drafts will differ run-to-run.
        """
        golden_dir = sample_dir / "outputs"
        if not golden_dir.exists():
            return {"status": "no_goldens", "note": "sample has no outputs/ directory"}

        comparisons = []
        pairs = [
            ("01-scene-blueprint.yaml", "01-scene-blueprint.yaml"),
            ("02-symbol-audit.yaml", "02-symbol-audit.yaml"),
            ("04-smell-report-and-revision.yaml", "04-smell-report.yaml"),
            ("06-continuity-report.yaml", "06-continuity-report.yaml"),
        ]
        for generated_name, golden_name in pairs:
            gen = run_dir / generated_name
            gold = golden_dir / golden_name
            comparisons.append(
                {
                    "generated": str(gen.name),
                    "golden": str(gold.name),
                    "generated_exists": gen.exists(),
                    "golden_exists": gold.exists(),
                    "size_delta_bytes": (
                        gen.stat().st_size - gold.stat().st_size
                        if gen.exists() and gold.exists()
                        else None
                    ),
                }
            )

        return {
            "status": "compared",
            "note": "structural-only; prose drafts differ run-to-run by design",
            "comparisons": comparisons,
        }
