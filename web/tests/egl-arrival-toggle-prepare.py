#!/usr/bin/env python3
"""Actual paid-arrival display-only acceptance; no injected tracker events."""
from pathlib import Path
import subprocess,sys,json,hashlib
r=Path(__file__).resolve().parents[2];o=Path(sys.argv[1]).resolve()
subprocess.run([sys.executable,str(r/'web/tests/egl-seed-target-toggle-prepare.py'),str(o)],check=True)
p=o/'main.zig';s=p.read_text();a=s.index('          _=pm;_=pw;');b=s.index('\n        std.debug.print("SEED_TARGET_COMPLETE',a)
s=s[:a]+r'''
          _=pm;_=pw;state.paused=true;state.showEscapeMenu=false;state.showPointDetails=false;state.showPlanetControl=false;state.selectedTool=.None;state.watchLifeView=true;
          const original=try std.json.stringifyAlloc(a,try saves.capture(a,state),.{});
          const initial=try std.json.parseFromSlice(saves.schema.Save,a,original,.{.allocate=.alloc_always});
          std.debug.assert(stella_arrival_effects(-1)==1);
          var ticks:usize=0;
          while(state.planet.propaguleFeedback.next_serial==1 and ticks<120):(ticks+=1){
            state.planet.simulate(game.loop,.{.dt=1440,.timeScale=1,.solarConstant=state.solarConstant,.gameTime=state.gameTime,.planetRotationTime=state.planetRotationTime,.solarVector=state.simulationSolarVector()});state.gameTime+=1440;
          }
          std.debug.assert(state.planet.propaguleFeedback.next_serial>1);
          const latest=state.planet.propaguleFeedback.next_serial-1;
          const event=state.planet.propaguleFeedback.events[@intCast((latest-1)%32)];
          state.selectedPoint=event.cell;std.debug.assert(state.fitLivingClusterResult(390,700)==1);state.update(&game,0);
          render(window);gl.finish();window.swapBuffers();
          var count:usize=0;for(state.propaguleVisuals.pulses)|pulse|{if(pulse.remaining>0)count+=1;}
          std.debug.assert(count>0);const glyphs=state.visibleSprouts;
          qa_capture("OUTPUT/shown.ppm");
          const before=try std.json.stringifyAlloc(a,try saves.capture(a,state),.{});
          const tracker=try std.json.stringifyAlloc(a,state.planet.propaguleFeedback,.{});
          std.debug.assert(stella_arrival_effects(0)==0);
          for(state.propaguleVisuals.pulses)|pulse|std.debug.assert(pulse.remaining==0);
          render(window);gl.finish();window.swapBuffers();qa_capture("OUTPUT/hidden.ppm");
          std.debug.assert(state.visibleSprouts==glyphs);
          std.debug.assert(std.mem.eql(u8,before,try std.json.stringifyAlloc(a,try saves.capture(a,state),.{})));
          std.debug.assert(std.mem.eql(u8,tracker,try std.json.stringifyAlloc(a,state.planet.propaguleFeedback,.{})));
          // New real events while hidden, deliberately without rendering any hidden frame.
          const hidden_start=state.planet.propaguleFeedback.next_serial;var hidden_ticks:usize=0;
          while(state.planet.propaguleFeedback.next_serial==hidden_start and hidden_ticks<120):(hidden_ticks+=1){
            state.planet.simulate(game.loop,.{.dt=1440,.timeScale=1,.solarConstant=state.solarConstant,.gameTime=state.gameTime,.planetRotationTime=state.planetRotationTime,.solarVector=state.simulationSolarVector()});state.gameTime+=1440;
          }
          std.debug.assert(state.planet.propaguleFeedback.next_serial>hidden_start);
          const hidden_save=try std.json.stringifyAlloc(a,try saves.capture(a,state),.{});
          const hidden_tracker=try std.json.stringifyAlloc(a,state.planet.propaguleFeedback,.{});
          std.debug.assert(stella_arrival_effects(1)==1);
          render(window);gl.finish();window.swapBuffers();qa_capture("OUTPUT/restored.ppm");
          for(state.propaguleVisuals.pulses)|pulse|std.debug.assert(pulse.remaining==0);
          std.debug.assert(std.mem.eql(u8,hidden_save,try std.json.stringifyAlloc(a,try saves.capture(a,state),.{})));
          std.debug.assert(std.mem.eql(u8,hidden_tracker,try std.json.stringifyAlloc(a,state.planet.propaguleFeedback,.{})));
          std.debug.assert(stella_arrival_effects(2)==-1 and stella_arrival_effects(-1)==1);
          std.debug.print("ARRIVAL_TOGGLE_PASS ticks={} actual_pulses={} glyphs={} hidden_ticks={} hidden_events={} save_rng_exact=true tracker_exact=true hidden_backlog_not_replayed=true\n",.{ticks,count,glyphs,hidden_ticks,state.planet.propaguleFeedback.next_serial-hidden_start});
          try saves.apply(state,initial.value);std.debug.assert(std.mem.eql(u8,original,try std.json.stringifyAlloc(a,try saves.capture(a,state),.{})));
        }
'''.replace('OUTPUT',str(o.parent))+s[b:];s=s.replace('SEED_TARGET_COMPLETE','ARRIVAL_TOGGLE_COMPLETE');p.write_text(s)
subprocess.run([sys.executable,str(r/'web/tests/audit-zig-exports.py'),str(r/'src/main.zig'),str(p)],check=True,stdout=(o.parent/'export-audit.json').open('w'))
(o.parent/'arrival-provenance.json').write_text(json.dumps({'head':subprocess.check_output(['git','rev-parse','HEAD'],cwd=r,text=True).strip(),'files':{f:hashlib.sha256((o/f).read_bytes()).hexdigest() for f in ['main.zig','states/play.zig','propagule_visuals.zig','simulation/planet.zig']}},indent=2)+'\n')
