# Prose Rhythm Rules

Concrete rules governing how the **Prose Rhythm Agent** renders prose under a pinned language style profile. Rules below are scaffolding — the per-language-style profile populates the actual numbers.

## Rule Set

### PR1 — Sentence-Length Distribution Honoring

Every paragraph's sentence-length histogram must fall within the profile's declared `sentence_density.distribution` band (with a small tolerance). Three consecutive sentences in the median band that the profile flags as a forbidden "translated rhythm" must be broken.

### PR2 — Breath Placement

Each language profile declares a `prose_rhythm.breath_placement` rule:

- **Front-breath**: a short opening sentence before a longer development. Common in compressed-literary English.
- **End-breath**: long developments closing on a short period. Common in Japanese-literary and certain Vietnamese registers.
- **Mid-breath**: rhythm built around a comma-pivot or em-dash; common in Russian-philosophical.

The agent matches paragraph-level rhythm to the profile's declared breath pattern.

### PR3 — Calque Detection and Removal

Constructions that read as "translated-from-English-default" are removed. The profile maintains an evolving `forbidden_constructions[]` list. Seed entries (always banished in non-English profiles):

- *"In that moment, she felt..."* → English-default temporal hedge + emotion-naming
- *"It was as if..."* → English-default explanatory simile structure
- *"With a mix of X and Y"* → English-default conjoined-abstraction
- *"The feeling of X washed over her"* → English-default emotion metaphor

Even when prose is generated in English, if the project's language style profile is "compressed-literary-English" the agent removes these as default-Wikipedia-English smells.

### PR4 — Paragraph Shape

Each profile declares typical paragraph shape:

- *short, frequent breaks* (compressed-modernist-English, certain Japanese-literary)
- *long, single-block* (Russian-philosophical, certain late-style English)
- *variable, tidal* (Vietnamese-literary often runs short-short-short-long when emotion accretes)

The agent enforces shape distributions over a window (e.g. per scene, per chapter section).

### PR5 — Emotion-Naming Budget

Each profile sets a `emotional_indirection.direct_naming_budget` — the maximum frequency of directly named emotions in narration (e.g. "she was afraid", "he was angry"). Most literary profiles set this to **0 in narration** except when the POV is *misnaming their own feeling*.

The agent counts and enforces.

### PR6 — Environmental Storytelling Weight

Each profile sets `environmental_storytelling.weight` between 0.0 and 1.0. The agent ensures the proportion of emotional rendering channeled through setting/weather/object matches the profile.

- A profile with weight 0.7 (Japanese-literary): most emotional beats are environmental.
- A profile with weight 0.3 (English-psychological): most emotional beats are introspective/object-anchored at close range.

### PR7 — Internal Monologue Mode

Each profile declares the supported internal-monologue modes:

- *stream-of-consciousness* (allowed / not allowed)
- *free indirect discourse* (allowed / preferred)
- *compressed-indirect* (preferred / preferred)
- *direct interior speech* (allowed / forbidden in narration)

The agent renders interiority only in the modes the profile supports.

### PR8 — Pacing (Scene-Time vs. Story-Time)

Each profile declares a `pacing_pattern`:

- *real-time render* — moments stretched; described action approximately equals reading time
- *compression* — large story-time per paragraph
- *tidal* — alternating compression and stretch, often around a turn beat

The agent honors the declared pattern; the Scene Director's `micro_beats[]` provides the structure.

### PR9 — Dialogue Tag Economy

Each profile declares tag-economy defaults:

- *tag-heavy* — "she said", "he answered" attached to most lines
- *tag-light* — tags only at speaker shifts or where ambiguity arises
- *action-beat replacement* — preference for a physical-action beat to identify speaker

The agent matches the profile's tag economy.

### PR10 — Voice Signature is Not Overridden

Rules PR1–PR9 are *language*-level. They constrain the prose register without overriding character `voice_signature`. If a character's signature says "sentences shorten under stress", that holds within whatever the profile's rhythm window allows. The two systems are layered:

```
character voice_signature   (specific to this character)
        ↓ rendered within ↓
language style profile      (general to the language register)
```

If they conflict, the orchestrator escalates — neither is silently overridden.

## Validation

The [language-style-validator](../../prompts/culture/language-style-validator.prompt.md) checks PR1–PR9 on every prose draft. The [anti-ai-editor](../../prompts/agents/anti-ai-editor.prompt.md) handles structural smells; the language style validator handles tradition-fit smells. The two run independently for adversarial isolation.

## Related

- [language-narrative-system.md](./language-narrative-system.md)
- [dialogue-culture-rules.md](./dialogue-culture-rules.md)
- [../../prompts/culture/prose-rhythm-agent.prompt.md](../../prompts/culture/prose-rhythm-agent.prompt.md)
- [../../prompts/culture/language-style-validator.prompt.md](../../prompts/culture/language-style-validator.prompt.md)
