#!/usr/bin/env python3
"""Actual current habitat view, input and target-water checks in isolated native copy."""
from pathlib import Path
import subprocess,sys
here=Path(__file__).resolve().parent;out=Path(sys.argv[1])
subprocess.run([sys.executable,str(here/'egl-life-visual-prepare.py'),str(out)],check=True)
p=out/'main.zig';s=p.read_text();needle='            if (frame == 25) { _ = state.testAction(3); }'
code='''            if(frame==25){
                const expected=state.selectedPoint;const sz=game.window.getFramebufferSize();
                state.mouseMoved(&game,@as(f32,@floatFromInt(sz.width))/2,@as(f32,@floatFromInt(sz.height))/2,0,0);
                std.debug.assert(state.selectedPoint==expected and state.pointerOnPlanet);
                const before=state.planet.waterMass[expected];
                std.debug.assert(std.math.isNan(state.setSelectedWaterTarget(@intCast(expected+1),3)) and state.planet.waterMass[expected]==before);
                std.debug.assert(std.math.isNan(state.setSelectedWaterTarget(@intCast(expected),6)) and state.planet.waterMass[expected]==before);
                const changed=state.setSelectedWaterTarget(@intCast(expected),3);std.debug.assert(std.math.isFinite(changed));
                std.debug.assert(@abs(state.planet.waterMass[expected]*state.planet.getKmPerWaterMass()*1000-3)<0.00001);
                const added=state.adjustSelectedWater(@intCast(expected),0.1);const removed=state.adjustSelectedWater(@intCast(expected),-0.1);
                std.debug.assert(@abs(added-0.1)<0.00001 and @abs(removed+0.1)<0.00001);
                const distance=state.targetCameraDistance;state.mouseScroll(&game,-2);std.debug.assert(state.targetCameraDistance>distance);
                state.mouseScroll(&game,2);std.debug.assert(@abs(state.targetCameraDistance-distance)<0.01);
                std.debug.print("HABITAT_INPUT selected={d} target3m=true stale_rejected=true invalid_rejected=true plus_minus01m=true zoom_inverse=true camera={d}\\n",.{expected,state.cameraDistance});
                _=state.testAction(3);
                if(std.posix.getenv("STELLA_QA_HEAT") != null)state.displayMode=.Temperature;
            }'''
assert needle in s;s=s.replace(needle,code);p.write_text(s)
