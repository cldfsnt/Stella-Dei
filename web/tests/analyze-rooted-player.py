from pathlib import Path
from fractions import Fraction as F
import json,struct
r=Path(__file__).resolve().parents[2];b=r.parent/'site-tmp/rooted-player'
def rows(n,tag):return [json.loads(l.split(' ',1)[1])for l in(b/n).read_text().splitlines()if l.startswith(tag+' ')]
original=json.load(open(r.parent/'site-tmp/wetlands-day21/day-21.json'));subject=original['origin']['stats']['next_lineage'];out=[]
for arm in range(2):
 m=f'main-{arm}.log';rr=f'resume-{arm}.log';assert 'COMPLETE'in(b/m).read_text()and 'COMPLETE'in(b/rr).read_text();assert(b/f'arm-{arm}-60.json').read_bytes()==(b/f'resume-arm-{arm}-60.json').read_bytes();assert(b/f'arm-{arm}-2-trace.json').read_bytes()==(b/f'arm-{arm}-2-off.json').read_bytes()
 for tag in ['ROOT_WATER','USED_H','MORTALITY','PAID_GROWTH','PATCH','BIRTH']:assert[x for x in rows(m,tag)if x['tick']>30]==rows(rr,tag),(arm,tag)
 initial=json.load(open(b/f'arm-{arm}-0.json'));founder=rows(m,'FOUNDER')[0];action=rows(m,'WATER_ACTION')[0];area=F(action['area']);c=initial['origin']['cells'][6]['sparse'][0]['value'];assert c['lineage']==subject and c['parent']==0 and c['generation']==0 and c['reproduction_credit']==0;assert F(c['support_mass'])==F(c['biomass'])/4
 source=(F(original['carbon_dioxide'])-F(initial['carbon_dioxide']))*10**9*len(initial['water'])*F(12,44);carbon=F(c['biomass'])*area;assert source>=carbon
 nutrient=F(original['origin']['cells'][6]['nutrient'])-F(initial['origin']['cells'][6]['nutrient']);ratio=F(struct.unpack('f',struct.pack('f',.1))[0]);assert nutrient>=F(c['biomass'])*ratio
 assert initial['origin']['stats']['nutrient_added']==original['origin']['stats']['nutrient_added'];assert initial['origin']['stats']['births']==original['origin']['stats']['births'];assert initial['origin']['stats']['next_lineage']==subject+1
 phase={x['tick']:x for x in rows(m,'ROOT_WATER')if x['lineage']==subject};used=rows(m,'USED_H');signed=F(0);absolute=F(0);rel=0
 for x in phase.values():
  debit=F(x['soil_before'])-F(x['soil_after']);assert F(x['credit'])+F(x['bare_credit'])<=debit;assert F(x['h'])*F(x['demand'])<=F(x['credit'])<=F(x['demand']);delta=(F(x['vapor_after'])-F(x['vapor_before']))*10**9-debit*F(x['area']);signed+=delta;absolute+=abs(delta)
  if debit:rel=max(rel,float(abs(delta)/(debit*F(x['area']))))
 for x in used:
  assert x['owner']==x['lineage']==subject;assert x['credit']==phase.get(x['tick'],{'credit':0})['credit'];assert x['denominator']==max(x['entry_demand'],x['current_demand']);assert F(x['h'])*F(x['denominator'])<=F(x['credit']);assert 0<=x['effective_h']<=x['h']<=1
  if x['current_demand']<=0:assert x['h']==0
 patch=rows(m,'PATCH');assert len(patch)==60;focals=[next((c for c in x['cohorts']if c['lineage']==subject and c['biomass']>0),None)for x in patch]
 births=rows(m,'BIRTH');mort=rows(m,'MORTALITY');growth=rows(m,'PAID_GROWTH');out.append(dict(arm=arm,founder=founder,actual_terrain=rows(m,'TERRAIN'),geometry=rows(m,'GEOMETRY'),action=action,source_carbon_paid_kg=float(source),created_carbon_kg=float(carbon),carbon_excess_kg=float(source-carbon),mineral_nitrogen_debit=float(nutrient),initial_cohort=c,alive_end=focals[-1],first_absent_tick=next((i+1 for i,c in enumerate(focals)if c is None),None),direct_children=[x['child']['lineage']for x in births if x['child']['parent']==subject],root_pulses=sum(x['credit']>0 for x in phase.values()),root_credit=sum(x['credit']for x in phase.values()),positive_consumed_ticks=len({x['tick']for x in used if x['effective_h']>0}),positive_final_demand_ticks=len({x['tick']for x in used if x['current_demand']>0}),max_used_h=max((x['effective_h']for x in used),default=0),paid_growth=sum(x['actual_carbon']for x in growth),mortality_debit=sum(x['dead']for x in mort),upkeep_debit=sum(x['upkeep']for x in mort),depth_min=min(x['depth_m']for x in patch),depth_max=max(x['depth_m']for x in patch),soil_min=min(x['soil']for x in patch),patch_trace=patch,source_signed_kg=float(signed),source_sumabs_kg=float(absolute),source_max_relative=rel,complete=[l for l in(b/m).read_text().splitlines()if l.startswith('COMPLETE')]))
a=json.load(open(b/'arm-0-0.json'));z=json.load(open(b/'arm-1-0.json'));z['origin']['cells'][6]['sparse'][0]['value']['root_fraction']=.5;assert a==z
(b/'results.json').write_text(json.dumps(out,indent=2)+'\n')
for x in out:print(json.dumps({k:v for k,v in x.items()if k not in ['patch_trace']},indent=2))
print('EXACT_INITIAL_ROOT_ONLY_AND_SOURCE_C_N_AND_ROOT_FUNDING_AND_RESTART_AND_TRACE_PARITY_PASS')
