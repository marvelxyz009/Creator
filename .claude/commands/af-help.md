---
description: List all AetherForge slash commands and what they do
---

Print the following help message to the user as a fenced markdown block, then ask which command they'd like to invoke. Do not modify or expand the content — print verbatim.

```
AetherForge Creator Framework — Slash Commands

  ▸ NEW USER? Start here:
  /af-start              — describe your story idea; AI asks ONLY about
                           what's missing (no cap on questions), then
                           generates input files, runs the 5-agent
                           pipeline, and presents the finished scene.

                           For zero/few questions: fill in the IDEA BRIEF
                           template at docs/idea-brief-template.md first
                           and paste it as your reply.

  ▸ PROJECT MANAGEMENT:
  /af-projects           — list every project under samples/; star marks the
                           active one; shows status per project
  /af-current            — show the active project + completion status +
                           the PROJECT.md summary in plain language
  /af-focus <name>       — set the active project. Other commands default to
                           it when you don't pass --sample.

  ▸ GENERATE OR EDIT:
  /af-create-scene       — run the 5-agent pipeline on the active project
                           (or specify --sample)
  /af-revise             — re-polish the prose of the active project
                           (re-runs anti-ai-editor + continuity-auditor)
  /af-agent <agent-id>   — run a single agent
                           agent-id ∈ {scene-director, symbolism-tracker,
                           dialogue-specialist, anti-ai-editor,
                           continuity-auditor}

  ▸ UTILITIES:
  /af-help               — show this help (you are here)
  /af-setup              — one-shot install: venv, dependencies, .env
  /af-status             — show generation status for the active project

CLI equivalents (work in any shell after `make setup` or `python scripts/setup.py`):

  python -m orchestrator focus <sample>           # set active project
  python -m orchestrator current                  # show active project
  python -m orchestrator list-projects            # list all projects
  python -m orchestrator summary [--sample <p>]   # rebuild PROJECT.md
  python -m orchestrator create-scene [--sample <p>]
  python -m orchestrator prepare-agent <agent> [--sample <p>]
  python -m orchestrator validate-agent-output <agent> [--sample <p>] --input <p>
  python -m orchestrator inspect-sample --sample <p>

What gets saved where:
  Each project lives at samples/<name>/. Inside it:
    inputs/                  — your structured premise (read-only at run time)
    generated/05-revised-draft.md   — ★ THE STORY (prose) ★
    generated/01..06-*.yaml  — canonical agent artifacts
    generated/manual/        — hydrated prompts + your saved replies
    PROJECT.md               — plain-language summary auto-maintained by the
                               orchestrator (read this to remember what you've
                               written, who's in it, and what's next)

Manual mode (slash commands + CLI both) requires no API key. The orchestrator
hydrates prompts; you (or Claude in chat) act as the agent; the orchestrator
validates the output and refreshes PROJECT.md on success.

Recommended first run:
  /af-start

For full documentation, see README.md at the repo root.
```
