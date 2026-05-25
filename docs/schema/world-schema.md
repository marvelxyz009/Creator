# World Schema

World is the **physical and social pressure** that forces the theme into action. Worldbuilding without theme is set dressing; theme without world is essay.

## Schema

```yaml
id: world:primary
name: "The Harbor of Calder"

premise: "A salt-port city where confession is a public utility — sins are recorded, weighed, and taxed."

logic:
  rules:
    - id: r1
      rule: "Confession before the kiln burns the spoken name into iron."
      consequence_if_broken: "The named owes the speaker silence for life."
    - id: r2
      rule: "An unburned confession spoils within three days."
  costs:
    - "Truth costs metal. Iron is taxed. The poor confess in whispers that don't survive."

locations:
  - id: loc:kiln
    function: "site of public confession"
    mood_default: "warm dread"
    symbolic_load: high
    bound_to_themes: [beat:t1]

  - id: loc:harbor
    function: "site of the inciting trauma"
    mood_default: "salt and aftermath"

social_layer:
  factions:
    - id: f:scribes
      role: "record and tax confessions"
      pressure_on_protagonist: "they want her unburned confession"

texture:
  sensory_palette:
    sight: ["iron, salt, wet wool, ember"]
    sound: ["kiln-roar, gull, the dull bell"]
    smell: ["brine, scorched metal, lamp-oil"]
  forbidden_textures: ["high-fantasy gloss", "magic-system jargon", "epic-poetic abstraction"]

constraints_on_story:
  - "Any confession scene must engage rule r1 or knowingly violate it."
  - "No scene set at the kiln may end with status quo intact."

unknowns:
  - "Why iron, not fire alone? Reserved for later reveal — do not resolve in act 1."
```

## Required Fields

- `premise` — one sentence, contains the world's *unusual constraint*.
- `logic.rules` — at least one rule that *creates dramatic pressure*, not just flavor.
- `texture.sensory_palette` — populated for all five senses (or explicit omission).
- `texture.forbidden_textures` — non-empty.

## Validation Rules

1. Every rule in `logic.rules` must have a `consequence_if_broken`. Rules without teeth are flavor.
2. At least one location must be `bound_to_themes` with a theme-beat id.
3. `constraints_on_story` must produce at least one scene-level rejection criterion the Scene Designer can enforce.
4. `unknowns` is required — the world must contain things the work will not explain in act 1.

## Related

- [[theme-schema]]
- [[scene-schema]]
- [[memory-graph]]
