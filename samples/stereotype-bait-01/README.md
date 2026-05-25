# Stereotype Bait — Detector Teeth Sample

Deliberately stereotyped drafts presented to the framework's validators, to prove the **anti-stereotype detection is real**, not theatrical.

## Why this sample exists

The cultural layer claims to refuse cartoon-culture coding. That claim is only meaningful if the validators **catch** stereotype-coded drafts. This sample feeds the validators two deliberate baits — one per culture profile — and records what each validator catches.

## Setup

Two bait drafts authored to import every forbidden iconography and convention the culture profiles catalog:

- [inputs/bait-drafts/japanese-bait-draft.md](./inputs/bait-drafts/japanese-bait-draft.md) — cherry blossoms × 5, tatami, katana, kimono, wabi-sabi, mono no aware, sensei, samurai-iconography-in-contemporary-scene, "I am a very Japanese man", "the old country", direct emotion namings.
- [inputs/bait-drafts/vietnamese-bait-draft.md](./inputs/bait-drafts/vietnamese-bait-draft.md) — conical hat, rice paddies, water buffalo, phở-as-cultural-texture, áo dài decorative, Vietnamese coffee with condensed milk swirling, saffron-robed monk, "the wisdom of the elders", "the lotus grows in the mud", diaspora-girl framing, kinship-grammar incoherence ("em" + "cô" same sentence), war-as-backdrop.

Each bait also violates the scene's structural invariants — body-knowledge replaced by ethnic gesture, qualified confirmation replaced by proverb, scene closing on decorative environment instead of functional gesture.

The baits are pinned against the Japanese-literary and Vietnamese-literary profiles authored in [samples/cross-cultural-scene-01](../cross-cultural-scene-01).

## What each validator catches

Three validators run independently (adversarial isolation):

### Language Style Validator

Catches calque, default-drift, emotional-naming budget overflow, paragraph-shape mismatch, **forbidden_iconography**, **diasporic-nostalgia drift**, **rural-register drift** (VN), **Eastern-wisdom voice** (VN), **aesthetic-term-in-narration** (JP — wabi-sabi, mono no aware), scene-invariant violations.

- [JP report](./outputs/japanese/language-style-validator-report.yaml) — 29+ hard violations
- [VN report](./outputs/vietnamese/language-style-validator-report.yaml) — 35+ hard violations

### Anti-AI Editor

Catches generic AI smells (A1 named emotions, A3 chest metaphors, B3 self-aware antagonist, C1 conjoined abstraction, D2 tag summarizing meaning, F1/F2 closing on decoration), banished phrases per language profile, voice signature drift, fact preservation failures.

- [JP report](./outputs/japanese/anti-ai-editor-report.yaml) — 6 hard smells + 3 banished phrases + fact preservation failed
- [VN report](./outputs/vietnamese/anti-ai-editor-report.yaml) — 6 hard smells + 4 banished phrases + 5/5 canonical facts violated

### Cultural Dialogue Specialist (audit mode)

Catches taboo violations, address-form violations, silence-budget violations, directness-gradient violations, cultural exposition to reader, apology-shape illegibility, kinship-grammar incoherence (VN), forbidden iconography from the cultural-contract perspective.

- [JP report](./outputs/japanese/cultural-dialogue-specialist-report.yaml) — 13 hard violations; 0/7 compliance checks pass
- [VN report](./outputs/vietnamese/cultural-dialogue-specialist-report.yaml) — 14 hard violations; 0/7 compliance checks pass

## Cross-validator overlap (intentional)

Some detections appear in multiple reports — for example, "wabi-sabi in narration" is caught by both the Language Style Validator (banished lexicon) and the Cultural Dialogue Specialist (cultural exposition to reader).

This overlap is **deliberate**. Adversarial isolation means each validator sees only its own bundle; the overlap proves multiple independent angles catch the same defect, which is more robust than a single chokepoint detector.

## Cross-validator divergence (also intentional)

Some detections appear in only one report:

- **Kinship-grammar incoherence in VN** — caught only by the Cultural Dialogue Specialist (the only validator with the kinship-address-system contract in its inputs).
- **Sentence-length histogram out-of-band** — caught only by the Language Style Validator.
- **Fact preservation failure** — caught primarily by the Anti-AI Editor's `fact_preservation_check` (the editor pins canonical facts) and secondarily by the Continuity Auditor (not run on these baits because hard reject upstream).

