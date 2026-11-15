#!/usr/bin/env python3
"""Read-only actual fire-discovery audit; no water or fuel assignment."""
from pathlib import Path
import subprocess,sys
r=Path(__file__).resolve().parents[2];o=Path(sys.argv[1]).resolve();subprocess.run([sys.executable,str(r/'web/tests/egl-arrival-toggle-prepare.py'),str(o)],check=True)
p=o/'main.zig';s=p.read_text();a=s.index('          _=pm;_=pw;');b=s.index('\n        std.debug.print("ARRIVAL_TOGGLE_COMPLETE',a)
s=s[:a]+r'''
          _=pm;_=pw;state.paused=true;state.showEscapeMenu=false;
          const before=try std.json.stringifyAlloc(a,try saves.capture(a,state),.{});const saved=try std.json.parseFromSlice(saves.schema.Save,a,before,.{.allocate=.alloc_always});
          var best:?usize=null;var best_depth:f32=std.math.inf(f32);var dry:usize=0;var wet:usize=0;const conv=state.planet.getKmPerWaterMass()*1000;
          for(state.planet.microbeCells,0..)|cell,i|{const point=state.planet.transformedPoints[i];const length=point.length();if(cell.detritus<=0 or !std.math.isFinite(length) or length<=0 or @abs(point.norm().z())>0.95)continue;
            const depth=state.planet.waterMass[i]*conv;if(depth==0){dry+=1;}else{wet+=1;if(depth<best_depth){best_depth=depth;best=i;}}
          }
          var result=state.findDetritus(true);var chunks:usize=1;while(result==2):(chunks+=1){result=state.findDetritus(false);}
          const selected=state.selectedPoint;const selected_depth=state.planet.waterMass[selected]*conv;
          // Finder intentionally changes view only. Restore its documented camera fields for exact biology/save comparison.
          const after=try saves.capture(a,state);var check=after;check.camera=saved.value.camera;check.camera_target=saved.value.camera_target;check.camera_distance=saved.value.camera_distance;check.target_distance=saved.value.target_distance;check.display_mode=saved.value.display_mode;
          std.debug.assert(std.mem.eql(u8,before,try std.json.stringifyAlloc(a,check,.{})));
          std.debug.print("FIRE_ROUTE_AUDIT result={} chunks={} dry_fuel={} wet_fuel={} selected={} selected_depth_m={d} selected_fuel={d} selected_taps={d} shallowest={} shallow_depth_m={d} shallow_fuel={d} shallow_taps={d} saved_biology_rng_exact=true\n",.{result,chunks,dry,wet,selected,selected_depth,state.planet.microbeCells[selected].detritus,@ceil(selected_depth),best.?,best_depth,state.planet.microbeCells[best.?].detritus,@ceil(best_depth)});
          try saves.apply(state,saved.value);std.debug.assert(std.mem.eql(u8,before,try std.json.stringifyAlloc(a,try saves.capture(a,state),.{})));
        }
'''+s[b:];p.write_text(s.replace('ARRIVAL_TOGGLE_COMPLETE','FIRE_ROUTE_COMPLETE'))
