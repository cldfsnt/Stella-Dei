#!/usr/bin/env python3
"""Display-only actual native same-world near/globe marker comparison."""
from pathlib import Path
import subprocess,sys,shutil,json,hashlib
r=Path(__file__).resolve().parents[2];o=Path(sys.argv[1]).resolve()
subprocess.run([sys.executable,str(r/'web/tests/egl-sandbox-find-prepare.py'),str(o)],check=True)
shutil.copy2(r/'src/experimental/rabbit_marker_scale.zig',o/'rabbit_marker_scale.zig')
p=o/'states/play.zig';s=p.read_text();a=s.index('        for (self.planet.lifeforms.items) |lifeform| {',s.index('    fn renderMobileUI'));b=s.index('        vg.beginPath();\n        vg.fillColor(nvg.rgba(8, 15, 28, 225));',a)
block=s[a:b];assert 'x - 6, y - 6, 12, 12, 6' in block
block=block.replace('            vg.beginPath();', '            qaRabbitMarkers+=1;\n            vg.beginPath();',1)
block=block.replace('x - 6, y - 6, 12, 12, 6','x - 6*marker_scale, y - 6*marker_scale, 12*marker_scale, 12*marker_scale, 6*marker_scale').replace('x - 2, y - 2, 4, 4, 2','x - 2*marker_scale, y - 2*marker_scale, 4*marker_scale, 4*marker_scale, 2*marker_scale')
s=s[:a]+'        qaRabbitMarkers=0;\n        const marker_scale=if(qaScaleRabbitMarkers)@import("../rabbit_marker_scale.zig").scale(self.cameraDistance,self.planet.radius) else 1;\n'+block+s[b:]
s=s.replace('    fn renderMobileUI(', '    pub var qaRabbitMarkers:usize=0;\n    pub var qaScaleRabbitMarkers:bool=true;\n    fn renderMobileUI(',1);p.write_text(s)
p=o/'main.zig';s=p.read_text();a=s.index('          _=pm;_=pw;');b=s.index('\n        std.debug.print("FORAGING_PRODUCTION_COMPLETE',a)
s=s[:a]+r'''
          _=pm;_=pw;std.debug.assert(state.planet.worldMode==.sandbox);
          const original=try std.json.stringifyAlloc(a,try saves.capture(a,state),.{});const initial=try std.json.parseFromSlice(saves.schema.Save,a,original,.{.allocate=.alloc_always});
          std.debug.assert(stella_find_sandbox_life(0)==1);const center=state.selectedPoint;
          for(0..3)|view|for(0..2)|variant|{
            try saves.apply(state,initial.value);@TypeOf(state.*).qaScaleRabbitMarkers=variant==1;
            state.paused=true;state.selectedTool=.None;state.showEscapeMenu=false;state.showPointDetails=false;state.showPlanetControl=false;
            state.selectedPoint=center;state.clickedPoint=center;state.cameraGroundPoint=center;
            const point=state.planet.transformedPoints[center];const distance=if(view==0)point.length()+200 else state.planet.radius*2.0;
            state.cameraPos=point.norm().scale(distance);state.targetCameraPos=state.cameraPos;state.cameraDistance=distance;state.targetCameraDistance=distance;
            if(view==2)std.debug.assert(stella_find_sandbox_life(1)==1);
            const before=try saves.capture(a,state);const frozen=try std.json.stringifyAlloc(a,before,.{});
            render(window);gl.finish();window.swapBuffers();qa_capture(try std.fmt.allocPrintZ(a,"OUTPUT/{s}-{d}.ppm",.{if(view==0)"close"else if(view==1)"globe"else"rabbit-close",variant}));
            var after=try saves.capture(a,state);after.camera=before.camera;after.camera_target=before.camera_target;after.camera_distance=before.camera_distance;after.target_distance=before.target_distance;
            std.debug.assert(std.mem.eql(u8,frozen,try std.json.stringifyAlloc(a,after,.{})));
            std.debug.assert(state.visibleSprouts>0 and state.visibleSprouts<=64);
            if(view==2)std.debug.assert(@TypeOf(state.*).qaRabbitMarkers>0 and @import("rabbit_marker_scale.zig").scale(state.cameraDistance,state.planet.radius)==1);
            std.debug.print("RABBIT_MARKER drawn={} view={} candidate={} scale={d} plants={} rabbits={} full_non_camera_save_rng_exact=true\n",.{@TypeOf(state.*).qaRabbitMarkers,view,variant,@import("rabbit_marker_scale.zig").scale(distance,state.planet.radius),state.visibleSprouts,state.planet.lifeforms.items.len});
          };
          try saves.apply(state,initial.value);std.debug.assert(stella_find_sandbox_life(1)==1);std.debug.assert(state.selectedTool==.None);
          var found=try saves.capture(a,state);found.camera=initial.value.camera;found.camera_target=initial.value.camera_target;found.camera_distance=initial.value.camera_distance;found.target_distance=initial.value.target_distance;found.display_mode=initial.value.display_mode;
          std.debug.assert(std.mem.eql(u8,original,try std.json.stringifyAlloc(a,found,.{})));
          try saves.apply(state,initial.value);std.debug.assert(std.mem.eql(u8,original,try std.json.stringifyAlloc(a,try saves.capture(a,state),.{})));
          std.debug.print("RABBIT_MARKER_PASS finder_exact_model=true original_restored=true no_simulation=true\n",.{});
        }
'''.replace('OUTPUT',str(o.parent))+s[b:];p.write_text(s)
(o.parent/'source-provenance.json').write_text(json.dumps({'head':subprocess.check_output(['git','rev-parse','HEAD'],cwd=r,text=True).strip(),'source':{f:hashlib.sha256((o/f).read_bytes()).hexdigest()for f in ['states/play.zig','rabbit_marker_scale.zig','main.zig']},'production_files_edited':False},indent=2)+'\n')
