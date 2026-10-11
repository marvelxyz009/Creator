---
name: studio-director
description: Run a local Creator Story Studio project from prose planning to source-linked manga; resume its saved queue and route skill work without losing revisions.
---

# Studio director

The writing is the source. Manga adapts approved prose. Read project.json, current chapter artifacts and job state before work. Select genre-specific techniques from references without importing plots or characters. Do not use XEROTH rules in unrelated projects.

Use `python -m story_studio.cli --data <data-dir> status` to inspect state. `prompt <project> <chapter> <stage>` exports an exact task with selected context and skill instructions. Complete it using available text tools; use `submit` with the same prompt packet so parents cannot silently change. For images use the built-in image tool if available, inspect references before generation, then import through `page` and mark review through `approve-page` only after visual inspection.

Autonomy is scoped to the requested chapter/arc. In semi mode approve edited prose after continuity review, then continue adaptation. In auto mode passing continuity may promote prose, but never approve images without visual review. Stop on missing model, unavailable image tool, conflicting canon or failed quality after bounded repair attempts. Never fabricate a generated page, fulfilled download, or passed review.

At finish show actual files and unresolved production status. Skill instructions do not invoke Codex or image_gen by themselves: the active agent or configured provider executes them.
