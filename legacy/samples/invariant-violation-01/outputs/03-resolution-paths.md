# Resolution Paths — Editor's Briefing

> This document is what the editor reads when the orchestrator pauses on an escalation. It is **deliberately not auto-summarized**: the editor reads structured frictions and chooses a path. The orchestrator does not pre-pick.

## What happened

The Cultural Adapter detected that the target culture profile (`culture:high-restraint-scholarly`) **cannot** serve the structural invariants of scene `scene:01` (the MVP Mira/Tomas confrontation).

The incompatibility is not a surface problem. It is a **complement set** problem: the channels the scene requires (body_somatic for the lighter firing; some directness gradient for the qualified confirmation; a domestic-object palette for the cracked symbol) are precisely the channels the profile forbids.

The adapter **did not emit a partial blueprint**. It halted, named the frictions, and surfaced four paths.

## The four paths, plainly

### Path A — Drop this sibling at this scene

> *"This profile and this scene are incompatible. We accept that."*

The sibling tree for `culture:high-restraint-scholarly` simply does not contain `scene:01`. Chapter plans for this sibling are marked: this scene is missing.

**Use when:** the editor wants to demonstrate that some scenes are not regenerable under some profiles, and is comfortable with sibling-canon non-uniformity.

**Cost:** one fewer sibling canon for this scene. The other siblings (baseline, JP, VN) still produce normally.

**Invariants:** preserved. No mutation. No degradation.

---

### Path B — Modify the culture profile

> *"Maybe the profile was over-constrained. Let's adjust it."*

The editor relaxes one or more profile fields. For example:
- raise `conflict_style.accusation_staging` from `refused` to `implied`;
- permit `body_somatic` as a channel for at least one emotion;
- extend `symbolism_preferences.available_loads` to include `domestic_object_use_wear`.

**Use when:** the profile was designed too tightly and the editor accepts that the loosening is the right artistic call.

**Cost:** every other scene already canonized under this profile must be **re-validated** against the loosened profile. This is expensive. The orchestrator will queue re-audits.

**Invariants:** preserved.

---

### Path C — Re-open Plot Engineer for a sibling-specific scene

> *"This sibling diverges here. Let it diverge structurally — a different scene serving the same theme beats."*

The Plot Engineer is asked to produce a sibling-specific scene that touches `[beat:t1, beat:t2, beat:t3]` and resolves an information beat — but in a form this profile can serve. For instance: a document-only scene in which Mira examines a redacted form and Tomas is physically absent; the qualified confirmation arrives via document annotation; no lighter, no body-knowledge — but a different body-of-knowledge moment (perhaps her fingers know the annotation's handwriting).

**Use when:** the editor wants the sibling to genuinely exist and is willing to treat it as a meaningfully different work that shares only the theme tree.

**Cost:** highest authorial cost. The sibling tree diverges from this scene forward. Subsequent scenes may also need to be sibling-specific.

**Invariants:** preserved (different scene, same theme tree, same character contradictions).

This is the **most honest** path. It is also the most labor.

---

### Path D — Editor authorizes invariant downgrade

> *"For this sibling only, the knowledge turn becomes a symbol-fire turn. The qualified confirmation does not arrive. The scene exists, but it is structurally lighter."*

The editor explicitly declares that, **for this sibling at this scene**, an invariant is being released. The release is recorded with editor id, timestamp, and a mandatory justification text.

**Use when:** the editor wants this sibling to exist at this scene and accepts that it is, by their conscious decision, a divergent realization.

**Cost:** the sibling carries a flag — `editor_authorized_divergence` — through canonization. It is *not* a silent mutation; it is a *declared* one.

**Invariants:** **declared divergence**, not preserved. This is the only path that loosens the invariant set, and it does so under named editorial responsibility.

---

## What is NOT a path

The orchestrator will **not** offer:

- Silent downgrade of the turn type.
- Silent swap of body_somatic to a different channel.
- "Approximate" adapter output emitted with a warning suppressed.
- Auto-retry under relaxed compatibility.
- A "best-effort" fallback to baseline (English-psychological) prose.

These options are **architecturally absent**. They are the failure modes the framework was built to refuse.

## Why this matters

A naïve cross-cultural pipeline takes path D silently every time, with no audit trail. The reader gets a "Japanese version" that is, structurally, a translation of the English version with surface decoration. The framework's stance is that this is dishonest production.

By forcing the editor to **pick** between A, B, C, and D — and by recording the pick — AetherForge converts a silent quality erosion into an explicit authorial decision. This is the entire point of regeneration as opposed to localization.

## What this sample proves

- The Cultural Adapter has **real teeth** — it detects compatibility frictions and refuses to emit a partial blueprint.
- The orchestrator's escalation routing is **structurally specified** (see `02-orchestrator-routing-decision.yaml`) — the architecture forbids silent fallback.
- The editor is given **structured choice**, not vibes — each path has a named cost and a named invariant integrity status.
- The framework treats "this regeneration is impossible" as a **first-class outcome**, not an error to suppress.

## Related

- [Cultural Adapter escalation report](./01-cultural-adapter-escalation.yaml)
- [Orchestrator routing decision spec](./02-orchestrator-routing-decision.yaml)
- [docs/culture/cultural-adaptation-rules.md](../../../docs/culture/cultural-adaptation-rules.md)
- [docs/language/localization-vs-regeneration.md](../../../docs/language/localization-vs-regeneration.md)
