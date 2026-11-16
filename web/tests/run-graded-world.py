from pathlib import Path
import os,subprocess,json,hashlib,gzip
r=Path(__file__).resolve().parents[2];b=r.parent/'site-tmp/graded-world';e=r/'web/tests/continuation-review/graded-protection';summary=[]
for kind in ['control','candidate']:
 for p in ['0','0.5','1']:
  stem=f'{kind}-{p}'
  for restart in [False,True]:
   env=dict(os.environ,EGL_PLATFORM='surfaceless',LIBGL_ALWAYS_SOFTWARE='1',QA_KIND=kind,QA_P=p);env.pop('QA_RESUME',None)
   if restart:env['QA_RESUME']='1'
   with (b/(stem+('-resume'if restart else '')+'.log')).open('wb')as f:subprocess.run([str(b/'build/bin/stella-egl')],cwd=r,env=env,stdout=f,stderr=subprocess.STDOUT,check=True,timeout=900)
  for suffix in ['', '.activity.json']:
   assert (b/(stem+'-final.json'+suffix)).read_bytes()==(b/(stem+'-resume.json'+suffix)).read_bytes(),(stem,suffix)
  rows=lambda path:[json.loads(l[7:]) for l in path.read_text().splitlines() if l.startswith('GRADED ')]
  main=rows(b/(stem+'.log'));again=rows(b/(stem+'-resume.log'));assert main[60:]==again
  if p=='0':
   actual=json.loads((b/(stem+'-final.json')).read_text());expected=json.loads((r.parent/f'site-tmp/thermal-nurture/{kind}/final.json').read_text());actual.pop('ground_thermal',None);actual['version']=expected['version'];
   for cell in actual['origin']['cells']:
    for c in cell.get('cohorts',[])+[x['value']for x in cell.get('sparse',[])]:
     assert c.pop('protective_investment',0)==0 and c.pop('protective_recovery',0)==0 and c.pop('protective_rest',False)==False
   assert actual==expected,(stem,'p0 released-equation parity')
  parent=[next((c for c in x['cell']['cohorts']if c['lineage']==1),None)for x in main]
  summary.append({'kind':kind,'investment':float(p),'final_parent':parent[-1],'rest_ticks':sum(bool(c and c['protective_rest'])for c in parent),'cold_ticks':sum(x['temperature']<278 for x in main),'final_soil':main[-1]['soil'],'births':main[-1]['stats']['births'],'hash':hashlib.sha256((b/(stem+'-final.json')).read_bytes()).hexdigest()})
  for name in [stem+'.log',stem+'-resume.log',stem+'-final.json',stem+'-final.json.activity.json']:(e/(name+'.gz')).write_bytes(gzip.compress((b/name).read_bytes(),mtime=0))
(e/'results.json').write_text(json.dumps(summary,indent=2)+'\n');print(json.dumps(summary,indent=2))
