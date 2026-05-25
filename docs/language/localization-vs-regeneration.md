# Localization vs. Regeneration

The framework's stance on cross-cultural narrative production. This document establishes the contract: **AetherForge does not translate or localize. It regenerates.**

## The Three Concepts

### Translation

> *"Same scene, same realization, different surface language."*

A translator preserves propositional content and tries to preserve voice. Even excellent literary translation is **lossy at every level above the lexicon**: rhythm, emotional logic, symbol palette, silence weight, address forms, taboo handling — these do not survive a faithful translation, and a *free* translation that captures them is no longer translation but **co-authorship**.

**Use case for the framework:** none, as a default. Translation may be a downstream tool a *human* applies to canonized output, but the framework itself does not produce translations.

### Localization

> *"Same scene, same plot beats, surface adapted: idioms swapped, names changed, references substituted."*

Localization preserves the **cognitive shape of the source culture** while changing surface markers. A localized text feels "set elsewhere" but still thinks like its origin. This is the default of much commercial cross-market publishing — and is precisely what literary readers experience as inauthentic.

**Use case for the framework:** limited. Localization is appropriate only when a single source culture is canonical (e.g. the project is, in-fiction, a Vietnamese work being published in an English-language market) and the source culture's cognitive shape *is* the artistic intent. In this case the language layer adapts; the cultural layer does not.

### Narrative Regeneration

> *"The structural invariants — theme, contradiction, turn-type, graph residue — are preserved. Everything downstream is re-derived under the target culture and language profile."*

A regenerated scene is **not a translated scene with surface adjustments**. It is a different scene serving the same structural role. Two characters confront each other over an edited memory — the same scene under an English-psychological profile and under a Japanese-literary profile will have different micro-beats, different symbol objects, different dialogue scripts, different rhythm, and different ending hooks. They will not differ in:

- what theme-beat they touch
- what the turn type is
- what enters the memory graph as residue
- whether the protagonist's contradiction is honored

**Use case for the framework:** the default. Whenever the framework operates across cultures or languages, it regenerates.

## Contract: What Survives Regeneration

The following are **structural invariants** — every cultural regeneration honors them:

| Invariant | Lives in |
|---|---|
| `theme.core_question` and `theme.forbidden_resolutions` | [theme schema](../schema/theme-schema.md) |
| `theme.beats[]` and their declared `mode` per scene | theme schema + scene blueprint |
| `plot_beat.intended_turn_type` and `plot_beat.knowledge_delta` | [plot-engineer](../../prompts/agents/plot-engineer.prompt.md) output |
| `character.contradictions[]` as structural shape | [character schema](../schema/character-schema.md) |
| `character.drives.{surface, buried}` (vocabulary may shift, structure does not) | character schema |
| `scene.turn` | [scene schema](../schema/scene-schema.md) |
| `scene.residue.graph_writes` | scene schema |
| All asymmetric `KNOWS` edges in the memory graph | [memory graph](../architecture/memory-graph.md) |

If a target culture profile *cannot* serve an invariant without violating it, the orchestrator escalates. The framework does not silently mutate invariants for cultural ease.

## Contract: What Is Re-Derived

| Re-derived field | Driven by |
|---|---|
| Symbol selection | culture profile `symbolism_preferences` + [symbolism-by-culture.md](../culture/symbolism-by-culture.md) |
| Emotional rendering mode | culture profile `emotional_expression` + [emotional-expression-matrix.md](../culture/emotional-expression-matrix.md) |
| Dialogue directness | culture profile `communication_style` + [dialogue-culture-rules.md](./dialogue-culture-rules.md) |
| Silence weight | culture profile `silence_usage` |
| Micro-beat ordering | culture profile `narrative_rhythm.beat_ordering` |
| Address-form resolution | culture profile `relationship_dynamics` |
| Taboo substitution | culture profile `taboo_topics` |
| Sentence density and rhythm | language style profile `sentence_density`, `prose_rhythm` |
| Dialogue tag economy | language style profile `dialogue_tag_economy` |
| Paragraph shape | language style profile `prose_rhythm.paragraph_shape` |
| Internal monologue mode | language style profile `internal_monologue_style` |

## Why Translation Cannot Be Bolted On

A common temptation: write in English, translate downstream. This fails because:

- Generative LLMs trained on English-default literary corpus produce **English-shaped emotional logic** even when asked to "be culturally appropriate."
- Symbol palettes leak: a "cracked glass" introduced in English persists through translation; the target language now carries a foreign object in a culturally inappropriate role.
- Dialogue directness is normalized to English-psychological defaults; high-restraint profiles end up reading as evasive rather than legible.
- Pacing and breath patterns are flattened to English defaults.

Translation works *down* the cognition stack. The framework chooses to operate *up* it, where the cognition is.

## Comparison Table

| Property | Translation | Localization | Narrative Regeneration |
|---|---|---|---|
| Plot preserved | ✓ | ✓ | ✓ (structurally) |
| Theme preserved | ✓ | ✓ | ✓ |
| Surface language adapted | ✓ | ✓ | ✓ |
| Idioms / names adapted | partial | ✓ | ✓ |
| Symbol palette adapted | ✗ | partial | ✓ |
| Emotional logic adapted | ✗ | ✗ | ✓ |
| Communication norms adapted | ✗ | ✗ | ✓ |
| Pacing / rhythm adapted | ✗ | ✗ | ✓ |
| Micro-beat order adapted | ✗ | ✗ | ✓ |
| Same artifact across cultures | ✓ | ≈ | ✗ (sibling artifacts) |

## What This Means Operationally

When a project declares multiple target cultures (e.g. "publish in Vietnamese and Japanese"), the framework produces **sibling canons** — not a single canon with translations. Each sibling shares invariants but is its own work. The orchestrator tracks them as distinct artifact trees rooted at the same theme/plot tree.

## What This Means Ethically

The framework refuses to flatten a culture into "a flavor on top of an English-default mind." It treats cross-cultural production as the demanding craft it is — and refuses shortcuts that produce content the source-culture reader recognizes as fake.

This is also why the **anti-stereotype discipline** in every culture profile is non-negotiable: a regeneration that reads as a stereotyped imitation is a worse failure than a translation, because it claims to be the thing it isn't.

## Related

- [language-narrative-system.md](./language-narrative-system.md)
- [../culture/cultural-narrative-layer.md](../culture/cultural-narrative-layer.md)
- [../culture/cultural-adaptation-rules.md](../culture/cultural-adaptation-rules.md)
