from pathlib import Path
import json,hashlib,shutil
r=Path(__file__).resolve().parents[2];tmp=r.parent/'site-tmp';o=tmp/'wasm-root-wind-established';o.mkdir(exist_ok=True);old=tmp/'wasm-root-wind-screen';sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
# Reuse exact accepted binary; control/API work made no scheduler changes.
for p in (tmp/'root-wind-controls/src/simulation').rglob('*'):
 if p.is_file():
  q=tmp/'root-wind-combined/src/simulation'/p.relative_to(tmp/'root-wind-controls/src/simulation');assert p.read_bytes()==q.read_bytes()
(o/'candidate').symlink_to((old/'candidate').resolve(),target_is_directory=True)
shutil.copy2(old/'graph.json',o/'graph.json')
for seed in [42,1337]:
 source=tmp/f'combined-strategy/{seed}-pioneer-day7.json';shutil.copy2(source,o/f'{seed}.json');x=json.loads(source.read_text());x['version']=10;x.pop('wind_dispersal')
 for c in x['origin']['cells']:
  for co in c.get('cohorts',[])or []:co.pop('aerial_allocation',None)
  for e in c.get('sparse',[])or []:e['value'].pop('aerial_allocation',None)
 (o/f'{seed}-projected-off.json').write_text(json.dumps(x,separators=(',',':')))
(o/'binary.json').write_text(json.dumps({p.name:{'sha256':sha(p),'bytes':p.stat().st_size}for p in [o/'candidate/profile.js',o/'candidate/profile.wasm']},indent=2)+'\n')
s=(r/'web/tests/run-wasm-root-wind-screen.py').read_text().replace("o=r.parent/'site-tmp/wasm-root-wind-screen'","o=r.parent/'site-tmp/wasm-root-wind-established'")
a=s.index('pairs=');b=s.index('\ndef run',a);s=s[:a]+"pairs={str(seed):{'A':('candidate',str(seed)+'-projected-off.json'),'B':('candidate',str(seed)+'.json')}for seed in [42,1337]}"+s[b:]
(r/'web/tests/run-root-wind-established-cost.py').write_text(s)
print('Prepared exact existing binary and fixed day7 inputs; no gates/timing executed')
