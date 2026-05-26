# Memory Graph Schema

The memory graph is the **single source of canonical truth** for a project: what characters exist, what events happened, what symbols are in play, what each character knows, what debts are open. A **graph excerpt** is a snapshot scoped to one scene's worth of relevant state — agents read excerpts, not the full graph.

The Scene Director, Continuity Auditor, and Symbolism Tracker all validate against this excerpt.

## Schema

```yaml
graph_excerpt:
  snapshot_at: "pre-scene-01"            # human label for the moment in story-time
  scope: "nodes and edges relevant to the upcoming scene only"

  nodes:
    characters:
      - id: char:<id>
        current_location: <loc:<id> | "in transit to ..." | free-text>
        current_state: "<one-sentence concrete state — armored / waiting / carrying X>"

    locations:
      - id: loc:<id>
        state: "<one-sentence concrete condition — staffed / abandoned / power intermittent>"

    events:
      - id: event:<slug>
        when: "<story-time reference — 'three years before scene' | 'five days before scene'>"
        who_present: [char:<id>, ...]
        who_knows_full: [char:<id>, ...]
        who_knows_partial: [char:<id>, ...]
        who_knows_nothing: [char:<id>, ...]
        status: <free-text — e.g. "redacted_in_archive", "publicly known", "hidden">
        content: null                    # optional — short factual description, only if reader needs it
        hidden_from: [char:<id>, ...]    # optional — who must not learn this

    symbols:
      - id: sym:<id>
        state: not_yet_introduced        # not_yet_introduced | introduced | transformed | resolved | betrayed | fired-by-body
        last_appearance: null            # short reference to the scene/location where it last appeared
        appearances_count: 0
        bound_to_beats: [beat:t<id>, ...]
        notes: "<one-sentence concrete note — what the object IS in the world>"

    debts:
      - id: debt:<id>
        owed_by: char:<id>
        owed_to: char:<id>
        content: "<one-sentence concrete — what is owed>"
        created_at: "<story-time reference>"
        pressure: medium                 # low | medium | high
        due_by: unresolved               # unresolved | act-1 | act-2 | act-3 | beat:p<id>

  edges:
    KNOWS:
      - { subject: char:<id> | reader, object: event:<id> | sym:<id>, level: full | partial | none }

    PRESENT_AT:
      - { subject: char:<id>, object: event:<id> }

    OWES:
      - { from: char:<id>, to: char:<id>, debt: debt:<id> }

    SYMBOLIZES:
      - { symbol: sym:<id>, theme_beat: beat:t<id> }
```

## Required Fields

- `graph_excerpt.snapshot_at` — a label so multiple excerpts can be ordered
- `graph_excerpt.scope` — one sentence on what this excerpt does and does NOT include
- `nodes.characters` — every character participating in the scene
- `nodes.symbols` — every symbol the scene may touch, even ones not yet introduced (must have explicit `state: not_yet_introduced`)
- `edges.KNOWS` — at least one entry per (character, event) pair that matters to the scene's asymmetry

## Validation Rules

1. Every id referenced in `edges[*]` must exist in `nodes`. Phantom references are hard-reject.
2. `symbols[].state` must be a valid state-machine value. The state machine: `not_yet_introduced → introduced → transformed → (resolved | betrayed)`. `fired-by-body` is a parallel terminal state for symbols whose firing happens through body-knowledge rather than conscious recognition.
3. `KNOWS.level` must be one of `full | partial | none`. Omitted = `none`.
4. For every `event` node, the union of `who_knows_full + who_knows_partial + who_knows_nothing` should cover every named character; missing characters default to `who_knows_nothing`.
5. A `debt` with `pressure: high` and `due_by: unresolved` past a project-defined window must be flagged by the Continuity Auditor.
6. `reader` is a valid edge subject in `KNOWS` only. It is not a character node and cannot own/owe debts.

## State Machine — Symbols

```
not_yet_introduced  ──introduce──▶  introduced
introduced          ──transform──▶  transformed
introduced          ──fire-by-body──▶  fired-by-body   (parallel terminal — body recognition without conscious naming)
transformed         ──resolve──▶  resolved
transformed         ──betray──▶  betrayed
(any state)         ──betray──▶  betrayed              (betrayal is always legal — explicit subversion)
```

Illegal transitions (hard reject by Symbolism Tracker):
- `transform` from `not_yet_introduced`
- `resolve` from `not_yet_introduced` or `introduced` (must transform first)
- Multiple `resolve`/`betray` on the same symbol within one project

## Asymmetry as Source of Tension

The graph's purpose is **asymmetric knowledge**: who knows what, who doesn't, who knows that the other doesn't know. Every scene's tension can be sourced to a `KNOWS` edge differential. If two characters share the same `KNOWS` set, the scene needs another source of friction (debt, symbol, environment).

When building an excerpt for a new scene, ask:
- What does the POV character know that the antagonist does not? (Or vice versa.)
- What does the reader know that both characters do not?
- What does one character not yet know about themselves? (E.g. a body-tell they cannot read.)

## Related

- [[character-schema]] — source of `char:<id>` ids and `knowledge_set`
- [[theme-schema]] — source of `beat:t<id>` ids for SYMBOLIZES edges and `sym:<id>` ids
- [[plot-beat-schema]] — `knowledge_delta` and `symbol_activity` write deltas onto this graph
- [[scene-schema]] — `residue.graph_writes[]` is how a finished scene mutates the graph
- [[agent-contracts]] (Continuity Auditor, Symbolism Tracker)
