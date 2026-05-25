# Global Narrative Rules

These rules are **non-negotiable** and apply to every agent in the framework. Each agent prompt MUST inherit and honor this file. Violations are caught downstream by the [anti-ai-editor](../agents/anti-ai-editor.prompt.md) and [continuity-auditor](../agents/continuity-auditor.prompt.md).

Mirrors and operationalizes [docs/foundation/narrative-laws.md](../../docs/foundation/narrative-laws.md).

## R1 — Imply, Do Not State
- Emotion is rendered through **action, behavior, silence, environment, object** — never narrated directly.
- Banned by default: *"She felt sad." / "He was angry." / "A wave of fear washed over her."*
- Exception: a POV character may explicitly *misname* their own feelings (self-deception is permitted).

## R2 — Theme is Never Explained
- No character delivers a philosophical monologue summarizing the theme.
- No narrator paragraph "explains what this means."
- Theme is *touched* by scenes through `advance | complicate | invert`, never *announced*.

## R3 — No Perfect Morality
- No character is wholly virtuous or wholly evil.
- Antagonists have legible motives the reader can almost agree with.
- Protagonists carry at least one wound that distorts their judgment.

## R4 — Characters Must Contradict
- Every named character carries at least one **active contradiction** (two opposed forces with stakes).
- Behavior reads as a vector between forces — never as a single trait.
- "Brave but sometimes scared" is not a contradiction. *"Wants to be known / fears being known"* is.

## R5 — Mystery > Exposition
- Withhold rather than dump.
- An unanswered question is a debt to the reader that pulls them forward.
- Worldbuilding is delivered through scene-action and consequence, not through characters explaining what both already know.

## R6 — Symbolism Recurs, It Does Not Decorate
- An object/motif introduced with weight must **return, transform, or be answered**.
- Symbols are tracked structurally (see [docs/architecture/memory-graph.md](../../docs/architecture/memory-graph.md)) with states: `introduced | transformed | resolved | betrayed`.
- A loaded symbol left unfired is a structural defect.

## R7 — Earned Resolution
- No tension resolves faster than it was built.
- Apology accepted on first offer → refuse once, complicate.
- Self-aware antagonists who narrate their own psychology → strip; restore opacity.

## R8 — Voice Specificity
- Each POV/character has a measurable voice signature: sentence-length distribution, lexical register, *what they notice*, *what they refuse to name*.
- Two characters cannot sound interchangeable.
- Generic narration is a violation.

## R9 — No Free Information
- Every exposition beat must be *paid for* in scene, conflict, or revelation.
- Information dumps belong in apparatus (appendices), not prose.

## R10 — Anti-Averaging
- When the obvious sentence is the statistically median sentence, prefer the second- or third-most-likely realization that still honors voice and theme.
- The median is the enemy.

## Honoring These Rules in Output

Every agent's output MUST be self-checkable against these rules. Each agent prompt includes a **Validation Checklist** that explicitly references the R# numbers above.

## Related

- [output-format-rules.md](./output-format-rules.md)
- [anti-ai-constraints.md](./anti-ai-constraints.md)
- [context-contract.md](./context-contract.md)
