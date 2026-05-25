"""Integration test for Scene Director end-to-end (Milestone 1).

This test calls the real Anthropic API. It auto-skips when ANTHROPIC_API_KEY
is unset (CI without secrets; local dev without keys).

Run manually with:

    pytest orchestrator/tests/test_scene_director_integration.py -ra -s

The `-s` lets you see structured-log lines as the test runs.
"""

from __future__ import annotations

import os
from pathlib import Path

import pytest

from orchestrator.workflows.scene_director_only import (
    REQUIRED_SCENE_BLUEPRINT_FIELDS,
    validate_scene_blueprint,
)


REQUIRES_API_KEY = pytest.mark.skipif(
    not os.environ.get("ANTHROPIC_API_KEY"),
    reason="ANTHROPIC_API_KEY not set — skipping live-LLM integration test",
)

REPO_ROOT = Path(__file__).resolve().parents[2]
MVP_SAMPLE = REPO_ROOT / "samples" / "mvp-scene-01"


# ─── Pure-Python validator tests (run always) ─────────────────────────────────

def test_validator_rejects_non_mapping_top_level() -> None:
    violations = validate_scene_blueprint("not a dict")  # type: ignore[arg-type]
    assert violations == ["top-level output is not a YAML mapping"]


def test_validator_rejects_missing_scene_blueprint() -> None:
    assert validate_scene_blueprint({}) == [
        "missing required top-level key: scene_blueprint"
    ]
    assert validate_scene_blueprint({"agent": "scene-director"}) == [
        "missing required top-level key: scene_blueprint"
    ]


def test_validator_rejects_non_mapping_scene_blueprint() -> None:
    violations = validate_scene_blueprint({"scene_blueprint": "oops"})
    assert violations == ["scene_blueprint is not a mapping"]


def test_validator_reports_each_missing_required_field() -> None:
    violations = validate_scene_blueprint({"scene_blueprint": {"scene_id": "scene:01"}})
    # Every required field except scene_id should be reported.
    for f in REQUIRED_SCENE_BLUEPRINT_FIELDS:
        if f == "scene_id":
            continue
        assert any(f in v for v in violations), f"expected violation for {f}"


def test_validator_rejects_empty_required_field_values() -> None:
    sb = {f: "x" for f in REQUIRED_SCENE_BLUEPRINT_FIELDS}
    sb["dialogue_intent"] = ""        # empty string
    sb["character_actions"] = []      # empty list
    sb["symbolism_used"] = {}         # empty mapping
    sb["ending_hook"] = None          # None
    violations = validate_scene_blueprint({"scene_blueprint": sb})
    assert any("dialogue_intent" in v and "empty" in v for v in violations)
    assert any("character_actions" in v and "empty" in v for v in violations)
    assert any("symbolism_used" in v and "empty" in v for v in violations)
    assert any("ending_hook" in v and "empty" in v for v in violations)


def test_validator_accepts_complete_blueprint() -> None:
    sb = {f: "non-empty-placeholder" for f in REQUIRED_SCENE_BLUEPRINT_FIELDS}
    # Make collection types non-empty so the "empty" check passes for them.
    sb["character_actions"] = [{"who": "char:mira"}]
    sb["symbolism_used"] = [{"id": "sym:x", "op": "introduce"}]
    sb["revealed_information"] = [{"what": "x"}]
    sb["hidden_information"] = [{"what": "x"}]
    sb["emotional_shift"] = {"pov_entry_state": "x", "pov_exit_state": "y"}
    sb["dialogue_intent"] = {"overall_register": "x"}
    sb["ending_hook"] = {"type": "gesture", "description": "x"}
    sb["purpose"] = {"one_sentence": "x"}
    assert validate_scene_blueprint({"scene_blueprint": sb}) == []


# ─── Live-LLM integration test (requires API key) ─────────────────────────────

@REQUIRES_API_KEY
def test_scene_director_end_to_end_against_mvp_sample() -> None:
    """End-to-end Scene Director run against the canonical MVP sample.

    Validates:
      - The integration produces status == "ok"
      - Output contains scene_blueprint with all required fields
      - The canonical artifact is written to samples/mvp-scene-01/generated/
      - Debug artifacts exist (hydrated-prompt, raw-response, extracted-yaml)
    """
    if not MVP_SAMPLE.exists():
        pytest.skip(f"sample not present: {MVP_SAMPLE}")

    from orchestrator.core.config import load_config
    from orchestrator.workflows.scene_director_only import run_scene_director

    config = load_config()
    result = run_scene_director(sample_dir=MVP_SAMPLE, config=config)

    # If this fails the assertion's message will include the agent's actual
    # diagnostic notes — useful when debugging from CI output.
    assert result.ok, (
        f"Scene Director did not succeed.\n"
        f"  status={result.status}\n"
        f"  attempts={result.attempt_count}\n"
        f"  validation_violations={result.validation_violations}\n"
        f"  notes={result.notes}\n"
        f"  debug_dir={result.debug_dir}\n"
    )

    # Structural assertions on output.
    assert result.output is not None
    assert "scene_blueprint" in result.output
    sb = result.output["scene_blueprint"]
    assert isinstance(sb, dict)
    for required in REQUIRED_SCENE_BLUEPRINT_FIELDS:
        assert required in sb, f"required field missing in output: {required}"

    # Canonical artifact written.
    assert result.artifact_path is not None
    assert result.artifact_path.exists()
    assert result.artifact_path.name == "01-scene-blueprint.yaml"

    # Debug artifacts written (before and after the LLM call).
    assert result.debug_dir is not None
    assert (result.debug_dir / "hydrated-prompt.md").exists()
    assert (result.debug_dir / "raw-scene-director-response.md").exists()
    assert (result.debug_dir / "extracted-yaml.yaml").exists()
