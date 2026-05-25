# Emotional Expression Matrix

A reference matrix describing how a given emotion may be **rendered structurally** under different cultural-literary profiles. The matrix is a *prior*, not a template — it tells the Cultural Adapter what tools the culture's literary tradition foregrounds, never what it must do.

## Important Disclaimer

These rows describe **literary-tradition tendencies** as encoded for this framework's regeneration purposes. They are not statements about how people in a culture *actually* feel or behave. Living cultures are heterogeneous; contemporary writers vary widely. Use the matrix to **avoid the median Western-psychological-realism default** when regenerating, not to impose a stereotype.

Each cell describes **how the rendering channel is used**, not what the emotion *is*.

## Matrix

| Emotion | Japanese-literary | Vietnamese-literary | English-psychological | Russian-philosophical |
|---|---|---|---|---|
| **Grief** | silence; absent person rendered through their leftover objects; seasonal cue; environmental emptiness | routine memory (a meal still cooked for someone gone); family implication; indirect sadness held inside ritual; the absent person referred to in third person by their relational title | fragmented introspection; object-association; involuntary memory triggered by sensory detail; the body before the mind | existential self-conflict; moral self-accusation; long internal speech that argues against itself; suffering claimed as proof of being awake |
| **Anger** | held; surfaces as small precision (a perfectly aligned object, an emphatic stillness); rarely raised voice; departure as statement | indirect — directed at a proxy (an object, a meal refused, a younger person scolded for the real target's offense); generational pressure | articulated, often in fragments; targeted self-talk; rationalization mid-outburst; later regret rendered as inventory | erupts as monologue; carries metaphysical weight; the angry character lectures the universe; immediately followed by self-loathing |
| **Love** | restraint; gestures over declarations; what is brought, prepared, remembered; a half-finished sentence | fed; expressed through caregiving, food, taking on burdens; rarely declared verbally between adults; declared sideways through a third party | named, examined, doubted, named again; subject to introspective audit | argued; tested against suffering and meaning; the lover demands proof in metaphysical terms |
| **Shame** | physical reduction (turning away, lowered gaze, the body smaller); often unwitnessed by the other character; rendered as composure failing in a single small detail | absorbed into the family register; carried for others; manifest as protectiveness or self-effacement | introspective spiral; second-person internal voice ("you should have known"); often interruptive of unrelated tasks | confessed at length; demands a witness; conflated with redemption-seeking |
| **Joy** | minor, momentary, weather-bound; rarely the scene's center; held against a coming loss | shared, communal, food-anchored; tempered by knowledge of the dead | fragile, suspect, examined for false notes; almost always immediately complicated | suspect; treated as either grace (rare, theological) or as denial of suffering |
| **Fear** | quiet, somatic — temperature, hands, the wrongness of small things; not narrated as fear | concealed from elders and children; expressed through over-care for them; rituals invoked | named in fragments; the body's responses inventoried as data | metaphysical, treated as a category of being rather than a passing state |
| **Longing** | rendered through season, distance, an empty room; the absent thing's leftover trace | tied to place — a house, a path, a riverbank; intergenerational | quasi-archaeological; the longing is examined as a relic; provenance reconstructed | doubled — longing for what one already has and fears losing; longing as proof of soul |

## How Agents Use This Matrix

The **Cultural Adapter** consults this matrix when rewriting the scene blueprint's `emotional_shift.mechanism` field.

> Example: A blueprint declares `pov_entry_state: armored, falsely steady`, `pov_exit_state: undermined certainty`, and the source rendering used "fragmented introspection + object-association" (English psychological). When regenerating under a Japanese-literary profile, the adapter rewrites the mechanism to *"silence held one beat too long; a single misaligned object that the POV does not realign"* — same residue, different channel.

The **Cultural Dialogue Specialist** consults this matrix when deciding whether an emotion is **named in dialogue** or **routed through behavior, third party, or refusal**.

The **Language Style Validator** uses this matrix to detect **channel mismatch**: a Japanese-literary regeneration that names anger directly in narration ("she was furious") is flagged.

## What This Matrix is NOT

- It is **not** a guide to "how people of culture X feel". It is a guide to *how literary traditions favored under profile X tend to channel rendering*.
- It is **not** prescriptive at the character level. A single character in any profile may be deliberately written *against* their culture's literary defaults — but that contrast is itself a structural decision that must be declared, not a sloppy inheritance from the source culture.
- It is **not** exhaustive. Cells are seeds; per-project profiles extend with specific channels.

## Extending the Matrix

To add a culture profile, supply for each emotion:
- **Primary channel** (silence | object | environment | dialogue-direct | dialogue-displaced | introspection | ritual | third-party-routing).
- **Forbidden channels** for this profile + this emotion (what would feel imported / wrong).
- **Anti-stereotype note** specific to the culture × emotion intersection.

See [schema/culture/emotional-expression.schema.yaml](../../schema/culture/emotional-expression.schema.yaml) for the structural form.

## Related

- [cultural-narrative-layer.md](./cultural-narrative-layer.md)
- [symbolism-by-culture.md](./symbolism-by-culture.md)
- Style files: [../literary-styles/](../literary-styles/)
