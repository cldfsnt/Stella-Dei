#!/usr/bin/env python3
import pathlib,subprocess,os,json,hashlib,gzip
r=pathlib.Path(__file__).resolve().parents[2];base=r.parent/'site-tmp/thermal-reservoir';e=r/'web/tests/continuation-review/thermal-reservoir';res=[]
for kind in ['control','candidate']:
 b=base/kind
 for arm in range(2):
  for resume in [False,True]:
   env=dict(os.environ,EGL_PLATFORM='surfaceless',LIBGL_ALWAYS_SOFTWARE='1',QA_ARM=str(arm),QA_END='120')
   env.pop('QA_RESUME',None)
   if resume:env['QA_RESUME']='1'
   log=b/f'{"resume" if resume else "main"}-{arm}.log'
   with log.open('wb') as f: subprocess.run([str(b/'build/bin/stella-egl')],cwd=r,env=env,stdout=f,stderr=subprocess.STDOUT,check=True,timeout=900)
  main=(b/f'main-{arm}.log').read_text().splitlines();again=(b/f'resume-{arm}.log').read_text().splitlines()
  assert 'COMPLETE' in '\n'.join(main) and 'COMPLETE' in '\n'.join(again)
  endpoint=b/f'arm-{arm}-120.json';assert endpoint.read_bytes()==(b/f'resume-arm-{arm}-120.json').read_bytes()
  rows=lambda tag:[json.loads(x[len(tag)+1:]) for x in main if x.startswith(tag+' ')]
  for tag in ['ROOT_WATER','USED_H','MORTALITY','PAID_GROWTH','PATCH','BIRTH']:
   a=[x for x in rows(tag) if x['tick']>60];z=[json.loads(x[len(tag)+1:])for x in again if x.startswith(tag+' ')];assert a==z,(kind,arm,tag)
  founder=rows('FOUNDER')[0];sid=int(founder['founder_id']);patch=rows('PATCH');mort=rows('MORTALITY');growth=rows('PAID_GROWTH');water=[x for x in rows('ROOT_WATER')if x['lineage']==sid];used=rows('USED_H')
  lives=[next((c for c in p['cohorts'] if c['lineage']==sid and c['biomass']>0),None)for p in patch]
  res.append(dict(kind=kind,arm=arm,cell=126 if arm==0 else 1845,receipt=founder,initial=rows('INITIAL_ENV')[0],alive=lives[-1],first_absent=next((i+1 for i,v in enumerate(lives)if v is None),None),temperature=[min(p['temperature']for p in patch),max(p['temperature']for p in patch)],cold_ticks=sum(p['temperature']<=273.15 for p in patch),depth_m=[min(p['depth_m']for p in patch),max(p['depth_m']for p in patch)],soil=[min(p['soil']for p in patch),max(p['soil']for p in patch)],growth=sum(x['actual_carbon']for x in growth),dead=sum(x['dead']for x in mort),upkeep=sum(x['upkeep']for x in mort),root_credit=sum(x['credit']for x in water),used_ticks=len({x['tick']for x in used if x['effective_h']>0}),children=[x for x in rows('BIRTH')if x['child']['parent']==sid],endpoint_sha256=hashlib.sha256(endpoint.read_bytes()).hexdigest()))
  for path in [b/f'main-{arm}.log',b/f'resume-{arm}.log',b/f'arm-{arm}-0.json',b/f'arm-{arm}-60.json',endpoint]:
   (e/f'{kind}-{path.name}.gz').write_bytes(gzip.compress(path.read_bytes(),mtime=0))
# Initial world+paid transaction is byte-identical, model coefficient is external QA identity only.
for arm in range(2):assert(base/'control'/f'arm-{arm}-0.json').read_bytes()==(base/'candidate'/f'arm-{arm}-0.json').read_bytes()
(e/'results.json').write_text(json.dumps(res,indent=2)+'\n');print(json.dumps(res,indent=2))
