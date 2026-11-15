from pathlib import Path
from fractions import Fraction as F
import json,sys
p=Path(sys.argv[1]);old=p.parent/'origin-root-drain';out=[]
def rows(file,tag):return [json.loads(l.split(' ',1)[1])for l in (p/file).read_text().splitlines()if l.startswith(tag+' ')]
for d in range(4):
 for a in range(2):
  m=f'main-{d}-{a}.log';r=f'resume-{d}-{a}.log';assert 'COMPLETE' in(p/m).read_text()and 'COMPLETE'in(p/r).read_text()
  assert(p/f'depth-{d}-arm-{a}-60.json').read_bytes()==(p/f'resume-depth-{d}-arm-{a}-60.json').read_bytes()
  for tag in ('BIRTH','FATE','ROOT_WATER','PATCH'):assert [x for x in rows(m,tag)if x['tick']>30]==rows(r,tag)
  if d==0:
   for t in [0,30,60]:assert(p/f'depth-0-arm-{a}-{t}.json').read_bytes()==(old/f'arm-{a}-{t}.json').read_bytes()
   for tag in ('BIRTH','FATE','ROOT_WATER'):
    prior=[json.loads(l.split(' ',1)[1])for l in(old/f'main-{a}.log').read_text().splitlines()if l.startswith(tag+' ')];assert rows(m,tag)==prior
  f=[x for x in rows(m,'FATE')if x['cohort']['lineage']==524];w=[x for x in rows(m,'ROOT_WATER')if x['lineage']==524];patch=rows(m,'PATCH');assert len(patch)==60
  signed=F(0);absolute=F(0);maxrelative=0.
  for x in w:
   debit=F(x['soil_before'])-F(x['soil_after']);assert F(x['credit'])+F(x['bare_credit'])<=debit;assert F(x['h'])*F(x['demand'])<=F(x['credit'])<=F(x['demand'])
   physical=debit*F(x['area']);err=(F(x['vapor_after'])-F(x['vapor_before']))*10**9-physical;signed+=err;absolute+=abs(err)
   if physical:maxrelative=max(maxrelative,float(abs(err)/physical))
  b=rows(m,'BIRTH');children=[x['child']['lineage']for x in b if x['child']['parent']==524]
  out.append({'depth_m':[0,.001,.01,.1][d],'ablated':bool(a),'drain':rows(m,'DRAIN')[0],'last_alive_tick':f[-1]['tick']if f else None,'alive_24h':any(x['tick']==60 for x in f),'last_biomass':f[-1]['cohort']['biomass']if f else None,'direct_children':children,'positive_root_pulses':sum(x['credit']>0 for x in w),'root_credit_kg_m2':sum(x['credit']for x in w),'phase_depths_m':[x['environment']['depth_km']*1000 for x in w],'phase_h':[x['h']for x in w],'patch_trace':patch,'shared_signed_kg':float(signed),'shared_sumabs_kg':float(absolute),'shared_maxrelative':maxrelative,'restart_exact':True,'complete':[l for l in(p/m).read_text().splitlines()if l.startswith('COMPLETE')]})
for d in range(4):
 a=json.loads((p/f'depth-{d}-arm-0-0.json').read_text());b=json.loads((p/f'depth-{d}-arm-1-0.json').read_text());b['origin']['cells'][18327]['sparse'][2]['value']['root_fraction']=a['origin']['cells'][18327]['sparse'][2]['value']['root_fraction'];assert a==b
(p/'analysis.json').write_text(json.dumps(out,indent=2))
for x in out:print({k:v for k,v in x.items()if k not in ('patch_trace','phase_depths_m','phase_h','drain')})
