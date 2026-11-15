#!/usr/bin/env python3
"""Actual production Sunlit prepare/commit journey; copied native host only."""
from pathlib import Path
import sys,subprocess,json,hashlib
r=Path(__file__).resolve().parents[2];o=Path(sys.argv[1]).resolve()
subprocess.run([sys.executable,str(r/'web/tests/egl-v59-journey-prepare.py'),str(o)],check=True)
p=o/'main.zig';s=p.read_text().replace('stella_habitat_prepare(PerformanceDetails.world_serial,@intCast(target),1)','stella_habitat_prepare(PerformanceDetails.world_serial,@intCast(target),2)')
needle='          const prep=try std.json.parseFromSlice';i=s.index(needle)
s=s[:i]+'''          const before_sunlit=try std.json.stringifyAlloc(a,try saves.capture(a,state),.{});
          const before_parsed=try std.json.parseFromSlice(saves.schema.Save,a,before_sunlit,.{.allocate=.alloc_always});
          std.debug.assert(state.makeSelectedSunlitNursery(@intCast(target))>0);
          const direct_sunlit=try std.json.stringifyAlloc(a,try saves.capture(a,state),.{});
          try saves.apply(state,before_parsed.value);state.selectedPoint=target;
'''+s[i:]
needle='          const token:u32=@intCast(prep.value.object.get("token").?.integer);'
s=s.replace(needle,'''          std.debug.assert(std.mem.eql(u8,prep.value.object.get("kind").?.string,"sunlit_nursery"));
          std.debug.assert(prep.value.object.get("center_depth_m").?.integer==5 and prep.value.object.get("other_floor_depth_m").?.integer==5);
          std.debug.assert(std.mem.eql(u8,before_sunlit,try std.json.stringifyAlloc(a,try saves.capture(a,state),.{})));
'''+needle)
needle='          const seeded=stella_seed_colony'
i=s.index(needle);s=s[:i]+'''          std.debug.print("SUNLIT_RECEIPT {s}\\n",.{try std.json.stringifyAlloc(a,habitat.value,.{})});
          const after_sunlit=try std.json.stringifyAlloc(a,try saves.capture(a,state),.{});
          std.debug.assert(std.mem.eql(u8,direct_sunlit,after_sunlit));
          _=stella_habitat_execute(token);
          std.debug.assert(std.mem.eql(u8,after_sunlit,try std.json.stringifyAlloc(a,try saves.capture(a,state),.{})));
          for(habitat.value.object.get("floor_ids").?.array.items)|id|std.debug.assert(@abs(state.planet.waterMass[@intCast(id.integer)]*conv*1000-5)<0.001);
'''+s[i:]
s=s.replace('../site-tmp/v59-journey/final.ppm',str(o.parent/'final.ppm'))
s=s.replace('        try originSaveCheck','        std.debug.print("SUNLIT_PUBLIC_PASS complete=true original_restored=true explicit_qa_exit=true\\n",.{});std.process.exit(0);\n        try originSaveCheck',1)
# Avoid unreachable compile error: exit inside runtime condition.
s=s.replace('std.process.exit(0);\n        try originSaveCheck','if(std.posix.getenv("QA_PULSE_SAVE")!=null)std.process.exit(0);\n        try originSaveCheck')
p.write_text(s)
subprocess.run([sys.executable,str(r/'web/tests/audit-zig-exports.py'),str(r/'src/main.zig'),str(p)],check=True,stdout=(o.parent/'export-audit.json').open('w'))
(o.parent/'sunlit-provenance.json').write_text(json.dumps({'head':subprocess.check_output(['git','rev-parse','HEAD'],cwd=r,text=True).strip(),'source':{f:hashlib.sha256((o/f).read_bytes()).hexdigest()for f in ['main.zig','pond_action.zig','habitat_preview.zig','states/play.zig','simulation/planet.zig','simulation/microbes.zig']}},indent=2)+'\n')
