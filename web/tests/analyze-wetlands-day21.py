from pathlib import Path
import json,hashlib
from fractions import Fraction as F
r=Path(__file__).resolve().parents[2];b=r.parent/'site-tmp/wetlands-day21';o=r/'web/tests/continuation-review/wetlands-day21'
rows={k:[]for k in ['TICK','BIRTH_SEEN','IDENTITY_LOST','ROOT_FATE','HYDRATION']}
for line in (b/'run.log').read_text().splitlines():
 for tag in rows:
  if line.startswith(tag+' '):rows[tag].append(json.loads(line[len(tag)+1:]));break
t=rows['TICK'];assert [x['tick']for x in t]==list(range(421,1261));assert (b/'day-21.json').read_bytes()==(b/'resume-day-21.json').read_bytes()
for x in rows['HYDRATION']:
 assert 0<=x['h']<=1 and F(x['h'])*max(F(x['entry_demand']),F(x['current_demand']))<=F(x['credit'])
 if x['h']>0:assert x['id']==x['owner']
s=json.loads((r.parent/'site-tmp/wetlands-journey/day-7.json').read_text());e=json.loads((b/'day-21.json').read_text())
def living(d):return {x['value']['lineage']:{'cell':i,**x['value']}for i,c in enumerate(d['origin']['cells'])for x in c['sparse']if x['value']['biomass']>0}
a=living(s);z=living(e);family={421};family_births=[]
for x in rows['BIRTH_SEEN']:
 c=x['cohort']
 if c['parent']in family:family.add(c['lineage']);family_births.append(x)
assert len(a)+sum(x['births']-x['losses']for x in t)==len(z)
root_ids={x['cohort']['lineage']for x in rows['ROOT_FATE']};supported={x['cohort']['lineage']for x in rows['ROOT_FATE']if x['cohort']['support_mass']>0};positive_h={x['id']for x in rows['HYDRATION']if x['h']>0}
result={'start_living':len(a),'end_living':len(z),'original_day7_remaining':len(set(a)&set(z)),'births':sum(x['births']for x in t),'losses':sum(x['losses']for x in t),'moves':sum(x['moves']for x in t),'daily':[x for x in t if x['tick']%60==0],'root_ids':sorted(root_ids),'supported_root_ids':sorted(supported),'positive_h_ids':sorted(positive_h),'root_credit_density_sum':sum(x['root_credit']for x in t),'hydration_fraction_checks':len(rows['HYDRATION']),'positive_h_calls':sum(x['positive_h_calls']for x in t),'max_h':max(x['max_h']for x in t),'family421_ids':sorted(family),'family421_living_end':[z[i]for i in sorted(family&z.keys())],'family421_births':family_births,'family421_losses':[x for x in rows['IDENTITY_LOST']if x['cohort']['lineage']in family],'feeding_kg_c':e['origin']['stats']['grazed_carbon']-s['origin']['stats']['grazed_carbon'],'grazing_respired_kg_c':e['origin']['stats']['grazing_respired_carbon']-s['origin']['stats']['grazing_respired_carbon'],'living_recorded_feeders':sum(c['lifetime_grazed']>0 for c in z.values()),'new_root_births':[x for x in rows['BIRTH_SEEN']if x['cohort']['root_fraction']>0],'exact_day14_restart':True,'hashes':{n:hashlib.sha256((b/n).read_bytes()).hexdigest()for n in ['day-14.json','day-21.json','resume-day-21.json']}}
(o/'results.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps({k:v for k,v in result.items()if k not in ['daily','family421_births','family421_losses','new_root_births']},indent=2))
