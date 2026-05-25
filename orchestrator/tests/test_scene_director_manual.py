"""Tests for Manual Agent Mode (Scene Director).

These tests do NOT call the Anthropic API. They cover:
  - `prepare_scene_director()` writes a hydrated prompt file
  - `validate_scene_director_output()` accepts valid YAML
  - `validate_scene_director_output()` rejects invalid YAML (parse fail)
  - `validate_scene_director_output()` rejects valid YAML missing required fields
  - markdown input with a fenced ```yaml ... ``` block works
"""

from __future__ import annotations

import textwrap
from pathlib import Path

import pytest

from orchestrator.core.config import load_config
from orchestrator.workflows.scene_director_manual import (
    prepare_scene_director,
    validate_scene_director_output,
)
from orchestrator.workflows.scene_director_only import REQUIRED_SCENE_BLUEPRINT_FIELDS


REPO_ROOT = Path(__file__).resolve().parents[2]
MVP_SAMPLE = REPO_ROOT / "samples" / "mvp-scene-01"


# ─── prepare-agent ────────────────────────────────────────────────────────────

def test_prepare_writes_manual_prompt_file() -> None:
    if not MVP_SAMPLE.exists():
        pytest.skip(f"sample not present: {MVP_SAMPLE}")

    config = load_config()
    result = prepare_scene_director(sample_dir=MVP_SAMPLE, config=config)

    assert result.ok, f"prepare failed: {result.notes}"
    assert result.prompt_path is not None
    assert result.prompt_path.exists()
    assert result.prompt_path.name == "scene-director-prompt.md"
    assert result.expected_output_path is not None
    assert result.expected_output_path.name == "scene-director-output.yaml"


def test_prepare_prompt_contains_required_sections() -> None:
    if not MVP_SAMPLE.exists():
        pytest.skip(f"sample not present: {MVP_SAMPLE}")

    config = load_config()
    result = prepare_scene_director(sample_dir=MVP_SAMPLE, config=config)
    assert result.prompt_path is not None
    content = result.prompt_path.read_text(encoding="utf-8")

    # Header for the human operator
    assert "# Scene Director — Manual Prompt" in content
    assert "For the human operator" in content
    # Boundary marker
    assert "--- BEGIN PROMPT ---" in content
    # System + task sections
    assert "AGENT ROLE" in content
    assert "TASK" in content
    # Required-output instructions
    assert "Required output" in content
    for required in REQUIRED_SCENE_BLUEPRINT_FIELDS:
        assert required in content, f"required field name missing in prompt: {required}"
    # Bundle YAML embedded
    assert "for_agent: scene-director" in content
    # Sample-specific inputs are pinned in the bundle
    assert "theme:primary" in content or "core_question" in content


def test_prepare_does_not_require_api_key(monkeypatch) -> None:
    """prepare-agent must work even with ANTHROPIC_API_KEY unset."""
    if not MVP_SAMPLE.exists():
        pytest.skip(f"sample not present: {MVP_SAMPLE}")

    monkeypatch.delenv("ANTHROPIC_API_KEY", raising=False)
    config = load_config()
    result = prepare_scene_director(sample_dir=MVP_SAMPLE, config=config)
    assert result.ok


# ─── validate-agent-output: success cases ─────────────────────────────────────

def _make_valid_output_yaml() -> str:
    """A minimal but schema-valid scene_blueprint as a YAML document string."""
    return textwrap.dedent("""\
        agent: scene-director
        status: ok
        scene_blueprint:
          scene_id: scene:01
          purpose:
            one_sentence: A scene that touches theme.
          emotional_shift:
            pov_entry_state: armored
            pov_exit_state: undermined
          conflict_type: epistemic
          character_actions:
            - who: char:mira
              action_intent: extract confirmation
          dialogue_intent:
            overall_register: archive-procedural
          symbolism_used:
            - id: sym:cracked-glass
              op: transform
          revealed_information:
            - what: qualified confirmation
              to: char:mira
          hidden_information:
            - what: redacted event content
              withheld_from: [char:mira, reader]
          ending_hook:
            type: gesture
            description: Mira sets the lighter back exactly.
        """)


def test_validate_accepts_pure_yaml_input(tmp_path: Path) -> None:
    sample = MVP_SAMPLE
    if not sample.exists():
        pytest.skip(f"sample not present: {sample}")

    inp = tmp_path / "scene-director-output.yaml"
    inp.write_text(_make_valid_output_yaml(), encoding="utf-8")

    config = load_config()
    result = validate_scene_director_output(
        sample_dir=sample, input_path=inp, config=config
    )

    assert result.ok, f"validate failed: {result.notes}; violations={result.validation_violations}"
    assert result.artifact_path is not None
    assert result.artifact_path.exists()
    assert result.artifact_path.name == "01-scene-blueprint.yaml"
    assert result.agent_status == "ok"


