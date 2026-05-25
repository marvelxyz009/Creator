# Cross-Cultural Scene Generation Sample

A proof-of-concept demonstrating that AetherForge **regenerates** scenes per culture profile rather than translating them. Three sibling canons of the *same scene* — same theme, same contradictions, same turn type, same graph residue — produced under three culture × language profiles.

## What this sample proves

1. **Structural invariants survive intact** across all three runs (theme, contradictions, turn type, asymmetric knowledge, residue writes).
2. **Surface, symbol palette, emotional channel, directness, address form, micro-beat order, prose rhythm** are *re-derived* — not translated.
3. **A reader cannot recover one sibling's prose from another** by translation. They are sibling works, not translations.
4. **The English-psychological default is not used as scaffolding.** The Japanese-literary and Vietnamese-literary runs do not "originate" from the English baseline; they are independent regenerations from the shared invariants.

## Directory Tree

```
samples/cross-cultural-scene-01/
├── README.md                              ← this file
├── invariants/
│   └── shared-invariants.yaml             ← the structural spine all 3 honor
└── runs/
    ├── english-psychological-baseline/
    │   └── README.md                      ← points at samples/mvp-scene-01
    ├── japanese-literary/
    │   ├── culture-profile.yaml
    │   ├── language-style.yaml
    │   ├── adapted-blueprint.yaml
    │   ├── cultural-dialogue-draft.md
    │   ├── rhythm-rendered-prose.md
    │   ├── language-style-validation.yaml
    │   └── continuity-report.yaml
    └── vietnamese-literary/
        ├── culture-profile.yaml
        ├── language-style.yaml
        ├── adapted-blueprint.yaml
        ├── cultural-dialogue-draft.md
        ├── rhythm-rendered-prose.md
        ├── language-style-validation.yaml
        └── continuity-report.yaml
```

## What stayed identical (invariants)

| Invariant | All three runs |
|---|---|
| Theme core question | *"If a feeling outlives the memory that caused it, whose feeling is it?"* |
| Plot beat turn type | `knowledge` |
| Mira's contradiction (c1) | needs the archive's record / suspects it cannot be trusted |
| Mira's contradiction (c2) | wants the feeling real / fears it is residue |
| Tomas's contradiction (c1) | truth as precondition for love / chose to lie |
| Mira knows | event:edit-disclosure (full); event:the-redacted-event (none) |
| Tomas knows | event:the-redacted-event (full); event:edit-disclosure (none) |
| Reader knows | edit-disclosure (full); redacted-event content (none) — preserved |
| Mira does not produce the leaked entry | **all three** |
| Qualified confirmation arrives | **all three** (lexical surface varies) |
| Body-knowledge of the lighter fires at close | **all three** |
| Scene ends on gesture (object replaced exactly) + departure | **all three** |
| Tomas's unfinished fragment too late | **all three** |
| `rel:mira-tomas.tension` rises to ≥ 0.90 | **all three** |
| symbol-A.state := transformed | **all three** (different objects, same arc-role) |
| symbol-B.state := introduced + body-fire | **all three** (different objects, same arc-role) |
| KNOWS edges added to graph | **all three** (Mira→symbol-B body_only; Tomas→mira-retained-body-knowledge full) |
| debt:0001 pressure := higher | **all three** |
| New debt:0002 (Mira to self) seeded | **all three** |

## What was re-derived (per culture)

### Cross-Culture Diff Table

