#!/usr/bin/env python3
"""Isolated exact contiguous SIMD membership predicate; no arithmetic or cache changes."""
from pathlib import Path
import subprocess,sys
r=Path(__file__).resolve().parents[2];o=Path(sys.argv[1]);subprocess.run([sys.executable,str(r/'web/tests/egl-natural60-prepare.py'),str(o)],check=True)
p=o/'simulation/planet.zig';s=p.read_text();s='pub var qa_edge_hoist:bool=false;\n'+s
needle='if (@reduce(.Or, origin == @as(IndexVector, @splat(target_elem)))) {'
assert s.count(needle)==1
s=s.replace(needle,'if (if(qa_edge_hoist) (target_elem >= origin[0] and target_elem-origin[0] < VECTOR_SIZE) else @reduce(.Or, origin == @as(IndexVector, @splat(target_elem)))) {')
p.write_text(s)
p=o/'main.zig';s=p.read_text();a=s.index('          const start_time=state.gameTime;');b=s.index('\n        try originSaveCheck',a)
s=s[:a]+r'''
          const frozen=try std.json.stringifyAlloc(a,try saves.capture(a,state),.{});
          const initial=try std.json.parseFromSlice(saves.schema.Save,a,frozen,.{.allocate=.alloc_always});
          var expected:?[]const u8=null;
          for([_]usize{0,1,1,0,0,1},0..)|arm,trial|{
            try saves.apply(state,initial.value);pm.qa_edge_hoist=arm==1;
            std.debug.assert(std.mem.eql(u8,frozen,try std.json.stringifyAlloc(a,try saves.capture(a,state),.{})));
            for(0..30)|_|{state.planet.simulate(game.loop,.{.dt=1440,.timeScale=1,.solarConstant=state.solarConstant,.gameTime=state.gameTime,.planetRotationTime=state.planetRotationTime,.solarVector=state.simulationSolarVector()});state.gameTime+=1440;}
            var timer=try std.time.Timer.start();
            for(0..300)|_|{state.planet.simulate(game.loop,.{.dt=1440,.timeScale=1,.solarConstant=state.solarConstant,.gameTime=state.gameTime,.planetRotationTime=state.planetRotationTime,.solarVector=state.simulationSolarVector()});state.gameTime+=1440;}
            const ns=timer.read();const endpoint=try std.json.stringifyAlloc(a,try saves.capture(a,state),.{});
            if(expected)|e|{std.debug.assert(std.mem.eql(u8,e,endpoint));}else expected=endpoint;
            std.debug.print("LIQUID_RANGE trial={d} arm={d} ticks=300 ns={d} ms_per_tick={d} complete_save_exact=true\n",.{trial,arm,ns,@as(f64,@floatFromInt(ns))/300e6});
          }
          try saves.apply(state,initial.value);std.debug.assert(std.mem.eql(u8,frozen,try std.json.stringifyAlloc(a,try saves.capture(a,state),.{})));
          std.debug.print("LIQUID_RANGE_PASS original_restored=true cross_model_fullstate_exact=true\n",.{});
        }
'''+s[b:];s=s.replace('_=pw;_=pm;const micro=@import("simulation/microbes.zig");','_=pw;');p.write_text(s)
