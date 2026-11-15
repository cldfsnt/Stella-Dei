#!/usr/bin/env python3
"""Frozen v57 vs persisted hydration candidate; no observer/shadow scan in timing."""
from pathlib import Path
import shutil,sys,hashlib,json,subprocess
r=Path(__file__).resolve().parents[2];dest=Path(sys.argv[1]).resolve();frozen=Path(sys.argv[2]).resolve();candidate=sys.argv[3]=='candidate'
shutil.copytree(frozen,dest,dirs_exist_ok=True)
if not candidate:
 for name in ['simulation/planet.zig','simulation/microbes.zig','save_schema.zig','save_game.zig']:
  (dest/name).write_bytes(subprocess.check_output(['git','show','b308b37:src/'+name],cwd=r))
else:
 p=dest/'simulation/planet.zig';s=p.read_text();s='\n'.join(l for l in s.split('\n') if not l.startswith('pub var qa_bio_') and 'var qa_water_before:' not in l and 'var qa_water_after:' not in l);p.write_text(s)
 # No exchange instrumentation is reached in zero-owned mode. Remove it regardless.
 p=dest/'simulation/hydration_exchange.zig';s=p.read_text();s=s.replace('pub var qa_max_residual:f64=0;pub var qa_sum_residual:f64=0;\n','').replace(' const qa_before=total(cell.*,liquid.*,vapor.*,area);\n','');start=s.find('const residual=total(')
 if start>=0:s=s[:start]+s[s.index('return flux;',start):]
 p.write_text(s)
p=dest/'main.zig';s=p.read_text();start=s.index('          const frozen=try std.json.stringifyAlloc(a,try saves.capture(a,state),.{});');end=s.index('\n        try originSaveCheck',start)
block=r'''
          _=pm;
          const frozen=try std.json.stringifyAlloc(a,try saves.capture(a,state),.{});const baseline=try std.json.parseFromSlice(saves.schema.Save,a,frozen,.{.allocate=.alloc_always});
          const parity=std.posix.getenv("QA_RETENTION_PARITY")!=null;
          const ticks:usize=if(parity)10 else 300;const warm:usize=if(parity)0 else 30;
          for(0..warm)|_|{state.planet.simulate(game.loop,.{.dt=1440,.timeScale=1,.solarConstant=state.solarConstant,.gameTime=state.gameTime,.planetRotationTime=state.planetRotationTime,.solarVector=state.simulationSolarVector()});state.gameTime+=1440;}
          var timer=try std.time.Timer.start();
          for(0..ticks)|_|{state.planet.simulate(game.loop,.{.dt=1440,.timeScale=1,.solarConstant=state.solarConstant,.gameTime=state.gameTime,.planetRotationTime=state.planetRotationTime,.solarVector=state.simulationSolarVector()});state.gameTime+=1440;}
          const ns=timer.read();
          std.debug.print("RETENTION_OVERHEAD candidate=CANDIDATE ticks={d} warmup={d} ns={d} partitions={d} cells={d} cell_bytes={d} cohort_bytes={d}\n",.{ticks,warm,ns,game.loop.getParallelCount(),state.planet.microbeCells.len,@sizeOf(micro.Cell),@sizeOf(micro.Cohort)});
          const endpoint=try std.json.stringifyAlloc(a,try saves.capture(a,state),.{});try std.fs.cwd().writeFile(.{.sub_path="OUTPUT/endpoint.json",.data=endpoint});
          try saves.apply(state,baseline.value);std.debug.assert(std.mem.eql(u8,frozen,try std.json.stringifyAlloc(a,try saves.capture(a,state),.{})));
        }
'''.replace('CANDIDATE',str(candidate).lower()).replace('OUTPUT',str(dest.parent))
s=s[:start]+block+s[end:];p.write_text(s)
(dest.parent/'provenance.json').write_text(json.dumps({'baseline_revision':'b308b37','candidate':candidate,'frozen_input':str(frozen),'files':{str(p.relative_to(dest)):hashlib.sha256(p.read_bytes()).hexdigest() for p in [dest/'main.zig',dest/'simulation/planet.zig',dest/'simulation/microbes.zig',dest/'save_schema.zig',dest/'save_game.zig']}},indent=2)+'\n')
