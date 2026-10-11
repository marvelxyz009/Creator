---
name: creator-studio
description: Operate a multi-genre prose and manga workshop entirely in chat, ask creative choices here, generate images with session tools, and persist local canon, revisions and progress.
---

# Creator chat workshop

Work inside the current conversation. Use its text reasoning and image tools; do not launch a UI, HTTP server, provider API or nested Codex/Claude process. Find the repo from CREATOR_HOME, the current workspace, or D:/Creator on this machine. Run file commands from that repo. Read AGENTS.md and story_studio/skills/studio-director/SKILL.md. The default data folder is <repo>/stories; STUDIO_DATA or --data overrides it. Existing .studio data can be opened explicitly; never delete or silently migrate it.

## Start and choose

Inspect `python -m story_studio status` first. On a new story use `start --seed "optional preference"`. Compose 2–4 distinct concept proposals (default 3; use 2 for a narrow decision or 4 only when four genuinely different directions help) in the chat using story-architect. Save a UTF-8 JSON array through `offer <session> <file>`: each option has title, summary, tradeoff and genres from the catalog. Present short choices and ask directly in chat using the available question tool. Wait for the human's answer; do not infer approval from silence. Convert numbered user options to zero-based indices within the saved set in `choose <session> <index> <proposal_revision>`.

Repeat with 2–4 story directions (default 3) (also length: short/novella/novel/series), then 2–4 art directions (default 3) (also direction: rtl/ltr/vertical). Condition each round on saved earlier choices. Regeneration uses offer and gets a new revision; do not apply an answer to obsolete options. Let the assistant infer title, settings, style and format, respecting stated constraints. After three choices the project is saved automatically. User corrections override defaults; avoid re-asking already settled choices.

## Write and resume

Use `resume <project> --chapter N` before continuing. Respect current non-stale canon, knowledge boundaries, seeds, character identities and the chosen emotional promise. Route specialist work through story-architect, character-designer, art-director, prose-writer and series-memory. Produce writing inside the active chat.

For every stage prepare `prompt <project> N <stage> task.json`, read its context, write the actual output file, then `submit <project> N <stage> task.json output.md`. The packet pins parent revisions. Stages are bible, outline, characters, art, draft, edit, continuity, adaptation, storyboard, lettering, image_prompt. Use approve for edited prose only after its matching passing continuity audit. An audit failure means revise the prose and re-audit; do not silently promote it. Checkpoint after approvals and imports; commands automatically update progress.md and progress.json. Keep chapter and phase scale proportional to the story.

## Draw here, save locally

Adapt approved current prose into source-linked scenes, page plans and exact dialogue. Use the active session's native image-generation/edit tool (imagegen in Codex when available), following that tool's skill. Inspect local references before editing. Use real reference sheets and include them in tool calls; do not invent that a sheet exists. Before generating prepare `image-task <project> N <page-number> image-task.json` to pin the approved prose and brief. Generate one proof page before scaling a chapter. For a new or rejected rendering, read [art review and approval](references/art-approval.md), inspect the actual proof and obtain human style approval before scaling. A technical pass or an art-direction title is not that approval. Preserve character identity and design balloons together with composition.

Persist the actual generated PNG using a local file returned by the tool or its supported artifact export. Import with `page <project> N <page-number> <absolute-png-path> --packet image-task.json`. No screenshots or programmatic drawings as substitutes for manga; no separate CLI/MCP credential setup for this workflow. If the session cannot generate or export an image, explain that concrete limitation rather than making a placeholder.

Read the actual generated image, not just its prompt. Review composition, acting, continuity, lettering, exact Vietnamese text and reading order. Save review JSON with image_sha256 of the imported PNG, inspected=true only after viewing, pass, notes, issues, expected_dialogue and observed_dialogue. Record via `review-page <project> <page-artifact> review.json`. Failed review is retained and does not approve. Repair with the session's image edit tool, import the new page revision, inspect again, and record a new review. Default to at most two targeted self-repairs per review round before presenting the unresolved tradeoff. If the user explicitly authorizes iteration until approval, continue in human review rounds under the linked art-review procedure; never claim an unseen image or unapproved style passed.

## Finish

Use export for approved prose and cbz for reviewed manga. Link actual local files and show actual images in chat. Keep project content local and ignored by Git; commit/push code or skills when requested. At the end record progress, pending choices, last approved source and next step. Do not promise background work after the chat stops.

## Multi-page image consistency

Before drawing pages, create and visually inspect a canonical reference pack: character turnaround or portrait sheet, expression sheet, signature costume/props and one art-style proof. Save actual images and a visual continuity ledger under the project's local references folder. Record character ID, file path, what was inspected, identity invariants, scene-dependent appearance and the current approved reference revision. A planned sheet is not a reference image.

Use the same approved identity images in every generation/edit call where that character appears; prepare an anchor page to validate acting, face and lettering before producing a chapter. Do not regenerate a character's face from prose descriptions each page. Keep permanent traits separate from costumes, injuries, dirt and lighting. Attach the preceding approved scene/page when it helps spatial and state continuity, while clearly requesting a new composition.

Review a new page beside canonical references and the preceding accepted page. Track face proportions, age, silhouette, hair, distinguishing marks, body build, costume closures, injury side, prop hand and screen direction. Record which actual reference files were viewed, observed differences and whether each is intentional. If identity drifts, edit the affected panel using the canonical references rather than regenerating the whole chapter. Preserve already successful acting, layout and dialogue. Stop to resolve conflicting references instead of averaging different faces. Never describe this process as a guarantee that an image model cannot drift.