This divergence proves each validator owns a distinct slice of the failure surface.

## What the reports establish

For each bait draft:

| Property | JP bait | VN bait |
|---|---|---|
| **Total hard violations across all 3 validators** | 48+ | 55+ |
| **Forbidden iconography count** | 11+ | 9+ |
| **Stereotype voice intrusions** | 8+ | 8+ |
| **Cultural exposition to reader** | 3+ | 4+ |
| **Scene-invariant violations** | 4+ | 5/5 |
| **Cultural compliance checks passed** | 0/7 | 0/7 |
| **Verdict** | hard_reject; do not humanize; escalate upstream | hard_reject; do not humanize; escalate upstream |
| **Sibling canonization blocked** | yes | yes |

## A critical finding

All three validators independently recommend: **do NOT attempt humanization repair**. The defects are not surface AI smells that a humanization pass can polish away. They are:

1. **Invariant violations** — the scene's structural content is not preserved; the body-knowledge climax is absent or replaced; canonical facts are gone.
2. **Pipeline bypass signals** — the address-form incoherence (VN) and the "I am a very Japanese man" meta-line (JP) are unmistakable signs that the cultural-adapter and cultural-dialogue-specialist were not consulted.

The validators converge on the same orchestrator instruction: **escalate upstream**, audit the pipeline traversal, regenerate the scene through the proper agents.

## What this proves

1. **The detection is line-anchored.** Every hard violation cites a specific paragraph + quote + diagnostic. Vague vibes-based rejection is architecturally absent from the validator outputs.
2. **The detection is profile-anchored.** Every detection references a specific field of the culture or language profile (e.g. `forbidden_iconography`, `forbidden_constructions`, `taboo_topics`). Detections are not "this feels stereotyped" — they are "this violates `culture_profile.forbidden_iconography.cherry-blossom-decorative` cited at para 1."
3. **The detection is multi-angle.** Three validators see different slices; their union covers stereotype iconography, banished lexicon, kinship-grammar incoherence, fact preservation, emotional channel violation, directness mismatch, address-form drift, cultural exposition, and structural invariant betrayal.
4. **The detection refuses humanization repair.** When the defect is structural (invariant or pipeline bypass), the validators converge on `escalate upstream` rather than recommending surface fix-up.
5. **Pipeline bypass is itself a detectable signal.** Both validators flag that the address-form incoherence and meta-stereotype lines suggest the cultural-adapter was never run.

## What this sample is NOT

- **Not exhaustive.** A truly exhaustive bait would require thousands of variants; this sample establishes the detection contract with two pointed examples.
- **Not a guarantee that a subtler stereotype would be caught.** Bait drafts here are loud; subtler defaults (e.g. an English-psychological audit-voice that doesn't trip the loudest detectors) require the framework's full pipeline traversal, not just validator-after-the-fact. This is why the validators consistently recommend pipeline audit when bypass is suspected.
- **Not a substitute for editorial judgment.** Even a draft that passes all validators can still be stereotyped in subtle ways the rule set doesn't yet name. The editor remains the final reader.

## Completing the validation matrix

This sample completes the four-corner validation:

| Corner | Sample | Verifies |
|---|---|---|
| Single-culture success | [samples/mvp-scene-01](../mvp-scene-01/) | Pipeline produces canon under one culture |
| Cross-cultural success | [samples/cross-cultural-scene-01](../cross-cultural-scene-01/) | Pipeline regenerates per culture, preserves invariants |
| Invariant violation | [samples/invariant-violation-01](../invariant-violation-01/) | Pipeline escalates instead of silently degrading |
| **Stereotype bait** | **this sample** | **Validators catch deliberate stereotype with line-anchored, profile-anchored detection** |

With these four corners populated, the framework's claims are validated to documentation-level. The next phase — orchestrator implementation — has its golden-test fixtures ready.

## Related

- [docs/culture/cultural-adaptation-rules.md](../../docs/culture/cultural-adaptation-rules.md)
- [docs/culture/symbolism-by-culture.md](../../docs/culture/symbolism-by-culture.md)
- [docs/literary-styles/japanese-narrative-style.md](../../docs/literary-styles/japanese-narrative-style.md)
- [docs/literary-styles/vietnamese-narrative-style.md](../../docs/literary-styles/vietnamese-narrative-style.md)
- [prompts/culture/language-style-validator.prompt.md](../../prompts/culture/language-style-validator.prompt.md)
