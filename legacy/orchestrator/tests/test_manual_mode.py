"""Tests for `orchestrator.workflows.manual_mode` — the registry-driven
manual-mode implementation that powers all 5 scene-generation agents.

No LLM calls. No API key required.
"""

from __future__ import annotations

import textwrap
from pathlib import Path

import pytest

from orchestrator.core.config import load_config
from orchestrator.workflows.manual_mode import (
    AGENT_SPECS,
    ALL_AGENT_IDS,
    _validate_schema,
    prepare_agent_prompt,
    validate_agent_output,
)


REPO_ROOT = Path(__file__).resolve().parents[2]
MVP_SAMPLE = REPO_ROOT / "samples" / "mvp-scene-01"


# ─── Registry sanity ─────────────────────────────────────────────────────────

def test_registry_includes_all_five_scene_agents() -> None:
    expected = {
        "scene-director",
        "symbolism-tracker",
        "dialogue-specialist",
        "anti-ai-editor",
        "continuity-auditor",
    }
    assert set(ALL_AGENT_IDS) == expected
    assert set(AGENT_SPECS.keys()) == expected


def test_each_spec_has_required_fields_populated() -> None:
    for agent_id, spec in AGENT_SPECS.items():
        assert spec.agent_id == agent_id, f"spec.agent_id mismatch for {agent_id}"
        assert spec.output_filename.endswith(".yaml"), agent_id
        assert spec.required_top_level, f"{agent_id} declares no required top-level keys"
        assert spec.bundle_builder is not None, agent_id


def test_prior_agents_chain_is_consistent() -> None:
    """Every prior agent named by a spec must itself be in the registry."""
    for agent_id, spec in AGENT_SPECS.items():
        for prior in spec.prior_agents_needed:
            assert prior in AGENT_SPECS, (
                f"{agent_id} declares prior {prior!r} but {prior!r} is not registered"
            )


# ─── Schema validator (driven by AGENT_SPECS) ────────────────────────────────

def test_validate_schema_rejects_non_mapping() -> None:
    spec = AGENT_SPECS["scene-director"]
    assert _validate_schema("not a dict", spec) == [   # type: ignore[arg-type]
        "top-level output is not a YAML mapping"
    ]


def test_validate_schema_rejects_missing_top_level() -> None:
    spec = AGENT_SPECS["scene-director"]
    violations = _validate_schema({}, spec)
    assert any("scene_blueprint" in v for v in violations)


def test_validate_schema_rejects_non_mapping_top_level() -> None:
    spec = AGENT_SPECS["scene-director"]
    violations = _validate_schema({"scene_blueprint": "oops"}, spec)
    assert violations == ["scene_blueprint is not a mapping"]


def test_validate_schema_reports_missing_subfields() -> None:
    spec = AGENT_SPECS["scene-director"]
    violations = _validate_schema(
        {"scene_blueprint": {"scene_id": "x"}}, spec
    )
    expected_missing = set(spec.required_subfields["scene_blueprint"]) - {"scene_id"}
    for field_name in expected_missing:
        assert any(field_name in v for v in violations)


def test_validate_schema_rejects_empty_subfield_values() -> None:
    spec = AGENT_SPECS["dialogue-specialist"]
    parsed = {"dialogue_draft": {"scene_id": "x", "pov": "y", "exchanges": []}}
    violations = _validate_schema(parsed, spec)
    assert any("exchanges" in v and "empty" in v for v in violations)


def test_validate_schema_accepts_minimal_complete_continuity_report() -> None:
    """continuity-auditor's spec has `audit_report` top-level with no subfields."""
    spec = AGENT_SPECS["continuity-auditor"]
    assert _validate_schema(
        {"audit_report": {"any_field": "any_value"}}, spec
    ) == []


# ─── prepare-agent (scene-director, no priors) ───────────────────────────────

def test_prepare_scene_director_writes_prompt_file() -> None:
    if not MVP_SAMPLE.exists():
        pytest.skip(f"sample not present: {MVP_SAMPLE}")

    config = load_config()
    result = prepare_agent_prompt(
        agent_id="scene-director",
        sample_dir=MVP_SAMPLE,
        config=config,
    )
    assert result.ok, result.notes
    assert result.prompt_path is not None
    assert result.prompt_path.exists()
    assert result.prompt_path.name == "scene-director-prompt.md"

    content = result.prompt_path.read_text(encoding="utf-8")
    assert "# scene-director — Manual Prompt" in content
    assert "--- BEGIN PROMPT ---" in content
    assert "AGENT ROLE" in content
    assert "TASK" in content
    assert "for_agent: scene-director" in content


def test_prepare_does_not_require_api_key(monkeypatch) -> None:
    if not MVP_SAMPLE.exists():
        pytest.skip(f"sample not present: {MVP_SAMPLE}")

    monkeypatch.delenv("ANTHROPIC_API_KEY", raising=False)
    config = load_config()
    result = prepare_agent_prompt(
        agent_id="scene-director", sample_dir=MVP_SAMPLE, config=config
    )
    assert result.ok


# ─── prepare-agent (downstream agents need priors on disk) ───────────────────

def test_prepare_symbolism_tracker_fails_without_prior_scene_director(
    tmp_path: Path,
) -> None:
    if not MVP_SAMPLE.exists():
        pytest.skip(f"sample not present: {MVP_SAMPLE}")

    config = load_config()
    # No scene-director artifact has been written → must raise.
    canonical = MVP_SAMPLE / "generated" / "01-scene-blueprint.yaml"
    canonical_existed = canonical.exists()
    canonical_backup: bytes | None = canonical.read_bytes() if canonical_existed else None

    if canonical_existed:
        canonical.unlink()    # remove it for the duration of this test

    try:
        with pytest.raises(FileNotFoundError, match="scene-director"):
            prepare_agent_prompt(
                agent_id="symbolism-tracker", sample_dir=MVP_SAMPLE, config=config
            )
    finally:
        # Restore so we don't leave the sample in a broken state for other tests.
        if canonical_backup is not None:
            canonical.write_bytes(canonical_backup)


