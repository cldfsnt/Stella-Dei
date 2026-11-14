#!/usr/bin/env python3
"""Static four-site visual fixture, not lifecycle evidence. Production is untouched."""
from pathlib import Path
import subprocess, sys
root=Path(__file__).resolve().parents[2]
out=Path(sys.argv[1] if len(sys.argv)>1 else '/tmp/stella-bio-visual-src')
subprocess.run([sys.executable,str(root/'web/tests/egl-prepare.py'),str(out),'--mobile','--paused'],check=True)
HOOK='            if (frame == 1 or frame == 26 or frame == 51 or frame == 76) {\n                const direction = if (frame==1) za.Vec3.new(1,0,0) else if(frame==26) za.Vec3.new(0,1,0) else if(frame==51) za.Vec3.new(0.3,0,0.95) else za.Vec3.new(-0.6,-0.7,-0.3);\n                const index = state.planet.getNearestPointTo(direction.norm().scale(state.planet.radius));\n                const point = state.planet.transformedPoints[index];\n                state.cameraPos = point.norm().scale(point.length()+100);\n                state.targetCameraPos = state.cameraPos;\n                state.cameraDistance = state.cameraPos.length(); state.targetCameraDistance = state.cameraDistance;\n                state.cameraGroundPoint = index;\n                @memset(state.planet.vegetation,0);\n                state.planet.vegetation[index]=0.7;\n                state.planet.waterMass[index]=0;\n                for(state.planet.getNeighbours(index))|n| { state.planet.vegetation[n]=0.7;state.planet.waterMass[n]=0; }\n                state.planet.lifeforms.clearRetainingCapacity();\n                const Rabbit=@import("simulation/life.zig").Lifeform;\n                state.planet.addLifeform(Rabbit.init(point,.Rabbit,0)) catch unreachable;\n                state.paused=true;\n            }\n'
p=out/'main.zig'
s=p.read_text().replace('            const i = state.selectedPoint;',HOOK+'            const i = state.selectedPoint;')
p.write_text(s)
p=out/'states/play.zig'
s=p.read_text().replace('var randomPrng = std.rand.DefaultPrng.init(@as(u64, @bitCast(std.time.milliTimestamp())));','var randomPrng = std.rand.DefaultPrng.init(20261113);')
s=s.replace('if (true) .{ .data = biology_visuals.groundedRabbit','if (std.posix.getenv("STELLA_VISUAL_BASELINE") == null) .{ .data = biology_visuals.groundedRabbit')
s=s.replace('        if (!biology_visuals.showSprouts', '        if (std.posix.getenv("STELLA_VISUAL_BASELINE") != null) return;\n        if (!biology_visuals.showSprouts')
p.write_text(s)
