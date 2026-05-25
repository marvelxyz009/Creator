# Scene Generation Workflow

End-to-end flow to produce **one canonized scene** from a plot beat. This is the atomic unit; chapter workflows compose scenes (see [chapter-generation-workflow](./chapter-generation-workflow.md)).

## Visual Flow

```
              ┌──────────────────────┐
              │   Vision Keeper      │  (pinned context — read only)
              │   Theme Analyst      │
              └──────────┬───────────┘
                         │
                         ▼
              ┌──────────────────────┐
              │ Character Psychologist│ (per scene: voice signatures pinned)
              └──────────┬───────────┘
                         │
                         ▼
              ┌──────────────────────┐
              │   Scene Director     │ → scene_blueprint.yaml
              └──────────┬───────────┘
                         │
                         ▼
              ┌──────────────────────┐
              │ Symbolism Tracker    │ ◀── (audit blueprint)
              └──────────┬───────────┘
                         │
                         ▼
              ┌──────────────────────┐
              │ Dialogue Specialist  │ → dialogue_draft.yaml
              └──────────┬───────────┘
                         │
                         ▼
              ┌──────────────────────┐
              │   Anti-AI Editor     │ ◀── (smell + humanize)
              └──────────┬───────────┘
                         │
                         ▼
              ┌──────────────────────┐
              │ Continuity Auditor   │ ◀── (graph validation)
              └──────────┬───────────┘
                         │
                         ▼
                       CANON
                  (graph.residue_writes commit)
```

## Step Sequence

### Step 0 — Orchestrator Setup
- Identify the target `plot_beat` (from Plot Engineer's output).
- Build the context bundle per [context-contract](../shared/context-contract.md).
- Pin: `theme.yaml`, `world.yaml`, participating `characters[]` (voice signatures only), prior scene's residue.

### Step 1 — Scene Director
- **Input:** plot beat + pinned bundle + memory-graph excerpt.
- **Output:** `scene_blueprint.yaml`.
- **Gate:** Blueprint validates against [scene-director](../agents/scene-director.prompt.md) checklist (has `turn`, has `residue.graph_writes`, has `theme_touch`).
- **Fail route:** `hard_reject` → re-open Plot Engineer if structural; else re-run with diagnostic.

### Step 2 — Symbolism Tracker (audit)
- **Input:** `scene_blueprint.yaml` + graph snapshot.
- **Output:** audit report (Mode A).
- **Gate:** No `hard_reject` from symbol state-machine.
- **Fail route:** `hard_reject` → re-open Scene Director with directive on which symbol op is illegal.

### Step 3 — Dialogue Specialist
- **Input:** `scene_blueprint.yaml`, participating voice signatures, asymmetric-knowledge map, recent canon voice window.
- **Output:** `dialogue_draft.yaml`.
- **Gate:** Voice swap test passes; no banned dialogue moves; rhythm arc present.
- **Fail route:** `soft_reject` → up to 2 re-runs with refined directive; on persistent failure, escalate to Character Psychologist.

### Step 4 — Anti-AI Editor (Pass 1: detect + humanize)
- **Input:** `dialogue_draft.yaml` (and prose if a Prose Agent has run — out of MVP scope but the slot exists).
- **Output:** smell report + revised draft.
- **Gate:** Hard smells = 0; net token reduction achieved; voice signatures honored.
- **Fail route:** Up to N=3 humanization cycles. On persistent failure → escalate to Scene Director (structural defect).

### Step 5 — Continuity Auditor
- **Input:** revised draft + graph snapshot + prior canon index.
- **Output:** audit report.
- **Gate:** Zero hard violations.
- **Fail route:** `hard_reject` → escalate to the agent whose artifact caused the contradiction.

### Step 6 — Canonization
- Orchestrator writes the scene's `residue.graph_writes` into the memory graph.
- Scene artifact moves to `canon/`.
- All stage reports retained under `runs/<timestamp>/scene-<id>/`.

## Loop & Re-entry Discipline

- Maximum total scene revision cycles: **3** (across all stages combined).
- Beyond 3, the orchestrator escalates upstream to **Plot Engineer** (defect is structural, not surface).
- Every re-run carries a `revision_directive` in the bundle (see [context-contract](../shared/context-contract.md)).

## Adversarial Independence

Symbolism Tracker, Anti-AI Editor, and Continuity Auditor are invoked with **minimal, independent bundles** — they must not be able to rationalize each other's leniency. See [docs/anti-ai/anti-ai-revision-pipeline.md](../../docs/anti-ai/anti-ai-revision-pipeline.md).

## Output Artifacts (per scene)

```
runs/<timestamp>/scene-<id>/
  ├─ scene_blueprint.yaml          (Scene Director)
  ├─ symbol_audit.yaml             (Symbolism Tracker)
  ├─ dialogue_draft.v1.yaml        (Dialogue Specialist)
  ├─ smell_report.v1.yaml          (Anti-AI Editor)
  ├─ revised_draft.v1.yaml         (Anti-AI Editor)
  ├─ ... (vN if multiple passes)
  ├─ continuity_report.yaml        (Continuity Auditor)
  └─ canon.yaml                    (final scene artifact)
```

## Related

- [chapter-generation-workflow](./chapter-generation-workflow.md)
- [revision-workflow](./revision-workflow.md)
