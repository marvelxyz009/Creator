"""Tests for orchestrator.prompts.render — Jinja2 hydration + YAML extraction."""

from __future__ import annotations

from orchestrator.core.bundle import Bundle
from orchestrator.prompts.render import (
    extract_yaml_from_response,
    render_system_prompt,
    render_user_prompt,
)


def test_render_user_prompt_includes_bundle_yaml() -> None:
    bundle = Bundle(
        for_agent="scene-director",
        task_id="t1",
        pinned_artifacts={"theme.yaml": {"id": "theme:primary"}},
        constraints={"rules": ["R1"]},
    )
    rendered = render_user_prompt(bundle)

    # The rendered user prompt must mention the agent and embed the bundle YAML.
    assert "scene-director" in rendered
    assert "```yaml" in rendered
    assert "theme:primary" in rendered
    assert "R1" in rendered


def test_render_user_prompt_includes_revision_directive_when_set() -> None:
    bundle = Bundle(
        for_agent="scene-director",
        task_id="t1",
        revision_directive="Cut all direct emotion namings in narration; re-render.",
    )
    rendered = render_user_prompt(bundle)
    assert "Revision directive" in rendered
    assert "Cut all direct emotion namings" in rendered


def test_render_user_prompt_omits_revision_section_when_unset() -> None:
    bundle = Bundle(for_agent="scene-director", task_id="t1")
    rendered = render_user_prompt(bundle)
    assert "Revision directive" not in rendered


def test_render_system_prompt_is_passthrough() -> None:
    body = "## Agent Identity\n\nYou are the test agent.\n"
    assert render_system_prompt(body) == body


def test_extract_yaml_from_fenced_block() -> None:
    response = """\
Here is my output:

```yaml
agent: scene-director
status: ok
scene_blueprint:
  scene_id: scene:01
```
"""
    parsed = extract_yaml_from_response(response)
    assert parsed is not None
    assert parsed["agent"] == "scene-director"
    assert parsed["status"] == "ok"
    assert parsed["scene_blueprint"]["scene_id"] == "scene:01"


def test_extract_yaml_falls_back_to_whole_response_when_unfenced() -> None:
    response = "agent: scene-director\nstatus: ok\n"
    parsed = extract_yaml_from_response(response)
    assert parsed == {"agent": "scene-director", "status": "ok"}


def test_extract_yaml_returns_none_on_unparseable() -> None:
    response = "this is just prose with no yaml structure"
    parsed = extract_yaml_from_response(response)
    # "prose..." is technically a YAML string scalar, not a dict — must be rejected.
    assert parsed is None
