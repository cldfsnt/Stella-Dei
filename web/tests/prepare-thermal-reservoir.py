#!/usr/bin/env python3
"""Fixed 0.1m versus 0.5m ground thermal reservoir assay; no production edits."""
import pathlib,shutil,hashlib,json
r=pathlib.Path(__file__).resolve().parents[2]; t=r.parent/'site-tmp';base=t/'rooted-natural/src';out=t/'thermal-reservoir';e=r/'web/tests/continuation-review/thermal-reservoir';e.mkdir(exist_ok=True)
meta={}
for name in ['control','candidate']:
 o=out/name/'src';assert not o.exists();shutil.copytree(base,o)
 for p in o.rglob('*.zig'):
  s=p.read_text();s=s.replace(str(t/'rooted-natural'),str(out/name))
  if p.name=='main.zig':
   s=s.replace('arm-{}-30.json','arm-{}-60.json').replace('if(resumed)30 else 0','if(resumed)60 else 0').replace('if(tick+1==30 or tick+1==end)','if(tick+1==60 or tick+1==end)')
  p.write_text(s)
 p=o/'simulation/surface_physics.zig'
 if name=='candidate':
  s=p.read_text();assert s.count('return area*(0.1*5513*700+mixed_depth*1000*water_cp);')==1
  s=s.replace('return area*(0.1*5513*700+mixed_depth*1000*water_cp);','return area*(0.5*5513*700+mixed_depth*1000*water_cp);')
  p.write_text(s)
 meta[name]={str(p.relative_to(o)):hashlib.sha256(p.read_bytes()).hexdigest() for p in sorted(o.rglob('*.zig'))}
# Only changed physics is the constant above; host output paths differ intentionally.
diff=[]
for key in meta['control']:
 if meta['control'][key]!=meta['candidate'][key]:diff.append(key)
assert sorted(diff)==['main.zig','save_game.zig','simulation/surface_physics.zig'],diff
(e/'source-hashes.json').write_text(json.dumps(meta,indent=2)+'\n')
(e/'physics-delta.txt').write_text('Only runtime physics delta: originHeatCapacity ground active thickness0.1m ->0.5m. Same density5513kg/m3,cp700J/kg/K, water mixed layer cap50m, all fluxes/biology unchanged. main/save_game differences are isolated QA output prefixes only.\n')
