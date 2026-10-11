# English-Psychological Baseline

This run is the **existing** [samples/mvp-scene-01](../../../mvp-scene-01/) output. It serves as the baseline against which the Japanese-literary and Vietnamese-literary regenerations are compared.

## Why this is the baseline

The MVP scene was authored under the English-psychological literary register (Cusk/Munro/Ishiguro lineage). This profile is the **statistical default** of contemporary LLM-generated literary prose — which is precisely why the framework needs to demonstrate that it can move *off* the default.

## Pinned profile (retroactive)

The MVP did not declare a culture profile (the cultural layer did not exist at that time). For comparison purposes we retrofit:

- **culture_profile_id:** `culture:english-psychological-contemporary`
- **language_style_id:** `lang:english-psychological-literary`
- **literary_style_doc_ref:** [docs/literary-styles/english-psychological-style.md](../../../../docs/literary-styles/english-psychological-style.md)

## Output artifacts (by reference)

| Artifact | Path |
|---|---|
| scene blueprint | [samples/mvp-scene-01/outputs/01-scene-blueprint.yaml](../../../mvp-scene-01/outputs/01-scene-blueprint.yaml) |
| symbol audit | [samples/mvp-scene-01/outputs/02-symbol-audit.yaml](../../../mvp-scene-01/outputs/02-symbol-audit.yaml) |
| dialogue draft (with smells) | [samples/mvp-scene-01/outputs/03-dialogue-draft.md](../../../mvp-scene-01/outputs/03-dialogue-draft.md) |
| smell report | [samples/mvp-scene-01/outputs/04-smell-report.yaml](../../../mvp-scene-01/outputs/04-smell-report.yaml) |
| revised draft (canonized) | [samples/mvp-scene-01/outputs/05-revised-draft.md](../../../mvp-scene-01/outputs/05-revised-draft.md) |
| continuity report | [samples/mvp-scene-01/outputs/06-continuity-report.yaml](../../../mvp-scene-01/outputs/06-continuity-report.yaml) |

## Key registers visible in this baseline

- **Direct accusation.** Mira's first lines confront Tomas head-on.
- **Symbol palette:** cracked glass + small brass lighter.
- **Setting register:** clinic interior with administrative tells (fluorescent flicker, dead refrigeration unit).
- **Address form:** first names throughout (`Mira`, `Tomas`).
- **Subtext mechanism:** line-level hedge and qualifier; introspection routed through `voice_signature.what_they_refuse_to_name`.
- **Apology shape:** verbalized (qualified admission).
- **Silence weight:** moderate — silences punctuate, do not carry.
- **Closing:** Mira lights the lighter, sets it back exactly as it was, walks out.

## What the cross-cultural runs preserve from this baseline

All structural invariants — see [../../invariants/shared-invariants.yaml](../../invariants/shared-invariants.yaml).

## What the cross-cultural runs change

See [../../README.md](../../README.md) for the cross-culture diff table.
