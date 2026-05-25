# Language Narrative System

A complement to the [cultural-narrative-layer](../culture/cultural-narrative-layer.md). Where the cultural layer handles **cognition** (what a scene attends to, what is named vs. implied, what symbols carry weight), the language layer handles **rhythm** — the sentence-level shape of prose under the target language tradition.

Culture and language are **coupled but separable**:

- A *Vietnamese-language Vietnamese-cultural* novel uses both layers' Vietnamese profiles.
- A *Japanese-cultural novel rendered in English prose* (like much diaspora literature) couples a Japanese cultural profile with an English-prose-rhythm profile.
- A *Russian-philosophical novel rendered in Vietnamese prose* is rare but legal — and the framework must support it.

## Position in the Pipeline

```
Cultural Cognition Layer        ← decides WHAT a scene attends to
       ↓
Language Rhythm Layer           ← decides HOW the sentences move
       ↓
Scene → Dialogue → Prose → Revision
```

The language layer runs *after* the cultural layer because emotional channel choice (a cultural decision) constrains sentence rhythm choice (a language decision) — not the reverse.

## What the Language Layer Manages

1. **Sentence density.** Compact (Japanese-literary, mid-period Hemingway-English) vs. expansive (Russian-philosophical, late-style Henry James) vs. variable.
2. **Prose rhythm.** Distribution of sentence lengths; placement of breath / pause; tolerance for fragmentation.
3. **Dialogue directness.** Independent of culture's *directness gradient* — *language*-level conventions of how speech is tagged, interrupted, broken.
4. **Emotional indirection.** Degree to which the language's literary register names emotion in narration vs. routes it through other channels.
5. **Environmental storytelling.** Weight of setting / weather / season in carrying interiority.
6. **Internal monologue style.** Stream-of-consciousness vs. compressed indirect vs. absent entirely.
7. **Pacing pattern.** How the language's tradition handles scene-time vs. story-time (real-time render vs. compression vs. tidal).

## Why This is Not Just a Style Setting

Sentence rhythm is **language-bound** in ways most "tone settings" ignore:

- A 22-word English sentence and a 22-character Japanese sentence are not equivalent objects.
- Vietnamese tonal phonology shapes sentence ending decisions in ways unrelated to English rhythm logic.
- Russian's morphological compression lets a one-clause sentence carry information that requires three English clauses.

Modeling "rhythm" as a knob detached from language tradition produces translated-feeling prose even when generated directly.

## The Language Style Profile

Captured in [schema/culture/language-style.schema.yaml](../../schema/culture/language-style.schema.yaml). Each profile defines:

- `sentence_density` — distribution of sentence lengths under tension and at rest.
- `prose_rhythm` — paragraph-shape histogram; breath placement.
- `dialogue_directness` — language-tradition convention, not cultural.
- `emotional_indirection` — narration's tolerance for naming emotion.
- `environmental_storytelling` — weight scale 0.0–1.0 for setting carrying interiority.
- `internal_monologue_style` — registered modes the language tradition supports.
- `pacing_pattern` — scene-time:story-time defaults.
- `forbidden_constructions` — language-specific calque / awkward translations to detect.
- `voice_continuity_tests` — readable-by-validator tests for "does this feel natively written?"

## The Detection Problem

The **Language Style Validator** detects prose that "feels translated" — even when no translation has occurred. Signals:

- Sentence-length distribution that mismatches the target profile.
- Calque constructions ("she felt a wave of X", "in that moment", "it was as if...") imported from English-default generative behavior.
- Emotional-naming rate that exceeds the profile's tolerance.
- Dialogue tag conventions imported from the wrong tradition.
- Paragraph shape (very short paragraphs in a tradition that defaults to long; very long paragraphs in a tradition that defaults to short).

See [../../prompts/culture/language-style-validator.prompt.md](../../prompts/culture/language-style-validator.prompt.md) for the validator contract.

## Interaction with Anti-AI Editor

The [anti-ai-editor](../../prompts/agents/anti-ai-editor.prompt.md) maintains a **base banished-phrase list** (mostly English-default smells). When a language profile is pinned, the editor:

1. **Subtracts** banished phrases that are not relevant to the pinned language profile (e.g. "delve" is meaningless in Vietnamese prose).
2. **Adds** language-specific banished phrases registered in the profile.
3. Reuses base structural rules (cut the last sentence, subtract before adding) — these are language-agnostic.

## Relationship to Vision-Keeper's Register Field

The Vision Keeper's `vision.register` is the **project-level intent**. The language style profile is the **per-rendering shape**. A project may have one register, one cultural profile, and multiple language profiles (e.g. a trilogy planned for two languages).

## What This Layer Does NOT Do

- It does not translate.
- It does not "style transfer" between authors — it operates on tradition-level conventions, not on a specific writer's voice.
- It does not override the character `voice_signature` — voice signatures must remain distinct *within* the chosen language register.

## Related

- [prose-rhythm-rules.md](./prose-rhythm-rules.md)
- [dialogue-culture-rules.md](./dialogue-culture-rules.md)
- [localization-vs-regeneration.md](./localization-vs-regeneration.md)
- [../culture/cultural-narrative-layer.md](../culture/cultural-narrative-layer.md)
- [../../schema/culture/language-style.schema.yaml](../../schema/culture/language-style.schema.yaml)
