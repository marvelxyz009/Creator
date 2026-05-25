# Japanese-Literary — Cultural Dialogue Draft

> **Agent:** cultural-dialogue-specialist · **scene_id:** scene:01-jp · **pov:** char:mira
> **Culture profile:** culture:japanese-literary · **Language style:** lang:japanese-literary-rendered-in-english
> **Status:** ok — taboo substitutions honored; silence budget = 4; address-form = no-address dominant.

---

The lock turned with the wrong sound. The corridor smelled of damp insulation and old lavender disinfectant. She pushed the door.

He was at the consultation desk by the window. A teacup before him, the chipped rim turned away from where she would stand. An old pocket lighter set against the cup's rim. A second cup, poured.

She did not sit. She did not take the cup.

"The appointment time has not changed," she said. It was not a question.

"No."

"Then I have not been late."

"You are not late."

The rain came against the seaward window. She crossed to the desk. She turned the teacup ninety degrees, so the chip faced her.

"There would be a form," she said. "For what is called *set aside*. I have not been allowed to see it."

He was a long time answering.

"The appointment time," he said, "has not changed. I should have told you that earlier."

<silence>

"You are answering a question I did not ask."

"Yes."

She kept her hand on the desk. The wood was colder than it should have been at this hour.

"Then I will ask one. What would be on that form. Partly. Within reason."

He did not look at the lighter. His thumb moved against the brass at the base.

"A portion," he said. "Of what we shared. I set it aside. At the time, that was the word I used."

"It is the word a licensed editor uses."

"I was a licensed editor."

"You were not licensed for me."

He set the lighter against the teacup's rim, very carefully. He reached, without looking, and turned the cup back the other way, so the chip faced away from her again.

<silence>

She nearly spoke. She did not.

"Did you ask," she said. "Before. Did you ask."

"I asked you something. I am not sure what I asked counts."

"That is the most honest sentence you have said since I came in."

"Yes."

The rain. The hum of the dead unit. The wrong cold under her hand.

<silence>

She lifted the lighter.

It was warm. She turned it once, the way he had. Her thumb went to the wheel from the side. Her index found the worn base without looking. She struck it once. The flame came up clean.

She did not look at him.

"There is no record of me having seen this," she said.

"No."

"Then I do not know what my hand is."

<silence>

She set the lighter back. Against the teacup's rim. The angle exactly as he had it.

She crossed to the door. Behind her, very quietly, a syllable he did not finish.

She stepped into the corridor.

---

## Cultural Compliance Notes (per [cultural-dialogue-specialist](../../../../prompts/culture/cultural-dialogue-specialist.prompt.md))

```yaml
directness_resolutions:
  - ex_first_line:
      source_directness: direct       # "You knew I'd come tonight"
      target_directness: implied
      mechanism: "procedural opening about the appointment time; never opens on the accusation"
  - ex_accusation_core:
      source_directness: direct       # "You weren't licensed for me"
      target_directness: implied → direct only when the form is named
      mechanism: "the line 'You were not licensed for me' is preserved verbatim from the source — under this profile it lands harder because the build-up was indirect"
  - ex_apology:
      target_directness: gestural
      mechanism: "Tomas places the lighter at the teacup's rim; the verbalized half-apology arrives in two short replies; no full apology is uttered"

address_form_resolutions:
  - speaker: char:mira → char:tomas
    form: no-address (dominant throughout — she does not say his name once)
  - speaker: char:tomas → char:mira
    form: no-address (dominant); 'Mira' (name alone, no honorific) is NOT used in this draft — left available for next scene's shift

silence_count: 4   # exchanges as <silence> with intent and subtext
silence_budget_compliance: within budget (weight 0.55)

taboo_substitutions:
  - "you edited my memory" → "the form" + "what is called set aside"
  - "I am angry / I am hurt" → not spoken; carried by refusal of the offered cup, hand placement, exit without looking
  - the word "edit" → never appears
  - the word "memory" → never appears
  - the word "feel" → never appears
  - the word "real" → never appears

apology_shape: gestural + qualified
  manifestation: "the lighter placed at the teacup's rim; 'I should have told you that earlier' (qualified, non-specific)"

no_cultural_exposition_to_reader: true
no_stereotype_iconography: true   # no temple, no kimono, no cherry blossom, no 'wabi-sabi' or 'mono no aware' anywhere
```

## Self-verification

- [x] Mira does NOT produce the leaked archive entry
- [x] Tomas's qualified confirmation arrives ("A portion. Of what we shared. I set it aside. At the time, that was the word I used.")
- [x] The lighter enters before Mira touches it (in fact appears in the opening paragraph)
- [x] Mira lights it correctly without prior archival memory
- [x] Scene ends on lighter set back exactly + Mira walking out + unfinished syllable
- [x] All seven `residue.graph_writes` from invariants are renderable from this draft
- [x] No forbidden lexicon ("edit", "memory", "feel", "real") appears in the draft
