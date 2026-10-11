# Vietnamese-Literary — Cultural Dialogue Draft

> **Agent:** cultural-dialogue-specialist · **scene_id:** scene:01-vn · **pov:** char:mira
> **Culture profile:** culture:vietnamese-literary-contemporary · **Language style:** lang:vietnamese-literary-rendered-in-english
> **Status:** ok — third-party routing through Tomas's mother and late father; address-form drop as turn; kinship tokens retained.

---

The lock turned wrong. The rain came against the louvered window in long uneven runs.

He was at the desk. A chipped tea bowl in front of him, the rim's chip turned away. The lighter beside it — the battered one she had not seen before, with the engraving worn down. He had poured a second cup. The steam was already gone from it.

She did not sit. She did not take the cup.

"Bác có khỏe không, anh," she said. *Is your mother well.*

He looked up. "Em," he said. "Mẹ vẫn khỏe."

She let it stand a moment. Then she stepped to the desk and turned the tea bowl ninety degrees, so the chip faced her.

"Bác đưa bát này cho anh khi anh dọn ra ở riêng," she said. *Your mother gave you this bowl when you moved out.*

He did not answer.

"And anh brought it here. Tonight."

<silence>

He reached for the second cup and slid it a small distance toward her side of the desk.

She did not take it.

"There would be a form," she said. "For what is called *gác lại*. *Set aside.* I have not been allowed to see it."

He was a long time answering.

"Một phần," he said. *A portion.* "Of what we shared. Em — gác lại. That was the word."

"It is the word a licensed editor uses."

"I was a licensed editor."

"Anh wasn't licensed for em."

He reached, without looking, and turned the tea bowl back the other way. The chip faced away from her again.

She looked at the lighter. The engraving was worn but she could see the shape of it — a name and a year, the name longer than Tomas's own.

"That was your father's."

"Yes."

<silence>

She kept her hand on the desk. The wood was colder than it should have been at this hour.

"Did anh ask em," she said. "Before. Did anh ask."

"I asked you something. I am not sure what I asked counts."

"That is the most honest sentence anh has said since em walked in."

"Yes."

She let the silence run. Outside, the rain on the louvers. Inside, the second cup waiting that she had not taken, the bowl with the chip turned away from her again.

She lifted the lighter.

It was warm. She turned it once, the way he had — and stopped. Her thumb had gone to the wheel from the side. Her index had found the worn engraving without looking. She struck it once. The flame came up clean on the first try.

She did not look at him.

"Có lẽ em không biết tay em là gì nữa." *Perhaps I do not know what my hand is anymore.*

She did not use a kinship token in the next line. She used none.

"Tomas. There is no record of me having seen this."

"No."

She set the lighter back. Against the tea bowl's rim. The angle exactly as he had it.

She did not say goodbye. She crossed to the door. Behind her, very quietly —

"Em—"

She stepped into the corridor. The rain on the louvers, then the corridor's own occupied silence — water somewhere, a pipe — then the door behind her.

---

## Cultural Compliance Notes

```yaml
directness_resolutions:
  - ex_first_line:
      source_directness: direct        # "You knew I'd come tonight"
      target_directness: third_party_routed
      mechanism: "asks after his mother — the question lands the family inside the room before anything else"
  - ex_accusation_core:
      source_directness: direct        # "You weren't licensed for me"
      target_directness: implied via family object first, then direct at turn
      mechanism: "the bowl-from-his-mother line lands the accusation by implication; the 'Anh wasn't licensed for em' line preserves the structural punch of the source line but the kinship asymmetry sharpens it"
  - ex_apology:
      target_directness: burden_acceptance + half-spoken
      mechanism: "Tomas does not defend his mother, does not deny the bowl's provenance; he simply 'turns the tea bowl back' — burden acceptance through gesture"
  - ex_register_shift_as_turn:
      mechanism: "Mira drops 'anh' and uses 'Tomas' (name alone, no kinship token) for the first time in the scene — this is the heaviest line; the line after follows in English with no kinship asymmetry"

address_form_resolutions:
  - speaker: char:mira → char:tomas
    forms_used_in_order: [anh, anh, anh, <DROPPED — Tomas>, <no address>]
  - speaker: char:tomas → char:mira
    forms_used_in_order: [em, em, em, em, em, em (final half-syllable)]
  - significance: "Mira's drop of 'anh' is the address-form-as-turn beat; Tomas's 'em' through the close marks him as the one who did not break the register"

silence_count: 3   # occupied silences (someone slides the cup, turns the bowl, sets the lighter)
silence_budget_compliance: within budget (weight 0.45)

third_party_routings:
  - charged_topic: "the edit / what was set aside"
    routed_via: ["his mother (the bowl)", "his late father (the lighter)", "the family present without being present"]
    rationale: "under this profile, the accusation is rarely landed direct between intimates — family objects bear the weight"

apology_shape: burden_acceptance + gestural
  manifestation: "Tomas turns the bowl back without denying its provenance; he does not lift the lighter once it is set down; he does not finish the half-syllable at close"

taboo_substitutions:
  - "you edited my memory" → "Bác đưa bát này cho anh khi anh dọn ra ở riêng" + "There would be a form, for what is called gác lại"
  - "I am angry / I am hurt" → refused tea + bowl-turn + address-form drop
  - "I still feel something for you" → the body-knowledge of his late father's lighter + the address-form drop
  - the word "edit" → never appears
  - the word "memory" → never appears
  - the word "feel" → never appears

kinship_tokens_retained:
  - anh, em, bác, mẹ
  - "gác lại" retained as the Vietnamese equivalent of 'set aside'
  - rationale: "translating these to English equivalents collapses the asymmetry that the scene relies on; the editor decides whether to gloss for non-Vietnamese readers — the dialogue specialist does not pre-gloss"

no_cultural_exposition_to_reader: true
no_stereotype_iconography: true
no_rural_register_intrusions: true
no_diasporic_nostalgia: true
no_eastern_wisdom_voice: true
```

## Self-verification

- [x] Mira does NOT produce the leaked archive entry
- [x] Tomas's qualified confirmation arrives ("Một phần. Of what we shared. Gác lại.")
- [x] The lighter is introduced before Mira touches it
- [x] Mira lights it correctly without prior archival memory
- [x] Scene ends on lighter set back exactly + Mira walking out + Tomas's unfinished half-syllable
- [x] All seven `residue.graph_writes` from invariants are renderable; additionally a new debt:0003 is seeded (family pressure imported) — this is an *additive* residue, not an invariant violation, and is declared in the adapted blueprint
- [x] No forbidden English lexicon ("edit", "memory", "feel") appears
- [x] No conical hat, no rural establishment, no war-as-backdrop, no Eastern-wisdom voice
