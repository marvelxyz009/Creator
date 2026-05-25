"""Command-line interface for the orchestrator.

Usage:
    python -m orchestrator run <workflow> --sample <path>

Currently supported workflows:
    scene-generation    — run the scene-generation-workflow end-to-end

Example:
    python -m orchestrator run scene-generation --sample samples/mvp-scene-01
"""

from __future__ import annotations

import argparse
import logging
import sys
from pathlib import Path

from orchestrator.core.config import Config, load_config

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

    parser.print_help()
    return 2


if __name__ == "__main__":  # pragma: no cover
    sys.exit(main())
