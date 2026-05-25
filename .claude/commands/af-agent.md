---
description: Run a single AetherForge agent through chat
---

You are about to act as ONE specific AetherForge agent. The user's command is:

```
/af-agent $ARGUMENTS
```

`$ARGUMENTS` should be an agent id (and optionally a sample path). Examples:
- `/af-agent scene-director`
- `/af-agent scene-director samples/mvp-scene-01`
- `/af-agent anti-ai-editor`

If `$ARGUMENTS` is empty, ask the user which agent. Valid agent ids:
- `scene-director`
- `symbolism-tracker`        (depends on scene-director output)
- `dialogue-specialist`      (depends on scene-director output)
- `anti-ai-editor`           (depends on scene-director + dialogue-specialist outputs)
- `continuity-auditor`       (depends on scene-director + anti-ai-editor outputs)

Default sample is `samples/mvp-scene-01` unless specified.

## What to do

1. **Sanity check**: if `.venv` doesn't exist, tell the user to run `/af-setup` first.

2. **Check prerequisites**: if the agent depends on prior agents, verify their canonical artifacts exist at `samples/<sample>/generated/`:
   - `scene-director`        → `01-scene-blueprint.yaml`
   - `dialogue-specialist`   → `03-dialogue-draft.yaml`
   - `anti-ai-editor`        → `04-anti-ai-report.yaml`
   
   If any required prior is missing, tell the user to either run `/af-create-scene` or `/af-agent <prior-id>` first.

3. **Hydrate the prompt** via Bash:
   ```
   python -m orchestrator prepare-agent <agent-id> --sample <sample-path>
   ```

4. **Read the hydrated prompt** with the Read tool:
   ```
   samples/<sample>/generated/manual/<agent-id>-prompt.md
   ```
   Find `--- BEGIN PROMPT ---`; everything below is the agent's role + task.

5. **Act as the agent**. Produce the YAML output following the agent's contract verbatim. Use ONLY information in the bundle; honor every anti-pattern and validation rule.

6. **Write the output** with the Write tool:
   ```
   samples/<sample>/generated/manual/<agent-id>-output.yaml
   ```
   Wrap your YAML in a ` ```yaml ... ``` ` fenced block.

7. **Validate** via Bash:
   ```
   python -m orchestrator validate-agent-output <agent-id> --sample <sample> --input samples/<sample>/generated/manual/<agent-id>-output.yaml
   ```

8. **Report** to the user:
   - On `✓ ok`: tell them the canonical artifact path. If the agent is `anti-ai-editor`, also call out that `samples/<sample>/generated/05-revised-draft.md` now contains the prose.
   - On `✗ hard_reject`: list the violations the orchestrator reported. Offer to retry (1 attempt) or escalate to the user.

## Retry on validation failure

If validation fails, you have ONE retry. Either:
- Edit the YAML file directly to fix the named violations
- Regenerate the agent output from scratch with the violations as feedback

If the retry also fails, stop and ask the user how to proceed.

## Important

- Do NOT skip the validate step.
- Do NOT modify files under `samples/<sample>/inputs/` or `samples/<sample>/outputs/`.
- If `$ARGUMENTS` contains an unknown agent id, list the valid ones and stop.
- Honor the agent contract verbatim — anti-patterns, refusals, voice signatures.
