from pathlib import Path
import subprocess,json,re,hashlib,statistics,datetime,sys
r=Path(__file__).resolve().parents[2];o=r.parent/'site-tmp/wasm-wind-stages';source=r.parent/'site-tmp/foraging-production/warm-actual-end.json';original=json.loads((r.parent/'site-tmp/wasm-wind-screen/gates.json').read_text())['off_sandbox82'];sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
def run(label,arm):
 p=o/(label+'.json');l=o/(label+'.log')
 with l.open('w')as f:subprocess.run(['node',str(o/arm/'profile.js'),str(source),str(o/'graph.json'),str(p),'72','0'],stdout=f,stderr=subprocess.STDOUT,check=True)
 assert sha(p)==original[arm]['sha256'],(arm,'instrumentation state/RNG')
 text=l.read_text();stages=[float(x.strip())/60 for x in re.search(r'WIND_STAGES .*?=\{([^}]+)\}',text)[1].split(',')];total=float(re.search(r'WASM_PLANET .*?total_ms=([\d.e+-]+)',text)[1])/60
 return {'arm':arm,'ms_per_tick':total,'stages_ms':stages,'endpoint_sha256':sha(p)}
if sys.argv[1]=='gates':
 result=[run('gate-'+arm,arm)for arm in ['baseline','candidate']];(o/'gates.json').write_text(json.dumps(result,indent=2));print(result)
else:
 assert (o/'gates.json').exists();start=datetime.datetime.now(datetime.timezone.utc).isoformat();rows=[]
 for i,arm in enumerate(['baseline','candidate','candidate','baseline']):
  row=run('time-'+str(i),arm);row['index']=i;rows.append(row);print(row,flush=True)
 summary={arm:{'median_ms':statistics.median(x['ms_per_tick']for x in rows if x['arm']==arm),'median_stages':[statistics.median(x['stages_ms'][j]for x in rows if x['arm']==arm)for j in range(5)]}for arm in ['baseline','candidate']}
 result={'start':start,'end':datetime.datetime.now(datetime.timezone.utc).isoformat(),'rows':rows,'summary':summary};(o/'timing.json').write_text(json.dumps(result,indent=2));print(result)
