"""Generic Manual Agent Mode infrastructure for all 5 scene-generation agents.

Provides a single registry-driven implementation of `prepare-agent` and
`validate-agent-output` for: scene-director, symbolism-tracker,
dialogue-specialist, anti-ai-editor, continuity-auditor.

Pattern (same for every agent):
    1. Read prior agents' canonical outputs from disk (or accept them in-memory)
    2. Build the agent's Bundle via the appropriate BundleAssembler method
    3. Hydrate the prompt template
    4. Write the manual prompt file under generated/manual/<agent>-prompt.md
    5. (Human pastes into Claude, saves reply to <agent>-output.yaml)
    6. Extract YAML from the saved reply
    7. Validate required top-level + required subfields per the agent's spec
    8. Write canonical artifact under generated/<spec.output_filename>
    9. Where applicable (anti-ai-editor), also extract the prose draft to
       generated/05-revised-draft.md as a convenience for the human reader.

No LLM calls anywhere in this module. The API-mode path lives separately
in scene_director_only.py.
"""

from __future__ import annotations

import logging
import time
from collections.abc import Callable
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from orchestrator.core.artifact import (
    read_markdown,
    read_yaml,
    write_markdown,
    write_yaml,
)
from orchestrator.core.bundle import Bundle, BundleAssembler
from orchestrator.core.config import Config
from orchestrator.prompts.loader import PromptLoader
from orchestrator.prompts.render import (
    extract_yaml_from_response,
    render_system_prompt,
    render_user_prompt,
)

logger = logging.getLogger("orchestrator.manual_mode")


# ─── Agent spec registry ──────────────────────────────────────────────────────

@dataclass(frozen=True)
class AgentSpec:
    """Per-agent configuration for the generic manual-mode driver."""

    agent_id: str
    output_filename: str               # canonical artifact name under generated/
    required_top_level: tuple[str, ...]
    required_subfields: dict[str, tuple[str, ...]]   # {top_key: (subfield, ...)}
    prior_agents_needed: tuple[str, ...]
    bundle_builder: Callable[[BundleAssembler, dict[str, dict[str, Any]]], Bundle]
    """Build the agent's bundle from (assembler, prior_outputs_by_agent_id)."""

    description: str = ""


def _bundle_scene_director(
    assembler: BundleAssembler, _prior: dict[str, dict[str, Any]]
) -> Bundle:
    return assembler.assemble_for_scene_director(task_id="scene:01")


def _bundle_symbolism_tracker(
    assembler: BundleAssembler, prior: dict[str, dict[str, Any]]
) -> Bundle:
    blueprint = prior["scene-director"].get("scene_blueprint", {})
    return assembler.assemble_for_symbolism_tracker(
        task_id="scene:01-symbol-audit",
        scene_blueprint=blueprint,
    )


def _bundle_dialogue_specialist(
    assembler: BundleAssembler, prior: dict[str, dict[str, Any]]
) -> Bundle:
    blueprint = prior["scene-director"].get("scene_blueprint", {})
    return assembler.assemble_for_dialogue_specialist(
        task_id="scene:01-dialogue",
        scene_blueprint=blueprint,
    )


def _bundle_anti_ai_editor(
    assembler: BundleAssembler, prior: dict[str, dict[str, Any]]
) -> Bundle:
    blueprint = prior["scene-director"].get("scene_blueprint", {})
    dialogue = prior["dialogue-specialist"].get("dialogue_draft", {})
    return assembler.assemble_for_anti_ai_editor(
        task_id="scene:01-anti-ai",
        draft=str(dialogue),
        scene_blueprint=blueprint,
    )


def _bundle_continuity_auditor(
    assembler: BundleAssembler, prior: dict[str, dict[str, Any]]
) -> Bundle:
    blueprint = prior["scene-director"].get("scene_blueprint", {})
    anti_ai = prior["anti-ai-editor"]
    revised = anti_ai.get("humanization_pass", {}).get("revised_draft", "")
    return assembler.assemble_for_continuity_auditor(
        task_id="scene:01-continuity",
        draft=str(revised),
        scene_blueprint=blueprint,
    )


