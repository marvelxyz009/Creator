# Humanization Rules

The active perturbation rules applied by the Humanization Agent after a draft has passed continuity and theme review. The goal: push prose away from the statistical median while preserving every canonical fact.

## Operating Principle

> A well-formed sentence that any competent model would produce is, by default, a sentence to question.

The Humanization Agent does **not** improve prose by adding flourish. It improves prose by **subtracting predictability** and **re-grounding** in the specific.

## The Rules

### H1 — Specificity Substitution
Replace any abstract noun with the **most material, most specific** alternative consistent with POV.

- "fear" → *the cold in her fingers; the wrong rhythm of her breath* (whichever the character would notice)
- "love" → never used in narration unless the POV is naming their own self-deception.

### H2 — Show The Refusal, Not The Feeling
When the POV is suppressing a feeling, render the **suppression mechanism** (object handled, sentence cut short, attention redirected) instead of the feeling itself.

### H3 — Cut The Last Beat
Most generated paragraphs over-explain in their final sentence. The default operation is **delete the last sentence and check** whether the paragraph is stronger.

### H4 — Voice Re-Pinning
Every paragraph is checked against the POV's `voice_signature`. Lines that any character could plausibly say are rewritten until they belong to **this** character or are deleted.

### H5 — Sentence-Length Perturbation
If sentence lengths fall within the median band (12–18 words) for more than three consecutive sentences, break the rhythm. Insert a short. Or an unusually long one that earns its length through specificity rather than subordination.

### H6 — Object Anchoring
Every emotional beat must touch a **physical object or environmental fact** present in the scene. No floating affect.

### H7 — Asymmetric Punctuation
Generative prose over-uses commas as breath. Humanization redistributes: more periods under stress, more semicolons in calculated speech, dashes for interruption, never em-dash as decoration.

### H8 — Banished Phrases
The Humanization Agent maintains an active blocklist seeded from Category G of [[ai-smells]] and grown per-project. Banished phrases are not "discouraged"; they are **deleted on sight** and the line is rebuilt.

### H9 — Subtract Before Adding
For each pass, the agent must produce a **net token-count reduction** unless the draft is being explicitly enriched at the editor's request. Default is compression.

### H10 — Preserve Canonical Facts
Humanization may rewrite *how* something is rendered. It may never change *what* happened. The agent re-validates against the [[memory-graph]] before returning.

### H11 — Insert Past-Anchors When Residue Is Thin
When the present scene is built on a charged past shared between participants and the reader has no anchored sense of what that past was, the present cannot carry weight. Insert 1–3 short interior past-facts (concrete time, place, person, object) in close-third POV — drawn from `memory_graph_excerpt`, `character.knowledge_set`, or `character.wound`.

These are POV-interior facts the character carries in mind right now — NOT staged flashback scenes. One sentence each. Permitted by [[narrative-laws]] R1: interior past-facts in close-third POV are not "staged flashback".

Detection signal: the scene has body-tells, symbol-fires, and asymmetric knowledge, but a careful reader cannot answer "what was between these two before". Without that anchor, the emotional residue floats.

### H12 — Language-Aware Politeness Pass (Dialogue)
For target languages with grammaticalized politeness (Vietnamese xưng hô, Japanese keigo, Korean honorifics, etc.), the English-language defaults — clipped fragments as restraint, bare grunts as cool — do not translate. Apply per-language overrides:

- **Vietnamese**: every dialogue line in a polite/intimate register must include at least one of (a) address particle, (b) sentence-final softener (`nhỉ`, `thôi`, `đó`, `mà`, `nhé`, `chứ`, `vậy`), (c) an extension/echo of the addressee's prior line. Bare `Ừ` standing alone reads as cold dismissal, not as discipline. Discipline in Vietnamese is rendered by full polite sentences whose content withholds, not by clipped syntax.
- **Subconscious leaks** in non-English languages should be culturally appropriate register shifts (Vietnamese: xưng hô shift from name to relational pronoun), not Anglo-style tacked-on fillers.

See [[anti-ai-constraints#language-register-rules]] for the full per-language reference.

### H13 — Render Discipline As Effort, Not Absence
A disciplined / repressing character whose suppression is rendered as *absence* (no thoughts, no body-tells, brief curt answers) reads to the reader as a passerby, not as a controlled protagonist or mirror. Render the suppression mechanism as a small visible act: catching oneself mid-thought, body-displacement to a neutral object, a sentence that breaks off, an over-fixation on a near object, an answer too quickly chosen.

The reader needs to feel the *shape of what is being held*, not the *fact that nothing is there*.

## Calibration Loop

The agent maintains, per project:
- A growing **banished phrase list** (seeded from G, extended by detector hits).
- A **voice-signature drift report** per POV.
- A **median-sentence histogram** flagged when prose collapses to it.

These calibrations live in the project's anti-AI state file (specified later in implementation).

## What Humanization is NOT

- Not stylization for its own sake.
- Not adding "literary" decoration.
- Not introducing ambiguity where the scene contract requires clarity.
- Not a substitute for the upstream stages — humanization on a thematically dead scene yields well-written nothing.

## Related

- [[ai-smells]]
- [[anti-ai-revision-pipeline]]
- [[narrative-laws]] (Law 3, Law 7, Law 9)