def test_prepare_anti_ai_editor_with_inmemory_priors() -> None:
    """Pass priors directly to skip the disk-read."""
    if not MVP_SAMPLE.exists():
        pytest.skip(f"sample not present: {MVP_SAMPLE}")

    config = load_config()
    fake_blueprint = {"scene_blueprint": {"scene_id": "scene:01"}}
    fake_dialogue = {"dialogue_draft": {"exchanges": [{"speaker": "x", "line": "y"}]}}

    result = prepare_agent_prompt(
        agent_id="anti-ai-editor",
        sample_dir=MVP_SAMPLE,
        config=config,
        prior_outputs={
            "scene-director": fake_blueprint,
            "dialogue-specialist": fake_dialogue,
        },
    )
    assert result.ok
    assert result.prompt_path is not None
    content = result.prompt_path.read_text(encoding="utf-8")
    assert "anti-ai-editor" in content
    assert "for_agent: anti-ai-editor" in content


# ─── validate-agent-output for non-scene-director agents ─────────────────────

def _write(path: Path, text: str) -> Path:
    path.write_text(text, encoding="utf-8")
    return path


def test_validate_symbolism_tracker_accepts_minimal_valid_yaml(tmp_path: Path) -> None:
    if not MVP_SAMPLE.exists():
        pytest.skip(f"sample not present: {MVP_SAMPLE}")

    inp = _write(
        tmp_path / "symbol.yaml",
        textwrap.dedent("""\
            agent: symbolism-tracker
            status: ok
            audit:
              scene_id: scene:01
              symbols_touched:
                - id: sym:cracked-glass
                  requested_op: transform
                  legality: legal
            """),
    )

    config = load_config()
    result = validate_agent_output(
        agent_id="symbolism-tracker",
        sample_dir=MVP_SAMPLE,
        input_path=inp,
        config=config,
    )
    assert result.ok, result.notes
    assert result.artifact_path is not None
    assert result.artifact_path.name == "02-symbol-audit.yaml"


def test_validate_anti_ai_editor_extracts_revised_draft_as_prose(tmp_path: Path) -> None:
    if not MVP_SAMPLE.exists():
        pytest.skip(f"sample not present: {MVP_SAMPLE}")

    revised_prose = "She did not sit. The lighter was on the desk.\n"
    inp = _write(
        tmp_path / "antiai.yaml",
        textwrap.dedent(f"""\
            agent: anti-ai-editor
            status: ok
            smell_report:
              hard_smells: []
            humanization_pass:
              applied_rules: [H1, H3]
              revised_draft: |
                {revised_prose.strip()}
            """),
    )

    config = load_config()
    result = validate_agent_output(
        agent_id="anti-ai-editor",
        sample_dir=MVP_SAMPLE,
        input_path=inp,
        config=config,
    )
    assert result.ok, result.notes
    assert "revised_draft" in result.extra_artifacts
    prose_path = result.extra_artifacts["revised_draft"]
    assert prose_path.name == "05-revised-draft.md"
    assert prose_path.exists()
    assert "lighter was on the desk" in prose_path.read_text(encoding="utf-8")


def test_validate_continuity_auditor_accepts_minimal(tmp_path: Path) -> None:
    if not MVP_SAMPLE.exists():
        pytest.skip(f"sample not present: {MVP_SAMPLE}")

    inp = _write(
        tmp_path / "cont.yaml",
        textwrap.dedent("""\
            agent: continuity-auditor
            status: ok
            audit_report:
              hard_violations: []
              summary:
                hard_violation_count: 0
            """),
    )

    config = load_config()
    result = validate_agent_output(
        agent_id="continuity-auditor",
        sample_dir=MVP_SAMPLE,
        input_path=inp,
        config=config,
    )
    assert result.ok, result.notes
    assert result.artifact_path is not None
    assert result.artifact_path.name == "06-continuity-report.yaml"


def test_validate_rejects_unknown_agent_id(tmp_path: Path) -> None:
    if not MVP_SAMPLE.exists():
        pytest.skip(f"sample not present: {MVP_SAMPLE}")

    inp = _write(tmp_path / "x.yaml", "agent: x\nstatus: ok\n")
    config = load_config()
    with pytest.raises(ValueError, match="Unknown agent"):
        validate_agent_output(
            agent_id="not-a-real-agent",
            sample_dir=MVP_SAMPLE,
            input_path=inp,
            config=config,
        )


def test_validate_markdown_with_fenced_block_works_for_all_agents(tmp_path: Path) -> None:
    """The fenced-block path is shared across agents — spot-check it for dialogue."""
    if not MVP_SAMPLE.exists():
        pytest.skip(f"sample not present: {MVP_SAMPLE}")

    md = textwrap.dedent("""\
        Here is the dialogue:

        ```yaml
        agent: dialogue-specialist
        status: ok
        dialogue_draft:
          scene_id: scene:01
          pov: char:mira
          exchanges:
            - id: ex01
              speaker: char:mira
              line: "Did you ask."
        ```

        End.
        """)
    inp = _write(tmp_path / "dialogue.md", md)

    config = load_config()
    result = validate_agent_output(
        agent_id="dialogue-specialist",
        sample_dir=MVP_SAMPLE,
        input_path=inp,
        config=config,
    )
    assert result.ok, result.notes
