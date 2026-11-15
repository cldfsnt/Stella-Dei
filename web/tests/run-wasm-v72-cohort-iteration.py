from pathlib import Path
import subprocess,json,re,hashlib,statistics,datetime,sys
r=Path(__file__).resolve().parents[2];o=r.parent/'site-tmp/wasm-v72-cohort-iteration';inputs={'dense_paid_autoseed':r.parent/'site-tmp/auto-seed/after.json','early_natural30':r.parent/'site-tmp/natural60-day30.json'};sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
def count(j):
 living=occupied=active=0
 for c in j['origin']['cells']:
  cs=c.get('cohorts',[])or [e['value']for e in c.get('sparse',[])or []];n=sum(co['biomass']>0 for co in cs);living+=n;occupied+=n>0;active+=n>0 or c['detritus']>0
 return dict(living=living,occupied=occupied,active=active)
def run(label,arm,source,ticks):
 p=o/(label+'.json');l=o/(label+'.log')
 with l.open('w')as f:subprocess.run(['node',str(o/arm/'profile.js'),str(source),str(o/'graph.json'),str(p),str(ticks),'0'],stdout=f,stderr=subprocess.STDOUT,check=True)
 return p,l.read_text()
if sys.argv[1]=='gates':
 result={}
 for name,inp in inputs.items():
  ends={};rows={}
  for arm in ['baseline','candidate']:
   p,l=run(name+'-'+arm+'-72',arm,inp,72);ends[arm]=p
   q,_=run(name+'-'+arm+'-resume',arm,p,10);v,_=run(name+'-'+arm+'-82',arm,inp,82);assert q.read_bytes()==v.read_bytes(),(name,arm,'restart')
   rows[arm]={'sha256':sha(p),'bytes':p.stat().st_size,'endpoint_counts':count(json.loads(p.read_text())),'fresh_process_restart_exact':True}
  assert ends['baseline'].read_bytes()==ends['candidate'].read_bytes(),(name,'state/RNG')
  result[name]={'input_sha256':sha(inp),'input_counts':count(json.loads(inp.read_text())),'arms':rows}
 (o/'gates.json').write_text(json.dumps(result,indent=2));print(result)
else:
 gates=json.loads((o/'gates.json').read_text());rows=[];start=datetime.datetime.now(datetime.timezone.utc).isoformat()
 for name,inp in inputs.items():
  for i,arm in enumerate(['baseline','candidate','candidate','baseline']):
   p,l=run('time-'+name+'-'+str(i),arm,inp,72);assert sha(p)==gates[name]['arms'][arm]['sha256'];ms=float(re.search(r'WASM_PLANET .*?total_ms=([\d.e+-]+)',l)[1]);row={'scenario':name,'arm':arm,'index':i,'ms_per_tick':ms/60};rows.append(row);print(row,flush=True)
 summary={}
 for name in inputs:
  a=statistics.median(x['ms_per_tick']for x in rows if x['scenario']==name and x['arm']=='baseline');b=statistics.median(x['ms_per_tick']for x in rows if x['scenario']==name and x['arm']=='candidate');summary[name]={'baseline':a,'candidate':b,'percent':100*(b/a-1)}
 result={'start':start,'end':datetime.datetime.now(datetime.timezone.utc).isoformat(),'rows':rows,'summary':summary};(o/'timing.json').write_text(json.dumps(result,indent=2));print(result)
