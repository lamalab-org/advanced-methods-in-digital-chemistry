"""Execute the native marimo notebooks and export recorded results for reading.

Run from course/: uv run --locked --group mof python scripts/build_notebook_previews.py
The MOF preview intentionally includes the test evaluation and bootstrap.
The editable notebook keeps these behind a checkbox by default.
"""
from pathlib import Path
import os
import subprocess
import sys

root = Path(__file__).resolve().parents[1]
output = root / "notebooks/previews"
output.mkdir(exist_ok=True)
for notebook in sorted((root / "notebooks").glob("*.py")):
    command = [sys.executable, "-m", "marimo", "export", "html", str(notebook),
               "--output", str(output / (notebook.stem + ".html")), "--force"]
    if notebook.stem == "03-mof-uptake":
        command += ["--", "--show-test"]
    subprocess.run(command, cwd=root, env={**os.environ, "MPLBACKEND": "Agg"}, check=True)
    print(f"Exported {notebook.stem}")
