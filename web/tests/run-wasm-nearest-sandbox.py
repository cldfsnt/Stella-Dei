#!/usr/bin/env python3
from pathlib import Path
import subprocess,json,hashlib,re,statistics,datetime,sys
r=Path(__file__).resolve().parents[2];o=r.parent/'site-tmp/wasm-nearest-sandbox';inp=r.parent/'site-tmp/foraging-production/warm-actual-end.json'
def run(label,mode,ticks,source=inp):
 dest=o/(label+'.json');log=o/(label+'.log')
 with log.open('w')as f:
  p=subprocess.run(['node',str(o/'profile.js'),str(source),str(o/'graph.json'),str(dest),str(ticks),str(mode)],cwd=r,stdout=f,stderr=subprocess.STDOUT)
 assert p.returncode==0,(label,p.returncode)
 return dest,log
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
if len(sys.argv)<2 or sys.argv[1]=='gates':
 proof={}
 for mode in (0,1):
  z,_=run(f'zero-{mode}',mode,0);assert json.loads(z.read_text())==json.loads(inp.read_text());proof[f'zero-{mode}']=sha(z)
  end,_=run(f'gate72-{mode}',mode,72)
  resumed,_=run(f'resumed-{mode}',mode,10,end)
  full,_=run(f'full82-{mode}',mode,82)
  assert resumed.read_bytes()==full.read_bytes(),('continuation',mode)
  proof[f'end72-{mode}']=sha(end);proof[f'continuation82-{mode}']=sha(full)
 assert (o/'gate72-0.json').read_bytes()==(o/'gate72-1.json').read_bytes()
 assert (o/'full82-0.json').read_bytes()==(o/'full82-1.json').read_bytes()
 (o/'integrity.json').write_text(json.dumps(proof,indent=2)+'\n');print('ALL_GATES_PASS')
else:
 assert sys.argv[1]=='timing'
 proof=json.loads((o/'integrity.json').read_text());rows=[];start=datetime.datetime.now(datetime.timezone.utc).isoformat()
 for arm,mode in enumerate([0,1,1,0]):
  dest,log=run(f'timing-{arm}',mode,72);assert sha(dest)==proof[f'end72-{mode}']
  line=next(l for l in log.read_text().splitlines()if l.startswith('WASM_PLANET '))
  total=float(re.search(r'total_ms=([\d.e+\-]+)',line)[1])
  rows.append(dict(arm=arm,candidate=bool(mode),timed_ticks=60,warmup_ticks=12,total_ms=total,per_tick_ms=total/60,endpoint_sha256=sha(dest)))
  print(json.dumps(rows[-1]),flush=True)
 b=statistics.median(x['per_tick_ms']for x in rows if not x['candidate']);c=statistics.median(x['per_tick_ms']for x in rows if x['candidate'])
 result=dict(start_utc=start,end_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),records=rows,baseline_median_ms=b,candidate_median_ms=c,change_percent=100*(c/b-1),scope='Actual wasm32 full Planet.simulate in Node; no rendering/browser/rAF/device FPS. One fixed world; fixed ABBA, no repeat-selection.')
 (o/'results.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result,indent=2))
