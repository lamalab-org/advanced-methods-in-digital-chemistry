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
    # Getting started: a chemical calculation

    The calculations use only built-in Python; marimo displays the notebook. The observations are synthetic. Read from top to bottom, then change one value and follow its effect through the dependent cells.

    **Goal:** explain what a cell does and verify a small result. We use numbers that can be checked by hand so that a running program and a correct calculation can be judged separately. No LLM account is required.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 1. A prediction
    Concentration is in mmol/L. Absorbance is dimensionless. Before running the cell, calculate the expected result for concentration 0.5.
    """)
    return


@app.cell
def _():
    concentration = 0.5
    slope = 0.8  # L/mmol
    intercept = 0.15
    return concentration, intercept, slope


@app.cell
def _(concentration, intercept, slope):
    prediction = slope * concentration + intercept
    print("Predicted absorbance:", prediction)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Change the concentration to 1.0. Predict the result first, then run the edited cell with Shift+Enter. In automatic mode, marimo also reruns the prediction cell because it uses `concentration`. Does the table below change? It uses a separate list of concentrations. Now change `slope`: which results should change?

    A notebook-wide name is defined in one cell. Edit that definition rather than assigning the same name in another cell.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 2. Several observations
    A list stores several values. `zip` pairs corresponding entries. Here the equal-length lists have one prediction and one observation per sample.
    """)
    return


@app.cell
def _(intercept, slope):
    concentrations = [0.0, 0.5, 1.0]
    observations = [0.16, 0.52, 0.98]
    predictions = [slope * c + intercept for c in concentrations]
    for c, observed, predicted in zip(concentrations, observations, predictions):
        print(f"c={c:.2f}, observed={observed:.2f}, predicted={predicted:.2f}")
    return observations, predictions


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 3. Quantify the errors
    Calculate the first residual by hand. Which line squares each residual? Which line averages?
    """)
    return


@app.cell
def _(observations, predictions):
    residuals = [p - y for p, y in zip(predictions, observations)]
    squared_errors = [e ** 2 for e in residuals]
    mse = sum(squared_errors) / len(squared_errors)
    print("Residuals:", residuals)
    print("Mean squared error:", mse)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 4. A small check on assisted code
    The function below is deliberately flawed if we intend it to calculate mean squared error. Use predictions `[2, 0]` and observations `[1, 1]`. Calculate the result by hand before asking an LLM for help.
    """)
    return


@app.cell
def _():
    def flawed_score(prediction, observation):
        residuals = [p - y for p, y in zip(prediction, observation)]
        return (sum(residuals) / len(residuals)) ** 2

    print("Flawed score:", flawed_score([2, 0], [1, 1]))
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    **Your task:** write a corrected version below. Then test it on an exact prediction and on the two residuals +1 and -1. The expected mean squared errors are 0 and 1 respectively. Explain why cancellation was a problem.
    """)
    return


@app.cell
def _():
    def corrected_score(prediction, observation):
        # Replace this placeholder, then call the function on your two checks.
        return None
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Exit check
    - Save your copy. Stop marimo with Ctrl+C in its terminal, then reopen the saved file with the same launch command and check that it runs.
    - Explain one line to your partner.
    - Record green (runs and understood), amber (runs, still unclear), or red (cannot run).
    - If you used an LLM, record its relevant suggestion and the independent check you performed.

    The next notebook introduces NumPy and Matplotlib. This first notebook does not require them.
    """)
    return


if __name__ == "__main__":
    app.run()
