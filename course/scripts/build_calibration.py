"""Build the shared synthetic calibration demonstration and student notebooks."""
from pathlib import Path
import json
import textwrap

import nbformat as nbf
import numpy as np
from numpy.polynomial import Polynomial

ROOT = Path(__file__).resolve().parents[1]
DATA_CODE = '''
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
'''
scope = {}
exec(DATA_CODE.replace('import matplotlib.pyplot as plt', ''), scope)
x, y = scope['c_train'], scope['A_train']
xv, yv = scope['c_validation'], scope['A_validation']
grid = np.linspace(0, 1.5, 181)
records = []
for degree in range(1, 10):
    model = Polynomial.fit(x, y, degree)
    records.append(dict(degree=degree, prediction=model(grid).tolist(),
                        train_mse=float(np.mean((model(x) - y)**2)),
                        validation_mse=float(np.mean((model(xv) - yv)**2))))
data = dict(seed=17, noise=0.055, grid=grid.tolist(),
            train=list(map(list, zip(x.tolist(), y.tolist()))),
            validation=list(map(list, zip(xv.tolist(), yv.tolist()))),
            baseline=float(y.mean()),
            baseline_train_mse=float(np.mean((y.mean()-y)**2)),
            baseline_validation_mse=float(np.mean((y.mean()-yv)**2)),
            models=records)
(ROOT/'activities/calibration-data.json').write_text(json.dumps(data, indent=2)+'\n')

