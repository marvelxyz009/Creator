# Agent Contracts

Every agent in [[agent-system]] is defined by a contract: **typed inputs**, **typed outputs**, **invariants**, and **failure modes**. Contracts are the source of truth for what an agent must accept, produce, and refuse.

## Contract Format

```yaml
agent: <name>
version: <semver>
stage: <pipeline stage number>
inputs:
  required: [<artifact refs / graph queries>]
  optional: [<...>]
outputs:
  artifact: <path / schema>
  graph_writes: [<node/edge types this agent may write>]
invariants:
  - <law or property that must hold on output>
failure_modes:
  - condition: <when to fail>
    response: <how to fail loudly>
```

## Selected Contracts

### Theme Architect

```yaml
agent: theme-architect
stage: 2
inputs:
  required: [vision.md]
outputs:
  artifact: theme.yaml      # see [[theme-schema]]
  graph_writes: [theme-beat]
invariants:
  - At least one explicit core_question.
  - At least one thematic opposition (e.g. "freedom vs. belonging").
  - Every theme-beat has a measurable scene-level test.
failure_modes:
  - condition: theme is a single noun ("love", "war").
    response: reject; demand opposition or question.
```

### Character Psychologist

```yaml
agent: character-psychologist
stage: 4
inputs:
  required: [theme.yaml, world.yaml]
outputs:
  artifact: characters/<name>.yaml   # see [[character-schema]]
  graph_writes: [character, relation, debt]
invariants:
  - Every character has >= 1 active contradiction.
  - Voice signature includes: sentence_length_distribution, lexical_register, what_they_notice, what_they_refuse_to_name.
  - No character resolvable to a single archetype label.
failure_modes:
  - condition: contradiction is cosmetic ("brave but sometimes scared").
    response: reject; demand structural opposition with stakes.
```

### Scene Designer

```yaml
agent: scene-designer
stage: 6
inputs:
  required: [plot.yaml, characters/*.yaml, theme.yaml]
  graph_queries:
    - unresolved debts among scene participants
    - symbols available to fire/transform
outputs:
  artifact: scenes/<id>.yaml         # see [[scene-schema]]
invariants:
  - Scene has: goal, conflict, turn, residue.
  - Scene measurably touches >= 1 theme-beat.
  - Scene leaves residue (debt, symbol-state, knowledge asymmetry) in the graph.
failure_modes:
  - condition: scene has no turn (state of participants unchanged).
    response: reject as "transit scene".
```

### Smell Detector (adversarial)

```yaml
agent: smell-detector
stage: 9
inputs:
  required: [prose-draft]
outputs:
  artifact: smell-report.yaml
invariants:
  - Reports every match against [[ai-smells]] taxonomy with line refs.
  - Does NOT rewrite. Reports only.
failure_modes:
  - condition: returns "no smells found" on a draft > 800 words.
    response: re-run with stricter threshold; suspect detector miscalibration.
```

### Continuity Agent (adversarial)

```yaml
agent: continuity-agent
stage: 10
inputs:
  required: [draft, memory-graph snapshot]
outputs:
  artifact: continuity-report.yaml
invariants:
  - Any contradiction with the graph is a hard reject.
  - Asymmetric-knowledge violations (a character "knows" something they shouldn't) are hard rejects.
failure_modes:
  - condition: graph is empty/uninitialized.
    response: fail loudly; do not pass-through.
```

### Humanization Agent

```yaml
agent: humanization-agent
stage: 11
inputs:
  required: [validated-draft, voice-signatures]
outputs:
  artifact: humanized-draft
invariants:
  - Applies all rules from [[humanization-rules]].
  - Preserves canonical facts; perturbs only realization.
failure_modes:
  - condition: output diverges from validated facts.
    response: reject own output; re-run with tighter fact pinning.
```

## Versioning

Contracts are versioned. A pipeline run pins a contract version per agent so reruns are reproducible.

## Related

- [[agent-system]]
- [[narrative-pipeline]]
- [[ai-smells]]
- [[humanization-rules]]
