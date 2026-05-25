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
| F3 | Symmetry of opening and closing image used as substitute for change. | Require an actual graph-level delta. |

## Category G — Lexical Tells

A working blocklist (extended by the Humanization Agent):

- *delve, tapestry, navigate (metaphoric), realm, intricate, mosaic, weave (metaphoric), testament to, in the tapestry of, a symphony of, whisper of, dance of*
- Pseudo-academic openers: *In conclusion, Ultimately, It is worth noting that*

Blocklist hits do not auto-reject; they raise the burden of justification.

## Severity

- **Hard reject:** A1, A3, A4, B1, C3, E1, F1, F2
- **Soft reject (justify or rewrite):** A2, B2, C1, C2, D1, D2, E2, F3
- **Flag for humanization pass:** Category G, C4, C5

## Related

- [[humanization-rules]]
- [[anti-ai-revision-pipeline]]
- [[narrative-laws]] (Law 3, Law 9)
