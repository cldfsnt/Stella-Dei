#!/usr/bin/env python3
from pathlib import Path
import subprocess,sys
root=Path(__file__).resolve().parents[2];out=Path(sys.argv[1])
subprocess.run([sys.executable,str(root/'web/tests/egl-ecology-pulse-prepare.py'),str(out)],check=True)
p=out/'main.zig';s=p.read_text();a=s.index('          var found=state.findRecordedFeeding(true);');b=s.index('\n        try originSaveCheck',a)
s=s[:a]+r'''
           _=pw;_=pm;const micro=@import("simulation/microbes.zig");
          const start_time=state.gameTime;
          for(0..4)|checkpoint|{
            if(checkpoint>0){for(0..600)|_|{state.planet.simulate(game.loop,.{.dt=1440,.timeScale=1,.solarConstant=state.solarConstant,.gameTime=state.gameTime,.planetRotationTime=state.planetRotationTime,.solarVector=state.simulationSolarVector()});state.gameTime+=1440;}}
            var count:usize=0;var occupied:usize=0;var mass:f64=0;var detritus:f64=0;var nutrient:f64=0;var generation:u32=0;var forms=[_]usize{0}**6;
            var lows=[_]f32{std.math.inf(f32)}**6;var highs=[_]f32{0}**6;
            var ids=std.AutoHashMap(u64,void).init(a);
            for(state.planet.microbeCells)|cell|{
              std.debug.assert(micro.validCell(cell,state.planet.microbeStats.next_lineage));
              var local:usize=0;detritus+=cell.detritus;nutrient+=cell.nutrient;
              for(cell.cohorts)|co|if(co.biomass>0){local+=1;count+=1;mass+=co.biomass;generation=@max(generation,co.generation);forms[@intFromEnum(micro.producerForm(co))]+=1;
                std.debug.assert(co.parent<co.lineage);const gop=try ids.getOrPut(co.lineage);std.debug.assert(!gop.found_existing);
                const traits=[_]f32{co.efficiency,co.optimum,co.structure,co.organization,co.feeding,co.mobility};for(traits,0..)|v,j|{lows[j]=@min(lows[j],v);highs[j]=@max(highs[j],v);}
              };if(local>0)occupied+=1;
            }
            std.debug.assert(state.planet.averageCarbonDioxideMass>=0 and state.planet.averageOxygenMass>=0);
            std.debug.print("NATURAL60 day={d} elapsed_days={d} colonies={d} patches={d} biomass_sum={d} detritus_sum={d} nutrient_sum={d} max_generation={d} forms={any} trait_min={any} trait_max={any} births={d} arrivals={d} tracked_losses={d} stats={s}\n",.{30+checkpoint*10,(state.gameTime-start_time)/86400,count,occupied,mass,detritus,nutrient,generation,forms,lows,highs,state.planet.microbeStats.births,state.planet.propaguleArrivals,state.planet.propaguleTrackedLosses,try std.json.stringifyAlloc(a,state.planet.microbeStats,.{})});
            for([_]usize{13594,13596,3421})|cell|std.debug.print("NATURAL60_HABITAT day={d} cell={d} depth_m={d} temp_K={d} nutrient={d} biomass={d}\n",.{30+checkpoint*10,cell,state.planet.waterMass[cell]*state.planet.getKmPerWaterMass()*1000,state.planet.temperature[cell],state.planet.microbeCells[cell].nutrient,micro.biomass(state.planet.microbeCells[cell])});
            // Snapshot biology before explicit camera-only framing, immediately frozen bytes.
            const snapshot=try std.json.stringifyAlloc(a,try saves.capture(a,state),.{});
            const snapshot_path=try std.fmt.allocPrint(a,"/workspace/scratch/f67c3ac60ca3/site-tmp/natural60-day{d}.json",.{30+checkpoint*10});try std.fs.cwd().writeFile(.{.sub_path=snapshot_path,.data=snapshot});
            const fit=state.findLivingClusterResult(390,700);render(window);gl.finish();window.swapBuffers();
            const image_path=try std.fmt.allocPrintZ(a,"/workspace/scratch/f67c3ac60ca3/site-tmp/natural60-day{d}.ppm",.{30+checkpoint*10});qa_capture(image_path);
            std.debug.print("NATURAL60_FRAME day={d} fit={d} screenshot=true\n",.{30+checkpoint*10,fit});
          }
        }
'''+s[b:];p.write_text(s)
