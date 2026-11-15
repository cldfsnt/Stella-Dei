#!/usr/bin/env python3
from pathlib import Path
import json,hashlib,struct
p=Path(__file__).resolve().parents[3]/'site-tmp/origin-land-gate';out={}
for name in ['natural','warm']:
 b=(p/f'baseline-{name}.json').read_bytes();c=(p/f'candidate-{name}.json').read_bytes();bj=json.loads(b);cj=json.loads(c)
 if cj['origin'] is not None:
  for old,new in zip(bj['origin']['cells'],cj['origin']['cells']):
   if 'cohorts'not in old and 'cohorts'in new:assert new.pop('cohorts')==[]
 assert bj==cj,(name,'old value mismatch')
 out[name]={'raw_bytes_equal':b==c,'old_values_equal_empty_cohorts_representation_only':True,'sha256':hashlib.sha256(c).hexdigest(),'bytes':len(c)}
a=(p/'beta2plus2.json').read_bytes();b=(p/'beta4.json').read_bytes();assert a==b,'fresh process continuation differs'
x=json.loads(b);cfg=x['beta_origin'];assert cfg['config']['enabled']
for v in cfg['soil']:assert 0<=v<=1
for v in cfg['vapor']:assert 0<=v<=3.4028234663852886e38
assert all(not cell['sparse'] for cell in x['origin']['cells'])
out['beta']={'fresh_process_2plus2_equals4':True,'sha256':hashlib.sha256(b).hexdigest(),'bytes':len(b),'positive_soil_empty_patches':sum(v>0 for v in cfg['soil']),'soil_density_sum_kg_per_m2':sum(cfg['soil']),'max_soil_kg_per_m2':max(cfg['soil']),'non_f32_vapor_cells':sum(struct.unpack('<f',struct.pack('<f',v))[0]!=v for v in cfg['vapor']),'no_cohorts_or_assigned_roots':True}
print(json.dumps(out,indent=2))
