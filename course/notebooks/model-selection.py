import marimo

__generated_with = "0.25.2"
app = marimo.App(width="medium")


@app.cell
def _():
    import marimo as mo
    import numpy as np
    import matplotlib.pyplot as plt
    from sklearn.pipeline import make_pipeline
    from sklearn.preprocessing import FunctionTransformer, PolynomialFeatures, StandardScaler
    from sklearn.linear_model import Ridge
    from sklearn.model_selection import KFold

    return FunctionTransformer, KFold, PolynomialFeatures, Ridge, StandardScaler, make_pipeline, mo, np, plt


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # How should we choose a model?

    We want to explain **why** a fit changes, then choose its settings using
    observations excluded from that fit. First compare underfitting, variation
    across training datasets, and regularisation. Then trace five-fold
    cross-validation. The smallest training error will not settle the choice.

    We return to **fitting a Lennard–Jones potential**, an example from my
    [MolSim lecture, p. 37](https://www.compchem.nl/wp-content/uploads/molsim2023/L09_Machine-Learning.pdf#page=37).
    Two particles have a separation $r$ and an interaction energy $U$.
    Put $s=r/\sigma$ and express energy in units of $\epsilon$:

    $$u(s)=U(r)/\epsilon=4(s^{-12}-s^{-6}).$$

    Here $\sigma$ is the separation where the energy is zero, and $\epsilon$
    is the depth of the well. We compute energies for $1\leq s\leq1.8$ and add
    artificial noise. The equation itself is deterministic. We fit polynomials
    to these noisy values; we are not fitting $\sigma$ or $\epsilon$.
    Knowing the reference curve lets us examine errors we could not identify
    from an ordinary dataset alone. This is a new implementation of the MolSim
    teaching example, with generated data and no final test score.
    """)
    return


@app.cell
def _(FunctionTransformer, PolynomialFeatures, Ridge, StandardScaler, make_pipeline):
    def reference_energy(s):
        return 4 * (s**-12 - s**-6)

    def new_model(degree, penalty, n_train):
        # Ridge uses a sum of squared errors. alpha=n_train*penalty gives
        # mean squared error + penalty*sum(w_j**2). The intercept is unpenalised.
        # Every call creates a new scaler and model; both fit on training only.
        return make_pipeline(
            # Fixed coordinate choice for the stated interval, not estimated
            # from data: s in [1, 1.8] becomes z in [-1, 1].
            FunctionTransformer(lambda s: (s - 1.4) / 0.4),
            PolynomialFeatures(degree=degree, include_bias=False),
            StandardScaler(),
            Ridge(alpha=n_train * penalty, solver="svd"),
        )

    return reference_energy, new_model


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 1. Repeat the measurements, then repeat the fit

    We generate **80 datasets of 18 energy values**, at the same separations,
    with independent Gaussian errors of standard deviation 0.06 in $U/\epsilon$.
    Keep the penalty at zero and compare degrees 1, 5, and 9. Then hold degree 9
    fixed and increase the penalty. Predict each change first.

    Bias concerns the average prediction relative to the reference energy.
    Variance concerns how predictions differ between training datasets. The
    curves, their average, and the error terms all use the same simulated runs.
    We use powers of $z=(s-1.4)/0.4$ as features, then standardise each feature
    within the fit. This fixed change of coordinate improves numerical
    conditioning. The penalty refers to coefficients in this chosen representation.
    """)
    return


@app.cell
def _(mo):
    degree_control = mo.ui.slider(1, 9, value=5, step=1, show_value=True, label="Degree")
    penalty_control = mo.ui.slider(
        steps=[0.0, 0.0001, 0.001, 0.01, 0.1, 1.0],
        value=0.0, show_value=True, label="Penalty strength lambda",
    )
    mo.vstack([degree_control, penalty_control])
    return degree_control, penalty_control


@app.cell
def _(reference_energy, np):
    noise_sd = 0.06
    repeated_x = np.linspace(1.0, 1.8, 18)
    grid = np.linspace(1.0, 1.8, 151)
    repeated_y = reference_energy(repeated_x)[None, :] + np.random.default_rng(2026).normal(
        0, noise_sd, size=(80, len(repeated_x))
    )
    return grid, noise_sd, repeated_x, repeated_y


