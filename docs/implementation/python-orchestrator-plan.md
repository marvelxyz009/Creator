# Python Orchestrator — Implementation Plan

The plan for shipping the AetherForge MVP orchestrator. Pinned implementation decisions:

- **Runtime:** Python 3.11+
- **LLM API:** Anthropic SDK only (no multi-provider abstraction)
- **Memory graph:** JSON files, repo-friendly
- **Orchestrator pattern:** hand-rolled DAG / state machine
- **Prompt hydration:** Jinja2 (user-prompt scaffold only; templates passed through verbatim as system prompts)
- **First runnable milestone:** `python -m orchestrator run scene-generation --sample samples/mvp-scene-01`

This document is the **build plan**, not the final architecture. The skeleton is committed; remaining work is the milestone checklist.

## Project layout (now committed)

```
/pyproject.toml                  ← project metadata + CLI entry point
/.env.example                    ← copy to .env, fill ANTHROPIC_API_KEY
/.gitignore                      ← ignores .env, __pycache__, runs/
/orchestrator/
  ├── __init__.py
  ├── __main__.py                ← python -m orchestrator
  ├── cli.py                     ← argparse + dispatch (run / list-workflows / inspect-sample)
  ├── README.md                  ← quickstart + project layout
  ├── core/
  │   ├── config.py              ← env + path resolution (load_config())
  │   ├── artifact.py            ← read_yaml / write_yaml / read_markdown / write_markdown
  │   ├── bundle.py              ← Bundle dataclass + BundleAssembler
  │   └── runner.py              ← Step, StepResult, RunReport, WorkflowRunner
  ├── llm/
  │   ├── client.py              ← LLMClient (Anthropic SDK wrapper)
  │   └── models.py              ← AGENT_MODEL_REGISTRY + model_for_agent()
  ├── prompts/
  │   ├── loader.py              ← PromptLoader (reads /prompts/agents/*.prompt.md)
  │   └── render.py              ← render_user_prompt / render_system_prompt / extract_yaml_from_response
  ├── graph/
  │   ├── memory.py              ← MemoryGraph (JSON-backed; from_excerpt / save / queries)
  │   └── schema.py              ← node/edge type constants + symbol state machine
  ├── workflows/
  │   ├── base.py                ← Workflow ABC (run / _make_run_dir / compare_to_golden)
  │   └── scene_generation.py    ← SceneGenerationWorkflow (the MVP target)
  ├── runs/.gitkeep
  └── tests/
      ├── test_artifact_io.py
      ├── test_bundle.py
      ├── test_prompt_render.py
      └── test_dag_order.py
/docs/implementation/python-orchestrator-plan.md   ← THIS FILE
```

## Dependencies (pinned in pyproject.toml)

| Dep | Purpose | Rationale |
|---|---|---|
| `anthropic` | LLM client | Official SDK; required by spec |
| `jinja2` | User-prompt hydration | Required by spec |
| `pyyaml` | YAML read/write | All artifacts are YAML/Markdown |
| `python-dotenv` | .env loading | Avoids handcrafting env parsing |
| `pytest` (dev) | Test runner | Standard |
| `pytest-cov` (dev) | Coverage reporting | Optional but cheap |
| `ruff` (dev) | Linter | Fast; minimal config |

**Not used (deliberately):**
- No LangChain / LangGraph / CrewAI / AutoGen — the user pinned hand-rolled DAG.
- No Pydantic — dataclasses are sufficient for MVP; revisit if validation becomes painful.
- No SQLAlchemy / SQLite — JSON files only.
- No async / aiohttp — sequential DAG; revisit if parallelism matters.
- No Click / Typer — argparse is enough.

## The DAG model

A workflow is a list of **`Step`** objects. Each `Step` has:

- `id` (string, used in `depends_on` references)
- `description`
- `depends_on` (list of other step ids)
- `fn` (a callable taking `(runner, prior_results)` returning a `StepResult`)
- `optional` (bool — if True, `hard_reject` does not halt the workflow)

The runner:

1. Topologically sorts steps (raises on cycle or unknown dep).
2. Executes in order.
3. After each step, inspects `status`. `ok | soft_reject` continues. `hard_reject | escalate` halts (unless step is optional).
4. Records every step's result + duration into a `RunReport`.
5. Writes `run-report.yaml` to the run dir.

