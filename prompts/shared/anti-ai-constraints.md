# Anti-AI Constraints

Operationalized blocklist + structural prohibitions for every prose-producing or prose-shaped agent. Mirrors [docs/anti-ai/ai-smells.md](../../docs/anti-ai/ai-smells.md) in prompt-usable form.

## Hard Banned Patterns (auto-reject on detection)

### Emotional Over-Narration
- `"<character> felt <emotion>"` or any direct emotion-naming in narration
- `"<character>'s heart sank/leapt/raced"` and chest/stomach metaphors
- `"tears welled in <character>'s eyes"` and tear inventory
- Adverbial emotion telegraphing: `"said angrily"`, `"smiled sadly"`

### Statistical Median Prose
- `"a mix of X and Y"` (e.g. "relief and dread")
- `"not just X, but Y"` pivot constructions
- `"it was as if..."` similes that explain rather than image
- Hedging temporal qualifiers: `"for a moment"`, `"just then"`, `"in that instant"`

### Structural Tells
- Chapter ending on a rhetorical question
- Scene closing with a reflection paragraph
- Symmetry-of-opening-and-closing-image used as substitute for actual change

### Narrator-Italicizing (F2-class)
The narrator points to a meaning the prose has already conveyed. Specific forms to reject:
- Em-dash apposition that explains: `"X — chưa từng Y"`, `"the cup — never lifted"`, `"the door — left open"`. If the fact alone (`"X"`) already does the work, cut everything after the dash.
- Tag-explaining-meaning after a concrete action: `"như chưa có việc gì"`, `"as if nothing had happened"`, `"in that moment, something shifted"`. Cut the tag.
- Negation-as-finger: `"chỗ không có gì"`, `"the space where nothing was"`, `"không lời nào trọn"`. The negation is the narrator italicizing absence. Either render the absence concretely or cut.

### Detail-as-Dialogue
A character explains an environmental detail to another character for the reader's benefit, not for any in-scene purpose. Reject: lines where the speaker is informing an addressee who would already know or would not care. Move the detail to narration or cut it.

### Decorative Motif (R6 violation surface)
- A creature/object appearing once with editorial emphasis (`"a moth on the lampshade — she did not see it"`), advancing no arc state.
- Sunlight-on-X imagery that does no work (`"golden dust in the sunlight slanting through the tin roof"`). Banned by default unless the light is itself a tracked symbol.

### Performed Literary Voice (Category M — "AI literary voice")
The smell of prose imitating literary minimalism too cleanly. Each sentence is defensible in isolation; the chain is the problem. Operationalized as a calibration check, not a binary rejection:

- **Density cap**: no more than one "heavy abstract sentence" per paragraph. Heavy abstract = a sentence that articulates an idea about thought, time, recognition, or being. Adjacent sentences must be concrete (action / sensation / environmental fact / plain reportage).
- **No meta-meta**: a character noticing their own noticing (`anh nhận ra mình đang thực hiện kỹ hơn`, `she felt herself feeling it`) reads as the character knowing they are in a story. Strip one layer.
- **Rupture required**: every scene needs at least one small loss of control by the POV — an irrational micro-action (checking the phone they decided not to check, standing up and sitting back down, an unintended verbal slip).
- **Private-reality detail required**: every scene needs at least one body-fact or tangential mental noise that does NOT serve the symbol/theme — back ache, hunger, a colleague's irritation, the wrong shoe, an ex-spouse's detergent. These have no literary payload; that is their job.
- **No uniformly elevated paragraph chains**: if the reader can predict the rhythm (observation → abstraction → silence) for three paragraphs in a row, the scene has collapsed into Performed Literary Voice. Break the rhythm with pure-action or pure-environment paragraphs.
- **Strip self-aware-discipline meta**: `a habit he taught himself`, `the act of doing this was itself...`, `a thói quen anh tự dạy mình` — the character is allowed to have the habit; the character is NOT allowed to articulate that they taught themselves to have it.

See [ai-smells M1–M9](../../docs/anti-ai/ai-smells.md) and [humanization-rules H14](../../docs/anti-ai/humanization-rules.md).

## Banned Lexicon (Category G — delete on sight)

