#!/usr/bin/env python3
"""Compare only validated feature-off metadata extensions; no numerical tolerance."""
from pathlib import Path
import json,hashlib,sys
p=Path(sys.argv[1]);b=Path(sys.argv[2]);rows=[]
for day in ['day30','day60','day90']:
 for suffix in ['', '.uninterrupted.json','.restored.json']:
  bp=b/day/('arm-0.json'+suffix);cp=p/(day+'-arm-0.json'+suffix);x=json.loads(bp.read_text());y=json.loads(cp.read_text())
  assert y['version']==10 and y['origin']['model_revision']==9
  assert y['origin']['cohort_encoding']==x['origin']['cohort_encoding']=='sparse_indexed'
  assert y['origin'].pop('root_config')==dict(enabled=False,law=0,conductance=1)
  assert y['origin'].pop('root_soil')==[]
  for cell in y['origin']['cells']:
   for entry in cell['sparse']:assert entry['value'].pop('root_fraction')==0
  y['version']=6;y['origin']['model_revision']=5
  a=json.dumps(x,sort_keys=True,separators=(',',':'),allow_nan=False);c=json.dumps(y,sort_keys=True,separators=(',',':'),allow_nan=False)
  row=dict(day=day,suffix=suffix,equal=a==c,baseline_sha256=hashlib.sha256(bp.read_bytes()).hexdigest(),candidate_sha256=hashlib.sha256(cp.read_bytes()).hexdigest());rows.append(row)
  if a!=c:
   mismatches=[]
   def diff(u,v,path=''):
    if isinstance(u,dict) and isinstance(v,dict):
     for k in sorted(set(u)|set(v)):
      if k not in u or k not in v:mismatches.append([path+'.'+k,'missing'])
      else:diff(u[k],v[k],path+'.'+k)
    elif isinstance(u,list) and isinstance(v,list):
     if len(u)!=len(v):mismatches.append([path,'length',len(u),len(v)])
     for i,(aa,bb) in enumerate(zip(u,v)):diff(aa,bb,path+'['+str(i)+']')
    elif json.dumps(u)!=json.dumps(v):mismatches.append([path,u,v])
   diff(x,y);row['first_differences']=mismatches[:20];row['difference_count']=len(mismatches)
  print(day,suffix,a==c)
(p/'off-parity.json').write_text(json.dumps(rows,indent=2)+'\n')
assert all(r['equal'] for r in rows),rows
