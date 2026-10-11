"""Entry point for `python -m orchestrator`.

Dispatches to orchestrator.cli.main().
"""

from orchestrator.cli import main

if __name__ == "__main__":
    raise SystemExit(main())
