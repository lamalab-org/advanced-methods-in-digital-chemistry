# Course sources and practicals

This directory contains the student Quarto book for **Advanced Methods in Digital Chemistry**, by Kevin Maik Jablonka. The [course outline](outline.qmd) gives the proposed ten-session sequence and its prerequisites. Three lecture drafts cover AI and science, learning from data, and MOF gas-uptake modelling, with notebooks and calibration and kernel activities. Additional chapters are in development.

Read the [published course](https://lamalab-org.github.io/advanced-methods-in-digital-chemistry/) or use `quarto preview` from this directory. `quarto render` builds `_book/` without executing Python. The repository workflow uses Quarto 1.8.24. Publishing instructions are in the [repository README](../README.md).

## Python environment

Follow [the setup chapter](https://lamalab-org.github.io/advanced-methods-in-digital-chemistry/setup.html) for Jan/Blablador, computing vocabulary, and uv installation. Windows users run the Python commands in Ubuntu on WSL 2; macOS and Linux users use their terminals. Chatbot access is optional.

From this directory:

```sh
uv sync --locked
uv run --locked python scripts/check_environment.py
uv run --locked jupyter lab --no-browser
```

Open the printed Jupyter URL in your browser, then open `notebooks/00-getting-started.ipynb` or `notebooks/02-calibration-lab.ipynb`. The course uses Python 3.12. `pyproject.toml` declares dependencies and `uv.lock` pins the environment. The downloadable `downloads/introductory-setup.zip` contains a compact copy of this environment and the introductory notebooks.

For the MOF practical, include its dependency group each time:

```sh
uv sync --locked --group mof
uv run --locked --group mof jupyter lab --no-browser
```

Open `notebooks/03-mof-uptake.ipynb`. The data are simulated CO₂ uptakes, with eight geometric descriptors. Source revision, units, subset hashes, and the original MolSim MIT notice are in `data/mof-uptake/`. The separate `downloads/mof-practical.zip` contains the notebook, data, and locked environment. No Kaggle account or GPU is needed.

Save student edits under a new notebook filename. The locked environment and all three notebooks have been checked on an Apple Silicon Mac. WSL/Ubuntu installation and Jan–Blablador access still need a classroom device pilot.

## Updating the material

- The website's shared visual assets and their sources are documented in [assets/README.md](assets/README.md). Edit the shared styles there; the local instructor book copies them during rendering.
- Edit student chapters in `lectures/`, with linked technical terms in `glossary.qmd` and suggested references in `reading.qmd`.
- `scripts/build_calibration.py` regenerates the calibration activity, shared generated data, and introductory notebooks. This clears notebook outputs and overwrites those files.
- `scripts/build_mof_lab.py` regenerates the MOF notebook. Its optional `--source PATH_TO_ML_MOLSIM` argument also rebuilds the data subset from the pinned upstream revision. Without it, the supplied data are preserved.
- After regenerating notebooks, execute them from fresh kernels and inspect results. Verification tools are in the `dev` dependency group; combine it with `mof` for the MOF notebook. Refresh the MOF plot images under `assets/` if their underlying results change.
- Rebuild the download archives after changing their inputs: `uv run --locked python scripts/build_setup_kit.py` and `uv run --locked --group mof python scripts/build_mof_kit.py`.
- After an intentional dependency update, refresh the pinned fallback with `uv export --locked --format requirements-txt --no-hashes --no-dev --no-emit-project --output-file requirements.txt`.

Build and validate from this directory:

```sh
quarto render
python3 scripts/check_site.py _book
```

The validator checks local links, required downloads, and exclusion of instructor material. The public build contains only the student book. Local teaching notes, source documents, caches, and environments are excluded from Git and publication.
