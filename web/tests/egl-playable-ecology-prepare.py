#!/usr/bin/env python3
"""Fixed seven-day current player loop observation; no model edits."""
from pathlib import Path
import subprocess,sys,json,hashlib
r=Path(__file__).resolve().parents[2];o=Path(sys.argv[1]).resolve();subprocess.run([sys.executable,str(r/'web/tests/egl-early-flow-prepare.py'),str(o)],check=True)
p=o/'main.zig';s=p.read_text().replace('state.gameTime-start<3*86400','state.gameTime-start<7*86400').replace('day==3','day==7')
needle='        render(window);gl.finish();window.swapBuffers();\n        std.debug.print("EARLY_VISIBILITY'
assert needle in s
block=r'''
        for(state.planet.microbeCells,0..)|patch,pi|if(M.biomass(patch)>0){
          std.debug.print("PLAYABLE_PATCH {s}\n",.{try std.json.stringifyAlloc(allocator,.{.day=day,.cell=pi,.depth=state.planet.waterMass[pi]*state.planet.getKmPerWaterMass()*1000,.temperature=state.planet.temperature[pi],.patch=patch},.{})});
        };
        std.debug.print("PLAYABLE_STATS day={} attempts={} arrivals={} losses={} grazed={d} births={}\n",.{day,state.planet.propaguleAttempts,state.planet.propaguleArrivals,state.planet.propaguleTrackedLosses,state.planet.microbeStats.grazed_carbon,state.planet.microbeStats.births});
        if(day==3 or day==7){const save=@import("save_game.zig");const frozen=try std.json.stringifyAlloc(allocator,try save.capture(allocator,state),.{});try std.fs.cwd().writeFile(.{.sub_path=try std.fmt.allocPrint(allocator,"OUTPUT/day-{d}.json",.{day}),.data=frozen});}
'''.replace('OUTPUT',str(o.parent))
s=s.replace(needle,block+needle)
# Preserve exact requested public exports if an older ancestor changed Pond to Nursery.
prod=(r/'src/main.zig').read_text()
import re
pat=r'export fn stella_make_pond\(expected_point:u32\) i32 \{.*?\n\}'
old=re.search(pat,s,re.S);new=re.search(pat,prod,re.S);assert old and new;s=s[:old.start()]+new.group()+s[old.end():]
p.write_text(s)
subprocess.run([sys.executable,str(r/'web/tests/audit-zig-exports.py'),str(r/'src/main.zig'),str(p)],check=True,stdout=(o.parent/'export-audit.json').open('w'))
(o.parent/'provenance.json').write_text(json.dumps({'head':subprocess.check_output(['git','rev-parse','HEAD'],cwd=r,text=True).strip(),'seed':42,'days':7,'source':{f:{'production':hashlib.sha256((r/'src'/f).read_bytes()).hexdigest(),'copy':hashlib.sha256((o/f).read_bytes()).hexdigest()}for f in ['simulation/microbes.zig','simulation/planet.zig','states/play.zig','main.zig']}},indent=2)+'\n')
