from pathlib import Path
import os,subprocess,json,gzip,hashlib
r=Path(__file__).resolve().parents[2];b=r.parent/'site-tmp/dry-establishment';exe=b/'build/bin/stella-egl'
def run(stage,off=False):
 env={**os.environ,'EGL_PLATFORM':'surfaceless','LIBGL_ALWAYS_SOFTWARE':'1','QA_STAGE':stage}
 if off:env['QA_OFF']='1'
 name=stage+('-off'if off else '')
 with (b/(name+'.log')).open('w')as f:subprocess.run([str(exe)],cwd=r,env=env,stdout=f,stderr=subprocess.STDOUT,check=True)
if not (b/'birth.json').exists():run('reconstruct')
def rows(lines):
 out=[]
 for line in lines:
  try:tag,raw=line.split(' ',1);x=json.loads(raw)
  except (ValueError,TypeError):continue
  if tag=='DRAWDOWN' or (tag in ['BIRTH_OR_INITIAL','DEATH','PROTECTION_STATE','DAILY','PATCH','ROOT_DAILY'] and 420<x.get('tick',0)<=592):out.append((tag,x))
 return out
with gzip.open(r/'web/tests/continuation-review/protective-natural-journey/main.log.gz','rt')as f:old=rows(f)
new=rows((b/'reconstruct.log').read_text().splitlines());assert sorted(old,key=lambda x:json.dumps(x,sort_keys=True))==sorted(new,key=lambda x:json.dumps(x,sort_keys=True)),('reconstruction event mismatch',len(old),len(new),next(((a,c)for a,c in zip(old,new)if a!=c),None))
print('EXACT_RECONSTRUCTION_RECORDED_ROWS',len(old),flush=True)
run('parity');run('parity',True);assert (b/'parity-on.json').read_bytes()==(b/'parity-off.json').read_bytes();print('EXACT_HOOK_PARITY',flush=True)
run('control');run('candidate')
def summary(stage):
 p=b/(stage+'.log');events=[];loss={};subject=[]
 for l in p.read_text().splitlines():
  try:tag,raw=l.split(' ',1);x=json.loads(raw)
  except(ValueError,TypeError):continue
  if tag.startswith('LOSS_'):loss.setdefault(tag,[]).append(x)
  if tag=='SUBJECT':subject.append(x)
  if tag in ('BIRTH_OR_INITIAL','DEATH') and x.get('tick',0)>592:events.append((tag,x))
 x=json.loads((b/(stage+'.json')).read_text());alive=[{'point':i,**v['value']}for i,c in enumerate(x['origin']['cells'])for v in c['sparse']if v['value']['biomass']>0];own=[c for c in alive if c['lineage']==246];children=[c for c in alive if c['parent']==246]
 return {'endpoint_sha256':hashlib.sha256((b/(stage+'.json')).read_bytes()).hexdigest(),'subject_final':own,'children_surviving':children,'subject_death':[z for t,z in events if t=='DEATH'and z['id']==246],'subject_births':[z for t,z in events if t=='BIRTH_OR_INITIAL'and z['cohort']['parent']==246],'upkeep':sum(z['paid']for z in loss.get('LOSS_UPKEEP',[])),'mortality':sum(z['dead']for z in loss.get('LOSS_MORTALITY',[])),'growth':sum(z['growth']for z in loss.get('LOSS_GROWTH',[])),'cleanup':[z for z in loss.get('LOSS_MORTALITY',[])if z['cleanup']],'loss_rows':loss,'subject_rows':subject}
out={s:summary(s)for s in ['control','candidate']};(b/'results.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps({s:{k:v for k,v in z.items()if k not in ['loss_rows','subject_rows']}for s,z in out.items()},indent=2))
