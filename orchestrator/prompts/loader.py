"""Load .prompt.md template files from the repo's /prompts/ directory.

Each .prompt.md file is treated as TWO logical sections:

  1. The Markdown document itself — the agent's identity, contract,
     validation checklist, anti-patterns. This is the SYSTEM PROMPT.

  2. The runtime bundle (from BundleAssembler) — the USER PROMPT. Composed by
     orchestrator.prompts.render with Jinja2.

For MVP, prompt templates are loaded raw. A future version may parse YAML
frontmatter blocks inside the Markdown to drive bundle assembly automatically.
"""

from __future__ import annotations

import logging
from dataclasses import dataclass
from pathlib import Path

logger = logging.getLogger(__name__)


@dataclass(frozen=True)
class PromptTemplate:
    """A loaded prompt template."""

    agent_id: str
    path: Path
    system_prompt_markdown: str

    @property
    def name(self) -> str:
        return self.agent_id


class PromptLoader:
    """Loads prompt templates from prompts_dir.

    Layout assumed:
        prompts/
          agents/<agent-id>.prompt.md
          culture/<agent-id>.prompt.md
          shared/<...>.md          (inheritance docs; loaded as-needed)
          workflows/<...>.md
    """

    def __init__(self, prompts_dir: Path):
        self.prompts_dir = prompts_dir.resolve()
        if not self.prompts_dir.exists():
            raise FileNotFoundError(f"Prompts directory not found: {self.prompts_dir}")

    def load(self, agent_id: str) -> PromptTemplate:
        """Find and load <agent_id>.prompt.md. Searches agents/ and culture/."""
        candidates = [
            self.prompts_dir / "agents" / f"{agent_id}.prompt.md",
            self.prompts_dir / "culture" / f"{agent_id}.prompt.md",
        ]
        for path in candidates:
            if path.exists():
                content = path.read_text(encoding="utf-8")
                logger.debug("Loaded prompt template: %s", path)
                return PromptTemplate(
                    agent_id=agent_id,
                    path=path,
                    system_prompt_markdown=content,
                )
        raise FileNotFoundError(
            f"No prompt template found for agent {agent_id!r}. Searched: {candidates}"
        )

    def load_shared(self, name: str) -> str:
        """Load a shared markdown file (e.g. global-narrative-rules.md)."""
        path = self.prompts_dir / "shared" / f"{name}.md"
        if not path.exists():
            raise FileNotFoundError(f"Shared prompt file not found: {path}")
        return path.read_text(encoding="utf-8")
