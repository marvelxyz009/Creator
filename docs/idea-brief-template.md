# Idea Brief Template

> Fill out as many fields as you can, then paste this into Claude after `/af-start`. Fields you skip will be turned into multiple-choice questions by the AI. The more you fill in advance, the fewer questions you'll be asked.
>
> **Bạn điền càng nhiều, AI càng hỏi ít. Field nào bạn không có → AI sẽ hỏi.**

Copy the block below, fill it in, paste it as your reply when `/af-start` asks for your idea.

---

```
# IDEA BRIEF

## 0. Framing (REQUIRED — these shape everything else)

- **Target language** (the language the prose will be written in):
  - [ ] Vietnamese
  - [ ] English
  - [ ] Japanese
  - [ ] Korean
  - [ ] Chinese
  - [ ] French
  - [ ] Spanish
  - [ ] Other: ___

- **Genre / form**:
  - [ ] literary-realism
  - [ ] psychological-close-third
  - [ ] speculative-fiction (sci-fi / soft-speculative)
  - [ ] historical-fiction
  - [ ] crime-noir
  - [ ] romance
  - [ ] coming-of-age
  - [ ] fairy-tale / magical-realism
  - [ ] horror
  - [ ] Other: ___

- **Setting — place + time** (cultural/temporal frame, distinct from world rules below):
  > e.g. "contemporary thị xã Vietnam", "1970s Hanoi after the war", "near-future US administrative city", "imagined medieval coast"

  [setting here]

- **Scope / length**:
  - [ ] scene-study (~800 words, one beat)
  - [ ] short-story (~3000–7000 words, single act)
  - [ ] novella (~15k–40k words)
  - [ ] novel-opening (first scene of a longer work)

## 1. Premise (REQUIRED)
> One sentence: who, where, what's at stake. Write it in the target language if you prefer — AI will detect and proceed.
> Câu một dòng: ai, ở đâu, đang gì.

[your premise here]

## 2. Project name (REQUIRED)
> Folder name. Lowercase, hyphens, no spaces. AI can suggest if you don't have one.

[your-project-slug]

## 3. Characters (REQUIRED — at least 2)

### Character A
- Name:
- Role: protagonist | antagonist | foil | mirror | chorus
- What they SAY they want (surface drive):
- What they ACTUALLY want (buried drive — must differ from above):
- Their wound (what damaged them before the scene starts):
- Their contradiction (two opposed forces with stakes — NOT "brave but sometimes scared"):
  - Force A:
  - Force B:

### Character B
- Name:
- Role:
- Surface drive:
- Buried drive:
- Wound:
- Contradiction:
  - Force A:
  - Force B:

## 4. The scene (REQUIRED)
- Location:
- Time (time of day, season, weather):
- What the POV character wants IN THIS SCENE (not in the whole story):
- What resists them (source of conflict):
- What CHANGES by scene's end — pick one:
  - knowledge — POV learns something irreversible
  - relation — bond between two characters shifts category
  - debt — a debt is opened, closed, or transformed
  - symbol-fire — a physical object becomes evidence
  - resolve — a question is answered (rare; use carefully)

## 5. Theme (REQUIRED)
- The question your story refuses to answer cheaply (must end with "?"):

- Cheap answers your work REFUSES (at least 3):
  1.
  2.
  3.

## 6. World (REQUIRED — even if contemporary realism, name 1 constraint)
- One unusual or active rule/constraint of this world:
- Consequence if that rule is broken:
- How it creates pressure on this specific scene:

## 7. Tone / texture (REQUIRED — pure tonal descriptors, independent of language + genre above)
> Pick a tonal texture. This is HOW the prose feels at the sentence level, not WHAT genre or language it's in.
- [ ] spare (Cusk / Ishiguro / late Hemingway)
- [ ] lyrical (long-breath sentences, image-forward)
- [ ] punchy (short, impacting, working-class register)
- [ ] lush (rich texture, multiple sensory channels per line)
- [ ] ironic-detached (cool narrator distance, dry wit)
- [ ] warm-domestic (intimate kitchen-table register)
- [ ] philosophical-expansive (Russian-literary tradition)
- [ ] domestic-technical (clinical terms used like kitchen terms)
- [ ] Other:

## 8. Symbol (REQUIRED)
- One physical object that will carry weight in the scene:
- What state it starts in:
- What you want it to do — pick one:
  - introduce only (sets up arc for later scenes)
  - introduce + transform (changes state within this scene)
  - introduce + fire (body-knowledge moment at scene close)
  - betray (object reveals something about whoever holds it)

## 9. Ending hook (REQUIRED — how the last beat lands)
- [ ] gesture — a single physical action; no words
- [ ] object — something placed exactly where it was
- [ ] silence — a beat held one too long
- [ ] environmental shift — weather, light, the room's temperature changes
- [ ] dialogue fragment — an unfinished syllable

## 10. Asymmetric knowledge (OPTIONAL but powerful)
> Who knows what that others do not?
- Character A knows but Character B does not:
- Character B knows but Character A does not:
- Reader knows but neither character does:

## 11. References / influences (OPTIONAL)
- Works that inspired this (books, films, essays):
- What you admire about them STRUCTURALLY (not surface-imitate):

## 12. Anything else (OPTIONAL)
> Constraints, voice samples, things you want preserved, things you absolutely refuse.
```

---

## How AI uses this

When you paste a filled brief into `/af-start`:

1. AI reads each section.
2. For each **REQUIRED** field that's empty, ambiguous, or missing — AI asks ONE multiple-choice question to fill it.
3. AI keeps asking until every REQUIRED field has a usable value. **No artificial cap on number of questions.**
4. AI does NOT ask about OPTIONAL fields unless answering them clarifies something already required.
5. Once everything is complete, AI generates the 7 YAML input files and runs the full 5-agent pipeline.

If you fill everything REQUIRED, AI may ask **zero questions** and go straight to generation.

## Example — minimum viable filled brief

A premise paragraph + names + 1 contradiction + 1 turn type is sometimes enough. AI will fill in plausible defaults for the rest (from your tone selection + premise context) and ask only when ambiguous.

## Tips for filling

- **Contradictions** must be two opposed forces with stakes. "Brave but cautious" fails. "Wants intimacy / fears being known" passes.
- **Drives** (surface vs. buried) MUST differ. If they match, you haven't gone deep enough.
- **Refusals** are the cheap answers you'd hate. The work won't reach for them.
- **Symbols** must hold a state machine. Pick one that can be picked up, broken, given, returned, refused.
- **Endings** never on a rhetorical question. Always on a thing, a gesture, or a silence.

## What this template is NOT

- Not a final document — it's just a way to compress your idea into one paste.
- Not exhaustive — the framework has more concepts (memory graph, theme beats, narrative laws). AI fills those in.
- Not enforced — you can paste a 1-line premise too. AI will just ask more questions.
