"""Interactive Manual Workflow Runner — chains all 5 scene-generation agents.

End-to-end flow with one CLI command:

    python -m orchestrator create-scene --sample <path>

Walks through scene-director → symbolism-tracker → dialogue-specialist →
anti-ai-editor → continuity-auditor. For each agent:

  1. Hydrates the manual prompt and writes it to disk.
  2. Prints clear instructions: where to find the prompt, where to save the
     reply, exactly what to run next.
  3. Waits for the human to press Enter (after they've copied the prompt into
     Claude in their IDE and saved the reply to the expected path).
  4. Validates the saved reply, writes canonical artifact, moves to next agent.
  5. On validation failure: offers retry / skip / quit.

After all 5 agents complete successfully, prints the path to the prose draft
(the "story" output) and a directory map of every canonical artifact written.

No LLM calls anywhere in this module. The human carries the messages between
Claude (in the IDE) and the orchestrator.
"""

from __future__ import annotations

import logging
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

from orchestrator.core.config import Config
from orchestrator.workflows.manual_mode import (
    AGENT_SPECS,
    PrepareResult,
    ValidateResult,
    prepare_agent_prompt,
    validate_agent_output,
)

logger = logging.getLogger("orchestrator.manual_workflow")


# The canonical execution order for the scene-generation workflow.
SCENE_GENERATION_ORDER: tuple[str, ...] = (
    "scene-director",
    "symbolism-tracker",
    "dialogue-specialist",
    "anti-ai-editor",
    "continuity-auditor",
)


@dataclass
class WorkflowResult:
    ok: bool
    sample_dir: Path
    agents_completed: list[str] = field(default_factory=list)
    agents_skipped: list[str] = field(default_factory=list)
    final_prose_path: Path | None = None
    aborted_at: str | None = None
    notes: str = ""


def _rel(path: Path, root: Path) -> str:
    try:
        return str(path.relative_to(root)).replace("\\", "/")
    except ValueError:
        return str(path)


def _hr(char: str = "─", width: int = 70) -> str:
    return char * width


def _banner(title: str, char: str = "=", width: int = 70) -> str:
    return f"{char * width}\n{title}\n{char * width}"


# ─── User interaction helpers ────────────────────────────────────────────────

def _prompt_continue() -> bool:
    """Ask the user to press Enter to validate. Returns True to continue,
    False to abort. Empty input = continue. 'q'/'quit' = abort."""
    try:
        reply = input("  Press Enter when ready to validate, or 'q' to quit: ").strip().lower()
    except (EOFError, KeyboardInterrupt):
        print()
        return False
    return reply not in {"q", "quit", "exit"}


def _prompt_after_failure() -> str:
    """Returns one of: 'retry', 'skip', 'quit'."""
    print()
    print("  Options:")
    print("    [r]etry — edit the output file and validate again")
    print("    [s]kip  — continue to the next agent (debug only)")
    print("    [q]uit  — abort the workflow")
    while True:
        try:
            choice = input("  Choice [r/s/q]: ").strip().lower()
        except (EOFError, KeyboardInterrupt):
            print()
            return "quit"
        if choice in {"r", "retry", ""}:
            return "retry"
        if choice in {"s", "skip"}:
            return "skip"
        if choice in {"q", "quit", "exit"}:
            return "quit"
        print(f"  Unrecognized choice {choice!r}. Try r / s / q.")


# ─── Per-agent step ──────────────────────────────────────────────────────────

def _print_prepare_block(
    agent_id: str,
    step_num: int,
    total: int,
    prep: PrepareResult,
    repo_root: Path,
) -> None:
    spec = AGENT_SPECS[agent_id]
    print()
    print(f"[{step_num}/{total}] {agent_id}")
    print(_hr())
    print(f"  Role: {spec.description}")
    print()
    if prep.prompt_path:
        print(f"  Hydrated prompt written to:")
        print(f"    {_rel(prep.prompt_path, repo_root)}")
    print()
    print("  → Open Claude (extension in VSCode/Cursor, or any LLM chat)")
    print("  → Open the prompt file above")
    print(f"  → Copy everything below the line `--- BEGIN PROMPT ---`")
    print("  → Paste into Claude as a new conversation")
    print("  → Save Claude's full reply to:")
    if prep.expected_output_path:
        print(f"    {_rel(prep.expected_output_path, repo_root)}")
    print()


def _validate_with_retry(
    agent_id: str,
    sample_dir: Path,
    input_path: Path,
    config: Config,
) -> tuple[ValidateResult, str]:
    """Validate, and on failure interactively offer retry/skip/quit.

    Returns (final_result, action_chosen). action_chosen ∈ {"ok", "skip", "quit"}.
    """
    while True:
        result = validate_agent_output(
            agent_id=agent_id,
            sample_dir=sample_dir,
            input_path=input_path,
            config=config,
        )
        if result.ok:
            return result, "ok"

        # Print diagnostics.
        print()
        print(f"  ✗ Validation failed for {agent_id}: {result.notes}")
        if result.validation_violations:
            for v in result.validation_violations:
                print(f"      - {v}")

        action = _prompt_after_failure()
        if action == "retry":
            print(f"  Edit {_rel(input_path, sample_dir.parent.parent)} and press Enter to re-validate.")
            try:
                input("  Press Enter to re-validate: ")
            except (EOFError, KeyboardInterrupt):
                print()
                return result, "quit"
            continue
        return result, action