AGENT_SPECS: dict[str, AgentSpec] = {
    "scene-director": AgentSpec(
        agent_id="scene-director",
        output_filename="01-scene-blueprint.yaml",
        required_top_level=("scene_blueprint",),
        required_subfields={
            "scene_blueprint": (
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
            ),
        },
        prior_agents_needed=(),
        bundle_builder=_bundle_scene_director,
        description="Produces the scene blueprint — the structural design.",
    ),
    "symbolism-tracker": AgentSpec(
        agent_id="symbolism-tracker",
        output_filename="02-symbol-audit.yaml",
        required_top_level=("audit",),
        required_subfields={
            "audit": ("scene_id", "symbols_touched"),
        },
        prior_agents_needed=("scene-director",),
        bundle_builder=_bundle_symbolism_tracker,
        description="Audits symbol state-machine legality on the scene blueprint.",
    ),
    "dialogue-specialist": AgentSpec(
        agent_id="dialogue-specialist",
        output_filename="03-dialogue-draft.yaml",
        required_top_level=("dialogue_draft",),
        required_subfields={
            "dialogue_draft": ("scene_id", "pov", "exchanges"),
        },
        prior_agents_needed=("scene-director",),
        bundle_builder=_bundle_dialogue_specialist,
        description="Drafts voice-specific dialogue for the scene.",
    ),
    "anti-ai-editor": AgentSpec(
        agent_id="anti-ai-editor",
        output_filename="04-anti-ai-report.yaml",
        required_top_level=("smell_report", "humanization_pass"),
        required_subfields={
            "humanization_pass": ("revised_draft", "applied_rules"),
        },
        prior_agents_needed=("scene-director", "dialogue-specialist"),
        bundle_builder=_bundle_anti_ai_editor,
        description="Smell scrub + humanization. Output's revised_draft IS the prose.",
    ),
    "continuity-auditor": AgentSpec(
        agent_id="continuity-auditor",
        output_filename="06-continuity-report.yaml",
        required_top_level=("audit_report",),
        required_subfields={
            "audit_report": (),    # presence-only check; structure varies
        },
        prior_agents_needed=("scene-director", "anti-ai-editor"),
        bundle_builder=_bundle_continuity_auditor,
        description="Validates against memory graph; reports only, no rewrite.",
    ),
}


ALL_AGENT_IDS: tuple[str, ...] = tuple(AGENT_SPECS.keys())


# ─── Result types ─────────────────────────────────────────────────────────────

@dataclass
class PrepareResult:
    status: str
    agent_id: str
    prompt_path: Path | None = None
    expected_output_path: Path | None = None
    manual_dir: Path | None = None
    system_chars: int = 0
    user_chars: int = 0
    duration_seconds: float = 0.0
    notes: str = ""

    @property
    def ok(self) -> bool:
        return self.status == "ok"


@dataclass
class ValidateResult:
    status: str
    agent_id: str
    output: dict[str, Any] | None = None
    artifact_path: Path | None = None
    extra_artifacts: dict[str, Path] = field(default_factory=dict)
    input_path: Path | None = None
    validation_violations: list[str] = field(default_factory=list)
    agent_status: str | None = None
    duration_seconds: float = 0.0
    notes: str = ""

    @property
    def ok(self) -> bool:
        return self.status == "ok"


# ─── Helpers ──────────────────────────────────────────────────────────────────

def _log_step(step: str, **kv: Any) -> None:
    if kv:
        logger.info("step=%s %s", step, " ".join(f"{k}={v}" for k, v in kv.items()))
    else:
        logger.info("step=%s", step)


def _load_prior_outputs(
    sample_dir: Path, needed: tuple[str, ...]
) -> dict[str, dict[str, Any]]:
    """Read each needed agent's canonical artifact from generated/."""
    out: dict[str, dict[str, Any]] = {}
    for agent_id in needed:
        spec = AGENT_SPECS[agent_id]
        path = sample_dir / "generated" / spec.output_filename
        if not path.exists():
            raise FileNotFoundError(
                f"Prior agent {agent_id!r} has not been canonized yet. "
                f"Expected file: {path}. "
                f"Run `prepare-agent {agent_id}` and `validate-agent-output {agent_id}` first."
            )
        out[agent_id] = read_yaml(path)
    return out


