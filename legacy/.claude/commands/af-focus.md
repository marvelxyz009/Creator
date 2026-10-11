---
description: Set the active project — subsequent commands default to this sample
---

The user wants to focus a project. `$ARGUMENTS` should be a sample name or path.

## What to do

1. Parse `$ARGUMENTS` to determine the sample path:
   - If it's a bare name like `my-novel`, treat it as `samples/my-novel`
   - If it's a path like `samples/my-novel`, use as-is
   - If empty: run `/af-projects` first and ask the user to pick

2. Verify the path exists. If not, list available projects via `python -m orchestrator list-projects` and ask the user to retype.

3. Run via Bash:
   ```
   python -m orchestrator focus <sample-path>
   ```

4. The orchestrator writes `.aetherforge/active-sample`, refreshes the sample's `PROJECT.md`, and prints confirmation.

5. After confirmation, run `/af-current` (or its equivalent — `python -m orchestrator current` via Bash) to show the project's status so the user sees what state it's in.

6. Suggest 3 follow-ups based on status:
   - If `complete`: offer `/af-agent anti-ai-editor` (re-polish prose) or open `PROJECT.md`
   - If `partial`: offer `/af-create-scene` to resume, or `/af-agent <next-id>` for the next missing agent
   - If `ready`: offer `/af-create-scene`
   - If `empty`: warn user — sample has no inputs/, suggest `/af-start` for a fresh project

## Don't

- Don't modify the sample's inputs.
- Don't auto-run agents — focusing alone doesn't trigger generation.
