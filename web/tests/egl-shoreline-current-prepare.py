#!/usr/bin/env python3
from pathlib import Path
import subprocess,sys,json,hashlib
r=Path(__file__).resolve().parents[2];o=Path(sys.argv[1]).resolve()
subprocess.run([sys.executable,str(r/'web/tests/egl-foraging-production-prepare.py'),str(o)],check=True)
p=o/'main.zig';s=p.read_text();a=s.index('          _=pm;_=pw;');b=s.index('\n        std.debug.print("FORAGING_PRODUCTION_COMPLETE',a)
s=s[:a]+r'''
          _=pm;_=pw;const M=@import("simulation/microbes.zig");std.debug.assert(state.planet.worldMode==.origin);
          state.paused=true;state.showEscapeMenu=false;state.showPointDetails=false;state.showPlanetControl=false;state.selectedTool=.None;
          const target:usize=12395;const ids=[_]u64{1104,931,1114};state.selectedPoint=target;
          for(ids,0..)|id,slot|std.debug.assert(state.planet.microbeCells[target].cohorts[slot].lineage==id);
          const original=try std.json.stringifyAlloc(a,try saves.capture(a,state),.{});
          const initial=try std.json.parseFromSlice(saves.schema.Save,a,original,.{.allocate=.alloc_always});
          for(0..3)|arm|{
            try saves.apply(state,initial.value);state.selectedPoint=target;state.pointerOnPlanet=true;
            qa_shore_arm=arm;std.debug.print("SHORE_START {s}\n",.{try std.json.stringifyAlloc(a,.{.arm=arm,.cell=state.planet.microbeCells[target],.inventory=qaShoreInventory(&state.planet)},.{})});
            for(0..60)|tick|{
              qa_shore_tick=tick;
              if((tick==0 and arm>0) or (tick==15 and arm==2)){
                const before=try std.json.stringifyAlloc(a,try saves.capture(a,state),.{});
                const owned=try std.json.parseFromSlice(saves.schema.Save,a,before,.{.allocate=.alloc_always});
                const old=state.planet.waterMass[target];
                if(tick==0)std.debug.assert(stella_test_action(2)==1) else std.debug.assert(stella_adjust_water(target,0.02)>0);
                const change=@as(f64,state.planet.waterMass[target])-old;
                @constCast(owned.value.water)[target]=state.planet.waterMass[target];
                std.debug.assert(std.mem.eql(u8,try std.json.stringifyAlloc(a,owned.value,.{}),try std.json.stringifyAlloc(a,try saves.capture(a,state),.{})));
                std.debug.print("SHORE_ACTION {s}\n",.{try std.json.stringifyAlloc(a,.{.arm=arm,.tick=tick,.change_native=change,.change_kg=change*1e9,.before_depth_m=old*state.planet.getKmPerWaterMass()*1000,.after_depth_m=state.planet.waterMass[target]*state.planet.getKmPerWaterMass()*1000},.{})});
              }
              state.planet.simulate(game.loop,.{.dt=1440,.timeScale=1,.solarConstant=state.solarConstant,.gameTime=state.gameTime,.planetRotationTime=state.planetRotationTime,.solarVector=state.simulationSolarVector()});state.gameTime+=1440;
              var masses=[_]f32{0,0,0};var locations=[_]usize{std.math.maxInt(usize),std.math.maxInt(usize),std.math.maxInt(usize)};
              for(state.planet.microbeCells,0..)|cell,ci|for(cell.cohorts)|co|for(ids,0..)|id,j|{if(co.lineage==id and co.biomass>0){masses[j]=co.biomass;locations[j]=ci;}};
              const depth=state.planet.waterMass[target]*state.planet.getKmPerWaterMass();var habitat:[4]f32=undefined;var heights:[4]f32=undefined;var protection:[4]f32=undefined;
              for(state.planet.microbeCells[target].cohorts,0..)|co,j|{habitat[j]=M.photosyntheticHabitat(co,depth,state.planet.temperature[target]);heights[j]=M.producerHeightMeters(co);protection[j]=M.filmProtection(co);}
              std.debug.print("SHORE_STEP {s}\n",.{try std.json.stringifyAlloc(a,.{.arm=arm,.tick=tick,.depth_m=depth*1000,.temperature=state.planet.temperature[target],.cell=state.planet.microbeCells[target],.original_masses=masses,.original_locations=locations,.habitat=habitat,.heights_m=heights,.film_protection=protection},.{})});
            }
            std.debug.print("SHORE_END {s}\n",.{try std.json.stringifyAlloc(a,.{.arm=arm,.inventory=qaShoreInventory(&state.planet),.stats=state.planet.microbeStats},.{})});
            const ending=try std.json.stringifyAlloc(a,try saves.capture(a,state),.{});var path:[1024]u8=undefined;
            try std.fs.cwd().writeFile(.{.sub_path=try std.fmt.bufPrint(&path,"OUTPUT/arm-{}.json",.{arm}),.data=ending});
            const parsed=try std.json.parseFromSlice(saves.schema.Save,a,ending,.{.allocate=.alloc_always});try saves.apply(state,parsed.value);
            std.debug.assert(std.mem.eql(u8,ending,try std.json.stringifyAlloc(a,try saves.capture(a,state),.{})));
            state.selectedPoint=target;state.watchLifeView=true;state.selectedTool=.None;_=state.fitLivingClusterResult(390,700);
            render(window);gl.finish();window.swapBuffers();qa_capture(try std.fmt.bufPrintZ(&path,"OUTPUT/arm-{}.ppm",.{arm}));
            std.debug.print("SHORE_ARM_PASS arm={} save_reload_exact=true\n",.{arm});
          }
          try saves.apply(state,initial.value);std.debug.assert(std.mem.eql(u8,original,try std.json.stringifyAlloc(a,try saves.capture(a,state),.{})));
          std.debug.print("SHORE_COMPLETE original_restored=true current_core=true\n",.{});std.process.exit(0);
        }
'''.replace('OUTPUT',str(o.parent))+s[b:]
s+='''
pub var qa_shore_arm:usize=0;
pub var qa_shore_tick:usize=0;
fn qaShoreInventory(p:anytype)struct{water_native:f64,carbon_density_sum:f64,nutrient_density_sum:f64}{
 var w:f64=0;var c:f64=0;var n:f64=0;const area=p.getMeanPointArea();
 for(p.waterMass,p.waterVaporMass)|l,v|w+=@as(f64,l)+v;
 for(p.microbeCells)|cell|{c+=cell.detritus;n+=cell.nutrient;for(cell.cohorts)|co|{c+=co.biomass;n+=@as(f64,co.biomass)*@as(f64,@import("simulation/microbes.zig").nutrient_per_carbon);}}
 c+=p.averageCarbonDioxideMass*@as(f64,@floatFromInt(p.vertices.len))*1e9/area*(12.0/44.0);
 return .{.water_native=w,.carbon_density_sum=c,.nutrient_density_sum=n};
}
'''
p.write_text(s)
p=o/'simulation/planet.zig';s=p.read_text();needle='            const flux = Microbes.step(cell, self.microbeEnvironment(i, light), dt);'
# Production may name immutable environment differently; no semantic replacement.
assert s.count(needle)==1
s=s.replace(needle,'            const qa_before_cell=cell.*;\n'+needle+'''
            if(i==12395)std.debug.print("SHORE_BIO {s}\\n",.{std.json.stringifyAlloc(self.allocator,.{.arm=@import("root").qa_shore_arm,.tick=@import("root").qa_shore_tick,.before=qa_before_cell,.after=cell.*,.flux=flux,.environment=self.microbeEnvironment(i, light)},.{}) catch unreachable});
''');p.write_text(s)
assert (o/'simulation/microbes.zig').read_bytes()==(r/'src/simulation/microbes.zig').read_bytes()
subprocess.run([sys.executable,str(r/'web/tests/audit-zig-exports.py'),str(r/'src/main.zig'),str(o/'main.zig')],check=True,stdout=(o.parent/'export-audit.json').open('w'))
(o.parent/'provenance.json').write_text(json.dumps({'input_sha256':hashlib.sha256((r.parent/'site-tmp/natural60-day60.json').read_bytes()).hexdigest(),'core_sha256':hashlib.sha256((r/'src/simulation/microbes.zig').read_bytes()).hexdigest(),'head':subprocess.check_output(['git','rev-parse','HEAD'],cwd=r,text=True).strip(),'files':{str(p.relative_to(o)):hashlib.sha256(p.read_bytes()).hexdigest()for p in o.rglob('*.zig')}},indent=2)+'\n')
