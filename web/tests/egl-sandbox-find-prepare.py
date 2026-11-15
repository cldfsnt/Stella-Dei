#!/usr/bin/env python3
"""Actual current40k Sandbox navigation, no biology or simulation steps."""
from pathlib import Path
import sys,subprocess
r=Path(__file__).resolve().parents[2];o=Path(sys.argv[1]).resolve()
subprocess.run([sys.executable,str(r/'web/tests/egl-foraging-production-prepare.py'),str(o)],check=True)
p=o/'main.zig';s=p.read_text();a=s.index('          _=pm;_=pw;');b=s.index('\n        std.debug.print("FORAGING_PRODUCTION_COMPLETE',a)
s=s[:a]+r'''
          _=pm;_=pw;std.debug.assert(state.planet.worldMode==.sandbox);
          const original=try std.json.stringifyAlloc(a,try saves.capture(a,state),.{});const initial=try std.json.parseFromSlice(saves.schema.Save,a,original,.{.allocate=.alloc_always});
          for(0..2)|kind|{
            try saves.apply(state,initial.value);const start_ns=std.time.nanoTimestamp();const result=stella_find_sandbox_life(@intCast(kind));const elapsed=std.time.nanoTimestamp()-start_ns;std.debug.assert(result==1);
            const selected=state.selectedPoint;std.debug.assert(state.selectedPoint==state.clickedPoint and state.selectedTool==.None and state.paused==initial.value.paused);
            if(kind==0)std.debug.assert(state.planet.vegetation[selected]>=0.08 and state.planet.waterMass[selected]*state.planet.getKmPerWaterMass()<=0.0005);
            var after=try saves.capture(a,state);after.camera=initial.value.camera;after.camera_target=initial.value.camera_target;after.camera_distance=initial.value.camera_distance;after.target_distance=initial.value.target_distance;after.display_mode=initial.value.display_mode;
            std.debug.assert(std.mem.eql(u8,original,try std.json.stringifyAlloc(a,after,.{})));
            render(window);gl.finish();window.swapBuffers();qa_capture(if(kind==0)"OUTPUT/plants.ppm"else"OUTPUT/rabbit.ppm");
            std.debug.print("SANDBOX_FIND_PASS kind={} result={} selected={} cover={d} action_ms={d} full_model_rng_exact=true\n",.{kind,result,selected,state.planet.vegetation[selected],@as(f64,@floatFromInt(elapsed))/1e6});
          }
          try saves.apply(state,initial.value);
          const plants=try a.dupe(f32,state.planet.vegetation);@memset(state.planet.vegetation,0);const no_plants=try std.json.stringifyAlloc(a,try saves.capture(a,state),.{});std.debug.assert(stella_find_sandbox_life(0)==0);std.debug.assert(std.mem.eql(u8,no_plants,try std.json.stringifyAlloc(a,try saves.capture(a,state),.{})));@memcpy(state.planet.vegetation,plants);
          const rabbits=state.planet.lifeforms.items;state.planet.lifeforms.items=rabbits[0..0];const no_rabbits=try std.json.stringifyAlloc(a,try saves.capture(a,state),.{});std.debug.assert(stella_find_sandbox_life(1)==0);std.debug.assert(std.mem.eql(u8,no_rabbits,try std.json.stringifyAlloc(a,try saves.capture(a,state),.{})));state.planet.lifeforms.items=rabbits;
          std.debug.assert(state.findSandboxLife(0,390,300)==-3);std.debug.assert(std.mem.eql(u8,original,try std.json.stringifyAlloc(a,try saves.capture(a,state),.{})));
          try saves.apply(state,initial.value);std.debug.assert(std.mem.eql(u8,original,try std.json.stringifyAlloc(a,try saves.capture(a,state),.{})));
          std.debug.print("SANDBOX_FIND_COMPLETE empty_failures_inert=true small_view_inert=true original_restored=true\n",.{});
        }
'''.replace('OUTPUT',str(o.parent))+s[b:];p.write_text(s)
subprocess.run([sys.executable,str(r/'web/tests/audit-zig-exports.py'),str(r/'src/main.zig'),str(p)],check=True,stdout=(o.parent/'export-audit.json').open('w'))
