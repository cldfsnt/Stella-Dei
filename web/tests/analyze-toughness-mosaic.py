#!/usr/bin/env python3
from pathlib import Path
import json,sys,hashlib,re
root=Path(sys.argv[1]);lines=(root/'run.log').read_text().splitlines()
days=[json.loads(l.split('MOSAIC_DAY ',1)[1])for l in lines if l.startswith('MOSAIC_DAY ')]
patches=[json.loads(l.split('MOSAIC_PATCH ',1)[1])for l in lines if l.startswith('MOSAIC_PATCH ')]
assert len(days)==28
assert sum(l.startswith('MOSAIC_PASS ')for l in lines)==4
assert 'MOSAIC_ORIGINAL_RESTORED' in lines
events=[];active=None
for line in lines:
 if line.startswith('MOSAIC_GATES '):active=int(re.search(r'arm=(\d+)',line)[1])
 elif active is not None and line.startswith('MOSAIC_COLONIZE '):
  fields=dict(x.split('=',1)for x in line.split()[1:]);fields['arm']=active;events.append(fields)
 elif line.startswith('MOSAIC_DAY ') and json.loads(line.split(' ',1)[1])['day']==7:active=None
results={'events':events,'days':days,'patches':patches,'arms':[],'snapshots':[]}
for arm in range(4):
 start=json.loads((root/f'arm-{arm}-start.json').read_text());end=json.loads((root/f'arm-{arm}-end.json').read_text())
 assert start['format']==end['format']=='sandbox-toughness-v1'
 assert start['law']==end['law']==1 and not start['mutation_enabled'] and not end['mutation_enabled']
 for value in [start,end]:
  assert len(value['state']['plants'])==len(value['state']['vegetation'])==40962
  assert all('toughness' in p and p['toughness'] in [0,.5] for p in value['state']['plants'])
 groups=[]
 for d in [0,.5]:
  ids=[i for i,(v,p) in enumerate(zip(start['state']['vegetation'],start['state']['plants'])) if v>0 and p['toughness']==d]
  groups.append({'d':d,'patches':len(ids),'cover':sum(start['state']['vegetation'][i]for i in ids),'temperature_min':min(start['state']['temperature'][i]for i in ids),'temperature_max':max(start['state']['temperature'][i]for i in ids)})
 results['arms'].append({'arm':arm,'initial':groups,'final':next(x for x in days if x['arm']==arm and x['day']==7)})
 for stage in ['start','end']:
  p=root/f'arm-{arm}-{stage}.json';results['snapshots'].append({'path':str(p),'sha256':hashlib.sha256(p.read_bytes()).hexdigest(),'bytes':p.stat().st_size})
for x in days:assert x['credit']<=150*x['removed']
(root/'results.json').write_text(json.dumps(results,indent=2)+'\n')
print(json.dumps(results['arms'],indent=2))
