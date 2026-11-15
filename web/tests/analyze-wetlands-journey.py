from pathlib import Path
import json,hashlib,gzip
from fractions import Fraction as F
r=Path(__file__).resolve().parents[2];b=r.parent/'site-tmp/wetlands-journey';out=r/'web/tests/continuation-review/wetlands-journey';out.mkdir(parents=True,exist_ok=True)
rows={k:[] for k in ['TICK','BIRTH_SEEN','IDENTITY_LOST','ROOT_FATE','HYDRATION']}
for line in (b/'run.log').read_text().splitlines():
 for tag in rows:
  if line.startswith(tag+' '): rows[tag].append(json.loads(line[len(tag)+1:]));break
t=rows['TICK'];assert len(t)==420 and [x['tick'] for x in t]==list(range(1,421));assert (b/'day-7.json').read_bytes()==(b/'resume-day-7.json').read_bytes()
for x in rows['HYDRATION']:
 assert x['h']>=0 and F(x['h'])*max(F(x['current_demand']),F(x['entry_demand']))<=F(x['credit'])
 if x['h']>0:assert x['id']==x['owner']
d0=json.loads((b/'day-0.json').read_text());d7=json.loads((b/'day-7.json').read_text())
def living(d):return [(i,s['value'])for i,c in enumerate(d['origin']['cells'])for s in c['sparse'] if s['value']['biomass']>0]
l0=living(d0);l7=living(d7);ids0={c['lineage']for _,c in l0};ids7={c['lineage']for _,c in l7};assert len(l0)+sum(x['births']-x['losses']for x in t)==len(l7)
roots={x['cohort']['lineage']for x in rows['ROOT_FATE']};births={x['cohort']['lineage']:x for x in rows['BIRTH_SEEN']};assert roots<=births.keys()
result={'source_world_seed':d0['seed'],'preview':json.loads((b/'preview.json').read_text()),'receipt':json.loads((b/'receipt.json').read_text()),'day0':{'living':len(l0),'occupied':len({i for i,_ in l0}),'biomass_sum':sum(c['biomass']for _,c in l0)},'days':[x for x in t if x['tick']%60==0],'total_births':sum(x['births']for x in t),'identity_losses':sum(x['losses']for x in t),'moves':sum(x['moves']for x in t),'original_founders_remaining':len(ids0&ids7),'newly_occupied_day7':len({i for i,_ in l7}-{i for i,_ in l0}),'ever_positive_root_ids':sorted(roots),'positive_root_births':[births[i]for i in sorted(roots)],'first_birth_tick':next((x['tick']for x in t if x['births']),None),'first_nonmat_tick':next((x['tick']for x in t if sum(x['forms'][1:])),None),'first_occupied_change_tick':next((x['tick']for x in t if x['occupied']!=len({i for i,_ in l0})),None),'source_funded_credit_sum':sum(x['root_credit']for x in t),'positive_h_function_calls':sum(x['positive_h_calls']for x in t),'max_h':max(x['max_h']for x in t),'hydation_fraction_checks':len(rows['HYDRATION']),'exact_restart':True,'state_hashes':{n:hashlib.sha256((b/n).read_bytes()).hexdigest()for n in ['day-0.json','day-3.json','day-7.json','resume-day-7.json']}}
(out/'results.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result,indent=2))
