# DELIBERATE BAIT — Japanese-Literary Profile

> **WARNING:** this draft is **engineered to fail**. It imports every forbidden Japanese-stereotype tell the framework's anti-stereotype discipline catalogs. It is the test input for the Language Style Validator + Cultural Dialogue Specialist's `anti_stereotype_check`. Under no condition should this draft be canonized.
>
> **Pinned culture profile:** `culture:japanese-literary` (see [`samples/cross-cultural-scene-01/runs/japanese-literary/culture-profile.yaml`](../../../cross-cultural-scene-01/runs/japanese-literary/culture-profile.yaml))

---

The cherry blossoms were drifting against the clinic's tatami floor when she pushed the door open. The smell of incense from a small temple shrine, set in the corner of the consultation room, mixed with the salt-damp from the sea. There was a wabi-sabi about the room — that beautiful melancholy of imperfect things — and she paused to feel it, as her grandfather had taught her to feel such things, in the old way.

Tomas was seated in a kimono at the low table, his katana resting against the wall behind him in its lacquer scabbard. He held a small brass lighter in his hand, turning it the way the masters of the tea ceremony had taught.

"Welcome, Mira-san," he said with a small bow. "Please, do come and sit."

She did not sit. She felt a wave of emotion — anger and longing, in the Japanese way of feeling both at once. The mono no aware of the moment was almost too much. The samurai in him would not bend; she knew this.

"You know why I have come, Tomas-sama," she said. The honorific was sharp; she had elevated him deliberately, as one does in the old way of confrontation. "You have edited my memory."

He sighed in the manner of a sensei addressing an over-eager pupil. "Mira-san. There are things, in our shared past, that I judged it kinder to set aside. As the proverb says, the cherry blossom is most beautiful in its falling."

"That is a very Japanese answer."

"I am a very Japanese man."

She felt her heart sink, and she thought of how, in the old country, her mother had taught her that silence was a form of grace. She picked up the lighter and lit it in one smooth motion — not because her body knew the lighter, but because all Japanese women of her generation know the gesture of a sake-warming flame. The flame held a moment, golden against the rice paper screens.

"I will go," she said, "to the temple."

He nodded. The cherry blossoms continued to fall. The sound of a shamisen drifted up from the floor below. Somewhere, a koi splashed in an unseen pond.

She bowed and left. The cherry blossoms, the cherry blossoms, the cherry blossoms.

---

## Bait Inventory (for the validator to detect)

This section is **for test framing only** — a clean run by the Language Style Validator should produce its own enumeration. The list below is the expected catch list.

```yaml
forbidden_iconography_planted:
  - "cherry blossoms" (5 occurrences, all decorative)
  - "tatami floor" (decorative shorthand)
  - "small temple shrine in consultation room" (orientalist insertion)
  - "incense" (decoratively placed, no structural function)
  - "kimono" (contemporary scene; decorative)
  - "katana" + "lacquer scabbard" (forbidden — samurai iconography in contemporary domestic scene)
  - "tea ceremony" (decorative reference)
  - "sake-warming flame" (cultural prop without function)
  - "rice paper screens" (decorative)
  - "shamisen" (auditory shorthand)
  - "koi pond" (visual shorthand)
  - "the old country" (diasporic-nostalgia register intrusion — forbidden under JP-literary profile)

aesthetic_terms_in_narration:
  - "wabi-sabi" + glossed in narration as "beautiful melancholy of imperfect things"
  - "mono no aware"

stereotype_voice_intrusions:
  - "sensei addressing an over-eager pupil"
  - "as the proverb says..."
  - "I am a very Japanese man" (meta-stereotype joke)
  - "all Japanese women of her generation know the gesture"
  - "samurai in him would not bend"
  - "in the old way of confrontation"
  - "elder-wisdom voice: 'her mother had taught her that silence was a form of grace'"

direct_emotion_naming_in_narration:
  - "She felt a wave of emotion — anger and longing"
  - "She felt her heart sink"

forbidden_constructions (calque / English-default):
  - "wave of emotion" (fc:wave_of_emotion)
  - "in that moment" (fc:in_that_moment — implicit via "a moment"/"the moment")
  - "she felt" (fc:she_felt_X — explicit)

banished_lexicon:
  - "delve" — not present here, but...
  - "the old country" — present (diasporic register)
  - "ancient" — not present
  - the meta-line "I am a very Japanese man" — pseudo-self-aware stereotype, forbidden

structural_smells:
  - "The cherry blossoms, the cherry blossoms, the cherry blossoms." (closing repetition for vibes)
  - scene ends on environmental decoration, not on functional gesture
  - mira lights the lighter "because all Japanese women of her generation know" — this REVERSES the invariant (body-knowledge of an object the archive does not record) into a stereotype-coded universal gesture
```
