---
description: Generate a complete narrative scene end-to-end through chat (no API key)
---

You are about to drive the AetherForge Creator Framework's full scene-generation workflow through chat. You will play the role of all 5 agents in sequence, with the Python orchestrator handling bundle assembly, prompt hydration, schema validation, and artifact writing.

## Setup check

If `.venv` does not exist at the repo root, tell the user to run `/af-setup` first and stop. Otherwise continue.

## What you will do

For each of these 5 agents in order:

1. **scene-director** — produces the scene blueprint (structural design)
2. **symbolism-tracker** — audits symbol state-machine legality
3. **dialogue-specialist** — drafts voice-specific dialogue
4. **anti-ai-editor** — smell scrub + humanization → produces the prose
5. **continuity-auditor** — validates against memory graph

### Per-agent loop

For each agent:

#### Step A — Ask the orchestrator to prepare the prompt

Run via Bash:
```
python -m orchestrator prepare-agent <agent-id> --sample <sample-path>
```

Default `<sample-path>` is `samples/mvp-scene-01` unless the user has specified another. Confirm with the user once at the start.

#### Step B — Read the hydrated prompt

Use the Read tool to read:
```
samples/<sample>/generated/manual/<agent-id>-prompt.md
```

The file has a `--- BEGIN PROMPT ---` marker. Everything below that line is the actual agent prompt. The section ABOVE is operator instructions you can ignore for the LLM work.

#### Step C — Act as the agent

Following the AGENT ROLE (system prompt) and TASK (user prompt) sections, produce the agent's required output. The "Required output" section at the bottom of the file lists which top-level YAML keys are required.

Honor:
- The agent's contract verbatim — including anti-patterns and validation checklist
- All narrative laws from `prompts/shared/global-narrative-rules.md`
- Use ONLY information in the bundle YAML; do not invent or hallucinate
- Output a single YAML document, no prose outside the fenced block

#### Step D — Write the output

Use the Write tool to write your YAML response to:
```
samples/<sample>/generated/manual/<agent-id>-output.yaml
```

Wrap the YAML in a fenced ` ```yaml ... ``` ` block. The orchestrator's extractor handles both fenced blocks and bare YAML.

#### Step E — Validate

Run via Bash:
```
python -m orchestrator validate-agent-output <agent-id> --sample <sample> --input samples/<sample>/generated/manual/<agent-id>-output.yaml
```

If it returns `✓ ok`, continue to the next agent.

If it returns `✗ hard_reject` with validation violations, you have three options:
1. **Fix in place** — Edit the YAML output file directly to address the violations, then re-run validate.
2. **Regenerate** — Act as the agent again with the violations as feedback, write a fresh output, then re-run validate.
3. **Escalate to user** — If the issue is genuinely ambiguous, ask the user how to proceed.

Cap retries at 2 per agent. If still failing after 2 retries, stop and explain to the user.

## After all 5 agents succeed

1. Read the final prose:
   ```
   samples/<sample>/generated/05-revised-draft.md
   ```

2. Present it to the user as the generated scene — render the prose in your reply as a fenced block so they can copy it. Cite the path.

3. List the canonical artifacts that were written (under `samples/<sample>/generated/`):
   ```
   01-scene-blueprint.yaml
   02-symbol-audit.yaml
   03-dialogue-draft.yaml
   04-anti-ai-report.yaml
   05-revised-draft.md          ← THE STORY
   06-continuity-report.yaml
   ```

4. Optionally suggest the user compare against the golden in `samples/<sample>/outputs/` (hand-authored reference).

## Important

- DO NOT modify files under `samples/<sample>/inputs/` — those are the fixed starting conditions.
- DO NOT modify files under `samples/<sample>/outputs/` — those are golden references.
- DO NOT skip the validate step — it's the framework's quality gate.
- DO NOT generate prose anywhere except via the anti-ai-editor's `humanization_pass.revised_draft` field.
- Respect the agent contracts; do not blend agents or skip steps.

## Default sample

If the user does not specify, use `samples/mvp-scene-01` — it's the canonical MVP sample with hand-authored golden outputs you can compare against.
