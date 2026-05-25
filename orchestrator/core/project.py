"""Project management — active sample focus + human-readable project summary.

A "project" in this MVP is a sample directory (samples/<name>/). Each project
has:
  - inputs/                   the structured YAML the agents consume
  - generated/                the artifacts the agents produce
  - PROJECT.md                human-readable summary (auto-maintained here)

Active project state is a single text file at .aetherforge/active-sample
(gitignored — per-contributor).
"""

from __future__ import annotations

import logging
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path

from orchestrator.core.artifact import read_optional_yaml

logger = logging.getLogger(__name__)


# ─── Active-sample persistence ────────────────────────────────────────────────

def _state_dir(repo_root: Path) -> Path:
    return repo_root / ".aetherforge"


def _active_sample_file(repo_root: Path) -> Path:
    return _state_dir(repo_root) / "active-sample"


def get_active_sample(repo_root: Path) -> Path | None:
    """Return the currently focused sample directory, or None if unset."""
    path = _active_sample_file(repo_root)
    if not path.exists():
        return None
    text = path.read_text(encoding="utf-8").strip()
    if not text:
        return None
    target = (repo_root / text).resolve()
    if not target.exists():
        logger.warning("Active sample %s no longer exists on disk", target)
        return None
    return target


def set_active_sample(repo_root: Path, sample_dir: Path) -> None:
    """Pin a sample as the focused project."""
    sample_dir = sample_dir.resolve()
    try:
        rel = sample_dir.relative_to(repo_root)
    except ValueError:
        rel = sample_dir
    state = _state_dir(repo_root)
    state.mkdir(parents=True, exist_ok=True)
    (state / "active-sample").write_text(str(rel).replace("\\", "/") + "\n", encoding="utf-8")
    logger.info("Active sample set to %s", rel)


def clear_active_sample(repo_root: Path) -> None:
    path = _active_sample_file(repo_root)
    if path.exists():
        path.unlink()


# ─── Project listing ──────────────────────────────────────────────────────────

@dataclass
class ProjectInfo:
    sample_dir: Path
    name: str
    has_inputs: bool
    canonized_agents: list[str]          # which agents have canonical artifacts
    has_prose: bool                      # 05-revised-draft.md exists
    is_active: bool

    @property
    def status_label(self) -> str:
        if self.has_prose:
            return "complete"
        if self.canonized_agents:
            return f"partial ({len(self.canonized_agents)}/5)"
        if self.has_inputs:
            return "ready (no scene yet)"
        return "empty"


_AGENT_OUTPUT_FILES: list[tuple[str, str]] = [
    ("scene-director", "01-scene-blueprint.yaml"),
    ("symbolism-tracker", "02-symbol-audit.yaml"),
    ("dialogue-specialist", "03-dialogue-draft.yaml"),
    ("anti-ai-editor", "04-anti-ai-report.yaml"),
    ("continuity-auditor", "06-continuity-report.yaml"),
]


def _inspect_sample(sample_dir: Path, active: Path | None) -> ProjectInfo:
    generated = sample_dir / "generated"
    canonized = [
        agent_id
        for agent_id, fname in _AGENT_OUTPUT_FILES
        if (generated / fname).exists()
    ]
    return ProjectInfo(
        sample_dir=sample_dir,
        name=sample_dir.name,
        has_inputs=(sample_dir / "inputs").exists(),
        canonized_agents=canonized,
        has_prose=(generated / "05-revised-draft.md").exists(),
        is_active=(active is not None and sample_dir.resolve() == active.resolve()),
    )


def list_projects(repo_root: Path) -> list[ProjectInfo]:
    """List all samples (= projects in MVP) under samples/."""
    samples_dir = repo_root / "samples"
    if not samples_dir.exists():
        return []
    active = get_active_sample(repo_root)
    projects = []
    for entry in sorted(samples_dir.iterdir()):
        if not entry.is_dir():
            continue
        if entry.name.startswith("."):
            continue
        projects.append(_inspect_sample(entry, active))
    return projects


