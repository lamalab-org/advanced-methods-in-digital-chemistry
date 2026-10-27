# Working with a coding assistant

Course instructions:
https://lamalab-org.github.io/advanced-methods-in-digital-chemistry/cli-assistant.html

This is a deliberately flawed mean squared error calculation. The inputs are
constructed examples, not chemical measurements. Use non-empty, equal-length
sequences of numbers throughout this exercise.

In this folder, using macOS/Linux or Ubuntu in WSL 2:

```sh
uv run --no-project --python 3.12 score.py
uv run --no-project --python 3.12 check_score.py
```

The initial checks should report two failures. Predict the results by hand,
then use a terminal coding assistant to inspect the calculation and propose
a minimal repair to score.py. Keep check_score.py unchanged. Compare the files
before and after, run the checks yourself, and devise another small case.

The course page explains installation, keeping a before-copy, and the optional
Codex/Blablador connection. digital-chemistry.config.toml contains connection
settings, not a credential. Do not save tokens in this folder or paste them
into a conversation. An assistant you already use is also welcome; pair work
is available when installation or access is unavailable.
