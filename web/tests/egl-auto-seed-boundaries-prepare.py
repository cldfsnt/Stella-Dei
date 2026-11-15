#!/usr/bin/env python3
"""Four-point actual Planet/transaction boundary gate; no production changes."""
from pathlib import Path
import sys,subprocess
r=Path(__file__).resolve().parents[2];o=Path(sys.argv[1]).resolve()
subprocess.run([sys.executable,str(r/'web/tests/egl-auto-seed-prepare.py'),str(o)],check=True)
p=o/'main.zig';s=p.read_text();a=s.index('          _=pm;_=pw;');b=s.index('\n        std.debug.print("AUTO_SEED_GATE',a)
s=s[:a]+r'''
          _=pw;state.paused=true;state.showEscapeMenu=false;
          const AS=@import("auto_seed.zig");const M=@import("simulation/microbes.zig");const world=@import("performance_details.zig").world_serial;
          const original=try std.json.stringifyAlloc(a,try saves.capture(a,state),.{});
          const real_planet=state.planet;
          const Snap=struct{fn capture(al:std.mem.Allocator,p:pm.Planet)![]u8{return std.json.stringifyAlloc(al,.{.cells=p.microbeCells,.stats=p.microbeStats,.co2=p.averageCarbonDioxideMass,.o2=p.averageOxygenMass,.water=p.waterMass,.temperature=p.temperature,.elevation=p.elevation,.seed=p.seed,.radius=p.radius},.{});}};
          for(0..2)|scenario|{
            state.planet=real_planet;state.planet.vertices=real_planet.vertices[0..4];
            state.planet.microbeCells=try a.alloc(M.Cell,4);state.planet.waterMass=try a.alloc(f32,4);state.planet.temperature=try a.alloc(f32,4);state.planet.elevation=try a.dupe(f32,real_planet.elevation[0..4]);
            state.planet.microbeStats=.{};
            for(state.planet.microbeCells,0..)|*c,i|c.*=M.initialized(i+1);
            @memset(state.planet.temperature,293.15);@memset(state.planet.waterMass,0.001/state.planet.getKmPerWaterMass());
            state.planet.averageCarbonDioxideMass=real_planet.averageCarbonDioxideMass;state.planet.averageOxygenMass=real_planet.averageOxygenMass;
            // Actual existing seed pays the first resident, leaving three slots.
            std.debug.assert(state.planet.seedMicrobes(0));
            std.debug.assert(state.planet.microbeCells[0].cohorts[0].biomass>0 and state.planet.microbeCells[0].cohorts[1].biomass==0);
            const area=@as(f64,state.planet.getMeanPointArea());
            if(scenario==1)state.planet.averageCarbonDioxideMass=@as(f64,@as(f32,@bitCast(@as(u32,1))))*area/1e9*(44.0/12.0);
            const before=try Snap.capture(a,state.planet);const input_cells=try a.dupe(M.Cell,state.planet.microbeCells);const input_stats=state.planet.microbeStats;const input_co2=state.planet.averageCarbonDioxideMass;const input_o2=state.planet.averageOxygenMass;
            var successes:usize=0;var eligible_count:usize=0;var source_fixed:f64=0;
            var allowed:[4]bool=undefined;for(&allowed,0..)|*yes,i|{yes.*=state.planet.seedEligibility(i)==.eligible;if(yes.*)eligible_count+=1;}
            std.debug.assert(eligible_count==4);
            for(allowed,0..)|yes,i|if(yes){const mass_before=M.biomass(state.planet.microbeCells[i]);const gas_before=state.planet.averageCarbonDioxideMass;if(state.planet.seedMicrobes(i))successes+=1;source_fixed+=@as(f64,M.biomass(state.planet.microbeCells[i]))-mass_before;std.debug.assert(state.planet.averageCarbonDioxideMass<=gas_before);};
            const expected=try Snap.capture(a,state.planet);const final_co2=state.planet.averageCarbonDioxideMass;
            if(scenario==0)std.debug.assert(successes==4)else std.debug.assert(successes>0 and successes<4);
            for(0..2)|attempt|{
              @memcpy(state.planet.microbeCells,input_cells);state.planet.microbeStats=input_stats;state.planet.averageCarbonDioxideMass=input_co2;state.planet.averageOxygenMass=input_o2;
              var reply=try std.json.parseFromSlice(std.json.Value,a,AS.start(state,world,world),.{.allocate=.alloc_always});const ticket:u32=@intCast(reply.value.object.get("token").?.integer);
              std.debug.assert(reply.value.object.get("ok").?.bool);
              while(std.mem.eql(u8,reply.value.object.get("phase").?.string,"planning"))reply=try std.json.parseFromSlice(std.json.Value,a,AS.step(state,world,ticket),.{.allocate=.alloc_always});
              std.debug.assert(std.mem.eql(u8,reply.value.object.get("phase").?.string,"ready"));
              for([_]struct{key:[]const u8,value:usize}{.{.key="eligible",.value=4},.{.key="planted",.value=successes},.{.key="skipped",.value=4-successes},.{.key="resource_skips",.value=4-successes},.{.key="identity_skips",.value=0},.{.key="ineligible",.value=0}})|check|std.debug.assert(reply.value.object.get(check.key).?.integer==check.value);
              std.debug.assert(std.mem.eql(u8,before,try Snap.capture(a,state.planet)));
              if(attempt==0){_=AS.cancel(ticket);std.debug.assert(std.mem.eql(u8,before,try Snap.capture(a,state.planet)));}else{const result=AS.apply(state,world,ticket);std.debug.assert(std.mem.indexOf(u8,result,"\"ok\":true")!=null);std.debug.assert(std.mem.eql(u8,expected,try Snap.capture(a,state.planet)));std.debug.print("AUTO_SEED_BOUNDARY scenario={} area_m2={d} co2_before={d} co2_after={d} measured_biomass_delta={d} fixed_carbon_kg={d} partial_existing_preserved={} receipt={s}\n",.{scenario,area,input_co2,final_co2,source_fixed,state.planet.microbeStats.fixed_carbon-input_stats.fixed_carbon,std.meta.eql(state.planet.microbeCells[0].cohorts[0],input_cells[0].cohorts[0]),result});}
            }
          }
          state.planet=real_planet;
          std.debug.assert(std.mem.eql(u8,original,try std.json.stringifyAlloc(a,try saves.capture(a,state),.{})));
          std.debug.print("AUTO_SEED_BOUNDARY_COMPLETE reference_exact=true cancel_unchanged=true original_restored=true synthetic_four_point_geometry=true\n",.{});
        }
'''+s[b:];p.write_text(s)
subprocess.run([sys.executable,str(r/'web/tests/audit-zig-exports.py'),str(r/'src/main.zig'),str(p)],check=True,stdout=(o.parent/'export-audit.json').open('w'))
