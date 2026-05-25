# Manual Agent Workflow

The default operational mode for the AetherForge orchestrator. **No Anthropic API key required.** The orchestrator handles file I/O, bundle assembly, prompt hydration, and output validation. The LLM call itself happens inside your IDE — typically the Claude extension in VSCode or Cursor.

## Why this mode exists

Most contributors to AetherForge work inside an IDE with Claude already integrated. They have a chat with Claude running while editing files; they do not maintain a separate Anthropic API account or pay per-call from an API key.

The framework's design — repo-based docs, prompts, schemas, and samples — is well-suited to this workflow. Claude in the IDE can already read every file in the repo. The orchestrator's job is therefore narrower than it would be with an API-only design: assemble the right context bundle, hydrate the right prompt, and validate what comes back.

This mirrors the [BMAD pattern](https://github.com/bmadcode/BMAD-METHOD): structured, prompt-driven AI work where the "agent" lives in your editor and the supporting infrastructure lives in version control.

## How it differs from API Mode

| | Manual Agent Mode | API Agent Mode |
|---|---|---|
| Where the LLM runs | Claude extension in your IDE | Anthropic API endpoint |
| Requires `ANTHROPIC_API_KEY` | No | Yes |
| LLM call mediated by | The human (copy-paste) | `orchestrator.llm.client` |
| Cost | Covered by your IDE's Claude plan | Per-token billing on your Anthropic key |
| Best for | Day-to-day authoring, iterative tuning, contributors without API access | Batch runs, CI, headless automation |
| Default? | **Yes** | Optional |
| Implementation | [`orchestrator/workflows/scene_director_manual.py`](../../orchestrator/workflows/scene_director_manual.py) | [`orchestrator/workflows/scene_director_only.py`](../../orchestrator/workflows/scene_director_only.py) |

Both modes share: bundle assembly, prompt loading, Jinja2 hydration, YAML extraction, schema validation, canonical artifact writing. The only divergence is *how* the LLM is invoked.

## Using it with the Claude extension in VSCode/Cursor

The end-to-end flow:

### a. Prepare the prompt

```bash
python -m orchestrator prepare-agent scene-director --sample samples/mvp-scene-01
```

The orchestrator:
- Loads inputs from `samples/mvp-scene-01/inputs/`
- Assembles the Scene Director's bundle (theme + world + characters + plot beat + memory graph excerpt)
- Loads `prompts/agents/scene-director.prompt.md`
- Hydrates the user-prompt scaffold with Jinja2 (embeds the bundle YAML)
- Writes a copy-paste-ready Markdown file:

```
samples/mvp-scene-01/generated/manual/scene-director-prompt.md
```

### b. Copy the prompt into Claude

Open the manual prompt file in your editor. Below the line `--- BEGIN PROMPT ---` is the content you give to Claude. Copy that entire section.

Open the Claude extension's chat panel in VSCode/Cursor. Start a fresh conversation. Paste the prompt as a single message.

### c. Ask Claude to follow the prompt and output YAML only

The prompt itself instructs Claude to "Emit a single YAML document wrapped in a ```yaml ... ``` fenced block. Do not write any prose before or after." This is usually enough.

If Claude includes a preamble or trailing prose anyway, that's fine — the validator in step **e.** extracts the YAML from the fenced block regardless.

### d. Save Claude's response

Save Claude's response — the full response, including any prose — to:

```
samples/mvp-scene-01/generated/manual/scene-director-output.yaml
```

`.yaml` and `.md` extensions are both fine. The validator handles either.

### e. Validate the output

```bash
python -m orchestrator validate-agent-output scene-director \
  --sample samples/mvp-scene-01 \
  --input samples/mvp-scene-01/generated/manual/scene-director-output.yaml
```

The orchestrator:
- Reads the file
- Extracts the YAML block (or parses the whole file as YAML if there's no fence)
- Validates the schema (all 10 required `scene_blueprint` fields present and non-empty)
- On success: writes the canonical artifact to `samples/mvp-scene-01/generated/01-scene-blueprint.yaml`
- On failure: prints a structured list of violations

### f. Commit the artifact (optional)

The canonical artifact lives under `samples/<sample>/generated/`, which is gitignored by default. You can compare it manually to the golden in `samples/<sample>/outputs/`, or commit it as a sibling alternative if you're building a new sample's golden set.

If you ARE building a new golden — copy the canonical to `outputs/`:

```bash
cp samples/mvp-scene-01/generated/01-scene-blueprint.yaml \
   samples/mvp-scene-01/outputs/01-scene-blueprint.yaml
git add samples/mvp-scene-01/outputs/01-scene-blueprint.yaml
git commit -m "Update golden scene blueprint"
```

For the existing MVP sample the golden was hand-authored as part of [the original sample committed earlier](../../samples/mvp-scene-01/outputs/01-scene-blueprint.yaml), and is not typically overwritten by a manual run.

## What happens on validation failure

If validation fails the orchestrator prints something like:

```
✗ validate-agent-output scene-director
  status              : hard_reject
  agent self-status   : ok
  duration            : 0.04s
  input               : samples/mvp-scene-01/generated/manual/scene-director-output.yaml
  validation violations: 3
    - scene_blueprint.symbolism_used is missing
    - scene_blueprint.hidden_information is empty
    - scene_blueprint.ending_hook is missing
```

You have three options:

1. **Edit the output file** directly to add the missing fields. Quick if the omission is small.
2. **Re-prompt Claude** in the same conversation with: *"Your previous output is missing `symbolism_used`, `hidden_information`, and `ending_hook`. Please regenerate the full YAML with these fields populated."*
3. **Re-run `prepare-agent`** to get a fresh prompt, start a new Claude conversation. Useful if the original conversation has drifted off-context.

Re-run `validate-agent-output` after each fix attempt.

## What gets written where

```
samples/<sample>/
├── inputs/                     ← read by the orchestrator
└── generated/                  ← all artifacts the orchestrator writes (gitignored)
    ├── 01-scene-blueprint.yaml ← canonical (written on successful validation)
    └── manual/
        ├── scene-director-prompt.md     ← written by prepare-agent
        └── scene-director-output.yaml   ← you save Claude's reply here
```

Nothing under `generated/` is committed by default. Everything is reproducible from `inputs/` + the prompt templates + an LLM session.

## When to use API mode instead

Reasons to switch to `run-agent scene-director`:

- **Batch validation across many samples** — manual copy-paste doesn't scale.
- **CI / automation** — a pipeline cannot click in an IDE.
- **Reproducibility audits** — API mode with `temperature=0` and a fixed model produces more stable outputs than IDE chat sessions.
- **No IDE access** — running on a server, in a container, or in a CI runner.

For everything else, manual mode is the recommended default.

## What stays the same between modes

The agent contract is identical. The bundle is identical. The prompt template is identical. The schema validator is identical. The canonical artifact format is identical. **The only difference is who carries the message between the orchestrator and Claude.**

This means a sample that passes in manual mode will (modulo LLM stochasticity) pass in API mode too, and vice versa. The two modes are interchangeable transports for the same content.

## Related

- [orchestrator README](../../orchestrator/README.md)
- [python-orchestrator-plan.md](./python-orchestrator-plan.md) — overall plan
- [prompts/agents/scene-director.prompt.md](../../prompts/agents/scene-director.prompt.md) — the agent contract
- [samples/mvp-scene-01/](../../samples/mvp-scene-01/) — the MVP sample
