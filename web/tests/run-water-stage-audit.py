#!/usr/bin/env python3
from pathlib import Path
import os,json,subprocess,shutil,hashlib
r=Path(__file__).resolve().parents[2];base=r.parent/'site-tmp';results=[]
for mode in ['production','candidate']:
 p=base/('water-stage-'+mode)
 for label,inp in [('day30','natural60-day30.json'),('day60','natural60-day60.json'),('day90','grazing-coupled/arm-0-day90.json')]:
  d=p/label;d.mkdir(exist_ok=True)
  env=os.environ|{'LIBGL_ALWAYS_SOFTWARE':'1','EGL_PLATFORM':'surfaceless','STELLA_ORIGIN_COUPLED':'1','STELLA_ORIGIN_FAST':'1','STELLA_ORIGIN_WIDTH':'390','STELLA_ORIGIN_HEIGHT':'700','QA_PULSE_SAVE':str(base/inp),'QA_ROOT_LABEL':label,'QA_ROOT_STAGE':'enabled','STELLA_EGL_CAPTURE_PREFIX':str(d/'capture')}
  with (d/'run.log').open('w') as f:proc=subprocess.run([str(p/'build/bin/stella-egl')],env=env,cwd=r,stdout=f,stderr=subprocess.STDOUT)
  assert proc.returncode==0,(mode,label,proc.returncode)
  if mode=='production':src=p/'arm-0.json';old=base/'root-one-day-baseline'/label/'arm-0.json'
  else:src=p/(label+'-arm-1.json');old=base/'root-world-qa'/(label+'-arm-1.json')
  shutil.copy2(src,d/'endpoint.json');same=src.read_bytes()==old.read_bytes()
  lines=(d/'run.log').read_text().splitlines();records=[json.loads(l.split('WATER_STAGE ',1)[1]) for l in lines if 'WATER_STAGE {' in l]
  assert len(records)>=60,(mode,label,len(records))
  # No preparatory simulation with QA_PULSE_SAVE; first60 are frozen horizon, later are save checks.
  sums={k:sum(x[k] for x in records[:60])for k in records[0]}
  row={'mode':mode,'label':label,'exit':proc.returncode,'endpoint_exact':same,'endpoint_sha256':hashlib.sha256(src.read_bytes()).hexdigest(),'record_count':len(records),'first60':sums};results.append(row);print(row,flush=True)
  (d/'stages.json').write_text(json.dumps(records,indent=2))
  assert same,(mode,label,'diagnostic changed endpoint')
(base/'water-stage-results.json').write_text(json.dumps(results,indent=2))