**No parallelism for MVP.** All steps run sequentially. The DAG model leaves room for parallel siblings later, but the runner does not yet support it.

## The agent-invocation contract

Every step that calls an agent does the same four things:

```
template = loader.load(agent_id)                 # /prompts/agents/<agent_id>.prompt.md
bundle   = assembler.assemble_for_<agent>(...)   # the tailored context
user_p   = render_user_prompt(bundle)            # Jinja2-rendered scaffold
sys_p    = render_system_prompt(template.body)   # the .prompt.md body, verbatim
response = llm.call(system=sys_p, user=user_p, model=model_for_agent(agent_id))
parsed   = extract_yaml_from_response(response.text)
artifact.write_yaml(output_path, parsed)
```

This is implemented as `SceneGenerationWorkflow._run_agent()`. When this pattern stabilizes across multiple workflows, factor it into a generic `AgentStep` wrapper.

### Why Jinja2 is not applied to the prompt template body

The agent prompt templates in `/prompts/` contain literal `{{ ... }}` examples in their YAML output sections. Running Jinja2 over the template body would substitute these. So the **system prompt is passed through verbatim**, and Jinja2 is applied only to the small user-prompt scaffold that embeds the bundle. This trades a little flexibility for not having to escape `{{` everywhere in the templates.

### Output parsing

The user prompt asks for a single ```yaml ... ``` fenced block. `extract_yaml_from_response`:

1. Tries to find a fenced YAML block by regex. If found, parses it.
2. Falls back to parsing the entire response as YAML.
3. Returns the parsed dict, or `None` if both attempts fail.
4. On `None`, the calling step records `status: hard_reject` and persists the raw response for forensics.

## Memory graph data model

A `MemoryGraph` is a JSON file with three top-level keys:

```json
{
  "nodes": {
    "char:mira":         { "type": "character", "data": { ... } },
    "sym:cracked-glass": { "type": "symbol",    "data": { "id": "sym:cracked-glass", "state": "transformed" } },
    ...
  },
  "edges": [
    { "type": "KNOWS",     "subject": "char:mira", "object": "event:edit-disclosure", "level": "full" },
    { "type": "OWES",      "from": "char:tomas",   "to": "char:mira", "debt": "debt:0001" },
    ...
  ],
  "metadata": {
    "schema_version": "0.1",
    "last_updated_at": "..."
  }
}
```

`MemoryGraph.from_excerpt()` converts a sample's `memory_graph_excerpt.yaml` (nested-by-category) into this flat representation. `save()` writes it back to disk with sorted keys-off so write order is meaningful.

Sample-input excerpts (`samples/*/inputs/memory_graph_excerpt.yaml`) are the **read-only starting state** for an MVP run. The runner mutates an in-memory copy; canonical graph commits happen later when chapter-level canonization is implemented.

## Configuration

`Config` is a frozen dataclass built by `load_config()`. It resolves:

- `repo_root` — found by walking up from `__file__` looking for `pyproject.toml`
- `prompts_dir`, `schema_dir`, `samples_dir`, `runs_dir`, `docs_dir`
- `anthropic_api_key`, `anthropic_model`, `anthropic_max_tokens`
- `log_level`

All env-var lookups happen exactly here. Other modules import `Config`, not `os.environ`.

## Testing strategy

Tests are intentionally minimal for MVP. The test pyramid:

| Level | Tests | What's covered |
|---|---|---|
| Unit | `test_artifact_io.py`, `test_prompt_render.py`, `test_dag_order.py` | Pure functions; no LLM calls |
| Integration (with sample fixtures) | `test_bundle.py` | Bundle assembly against real `samples/mvp-scene-01/inputs/` |
| End-to-end (against LLM) | not in this milestone | Will run the actual scene-generation workflow and compare structurally to goldens |

Run with:
```bash
pytest -ra
```

The four committed test files cover:
- **Loading inputs** — `test_artifact_io.py::test_sample_mvp_inputs_parseable`, `test_bundle.py::test_bundle_assembler_for_scene_director`
- **Prompt hydration** — `test_prompt_render.py` (all tests)
- **DAG execution order** — `test_dag_order.py` (topological order, cycle detection, dry-run, hard-reject halt, optional-step continuation)
- **Output writing** — `test_artifact_io.py::test_write_then_read_yaml`, `test_write_then_read_markdown`

