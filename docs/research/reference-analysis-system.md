# Reference Analysis System

A subsystem for ingesting reference works (novels, stories, screenplays) and extracting **structural patterns** that feed the upstream stages of the [[narrative-pipeline]] — without ever copying voice or substance.

## What we extract

Not prose. Not style. Structure.

| Layer | Examples of extracted artifacts |
|---|---|
| Macro | Act structure, tension curves, POV rotation cadence, reveal placement. |
| Meso | Scene-level turn types, residue patterns, theme-touch distribution. |
| Micro | Sentence-rhythm signatures, paragraph-shape distributions, dialogue-tag economy. |
| Negative | What the reference **refuses** to do (resolutions avoided, words absent, beats never used). |

The negative-space extraction is as important as the positive — it informs the project's `forbidden_resolutions` and `forbidden_textures`.

## Pipeline

```
reference text
   │
   ▼
[Tokenize + segment]   → paragraphs, scenes (heuristic), chapters
   │
   ▼
[Macro Analyst]        → act/beat map, tension curve estimate
[Meso Analyst]         → scene-turn taxonomy, residue patterns
[Micro Analyst]        → rhythm histograms, register fingerprint
[Negative Analyst]     → absent patterns, refused resolutions
   │
   ▼
reference-profile.yaml
   │
   ▼
fed (as influence, not content) into:
   - Theme Architect (via `core_question` priors)
   - Plot Architect (via tension-curve priors)
   - Scene Designer (via turn-type frequencies)
```

## Output: `reference-profile.yaml`

```yaml
id: ref:[work-id]
provenance: { title, author, year, license_note }

macro:
  act_structure: [...]
  tension_curve: [...]        # normalized
  reveal_placement: [...]

meso:
  scene_turn_distribution:
    knowledge: 0.31
    relation:  0.22
    debt:      0.18
    symbol-fire: 0.14
    resolve:   0.15
  residue_density: 0.86

micro:
  sentence_length_histogram: [...]
  paragraph_shape_distribution: [...]
  dialogue_tag_economy: "low; relies on action beats"

negative:
  refused_resolutions: ["redemption-by-sacrifice", "villain-monologue"]
  absent_phrases: [...]
  beats_never_used: [...]
```

## Use as Priors, Not Templates

Reference profiles are **priors**, not templates. The Plot Architect may consult three references and synthesize, but the project's own theme and constraints always override. No agent may emit prose that reproduces reference text.

## Ethics & Provenance

- Provenance is mandatory on every profile.
- The system **stores patterns, not text**. Source text is consumed for analysis and discarded.
- The framework refuses to operate as a style-cloning device. See [[narrative-laws]] Law 7.

## Related

- [[narrative-technique-library]]
- [[narrative-pipeline]]
