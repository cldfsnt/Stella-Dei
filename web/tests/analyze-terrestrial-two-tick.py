#!/usr/bin/env python3
"""Exact stored-binary target phase ledger; observational, no model corrections."""
import json,sys
from pathlib import Path
from fractions import Fraction as F
p=Path(sys.argv[1]);lines=p.read_text().splitlines();columns=[];ends={};before={}
for line in lines:
 if line.startswith('TERRESTRIAL_AFTER '):
  x=json.loads(line.split(' ',1)[1]);ends[x['arm']]=x
 if line.startswith('TERRESTRIAL_BEFORE '):
  x=json.loads(line.split(' ',1)[1]);before.setdefault(x['arm'],x)
 if not line.startswith('TERRESTRIAL_COLUMN '):continue
 x=json.loads(line.split(' ',1)[1]);b=x['before'];a=F(x['area']);legs=[]
 for name,s in zip(['standing_evaporation','soil_evaporation','condensation','infiltration','drainage'],x['result']['stages']):
  soil=(F(s['soil'])-F(b['soil']))*a;liq=(F(s['liquid'])-F(b['liquid']))*10**9;vap=(F(s['vapor'])-F(b['vapor']))*10**9
  residual=soil+liq+vap
  row=dict(phase=name,soil_delta_kg=float(soil),liquid_delta_kg=float(liq),vapor_delta_kg=float(vap),residual_kg=float(residual),exact_residual=str(residual))
  if name=='soil_evaporation' and soil<0:
   relative=abs(residual)/(-soil);row['relative_source_error']=float(relative);assert relative<=F(1,2**20)
  if name=='infiltration':assert soil<=-liq
  legs.append(row);b=s
 columns.append(dict(dt=x['dt'],before=x['before'],request_native=x['result']['request_native'],legs=legs))
assert 'TERRESTRIAL_GATE_COMPLETE no_long_run=true legacy_import_zero=true' in lines
out=dict(columns=columns,endpoints=ends,initial=before,root_pulse_lines=sum(x.startswith('VAPOR_ROOT ') for x in lines),scope='Exact binary-value phase residuals, not whole-world closure; native mass unit 1e9kg.')
print(json.dumps(out,indent=2))
