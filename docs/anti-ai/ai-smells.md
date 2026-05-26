# AI Smells

A taxonomy of the recurring failure patterns of generative prose. The Smell Detector ([[agent-system]]) uses this catalog; the Humanization Agent ([[humanization-rules]]) is tuned against it.

## Category A — Emotional Over-Narration

| # | Pattern | Example | Fix Direction |
|---|---|---|---|
| A1 | Naming the feeling | "She felt a wave of sadness." | Render through body, object, or rhythm. |
| A2 | Adverbial telegraphing | "He said angrily." | Cut adverb; let the line carry it. |
| A3 | Heart/chest/stomach metaphors | "Her heart sank." | Forbid by default; require novel embodiment. |
| A4 | Tear inventory | "Tears welled in her eyes." | Replace with displacement or refusal. |

## Category B — Premature Resolution

| # | Pattern | Fix Direction |
|---|---|---|
| B1 | Tension introduced and resolved within the same scene without cost. | Add cost or carry forward. |
| B2 | Apology accepted on first offer. | Refuse once; complicate. |
| B3 | Antagonist understands themselves out loud. | Strip self-awareness; restore opacity. |

## Category C — Statistical Median Prose

| # | Pattern | Fix Direction |
|---|---|---|
| C1 | "A mix of X and Y" constructions ("relief and dread"). | Pick one and specify, or render via concrete behavior. |
| C2 | Tricolon abuse ("the wind, the salt, and the silence"). | Demote to one specific image. |
| C3 | "Not just X, but Y" pivots. | Forbidden by default. |
| C4 | Hedging temporal qualifiers ("for a moment", "just then"). | Cut. |
| C5 | "It was as if..." similes that explain rather than image. | Replace with the image itself. |

## Category D — Voice Collapse

| # | Pattern | Fix Direction |
|---|---|---|
| D1 | All POVs notice the same things. | Cross-check against `voice_signature.what_they_notice`. |
| D2 | Dialogue tagging that summarizes meaning ("he said, trying to be brave"). | Cut the tag's meaning; let voice do work. |
| D3 | Two characters using the same lexical register. | Diverge registers per character schema. |

## Category E — Worldbuilding Tells

| # | Pattern | Fix Direction |
|---|---|---|
| E1 | Exposition delivered by a character explaining what both characters already know. | Cut; relocate to scene-action. |
| E2 | Sensory palettes that drift toward genre-default. | Re-pin against `world.texture.sensory_palette`. |
| E3 | Magic/system jargon used decoratively. | Forbid unless functionally load-bearing. |

## Category F — Structural Tells

| # | Pattern | Fix Direction |
|---|---|---|
| F1 | Chapter ending on a question. | Forbidden by default; require a gesture or object instead. |
| F2 | Scene closing with a reflection paragraph. | Cut last paragraph; end on the action that caused it. |
| F2a | Narrator italicizing: em-dash apposition that explains (`"X — chưa từng Y"`), tag-explaining-meaning after concrete action (`"như chưa có việc gì"`), negation-as-finger (`"chỗ không có gì"`). | Cut the explaining clause; let the fact stand alone. |
| F3 | Symmetry of opening and closing image used as substitute for change. | Require an actual graph-level delta. |
| F4 | Decorative motif — object/creature/light appearing once with editorial emphasis, advancing no arc state. | Cut, or promote to a tracked symbol via [[symbolism-tracker]]. |
| F5 | Detail-as-dialogue — a character explains an environmental detail to an addressee who would know or not care, solely to inform the reader. | Move detail to narration or cut. |

## Category H — Discipline-As-Absence

| # | Pattern | Fix Direction |
|---|---|---|
| H1 | A "controlled / disciplined" character rendered through omission — no body-tells, no caught-thoughts, no over-fixation on an object — reads as a passerby, not as restraint. | Render suppression as a small visible act (see [[humanization-rules]] H13). |
| H2 | Curt monosyllabic answers (`"Ừ."`, `"Còn."`, `"Lâu rồi."`) used as a stand-in for discipline in languages with grammaticalized politeness. | Replace with full polite sentences whose content withholds. See Category L for language-specific rules. |

## Category L — Language-Specific Smells (non-English target)

The Smell Detector applies the English-language categories above plus per-language overrides. The framework's default rhythm-of-restraint is English-minimalist; other languages require their own rules.

### Vietnamese

