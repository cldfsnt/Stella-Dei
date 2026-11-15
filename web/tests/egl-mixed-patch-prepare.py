#!/usr/bin/env python3
from pathlib import Path
import subprocess,sys
root=Path(__file__).resolve().parents[2];out=Path(sys.argv[1])
subprocess.run([sys.executable,str(root/'web/tests/egl-ecology-pulse-prepare.py'),str(out)],check=True)
p=out/'main.zig';s=p.read_text();a=s.index('          var found=state.findRecordedFeeding(true);');b=s.index('\n        try originSaveCheck',a)
s=s[:a]+r'''
          const cell:usize=13594;state.selectedPoint=cell;
          for(0..2)|window_index|{
            const frozen=try std.json.stringifyAlloc(a,try saves.capture(a,state),.{});
            const baseline=try std.json.parseFromSlice(saves.schema.Save,a,frozen,.{.allocate=.alloc_always});
            try saves.apply(state,baseline.value);state.selectedPoint=cell;state.paused=false;
            pm.qa_watch_cell=cell;pm.qa_flux=0;pm.qa_fixed=0;pm.qa_recycled=0;
            std.debug.print("MIXED_START window={d} time={d} water={d} temperature={d} nutrient={d}\n",.{window_index,state.gameTime,state.planet.waterMass[cell],state.planet.temperature[cell],state.planet.microbeCells[cell].nutrient});
            for(state.planet.microbeCells[cell].cohorts)|co|if(co.biomass>0){std.debug.print("MIXED_TRAIT window={d} id={d} biomass={d} efficiency={d} feeding={d} organization={d} support={d} structure={d} optimum={d}\n",.{window_index,co.lineage,co.biomass,co.efficiency,co.feeding,co.organization,co.support_mass,co.structure,co.optimum});};
            std.debug.assert(patchWatchStartForState(state,@intCast(cell))==1);
            for(0..60)|_|{state.planet.simulate(game.loop,.{.dt=1440,.timeScale=1,.solarConstant=state.solarConstant,.gameTime=state.gameTime,.planetRotationTime=state.planetRotationTime,.solarVector=state.simulationSolarVector()});state.gameTime+=1440;}
            const watched=pw.current;std.debug.assert(watched.ticks==60 and watched.elapsed==86400);
            std.debug.assert(watched.consumed==pm.qa_flux and watched.fixed==pm.qa_fixed and watched.recycled==pm.qa_recycled);
            const endpoint=pw.Watch.population(state.planet.microbeCells[cell].cohorts).?;std.debug.assert(std.meta.eql(endpoint.members,watched.end_members));
            std.debug.print("MIXED_RESULT window={d} snapshot={s}\n",.{window_index,try std.json.stringifyAlloc(a,.{.start_members=watched.start_members.entries[0..watched.start_members.len],.end_members=watched.end_members.entries[0..watched.end_members.len],.elapsed=watched.elapsed,.fixed=watched.fixed,.recycled=watched.recycled,.consumed=watched.consumed},.{})});
            std.debug.print("MIXED_END window={d} time={d} water={d} temperature={d} nutrient={d}\n",.{window_index,state.gameTime,state.planet.waterMass[cell],state.planet.temperature[cell],state.planet.microbeCells[cell].nutrient});
            const observed_save=try std.json.stringifyAlloc(a,try saves.capture(a,state),.{});
            try saves.apply(state,baseline.value);state.selectedPoint=cell;state.paused=false;
            for(0..60)|_|{state.planet.simulate(game.loop,.{.dt=1440,.timeScale=1,.solarConstant=state.solarConstant,.gameTime=state.gameTime,.planetRotationTime=state.planetRotationTime,.solarVector=state.simulationSolarVector()});state.gameTime+=1440;}
            const unobserved=try std.json.stringifyAlloc(a,try saves.capture(a,state),.{});std.debug.assert(std.mem.eql(u8,observed_save,unobserved));
            std.debug.print("MIXED_PARITY window={d} full_saved_world_exact=true\n",.{window_index});
          }
        }
''' +s[b:];p.write_text(s)
