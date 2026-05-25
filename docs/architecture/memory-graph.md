# Memory Graph

The structural memory of the narrative. Replaces the "long prompt of previous chapters" pattern with an **addressable, queryable graph** of facts, relations, and unresolved tensions.

## Why a graph

A long prompt forces every agent to re-derive what matters. A graph lets [[context-assembly]] **answer a question**: *what does this scene need to know?*

- *"What does Mira still owe Tomas emotionally?"* → query unresolved debts between nodes `char:mira` and `char:tomas`.
- *"Has the iron key been seen since chapter 4?"* → query symbol node `sym:iron-key` for state and last appearance.

## Node Types

| Type | Examples | Tracked Properties |
|---|---|---|
| `character` | mira, tomas | mood, location, knowledge_set, last_seen, voice_signature |
| `relation` | mira↔tomas | type (love/debt/rival), tension, history, unresolved_beats |
| `event` | "the fire at the harbor" | when, who_present, who_knows, consequences |
| `symbol` | iron-key, the-red-coat | state {introduced, transformed, resolved, betrayed}, appearances |
| `location` | the kiln, the harbor | mood, last_state, secrets |
| `theme-beat` | "trust is paid in silence" | scenes_advancing, scenes_complicating, scenes_inverting |
| `debt` | "tomas owes mira the truth" | created_in, owed_by, owed_to, pressure, due_by_act |

## Edge Types

- `KNOWS` — character knows event/fact (asymmetric — drives dramatic irony)
- `PRESENT_AT` — character was at event
- `OWES` — debt edge between characters or character→reader
- `SYMBOLIZES` — symbol → theme-beat
- `CONTRADICTS` — between traits within a character (powers [[character-schema]] contradictions)
- `RESOLVES` / `COMPLICATES` / `INVERTS` — scene → theme-beat

## Asymmetric Knowledge

Critical: the graph tracks **who knows what**, not just what is true. This enables dramatic irony, lies, and discovery scenes to be planned structurally rather than improvised.

```
event:harbor-fire
  ├─ PRESENT_AT → mira (knows: true cause)
  ├─ KNOWS → tomas (knows: official story only)
  └─ KNOWS → reader (knows: true cause, since ch.7)
```

## Lifecycle

1. **Write** — generative stages append nodes/edges as artifacts are produced.
2. **Validate** — the Continuity Agent queries the graph to check no draft contradicts established state.
3. **Resolve** — debts and symbols are closed by scenes that fire them; unresolved debts at the end of the work are flagged as structural failures.

## Storage (logical)

For this documentation phase, the graph is specified as a **logical model**. Implementation (file-backed JSON-LD vs. embedded graph DB) is deferred to the implementation phase, but agent contracts must already speak the node/edge vocabulary above.

## Related

- [[context-assembly]]
- [[narrative-pipeline]]
- [[character-schema]]
- [[scene-schema]]