# ─── Human-readable PROJECT.md ────────────────────────────────────────────────

def _h(line: str, level: int = 1) -> str:
    return f"{'#' * level} {line}\n\n"


def _summarize_character(data: dict) -> str:
    c = data.get("character") or data
    name = c.get("name", "?")
    role = c.get("role", "?")
    contradictions = c.get("contradictions") or []
    drives = c.get("drives") or {}
    parts = [f"**{name}** — {role}"]
    if contradictions:
        forces = contradictions[0].get("forces") or {}
        a, b = forces.get("a", "?"), forces.get("b", "?")
        parts.append(f"  - Contradiction: *{a}* vs *{b}*")
    surface = drives.get("surface")
    buried = drives.get("buried")
    if surface or buried:
        parts.append(f"  - Wants on the surface: *{surface or '—'}*")
        parts.append(f"  - Wants underneath: *{buried or '—'}*")
    voice = c.get("voice_signature") or {}
    refuse = voice.get("what_they_refuse_to_name") or []
    if refuse:
        parts.append(f"  - Refuses to name: {', '.join(f'`{x}`' for x in refuse[:4])}")
    return "\n".join(parts) + "\n"


def _summarize_scene(generated_dir: Path) -> tuple[str, str | None]:
    """Return (summary_block_markdown, prose_path_str_or_None)."""
    blueprint = read_optional_yaml(generated_dir / "01-scene-blueprint.yaml") or {}
    sb = blueprint.get("scene_blueprint") or {}

    purpose = sb.get("purpose") or {}
    purpose_text = (
        purpose.get("one_sentence")
        if isinstance(purpose, dict)
        else (purpose if isinstance(purpose, str) else None)
    )
    turn = sb.get("turn") or {}
    turn_type = turn.get("type") if isinstance(turn, dict) else None
    turn_desc = turn.get("description") if isinstance(turn, dict) else None
    ending = sb.get("ending_hook") or {}
    ending_type = ending.get("type") if isinstance(ending, dict) else None
    ending_desc = ending.get("description") if isinstance(ending, dict) else None

    parts = []
    if purpose_text:
        parts.append(f"**Why this scene exists:** {purpose_text}\n")
    if turn_type:
        parts.append(f"**What changes:** `{turn_type}`" + (f" — {turn_desc}" if turn_desc else "") + "\n")
    if ending_type:
        parts.append(f"**How it ends:** `{ending_type}`" + (f" — {ending_desc}" if ending_desc else "") + "\n")

    prose_path = generated_dir / "05-revised-draft.md"
    prose_str = None
    if prose_path.exists():
        prose_str = prose_path.read_text(encoding="utf-8").rstrip()
        parts.append("\n**Prose:**\n\n")
        parts.append("```\n" + prose_str + "\n```\n")
    else:
        parts.append("_(Prose not yet generated — run `/af-agent anti-ai-editor` or `/af-create-scene`.)_\n")

    continuity = read_optional_yaml(generated_dir / "06-continuity-report.yaml") or {}
    ar = continuity.get("audit_report") or {}
    hv = ar.get("hard_violations")
    if hv is not None:
        n = len(hv) if isinstance(hv, list) else 0
        parts.append(f"\n**Continuity audit:** {n} hard violation(s).\n")

    return "\n".join(parts), (str(prose_path) if prose_path.exists() else None)


