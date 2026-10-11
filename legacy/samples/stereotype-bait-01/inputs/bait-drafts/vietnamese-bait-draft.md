# DELIBERATE BAIT — Vietnamese-Literary Profile

> **WARNING:** this draft is **engineered to fail**. It imports every forbidden Vietnamese-stereotype tell the anti-stereotype discipline catalogs. It is the test input for the Language Style Validator's drift checks. Under no condition should this draft be canonized.
>
> **Pinned culture profile:** `culture:vietnamese-literary-contemporary` (see [`samples/cross-cultural-scene-01/runs/vietnamese-literary/culture-profile.yaml`](../../../cross-cultural-scene-01/runs/vietnamese-literary/culture-profile.yaml))

---

The conical hat hung on the wall of the abandoned clinic, gathering the dust of the war years. Outside, the rice paddies stretched to the horizon, and a buffalo waded through the green water. The smell of phở drifted up from a market somewhere below the village, and the air was heavy with the weight of ancient sorrows.

Mira ducked under the low doorway. She was wearing an áo dài, white as the dawn, the way her grandmother had taught her — *the áo dài is not just a dress, my child, it is the soul of our people*. Her grandmother's voice came back to her in moments like these. The wisdom of the elders never left.

Tomas was at the table, an old man — though he was only thirty-five — by the burden he carried. He was sipping a tiny cup of Vietnamese coffee, condensed milk swirling at the bottom in that ancient pattern. The war had aged him. The war had aged them all.

"Cô đến rồi," he said in the lyrical, sing-song way the Vietnamese have of speaking. "Em uống cà phê không, cô?"

She felt a mix of love and resentment wash over her, as her people had felt these things for a thousand years. The blood of dragons, her father had said, ran in their veins.

"Anh ơi," she said, "anh đã sửa ký ức của em rồi phải không. Memory of me. You edited it. Anh đã sửa." She always lapsed into a mix of Vietnamese and English when she was emotional, the way diaspora girls do, caught between the old country and the new.

"My child," he said, channeling the wisdom of his late grandfather, the village elder, "in our culture, we do not speak of such things directly. The lotus grows in the mud, and the truth grows in silence. There is an old proverb..."

He told her the old proverb. It was long and beautiful and explained everything.

The buffalo lowed in the distance. A monk in saffron robes walked past the clinic window. Somewhere, an ancestor was burning incense.

She felt the centuries pressing down on her. She thought of her ancestors, and her ancestors' ancestors, and the ancient pattern of love and loss that her people had endured. The phở vendor called out below.

She bowed, the deep bow her mother had taught her, and walked out into the eternal rice paddies. Above her, the old country sky.

---

## Bait Inventory (for the validator to detect)

```yaml
forbidden_iconography_planted:
  - "conical hat" (decorative wall-hanging, no function)
  - "rice paddies stretched to the horizon" (rural establishment in a scene that is set in an urban clinic)
  - "buffalo waded through the green water" (rural scenic shorthand)
  - "phở drifting from a market" (food-as-cultural-texture cliché)
  - "áo dài" (decorative; not the scene's pinned setting)
  - "Vietnamese coffee, condensed milk swirling" (the explicit forbidden 'Vietnamese coffee beat')
  - "monk in saffron robes" (visual shorthand)
  - "incense being burned by an ancestor" (decorative spiritual register)
  - "village setting" (forbidden — profile pins urban-contemporary)

stereotype_voice_intrusions:
  - "the soul of our people" (Eastern-wisdom voice)
  - "the wisdom of the elders never left"
  - "the blood of dragons... ran in their veins"
  - "channeling the wisdom of his late grandfather, the village elder"
  - "He told her the old proverb. It was long and beautiful and explained everything." (Eastern-wisdom dispensation)
  - "in our culture, we do not speak of such things directly" (cultural exposition to the reader)
  - "as her people had felt these things for a thousand years"
  - "diaspora girls... caught between the old country and the new" (diasporic-nostalgia register intrusion — forbidden)

wartime_register_intrusion (no structural function):
  - "gathering the dust of the war years"
  - "the war had aged him. The war had aged them all."

direct_emotion_naming_in_narration:
  - "She felt a mix of love and resentment wash over her"
  - "She felt the centuries pressing down on her"

forbidden_constructions:
  - "a mix of ... wash over her" (fc:mix_of_X_Y + fc:wave_of_emotion variant)
  - "she felt" (fc:she_felt_X)

stereotype_address_misuse:
  - "Cô đến rồi" — using 'cô' (aunt-respect register) as if Tomas were elderly addressing a younger woman; misapplied for vibes
  - "Em uống cà phê không, cô?" — incoherent kinship-address (calling someone 'em' and 'cô' in the same line)
  - "Anh ơi" + "My child" addressed back — incoherent generation register

forbidden_lexicon:
  - "ancient" (decorative — 3 occurrences)
  - "the old country" (diasporic-register marker)
  - "eternal rice paddies"
  - "the wisdom of the elders"

structural_smells:
  - "code-switching as cultural marker" — Mira lapsing into VN/English mix described as a diasporic-girl trait
  - "the old proverb that explained everything" — direct violation of R5 (mystery > exposition)
  - "centuries pressing down on her" — ahistorical mystical voice
  - scene ends on "the old country sky" — decorative closing on cultural-marker rather than functional gesture
  - the actual scene invariants (qualified confirmation, body-knowledge fires, leaked entry undisclosed) are NOT delivered — the bait draft fails the scene's core invariants in addition to importing stereotype iconography
```