HTML = r'''<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>Calibration: fitting and predicting</title>
<style>
*{box-sizing:border-box}body{font:16px/1.5 system-ui,sans-serif;color:#29242a;background:#fff;margin:0;padding:24px;max-width:960px}h1{font-size:25px;line-height:1.2;margin:0 0 8px}p{margin:8px 0 14px}.muted{color:#625963;font-size:14px}label{display:block;margin:12px 0}input[type=range]{width:min(380px,75%);vertical-align:middle;accent-color:#7d243b}input[type=checkbox]{accent-color:#7d243b}output{font-weight:700;color:#7d243b}svg{width:100%;height:auto;display:block;margin:8px 0}#scores{font-variant-numeric:tabular-nums;padding:12px 0;border-top:1px solid #ddd;border-bottom:1px solid #ddd}summary{cursor:pointer}table{border-collapse:collapse;margin-top:10px;font-size:14px}td,th{padding:5px 12px;border-bottom:1px solid #ddd;text-align:right}th:first-child,td:first-child{text-align:left}a{color:#7d243b}@media(max-width:540px){body{padding:16px}h1{font-size:22px}}
</style></head><body>
<h1>Fitting a calibration curve</h1>
<p>How much flexibility helps on measurements the model did not fit?</p>
<p class="muted">Synthetic absorbance data. Twelve training observations; seventeen validation observations. No experimental data or final test set.</p>
<label for="degree">Polynomial degree: <output id="degree-value" for="degree">1</output><br><input id="degree" type="range" min="1" max="9" step="1" value="1"></label>
<label><input id="validation" type="checkbox"> Reveal validation observations and their error</label>
<label><input id="extrapolate" type="checkbox"> Show predictions beyond the measured concentration range</label>
<svg id="plot" viewBox="0 0 780 340" role="img" aria-labelledby="plot-title plot-desc"><title id="plot-title">Synthetic calibration data and polynomial fit</title><desc id="plot-desc">Blue circles are training observations; burgundy squares are validation observations when revealed. The dark curve is a model prediction.</desc></svg>
<p id="scores" aria-live="polite"></p>
<p id="interpretation"></p>
<p class="muted">The axis scale is fixed: portions of extreme curves can leave the plot. The shaded region has no observations. It cannot validate extrapolation.</p>
<details><summary>Numerical model comparison</summary><p class="muted">Validation values appear after you reveal those observations. Using them to choose a degree makes this model selection, not final testing.</p><table id="comparison"></table></details>
<details><summary>What generated the data?</summary><p>Concentrations are in mmol/L. Absorbance was generated as 0.15 + 0.8 × concentration plus Gaussian noise with standard deviation 0.055, using NumPy seed 17. Each degree is fitted by least squares to the same training observations. These assumptions belong to this teaching simulation; a real calibration requires experimental checks.</p><p><a href="calibration-data.json" download>Download all data and precomputed curves</a></p></details>
<script>
const DATA = __DATA__;
const el = id => document.getElementById(id);
const NS='http://www.w3.org/2000/svg';
function add(parent,name,attrs,text){const n=document.createElementNS(NS,name);for(const [k,v] of Object.entries(attrs||{}))n.setAttribute(k,v);if(text!==undefined)n.textContent=text;parent.appendChild(n);return n;}
function update(){
 const d=Number(el('degree').value),show=el('validation').checked,extra=el('extrapolate').checked,m=DATA.models[d-1];
 el('degree-value').value=d;
 const svg=el('plot'); svg.querySelectorAll(':scope > g,:scope > defs').forEach(n=>n.remove());
 const left=64,right=755,top=18,bottom=282,xmax=extra?1.5:1.05,ymin=-.15,ymax=1.65;
 const X=x=>left+(right-left)*x/xmax,Y=y=>bottom-(bottom-top)*(y-ymin)/(ymax-ymin);
 const defs=add(svg,'defs'),clip=add(defs,'clipPath',{id:'bounds'});add(clip,'rect',{x:left,y:top,width:right-left,height:bottom-top});
 const g=add(svg,'g');
 if(extra){add(g,'rect',{x:X(1),y:top,width:X(1.5)-X(1),height:bottom-top,fill:'#f4eff1'});add(g,'text',{x:X(1.04),y:35,fill:'#6e4250','font-size':13},'No observations');}
 for(let a=0;a<=1.6;a+=.4){add(g,'line',{x1:left,y1:Y(a),x2:right,y2:Y(a),stroke:'#e8e4e6'});add(g,'text',{x:left-12,y:Y(a)+5,'text-anchor':'end','font-size':13,fill:'#514952'},a.toFixed(1));}
 for(let c=0;c<=xmax+.001;c+=.25){add(g,'line',{x1:X(c),y1:bottom,x2:X(c),y2:bottom+5,stroke:'#666'});add(g,'text',{x:X(c),y:bottom+23,'text-anchor':'middle','font-size':13,fill:'#514952'},c.toFixed(2));}
 add(g,'line',{x1:left,y1:bottom,x2:right,y2:bottom,stroke:'#555'});add(g,'line',{x1:left,y1:top,x2:left,y2:bottom,stroke:'#555'});
 add(g,'text',{x:410,y:332,'text-anchor':'middle','font-size':14},'Concentration / mmol L⁻¹');
 add(g,'text',{transform:'translate(18 155) rotate(-90)','text-anchor':'middle','font-size':14},'Absorbance');
 const marks=add(g,'g',{'clip-path':'url(#bounds)'});
 const path=DATA.grid.map((x,i)=>(i?'L':'M')+X(x).toFixed(3)+','+Y(m.prediction[i]).toFixed(3)).join(' ');
 add(marks,'path',{d:path,stroke:'#32333c','stroke-width':2.5,fill:'none'});
 for(const [x,y] of DATA.train)add(marks,'circle',{cx:X(x),cy:Y(y),r:5,fill:'#236a9a',stroke:'white','stroke-width':1});
 if(show)for(const [x,y] of DATA.validation)add(marks,'rect',{x:X(x)-4,y:Y(y)-4,width:8,height:8,fill:'#a22d50',stroke:'white','stroke-width':1});
 el('scores').textContent=`Degree ${d} · Training MSE: ${m.train_mse.toFixed(5)}`+(show?` · Validation MSE: ${m.validation_mse.toFixed(5)}`:' · Validation error hidden');
 el('interpretation').textContent=show?'Blue circles: training. Burgundy squares: validation. Which model would you choose, and what observation supports that choice?':'Blue circles: training. Predict what will happen on new observations before revealing them.';
 const table=el('comparison');table.replaceChildren();const head=table.createTHead().insertRow();for(const t of ['Model','Training MSE','Validation MSE']){const th=document.createElement('th');th.scope='col';th.textContent=t;head.append(th);}
 const body=table.createTBody();for(const rec of [{degree:'Mean baseline',train_mse:DATA.baseline_train_mse,validation_mse:DATA.baseline_validation_mse},...DATA.models]){const row=body.insertRow();for(const t of [typeof rec.degree==='number'?`Degree ${rec.degree}`:rec.degree,rec.train_mse.toFixed(5),show?rec.validation_mse.toFixed(5):'Hidden'])row.insertCell().textContent=t;}
}
['degree','validation','extrapolate'].forEach(id=>el(id).addEventListener('input',update));update();
</script></body></html>'''
(ROOT/'activities/calibration.html').write_text(HTML.replace('__DATA__',json.dumps(data)))

