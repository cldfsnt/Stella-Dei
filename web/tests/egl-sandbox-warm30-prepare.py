#!/usr/bin/env python3
"""Fixed no-care continuation of earned warm finite-foraging world."""
from pathlib import Path
import subprocess,sys,json,hashlib
r=Path(__file__).resolve().parents[2];o=Path(sys.argv[1]).resolve()
subprocess.run([sys.executable,str(r/'web/tests/egl-foraging-production-prepare.py'),str(o)],check=True)
p=o/'simulation/life.zig';s=p.read_text();s='pub var qa_removed:f64=0;pub var qa_credit:f64=0;pub var qa_error:f64=0;pub var qa_patch:[]f64=&.{};\n'+s
s=s.replace('planet.vegetation[idx] = bite.after;','const qa_sat_before=self.satiety;\n                planet.vegetation[idx] = bite.after;')
s=s.replace('planet.rabbitMeals += 1;','qa_removed+=bite.eaten;qa_credit+=@as(f64,self.satiety)-qa_sat_before;qa_error+=@abs((@as(f64,self.satiety)-qa_sat_before)-@as(f64,bite.eaten)*150);if(idx<qa_patch.len)qa_patch[idx]+=bite.eaten;\n                planet.rabbitMeals += 1;')
p.write_text(s)
p=o/'main.zig';s=p.read_text();a=s.index('          _=pm;_=pw;');b=s.index('\n        std.debug.print("FORAGING_PRODUCTION_COMPLETE',a)
s=s[:a]+r'''
          _=pm;_=pw;std.debug.assert(state.planet.worldMode==.sandbox);
          const Life=@import("simulation/life.zig");const original=try std.json.stringifyAlloc(a,try saves.capture(a,state),.{});const initial=try std.json.parseFromSlice(saves.schema.Save,a,original,.{.allocate=.alloc_always});
          const n=state.planet.vegetation.len;const conv=state.planet.getKmPerWaterMass();const island=try a.alloc(bool,n);@memset(island,false);const queue=try a.alloc(usize,n);queue[0]=436;island[436]=true;var head:usize=0;var count:usize=1;
          while(head<count):(head+=1){for(state.planet.getNeighbours(queue[head]))|x|if(!island[x] and state.planet.waterMass[x]*conv<=0.0005){island[x]=true;queue[count]=x;count+=1;};}
          const previous=try a.dupe(f32,state.planet.vegetation);const deaths_by_patch=try a.alloc(u32,n);const recover_by_patch=try a.alloc(u32,n);@memset(deaths_by_patch,0);@memset(recover_by_patch,0);
          Life.qa_patch=try a.alloc(f64,n);@memset(Life.qa_patch,0);const day_start=try a.alloc(f32,n);
          var extinctions:usize=0;var recoveries:usize=0;const initial_rabbits=state.planet.lifeforms.items.len;var peak_rabbits=initial_rabbits;const initial_births=state.planet.rabbitBirths;const initial_deaths=state.planet.rabbitDeaths;
          std.debug.print("WARM30_SETUP island_cells={} rabbits={} start_time={d} no_new_intervention=true\n",.{count,initial_rabbits,state.gameTime});const run_start=std.time.nanoTimestamp();
          for(0..16)|day|{
            @memcpy(day_start,state.planet.vegetation);@memset(Life.qa_patch,0);
            for(0..60)|_|{
              loop.pump(16);state.planet.simulate(game.loop,.{.dt=1440,.timeScale=1,.solarConstant=state.solarConstant,.gameTime=state.gameTime,.planetRotationTime=state.planetRotationTime,.solarVector=state.simulationSolarVector()});state.gameTime+=1440;loop.pump(16);
              for(state.planet.vegetation,0..)|v,i|{std.debug.assert(std.math.isFinite(v) and v>=0 and v<=1);if(previous[i]>0 and v==0){extinctions+=1;deaths_by_patch[i]+=1;}if(previous[i]==0 and v>0){recoveries+=1;recover_by_patch[i]+=1;}previous[i]=v;}
              peak_rabbits=@max(peak_rabbits,state.planet.lifeforms.items.len);std.debug.assert(initial_rabbits+state.planet.rabbitBirths-initial_births-(state.planet.rabbitDeaths-initial_deaths)==state.planet.lifeforms.items.len);
            }
            var cover:f64=0;var island_cover:f64=0;var alive:usize=0;var island_alive:usize=0;var low:usize=0;var min_sat:f32=100;var sum_sat:f64=0;
            for(state.planet.vegetation,0..)|v,i|{
              cover+=v;if(v>0)alive+=1;if(v>0 and v<0.01)low+=1;if(island[i]){island_cover+=v;if(v>0)island_alive+=1;}
              if(day_start[i]>0 or v>0 or Life.qa_patch[i]>0)std.debug.print("WARM30_PATCH {s}\n",.{try std.json.stringifyAlloc(a,.{.day=day+15,.patch=i,.island=island[i],.before=day_start[i],.after=v,.grazed=Life.qa_patch[i],.extinctions=deaths_by_patch[i],.recoveries=recover_by_patch[i],.temperature=state.planet.temperature[i],.depth_m=state.planet.waterMass[i]*conv*1000},.{})});
            }
            for(state.planet.lifeforms.items)|rabbit|{min_sat=@min(min_sat,rabbit.satiety);sum_sat+=rabbit.satiety;}
            std.debug.print("WARM30_DAY {s}\n",.{try std.json.stringifyAlloc(a,.{.day=day+15,.peak_rabbits=peak_rabbits,.cover=cover,.island_cover=island_cover,.living_patches=alive,.island_living=island_alive,.low_patches=low,.extinctions=extinctions,.recoveries=recoveries,.rabbits=state.planet.lifeforms.items.len,.births=state.planet.rabbitBirths,.deaths=state.planet.rabbitDeaths,.meals=state.planet.rabbitMeals,.minimum_satiety=min_sat,.sum_satiety=sum_sat,.removed=Life.qa_removed,.credit=Life.qa_credit,.credit_error_abs=Life.qa_error,.plant_births=state.planet.plantBirths,.center_temperature=state.planet.temperature[436]},.{})});
          }
          std.debug.print("WARM30_RUNTIME seconds={d}\n",.{@as(f64,@floatFromInt(std.time.nanoTimestamp()-run_start))/1e9});
          const actual=try std.json.stringifyAlloc(a,try saves.capture(a,state),.{});try std.fs.cwd().writeFile(.{.sub_path="OUTPUT/day30.json",.data=actual});const endpoint=try std.json.parseFromSlice(saves.schema.Save,a,actual,.{.allocate=.alloc_always});
          for(0..10)|_|{state.planet.simulate(game.loop,.{.dt=1440,.timeScale=1,.solarConstant=state.solarConstant,.gameTime=state.gameTime,.planetRotationTime=state.planetRotationTime,.solarVector=state.simulationSolarVector()});state.gameTime+=1440;}
          const uninterrupted=try std.json.stringifyAlloc(a,try saves.capture(a,state),.{});try saves.apply(state,endpoint.value);std.debug.assert(std.mem.eql(u8,actual,try std.json.stringifyAlloc(a,try saves.capture(a,state),.{})));
          for(0..10)|_|{state.planet.simulate(game.loop,.{.dt=1440,.timeScale=1,.solarConstant=state.solarConstant,.gameTime=state.gameTime,.planetRotationTime=state.planetRotationTime,.solarVector=state.simulationSolarVector()});state.gameTime+=1440;}
          std.debug.assert(std.mem.eql(u8,uninterrupted,try std.json.stringifyAlloc(a,try saves.capture(a,state),.{})));try saves.apply(state,endpoint.value);
          state.selectedPoint=436;state.selectedTool=.None;state.showEscapeMenu=false;state.showPointDetails=false;state.showPlanetControl=false;const point=state.planet.transformedPoints[436];state.cameraPos=point.norm().scale(point.length()+200);state.targetCameraPos=state.cameraPos;state.cameraDistance=state.cameraPos.length();state.targetCameraDistance=state.cameraDistance;state.cameraGroundPoint=436;
          render(window);gl.finish();window.swapBuffers();qa_capture("OUTPUT/day30.ppm");
          try saves.apply(state,initial.value);std.debug.assert(std.mem.eql(u8,original,try std.json.stringifyAlloc(a,try saves.capture(a,state),.{})));
          std.debug.print("WARM30_PASS endpoint_reload_exact=true true_continuation_exact=true original_restored=true\n",.{});
        }
'''.replace('OUTPUT',str(o.parent))+s[b:];p.write_text(s)
subprocess.run([sys.executable,str(r/'web/tests/audit-zig-exports.py'),str(r/'src/main.zig'),str(p)],check=True,stdout=(o.parent/'export-audit.json').open('w'))
(o.parent/'source-hashes.json').write_text(json.dumps({f:hashlib.sha256((o/f).read_bytes()).hexdigest()for f in ['main.zig','simulation/life.zig','simulation/foraging.zig','simulation/ecology.zig','simulation/planet.zig']},indent=2)+'\n')
