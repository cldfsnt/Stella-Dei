from pathlib import Path
import json,hashlib
r=Path(__file__).resolve().parents[2];t=r.parent/'site-tmp';b=t/'natural-shoreline';b.mkdir(exist_ok=True)
s=(r/'web/tests/prepare-calm-release-native.py').read_text().replace("b=t/'calm-release-native'","b=t/'natural-shoreline'").replace("web/tests/calm-release-qa.txt","web/tests/natural-shoreline-qa.txt")
exec(compile(s,str(r/'web/tests/prepare-calm-release-native.py'),'exec'),{'__file__':str(r/'web/tests/prepare-calm-release-native.py')})
o=b/'src';p=o/'simulation/shore_audit.zig';p.write_text('''const std=@import("std");pub var enabled=true;pub var tick:usize=0;pub var credits:f64=0;pub var used:usize=0;pub fn credit(id:u64,v:f64)void{if(!enabled or v<=0)return;credits+=v;std.debug.print("ROOT_CREDIT tick={} id={} kg_m2={e}\\n",.{tick,id,v});}pub fn hydration(id:u64,h:f32)void{if(!enabled or h<=0)return;used+=1;std.debug.print("ROOT_USED tick={} id={} h={e}\\n",.{tick,id,h});}\n''')
p=o/'simulation/planet.zig';s=p.read_text();needle='self.waterMass[i]=column.state.liquid;';assert s.count(needle)==1;s=s.replace(needle,'for(0..4)|slot|{@import("shore_audit.zig").credit(self.microbeCells[i].cohorts[slot].lineage,column.root_credits[slot]);}\n            '+needle);p.write_text(s)
p=o/'simulation/microbes.zig';s=p.read_text();needle='         const wet_mortality=0.04+';assert s.count(needle)==1;s=s.replace(needle,'        @import("shore_audit.zig").hydration(c.lineage,hydrated);\n'+needle);p.write_text(s)
(b/'source-hashes.json').write_text(json.dumps({str(p.relative_to(o)):hashlib.sha256(p.read_bytes()).hexdigest()for p in o.rglob('*.zig')},indent=2))
