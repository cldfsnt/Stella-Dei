#!/usr/bin/env python3
from pathlib import Path
from fractions import Fraction as F
import json,sys
rows={}
for l in Path(sys.argv[1]).read_text().splitlines():
 if l.startswith('SHORE_') and ' {' in l:
  tag,data=l.split(' ',1);rows.setdefault(tag,[]).append(json.loads(data))
def carbon(c):return F(c['detritus'])+sum((F(z['biomass'])for z in c['cohorts']),F(0))
def nutrient(c):return F(c['nutrient'])+sum((F(z['biomass'])*F(0.10000000149011612)for z in c['cohorts']),F(0))
arms=[]
for arm in range(3):
 steps=[x for x in rows['SHORE_STEP']if x['arm']==arm];bio=[x for x in rows['SHORE_BIO']if x['arm']==arm];actions=[x for x in rows.get('SHORE_ACTION',[])if x['arm']==arm]
 assert len(steps)==60
 start=next(x for x in rows['SHORE_START']if x['arm']==arm);end=next(x for x in rows['SHORE_END']if x['arm']==arm)
 residuals=[(carbon(x['after'])-carbon(x['before'])-F(x['flux']['fixed'])+F(x['flux']['recycled']),nutrient(x['after'])-nutrient(x['before']))for x in bio]
 arms.append(dict(arm=arm,actions=actions,initial_cell=start['cell'],at6h=steps[14],endpoint=steps[-1],
   dry_endpoints=sum(x['depth_m']==0 for x in steps),film_endpoints=sum(0<x['depth_m']<.2 for x in steps),aquatic_endpoints=sum(x['depth_m']>=.2 for x in steps),
   depth_min=min(x['depth_m']for x in steps),depth_max=max(x['depth_m']for x in steps),first_depth_m=steps[0]['depth_m'],
   any_air_exposed_endpoints=sum(any(c['biomass']>0 and h>x['depth_m']for c,h in zip(x['cell']['cohorts'],x['heights_m']))for x in steps),
   flux_totals={k:sum(x['flux'][k]for x in bio)for k in ['fixed','recycled','grazed']},
   max_abs_carbon_residual=float(max((abs(a)for a,b in residuals),default=F(0))),
   max_abs_nutrient_residual=float(max((abs(b)for a,b in residuals),default=F(0))),
   sumabs_carbon_residual=float(sum((abs(a)for a,b in residuals),F(0))),
   sumabs_nutrient_residual=float(sum((abs(b)for a,b in residuals),F(0))),
   water_residual_native=end['inventory']['water_native']-start['inventory']['water_native']-sum(x['change_native']for x in actions),
   carbon_inventory_delta=end['inventory']['carbon_density_sum']-start['inventory']['carbon_density_sum'],
   nutrient_inventory_delta=end['inventory']['nutrient_density_sum']-start['inventory']['nutrient_density_sum']))
assert 'SHORE_COMPLETE original_restored=true current_core=true' in Path(sys.argv[1]).read_text()
print(json.dumps(dict(arms=arms,scope='60 posttick samples perarm, not continuous exposure integration. Exact binary physiology residuals; approximate wholeworld inventories retain inherited drift.'),indent=2))
