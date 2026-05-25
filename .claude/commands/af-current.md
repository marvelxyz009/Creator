---
description: Show the active project — status, generated artifacts, and how to keep editing it
---

The user wants to see which project is currently focused and how complete it is.

## What to do

1. Run via Bash:
   ```
   python -m orchestrator current
   ```

2. The orchestrator prints something like:
   ```
   Active project : samples/my-novel-prologue
   Status         : partial (3/5)
   Canonized      :
     ✓ scene-director
     ✓ symbolism-tracker
     ✓ dialogue-specialist
   Summary        : samples/my-novel-prologue/PROJECT.md
   ```

3. Relay verbatim.

4. If `PROJECT.md` is listed, also read it and surface the most useful snippet:
   - The "What this story is about" section
   - The "Scene" section (if prose exists, include the first 30 lines of prose)
   - The "Where things are saved" table

5. Suggest the most relevant next command based on status:
   - `complete` → `/af-agent anti-ai-editor` to polish, or just open the prose file
   - `partial (N/5)` → name the next missing agent and offer `/af-agent <id>` or `/af-create-scene` to resume
   - `ready` → `/af-create-scene`
   - `empty` / no active project → `/af-start` for a new project, `/af-projects` to see options

## Don't

- Don't change focus.
- Don't run any agents.
- Don't modify any files.

Read-only command.
