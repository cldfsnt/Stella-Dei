#!/usr/bin/env python3
"""Actual day60 naturally shallow mixed-patch dry pulse and optional single rescue."""
from pathlib import Path
import subprocess,sys
root=Path(__file__).resolve().parents[2];out=Path(sys.argv[1])
subprocess.run([sys.executable,str(root/'web/tests/egl-water-paired-prepare.py'),str(out)],check=True)
p=out/'main.zig';s=p.read_text();s=s.replace('const cell:usize=13594','const cell:usize=12395').replace('for(0..2)|branch|','for(0..3)|branch|').replace('std.debug.assert(depth>1 and','std.debug.assert(depth>0 and depth<0.2 and').replace('if(branch==1)','if(branch>0)').replace('changed==branch','changed==@as(usize,if(branch>0) 1 else 0)').replace('for(0..60)|tick|','for(0..180)|tick|').replace('if(tick==14 or tick==59)','if(tick==0 or tick==2 or tick==14 or tick==59 or tick==179)')
needle='''                render(window);gl.finish();window.swapBuffers();
              }
            }
          }
'''
assert needle in s
s=s.replace(needle,r'''                render(window);gl.finish();window.swapBuffers();
              }
              if(branch==2 and tick==14){
                const frozen_rescue=try std.json.stringifyAlloc(a,try saves.capture(a,state),.{});const parsed_rescue=try std.json.parseFromSlice(saves.schema.Save,a,frozen_rescue,.{.allocate=.alloc_always});
                const previous=state.planet.waterMass[cell];const delta=state.setSelectedWaterTarget(@intCast(cell),0.5);std.debug.assert(std.math.isFinite(delta));
                var rescued=try saves.capture(a,state);var changed_count:usize=0;for(parsed_rescue.value.water,rescued.water,0..)|b,c,i|if(b!=c){std.debug.assert(i==cell);changed_count+=1;};rescued.water=parsed_rescue.value.water;
                std.debug.assert(std.mem.eql(u8,frozen_rescue,try std.json.stringifyAlloc(a,rescued,.{})));
                std.debug.print("SHALLOW_RESCUE hours=6 target_m=0.5 depth_m={d} external_water_units={d} changed_patches={d} nonwater_save_exact=true feedback={s}\n",.{state.planet.waterMass[cell]*state.planet.getKmPerWaterMass()*1000,@as(f64,state.planet.waterMass[cell])-previous,changed_count,state.mobileFeedback});
                render(window);gl.finish();window.swapBuffers();
              }
            }
          }
''')
s=s.replace('                render(window);gl.finish();window.swapBuffers();\n              }', '                std.debug.print("SHALLOW_COHORTS branch={d} tick={d} cells={s}\\n",.{branch,tick+1,try std.json.stringifyAlloc(a,state.planet.microbeCells[cell],.{})});\n                render(window);gl.finish();window.swapBuffers();\n              }')
s=s.replace('            const before_bytes=', '            var global_start:f64=0;for(state.planet.waterMass,state.planet.waterVaporMass)|liquid,vapor|global_start+=@as(f64,liquid)+@as(f64,vapor);std.debug.print("SHALLOW_GLOBAL_START branch={d} liquid_vapor_units={d}\\n",.{branch,global_start});\n            const before_bytes=')
s=s.replace('                std.debug.print("SHALLOW_COHORTS', '                var global_water:f64=0;for(state.planet.waterMass,state.planet.waterVaporMass)|liquid,vapor|global_water+=@as(f64,liquid)+@as(f64,vapor);std.debug.print("SHALLOW_GLOBAL branch={d} tick={d} liquid_vapor_units={d}\\n",.{branch,tick+1,global_water});\n                std.debug.print("SHALLOW_COHORTS')
s=s.replace('                render(window);gl.finish();window.swapBuffers();\n              }', '                render(window);gl.finish();window.swapBuffers();const shot=try std.fmt.allocPrintZ(a,"/workspace/scratch/f67c3ac60ca3/site-tmp/shallow-recovery/branch-{d}-tick-{d}.ppm",.{branch,tick+1});qa_capture(shot);\n              }')
s=s.replace('WATER_PAIRED','SHALLOW').replace('SHALLOW_RESCUE','SHALLOW_REWATER');p.write_text(s)
