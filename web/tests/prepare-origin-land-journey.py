#!/usr/bin/env python3
from pathlib import Path
import shutil,hashlib,json
r=Path(__file__).resolve().parents[2];base=r.parent/'site-tmp/origin-land-journey';o=base/'src';src=r.parent/'site-tmp/origin-land-gate/candidate/src'
assert not o.exists(),'do not replace running/frozen journey'
shutil.copytree(src,o)
(base/'input-source-hashes.json').write_text(json.dumps({str(p.relative_to(src)):hashlib.sha256(p.read_bytes()).hexdigest()for p in src.rglob('*.zig')},indent=2))
(o/'simulation/land_journey_audit.zig').write_text('''const std=@import("std");pub var tick:usize=0;pub var enabled:bool=false;
pub fn emit(comptime tag:[]const u8,value:anytype)void{if(!enabled)return;var buffer:[8192]u8=undefined;var stream=std.io.fixedBufferStream(&buffer);std.json.stringify(value,.{},stream.writer()) catch unreachable;std.debug.print("{s} {s}\\n",.{tag,stream.getWritten()});}
''')
p=o/'simulation/microbes.zig';s=p.read_text();s=s.replace('    var child=parent.*;','    const qa_parent=parent.*;const qa_rng=donor.rng;\n    var child=parent.*;',1);s=s.replace('    stats.next_lineage+=1;stats.births+=1;','''    stats.next_lineage+=1;stats.births+=1;
    @import("land_journey_audit.zig").emit("BIRTH",.{.tick=@import("land_journey_audit.zig").tick,.parent_before=qa_parent,.parent_after=parent.*,.child=child,.rng_before=qa_rng,.rng_after=donor.rng,.mutate=mutate,.config=config});''',1);p.write_text(s)
p=o/'simulation/shared_soil.zig';s=p.read_text();s=s.replace(' return out;',''' for(cell.cohorts,0..)|co,i|if(co.biomass>0 and co.root_fraction>0){@import("land_journey_audit.zig").emit("ROOT_WATER",.{.tick=@import("land_journey_audit.zig").tick,.lineage=co.lineage,.cohort=co,.soil_before=soil,.soil_after=out.soil,.vapor_before=vapor,.vapor_after=out.vapor,.area=area,.environment=env,.demand=out.demand[i],.credit=out.credits[i],.h=out.h[i],.shared_paid=out.paid,.bare_credit=out.bare_credit,.residual_density=out.vapor_rounding_density});};
 return out;''');p.write_text(s)
p=o/'main.zig';s=p.read_text().replace('if (!is_web or !web_initialized or !game.state_init)', 'if (!web_initialized or !game.state_init)');a=s.index('    const saves=@import("save_game.zig");const P=');b=s.index('\nconst expect =',a);s=s[:a]+(r/'web/tests/origin-land-journey-qa.txt').read_text().replace('OUTPUT',str(base))+s[b:];p.write_text(s)
(base/'source-hashes.json').write_text(json.dumps({str(p.relative_to(o)):hashlib.sha256(p.read_bytes()).hexdigest()for p in o.rglob('*.zig')},indent=2))
