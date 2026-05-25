# 05 — Revised Draft (v1, post-humanization)

> **Agent:** anti-ai-editor · **scene_id:** scene:01 · **pov:** char:mira
> **Status:** ok — hard smells = 0; net token reduction achieved; canonical facts preserved.
> Word count: ~720 (down from ~860 in v1; net reduction ≈ 140 tokens / 16%).

---

The clinic's door had not been re-locked since the closure. Mira pushed it. Salt-damp came up off the floor.

Tomas was at the consultation desk by the window. He had a small brass lighter in his hand and he was turning it, once, the way he turned things when he was waiting.

She did not sit.

"You knew I'd come tonight," she said.

"I hoped you would."

"That isn't the same thing."

He set the lighter on the edge of the desk.

Mira crossed to the desk and moved the stapler an inch to the left, into its old alignment. The fluorescent above them ticked.

"Five days ago," she said, "I asked you a direct question. About my record. You answered with a sentence I have been turning over since."

"I remember the sentence."

"Then you also remember it wasn't an answer."

His mouth moved into something he did not finish. "Mira. There were things, in that period of your life, that—"

"Don't."

"—that I judged it kinder to set aside."

"*Set aside.*"

"It is the word I used at the time."

"It is the word a licensed editor uses on a form."

"I was a licensed editor."

"You weren't licensed for me."

Outside, the wave came in on the stones. He picked up the lighter again. She watched his hand and did not let her face know she was watching.

"I set aside a portion of what we shared," he said. "Partly. Within reason."

"Within whose reason?"

"Mine. At the time."

There was a piece of cracked glass set into the surface of the desk, an old workplace ornament, and two of the shards had drifted out of alignment. She fitted them back together with the side of her thumb, mid-sentence.

"What do you think I am supposed to do with that," she said. "Now that you've told me."

"I'm not sure you needed to know even that much."

"I wake at four. I have been waking at four for three years. There is no file attached."

"I know."

"You have more than an idea."

He reached, without looking, and straightened the stapler she had moved.

She nearly laughed. The laugh did not come. "You can't help it," she said. "You see something off and you fix it."

"It's a habit."

"It's a tell."

"Mira—"

"Did you ask me first." She could not lift it into a question by then. "Before you set anything aside. Did you ask."

"I asked you something. I'm not sure what I asked counts."

"That's the most honest sentence you have said since I walked in."

"I know."

The hum of the dead refrigeration unit. The wave. The fluorescent tick.

She reached across the desk and picked up the lighter.

It was warm. She turned it once, the way he had — and stopped. Her thumb had gone to the wheel from the side, not the top. Her index had braced the base where it was worn. She struck it once. The flame came up clean on the first try.

She looked at the flame.

"I have never seen this lighter before," she said.

"No."

"My record does not contain a single instance of me seeing this lighter."

"No."

"Then explain to me how my hand knows where the worn part is."

He did not answer. She would not have let him.

She set the lighter back on the desk, exactly where it had been, the angle exactly as he had left it. She crossed to the door. Behind her, very quietly, he said something that might have been her name and might have been a fragment of a longer word he had decided, too late, not to say.

She walked out into the salt and the wave.

---

## Humanization Pass Log

```yaml
applied_rules: [H1, H2, H3, H4, H6, H7, H8, H9, H10]

delta:
  tokens_before: ~860
  tokens_after: ~720
  net_reduction: ~140

cuts:
  - removed: "a mix of cold and stillness she had not prepared for"
    replaced_by: "Salt-damp came up off the floor."          # H1 + H8
  - removed: "Mira felt a wave of unease move through her chest"
    replaced_by: "<cut entirely; the following object-action carries it>"  # H2 + H3
  - removed: "She felt anger rise in her, sharp and sudden, but she did not let it show."
    replaced_by: "<cut entirely; the cracked-glass action immediately following carries it>"  # H2
  - removed: "For a moment, neither of them spoke"
    replaced_by: "<cut entirely; the fluorescent tick replaces the hedge>"  # H8 (banished phrase)
  - removed: "He smiled, sadly,"
    replaced_by: "His mouth moved into something he did not finish."        # H4 (Tomas voice — qualifiers, unfinished gestures)
  - removed: "He looked at her for a long moment"
    replaced_by: "<cut entirely; the next line carries the beat>"            # H8
  - removed: "the way someone turns a coin to decide which side they had meant"
    replaced_by: "the way he turned things when he was waiting"             # H1 + H4 (POV-specific knowledge)
  - removed: "'Do you know what that is like?'"
    replaced_by: "'There is no file attached.'"                              # H2 + soft_smell s_s1 fix; removes rhetorical question and monologue length

preserved_facts:
  - "Mira does NOT produce the leaked archive entry"                        # confirmed unchanged
  - "Tomas confirms via 'set aside' + 'partly' + 'within reason'"           # confirmed unchanged
  - "Lighter enters before Mira touches it (now even earlier in scene)"     # preserved
  - "Mira lights it correctly without prior archival memory"                # preserved
  - "Scene ends on lighter set back exactly + Mira walking out"             # preserved

banished_replacements:
  - { removed: "a mix of",          replaced_by: "<deletion + sentence break>" }
  - { removed: "for a moment",      replaced_by: "<deletion>" }
  - { removed: "for a long moment", replaced_by: "<deletion>" }

self_verification:
  no_facts_changed: true
  voice_signatures_honored: true
  net_subtraction_achieved: true
  hard_smells_remaining: 0
```
