#!/usr/bin/env python3
"""Actual 30-day seeded nursery: exact flux oracle and observation-on/off save identity."""
from pathlib import Path
import subprocess,sys
root=Path(__file__).resolve().parents[2];out=Path(sys.argv[1])
subprocess.run([sys.executable,str(root/'web/tests/egl-feeding-find-prepare.py'),str(out)],check=True)
p=out/'simulation/planet.zig';s=p.read_text();s='pub var qa_watch_cell:usize=0;pub var qa_flux:f64=0;\n'+s;s=s.replace('            if(observing)watch.record(i,flux.grazed);','            if(i==qa_watch_cell)qa_flux+=@as(f64,flux.grazed);\n            if(observing)watch.record(i,flux.grazed);');p.write_text(s)
p=out/'main.zig';s=p.read_text();n='        try originSaveCheck(state,allocator);';h=r'''
        {
          const saves=@import("save_game.zig");const pw=@import("patch_watch.zig");const pm=@import("simulation/planet.zig");
          var arena=std.heap.ArenaAllocator.init(allocator);defer arena.deinit();const a=arena.allocator();
          var found=state.findRecordedFeeding(true);while(found==2)found=state.findRecordedFeeding(false);std.debug.assert(found==1);
          // QA-only selection: first naturally populated patch containing both a living feeder and another living cohort. No trait/resources assignments.
          var coexist=false;for(state.planet.microbeCells,0..)|pc,pi|{var living:usize=0;var feeder=false;for(pc.cohorts)|co|{if(co.biomass>0){living+=1;if(co.feeding>0)feeder=true;}}if(living>=2 and feeder){state.selectedPoint=pi;coexist=true;break;}}
          std.debug.assert(coexist);

          const frozen=try std.json.stringifyAlloc(a,try saves.capture(a,state),.{});
          try std.fs.cwd().writeFile(.{.sub_path="/workspace/scratch/f67c3ac60ca3/site-tmp/watch-natural-30day.json",.data=frozen});
          const parsed_before=try std.json.parseFromSlice(saves.schema.Save,a,frozen,.{.allocate=.alloc_always});const before=parsed_before.value;const start_time=state.gameTime;const cell=state.selectedPoint;
          try saves.apply(state,before);state.selectedPoint=cell;
          pm.qa_watch_cell=cell;pm.qa_flux=0;
          std.debug.print("WATCH_STAGE begin cell={d} paused={} menu={}\n",.{cell,state.paused,state.showEscapeMenu});
          std.debug.assert(patchWatchStartForState(state,@intCast(cell))==1);
          for(0..60)|_|{state.planet.simulate(game.loop,.{.dt=1440,.timeScale=1,.solarConstant=state.solarConstant,.gameTime=state.gameTime,.planetRotationTime=state.planetRotationTime,.solarVector=state.simulationSolarVector()});state.gameTime+=1440;}
          const watched=pw.current;std.debug.print("WATCH_STAGE recorded active={} ticks={d} elapsed={d} intake={d} oracle={d}\n",.{watched.active,watched.ticks,watched.elapsed,watched.consumed,pm.qa_flux});std.debug.assert(watched.active);std.debug.assert(watched.ticks==60 and watched.elapsed==86400);std.debug.assert(watched.consumed==pm.qa_flux);
          const with_watch=try std.json.stringifyAlloc(a,try saves.capture(a,state),.{});
          try saves.apply(state,before);state.selectedPoint=cell;std.debug.assert(!pw.current.active);std.debug.assert(state.gameTime==start_time);
          for(0..60)|_|{state.planet.simulate(game.loop,.{.dt=1440,.timeScale=1,.solarConstant=state.solarConstant,.gameTime=state.gameTime,.planetRotationTime=state.planetRotationTime,.solarVector=state.simulationSolarVector()});state.gameTime+=1440;}
          const without_watch=try std.json.stringifyAlloc(a,try saves.capture(a,state),.{});std.debug.print("WATCH_STAGE parity={} selected_after_load={d}\n",.{std.mem.eql(u8,with_watch,without_watch),state.selectedPoint});
          if(!std.mem.eql(u8,with_watch,without_watch)){try std.fs.cwd().writeFile(.{.sub_path="/workspace/scratch/f67c3ac60ca3/site-tmp/watch-on.json",.data=with_watch});try std.fs.cwd().writeFile(.{.sub_path="/workspace/scratch/f67c3ac60ca3/site-tmp/watch-off.json",.data=without_watch});}
          std.debug.assert(std.mem.eql(u8,with_watch,without_watch));
          state.selectedPoint=cell;
          std.debug.assert(patchWatchStartForState(state,@intCast(cell))==1);state.paused=true;state.update(&game,0);std.debug.assert(!pw.current.active);state.paused=false;
          std.debug.assert(patchWatchStartForState(state,@intCast(cell))==1);state.selectedPoint=(cell+1)%state.planet.vertices.len;pw.current.guard(state.selectedPoint,PerformanceDetails.world_serial,state.gameTime,pw.nowMs(),false);std.debug.assert(!pw.current.active);state.selectedPoint=cell;
          try saves.apply(state,before);
          std.debug.print("PATCH_WATCH natural_world=true cell={d} consumed={d} oracle={d} ticks={d} sim_seconds={d} exact_flux=true on_off_save_identical=true pause_selection_load_cancel=true no_biology_changes=true\n",.{cell,watched.consumed,watched.consumed,watched.ticks,watched.elapsed});
        }
''';assert n in s;s=s.replace(n,h+n,1);s=s.replace('/workspace/scratch/f67c3ac60ca3/site-tmp',str(out.parent));p.write_text(s)
