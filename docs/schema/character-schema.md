# Character Schema

Characters are **systems of contradiction**, not bundles of traits. The schema is built to make this structural, queryable, and enforceable.

## Schema

```yaml
id: char:mira
name: Mira Vale
role: protagonist            # protagonist | antagonist | foil | mirror | chorus
archetype_seed: null         # informational only; never the whole character

contradictions:
  - id: c1
    forces:
      a: "wants to be fully known"
      b: "fears that being known will be used against her"
    pressure: high           # low | medium | high
    resolution_due_by: act-3 # graph-tracked debt

drives:
  surface: "find her brother"            # what she says she wants
  buried: "be forgiven by her brother"   # what she actually wants

wound:
  origin: "abandoned the brother in the harbor fire (ch.7 reveal)"
  current_pressure: medium

voice_signature:
  sentence_length_distribution: "short bursts under stress; long when lying"
  lexical_register: "working-class harbor vocabulary; avoids abstract nouns"
  what_they_notice: ["hands", "exits", "the weight of cloth"]
  what_they_refuse_to_name: ["the fire", "her brother by first name"]
  rhythmic_tells: ["repeats a word when frightened", "ends statements as questions when conceding"]

knowledge_set:
  knows:
    - event:harbor-fire (true cause)
    - sym:iron-key (origin)
  hidden_from:
    - char:tomas

relations:
  - with: char:tomas
    type: "unspoken debt + unspoken want"
    tension: 0.8
    unresolved_beats: [confess-fire, accept-help]

contradiction_tests:
  - "If forced to choose between being seen and being safe, the choice must cost something."
  - "She must lie at least once where the lie reveals more than the truth would."

forbidden:
  - flat exposition of her wound
  - any line that summarizes her psychology in narration
```

## Required Fields

- `id`, `name`, `role`
- `contradictions` — at least one, with `forces.a` and `forces.b` materially opposed.
- `drives.surface` and `drives.buried` — must differ.
- `voice_signature` — all four sub-fields populated.
- `wound` — even minor characters carry one; chorus characters may declare `wound: null` with justification.

## Validation Rules

1. `contradictions[].forces.a` and `.b` must be **materially opposed**, not graded ("brave but cautious" fails).
2. `drives.surface == drives.buried` is a hard reject.
3. `voice_signature.what_they_refuse_to_name` must not be empty for any named POV character.
4. `knowledge_set.knows` must reference real nodes in the [[memory-graph]].
5. Two characters cannot share an identical `voice_signature`. The Voice Auditor enforces this.

## Related

- [[memory-graph]]
- [[narrative-laws]] (Law 2, Law 7)
- [[agent-contracts]] (Character Psychologist)