| # | Pattern | Fix Direction |
|---|---|---|
| L-VI-1 | Choppy fragment chains — three or more period-separated fragments of ≤4 words consecutively (`"Mở. Rồi khép. Không cầm gì."`). English minimalism translated to Vietnamese reads as unnatural staccato. | Subtract via subject-elision and connectors (`rồi`, `mà`, `đoạn`, `xong`, `để`), not via period-chopping. |
| L-VI-2 | Dangling adjective/adverb fragments (`"Anh hít vào. Chậm."`). | Join into one breath: `"Anh hít vào chậm."` or `"Anh hít một hơi rất chậm."`. |
| L-VI-3 | ≥3 consecutive sentences starting with the same subject (`"Cô X. Cô Y. Cô Z."`). | Break with action-shift, object-anchor, or elided subject. |
| L-VI-4 | Bare `"Ừ"` standing alone or opening a polite reply. Heavy in Vietnamese — reads as actively cold. | Reserve for canonical cold moments only. Prefer `"Phải."`, `"Đúng vậy."`, `"Có thể vậy thật."`, `"Cũng đúng đó."`. |
| L-VI-5 | Dialogue lines without address particle (name, `anh`, `em`, `chị`, `cô`) or sentence-final softener (`nhỉ`, `thôi`, `đó`, `mà`, `nhé`, `chứ`, `vậy`). Reads as disrespectful, not as discipline. | Add at least one of: address particle, softener, or extension that echoes the addressee. |
| L-VI-6 | Anglo-style tacked-on filler particle as subconscious leak (`"...lâu không, à?"`). Does not occur naturally in Vietnamese. | Replace with a culturally appropriate leak: a xưng hô shift (disciplined-name → relational pronoun), a small repetition (`"em về… em về lần này lâu không?"`), a tender particle out of register (`"đi cẩn thận nhé em"`). |
| L-VI-7 | Theme abstract nouns leaked into narration (`ký ức` as abstract, `kỷ niệm`, `tình yêu`, `trái tim`, `linh hồn`, `định mệnh`, `vĩnh viễn`). | Replace with concrete sense (a record, a file, a year, a place, a hair-tie) or remove. Per-project blacklist extends this list. |
| L-VI-8 | English loanword used as common noun in Vietnamese prose where a Vietnamese equivalent exists (`block`, `set`, `key`, `framework`, `feedback`). Reads as anglicism, breaks register. | Replace with Vietnamese equivalent: `block` → `khu nhà` / `chung cư` / `tòa nhà`; `feedback` → `phản hồi`; etc. Exception: technical terms with no native equivalent in current Vietnamese register. |
| L-VI-9 | Spatial preposition used for time approximation (`quanh 2:05`, `quanh giờ ấy`). `Quanh` means *around* in the spatial sense only (or in compound `loanh quanh` = wandering). | Use `khoảng` for approximate time (`khoảng 2:05`), `chừng` (`chừng nửa đêm`), or `vào khoảng` for a window. |
| L-VI-10 | Hyphen-chained word compounds used as conceptual labels (`không-gọi`, `không-cho-vào`, `body-knowledge`, `chưa-biết`). Vietnamese does not form nominal compounds with hyphens. | Either use quotes for conceptual labeling (`cái "không gọi" ấy`), or expand into a natural phrase (`cái việc anh không gọi`, `cái mà anh không cho vào`). |
| L-VI-11 | Em-dash + bare-noun apposition as minimalist description (`X — nhựa, hơi lung lay`, `Công tắc — đỏ`). English-translation tell; Vietnamese describes attributes inside the clause, not as appositive fragments. | Either: integrate into the clause (`Công tắc nhựa đỏ trong tầm tay`); or use a full descriptive clause after the dash (`X — vật bằng nhựa, hơi lung lay`); never bare noun alone. |
| L-VI-12 | Stacked time adverbials placed back-to-back (`Sau đó, gần sáng,`; `Lúc nãy, ban chiều,`; `Hồi trước, năm ngoái,`). Reads as two competing time anchors fighting each other. | Pick one and integrate the other: `Đến gần sáng,...`; `Sau đó một lúc, gần sáng,...`; `Ban chiều lúc nãy,...`. |
| L-VI-13 | Abstract metacognitive phrasing about modes of thought (`anh không nghĩ điều này bằng câu`, `cô cảm điều ấy không bằng lời`, `ý nghĩ chưa thành chữ`). Tries to render non-verbal cognition explicitly — opaque in Vietnamese, exposes the seam between what the narrator can say and what the character "feels". | Render through behavior: show the character doing the thing the unverbalized thought is about (a hand staying on the switch, eyes returning to the same window). If absolutely necessary in interior prose, use concrete somatic anchor (`anh chỉ thấy lòng bàn tay nóng lên`) instead of meta-language about thought. |

