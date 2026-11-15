#!/usr/bin/env python3
"""Isolated prescribed phenotype rendering only; never edits production or simulates."""
from pathlib import Path
import subprocess,sys,hashlib,json
r=Path(__file__).resolve().parents[2];o=Path(sys.argv[1]).resolve()
subprocess.run([sys.executable,str(r/'web/tests/egl-sandbox-find-prepare.py'),str(o)],check=True)
p=o/'simulation/ecology.zig';s=p.read_text();assert 'toughness:' not in s;s=s.replace('pub const Plant = struct {','pub const Plant = struct {\n    toughness:f32=0,');p.write_text(s)
p=o/'states/play.zig';s=p.read_text();needle='renderProducerGlyph(vg,"branching",color);';assert s.count(needle)==1
s=s.replace(needle,'if(qaToughnessVisual)renderToughnessGlyph(vg,self.planet.plantTraits[index].toughness,color) else renderProducerGlyph(vg,"branching",color);')
a=s.index('    fn renderProducerGlyph(')
helper='''    pub var qaToughnessVisual:bool=true;
    // Prescribed handling-resistance illustration, not a new plant species.
    // Identical path/draw budget: stem, three paired leaves, one highlight.
    fn renderToughnessGlyph(vg:nvg,d:f32,color:[3]u8) void {
        if(d<=0 or !std.math.isFinite(d)){renderProducerGlyph(vg,"branching",color);return;}
        const t=std.math.clamp(d*2,0,1);
        const edge=nvg.rgb(12,49,44);
        vg.strokeColor(edge);vg.strokeWidth(2.2);vg.fillColor(nvg.rgb(color[0],color[1],color[2]));
        vg.beginPath();vg.moveTo(0,0);vg.lineTo(0,-32);vg.strokeColor(edge);vg.strokeWidth(4);vg.stroke();
        var i:usize=0;while(i<3):(i+=1){
            const y=-8-@as(f32,@floatFromInt(i))*8;
            const w=(13-@as(f32,@floatFromInt(i))*3)*(0.55+0.45*t);
            const h=2+6*t;
            vg.strokeWidth(2);vg.beginPath();vg.moveTo(0,y+4);
            vg.bezierTo(-w,y+4,-w-3,y+3,-w,y-h);
            vg.bezierTo(-w+2,y-h,-1,y,0,y+4);
            vg.moveTo(0,y);vg.bezierTo(w,y,w+3,y-1,w,y-h-4);
            vg.bezierTo(w-2,y-h-4,1,y-4,0,y);vg.fill();vg.stroke();
        }
        vg.beginPath();vg.fillColor(nvg.rgba(230,255,223,220));vg.circle(-3,-12,1.7);vg.fill();
    }

'''
s=s[:a]+helper+s[a:];p.write_text(s)
p=o/'main.zig';s=p.read_text();a=s.index('          _=pm;_=pw;');b=s.index('\n        std.debug.print("FORAGING_PRODUCTION_COMPLETE',a)
s=s[:a]+r'''
          _=pm;_=pw;std.debug.assert(state.planet.worldMode==.sandbox);
          const original=try std.json.stringifyAlloc(a,try saves.capture(a,state),.{});
          const initial=try std.json.parseFromSlice(saves.schema.Save,a,original,.{.allocate=.alloc_always});
          std.debug.assert(stella_find_sandbox_life(0)==1);const center=state.selectedPoint;
          for(0..2)|view|{
            for(0..4)|variant|{
              try saves.apply(state,initial.value);
              for(state.planet.plantTraits)|*plant|plant.toughness=if(variant<2)0 else if(variant==2)0.25 else 0.5;
              @TypeOf(state.*).qaToughnessVisual=variant!=0;
              state.paused=true;state.selectedTool=.None;state.showEscapeMenu=false;state.showPointDetails=false;state.showPlanetControl=false;
              state.selectedPoint=center;state.clickedPoint=center;state.cameraGroundPoint=center;
              const point=state.planet.transformedPoints[center];const distance=if(view==0)point.length()+200 else state.planet.radius*2.0;
              state.cameraPos=point.norm().scale(distance);state.targetCameraPos=state.cameraPos;state.cameraDistance=distance;state.targetCameraDistance=distance;
              const before=try saves.capture(a,state);const frozen=try std.json.stringifyAlloc(a,before,.{});
              render(window);gl.finish();window.swapBuffers();
              const name=try std.fmt.allocPrintZ(a,"OUTPUT/{s}-{d}.ppm",.{if(view==0)"close"else"globe",variant});qa_capture(name);
              var after=try saves.capture(a,state);after.camera=before.camera;after.camera_target=before.camera_target;after.camera_distance=before.camera_distance;after.target_distance=before.target_distance;
              std.debug.assert(std.mem.eql(u8,frozen,try std.json.stringifyAlloc(a,after,.{})));
              std.debug.assert(state.visibleSprouts>0 and state.visibleSprouts<=64);
              std.debug.print("TOUGH_VISUAL view={} variant={} d={d} visible={} center={} full_non_camera_save_rng_exact=true\n",.{view,variant,state.planet.plantTraits[center].toughness,state.visibleSprouts,center});
            }
          }
          try saves.apply(state,initial.value);std.debug.assert(std.mem.eql(u8,original,try std.json.stringifyAlloc(a,try saves.capture(a,state),.{})));
          std.debug.print("TOUGH_VISUAL_PASS no_simulation=true prescribed_traits=true original_restored=true\n",.{});
        }
'''.replace('OUTPUT',str(o.parent))+s[b:];p.write_text(s)
(o.parent/'visual-provenance.json').write_text(json.dumps({'head':subprocess.check_output(['git','rev-parse','HEAD'],cwd=r,text=True).strip(),'source':{f:hashlib.sha256((o/f).read_bytes()).hexdigest()for f in ['simulation/ecology.zig','states/play.zig','main.zig']},'scope':'isolated render only, prescribed traits, no biology candidate or schema promotion'},indent=2)+'\n')
