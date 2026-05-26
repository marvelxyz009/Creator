# Vision Schema

Vision is the **author's contract with the work**: tone, scope, what the work refuses, what success looks like. Every downstream agent consults vision when making register/scope/refusal decisions. Vision is set by the Vision Keeper and rarely changes during generation.

## Schema

```yaml
one_sentence: "<the work distilled to one sentence — POV character + their question + the world's resistance>"

emotional_intent:
  primary: "<the dominant feeling the work cultivates — phrased as a felt experience, not an abstraction>"
  secondary:
    - "<one supporting feeling>"
    - "<another supporting feeling>"

intellectual_intent:
  question_the_work_lives_inside: "<the unanswerable question the work refuses to close>"
  refusal_to_answer_cheaply: "<one sentence on what the work will NOT do to resolve the question>"

register:
  tonal: "<concrete tonal descriptors — texture words, not adjectives>"
  formal_or_vernacular: "<where on the register spectrum + any technical-as-domestic notes>"
  pacing_default: "<measured | brisk | breath-paced + a sentence on how rhythm works>"

scope:
  intended_length: short_story         # short_story | novella | novel | scene_study
  structural_shape: "<single-scene | episodic | braided | linear-progress | other — one phrase>"
  time_span: "<concrete duration of the work's diegetic time>"

refusals:
  - "<one forbidden move, concrete and specific>"
  - "<one forbidden move>"
  - "<...>"                            # at least 3; more is better

anchoring_references:
  - title_or_id: "ref:<slug>"
    what_we_admire_structurally: "<one-sentence — what THIS reference shows the work how to do>"
    what_we_will_not_imitate: "<one-sentence — the trap of this reference>"
  - title_or_id: "ref:<slug>"
    what_we_admire_structurally: "<...>"
    what_we_will_not_imitate: "<...>"

forbidden_textures:
  - "<a genre/register trap the work must NOT slip into>"
  - "<...>"

success_criteria:
  - "<one falsifiable test — 'the reader cannot tell whether X' / 'no sentence states Y'>"
  - "<...>"
```

## Required Fields

- `one_sentence`
- `emotional_intent.primary`
- `intellectual_intent.question_the_work_lives_inside`
- `register` — all three sub-fields
- `scope.intended_length` and `scope.structural_shape`
- `refusals` — at least 3
- `success_criteria` — at least 2, each falsifiable (a test you could run on the finished prose)

## Validation Rules

1. `one_sentence` must contain a POV-character reference, a question or want, and a world-resistance. "A man goes home" fails. "A man returns home to a city whose archive no longer agrees that his daughter ever lived" passes.
2. `emotional_intent.primary` must be a **felt experience phrased concretely**, not an abstract noun. "Grief" fails. "The slow nausea of recognizing an absence" passes.
3. `intellectual_intent.question_the_work_lives_inside` must end with `?`.
4. `refusals[]` must be **specific moves**, not generic principles. "No clichés" fails. "No reconciliation; no clean accusation; no clean denial" passes.
5. `success_criteria[]` must be **falsifiable** — phrased so that a reader could check yes/no after finishing the work.
6. `anchoring_references` must include `what_we_will_not_imitate` for each entry. References without traps named are aspirational, not directional.

## How Downstream Agents Use Vision

- **Theme Analyst** sources `intellectual_intent.question_the_work_lives_inside` for `theme.core_question`.
- **Scene Director** consults `register` for tone consistency and `refusals` for scene-level forbidden moves.
- **Dialogue Specialist** consults `register.tonal` and `register.formal_or_vernacular`.
- **Anti-AI Editor** consults `forbidden_textures` for smell calibration and `success_criteria` for evaluation.
- **Continuity Auditor** consults `refusals` as additional reject conditions.

## Related

- [[theme-schema]] — `theme.core_question` derives from `intellectual_intent.question_the_work_lives_inside`
- [[world-schema]] — `register` and `forbidden_textures` shape `world.texture`
- [[agent-contracts]] (Vision Keeper)
