# Advanced Methods in Digital Chemistry

An English-language course for master's students in chemistry, by Kevin Maik Jablonka.

**[Read the course](https://lamalab-org.github.io/advanced-methods-in-digital-chemistry/)** · **[Getting set up](https://lamalab-org.github.io/advanced-methods-in-digital-chemistry/setup.html)**

The course connects scientific questions and human modelling choices to statistical learning, molecular representations, and practical model building. The current material includes three lecture drafts, a glossary, suggested readings, an interactive calibration activity, and downloadable Python notebooks and data. Further chapters are in development.

## Build and preview

Install [Quarto](https://quarto.org/docs/get-started/). The deployment uses Quarto 1.8.24. From the repository root:

```sh
quarto preview course
```

To build and check the student site:

```sh
quarto render course
python3 course/scripts/check_site.py course/_book
```

The output is `course/_book/`. Rendering the book does not execute the notebooks or require the course Python environment. See [course/README.md](course/README.md) for the notebook environment, data provenance, and instructions for rebuilding the downloadable kits.

## Publishing

Pushing to `main` runs [Publish course](.github/workflows/pages.yml), which renders and checks the student book, then deploys it through GitHub Pages. The workflow can also be started manually from the repository's Actions tab. No personal access token or separate publishing branch is required.

This repository contains student material. Instructor notes, source slides, working documents, local environments, and generated site output are excluded from version control. Only `course/_book/` is uploaded for publication.

The MOF practical retains its source attribution and MIT notice in [course/data/mof-uptake/](course/data/mof-uptake/). References to external publications and books link to their sources.
