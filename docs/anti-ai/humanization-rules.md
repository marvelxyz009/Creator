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

### H14 — Rupture and Private Reality (anti-AI-literary-voice)
Generated prose tends toward uniform literary elevation — every detail serves the theme, every sentence wants to be the best sentence, every character is super-aware of their own discipline. This produces the "AI literary voice" smell: technically defensible per sentence, ngột thở at the paragraph level.

Counter-moves to apply after H1–H13:

- **Rupture** — at least one small loss of control per scene that the character did not intend. A hand that moves before the eye decides. A check of the phone they had decided not to check. Standing up and sitting back down for no reason. The character is briefly NOT the calibrated being they have been performing.

- **Private reality detail** — at least one body-fact or tangential worry per scene that does NOT serve the symbol or the theme. A foot gone numb. Hunger. Needing to pee but staying. A memory of a fight with a colleague yesterday. The wrong shoe. Detergent smell from an ex's clothes. These details have no literary payoff. That is the point. Their job is to anchor the character in a real life with body-needs and non-thematic mental noise.

- **Density cap on elevated sentences** — no more than one "heavy abstract sentence" per paragraph. The neighboring sentences must be concrete: action, sensation, environmental fact, or boring reportage. Without breath between, the reader cannot feel the abstract sentences as elevated — they all flatten into the same register.

- **Strip the meta-meta** — character self-awareness about their own discipline (`a habit he taught himself`, `anh nhận ra mình đang thực hiện việc đó kỹ hơn`) reads as the character knowing they are a character. Cut. Discipline shows through action, not through awareness of discipline.

- **Allow boring sentences** — the reader needs valleys to feel the peaks. After producing a beautiful sentence, the next sentence should be plain. Trust the reader to register the gradient.

Detection signal: re-read the draft and try to predict the next beat after each paragraph. If you predict correctly ≥ 70% of the time, the rhythm is too even — apply H14 ruptures and density cap.

### H15 — Emotional Crest (anti-flatline)
A scene built on full suppression / restraint from beginning to end reads as flat, no matter how technically clean. Without one moment of crested felt sensation that the character then immediately suppresses, the reader has no thermometer for the discipline's stakes.

Required for short_story and scene_study forms (other forms may have different cresting patterns):

- **One moment of crested felt sensation** — somatic, concrete, named (not as emotion but as body-fact). Examples: `Một thứ lạnh chạy dọc sống lưng anh.` / `Tim cô đập một nhịp lệch.` / `Lòng bàn tay anh bỗng nóng lên một độ.` Place this at or near the canonical turn beat. The sensation should NOT be followed by a narrator-explanation of what it means — just the next concrete action.

- **One moment of explicit desire before restraint** — the character WANTED to do the forbidden thing, before they didn't do it. `Một thoáng, có thể nửa giây, anh muốn gạt nó. Nhưng anh không gạt.` Required: the `nhưng` connector (L-VI-16) and a time-qualifier that bounds the desire (`một thoáng`, `chỉ trong một nhịp`, `nửa giây`). Without the bounded desire, the restraint reads as having cost nothing.

- **One heart line** — a single sentence (or two clauses) in close-third POV that contains the work's central asymmetry or wound, in plain Vietnamese, no abstraction, no metaphor. Pattern: a fact about the character + a fact about the addressee/world, joined by `nhưng` or `mà`. Examples: `Trong nhiều năm anh đã đợi đèn cô. Mà cô không biết.` / `Cô đã chờ anh không bằng tên. Mà anh chưa bao giờ tới.` Place this near the end, just before the final environmental beat. The heart line should be the most plain sentence in the scene — the elevated sentences earn it.

Detection signal: ask "where is the moment the discipline costs something visible?" If there is no answer, H15 is missing.

### H16 — Do Not Cut Substance to Fix "Abstraction Too Much"
When a critic says `literary abstraction vẫn hơi nhiều` or `câu trừu tượng dày`, the temptation is to delete every abstract sentence and replace with concrete reportage. **This is the wrong fix.** The substance the abstract sentences carry — the character's interior architecture, the canonical wound, the heart line — usually needs to STAY. What needs to go is the *meta-layer over* the abstraction (`anh nhận ra rằng...`, `cái đó đã trở thành một dạng khác của...`), not the abstraction itself.

Process when responding to "abstraction too much":
1. List every abstract/elevated sentence in the draft.
2. Rank by function — which one IS the heart line? Which ones support it? Which ones repeat or restate?
3. Keep the heart line and one or two strongest supports. Cut the rest. Do NOT cut to zero.
4. For the cut ones, ask: is the substance still needed? If yes, render that substance through concrete action elsewhere. Do not lose the substance.

The cắt-sạch (cut-everything) trap produces hollow prose that reads "clean" but says nothing. The reader was complaining about density, not about presence.

### H17 — Post-Write Vietnamese Sweep
Before finalizing prose for a Vietnamese target language, run these scans:

1. **Em-dash count**: grep `—`. For each occurrence, classify as (a) true parallel that needs em-dash, (b) gloss/parenthetical — cut and restructure, (c) staged hesitation — replace with `...`. Target em-dash count for Vietnamese prose: 0 unless (a) is unavoidable.
2. **Standalone short sentences**: every sentence ≤ 4 Vietnamese words. For each, classify as (a) clock-stamp (`2:17.`) — keep, (b) intentional rupture beat — keep if H14 calls for it, (c) accidental dangling fragment — expand or merge into adjacent sentence.
3. **Willful-contradiction pairs**: search for the pattern `<want-action>. <not-action>.` (e.g. `Anh muốn X. Anh không X.`). Insert `Nhưng` or `Mà` between them (L-VI-16).
4. **Reverse-translation spot-check**: pick three sentences that feel "literary" and back-translate to English. If the English reads as fluent literary prose, the Vietnamese is suspect — rewrite in Vietnamese-native syntax.

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
