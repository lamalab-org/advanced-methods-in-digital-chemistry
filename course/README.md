# Course sources and practicals

This directory contains the student Quarto book for **Advanced Methods in Digital Chemistry**, by Kevin Maik Jablonka. The [course outline](outline.qmd) gives the ten topic groups and the updated timetable: 11 November (12:10–16:00), 2 December and 9 December (12:00–16:00). There is no teaching on 18 or 25 November, or 16, 23 or 30 December; the listed 2027 dates still need confirmation. The current chapters cover AI and science, learning from data, MOF gas-uptake modelling, and a follow-up model-selection practical, with marimo notebooks and calibration and kernel activities. Additional chapters are in development.

Read the [published course](https://lamalab-org.github.io/advanced-methods-in-digital-chemistry/) or use `quarto preview` from this directory. `quarto render` builds `_book/` without executing Python. The repository workflow uses Quarto 1.8.24. Publishing instructions are in the [repository README](../README.md).

## Python environment

Follow [the setup chapter](https://lamalab-org.github.io/advanced-methods-in-digital-chemistry/setup.html) for Jan/Blablador, computing vocabulary, and uv installation. Windows users run the Python commands in Ubuntu on WSL 2; macOS and Linux users use their terminals. Chatbot access is optional.

From this directory:

```sh
uv sync --locked
uv run --locked python scripts/check_environment.py
uv run --locked marimo edit notebooks/00-getting-started.py --headless
```

Open the complete local URL printed by marimo in your browser. The command opens `notebooks/00-getting-started.py`. For lecture 2, stop the server with Ctrl+C and replace the filename in the command with `notebooks/02-calibration-lab.py`. The course uses Python 3.12. `pyproject.toml` declares dependencies and `uv.lock` pins the environment. The downloadable `downloads/course-kit.zip` contains the shared environment, all four notebooks and previews, MOF data, and the terminal exercise.

For the MOF practical, use the same environment:

```sh
uv sync --locked
uv run --locked marimo edit notebooks/03-mof-uptake.py --headless
```

Open `notebooks/03-mof-uptake.py`. The data are simulated CO₂ uptakes, with eight geometric descriptors. Source revision, units, subset hashes, and the original MolSim MIT notice are in `data/mof-uptake/`. The same course kit contains this notebook, data, and locked environment. No Kaggle account or GPU is needed.

The notebooks are Python source files; `notebooks/previews/` holds HTML exports with code and recorded results. The previews cannot recompute results and load marimo display assets from a CDN, so opening them requires an internet connection. Save student edits under a new notebook filename. The locked environment and all four notebooks have been checked on an Apple Silicon Mac. WSL/Ubuntu installation and Jan–Blablador access still need a classroom device pilot.

## Model-selection practical

The [follow-up notes](lectures/model-selection.qmd) and `notebooks/model-selection.py` connect underfitting and overfitting, bias and variance, regularisation, and cross-validation before the neural-network session. Run it with `uv run --locked marimo edit notebooks/model-selection.py --headless`. It uses the same installed environment as the MOF exercise and simulated data only. Its controls compare repeated fits and penalty strengths, then show five-fold assignments and a candidate comparison with preprocessing fitted inside each fold. The final selected procedure is refitted on development data; no final test score is reported. The course kit includes both notebooks and their recorded previews.

## Terminal coding-assistant practical

The [coding-assistant guide](https://lamalab-org.github.io/advanced-methods-in-digital-chemistry/cli-assistant.html) uses a small, deliberately flawed mean squared error function. Its source files are in `practicals/cli-assistant/`, and the shared `downloads/course-kit.zip` includes the same subfolder. It requires only Python 3.12's standard library. The initial check script should fail on two cases; do not repair the distributed starter.

The guide includes a named Codex CLI profile for Blablador, based on Jülich's guide and current Codex documentation. The profile contains no token. The exercise and its expected correction are checked locally; the authenticated Blablador CLI tool-use sequence still needs a classroom pilot. A successful chat connection alone does not verify that sequence.

## Updating the material

- The website's shared visual assets and their sources are documented in [assets/README.md](assets/README.md). Edit the shared styles there; the local instructor book copies them during rendering.
- Keep the remaining 2026 teaching dates in `_includes/2026-schedule.qmd`, shared by the home page and outline. Session guides live in `sessions/`; the 11 November guide links to existing notebooks without embedding them. Share the project-ideas document privately with enrolled students, not through the public repository.
- Edit student chapters in `lectures/`, with linked technical terms in `glossary.qmd` and suggested references in `reading.qmd`.
- Edit the marimo notebooks directly in `notebooks/*.py`. `scripts/build_calibration.py` regenerates only the independent browser activity and its shared data.
- `scripts/build_mof_lab.py` checks the supplied data hash. Its optional `--source PATH_TO_ML_MOLSIM` argument rebuilds the subset from the pinned upstream revision. It does not overwrite the notebook.
- Check notebook structure with `uv run --locked marimo check notebooks/*.py`. Execute and refresh the recorded HTML previews with `uv run --locked python scripts/build_notebook_previews.py`. This deliberately includes test results in the MOF preview; the live notebook waits for its test checkbox. Inspect the outputs and try the interactive controls before publishing. Refresh the MOF plot images under `assets/` if their underlying results change.
- Rebuild the single course download after changing its inputs: `uv run --locked python scripts/build_course_kit.py`. It includes all four notebooks, their previews, data and notices, environment files, the check script, and only the four named terminal-exercise files.
- After an intentional dependency update, refresh the pinned fallback with `uv export --locked --format requirements-txt --no-hashes --no-dev --no-emit-project --output-file requirements.txt`.

Build and validate from this directory:

```sh
quarto render
python3 scripts/check_site.py _book
```

The validator checks local links, required downloads, and exclusion of instructor material. The public build contains only the student book. Local teaching notes, source documents, caches, and environments are excluded from Git and publication.
