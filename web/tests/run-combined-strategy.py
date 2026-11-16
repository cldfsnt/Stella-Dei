from pathlib import Path
import subprocess,os,json,sys,hashlib
r=Path(__file__).resolve().parents[2];b=r.parent/'site-tmp/combined-strategy';exe=b/'install/bin/stella-egl'
def run(seed,kind,name,**kw):
 env=os.environ|{'LIBGL_ALWAYS_SOFTWARE':'1','QA_SEED':str(seed)}|({'QA_PIONEER':'1'}if kind=='pioneer'else{})|{k:str(v)for k,v in kw.items()}
 with(b/name).open('wb')as f:subprocess.run([str(exe)],env=env,stdout=f,stderr=subprocess.STDOUT,check=True,timeout=1000)
def normalize(s):
 s=json.loads(json.dumps(s));s['version']=10;s.pop('wind_dispersal',None)
 for c in s['origin']['cells']:
  for co in c['sparse']:co['value'].pop('aerial_allocation',None)
 return s
if '--execute' not in sys.argv:
 proof={}
 for seed in (42,1337):
  for kind in ('ordinary','pioneer'):run(seed,kind,f'{seed}-{kind}-preflight.log',QA_PREFLIGHT=1)
  a=json.load(open(b/f'{seed}-ordinary-preseed.json'));p=json.load(open(b/f'{seed}-pioneer-preseed.json'));assert normalize(a)==normalize(p)
  a=json.load(open(b/f'{seed}-ordinary-initial.json'));p=json.load(open(b/f'{seed}-pioneer-initial.json'));assert normalize(a)==normalize(p)
  records=[]
  for kind in ('ordinary','pioneer'):
   lines=(b/f'{seed}-{kind}-preflight.log').read_text().splitlines();rows=lambda t:[json.loads(l.split(' ',1)[1])for l in lines if l.startswith(t+' ')];e=rows('ELIGIBILITY')[0];receipt=rows('BULK_RECEIPT')[0];founders=rows('FOUNDER');assert len(founders)==len(e['indices']);assert[ x['cell']for x in founders]==e['indices'];records.append({'kind':kind,'eligible':e['indices'],'receipt':receipt,'worldseed':a['seed']})
  assert records[0]['eligible']==records[1]['eligible'];assert records[0]['receipt']==records[1]['receipt'];proof[str(seed)]=records
 (b/'preflight-proof.json').write_text(json.dumps(proof,indent=2));print(json.dumps(proof,indent=2));print('PREFLIGHT_MATCHED_ENV_RESOURCES_LOCATION_ONLY_AERIAL_CONFIG_DIFF_PASS')
else:
 for seed in (42,1337):
  for kind in ('ordinary','pioneer'):
   run(seed,kind,f'{seed}-{kind}.log');run(seed,kind,f'{seed}-{kind}-resume.log',QA_RESUME=1)
   a=b/f'{seed}-{kind}-day7.json';p=b/f'resume-{seed}-{kind}-day7.json';assert a.read_bytes()==p.read_bytes();print(seed,kind,'EXACT_RESTART',hashlib.sha256(a.read_bytes()).hexdigest(),flush=True)
