# Chapter 01 — Baseline Sample

A three-scene chapter that validates [prompts/workflows/chapter-generation-workflow.md](../../prompts/workflows/chapter-generation-workflow.md) — specifically the **chapter-level audits** (3a–3e) that cannot be performed scene-by-scene.

## What this sample proves

1. A chapter has its own **internal arc** that scenes serve.
2. **Cross-scene voice continuity** is detectable and verifiable per POV.
3. **Symbol rhythm** is auditable across a scene window.
4. **Debt pressure curve** can be tracked through a chapter and rebalanced structurally.
5. **Anti-AI second pass** at chapter level catches cross-scene patterns that scene-level passes miss.
6. **A POV shift** can be the structural pivot of a chapter, and the shift's legibility is auditable.

## Directory tree

```
samples/chapter-01-baseline/
├── README.md                                  ← this file
├── chapter-plan.yaml                          ← the chapter's design contract
├── scenes/
│   ├── scene-01-reference.md                  ← pointer to samples/mvp-scene-01 (opening-disturbance)
│   ├── scene-02/
│   │   ├── scene-blueprint.yaml
│   │   ├── final-prose.md
│   │   └── continuity-report.yaml
│   └── scene-03/
│       ├── scene-blueprint.yaml
│       ├── final-prose.md
│       └── continuity-report.yaml
├── chapter-audit/
│   ├── 3a-theme-arc-coherence.yaml
│   ├── 3b-voice-continuity.yaml
│   ├── 3c-symbol-rhythm.yaml
│   ├── 3d-debt-pressure-curve.yaml
│   └── 3e-anti-ai-second-pass.yaml
└── canon/
    └── chapter-01-canon-summary.md
```

## Chapter at a glance

| Aspect | Value |
|---|---|
| Title | "Forty Days" (references world rule r2 — edits reversible only within 40 days) |
| Sibling | baseline (English-psychological) |
| POV rhythm | `[mira, mira, tomas]` |
| Scene functions | opening-disturbance → mid-complication → end-turn |
| Theme-touch distribution | advance 0.22 / complicate 0.67 / invert 0.11 |
| Total canonical word count | ~1,960 |
| Open debts at chapter close | debt:0001 (0.95) + debt:0004 (0.95, time-bounded 39 days) |
| Symbols active in chapter | 4 (cracked-glass, lighter, complaint-form, badge); 1 arc-complete |
| POV shift | one, at scene 03; structural pivot |

## What was new compared to scene-level samples

The MVP scene sample (`samples/mvp-scene-01`) validated single-scene generation. This sample's new contribution is the **chapter-level audits**, which test properties that cannot be verified scene-by-scene:

### Audit 3a — Theme arc coherence
Validates that the chapter's *distribution* of theme-touches (advance / complicate / invert) matches the chapter plan, AND that the placement of any invert beat is structurally efficient (here: lands on the POV shift).

### Audit 3b — Voice continuity
Per POV, across all scenes the POV appears in: signature checks, drift detection, swap test. Crucially, this audit verifies that **Tomas's dialogue signature transposes cleanly to his interior signature** when the POV shifts — a property only auditable cross-scene.