# ─── Main entry point ────────────────────────────────────────────────────────

def run_scene_generation_manual(sample_dir: Path, config: Config) -> WorkflowResult:
    """Walk through the 5 scene-generation agents interactively.

    The function blocks on `input()` after each `prepare-agent` step, waiting
    for the human to copy-paste through Claude and save the reply. This is
    intentional — the workflow is human-in-the-loop by design.
    """
    sample_dir = sample_dir.resolve()
    if not (sample_dir / "inputs").exists():
        return WorkflowResult(
            ok=False,
            sample_dir=sample_dir,
            notes=f"Sample missing inputs/: {sample_dir}",
        )

    result = WorkflowResult(ok=True, sample_dir=sample_dir)
    total = len(SCENE_GENERATION_ORDER)

    print(_banner("Manual Scene Generation Workflow"))
    print(f"Sample : {_rel(sample_dir, config.repo_root)}")
    print(f"Output : {_rel(sample_dir / 'generated', config.repo_root)}/")
    print(f"Agents : {' → '.join(SCENE_GENERATION_ORDER)}")
    print(_banner("", char="="))

    # Carry each agent's parsed output in memory so we don't depend on
    # round-tripping to disk for the chain (though disk is also written).
    prior_outputs: dict[str, dict[str, Any]] = {}

    for i, agent_id in enumerate(SCENE_GENERATION_ORDER, start=1):
        # ─ Phase 1: prepare ───────────────────────────────────────────────────
        try:
            prep = prepare_agent_prompt(
                agent_id=agent_id,
                sample_dir=sample_dir,
                config=config,
                prior_outputs={a: prior_outputs[a] for a in AGENT_SPECS[agent_id].prior_agents_needed},
            )
        except Exception as exc:
            logger.exception("prepare failed")
            print(f"\n  ✗ Prepare failed for {agent_id}: {exc}")
            result.ok = False
            result.aborted_at = agent_id
            result.notes = f"prepare raised: {exc}"
            return result

        _print_prepare_block(agent_id, i, total, prep, config.repo_root)

        if not _prompt_continue():
            result.ok = False
            result.aborted_at = agent_id
            result.notes = "user quit during prepare phase"
            print()
            print(_banner("Workflow aborted by user"))
            return result

        # ─ Phase 2: validate ──────────────────────────────────────────────────
        val, action = _validate_with_retry(
            agent_id=agent_id,
            sample_dir=sample_dir,
            input_path=prep.expected_output_path,  # type: ignore[arg-type]
            config=config,
        )

        if action == "quit":
            result.ok = False
            result.aborted_at = agent_id
            result.notes = "user quit during validate phase"
            print()
            print(_banner("Workflow aborted by user"))
            return result

        if action == "skip":
            print(f"  ⚠ Skipping {agent_id} (output not canonized; downstream may fail).")
            result.agents_skipped.append(agent_id)
            # We don't add to prior_outputs because we have nothing valid.
            # Downstream agents that depend on this will hit a hard error.
            continue

        # action == "ok"
        if val.output is not None:
            prior_outputs[agent_id] = val.output
        result.agents_completed.append(agent_id)

        print()
        print(f"  ✓ {agent_id} canonized: {_rel(val.artifact_path, config.repo_root) if val.artifact_path else '?'}")
        for label, path in val.extra_artifacts.items():
            print(f"    + {label}: {_rel(path, config.repo_root)}")

    # ─ Final report ───────────────────────────────────────────────────────────
    prose_path = sample_dir / "generated" / "05-revised-draft.md"
    if prose_path.exists():
        result.final_prose_path = prose_path

    print()
    print(_banner("Scene generation complete"))
    print()
    print(f"Agents completed: {len(result.agents_completed)}/{total}")
    for a in result.agents_completed:
        print(f"  ✓ {a}")
    if result.agents_skipped:
        print(f"Agents skipped  : {len(result.agents_skipped)}")
        for a in result.agents_skipped:
            print(f"  ⚠ {a}")

    print()
    print("Canonical artifacts (under samples/<sample>/generated/):")
    generated_dir = sample_dir / "generated"
    for filename in (
        "01-scene-blueprint.yaml",
        "02-symbol-audit.yaml",
        "03-dialogue-draft.yaml",
        "04-anti-ai-report.yaml",
        "05-revised-draft.md",
        "06-continuity-report.yaml",
    ):
        path = generated_dir / filename
        marker = "✓" if path.exists() else "·"
        label = ""
        if filename == "05-revised-draft.md" and path.exists():
            label = "  ← THE STORY (prose)"
        print(f"  {marker} {filename}{label}")

    if result.final_prose_path is not None:
        print()
        print(f"Final prose: {_rel(result.final_prose_path, config.repo_root)}")
        print("Open this file to read the generated scene.")

    print(_banner("", char="="))
    return result
