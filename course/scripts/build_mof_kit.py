"""Package the executed MOF notebook, pinned data, notices, and environment."""
from pathlib import Path
from zipfile import ZIP_DEFLATED, ZipFile

root = Path(__file__).resolve().parents[1]
files = ["pyproject.toml", "uv.lock", ".python-version", "notebooks/03-mof-uptake.ipynb"]
files += [str(path.relative_to(root)) for path in sorted((root / "data/mof-uptake").iterdir()) if path.is_file()]
instructions = """Advanced Methods in Digital Chemistry: MOF practical

Extract this complete folder; the notebook needs its data/ directory.
Use Ubuntu's Bash shell in WSL on Windows, or Terminal on macOS/Linux.
On Windows, keep the project in the Linux home directory, as in the course setup.
From the extracted folder containing pyproject.toml:

    uv sync --locked --group mof
    uv run --locked --group mof jupyter lab --no-browser

Open the full localhost URL printed by Jupyter in your browser.
Keep its terminal open. Open notebooks/03-mof-uptake.ipynb.
Use the mof group flag each time you launch with uv run.
Save your edited notebook under a new name.

The first package installation requires internet access. The notebook then
runs on local supplied data, without Kaggle or chatbot accounts or a GPU.
Its saved outputs support a read-through if execution is unavailable.
Jan/Blablador remains optional assistance, configured through the course setup.

The targets are simulated CO2 uptakes, not experimental measurements.
Read data/mof-uptake/README.md for units, provenance, and evaluation scope.
The original MolSim MIT notice is retained beside the data.
"""
out = root / "downloads/mof-practical.zip"
with ZipFile(out, "w", compression=ZIP_DEFLATED) as archive:
    for name in files:
        archive.write(root / name, "digital-chemistry-mof/" + name)
    archive.writestr("digital-chemistry-mof/START-HERE.txt", instructions)
    archive.writestr("digital-chemistry-mof/.gitignore", ".venv/\n.ipynb_checkpoints/\n.env\n")
print(f"Created {out.name} ({out.stat().st_size:,} bytes)")
