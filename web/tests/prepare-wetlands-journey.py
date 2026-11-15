from pathlib import Path
import shutil,json,hashlib
r=Path(__file__).resolve().parents[2];b=r.parent/'site-tmp/wetlands-journey';o=b/'src';src=r.parent/'site-tmp/wetlands-native/src';assert not o.exists();shutil.copytree(src,o)
p=o/'main.zig';s=p.read_text();a=s.index('    const saves=@import("save_game.zig");const M=');e=s.index('\nconst expect =',a);s=s[:a]+(r/'web/tests/wetlands-journey-qa.txt').read_text().replace('OUTPUT',str(b))+s[e:];p.write_text(s)
p=o/'save_game.zig';p.write_text(p.read_text().replace('/wetlands-native/disk/','/wetlands-journey/disk/'))
(o/'simulation/wetlands_audit.zig').write_text('''const std=@import("std");pub var enabled=false;pub var tick:usize=0;pub var credits:f64=0;pub var signals:usize=0;pub var max_h:f32=0;
pub fn emit(comptime tag:[]const u8,v:anytype)void{if(!enabled)return;var b:[8192]u8=undefined;var s=std.io.fixedBufferStream(&b);std.json.stringify(v,.{},s.writer()) catch unreachable;std.debug.print("{s} {s}\\n",.{tag,s.getWritten()});}
''')
p=o/'simulation/planet.zig';s=p.read_text();needle='            const flux = Microbes.step(cell, env, dt);';assert s.count(needle)==1;s=s.replace(needle,'''            const qa=@import("wetlands_audit.zig");if(qa.enabled)for(env.root_credit)|credit|{qa.credits+=credit;};
'''+needle);p.write_text(s)
p=o/'simulation/microbes.zig';s=p.read_text();needle='    return @import("final_demand.zig").signal(env.root_credit[slot],env.root_owner[slot],c.lineage,@max(entry_demand,current));';assert s.count(needle)==1;s=s.replace(needle,'''    const h=@import("final_demand.zig").signal(env.root_credit[slot],env.root_owner[slot],c.lineage,@max(entry_demand,current));
    const qa=@import("wetlands_audit.zig");if(qa.enabled){if(h>0)qa.signals+=1;qa.max_h=@max(qa.max_h,h);qa.emit("HYDRATION",.{.tick=qa.tick,.id=c.lineage,.owner=env.root_owner[slot],.credit=env.root_credit[slot],.current_demand=current,.entry_demand=entry_demand,.h=h});}return h;''');p.write_text(s)
(b/'source-hashes.json').write_text(json.dumps({str(p.relative_to(o)):hashlib.sha256(p.read_bytes()).hexdigest()for p in o.rglob('*.zig')},indent=2))