## Category G — Lexical Tells

A working blocklist (extended by the Humanization Agent):

- *delve, tapestry, navigate (metaphoric), realm, intricate, mosaic, weave (metaphoric), testament to, in the tapestry of, a symphony of, whisper of, dance of*
- Pseudo-academic openers: *In conclusion, Ultimately, It is worth noting that*

Blocklist hits do not auto-reject; they raise the burden of justification.

## Category M — Performed Literary Voice ("AI literary voice")

The smell of prose that imitates literary minimalism too cleanly. Each sentence might be defensible in isolation; the chain is the problem. Generated prose often hits these because the model is performing "literary depth" rather than rendering a specific character's specific life.

| # | Pattern | Fix Direction |
|---|---|---|
| M1 | Predictable rhythm: observation → abstraction → silence triplet repeated more than twice in a row. The reader can predict the next beat. | Break the pattern. Insert a paragraph that is pure action with no reflection, OR a private-reality detail with no thematic payload. |
| M2 | Character self-aware about their own discipline (`a habit he taught himself`, `the act of doing this was itself...`, `anh thực hiện kỹ hơn thường ngày, đủ kỹ để nhận ra mình đang thực hiện nó`). The character knows they are being a character. | Strip the meta-layer. If discipline must show, show through action (the hand stayed; the second look did not come), not through the character's awareness of their own discipline. |
| M3 | Every detail serves the metaphor. There is no "garbage" — no neutral observation, no body-fact unrelated to theme. | Insert 1–2 details per scene that **do not serve the symbol or the theme**. A stomach gurgle. The wrong shoe. The phone buzzing in the other room. A thought about tomorrow's dentist. |
| M4 | No rupture — the character never loses small control. Every micro-action is measured, deliberate, calibrated. | Add at least one rupture per scene: a small loss of control the character did not intend (a hand that moves before the eye decides; a sentence half-spoken; a small irrational action — checking a phone they had decided not to check, getting up and sitting back down without doing anything). |
| M5 | Cinematic framing of mundane detail without character-specific perception. "The rectangle of light on the floor." "The cooling tea." Could be in any literary story. | Replace with **character-specific weird perception**: what does THIS specific person notice that another literary character would not? An ex-spouse's brand of detergent. A specific wrong-tuned radio frequency. The way one ear hears less. |
| M6 | Meta-meta — character notices their own noticing (`anh nhận ra mình đang nghĩ về điều ấy`, `cái sự để ý ấy cũng là một dạng để ý khác`). | Cut one layer. Either character notices, or narrator notices character's noticing — never both. Default: cut the meta-meta entirely. |
| M7 | Heavy abstract sentence followed by another heavy abstract sentence with no concrete breath between. Reader has no place to land. | Cap density: no more than **one heavy abstract sentence per paragraph**. The next sentence must be concrete action, sensation, or environmental fact. |
| M8 | Lack of "private reality" — the character is rendered only through their literary-relevant perceptions. They never have a body-need, a financial worry, a small bored thought, a memory that has nothing to do with the scene's question. | Add at least one private-reality beat per scene: a body fact (a back ache, hunger, needing to pee), a non-thematic worry (rent, a colleague's irritation), or a tangential memory (something that happened yesterday at work). |
| M9 | "Every sentence wants to be the best sentence" — the prose is uniformly elevated. There are no boring sentences to give the good ones contrast. | The reader needs valleys to feel the peaks. Cut 30–40% of the elevated sentences. Replace with plain reportage. The remaining elevated sentences will hit harder. |

## Severity

- **Hard reject:** A1, A3, A4, B1, C3, E1, F1, F2, F2a, F5
- **Soft reject (justify or rewrite):** A2, B2, C1, C2, D1, D2, E2, F3, F4, H1, H2, M2, M4, M6
- **Flag for humanization pass:** Category G, C4, C5, all of Category L (per active target language), all of Category M (calibration — count incidences, do not auto-reject)

## Related

- [[humanization-rules]]
- [[anti-ai-revision-pipeline]]
- [[narrative-laws]] (Law 3, Law 9)
