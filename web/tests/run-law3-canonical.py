from pathlib import Path
import os,subprocess,json,re,hashlib,statistics,datetime,sys
r=Path(__file__).resolve().parents[2];tmp=r.parent/'site-tmp';o=tmp/'law3-canonical';sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
inputs={'early-off':o/'early-off.json','early-law3':o/'early-law3.json','populated-law3':o/'day30-100mm.json','historical-law1':tmp/'origin-land-day30/day-30.json','historical-law2':tmp/'origin-basal-native/law2-initial.json'}
def norm(j):
 j=json.loads(json.dumps(j));
 if not j.get('beta_origin'):j['version']=7
 j.setdefault('sandbox_defense',None)
 for p in j['plants']:p.setdefault('toughness',0)
 if j.get('origin'):
  for c in j['origin']['cells']:
   if c.get('cohorts')==[]:c.pop('cohorts')
 return j
def run(label,arm,inp,ticks):
 p=o/(label+'.json');l=o/(label+'.log')
 with l.open('w')as f:subprocess.run(['node',str(o/arm/'profile.js'),str(inp),str(o/'graph.json'),str(p),str(ticks),'0'],stdout=f,stderr=subprocess.STDOUT,check=True,timeout=180)
 return p,l.read_text()
if sys.argv[1]=='gates':
 result={}
 for scenario,inp in inputs.items():
  end={}
  for arm in ['baseline','candidate']:
   z,_=run(f'{scenario}-{arm}-zero',arm,inp,0);assert norm(json.loads(z.read_bytes()))==norm(json.loads(inp.read_bytes())),(scenario,arm,'zero')
   n=72 if scenario in ['early-off','early-law3','populated-law3']else 4
   p,log=run(f'{scenario}-{arm}-{n}',arm,inp,n);end[arm]=p.read_bytes()
   if 'law3' in scenario:
    q,_=run(f'{scenario}-{arm}-resume',arm,p,2);s,_=run(f'{scenario}-{arm}-continuous',arm,inp,n+2);assert q.read_bytes()==s.read_bytes(),(scenario,arm,'restart')
   result[scenario+'-'+arm]={'sha256':sha(p),'ticks':n,'zero_exact':True,'restart_exact':True if 'law3'in scenario else None,'layout':[line for line in log.splitlines()if 'MEMORY' in line or 'LAYOUT' in line]}
  assert end['baseline']==end['candidate'],(scenario,'borrowed parity')
 # Actual native reference vs canonical borrowed on unchanged fixed day30/100mm.
 for name,inp in [('law3',tmp/'origin-final-demand-native/law3-initial.json'),('law2',inputs['historical-law2']),('law1',inputs['historical-law1']),('populated100mm',inputs['populated-law3']),('legacy',tmp/'natural60-day60.json')]:
  files=[]
  for arm,exe in [('reference',tmp/'origin-final-demand-native/install/bin/stella-egl'),('candidate',o/'native/install/bin/stella-egl')]:
   p=o/f'native-{name}-{arm}.json';env=dict(os.environ,EGL_PLATFORM='surfaceless',LIBGL_ALWAYS_SOFTWARE='1',QA_LAND_INPUT=str(inp),QA_LAND_OUTPUT=str(p),QA_LAND_TICKS='4')
   with (o/f'native-{name}-{arm}.log').open('w')as f:subprocess.run([str(exe)],cwd=r,env=env,stdout=f,stderr=subprocess.STDOUT,check=True,timeout=180)
   files.append(p)
  assert files[0].read_bytes()==files[1].read_bytes(),('native',name)
  result['native-'+name]={'exact':True,'sha256':sha(files[0])}
 (o/'gates.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result,indent=2))
else:
 gates=json.loads((o/'gates.json').read_text());start=datetime.datetime.now(datetime.timezone.utc).isoformat();rows=[]
 for scenario in ['early-off','early-law3','populated-law3']:
  for i,arm in enumerate(['baseline','candidate','candidate','baseline']):
   p,log=run(f'time-{scenario}-{i}',arm,inputs[scenario],72);assert sha(p)==gates[scenario+'-'+arm]['sha256']
   ms=float(re.search(r'WASM_PLANET .*?total_ms=([\d.e+-]+)',log)[1]);row={'scenario':scenario,'index':i,'arm':arm,'ms_per_tick':ms/60};rows.append(row);print(row,flush=True)
 summary={}
 for scenario in ['early-off','early-law3','populated-law3']:
  a=statistics.median(x['ms_per_tick']for x in rows if x['scenario']==scenario and x['arm']=='baseline');b=statistics.median(x['ms_per_tick']for x in rows if x['scenario']==scenario and x['arm']=='candidate');summary[scenario]={'reference_ms':a,'canonical_ms':b,'percent':100*(b/a-1)}
 out={'start':start,'end':datetime.datetime.now(datetime.timezone.utc).isoformat(),'rows':rows,'summary':summary};(o/'timing.json').write_text(json.dumps(out,indent=2)+'\n');print(summary)
