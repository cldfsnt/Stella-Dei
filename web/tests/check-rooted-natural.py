from pathlib import Path
from fractions import Fraction as F
import json,subprocess,os,hashlib,struct,sys
r=Path(__file__).resolve().parents[2];b=r.parent/'site-tmp/rooted-natural';original=json.load(open(r.parent/'site-tmp/wetlands-day21/day-21.json'))
def run(name,**kw):
 with(b/name).open('wb')as out:subprocess.run([str(b/'install/bin/stella-egl')],env=os.environ|{'LIBGL_ALWAYS_SOFTWARE':'1'}|{k:str(v)for k,v in kw.items()},stdout=out,stderr=subprocess.STDOUT,check=True,timeout=900)
for arm in ([] if '--analyze-only' in sys.argv else range(2)):
 run(f'trace-{arm}.log',QA_ARM=arm,QA_END=2,QA_SUFFIX='-trace');run(f'off-{arm}.log',QA_ARM=arm,QA_END=2,QA_SUFFIX='-off',QA_TRACE_OFF=1)
 run(f'main-{arm}.log',QA_ARM=arm);run(f'resume-{arm}.log',QA_ARM=arm,QA_RESUME=1)
rows=lambda n,tag:[json.loads(l.split(' ',1)[1])for l in(b/n).read_text().splitlines()if l.startswith(tag+' ')]
results=[]
for arm,point in enumerate((126,1845)):
 m=f'main-{arm}.log';assert(b/f'arm-{arm}-60.json').read_bytes()==(b/f'resume-arm-{arm}-60.json').read_bytes();assert(b/f'arm-{arm}-2-trace.json').read_bytes()==(b/f'arm-{arm}-2-off.json').read_bytes()
 for tag in ('ROOT_WATER','USED_H','MORTALITY','PAID_GROWTH','PATCH','BIRTH'):assert[x for x in rows(m,tag)if x['tick']>30]==rows(f'resume-{arm}.log',tag)
 initial=json.load(open(b/f'arm-{arm}-0.json'));c=initial['origin']['cells'][point]['sparse'][0]['value'];sid=c['lineage'];area=F(rows(m,'INITIAL_ENV')[0]['area']);source=(F(original['carbon_dioxide'])-F(initial['carbon_dioxide']))*10**9*len(initial['water'])*F(12,44);created=F(c['biomass'])*area;assert source>=created;assert F(c['support_mass'])==F(c['biomass'])/4;assert c['root_fraction']==.5 and c['reproduction_credit']==0 and c['generation']==0
 n=F(original['origin']['cells'][point]['nutrient'])-F(initial['origin']['cells'][point]['nutrient']);assert n>=F(c['biomass'])*F(struct.unpack('f',struct.pack('f',.1))[0])
 for field in ('elevation','water','temperature','rainfall','vapor','seed'):assert initial[field]==original[field],field
 assert initial['beta_origin']==original['beta_origin'];assert initial['origin']['stats']['nutrient_added']==original['origin']['stats']['nutrient_added']
 phases={x['tick']:x for x in rows(m,'ROOT_WATER')if x['lineage']==sid};used=rows(m,'USED_H');residual=F(0)
 for x in phases.values():
  debit=F(x['soil_before'])-F(x['soil_after']);assert F(x['credit'])+F(x['bare_credit'])<=debit;residual+=(F(x['vapor_after'])-F(x['vapor_before']))*10**9-debit*F(x['area'])
 for x in used:assert x['owner']==x['lineage']==sid and F(x['h'])*F(max(x['entry_demand'],x['current_demand']))<=F(x['credit'])
 patches=rows(m,'PATCH');live=[next((c for c in p['cohorts']if c['lineage']==sid and c['biomass']>0),None)for p in patches];g=rows(m,'PAID_GROWTH');mort=rows(m,'MORTALITY')
 results.append(dict(arm=arm,cell=point,initial=rows(m,'INITIAL_ENV')[0],receipt=rows(m,'FOUNDER')[0],source_excess_kg=float(source-created),end=live[-1],death_tick=next((i+1 for i,c in enumerate(live)if c is None),None),children=[x for x in rows(m,'BIRTH')if x['child']['parent']==sid],growth=sum(x['actual_carbon']for x in g),mortality=sum(x['dead']for x in mort),upkeep=sum(x['upkeep']for x in mort),root_credit=sum(x['credit']for x in phases.values()),root_pulses=sum(x['credit']>0 for x in phases.values()),positive_h_ticks=len({x['tick']for x in used if x['h']>0}),depth_range=[min(x['depth_m']for x in patches),max(x['depth_m']for x in patches)],temperature_range=[min(x['temperature']for x in patches),max(x['temperature']for x in patches)],signed_water_residual_kg=float(residual),first_growth_tick=g[0]['tick']if g else None))
(b/'results.json').write_text(json.dumps(results,indent=2));print(json.dumps(results,indent=2));print('EXACT_RESTART_OBSERVER_PARITY_SOURCE_FUNDING_AND_ENVIRONMENT_UNCHANGED_PASS')
