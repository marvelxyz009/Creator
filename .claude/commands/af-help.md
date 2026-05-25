---
description: List all AetherForge slash commands and what they do
---

Print the following help message to the user as a fenced markdown block, then ask which command they'd like to invoke. Do not modify or expand the content — print verbatim.

```
AetherForge Creator Framework — Slash Commands

  /af-help               — show this help (you are here)
  /af-setup              — one-shot install: venv, dependencies, .env
  /af-create-scene       — generate a scene end-to-end through chat
                           (walks through all 5 agents: scene-director,
                           symbolism-tracker, dialogue-specialist,
                           anti-ai-editor, continuity-auditor)
  /af-agent <agent-id>   — run a single agent through chat
                           agent-id ∈ {scene-director, symbolism-tracker,
                           dialogue-specialist, anti-ai-editor,
                           continuity-auditor}
  /af-status             — show generation status of a sample
                           (which agents have canonical artifacts written)

CLI equivalents (work in any shell after `make setup` or `python scripts/setup.py`):

  python -m orchestrator create-scene --sample samples/mvp-scene-01
  python -m orchestrator prepare-agent <agent> --sample <path>
  python -m orchestrator validate-agent-output <agent> --sample <path> --input <path>
  python -m orchestrator inspect-sample --sample <path>

What the framework does:
  Generates literary narrative scenes through a 5-agent pipeline. Each
  agent reads structured inputs, produces structured YAML output, and
  validates against schemas. The final output (under
  samples/<sample>/generated/05-revised-draft.md) is the prose — the story.

  Manual mode (slash commands and CLI both) requires no API key. The
  orchestrator hydrates prompts, you (or Claude in chat) act as the agent,
  the orchestrator validates the output.

For full documentation, see README.md at the repo root.
```
