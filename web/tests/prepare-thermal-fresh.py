from pathlib import Path
import shutil,json,hashlib
r=Path(__file__).resolve().parents[2];t=r.parent/'site-tmp';e=r/'web/tests/continuation-review/thermal-fresh';e.mkdir(exist_ok=True);base=t/'root-wind-controls-native/src'
for kind in ['control','candidate']:
 b=t/'thermal-fresh'/kind;o=b/'src';assert not o.exists();shutil.copytree(base,o)
 p=o/'main.zig';s=p.read_text();start=s.index('    const saves=@import("save_game.zig");var arena=');end=s.index('\nconst expect =',start);s=s[:start]+(r/'web/tests/thermal-fresh-qa.txt').read_text().replace('OUTPUT',str(b))+s[end:];p.write_text(s)
 p=o/'save_game.zig';p.write_text(p.read_text().replace(str(t/'root-wind-controls-native'),str(b)))
 # Use unchanged observer-only lineage helper from frozen natural QA.
 old=t/'rooted-natural/src/simulation';shutil.copy2(old/'land_journey_audit.zig',o/'simulation/land_journey_audit.zig')
 p=o/'simulation/microbes.zig';s=p.read_text();s=s.replace('fundedHydration(c.*,env,elapsed,i,interval_demand[i])','qaFundedHydration(c.*,env,elapsed,i,interval_demand[i],"mortality")').replace('fundedHydration(c,env,elapsed,i,interval_demand[i])','qaFundedHydration(c,env,elapsed,i,interval_demand[i],"growth")');oldtext=(old/'microbes.zig').read_text();s+=oldtext[oldtext.index('\nfn qaFundedHydration'):];p.write_text(s)
 p=o/'simulation/shared_soil.zig';s=p.read_text();line=next(l for l in (old/'shared_soil.zig').read_text().splitlines()if '.emit("ROOT_WATER"'in l);s=s.replace(' return out;',line+'\n return out;',1);p.write_text(s)
 if kind=='candidate':
  p=o/'simulation/surface_physics.zig';s=p.read_text();assert s.count('return area*(0.1*5513*700+mixed_depth*1000*water_cp);')==1;p.write_text(s.replace('return area*(0.1*5513*700+mixed_depth*1000*water_cp);','return area*(0.5*5513*700+mixed_depth*1000*water_cp);'))
 (e/(kind+'-source-hashes.json')).write_text(json.dumps({str(p.relative_to(o)):hashlib.sha256(p.read_bytes()).hexdigest()for p in o.rglob('*.zig')},indent=2)+'\n')
