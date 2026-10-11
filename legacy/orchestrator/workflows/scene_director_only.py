"""Milestone 1: Scene Director end-to-end integration.

Single-agent integration path. Implements the 7-step flow from inputs to
canonized artifact for ONE agent (Scene Director) only. NOT part of the
full scene-generation workflow DAG — that's Milestone 2.

This module exists to validate the orchestrator's plumbing — bundle assembly,
prompt hydration, LLM call, YAML extraction, schema validation, artifact
write — against a real Claude response before expanding to the full DAG.

Flow:
    1. Load inputs (via BundleAssembler)
    2. Assemble bundle
    3. Hydrate prompts (system = template body; user = Jinja2-rendered scaffold)
    4. Persist debug artifacts (hydrated prompt — written BEFORE the LLM call
       so failures still leave a reproducible artifact)
    5. Call Anthropic
    6. Persist raw response
    7. Extract YAML (with 1 retry via repair prompt if parse fails)
    8. Persist extracted YAML
    9. Validate schema (required fields)
    10. Write canonical artifact to samples/<sample>/generated/

If any step fails the function returns a structured result with `status:
hard_reject` and diagnostic notes. It does NOT raise on agent-side failures
(missing fields, parse fail) — those are domain outcomes, not exceptions.
It DOES raise on infrastructure failures (missing API key, missing template,
missing sample directory).
"""

from __future__ import annotations

import logging
import time
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

from orchestrator.core.artifact import write_markdown, write_yaml
from orchestrator.core.bundle import BundleAssembler
from orchestrator.core.config import Config
from orchestrator.llm.client import LLMClient
from orchestrator.llm.models import model_for_agent
from orchestrator.prompts.loader import PromptLoader
from orchestrator.prompts.render import (
    extract_yaml_from_response,
    render_system_prompt,
    render_user_prompt,
)

logger = logging.getLogger("orchestrator.scene_director")


# ─── Schema validation ────────────────────────────────────────────────────────

REQUIRED_SCENE_BLUEPRINT_FIELDS: tuple[str, ...] = (
    "scene_id",
    "purpose",
    "emotional_shift",
    "conflict_type",
    "character_actions",
    "dialogue_intent",
    "symbolism_used",
    "revealed_information",
    "hidden_information",
    "ending_hook",
)


def validate_scene_blueprint(parsed: dict[str, Any]) -> list[str]:
    """Return a list of violation messages. Empty list = pass.

    Validates only the user-specified required fields. Additional fields the
    agent produces (goal, opposition, stakes, turn, residue, prose_constraints,
    micro_beats) are allowed but not required at this layer; downstream
    workflow stages will check them.
    """
    if not isinstance(parsed, dict):
        return ["top-level output is not a YAML mapping"]

    if "scene_blueprint" not in parsed:
        return ["missing required top-level key: scene_blueprint"]

    sb = parsed["scene_blueprint"]
    if not isinstance(sb, dict):
        return ["scene_blueprint is not a mapping"]

    violations: list[str] = []
    for field_name in REQUIRED_SCENE_BLUEPRINT_FIELDS:
        if field_name not in sb:
            violations.append(f"scene_blueprint.{field_name} is missing")
            continue
        value = sb[field_name]
        if value is None or value == "" or value == [] or value == {}:
            violations.append(f"scene_blueprint.{field_name} is empty")
    return violations


# ─── Result type ──────────────────────────────────────────────────────────────

@dataclass
class SceneDirectorResult:
    """Outcome of a Scene Director integration run."""

    status: str   # "ok" | "hard_reject"
    output: dict[str, Any] | None = None
    artifact_path: Path | None = None
    debug_dir: Path | None = None
    debug_paths: dict[str, Path] = field(default_factory=dict)
    validation_violations: list[str] = field(default_factory=list)
    attempt_count: int = 1
    input_tokens: int = 0
    output_tokens: int = 0
    model: str = ""
    duration_seconds: float = 0.0
    agent_status: str | None = None    # status field the agent itself returned
    notes: str = ""

    @property
    def ok(self) -> bool:
        return self.status == "ok"


# ─── Structured logging helper ────────────────────────────────────────────────

def _log_step(step: str, **fields: Any) -> None:
    """Log one step with key=value fields. Matches the structured-logging spec."""
    if fields:
        kvs = " ".join(f"{k}={v}" for k, v in fields.items())
        logger.info("step=%s %s", step, kvs)
    else:
        logger.info("step=%s", step)


