from pathlib import Path
import json,hashlib
r=Path(__file__).resolve().parents[2]
for beta,name in [(True,'growth-form-native'),(False,'growth-form-main-native')]:
 script=(r/'web/tests/prepare-wetlands-native.py').read_text().replace("'site-tmp/wetlands-native'",f"'site-tmp/{name}'")
 if not beta:script=script.replace("src=r.parent/'site-tmp/wetlands-preview/src'","src=r/'src'").replace("assert '\"/wetlands-saves/world.json\"' in original;", "assert '\"/saves/world.json\"' in original;").replace("original.replace('/wetlands-saves'","original.replace('/saves'")
 exec(compile(script,str(r/'web/tests/prepare-wetlands-native.py'),'exec'),{'__file__':str(r/'web/tests/prepare-wetlands-native.py')})
 b=r.parent/f'site-tmp/{name}';p=b/'src/main.zig';s=p.read_text();a=s.index('    const saves=@import("save_game.zig");const M=');e=s.index('\nconst expect =',a);inp=r.parent/('site-tmp/wetlands-journey/day-7.json' if beta else 'site-tmp/root-only-baseline-coordinator/day60/arm-0.json');s=s[:a]+(r/'web/tests/growth-form-native-qa.txt').read_text().replace('OUTPUT',str(b)).replace('INPUT',str(inp)).replace('BETA','true' if beta else 'false')+s[e:];p.write_text(s)
 (b/'source-hashes.json').write_text(json.dumps({str(p.relative_to(b/'src')):hashlib.sha256(p.read_bytes()).hexdigest()for p in (b/'src').rglob('*.zig')},indent=2))
