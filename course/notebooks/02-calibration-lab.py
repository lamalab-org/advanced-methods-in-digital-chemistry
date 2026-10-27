import marimo

__generated_with = "0.25.2"
app = marimo.App(width="medium")


@app.cell
def _():
    import marimo as mo

    return (mo,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # Learning from a calibration experiment

    **Synthetic data, not laboratory results.** This notebook uses the same default data as the browser activity: seed 17 and noise standard deviation 0.055. It needs NumPy and Matplotlib. No data downloads, API keys, GPU, or LLM account are required.

    The purpose is to explain what changes when we fit a more flexible curve. Predict the effect of one change, inspect the result, and say which observations influenced the choice. By the end, you should be able to explain why a smaller training error need not mean better predictions for other measurements.

    We use validation data to explore model choices. This is not a final test-set evaluation. In a research project, reserve a separate final evaluation relevant to the intended use.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 1. Generate the observations
    Concentration `c` is in mmol/L. Absorbance `A` is dimensionless. The simulator assumes a linear relationship plus independent Gaussian noise. A real experiment may violate these assumptions.

    Identify which arrays contain training observations and which contain validation observations.
    """)
    return


@app.cell
def _():
    import numpy as np
    from numpy.polynomial import Polynomial
    import matplotlib.pyplot as plt

    # Synthetic teaching data, not experimental measurements.
    # concentration: mmol/L; absorbance: dimensionless.
    seed = 17
    noise = 0.055
    rng = np.random.default_rng(seed)
    c_train = np.linspace(0.02, 0.98, 12)
    A_train = 0.15 + 0.8 * c_train + rng.normal(0, noise, c_train.size)
    c_validation = np.linspace(0.04, 0.96, 17)
    A_validation = 0.15 + 0.8 * c_validation + rng.normal(0, noise, c_validation.size)
    return A_train, A_validation, Polynomial, c_train, c_validation, np, plt


@app.cell
def _(A_train, c_train, c_validation):
    print("Training observations:", len(c_train))
    print("Validation observations:", len(c_validation))
    print("First pair:", c_train[0], A_train[0])
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 2. Start with a baseline
    The mean of the training responses gives a constant prediction. Do not use validation responses to fit this baseline. Predict whether a line should improve on it in this simulation.
    """)
    return


@app.cell
def _(A_train, A_validation, mo, np):
    def mse(prediction, observation):
        return np.mean((prediction - observation) ** 2)

    baseline = A_train.mean()
    print("Baseline value:", baseline)
    print("Baseline training MSE:", mse(baseline, A_train))
    print("Baseline validation MSE:", mse(baseline, A_validation))
    mo.md(f"""
    | Constant baseline | MSE |
    |---|---:|
    | Training | {mse(baseline, A_train):.5f} |
    | Validation | {mse(baseline, A_validation):.5f} |
    """)
    return (mse,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 3. Fit a polynomial
    Predict what will happen, then move the degree slider from 1 to a larger value. The fit, errors, and plot update together. `Polynomial.fit` fits by least squares and uses a scaled coordinate internally to improve numerical conditioning. It receives only the training observations. The degree is a model choice; the coefficients are fitted parameters.
    """)
    return


@app.cell
def _(mo):
    degree_control = mo.ui.slider(1, 9, value=1, step=1, label="Polynomial degree", show_value=True)
    degree_control
    return (degree_control,)


@app.cell
def _(
    A_train,
    A_validation,
    Polynomial,
    c_train,
    c_validation,
    degree_control,
    mo,
    mse,
):
    degree = degree_control.value
    model = Polynomial.fit(c_train, A_train, degree)
    print("Training MSE:", mse(model(c_train), A_train))
    print("Validation MSE:", mse(model(c_validation), A_validation))
    mo.md(f"""
    **Degree {degree}**

    | Observations | MSE |
    |---|---:|
    | Training | {mse(model(c_train), A_train):.5f} |
    | Validation | {mse(model(c_validation), A_validation):.5f} |
    """)
    return degree, model


@app.cell
def _(A_train, A_validation, c_train, c_validation, degree, mo, model, np, plt):
    grid = np.linspace(0, 1.5, 181)
    fig, ax = plt.subplots(figsize=(8, 4))
    ax.axvspan(1, 1.5, color="#eee7ea", label="No observations")
    ax.scatter(c_train, A_train, label="Training", color="#236a9a", zorder=3)
    ax.scatter(c_validation, A_validation, marker="s", label="Validation", color="#a22d50", zorder=3)
    ax.plot(grid, model(grid), color="#32333c", label=f"Degree {degree}")
    ax.set(xlabel="Concentration / mmol L$^{-1}$", ylabel="Absorbance",
           xlim=(0, 1.5), ylim=(-0.15, 1.65), title="Synthetic calibration")
    ax.legend(loc="upper left")
    fig.tight_layout()
    plt.close(fig)
    # The fixed axis can clip extreme predictions. Inspect numbers below as well.
    print("Prediction at 1.4 mmol/L:", float(model(1.4)))
    mo.vstack([fig, mo.md(f"Prediction at 1.4 mmol/L: **{float(model(1.4)):.3f}**. The fixed vertical axis may clip extreme predictions.")])
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 4. Compare the model choices
    Before running, predict how the training error will change. Then compare with validation error. The validation measurements are being used for model selection, so their best score is not an unbiased final estimate for the selected procedure.
    """)
    return


@app.cell
def _(A_train, A_validation, Polynomial, c_train, c_validation, mse):
    comparison = []
    for d in range(1, 10):
        candidate = Polynomial.fit(c_train, A_train, d)
        train_error = mse(candidate(c_train), A_train)
        validation_error = mse(candidate(c_validation), A_validation)
        comparison.append((d, train_error, validation_error))
        print(f"degree={d}: train={train_error:.5f}, validation={validation_error:.5f}")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 5. One controlled change
    Change `noise` in the data-generating cell and run that cell with Shift+Enter. In automatic mode, marimo reruns the dependent calculations and plots. The fixed seed makes the comparison repeatable. Explain what happened to fitting and validation. This creates a new simulated experiment; it does not establish how a real instrument behaves.

    Extension: repeat several seeds. Is the same degree selected every time? Do not choose a seed simply because it gives your preferred conclusion.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 6. Check an assisted implementation
    The following function is deliberately flawed for mean squared error. Calculate its output for residuals +1 and -1 before running it. An LLM may help explain or fix the code, but you must execute an independent check.
    """)
    return


@app.cell
def _(mse, np):
    def flawed_score(prediction, observation):
        return ((prediction - observation).mean()) ** 2

    p = np.array([2.0, 0.0])
    y = np.array([1.0, 1.0])
    print("Flawed score:", flawed_score(p, y))
    print("Mean squared error:", mse(p, y))
    assert np.isclose(mse(p, y), 1.0)
    assert np.isclose(mse(y, y), 0.0)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Write a short interpretation
    1. State the model choice and the evidence for it.
    2. Explain which data fitted parameters and which data influenced model selection.
    3. State one assumption needed to use the calibration elsewhere.
    4. Propose an additional measurement or final evaluation.
    5. If you used an LLM, record a consequential suggestion and how you checked it.

    Save your work under a new filename. Before sharing, stop marimo with Ctrl+C in its terminal and reopen the saved file. Record your chosen slider value in your interpretation: a current widget setting is not a substitute for documenting the model choice.
    """)
    return


if __name__ == "__main__":
    app.run()
