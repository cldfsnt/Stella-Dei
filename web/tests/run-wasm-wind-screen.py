from pathlib import Path
import subprocess,json,re,hashlib,statistics,datetime,sys
r=Path(__file__).resolve().parents[2];o=r.parent/'site-tmp/wasm-wind-screen';sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
inputs={'off_origin30':{a:r.parent/'site-tmp/natural60-day30.json' for a in ['baseline','candidate']},'off_sandbox82':{a:r.parent/'site-tmp/foraging-production/warm-actual-end.json' for a in ['baseline','candidate']},'enabled_pioneer_day3':{'baseline':o/'pioneer-day3-projected-legacy.json','candidate':o/'pioneer-day3.json'}}
def run(label,arm,source,ticks):
 p=o/(label+'.json');l=o/(label+'.log')
 with l.open('w')as f:subprocess.run(['node',str(o/arm/'profile.js'),str(source),str(o/'graph.json'),str(p),str(ticks),'0'],stdout=f,stderr=subprocess.STDOUT,check=True)
 return p,l.read_text()
def canonical(x):
 if isinstance(x,dict) and "plants" in x and "version" in x:
  x=dict(x)
  if x["version"]<=7:x["version"]=7
  x.setdefault("sandbox_defense",None)
  x["plants"]=[dict(p,toughness=p.get("toughness",0))for p in x["plants"]]
 if isinstance(x,dict):return {k:canonical(v)for k,v in x.items() if not(k=='cohorts' and v==[])}
 if isinstance(x,list):return [canonical(v)for v in x]
 return x
if sys.argv[1]=='gates':
 result={}
 for name,arms in inputs.items():
  ends={};rows={}
  for arm,inp in arms.items():
   z,_=run(name+'-'+arm+'-zero',arm,inp,0);assert canonical(json.loads(z.read_text()))==canonical(json.loads(inp.read_text())),(name,arm,'zero')
   p,l=run(name+'-'+arm+'-72',arm,inp,72);ends[arm]=p
   q,_=run(name+'-'+arm+'-resume',arm,p,10);v,_=run(name+'-'+arm+'-82',arm,inp,82);assert q.read_bytes()==v.read_bytes(),(name,arm,'restart')
   rows[arm]={'input_sha256':sha(inp),'sha256':sha(p),'bytes':p.stat().st_size,'zero_typed_exact':True,'fresh_process_restart_exact':True,'layout':re.search(r'LAYOUT .*',l)[0],'wind_final':re.search(r'WIND_FINAL .*',l)[0]if 'WIND_FINAL' in l else None}
  if name.startswith('off_'):assert ends['baseline'].read_bytes()==ends['candidate'].read_bytes(),(name,'state/RNG')
  result[name]=rows;print(name,rows,flush=True)
 (o/'gates.json').write_text(json.dumps(result,indent=2))
else:
 gates=json.loads((o/'gates.json').read_text());rows=[];start=datetime.datetime.now(datetime.timezone.utc).isoformat()
 for name,arms in inputs.items():
  for i,arm in enumerate(['baseline','candidate','candidate','baseline']):
   p,l=run('time-'+name+'-'+str(i),arm,arms[arm],72);assert sha(p)==gates[name][arm]['sha256'];ms=float(re.search(r'WASM_PLANET .*?total_ms=([\d.e+-]+)',l)[1]);row={'scenario':name,'arm':arm,'index':i,'ms_per_tick':ms/60};rows.append(row);print(row,flush=True)
 summary={}
 for name in inputs:
  a=statistics.median(x['ms_per_tick']for x in rows if x['scenario']==name and x['arm']=='baseline');b=statistics.median(x['ms_per_tick']for x in rows if x['scenario']==name and x['arm']=='candidate');summary[name]={'baseline':a,'candidate':b,'percent':100*(b/a-1)}
 result={'start':start,'end':datetime.datetime.now(datetime.timezone.utc).isoformat(),'rows':rows,'summary':summary};(o/'timing.json').write_text(json.dumps(result,indent=2));print(result)
