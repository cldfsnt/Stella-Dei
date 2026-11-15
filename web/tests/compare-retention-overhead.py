#!/usr/bin/env python3
"""Exact old-state comparison; reject nonzero hydration instead of stripping it."""
import json,sys,hashlib
from pathlib import Path
p=Path(sys.argv[1]);a=json.loads((p/'baseline/endpoint.json').read_text());b=json.loads((p/'candidate/endpoint.json').read_text())
assert b['version']==8 and a['version']==6
b['version']=a['version'];o=b['origin'];assert o.pop('retention_mutation')=={'law':0,'enabled':False,'stream_seed':0};assert o['model_revision']==7;o['model_revision']=a['origin']['model_revision']
for cell in o['cells']:
 for name in ['liquid_return','vapor_return']:assert cell.pop(name,0)==0
 for entry in cell.get('sparse',[]):
  c=entry['value']
  for name in ['retention_allocation','stored_water']:assert c.pop(name,0)==0
assert a==b,'OLD STATE OR RNG DIFFERS'
print(json.dumps({'exact_old_state_rng':True,'normalization':'version/model_revision/default config and explicitly zero new material fields only','hashes':{x:hashlib.sha256((p/x/'endpoint.json').read_bytes()).hexdigest() for x in ['baseline','candidate']}},indent=2))
