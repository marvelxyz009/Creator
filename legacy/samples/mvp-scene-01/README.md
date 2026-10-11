# MVP Scene 01 — Sample Generation

A fully populated walkthrough of the [scene-generation-workflow](../../prompts/workflows/scene-generation-workflow.md) for a single scene. This sample exists to **validate the prompt templates and workflow** end-to-end against a concrete, non-trivial narrative case.

## Scene Premise

> **Genre:** psychological sci-fi / melancholic mystery
> **Setting:** Vel Anor — a coastal administrative city whose state runs a Memory Archive that can edit citizens' memory.
> **Scene:** Mira confronts Tomas in an abandoned memory clinic. She has obtained a leaked archive entry showing he edited a portion of her memory of him. The scene **complicates rather than resolves**: it withholds the content of the redacted event and instead lets Mira's body recognize his lighter despite her archive containing no record of her ever seeing it.

## What This Sample Validates

| Concern | File(s) demonstrating it |
|---|---|
| **Theme schema produces testable beats** | `inputs/theme.yaml` |
| **Characters render as contradictions, not traits** | `inputs/characters/*.yaml` |
| **World rules pressure theme dramatically** | `inputs/world.yaml` |
| **Plot beats specify intended turn-type + knowledge delta** | `inputs/plot_beat.yaml` |
| **Memory graph asymmetric-KNOWS works in practice** | `inputs/memory_graph_excerpt.yaml` |
| **Scene Director produces blueprint with turn, residue, prose_constraints** | `outputs/01-scene-blueprint.yaml` |
| **Symbolism Tracker enforces state-machine legality** | `outputs/02-symbol-audit.yaml` |
| **Dialogue Specialist drafts (with smells) before humanization** | `outputs/03-dialogue-draft.md` |
| **Anti-AI Editor catches concrete smells with line refs** | `outputs/04-smell-report.yaml` |
| **Humanization produces a measurably leaner, voice-pinned draft** | `outputs/05-revised-draft.md` |
| **Continuity Auditor anchors every verdict to a graph node** | `outputs/06-continuity-report.yaml` |

## File-by-File Notes

### Inputs

- **`vision.yaml`** — Validates that [vision-keeper](../../prompts/agents/vision-keeper.prompt.md) produces a *durable spine*, not a back-cover blurb. Note the explicit `refusals[]` and `success_criteria[]` that downstream agents will be tested against.
- **`theme.yaml`** — Validates that [theme-analyst](../../prompts/agents/theme-analyst.prompt.md) makes theme into *testable beats* with `test_question` and `expected_modes_distribution`. The `core_question` is genuinely open; `forbidden_resolutions` is non-empty.
- **`world.yaml`** — Validates [lore-architect](../../prompts/agents/lore-architect.prompt.md): every rule has `consequence_if_broken`; factions carry `internal_contradiction`; `unknowns` are reserved.
- **`characters/mira.yaml`, `tomas.yaml`** — Validates [character-psychologist](../../prompts/agents/character-psychologist.prompt.md). The two contradictions per character are *materially opposed* (not graded). Voice signatures differ along all four required axes. `what_they_refuse_to_name[]` populated for both POVs. Each contradiction is `bound_to_opposition` from `theme.yaml`.
- **`plot_beat.yaml`** — A single beat slice (not the full plot). Validates that [plot-engineer](../../prompts/agents/plot-engineer.prompt.md) output is *consumable per scene* by the Scene Director.
- **`memory_graph_excerpt.yaml`** — Validates that the [memory-graph](../../docs/architecture/memory-graph.md) supports asymmetric `KNOWS` edges, symbol state, and open debts before a scene runs. Note: `event:the-redacted-event` has `who_knows_nothing: [char:mira]` — this gates the scene.

### Outputs