def _validate_schema(
    parsed: dict[str, Any], spec: AgentSpec
) -> list[str]:
    """Return list of violation messages. Empty = pass."""
    if not isinstance(parsed, dict):
        return ["top-level output is not a YAML mapping"]

    violations: list[str] = []
    for top in spec.required_top_level:
        if top not in parsed:
            violations.append(f"missing required top-level key: {top}")
            continue
        if not isinstance(parsed[top], dict):
            violations.append(f"{top} is not a mapping")
            continue
        for sub in spec.required_subfields.get(top, ()):
            if sub not in parsed[top]:
                violations.append(f"{top}.{sub} is missing")
                continue
            value = parsed[top][sub]
            if value is None or value == "" or value == [] or value == {}:
                violations.append(f"{top}.{sub} is empty")
    return violations


# ─── Manual prompt template ───────────────────────────────────────────────────

_MANUAL_PROMPT_HEADER = """\
# {agent_id} — Manual Prompt

> Generated by `python -m orchestrator prepare-agent {agent_id} --sample {sample}`
> Generated at: {timestamp}
> Mode: **Manual Agent Mode** (no Anthropic API call from the orchestrator)
> Agent role: {description}

## For the human operator

1. Open Claude (the extension in VSCode/Cursor, the web app, or any LLM chat).
2. Paste **everything below the `--- BEGIN PROMPT ---` line** into a new
   conversation.
3. Save Claude's full response to:
   ```
   {expected_output_path}
   ```
   Both `.yaml` and `.md` extensions work — the validator extracts the YAML.
4. Run:
   ```
   python -m orchestrator validate-agent-output {agent_id} \\
     --sample {sample} \\
     --input {expected_output_path}
   ```

If validation fails the orchestrator lists specific violations. Edit the
output (or re-prompt Claude) and re-run validate-agent-output.

--- BEGIN PROMPT ---

# AGENT ROLE — System Prompt

{system_prompt}

---

# TASK — User Prompt

{user_prompt}

---

# Required output

Emit a **single YAML document** wrapped in a fenced ```` ```yaml ... ``` ````
block. At minimum include these required keys:

{required_fields_list}

Do not write any prose before or after the fenced block. Output the YAML and
nothing else.
"""


def _build_required_fields_list(spec: AgentSpec) -> str:
    lines = []
    for top in spec.required_top_level:
        lines.append(f"- `{top}` (mapping)")
        for sub in spec.required_subfields.get(top, ()):
            lines.append(f"  - `{top}.{sub}`")
    return "\n".join(lines)


def _build_manual_prompt(
    *,
    spec: AgentSpec,
    sample_name: str,
    system_prompt: str,
    user_prompt: str,
    expected_output_path: Path,
    repo_root: Path,
) -> str:
    timestamp = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")

    def _rel(p: Path) -> str:
        try:
            return str(p.relative_to(repo_root)).replace("\\", "/")
        except ValueError:
            return str(p)

    return _MANUAL_PROMPT_HEADER.format(
        agent_id=spec.agent_id,
        sample=sample_name,
        description=spec.description,
        timestamp=timestamp,
        expected_output_path=_rel(expected_output_path),
        system_prompt=system_prompt.strip(),
        user_prompt=user_prompt.strip(),
        required_fields_list=_build_required_fields_list(spec),
    )


# ─── Public API: prepare ──────────────────────────────────────────────────────

