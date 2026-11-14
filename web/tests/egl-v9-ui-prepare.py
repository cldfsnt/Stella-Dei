#!/usr/bin/env python3
"""Isolated actual-engine mobile guidance test fixture. No production state edits."""
from pathlib import Path
import subprocess,sys
out=Path(sys.argv[1] if len(sys.argv)>1 else '/tmp/stella-v9-ui-src')
subprocess.run([sys.executable,str(Path(__file__).with_name('egl-prepare.py')),str(out),'--mobile','--paused'],check=True)
p=out/'main.zig';s=p.read_text();s=s.replace('            const i = state.selectedPoint;',r'''            const i = state.selectedPoint;
            if (frame == 15) std.debug.assert(state.timeScale == 21600);
            if (frame == 25) std.debug.assert(state.timeScale == 86400);
            if (frame == 35) std.debug.assert(state.timeScale == 3600);
            if (frame == 55) std.debug.assert(state.planet.lifeforms.items.len == 0);
            if (frame == 70) std.debug.assert(state.planet.lifeforms.items.len == 2);
            std.debug.print("V9_UI frame={d} speed={d} rabbits={d} notice={s}\n", .{frame,state.timeScale,state.planet.lifeforms.items.len,state.mobileFeedback});''')
s+='''
pub export fn egl_habitat(wet: c_int) void {
    switch (game.state) {
        .Playing => |*state| {
            std.debug.assert(state.pointerOnPlanet);
            std.debug.assert(state.selectedTool == .PlaceLife);
            state.planet.waterMass[state.selectedPoint] = (if (wet == 1) @as(f32,0.0021) else 0) / state.planet.getKmPerWaterMass();
            state.planet.vegetation[state.selectedPoint] = 0.5;
        },
        else => unreachable,
    }
}
''';p.write_text(s)