@app.cell
def _(degree_control, grid, reference_energy, new_model, noise_sd, np,
      penalty_control, repeated_x, repeated_y):
    predictions = []
    training_errors = []
    for _responses in repeated_y:
        _model = new_model(degree_control.value, penalty_control.value, len(repeated_x))
        _model.fit(repeated_x[:, None], _responses)
        predictions.append(_model.predict(grid[:, None]))
        training_errors.append(np.mean((_model.predict(repeated_x[:, None]) - _responses)**2))
    predictions = np.asarray(predictions)
    average_prediction = predictions.mean(axis=0)
    bias_squared = np.mean((average_prediction - reference_energy(grid))**2)
    prediction_variance = np.mean(predictions.var(axis=0, ddof=0))
    expected_error_estimate = bias_squared + prediction_variance + noise_sd**2
    return (average_prediction, bias_squared, expected_error_estimate,
            prediction_variance, predictions, training_errors)


@app.cell
def _(average_prediction, bias_squared, degree_control, expected_error_estimate,
      grid, reference_energy, mo, noise_sd, np, penalty_control, plt,
      prediction_variance, predictions, training_errors):
    _fig, _axes = plt.subplots(1, 2, figsize=(10, 4))
    for _index, _prediction in enumerate(predictions[:12]):
        _axes[0].plot(grid, _prediction, color="#842c43", alpha=0.2,
                      label="Individual fits (12 shown)" if _index == 0 else None)
    _axes[0].plot(grid, average_prediction, color="#842c43", lw=2, label="Mean of 80 fits")
    _axes[0].plot(grid, reference_energy(grid), color="#17252f", ls="--", label="Lennard–Jones reference")
    _axes[0].set(xlabel=r"Separation $r/\sigma$", ylabel=r"Energy $U/\epsilon$",
                 title=f"Degree {degree_control.value}; lambda={penalty_control.value:g}")
    _axes[0].legend(fontsize=8)
    _axes[1].bar(["Squared bias", "Variance", "Noise"],
                 [bias_squared, prediction_variance, noise_sd**2],
                 color=["#842c43", "#186d74", "#89979f"])
    _axes[1].set(ylabel=r"Squared error in $U/\epsilon$", title="Average over the plotted input grid")
    _fig.tight_layout()
    plt.close(_fig)
    mo.vstack([_fig, mo.md(f"""
    | Quantity | Value |
    |---|---:|
    | Average training MSE | {np.mean(training_errors):.6f} |
    | Estimated squared bias | {bias_squared:.6f} |
    | Estimated prediction variance | {prediction_variance:.6f} |
    | Known conditional noise variance | {noise_sd**2:.6f} |
    | Sum of the three error terms | {expected_error_estimate:.6f} |

    The first two error terms use 80 fits, so they are Monte Carlo estimates.
    Their sum plus the known noise variance estimates expected squared error
    for a fresh response, averaged uniformly over this input grid, for this
    fixed design of training separations. It is **not an observed test MSE**
    and is not necessarily comparable to a training error averaged at other
    separations. These are errors relative to our chosen potential with added
    noise. They do not establish accuracy for a real substance, for forces,
    or outside the fitted interval.
    """)])
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 2. Choose settings when we have only one dataset

    Now use **60 new, independent development observations** with separations
    $r/\sigma$ sampled uniformly between 1 and 1.8. This is a separate dataset from
    the repeated-measurement exercise. The generating function will not be used
    to score candidates. The observations must provide our comparison.

    Each row in the diagram below is a new fit. Purple marks its validation
    observations; grey marks its training observations. Follow one column:
    when may that observation's target enter fitting? Each candidate gets the
    same five splits. Changing the assignment is still development work; do
    not search for a split that makes a preferred model win.
    """)
    return


@app.cell
def _(reference_energy, noise_sd, np):
    _rng = np.random.default_rng(107)
    development_x = _rng.uniform(1.0, 1.8, 60)
    development_y = reference_energy(development_x) + _rng.normal(0, noise_sd, 60)
    return development_x, development_y


@app.cell
def _(mo):
    fold_seed_control = mo.ui.slider(0, 9, value=0, step=1,
                                    show_value=True, label="Fold assignment seed")
    fold_seed_control
    return (fold_seed_control,)


@app.cell
def _(KFold, development_x, fold_seed_control, np, plt):
    folds = list(KFold(n_splits=5, shuffle=True,
                      random_state=fold_seed_control.value).split(development_x))
    _membership = np.zeros((5, len(development_x)))
    for _row, (_train, _validation) in enumerate(folds):
        _membership[_row, _validation] = 1
    from matplotlib.colors import ListedColormap

    _fig, _ax = plt.subplots(figsize=(10, 2.5))
    _ax.imshow(_membership, cmap=ListedColormap(["#d4dce0", "#842c43"]),
               aspect="auto", interpolation="nearest", vmin=0, vmax=1)
    _ax.set(xlabel="Observation index (the same columns in every row)", ylabel="Fit",
            yticks=range(5), yticklabels=range(1, 6),
            title="Grey: train. Purple: validate. Each observation is validated once.")
    _fig.tight_layout()
    plt.close(_fig)
    _fig
    return (folds,)


@app.cell
def _(development_x, development_y, folds, new_model, np):
    cv_results = []
    for _degree in (1, 2, 5, 9):
        for _penalty in (0.0, 0.001, 0.01, 0.1):
            _errors = []
            for _train, _validation in folds:
                _candidate = new_model(_degree, _penalty, len(_train))
                _candidate.fit(development_x[_train, None], development_y[_train])
                _predicted = _candidate.predict(development_x[_validation, None])
                _errors.append(float(np.mean((_predicted - development_y[_validation])**2)))
            cv_results.append({"Degree": _degree, "Lambda": _penalty,
                               **{f"Fold {i+1}": error for i, error in enumerate(_errors)},
                               "Mean MSE": float(np.mean(_errors))})
    cv_results.sort(key=lambda row: row["Mean MSE"])
    chosen = cv_results[0]
    return chosen, cv_results


@app.cell
def _(chosen, cv_results, mo):
    mo.vstack([mo.ui.table(cv_results, selection=None), mo.md(f"""
    The smallest mean validation MSE is **{chosen['Mean MSE']:.6f}**, for degree
    **{chosen['Degree']}** and lambda **{chosen['Lambda']:g}**. We used these scores
    to select the setting. They are not an untouched final evaluation of it.
    Each fold contains 12 validation rows and 48 training rows. Their equal
    sizes justify taking the unweighted mean of the five MSEs.

    The folds share training data. The spread of their five scores is not
    automatically a confidence interval. Changing the seed reorganises the
    same 60 measurements; it does not provide 60 new ones.
    """)])
    return


@app.cell
def _(chosen, development_x, development_y, new_model):
    selected_model = new_model(chosen["Degree"], chosen["Lambda"], len(development_x))
    selected_model.fit(development_x[:, None], development_y)
    return (selected_model,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 3. What evidence is still missing?

    We refitted the chosen procedure on all 60 development observations. We
    have **not evaluated this refit on a final test set**. That would require
    independent reserved observations relevant to the intended use, or an outer
    evaluation that repeats the whole selection procedure inside each training
    portion. Its result would still be an empirical error estimate.

    Explain why the scaler is created inside every fit. Then imagine that the
    rows are repeated measurements of ten molecules. Would random folds answer
    a question about an eleventh molecule? Which observations should remain
    together? Name the information you would need before implementing that split.

    If you use an assistant, ask it to trace one fold's inputs to the scaler,
    model, and score. Check the indexing yourself. A function named
    `cross_validate` would not establish that the split answers our chemical question.

    **Leave with:** one justified choice, one limitation of its evaluation,
    and one check you would use in your project. See the course notes for
    [the reasoning and suggested references](https://lamalab-org.github.io/advanced-methods-in-digital-chemistry/lectures/model-selection.html).
    """)
    return


if __name__ == "__main__":
    app.run()
