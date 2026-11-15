from pathlib import Path
import subprocess,json,re,hashlib,statistics,datetime,sys
r=Path(__file__).resolve().parents[2];o=r.parent/'site-tmp/wasm-land-borrowed';inp=r.parent/'site-tmp/wasm-land-screen/empty-beta.json';sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
def run(label,arm):
 p=o/(label+'.json');l=o/(label+'.log')
 with l.open('w')as f:subprocess.run(['node',str(o/arm/'profile.js'),str(inp),str(o/'graph.json'),str(p),'72','0'],stdout=f,stderr=subprocess.STDOUT,check=True)
 return p,l.read_text()
if sys.argv[1]=='gates':
 expected=json.loads((r.parent/'site-tmp/wasm-land-screen/gates.json').read_text())['beta-candidate']['sha256'];rows={}
 for arm in ['baseline','candidate']:
  p,l=run('gate-'+arm,arm);assert sha(p)==expected;rows[arm]=sha(p)
 (o/'gates.json').write_text(json.dumps(rows,indent=2));print(rows)
else:
 gates=json.loads((o/'gates.json').read_text());assert json.loads((o/'native/parity.json').read_text())['passed'];rows=[];start=datetime.datetime.now(datetime.timezone.utc).isoformat()
 for i,arm in enumerate(['baseline','candidate','candidate','baseline']):
  p,l=run('time-'+str(i),arm);assert sha(p)==gates[arm];ms=float(re.search(r'WASM_PLANET .*?total_ms=([\d.e+-]+)',l)[1]);row={'arm':arm,'index':i,'ms_per_tick':ms/60};rows.append(row);print(row,flush=True)
 a=statistics.median(x['ms_per_tick']for x in rows if x['arm']=='baseline');b=statistics.median(x['ms_per_tick']for x in rows if x['arm']=='candidate');result={'start':start,'end':datetime.datetime.now(datetime.timezone.utc).isoformat(),'rows':rows,'baseline':a,'candidate':b,'percent':100*(b/a-1)};(o/'timing.json').write_text(json.dumps(result,indent=2));print(result)
