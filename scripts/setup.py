"""Install the active local studio, without model/provider dependencies."""
import subprocess
import sys
from pathlib import Path

if sys.version_info < (3, 11):
    raise SystemExit("Python 3.11+ required")
root = Path(__file__).resolve().parent.parent
subprocess.run([sys.executable, "-m", "pip", "install", "-e", str(root)], check=True)
print("Run: python -m story_studio")
