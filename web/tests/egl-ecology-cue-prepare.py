#!/usr/bin/env python3
"""Actual observer purity/census and earned-fuel cue gate, no assigned biology."""
from pathlib import Path
import subprocess,sys,json,hashlib
r=Path(__file__).resolve().parents[2];o=Path(sys.argv[1]).resolve();subprocess.run([sys.executable,str(r/'web/tests/egl-arrival-toggle-prepare.py'),str(o)],check=True)
p=o/'main.zig';s=p.read_text();a=s.index('          _=pm;_=pw;');b=s.index('\n        std.debug.print("ARRIVAL_TOGGLE_COMPLETE',a)
s=s[:a]+r'''
          _=pm;_=pw;state.paused=true;state.showEscapeMenu=false;
          const E=@import("world_ecology.zig");const M=@import("simulation/microbes.zig");const world=@import("performance_details.zig").world_serial;
          const original=try std.json.stringifyAlloc(a,try saves.capture(a,state),.{});
          const initial=try std.json.parseFromSlice(saves.schema.Save,a,original,.{.allocate=.alloc_always});
          var counts=[_]usize{0}**6;var masses=[_]f64{0}**6;var start_living:usize=0;
          for(state.planet.microbeCells)|cell|for(cell.cohorts)|co|{if(co.biomass>0){const form=@intFromEnum(M.producerForm(co));counts[form]+=1;masses[form]+=co.biomass;start_living+=1;}};
          var snap=try std.json.parseFromSlice(std.json.Value,a,E.snapshot(&state.planet,world,state.gameTime,true),.{.allocate=.alloc_always});
          std.debug.assert(snap.value.object.get("scanned").?.integer==512);var chunks:usize=1;
          while(std.mem.eql(u8,snap.value.object.get("status").?.string,"pending")):(chunks+=1){snap=try std.json.parseFromSlice(std.json.Value,a,E.snapshot(&state.planet,world,state.gameTime,false),.{.allocate=.alloc_always});}
          for(snap.value.object.get("forms").?.array.items)|form|{var matched=false;for(0..6)|i|{if(std.mem.eql(u8,form.object.get("form").?.string,M.producerFormName(@enumFromInt(i)))){matched=true;std.debug.assert(form.object.get("colony_count").?.integer==counts[i]);const val=form.object.get("biomass_sum").?;const mass:f64=if(val==.float)val.float else @floatFromInt(val.integer);std.debug.assert(mass==masses[i]);}}std.debug.assert(matched);}
          std.debug.assert(snap.value.object.get("recent").?==.null);
          std.debug.assert(std.mem.eql(u8,original,try std.json.stringifyAlloc(a,try saves.capture(a,state),.{})));
          var off:[]const u8="";
          for(0..2)|arm|{try saves.apply(state,initial.value);E.enabled=arm==1;E.reset();const births=state.planet.microbeStats.births;
            for(0..30)|_|{state.planet.simulate(game.loop,.{.dt=1440,.timeScale=1,.solarConstant=state.solarConstant,.gameTime=state.gameTime,.planetRotationTime=state.planetRotationTime,.solarVector=state.simulationSolarVector()});state.gameTime+=1440;}
            const end=try std.json.stringifyAlloc(a,try saves.capture(a,state),.{});if(arm==0){off=end;}else{
              std.debug.assert(std.mem.eql(u8,off,end));var living:usize=0;for(state.planet.microbeCells)|cell|for(cell.cohorts)|co|{if(co.biomass>0)living+=1;};
              const recent_bytes=try a.dupe(u8,E.snapshot(&state.planet,world,state.gameTime,false));const result=try std.json.parseFromSlice(std.json.Value,a,recent_bytes,.{});const recent=result.value.object.get("recent").?.object.get("counts").?.object;
              std.debug.assert(recent.get("births").?.integer==state.planet.microbeStats.births-births);
              std.debug.assert(recent.get("deaths").?.integer==start_living+state.planet.microbeStats.births-births-living);
              for(0..3)|_|std.debug.assert(std.mem.eql(u8,recent_bytes,E.snapshot(&state.planet,world,state.gameTime,false)));
              std.debug.print("ECOLOGY_NATIVE_PASS chunks={} colonies={} full_save_rng_on_off_exact=true births={} deaths={} paused_queries_exact=true snapshot={s}\n",.{chunks,start_living,recent.get("births").?.integer,recent.get("deaths").?.integer,recent_bytes});
            }
          }
          try saves.apply(state,initial.value);std.debug.assert(std.mem.indexOf(u8,E.snapshot(&state.planet,world,state.gameTime,false),"\"recent\":null")!=null);
          // Same genuine earned fuel/one Water− as the preserved natural-fire test.
          state.selectedPoint=12395;state.pointerOnPlanet=true;std.debug.assert(state.testAction(2));state.selectedTool=.None;
          const dry=try std.json.stringifyAlloc(a,try saves.capture(a,state),.{});const dry_save=try std.json.parseFromSlice(saves.schema.Save,a,dry,.{.allocate=.alloc_always});
          const direct=@import("experimental/planet_ignition.zig").ignite(&state.planet,12395,12395);std.debug.assert(direct.success());const direct_save=try std.json.stringifyAlloc(a,try saves.capture(a,state),.{});
          try saves.apply(state,dry_save.value);state.selectedPoint=12395;const shown=state.applyIgnition(12395);std.debug.assert(std.meta.eql(direct,shown));std.debug.assert(state.ignitionCue!=null and state.ignitionCueSeconds>0);
          std.debug.assert(std.mem.eql(u8,direct_save,try std.json.stringifyAlloc(a,try saves.capture(a,state),.{})));
          _=stella_arrival_effects(0);const point=state.planet.transformedPoints[12395];state.cameraPos=point.norm().scale(point.length()+200);state.targetCameraPos=state.cameraPos;state.cameraDistance=state.cameraPos.length();state.targetCameraDistance=state.cameraDistance;state.showPointDetails=false;state.showPlanetControl=false;
          render(window);gl.finish();window.swapBuffers();qa_capture("OUTPUT/ignited.ppm");
          const rendered=try std.json.stringifyAlloc(a,try saves.capture(a,state),.{});const refusal=state.applyIgnition(12395);std.debug.assert(!refusal.success() and state.ignitionCue==null and state.ignitionCueSeconds==0);std.debug.assert(std.mem.eql(u8,rendered,try std.json.stringifyAlloc(a,try saves.capture(a,state),.{})));
          render(window);gl.finish();window.swapBuffers();qa_capture("OUTPUT/blocked.ppm");
          try saves.apply(state,initial.value);state.selectedPoint=12395;const wet=state.applyIgnition(12395);std.debug.assert(!wet.success() and state.ignitionCue==null);
          std.debug.assert(std.mem.eql(u8,original,try std.json.stringifyAlloc(a,try saves.capture(a,state),.{})));
          std.debug.print("IGNITION_CUE_PASS direct_physics_exact=true actual_burn_kg={d} heat_K={d} hidden_arrivals_independent=true nofuel_wet_clear=true load_reset=true original_restored=true\n",.{shown.burned_carbon_kg,shown.temperature_delta});
        }
'''.replace('OUTPUT',str(o.parent))+s[b:];s=s.replace('ARRIVAL_TOGGLE_COMPLETE','ECOLOGY_CUE_COMPLETE');p.write_text(s)
subprocess.run([sys.executable,str(r/'web/tests/audit-zig-exports.py'),str(r/'src/main.zig'),str(p)],check=True,stdout=(o.parent/'export-audit.json').open('w'))
(o.parent/'source-hashes.json').write_text(json.dumps({f:hashlib.sha256((o/f).read_bytes()).hexdigest()for f in ['main.zig','states/play.zig','world_ecology.zig','recent_ecology.zig','ignition_visuals.zig','save_game.zig','simulation/planet.zig']},indent=2)+'\n')
