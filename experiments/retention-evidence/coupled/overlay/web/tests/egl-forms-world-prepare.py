#!/usr/bin/env python3
"""Full coupled world: production contained-basin + Seed actions, no assigned traits."""
from pathlib import Path
import subprocess,sys
here=Path(__file__).resolve().parent;out=Path(sys.argv[1])
subprocess.run([sys.executable,str(here/'egl-producer-diagnostic-prepare.py'),str(out)],check=True)
p=out/'main.zig';s=p.read_text()
a=s.index('    if(std.posix.getenv("STELLA_PRODUCER_EXPAND")');b=s.index('    {const point=state.selectedPoint;',a)
s=s[:a]+'''    {
      const center=state.selectedPoint;var patches:[7]usize=undefined;patches[0]=center;
      for(state.planet.getNeighbours(center),0..)|n,k|patches[k+1]=n;
      const depth: f32=15;
      std.debug.assert(state.makeSelectedPond(@intCast(center))>0);
      for(patches)|patch|{
        state.selectedPoint=patch;state.pointerOnPlanet=true;
        // Water was set by the same production Make Pond callback as the UI.
        std.debug.assert(@abs(state.planet.waterMass[patch]*state.planet.getKmPerWaterMass()*1000-depth)<0.001);
        const seeded=if(std.posix.getenv("STELLA_FORMS_SINGLE")!=null) false else state.testAction(3);
        std.debug.print("FORMS_PLAYER_INITIAL patch={d} water_target={d} seeded={} biology_assigned=false\\n",.{patch,depth,seeded});
      }
      state.selectedPoint=center;
    }
'''+s[b:]
marker='            if(i%60==59){\n                const center=state.selectedPoint;'
report='''            if(i%300==299 and std.posix.getenv("STELLA_FORMS_CARE")!=null){
              state.selectedPoint=idx;state.pointerOnPlanet=true;const watered=state.makeSelectedPond(@intCast(idx));
              std.debug.assert(watered>0);std.debug.print("FORMS_PLAYER_REFILL day={d} patches={d} automatic_game_policy=false\\n",.{(i+1)/60,watered});
            }
            if(i%60==59){
              const Microbes=@import("simulation/microbes.zig");var counts=[_]usize{0} ** 6;var living:usize=0;
              for(state.planet.microbeCells)|cell|for(cell.cohorts)|co|{if(co.biomass>0){counts[@intFromEnum(Microbes.producerForm(co))]+=1;living+=1;}};
              std.debug.print("FORMS_DAY day={d} living={d} counts={any}\\n",.{(i+1)/60,living,counts});
            }
'''
assert marker in s;s=s.replace(marker,report+marker,1);p.write_text(s)