def md(s): return nbf.v4.new_markdown_cell(textwrap.dedent(s).strip())
def code(s): return nbf.v4.new_code_cell(textwrap.dedent(s).strip())
def notebook(cells, path):
    nb = nbf.v4.new_notebook(cells=cells)
    nb.metadata.kernelspec = dict(display_name='Python 3', language='python', name='python3')
    nb.metadata.language_info = dict(name='python', version='3')
    nbf.validate(nb)
    nbf.write(nb, path)

notebook([
md('''# Getting started: a chemical calculation

This notebook uses only built-in Python. The observations are synthetic. Run cells from top to bottom, change one value, then restart the kernel and run all cells.

**Goal:** explain what a cell does and verify a small result. No LLM account is required.'''),
md('''## 1. A prediction
Concentration is in mmol/L. Absorbance is dimensionless. Before running the cell, calculate the expected result for concentration 0.5.'''),
code('''concentration = 0.5
slope = 0.8  # L/mmol
intercept = 0.15
prediction = slope * concentration + intercept
print("Predicted absorbance:", prediction)'''),
md('''Change the concentration to 1.0. Predict the result first. What happens if you execute a later cell before rerunning this one?'''),
md('''## 2. Several observations
A list stores several values. `zip` pairs corresponding entries. Here the equal-length lists have one prediction and one observation per sample.'''),
code('''concentrations = [0.0, 0.5, 1.0]
observations = [0.16, 0.52, 0.98]
predictions = [slope * c + intercept for c in concentrations]
for c, observed, predicted in zip(concentrations, observations, predictions):
    print(f"c={c:.2f}, observed={observed:.2f}, predicted={predicted:.2f}")'''),
md('''## 3. Quantify the errors
Calculate the first residual by hand. Which line squares each residual? Which line averages?'''),
code('''residuals = [p - y for p, y in zip(predictions, observations)]
squared_errors = [e ** 2 for e in residuals]
mse = sum(squared_errors) / len(squared_errors)
print("Residuals:", residuals)
print("Mean squared error:", mse)'''),
md('''## 4. A small check on assisted code
The function below is deliberately flawed if we intend it to calculate mean squared error. Use predictions `[2, 0]` and observations `[1, 1]`. Calculate the result by hand before asking an LLM for help.'''),
code('''def flawed_score(prediction, observation):
    residuals = [p - y for p, y in zip(prediction, observation)]
    return (sum(residuals) / len(residuals)) ** 2

print("Flawed score:", flawed_score([2, 0], [1, 1]))'''),
md('''**Your task:** write a corrected version below. Then test it on an exact prediction and on the two residuals +1 and -1. The expected mean squared errors are 0 and 1 respectively. Explain why cancellation was a problem.'''),
code('''# Add your corrected function and the two checks here.'''),
md('''## Exit check
- Restart the kernel and run all cells.
- Explain one line to your partner.
- Record green (runs and understood), amber (runs, still unclear), or red (cannot run).
- If you used an LLM, record its relevant suggestion and the independent check you performed.

The next notebook introduces NumPy and Matplotlib. This first notebook does not require them.''')
], ROOT/'notebooks/00-getting-started.ipynb')

