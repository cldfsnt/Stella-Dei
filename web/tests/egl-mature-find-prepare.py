#!/usr/bin/env python3
from pathlib import Path
import subprocess,sys
root=Path(__file__).resolve().parents[2];out=Path(sys.argv[1])
subprocess.run([sys.executable,str(root/'web/tests/egl-ecology-pulse-prepare.py'),str(out)],check=True)
p=out/'main.zig';s=p.read_text();start=s.index('          var found=state.findRecordedFeeding(true);');end=s.index('\n        try originSaveCheck',start)
s=s[:start]+r'''
          _=pw;_=pm;const M=@import("simulation/microbes.zig");
          const frozen=try std.json.stringifyAlloc(a,try saves.capture(a,state),.{});const baseline=try std.json.parseFromSlice(saves.schema.Save,a,frozen,.{.allocate=.alloc_always});
          for(0..2)|branch|{
            try saves.apply(state,baseline.value);state.selectedPoint=13594;std.debug.assert(M.biomass(state.planet.microbeCells[13594])==0);state.paused=true;state.timeScale=86400;state.watchLife();
            state.targetCameraPos=state.planet.transformedPoints[13594].norm().scale(5300);state.cameraPos=state.targetCameraPos;state.cameraDistance=5300;state.targetCameraDistance=5300;
            render(window);gl.finish();window.swapBuffers();
            const beforeBytes=try std.json.stringifyAlloc(a,try saves.capture(a,state),.{});const beforeParsed=try std.json.parseFromSlice(saves.schema.Save,a,beforeBytes,.{.allocate=.alloc_always});const before=beforeParsed.value;
            const result=if(branch==0)state.fitLivingClusterResult(390,700) else state.findLivingClusterResult(390,700);
            const after=try saves.capture(a,state);var normalized=after;normalized.camera=before.camera;normalized.camera_target=before.camera_target;normalized.camera_distance=before.camera_distance;normalized.target_distance=before.target_distance;
            std.debug.assert(std.mem.eql(u8,try std.json.stringifyAlloc(a,before,.{}),try std.json.stringifyAlloc(a,normalized,.{})));
            render(window);gl.finish();window.swapBuffers();
            std.debug.print("MATURE_FIND branch={d} result={d} selected={d} selected_mass={d} rendered={d} targets={d} paused={} pace={d} time={d} feedback={s} deep_non_camera_save_exact=true\n",.{branch,result,state.selectedPoint,M.biomass(state.planet.microbeCells[state.selectedPoint]),state.visibleSprouts,state.colonyTargets.count,state.paused,state.timeScale,state.gameTime,state.mobileFeedback});
            if(branch==1 and state.colonyTargets.count>0){const target=state.colonyTargets.items[0];qa_pointer(target.x,target.y,0);state.mousePressed(&game,.left);
              std.debug.assert(state.selectedPoint==target.cell and M.biomass(state.planet.microbeCells[target.cell])>0);
              var picked=try saves.capture(a,state);picked.camera=before.camera;picked.camera_target=before.camera_target;picked.camera_distance=before.camera_distance;picked.target_distance=before.target_distance;
              std.debug.assert(std.mem.eql(u8,try std.json.stringifyAlloc(a,before,.{}),try std.json.stringifyAlloc(a,picked,.{})));
              render(window);gl.finish();window.swapBuffers();
              std.debug.print("MATURE_PICK selected={d} biomass={d} visible_glyph_pick=true deep_non_camera_save_exact=true\n",.{target.cell,M.biomass(state.planet.microbeCells[target.cell])});
            }
          }
          try saves.apply(state,baseline.value);std.debug.assert(std.mem.eql(u8,frozen,try std.json.stringifyAlloc(a,try saves.capture(a,state),.{})));
        }
''' +s[end:];p.write_text(s)
