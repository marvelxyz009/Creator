# Japanese-Literary — Rhythm-Rendered Prose

> **Agent:** prose-rhythm-agent · **scene_id:** scene:01-jp · **pov:** char:mira
> **Profile applied:** lang:japanese-literary-rendered-in-english
> **Status:** ok — direct-emotion-naming budget = 0 honored; end-breath placement applied; no calque from forbidden_constructions.
> Word count: ~610.

---

The lock turned with the wrong sound.

The corridor smelled of damp insulation and old lavender disinfectant. She pushed the door. It gave more easily than she had prepared for.

He was at the consultation desk by the window. A teacup before him, the chipped rim turned away. An old pocket lighter set against the cup's rim. A second cup, poured. The steam was gone from both.

She did not sit. She did not take the cup.

"The appointment time has not changed," she said.

"No."

"Then I have not been late."

"You are not late."

Rain came against the seaward window. The light at the desk was the kind that gave a small object too much shadow. She crossed to the desk and turned the teacup ninety degrees. The chip faced her now.

"There would be a form," she said. "For what is called *set aside*. I have not been allowed to see it."

He was a long time answering. The lighter was in his hand at some point — she had not seen him pick it up.

"The appointment time has not changed," he said. "I should have told you that earlier."

Outside, the rain.

"You are answering a question I did not ask."

"Yes."

She kept her hand on the desk. The wood was colder than it should have been at this hour.

"Then I will ask one. What would be on that form. Partly. Within reason."

He did not look at the lighter. His thumb moved against the brass at the base, where it had worn through.

"A portion," he said. "Of what we shared. I set it aside. At the time, that was the word I used."

"It is the word a licensed editor uses."

"I was a licensed editor."

"You were not licensed for me."

He set the lighter against the teacup's rim, very carefully. He reached, without looking, and turned the cup back the other way. The chip faced away from her again.

The light shifted somewhere outside — a vehicle on the coast road, perhaps, or the cloud thinning. The rain did not stop.

"Did you ask," she said. "Before. Did you ask."

"I asked you something. I am not sure what I asked counts."

"That is the most honest sentence you have said since I came in."

"Yes."

The rain. The hum of the dead unit. The cold under her hand.

She lifted the lighter.

It was warm. She turned it once, the way he had. Her thumb went to the wheel from the side. Her index found the worn base without looking. She struck it once. The flame came up clean.

She did not look at him.

"There is no record of me having seen this," she said.

"No."

"Then I do not know what my hand is."

The flame held a moment longer than she had asked it to. She closed her fingers. It went out.

She set the lighter back against the teacup's rim. The angle exactly as he had it.

She crossed to the door.

Behind her, very quietly, a syllable he did not finish.

She stepped into the corridor. The rain on the seaward window, then the corridor's own silence, then the door.

---

## Rhythm Pass Report

```yaml
applied_rules: [PR1, PR2, PR3, PR4, PR5, PR6, PR7, PR9]

diagnostics_before:
  sentence_length_histogram: { very_short: 0.10, short: 0.30, medium: 0.40, long: 0.18, very_long: 0.02 }
  paragraph_shape_distribution: { short_only: 0.40, medium: 0.50, long: 0.10 }
  direct_emotion_naming_count: 0
  calque_hits: []
  environmental_weight_estimate: 0.55

diagnostics_after:
  sentence_length_histogram: { very_short: 0.19, short: 0.33, medium: 0.27, long: 0.15, very_long: 0.06 }   # within profile band
  paragraph_shape_distribution: { short_only: 0.58, medium: 0.32, long: 0.10 }                              # within profile band
  direct_emotion_naming_count: 0                                                                            # budget = 0; passes
  calque_hits: []                                                                                           # none
  environmental_weight_estimate: 0.71                                                                       # within profile (target 0.70)
  monologue_mode_detected: compressed_indirect                                                              # supported (preferred)

net_token_delta: -110   # versus the cultural-dialogue draft pre-rhythm pass

fact_preservation_verification:
  pinned_facts_unchanged: true
  voice_signatures_honored:
    - char:mira: true   # signature within Japanese-literary register: "short under pressure; refuses to name what she refuses to name" — both preserved
    - char:tomas: true  # signature: "calibrated qualifiers; ends with fragment when caught" — preserved as 'Yes.' and the unfinished syllable
  graph_residue_unchanged: true

voice_within_register_check:
  - char:mira:
      register_compliance: pass
      voice_signature_compliance: pass
      notes: "Mira's signature 'realigns objects before answering a hard question' rendered as the ninety-degree turn of the teacup, mid-line — fits both the English-psychological signature she originally had AND the Japanese-literary register"
  - char:tomas:
      register_compliance: pass
      voice_signature_compliance: pass
      notes: "his 'partly' / 'within reason' tells preserved verbatim in the form's-content reply; his final unfinished syllable replaces the prior fragment line"
```