- **`01-scene-blueprint.yaml`** — The atomic output of [scene-director](../../prompts/agents/scene-director.prompt.md). Validates: `turn` present, `residue.graph_writes` non-empty, `ending_hook.type: gesture` (not question), `prose_constraints.forbidden[]` is scene-specific (not generic), `micro_beats[]` mapped.
- **`02-symbol-audit.yaml`** — Validates [symbolism-tracker](../../prompts/agents/symbolism-tracker.prompt.md) Mode A (audit). Legality check: `sym:cracked-glass.introduced → transformed` is a legal transition; `sym:old-lighter.not_yet_introduced → introduced` is legal. Both `forbidden_uses` are honored. Recommendations for future scenes are emitted.
- **`03-dialogue-draft.md`** — The **first-pass rendering**. *Deliberately* carries Category A1, C1, C4, A2 smells so the next stage has something to bite. Note: blueprint-level constraints (POV, lighter staging, no rhetorical-question close) are already honored; only surface-level realization is degraded. **Format note**: the prompt template specifies YAML for dialogue draft; this sample renders prose-form because the prose stage is conceptually the consumer downstream of dialogue. Treat this as the dialogue-specialist output composited with a prose-stage rendering for sample-readability. An orchestrator implementation may choose to keep these stages strictly separate.
- **`04-smell-report.yaml`** — Validates [anti-ai-editor](../../prompts/agents/anti-ai-editor.prompt.md) detection pass: every smell has a category code, a line ref, an offending quote, and a diagnostic. Voice-drift entries are tied to specific characters. Banished-phrase hits include "a mix of", "for a moment", "for a long moment". Status is `soft_reject` — pipeline continues to humanization.
- **`05-revised-draft.md`** — Validates the humanization pass. **Net token reduction: ~140 (16%)** — `delta` is positive (H9). Every cut is logged with an applied rule code. `preserved_facts[]` re-verified against the blueprint. Self-verification block confirms no hard smells remain.
- **`06-continuity-report.yaml`** — Validates [continuity-auditor](../../prompts/agents/continuity-auditor.prompt.md). Every check is graph-anchored: knowledge asymmetry per character, symbol state transitions, debt pressure changes, residue-writes traced to specific draft beats. Status: `ok`, `canonization_authorized: true`.

## What This Sample Demonstrates Working

1. **End-to-end traceability.** Every claim in the final continuity report traces to a graph node or blueprint field.
2. **Asymmetric knowledge is real.** Mira holds the leaked entry; Tomas does not learn that fact; the reader knows Mira holds it. All three knowledge states are preserved.
3. **Symbols advance via state machine.** Cracked-glass moves `introduced → transformed`. Lighter is introduced. Neither is named as a symbol in narration.
4. **Humanization measurably subtracts.** Token count drops ~16% while every canonical fact is preserved.
5. **The ending hook works without narration.** The lighter-firing beat carries the theme-touch (beat:t3 advance) without a single sentence of reflection.

## What This Sample Does NOT Cover

- **Multi-scene chapter-level audits** ([chapter-generation-workflow](../../prompts/workflows/chapter-generation-workflow.md)).
- **Re-opening upstream** when a hard reject fires — this sample's flow was clean enough that no escalation triggered. A follow-up sample should deliberately stage an escalation (e.g. Symbolism Tracker rejecting an illegal symbol op) to validate the failure path.
- **Multiple humanization cycles.** Only one pass was needed here. A more degraded first draft would exercise the N=3 loop.
- **Voice-drift across scenes.** Voice continuity is tested per-character within a scene; cross-scene drift detection is a chapter-level concern.

## Template Issues Found

None blocking. Two minor notes from authoring this sample:

1. **Dialogue draft format ambiguity.** The dialogue-specialist prompt emits YAML; in practice, downstream prose-stage rendering benefits from an intermediate markdown form for human review. The orchestrator should decide whether to keep these as two stages (YAML dialogue → markdown prose) or merge them. The sample currently composites them under `03-dialogue-draft.md`; the prompt template was not modified.
2. **Symbol "compressed introduction + fire" case.** The `sym:old-lighter` arc compressed introduction and body-fire into one scene. The Symbolism Tracker prompt handles this correctly (notes the compression and recommends rest), but the prompt template could add an explicit field for "intra-scene multi-op" to make the audit more rigorous. Non-blocking.

## Next Steps

1. **Author a deliberate-failure sample** that triggers `hard_reject` from the Continuity Auditor (e.g. Mira refers in dialogue to an event the graph says she does not know) — validates the escalation path.
2. **Author a chapter-level sample** (3 scenes) — validates [chapter-generation-workflow](../../prompts/workflows/chapter-generation-workflow.md) including theme-arc and symbol-rhythm chapter-level audits.
3. **Begin orchestrator implementation** once the failure-path sample is in place. The samples here become golden-test fixtures.

## Related

- [docs/foundation/creator-framework-manifest.md](../../docs/foundation/creator-framework-manifest.md)
- [prompts/workflows/scene-generation-workflow.md](../../prompts/workflows/scene-generation-workflow.md)
- [prompts/workflows/revision-workflow.md](../../prompts/workflows/revision-workflow.md)
