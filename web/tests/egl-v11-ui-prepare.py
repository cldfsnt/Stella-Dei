#!/usr/bin/env python3
"""Isolated UI fixture: inserts one real rabbit only to test status presentation.
Does not demonstrate breeding, evolution or population survival.
"""
from pathlib import Path
import subprocess,sys
root=Path(__file__).resolve().parents[2]
out=Path(sys.argv[1] if len(sys.argv)>1 else '/tmp/stella-v11-ui-src')
subprocess.run([sys.executable,str(root/'web/tests/egl-prepare.py'),str(out),'--mobile','--paused'],check=True)
HOOK='            if (frame == 45) {\n                const point = state.clickedPoint;\n                state.planet.lifeforms.clearRetainingCapacity();\n                state.planet.addLifeform(@import("simulation/life.zig").Lifeform.init(state.planet.transformedPoints[point], .Rabbit, state.gameTime)) catch unreachable;\n            }\n            std.debug.print("UI frame={d} inspect={} animal={} menu={} armed={}\\n",.{frame,state.showPointDetails,state.inspectAnimal,state.showEscapeMenu,state.leavePlanetArmed});\n'
p=out/'main.zig'
p.write_text(p.read_text().replace('            const i = state.selectedPoint;',HOOK+'            const i = state.selectedPoint;'))
