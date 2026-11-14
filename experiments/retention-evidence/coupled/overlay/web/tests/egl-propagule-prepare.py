#!/usr/bin/env python3
"""Production 15m basin, one explicit seed, normal Grow; no experimental flags."""
from pathlib import Path
import subprocess,sys,os
here=Path(__file__).resolve().parent
root=Path(os.environ.get('STELLA_SOURCE_ROOT',str(here.parents[1])))
out=Path(sys.argv[1])
subprocess.run([sys.executable,str(root/'web/tests/egl-starter-prepare.py'),str(out)],check=True)
p=out/'main.zig';s=p.read_text()
s=s.replace('state.timeScale=if(fast)86400 else 3600;', 'state.timeScale=if(fast)21600 else 3600;').replace('(std.fmt.parseInt(usize,d,10) catch 40)*60','(std.fmt.parseInt(usize,d,10) catch 40)*240').replace('if(i%60==59)','if(i%240==239)').replace('(i+1)/60','(i+1)/240')
needle='            var tick_timer=try std.time.Timer.start();'
s=s.replace(needle,'''            if(i%240==239){
                var occupied:usize=0;var bio:f64=0;for(state.planet.microbeCells)|cell|{const mass=@import("simulation/microbes.zig").biomass(cell);bio+=mass;if(mass>0)occupied+=1;}
                std.debug.print("PROPAGULE_DAY day={d} grow_seconds={d} occupied={d} biomass={d} attempts={d} arrivals={d} tracked_colony_losses={d} production_15m=true\\n",.{(i+1)/240,(i+1)/60,occupied,bio,state.planet.propaguleAttempts,state.planet.propaguleArrivals,state.planet.propaguleTrackedLosses});
            }
'''+needle)
s=s.replace(' try saves.apply(state,parsed.value);', ' state.planet.propaguleFeedback.next_serial=17;state.planet.propaguleAttempts=3;state.planet.propaguleArrivals=2;state.planet.propaguleTrackedLosses=1;\n try saves.apply(state,parsed.value);')
s=s.replace(' const restored=try std.json.stringifyAlloc', ''' std.debug.assert(state.planet.propaguleFeedback.next_serial==1);
 std.debug.assert(state.planet.propaguleAttempts==0 and state.planet.propaguleArrivals==0 and state.planet.propaguleTrackedLosses==0);
 std.debug.print("PROPAGULE_LOAD transient_observers_cleared=true save_schema_unchanged=true\\n",.{});
 const restored=try std.json.stringifyAlloc''')
assert 'PROPAGULE_DAY' in s and 'PROPAGULE_LOAD' in s
p.write_text(s)
