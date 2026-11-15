#!/usr/bin/env python3
"""Fixed mature shoreline donor, legal nursery rim and finite-soil pair. QA only."""
from pathlib import Path
import subprocess,sys,json,hashlib
r=Path(__file__).resolve().parents[2];o=Path(sys.argv[1]).resolve()
subprocess.run([sys.executable,str(r/'web/tests/egl-terrestrial-shared-prepare.py'),str(o)],check=True)
p=o/'main.zig';s=p.read_text()
s=s.replace('const from:usize=29440;const target:usize=29441;const slot:usize=0;','const from:usize=12395;const target:usize=3121;const slot:usize=1;')
s=s.replace('lineage==44','lineage==931').replace('"44"','"931"').replace('@as(u64,44)','@as(u64,931)')
s=s.replace(' and state.planet.waterMass[target]==0','')
needle='          std.debug.print("TERRESTRIAL_STAGE enable\\n",.{});'
assert s.count(needle)==1
s=s.replace(needle,r'''          state.selectedPoint=204;state.pointerOnPlanet=true;
          const shape_before=try std.json.stringifyAlloc(a,try saves.capture(a,state),.{});
          const shape_owned=try std.json.parseFromSlice(saves.schema.Save,a,shape_before,.{.allocate=.alloc_always});
          std.debug.assert(stella_make_nursery(204)==19);
          var water_delta:f64=0;var changed:usize=0;
          for(state.planet.waterMass,state.planet.elevation,0..)|water,elev,i|{
            water_delta+=@as(f64,water)-shape_owned.value.water[i];
            if(water!=shape_owned.value.water[i] or elev!=shape_owned.value.elevation[i])changed+=1;
            @constCast(shape_owned.value.water)[i]=water;@constCast(shape_owned.value.elevation)[i]=elev;
          }
          std.debug.assert(std.mem.eql(u8,try std.json.stringifyAlloc(a,shape_owned.value,.{}),try std.json.stringifyAlloc(a,try saves.capture(a,state),.{})));
          std.debug.assert(state.planet.waterMass[target]==0);
          std.debug.print("MATURE_TERRAFORM {s}\n",.{try std.json.stringifyAlloc(a,.{.center=@as(usize,204),.target=target,.changed=changed,.water_delta_native=water_delta},.{})});
'''+needle)
s=s.replace('state.planet.rootConfig=.{.enabled=true,.law=1,.conductance=10};','state.planet.rootConfig=.{.enabled=true,.law=1,.conductance=10};@import("simulation/shared_soil.zig").enabled=true;')
needle='          state.planet.simulate(game.loop,.{.dt=1440,.timeScale=1,.solarConstant=state.solarConstant,.gameTime=state.gameTime,.planetRotationTime=state.planetRotationTime,.solarVector=state.simulationSolarVector()});state.gameTime+=1440;'
assert s.count(needle)==1;s=s.replace(needle,'          for(0..60)|_|{\n'+needle+'\n          }')
s=s.replace('for(0..4)|arm|{','for(0..2)|arm|{')
s=s.replace('@import("simulation/shared_soil.zig").enabled=arm>=2;const trial_dt:f32=1440;const trial_ticks:usize=2;','@import("simulation/shared_soil.zig").enabled=true;const trial_dt:f32=1440;const trial_ticks:usize=60;')
s=s.replace('            const ending=try',r'''            var living_cell:usize=std.math.maxInt(usize);var living_mass:f32=0;var children:usize=0;
            for(state.planet.microbeCells,0..)|cell,i|for(cell.cohorts)|co|{
              if(co.lineage==931 and co.biomass>0){living_cell=i;living_mass=co.biomass;}
              if(co.parent==931 and co.biomass>0)children+=1;
            };
            std.debug.print("MATURE_FATE {s}\n",.{try std.json.stringifyAlloc(a,.{.arm=arm,.cell=living_cell,.biomass=living_mass,.living_direct_children=children,.target_cell=state.planet.microbeCells[target]},.{})});
            const ending=try''',1)
p.write_text(s)
p=o/'simulation/planet.zig';s=p.read_text().replace('if(i==29441)','if(i==3121)');p.write_text(s)
(o.parent/'mature-provenance.json').write_text(json.dumps({'input':str(r.parent/'site-tmp/natural60-day60.json'),'input_sha256':hashlib.sha256((r.parent/'site-tmp/natural60-day60.json').read_bytes()).hexdigest(),'files':{str(p.relative_to(o)):hashlib.sha256(p.read_bytes()).hexdigest()for p in o.rglob('*.zig')}},indent=2)+'\n')
