#!/usr/bin/env python3
from pathlib import Path
import subprocess,sys
r=Path(__file__).resolve().parents[2];o=Path(sys.argv[1]).resolve()
subprocess.run([sys.executable,str(r/'web/tests/egl-sunlit-journey-prepare.py'),str(o)],check=True)
p=o/'main.zig';s=p.read_text();a=s.index('          _=pm;_=pw;');b=s.index('\n        std.debug.print("SUNLIT_PUBLIC_PASS',a)
s=s[:a]+r'''
          _=pm;_=pw;state.paused=true;state.showEscapeMenu=false;state.showPointDetails=false;state.showPlanetControl=false;state.selectedPoint=40249;state.displayMode=.Normal;
          const frozen=try std.json.stringifyAlloc(a,try saves.capture(a,state),.{});
          const baseline=try std.json.parseFromSlice(saves.schema.Save,a,frozen,.{.allocate=.alloc_always});
          const world=PerformanceDetails.world_serial;const pace=state.timeScale;const time=state.gameTime;
          for(0..4)|case|{
            state.selectedPoint=40249;
            std.debug.assert(stella_find_offspring(1,world,40249,"4")==2);
            if(case==0){_=stella_find_offspring(2,world,40249,"4");std.debug.assert(stella_find_offspring(0,world,40249,"4")==-4);}
            if(case==1)std.debug.assert(stella_find_offspring(0,world+1,40249,"4")==-4);
            if(case==2){state.selectedPoint=40248;std.debug.assert(stella_find_offspring(0,world,40249,"4")==-4);}
            if(case==3){var slot:usize=0;for(state.planet.microbeCells[40249].cohorts,0..)|co,i|if(co.lineage==4){slot=i;};const old=state.planet.microbeCells[40249].cohorts[slot];state.planet.microbeCells[40249].cohorts[slot]=.{};std.debug.assert(stella_find_offspring(0,world,40249,"4")==-4);state.planet.microbeCells[40249].cohorts[slot]=old;}
            std.debug.assert(std.mem.eql(u8,frozen,try std.json.stringifyAlloc(a,try saves.capture(a,state),.{})));
          }
          state.selectedPoint=40249;std.debug.assert(stella_find_offspring(1,world,40249,"4")==2);
          try saves.apply(state,baseline.value);state.selectedPoint=40249;
          std.debug.assert(stella_find_offspring(0,PerformanceDetails.world_serial,40249,"4")==-4);
          var result=stella_find_offspring(1,PerformanceDetails.world_serial,40249,"4");var chunks:usize=1;
          while(result==2){std.debug.assert(chunks<100);std.debug.assert(std.mem.eql(u8,frozen,try std.json.stringifyAlloc(a,try saves.capture(a,state),.{})));result=stella_find_offspring(0,PerformanceDetails.world_serial,40249,"4");chunks+=1;}
          std.debug.assert(result==1 and chunks>1 and state.selectedPoint==10071);
          var child=false;for(state.planet.microbeCells[10071].cohorts)|co|{if(co.biomass>0 and co.parent==4 and co.lineage==80)child=true;}std.debug.assert(child);
          state.update(&game,0);render(window);gl.finish();window.swapBuffers();
          var picked=false;for(state.colonyTargets.items[0..state.colonyTargets.count])|hit|{if(hit.cell==10071){qa_pointer(hit.x,hit.y,0);state.mousePressed(&game,.left);std.debug.assert(state.selectedPoint==10071 and state.colonyPeek.cell.?==10071);picked=true;break;}}std.debug.assert(picked);
          const snap=try std.json.parseFromSlice(std.json.Value,a,std.mem.span(stella_life_snapshot()),.{.allocate=.alloc_always});std.debug.assert(snap.value.object.get("cell").?.integer==10071);
          var after=try saves.capture(a,state);after.camera=baseline.value.camera;after.camera_target=baseline.value.camera_target;after.camera_distance=baseline.value.camera_distance;after.target_distance=baseline.value.target_distance;
          std.debug.assert(std.mem.eql(u8,frozen,try std.json.stringifyAlloc(a,after,.{})));
          std.debug.assert(state.paused and state.timeScale==pace and state.gameTime==time);
          qa_capture("OUTPUT/final.ppm");
          std.debug.print("OFFSPRING_PASS chunks={d} parent=4 source=40249 child=80 target=10071 render_pick=true frozen_model_rng_exact=true stale_cancel_load=true\n",.{chunks});
        }
''' .replace('OUTPUT',str(o.parent))+s[b:]
s=s.replace('SUNLIT_PUBLIC_PASS complete=true original_restored=true explicit_qa_exit=true','OFFSPRING_EXIT complete=true camera_normalized_model_exact=true explicit_qa_exit=true');p.write_text(s)
subprocess.run([sys.executable,str(r/'web/tests/audit-zig-exports.py'),str(r/'src/main.zig'),str(p)],check=True,stdout=(o.parent/'export-audit-final.json').open('w'))
