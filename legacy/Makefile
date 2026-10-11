# AetherForge Creator Framework — convenience targets

.PHONY: setup test test-all clean help create-scene

# Default target
help:
	@echo "AetherForge Creator Framework — make targets:"
	@echo ""
	@echo "  make setup         — one-shot install (creates .venv, installs deps, copies .env)"
	@echo "  make test          — run the unit tests (no API key required)"
	@echo "  make test-all      — run all tests including LLM integration (needs ANTHROPIC_API_KEY)"
	@echo "  make create-scene  — generate scene end-to-end against samples/mvp-scene-01"
	@echo "  make clean         — remove .venv, caches, generated runs"
	@echo ""
	@echo "Slash commands (in Claude Code chat):"
	@echo "  /af-create-scene   — interactive scene generation through chat"
	@echo "  /af-agent <id>     — run a single agent through chat"
	@echo "  /af-help           — list slash commands"
	@echo ""
	@echo "For the full command reference, see README.md"

setup:
	python scripts/setup.py

test:
	pytest -ra

test-all:
	pytest -ra orchestrator/tests/

create-scene:
	python -m orchestrator create-scene --sample samples/mvp-scene-01

clean:
	rm -rf .venv .pytest_cache .ruff_cache
	rm -rf orchestrator/runs/*
	rm -rf samples/*/generated
	find . -type d -name __pycache__ -prune -exec rm -rf {} +
	find . -type d -name "*.egg-info" -prune -exec rm -rf {} +
