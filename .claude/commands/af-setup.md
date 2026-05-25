---
description: Run the one-shot AetherForge installer (venv + deps + .env)
---

You are helping the user install the AetherForge Creator Framework on this machine.

## What to do

1. Run the setup script via Bash:

   ```
   python scripts/setup.py
   ```

2. Watch the output. The script prints `[N/5]` progress markers. It is idempotent — safe to re-run.

3. If the script succeeds, summarize what was done in plain language:
   - A virtual environment was created at `.venv/`
   - Dependencies installed: `anthropic`, `jinja2`, `pyyaml`, `python-dotenv`, `pytest`
   - `.env` was created from `.env.example` (no need to edit it unless the user wants API mode)
   - The `orchestrator` package was verified to import cleanly

4. Tell the user how to activate the venv:
   - **Windows:** `.venv\Scripts\activate`
   - **Mac/Linux:** `source .venv/bin/activate`

5. Tell them they can now:
   - Run the tests: `pytest -ra`
   - Generate a scene end-to-end: `/af-create-scene`  (or `python -m orchestrator create-scene --sample samples/mvp-scene-01`)

## If the script fails

Read the error message and explain what went wrong:
- **Python version too old** → user needs Python 3.11+
- **pip install failed** → likely network issue; ask user to re-run manually with verbose pip output: `python -m pip install -e ".[dev]"`
- **venv module missing** → on some Linux distros: `sudo apt install python3-venv`

Do not try to debug network issues for the user — just surface the error and suggest re-running the script.

## Do not

- Do not modify `pyproject.toml` or `setup.py`.
- Do not install global packages.
- Do not skip the venv creation step.
