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

## Calibration

The banned-lexicon list is a starting seed. Per project, the [anti-ai-editor](../agents/anti-ai-editor.prompt.md) maintains an extended list of locally-overused phrases.

## Related

- [global-narrative-rules.md](./global-narrative-rules.md) — R1, R10
- [docs/anti-ai/ai-smells.md](../../docs/anti-ai/ai-smells.md) — full taxonomy
- [docs/anti-ai/humanization-rules.md](../../docs/anti-ai/humanization-rules.md) — repair rules
