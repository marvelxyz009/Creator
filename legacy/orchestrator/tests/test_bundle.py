"""Tests for orchestrator.core.bundle — context bundle assembly."""

from __future__ import annotations

from pathlib import Path

import pytest

from orchestrator.core.bundle import Bundle, BundleAssembler


def test_bundle_to_dict_roundtrip() -> None:
    b = Bundle(
        for_agent="scene-director",
        task_id="t1",
        pinned_artifacts={"theme.yaml": {"id": "theme:primary"}},
        constraints={"rules": ["R1", "R2"]},
        budget_tokens=4000,
    )
    d = b.to_dict()
    assert d["for_agent"] == "scene-director"
    assert d["task_id"] == "t1"
    assert d["budget_tokens"] == 4000
    assert d["pinned_artifacts"]["theme.yaml"]["id"] == "theme:primary"
    assert d["constraints"]["rules"] == ["R1", "R2"]
    assert d["revision_directive"] is None


def test_bundle_assembler_for_scene_director() -> None:
    repo_root = Path(__file__).resolve().parents[2]
    sample_dir = repo_root / "samples" / "mvp-scene-01"
    if not (sample_dir / "inputs" / "theme.yaml").exists():
        pytest.skip("mvp-scene-01 sample not present")

    assembler = BundleAssembler(sample_dir=sample_dir)
    bundle = assembler.assemble_for_scene_director(task_id="scene:01")

    assert bundle.for_agent == "scene-director"
    assert "theme.yaml" in bundle.pinned_artifacts
    assert "world.yaml" in bundle.pinned_artifacts
    assert "characters/mira.yaml" in bundle.pinned_artifacts
    assert "characters/tomas.yaml" in bundle.pinned_artifacts
    assert "plot_beat.yaml" in bundle.pinned_artifacts
    assert "memory_graph_excerpt.yaml" in bundle.pinned_artifacts
    assert bundle.constraints.get("rules"), "rules must be populated"


def test_bundle_assembler_raises_on_missing_sample_input(tmp_path: Path) -> None:
    """If a required artifact is missing the assembler raises FileNotFoundError."""
    empty_sample = tmp_path / "empty-sample"
    (empty_sample / "inputs").mkdir(parents=True)
    assembler = BundleAssembler(sample_dir=empty_sample)
    with pytest.raises(FileNotFoundError):
        assembler.assemble_for_scene_director(task_id="t1")
