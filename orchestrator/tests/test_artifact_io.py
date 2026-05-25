"""Tests for orchestrator.core.artifact — YAML/Markdown read+write."""

from __future__ import annotations

from pathlib import Path

import pytest

from orchestrator.core.artifact import (
    read_markdown,
    read_optional_yaml,
    read_yaml,
    write_markdown,
    write_yaml,
)


def test_write_then_read_yaml(tmp_path: Path) -> None:
    target = tmp_path / "nested" / "out.yaml"
    payload = {"agent": "scene-director", "status": "ok", "list": [1, 2, 3]}
    write_yaml(target, payload)
    assert target.exists()
    assert read_yaml(target) == payload


def test_write_then_read_markdown(tmp_path: Path) -> None:
    target = tmp_path / "nested" / "out.md"
    text = "# Header\n\nbody.\n"
    write_markdown(target, text)
    assert target.exists()
    assert read_markdown(target) == text


def test_read_yaml_missing_raises(tmp_path: Path) -> None:
    with pytest.raises(FileNotFoundError):
        read_yaml(tmp_path / "does-not-exist.yaml")


def test_read_optional_yaml_missing_returns_none(tmp_path: Path) -> None:
    assert read_optional_yaml(tmp_path / "does-not-exist.yaml") is None


def test_read_yaml_rejects_non_dict_top_level(tmp_path: Path) -> None:
    p = tmp_path / "list-only.yaml"
    p.write_text("- 1\n- 2\n- 3\n", encoding="utf-8")
    with pytest.raises(ValueError):
        read_yaml(p)


def test_round_trip_preserves_key_order(tmp_path: Path) -> None:
    """sort_keys=False is set so write order is preserved."""
    target = tmp_path / "ordered.yaml"
    payload = {"z": 1, "a": 2, "m": 3}
    write_yaml(target, payload)
    text = target.read_text(encoding="utf-8")
    assert text.index("z:") < text.index("a:") < text.index("m:")


def test_sample_mvp_inputs_parseable() -> None:
    """The mvp-scene-01 input artifacts must be valid YAML our reader accepts."""
    repo_root = Path(__file__).resolve().parents[2]
    inputs = repo_root / "samples" / "mvp-scene-01" / "inputs"
    if not inputs.exists():
        pytest.skip("mvp-scene-01 sample not present")

    for required in ("vision.yaml", "theme.yaml", "world.yaml", "plot_beat.yaml"):
        data = read_yaml(inputs / required)
        assert isinstance(data, dict)
        assert data
