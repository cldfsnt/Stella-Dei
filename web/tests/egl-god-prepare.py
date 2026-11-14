#!/usr/bin/env python3
"""Actual generated-world god actions; no synthetic water or biology."""
from pathlib import Path
import subprocess,sys
here=Path(__file__).resolve().parent;out=Path(sys.argv[1])
subprocess.run([sys.executable,str(here/'egl-starter-prepare.py'),str(out)],check=True)
p=out/'main.zig';s=p.read_text();needle='    const paused=state.paused;const pace=state.timeScale;'
s=s.replace(needle,needle+'''
    var sum_before:f64=0;for(state.planet.waterMass)|v|{sum_before+=v;}
    const stale=state.applyGodAction(.wave,point+1);std.debug.assert(!stale.success());
    const w=state.applyGodAction(.wave,point);std.debug.assert(w.success());
    var sum_after:f64=0;for(state.planet.waterMass)|v|{sum_after+=v;}
    std.debug.assert(@abs(sum_before-sum_after)<=@max(1e-4,sum_before*1e-7));
    const temp_before=state.planet.temperature[point];
    const h=state.applyGodAction(.lightning,point);std.debug.assert(h.success());
    std.debug.assert(h.heat_joules>0 and state.planet.temperature[point]>temp_before);
    std.debug.assert(state.paused==paused and state.timeScale==pace);
    std.debug.print("GOD_REAL water_before={d} water_after={d} moved={d} cells={d} temp_before={d} temp_after={d} heat_joules={d} stale_rejected=true pace_pause_preserved=true\\\\n",.{sum_before,sum_after,w.moved_mass,w.count,temp_before,state.planet.temperature[point],h.heat_joules});
''');assert 'GOD_REAL' in s;p.write_text(s)
