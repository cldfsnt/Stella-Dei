from pathlib import Path
import subprocess,json,hashlib,re,statistics,datetime,sys
r=Path(__file__).resolve().parents[2];o=r.parent/'site-tmp/wasm-land-screen'
inputs={'natural':r.parent/'site-tmp/natural60-day60.json','warm':r.parent/'site-tmp/foraging-production/warm-actual-end.json','empty':o/'empty-off.json','beta':o/'empty-beta.json'}
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
def norm(j):
 j=json.loads(json.dumps(j));j['version']=7
 j.setdefault('sandbox_defense',None)
 for p in j['plants']:p.setdefault('toughness',0)
 if j.get('origin'):
  for c in j['origin']['cells']:
   if c.get('cohorts')==[]:c.pop('cohorts')
 return j
def run(name,arm,inp,ticks):
 p=o/(name+'.json');l=o/(name+'.log')
 with l.open('w')as f:subprocess.run(['node',str(o/arm/'profile.js'),str(inp),str(o/'graph.json'),str(p),str(ticks),'0'],stdout=f,stderr=subprocess.STDOUT,check=True)
 return p,json.loads(p.read_text()),l.read_text()
if sys.argv[1]=='gates':
 result={}
 for name,inp in inputs.items():
  arms=['candidate']if name=='beta'else ['baseline','candidate']
  endpoints={}
  for arm in arms:
   pre,j,_=run(name+'-'+arm+'-zero',arm,inp,0);assert norm(j)==norm(json.loads(inp.read_text())),(name,arm,'zero')
   p,j,l=run(name+'-'+arm+'-72',arm,inp,72);endpoints[arm]=norm(j)
   q,k,_=run(name+'-'+arm+'-resume',arm,p,10);v,z,_=run(name+'-'+arm+'-82',arm,inp,82);assert k==z,(name,arm,'continuation')
   row={'sha256':sha(p),'bytes':p.stat().st_size,'continuation_exact':True,'layout':[x for x in l.splitlines()if 'LAYOUT' in x]}
   if name=='beta':
    b=j['beta_origin'];assert all(0<=v<=1 for v in b['soil']);assert all(0<=v<=3.4028234663852886e38 for v in b['vapor']);row.update(soil_sum_density=sum(b['soil']),soil_max=max(b['soil']),soil_positive=sum(v>0 for v in b['soil']))
   result[name+'-'+arm]=row
  if len(arms)==2:assert endpoints['baseline']==endpoints['candidate'],(name,'off parity')
 (o/'gates.json').write_text(json.dumps(result,indent=2));print(json.dumps(result,indent=2))
else:
 gates=json.loads((o/'gates.json').read_text());rows=[];start=datetime.datetime.now(datetime.timezone.utc).isoformat()
 for scenario in ['natural','warm','empty','beta']:
  for i,arm in enumerate(['baseline','candidate','candidate','baseline']):
   inp=inputs['empty']if scenario=='beta'and arm=='baseline'else inputs[scenario]
   key=('empty'if scenario=='beta'and arm=='baseline'else scenario)+'-'+arm
   p,j,l=run(f'time-{scenario}-{i}',arm,inp,72);assert sha(p)==gates[key]['sha256']
   ms=float(re.search(r'WASM_PLANET .*?total_ms=([\d.e+-]+)',l)[1]);row={'scenario':scenario,'index':i,'arm':arm,'ms_per_tick':ms/60};rows.append(row);print(row,flush=True)
 summary={}
 for s in ['natural','warm','empty','beta']:
  a=statistics.median(x['ms_per_tick']for x in rows if x['scenario']==s and x['arm']=='baseline');b=statistics.median(x['ms_per_tick']for x in rows if x['scenario']==s and x['arm']=='candidate');summary[s]={'baseline_ms':a,'candidate_ms':b,'percent':100*(b/a-1)}
 (o/'timing.json').write_text(json.dumps({'start':start,'end':datetime.datetime.now(datetime.timezone.utc).isoformat(),'rows':rows,'summary':summary},indent=2));print(summary)
