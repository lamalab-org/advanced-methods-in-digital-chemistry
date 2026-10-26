"""Package only the files needed for the introductory student environment."""
from pathlib import Path
from zipfile import ZIP_DEFLATED, ZipFile

root = Path(__file__).resolve().parents[1]
files = [
    "pyproject.toml", ".python-version", "uv.lock", "requirements.txt",
    "scripts/check_environment.py", "notebooks/00-getting-started.ipynb",
    "notebooks/02-calibration-lab.ipynb",
]
readme = """Advanced Methods in Digital Chemistry: introductory setup

1. Set up the assistant first so it can help during Python installation.
Install Jan Desktop from https://jan.ai/download and connect it to
Blablador using Juelich's guide:
https://sdlaml.pages.jsc.fz-juelich.de/ai/guides/blablador_jan_ai/
Each student uses their own Blablador token. Enter it only in the provider's
credential field; keep it out of chat messages, notebooks, and screenshots.
Jan connects directly to the remote provider. Local model installation
and Jan's Local API Server are unnecessary for this exercise.

Select a Blablador model and send a first message. For example:
"Suppose a setup command cannot find pyproject.toml. Help me work out what
to check before reinstalling anything. Ask which operating system I use,
explain one check, and say what its result would help us distinguish."
This conversation needs no working Python installation. The file may be
missing, or the command may have been run from the wrong folder.

If Jan is unsuitable, use https://blablador.fz-juelich.de/ in a browser.
If service access is unavailable, continue with a partner or instructor.
Chat access is optional; it is not required for the Python setup.

2. Windows: use Ubuntu in WSL 2 for all Python work; Jan stays on Windows.
If Ubuntu in WSL 2 is not already available, arrange instructor/IT support
and follow https://learn.microsoft.com/en-us/windows/wsl/install
The one-time Windows installation command, entered in Windows Command
Prompt opened as administrator, is:

   wsl --install -d Ubuntu

Restart if requested, then open Ubuntu and create its Linux user account.
Inside Ubuntu, wsl.exe --list --verbose should show VERSION 2 for Ubuntu.
All course commands from here run in Ubuntu's Bash shell. If provisioning
is blocked, use pair work or the supported notebook service while getting
help. macOS/Linux users continue with their existing terminal.

3. Before using Python tools: a terminal is the window for commands;
a shell such as Bash or zsh interprets them. Open Ubuntu on Windows or
Terminal on macOS/Linux. Type commands without prompt markers such as $.
Use pwd to show the current folder, ls to list its contents, and cd followed
by a quoted folder path to change directory. Find pyproject.toml before
running the setup commands below.

4. Install uv using https://docs.astral.sh/uv/getting-started/installation/
On Windows, install the Linux version inside Ubuntu in WSL. The official
installer for Linux and macOS is:

   curl -LsSf https://astral.sh/uv/install.sh | sh

Open a new terminal in the same environment, then check uv --version.
On macOS, brew install uv is an option if Homebrew is already installed.

5. Extract this complete folder. On Windows, keep the project in the
Linux home folder. In Ubuntu run cd ~ and then explorer.exe . to open that
folder in Windows File Explorer. Copy the extracted digital-chemistry-intro
folder into it, then in Ubuntu run:

   cd ~/digital-chemistry-intro

On macOS/Linux, navigate to the extracted project in your terminal.
Check that ls shows pyproject.toml.

6. Run the same commands inside Ubuntu on WSL, macOS, or Linux:

   uv sync --locked
   uv run --locked python scripts/check_environment.py
   uv run --locked jupyter lab --no-browser

Keep the terminal running. Copy Jupyter's complete printed localhost URL,
including its token, into your browser. On Windows use the Windows browser;
the server and Python kernel run in WSL. Keep that URL out of chat messages.

The virtual environment is the project's Python and installed packages in
.venv. uv creates it; uv run selects it without a separate activation step.
pyproject.toml declares dependencies; uv.lock records their versions.
Run the commands above in your shell, and Python code in notebook cells.
The kernel executes those cells and remembers variables until restarted.
Restarting clears those variables but keeps installed packages and files.

Open notebooks/00-getting-started.ipynb. Select the course .venv Python
kernel if prompted. Restart the kernel and run all cells. Explain the
calibration calculation and change one input.
For WSL, sys.executable should point to the Linux project's .venv/bin/python,
and sys.platform should be linux. The Windows and Linux environments are
separate even though they are on the same laptop.

The supplied Python version is 3.12. This kit needs internet access to
download packages initially. It does not require a GPU or an LLM account.

When asking the assistant about a setup error, include your operating
system and environment (for example, Windows with Ubuntu in WSL 2),
where you entered the command, the command, its error message,
and what you expected. Remove credentials and private details first.
Ask for one check at a time. Read the proposed check, predict what it might
show, and compare with the observed result. Use the supplied project,
locked dependencies, and official course instructions as the reference.
Keep the original error and the change that resolved it.

Save edited notebooks under a new filename. This kit contains synthetic
teaching observations, not laboratory data. Ask the instructor about the
browser fallback if local installation is unavailable.

Optional background: MIT's Missing Semester, introduction to the shell:
https://missing.csail.mit.edu/2026/course-shell/
Start with the sections on what a shell is and navigating folders. Its full
Unix exercise set is optional; Windows students use Ubuntu's Bash in WSL.
"""
out = root / "downloads" / "introductory-setup.zip"
out.parent.mkdir(exist_ok=True)
with ZipFile(out, "w", compression=ZIP_DEFLATED) as archive:
    for name in files:
        archive.write(root / name, "digital-chemistry-intro/" + name)
    archive.writestr("digital-chemistry-intro/START-HERE.txt", readme)
    archive.writestr("digital-chemistry-intro/.gitignore", ".venv/\n.ipynb_checkpoints/\n.env\n")
print(f"Created {out.name} ({out.stat().st_size:,} bytes)")
