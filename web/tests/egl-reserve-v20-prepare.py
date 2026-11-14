#!/usr/bin/env python3
"""Exact v20 nursery/Grow, optional explicit one-time shelf, no biology assignment."""
from pathlib import Path
import subprocess,sys
here=Path(__file__).resolve().parent;out=Path(sys.argv[1])
subprocess.run([sys.executable,str(here/'egl-nursery-prepare.py'),str(out)],check=True)
p=out/'simulation/planet.zig';s=p.read_text().replace('            .liquid_available =','            .reserve_enabled=std.posix.getenv("STELLA_DISABLE_RESERVE")==null,\n            .liquid_available =');s=s.replace('            self.applyMicrobeWater(i,flux);', '            if(i==3421 and self.waterMass[i]==0 and flux.fixed>0)std.debug.print("SHORE_DRY_FIXATION day={d} fixed={d} reserve_after={d} carry_before={d} temperature={d}\\n",.{options.gameTime/86400,flux.fixed,Microbes.storedWater(cell.*),cell.surface_water_carry,self.temperature[i]});\n            self.applyMicrobeWater(i,flux);')
s=s.replace('self.propaguleArrivals+|=1;self.propaguleFeedback.arrived(i,n,lineage,options.gameTime);','self.propaguleArrivals+|=1;self.propaguleFeedback.arrived(i,n,lineage,options.gameTime);if(n==3421)std.debug.print("SHORE_REAL_ARRIVAL day={d} from={d} id={d} parent={d} depth_m={d}\\n",.{options.gameTime/86400,i,lineage,cell.cohorts[cohort].lineage,self.waterMass[n]*self.getKmPerWaterMass()*1000});')
s='pub var qa_stress_active:bool=false;pub var qa_tick:u64=0;pub var qa_before_flow:f32=0;pub var qa_after_flow:f32=0;pub var qa_stress_cell:usize=std.math.maxInt(usize);pub var qa_taken_total:f64=0;pub var qa_returned_total:f64=0;pub var qa_evaporated_total:f64=0;pub var qa_dry_ticks:u64=0;pub var qa_dry_fixed:f64=0;\n'+s
s=s.replace('        const cell=&self.microbeCells[index];\n        const accepted=', '        qa_taken_total+=flux.water_taken;qa_returned_total+=flux.water_returned;qa_evaporated_total+=flux.water_evaporated;\n        const cell=&self.microbeCells[index];\n        const accepted=')
s=s.replace('            self.applyMicrobeWater(i,flux);','            if(i==qa_stress_cell and self.waterMass[i]==0){qa_dry_ticks+=1;qa_dry_fixed+=flux.fixed;}\n            self.applyMicrobeWater(i,flux);')
s=s.replace('                @memcpy(self.newWaterMass, self.waterMass);','                if(qa_stress_active){qa_tick+=1;qa_before_flow=self.waterMass[qa_stress_cell];}\n                @memcpy(self.newWaterMass, self.waterMass);')
s=s.replace('                self.simulateAtmosphereWater(dt);','                if(qa_stress_active)qa_after_flow=self.waterMass[qa_stress_cell];\n                self.simulateAtmosphereWater(dt);\n                if(qa_stress_active)std.debug.print("STRESS_HYDRO tick={d} before={d} after_flow={d} after_phase={d}\\n",.{qa_tick,qa_before_flow,qa_after_flow,self.waterMass[qa_stress_cell]});')
s=s.replace('            self.waterMass[i]=@floatCast(result.liquid);','            if(qa_stress_active and i==qa_stress_cell)std.debug.print("STRESS_PHASE tick={d} evaporated={d} condensed={d}\\n",.{qa_tick,result.evaporated,result.condensed});\n            self.waterMass[i]=@floatCast(result.liquid);')
s=s.replace('                self.newWaterMass[target[i]] += transmitted[i];','                if(qa_stress_active and (target[i]==qa_stress_cell or origin[i]==qa_stress_cell) and transmitted[i]>0)std.debug.print("STRESS_EDGE tick={d} from={d} to={d} mass={d}\\n",.{qa_tick,origin[i],target[i],transmitted[i]});\n                self.newWaterMass[target[i]] += transmitted[i];')
p.write_text(s)
p=out/'main.zig';s=p.read_text();s=s.replace('    originReport("empty",state);','    originReport("empty",state);\n'+(here/'reserve-v6-migration.zig.part').read_text()+(here/'reserve-dry-edge.zig.part').read_text());needle='            var tick_timer=try std.time.Timer.start();'
s=s.replace(needle,'''            if(std.posix.getenv("QA_SHORE")!=null and i==4800){
                const shore=state.planet.getNeighbours(idx)[0];
                const surface=state.planet.elevation[idx]+state.planet.waterMass[idx]*state.planet.getKmPerWaterMass();
                state.planet.elevation[shore]=surface-0.00015;state.selectedPoint=shore;
                std.debug.assert(std.math.isFinite(state.setSelectedWaterTarget(@intCast(shore),0.15)));
                state.selectedPoint=idx;
                std.debug.print("SHORE_ACTION day=20 cell={d} one_time_water_m=0.15 biological_edits=false\\n",.{shore});
            }
            if(i%240==239){
                const M=@import("simulation/microbes.zig");const shore=state.planet.getNeighbours(idx)[0];
                const cell=state.planet.microbeCells[shore];var capable:usize=0;
                for(cell.cohorts)|co|if(co.biomass>0 and M.shoreCapable(co)){capable+=1;};
                std.debug.print("RESERVE_DAY day={d} shore={d} depth_m={d} biomass={d} reserve={d} protected={d}\\n",.{(i+1)/240,shore,state.planet.waterMass[shore]*state.planet.getKmPerWaterMass()*1000,M.biomass(cell),M.storedWater(cell),capable});
            }
'''+needle)
s=s.replace('        std.debug.print("TOTAL_WATER','        var tissue_and_carry:f64=0;for(state.planet.microbeCells)|cell|tissue_and_carry+=(@import("simulation/microbes.zig").storedWater(cell)+cell.surface_water_carry+cell.vapor_water_carry)*state.planet.getMeanPointArea()/1e9;water_end+=tissue_and_carry;\n        std.debug.print("TOTAL_WATER')
needle=' std.debug.print("ORIGIN_SAVE bytes=';i=s.index(needle);end=s.index('\n}',i)
s=s[:end]+'''
 state.selectedPoint=13596;state.pointerOnPlanet=true;
 _=state.planet.setWaterDepthMeters(state.selectedPoint,0);
 try (try saves.capture(a,state)).validate();
 _=state.makeSelectedNursery(@intCast(state.selectedPoint));
 try (try saves.capture(a,state)).validate();
 const wave=@import("god_actions.zig").wave(&state.planet,state.selectedPoint,state.selectedPoint);std.debug.assert(wave.success());
 try (try saves.capture(a,state)).validate();
 std.debug.print("PAUSED_NURSERY_SAVE fine_drain=true wave=true canonical=true\\n",.{});
'''+s[end:]
p.write_text(s)
