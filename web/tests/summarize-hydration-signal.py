from pathlib import Path
import json,sys
p=Path(sys.argv[1]);read=lambda name:[json.loads(l.split('SIGNAL_MATRIX ',1)[1])for l in (p/name).read_text().splitlines()if 'SIGNAL_MATRIX ' in l]
a=read('first-run.log');b=read('run-traces.log');assert len(a)==len(b)==312
added=['uptake','evaporation','last_height_m','last_exposure']
for x,y in zip(a,b):assert x=={k:v for k,v in y.items()if k not in added},'read-only traces changed outcomes'
ends=[x for x in b if x['day']==x['horizon_days']];assert len(ends)==80
rows=[]
for x in ends:
 rows.append({k:x[k]for k in ['fixture','law','initial_depth_m','dt_s','horizon_days','extinction_tick','uptake','evaporation','last_height_m','last_exposure','water_residual','carbon_residual','nitrogen_residual']}|{'mass':sum(c['biomass']for c in x['cohorts']),'water':sum(c['stored_water']for c in x['cohorts']),'living':[{k:c[k]for k in ['lineage','biomass','support_mass','retention_allocation','stored_water']}for c in x['cohorts']if c['biomass']>0]})
print(json.dumps({'cases':80,'daily_records':312,'trace_parity':True,'births_simulated':False,'all_dry_extinct_day1':all(sum(c['biomass']for c in x['cohorts'])==0 for x in b if x['initial_depth_m']==0 and x['day']==1),'max_water_residual':max(x['water_residual']for x in b),'max_carbon_residual':max(x['carbon_residual']for x in b),'max_nitrogen_residual':max(x['nitrogen_residual']for x in b),'endpoints':rows},indent=2))
