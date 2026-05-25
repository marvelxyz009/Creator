# Narrative Technique Library

A curated, structured catalog of named narrative techniques the framework can invoke by reference. Agents cite techniques by id; the library provides the definition, the structural requirements, and the failure modes.

## Entry Format

```yaml
id: tech:<slug>
name: <Human-Readable Name>
family: pov | structure | tension | revelation | symbolism | voice | dialogue
short: <one-sentence definition>
structural_requirements:
  - <what must be true in the graph / schema for this technique to be valid>
how_to_invoke:
  - <agent-level instructions>
failure_modes:
  - <how this technique collapses into AI-smell when misapplied>
related: [tech:..., laws:..., smells:...]
```

## Seed Entries

### tech:withheld-pov
**Family:** pov
**Short:** Render a scene from a POV that refuses to name what the POV most thinks about.
**Structural requirements:**
- POV character has a populated `voice_signature.what_they_refuse_to_name`.
- The unnamed subject must be present in the graph (event, person, or symbol).
**Failure modes:**
- Collapses into A1 / A3 of [[ai-smells]] if the refusal leaks into explicit narration.

### tech:dramatic-irony-asymmetric
**Family:** revelation
**Short:** Reader knows what one or more characters do not; the scene's pressure comes from the gap.
**Structural requirements:**
- The [[memory-graph]] must have asymmetric `KNOWS` edges established **before** the scene.
**Failure modes:**
- Tipping the asymmetry too early.
- Characters acting *as if* they suspect what they shouldn't.

### tech:object-as-debt
**Family:** symbolism
**Short:** A physical object carries an unresolved promise between characters; its movement IS the plot beat.
**Structural requirements:**
- Symbol node with state machine in graph.
- A debt edge bound to the symbol.
**Failure modes:**
- Symbol over-named in narration (Category G of [[ai-smells]]).
- Symbol fires without cost.

### tech:earned-silence
**Family:** dialogue
**Short:** A character does not answer; the absence is the answer.
**Structural requirements:**
- A direct question is on the table.
- POV (or another character) registers the silence via gesture or environment, not narration.

### tech:rhythmic-shortening
**Family:** voice
**Short:** Under stress, the POV's sentences shorten faster than the action requires.
**Structural requirements:**
- POV's `voice_signature.rhythmic_tells` includes a stress-rhythm.
**Failure modes:**
- Becomes mannerism if used outside stress contexts.

### tech:inverted-beat
**Family:** structure
**Short:** A scene that appears to advance a theme-beat actually inverts it on closer reading.
**Structural requirements:**
- The scene's `theme_touch.mode` is `invert`, but the surface reading appears as `advance`.
**Failure modes:**
- Reader can't recover the inversion → it's just confusion.

### tech:misplaced-object
**Family:** symbolism
**Short:** An object appears where it should not, three scenes before its meaning is named.
**Structural requirements:**
- Symbol introduced with low explicit weight; appearance count tracked in graph.

### tech:lying-narrator-localized
**Family:** pov
**Short:** A POV character lies in *narration* (not just dialogue) about their own feelings.
**Structural requirements:**
- `voice_signature.what_they_refuse_to_name` and `drives.buried` both populated.
- The lie must be **falsifiable later** by graph state.

## Discovery & Growth

New techniques are added via the [[reference-analysis-system]] when a pattern recurs across references with measurable structural signatures. Each addition is reviewed for:
- Structural definability (can an agent enforce it?)
- Distinct failure modes (vs. existing techniques)
- Compatibility with [[narrative-laws]]

## Related

- [[reference-analysis-system]]
- [[scene-schema]]
- [[ai-smells]]
