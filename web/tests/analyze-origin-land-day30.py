#!/usr/bin/env python3
from pathlib import Path
from fractions import Fraction as F
import hashlib,json,struct,re,sys,collections
p=Path(sys.argv[1]);out={}
def rows(name,tag):
 with (p/name).open()as f:
  for l in f:
   if l.startswith(tag+' '):yield json.loads(l[len(tag)+1:])
def prop(x):
 c=x['child'];d=hashlib.sha256(b'STELLA-ROOT1'+b'\0'*4+struct.pack('<QQQI',42,c['parent'],c['lineage'],c['generation'])).digest();return (1/32 if d[1]&1==0 else -1/32) if d[0]&63==0 else 0
births=0;pos=neg=clipped=fromzero=0;rootborn=set();rootinherited=set()
for x in rows('main.log','BIRTH'):
 births+=1;c=x['child'];old=x['parent_before'];q=prop(x);pos+=q>0;neg+=q<0;clipped+=q<0 and old['root_fraction']==0
 assert c['root_fraction']==max(0,min(1,old['root_fraction']+q));s=x['rng_before']
 for _ in range(6):s=(s+0x9e3779b97f4a7c15)&(2**64-1);s=s or 1
 assert s==x['rng_after'];assert x['parent_after']['biomass']<old['biomass'] and x['parent_after']['reproduction_credit']<old['reproduction_credit']
 if c['root_fraction']>0:rootborn.add(c['lineage']);fromzero+=old['root_fraction']==0
 if c['root_fraction']>0 and old['root_fraction']>0:rootinherited.add(c['lineage'])
first={};last={};supported=set();dry=set();maxroot=0.;maxsupport=0.
for x in rows('main.log','ROOT_FATE'):
 c=x['cohort'];i=c['lineage'];first.setdefault(i,x);last[i]=x
 if c['support_mass']*c['root_fraction']>0:supported.add(i)
 if x['depth_m']<.2:dry.add(i)
 maxroot=max(maxroot,c['root_fraction']);maxsupport=max(maxsupport,c['support_mass']*c['root_fraction'])
paid=set();paid_supported=set();credits=0.;events=0;maxh=0.;mindepth=None
for x in rows('main.log','ROOT_WATER'):
 assert x['credit']>=0 and x['credit']<=x['demand'];assert F(x['h'])*F(x['demand'])<=F(x['credit'])
 if x['credit']>0:
  events+=1;paid.add(x['lineage']);credits+=x['credit'];maxh=max(maxh,x['h']);mindepth=min(mindepth,x['environment']['depth_km']*1000)if mindepth is not None else x['environment']['depth_km']*1000
  if x['cohort']['support_mass']*x['cohort']['root_fraction']>0:paid_supported.add(x['lineage'])
for tag in ['BIRTH','ROOT_FATE','ROOT_WATER']:
 a=[x for x in rows('main.log',tag)if x['tick']>840];b=list(rows('resume.log',tag));assert a==b;out['restart_'+tag.lower()+'_events_exact']=len(a)
for day in [21,30]:assert(p/f'day-{day}.json').read_bytes()==(p/f'resume-day-{day}.json').read_bytes()
ticks=[l.strip()for l in(p/'main.log').read_text().splitlines()if l.startswith('TICK ')];assert len(ticks)==1380 and int(re.search(r'births=(\d+)',ticks[-1])[1])==184+births
out.update(new_births=births,positive_proposals=pos,negative_proposals=neg,clipped_negative_at_zero=clipped,positive_from_zero=fromzero,root_born_lineages=len(rootborn),inherited_positive_children=len(rootinherited),positive_root_observed=len(last),paid_tissue_lineages=len(supported),sub20cm_lineages=len(dry),positive_water_events=events,water_paid_lineages=len(paid),paid_supported_lineages=len(paid_supported),credited_density_sum=credits,max_h=maxh,min_paid_depth_m=mindepth,max_allocation=maxroot,max_root_tissue_density=maxsupport,day30_root_alive=sum(x['tick']==1800 for x in last.values()),daily=[l for l in ticks if int(re.search(r'tick=(\d+)',l)[1])%60==0],fresh_process_day14_to30_exact=True,day30_sha256=hashlib.sha256((p/'day-30.json').read_bytes()).hexdigest())
# Source-law reconstruction, not a separately logged native height measurement.
f32=lambda x:struct.unpack('<f',struct.pack('<f',x))[0]
shallow=collections.Counter();height_max=0.;depth_min=None
for x in rows('main.log','ROOT_WATER'):
 c=x['cohort'];e=x['environment'];depth=e['depth_km']*1000
 if depth>=.2:continue
 height=min(.5,f32(f32(f32(f32(.2)*f32(c['support_mass']*f32(1-c['root_fraction'])))/f32(max(0,f32(c['biomass']-c['support_mass']))+f32(.01)))*f32(f32(1+f32(f32(.6)*f32(1-c['efficiency'])))-f32(f32(.3)*c['structure']))))
 shallow['events']+=1;shallow['support_positive']+=c['support_mass']>0;shallow['temperature_eligible']+=273.15<e['temperature']<355;shallow['height_below_depth']+=height<=depth;height_max=max(height_max,height);depth_min=depth if depth_min is None else min(depth_min,depth)
out['shallow_phase']=dict(shallow);out['shallow_reconstructed_height_max_m']=height_max;out['shallow_min_depth_m']=depth_min
out['checkpoints']={}
for day in [14,21,30]:
 saved=json.loads((p/f'day-{day}.json').read_text());cohorts=[x['value']for cell in saved['origin']['cells']for x in cell.get('sparse',[])if x['value']['biomass']>0 and x['value']['root_fraction']>0];out['checkpoints'][day]={'positive_root':len(cohorts),'supported_root':sum(c['support_mass']>0 for c in cohorts),'lineages':[c['lineage']for c in cohorts]}
out['fates']=[{'lineage':i,'first_tick':first[i]['tick'],'last_tick':last[i]['tick'],'last_cell':last[i]['cell'],'mass':last[i]['cohort']['biomass'],'allocation':last[i]['cohort']['root_fraction'],'root_tissue':last[i]['cohort']['support_mass']*last[i]['cohort']['root_fraction'],'ever_paid_tissue':i in supported,'ever_water':i in paid,'alive_day30':last[i]['tick']==1800}for i in sorted(last)]
(p/'analysis.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps({k:v for k,v in out.items()if k!='fates'},indent=2))