These map 1:1 to the user's stated test requirements.

## Milestones

### Milestone 0 — Skeleton (DONE in this commit)
- pyproject.toml, .env.example, .gitignore
- Full `orchestrator/` package layout
- All module skeletons with type-hinted signatures + docstrings
- Substantive implementations for: `config`, `artifact`, `runner`, `loader`, `render`, `models`, `schema`, `memory`, `bundle` (per-agent assemblers for the 5 scene-generation agents)
- Workflow base class + `SceneGenerationWorkflow` (DAG + per-agent step functions wired)
- 4 test files with passing tests on the trivial path
- README + this implementation plan

After Milestone 0: `python -m orchestrator inspect-sample --sample samples/mvp-scene-01` works. Tests pass on a machine with no `ANTHROPIC_API_KEY`. The orchestrator does NOT call the LLM yet.

### Milestone 1 — Single agent call working end-to-end

**Goal:** `python -m orchestrator run scene-generation --sample samples/mvp-scene-01 --dry-run` plans the DAG. With an API key set, a non-dry-run executes the scene-director step alone and writes `01-scene-blueprint.yaml`.

Tasks:
1. Verify `LLMClient.call()` against a trivial prompt manually.
2. Iterate on the user-prompt scaffold in `prompts/render.py` until scene-director returns parseable YAML reliably.
3. Confirm `extract_yaml_from_response` survives Opus 4.7's actual response formatting (may need to handle ``` blocks with language modifiers, indentation, etc).
4. Confirm `01-scene-blueprint.yaml` writes correctly.
5. Add an integration smoke test that requires `ANTHROPIC_API_KEY` (skip if missing) — single agent call, parseable output, file written.

### Milestone 2 — Full scene-generation DAG

**Goal:** All five steps (`scene-director` → `symbolism-tracker` → `dialogue-specialist` → `anti-ai-editor` → `continuity-auditor`) execute in sequence. Each step's output becomes input to the next where the DAG declares it.

Tasks:
1. Wire each agent's `_run_agent` invocation correctly (already in `scene_generation.py` — debug as needed).
2. Handle the `anti-ai-editor`'s special output (markdown body inside YAML structure — `humanization_pass.revised_draft`).
3. Validate that `continuity-auditor` receives a draft string consistent with its prompt's `draft_under_audit` input contract.
4. Verify the run report includes per-step durations, token counts, statuses, artifact paths.
5. Run against `samples/mvp-scene-01` and confirm a non-empty run dir.

### Milestone 3 — Golden comparison

**Goal:** `--compare-golden` produces a structural diff between generated artifacts and committed sample `outputs/`. Comparison is **informational** (does not fail the run).

Tasks:
1. For each agent's output, compare top-level YAML keys to the golden.
2. Compare `status` field exact match.
3. Compare key-presence in nested sections (e.g. `scene_blueprint.turn`, `scene_blueprint.residue.graph_writes`).
4. Do NOT compare prose text content; do NOT compare ordering of list items.
5. Write `golden-comparison.yaml` into the run dir summarizing matches/misses.
6. Surface match rate in the run report's `notes`.

### Milestone 4 — Memory-graph integration

**Goal:** The orchestrator loads the sample's `memory_graph_excerpt.yaml` into a `MemoryGraph`, passes it to agents that need it, applies declared `residue.graph_writes` after each scene's canonization, and writes the post-run graph to the run dir.

Tasks:
1. `MemoryGraph.from_excerpt()` already implemented — verify against `samples/mvp-scene-01/inputs/memory_graph_excerpt.yaml`.
2. Each step that emits `residue.graph_writes` parses and applies them to the in-memory graph.
3. Symbol state transitions validated against `is_legal_symbol_transition()`.
4. After successful canonization, write the updated graph to `<run_dir>/memory-graph.post.json`.

### Milestone 5 — Soft-reject and revision loop

**Goal:** When `anti-ai-editor` returns `soft_reject`, the orchestrator re-runs it with a `revision_directive` up to N times.

