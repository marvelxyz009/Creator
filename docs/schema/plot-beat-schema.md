# Plot Beat Schema

A plot beat is **one unit of story-level pressure** the scene must enact. It binds together: which characters meet, what theme-beats the scene tests, which symbols move, what knowledge shifts, and what kind of turn this is. The Scene Director consumes a plot beat and produces a scene blueprint that fulfills it.

## Schema

```yaml
id: beat:p<id>                     # e.g. beat:p07
function: complication             # setup | complication | escalation | reversal | resolution
touches_theme_beats: [beat:t1, beat:t2]   # one or more theme beats this plot beat tests
theme_mode: complicate             # advance | complicate | invert (one per beat or per-beat map)

participating_characters: [char:<id>, char:<id>]
pov_default: char:<id>             # the Scene Director may override with justification
pov_mode: alternating_close_third  # single-pov | alternating_close_third | omniscient
pov_notes: null                    # optional — when alternating, how the handoffs work

intended_turn_type: knowledge      # knowledge | relation | resolve | symbol-fire | debt

symbol_activity:
  - id: sym:<id>
    op: introduce                  # introduce | transform | resolve | betray | fire-by-body
  - id: sym:<id>
    op: transform

knowledge_delta:
  character_gains:
    - who: char:<id>
      gains: "<one-sentence specific gain — what they NOW know that they did not before>"
    - who: char:<id>
      gains: "<...>"
  reader_gains: "<what the reader's understanding becomes — including 'ambiguity preserved' as a valid outcome>"

intended_tension_after: 0.85       # 0.0–1.0; the tension level this beat should leave on the participants' relation
tension_note: null                 # optional — explain a non-obvious target (e.g. tension drops because resolution; not because of giving up)

notes_for_scene_director:
  - "<one-sentence directive about how the scene must NOT resolve this beat>"
  - "<one-sentence ordering constraint, if any>"
  - "<one-sentence what the scene close must achieve at the level of subtext>"
```

## Required Fields

- `id`, `function`
- `touches_theme_beats` — at least one beat:t<id> from `theme.yaml.beats[]`
- `theme_mode` — `advance` | `complicate` | `invert`
- `participating_characters` — at least one
- `intended_turn_type` — never `atmosphere` (atmosphere is not a turn)
- `knowledge_delta.character_gains` — at least one entry, OR `reader_gains` if the scene is reader-aware only
- `intended_tension_after` — explicit number

## Validation Rules

1. Every `touches_theme_beats[]` id must exist in `theme.yaml.beats[]`.
2. Every `participating_characters[]` id must exist as a character node.
3. `symbol_activity[].id` must exist in `theme.yaml.symbols[]`; `op` must be a legal next state for the symbol's current state (the Symbolism Tracker enforces; see [[memory-graph]]).
4. `intended_turn_type` must NOT be `atmosphere`. Scenes without a turn type are not scenes.
5. `knowledge_delta` cannot be empty — if no character gains anything, the scene is a transit scene and must be rejected.
6. `function: resolution` requires a prior `setup` and at least one `complication` in the canon for the same theme thread; the Plot Engineer enforces.
7. `notes_for_scene_director[]` should name at least one **anti-direction** (what the scene must NOT do) — this is where forbidden_resolutions get scene-localized.

## Function values

- `setup` — plant something the work will later pay off
- `complication` — make the protagonist's task harder or the question more ambiguous; **does not resolve**
- `escalation` — raise tension by deepening an existing conflict
- `reversal` — invert an earlier expectation; what looked like X is now Y (or the reader's reading shifts)
- `resolution` — close one thread; can be tragic, ironic, or earned — never cheap

## Theme Mode values

- `advance` — the scene moves the theme-beat forward; the work's stance on this beat gets sharper
- `complicate` — the scene makes the theme-beat harder to read; both sides of the opposition get weight
- `invert` — the scene reverses the apparent stance on this beat

## Related

- [[theme-schema]] — source of `beat:t<id>` ids
- [[scene-schema]] — what the Scene Director writes from this beat
- [[memory-graph]] — `symbol_activity` and `knowledge_delta` write into the graph
- [[agent-contracts]] (Plot Engineer)
