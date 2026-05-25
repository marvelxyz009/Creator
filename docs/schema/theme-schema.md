# Theme Schema

Theme is not a topic. It is a **question the work refuses to answer cheaply** plus the structural oppositions that hold it open.

## Schema

```yaml
id: theme:primary
title: "Trust is paid in silence."

core_question: "What does it cost to be known?"

oppositions:
  - a: "to be seen"
    b: "to be safe"
  - a: "loyalty to person"
    b: "loyalty to truth"

beats:
  - id: beat:t1
    statement: "Confession buys safety only when it costs the confessor something."
    advanced_by: []     # populated by Scene Designer
    complicated_by: []
    inverted_by: []

  - id: beat:t2
    statement: "What we refuse to name still runs the room."
    advanced_by: []
    complicated_by: []
    inverted_by: []

forbidden_resolutions:
  - "Love conquers all."
  - "Truth always sets you free."
  - "The wound heals because time passes."

symbols:
  - id: sym:iron-key
    binds_to: [beat:t1]
    arc: "introduced as burden → transformed into proof → resolved as gift OR betrayed as weapon"

  - id: sym:red-coat
    binds_to: [beat:t2]
    arc: "appears unnamed three times before it is identified"

voice_of_theme:
  register: "spare, materially specific, allergic to abstraction"
  forbidden_words: ["destiny", "soul", "journey", "healing"]
```

## Required Fields

- `core_question` — must be a question, not a statement.
- `oppositions` — at least one materially opposed pair.
- `beats` — at least three thematic beats, each a falsifiable statement.
- `forbidden_resolutions` — anti-patterns the work refuses.

## Validation Rules

1. `core_question` must end with `?` and not be answerable in five words.
2. Each `beats[].statement` must be testable at scene level (the Theme Sentinel can ask: did this scene *advance / complicate / invert* this beat?).
3. `forbidden_resolutions` must be non-empty — the work must know what it refuses.
4. Every symbol declared here must appear as a `symbol` node in the [[memory-graph]] with a state machine.

## Coupling

- Scenes ([[scene-schema]]) must list which `beats[].id` they touch and how (`advance | complicate | invert`).
- Characters ([[character-schema]]) must have at least one `contradiction` that maps to an `oppositions` pair.

## Related

- [[narrative-laws]] (Law 1)
- [[memory-graph]]
- [[scene-schema]]
