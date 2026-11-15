#!/usr/bin/env python3
from pathlib import Path
import subprocess,sys
root=Path(__file__).resolve().parents[2];out=Path(sys.argv[1])
subprocess.run([sys.executable,str(root/'web/tests/egl-ecology-pulse-prepare.py'),str(out)],check=True)
p=out/'main.zig';s=p.read_text();start=s.index('          var found=state.findRecordedFeeding(true);');end=s.index('\n        try originSaveCheck',start)
s=s[:start]+r'''
          _=pm;state.selectedPoint=12395;state.paused=true;state.timeScale=21600;state.showEscapeMenu=false;state.showPointDetails=false;state.showPlanetControl=false;
          state.pointerOnPlanet=true;std.debug.assert(state.testAction(2));state.pointerOnPlanet=false;
          const expected:i32=12395;const world=PerformanceDetails.world_serial;
          const frozen=try std.json.stringifyAlloc(a,try saves.capture(a,state),.{});
          const prior=pw.current;
          std.debug.assert(patchWatchStartCheckedForState(state,expected,world+%1,true)==-2);
          std.debug.assert(patchWatchStartCheckedForState(state,expected+1,world,true)==-2);
          std.debug.assert(patchWatchStartCheckedForState(state,expected,world,false)==-2);
          std.debug.assert(state.paused and state.timeScale==21600 and std.meta.eql(prior,pw.current));
          std.debug.assert(std.mem.eql(u8,frozen,try std.json.stringifyAlloc(a,try saves.capture(a,state),.{})));
          std.debug.assert(patchWatchStartCheckedForState(state,expected,world,true)==1);
          std.debug.assert(!state.paused and state.timeScale==21600);
          const population=pw.Watch.population(state.planet.microbeCells[12395].cohorts).?;
          std.debug.assert(pw.current.start_biomass==population.biomass and pw.current.start_colonies==population.colonies and std.meta.eql(pw.current.start_members,population.members));
          var changed=try saves.capture(a,state);changed.paused=true;std.debug.assert(std.mem.eql(u8,frozen,try std.json.stringifyAlloc(a,changed,.{})));
          const running=try std.json.stringifyAlloc(a,try saves.capture(a,state),.{});
          std.debug.assert(patchWatchStartCheckedForState(state,expected,world,false)==1);
          std.debug.assert(std.mem.eql(u8,running,try std.json.stringifyAlloc(a,try saves.capture(a,state),.{})));
          state.paused=true;const old_watch=pw.current;const old_mass=state.planet.microbeCells[12395].cohorts[0].biomass;
          state.planet.microbeCells[12395].cohorts[0].biomass=std.math.nan(f32);
          std.debug.assert(patchWatchStartCheckedForState(state,expected,world,true)==-3);
          std.debug.assert(state.paused and state.timeScale==21600 and std.meta.eql(old_watch,pw.current));
          state.planet.microbeCells[12395].cohorts[0].biomass=old_mass;
          std.debug.assert(std.mem.eql(u8,frozen,try std.json.stringifyAlloc(a,try saves.capture(a,state),.{})));
          std.debug.print("CHECKED_WATCH actual_postwater_baseline=true stale_world_selection_unchanged=true paused_normal_refused=true explicit_resume_only_pause_changed=true running_start_save_exact=true invalid_population_pause_watch_rollback=true controlled_invalid_mass_restored=true world={d} biomass={d} colonies={d}\n",.{world,population.biomass,population.colonies});
        }
''' +s[end:];p.write_text(s)