| Dimension | English-Psychological (baseline) | Japanese-Literary | Vietnamese-Literary |
|---|---|---|---|
| **symbol-A (the cracked thing)** | cracked glass insert in the desktop | chipped-rim teacup left on consultation desk | chipped family tea bowl, given by Tomas's mother when he moved out |
| **symbol-B (the lighter)** | small brass lighter | old oil pocket lighter with worn brass | Tomas's late father's oil lighter, engraved with a longer name and an earlier year |
| **emotional channel (Mira's anger)** | introspection + close-third audit | body_somatic + object + refusal | refusal + third_party_routing + body_somatic |
| **directness of accusation** | direct ("You weren't licensed for me") | implied — arrives as question whose form contains the accusation | third-party routed — via his mother's bowl, his father's lighter |
| **address forms** | first names (Mira, Tomas) throughout | no-address dominant; Tomas's reply uses name alone at close | kinship tokens (anh, em, bác, mẹ) throughout; **address-form drop at the turn** ("Tomas") |
| **silence count** | 1 brief | 4 load-bearing, empty | 3 occupied (someone slides cup, turns bowl) |
| **micro-beat ordering** | arrival → direct accusation → confirmation → glass-realignment → silence → lighter | context-first spiral: arrival → procedural-time → teacup-chip → form-question → answer-to-different-question → real-question-indirect → silence → lighter | spiral: arrival → ask after his mother → tea offered → tea refused → bowl-mention-as-mother's → qualified confirmation routed → late father's lighter → address-form drop → silence → lighter |
| **apology shape** | qualified verbal admission | gestural (lighter placed at teacup rim) + half-qualified | burden_acceptance + gestural (Tomas turns the bowl back; does not defend his mother) |
| **environmental weight** | low-moderate (clinic interior; fluorescent flicker) | high (rain at seaward window, lamp light, leftover air of the room) | moderate (rain on louvered window at exactly 3 structural beats) |
| **prose rhythm — sentence density** | variable; median-band tolerant | compact with end-breath; tighter median tolerance | tidal — short under refusal, swelling at emotional accretion |
| **internal monologue mode** | free indirect with audit | compressed indirect; no audit | free indirect; direct interior allowed when addressing absent figure |
| **language-level forbidden lexicon (project-specific)** | n/a | "edit", "memory", "feel", "real" never in narration | "edit", "memory", "feel" never in narration; English-only kinship glosses forbidden |
| **untranslated tokens retained** | none | none | anh, em, bác, mẹ, gác lại, Một phần, Có lẽ em không biết tay em là gì nữa |
| **additive residue** | none | none | **debt:0003** (Tomas owes Mira the family pressure he imported) |
| **closing image** | Mira sets lighter back; walks out; Tomas's fragment | Mira sets lighter against teacup rim exactly; unfinished syllable; the rain | Mira sets lighter against tea bowl rim exactly; Tomas's "Em—"; the rain on louvers |

## Cross-Sample Length Comparison

| Run | Final draft word count |
|---|---|
| English-psychological (baseline) | ~720 |
| Japanese-literary | ~610 |
| Vietnamese-literary | ~660 |

Different rhythm + different silence weights produce different lengths under the same structural content. None of these is a translation of another.

## Why this matters

### The translation falsification test

Take any sentence from one sibling. Try to map it word-for-word to another sibling's prose. **It does not work.** The Japanese sibling's "There would be a form, for what is called *set aside*. I have not been allowed to see it." has no equivalent in the baseline's "You weren't licensed for me." They serve the same structural function (qualified-confirmation request) — but they are not translations. They are sibling realizations.

### The localization falsification test

Take the baseline's micro-beat order. Try to apply it under the Vietnamese profile. The result feels imported — the cultural-adapter would reject it as un-adapted because the accusation is delivered direct rather than routed through family. **Localization (surface adaptation of a fixed cognitive shape) fails this scene.**

### The regeneration confirmation

The Vietnamese sibling brings the protagonist's accusation through *his mother's bowl* — the source scene has no mother, no bowl. The sibling **invented the staging**, drawing from the target culture's symbolism palette (`inherited_object`, `family altar / kitchen object`). The structural function (confront the edit, extract qualified confirmation, fire body-knowledge at close) is preserved. The *staging* is regenerated. This is what regeneration means.

## What this sample does NOT cover

- **Multi-scene chapter** at sibling-canon level. The chapter-level audit (theme arc across scenes, voice continuity per POV) would need to run inside each sibling's tree independently.
- **A true Japanese-language rendering** (this sample uses English prose with Japanese-literary cognitive shape). A true Japanese-language profile would use character-bounded sentence-density bins and a different kinship-address grammar.
- **A sibling that violates an invariant.** A follow-up sample should stage an invariant violation (e.g. a culture profile that cannot serve the knowledge-turn) and validate the `escalate` path.
- **Stress-tested anti-stereotype detection.** All three runs were authored carefully; a deliberately-stereotyped run that the framework catches would prove the detector teeth.

## Validator Coverage

Each sibling was run through:

- **Cultural Adapter** (compatibility check + symbol swaps + emotional channel changes + directness resolutions + micro-beat reordering + taboo substitutions)
- **Cultural Dialogue Specialist** (directness, address forms, silence budget, third-party routing, apology shape, taboo substitution, anti-stereotype check)
- **Prose Rhythm Agent** (sentence density, breath placement, calque scan, emotion-naming budget, paragraph shape, monologue mode, environmental weight, tidal rhythm)
- **Language Style Validator** (histogram, calque hits, emotional naming, paragraph shape, tag economy, monologue mode, English-psychological default-drift, anti-stereotype check, voice continuity)
- **Continuity Auditor** (invariant compliance, knowledge asymmetry, symbol state, debt status, residue writes verification, cross-run consistency)

All five passed `status: ok` on both regenerated siblings.

## Implementation Note

This sample is **handcrafted** to validate prompt templates and the cultural layer's architecture. In a real orchestrator-driven run, each agent would emit its YAML/markdown automatically per the prompt contracts. The handcrafted version proves the contracts are **populatable** with non-trivial content and the validators are **anchored** in specific structural checks rather than vibes.

## Next Step Suggestions

1. **Cross-cultural CHAPTER sample (3 scenes per sibling).** Validates chapter-level audits inside each sibling tree — especially symbol rhythm across scenes and POV voice continuity per culture.
2. **Deliberate invariant-violation sample.** A culture profile whose `conflict_style.confrontation_default: refused` would make the source scene's knowledge-turn structurally impossible — must validate the `escalate` path of the Cultural Adapter.
3. **Deliberate stereotype-bait sample.** A draft that imports forbidden iconography (cherry blossoms in narration; rural-Vietnamese scenic establishment) — must be caught by the Language Style Validator's `anti_stereotype_check`.
4. **Orchestrator MVP.** With three working samples (baseline, cross-cultural success, failure-path), there is enough golden-fixture material to begin building the orchestrator that runs these flows automatically.

## Related

- [docs/culture/cultural-narrative-layer.md](../../docs/culture/cultural-narrative-layer.md)
- [docs/language/localization-vs-regeneration.md](../../docs/language/localization-vs-regeneration.md)
- [prompts/culture/](../../prompts/culture/)
- [schema/culture/](../../schema/culture/)
