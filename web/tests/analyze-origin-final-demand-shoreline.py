from pathlib import Path
from fractions import Fraction as F
import json,sys
p=Path(sys.argv[1]);old=p.parent/'origin-root-drain';out=[]
def rows(file,tag):return [json.loads(l.split(' ',1)[1])for l in (p/file).read_text().splitlines()if l.startswith(tag+' ')]
for d in (0,1,3):
 for a in (0,):
  m=f'main-{d}-{a}.log';r=f'resume-{d}-{a}.log';assert 'COMPLETE' in(p/m).read_text()and 'COMPLETE'in(p/r).read_text()
  assert(p/f'depth-{d}-arm-{a}-60.json').read_bytes()==(p/f'resume-depth-{d}-arm-{a}-60.json').read_bytes()
  for tag in ('BIRTH','FATE','ROOT_WATER','PATCH','USED_H'):assert [x for x in rows(m,tag)if x['tick']>30]==rows(r,tag)
  f=[x for x in rows(m,'FATE')if x['cohort']['lineage']==524];w=[x for x in rows(m,'ROOT_WATER')if x['lineage']==524];patch=rows(m,'PATCH');assert len(patch)==60
  signed=F(0);absolute=F(0);maxrelative=0.
  for x in w:
   debit=F(x['soil_before'])-F(x['soil_after']);assert F(x['credit'])+F(x['bare_credit'])<=debit;assert F(x['h'])*F(x['demand'])<=F(x['credit'])<=F(x['demand'])
   physical=debit*F(x['area']);err=(F(x['vapor_after'])-F(x['vapor_before']))*10**9-physical;signed+=err;absolute+=abs(err)
   if physical:maxrelative=max(maxrelative,float(abs(err)/physical))
  b=rows(m,'BIRTH');children=[x['child']['lineage']for x in b if x['child']['parent']==524]
  out.append({'depth_m':[0,.001,.01,.1][d],'ablated':bool(a),'drain':rows(m,'DRAIN')[0],'last_alive_tick':f[-1]['tick']if f else None,'alive_24h':any(x['tick']==60 for x in f),'last_biomass':f[-1]['cohort']['biomass']if f else None,'direct_children':children,'positive_root_pulses':sum(x['credit']>0 for x in w),'root_credit_kg_m2':sum(x['credit']for x in w),'phase_depths_m':[x['environment']['depth_km']*1000 for x in w],'phase_h':[x['h']for x in w],'patch_trace':patch,'shared_signed_kg':float(signed),'shared_sumabs_kg':float(absolute),'shared_maxrelative':maxrelative,'restart_exact':True,'complete':[l for l in(p/m).read_text().splitlines()if l.startswith('COMPLETE')]})
old_results=json.loads((p.parent/'origin-basal-shoreline/analysis.json').read_text());
for current,prior in zip(out,[x for x in old_results if not x['ablated'] and x['depth_m'] in (0,.001,.1)]):current['law2_reference']={k:prior[k]for k in ('last_alive_tick','alive_24h','last_biomass','positive_root_pulses','root_credit_kg_m2','direct_children')}
(p/'analysis.json').write_text(json.dumps(out,indent=2))
for x in out:print({k:v for k,v in x.items()if k not in ('patch_trace','phase_depths_m','phase_h','drain')})

for d in (0,1,3):
 used=rows(f'main-{d}-0.log','USED_H');phase={x['tick']:x for x in rows(f'main-{d}-0.log','ROOT_WATER')if x['lineage']==524}
 for x in used:
  assert x['owner']==x['lineage']==524
  assert x['credit']==phase[x['tick']]['credit']
  assert x['denominator']==max(x['entry_demand'],x['current_demand'])
  assert F(x['h'])*F(x['denominator'])<=F(x['credit'])
  assert 0<=x['effective_h']<=x['h']<=1
  if x['current_demand']<=0:assert x['h']==0
 print('CONSUMPTION',d,'records',len(used),'positive',sum(x['h']>0 for x in used),'first',used[:2])
(p/'consumption.json').write_text(json.dumps({d:rows(f'main-{d}-0.log','USED_H')for d in (0,1,3)},indent=2))
for d in (0,3):
 current=json.loads((p/f'depth-{d}-arm-0-60.json').read_text());prior=json.loads((p.parent/f'origin-basal-shoreline/depth-{d}-arm-0-60.json').read_text())
 current['version']=prior['version'];current['beta_origin']['format']=prior['beta_origin']['format'];current['beta_origin']['config']['physiology_law']=2;assert current==prior
 print('LAW2_COMPLETE_STATE_EXCEPT_IDENTITY',d,True)