def prepare_agent_prompt(
    agent_id: str,
    sample_dir: Path,
    config: Config,
    prior_outputs: dict[str, dict[str, Any]] | None = None,
) -> PrepareResult:
    """Build a manual prompt file for the given agent. No LLM call.

    `prior_outputs` is optional. If omitted, the function reads each prior
    agent's canonical artifact from disk (samples/<sample>/generated/...).
    Pass in-memory dicts to short-circuit disk reads in the interactive runner.
    """
    if agent_id not in AGENT_SPECS:
        raise ValueError(f"Unknown agent: {agent_id!r}. Known: {ALL_AGENT_IDS}")

    spec = AGENT_SPECS[agent_id]
    t0 = time.time()
    sample_dir = sample_dir.resolve()

    if not (sample_dir / "inputs").exists():
        raise FileNotFoundError(
            f"Sample missing inputs/: {sample_dir}. "
            f"Run `python -m orchestrator inspect-sample --sample {sample_dir}` to debug."
        )

    manual_dir = sample_dir / "generated" / "manual"
    manual_dir.mkdir(parents=True, exist_ok=True)
    prompt_path = manual_dir / f"{agent_id}-prompt.md"
    expected_output_path = manual_dir / f"{agent_id}-output.yaml"

    # Load prior outputs if not provided.
    if prior_outputs is None:
        prior_outputs = _load_prior_outputs(sample_dir, spec.prior_agents_needed)
    else:
        missing = [a for a in spec.prior_agents_needed if a not in prior_outputs]
        if missing:
            raise ValueError(
                f"Missing prior outputs for {agent_id}: {missing}"
            )

    # Assemble bundle for this agent.
    assembler = BundleAssembler(sample_dir=sample_dir)
    bundle = spec.bundle_builder(assembler, prior_outputs)
    _log_step(
        "bundle_loaded",
        agent=agent_id,
        sample=sample_dir.name,
        pinned_artifacts=len(bundle.pinned_artifacts),
    )

    # Load + hydrate.
    loader = PromptLoader(prompts_dir=config.prompts_dir)
    template = loader.load(agent_id)
    system_prompt = render_system_prompt(template.system_prompt_markdown)
    user_prompt = render_user_prompt(bundle)
    _log_step(
        "prompt_hydrated",
        agent=agent_id,
        template=str(template.path.relative_to(config.repo_root)),
        system_chars=len(system_prompt),
        user_chars=len(user_prompt),
    )

    # Build and write manual prompt.
    content = _build_manual_prompt(
        spec=spec,
        sample_name=sample_dir.name,
        system_prompt=system_prompt,
        user_prompt=user_prompt,
        expected_output_path=expected_output_path,
        repo_root=config.repo_root,
    )
    write_markdown(prompt_path, content)
    _log_step(
        "manual_prompt_written",
        agent=agent_id,
        path=str(prompt_path.relative_to(config.repo_root)),
        size_chars=len(content),
    )

    return PrepareResult(
        status="ok",
        agent_id=agent_id,
        prompt_path=prompt_path,
        expected_output_path=expected_output_path,
        manual_dir=manual_dir,
        system_chars=len(system_prompt),
        user_chars=len(user_prompt),
        duration_seconds=time.time() - t0,
        notes=f"manual prompt ready for {agent_id}",
    )


# ─── Public API: validate ─────────────────────────────────────────────────────

