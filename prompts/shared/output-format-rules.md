# Output Format Rules

Every agent emits **structured output** — never free-form prose mixed with structured data. This file defines the universal rules.

## Format Choice

- **YAML** for: schemas, blueprints, reports, validators, contracts.
- **Markdown** for: prose drafts (Prose Agent only), Vision document.
- **No JSON in agent outputs.** YAML is preferred for human readability and comment support.

## Universal Envelope

Every agent output begins with this envelope:

```yaml
agent: <agent-id>           # e.g. scene-director
agent_version: <semver>
run_id: <opaque id>
inputs_hash: <hash of inputs bundle>
generated_at: <ISO-8601>
status: ok | soft_reject | hard_reject | escalate
notes: <optional, short>
```

Followed by the agent-specific body.

## Body Rules

1. **No prose where structure is expected.** A field named `purpose` accepts a sentence; a field named `character_actions` accepts a list of structured items.
2. **No nested free-text dumps.** If a field would exceed ~200 words of free text, it MUST be decomposed into sub-fields.
3. **No "see above" / "as previously stated".** Every field stands alone.
4. **No prompts inside outputs.** Agents do not embed instructions for the next agent inside their output — that's the orchestrator's job.
5. **Cite IDs, not summaries.** When referencing characters, scenes, symbols — cite the canonical id (`char:mira`, `sym:iron-key`, `scene:04-12`). Do not paraphrase identity.

## Failure Output

When `status: hard_reject` or `escalate`, the body MUST contain:

```yaml
rejection:
  reason: <one-sentence>
  violated_rules: [R3, R6, ...]      # rule ids from global-narrative-rules
  upstream_artifact_at_fault: <artifact ref, if known>
  suggested_repair: <one short paragraph>
```

## Length Discipline

- Blueprints: ≤ ~400 lines of YAML.
- Reports: ≤ ~200 lines.
- Free-text fields inside structured output: ≤ ~120 words.
- Prose drafts (Prose Agent only): bounded by scene contract (typically 600–2000 words).

If an output exceeds these bounds, the agent must compress or escalate — never silently produce a wall of text.

## Identifier Conventions

| Type | Prefix | Example |
|---|---|---|
| Character | `char:` | `char:mira` |
| Symbol | `sym:` | `sym:iron-key` |
| Location | `loc:` | `loc:kiln` |
| Event | `event:` | `event:harbor-fire` |
| Theme-beat | `beat:` | `beat:t1` |
| Scene | `scene:` | `scene:04-12` |
| Relation | `rel:` | `rel:mira-tomas` |
| Debt | `debt:` | `debt:0007` |

## Related

- [global-narrative-rules.md](./global-narrative-rules.md)
- [context-contract.md](./context-contract.md)
