# AetherForge Creator Framework

A multi-agent framework for producing literary narrative through structured prompts, schemas, and validation — designed to resist the statistical regression to mean known as "AI smell." Inspired by [BMAD-METHOD](https://github.com/bmadcode/BMAD-METHOD)'s approach: repo-based docs, prompts, workflows; AI agents do the work inside your IDE; the framework provides validation and orchestration.

**Default operational mode is manual:** no Anthropic API key required. The framework hydrates prompts; you paste them into Claude (in VSCode/Cursor extension or any LLM chat); the framework validates the response and writes canonical artifacts.

---

## 🚀 Quickstart

### One-time setup

```bash
git clone <this-repo>
cd Creator
python scripts/setup.py
```

Or on Windows:
```cmd
setup.bat
```

Or on Mac/Linux with `make`:
```bash
make setup
```

The setup script:
1. Verifies Python 3.11+
2. Creates `.venv/`
3. Installs dependencies (anthropic, jinja2, pyyaml, dotenv, pytest)
4. Copies `.env.example` to `.env` (only needed for optional API mode)
5. Verifies the orchestrator imports cleanly

It's idempotent — safe to re-run.

### Activate the venv

**Windows:**
```cmd
.venv\Scripts\activate
```

**Mac/Linux:**
```bash
source .venv/bin/activate
```

### Generate your first story (recommended)

In a Claude Code chat session opened in this repo:

```
/af-start
```

Claude will:
1. Ask you to paste your story idea (1-5 sentences — anything you have).
2. Ask ~8 guided questions with **multiple-choice answers** (A / B / C / D / "tell me yours").
3. Auto-generate all the input YAML files into `samples/<your-project>/inputs/`.
4. Run the full 5-agent pipeline automatically.
5. Print the finished scene to you.

You read the story at the end. No YAML editing, no per-agent copy-paste, no API key. One command, then a conversation.

### Alternatives

**Run the canonical MVP sample** (inputs already prepared, just to see the pipeline work):
```bash
python -m orchestrator create-scene --sample samples/mvp-scene-01
```
Or in chat: `/af-create-scene`

**Per-agent control** (after a project's inputs already exist):
```
/af-agent scene-director
/af-agent anti-ai-editor
```

All paths produce the same final artifact: `samples/<project>/generated/05-revised-draft.md` — the prose.

---

## 🎯 Slash commands (Claude Code chat)

When you open this repo in a Claude Code chat session, these slash commands become available. They're stored in [`.claude/commands/`](.claude/commands/).

| Command | What it does |
|---|---|
| **`/af-start`** | ⭐ **New user? Start here.** Paste idea → answer Q&A → get story. |
| `/af-create-scene` | Run the 5-agent pipeline on a sample whose `inputs/` already exists |
| `/af-agent <id>` | Run a single agent (e.g. `/af-agent anti-ai-editor`) |
| `/af-help` | List slash commands + CLI equivalents |
| `/af-setup` | Run the one-shot installer (`python scripts/setup.py`) |
| `/af-status` | Show what's already been generated for a sample |

The slash commands use Claude to act AS the agents — the Python orchestrator hydrates prompts and validates outputs, Claude does the LLM work in the chat session. **No API key needed.**

---

## 🖥️ CLI commands

### Recommended end-to-end

```bash
python -m orchestrator create-scene --sample <sample-path>
```

Interactive runner. Walks through `scene-director → symbolism-tracker → dialogue-specialist → anti-ai-editor → continuity-auditor`. Pauses after each step so you can paste the hydrated prompt into Claude in your IDE, save the reply, then continue. **No API key required.**

### Per-agent (advanced)

```bash
# Hydrate a single agent's prompt
python -m orchestrator prepare-agent <agent-id> --sample <sample-path>

# Validate the agent's output (after you've saved Claude's reply)
python -m orchestrator validate-agent-output <agent-id> --sample <sample-path> --input <reply-file>
```

`<agent-id>` ∈ `{scene-director, symbolism-tracker, dialogue-specialist, anti-ai-editor, continuity-auditor}`

Downstream agents depend on prior agents' canonical artifacts; run them in order — or just use `create-scene` which handles ordering for you.

### Utilities

```bash
# List available workflows
python -m orchestrator list-workflows

# Inspect a sample's directory tree and required inputs
python -m orchestrator inspect-sample --sample <sample-path>

# Verbose logging
python -m orchestrator --log-level DEBUG create-scene --sample samples/mvp-scene-01
```

### API mode (optional)

```bash
# Set your key in .env first:
#   ANTHROPIC_API_KEY=sk-ant-...

# Then call Anthropic directly (Scene Director only at MVP):
python -m orchestrator run-agent scene-director --sample <sample-path>
```

API mode hits the Anthropic SDK; manual mode goes through your IDE's Claude. Both produce the same canonical artifacts.

### Make targets

```bash
make setup         # one-shot install
make test          # run unit tests (no API key)
make test-all      # run all tests incl. live LLM (needs API key)
make create-scene  # default-sample scene generation
make clean         # remove .venv, caches, generated runs
make help          # list make targets + slash commands
```

---

## 📂 Project layout

```
Creator/
├── README.md                     ← you are here
├── pyproject.toml                ← Python project metadata
├── Makefile                      ← convenience targets
├── setup.bat                     ← Windows setup wrapper
├── .env.example                  ← copy to .env if you want API mode
│
├── scripts/
│   └── setup.py                  ← one-shot installer (stdlib only)
│
├── .claude/
│   └── commands/                 ← slash commands for Claude Code
│       ├── af-help.md
│       ├── af-setup.md
│       ├── af-create-scene.md
│       ├── af-agent.md
│       └── af-status.md
│
├── docs/                         ← framework documentation
│   ├── foundation/               manifest, philosophy, 10 narrative laws
│   ├── architecture/             pipeline, memory graph, context assembly
│   ├── agents/                   agent system + contracts
│   ├── schema/                   character/theme/world/scene schemas
│   ├── anti-ai/                  AI smells, humanization, revision pipeline
│   ├── culture/                  cultural narrative layer
│   ├── language/                 language narrative system
│   ├── literary-styles/          JP/VN/EN-psych/RU-philos profiles
│   ├── mvp/                      MVP scope, first generation flow
│   ├── research/                 reference analysis, technique library
│   └── implementation/           orchestrator + manual workflow plans
│
├── prompts/                      ← prompt templates (the agent contracts)
│   ├── agents/                   10 generative + validator agents
│   ├── shared/                   global rules, output format, anti-AI constraints
│   ├── workflows/                scene / chapter / revision workflows
│   └── culture/                  4 cultural agents
│
├── schema/                       ← YAML schemas for culture profiles
│
├── samples/                      ← golden validation fixtures
│   ├── mvp-scene-01/             single-scene success (RUN THIS)
│   ├── cross-cultural-scene-01/  JP + VN sibling regenerations
│   ├── invariant-violation-01/   escalate-path proof
│   ├── stereotype-bait-01/       detector teeth proof
│   └── chapter-01-baseline/      3-scene chapter + 5 audits
│
└── orchestrator/                 ← Python runner
    ├── core/                     config, artifact IO, bundle, DAG runner
    ├── llm/                      Anthropic SDK wrapper
    ├── prompts/                  loader + Jinja2 render + YAML extract
    ├── graph/                    JSON memory graph + symbol state machine
    ├── workflows/                manual_mode + workflow runner + API path
    ├── tests/                    5 test files, ~50 cases
    ├── cli.py
    └── README.md                 ← orchestrator-specific reference
```

---

## 📖 Where to read next

| To understand... | Read this |
|---|---|
| **What the framework IS** | [`docs/foundation/creator-framework-manifest.md`](docs/foundation/creator-framework-manifest.md) |
| **Why it exists (philosophy)** | [`docs/foundation/core-philosophy.md`](docs/foundation/core-philosophy.md) |
| **The 10 narrative laws** | [`docs/foundation/narrative-laws.md`](docs/foundation/narrative-laws.md) |
| **The 11-stage pipeline** | [`docs/architecture/narrative-pipeline.md`](docs/architecture/narrative-pipeline.md) |
| **Memory graph design** | [`docs/architecture/memory-graph.md`](docs/architecture/memory-graph.md) |
| **Anti-AI revision system** | [`docs/anti-ai/anti-ai-revision-pipeline.md`](docs/anti-ai/anti-ai-revision-pipeline.md) |
| **Cross-cultural regeneration** | [`docs/language/localization-vs-regeneration.md`](docs/language/localization-vs-regeneration.md) |
| **Manual workflow step-by-step** | [`docs/implementation/manual-agent-workflow.md`](docs/implementation/manual-agent-workflow.md) |
| **Python orchestrator details** | [`orchestrator/README.md`](orchestrator/README.md) |
| **Implementation roadmap** | [`docs/implementation/python-orchestrator-plan.md`](docs/implementation/python-orchestrator-plan.md) |

---

## 🧪 Tests

```bash
# Unit tests — no API key required (default)
pytest -ra

# Integration test against Anthropic API — auto-skips if no key
pytest orchestrator/tests/test_scene_director_integration.py -ra -s
```

~50 test cases, all green without an API key.

---

## 🏗️ What gets written where

Generated artifacts (gitignored — reproducible from inputs):

```
samples/<sample>/generated/
├── 01-scene-blueprint.yaml         ← scene structure
├── 02-symbol-audit.yaml            ← symbol audit
├── 03-dialogue-draft.yaml          ← dialogue draft
├── 04-anti-ai-report.yaml          ← smell report + humanization log
├── 05-revised-draft.md             ← ★ THE STORY (prose) ★
├── 06-continuity-report.yaml       ← continuity audit
└── manual/                         ← hydrated prompts + saved Claude replies
    ├── scene-director-prompt.md
    ├── scene-director-output.yaml
    └── ... (per agent)
```

The "story" is **`05-revised-draft.md`**. That's the readable prose output of the framework.

---

## 🤝 Design decisions

| Choice | Rationale |
|---|---|
| Manual mode default, API mode optional | Most contributors use Claude in their IDE; no per-token billing needed |
| Hand-rolled DAG (no LangGraph etc.) | Debuggability beats framework magic at MVP scale |
| JSON-backed memory graph (no DB) | Repo-versionable, inspectable in any editor |
| Anthropic SDK only (no multi-provider abstraction) | Single use case; abstract when a second use case appears |
| Jinja2 only on the user-prompt scaffold (not on .prompt.md bodies) | Avoids collision with literal `{{ }}` examples in templates |
| `.claude/commands/` slash commands | Claude Code's standard convention; works alongside the CLI |
| Schema validators reject empty fields | Catches "valid YAML but agent skipped a section" cases |
| Adversarial validator isolation | Each validator runs with minimal bundle; prevents rationalizing each other's leniency |
| Five-corner sample matrix | Proves success path, cross-culture, escalate, stereotype detection, chapter-level |

For the longer rationale see [`docs/foundation/creator-framework-manifest.md`](docs/foundation/creator-framework-manifest.md) and [`docs/implementation/python-orchestrator-plan.md`](docs/implementation/python-orchestrator-plan.md).

---

## 📜 License

Proprietary — see `pyproject.toml`.
