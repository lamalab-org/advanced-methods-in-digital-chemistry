"""Build the shared synthetic calibration demonstration and its data."""
from pathlib import Path
import json

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
</style><link rel="stylesheet" href="../assets/activities.css"></head><body>
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

print('Built calibration activity and shared data. Edit the marimo notebooks directly.')
