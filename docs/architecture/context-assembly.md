# Context Assembly

The component that builds a **tailored context bundle** for every agent invocation. No agent receives "the whole project" — each receives exactly what its contract requires.

## Why this exists

Naïve pipelines stuff every prior artifact into the next prompt. This:
- Wastes tokens.
- Encourages averaging (the model attends to noise).
- Hides which inputs actually drove which decisions.
- Makes failures un-diagnosable.

Context Assembly inverts the default: **starvation is the default; inclusion is justified**.

## The Assembly Contract

For every agent invocation, the assembler produces:

```yaml
bundle:
  agent: scene-designer
  task_id: scene-04-12
  pinned:
    - theme.yaml#core_question
    - characters/mira.yaml#contradiction
    - characters/tomas.yaml#voice_signature
  graph_queries:
    - "unresolved debts between mira and tomas"
    - "symbols introduced but unresolved as of act 2"
    - "what mira knows that tomas does not"
  recent_canon:
    - scene-04-11.prose (last 400 words only)
  constraints:
    - narrative-laws: [law-2, law-3, law-6]
  budget_tokens: 6000
```

## Assembly Rules

1. **Pin what the contract names.** Every agent contract in [[agent-contracts]] lists which schema fields it *must* see. Those are pinned.
2. **Query, don't dump.** Memory is fetched via graph queries against the [[memory-graph]], not by including raw prior prose.
3. **Bound recency.** Recent canon prose is included only as the last N words for voice continuity — never full chapters.
4. **Budget-aware.** Each bundle has a token budget. Overflow forces the assembler to *summarize-and-cite* rather than include verbatim.
5. **Trace every inclusion.** The bundle records *why* each piece was included. Failures can be traced to missing or wrong inclusions.

## What is NOT in the bundle

- Prior prompts.
- The agent's own previous outputs (unless explicitly re-opened).
- Other agents' working notes.
- Generic "writing tips".

## Interaction with Revision

When the [[anti-ai-revision-pipeline]] re-runs a stage, it can attach a **revision directive** to the bundle, e.g. *"the prior draft violated Law 3 in paragraph 4 — rewrite to imply rather than state"*. This is the only sanctioned form of cross-stage feedback.

## Related

- [[memory-graph]]
- [[narrative-pipeline]]
- [[agent-contracts]]
