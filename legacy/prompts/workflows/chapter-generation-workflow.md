# Chapter Generation Workflow

A chapter is a **sequence of scenes** chosen such that the chapter's own arc — its own micro-shape of tension, release, and turn — is honored. Chapters are **not** mere prose concatenations; they are structurally distinct.

## Visual Flow

```
Plot Engineer ──── act/beat tree ─────────────────────────┐
                                                          │
                                                          ▼
                                          ┌─────────────────────────┐
                                          │   Chapter Planner       │
                                          │   (orchestrator role)   │
                                          └────────────┬────────────┘
                                                       │
                                       chapter_plan.yaml (sequence of plot beats)
                                                       │
                ┌──────────────────────────────────────┴──────────────────────┐
                ▼                                                             ▼
        [Scene Generation Workflow]    × N  (one per scene in chapter_plan)
                │
                ▼
        canonized scenes  ─────────┐
                                   │
                                   ▼
                       ┌─────────────────────────┐
                       │ Chapter-Level Audit     │
                       │  - Theme arc coherence  │
                       │  - Voice continuity     │
                       │  - Symbol rhythm        │
                       │  - Debt pressure curve  │
                       │  - Anti-AI second pass  │
                       └────────────┬────────────┘
                                    │
                                    ▼
                              CHAPTER CANON
```

## Step 1 — Chapter Planning

The orchestrator (or a dedicated Chapter Planner role) selects a contiguous slice of `plot.beats[]` for this chapter.

Constraints on chapter shape:

- **Internal arc.** Chapter has its own opening-disturbance, mid-complication, and end-turn — even when embedded in a larger act arc.
- **POV discipline.** POV changes per scene allowed, but the chapter declares its **POV rhythm** (e.g. `[mira, mira, tomas, mira]`).
- **Tension shape.** Chapter has a declared tension shape (e.g. `slow-build → relief → spike → quiet residue`).
- **Symbol rhythm.** Chapter must touch symbols deliberately — over-touch fatigues, under-touch drifts.
- **Debt pressure curve.** Each chapter raises pressure on at least one open debt OR introduces a new one.

### Chapter Plan Output

```yaml
chapter_plan:
  id: chapter:<id>
  position: act-<n>.chapter-<m>
  plot_beats_covered: [beat:p<id>, ...]
  scene_sequence:
    - scene_id: scene:<id>
      plot_beat: beat:p<id>
      pov: char:<id>
      function_in_chapter: opening | complication | mid-turn | rest | end-turn | aftermath
  pov_rhythm: [char:<id>, ...]
  tension_shape: <terse — e.g. "slow-build → relief → spike → quiet residue">
  symbol_rhythm:
    - symbol: sym:<id>
      touches: [<scene ids where it appears>]
  debt_pressure_arc:
    - debt: debt:<id>
      pressure_in_each_scene: [<floats>]
  forbidden_within_chapter:
    - <e.g. "no scene ends on dialogue resolution">
```

## Step 2 — Per-Scene Generation

For each scene in `scene_sequence`:
- Run the full [scene-generation-workflow](./scene-generation-workflow.md).
- Scene context bundle includes a **chapter_position hint** so Scene Director knows whether this is opening / mid-turn / end-turn.
- Voice-continuity window for POV pulls from the *immediately prior canon scene* with that POV, not from the prior scene-in-chapter.

## Step 3 — Chapter-Level Audit

After all scenes are canonized, run a **chapter-level audit** that cannot be performed scene-by-scene:

### 3a — Theme Arc Coherence
- Does the chapter's sequence of `theme_touch[].mode` (advance/complicate/invert) form a meaningful arc, or is it noise?
- Reject chapters that touch every theme-beat in `advance` mode — too monotonic.

### 3b — Voice Continuity
- For each POV, run the [anti-ai-editor](../agents/anti-ai-editor.prompt.md) in **voice-drift detection mode** across all that POV's scenes in the chapter.

### 3c — Symbol Rhythm
- [symbolism-tracker](../agents/symbolism-tracker.prompt.md) audits the chapter as a whole — looking for over-recurrence and dangling symbols at chapter close.

### 3d — Debt Pressure Curve
- Verify `debt_pressure_arc` declared in the plan matches what was actually written.
- Debts whose pressure plateaued through the chapter without movement are flagged.

### 3e — Anti-AI Second Pass
- Anti-AI Editor runs on the **chapter as a whole**, looking for cross-scene smells:
  - Same metaphor reused across scenes.
  - Same sentence-rhythm in different POVs.
  - Repeated lexical tells beyond signature distinctiveness.

## Step 4 — Chapter Canonization

- Chapter artifact: `canon/chapter-<id>/`
  - `chapter_plan.yaml`
  - symlinks or copies to each scene's `canon.yaml`
  - `chapter_audit.yaml` (theme arc, voice, symbol, debt, anti-AI second pass)
- Memory graph confirms all chapter-level residue.

## Loop Discipline at Chapter Level

- If chapter-level audit fails on **theme arc**: re-open Chapter Planner (re-sequence or re-select beats).
- If chapter-level audit fails on **voice continuity**: re-open the offending scenes with directive.
- If chapter-level audit fails on **symbol rhythm**: re-open Symbolism Tracker for proposal, then offending scene(s).
- Max chapter-level re-runs: **2**. Beyond that, escalate to Plot Engineer.

## What This Workflow is NOT

- It is **not** a prose-concatenation pass. Chapters are *composed*, not *glued*.
- It is **not** a continuity sweep — that's per-scene's Continuity Auditor's job.
- It is **not** a style-unification pass — voice differentiation per POV is preserved.

## Related

- [scene-generation-workflow](./scene-generation-workflow.md)
- [revision-workflow](./revision-workflow.md)
- [docs/architecture/narrative-pipeline.md](../../docs/architecture/narrative-pipeline.md)