notebook([
md('''# Learning from a calibration experiment

**Synthetic data, not laboratory results.** This notebook uses the same default data as the browser activity: seed 17 and noise standard deviation 0.055. It needs NumPy and Matplotlib. No data downloads, API keys, GPU, or LLM account are required.

We use validation data to explore model choices. This is not a final test-set evaluation. In a research project, reserve a separate final evaluation relevant to the intended use.'''),
md('''## 1. Generate the observations
Concentration `c` is in mmol/L. Absorbance `A` is dimensionless. The simulator assumes a linear relationship plus independent Gaussian noise. A real experiment may violate these assumptions.

Identify which arrays contain training observations and which contain validation observations.'''),
code(DATA_CODE),
code('''print("Training observations:", len(c_train))
print("Validation observations:", len(c_validation))
print("First pair:", c_train[0], A_train[0])'''),
md('''## 2. Start with a baseline
The mean of the training responses gives a constant prediction. Do not use validation responses to fit this baseline. Predict whether a line should improve on it in this simulation.'''),
code('''def mse(prediction, observation):
    return np.mean((prediction - observation) ** 2)

baseline = A_train.mean()
print("Baseline value:", baseline)
print("Baseline training MSE:", mse(baseline, A_train))
print("Baseline validation MSE:", mse(baseline, A_validation))'''),
md('''## 3. Fit a polynomial
Change `degree` from 1 to a larger value. `Polynomial.fit` fits by least squares and uses a scaled coordinate internally to improve numerical conditioning. It receives only the training observations. The degree is a model choice; the coefficients are fitted parameters.'''),
code('''degree = 1
model = Polynomial.fit(c_train, A_train, degree)
print("Training MSE:", mse(model(c_train), A_train))
print("Validation MSE:", mse(model(c_validation), A_validation))'''),
code('''grid = np.linspace(0, 1.5, 181)
fig, ax = plt.subplots(figsize=(8, 4))
ax.axvspan(1, 1.5, color="#eee7ea", label="No observations")
ax.scatter(c_train, A_train, label="Training", color="#236a9a", zorder=3)
ax.scatter(c_validation, A_validation, marker="s", label="Validation", color="#a22d50", zorder=3)
ax.plot(grid, model(grid), color="#32333c", label=f"Degree {degree}")
ax.set(xlabel="Concentration / mmol L$^{-1}$", ylabel="Absorbance",
       xlim=(0, 1.5), ylim=(-0.15, 1.65), title="Synthetic calibration")
ax.legend(loc="upper left")
fig.tight_layout()
plt.show()
# The fixed axis can clip extreme predictions. Inspect numbers below as well.
print("Prediction at 1.4 mmol/L:", float(model(1.4)))'''),
md('''## 4. Compare the model choices
Before running, predict how the training error will change. Then compare with validation error. The validation measurements are being used for model selection, so their best score is not an unbiased final estimate for the selected procedure.'''),
code('''comparison = []
for d in range(1, 10):
    candidate = Polynomial.fit(c_train, A_train, d)
    train_error = mse(candidate(c_train), A_train)
    validation_error = mse(candidate(c_validation), A_validation)
    comparison.append((d, train_error, validation_error))
    print(f"degree={d}: train={train_error:.5f}, validation={validation_error:.5f}")'''),
md('''## 5. One controlled change
Change the `noise` value in the first code cell and run all cells again. Explain what happened to fitting and validation. This creates a new simulated experiment; it does not establish how a real instrument behaves.

Extension: repeat several seeds. Is the same degree selected every time? Do not choose a seed simply because it gives your preferred conclusion.'''),
md('''## 6. Check an assisted implementation
The following function is deliberately flawed for mean squared error. Calculate its output for residuals +1 and -1 before running it. An LLM may help explain or fix the code, but you must execute an independent check.'''),
code('''def flawed_score(prediction, observation):
    return ((prediction - observation).mean()) ** 2

p = np.array([2.0, 0.0])
y = np.array([1.0, 1.0])
print("Flawed score:", flawed_score(p, y))
print("Mean squared error:", mse(p, y))
assert np.isclose(mse(p, y), 1.0)
assert np.isclose(mse(y, y), 0.0)'''),
md('''## Submit a short interpretation
1. State the model choice and the evidence for it.
2. Explain which data fitted parameters and which data influenced model selection.
3. State one assumption needed to use the calibration elsewhere.
4. Propose an additional measurement or final evaluation.
5. If you used an LLM, record a consequential suggestion and how you checked it.

Restart the kernel and run all cells before sharing the notebook. Save your work under a new filename.''')
], ROOT/'notebooks/02-calibration-lab.ipynb')
print('Built calibration activity, shared data, and two student notebooks.')
