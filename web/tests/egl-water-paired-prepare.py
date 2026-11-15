#!/usr/bin/env python3
"""Actual earned mixed-patch world, one real water tap vs matched no-action."""
from pathlib import Path
import subprocess,sys
root=Path(__file__).resolve().parents[2];out=Path(sys.argv[1])
subprocess.run([sys.executable,str(root/'web/tests/egl-ecology-pulse-prepare.py'),str(out)],check=True)
p=out/'main.zig';s=p.read_text();start=s.index('          var found=state.findRecordedFeeding(true);');end=s.index('\n        try originSaveCheck',start)
s=s[:start]+r'''
          const cell:usize=13594;const M=@import("simulation/microbes.zig");
          const frozen=try std.json.stringifyAlloc(a,try saves.capture(a,state),.{});
          const baseline=try std.json.parseFromSlice(saves.schema.Save,a,frozen,.{.allocate=.alloc_always});
          for(0..2)|branch|{
            try saves.apply(state,baseline.value);state.selectedPoint=cell;state.paused=true;state.timeScale=86400;state.watchLife();
            state.targetCameraPos=state.planet.transformedPoints[cell];_=state.fitLivingClusterResult(390,700);
            const before_bytes=try std.json.stringifyAlloc(a,try saves.capture(a,state),.{});const before_parsed=try std.json.parseFromSlice(saves.schema.Save,a,before_bytes,.{.allocate=.alloc_always});const before=before_parsed.value;const wm=state.planet.waterMass[cell];const depth=wm*state.planet.getKmPerWaterMass()*1000;
            std.debug.assert(depth>1 and M.biomass(state.planet.microbeCells[cell])>0);
            render(window);gl.finish();window.swapBuffers();
            if(branch==1){state.pointerOnPlanet=true;std.debug.assert(state.testAction(2));state.pointerOnPlanet=false;}
            if(branch==1){const feedback_before=try a.dupe(u8,state.mobileFeedback);const feedback_seconds=state.mobileFeedbackSeconds;
              var invalid=try saves.capture(a,state);invalid.version=999;
              if(saves.apply(state,invalid)) |_| {unreachable;} else |_| {}
              std.debug.assert(std.mem.eql(u8,feedback_before,state.mobileFeedback) and feedback_seconds==state.mobileFeedbackSeconds);
              std.debug.print("WATER_FAILED_LOAD feedback_unchanged=true\n",.{});
            }
            const after=try saves.capture(a,state);var normalized=after;normalized.water=before.water;
            std.debug.assert(std.mem.eql(u8,try std.json.stringifyAlloc(a,before,.{}),try std.json.stringifyAlloc(a,normalized,.{})));
            var changed:usize=0;var removed:f64=0;for(before.water,after.water,0..)|b,c,i|{if(b!=c){changed+=1;std.debug.assert(i==cell);}removed+=@as(f64,b)-@as(f64,c);}
            std.debug.assert(changed==branch and removed>=0);
            std.debug.print("WATER_PAIRED_ACTION branch={d} patch={d} initial_depth_m={d} final_depth_m={d} removed_mass_units={d} removed_kg={d} changed_patches={d} all_nonwater_save_exact=true feedback={s}\n",.{branch,cell,depth,state.planet.waterMass[cell]*state.planet.getKmPerWaterMass()*1000,removed,removed*1e9,changed,state.mobileFeedback});
            render(window);gl.finish();window.swapBuffers();
            state.paused=false;pm.qa_watch_cell=cell;pm.qa_flux=0;pm.qa_fixed=0;pm.qa_recycled=0;std.debug.assert(patchWatchStartForState(state,@intCast(cell))==1);
            for(0..60)|tick|{
              state.planet.simulate(game.loop,.{.dt=1440,.timeScale=1,.solarConstant=state.solarConstant,.gameTime=state.gameTime,.planetRotationTime=state.planetRotationTime,.solarVector=state.simulationSolarVector()});state.gameTime+=1440;
              if(tick==14 or tick==59){const c=state.planet.microbeCells[cell];std.debug.assert(M.validCell(c,state.planet.microbeStats.next_lineage));
                std.debug.print("WATER_PAIRED_FATE branch={d} hours={d} depth_m={d} temperature_K={d} biomass={d} nutrient={d} detritus={d} fixed={d} recycled={d} grazed={d} members={s}\n",.{branch,(tick+1)*1440/3600,state.planet.waterMass[cell]*state.planet.getKmPerWaterMass()*1000,state.planet.temperature[cell],M.biomass(c),c.nutrient,c.detritus,pm.qa_fixed,pm.qa_recycled,pm.qa_flux,try std.json.stringifyAlloc(a,pw.Watch.population(c.cohorts).?.members,.{})});
                render(window);gl.finish();window.swapBuffers();
              }
            }
          }
          try saves.apply(state,baseline.value);std.debug.assert(std.mem.eql(u8,frozen,try std.json.stringifyAlloc(a,try saves.capture(a,state),.{})));
          std.debug.assert(state.mobileFeedback.len==0 and state.mobileFeedbackSeconds==0);
          std.debug.print("WATER_LOADED_WORLD feedback_cleared=true\n",.{});
          std.debug.print("WATER_PAIRED_RESTORE exact=true organism_injection=false no_extra_care=true\n",.{});
        }
''' +s[end:];p.write_text(s)
