"""Command-line interface for the orchestrator.

Primary command (no API key required):

      python -m orchestrator create-scene --sample <path>

Walks interactively through all 5 scene-generation agents
(scene-director → symbolism-tracker → dialogue-specialist → anti-ai-editor →
continuity-auditor). For each agent the runner hydrates the prompt, prints
clear instructions, waits while you copy-paste through Claude in your IDE,
then validates the saved reply. The final prose lands in
`samples/<sample>/generated/05-revised-draft.md`.

Per-agent commands (manual mode, no API key):
      python -m orchestrator prepare-agent <agent-id> --sample <path>
      python -m orchestrator validate-agent-output <agent-id> \\
          --sample <path> --input <path-to-claude-output>

API mode (optional, requires ANTHROPIC_API_KEY):
      python -m orchestrator run-agent scene-director --sample <path>

Utility commands:
      python -m orchestrator inspect-sample --sample <path>
      python -m orchestrator list-workflows

Quick example end-to-end:

      python -m orchestrator create-scene --sample samples/mvp-scene-01
"""

from __future__ import annotations

import argparse
import logging
import sys
from pathlib import Path

# Ensure stdout/stderr accept UTF-8 so unicode glyphs (✓ ✗ → · ⚠) print on
# Windows consoles whose default codepage is cp1252. Best-effort; on terminals
# that already accept UTF-8 this is a no-op. Must run BEFORE the first print.
for _stream in (sys.stdout, sys.stderr):
    if hasattr(_stream, "reconfigure"):
        try:
            _stream.reconfigure(encoding="utf-8", errors="backslashreplace")
        except Exception:
            pass

from orchestrator.core.config import Config, load_config  # noqa: E402

logger = logging.getLogger(__name__)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="python -m orchestrator",
        description="AetherForge Creator Framework — MVP orchestrator.",
    )
    parser.add_argument(
        "--log-level",
        default=None,
        help="Override AETHERFORGE_LOG_LEVEL (DEBUG | INFO | WARNING | ERROR).",
    )

    subparsers = parser.add_subparsers(dest="command", required=True)

    # `run` subcommand
    run = subparsers.add_parser("run", help="Run a workflow.")
    run.add_argument(
        "workflow",
        choices=["scene-generation"],
        help="Which workflow to run.",
    )
    run.add_argument(
        "--sample",
        type=Path,
        required=True,
        help="Path to a sample directory (must contain inputs/).",
    )
    run.add_argument(
        "--compare-golden",
        action="store_true",
        default=True,
        help="Compare generated artifacts against sample's golden outputs/ (default: on).",
    )
    run.add_argument(
        "--no-compare-golden",
        action="store_false",
        dest="compare_golden",
        help="Skip golden comparison.",
    )
    run.add_argument(
        "--dry-run",
        action="store_true",
        help="Plan and report the DAG without calling the LLM.",
    )

    # `list-workflows` subcommand (utility)
    subparsers.add_parser("list-workflows", help="List available workflows.")

    # `inspect-sample` subcommand (utility)
    inspect = subparsers.add_parser(
        "inspect-sample", help="Inspect a sample directory's structure."
    )
    inspect.add_argument("--sample", type=Path, required=True)

    # All 5 agents in the scene-generation workflow support manual mode.
    # Pulled from the AGENT_SPECS registry so adding new agents touches one place.
    from orchestrator.workflows.manual_mode import ALL_AGENT_IDS
    _agent_choices = list(ALL_AGENT_IDS)

    # `prepare-agent` subcommand (Manual Agent Mode, phase 1; no API key)
    prepare = subparsers.add_parser(
        "prepare-agent",
        help=(
            "Manual mode: hydrate an agent's prompt and write it to disk for "
            "the human to paste into Claude (no API call)."
        ),
    )
    prepare.add_argument(
        "agent_id",
        choices=_agent_choices,
        help="Which agent. All 5 scene-generation agents supported.",
    )
    prepare.add_argument("--sample", type=Path, required=True, help="Sample directory.")

    # `validate-agent-output` subcommand (Manual Agent Mode, phase 2; no API key)
    validate = subparsers.add_parser(
        "validate-agent-output",
        help=(
            "Manual mode: validate the agent output a human pasted in, extract "
            "YAML, and write the canonical artifact on success (no API call)."
        ),
    )
    validate.add_argument(
        "agent_id",
        choices=_agent_choices,
        help="Which agent.",
    )
    validate.add_argument("--sample", type=Path, required=True, help="Sample directory.")
    validate.add_argument(
        "--input",
        type=Path,
        required=True,
        help=(
            "Path to the file containing the agent's output. Accepts .yaml or .md. "
            "If .md, the validator extracts the YAML from a fenced ```yaml ... ``` block."
        ),
    )

    # `create-scene` subcommand — interactive end-to-end manual workflow
    create_scene = subparsers.add_parser(
        "create-scene",
        help=(
            "Manual mode end-to-end: walk interactively through all 5 agents "
            "and write the final prose. Pauses after each prepare step so you "
            "can copy-paste through Claude in your IDE."
        ),
    )
    create_scene.add_argument(
        "--sample", type=Path, required=True, help="Sample directory."
    )

    # `run-agent` subcommand (API Agent Mode; requires ANTHROPIC_API_KEY)
    run_agent = subparsers.add_parser(
        "run-agent",
        help=(
            "API mode (optional): call Anthropic and run a single agent "
            "end-to-end. Requires ANTHROPIC_API_KEY."
        ),
    )
    run_agent.add_argument(
        "agent_id",
        choices=["scene-director"],
        help="Which agent. API mode supports scene-director (others can be added).",
    )
    run_agent.add_argument(
        "--sample",
        type=Path,
        required=True,
        help="Path to a sample directory.",
    )

    return parser


