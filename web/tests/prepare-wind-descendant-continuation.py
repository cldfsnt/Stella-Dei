from pathlib import Path
import shutil,json,hashlib
r=Path(__file__).resolve().parents[2];src=r.parent/'site-tmp/wind-bulk/src';live=r.parent/'site-tmp/wind-dispersal/src';o=r.parent/'site-tmp/wind-descendant-continuation';assert not(o/'src').exists();shutil.copytree(src,o/'src')
proof={}
for n in ['simulation/planet.zig','simulation/microbes.zig','simulation/life.zig','simulation/wind_packet.zig','simulation/wind_genetics.zig','simulation/wind_dispersal.zig','save_schema.zig']:
 a=(src/n).read_text();b=(live/n).read_text();original=a
 if n.endswith('planet.zig'):a='\n'.join(x for x in a.split('\n')if'const qa_source_before='not in x and '@import("wind_audit.zig").endpoints('not in x)
 assert a==b,n;proof[n]={'live_sha256':hashlib.sha256(b.encode()).hexdigest(),'adapter_sha256':hashlib.sha256(original.encode()).hexdigest(),'equal_except_two_observation_lines':True}
for arm in ['ordinary','pioneer']:shutil.copy2(src.parent/(arm+'-day7.json'),o/(arm+'-input.json'))
p=o/'src/main.zig';s=p.read_text();a=s.index('    const saves=@import("save_game.zig");const M=');b=s.index('\nconst expect =',a);s=s[:a]+(r/'web/tests/wind-descendant-continuation-qa.txt').read_text().replace('OUTPUT',str(o))+s[b:];p.write_text(s)
(o/'model-parity.json').write_text(json.dumps(proof,indent=2));(o/'source-hashes.json').write_text(json.dumps({str(p.relative_to(o/'src')):hashlib.sha256(p.read_bytes()).hexdigest()for p in(o/'src').rglob('*.zig')},indent=2))
