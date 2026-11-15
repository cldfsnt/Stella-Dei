#!/usr/bin/env python3
"""Read-only complete-cohort census of named archived trajectories, no new simulation."""
from pathlib import Path
import json,math,statistics,hashlib
r=Path(__file__).resolve().parents[2];base=r.parent/'site-tmp'
manifest=[('natural',f'natural60-day{d}.json')for d in (30,40,50,60)]
manifest += [('natural continuation','grazing-coupled/arm-0-day90.json'),('grazing ablation control','grazing-coupled/arm-1-day90.json')]
manifest += [('Sunlit intervention journey',f'sunlit14/day-{d}.json')for d in (7,14)]
manifest += [('experimental retention mutation',f'retention-coupled/arm-{i}.json')for i in range(6)]
def dist(v):
 v=sorted(v);return dict(min=v[0],p25=v[int((len(v)-1)*.25)],median=statistics.median(v),p75=v[int((len(v)-1)*.75)],max=v[-1])
out=[]
for family,name in manifest:
 p=base/name;x=json.loads(p.read_text());rows=[]
 for i,cell in enumerate(x['origin']['cells']):
  cs=[(z['index'],z['value'])for z in cell['sparse']] if cell.get('sparse')is not None else list(enumerate(cell.get('cohorts',[])))
  for slot,c in cs:
   if c['biomass']<=0:continue
   s=c['structure'];m=c['biomass'];k=4-3.3*s
   rows.append(dict(cell=i,slot=slot,id=c['lineage'],parent=c['parent'],generation=c['generation'],biomass=m,support_mass=c['support_mass'],structure=s,efficiency=c['efficiency'],feeding=c['feeding'],mobility=c['mobility'],dry_mortality_per_day=k,dry_loss_halflife_hours=24*math.log(2)/k,structure_growth_multiplier=1-.5*s,support_upkeep_per_day=c['support_mass']*.12*(1+.4*max(0,c['efficiency']-1)),constant_dry_time_to_cutoff_hours=max(0,24*math.log(m/.0025)/k)))
 keys=['structure','biomass','support_mass','generation','dry_mortality_per_day','dry_loss_halflife_hours','structure_growth_multiplier','support_upkeep_per_day','constant_dry_time_to_cutoff_hours']
 out.append(dict(file=name,family=family,sha256=hashlib.sha256(p.read_bytes()).hexdigest(),version=x['version'],game_time=x['game_time'],living=len(rows),occupied=len(set(z['cell']for z in rows)),distributions={k:dist([z[k]for z in rows])for k in keys},counts_structure_ge={str(t):sum(z['structure']>=t for z in rows)for t in (.1,.25,.5,.75)},cohorts=rows))
print(json.dumps(dict(scope='Named complete archived trajectories; all living cohorts, no donor selection or new outcomes. Separate counterfactual/experimental families, not independent replicates.',analytic='Constant isolated dry mortality only: ignores height, upkeep, temperature, feeding, reproduction, movement, water and discrete cutoff. Not full-scheduler survival proof.',source_sha256=hashlib.sha256((r/'src/simulation/microbes.zig').read_bytes()).hexdigest(),snapshots=out),indent=2))
