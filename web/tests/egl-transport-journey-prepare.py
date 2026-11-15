#!/usr/bin/env python3
from pathlib import Path
import subprocess,sys
root=Path(__file__).resolve().parents[2];out=Path(sys.argv[1])
subprocess.run([sys.executable,str(root/'web/tests/egl-ecology-pulse-prepare.py'),str(out)],check=True)
p=out/'main.zig';s=p.read_text();start=s.index('          var found=state.findRecordedFeeding(true);');end=s.index('\n        try originSaveCheck',start)
s=s[:start]+r'''
          _=pm;_=pw;const M=@import("simulation/microbes.zig");
          const frozen=try std.json.stringifyAlloc(a,try saves.capture(a,state),.{});const baseline=try std.json.parseFromSlice(saves.schema.Save,a,frozen,.{.allocate=.alloc_always});
          var watched_endpoint:?[]const u8=null;
          for(0..3)|arm|{
            try saves.apply(state,baseline.value);state.selectedPoint=12344;state.paused=true;state.timeScale=86400;state.simulationClock.reset();state.showEscapeMenu=false;state.showPointDetails=false;state.showPlanetControl=false;
            if(arm>0){const preview=try std.json.parseFromSlice(std.json.Value,a,std.mem.span(stella_transport_prepare(PerformanceDetails.world_serial,12344,3,13594,"120")),.{});std.debug.assert(preview.value.object.get("ok").?.bool);const token:u32=@intCast(preview.value.object.get("token").?.integer);
              const moved=try std.json.parseFromSlice(std.json.Value,a,std.mem.span(stella_transport_execute(token)),.{});std.debug.assert(moved.value.object.get("ok").?.bool);
              const inspect=try std.json.parseFromSlice(std.json.Value,a,std.mem.span(stella_transport_inspect(PerformanceDetails.world_serial,13594,"120")),.{});std.debug.assert(inspect.value.object.get("ok").?.bool and state.selectedPoint==13594);
            }
            const watched_cell=state.selectedPoint;state.watchLife();state.targetCameraPos=state.planet.transformedPoints[watched_cell];_=state.fitLivingClusterResult(390,700);
            std.debug.assert(stella_patch_watch_start_checked(@intCast(watched_cell),PerformanceDetails.world_serial,1)==1 and !state.paused and state.timeScale==86400);
            if(arm==2)stella_patch_watch_stop(0);
            const initial=try std.json.parseFromSlice(std.json.Value,a,std.mem.span(stella_patch_watch_snapshot()),.{.allocate=.alloc_always});_=initial;
            render(window);gl.finish();window.swapBuffers();
            var family=std.AutoHashMap(u64,void).init(a);try family.put(120,{});const first_new_id=state.planet.microbeStats.next_lineage;var offspring:usize=0;var frames:usize=0;var next_day:usize=3;var lost_original_at:f64=-1;const start_time=state.gameTime;const start_births=state.planet.microbeStats.births;std.debug.print("TRANSPORT_FAMILY_BASELINE arm={d} first_new_id={d} root_only=true preexisting_descendants_excluded=true\n",.{arm,first_new_id});
            while(state.gameTime-start_time<10*86400 and frames<3000):(frames+=1){
              loop.pump(16);state.update(&game,1.0/60.0);loop.pump(16);
              var original_alive=false;
              for(state.planet.microbeCells)|c|for(c.cohorts)|co|{if(co.biomass>0){if(co.lineage==120)original_alive=true;if(co.lineage>=first_new_id and family.contains(co.parent) and !family.contains(co.lineage)){try family.put(co.lineage,{});offspring+=1;}}};
              if(!original_alive and lost_original_at<0)lost_original_at=(state.gameTime-start_time)/86400;
              if(state.gameTime-start_time>=@as(f64,@floatFromInt(next_day))*86400){
                var alive:usize=0;var mass:f64=0;var family_support:f64=0;var generation:u32=0;
                for(state.planet.microbeCells,0..)|c,i|for(c.cohorts)|co|{if(co.biomass>0 and family.contains(co.lineage)){alive+=1;mass+=co.biomass;family_support+=co.support_mass;generation=@max(generation,co.generation);if(co.lineage==120)std.debug.print("TRANSPORT_JOURNEY_ORIGINAL arm={d} day={d} cell={d} cohort={s}\n",.{arm,next_day,i,try std.json.stringifyAlloc(a,co,.{})});}};
                std.debug.print("TRANSPORT_JOURNEY arm={d} day={d} actual_days={d} selected={d} paused={} requested={d} original_alive={} first_absent_day={d} tracked_family_alive={d} new_offspring_seen={d} family_mass={d} family_support={d} max_generation={d} world_births_delta={d} source_mass={d} target_mass={d} target_water_m={d} target_temp={d} watch={s}\n",.{arm,next_day,(state.gameTime-start_time)/86400,state.selectedPoint,state.paused,state.timeScale,original_alive,lost_original_at,alive,offspring,mass,family_support,generation,state.planet.microbeStats.births-start_births,M.biomass(state.planet.microbeCells[12344]),M.biomass(state.planet.microbeCells[13594]),state.planet.waterMass[13594]*state.planet.getKmPerWaterMass()*1000,state.planet.temperature[13594],std.mem.span(stella_patch_watch_snapshot())});
                std.debug.assert(state.selectedPoint==watched_cell and !state.paused and state.timeScale==86400);
                render(window);gl.finish();window.swapBuffers();const shot=try std.fmt.allocPrintZ(a,"/workspace/scratch/f67c3ac60ca3/site-tmp/transport-journey/arm-{d}-day-{d}.ppm",.{arm,next_day});qa_capture(shot);next_day=10;
              }
            }
            std.debug.assert(state.gameTime-start_time>=10*86400);
            if(arm==1)watched_endpoint=try std.json.stringifyAlloc(a,try saves.capture(a,state),.{});
            if(arm==2){std.debug.assert(std.mem.eql(u8,watched_endpoint.?,try std.json.stringifyAlloc(a,try saves.capture(a,state),.{})));std.debug.print("TRANSPORT_JOURNEY_OBSERVER_PARITY actual10day_full_saved_world_exact=true\n",.{});}
            std.debug.print("TRANSPORT_JOURNEY_DONE arm={d} frames={d} fixed_input_dt=1/60 actual_update_scheduler=true no_browser_speed_claim=true\n",.{arm,frames});
          }
          try saves.apply(state,baseline.value);std.debug.assert(std.mem.eql(u8,frozen,try std.json.stringifyAlloc(a,try saves.capture(a,state),.{})));
        }
''' +s[end:];s=s.replace('if (!is_web or !web_initialized or !game.state_init) return null;','if (!game.state_init) return null; // Isolated native real-export bridge.');p.write_text(s)
