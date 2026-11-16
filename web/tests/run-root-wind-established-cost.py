from pathlib import Path
import subprocess,json,re,hashlib,statistics,datetime,sys
r=Path(__file__).resolve().parents[2];o=r.parent/'site-tmp/wasm-root-wind-established';sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
pairs={str(seed):{'A':('candidate',str(seed)+'-projected-off.json'),'B':('candidate',str(seed)+'.json')}for seed in [42,1337]}
def run(label,arm,inp,ticks):
 p=o/(label+'.json');l=o/(label+'.log')
 with l.open('w')as f:subprocess.run(['node',str(o/arm/'profile.js'),str(inp),str(o/'graph.json'),str(p),str(ticks),'0'],stdout=f,stderr=subprocess.STDOUT,check=True,timeout=300)
 return p,l.read_text()
def normalized(x):
 if isinstance(x,dict):return {k:normalized(v)for k,v in x.items()if not(k=='cohorts'and v==[])}
 if isinstance(x,list):return [normalized(v)for v in x]
 return x
if sys.argv[1]=='gates':
 result={}
 for scenario,arms in pairs.items():
  result[scenario]={};ends={}
  for label,(arm,name)in arms.items():
   inp=o/name;prefix=scenario+'-'+label
   p,log=run(prefix+'-zero',arm,inp,0);assert normalized(json.loads(p.read_bytes()))==normalized(json.loads(inp.read_bytes())),(prefix,'zero')
   p,log=run(prefix+'-72',arm,inp,72);ends[label]=p
   q,_=run(prefix+'-resume',arm,p,10);v,_=run(prefix+'-82',arm,inp,82);assert q.read_bytes()==v.read_bytes(),(prefix,'restart')
   result[scenario][label]={'arm':arm,'input':name,'input_sha256':sha(inp),'endpoint_sha256':sha(p),'save_bytes':p.stat().st_size,'zero_typed_exact':True,'restart_exact':True,'layout':[s for s in log.splitlines()if any(k in s for k in ['LAYOUT','MEMORY','HEAP_CAPACITY','WIND_FINAL'])]}
  if scenario=='historical_off':assert ends['A'].read_bytes()==ends['B'].read_bytes(),'historical state/RNG'
  print(scenario,result[scenario],flush=True)
 (o/'gates.json').write_text(json.dumps(result,indent=2)+'\n')
elif sys.argv[1]=='timing':
 gates=json.loads((o/'gates.json').read_text());rows=[];start=datetime.datetime.now(datetime.timezone.utc).isoformat()
 for scenario,arms in pairs.items():
  for i,label in enumerate(['A','B','B','A']):
   arm,name=arms[label];p,log=run('time-'+scenario+'-'+str(i),arm,o/name,72);assert sha(p)==gates[scenario][label]['endpoint_sha256'];ms=float(re.search(r'WASM_PLANET .*?total_ms=([\d.e+-]+)',log)[1]);row={'scenario':scenario,'label':label,'index':i,'total_ms':ms,'ms_per_tick':ms/60};rows.append(row);print(row,flush=True)
 summary={}
 for scenario in pairs:
  a=[v['ms_per_tick']for v in rows if v['scenario']==scenario and v['label']=='A'];b=[v['ms_per_tick']for v in rows if v['scenario']==scenario and v['label']=='B'];am=statistics.median(a);bm=statistics.median(b);summary[scenario]={'A_ms':a,'B_ms':b,'A_median_ms':am,'B_median_ms':bm,'percent':100*(bm/am-1)}
 (o/'timing.json').write_text(json.dumps({'start':start,'end':datetime.datetime.now(datetime.timezone.utc).isoformat(),'rows':rows,'summary':summary},indent=2)+'\n');print(summary)
