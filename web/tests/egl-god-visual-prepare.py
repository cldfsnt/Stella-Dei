#!/usr/bin/env python3
"""Actual one-shot interventions, separated for visual capture; no fake deltas."""
from pathlib import Path
import subprocess,sys
root=Path(__file__).resolve().parents[2];out=Path(sys.argv[1])
subprocess.run([sys.executable,str(root/'web/tests/egl-prepare.py'),str(out),'--mobile','--paused'],check=True)
p=out/'main.zig';s=p.read_text();marker='            const i = state.selectedPoint;'
hook=r'''            if(frame==25){
                state.planet.beginOrigin() catch unreachable;
                std.debug.assert(state.focusSeedableHabitat());
                std.debug.assert(state.makeSelectedPond(@intCast(state.selectedPoint))>0);
                state.selectedTool=.None;
                state.showPointDetails=false;state.pointerOnPlanet=false;
            }
            if(frame==45 or frame==85){
                const kind: @import("god_actions.zig").Kind=if(frame==45) .wave else .lightning;
                const receipt=state.applyGodAction(kind,@intCast(state.selectedPoint));
                std.debug.assert(receipt.success());
                std.debug.print("GOD_VISUAL actual_action={s} cells={d} moved_mass={d} heat_joules={d}\n",.{@tagName(kind),receipt.count,receipt.moved_mass,receipt.heat_joules});
            }
'''
assert marker in s;s=s.replace(marker,hook+marker);p.write_text(s)
