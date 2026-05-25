# English Psychological Style — Literary Profile

> **Scope:** a literary register dominant across post-1950 Anglophone literary fiction — running from Henry James through late Hemingway, Bowen, Munro, Marilynne Robinson, Ishiguro (in English), Rachel Cusk, and the contemporary "interior literary" novel. It is **not** "how English speakers think." The Anglophone tradition includes many registers that do not match this profile (genre, comic, maximalist, oral-tradition, etc.).

## Emotional Rhythm

- Emotion is **examined**. The interior voice is foregrounded; the reader spends much of the scene inside the POV's introspection.
- Affect is often **named, then doubted** — "she felt afraid; or what she had learned to call afraid."
- The body is an instrument of evidence — sleep, appetite, blood pressure, posture — and is *interpreted* by the POV as data.
- Beats often close on a small interior recognition, sometimes followed by an immediate self-correction.

## Dialogue Behavior

- Confrontation is often direct; the topic is named.
- First-name address dominates almost throughout; address-form shifts are rare and small.
- Apologies are typically verbalized; an unspoken apology reads as cowardice in the register's default values.
- Subtext exists but operates at the line level (irony, hedge, qualifier) rather than at the scene-routing level.
- Silence is used, but typically as a momentary beat inside a scene of speech, not as the scene's load-bearing structure.

## Pacing

- Scenes often run at variable rates inside themselves — compression of weeks into a paragraph, real-time on a single conversation.
- Story-time and scene-time are interleaved openly; flashback is mediated by an interpreting narrator.
- Paragraphs cluster around a single object of attention, often examined from several angles.

## Implication Style

- Emotional weight is carried by **objects examined at close range** — the cracked glass, the unopened letter, the email left up on the screen.
- The body's failures (insomnia, weight loss, the tic, the held breath) carry emotional information the POV mind cannot.
- Weather is allowed, but the register is self-conscious about it; "the weather as mood" is often slyly acknowledged.

## Symbolism Tendencies

See [symbolism-by-culture.md#english-psychological-palette](../culture/symbolism-by-culture.md). Common loads:

- single domestic objects examined closely
- documents (letters, files, emails, court papers)
- the body's malfunctions
- the suburban or near-urban interior
- public-private spaces (cafés, waiting rooms)
- the obsolete object recovered

Cliché to avoid: the mirror-reveals-self beat; the cigarette as moral-ambivalence shorthand; the broken family photograph as cheap symbol; "she stared out the window" as introspection cue.

## Philosophical Worldview (literary-register only)

- The self is examined, audited, and treated as constructed — but the construction is the proper subject of inquiry, not a problem to be dissolved.
- Truth is held under suspicion of self-deception; the POV is reliable in detail and unreliable in interpretation.
- Moral seriousness is performed quietly — the register distrusts theatrical morality.

## Anti-Stereotype Notes

- **Forbidden:** treating this profile as "neutral" or "universal." It is one literary register among many. Generative LLMs default toward this register; the framework explicitly resists that default unless this profile is the pinned target.
- **Forbidden:** the MFA-workshop neutral interior monologue beat as scene-filler.
- **Forbidden:** the "Anglo-American = direct" stereotype. The register's directness is heavily qualified, hedged, and ironized at the sentence level.
- **Forbidden:** "literary realism" as code for "this profile" — many literary realisms exist; this is one register inside that broad category.
- **Forbidden:** treating introspection as a sign of depth. Introspection is this profile's *channel*; depth is independent of channel.

## What This Profile Is For

Consulted by:
- **Cultural Adapter** — when the project explicitly pins English-psychological as the target register (e.g. the MVP scene in `samples/mvp-scene-01/`).
- **Cultural Dialogue Specialist** — for line-level subtext through hedge/qualifier; first-name address default; verbalized-apology defaults.
- **Prose Rhythm Agent** — for variable paragraph length, mid-breath placement around comma-pivots, tolerance for free indirect discourse and close-third introspection.
- **Language Style Validator** — for detecting genre-default smells that mismatch the literary register specifically (e.g. thriller pacing leaking into the psychological scene).

## Note on Default Drift

LLMs trained predominantly on English literary corpora collapse toward this register by default. The framework treats this as a **failure mode** when any other profile is pinned: the Cultural Adapter and Language Style Validator are both responsible for catching English-psychological habits that leaked through under, e.g. a Vietnamese-literary pinning.

## Related

- [japanese-narrative-style.md](./japanese-narrative-style.md)
- [vietnamese-narrative-style.md](./vietnamese-narrative-style.md)
- [russian-philosophical-style.md](./russian-philosophical-style.md)
- [../culture/cultural-narrative-layer.md](../culture/cultural-narrative-layer.md)
