#!/usr/bin/env python3
import json,re,sys
from pathlib import Path
p=Path(sys.argv[1]);lines=p.read_text().splitlines();arms={i:{k:[]for k in ['loss','potential','cap','flux','before','after']}for i in range(4)};arm=None;hashes={}
for l in lines:
 if l.startswith('TERRESTRIAL_BEFORE '):
  x=json.loads(l.split(' ',1)[1]);arm=x['arm'];arms[arm]['before'].append(x)
 elif l.startswith('TERRESTRIAL_AFTER '):arms[arm]['after'].append(json.loads(l.split(' ',1)[1]))
 elif l.startswith('BUDGET_END '):
  m=re.search(r'arm=(\d+) sha=(\w+)',l);hashes[int(m[1])]=m[2]
 else:
  for tag,key in [('BUDGET_LOSS','loss'),('BUDGET_POTENTIAL','potential'),('BUDGET_CAP','cap'),('BUDGET_FLUX','flux')]:
   if l.startswith(tag+' '):arms[arm][key].append(json.loads(l.split(' ',1)[1]))
assert hashes[0]==hashes[2] and hashes[1]==hashes[3]
old=Path(sys.argv[2]).read_text().splitlines()
for tag,key in [('TERRESTRIAL_BEFORE','before'),('TERRESTRIAL_AFTER','after')]:
 expected=[json.loads(l.split(' ',1)[1])for l in old if l.startswith(tag+' ')]
 actual=arms[0][key]+arms[1][key];assert actual==expected,(tag,'original target changed')
summary=[]
for i in [2,3]:
 a=arms[i];assert all(len(a[k])==60 for k in ['loss','cap','flux','before','after'])
 fixed=sum(x['flux']['fixed']for x in a['flux']);upkeep=sum(x['upkeep']for x in a['loss']);death=sum(b['cohort']['biomass']-l['upkeep']+f['flux']['fixed']-f['after']['cohorts'][0]['biomass'] for b,l,f in zip(a['before'],a['loss'],a['flux']))
 summary.append({'arm':i,'root_fraction':a['before'][0]['cohort']['root_fraction'],'fixed_carbon':fixed,'upkeep':upkeep,'inferred_actual_mortality_carbon':death,'grazed':sum(x['flux']['grazed']for x in a['flux']),'light_zero_ticks':sum(x['env']['light']==0 for x in a['loss']),'positive_fixed_ticks':sum(x['flux']['fixed']>0 for x in a['flux']),'zero_potential_ticks':sum(x['potential']==0 for x in a['cap']),'carbon_cap_ticks':sum(x['carbon']<x['potential']for x in a['cap']),'nutrient_cap_ticks':sum(x['nutrient_carbon']<x['potential']for x in a['cap']),'space_cap_ticks':sum(x['space']<x['potential']for x in a['cap']),'min_carbon_available':min(x['carbon']for x in a['cap']),'min_nutrient_carbon':min(x['nutrient_carbon']for x in a['cap']),'max_surface_light':max(x['env']['light']for x in a['loss']),'hydrated_ticks':sum(x['hydrated']>0 for x in a['loss']),'first_two':[{'loss':a['loss'][j],'potential':a['potential'][j],'flux':a['flux'][j]['flux']}for j in range(2)]})
print(json.dumps({'full_endpoint_hashes':hashes,'original_target_records_exact':True,'summary':summary},indent=2))
