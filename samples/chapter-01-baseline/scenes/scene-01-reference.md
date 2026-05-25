# Scene 01 — Reference

Scene 01 is the **chapter's opening-disturbance**. It is already canonized in [samples/mvp-scene-01](../../mvp-scene-01/).

## Canonical artifacts (by reference)

| Artifact | Path |
|---|---|
| scene blueprint | [samples/mvp-scene-01/outputs/01-scene-blueprint.yaml](../../mvp-scene-01/outputs/01-scene-blueprint.yaml) |
| symbol audit | [samples/mvp-scene-01/outputs/02-symbol-audit.yaml](../../mvp-scene-01/outputs/02-symbol-audit.yaml) |
| dialogue draft (with smells) | [samples/mvp-scene-01/outputs/03-dialogue-draft.md](../../mvp-scene-01/outputs/03-dialogue-draft.md) |
| smell report | [samples/mvp-scene-01/outputs/04-smell-report.yaml](../../mvp-scene-01/outputs/04-smell-report.yaml) |
| revised draft (canon) | [samples/mvp-scene-01/outputs/05-revised-draft.md](../../mvp-scene-01/outputs/05-revised-draft.md) |
| continuity report | [samples/mvp-scene-01/outputs/06-continuity-report.yaml](../../mvp-scene-01/outputs/06-continuity-report.yaml) |

## Residue summary (what enters scenes 02 and 03)

After scene 01:

- `rel:mira-tomas.tension` = 0.92
- `sym:cracked-glass.state` = `transformed` (next legal ops: `resolve | betray`)
- `sym:old-lighter.state` = `introduced` + body-fire (rest recommended ≥ 2 scenes)
- new edge: `KNOWS { subject: char:mira, object: sym:old-lighter, level: body_only }`
- new edge: `KNOWS { subject: char:tomas, object: 'mira-retained-body-knowledge', level: full }`
- `debt:0001` (Tomas owes Mira the truth) — pressure raised
- `debt:0002` (Mira owes self: decide whether body-knowledge counts as evidence) — newly seeded
- Mira holds the leaked archive entry; Tomas does not know
- content of `event:the-redacted-event` remains undelivered to Mira and reader

## Function in this chapter

**Opening-disturbance.** The chapter inherits all of scene 01's residue as starting conditions. Subsequent scenes must honor — and pressure — that residue.
