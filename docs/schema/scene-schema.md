# Scene Schema

A scene is the **atomic unit of narrative change**. If nothing changes — knowledge, relation, debt, symbol state — it is not a scene; it is transit.

## Schema

```yaml
id: scene:04-12
act: 2
chapter: 4
position_in_chapter: 12

participants: [char:mira, char:tomas]
pov: char:mira
location: loc:kiln
time: "dusk; the bell has rung twice"

goal:                # what POV wants in THIS scene
  who: char:mira
  what: "leave the kiln without confessing the brother"

opposition:          # what resists
  source: char:tomas
  form: "he already knows; he is offering her the chance to say it"

stakes:
  if_won: "she keeps the secret; the debt grows heavier"
  if_lost: "the name burns into iron; rule r1 fires"

theme_touch:
  - beat: beat:t1
    mode: complicate   # advance | complicate | invert

turn:                # the moment of change — required
  type: knowledge | relation | resolve | symbol-fire | debt
  description: "Tomas sets the iron key on the rim of the kiln. Mira understands he knew before she arrived."

residue:             # what the scene leaves in the graph
  graph_writes:
    - update: relation:mira-tomas.tension := 0.95
    - update: sym:iron-key.state := transformed
    - new: debt { owed_by: char:mira, owed_to: char:tomas, content: "the name", due_by_act: 3 }

knowledge_deltas:
  - char:mira now knows: "tomas knew the true cause of the fire"
  - reader now knows: "tomas has known since chapter 2"

constraints:
  - "No internal narration of mira's fear. Render through hands, breath, and the placement of the key."
  - "Tomas speaks <= 4 lines. Each line is shorter than the one before."

forbidden:
  - "Direct statement of feeling."
  - "Any line that summarizes the relationship to date."

beats:               # micro-structure inside the scene
  - "arrival — wrong rhythm of the bell"
  - "the key appears on the rim"
  - "tomas's first short line"
  - "mira's lie that overshoots"
  - "the kiln's heat shifts"
  - "exit — she takes the key, he lets her"
```

## Required Fields

- `participants`, `pov`, `location`
- `goal`, `opposition`, `stakes`
- `theme_touch` — at least one entry; scenes that touch no theme are rejected.
- `turn` — required; scenes without a turn are rejected.
- `residue.graph_writes` — required; a scene must leave something in the [[memory-graph]].

## Validation Rules

1. `turn.type` must be one of the enumerated change types. "Atmosphere" is not a turn.
2. `residue.graph_writes` must produce at least one observable graph delta.
3. `theme_touch[].mode` must be honored — the Theme Sentinel will check the resulting prose for the declared mode.
4. `constraints` and `forbidden` are passed verbatim into the Prose Agent's bundle by [[context-assembly]].

## Related

- [[theme-schema]]
- [[character-schema]]
- [[world-schema]]
- [[memory-graph]]
- [[narrative-laws]] (Law 1, Law 8)
