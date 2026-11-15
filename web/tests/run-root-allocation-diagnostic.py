from pathlib import Path
from fractions import Fraction as F
import subprocess,os,json,hashlib,datetime
r=Path(__file__).resolve().parents[2];p=r.parent/'site-tmp/root-allocation-diagnostic';exe=p/'install/bin/stella-egl';results=[]
def rows(arm,tag,resume=False):return [json.loads(l.split(' ',1)[1]) for l in (p/f'{"resume" if resume else "main"}-0-{arm}.log').read_text().splitlines() if l.startswith(tag+' ')]
start=datetime.datetime.now(datetime.timezone.utc).isoformat()
for a in (0,1):
 for mode in ('main','resume'):
  with (p/f'{mode}-0-{a}.log').open('w') as f:subprocess.run([str(exe)],cwd=r,env=dict(os.environ,EGL_PLATFORM='surfaceless',LIBGL_ALWAYS_SOFTWARE='1',QA_DEPTH='0',QA_ARM=str(a),QA_JOURNEY_MODE=mode),stdout=f,stderr=subprocess.STDOUT,check=True,timeout=180)
 assert (p/f'depth-0-arm-{a}-60.json').read_bytes()==(p/f'resume-depth-0-arm-{a}-60.json').read_bytes()
 for tag in ('BIRTH','FATE','ROOT_WATER','PATCH','USED_H'):assert [x for x in rows(a,tag) if x['tick']>30]==rows(a,tag,True)
 phases=[x for x in rows(a,'ROOT_WATER') if x['lineage']==524];bytick={x['tick']:x for x in phases};used=rows(a,'USED_H')
 for x in phases:
  debit=F(x['soil_before'])-F(x['soil_after']);assert F(x['credit'])+F(x['bare_credit'])<=debit;assert F(x['h'])*F(x['demand'])<=F(x['credit'])<=F(x['demand'])
 for x in used:
  assert x['owner']==x['lineage']==524 and x['credit']==bytick[x['tick']]['credit'];assert x['denominator']==max(x['entry_demand'],x['current_demand']);assert F(x['h'])*F(x['denominator'])<=F(x['credit']);assert 0<=x['effective_h']<=x['h']<=1
  if x['current_demand']<=0:assert x['h']==0
 fate=[x for x in rows(a,'FATE') if x['cohort']['lineage']==524];patch=rows(a,'PATCH');assert len(patch)==60
 results.append({'arm':a,'root_fraction':.03125 if a==0 else .25,'alive24h':any(x['tick']==60 for x in fate),'last_alive_tick':fate[-1]['tick'] if fate else None,'last_live_cohort':fate[-1]['cohort'] if fate else None,'root_credit_kg_m2':sum(x['credit'] for x in phases),'positive_pulses':sum(x['credit']>0 for x in phases),'first_consumption':used[:2],'consumption_records':len(used),'direct_children':[x['child']['lineage'] for x in rows(a,'BIRTH') if x['child']['parent']==524],'restart_exact':True,'fate':fate})
a=json.loads((p/'depth-0-arm-0-0.json').read_text());b=json.loads((p/'depth-0-arm-1-0.json').read_text());diff=[]
def compare(a,b,path=''):
 if type(a)!=type(b):diff.append((path,a,b))
 elif isinstance(a,dict):
  assert a.keys()==b.keys()
  for k in a:compare(a[k],b[k],path+'/'+k)
 elif isinstance(a,list):
  assert len(a)==len(b)
  for i,(x,y) in enumerate(zip(a,b)):compare(x,y,path+'/'+str(i))
 elif a!=b:diff.append((path,a,b))
compare(a,b);assert len(diff)==1 and diff[0][0].endswith('/root_fraction') and diff[0][1:]==(.03125,.25),diff
assert (p/'depth-0-arm-0-60.json').read_bytes()==(p.parent/'origin-final-demand-shoreline/depth-0-arm-0-60.json').read_bytes()
co=results[0]['first_consumption'][0]['cohort'];support=co['support_mass'];opportunity={'support_at_first_consumption':support,'original_root':support/32,'prescribed_root':support/4,'aboveground_original':support*(1-1/32),'aboveground_prescribed':support*.75,'aboveground_relative_reduction':1-.75/(1-1/32)}
report={'start_utc':start,'end_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'initial_only_difference':diff,'control_exact_frozen':True,'opportunity_at_first_consumption':opportunity,'arms':results,'hashes':{x.name:hashlib.sha256(x.read_bytes()).hexdigest() for x in p.glob('*.json')}}
(p/'results.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps({k:v for k,v in report.items() if k not in ('arms','hashes')},indent=2));print(json.dumps([{k:v for k,v in a.items() if k not in ('fate','first_consumption')} for a in results],indent=2))
