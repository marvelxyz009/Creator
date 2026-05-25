# Narrative Pipeline

The core production graph. Each node is a stage; each stage is owned by one or more agents (see [[agent-system]]). Edges are **frozen artifact handoffs**, not free-form prompt chains.

## Pipeline Stages

| # | Stage | Owner Agent(s) | Input Artifact | Output Artifact |
|---|---|---|---|---|
| 1 | Vision | Vision Agent | brief, references | `vision.md` |
| 2 | Theme | Theme Architect | `vision.md` | `theme.yaml` ([[theme-schema]]) |
| 3 | Worldbuilding | World Architect | `theme.yaml` | `world.yaml` ([[world-schema]]) |
| 4 | Character Psychology | Character Psychologist | `theme.yaml`, `world.yaml` | `characters/*.yaml` ([[character-schema]]) |
| 5 | Plot Architecture | Plot Architect | all prior | `plot.yaml` (act/beat tree) |
| 6 | Scene Design | Scene Designer | `plot.yaml`, characters | `scenes/*.yaml` ([[scene-schema]]) |
| 7 | Dialogue | Dialogue Agent | scene + character voices | dialogue draft |
| 8 | Prose | Prose Agent | scene + dialogue | prose draft |
| 9 | Revision | Revision Agents | prose draft | revised draft |
| 10 | Continuity Validation | Continuity Agent | draft + [[memory-graph]] | validation report |
| 11 | Humanization | Humanization Agent | validated draft | canon-eligible draft |

## Flow Rules

1. **No backflow without explicit re-open.** A downstream stage cannot mutate an upstream artifact silently. If Scene Design discovers a character problem, it opens a *revision request* against the Character Psychology artifact, which is re-run.

2. **Artifacts are versioned.** Every regeneration creates a new version; the [[memory-graph]] points at the canon version.

3. **Context is assembled, not inherited.** Each stage receives a tailored context bundle from [[context-assembly]], not the full prior pipeline output.

4. **Failure is local.** A stage that cannot satisfy its contract fails loudly with structured diagnostics — it does not silently produce degraded output.

## Stage Detail: Generation vs. Validation

The pipeline alternates **generative stages** (1–8) with **adversarial stages** (9–11). The adversarial stages are deliberately tuned to **reject** rather than accept:

- **Revision Agents** look for [[ai-smells]] and violations of [[narrative-laws]].
- **Continuity Agent** validates against the [[memory-graph]].
- **Humanization Agent** perturbs prose away from statistical median (see [[humanization-rules]]).

A draft typically cycles through 9 → 10 → 11 multiple times before canonization.

## Related

- [[agent-system]]
- [[agent-contracts]]
- [[context-assembly]]
- [[memory-graph]]
