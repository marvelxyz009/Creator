# Symbolism by Culture

A reference catalog of **symbol palettes** available per cultural-literary profile. The catalog tells the Cultural Adapter what objects, images, and motifs the target tradition tends to load with weight — and what loads are forbidden as cliché within that same tradition.

## Important Disclaimer

These palettes describe **literary traditions and conventions**, not the lived material culture of any group of people. Modern writers in any tradition routinely break, invert, or refuse these conventions — and an in-tradition writer's *refusal* of a convention can itself be a structural move. The catalog is a *prior* the Cultural Adapter consults when proposing a symbol; the final selection still requires the Symbolism Tracker's state-machine check.

## Palettes

### Japanese-literary palette

**Available loads:**
- rain (light, slow, gendered as solitary)
- seasons (especially transitions — early autumn, late spring)
- trains and stations (departure, arrival, the in-between)
- empty rooms (a person's leftover air)
- domestic objects with use-wear (a chipped cup, a folded coat)
- the cicada / the snow / weather as state-of-mind without metaphor announcement
- water-margins (riverbanks, coasts)

**Forbidden as cliché:**
- cherry blossoms used decoratively without arc
- "samurai" / "katana" iconography in contemporary domestic scenes
- "zen" objects used to signal meditativeness

**Anti-stereotype note:** the palette skews quiet-domestic; do not assume "Japanese symbol = nature-mystical". A train station is doing as much work as a temple, often more.

### Vietnamese-literary palette

**Available loads:**
- meals — especially the meal cooked for someone absent
- incense and family altars (without naming them as "exotic")
- old houses, courtyards, narrow alleys
- rain on a tin roof
- the river / the field at dusk
- a generation gap rendered through a single object (a watch, a comb)
- inherited debt, inherited silence
- a photograph not on a wall but tucked into a book

**Forbidden as cliché:**
- conical hats used as visual shorthand
- war-as-backdrop where the war is not structurally active in the scene
- "rice paddy" as scenic establishing without character function

**Anti-stereotype note:** the palette is heavily domestic and intergenerational, but urban contemporary Vietnamese fiction also uses traffic noise, motorbike exhaust, market voices — do not collapse to a single rural register.

### English-psychological palette

**Available loads:**
- single domestic objects examined at close range (a cracked glass, a kitchen knife, a folded coat)
- texts and documents (letters, files, an email left open)
- weather as mood (but with self-awareness)
- the body's own malfunctions (sleep, appetite, blood pressure)
- the suburban or near-urban interior
- public-private spaces (cafés, waiting rooms, hotel lobbies)
- the obsolete object recovered (a tape, a key)

**Forbidden as cliché:**
- "the mirror reveals the self" beat
- the cigarette as shorthand for moral ambivalence
- the "broken family photograph" beat used without preparation

**Anti-stereotype note:** psychological realism is a literary register, not a description of "English-speaking minds." The palette favors *examined* objects — but examined-ness can become its own cliché.

### English sci-fi (psychological-sci-fi sub-palette)

**Available loads:**
- neon decay, light pollution, the wrong color of streetlight
- static noise, the dead refrigeration unit, the hum
- obsolete technology recovered in a new context
- surveillance traces (a camera, a log file)
- the bureaucratic form as artifact
- the abandoned institutional space (clinics, archives, schools)

**Forbidden as cliché:**
- "the city as character" without the city actually doing anything
- chrome / black-trenchcoat / rain-as-grit cyberpunk-default visuals
- "the AI smiles" or any robotic anthropomorphism used for shorthand

**Anti-stereotype note:** the sub-palette is post-cyberpunk; melancholy is favored over grit; the artifacts are administrative rather than corporate-spectacular.

### Russian-philosophical palette

**Available loads:**
- snow (not romantic — present, heavy, structural)
- the long room, the corridor, the kitchen at night
- the document (letter, manuscript, confession)
- alcohol as social architecture, not character indulgence
- the icon, the threshold, the unanswered door
- weather as moral pressure
- the train — but as ordeal, not transit

**Forbidden as cliché:**
- vodka as a personality trait
- "the Russian soul" invoked or alluded to in narration
- pseudo-Dostoevsky monologue presented as character voice

**Anti-stereotype note:** the philosophical-monologue tradition is real but easily caricatured; modern Russian and Russian-diaspora writing uses far more compression and material specificity than the cliché allows.

## How the Cultural Adapter Uses Palettes

1. The adapter receives the source scene blueprint's `symbolism_used[]` (e.g. `sym:cracked-glass`).
2. It looks up the symbol's **arc-role** (e.g. "small domestic damage returned as evidence of body-knowledge").
3. It selects from the **target culture's palette** a candidate object that can serve the same arc-role.
4. It proposes the swap; the **Symbolism Tracker** validates that the new candidate can hold the same state machine.
5. If no palette candidate can serve the role, the adapter **escalates** — it does not import a foreign object silently.

## How the Symbolism Tracker Uses Palettes

The tracker rejects:
- A symbol drawn from a palette other than the pinned culture profile's, unless explicitly authorized by `cross_palette_authorized: true`.
- A symbol from the **forbidden as cliché** list, unless explicitly authorized with structural justification.

## Extension

Per project, the editor may extend a palette with project-specific symbols. Extensions are stored in the project's culture profile under `symbolism_preferences.extensions[]`. The framework treats extensions as in-palette for that project only.

## Related

- [cultural-narrative-layer.md](./cultural-narrative-layer.md)
- [emotional-expression-matrix.md](./emotional-expression-matrix.md)
- [../literary-styles/](../literary-styles/)
- [../../schema/culture/culture-profile.schema.yaml](../../schema/culture/culture-profile.schema.yaml)
