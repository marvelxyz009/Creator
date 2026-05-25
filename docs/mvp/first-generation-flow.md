# First Generation Flow

The concrete, step-by-step run that produces the MVP chapter described in [[mvp-scope]]. This is the walkthrough that every implementer should be able to trace, stage by stage, against the artifacts on disk.

## Pre-Run Inputs

- `brief.md` — one page: premise, intended tone, intended length, intended audience.
- 1 reference work, profiled via [[reference-analysis-system]] → `reference-profile.yaml`.

## Step-by-Step

### Step 1 — Vision
- **Agent:** Vision Agent
- **In:** `brief.md`, `reference-profile.yaml`
- **Out:** `vision.md` (one page; not a schema — prose distillation)
- **Gate:** Editor (human) signs off before stage 2 begins.

### Step 2 — Theme
- **Agent:** Theme Architect
- **Out:** `theme.yaml` per [[theme-schema]]
- **Gate:** Schema validation. `core_question` ends with `?`. Oppositions material. Forbidden resolutions non-empty.

### Step 3 — World
- **Agent:** World Architect
- **Out:** `world.yaml` per [[world-schema]]
- **Gate:** Every `logic.rules[]` has teeth. At least one location bound to theme.

### Step 4 — Characters
- **Agent:** Character Psychologist
- **Out:** `characters/<pov>.yaml`, `characters/<counterpart>.yaml` per [[character-schema]]
- **Gate:** Each character carries an active contradiction. Voice signatures differ.
- **Graph writes:** character nodes, initial relation edge between the two.

### Step 5 — Plot
- **Agent:** Plot Architect
- **Out:** `plot.yaml` — 3 acts, ~9 beats. Each beat: target theme-beat id(s) and target turn-type.
- **Gate:** Tension curve monotonicity-with-relief checked against `reference-profile.yaml` priors.

### Step 6 — Scenes
- **Agent:** Scene Designer
- **Out:** `scenes/01.yaml`, `scenes/02.yaml`, `scenes/03.yaml` per [[scene-schema]]
- **Gate:** Each scene has a `turn` and non-empty `residue.graph_writes`. Theme-touch declared.

### Step 7 — Dialogue
- **Agent:** Dialogue Agent (per scene)
- **In:** scene + character `voice_signature`
- **Out:** dialogue drafts attached to scene artifacts.
- **Gate:** Voice Auditor preview check; refuse generic dialogue early.

### Step 8 — Prose
- **Agent:** Prose Agent (per scene)
- **In:** scene + dialogue + bundle from [[context-assembly]]
- **Out:** `drafts/scene-XX.prose.md`
- **Note:** This output is **not canon**. It is raw material for stage 9+.

### Step 9 — Revision (adversarial)
- **Agents:** Theme Sentinel → Smell Detector → Voice Auditor (independent invocations)
- **Out:** structured reports.
- **Routing:**
  - Hard rejects → re-open upstream (scene or character).
  - Soft rejects → annotate; pass to humanization.

### Step 10 — Continuity Validation
- **Agent:** Continuity Agent
- **In:** draft + memory-graph snapshot
- **Out:** continuity report.
- **Routing:** any contradiction → hard reject; re-open scene with directive.

### Step 11 — Humanization
- **Agent:** Humanization Agent
- **In:** validated draft + voice signatures + banished-phrase list
- **Out:** humanized draft (net token reduction expected per H9).
- **Re-validation sweep:** Smell Detector + Voice Auditor + Continuity Agent re-run.

### Canonization
- The chapter is written to `canon/chapter-01.md`.
- Graph writes from each scene's `residue` are committed.
- Reports from all stages are retained under `runs/<timestamp>/`.

## Comparison Run

Independently, a **baseline run** issues a single prompt:

> *"Write chapter 1 of a novel about [premise from brief]. ~4,000 words. Literary tone."*

Both outputs are presented blind to the human evaluator per [[mvp-scope]] success criteria.

## Failure Drills (must demonstrate at least one)

1. **Forced upstream re-open** — at least one scene is rejected by Theme Sentinel and re-designed.
2. **Symbol fire across scenes** — a symbol introduced in scene 1 transforms in scene 3 via the graph.
3. **Humanization subtraction** — Humanization pass measurably reduces tokens while preserving canonical facts (verified by Continuity Agent re-run).

## Related

- [[mvp-scope]]
- [[narrative-pipeline]]
- [[anti-ai-revision-pipeline]]
- [[memory-graph]]
