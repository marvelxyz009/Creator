---
description: Re-polish the prose of the active project (re-runs the anti-ai-editor on the existing scene)
---

The user wants to revise the prose of the focused project — without redoing the scene blueprint, dialogue, or other upstream stages.

## What to do

1. Verify there IS an active project:
   ```
   python -m orchestrator current
   ```
   If no active project, tell the user to run `/af-focus <name>` first and stop.

2. Verify the prerequisites exist for the anti-ai-editor:
   - `01-scene-blueprint.yaml` must exist in `samples/<active>/generated/`
   - `03-dialogue-draft.yaml` must exist in `samples/<active>/generated/`
   
   If either is missing, tell the user the upstream agents haven't been run; suggest `/af-create-scene` instead.

3. Run the anti-ai-editor by invoking `/af-agent anti-ai-editor` (or its underlying flow):
   - `python -m orchestrator prepare-agent anti-ai-editor` (uses active sample)
   - Read the hydrated prompt
   - Act as the anti-ai-editor, applying H1-H10 humanization rules
   - Write the YAML output to `samples/<active>/generated/manual/anti-ai-editor-output.yaml`
   - `python -m orchestrator validate-agent-output anti-ai-editor --input <path>`
   - On success, the orchestrator overwrites `samples/<active>/generated/05-revised-draft.md` with the new prose

4. After success:
   - Read the new prose from `05-revised-draft.md`
   - Present it to the user inside a fenced block
   - Note that `PROJECT.md` has been auto-refreshed

5. Also run continuity-auditor as a follow-up (the prose changed; the audit may need to re-run):
   - `/af-agent continuity-auditor` (or the underlying flow)
   - Report any new violations

## When this is appropriate

Use `/af-revise` for:
- Prose tightening (the most common edit)
- Removing AI smells the user noticed
- Trying a different humanization pass with the same blueprint
- Adjusting tone (the user can add a hint in their reply when acting as anti-ai-editor)

Don't use it for:
- Changing what happens in the scene (use `/af-agent scene-director` instead)
- Changing characters or theme (re-run `/af-start` for a new project rooted in those changes)
