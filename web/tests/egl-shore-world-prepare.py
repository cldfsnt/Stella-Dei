#!/usr/bin/env python3
"""Coupled-world shore probe: explicit single shelf edit, no biology injection/refill."""
from pathlib import Path
import subprocess,sys
here=Path(__file__).resolve().parent;out=Path(sys.argv[1])
subprocess.run([sys.executable,str(here/'egl-forms-world-prepare.py'),str(out)],check=True)
p=out/'main.zig';s=p.read_text();needle='            var tick_timer=try std.time.Timer.start();'
insert='''            if(i==1200){
                const shore=state.planet.getNeighbours(idx)[0];
                const surface=state.planet.elevation[idx]+state.planet.waterMass[idx]*state.planet.getKmPerWaterMass();
                state.planet.elevation[shore]=surface-0.00015;
                state.selectedPoint=shore;
                std.debug.assert(std.math.isFinite(state.setSelectedWaterTarget(@intCast(shore),0.15)));
                state.selectedPoint=idx;
                std.debug.print("SHORE_ACTION day=20 cell={d} raised_shelf=true actual_water_target_m=0.15 biological_edits=false repeat=false\\n",.{shore});
            }
'''
assert needle in s;s=s.replace(needle,insert+needle,1)
needle='            if(i%60==59){\n              const Microbes='
insert='''            if(i>=1200 and i%60==59){
                const M=@import("simulation/microbes.zig");const shore=state.planet.getNeighbours(idx)[0];
                const cell=state.planet.microbeCells[shore];var capable:u32=0;var protection:f32=0;
                for(state.planet.microbeCells[idx].cohorts)|co|if(co.biomass>0){std.debug.print("SHORE_DONOR day={d} id={d} mass={d} credit={d} organization={d} support={d} structure={d} protection={d}\\n",.{(i+1)/60,co.lineage,co.biomass,co.reproduction_credit,co.organization,co.support_mass,co.structure,M.shoreProtection(co)});};
                for(cell.cohorts)|co|{if(co.biomass>0 and M.shoreCapable(co))capable+=1;protection=@max(protection,M.shoreProtection(co));}
                std.debug.print("SHORE_DAY day={d} depth_m={d} biomass={d} reserve={d} capable={d} max_protection={d}\\n",.{(i+1)/60,state.planet.waterMass[shore]*state.planet.getKmPerWaterMass()*1000,M.biomass(cell),M.storedWater(cell),capable,protection});
            }
'''
assert needle in s;s=s.replace(needle,insert+needle,1)
s=s.replace('        std.debug.print("TOTAL_WATER', '        var tissue_water:f64=0;for(state.planet.microbeCells)|cell|tissue_water+=@as(f64,@import("simulation/microbes.zig").storedWater(cell)+cell.surface_water_carry+cell.vapor_water_carry)*state.planet.getMeanPointArea()/1e9;\n        std.debug.print("TISSUE_WATER billion_kg={d}\\n",.{tissue_water});water_end+=tissue_water;\n        std.debug.print("TOTAL_WATER')
p.write_text(s)
