from pathlib import Path
import subprocess,os,json,hashlib
r=Path(__file__).resolve().parents[2];base=r.parent/'site-tmp/cutoff-trial';proof={}
for seed in(42,1337):
 for mode in('legacy','small'):
  b=base/mode;arm=f'{seed}-pioneer';env=os.environ|{'LIBGL_ALWAYS_SOFTWARE':'1','QA_SEED':str(seed),'QA_PIONEER':'1'}
  for resumed in(False,True):
   name=arm+('-resume'if resumed else '')+'.log'
   with(b/name).open('wb')as f:subprocess.run([str(b/'install/bin/stella-egl')],env=env|({'QA_RESUME':'1'}if resumed else {}),stdout=f,stderr=subprocess.STDOUT,check=True,timeout=1000)
   print('COMPLETE',mode,name,flush=True)
  x=(b/f'{arm}-day14.json').read_bytes();y=(b/f'resume-{arm}-day14.json').read_bytes();assert x==y
  v=json.loads(x);assert v['format']=='cutoff_qa_v1';assert abs(v['threshold']-({'legacy':.0025,'small':.001}[mode]))<1e-9
  if mode=='legacy':assert v['state']==json.load(open(r.parent/'site-tmp/combined-day21'/f'{arm}-day14.json'))
  def trace(path):
   z=[]
   for line in path.read_text().splitlines():
    try:tag,w=line.split(' ',1);w=json.loads(w)
    except(ValueError,json.JSONDecodeError):continue
    if tag=='START':continue
    if w.get('tick',0)>600 or tag.startswith('WIND_')and w.get('time',0)>=864000:z.append(line)
   return '\n'.join(z).encode()
  a=trace(b/f'{arm}.log');c=trace(b/f'{arm}-resume.log');assert a==c
  proof[f'{seed}-{mode}']={'sha256':hashlib.sha256(x).hexdigest(),'trace_sha256':hashlib.sha256(a).hexdigest(),'legacy_exact_previous':mode=='legacy'}
  print('EXACT_RESTART',seed,mode,proof[f'{seed}-{mode}'],flush=True)
(base/'restart-proof.json').write_text(json.dumps(proof,indent=2))
