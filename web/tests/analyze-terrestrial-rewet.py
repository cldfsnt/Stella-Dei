#!/usr/bin/env python3
import json,sys
from pathlib import Path
from fractions import Fraction as F
rows={}
for l in Path(sys.argv[1]).read_text().splitlines():
 if l.startswith(('REWET_','TERRESTRIAL_AFTER ','TERRESTRIAL_BEFORE ')) and ' {' in l:
  tag,data=l.split(' ',1);rows.setdefault(tag,[]).append(json.loads(data))
def carbon(c):return sum((F(x['biomass'])for x in c['cohorts']),F(c['detritus']))
def nitrogen(c):return F(c['nutrient'])+sum((F(x['biomass'])*F(0.10000000149011612)for x in c['cohorts']),F(0))
res=[]
for x in rows.get('REWET_BIO',[]):
 dc=carbon(x['after'])-carbon(x['before'])-F(x['flux']['fixed'])+F(x['flux']['recycled'])
 dn=nitrogen(x['after'])-nitrogen(x['before'])
 res.append((abs(dc),abs(dn),dc,dn))
arms=[]
for arm in range(4):
 fate=[x for x in rows['REWET_FATE']if x['arm']==arm]
 aft=[x for x in rows['TERRESTRIAL_AFTER']if x['arm']==arm]
 assert len(fate)==len(aft)==60
 inv=[x['inventory']for x in rows['REWET_INVENTORY']if x['arm']==arm]
 action=[x for x in rows.get('REWET_ACTION',[])if x['arm']==arm]
 dry=[x for x in aft if x['depth_m']==0]
 lost=next((x['tick']+1 for x in fate if x['id44_biomass']==0),None)
 arms.append(dict(arm=arm,root_fraction=0.25 if arm%2 else 0,rewet=arm>=2,
  id44_biomass_at12h=fate[29]['id44_biomass'],id44_biomass_at24h=fate[-1]['id44_biomass'],
  first_absent_tick=lost,endpoint_fate=fate[-1],endpoint_environment=aft[-1],
  dry_ticks=len(dry),post12h_depth_min=min(x['depth_m']for x in aft[30:]),
  post12h_depth_max=max(x['depth_m']for x in aft[30:]),actions=action,
  world_water_residual_native=inv[1]['water_native']-inv[0]['water_native']-sum(x['added_native']for x in action),
  world_carbon_delta_density_sum=inv[1]['carbon_density_sum']-inv[0]['carbon_density_sum'],
  world_nutrient_delta_density_sum=inv[1]['nutrient_density_sum']-inv[0]['nutrient_density_sum']))
print(json.dumps(dict(arms=arms,target_biological_steps=len(res),
 max_abs_target_carbon_residual=float(max((x[0]for x in res),default=F(0))),
 max_abs_target_nutrient_residual=float(max((x[1]for x in res),default=F(0))),
 sumabs_target_carbon_residual=float(sum((x[0]for x in res),F(0))),
 sumabs_target_nutrient_residual=float(sum((x[1]for x in res),F(0))),
 scope='C/N residuals are exact binary target physiology observations; whole-world sums are approximate diagnostics, not conservation approval.'),indent=2))