def configure_logging(level_override: str | None, config: Config) -> None:
    level_name = (level_override or config.log_level).upper()
    level = getattr(logging, level_name, logging.INFO)
    logging.basicConfig(
        level=level,
        format="%(asctime)s | %(levelname)-7s | %(name)s | %(message)s",
        datefmt="%H:%M:%S",
    )


def cmd_run(args: argparse.Namespace, config: Config) -> int:
    """Dispatch to the requested workflow."""
    if args.workflow == "scene-generation":
        # Imported here to keep CLI startup fast and to keep import errors
        # local to the command path that needs them.
        from orchestrator.workflows.scene_generation import SceneGenerationWorkflow

        wf = SceneGenerationWorkflow(config=config)
        report = wf.run(
            sample_dir=args.sample.resolve(),
            compare_golden=args.compare_golden,
            dry_run=args.dry_run,
        )
        # The Workflow.run() contract returns a RunReport with .ok bool
        return 0 if report.ok else 1

    logger.error("Unknown workflow: %s", args.workflow)
    return 2


def cmd_list_workflows(args: argparse.Namespace, config: Config) -> int:
    print("Available workflows:")
    print("  scene-generation    — scene-level pipeline (MVP target)")
    print("  chapter-generation  — chapter-level pipeline (not yet implemented)")
    print("  cross-cultural      — cultural regeneration (not yet implemented)")
    return 0


def cmd_inspect_sample(args: argparse.Namespace, config: Config) -> int:
    """Print the sample's directory tree and whether required inputs exist."""
    from orchestrator.core.artifact import inspect_sample

    return inspect_sample(args.sample.resolve())


def cmd_run_agent(args: argparse.Namespace, config: Config) -> int:
    """API mode: run a single agent against the live Anthropic API."""
    if not config.has_api_key:
        logger.error(
            "ANTHROPIC_API_KEY is not set or malformed. "
            "Copy .env.example to .env and fill it in — or use Manual Agent Mode "
            "instead: `python -m orchestrator prepare-agent scene-director ...`"
        )
        return 2

    if args.agent_id == "scene-director":
        from orchestrator.workflows.scene_director_only import (
            print_summary,
            run_scene_director,
        )

        result = run_scene_director(sample_dir=args.sample.resolve(), config=config)
        print_summary(result, repo_root=config.repo_root)
        return 0 if result.ok else 1

    logger.error("Unknown agent: %s", args.agent_id)
    return 2


def cmd_prepare_agent(args: argparse.Namespace, config: Config) -> int:
    """Manual mode phase 1: hydrate prompt + write to disk. No API call."""
    from orchestrator.workflows.manual_mode import (
        prepare_agent_prompt,
        print_prepare_summary,
    )

    try:
        result = prepare_agent_prompt(
            agent_id=args.agent_id,
            sample_dir=args.sample.resolve(),
            config=config,
        )
    except FileNotFoundError as exc:
        logger.error("%s", exc)
        return 1
    except ValueError as exc:
        logger.error("%s", exc)
        return 2

    print_prepare_summary(result, repo_root=config.repo_root)
    return 0 if result.ok else 1


def cmd_validate_agent_output(args: argparse.Namespace, config: Config) -> int:
    """Manual mode phase 2: validate the agent's output the human pasted in."""
    from orchestrator.workflows.manual_mode import (
        print_validate_summary,
        validate_agent_output,
    )

    result = validate_agent_output(
        agent_id=args.agent_id,
        sample_dir=args.sample.resolve(),
        input_path=args.input.resolve(),
        config=config,
    )
    print_validate_summary(result, repo_root=config.repo_root)
    return 0 if result.ok else 1


def cmd_create_scene(args: argparse.Namespace, config: Config) -> int:
    """Manual mode end-to-end: walk through all 5 agents interactively."""
    from orchestrator.workflows.manual_workflow_runner import (
        run_scene_generation_manual,
    )

    result = run_scene_generation_manual(
        sample_dir=args.sample.resolve(),
        config=config,
    )
    return 0 if result.ok else 1


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)

    config = load_config()
    configure_logging(args.log_level, config)

    if args.command == "run":
        return cmd_run(args, config)
    if args.command == "list-workflows":
        return cmd_list_workflows(args, config)
    if args.command == "inspect-sample":
        return cmd_inspect_sample(args, config)
    if args.command == "run-agent":
        return cmd_run_agent(args, config)
    if args.command == "prepare-agent":
        return cmd_prepare_agent(args, config)
    if args.command == "validate-agent-output":
        return cmd_validate_agent_output(args, config)
    if args.command == "create-scene":
        return cmd_create_scene(args, config)

    parser.print_help()
    return 2


if __name__ == "__main__":  # pragma: no cover
    sys.exit(main())
