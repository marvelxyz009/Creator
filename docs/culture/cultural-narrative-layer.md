# Cultural Narrative Layer

A structural layer inserted into the [narrative-pipeline](../architecture/narrative-pipeline.md) between *character psychology* and *prose generation*. Its purpose: the framework must **regenerate** scenes for a target cultural cognition — not translate text after the fact.

## Position in the Pipeline

```
Vision
  ↓
Theme
  ↓
Worldbuilding
  ↓
Character Psychology
  ↓
┌──────────────────────────────┐
│  Cultural Cognition Layer    │   ← NEW
│  - culture profile pinned    │
│  - emotional logic resolved  │
│  - symbol palette swapped    │
└──────────┬───────────────────┘
           ↓
┌──────────────────────────────┐
│  Language Rhythm Layer       │   ← NEW
│  - prose rhythm profile      │
│  - sentence density          │
│  - dialogue directness       │
└──────────┬───────────────────┘
           ↓
Scene Design  →  Dialogue  →  Prose  →  Revision
```

The cultural layer is **not a post-translation filter**. It modifies the **scene design** and **dialogue intent** *before* prose is rendered. Two scenes serving the same plot beat, generated under two different culture profiles, will differ at the level of *what happens*, not only of *how the sentence is phrased*.

## Why Translation Fails

A naive multilingual pipeline writes prose in English, then translates. This destroys:

- **Emotional logic.** A grief rendered through fragmented introspection (English psychological) does not translate into Japanese literary silence — it renders as awkward overexplanation.
- **Symbol palette.** A neon-decay symbol set has no equivalent in a Vietnamese family-altar palette; a literal swap is grotesque.
- **Communication norms.** Direct accusation in dialogue, fitted to one cultural script, reads as social violence in another.
- **Pacing.** Sentence density and rhythm of silence are language-bound; translation flattens them.

Translation preserves *propositional content*. Narrative culture is not propositional.

## The Three Concepts

### 1. Translation
Same scene, same realization, different surface language. Lossy at every level above lexicon. **Not used by this framework.**

### 2. Localization
Same scene, same plot beats, surface adapted: idioms swapped, names changed, references substituted. Still preserves the *cognitive shape* of the source culture. **Used only for surface adaptation when a single source culture is canonical.**

### 3. Narrative Regeneration
The plot beat, theme-touch, and character contradictions are preserved as **structural invariants**. Everything downstream — scene design, symbol choice, dialogue logic, prose rhythm, emotional rendering — is **re-derived** under the target culture profile. **This is the framework's default.**

See [localization-vs-regeneration.md](../language/localization-vs-regeneration.md) for the contract.

## What Is Preserved Across Cultures (Invariants)

- The **theme's core question** and **forbidden resolutions**.
- The **plot beat's** declared turn type and knowledge delta.
- The **character contradiction** (forces a/b, drives surface/buried).
- The **memory graph state** (debts, asymmetric knowledge, event facts).
- The **scene's residue requirements** (what must enter the graph after the scene).

## What Is Re-Derived Per Culture

- The **symbol palette** binding to theme-beats (cracked glass vs. cracked teacup vs. cracked altar bowl — same arc role, different cultural load).
- The **emotional rendering mode** (silence vs. routine vs. introspection vs. moral self-attack).
- The **dialogue directness** (whether the protagonist accuses outright, indirectly, through a third party, or by refusal to address).
- The **prose rhythm** (sentence density, paragraph shape, breath placement).
- The **environmental storytelling weight** (how much of the emotion is carried by setting vs. behavior vs. internal monologue).
- The **micro-beat ordering** inside the scene.

## How a Cultural Run Works

1. **Pin culture profile.** The orchestrator selects a `culture_profile` (see [schema/culture/culture-profile.schema.yaml](../../schema/culture/culture-profile.schema.yaml)).
2. **Pin language style profile.** Often coupled to culture, but separable (e.g. an English-language novel set in a Vietnamese cultural cognition).
3. **Cultural Adapter agent** rewrites the scene blueprint: re-resolves symbol palette, emotional rendering, dialogue directness, micro-beat ordering.
4. **Cultural Dialogue Specialist** drafts dialogue under target communication norms.
5. **Prose Rhythm Agent** renders prose under target language style.
6. **Language Style Validator** detects translated-feeling prose, directness mismatch, symbolism mismatch.
7. The standard revision/continuity pipeline runs as before — adversarial validators inherit cultural constraints from the pinned profile.

## Anti-Stereotype Discipline

The framework refuses cartoon-culture coding. See the per-culture style files in [docs/literary-styles/](../literary-styles/) for what is allowed vs. forbidden in each profile. As a rule:

- "Japanese = anime silence" — **forbidden.** Use: *"literary communication often relies on implication, social restraint, and environmental emotional projection — but contemporary Japanese writers vary widely; profile encodes a literary register, not a national personality."*
- "Vietnamese = sentimental family scenes" — **forbidden.** Use: *"emotional weight often travels through meals, ancestral spaces, and indirect address — but the profile names structural tendencies, not a fixed emotional palette."*

Every culture profile carries an explicit `anti_stereotype_notes` field that the orchestrator surfaces to every cultural agent.

## Related

- [cultural-adaptation-rules.md](./cultural-adaptation-rules.md)
- [emotional-expression-matrix.md](./emotional-expression-matrix.md)
- [symbolism-by-culture.md](./symbolism-by-culture.md)
- [language-narrative-system.md](../language/language-narrative-system.md)
- [localization-vs-regeneration.md](../language/localization-vs-regeneration.md)
