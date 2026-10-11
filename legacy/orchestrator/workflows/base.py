"""Base class for workflows. Concrete workflows subclass this."""

from __future__ import annotations

import logging
import time
from abc import ABC, abstractmethod
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from orchestrator.core.artifact import write_yaml
from orchestrator.core.config import Config
from orchestrator.core.runner import RunReport, Step, WorkflowRunner

logger = logging.getLogger(__name__)


class Workflow(ABC):
    """Abstract base for all workflows.

    Subclass contract:
      - `workflow_id` class attribute
      - `build_steps(...)` returns the ordered list of Steps
      - `run(sample_dir, compare_golden, dry_run)` orchestrates the run
    """

    workflow_id: str = "abstract"

    def __init__(self, config: Config):
        self.config = config

    @abstractmethod
    def build_steps(self, sample_dir: Path, run_dir: Path) -> list[Step]:
        """Return the workflow's DAG."""
        raise NotImplementedError

    @abstractmethod
    def compare_to_golden(
        self, sample_dir: Path, run_dir: Path, report: RunReport
    ) -> dict[str, Any]:
        """Compare generated artifacts against sample's outputs/ if present.

        Returns a dict to attach to RunReport.golden_comparison. Should be
        non-strict: comparison is INFORMATIONAL for MVP, not pass/fail.
        """
        raise NotImplementedError

    # ─── Standard run wrapper ────────────────────────────────────────────────

    def run(
        self,
        sample_dir: Path,
        compare_golden: bool = True,
        dry_run: bool = False,
    ) -> RunReport:
        """Execute this workflow against a sample directory."""
        if not (sample_dir / "inputs").exists():
            raise FileNotFoundError(
                f"Sample is missing inputs/: {sample_dir}. "
                "Run `python -m orchestrator inspect-sample --sample <path>` to debug."
            )

        run_dir = self._make_run_dir(sample_dir)
        logger.info("Run directory: %s", run_dir)

        steps = self.build_steps(sample_dir=sample_dir, run_dir=run_dir)

        runner = WorkflowRunner(run_dir=run_dir, dry_run=dry_run)
        report = runner.execute(
            steps=steps,
            workflow_id=self.workflow_id,
            sample_dir=sample_dir,
        )

        if compare_golden and not dry_run:
            try:
                report.golden_comparison = self.compare_to_golden(
                    sample_dir=sample_dir, run_dir=run_dir, report=report
                )
            except Exception as exc:
                logger.exception("Golden comparison failed")
                report.golden_comparison = {"error": str(exc)}

        # Persist the report
        write_yaml(run_dir / "run-report.yaml", report.to_dict())
        logger.info(
            "Run complete: %s — %s (%.2fs)",
            self.workflow_id,
            "ok" if report.ok else "FAILED",
            report.duration_seconds,
        )
        return report

    def _make_run_dir(self, sample_dir: Path) -> Path:
        timestamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
        sample_name = sample_dir.name
        run_dir = self.config.runs_dir / f"{self.workflow_id}__{sample_name}__{timestamp}"
        run_dir.mkdir(parents=True, exist_ok=True)
        return run_dir