def test_validate_accepts_markdown_with_fenced_yaml_block(tmp_path: Path) -> None:
    sample = MVP_SAMPLE
    if not sample.exists():
        pytest.skip(f"sample not present: {sample}")

    md = (
        "Here is the scene blueprint:\n\n"
        "```yaml\n"
        + _make_valid_output_yaml()
        + "```\n\n"
        "End of response.\n"
    )
    inp = tmp_path / "scene-director-output.md"
    inp.write_text(md, encoding="utf-8")

    config = load_config()
    result = validate_scene_director_output(
        sample_dir=sample, input_path=inp, config=config
    )
    assert result.ok, f"validate failed: {result.notes}; violations={result.validation_violations}"
    assert result.artifact_path is not None
    assert result.artifact_path.exists()


# ─── validate-agent-output: failure cases ─────────────────────────────────────

def test_validate_rejects_missing_input_file(tmp_path: Path) -> None:
    sample = MVP_SAMPLE
    if not sample.exists():
        pytest.skip(f"sample not present: {sample}")

    config = load_config()
    result = validate_scene_director_output(
        sample_dir=sample, input_path=tmp_path / "does-not-exist.yaml", config=config
    )
    assert not result.ok
    assert "not found" in result.notes


def test_validate_rejects_empty_input_file(tmp_path: Path) -> None:
    sample = MVP_SAMPLE
    if not sample.exists():
        pytest.skip(f"sample not present: {sample}")

    inp = tmp_path / "empty.yaml"
    inp.write_text("", encoding="utf-8")

    config = load_config()
    result = validate_scene_director_output(
        sample_dir=sample, input_path=inp, config=config
    )
    assert not result.ok
    assert "empty" in result.notes


def test_validate_rejects_unparseable_yaml(tmp_path: Path) -> None:
    sample = MVP_SAMPLE
    if not sample.exists():
        pytest.skip(f"sample not present: {sample}")

    inp = tmp_path / "bad.md"
    inp.write_text(
        "Claude here. I wasn't able to write YAML this time. Just prose.\n",
        encoding="utf-8",
    )

    config = load_config()
    result = validate_scene_director_output(
        sample_dir=sample, input_path=inp, config=config
    )
    assert not result.ok
    assert "could not extract YAML" in result.notes


def test_validate_rejects_yaml_missing_required_fields(tmp_path: Path) -> None:
    sample = MVP_SAMPLE
    if not sample.exists():
        pytest.skip(f"sample not present: {sample}")

    minimal = textwrap.dedent("""\
        agent: scene-director
        status: ok
        scene_blueprint:
          scene_id: scene:01
          purpose:
            one_sentence: x
        """)
    inp = tmp_path / "partial.yaml"
    inp.write_text(minimal, encoding="utf-8")

    config = load_config()
    result = validate_scene_director_output(
        sample_dir=sample, input_path=inp, config=config
    )
    assert not result.ok
    # The blueprint has scene_id + purpose; the other 8 should be reported missing
    missing_fields_reported = {
        v.replace("scene_blueprint.", "").replace(" is missing", "")
        for v in result.validation_violations
        if v.endswith("is missing")
    }
    for f in REQUIRED_SCENE_BLUEPRINT_FIELDS:
        if f in ("scene_id", "purpose"):
            continue
        assert f in missing_fields_reported, f"expected {f} reported as missing"


def test_validate_does_not_write_canonical_when_validation_fails(tmp_path: Path) -> None:
    sample = MVP_SAMPLE
    if not sample.exists():
        pytest.skip(f"sample not present: {sample}")

    # Author a known-bad output
    inp = tmp_path / "bad.yaml"
    inp.write_text("agent: scene-director\nstatus: ok\n", encoding="utf-8")

    canonical = sample / "generated" / "01-scene-blueprint.yaml"
    canonical_existed_before = canonical.exists()
    canonical_mtime_before = canonical.stat().st_mtime if canonical_existed_before else None

    config = load_config()
    result = validate_scene_director_output(
        sample_dir=sample, input_path=inp, config=config
    )

    assert not result.ok
    # If the canonical existed before this call, it should be unchanged.
    if canonical_existed_before:
        assert canonical.stat().st_mtime == canonical_mtime_before
