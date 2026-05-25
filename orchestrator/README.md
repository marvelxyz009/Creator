# AetherForge Orchestrator (Python MVP)

Minimal Python runner that executes the documented workflows from [/prompts/workflows/](../prompts/workflows/) against the documented samples in [/samples/](../samples/).

**Status:** Milestone 1 implemented — Scene Director runs end-to-end against `samples/mvp-scene-01` using the real Anthropic API. Multi-agent DAG (Milestone 2+) is still under construction. See [the implementation plan](../docs/implementation/python-orchestrator-plan.md) for milestone breakdown.

## Quickstart

```bash
# 1. Create a Python 3.11+ virtual environment
python -m venv .venv
source .venv/bin/activate                # on Windows: .venv\Scripts\activate

# 2. Install
pip install -e ".[dev]"

# 3. Configure
cp .env.example .env
# Edit .env to add your ANTHROPIC_API_KEY.

# 4. Sanity-check the layout
python -m orchestrator inspect-sample --sample samples/mvp-scene-01

# 5. Run unit tests (no API key required)
pytest -ra

# 6. ⭐ Milestone 1: run the Scene Director agent end-to-end
python -m orchestrator run-agent scene-director --sample samples/mvp-scene-01

# 7. Run the integration test (LLM call; auto-skipped if no API key)
pytest orchestrator/tests/test_scene_director_integration.py -ra -s

# 8. (Milestone 2+) — full workflow, not yet stable
python -m orchestrator run scene-generation --sample samples/mvp-scene-01 --dry-run
```

### What Milestone 1 produces

A successful `run-agent scene-director` writes the following under
`samples/mvp-scene-01/generated/` (all gitignored):

```
samples/mvp-scene-01/generated/
├── 01-scene-blueprint.yaml             ← canonical generated output
└── debug/
    ├── hydrated-prompt.md              ← system + user prompts sent to Claude
    ├── raw-scene-director-response.md  ← exact Claude response (incl. retry, if any)
    ├── repair-prompt-1.md              ← only present if YAML extraction needed a retry
    └── extracted-yaml.yaml             ← the parsed YAML, prior to schema validation
```

These artifacts make it possible to fully reconstruct what was asked and what
was returned, run-over-run, without re-calling the API.

Full multi-agent runs (Milestone 2+) write to
`orchestrator/runs/<workflow-id>__<sample-name>__<timestamp>/` instead.

## CLI reference

```
python -m orchestrator run-agent scene-director --sample <path>      # Milestone 1
python -m orchestrator run <workflow> --sample <path> [--dry-run]    # Milestone 2+
python -m orchestrator list-workflows
python -m orchestrator inspect-sample --sample <path>
```

Global flag:
- `--log-level {DEBUG,INFO,WARNING,ERROR}` — overrides `AETHERFORGE_LOG_LEVEL`.

## Project layout

```
orchestrator/
├── __init__.py
├── __main__.py                 # python -m orchestrator entry
├── cli.py                      # argparse + dispatch
├── core/
│   ├── config.py               # env + path resolution
│   ├── artifact.py             # YAML/Markdown read+write
│   ├── bundle.py               # context bundle assembly (per agent contract)
│   └── runner.py               # DAG runner / state machine
├── llm/
│   ├── client.py               # Anthropic SDK wrapper
│   └── models.py               # agent → model registry
├── prompts/                    # LOADER CODE for prompt templates
│   ├── loader.py               # reads /prompts/agents/*.prompt.md
│   └── render.py               # Jinja2 user-prompt hydration + YAML extraction
├── graph/
│   ├── memory.py               # JSON-backed memory graph
│   └── schema.py               # node/edge type constants + symbol state machine
├── workflows/
│   ├── base.py                 # Workflow ABC
│   └── scene_generation.py     # MVP target
├── runs/                       # generated artifacts (gitignored)
└── tests/
    ├── test_artifact_io.py
    ├── test_bundle.py
    ├── test_prompt_render.py
    └── test_dag_order.py
```

## Repo-level files in scope

```
/pyproject.toml                                       # project metadata + entry point
/.env.example                                         # template — copy to .env
/.gitignore                                           # ignores .env, runs/, __pycache__/...
/docs/implementation/python-orchestrator-plan.md      # implementation plan
```

## Running the tests

```bash
# Unit tests — no API key required, run always
pytest -ra

# Integration test — calls Claude; auto-skips if ANTHROPIC_API_KEY is unset
pytest orchestrator/tests/test_scene_director_integration.py -ra -s
```

Tests are deliberately minimal at MVP:

| Test file | What it verifies | Requires API key? |
|---|---|---|
| `test_artifact_io.py` | YAML/Markdown read+write; sample inputs parseable | no |
| `test_bundle.py` | Bundle assembly from a real sample; missing input raises | no |
| `test_prompt_render.py` | Jinja2 user-prompt hydration; YAML extraction from agent responses | no |
| `test_dag_order.py` | Topological order; cycle detection; dry-run; hard_reject halts | no |
| `test_scene_director_integration.py` | Pure validator logic (always) + end-to-end LLM call (skip-without-key) | partial |

Unit tests have no network dependencies. The integration test auto-skips when
`ANTHROPIC_API_KEY` is unset, so CI without secrets stays green.

## Milestone 1 — Scene Director end-to-end (current state)

The single-agent integration path lives in
[`orchestrator/workflows/scene_director_only.py`](workflows/scene_director_only.py).
It implements:

1. **Load inputs** — via `BundleAssembler.assemble_for_scene_director()`.
2. **Hydrate prompts** — system = prompt template body verbatim; user = Jinja2 scaffold with bundle YAML embedded.
3. **Persist hydrated prompt** to `debug/hydrated-prompt.md` *before* the LLM call (so failures still leave a reproducible artifact).
4. **Call Anthropic** — model from `AGENT_MODEL_REGISTRY` (defaults to Opus 4.7).
5. **Persist raw response** to `debug/raw-scene-director-response.md`.
6. **Extract YAML** — first as a fenced block, then as a fallback whole-response parse.
7. **Retry once on extract failure** — sends a short repair prompt ("Convert the previous response into valid YAML only.") and re-parses.
8. **Validate schema** — checks all ten required fields under `scene_blueprint`. Empty fields (`None`, `""`, `[]`, `{}`) are rejected.
9. **Write canonical artifact** to `samples/<sample>/generated/01-scene-blueprint.yaml`.

The function emits structured log lines for each step:

```
step=bundle_loaded sample=mvp-scene-01 pinned_artifacts=6 rules=7
step=prompt_hydrated template=prompts/agents/scene-director.prompt.md system_chars=8521 user_chars=12305
step=llm_invoked model=claude-opus-4-7 input_tokens=4612 output_tokens=2204 stop_reason=end_turn
step=yaml_extracted success=true attempt=1 top_level_keys=['agent', 'agent_version', 'status', 'scene_blueprint']
step=schema_validated violations=0
step=artifact_written path=samples/mvp-scene-01/generated/01-scene-blueprint.yaml
```

Use `--log-level DEBUG` to see additional detail.

### Returned result

`run_scene_director()` returns a `SceneDirectorResult` with: `status`, `output`
(parsed YAML), `artifact_path`, `debug_dir`, `debug_paths`,
`validation_violations`, `attempt_count`, `input_tokens`, `output_tokens`,
`model`, `duration_seconds`, `agent_status` (the `status` field the agent
itself emitted), and `notes`.

`status == "ok"` only when all of: YAML parsed, schema validated, artifact
written. Anything else is `hard_reject` with `notes` explaining which step
failed.

## What this orchestrator is

- A direct implementation of the documented workflows.
- An exercise in keeping LLM-narrative code **debuggable** — explicit steps, structured artifacts, no framework magic.
- A golden-fixture runner: every sample under `/samples/` becomes a regression target.

## What this orchestrator is NOT (deliberate non-goals)

- **No multi-provider abstraction.** Anthropic only. The user pinned this; revisit when there's an actual second provider.
- **No graph database.** JSON files only. The user pinned this; inspectability beats query power at MVP scale.
- **No parallelism.** The DAG runner is sequential. Add concurrency only when an actual workflow needs it.
- **No UI, no frontend, no API server.** This is a CLI.
- **No caching, no streaming, no token-cost optimization at MVP.** Layer those when prompts stabilize.
- **No automated golden-diff strict-equality testing.** Prose drafts differ run-to-run by design (model temperature, sampling); the comparison is structural and informational.

## When you run into something not implemented

Many functions in the skeleton are intentional stubs or have minimal implementations marked `NotImplementedError` or `# TODO`. See [the implementation plan](../docs/implementation/python-orchestrator-plan.md) for the milestone order; pick up the next milestone's checklist.

## Related

- [docs/implementation/python-orchestrator-plan.md](../docs/implementation/python-orchestrator-plan.md) — the milestone plan
- [prompts/workflows/scene-generation-workflow.md](../prompts/workflows/scene-generation-workflow.md) — the workflow this MVP implements
- [samples/mvp-scene-01/](../samples/mvp-scene-01/) — the golden sample the MVP targets