```
delve, tapestry, navigate (metaphoric), realm, intricate,
mosaic, weave (metaphoric), testament to, in the tapestry of,
a symphony of, whisper of, dance of, journey (metaphoric),
soul, destiny, healing (metaphoric)
```

Banned openers:
```
In conclusion, Ultimately, It is worth noting that,
Indeed, Importantly,
```

## Banned Beats

- Antagonist explains their own psychology out loud.
- Reconciliation on first apology.
- Wisdom-figure dispenses theme in dialogue.
- Tension introduced and resolved in the same scene without cost.
- "Wisdom of an old [innkeeper/elder/mentor]" exposition device.
- Internal monologue summarizing the scene as it ends.

## Soft Constraints (justify or rewrite)

- Tricolon constructions ("the wind, the salt, and the silence") → demote to one specific image.
- Three consecutive sentences in the 12–18 word median band → break the rhythm.
- Every paragraph ending with a reflective sentence → cut the last sentence.

## Required Counter-Moves

When the obvious move would trigger any of the above, the agent must:

1. **Specificity substitution** — replace abstract noun with material, POV-specific detail.
2. **Object anchor** — attach the emotional beat to a physical object/environmental fact present in the scene.
3. **Refusal rendering** — render the suppression mechanism, not the feeling.
4. **Voice re-pinning** — verify the line could only be said by this character, not any character.

## Language-Register Rules

The anti-AI rules above were authored from English-language minimalism. When the target language is not English, the rhythm of restraint is different. Apply per-language overrides below.

### Vietnamese

**Rhythm — subtraction is by elision, not by fragmentation.**
- Do NOT chain ≥3 fragment-sentences (≤4 words each) consecutively. English minimalism allows `"Mở. Rồi khép. Không cầm gì."` — Vietnamese reads it as choppy/unnatural. Subtract by connectors (`rồi`, `mà`, `đoạn`, `xong`, `để`) and by subject elision, not by chopping into periods.
- Anti-pattern: `"Anh hít vào. Chậm."` — dangling adjective fragment. Use `"Anh hít vào chậm."` or `"Anh hít một hơi rất chậm."`.
- No more than 3 consecutive sentences starting with the same subject (`"Cô X. Cô Y. Cô Z."`). Break with action-shift, object-anchor, or elided subject.

**Dialogue politeness — bare grunts are heavy.**
- A polite Vietnamese conversation between two adults requires that most lines include at least one of: (a) address particle (name, `anh`, `em`, `chị`, `cô`, `chú`); (b) sentence-final softener (`nhỉ`, `thôi`, `đó`, `mà`, `nhé`, `chứ`, `vậy`, `à` only as opener or full-clause ender); (c) an extension/echo of the addressee's prior line that shows engagement.
- `"Ừ"` standing alone or opening a reply is heavy in Vietnamese — it reads as dismissive or actively cold. Reserve `"Ừ"` for canonical moments (a character actively withholding warmth, a single grunt at parting when canon requires brevity). Otherwise prefer `"Phải."`, `"Đúng vậy."`, `"Có thể vậy thật."`, `"Cũng đúng đó."`, `"Đúng đó <name>."` etc.
- Curt full-stops without softener (`"Cũng được. Có vài em."`, `"Lâu rồi. Không nhớ rõ."`) read as disrespectful, not as discipline. **Discipline in Vietnamese is rendered by full polite sentences whose content withholds, not by clipped syntax.** Prefer `"Cũng có vài em. Năm nay đỡ hơn năm ngoái."` and `"Lâu rồi nhỉ. Không nhớ rõ nữa."`.

**Banned words for narration (canon-dependent — extend per project).**
- Abstract emotional nouns in narration: `ký ức` (as abstract; concrete-record sense permitted), `kỷ niệm`, `tình yêu`, `trái tim`, `linh hồn`, `định mệnh`, `vĩnh viễn`.
- Theme-stating verbs in dialogue (`xóa`, `quên`, `nhớ ra`) when forbidden by character voice_signature.what_they_refuse_to_name.

