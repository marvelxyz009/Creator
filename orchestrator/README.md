# AetherForge Orchestrator (Python MVP)

Minimal Python runner that executes the documented workflows from [/prompts/workflows/](../prompts/workflows/) against the documented samples in [/samples/](../samples/).

**Status:** skeleton committed; first runnable milestone is `python -m orchestrator run scene-generation --sample samples/mvp-scene-01`. See [the implementation plan](../docs/implementation/python-orchestrator-plan.md) for milestone breakdown.

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

# 5. Dry-run (plans the DAG, no LLM calls)
python -m orchestrator run scene-generation --sample samples/mvp-scene-01 --dry-run

# 6. Real run
python -m orchestrator run scene-generation --sample samples/mvp-scene-01
```

Each run writes its artifacts to `orchestrator/runs/<workflow-id>__<sample-name>__<timestamp>/`. The directory is gitignored (see [.gitignore](../.gitignore)) — run artifacts are reproducible from source and are not committed.

## CLI reference

```
python -m orchestrator run <workflow> --sample <path> [--dry-run] [--no-compare-golden]
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
pytest -ra
```

Tests are deliberately minimal at MVP:

| Test file | What it verifies |
|---|---|
| `test_artifact_io.py` | YAML/Markdown read+write; sample inputs parseable |
| `test_bundle.py` | Bundle assembly from a real sample; missing input raises |
| `test_prompt_render.py` | Jinja2 user-prompt hydration; YAML extraction from agent responses |
| `test_dag_order.py` | Topological order; cycle detection; dry-run; hard_reject halts |

The tests **do not** call the Anthropic API. LLM-touching tests would belong in an integration suite (out of MVP scope).

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
