#!/usr/bin/env python3
"""Actual-engine direct starter callbacks; never assigns biology or auto-care."""
from pathlib import Path
import subprocess,sys
here=Path(__file__).resolve().parent;out=Path(sys.argv[1])
subprocess.run([sys.executable,str(here/'egl-forms-world-prepare.py'),str(out)],check=True)
p=out/'main.zig';s=p.read_text()
s=s.replace('    const size=window.getFramebufferSize();\n    qa_click(@as(f64,@floatFromInt(size.width))/2,350);', '''    { const point: u32=@intCast(state.selectedPoint);
    const paused=state.paused;const pace=state.timeScale;
    const starter_biomass_before=@import("simulation/microbes.zig").biomass(state.planet.microbeCells[point]);
    std.debug.assert(state.seedSelectedColony(point+1)==-1);
    std.debug.assert(@import("simulation/microbes.zig").biomass(state.planet.microbeCells[point])==starter_biomass_before);
    std.debug.assert(state.makeSelectedPond(point)>0);
    state.pointerOnPlanet=false; // HTML controls are outside the 3D canvas.
    std.debug.assert(state.seedSelectedColony(point)==1);
    std.debug.assert(state.paused==paused and state.timeScale==pace);
    std.debug.assert(@import("simulation/microbes.zig").biomass(state.planet.microbeCells[point])>starter_biomass_before);
    std.debug.print("STARTER_REAL stale_rejected=true off_canvas_seed=true pace_pause_preserved=true no_auto_care=true\\n",.{}); }''')
assert 'STARTER_REAL' in s;p.write_text(s)
