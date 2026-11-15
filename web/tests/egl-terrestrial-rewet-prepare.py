#!/usr/bin/env python3
"""Fixed24h dry/one-rewet actual scheduler experiment; no parameter changes."""
from pathlib import Path
import subprocess,sys,json,hashlib
r=Path(__file__).resolve().parents[2];o=Path(sys.argv[1]).resolve()
subprocess.run([sys.executable,str(r/'web/tests/egl-terrestrial-shared-prepare.py'),str(o)],check=True)
p=o/'main.zig';s=p.read_text()
s=s.replace('@import("simulation/shared_soil.zig").enabled=arm>=2;const trial_dt:f32=1440;const trial_ticks:usize=2;','@import("simulation/shared_soil.zig").enabled=true;const trial_dt:f32=1440;const trial_ticks:usize=60;')
needle='            for(0..trial_ticks)|tick|{'
assert s.count(needle)==1
s=s.replace(needle,r'''            std.debug.print("REWET_INVENTORY {s}\n",.{try std.json.stringifyAlloc(a,.{.arm=arm,.endpoint=false,.inventory=qaRewetInventory(&state.planet)},.{})});
            for(0..trial_ticks)|tick|{
              if(tick==30 and arm>=2){
                state.selectedPoint=target;state.pointerOnPlanet=true;state.paused=true;
                const before_action=try std.json.stringifyAlloc(a,try saves.capture(a,state),.{});
                const owned_action=try std.json.parseFromSlice(saves.schema.Save,a,before_action,.{.allocate=.alloc_always});
                const old_water=state.planet.waterMass[target];std.debug.assert(stella_test_action(1)==1);
                const added=@as(f64,state.planet.waterMass[target])-old_water;
                @constCast(owned_action.value.water)[target]=state.planet.waterMass[target];
                std.debug.assert(std.mem.eql(u8,try std.json.stringifyAlloc(a,owned_action.value,.{}),try std.json.stringifyAlloc(a,try saves.capture(a,state),.{})));
                std.debug.print("REWET_ACTION {s}\n",.{try std.json.stringifyAlloc(a,.{.arm=arm,.tick=tick,.added_native=added,.added_kg=added*1e9,.depth_m=state.planet.waterMass[target]*state.planet.getKmPerWaterMass()*1000,.soil=state.planet.rootSoil[target]},.{})});
              }
''')
needle='              std.debug.print("TERRESTRIAL_AFTER'
idx=s.index(needle)
s=s[:idx]+r'''              var found_cell:usize=std.math.maxInt(usize);var found_mass:f32=0;var child_count:usize=0;var child_mass:f64=0;
              for(state.planet.microbeCells,0..)|cell,ci|for(cell.cohorts)|co|{
                if(co.lineage==44 and co.biomass>0){found_cell=ci;found_mass=co.biomass;}
                if(co.parent==44 and co.biomass>0){child_count+=1;child_mass+=co.biomass;}
              };
              std.debug.print("REWET_FATE {s}\n",.{try std.json.stringifyAlloc(a,.{.arm=arm,.tick=tick,.id44_cell=found_cell,.id44_biomass=found_mass,.living_direct_children=child_count,.direct_child_biomass=child_mass,.target=state.planet.microbeCells[target],.temperature=state.planet.temperature[target]},.{})});
'''+s[idx:]
needle='            const ending=try'
s=s.replace(needle,r'''            std.debug.print("REWET_INVENTORY {s}\n",.{try std.json.stringifyAlloc(a,.{.arm=arm,.endpoint=true,.inventory=qaRewetInventory(&state.planet)},.{})});
'''+needle,1)
s+='''
fn qaRewetInventory(p:anytype)struct{water_native:f64,carbon_density_sum:f64,nutrient_density_sum:f64}{
 var w:f64=0;var c:f64=0;var n:f64=0;const area=p.getMeanPointArea();
 for(p.waterMass,p.waterVaporMass,p.rootSoil)|l,v,soil|w+=@as(f64,l)+v+soil*area/1e9;
 for(p.microbeCells)|cell|{
  c+=cell.detritus;n+=cell.nutrient;
  for(cell.cohorts)|co|{c+=co.biomass;n+=@as(f64,co.biomass)*@as(f64,@import("simulation/microbes.zig").nutrient_per_carbon);}
 }
 c+=p.averageCarbonDioxideMass*@as(f64,@floatFromInt(p.vertices.len))*1e9/area*(12.0/44.0);
 return .{.water_native=w,.carbon_density_sum=c,.nutrient_density_sum=n};
}
'''
p.write_text(s)
p=o/'simulation/planet.zig';s=p.read_text();needle='            const flux = Microbes.step(cell, environment, dt);';assert s.count(needle)==1
s=s.replace(needle,'''            const qa_before_cell=cell.*;
'''+needle+'''
            if(i==29441) std.debug.print("REWET_BIO {s}\\n",.{std.json.stringifyAlloc(self.allocator,.{.before=qa_before_cell,.after=cell.*,.flux=flux,.environment=environment,.dt=dt},.{}) catch unreachable});
''');p.write_text(s)
(o.parent/'provenance.json').write_text(json.dumps({'input_sha256':hashlib.sha256((r.parent/'site-tmp/sunlit14/day-14.json').read_bytes()).hexdigest(),'files':{str(p.relative_to(o)):hashlib.sha256(p.read_bytes()).hexdigest()for p in o.rglob('*.zig')}},indent=2)+'\n')