# ─── The integration entry point ──────────────────────────────────────────────

REPAIR_USER_PROMPT_TEMPLATE = """\
Your previous response could not be parsed as YAML.

Convert your previous response into valid YAML only. Wrap the YAML in a single
fenced block:

```yaml
...
```

Do not write any prose before or after the fenced block. Do not include any
explanation. Output the YAML and nothing else.

---

Previous response:

{previous}
"""


def run_scene_director(sample_dir: Path, config: Config) -> SceneDirectorResult:
    """Run the Scene Director agent end-to-end against a single sample.

    Returns a SceneDirectorResult. Does not raise on domain failures
    (validation fail, parse fail). Raises on infrastructure issues only
    (missing API key, missing template file, missing sample inputs).
    """
    t_start = time.time()

    sample_dir = sample_dir.resolve()
    if not (sample_dir / "inputs").exists():
        raise FileNotFoundError(
            f"Sample is missing inputs/: {sample_dir}. "
            f"Run `python -m orchestrator inspect-sample --sample {sample_dir}` to debug."
        )

    debug_dir = sample_dir / "generated" / "debug"
    debug_dir.mkdir(parents=True, exist_ok=True)
    artifact_path = sample_dir / "generated" / "01-scene-blueprint.yaml"

    result = SceneDirectorResult(status="hard_reject", debug_dir=debug_dir)
    result.debug_paths["debug_dir"] = debug_dir
    result.debug_paths["artifact_path"] = artifact_path

    # ─── Step 1+2: load inputs and assemble bundle ────────────────────────────
    assembler = BundleAssembler(sample_dir=sample_dir)
    bundle = assembler.assemble_for_scene_director(task_id="scene:01")
    _log_step(
        "bundle_loaded",
        sample=sample_dir.name,
        pinned_artifacts=len(bundle.pinned_artifacts),
        rules=len(bundle.constraints.get("rules", [])),
    )

    # ─── Step 3: load template + hydrate ─────────────────────────────────────
    loader = PromptLoader(prompts_dir=config.prompts_dir)
    template = loader.load("scene-director")
    system_prompt = render_system_prompt(template.system_prompt_markdown)
    user_prompt = render_user_prompt(bundle)
    _log_step(
        "prompt_hydrated",
        template=str(template.path.relative_to(config.repo_root)),
        system_chars=len(system_prompt),
        user_chars=len(user_prompt),
    )

    # ─── Step 4: persist hydrated prompt for debug (BEFORE the LLM call) ─────
    hydrated_path = debug_dir / "hydrated-prompt.md"
    write_markdown(
        hydrated_path,
        f"# Hydrated prompt — scene-director\n\n"
        f"Sample: `{sample_dir.name}`\n\n"
        f"## System prompt\n\n{system_prompt}\n\n"
        f"## User prompt\n\n{user_prompt}\n",
    )
    result.debug_paths["hydrated_prompt"] = hydrated_path

    # ─── Step 5: call the LLM ─────────────────────────────────────────────────
    llm = LLMClient(
        api_key=config.anthropic_api_key,
        default_model=config.anthropic_model,
        default_max_tokens=config.anthropic_max_tokens,
    )
    model = model_for_agent("scene-director", default=config.anthropic_model)
    response = llm.call(system_prompt=system_prompt, user_prompt=user_prompt, model=model)
    result.input_tokens = response.input_tokens
    result.output_tokens = response.output_tokens
    result.model = response.model
    _log_step(
        "llm_invoked",
        model=response.model,
        input_tokens=response.input_tokens,
        output_tokens=response.output_tokens,
        stop_reason=response.stop_reason,
    )

    # Always persist the raw response (overwritten if retry runs).
    raw_path = debug_dir / "raw-scene-director-response.md"
    write_markdown(
        raw_path,
        f"# Raw response — scene-director\n\n"
        f"Model: `{response.model}`\n"
        f"Input tokens: {response.input_tokens}\n"
        f"Output tokens: {response.output_tokens}\n"
        f"Stop reason: `{response.stop_reason}`\n\n"
        f"## Response text\n\n{response.text}\n",
    )
    result.debug_paths["raw_response"] = raw_path

    # ─── Step 6: extract YAML, with one retry via repair prompt ──────────────
    parsed = extract_yaml_from_response(response.text)
    retry_response = None

    if parsed is None:
        logger.warning("YAML extraction failed on first attempt; retrying with repair prompt")
        repair_user = REPAIR_USER_PROMPT_TEMPLATE.format(previous=response.text)

        # Write the repair-attempt user prompt for forensics.
        repair_prompt_path = debug_dir / "repair-prompt-1.md"
        write_markdown(
            repair_prompt_path,
            f"# Repair user prompt — attempt 2\n\n## User prompt\n\n{repair_user}\n",
        )
        result.debug_paths["repair_prompt"] = repair_prompt_path

        retry_response = llm.call(system_prompt=system_prompt, user_prompt=repair_user, model=model)
        result.attempt_count = 2
        result.input_tokens += retry_response.input_tokens
        result.output_tokens += retry_response.output_tokens

        # Overwrite raw-response with combined log of both attempts.
        write_markdown(
            raw_path,
            f"# Raw response — scene-director (2 attempts)\n\n"
            f"Model: `{response.model}`\n\n"
            f"## Attempt 1 (original)\n\n"
            f"Tokens: in={response.input_tokens} out={response.output_tokens}\n\n"
            f"```\n{response.text}\n```\n\n"
            f"## Attempt 2 (repair prompt)\n\n"
            f"Tokens: in={retry_response.input_tokens} out={retry_response.output_tokens}\n"
            f"Stop reason: `{retry_response.stop_reason}`\n\n"
            f"```\n{retry_response.text}\n```\n",
        )
        _log_step(
            "llm_invoked_retry",
            model=retry_response.model,
            input_tokens=retry_response.input_tokens,
            output_tokens=retry_response.output_tokens,
        )

        parsed = extract_yaml_from_response(retry_response.text)

    if parsed is None:
        result.notes = "YAML extraction failed after 1 retry"
        result.duration_seconds = time.time() - t_start
        _log_step("yaml_extracted", success=False, notes=result.notes)
        return result

    _log_step(
        "yaml_extracted",
        success=True,
        attempt=result.attempt_count,
        top_level_keys=list(parsed.keys()),
    )

    # Persist the extracted YAML for debug.
    extracted_path = debug_dir / "extracted-yaml.yaml"
    write_yaml(extracted_path, parsed)
    result.debug_paths["extracted_yaml"] = extracted_path
    result.output = parsed
    result.agent_status = parsed.get("status")

    # ─── Step 7: validate schema ──────────────────────────────────────────────
    violations = validate_scene_blueprint(parsed)
    result.validation_violations = violations
    _log_step("schema_validated", violations=len(violations))

    if violations:
        result.notes = (
            f"schema validation failed: {len(violations)} violation(s). "
            f"See result.validation_violations and {extracted_path} for details."
        )
        result.duration_seconds = time.time() - t_start
        return result

    # ─── Step 8: write canonical artifact ─────────────────────────────────────
    write_yaml(artifact_path, parsed)
    result.artifact_path = artifact_path
    _log_step("artifact_written", path=str(artifact_path.relative_to(config.repo_root)))

    result.status = "ok"
    result.duration_seconds = time.time() - t_start
    result.notes = "scene blueprint generated and validated successfully"
    return result