def build_project_summary(sample_dir: Path, repo_root: Path) -> str:
    """Build a self-contained Markdown summary of the project for the author."""
    sample_dir = sample_dir.resolve()
    inputs = sample_dir / "inputs"
    generated = sample_dir / "generated"

    out: list[str] = []
    out.append(_h(sample_dir.name, 1))
    ts = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")
    out.append(f"> Auto-generated by AetherForge — last updated {ts}\n\n")
    out.append(
        "> This file is a plain-language map of your project. Read top-to-bottom "
        "to remember what you're writing, who's in it, and what's been generated.\n\n"
    )

    # ─ What this story is about ─
    vision = read_optional_yaml(inputs / "vision.yaml") or {}
    theme = read_optional_yaml(inputs / "theme.yaml") or {}
    v = vision.get("vision") or {}
    t = theme.get("theme") or {}

    out.append(_h("What this story is about", 2))
    if v.get("one_sentence"):
        out.append(f"_{v['one_sentence']}_\n\n")
    if t.get("core_question"):
        out.append(f"**Core question:** {t['core_question']}\n\n")

    emo = (v.get("emotional_intent") or {}).get("primary")
    if emo:
        out.append(f"**Emotional intent:** {emo}\n\n")

    refusals = v.get("refusals") or []
    forbidden = t.get("forbidden_resolutions") or []
    if refusals or forbidden:
        out.append(_h("What this work refuses", 3))
        for r in refusals:
            out.append(f"- {r}\n")
        for r in forbidden:
            out.append(f"- (forbidden resolution) {r}\n")
        out.append("\n")

    # ─ Characters ─
    out.append(_h("Characters", 2))
    char_dir = inputs / "characters"
    if char_dir.exists():
        for char_file in sorted(char_dir.glob("*.yaml")):
            char_data = read_optional_yaml(char_file) or {}
            out.append(_summarize_character(char_data))
            out.append("\n")
    else:
        out.append("_(No character files found.)_\n\n")

    # ─ World ─
    world = (read_optional_yaml(inputs / "world.yaml") or {}).get("world") or {}
    if world:
        out.append(_h("World", 2))
        if world.get("name"):
            out.append(f"**{world['name']}**\n\n")
        if world.get("premise"):
            out.append(f"{world['premise']}\n\n")

    # ─ The scene(s) ─
    out.append(_h("Scene", 2))
    if generated.exists():
        scene_md, prose_path = _summarize_scene(generated)
        out.append(scene_md)
        out.append("\n")
    else:
        out.append("_(No scene has been generated yet — run `/af-create-scene`.)_\n\n")

    # ─ Files ─
    out.append(_h("Where things are saved", 2))
    out.append("| What | Path |\n|---|---|\n")
    out.append(f"| Project inputs (read-only) | `{inputs.relative_to(repo_root).as_posix()}/` |\n")
    out.append(
        f"| Generated artifacts | `{generated.relative_to(repo_root).as_posix() if generated.exists() else (sample_dir.relative_to(repo_root) / 'generated').as_posix()}/` |\n"
    )
    if (generated / "05-revised-draft.md").exists():
        out.append(
            f"| ★ Prose (THE STORY) | `{(generated / '05-revised-draft.md').relative_to(repo_root).as_posix()}` |\n"
        )
    out.append(f"| This summary | `{(sample_dir / 'PROJECT.md').relative_to(repo_root).as_posix()}` |\n")
    out.append("\n")

    # ─ How to keep working ─
    out.append(_h("Editing this project", 2))
    rel = sample_dir.relative_to(repo_root).as_posix()
    out.append("All editing commands run against this project — first focus it:\n\n")
    out.append("```\n")
    out.append(f"python -m orchestrator focus {rel}\n")
    out.append("```\n\n")
    out.append("Then in a Claude Code chat:\n\n")
    out.append("| Want to... | Command |\n|---|---|\n")
    out.append("| Polish the prose only | `/af-agent anti-ai-editor` |\n")
    out.append("| Re-do the scene structure | `/af-agent scene-director` |\n")
    out.append("| Re-do the dialogue | `/af-agent dialogue-specialist` |\n")
    out.append("| Re-run all 5 agents | `/af-create-scene` |\n")
    out.append("| Add another scene (multi-scene workflow) | _planned — see roadmap_ |\n")
    out.append("\n")

    return "".join(out)


def write_project_summary(sample_dir: Path, repo_root: Path) -> Path:
    """Build + write PROJECT.md for the sample. Returns the path."""
    content = build_project_summary(sample_dir, repo_root)
    target = sample_dir / "PROJECT.md"
    target.write_text(content, encoding="utf-8")
    logger.info("Wrote project summary: %s", target.relative_to(repo_root))
    return target
