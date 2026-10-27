"""Build a bounded adaptation of Kevin Jablonka's MolSim 2024 practical.

Run from course/ with the mof group. To re-extract the teaching subset:
  python scripts/build_mof_lab.py --source ../.working/ml_molsim
Without --source, verify the checked-in subset hash.
The marimo notebook is edited directly in notebooks/03-mof-uptake.py.
"""
from pathlib import Path
import argparse
import csv
import hashlib
import json
import shutil
import subprocess

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
COMMIT = "0ebed176b972c9ba9ddf7b6e3a4d04eaf3f32409"
SOURCE_URL = f"https://github.com/kjappelbaum/ml_molsim/tree/{COMMIT}"
FEATURES = ["Di", "Df", "Dif", "density [g/cm^3]", "total_SA_volumetric",
            "total_SA_gravimetric", "total_POV_volumetric", "total_POV_gravimetric"]
TARGET = "pure_uptake_CO2_298.00_1600000"
DATA = ROOT / "data/mof-uptake"


def extract(source):
    revision = subprocess.check_output(
        ["git", "-C", str(source), "rev-parse", "HEAD"], text=True).strip()
    if revision != COMMIT:
        raise ValueError(f"Expected source revision {COMMIT}, found {revision}")
    raw = source / "data/data.csv"
    with raw.open() as handle:
        rows = list(csv.DictReader(handle))
    # Subsample without looking at targets; keep all selected rows and values.
    selected = sorted(np.random.default_rng(4242).choice(len(rows), 1500, replace=False).tolist())
    DATA.mkdir(parents=True, exist_ok=True)
    output = DATA / "mof-uptake.csv"
    columns = ["source_row", "MOFname"] + FEATURES + [TARGET]
    with output.open("w", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=columns)
        writer.writeheader()
        for index in selected:
            writer.writerow({"source_row": index, **{k: rows[index][k] for k in columns[1:]}})
    provenance = {
        "repository": "https://github.com/kjappelbaum/ml_molsim",
        "branch_at_retrieval": "2024", "commit": COMMIT,
        "retrieved": "2026-10-26", "source_file": "data/data.csv",
        "source_sha256": hashlib.sha256(raw.read_bytes()).hexdigest(),
        "subset_sha256": hashlib.sha256(output.read_bytes()).hexdigest(),
        "source_rows": len(rows), "subset_rows": len(selected),
        "subset_seed": 4242, "selection": "NumPy default_rng.choice without replacement; sorted source indices; no target filtering",
        "source_row_convention": "zero-based data-row index excluding CSV header",
        "columns": columns, "features": FEATURES, "target": TARGET,
        "target_kind": "GCMC-computed pure CO2 uptake, not experimental uptake",
        "temperature_K": 298.0, "pressure_Pa": 1600000,
        "target_units": "mmol/g (numerically equal to mol/kg)",
        "license_file": "LICENSE-ml_molsim.txt",
        "grouping_limit": "Unique MOF names are retained; chemically independent framework families are not established by this subset.",
    }
    (DATA / "provenance.json").write_text(json.dumps(provenance, indent=2) + "\n")
    shutil.copyfile(source / "LICENSE", DATA / "LICENSE-ml_molsim.txt")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source", type=Path)
    args = parser.parse_args()
    if args.source: extract(args.source)
    if not (DATA / "provenance.json").exists():
        raise FileNotFoundError("Data missing; supply --source with the pinned reference checkout.")
    provenance = json.loads((DATA / "provenance.json").read_text())
    assert hashlib.sha256((DATA / "mof-uptake.csv").read_bytes()).hexdigest() == provenance["subset_sha256"]
    print("MOF data match the recorded provenance.")
