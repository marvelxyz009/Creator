# Dialogue Culture Rules

Rules governing how the **Cultural Dialogue Specialist** rewrites dialogue under a pinned culture profile. These rules layer *on top of* the base [dialogue-specialist](../../prompts/agents/dialogue-specialist.prompt.md) — they do not replace its voice-signature, subtext, or anti-pattern obligations.

## What Changes Per Culture

For any given conflict (accusation, refusal, apology, confession, declaration, demand):

1. **Directness gradient.** Whether the topic is named directly, implied through related topic, refused entirely.
2. **Address form.** Kinship term, status term, name, no-address.
3. **Turn-taking and interruption.** Whether interruption is allowed; whose turn is sacred.
4. **Silence as utterance.** Silence's weight as a "line" — can a silence be a refusal? a concession?
5. **Third-party routing.** Whether a charged topic is addressed to the actual subject or to a proxy (an object, an absent person, a younger character).
6. **Honorific / register shifts.** Whether a register-shift mid-scene carries dramatic weight (often heavy in East-Asian profiles; subtle in English-psychological).
7. **Apology shape.** What constitutes a legitimate apology — direct admission, oblique acknowledgment, gesture without words, accepting a debt.
8. **Taboo handling.** What is not allowed to be said directly, and the authorized substitutes.

## Rule Set

### DC1 — Directness Gradient Resolution

For every charged exchange, the dialogue specialist consults the culture profile's `communication_style.directness` and `conflict_style` and resolves:

- *direct* — the topic is named.
- *implied* — the topic is gestured at via related vocabulary; the listener understands.
- *refused* — the topic is structurally avoided; the avoidance itself is the communication.

A scene's epistemic conflict (declared by the Scene Director) is preserved; the *staging* shifts.

### DC2 — Address-Form Resolution per Exchange

For each line involving a named addressee, the dialogue specialist resolves the address form. In low-restraint English-psychological, characters call each other by first name almost throughout. In high-restraint East-Asian or Vietnamese family contexts, the *change* in address form across a scene can be the turn beat itself.

### DC3 — Silence-as-Utterance Budget

Each culture profile declares a `silence_usage` weight. The dialogue specialist may convert a dialogue exchange to a silence (labeled with `<silence>` plus intent + subtext) up to the profile's budget. In high-silence profiles, the budget is generous and silence does load-bearing work.

### DC4 — Third-Party Routing Permission

Some profiles authorize a character to speak *to* one person *about* another in the second person — addressing a child to wound a parent, addressing an object to wound a partner. The dialogue specialist may use this routing only when the profile permits.

### DC5 — Apology Shape Discipline

Each profile declares which apology shapes are *legible*. An English-psychological direct admission ("I'm sorry I edited your memory") is often illegible in a high-restraint profile, where the legible apology is a gesture (cooking the meal, fixing the misaligned object, taking on a burden). The dialogue specialist must render apologies in the profile's legible shape.

### DC6 — Taboo Substitution

For every taboo declared in the culture profile, the dialogue specialist verifies no line names it directly. Authorized substitutions: euphemism, displacement onto an object, displacement onto a third party, structured silence.

> Example: a culture profile that lists *"naming a parent's mistake to their face"* as taboo will not allow Mira to accuse Tomas's mother directly. The accusation routes through an object Tomas's mother gave him, through Tomas's defense of her, or through Mira's pointed refusal to mention her at all.

### DC7 — Register Shift as Turn-Beat Eligibility

In profiles where register shifts (formal → familiar, kinship → status, name → no-address) carry heavy dramatic weight, the dialogue specialist may stage the scene's `turn` *as a register shift*. This must be declared explicitly in the dialogue draft and validated against the Scene Director's `turn.type` (knowledge / relation / resolve / symbol-fire / debt) — a register shift typically maps to `relation`.

### DC8 — Don't Import Foreign Tag-Economy

English-default fiction uses heavy dialogue tags ("she said", "he replied"). Other traditions vary widely. The dialogue specialist consults the language style profile's `dialogue_tag_economy` and matches.

### DC9 — Don't Import Foreign Subtext Conventions

A profile that prefers *refused-topic* communication will not feel "subtextual" to a reader of a different tradition — it will feel evasive or even dishonest if the reader is reading with the wrong convention in mind. The dialogue specialist does not soften the convention to be cross-readable; the convention is the convention. (Surfacing the convention for cross-cultural readers is the editor's choice, not the agent's.)

### DC10 — Voice Signature Still Holds

DC1–DC9 are culture-level. They constrain *how* a character speaks under their culture's rules. The character's `voice_signature` constrains *how this specific character* speaks within that culture. If the two conflict, the orchestrator escalates.

## Examples (anti-stereotype, illustrative only)

> **Scene:** Mira confronts Tomas about an edited memory.
>
> **English-psychological staging (source):** Mira's first line is a direct accusation. Tomas's response is a qualified deflection.
>
> **Japanese-literary staging (regenerated):** Mira's first line is procedural — she asks whether the appointment time still holds. The accusation arrives in her fifth or sixth line, and it arrives as a question whose form contains the accusation. Tomas does not deflect; he answers a different question. The turn lands when he places the lighter on the desk.
>
> **Vietnamese-literary staging (regenerated):** Mira begins by asking after Tomas's mother. He answers warily. The accusation routes through their shared memory of his mother's house. The turn lands when Mira refuses an offered cup of tea — a refusal that under this profile is a louder line than any direct accusation could be.

These are *illustrative*. Specific projects will tune their profiles, and individual characters may be written against the default — but the *deviation* is then itself a structural choice that must be declared.

## Related

- [language-narrative-system.md](./language-narrative-system.md)
- [prose-rhythm-rules.md](./prose-rhythm-rules.md)
- [../culture/cultural-adaptation-rules.md](../culture/cultural-adaptation-rules.md)
- [../../prompts/culture/cultural-dialogue-specialist.prompt.md](../../prompts/culture/cultural-dialogue-specialist.prompt.md)