# ─── Pretty-print summary for CLI ─────────────────────────────────────────────

def print_summary(result: SceneDirectorResult, repo_root: Path) -> None:
    """Print a concise human-readable summary to stdout."""
    icon = "✓" if result.ok else "✗"
    label = "succeeded" if result.ok else "failed"
    print(f"{icon} Scene Director {label}")
    print(f"  status              : {result.status}")
    if result.agent_status:
        print(f"  agent self-status   : {result.agent_status}")
    print(f"  attempts            : {result.attempt_count}")
    print(f"  tokens              : {result.input_tokens} in, {result.output_tokens} out")
    if result.model:
        print(f"  model               : {result.model}")
    print(f"  duration            : {result.duration_seconds:.2f}s")
    if result.validation_violations:
        print(f"  validation violations: {len(result.validation_violations)}")
        for v in result.validation_violations:
            print(f"    - {v}")
    if result.artifact_path:
        try:
            rel = result.artifact_path.relative_to(repo_root)
        except ValueError:
            rel = result.artifact_path
        print(f"  artifact            : {rel}")
    if result.debug_dir:
        try:
            rel = result.debug_dir.relative_to(repo_root)
        except ValueError:
            rel = result.debug_dir
        print(f"  debug artifacts     : {rel}/")
    if result.notes:
        print(f"  notes               : {result.notes}")
