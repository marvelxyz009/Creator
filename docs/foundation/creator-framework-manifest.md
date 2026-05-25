# AetherForge Creator Framework — Manifest

> **BMAD-for-Narrative**: A structured, multi-agent narrative production framework where AI does not write stories directly, but flows through a deterministic pipeline of specialized cognitive stages.

## Purpose

AetherForge Creator Framework is a methodology + toolchain for producing **long-form narrative artifacts** (novels, serialized fiction, interactive narratives, screenplays) that:

1. Maintain **thematic spine** across hundreds of thousands of words.
2. Resist the statistical regression to mean known as "AI smell".
3. Treat **character contradiction** as a first-class structural primitive.
4. Encode **memory** as a graph, not a context window.
5. Submit every generated unit to an **anti-AI revision pass** before it is considered canon.

## The Pipeline

```
Vision
  ↓
Theme
  ↓
Worldbuilding
  ↓
Character Psychology
  ↓
Plot Architecture
  ↓
Scene Design
  ↓
Dialogue
  ↓
Prose
  ↓
Revision
  ↓
Continuity Validation
  ↓
Humanization Pass
  ↓
[Canon]
```

Each stage is owned by one or more **specialized agents** with explicit input/output contracts. Outputs from a stage are **frozen artifacts** consumed by downstream stages — never re-derived ad-hoc by a single monolithic prompt.

## Non-Goals (for this phase)

- No UI.
- No backend / database deployment.
- No model fine-tuning.
- No end-user product surface.

This phase produces **documentation, schema, agent contracts, and pipeline definitions** only.

## Foundational Bets

- **Structure beats prompting.** A weak model inside a strong pipeline outperforms a strong model behind a single prompt.
- **Constraint beats creativity.** Narrative quality emerges from honored constraints (theme, voice, contradiction), not from generative freedom.
- **Revision beats generation.** First-draft output is raw material; canon is what survives the revision agents.
- **Memory beats context.** A graph of facts, relations, and emotional debts outperforms a long prompt of "previously...".

## Related

- [[core-philosophy]]
- [[narrative-laws]]
- [[narrative-pipeline]]
- [[agent-system]]