def validate_agent_output(
    agent_id: str,
    sample_dir: Path,
    input_path: Path,
    config: Config,
) -> ValidateResult:
    """Read agent's output file, extract YAML, validate schema, write artifact.

    Returns a ValidateResult. Does NOT raise on domain failures.
    """
    if agent_id not in AGENT_SPECS:
        raise ValueError(f"Unknown agent: {agent_id!r}. Known: {ALL_AGENT_IDS}")

    spec = AGENT_SPECS[agent_id]
    t0 = time.time()
    sample_dir = sample_dir.resolve()
    input_path = input_path.resolve()

    result = ValidateResult(
        status="hard_reject", agent_id=agent_id, input_path=input_path
    )

    if not input_path.exists():
        result.notes = f"input file not found: {input_path}"
        result.duration_seconds = time.time() - t0
        return result

    raw_text = read_markdown(input_path)
    if not raw_text.strip():
        result.notes = f"input file is empty: {input_path}"
        result.duration_seconds = time.time() - t0
        return result

    _log_step("output_loaded", agent=agent_id, size_chars=len(raw_text))

    parsed = extract_yaml_from_response(raw_text)
    if parsed is None:
        result.notes = (
            "could not extract YAML. Expected a ```yaml ... ``` fenced block "
            "or a pure YAML document. Edit the input or re-prompt Claude with: "
            "'Output the YAML wrapped in a single ```yaml ... ``` fenced block.'"
        )
        _log_step("yaml_extracted", agent=agent_id, success=False)
        result.duration_seconds = time.time() - t0
        return result

    _log_step(
        "yaml_extracted",
        agent=agent_id,
        success=True,
        top_level_keys=list(parsed.keys()),
    )

    result.output = parsed
    result.agent_status = parsed.get("status")

    violations = _validate_schema(parsed, spec)
    result.validation_violations = violations
    _log_step("schema_validated", agent=agent_id, violations=len(violations))

    if violations:
        result.notes = (
            f"schema validation failed: {len(violations)} violation(s)."
        )
        result.duration_seconds = time.time() - t0
        return result

    # Write canonical artifact.
    artifact_path = sample_dir / "generated" / spec.output_filename
    write_yaml(artifact_path, parsed)
    result.artifact_path = artifact_path
    _log_step(
        "artifact_written",
        agent=agent_id,
        path=str(artifact_path.relative_to(config.repo_root)),
    )

    # Special case: anti-ai-editor — extract the prose draft as a separate
    # convenience file for the human reader. This is THE STORY output.
    if agent_id == "anti-ai-editor":
        revised = (
            parsed.get("humanization_pass", {}).get("revised_draft", "")
            if isinstance(parsed.get("humanization_pass"), dict)
            else ""
        )
        if revised:
            prose_path = sample_dir / "generated" / "05-revised-draft.md"
            write_markdown(prose_path, str(revised))
            result.extra_artifacts["revised_draft"] = prose_path
            _log_step(
                "prose_extracted",
                agent=agent_id,
                path=str(prose_path.relative_to(config.repo_root)),
                chars=len(str(revised)),
            )

    result.status = "ok"
    result.duration_seconds = time.time() - t0
    result.notes = f"{agent_id} output validated and canonized"
    return result


# ─── Pretty-printers ──────────────────────────────────────────────────────────

def _rel(path: Path, root: Path) -> str:
    try:
        return str(path.relative_to(root)).replace("\\", "/")
    except ValueError:
        return str(path)


def print_prepare_summary(result: PrepareResult, repo_root: Path) -> None:
    icon = "✓" if result.ok else "✗"
    print(f"{icon} prepare-agent {result.agent_id}")
    print(f"  status              : {result.status}")
    print(f"  system prompt chars : {result.system_chars}")
    print(f"  user prompt chars   : {result.user_chars}")
    print(f"  duration            : {result.duration_seconds:.2f}s")
    if result.prompt_path:
        print(f"  manual prompt       : {_rel(result.prompt_path, repo_root)}")
    if result.expected_output_path:
        print(f"  save Claude reply to: {_rel(result.expected_output_path, repo_root)}")
    print()
    print("Next steps:")
    print("  1. Open the manual prompt file (path above)")
    print("  2. Copy the section below '--- BEGIN PROMPT ---'")
    print("  3. Paste into Claude (extension in VSCode/Cursor, or any LLM chat)")
    print("  4. Save Claude's reply to the path above")
    print(f"  5. python -m orchestrator validate-agent-output {result.agent_id} \\")
    print(f"       --sample <sample> --input <reply-path>")


def print_validate_summary(result: ValidateResult, repo_root: Path) -> None:
    icon = "✓" if result.ok else "✗"
    print(f"{icon} validate-agent-output {result.agent_id}")
    print(f"  status              : {result.status}")
    if result.agent_status:
        print(f"  agent self-status   : {result.agent_status}")
    print(f"  duration            : {result.duration_seconds:.2f}s")
    if result.input_path:
        print(f"  input               : {_rel(result.input_path, repo_root)}")
    if result.validation_violations:
        print(f"  violations          : {len(result.validation_violations)}")
        for v in result.validation_violations:
            print(f"    - {v}")
    if result.artifact_path:
        print(f"  canonical artifact  : {_rel(result.artifact_path, repo_root)}")
    for label, path in result.extra_artifacts.items():
        print(f"  + {label:18}: {_rel(path, repo_root)}")
    if result.notes:
        print(f"  notes               : {result.notes}")
