#!/usr/bin/env python3
"""Benchmark only: exact same day of physics, with/without per-tick drawing."""
from pathlib import Path
import subprocess,sys,json,hashlib
root=Path(__file__).resolve().parents[2];out=Path(sys.argv[1])
subprocess.run([sys.executable,str(root/'web/tests/egl-natural60-prepare.py'),str(out)],check=True)
p=out/'simulation/planet.zig';s=p.read_text();needle='if (@import("builtin").target.cpu.arch != .wasm32) {';assert s.count(needle)==1;s=s.replace(needle,'if (false) { // QA browser-policy: no native-only atmosphere mesh upload.');p.write_text(s)
p=out/'main.zig';s=p.read_text().replace('const micro=@import("simulation/microbes.zig");','');start=s.index('          const start_time=state.gameTime;');end=s.index('\n        try originSaveCheck',start)
s=s[:start]+r'''
          state.paused=true;state.showEscapeMenu=false;state.showPlanetControl=false;state.showPointDetails=false;state.pointerOnPlanet=false;
          _=state.findLivingClusterResult(390,700);
          // Unmeasured camera settling and GL shader warmup, before frozen benchmark state.
          for(0..100)|_|{loop.pump(16);render(window);gl.finish();window.swapBuffers();}
          const frozen_bytes=try std.json.stringifyAlloc(a,try saves.capture(a,state),.{});
          const frozen=try std.json.parseFromSlice(saves.schema.Save,a,frozen_bytes,.{.allocate=.alloc_always});
          var reference:?[]const u8=null;
          std.debug.print("ADVANCE_PLATFORM renderer={s} parallel={d} width={d} height={d} cells={d}\n",.{std.mem.span(gl.getString(gl.RENDERER).?),loop.getParallelCount(),window.getFramebufferSize().width,window.getFramebufferSize().height,state.planet.vertices.len});
          for([_]bool{false,true,true,false,false,true},0..)|hidden,trial|{
            loop.pump(1024);try saves.apply(state,frozen.value);state.simulationClock.reset();
            std.debug.assert(std.mem.eql(u8,frozen_bytes,try std.json.stringifyAlloc(a,try saves.capture(a,state),.{})));
            render(window);gl.finish();window.swapBuffers();loop.pump(16);
            var clock=try std.time.Timer.start();var callbacks_ns:u64=0;var max_callback_ns:u64=0;var physics_ns:u64=0;var draw_ns:u64=0;var times:[60]f64=undefined;
            for(0..60)|tick|{
              var callback=try std.time.Timer.start();glfw.pollEvents();loop.pump(16);
              var phy=try std.time.Timer.start();
              state.planet.simulate(game.loop,.{.dt=1440,.timeScale=1,.solarConstant=state.solarConstant,.gameTime=state.gameTime,.planetRotationTime=state.planetRotationTime,.solarVector=state.simulationSolarVector()});state.gameTime+=1440;state.renderGameTime=state.gameTime;
              physics_ns+=phy.read();loop.pump(16);
              if(!hidden){var draw=try std.time.Timer.start();render(window);gl.finish();window.swapBuffers();draw_ns+=draw.read();}
              const spent=callback.read();callbacks_ns+=spent;max_callback_ns=@max(max_callback_ns,spent);times[tick]=@as(f64,@floatFromInt(spent))/1e6;
            }
            const ticks_ns=clock.read();var final=try std.time.Timer.start();render(window);gl.finish();window.swapBuffers();const final_ns=final.read();const whole_ns=clock.read();
            std.mem.sort(f64,&times,{},std.sort.asc(f64));
            std.debug.assert(state.paused and state.timeScale==frozen.value.time_scale and state.gameTime==frozen.value.game_time+86400);
            const result=try std.json.stringifyAlloc(a,try saves.capture(a,state),.{});
            const path=try std.fmt.allocPrint(a,"/workspace/scratch/f67c3ac60ca3/site-tmp/advance-day/trial-{d}.json",.{trial});try std.fs.cwd().writeFile(.{.sub_path=path,.data=result});
            const equal=if(reference)|prior|std.mem.eql(u8,prior,result) else true;if(reference==null)reference=result;
            std.debug.print("ADVANCE_RESULT {s}\n",.{try std.json.stringifyAlloc(a,.{.trial=trial,.hidden=hidden,.ticks=60,.simulation_seconds=86400,.callbacks_ms=@as(f64,@floatFromInt(callbacks_ns))/1e6,.ticks_elapsed_ms=@as(f64,@floatFromInt(ticks_ns))/1e6,.total_ms=@as(f64,@floatFromInt(whole_ns))/1e6,.physics_ms=@as(f64,@floatFromInt(physics_ns))/1e6,.draw_ms=@as(f64,@floatFromInt(draw_ns))/1e6,.final_redraw_ms=@as(f64,@floatFromInt(final_ns))/1e6,.max_callback_ms=@as(f64,@floatFromInt(max_callback_ns))/1e6,.p95_callback_ms=times[56],.full_save_equal=equal,.paused_preserved=state.paused,.pace_preserved=state.timeScale==frozen.value.time_scale},.{})});
            std.debug.assert(equal);
          }
          try saves.apply(state,frozen.value);std.debug.assert(std.mem.eql(u8,frozen_bytes,try std.json.stringifyAlloc(a,try saves.capture(a,state),.{})));
          std.debug.print("ADVANCE_PASS six_trials_full_save_identical=true sixty_ticks_each=true paused_pace_preserved=true original_restored=true\n",.{});
        }
'''+s[end:];p.write_text(s)
files=['main.zig','simulation/planet.zig','simulation/microbes.zig','states/play.zig','loop.zig']
(out.parent/'provenance.json').write_text(json.dumps({'head':subprocess.check_output(['git','rev-parse','HEAD'],cwd=root,text=True).strip(),'production':{f:hashlib.sha256((root/'src'/f).read_bytes()).hexdigest() for f in files},'copied':{f:hashlib.sha256((out/f).read_bytes()).hexdigest() for f in files}},indent=2)+'\n')
