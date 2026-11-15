#!/usr/bin/env python3
"""Extend copied replay with explicit dt, rotation-rate and wind perturbations."""
from pathlib import Path
import subprocess,sys
root=Path(__file__).resolve().parents[2];source=Path(sys.argv[1]);out=Path(sys.argv[2])
subprocess.run([sys.executable,str(root/'web/tests/egl-cpu-replay-prepare.py'),str(source),str(out)],check=True)
p=out/'main.zig';s=p.read_text().replace('for(0..4)|stage|','for(0..8)|stage|')
old='        render(window);gl.finish();window.swapBuffers();\n        for(0..3)|_|{state.planet.simulate(game.loop,.{.dt=1440'
new='        if(stage==5)state.planetRotationTime*=0.7;\n        if(stage==6)state.planet.airVelocity[0].data[0]+=0.01;\n        if(stage==7)try saves.apply(state,frozen.value);\n        const step:f32=if(stage==4)720 else 1440;\n        render(window);gl.finish();window.swapBuffers();\n        for(0..3)|_|{state.planet.simulate(game.loop,.{.dt=step'
assert old in s;s=s.replace(old,new,1)
s=s.replace('.solarVector=state.simulationSolarVector()});state.gameTime+=1440;}\n        if(std.posix.getenv("STELLA_CPU_RESULT_PREFIX"))','.solarVector=state.simulationSolarVector()});state.gameTime+=step;}\n        if(std.posix.getenv("STELLA_CPU_RESULT_PREFIX"))',1);p.write_text(s)
# Optional first-frame sampling includes cache allocation / cold misses.
p=out/'main.zig';s=p.read_text();needle='  for(0..12)|_|{state.update(&game,1.0/60.0);';assert needle in s
s=s.replace(needle,'  const warmup:usize=if(std.posix.getenv("STELLA_CPU_COLD")!=null)0 else 12;\n  for(0..warmup)|_|{state.update(&game,1.0/60.0);',1);p.write_text(s)
