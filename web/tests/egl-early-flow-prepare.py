#!/usr/bin/env python3
"""Three-day generated-world actual starter actions; no biological injection."""
from pathlib import Path
import subprocess,sys
root=Path(__file__).resolve().parents[2];out=Path(sys.argv[1]);subprocess.run([sys.executable,str(root/'web/tests/egl-nursery-prepare.py'),str(out)],check=True)
p=out/'states/play.zig';s=p.read_text();assert 'STELLA_PRODUCER_SEED' in s;s=s.replace('STELLA_PRODUCER_SEED','QA_FLOW_SEED');p.write_text(s)
p=out/'main.zig';s=p.read_text();a=s.index('    var max_structure:f32=0;var max_generation:u32=0;');b=s.index('fn originReport(',a)
h=r'''
    const M=@import("simulation/microbes.zig");var state=&game.state.Playing;state.paused=true;
    render(window);gl.finish();window.swapBuffers();
    const found=state.focusSeedableHabitat();
    std.debug.print("EARLY_FIND rng_seed={s} generated_seed={d} found={} cells={d}\n",.{std.posix.getenv("QA_FLOW_SEED") orelse "1337",state.planet.seed,found,state.planet.vertices.len});
    if(!found)return;
    const cell=state.selectedPoint;const point:u32=@intCast(cell);const paused=state.paused;const pace=state.timeScale;
    const beforeWater=state.planet.waterMass[cell]*state.planet.getKmPerWaterMass()*1000;
    const nursery=state.makeSelectedNursery(point);state.pointerOnPlanet=false;const seeded=state.seedSelectedColony(point);
    std.debug.assert(state.paused==paused and state.timeScale==pace);
    state.watchLife();render(window);gl.finish();window.swapBuffers();
    std.debug.print("EARLY_ACTIONS patch={d} nursery={d} seed={d} prior_depth_m={d} depth_m={d} temp_K={d} mass={d} reason={s} pause_pace_preserved=true\n",.{cell,nursery,seeded,beforeWater,state.planet.waterMass[cell]*state.planet.getKmPerWaterMass()*1000,state.planet.temperature[cell],M.biomass(state.planet.microbeCells[cell]),@tagName(state.planet.seedEligibility(cell))});
    if(nursery<=0 or seeded!=1)return;
    // Same assignments as speed control; no simulation state or organism is injected.
    state.timeScale=86400;state.simulationClock.reset();std.debug.assert(state.paused);state.paused=false;
    const start=state.gameTime;var day:usize=0;var frames:usize=0;var minWater:f32=std.math.inf(f32);var maxWater:f32=0;var minTemp:f32=std.math.inf(f32);var maxTemp:f32=0;var firstArrival:f64=-1;var firstBirth:f64=-1;
    while(state.gameTime-start<3*86400 and frames<1000):(frames+=1){
      loop.pump(16);state.update(&game,1.0/60.0);loop.pump(16);
      const water=state.planet.waterMass[cell]*state.planet.getKmPerWaterMass()*1000;minWater=@min(minWater,water);maxWater=@max(maxWater,water);minTemp=@min(minTemp,state.planet.temperature[cell]);maxTemp=@max(maxTemp,state.planet.temperature[cell]);
      if(firstArrival<0 and state.planet.propaguleArrivals>0)firstArrival=(state.gameTime-start)/86400;
      if(firstBirth<0 and state.planet.microbeStats.births>0)firstBirth=(state.gameTime-start)/86400;
      if(state.gameTime-start>=@as(f64,@floatFromInt(day+1))*86400){
        day+=1;var occupied:usize=0;var colonies:usize=0;var mass:f64=0;var support:f64=0;var gen:u32=0;
        for(state.planet.microbeCells)|c|{if(M.biomass(c)>0)occupied+=1;for(c.cohorts)|co|if(co.biomass>0){colonies+=1;mass+=co.biomass;support+=co.support_mass;gen=@max(gen,co.generation);};}
        std.debug.print("EARLY_DAY day={d} actual_days={d} occupied={d} colonies={d} biomass_sum={d} selected_mass={d} selected_depth_m={d} selected_K={d} nutrient={d} detritus={d} support_sum={d} generation={d} births={d} arrivals={d} tracked_losses={d}\n",.{day,(state.gameTime-start)/86400,occupied,colonies,mass,M.biomass(state.planet.microbeCells[cell]),water,state.planet.temperature[cell],state.planet.microbeCells[cell].nutrient,state.planet.microbeCells[cell].detritus,support,gen,state.planet.microbeStats.births,state.planet.propaguleArrivals,state.planet.propaguleTrackedLosses});
        render(window);gl.finish();window.swapBuffers();
        std.debug.print("EARLY_VISIBILITY day={d} occupied={d} rendered={d} targets={d} camera_distance={d} watch_view={}\n",.{day,occupied,state.visibleSprouts,state.colonyTargets.count,state.cameraDistance,state.watchLifeView});
      }
    }
    std.debug.print("EARLY_RESULT completed={} frames={d} simulated_days={d} requested_hours_per_sec=24 fixed_input_dt=1/60 browser_pace_claim=false first_birth_day={d} first_arrival_day={d} min_water_m={d} max_water_m={d} min_K={d} max_K={d} seed_calls=1 nursery_calls=1 later_care=false\n",.{day==3,frames,(state.gameTime-start)/86400,firstBirth,firstArrival,minWater,maxWater,minTemp,maxTemp});
    std.debug.assert(day==3);
    const size=window.getFramebufferSize();const before=state.visibleSprouts;const beforeTime=state.gameTime;const beforeBirths=state.planet.microbeStats.births;const beforeArrivals=state.planet.propaguleArrivals;
    const saves=@import("save_game.zig");var audit=std.heap.ArenaAllocator.init(allocator);defer audit.deinit();const aa=audit.allocator();
    const failureBefore=try std.json.stringifyAlloc(aa,try saves.capture(aa,state),.{});
    std.debug.assert(state.fitLivingClusterResult(1,1)==-3);
    std.debug.assert(std.mem.eql(u8,failureBefore,try std.json.stringifyAlloc(aa,try saves.capture(aa,state),.{})));
    const saved_bytes=try std.json.stringifyAlloc(aa,try saves.capture(aa,state),.{});const saved_parsed=try std.json.parseFromSlice(saves.schema.Save,aa,saved_bytes,.{.allocate=.alloc_always});const saved=saved_parsed.value;const oldPause=state.paused;const oldPace=state.timeScale;
    const compactWidth=(@as(f32,@floatFromInt(size.width))-40)/4;
    qa_pointer(24+2.5*compactWidth,28,1);render(window);gl.finish();
    qa_pointer(24+2.5*compactWidth,28,0);render(window);gl.finish();
    const fitted:i32=if(std.mem.startsWith(u8,state.mobileFeedback,"Fitted")) 1 else 0;
    std.debug.assert(state.paused==oldPause and state.timeScale==oldPace and state.watchLifeView);
    var after=try saves.capture(aa,state);
    std.debug.assert(std.mem.eql(u8,try std.json.stringifyAlloc(aa,saved.origin,.{}),try std.json.stringifyAlloc(aa,after.origin,.{})));
    after.camera=saved.camera;after.camera_target=saved.camera_target;after.camera_distance=saved.camera_distance;after.target_distance=saved.target_distance;
    std.debug.assert(std.mem.eql(u8,try std.json.stringifyAlloc(aa,saved,.{}),try std.json.stringifyAlloc(aa,after,.{})));
    std.debug.print("EARLY_UI_FIT width={d} button_width={d} actual_press_release=true origin_planet_save_exact=true pause_pace_preserved=true\n",.{size.width,compactWidth});
    if(fitted==1){const pause=state.paused;state.paused=true;state.update(&game,0);state.paused=pause;render(window);gl.finish();window.swapBuffers();}
    std.debug.assert(state.gameTime==beforeTime and state.planet.microbeStats.births==beforeBirths and state.planet.propaguleArrivals==beforeArrivals);
    std.debug.print("EARLY_EXPLICIT_FIT result={d} rendered_before={d} rendered_after={d} time_births_arrivals_unchanged=true no_auto_framing=true\n",.{fitted,before,state.visibleSprouts});
}

'''
s=s[:a]+h+s[b:];p.write_text(s)
