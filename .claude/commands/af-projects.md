---
description: List all projects under samples/ with their status, marking the active one
---

The user wants to see all narrative projects in this repo and which one is currently focused.

## What to do

1. Run via Bash:
   ```
   python -m orchestrator list-projects
   ```

2. The orchestrator prints a table like:
   ```
      Name                                Status                    Prose?
   ───────────────────────────────────────────────────────────────────────
      mvp-scene-01                        complete                  ✓
   ★  my-novel-prologue                   partial (3/5)             ·
      ghosts-and-rooms                    ready (no scene yet)      ·
   ```
   `★` marks the active project. `✓` in Prose? column means the story prose has been generated.

3. Relay the table to the user verbatim.

4. After the table, offer 3 next steps:
   - To switch focus: `/af-focus <name>`
   - To see the active project's status: `/af-current`
   - To start a new project: `/af-start`

## Don't

- Don't modify any files.
- Don't try to "fix" partial projects automatically.
