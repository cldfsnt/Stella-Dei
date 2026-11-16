from pathlib import Path
import json,subprocess,os,hashlib
r=Path(__file__).resolve().parents[2];b=r.parent/'site-tmp/cutoff-trial/small';p=b/'42-pioneer-day10.json';original=p.read_bytes();proof=[]
for name,change in [('wrong-threshold',{'threshold':.0025}),('wrong-format',{'format':'not_a_cutoff_law'})]:
 x=json.loads(original);x.update(change)
 try:
  p.write_text(json.dumps(x))
  with(b/(name+'.log')).open('wb')as f:result=subprocess.run([str(b/'install/bin/stella-egl')],env=os.environ|{'LIBGL_ALWAYS_SOFTWARE':'1','QA_SEED':'42','QA_PIONEER':'1','QA_RESUME':'1'},stdout=f,stderr=subprocess.STDOUT,timeout=120)
  assert result.returncode!=0,name;log=(b/(name+'.log')).read_text();assert 'CUTOFF_COMPLETE'not in log and 'START 'not in log
  proof.append({'case':name,'exit':result.returncode,'no_scheduler_started':True})
 finally:p.write_bytes(original)
assert p.read_bytes()==original
(b.parent/'identity-proof.json').write_text(json.dumps({'cases':proof,'restored_original_sha256':hashlib.sha256(original).hexdigest()},indent=2))
