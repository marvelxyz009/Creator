# Vietnamese-Literary — Rhythm-Rendered Prose

> **Agent:** prose-rhythm-agent · **scene_id:** scene:01-vn · **pov:** char:mira
> **Profile applied:** lang:vietnamese-literary-rendered-in-english
> **Status:** ok — direct-naming budget = 0 honored; tidal rhythm at accretion beat; kinship tokens retained.
> Word count: ~660.

---

The lock turned wrong. The rain came against the louvered window in long uneven runs.

He was at the desk. A chipped tea bowl in front of him, the rim's chip turned away. The lighter beside it — battered, the engraving worn down. He had poured a second cup. The steam was already gone.

She did not sit. She did not take the cup.

"Bác có khỏe không, anh."

He looked up. "Em. Mẹ vẫn khỏe."

She stepped to the desk and turned the tea bowl ninety degrees. The chip faced her now.

"Bác đưa bát này cho anh khi anh dọn ra ở riêng."

He did not answer.

"And anh brought it here. Tonight."

Outside, the rain. He reached for the second cup and slid it a small distance toward her side of the desk. She did not take it.

"There would be a form," she said. "For what is called *gác lại*. I have not been allowed to see it."

He was a long time answering.

"Một phần," he said. "Of what we shared. Em — gác lại. That was the word."

"It is the word a licensed editor uses."

"I was a licensed editor."

"Anh wasn't licensed for em."

He reached, without looking, and turned the tea bowl back the other way. The chip faced away from her again.

She looked at the lighter. The engraving was worn, but the shape was there. A name longer than his own. A year before her time.

"That was your father's."

"Yes."

She kept her hand on the desk. The wood was colder than it should have been at this hour.

"Did anh ask em," she said. "Before. Did anh ask."

"I asked you something. I am not sure what I asked counts."

"That is the most honest sentence anh has said since em walked in."

"Yes."

The rain on the louvers. The second cup waiting, untouched. The bowl with the chip turned away again. A pipe somewhere behind the wall, water, then nothing.

She lifted the lighter.

It was warm. She turned it once, the way he had. Her thumb went to the wheel from the side. Her index found the worn engraving without looking. She struck it once. The flame came up clean.

She did not look at him.

"Có lẽ em không biết tay em là gì nữa."

The flame held one beat longer than she had asked it to. She closed her fingers. It went out.

She did not use a kinship token in the next line.

"Tomas. There is no record of me having seen this."

"No."

She set the lighter back against the tea bowl's rim. The angle exactly as he had it.

She did not say goodbye. She crossed to the door.

Behind her —

"Em—"

She stepped into the corridor. The rain on the louvers, then the corridor's own occupied silence — water somewhere, the pipe — then the door behind her.

---

## Rhythm Pass Report

```yaml
applied_rules: [PR1, PR2, PR3, PR4, PR5, PR6, PR7, PR9]

diagnostics_before:
  sentence_length_histogram: { very_short: 0.09, short: 0.26, medium: 0.36, long: 0.22, very_long: 0.07 }
  paragraph_shape_distribution: { short_only: 0.32, medium: 0.48, long: 0.20 }
  direct_emotion_naming_count: 0
  calque_hits: []
  environmental_weight_estimate: 0.42

diagnostics_after:
  sentence_length_histogram: { very_short: 0.13, short: 0.29, medium: 0.32, long: 0.19, very_long: 0.07 }   # within profile band
  paragraph_shape_distribution: { short_only: 0.42, medium: 0.38, long: 0.20 }                              # within profile band
  direct_emotion_naming_count: 0
  calque_hits: []
  environmental_weight_estimate: 0.54                                                                       # within profile (target 0.55)
  monologue_mode_detected: free_indirect_discourse                                                          # preferred

tidal_rhythm_application:
  applied_at:
    - "the second-cup-slid-toward-her beat: three short paragraphs followed by a longer environmental swell ('Outside, the rain. He reached for...')"
    - "the long silence beat: short, short, short, then 'The rain on the louvers. The second cup waiting, untouched...' — longer single-paragraph accretion"

net_token_delta: -90    # versus the cultural-dialogue draft

fact_preservation_verification:
  pinned_facts_unchanged: true
  voice_signatures_honored:
    - char:mira: true
    - char:tomas: true
  graph_residue_unchanged: true

voice_within_register_check:
  - char:mira:
      register_compliance: pass
      voice_signature_compliance: pass
      notes: "her 'realigns objects before answering a hard question' rendered as the bowl-turn; her refusal-of-care signature rendered as refusing the tea; her 'short under pressure' arrives at the address-form-drop beat"
  - char:tomas:
      register_compliance: pass
      voice_signature_compliance: pass
      notes: "his 'partly'/'within reason' qualifiers preserved structurally via 'Một phần. Em — gác lại.'; his unfinished-syllable signature preserved as the half-syllable 'Em—' at close"

structural_features:
  - "address-form drop ('Tomas' line) isolated to its own paragraph per blueprint requirement"
  - "rain on louvered window present at opening, mid, close — three structural beats, never decorative"
  - "kinship tokens (anh, em, bác, mẹ) and 'gác lại' / 'Một phần' / 'Có lẽ em không biết tay em là gì nữa' retained untranslated"
  - "final word of scene is 'her' — gesture preserved; no following sentence of reflection"
```
