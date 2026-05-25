# Context Contract

Every agent receives a **tailored context bundle** — never the whole project. This file defines the contract the orchestrator honors when assembling that bundle, and the contract each agent honors when consuming it.

Mirrors [docs/architecture/context-assembly.md](../../docs/architecture/context-assembly.md).

## Bundle Shape

```yaml
bundle:
  for_agent: <agent-id>
  task_id: <opaque>
  budget_tokens: <int>

  pinned_artifacts:
    - path: <artifact path>
      fields: [<field paths>]      # only these fields are loaded

  graph_queries:
    - description: <human-readable>
      result: <inline result>

  recent_canon:
    - scene: <scene-id>
      window: last_N_words
      content: <prose snippet>

  constraints:
    rules: [R1, R3, R6, ...]       # explicit rule ids to honor
    additional: <free text>

  revision_directive: <optional — only present on re-runs>
```

## Inclusion Rules (orchestrator side)

1. **Starvation default.** Include nothing unless the agent contract requires it.
2. **Pin what the contract names.** Each agent prompt lists `required_inputs`; those are pinned.
3. **Query, don't dump.** Memory comes from graph queries, not from concatenated prior prose.
4. **Bound recency.** `recent_canon` is the **last N words only**, for voice continuity — never full chapters.
5. **Trace every inclusion.** Every piece of bundle data has a justification field.

## Consumption Rules (agent side)

Every agent prompt enforces:

1. **Use only what is in the bundle.** Do not hallucinate prior facts, characters, or events not present.
2. **If a required input is missing, escalate.** Status `escalate`, name the missing input. Do not improvise.
3. **Do not re-summarize the bundle in the output.** The output is the agent's *new* contribution.
4. **Honor `revision_directive` if present.** It supersedes default behavior for this run.

## Missing Input Protocol

When required input is absent:

```yaml
status: escalate
rejection:
  reason: "Required input missing"
  missing_inputs: [<input names>]
  suggested_repair: "Re-run [upstream agent] to produce <artifact>"
```

The agent does NOT invent the missing input.

## Voice Continuity Window

When `recent_canon` is included for voice continuity:
- Window is typically the **last 300–500 words** of the most recent canon scene featuring the relevant POV.
- It is consumed for **voice signature reference only** — not for plot recall (plot comes from the graph).

## Related

- [global-narrative-rules.md](./global-narrative-rules.md)
- [output-format-rules.md](./output-format-rules.md)
- [docs/architecture/context-assembly.md](../../docs/architecture/context-assembly.md)
- [docs/architecture/memory-graph.md](../../docs/architecture/memory-graph.md)
