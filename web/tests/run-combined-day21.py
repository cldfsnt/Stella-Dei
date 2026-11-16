from pathlib import Path
import subprocess,os,hashlib,json
r=Path(__file__).resolve().parents[2];b=r.parent/'site-tmp/combined-day21';proof={}
for seed in (42,1337):
 for kind in ('ordinary','pioneer'):
  arm=f'{seed}-{kind}';env=os.environ|{'LIBGL_ALWAYS_SOFTWARE':'1','QA_SEED':str(seed)}|({'QA_PIONEER':'1'}if kind=='pioneer'else{})
  for resume in (False,True):
   name=f'{arm}'+('-resume'if resume else '')+'.log'
   with(b/name).open('wb')as f:subprocess.run([str(b/'install/bin/stella-egl')],env=env|({'QA_RESUME':'1'}if resume else {}),stdout=f,stderr=subprocess.STDOUT,check=True,timeout=1000)
   print('COMPLETE',name,flush=True)
  x=(b/f'{arm}-day21.json').read_bytes();y=(b/f'resume-{arm}-day21.json').read_bytes();assert x==y,arm
  def trace(path):
   result=[]
   for l in path.read_text().splitlines():
    try:tag,payload=l.split(' ',1);v=json.loads(payload)
    except (ValueError,json.JSONDecodeError):continue
    if tag in ('START',):continue
    if v.get('tick',0)>840:result.append(l)
    elif tag.startswith('WIND_') and v.get('time',0)>=1209600:result.append(l)
   return '\n'.join(result).encode()
  a=trace(b/f'{arm}.log');c=trace(b/f'{arm}-resume.log');assert a==c,(arm,'trace')
  proof[arm]={'endpoint_sha256':hashlib.sha256(x).hexdigest(),'trace_sha256':hashlib.sha256(a).hexdigest(),'trace_bytes':len(a)}
  print('EXACT_RESTART',arm,proof[arm],flush=True)
(b/'restart-proof.json').write_text(json.dumps(proof,indent=2))
