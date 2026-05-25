"""Configuration: env loading + path resolution.

Single source of truth for environment variables and well-known repo paths.
All other modules import paths from here rather than computing them ad-hoc.
"""

from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path

from dotenv import load_dotenv

# Load .env from the repo root (if present). load_dotenv is idempotent.
load_dotenv()


def _find_repo_root(start: Path) -> Path:
    """Walk up from `start` to find the repo root (marker: pyproject.toml)."""
    cur = start.resolve()
    for parent in (cur, *cur.parents):
        if (parent / "pyproject.toml").exists():
            return parent
    # Fallback: two directories up from this file (orchestrator/core/config.py → repo root).
    return Path(__file__).resolve().parents[2]


@dataclass(frozen=True)
class Config:
    """Resolved configuration. Frozen so it can be passed around safely."""

    # Paths (all absolute)
    repo_root: Path
    docs_dir: Path
    prompts_dir: Path
    schema_dir: Path
    samples_dir: Path
    runs_dir: Path

    # LLM
    anthropic_api_key: str
    anthropic_model: str
    anthropic_max_tokens: int

    # Runtime
    log_level: str

    @property
    def has_api_key(self) -> bool:
        return bool(self.anthropic_api_key and self.anthropic_api_key.startswith("sk-"))


def load_config() -> Config:
    """Build a Config from the environment + repo layout.

    Does not validate the API key — the LLM client validates on first use.
    """
    repo_root_env = os.environ.get("AETHERFORGE_REPO_ROOT")
    repo_root = Path(repo_root_env).resolve() if repo_root_env else _find_repo_root(Path(__file__))

    runs_dir_env = os.environ.get("AETHERFORGE_RUNS_DIR")
    runs_dir = (
        Path(runs_dir_env).resolve()
        if runs_dir_env
        else (repo_root / "orchestrator" / "runs")
    )

    return Config(
        repo_root=repo_root,
        docs_dir=repo_root / "docs",
        prompts_dir=repo_root / "prompts",
        schema_dir=repo_root / "schema",
        samples_dir=repo_root / "samples",
        runs_dir=runs_dir,
        anthropic_api_key=os.environ.get("ANTHROPIC_API_KEY", ""),
        anthropic_model=os.environ.get("ANTHROPIC_MODEL", "claude-opus-4-7"),
        anthropic_max_tokens=int(os.environ.get("ANTHROPIC_MAX_TOKENS", "4096")),
        log_level=os.environ.get("AETHERFORGE_LOG_LEVEL", "INFO"),
    )