Tasks:
1. Detect `status: soft_reject` on `anti-ai-editor` result.
2. Build a revision directive from the smell report (line refs + diagnostic).
3. Re-invoke with `bundle.revision_directive` set.
4. Cap at N=3 cycles; on persistent failure escalate.

### Milestone 6 — Polish + docs

- Better error messages on missing env var, missing prompt template, malformed sample.
- Logging volume tuning — DEBUG should be useful, INFO should be brief.
- Update README with a real example output snippet from a successful run.
- Optional: add a `replay` subcommand to re-run a previous run's prompts against the LLM without re-assembling bundles.

## Non-goals (explicit)

- **No multi-provider abstraction.** Single-purpose Anthropic SDK wrapper. If a second provider is ever added, the abstraction emerges from the second use case, not from speculation.
- **No graph DB.** JSON files. The repo-versioning gains outweigh the query gains at this scale.
- **No async / parallel DAG execution.** The validators *could* run in parallel (they are adversarially isolated by design) — but at MVP scale the sequential clarity wins. Revisit when an actual workflow blocks on it.
- **No streaming.** No partial-output handling. Full responses only.
- **No prompt caching.** Worth revisiting in Milestone 5+ when system prompts stabilize.
- **No web UI, no API server, no frontend.** Pinned by spec.
- **No automated strict-equality golden tests.** Prose generation is stochastic; strict diffs are noise.
- **No model fine-tuning.** Not the framework's bet.

## Risk register

| Risk | Mitigation |
|---|---|
| LLM returns prose that wraps the YAML block awkwardly | `extract_yaml_from_response` already handles unfenced + fenced; expand cases as observed |
| Long prompt templates exceed model context | Per-agent `budget_tokens` in Bundle; system prompt size monitored; templates already chunked into agent/shared/workflow files |
| Prose drafts vary wildly run-to-run | Goldens compared structurally, not by content. This is *the design*, not a defect |
| API key absent in CI | Tests skip LLM-touching cases via `pytest.skip` when `ANTHROPIC_API_KEY` is unset |
| Agent emits `escalate` and the runner does not know what to do | Captured in `StepResult.status`; runner halts; the editor (human) handles. No silent fallback (see invariant-violation-01 sample for the contract) |
| Cycle introduced in a workflow DAG | `WorkflowRunner.topological_order` raises on cycle; covered by `test_dag_order.py::test_topological_order_detects_cycle` |
| Sample inputs malformed | `BundleAssembler` raises `FileNotFoundError` early; CLI's `inspect-sample` helps debug |

## How to extend

When adding a new workflow:
1. Create `orchestrator/workflows/<name>.py` subclassing `Workflow`.
2. Implement `build_steps()` returning a list of `Step`s, each with a closure for `fn`.
3. Implement `compare_to_golden()` — usually a few key-presence checks.
4. Add `<workflow-id>` to the `argparse` choices in `cli.py`.
5. Add an integration smoke test under `orchestrator/tests/`.

When adding a new agent:
1. Add `/prompts/agents/<agent-id>.prompt.md` or `/prompts/culture/<agent-id>.prompt.md`.
2. Add an entry in `AGENT_MODEL_REGISTRY` (orchestrator/llm/models.py).
3. Add an `assemble_for_<agent>()` method to `BundleAssembler` for this agent's inputs.
4. Wire it into whichever workflows need it.

## Open questions to revisit

- **Output-format detection.** Currently the workflow hard-codes `output_format: "yaml"` per step. Some agents (Prose Agent eventually) emit Markdown. The cleanest fix is a `expected_output_format` field on the prompt template's frontmatter — but we are not parsing frontmatter yet.
- **Bundle assembly automation.** Currently `BundleAssembler` has one method per agent. A clean version would parse the prompt template's "Inputs (required)" section and assemble automatically. Defer until the per-agent variation stabilizes.
- **Symbol state machine enforcement.** `graph/schema.is_legal_symbol_transition` is implemented but not yet called by any agent step. Wire it into the symbolism-tracker step in Milestone 4.

## Related

- [orchestrator README](../../orchestrator/README.md)
- [prompts/workflows/scene-generation-workflow.md](../../prompts/workflows/scene-generation-workflow.md)
- [samples/mvp-scene-01/](../../samples/mvp-scene-01/) — the MVP target sample
