#!/usr/bin/env python
"""AetherForge Creator Framework — one-shot setup script.

Usage:
    python scripts/setup.py

What this does:
    1. Verifies Python version (3.11+ required)
    2. Creates .venv/ virtual environment if missing
    3. Installs dependencies into .venv (pip install -e ".[dev]")
    4. Copies .env.example to .env if .env doesn't exist (you only need .env
       for optional API mode — manual mode works without it)
    5. Verifies the install by importing the orchestrator package
    6. Prints next-steps

Idempotent — safe to re-run. Won't recreate the venv or overwrite .env.

This script uses STDLIB ONLY so it can run on a freshly-cloned repo with no
dependencies pre-installed.
"""

from __future__ import annotations

import os
import shutil
import subprocess
import sys
import venv
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
VENV_DIR = REPO_ROOT / ".venv"
MIN_PYTHON = (3, 11)


def _banner(msg: str, char: str = "=") -> None:
    print()
    print(char * 70)
    print(msg)
    print(char * 70)


def _step(n: int, total: int, msg: str) -> None:
    print(f"\n[{n}/{total}] {msg}")


def check_python_version() -> None:
    if sys.version_info < MIN_PYTHON:
        major, minor = MIN_PYTHON
        print(f"  ✗ ERROR: Python {major}.{minor}+ required.")
        print(f"      You have: Python {sys.version.split()[0]}")
        print(f"      Install Python {major}.{minor}+ and re-run this script.")
        sys.exit(1)
    print(
        f"  ✓ Python {sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}"
    )


def create_venv() -> None:
    if VENV_DIR.exists():
        print(f"  ✓ venv already exists at .venv/ (skipping creation)")
        return
    print(f"  → Creating venv at .venv/ ...")
    venv.create(str(VENV_DIR), with_pip=True, clear=False, system_site_packages=False)
    print(f"  ✓ Created.")


def _venv_python() -> Path:
    if os.name == "nt":
        return VENV_DIR / "Scripts" / "python.exe"
    return VENV_DIR / "bin" / "python"


def install_deps() -> None:
    python = _venv_python()
    if not python.exists():
        print(f"  ✗ ERROR: venv Python not found at {python}")
        print(f"      The venv creation step appears to have failed.")
        sys.exit(2)
    print(f"  → Installing dependencies (this may take a minute)...")
    try:
        subprocess.check_call(
            [str(python), "-m", "pip", "install", "--quiet", "-e", ".[dev]"],
            cwd=str(REPO_ROOT),
        )
    except subprocess.CalledProcessError as exc:
        print(f"  ✗ ERROR: pip install failed (exit {exc.returncode}).")
        print(f"      Try running it manually to see the full output:")
        print(f'         {python} -m pip install -e ".[dev]"')
        sys.exit(3)
    print(f"  ✓ Installed: anthropic, jinja2, pyyaml, python-dotenv, pytest")


def ensure_env_file() -> None:
    src = REPO_ROOT / ".env.example"
    dst = REPO_ROOT / ".env"
    if dst.exists():
        print(f"  ✓ .env already exists (not overwriting)")
        return
    if not src.exists():
        print(f"  ⚠ .env.example missing — skipping")
        return
    shutil.copy2(src, dst)
    print(f"  ✓ Created .env from .env.example")
    print(f"    (You only need to edit .env if you want optional API mode.)")


def verify_install() -> None:
    python = _venv_python()
    try:
        subprocess.check_call(
            [
                str(python),
                "-c",
                "import orchestrator; print('  ✓ orchestrator', orchestrator.__version__, 'imports cleanly')",
            ],
            cwd=str(REPO_ROOT),
        )
    except subprocess.CalledProcessError:
        print(f"  ✗ ERROR: orchestrator package can't be imported after install.")
        sys.exit(4)


def print_next_steps() -> None:
    if os.name == "nt":
        activate = ".venv\\Scripts\\activate"
    else:
        activate = "source .venv/bin/activate"

    _banner("Setup complete!")
    print()
    print("Next steps:")
    print()
    print(f"  1. Activate the virtual environment:")
    print(f"       {activate}")
    print()
    print(f"  2. Run the tests to confirm everything works:")
    print(f"       pytest -ra")
    print()
    print(f"  3. Generate your first scene end-to-end:")
    print(f"       python -m orchestrator create-scene --sample samples/mvp-scene-01")
    print()
    print(f"  Or in a Claude Code chat (after cd to this repo):")
    print(f"       /af-create-scene")
    print()
    print(f"For the full command reference, see README.md at the repo root.")
    print("=" * 70)


def main() -> int:
    _banner("AetherForge Creator Framework — Setup")
    _step(1, 5, "Check Python version")
    check_python_version()
    _step(2, 5, "Create virtual environment")
    create_venv()
    _step(3, 5, "Install dependencies")
    install_deps()
    _step(4, 5, "Create .env (optional, for API mode)")
    ensure_env_file()
    _step(5, 5, "Verify install")
    verify_install()
    print_next_steps()
    return 0


if __name__ == "__main__":
    sys.exit(main())
