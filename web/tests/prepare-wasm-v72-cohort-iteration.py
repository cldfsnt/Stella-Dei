from pathlib import Path
import shutil,json,hashlib
r=Path(__file__).resolve().parents[2];o=r.parent/'site-tmp/wasm-v72-cohort-iteration';o.mkdir(exist_ok=True);src=r.parent/'site-tmp/wasm-land-screen/baseline/src'
for arm in ['baseline','candidate']:
 d=o/arm/'src';shutil.copytree(src,d,dirs_exist_ok=True)
 if arm=='candidate':
  p=d/'simulation/microbes.zig';s=p.read_text();a=s.index('pub fn step(');b=s.index('\npub fn ',a+1);part=s[a:b];needle='    for(cell.cohorts,0..) |c,i| {';assert part.count(needle)==1;part=part.replace(needle,'    for(&cell.cohorts,0..) |c,i| {');s=s[:a]+part+s[b:];p.write_text(s)
 (o/arm/'source-hashes.json').write_text(json.dumps({str(p.relative_to(d)):hashlib.sha256(p.read_bytes()).hexdigest()for p in d.rglob('*.zig')},indent=2))
shutil.copyfile(r.parent/'site-tmp/wasm-land-screen/graph.json',o/'graph.json')
