# MVP Scope

The minimum end-to-end demonstration that proves the [[narrative-pipeline]] produces measurably better narrative output than a single-prompt baseline.

## MVP Goal

**Produce one canonized chapter (~3,000–5,000 words) of a single-POV narrative through the full pipeline**, with every stage's artifact persisted and every adversarial gate firing at least once.

## In Scope

- All eleven pipeline stages exercised end-to-end.
- Full set of schemas authored for a single project:
  - 1 `theme.yaml`
  - 1 `world.yaml`
  - 2 characters (POV + 1 counterpart)
  - 1 plot skeleton (3 acts, ~9 beats)
  - 3 scenes designed in [[scene-schema]] form
- A working [[memory-graph]] (logical model; file-backed JSON is sufficient).
- All adversarial agents executing per [[anti-ai-revision-pipeline]]:
  - Theme Sentinel
  - Smell Detector (against [[ai-smells]] hard-rejects)
  - Voice Auditor
  - Continuity Agent
  - Humanization Agent
- One reference work analyzed via [[reference-analysis-system]], yielding a `reference-profile.yaml` used as a prior.
- Comparison artifact: the same prompt run through a **baseline single-prompt model**, evaluated side-by-side.

## Out of Scope (explicit)

- Multi-POV narratives.
- More than one chapter.
- UI of any kind.
- Backend / database deployment (file-backed only).
- Fine-tuning.
- Distribution / publishing.
- Authentication, user accounts, multi-user collaboration.
- Performance optimization beyond "the pipeline completes".

## Success Criteria

The MVP succeeds if:

1. The chapter passes its own canon gate ([[anti-ai-revision-pipeline]]) without manual override.
2. The Smell Detector reports zero hard-reject smells on the canon draft.
3. The Voice Auditor confirms POV `voice_signature` is honored end-to-end.
4. The Continuity Agent's graph snapshot at chapter end matches expected residue from each scene.
5. A blind human reader, given canon vs. baseline, prefers canon on at least two of three rubric axes: *theme presence*, *character specificity*, *resistance to AI smell*.

## Out-Successes (signals MVP exceeded targets)

- A revision loop catches a structural defect and forces an upstream re-open — proves the gate is real.
- A symbol introduced in scene 1 fires meaningfully in scene 3 via the graph, not via prompt recall.
- The Humanization Agent produces a net token reduction with no fact loss.

## Related

- [[first-generation-flow]]
- [[narrative-pipeline]]
- [[anti-ai-revision-pipeline]]
