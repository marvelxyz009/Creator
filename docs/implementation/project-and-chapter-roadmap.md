# Project & Chapter Roadmap

What the orchestrator can do today vs. what's documented but not yet implemented. This file answers the recurring author questions: *where is my story saved, how do I switch between projects, how do chapters work, how do I see what I have in plain language?*

## Today — single-scene projects with focus + readable summary

### What's built

Each project is a sample directory: `samples/<name>/`. The orchestrator tracks an **active project** at `.aetherforge/active-sample` (gitignored — per-contributor). Most commands default to the active project when `--sample` is omitted.

| Capability | CLI | Slash |
|---|---|---|
| Start a new project from an idea | (no CLI yet — use slash) | `/af-start` |
| List all projects with status | `list-projects` | `/af-projects` |
| Set the active project | `focus <sample>` | `/af-focus <name>` |
| Show active project + summary | `current` | `/af-current` |
| Rebuild human-readable summary | `summary [--sample <p>]` | _(auto-runs on success)_ |
| Generate scene end-to-end | `create-scene [--sample <p>]` | `/af-create-scene` |
| Polish prose only | `prepare/validate anti-ai-editor` | `/af-revise` |
| Run one specific agent | `prepare-agent <id>; validate-agent-output <id>` | `/af-agent <id>` |

### Where things live per project

```
samples/<project>/
├── PROJECT.md                ★ plain-language summary, auto-maintained
├── inputs/                     structured premise (read-only at run time)
│   ├── vision.yaml
│   ├── theme.yaml
│   ├── world.yaml
│   ├── plot_beat.yaml
│   ├── memory_graph_excerpt.yaml
│   └── characters/
│       ├── <name1>.yaml
│       └── <name2>.yaml
└── generated/                  artifacts written by agents (gitignored)
    ├── 01-scene-blueprint.yaml
    ├── 02-symbol-audit.yaml
    ├── 03-dialogue-draft.yaml
    ├── 04-anti-ai-report.yaml
    ├── 05-revised-draft.md   ★ THE STORY (prose)
    ├── 06-continuity-report.yaml
    └── manual/                 per-agent hydrated prompts + saved Claude replies
```

`PROJECT.md` is the file an author opens to remember: what the story is about, who the characters are, what scene has been generated, where the prose lives, and which commands edit what. The orchestrator regenerates it after every successful `validate-agent-output` and after `focus`.

### What's stable now

- One scene per project.
- Single canonical prose at `generated/05-revised-draft.md`.
- All editing commands work on the active project unless explicitly overridden.
- All validators (schema, continuity) run as before — the project layer is additive, not a refactor.

---

## Planned — multi-scene projects (Milestone 7)

The framework documentation already describes the structure ([scene-generation-workflow](../../prompts/workflows/scene-generation-workflow.md), [chapter-generation-workflow](../../prompts/workflows/chapter-generation-workflow.md)) and a hand-authored sample ([samples/chapter-01-baseline/](../../samples/chapter-01-baseline/)). The orchestrator does not yet implement it.

### Target structure

```
samples/<project>/
├── PROJECT.md
├── shared/                     theme/world/characters shared across all scenes
│   ├── vision.yaml
│   ├── theme.yaml
│   ├── world.yaml
│   └── characters/
└── scenes/
    ├── scene-01/
    │   ├── plot_beat.yaml      per-scene plot beat
    │   ├── memory_graph_excerpt.yaml   snapshot at scene start
    │   ├── SCENE.md            per-scene plain-language summary
    │   └── generated/
    │       └── ... (canonical artifacts + prose)
    ├── scene-02/
    └── ...
```

### What this enables

- Multiple scenes share theme/world/characters automatically.
- Each scene's `memory_graph_excerpt.yaml` inherits residue from the previous scene's `06-continuity-report.yaml` — the graph propagates.
- `PROJECT.md` becomes a TOC: every scene's prose appears in reading order with cross-scene structural commentary.
- Per-scene `SCENE.md` captures: what beat it serves, what residue it leaves, how it relates to neighbors.

### CLI / slash additions planned

| Capability | Likely CLI | Likely slash |
|---|---|---|
| Add a new scene to the active project | `add-scene` | `/af-add-scene` |
| List scenes in active project | `list-scenes` | `/af-scenes` |
| Generate one specific scene | `create-scene --scene <id>` | `/af-create-scene <id>` |
| Read the full chapter as prose | `read-chapter` | `/af-read` |
| Propagate memory-graph residue forward | (automatic on canonization) | — |

---

## Planned — chapter-level audits (Milestone 8)

Documented in [`prompts/workflows/chapter-generation-workflow.md`](../../prompts/workflows/chapter-generation-workflow.md). After all scenes in a chapter are canonized, run the 5 chapter-level audits:

- **3a — theme arc coherence** — distribution of advance / complicate / invert across scenes
- **3b — voice continuity** — per POV across scenes
- **3c — symbol rhythm** — arc completeness + over-recurrence detection
- **3d — debt pressure curve** — which debts spike / retire / persist
- **3e — anti-AI second pass** — cross-scene metaphor reuse, voice drift

The hand-authored sample [`samples/chapter-01-baseline/`](../../samples/chapter-01-baseline/) shows the audit outputs in their final form. The orchestrator needs to:
- Schedule audits when chapter is "complete" (all declared scenes canonized)
- Invoke each audit as a single agent (manual mode = `/af-agent <audit-id>`)
- Surface findings in a chapter-level `CHAPTER.md`

---

## Planned — cross-cultural sibling projects (Milestone 9)

Documented in [`docs/language/localization-vs-regeneration.md`](../language/localization-vs-regeneration.md). Sibling canons under different culture profiles.

```
samples/<project>/
├── shared-invariants.yaml      theme + plot beats + character contradictions
└── siblings/
    ├── english-psychological/  (one sibling per culture profile)
    ├── japanese-literary/
    └── vietnamese-literary/
```

Hand-authored sample exists at [`samples/cross-cultural-scene-01/`](../../samples/cross-cultural-scene-01/). Orchestrator integration deferred.

---

## What is NOT planned

- A GUI / web UI. The framework remains repo-based + chat-driven.
- Auto-publishing (ebook export, etc.) — out of scope.
- Multi-author collaboration features (merge conflicts on PROJECT.md etc.) — handled by git, not the orchestrator.
- Real-time collaboration. The framework is single-user-at-a-time per project.

---

## How to follow progress

This file lists what's planned. Status of each item:

| Item | Status |
|---|---|
| Active-project focus | ✓ shipped |
| `PROJECT.md` auto-summary | ✓ shipped |
| `/af-projects`, `/af-focus`, `/af-current`, `/af-revise` | ✓ shipped |
| Multi-scene structure | ⬜ planned (Milestone 7) |
| Chapter-level audits | ⬜ planned (Milestone 8) |
| Cross-cultural siblings in orchestrator | ⬜ planned (Milestone 9) |

When a milestone ships, this table updates.
