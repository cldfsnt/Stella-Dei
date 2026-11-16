from pathlib import Path
import shutil,json,hashlib
r=Path(__file__).resolve().parents[2];t=r.parent/'site-tmp';b=t/'unified-land-starter'
s=(r/'web/tests/prepare-calm-release-native.py').read_text().replace("b=t/'calm-release-native'","b=t/'unified-land-starter'").replace("src=t/'root-calm/src'","src=t/'unified-game/src'").replace('root-calm-engine/source-hashes.json','unified-native/source-hashes.json').replace('calm-release-qa.txt','unified-land-starter-qa.txt').replace("t/'wetlands-day21/day-21.json'","t/'protective-journey/fresh.json'")
exec(compile(s,str(r/'web/tests/prepare-calm-release-native.py'),'exec'),{'__file__':str(r/'web/tests/prepare-calm-release-native.py')})
o=b/'src';shutil.copy2(t/'protective-journey/src/simulation/shore_audit.zig',o/'simulation/shore_audit.zig')
p=o/'simulation/planet.zig';s=p.read_text();needle='self.waterMass[i]=column.state.liquid;';assert s.count(needle)==1;s=s.replace(needle,'for(0..4)|slot|{@import("shore_audit.zig").credit(self.microbeCells[i].cohorts[slot].lineage,column.root_credits[slot]);}\n            '+needle);p.write_text(s)
p=o/'simulation/microbes.zig';s=p.read_text();needle='         const wet_mortality=0.04+';assert s.count(needle)==1;s=s.replace(needle,'        @import("shore_audit.zig").hydration(c.lineage,hydrated);\n'+needle);p.write_text(s)
(b/'source-hashes.json').write_text(json.dumps({str(p.relative_to(o)):hashlib.sha256(p.read_bytes()).hexdigest()for p in o.rglob('*.zig')},indent=2))
