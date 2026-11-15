#!/usr/bin/env python3
import json,sys,hashlib
from pathlib import Path
p=Path(sys.argv[1]);rows=p.read_text().splitlines();a={i:{k:[]for k in ['before','after','loss','potential','cap','flux']}for i in range(2)};arm=None;wait=[];setup=None;fates=[]
for l in rows:
 if l.startswith('DAYLIGHT_WAIT '):wait.append(json.loads(l.split(' ',1)[1]))
 if l.startswith('TERRESTRIAL_SETUP '):setup=json.loads(l.split(' ',1)[1])
 if l.startswith('MATURE_FATE '):fates.append(json.loads(l.split(' ',1)[1]))
 if l.startswith('TERRESTRIAL_BEFORE '):
  x=json.loads(l.split(' ',1)[1]);arm=x['arm'];a[arm]['before'].append(x)
 elif l.startswith('TERRESTRIAL_AFTER '):a[arm]['after'].append(json.loads(l.split(' ',1)[1]))
 else:
  for tag,k in [('BUDGET_LOSS','loss'),('BUDGET_POTENTIAL','potential'),('BUDGET_CAP','cap'),('BUDGET_FLUX','flux')]:
   if l.startswith(tag+' '):a[arm][k].append(json.loads(l.split(' ',1)[1]))
assert wait[-1]['biological_light']>0 and all(x['biological_light']==0 for x in wait[:-1])
assert len(fates)==2
out=[]
for i,d in a.items():
 assert all(len(d[k])==60 for k in ['before','after','cap','flux'])
 out.append(dict(arm=i,start_mass=d['before'][0]['cohort']['biomass'],end_mass=d['after'][-1]['cohort']['biomass'],fixed=sum(x['flux']['fixed']for x in d['flux']),upkeep=sum(x['upkeep']for x in d['loss']),hydrated_ticks=sum(x['hydrated']>0 for x in d['loss']),positive_fixation_ticks=sum(x['flux']['fixed']>0 for x in d['flux']),first_two=[dict(loss=d['loss'][j],flux=d['flux'][j]['flux'])for j in range(2)],depth_start=d['before'][0]['depth_m'],depth_first=d['after'][0]['depth_m'],depth_end=d['after'][-1]['depth_m'],max_mass=max(x['cohort']['biomass']for x in d['after']),fate=fates[i]))
print(json.dumps(dict(wait=wait,setup=setup,arms=out,endpoint_sha256={f.name:hashlib.sha256(f.read_bytes()).hexdigest()for f in p.parent.glob('arm*.json')}),indent=2))
