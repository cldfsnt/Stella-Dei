from pathlib import Path
import json,subprocess,hashlib,re,statistics,sys,datetime
r=Path(__file__).resolve().parents[2];o=r.parent/'site-tmp/wasm-land-empty-fast';empty=r.parent/'site-tmp/wasm-land-screen/empty-beta.json'
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
def run(label,arm,inp,ticks,trace):
 p=o/(label+'.json');l=o/(label+'.log')
 with l.open('w')as f:subprocess.run(['node',str(o/arm/'profile.js'),str(inp),str(o/'graph.json'),str(p),str(ticks),str(trace)],stdout=f,stderr=subprocess.STDOUT,check=True)
 return p,l.read_text()
if sys.argv[1]=='gates':
 live=Path(sys.argv[2]);j=json.loads(live.read_text());assert j['beta_origin']
 found=False
 for cell in j['origin']['cells']:
  for entry in cell.get('sparse',[]) or []:
   co=entry['value']
   if co['biomass']>0:
    co['root_fraction']=.25;found=True;break
  if found:break
 assert found,'Need valid living beta fixture; do not extend ecology to find roots.'
 prescribed=o/'prescribed-root-fallback.json';prescribed.write_text(json.dumps(j,separators=(',',':')))
 results={}
 for name,inp,ticks in [('empty',empty,72),('live',live,2),('prescribed-root',prescribed,2)]:
  rows=[]
  for arm in ['baseline','candidate']:
   p,l=run(name+'-'+arm,arm,inp,ticks,1);rows.append((p,l))
  assert rows[0][0].read_bytes()==rows[1][0].read_bytes(),(name,'state')
  hashes=[re.search(r'DELIVERED_HASH (\d+)',l)[1]for p,l in rows];assert hashes[0]==hashes[1],(name,'delivered')
  results[name]={'input_sha256':sha(inp),'endpoint_sha256':sha(rows[0][0]),'ticks':ticks,'fullstate_exact':True,'delivered_hash':hashes[0],'guard':next(x for x in rows[1][1].splitlines()if x.startswith('FAST_GUARD'))}
 (o/'gates.json').write_text(json.dumps(results,indent=2));print(results)
else:
 g=json.loads((o/'gates.json').read_text());rows=[];start=datetime.datetime.now(datetime.timezone.utc).isoformat()
 for i,arm in enumerate(['baseline','candidate','candidate','baseline']):
  p,l=run('time-'+str(i),arm,empty,72,0);assert sha(p)==g['empty']['endpoint_sha256'];ms=float(re.search(r'WASM_PLANET .*?total_ms=([\d.e+-]+)',l)[1]);row={'arm':arm,'index':i,'ms_per_tick':ms/60};rows.append(row);print(row,flush=True)
 a=statistics.median(x['ms_per_tick']for x in rows if x['arm']=='baseline');b=statistics.median(x['ms_per_tick']for x in rows if x['arm']=='candidate');result={'start':start,'end':datetime.datetime.now(datetime.timezone.utc).isoformat(),'rows':rows,'percent':100*(b/a-1),'baseline':a,'candidate':b};(o/'timing.json').write_text(json.dumps(result,indent=2));print(result)
