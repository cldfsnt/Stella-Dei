#!/usr/bin/env python3
"""Isolated per-source atmospheric edge checks; no precision/cache changes."""
from pathlib import Path
import subprocess,sys
r=Path(__file__).resolve().parents[2];o=Path(sys.argv[1]);subprocess.run([sys.executable,str(r/'web/tests/egl-natural60-prepare.py'),str(o)],check=True)
p=o/'simulation/planet.zig';s=p.read_text();s='pub var qa_edge_hoist:bool=false;\n'+s
needle='            for(self.getNeighbours(i),0..)|n,j|rates[j]=self.atmosphericEdgeRate(i,n);';assert s.count(needle)==1
s=s.replace(needle,'''            if(!qa_edge_hoist){for(self.getNeighbours(i),0..)|n,j|rates[j]=self.atmosphericEdgeRate(i,n);}else{
                const point=self.transformedPoints[i];const from:[3]f64=.{point.x(),point.y(),point.z()};
                const wind:[3]f64=if(self.atmosphericWindScratch.len==self.transformedPoints.len) blk:{const w=self.atmosphericWindScratch[i];break :blk .{w[0],w[1],w[2]};}else self.atmosphericWind(i);
                var valid=true;for(0..3)|k|{if(!std.math.isFinite(from[k]) or !std.math.isFinite(wind[k]))valid=false;}
                for(self.getNeighbours(i),0..)|n,j|{
                    if(!valid){rates[j]=0;continue;}const b=self.transformedPoints[n];const to:[3]f64=.{b.x(),b.y(),b.z()};
                    var length2:f64=0;var dot:f64=0;var dest_valid=true;
                    for(0..3)|k|{if(!std.math.isFinite(to[k])){dest_valid=false;break;}const d=to[k]-from[k];length2+=d*d;dot+=wind[k]*d;}
                    rates[j]=if(!dest_valid or length2<=0 or !std.math.isFinite(length2) or !std.math.isFinite(dot))0 else @max(0,dot/length2);
                }
            }''');p.write_text(s)
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
            std.debug.print("EDGE_CLEAN trial={d} arm={d} ticks=300 ns={d} ms_per_tick={d} complete_save_exact=true\n",.{trial,arm,ns,@as(f64,@floatFromInt(ns))/300e6});
          }
          try saves.apply(state,initial.value);std.debug.assert(std.mem.eql(u8,frozen,try std.json.stringifyAlloc(a,try saves.capture(a,state),.{})));
          std.debug.print("EDGE_CLEAN_PASS original_restored=true cross_model_fullstate_exact=true\n",.{});
        }
'''+s[b:];s=s.replace('_=pw;_=pm;const micro=@import("simulation/microbes.zig");','_=pw;');p.write_text(s)
