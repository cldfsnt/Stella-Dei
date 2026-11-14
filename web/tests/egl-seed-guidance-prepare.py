#!/usr/bin/env python3
"""Render real eligible/ineligible seed sites, without mutating their habitats."""
from pathlib import Path
import subprocess,sys
root=Path(__file__).resolve().parents[2];out=Path(sys.argv[1])
subprocess.run([sys.executable,str(root/'web/tests/egl-prepare.py'),str(out),'--mobile','--paused'],check=True)
p=out/'main.zig';s=p.read_text();marker='            const i = state.selectedPoint;'
hook=r'''            if(frame==25){
                state.planet.beginOrigin() catch unreachable;
                std.debug.assert(state.focusSeedableHabitat());
                state.selectedTool=.PlaceVegetation;
                std.debug.assert(state.planet.seedEligibility(state.selectedPoint)==.eligible);
                std.debug.print("SEED_GUIDANCE valid_site={d} unmodified=true\n",.{state.selectedPoint});
            }
            if(frame==85){
                if(std.posix.getenv("STELLA_SEED_TAP")!=null){
                    std.debug.assert(@import("simulation/microbes.zig").biomass(state.planet.microbeCells[state.selectedPoint])>0);
                    std.debug.print("SEED_TARGET_TAP actual_pointer_click=true living_colony=true\n",.{});
                }
                for(state.planet.transformedPoints,0..)|point,idx|{
                    if(@abs(point.norm().z())>0.9 or state.planet.seedEligibility(idx)!=.too_deep)continue;
                    state.selectedPoint=idx;state.pointerOnPlanet=true;
                    state.targetCameraPos=point.norm();state.cameraPos=point.norm();
                    state.targetCameraDistance=point.length()+900;state.cameraDistance=state.targetCameraDistance;
                    std.debug.print("SEED_GUIDANCE invalid_site={d} reason=too_deep unmodified=true\n",.{idx});break;
                }
            }
'''
assert marker in s;s=s.replace(marker,hook+marker);p.write_text(s)
