#!/usr/bin/env python3
"""One ABBA scheduler-only observer overhead sanity gate, no production edits."""
from pathlib import Path
import subprocess,sys,json,hashlib
r=Path(__file__).resolve().parents[2];o=Path(sys.argv[1]).resolve()
subprocess.run([sys.executable,str(r/'web/tests/egl-ecology-cue-prepare.py'),str(o)],check=True)
p=o/'simulation/planet.zig';s=p.read_text();old='physiology_deaths +|= WorldEcology.physiologyDeaths(before_cohorts,cell.cohorts);';assert old in s;s=s.replace(old,'if(WorldEcology.enabled) '+old);p.write_text(s)
p=o/'main.zig';s=p.read_text();a=s.index('          _=pm;_=pw;');b=s.index('\n        std.debug.print("ECOLOGY_CUE_COMPLETE',a)
s=s[:a]+r'''
          _=pm;_=pw;state.paused=true;state.showEscapeMenu=false;
          const E=@import("world_ecology.zig");
          const original=try std.json.stringifyAlloc(a,try saves.capture(a,state),.{});
          const initial=try std.json.parseFromSlice(saves.schema.Save,a,original,.{.allocate=.alloc_always});
          var reference:[]const u8="";
          for([_]bool{false,true,true,false},0..)|enabled,arm|{
            try saves.apply(state,initial.value);E.enabled=enabled;E.reset();
            for(0..12)|_|{state.planet.simulate(game.loop,.{.dt=1440,.timeScale=1,.solarConstant=state.solarConstant,.gameTime=state.gameTime,.planetRotationTime=state.planetRotationTime,.solarVector=state.simulationSolarVector()});state.gameTime+=1440;}
            var nanos:[60]u64=undefined;
            for(&nanos)|*elapsed|{var timer=try std.time.Timer.start();state.planet.simulate(game.loop,.{.dt=1440,.timeScale=1,.solarConstant=state.solarConstant,.gameTime=state.gameTime,.planetRotationTime=state.planetRotationTime,.solarVector=state.simulationSolarVector()});state.gameTime+=1440;elapsed.*=timer.read();}
            const endpoint=try std.json.stringifyAlloc(a,try saves.capture(a,state),.{});if(arm==0)reference=endpoint;std.debug.assert(std.mem.eql(u8,reference,endpoint));
            var total:u64=0;for(nanos)|n|total+=n;
            std.debug.print("OBSERVER_TIMING {s}\n",.{try std.json.stringifyAlloc(a,.{.arm=arm,.enabled=enabled,.ticks=60,.warmup=12,.total_ns=total,.tick_ns=nanos,.full_save_rng_exact=true},.{})});
          }
          E.enabled=true;try saves.apply(state,initial.value);std.debug.assert(std.mem.eql(u8,original,try std.json.stringifyAlloc(a,try saves.capture(a,state),.{})));
        }
'''+s[b:];p.write_text(s)
(o.parent/'overhead-provenance.json').write_text(json.dumps({'source_head':subprocess.check_output(['git','rev-parse','HEAD'],cwd=r).decode().strip(),'guard_note':'QA only guards physiologyDeaths when observer disabled; existing before_cohorts remains unchanged. No render/census/serialization inside timed loop.','hashes':{f:hashlib.sha256((o/f).read_bytes()).hexdigest() for f in ['main.zig','simulation/planet.zig','world_ecology.zig','recent_ecology.zig']}},indent=2)+'\n')
