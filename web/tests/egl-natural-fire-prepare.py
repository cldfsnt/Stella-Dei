#!/usr/bin/env python3
"""Naturally earned shallow fuel, actual UI exports, untouched/drain/burn arms."""
from pathlib import Path
import subprocess,sys
root=Path(__file__).resolve().parents[2];out=Path(sys.argv[1])
subprocess.run([sys.executable,str(root/'web/tests/egl-water-paired-prepare.py'),str(out)],check=True)
p=out/'main.zig';s=p.read_text().replace('const cell:usize=13594','const cell:usize=12395').replace('for(0..2)|branch|','for(0..3)|branch|').replace('std.debug.assert(depth>1 and','std.debug.assert(depth>0 and depth<0.2 and').replace('if(branch==1)','if(branch>0)').replace('changed==branch','changed==@as(usize,if(branch>0) 1 else 0)').replace('for(0..60)|tick|','for(0..180)|tick|').replace('if(tick==14 or tick==59)','if(tick==14 or tick==59 or tick==179)')
n='            state.paused=false;pm.qa_watch_cell=cell;';h=r'''
            const fire_before_bytes=try std.json.stringifyAlloc(a,try saves.capture(a,state),.{});const fire_before=try std.json.parseFromSlice(saves.schema.Save,a,fire_before_bytes,.{.allocate=.alloc_always});
            const preview=try std.json.parseFromSlice(std.json.Value,a,std.mem.span(stella_god_target()),.{.allocate=.alloc_always});
            std.debug.assert(std.mem.eql(u8,fire_before_bytes,try std.json.stringifyAlloc(a,try saves.capture(a,state),.{})));
            std.debug.print("NATURAL_FIRE_PREVIEW branch={d} actual_export={s}\n",.{branch,try std.json.stringifyAlloc(a,preview.value,.{})});
            if(branch==0){const refused=try std.json.parseFromSlice(std.json.Value,a,std.mem.span(stella_god_action(3,@intCast(cell))),.{});std.debug.assert(std.mem.eql(u8,refused.value.object.get("failure").?.string,"wet"));std.debug.assert(std.mem.eql(u8,fire_before_bytes,try std.json.stringifyAlloc(a,try saves.capture(a,state),.{})));}
            if(branch==2){const receipt=try std.json.parseFromSlice(std.json.Value,a,std.mem.span(stella_god_action(3,@intCast(cell))),.{.allocate=.alloc_always});std.debug.assert(std.mem.eql(u8,receipt.value.object.get("failure").?.string,"none"));
              std.debug.print("NATURAL_FIRE_BURN receipt={s}\n",.{try std.json.stringifyAlloc(a,receipt.value,.{})});
              const burned=try std.json.stringifyAlloc(a,try saves.capture(a,state),.{});var check=try std.json.parseFromSlice(saves.schema.Save,a,burned,.{.allocate=.alloc_always});
              check.value.oxygen=fire_before.value.oxygen;check.value.carbon_dioxide=fire_before.value.carbon_dioxide;@constCast(check.value.temperature)[cell]=fire_before.value.temperature[cell];@constCast(check.value.origin.?.cells)[cell].detritus=fire_before.value.origin.?.cells[cell].detritus;
              std.debug.assert(std.mem.eql(u8,fire_before_bytes,try std.json.stringifyAlloc(a,check.value,.{})));
              std.debug.print("NATURAL_FIRE_ATOMIC only_detritus_selected_temperature_global_o2_co2_changed=true live_nutrients_rng_pause_clock_exact=true\n",.{});
              render(window);gl.finish();window.swapBuffers();qa_capture("/workspace/scratch/f67c3ac60ca3/site-tmp/natural-fire/just-burned.ppm");
            }
''' +n
assert n in s;s=s.replace(n,h)
s=s.replace('                render(window);gl.finish();window.swapBuffers();\n              }',r'''                std.debug.print("NATURAL_FIRE_COHORTS branch={d} tick={d} cell={s}\n",.{branch,tick+1,try std.json.stringifyAlloc(a,state.planet.microbeCells[cell],.{})});
                render(window);gl.finish();window.swapBuffers();const shot=try std.fmt.allocPrintZ(a,"/workspace/scratch/f67c3ac60ca3/site-tmp/natural-fire/branch-{d}-tick-{d}.ppm",.{branch,tick+1});qa_capture(shot);
              }''')
s=s.replace('if (!is_web or !web_initialized or !game.state_init) return null;','if (!game.state_init) return null; // Native test availability bridge for real exports.').replace('WATER_PAIRED','NATURAL_FIRE');p.write_text(s)