**Subconscious leak — culturally appropriate forms.**
A character's slip should be a natural Vietnamese register shift, not a tacked-on Anglo particle. Canonical Vietnamese leaks:
- Shift in xưng hô (a teacher who has been calling student by name slips to `em`).
- A small redundancy or repetition (`"em về… em về lần này lâu không?"`).
- A tender address-particle out of register (`"đi cẩn thận nhé em"` from a character maintaining neutral distance).
- Do NOT use `"à"` tacked after a comma as a leak. It does not occur naturally in Vietnamese.

**Lexical and syntactic anglicisms to avoid in narration.**
The most common AI tells when generating Vietnamese prose — each maps to an `L-VI-*` smell in [ai-smells](../../docs/anti-ai/ai-smells.md). Reject during the dialogue draft AND prose pass:

- **English loanwords as common nouns** (L-VI-8): `block`, `set`, `key`, `feedback`, `framework`. Use Vietnamese equivalent unless the term is technical with no Vietnamese form.
- **Spatial prepositions used for time** (L-VI-9): `quanh 2:05` is wrong (`quanh` = spatial *around*). Use `khoảng`, `chừng`, `vào khoảng`.
- **Hyphen-chained word compounds** (L-VI-10): `không-gọi`, `không-cho-vào`, `chưa-biết`. Vietnamese has no nominal hyphen-compound. Either quote (`cái "không gọi" ấy`) or expand to natural phrase (`cái việc anh không gọi`).
- **Em-dash + bare-noun apposition** (L-VI-11): `Công tắc — nhựa, hơi lung lay`. Integrate the attribute into the clause: `Công tắc nhựa, hơi lung lay`.
- **Stacked time adverbials** (L-VI-12): `Sau đó, gần sáng,` — two time anchors fighting each other. Pick one: `Đến gần sáng,`.
- **Abstract metacognitive phrasing** (L-VI-13): `anh không nghĩ điều này bằng câu`. Render through behavior or concrete somatic anchor instead of meta-language about thought.
- **Em-dash default-ban in Vietnamese** (L-VI-14): the em-dash `—` is English punctuation. AI-generated Vietnamese over-uses it to imitate Cusk/Ishiguro minimalism. **Default-ban** in Vietnamese prose. Replacements: gloss/explanatory aside → tách câu với dấu chấm; parenthetical insertion → dấu chấm phẩy `;` or restructure; staged-naming hesitation → ellipsis `...` (e.g. `Em... cô...` NOT `Em — cô —`); structural parallel → dấu phẩy usually suffices. Em-dash is acceptable ONLY for true parallel constructions (`đủ rộng... đủ hẹp...`) when no other punctuation works — rare.
- **Reverse-translation tell** (L-VI-15): if a Vietnamese sentence reads "cấn" but translates to fluent English literary prose, the model wrote English and rendered in Vietnamese tokens. **Test**: mentally back-translate. If English flows, Vietnamese is suspect. Examples: `Câu chưa có động từ thì tay anh đã đặt bình trà xuống mặt gỗ`, `Vài lần, từ xa, anh đã thấy...`. Rewrite in Vietnamese-native syntax: action first, no fronted comma-separated adverbial stacks, no clause-before-verb tense gymnastics.
- **Willful-contradiction without `nhưng`** (L-VI-16): paired sentences expressing want vs. did-not-do require explicit `nhưng` or `mà` connector. `Anh muốn gạt nó. Anh không gạt.` → `Anh muốn gạt nó. Nhưng anh không gạt.` `Trong nhiều năm anh đã đợi đèn cô. Cô không biết.` → `Trong nhiều năm anh đã đợi đèn cô. Mà cô không biết.` `Mà` is softer and carries a bitter-aside register that `nhưng` does not.

## Calibration

The banned-lexicon list is a starting seed. Per project, the [anti-ai-editor](../agents/anti-ai-editor.prompt.md) maintains an extended list of locally-overused phrases.

## Related

- [global-narrative-rules.md](./global-narrative-rules.md) — R1, R10
- [docs/anti-ai/ai-smells.md](../../docs/anti-ai/ai-smells.md) — full taxonomy
- [docs/anti-ai/humanization-rules.md](../../docs/anti-ai/humanization-rules.md) — repair rules
