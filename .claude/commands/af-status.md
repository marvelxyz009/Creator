---
description: Show generation status for a sample (which agents have canonical artifacts)
---

The user wants to see what's been generated for a sample. Default sample: `samples/mvp-scene-01` unless they specified another via `$ARGUMENTS`.

## What to do

1. Decide the sample path:
   - If `$ARGUMENTS` is non-empty and looks like a path, use it
   - Otherwise default to `samples/mvp-scene-01`

2. Run the orchestrator's inspect command via Bash:
   ```
   python -m orchestrator inspect-sample --sample <sample-path>
   ```

3. Additionally, check which canonical artifacts exist under `samples/<sample>/generated/` using the Read or Bash (ls) tool. Build a table like:

   ```
   Agent                  Canonical artifact          Status
   ─────────────────────────────────────────────────────────
   scene-director         01-scene-blueprint.yaml     ✓ / ·
   symbolism-tracker      02-symbol-audit.yaml        ✓ / ·
   dialogue-specialist    03-dialogue-draft.yaml      ✓ / ·
   anti-ai-editor         04-anti-ai-report.yaml      ✓ / ·
                          05-revised-draft.md         ✓ / ·   ← THE STORY
   continuity-auditor     06-continuity-report.yaml   ✓ / ·
   ```

   `✓` = artifact exists, `·` = not generated yet.

4. If 05-revised-draft.md exists, offer to print it (or its first 30 lines).

5. Suggest next steps based on what's missing:
   - If nothing exists: `/af-create-scene` or `/af-agent scene-director`
   - If partial: `/af-agent <next-agent-id>`
   - If complete: tell user the story is at `samples/<sample>/generated/05-revised-draft.md`

## Do not

- Do not modify any files.
- Do not generate any agent outputs.
- Do not run prepare-agent or validate-agent-output.

This is a read-only status command.
