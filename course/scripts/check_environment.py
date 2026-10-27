"""Quick local check for the introductory notebook environment; no network access."""
import importlib
import math
import subprocess
import sys
from importlib.metadata import version
from pathlib import Path


def main():
    print(f"Python {sys.version.split()[0]}")
    print(f"Interpreter: {sys.executable}")
    issues = []
    if sys.version_info[:2] != (3, 12):
        issues.append("Use the course's Python 3.12 environment with uv run.")

    for package, module in [
        ("numpy", "numpy"),
        ("matplotlib", "matplotlib"),
        ("marimo", "marimo"),
        ("ruff", "ruff"),
    ]:
        try:
            importlib.import_module(module)
            print(f"OK: {package} {version(package)}")
        except Exception as exc:
            issues.append(f"Could not import {package}: {type(exc).__name__}: {exc}")

    if not issues:
        import matplotlib
        matplotlib.use("Agg")
        import matplotlib.pyplot as plt
        import numpy as np
        from numpy.polynomial import Polynomial

        c = np.array([0.0, 0.5, 1.0])
        absorbance = 0.15 + 0.8 * c
        model = Polynomial.fit(c, absorbance, 1)
        assert math.isclose(float(model(0.5)), 0.55, rel_tol=1e-10)
        fig, ax = plt.subplots()
        ax.plot(c, model(c))
        ax.set(xlabel="Concentration / mmol L$^{-1}$", ylabel="Absorbance")
        fig.canvas.draw()
        plt.close(fig)
        print("OK: fitted a calibration curve and rendered a plot in memory.")
        formatting = subprocess.run(
            [sys.executable, "-m", "ruff", "format", "--stdin-filename", "check.py", "-"],
            input="prediction=0.8*0.5+0.15\n", text=True,
            capture_output=True, check=True,
        )
        assert "prediction = 0.8 * 0.5 + 0.15" in formatting.stdout
        print("OK: Ruff can format a notebook calculation when saving.")

    root = Path(__file__).resolve().parents[1]
    for name in ["00-getting-started.py", "02-calibration-lab.py"]:
        if not (root / "notebooks" / name).is_file():
            issues.append(f"Missing notebook: {name}. Extract the complete course folder.")

    if issues:
        for issue in issues:
            print(f"ACTION: {issue}")
        return 1

    print("READY: uv run --locked marimo edit notebooks/00-getting-started.py --headless")
    print("This checks the local Python tools; it does not test Jan or Blablador access.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
