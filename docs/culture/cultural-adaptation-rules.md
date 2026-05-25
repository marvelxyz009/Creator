# Cultural Adaptation Rules

The rules the **Cultural Adapter agent** follows when regenerating a scene blueprint for a target culture profile. These rules sit on top of the [global-narrative-rules](../../prompts/shared/global-narrative-rules.md) — they do not replace them.

## The Invariant Set (do NOT change)

When adapting, these MUST survive intact:

- `theme.core_question` and `theme.forbidden_resolutions`
- `plot_beat.theme_mode` and `plot_beat.intended_turn_type`
- `character.contradictions` and `character.drives.{surface, buried}` *as structural shapes* — surface vocabulary may change
- `scene.turn` (the moment of change)
- `scene.residue.graph_writes` (what enters the memory graph)
- All asymmetric `KNOWS` edges

If a culture's typical scene logic would violate one of these, the adapter rewrites the *staging* — not the invariant. If the invariant truly cannot be served by the culture's logic, the adapter **escalates** rather than silently mutating.

## The Re-Derivation Set (DO change)

For each scene the adapter re-resolves:

1. **Symbol selection** — from culture profile's `symbolism_preferences` and ([symbolism-by-culture.md](./symbolism-by-culture.md)). The symbol's *arc-role* is preserved; the *object* is swapped.
2. **Emotional rendering mode** — per [emotional-expression-matrix.md](./emotional-expression-matrix.md) and the culture profile's `emotional_expression` field.
3. **Dialogue directness gradient** — how confrontation, refusal, apology, accusation are staged.
4. **Silence weight** — how much of the scene is carried by what is NOT said vs. what is said.
5. **Environmental storytelling weight** — how much emotion is projected onto setting, weather, light, season.
6. **Micro-beat ordering** — some cultures front-load context and back-load the turn; others invert.
7. **Social hierarchy enactment** — who speaks first, who interrupts, who refuses to interrupt, who is addressed by which form.
8. **Taboo handling** — what is *not* allowed to be said directly, and what substitutes for it.

## The Substitution Rules

### Rule CA1 — Arc-Role Preservation in Symbol Swap

A symbol's *function in the arc* is preserved. Its *manifestation* is swapped to one the culture profile authorizes.

> Example: `sym:cracked-glass` (English psychological palette) → `sym:cracked-teacup` (East-Asian domestic palette). Both serve the role "introduced as a small domestic damage that returns as evidence of body-knowledge." The swap is legal only if the new object can hold the same state machine (`introduced → transformed → resolved | betrayed`).

### Rule CA2 — Directness Translation

A scene's *epistemic conflict* (e.g. accusation, confession, refusal) is preserved. Its *directness* is gradient-shifted to the culture profile's `conflict_style`.

> Example: a direct accusation ("You edited my memory.") in one profile becomes, in a high-restraint profile, a question that contains the accusation by implication ("How long have you known I would come tonight?") — or a refusal to address the subject directly until very late in the scene.

### Rule CA3 — Emotion Channel Swap

If the source rendering uses *fragmented introspection* and the target profile favors *environmental projection*, the adapter rewrites the emotional beat as weather, light, object, or seasonal cue — without losing the residue write to the graph.

### Rule CA4 — Silence Re-Weighting

Each culture profile declares a `silence_usage` weight. The adapter may convert dialogue exchanges to silences (or vice versa) within the budget declared by the profile.

### Rule CA5 — Micro-Beat Reordering

If the culture profile declares `narrative_rhythm.beat_ordering: context_first | turn_first | spiral`, the adapter reorders the blueprint's `micro_beats[]` accordingly, while preserving the position of `turn.type` as the structural pivot.

### Rule CA6 — Address-Form Resolution

For every dialogue exchange involving named characters, the adapter resolves *which address form* each speaker uses (kinship term, status term, name, pronoun, no-address) per the culture's `relationship_dynamics`.

### Rule CA7 — Taboo Substitution

For each `taboo_topics` entry in the culture profile, the adapter checks every dialogue beat and prose constraint. If the source scene names the taboo directly, the adapter substitutes the culture's authorized indirection mechanism (euphemism, displacement onto an object, displacement onto a third party, structured silence).

## What the Adapter Refuses to Do

- Add a symbol from a culture not authorized by the target profile.
- Render an emotion in a mode the profile lists under `forbidden_modes`.
- Force a "Western three-act structure" onto a culture whose narrative rhythm declares otherwise.
- Insert exposition explaining the cultural detail to the reader (R5 — Mystery > Exposition still applies; the culture is lived, not lectured).
- Code-switch into the source culture's logic when "easier" — the adapter must commit to the profile.

## The Compatibility Check

Before regenerating, the adapter runs a compatibility check:

```yaml
compatibility:
  theme_compatible: true | false
  contradictions_compatible: true | false
  turn_type_compatible: true | false
  symbol_palette_resolvable: true | false
  notes: <list of frictions>
```

If any check returns `false`, the adapter **escalates** with a structured report — it does not improvise.

## Related

- [cultural-narrative-layer.md](./cultural-narrative-layer.md)
- [emotional-expression-matrix.md](./emotional-expression-matrix.md)
- [symbolism-by-culture.md](./symbolism-by-culture.md)
- [../../prompts/culture/cultural-adapter.prompt.md](../../prompts/culture/cultural-adapter.prompt.md)
