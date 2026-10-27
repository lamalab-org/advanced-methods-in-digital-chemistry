"""Package the marimo MOF notebook and its HTML preview, pinned data, notices, and environment."""
from pathlib import Path
from zipfile import ZIP_DEFLATED, ZipFile

root = Path(__file__).resolve().parents[1]
files = ["pyproject.toml", "uv.lock", ".python-version", "notebooks/03-mof-uptake.py",
         "notebooks/previews/03-mof-uptake.html", "notebooks/model-selection.py",
         "notebooks/previews/model-selection.html"]
files += [str(path.relative_to(root)) for path in sorted((root / "data/mof-uptake").iterdir()) if path.is_file()]
instructions = """Advanced Methods in Digital Chemistry: MOF practical

Extract this complete folder; the notebook needs its data/ directory.
Use Ubuntu's Bash shell in WSL on Windows, or Terminal on macOS/Linux.
On Windows, keep the project in the Linux home directory, as in the course setup.
From the extracted folder containing pyproject.toml:

    uv sync --locked --group mof
    uv run --locked --group mof marimo edit notebooks/03-mof-uptake.py --headless

Open the full localhost URL printed by marimo in your browser.
Keep its terminal open. The command opens notebooks/03-mof-uptake.py.
Use the mof group flag each time you launch with uv run.
Save your edited notebook under a new name.

For the follow-up on bias, variance, regularisation and cross-validation:

    uv run --locked --group mof marimo edit notebooks/model-selection.py --headless

This notebook revisits the MolSim potential-fitting example, using Lennard–Jones
energies with artificial noise. It does not report a final test score.
Its recorded default calculation is in notebooks/previews/model-selection.html.

The first package installation requires internet access. The notebook then
runs on local supplied data, without Kaggle or chatbot accounts or a GPU.
notebooks/previews/03-mof-uptake.html provides code and recorded results
for reading if execution is unavailable; its controls do not rerun Python.
The preview includes test results. Leave the live notebook test checkbox
unchecked until you record a model choice. After seeing any test results,
further model changes are exploratory; unchecking does not make them unseen.
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
    archive.writestr("digital-chemistry-mof/.gitignore", ".venv/\n__marimo__/\n.env\n")
print(f"Created {out.name} ({out.stat().st_size:,} bytes)")
