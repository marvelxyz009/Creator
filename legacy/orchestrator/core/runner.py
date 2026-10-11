"""DAG runner: executes a workflow's ordered steps with explicit transitions.

Design choice: hand-rolled, no graph library. A workflow is a list of Steps
with named dependencies; the runner topologically sorts and executes in order.
This trades capability (no parallelism, no branching by default) for
debuggability and explicit control flow.

Adversarial-validator isolation is enforced here: each step receives only the
bundle the Workflow declares for it; no step sees another step's bundle.
"""

from __future__ import annotations

import logging
import time
from collections.abc import Callable
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

logger = logging.getLogger(__name__)


@dataclass
class StepResult:
    """Output of one step's execution."""

    step_id: str
    status: str          # "ok" | "soft_reject" | "hard_reject" | "escalate" | "skipped"
    output: Any = None   # the agent's parsed output (typically a dict from YAML)
    raw_output: str = "" # the agent's raw text response (for audit / replay)
    artifact_path: Path | None = None  # where the output was written
    duration_seconds: float = 0.0
    notes: str = ""

    @property
    def ok(self) -> bool:
        return self.status == "ok"


@dataclass
class Step:
    """One step in a workflow DAG.

    `fn` is a callable that takes (runner, prior_results) and returns a StepResult.
    The callable is responsible for: bundle assembly, LLM call, output parsing,
    artifact write. It typically dispatches to a specialized handler module.
    """

    id: str
    description: str
    depends_on: list[str] = field(default_factory=list)
    fn: Callable[["WorkflowRunner", dict[str, StepResult]], StepResult] | None = None
    """The function that executes this step. None during planning-only mode."""

    optional: bool = False
    """If True, hard_reject does NOT halt the workflow."""


@dataclass
class RunReport:
    """Final report of a workflow run. Serialized as YAML to the run dir."""

    workflow_id: str
    sample_dir: Path
    run_dir: Path
    started_at: float
    finished_at: float
    steps: list[StepResult] = field(default_factory=list)
    ok: bool = True
    golden_comparison: dict[str, Any] | None = None
    notes: list[str] = field(default_factory=list)

    @property
    def duration_seconds(self) -> float:
        return self.finished_at - self.started_at

    def to_dict(self) -> dict[str, Any]:
        return {
            "workflow_id": self.workflow_id,
            "sample_dir": str(self.sample_dir),
            "run_dir": str(self.run_dir),
            "started_at": self.started_at,
            "finished_at": self.finished_at,
            "duration_seconds": round(self.duration_seconds, 2),
            "ok": self.ok,
            "steps": [
                {
                    "step_id": s.step_id,
                    "status": s.status,
                    "duration_seconds": round(s.duration_seconds, 2),
                    "artifact_path": str(s.artifact_path) if s.artifact_path else None,
                    "notes": s.notes,
                }
                for s in self.steps
            ],
            "golden_comparison": self.golden_comparison,
            "notes": self.notes,
        }


class WorkflowRunner:
    """Executes an ordered list of Steps. No magic; no framework dependencies."""

    def __init__(self, run_dir: Path, dry_run: bool = False):
        self.run_dir = run_dir
        self.dry_run = dry_run
        self.run_dir.mkdir(parents=True, exist_ok=True)

    def topological_order(self, steps: list[Step]) -> list[Step]:
        """Return steps in topological order. Raises if a cycle is detected."""
        by_id = {s.id: s for s in steps}
        for s in steps:
            for dep in s.depends_on:
                if dep not in by_id:
                    raise ValueError(f"Step {s.id!r} depends on unknown step {dep!r}")

        ordered: list[Step] = []
        seen: set[str] = set()
        visiting: set[str] = set()

        def visit(step_id: str) -> None:
            if step_id in seen:
                return
            if step_id in visiting:
                raise ValueError(f"Cycle detected at step {step_id!r}")
            visiting.add(step_id)
            for dep in by_id[step_id].depends_on:
                visit(dep)
            visiting.remove(step_id)
            seen.add(step_id)
            ordered.append(by_id[step_id])

        for s in steps:
            visit(s.id)
        return ordered

    def execute(
        self,
        steps: list[Step],
        workflow_id: str,
        sample_dir: Path,
    ) -> RunReport:
        """Execute the DAG. Halts on hard_reject unless the step is optional."""
        ordered = self.topological_order(steps)

        report = RunReport(
            workflow_id=workflow_id,
            sample_dir=sample_dir,
            run_dir=self.run_dir,
            started_at=time.time(),
            finished_at=0.0,
        )

        results: dict[str, StepResult] = {}

        for step in ordered:
            logger.info("→ %s (%s)", step.id, step.description)
            t0 = time.time()

            if self.dry_run:
                result = StepResult(step_id=step.id, status="skipped", notes="dry-run")
            elif step.fn is None:
                result = StepResult(step_id=step.id, status="skipped", notes="no fn bound")
            else:
                try:
                    result = step.fn(self, results)
                except Exception as exc:
                    logger.exception("Step %s raised", step.id)
                    result = StepResult(
                        step_id=step.id, status="hard_reject", notes=f"exception: {exc}"
                    )

            result.duration_seconds = time.time() - t0
            results[step.id] = result
            report.steps.append(result)
            logger.info(
                "  ↳ %s in %.2fs%s",
                result.status,
                result.duration_seconds,
                f" — {result.notes}" if result.notes else "",
            )

            if result.status in ("hard_reject", "escalate") and not step.optional:
                report.ok = False
                report.notes.append(f"Halted at step {step.id!r} with status {result.status}")
                break

        report.finished_at = time.time()
        return report
