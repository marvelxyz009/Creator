# Revision Workflow

When an artifact (scene blueprint, dialogue draft, prose draft, or chapter) is rejected — or when an editor (human) marks accepted material as "compliant but dead" — this workflow is invoked.

Revision is **structured**, not vibes-based. Each revision **layer** has a specific lens, a specific agent, and a specific acceptance criterion.

## The Five Revision Layers

```
┌───────────────────────────────────────────┐
│ 1. Thematic Revision                      │
│    lens: does this still touch theme?     │
│    agent: theme-analyst (re-validator role)│
└─────────────────┬─────────────────────────┘
                  │
                  ▼
┌───────────────────────────────────────────┐
│ 2. Character Consistency Revision         │
│    lens: do characters honor contradiction?│
│    agent: character-psychologist + voice  │
└─────────────────┬─────────────────────────┘
                  │
                  ▼
┌───────────────────────────────────────────┐
│ 3. Prose Rhythm Revision                  │
│    lens: rhythm, pacing, sentence shape   │
│    agent: anti-ai-editor (rhythm focus)   │
└─────────────────┬─────────────────────────┘
                  │
                  ▼
┌───────────────────────────────────────────┐
│ 4. Anti-AI Revision                       │
│    lens: smells, lexicon, voice drift     │
│    agent: anti-ai-editor (full pass)      │
└─────────────────┬─────────────────────────┘
                  │
                  ▼
┌───────────────────────────────────────────┐
│ 5. Continuity Validation                  │
│    lens: graph consistency                │
│    agent: continuity-auditor              │
└─────────────────┬─────────────────────────┘
                  │
                  ▼
                CANON
```

Layers are **strictly ordered**. Higher layers expose problems that make lower-layer work wasted — fix theme before polishing prose.

## Layer 1 — Thematic Revision

- **Lens:** Does the scene/chapter still measurably touch its declared theme-beat in the declared mode (`advance | complicate | invert`)?
- **Procedure:** Theme Analyst (in re-validator mode) reads only the draft + the relevant `theme.beats[]`. Asks the `test_question` declared at theme-design time.
- **Outcome:**
  - `pass` → proceed to Layer 2.
  - `fail` → re-open Scene Director with directive that names which theme-beat is unmet and how.

## Layer 2 — Character Consistency Revision

- **Lens:** Are characters acting from their contradiction? Voice signatures held?
- **Procedure:**
  - Character Psychologist (re-validator mode) checks each character's `contradiction_tests` against the draft.
  - Voice signatures are checked line-by-line against the draft.
- **Outcome:**
  - `pass` → proceed to Layer 3.
  - `fail` (contradiction violated) → re-open Scene Director or Plot Engineer (structural).
  - `fail` (voice drift) → route to Layer 3/4 (Anti-AI Editor handles voice re-pinning).

## Layer 3 — Prose Rhythm Revision

- **Lens:** Sentence-length distribution, paragraph shape, breath control.
- **Procedure:**
  - Anti-AI Editor in **rhythm-only mode** — checks H5 (sentence-length perturbation), H7 (asymmetric punctuation), F2/F3 (structural tells).
  - Does NOT yet apply full smell scrub — that's Layer 4.
- **Outcome:**
  - `pass` → Layer 4.
  - `fail` → revise rhythm; max 2 cycles.

## Layer 4 — Anti-AI Revision

- **Lens:** Full smell scrub + humanization.
- **Procedure:** Full [anti-ai-editor](../agents/anti-ai-editor.prompt.md) pass — detect (all categories) + humanize (all H rules).
- **Outcome:**
  - `pass` (hard smells = 0, net subtraction achieved) → Layer 5.
  - `fail` after N=3 cycles → escalate to Scene Director.

## Layer 5 — Continuity Validation

- **Lens:** Memory-graph consistency.
- **Procedure:** [continuity-auditor](../agents/continuity-auditor.prompt.md) full run.
- **Outcome:**
  - `pass` → canonize.
  - `fail` → re-open the agent whose artifact caused the graph contradiction (often: Scene Director's `residue` was wrong, OR upstream artifact had a slip).

## The "Compliant But Dead" Path

When the editor (human) flags accepted material as **technically clean but flat**, none of the validators caught the problem — by definition. Run the **calibration loop**:

1. The editor names which property feels dead (e.g. "POV is too neutral", "theme is being advanced but never complicated").
2. The orchestrator updates the relevant agent's **calibration file**:
   - `voice_signature` tightened (more specific `what_they_refuse_to_name`, more aggressive `rhythmic_tells`).
   - `theme.beats[].expected_modes_distribution` rebalanced (more `complicate`, fewer `advance`).
   - `banished_phrases[]` extended with locally-overused phrases.
3. The flagged material is sent through the revision flow from Layer 1 with the recalibrated agents.

This loop is how the framework **gets sharper over time**.

## Revision Budget

Per artifact:
- Per-layer cycles: 3.
- Total revision cycles before mandatory upstream escalation: 5.
- Editor (human) can override budgets explicitly.

## Output Artifacts

```
runs/<timestamp>/<artifact>/revisions/
  ├─ layer-1-thematic.report.yaml
  ├─ layer-2-character.report.yaml
  ├─ layer-3-rhythm.report.yaml
  ├─ layer-4-anti-ai.report.yaml
  ├─ layer-5-continuity.report.yaml
  └─ final-canon.yaml | escalation.yaml
```

## Related

- [scene-generation-workflow](./scene-generation-workflow.md)
- [chapter-generation-workflow](./chapter-generation-workflow.md)
- [docs/anti-ai/anti-ai-revision-pipeline.md](../../docs/anti-ai/anti-ai-revision-pipeline.md)
