# MOF uptake teaching subset

Immediate source: Kevin Jablonka's [MolSim repository](https://github.com/kjappelbaum/ml_molsim/tree/0ebed176b972c9ba9ddf7b6e3a4d04eaf3f32409), branch `2024` at retrieval on 26 October 2026. The source notebook describes the labels as GCMC-computed CO₂ uptake. This is a subset of the supplied `data/data.csv`, not newly generated or experimentally measured data.

`provenance.json` records the full revision, source and subset SHA-256 hashes, selection rule, feature names, and target. The accompanying MIT notice is retained verbatim in `LICENSE-ml_molsim.txt`.

The teaching file retains 1,500 of 17,379 rows, sampled without replacement using NumPy `default_rng(4242)`, then sorted by source position. Selection did not use uptake values. It retains eight geometric features, the target, MOF names, and zero-based original data-row numbers. No selected values were changed. All selected feature and target values are finite. The feature subset is a deliberate teaching choice; the original notebook also supplies descriptors of chemical composition and connectivity.

| Column | Meaning / units |
|---|---|
| `source_row` | Zero-based row in the original CSV, excluding its header; provenance only |
| `MOFname` | Original structure identifier; not a model input or a certified independent family label |
| `Di` | Largest included-sphere diameter / Å |
| `Df` | Largest free-sphere diameter / Å |
| `Dif` | Largest included-sphere diameter along the free path / Å |
| `density [g/cm^3]` | Framework density / g cm⁻³ |
| `total_SA_volumetric` | Total surface area per framework volume / m² cm⁻³ |
| `total_SA_gravimetric` | Total surface area per framework mass / m² g⁻¹ |
| `total_POV_volumetric` | Total pore volume per framework volume / cm³ cm⁻³ |
| `total_POV_gravimetric` | Total pore volume per framework mass / cm³ g⁻¹ |
| `pure_uptake_CO2_298.00_1600000` | Computed pure CO₂ uptake at 298 K and 1,600,000 Pa, in mmol g⁻¹ (numerically equal to mol kg⁻¹) |

The source notebook explains the geometric descriptors. The matching target name and its conditions/units are also documented in the [mofdscribe dataset reference](https://mofdscribe.readthedocs.io/en/latest/api/data.html). That documentation is a reference for column meaning, not a claim that this workshop CSV is an unmodified release of a particular mofdscribe dataset. The original CSV's complete simulation settings and row-level database lineage have not been independently reconstructed here.

The notebook uses a fixed random 900/300/300 training/validation/test split. Unique names and disjoint rows do not imply chemically independent materials. No framework-family split is claimed. The row-wise bootstrap is an illustration conditional on the fitted model and on treating rows as independently sampled units. It does not quantify uncertainty for new chemical families, different simulation protocols, or experimental adsorption.

Re-extract with `python scripts/build_mof_lab.py --source PATH_TO_PINNED_CHECKOUT` from the course directory. Re-extraction checks the source revision and clears the generated notebook's outputs; retain student work separately.
