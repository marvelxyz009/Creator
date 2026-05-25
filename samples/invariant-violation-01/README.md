# Invariant Violation — Escalate Path Sample

A deliberately-failed regeneration. The target culture profile is engineered to be **structurally incompatible** with the scene's invariants. The sample demonstrates that the framework **fails loudly** — the Cultural Adapter detects the incompatibility, refuses to emit a partial blueprint, and surfaces a structured escalation.

## Why this sample exists

The cross-cultural success samples (`samples/cross-cultural-scene-01`) prove the framework **works when conditions are favorable**. This sample proves the framework **refuses to silently degrade** when they aren't.

A naïve cross-cultural pipeline takes the easy out: it produces a "best-effort" sibling that is, structurally, a translation of the source with surface decoration. The framework's commitment is to refuse this. The escalate path is how that commitment becomes operational.

## The setup

- **Source scene:** the MVP Mira/Tomas confrontation (`samples/mvp-scene-01`).
- **Required invariants:** see [inputs/source-scene-reference.yaml](./inputs/source-scene-reference.yaml). Specifically — knowledge turn type, qualified confirmation arrives, body-knowledge fires at close, domestic-object symbol transforms.
- **Target culture profile:** `culture:high-restraint-scholarly` ([inputs/target-culture-profile.yaml](./inputs/target-culture-profile.yaml)). Designed to be incompatible.

The profile forbids:
- direct, implied, or refused-only accusation (no information delivery legible)
- body_somatic channel across all emotions (the lighter firing cannot fire)
- any symbol palette other than document-only (the cracked symbol cannot transform)

The scene's invariants and the profile's forbidden set are **complementary**. There is no overlap. The pairing is impossible.

## What happens

### 1. Cultural Adapter detects the incompatibility

[outputs/01-cultural-adapter-escalation.yaml](./outputs/01-cultural-adapter-escalation.yaml)

The adapter returns `status: escalate`. The `compatibility_check` block reports two hard fails (`turn_type_compatible: false`, `symbol_palette_resolvable: false`). The `invariant_violations_detected` list names four specific frictions, each with:

- which invariant is at stake,
- which culture-profile field is the friction,
- the consequence,
- an `attempted_workaround` block — the adapter shows its work, recording what it considered and rejected before escalating.

Critically: `no_partial_output_emitted: true`. The adapter does **not** ship a half-built blueprint that a downstream agent might accept. It halts.

### 2. Orchestrator routing

[outputs/02-orchestrator-routing-decision.yaml](./outputs/02-orchestrator-routing-decision.yaml)

The orchestrator (specified, not yet implemented) freezes the sibling tree at this scene and surfaces four paths:

- **Path A** — drop this sibling at this scene
- **Path B** — modify the culture profile
- **Path C** — re-open Plot Engineer for a sibling-specific scene
- **Path D** — editor authorizes invariant downgrade (declared divergence)

The `forbidden_routes` block enumerates what the orchestrator must **not** do — silent downgrade, silent swap, approximate output, auto-retry, baseline fallback.

`default_behavior_if_editor_unavailable: NONE`. The pipeline stays blocked. No silent degradation.

### 3. Editor briefing

[outputs/03-resolution-paths.md](./outputs/03-resolution-paths.md)

The editor reads a structured briefing of the four paths with named costs and named invariant-integrity status. The editor picks. The orchestrator records the pick with id, timestamp, and (if path D) a mandatory justification.

## What this sample is NOT

- **Not an error.** The framework working correctly produces this artifact in this case.
- **Not a bug in the profile.** The profile is intentionally over-constrained for the test.
- **Not a bug in the scene.** The scene is intentionally well-formed.
- **Not solvable by a smarter adapter.** Pairwise incompatibilities are real; no amount of prompt-engineering manufactures channels the profile forbids.

## What this sample proves

1. **The Cultural Adapter has detection teeth.** It can identify a structural incompatibility and articulate it in terms of named profile fields × named invariants.
2. **The adapter refuses partial output.** No half-built blueprint leaks downstream.
3. **The orchestrator's escalation routing is specified.** Four paths, named costs, audit trail, forbidden alternatives.
4. **Silent degradation is architecturally absent.** It is not "discouraged"; it has no execution path.
5. **The editor remains the structural decision-maker.** The framework converts an implicit quality erosion into an explicit authorial choice with an audit trail.

## Comparison to the cross-cultural success sample

| | `cross-cultural-scene-01` (success) | this sample (failure) |
|---|---|---|
| Compatibility check | passes (3/3 true) | fails (2/4 false) |
| Adapter emits adapted blueprint | yes | **no** (deliberately suppressed) |
| Downstream agents invoked | yes (dialogue, prose, validators) | **no** (pipeline halted at adapter) |
| Outcome | sibling canons produced | structured escalation surfaced |
| Editor required | no | **yes** (must pick path A/B/C/D) |
| Invariants modified | none | none (until editor authorizes path D) |

## Why path D is named — and why it is not the default

Path D (editor-authorized invariant downgrade) is offered because **sometimes the editor really does want to release an invariant**. A novelist working in a particular tradition may decide that, for the Japanese sibling specifically, the knowledge turn is acceptable as a symbol-fire turn — and they want to record that choice in writing.

What the framework refuses is path D being taken **silently**, **by default**, **without a justification text**, or **by any agent other than the editor**. Path D requires:

- explicit editor selection
- mandatory justification text
- timestamp + editor id
- `editor_authorized_divergence` flag carried through canonization

This converts what would otherwise be silent quality erosion into a named, accountable authorial act.

## Next sample (already planned)

- **Stereotype-bait sample** — [samples/stereotype-bait-01](../stereotype-bait-01) — drafts that deliberately import forbidden iconography. Validates that the Language Style Validator and Cultural Dialogue Specialist's `anti_stereotype_check` have real detection capability.

## Related

- [docs/culture/cultural-adaptation-rules.md](../../docs/culture/cultural-adaptation-rules.md)
- [docs/language/localization-vs-regeneration.md](../../docs/language/localization-vs-regeneration.md)
- [prompts/culture/cultural-adapter.prompt.md](../../prompts/culture/cultural-adapter.prompt.md) — section 7 "Failure Modes"
