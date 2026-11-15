#!/usr/bin/env python3
"""Extend preserved natural patch-watch acceptance with actual ecology flux/state oracles."""
from pathlib import Path
import subprocess,sys
root=Path(__file__).resolve().parents[2];out=Path(sys.argv[1])
subprocess.run([sys.executable,str(root/'web/tests/egl-patch-watch-prepare.py'),str(out)],check=True)
p=out/'simulation/planet.zig';s=p.read_text()
s='pub var qa_fixed:f64=0;pub var qa_recycled:f64=0;\n'+s
needle='            if(observing)watch.recordFlux(i,flux.fixed,flux.recycled,flux.grazed);'
assert s.count(needle)==1
s=s.replace(needle,'            if(i==qa_watch_cell){qa_flux+=@as(f64,flux.grazed);qa_fixed+=@as(f64,flux.fixed);qa_recycled+=@as(f64,flux.recycled);}\n'+needle)
p.write_text(s)
p=out/'main.zig';s=p.read_text()
s=s.replace('pm.qa_watch_cell=cell;pm.qa_flux=0;','pm.qa_watch_cell=cell;pm.qa_flux=0;pm.qa_fixed=0;pm.qa_recycled=0;')
needle='std.debug.assert(watched.consumed==pm.qa_flux);'
assert s.count(needle)==1
s=s.replace(needle,needle+'''
          std.debug.assert(watched.fixed==pm.qa_fixed and watched.recycled==pm.qa_recycled);
          const end_pop=pw.Watch.population(state.planet.microbeCells[cell].cohorts).?;
          std.debug.assert(watched.end_biomass==end_pop.biomass and watched.end_colonies==end_pop.colonies);
          std.debug.print("ECOLOGY_PULSE fixed={d} recycled={d} biomass={d}->{d} colonies={d}->{d} exact_oracle=true final_scheduler_population=true\\n",.{watched.fixed,watched.recycled,watched.start_biomass,watched.end_biomass,watched.start_colonies,watched.end_colonies});
''')
needle='std.debug.assert(patchWatchStartForState(state,@intCast(cell))==1);\n          for(0..60)'
assert s.count(needle)==1
s=s.replace(needle,'''std.debug.assert(patchWatchStartForState(state,@intCast(cell))==1);
          const start_pop=pw.Watch.population(state.planet.microbeCells[cell].cohorts).?;
          std.debug.assert(pw.current.start_biomass==start_pop.biomass and pw.current.start_colonies==start_pop.colonies);
          for(0..60)''')
# Optional reuse of preserved actual 30-day save, rather than rerunning its history.
# The caller still starts real engine and normal nursery fixture before this hook.
needle='          var found=state.findRecordedFeeding(true);'
assert s.count(needle)==1
s=s.replace(needle,'''          if(std.process.getEnvVarOwned(allocator,"QA_PULSE_SAVE") catch null)|saved_path|{
            defer allocator.free(saved_path);
            const saved_bytes=try std.fs.cwd().readFileAlloc(a,saved_path,100*1024*1024);
            const saved_parsed=try std.json.parseFromSlice(saves.schema.Save,a,saved_bytes,.{.allocate=.alloc_always});
            try saves.apply(state,saved_parsed.value);state.paused=false;state.showEscapeMenu=false;
          }
'''+needle)
# Feeding-finder acceptance belongs to its own retained harness; avoid replaying its old numeric-ID assertion.
a=s.index('        {\n            const saves=@import("save_game.zig");var arena=')
b=s.index('        {\n          const saves=',a)
s=s[:a]+s[b:]
s=s.replace('for(0..@as(usize,if(fast)', 'for(0..@as(usize,if(std.posix.getenv("QA_PULSE_SAVE")!=null) 0 else if(fast)')
p.write_text(s)
