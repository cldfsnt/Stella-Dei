#!/usr/bin/env python3
"""No-shadow actual coupled performance gate using arithmetic candidate only."""
from pathlib import Path
import sys,subprocess
r=Path(__file__).resolve().parents[2];o=Path(sys.argv[1]);subprocess.run([sys.executable,str(r/'web/tests/egl-receipt-engine-prepare.py'),str(o)],check=True)
p=o/'simulation/microbes.zig';s=p.read_text();a=s.index('pub fn step(cell:*Cell');b=s.index('\nfn boundedAdd',a);s=s[:a]+'''pub fn step(cell:*Cell,env:Environment,elapsed:f32) Flux {return if(qa_candidate)receiptStep(cell,env,elapsed) else baselineStep(cell,env,elapsed);}
'''+s[b:];s=s.replace('pub var qa_candidate:bool=false;','pub var qa_candidate:bool=true;');p.write_text(s)
p=o/'main.zig';s=p.read_text();a=s.index('          const qa_dt:f32=');b=s.index('\n        try originSaveCheck',a)
s=s[:a]+r'''
          for([_]usize{0,1,1,0,0,1},0..)|arm,trial|{
            try saves.apply(state,initial.value);micro.qa_candidate=arm==1;
            std.debug.assert(std.mem.eql(u8,frozen,try std.json.stringifyAlloc(a,try saves.capture(a,state),.{})));
            // Identical untimed restored-world warmup for each arm.
            for(0..30)|_|{state.planet.simulate(game.loop,.{.dt=1440,.timeScale=1,.solarConstant=state.solarConstant,.gameTime=state.gameTime,.planetRotationTime=state.planetRotationTime,.solarVector=state.simulationSolarVector()});state.gameTime+=1440;}
            var timer=try std.time.Timer.start();
            for(0..300)|_|{state.planet.simulate(game.loop,.{.dt=1440,.timeScale=1,.solarConstant=state.solarConstant,.gameTime=state.gameTime,.planetRotationTime=state.planetRotationTime,.solarVector=state.simulationSolarVector()});state.gameTime+=1440;}
            const ns=timer.read();var colonies:usize=0;
            for(state.planet.microbeCells)|pc|{std.debug.assert(micro.validCell(pc,state.planet.microbeStats.next_lineage));for(pc.cohorts)|co|{if(co.biomass>0)colonies+=1;}}
            std.debug.print("RECEIPT_CLEAN trial={d} arm={d} ticks=300 ns={d} ms_per_tick={d} colonies={d}\n",.{trial,arm,ns,@as(f64,@floatFromInt(ns))/300e6,colonies});
          }
          try saves.apply(state,initial.value);std.debug.assert(std.mem.eql(u8,frozen,try std.json.stringifyAlloc(a,try saves.capture(a,state),.{})));
          std.debug.print("RECEIPT_CLEAN_PASS no_shadow=true original_restored=true\n",.{});
        }
'''+s[b:];p.write_text(s)
