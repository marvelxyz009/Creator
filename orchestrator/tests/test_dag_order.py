"""Tests for orchestrator.core.runner — DAG topological order + dry-run execution."""

from __future__ import annotations

from pathlib import Path

import pytest

from orchestrator.core.runner import Step, StepResult, WorkflowRunner


def make_step(step_id: str, depends_on: list[str] | None = None) -> Step:
    return Step(
        id=step_id,
        description=f"step {step_id}",
        depends_on=depends_on or [],
        fn=lambda runner, prior: StepResult(step_id=step_id, status="ok"),
    )


def test_topological_order_respects_dependencies(tmp_path: Path) -> None:
    runner = WorkflowRunner(run_dir=tmp_path)
    steps = [
        make_step("c", depends_on=["b"]),
        make_step("a"),
        make_step("b", depends_on=["a"]),
    ]
    ordered = runner.topological_order(steps)
    ids = [s.id for s in ordered]
    assert ids.index("a") < ids.index("b") < ids.index("c")


def test_topological_order_detects_cycle(tmp_path: Path) -> None:
    runner = WorkflowRunner(run_dir=tmp_path)
    a = make_step("a", depends_on=["b"])
    b = make_step("b", depends_on=["a"])
    with pytest.raises(ValueError, match="Cycle"):
        runner.topological_order([a, b])


def test_topological_order_rejects_unknown_dependency(tmp_path: Path) -> None:
    runner = WorkflowRunner(run_dir=tmp_path)
    a = make_step("a", depends_on=["ghost"])
    with pytest.raises(ValueError, match="unknown step"):
        runner.topological_order([a])


def test_dry_run_executes_in_order_without_calling_fn(tmp_path: Path) -> None:
    called: list[str] = []

    def real_fn(step_id: str):
        def _fn(runner, prior):
            called.append(step_id)
            return StepResult(step_id=step_id, status="ok")
        return _fn

    steps = [
        Step(id="b", description="b", depends_on=["a"], fn=real_fn("b")),
        Step(id="a", description="a", fn=real_fn("a")),
    ]
    runner = WorkflowRunner(run_dir=tmp_path, dry_run=True)
    report = runner.execute(steps, workflow_id="test", sample_dir=tmp_path)

    assert report.ok is True
    assert [r.step_id for r in report.steps] == ["a", "b"]
    assert all(r.status == "skipped" for r in report.steps)
    assert called == []   # dry_run must skip fn invocation


def test_execute_halts_on_hard_reject(tmp_path: Path) -> None:
    def step_a(runner, prior):
        return StepResult(step_id="a", status="ok")

    def step_b(runner, prior):
        return StepResult(step_id="b", status="hard_reject", notes="bad")

    def step_c(runner, prior):
        return StepResult(step_id="c", status="ok")

    steps = [
        Step(id="a", description="a", fn=step_a),
        Step(id="b", description="b", depends_on=["a"], fn=step_b),
        Step(id="c", description="c", depends_on=["b"], fn=step_c),
    ]
    runner = WorkflowRunner(run_dir=tmp_path)
    report = runner.execute(steps, workflow_id="test", sample_dir=tmp_path)

    assert report.ok is False
    assert [r.step_id for r in report.steps] == ["a", "b"]   # c never ran


def test_execute_continues_past_optional_hard_reject(tmp_path: Path) -> None:
    def step_a(runner, prior):
        return StepResult(step_id="a", status="ok")

    def step_b(runner, prior):
        return StepResult(step_id="b", status="hard_reject")

    def step_c(runner, prior):
        return StepResult(step_id="c", status="ok")

    steps = [
        Step(id="a", description="a", fn=step_a),
        Step(id="b", description="b", depends_on=["a"], fn=step_b, optional=True),
        Step(id="c", description="c", depends_on=["b"], fn=step_c),
    ]
    runner = WorkflowRunner(run_dir=tmp_path)
    report = runner.execute(steps, workflow_id="test", sample_dir=tmp_path)

    assert [r.step_id for r in report.steps] == ["a", "b", "c"]
    # ok is still True because the only failure was on an optional step
    assert report.ok is True