### Audit 3c — Symbol rhythm
Across the chapter, verifies arc progression, over-recurrence avoidance, rest discipline, cross-symbol pressure distribution. Surfaces blueprint deviations (here: sym:cognitive-collapse-badge omitted in scene 03's humanization pass) and recommends remediation (re-schedule to chapter 02). Tracks **new seedlings** (the rim chip introduced in scene 02) for next-chapter planning.

### Audit 3d — Debt pressure curve
Tracks the *composition* of debt pressure across scenes — not just the rising/falling magnitude but **which debts are active and which retire/spike at which scenes**. Identifies structural rebalancing (here: Mira's self-debt retires-by-counter-move while Tomas accumulates two debts at end-turn) as the chapter's actual plot.

### Audit 3e — Anti-AI second pass
Catches cross-scene patterns invisible to scene-level passes:
- metaphor reuse across scenes
- rhythm drift per POV across scenes
- voice-signature collisions between POVs
- closing-image distinctiveness across scenes
- POV-shift drift (the new POV must NOT import English-psychological default-drift)

Surfaces one soft finding: all three scenes close on small objects — flagged for chapter 02 to vary close type.

## What the chapter shows operationally

### POV shift as structural pivot
The scene 03 POV shift to Tomas is the chapter's most efficient structural move. The shift happens precisely at the chapter's invert beat (beat:t1 — care that withholds vs. manipulation), inverting the reader's reading of Tomas's withholding by giving them his interior. This is structurally efficient because:

- it requires no new exposition
- it costs nothing in plot mechanics
- it produces an inversion via *proximity*, not declaration
- the reader's reading of every prior Tomas line in scene 01 retroactively shifts

### Debt-substitution as chapter shape
A naive chapter has all debts rising monotonically. This chapter retires one debt (Mira's self-debt) and introduces a new one (debt:0004) in the same arc, so the total pressure rises without exhausting the reader. The substitution IS the chapter's structural breath.

### Symbol rest discipline
The lighter rests for two scenes (per the scene-01 symbolism-tracker recommendation). The rest is enforced — even when Tomas handles the lighter in scene 03, the handling does not advance the lighter's state. This proves that *rest is a real instruction the framework honors* — symbols are not just plot tokens to be deployed maximally.

### Blueprint deviation handling
Scene 03's blueprint included sym:cognitive-collapse-badge for introduction; the humanization pass elected to subtract it. The continuity report flagged this as a soft deviation; chapter audit 3c picked it up and recommended re-scheduling to chapter 02. This shows the framework's **graceful deviation handling** — small humanization subtractions are not invariant violations and are routed to next-chapter planning rather than rejected.

## What this sample does NOT cover

- **Cross-cultural chapter regeneration.** Sibling chapters under Japanese-literary or Vietnamese-literary would require running the cultural layer across all three scenes; not produced here.
- **A chapter-level escalation path.** If chapter audit 3a (theme arc) had failed, the orchestrator would re-open the Chapter Planner or Plot Engineer. This sample's chapter passed all five audits; the escalation path remains specification-only.
- **Multiple chapters in sequence.** Chapter-to-chapter audits (theme arc across the work, debt schedule across the work, POV rhythm at work level) are work-level concerns, not validated here.

## Completing the documentation matrix

With this sample committed, the documentation-level matrix is closed:

| Property | Sample | Status |
|---|---|---|
| Single-scene generation | [mvp-scene-01](../mvp-scene-01) | ✓ |
| Cross-cultural regeneration (sibling success) | [cross-cultural-scene-01](../cross-cultural-scene-01) | ✓ |
| Invariant-violation escalation | [invariant-violation-01](../invariant-violation-01) | ✓ |
| Stereotype detection teeth | [stereotype-bait-01](../stereotype-bait-01) | ✓ |
| Chapter-level audits | **this sample** | ✓ |

All five corners populated. The framework's documentation-level validation is complete.

## Next phase

The next reasonable step is **orchestrator implementation**. With five golden-fixture samples in place — covering success path, cross-cultural path, escalation path, stereotype detection, and chapter-level audits — an implementation has the regression targets it needs.

Infrastructure decisions to make before implementation:
- runtime: Python or TypeScript?
- LLM API: Anthropic / OpenAI / multi-provider abstraction?
- memory graph: JSON-LD files, SQLite, or in-memory dict?
- orchestrator pattern: hand-rolled state machine, LangGraph, custom DAG?
- prompt-template hydration: simple string interpolation or a templating engine?

These are project-level decisions and should be surfaced to the editor / project owner before any code is written.

## Related

- [prompts/workflows/chapter-generation-workflow.md](../../prompts/workflows/chapter-generation-workflow.md)
- [prompts/workflows/scene-generation-workflow.md](../../prompts/workflows/scene-generation-workflow.md)
- [prompts/workflows/revision-workflow.md](../../prompts/workflows/revision-workflow.md)
- [docs/architecture/narrative-pipeline.md](../../docs/architecture/narrative-pipeline.md)
