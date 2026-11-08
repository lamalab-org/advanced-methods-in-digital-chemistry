"""Build the shared student kit from an explicit list of public resources."""
from pathlib import Path
from zipfile import ZIP_DEFLATED, ZipFile, ZipInfo

root = Path(__file__).resolve().parents[1]
stems = ("00-getting-started", "02-calibration-lab", "03-mof-uptake", "model-selection")
files = ["pyproject.toml", ".python-version", "uv.lock", "requirements.txt",
         "scripts/check_environment.py"]
for stem in stems:
    files += [f"notebooks/{stem}.py", f"notebooks/previews/{stem}.html"]
files += [str(p.relative_to(root)) for p in sorted((root / "data/mof-uptake").iterdir()) if p.is_file()]
files += [f"practicals/cli-assistant/{name}" for name in
          ("README.md", "score.py", "check_score.py", "digital-chemistry.config.toml")]
readme = """Advanced Methods in Digital Chemistry: course kit

One folder and one Python environment for all course notebooks.
Setup guide: https://lamalab-org.github.io/advanced-methods-in-digital-chemistry/setup.html

Extract this complete folder. Keep data/ beside notebooks/.
On Windows, use Ubuntu in WSL 2 and keep this folder inside your Linux home
directory, following the setup guide. On macOS/Linux, use your terminal.
Install uv using https://docs.astral.sh/uv/getting-started/installation/
Then navigate to this extracted folder, where ls shows pyproject.toml:

    uv --version
    uv sync --locked
    uv run --locked python scripts/check_environment.py
    uv run --locked marimo edit --headless

Open the complete local URL printed by marimo, including its access token.
In the browser, choose a file in notebooks/:

    00-getting-started.py   basic Python and reactive notebooks
    02-calibration-lab.py   fitting a calibration curve
    03-mof-uptake.py        predicting simulated MOF gas uptake
    model-selection.py     bias, variance, regularisation, cross-validation

To open a particular notebook directly, for example:

    uv run --locked marimo edit notebooks/03-mof-uptake.py --headless

Use this same folder and these commands for later classes. uv installs all
course dependencies by default; uv run selects the environment automatically.
Keep the terminal open while working. Save edited notebooks under a new name.
Stop marimo with Ctrl+C in the terminal. Reopen with the same command.

The initial package installation needs internet access. Computation then
uses the supplied local data; no Kaggle account, GPU, or chatbot is required.
An assistant such as Jan with Blablador is optional; see the setup guide.
Do not share tokens or the token-bearing local marimo URL in chat messages.

notebooks/previews/ contains recorded results; its controls do not rerun
Python, and its display assets require internet access. The MOF preview
includes test results. In the live notebook, record your model choice before
checking the final-test box. Once seen, test results cannot be made unseen;
later model changes are exploratory.

The MOF targets are simulated CO2 uptakes, not experimental measurements.
Read data/mof-uptake/README.md for units, provenance, evaluation scope, and
the retained source notice. The other notebooks use teaching/simulated data.

The optional terminal-assistant exercise is in practicals/cli-assistant/.
Open a terminal in that subfolder and follow its README. Two initial checks
are deliberately failing; finding and correcting the error is the exercise.
"""
target = root / "downloads/course-kit.zip"
target.parent.mkdir(exist_ok=True)
with ZipFile(target, "w") as archive:
    def add(name, data):
        info = ZipInfo(f"digital-chemistry-course/{name}", date_time=(2026, 11, 8, 0, 0, 0))
        info.compress_type = ZIP_DEFLATED
        info.external_attr = 0o644 << 16
        archive.writestr(info, data)

    for name in files:
        add(name, (root / name).read_bytes())
    add("START-HERE.txt", readme.encode())
    add(".gitignore", b".venv/\n__marimo__/\n.env\n")
print(f"Built {target.name}: {len(files) + 2} files, {target.stat().st_size:,} bytes.")
