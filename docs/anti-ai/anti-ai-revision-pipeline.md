# Anti-AI Revision Pipeline

The gauntlet a draft must survive before it is admitted to canon. This pipeline is the **canonization gate** referenced by Law 10 of the [[narrative-laws]].

## Flow

```
prose-draft
   │
   ▼
[1] Theme Sentinel        ── does this scene advance/complicate/invert its declared beats?
   │                         reject → re-open Scene Design
   ▼
[2] Smell Detector        ── scan against [[ai-smells]] taxonomy
   │                         hard-reject smells → reject
   │                         soft-reject smells → annotate
   ▼
[3] Voice Auditor         ── line-by-line against each character's voice_signature
   │                         POV drift → reject
   │                         dialogue voice collapse → reject
   ▼
[4] Continuity Agent      ── validate against [[memory-graph]]
   │                         fact contradiction → reject
   │                         asymmetric-knowledge violation → reject
   ▼
[5] Humanization Agent    ── apply [[humanization-rules]]
   │                         enforce subtraction; re-pin voice; debanish phrases
   ▼
[6] Re-validation Sweep   ── Smell Detector + Voice Auditor + Continuity Agent run again
   │                         if any reject → loop back to [5] OR fail upstream
   ▼
CANON
```

## Loop Discipline

- Maximum revision cycles per scene: **3** by default. Beyond that, the pipeline escalates to the upstream stage (Scene Design or Character Psychology) on the assumption that the defect is structural, not surface.
- Each cycle's reports are retained as artifacts for traceability and for tuning the agents.

## Rejection vs. Annotation

- **Hard rejection** halts the pipeline and re-opens the offending upstream stage.
- **Soft rejection** annotates the draft with required revisions but allows the Humanization Agent to attempt the fix.
- **Annotation** is informational; no halt, no required rewrite.

The mapping from smell category to severity is defined in [[ai-smells]].

## Adversarial Independence

Each validator is invoked with a **minimal bundle** containing only what it needs:
- Theme Sentinel sees `theme.yaml` and the draft.
- Voice Auditor sees voice signatures and the draft.
- Continuity Agent sees the [[memory-graph]] snapshot and the draft.

This isolation prevents validators from rationalizing each other's permissive readings — they must judge independently.

## Output Contracts

Every validator emits a structured report. Reports never contain rewrites; rewrites are only authored by the Humanization Agent or, on escalation, by the re-opened generative agent.

## Anti-Pattern: The Optimization Trap

A naive pipeline tuned to minimize validator rejection rates will collapse to **bland but compliant** prose. Mitigations:

- The Humanization Agent's H9 (subtract-before-adding) and H1 (specificity substitution) push against blandness from the inside.
- Periodic sampling: the editor (human) reviews accepted scenes and can mark them as **"compliant but dead"** — this raises the bar for future validator calibration.

## Related

- [[ai-smells]]
- [[humanization-rules]]
- [[narrative-laws]]
- [[agent-contracts]]
