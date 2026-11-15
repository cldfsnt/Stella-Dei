#!/usr/bin/env python3
"""Independent actual export/callback acceptance, native availability bridge only."""
from pathlib import Path
import subprocess,sys
r=Path(__file__).resolve().parents[2];o=Path(sys.argv[1]);subprocess.run([sys.executable,str(r/'web/tests/egl-natural60-prepare.py'),str(o)],check=True)
p=o/'main.zig';s=p.read_text();s=s.replace('if (!is_web or !web_initialized or !game.state_init) return null;','if (!web_initialized or !game.state_init) return null; // QA native export availability bridge')
s=s.replace('fn render(window: glfw.Window) void {','var qa_render_count:usize=0;\nfn render(window: glfw.Window) void {\n    qa_render_count+=1;')
a=s.index('          const start_time=state.gameTime;');b=s.index('\n        try originSaveCheck',a)
s=s[:a]+r'''
          web_initialized=true;
          state.paused=true;state.showEscapeMenu=false;state.showPlanetControl=false;state.showPointDetails=false;
          _=state.findLivingClusterResult(390,700);
          for(0..100)|_|{render(window);gl.finish();window.swapBuffers();}
          const frozen_bytes=try std.json.stringifyAlloc(a,try saves.capture(a,state),.{});
          const frozen=try std.json.parseFromSlice(saves.schema.Save,a,frozen_bytes,.{.allocate=.alloc_always});
          const world=PerformanceDetails.world_serial;
          // Independent ordinary sixty-tick reference, same final real render.
          for(0..60)|_|{loop.pump(16);state.planet.simulate(game.loop,.{.dt=1440,.timeScale=1,.solarConstant=state.solarConstant,.gameTime=state.gameTime,.planetRotationTime=state.planetRotationTime,.solarVector=state.simulationSolarVector()});state.gameTime+=1440;state.renderGameTime=state.gameTime;loop.pump(16);}
          render(window);gl.finish();window.swapBuffers();
          const expected=try std.json.stringifyAlloc(a,try saves.capture(a,state),.{});
          try saves.apply(state,frozen.value);AdvanceDay.current=.{};
          const stale=try std.json.parseFromSlice(std.json.Value,a,std.mem.span(stella_advance_start(world+1)),.{});std.debug.assert(!stale.value.object.get("ok").?.bool);
          std.debug.assert(std.mem.eql(u8,frozen_bytes,try std.json.stringifyAlloc(a,try saves.capture(a,state),.{})));
          state.paused=false;const running=try std.json.parseFromSlice(std.json.Value,a,std.mem.span(stella_advance_start(world)),.{});std.debug.assert(!running.value.object.get("ok").?.bool);state.paused=true;
          const started=try std.json.parseFromSlice(std.json.Value,a,std.mem.span(stella_advance_start(world)),.{});std.debug.assert(started.value.object.get("ok").?.bool);
          const token=AdvanceDay.current.token;const before_controls=try std.json.stringifyAlloc(a,try saves.capture(a,state),.{});
          std.debug.assert(stella_save()==-4 and stella_load()==-4 and stella_set_speed(3600)==-1);
          std.debug.assert(!std.math.isFinite(stella_adjust_water(@intCast(state.selectedPoint),0.1)));
          _=stella_seed_colony(@intCast(state.selectedPoint));_=stella_test_action(1);stella_zoom(2);cursorPosCallback(window,42,42);mouseScroll(window,0,1);mousePressed(window,.left);
          const wrong_cancel=try std.json.parseFromSlice(std.json.Value,a,std.mem.span(stella_advance_cancel(token+1)),.{});std.debug.assert(!wrong_cancel.value.object.get("ok").?.bool);
          std.debug.assert(std.mem.eql(u8,before_controls,try std.json.stringifyAlloc(a,try saves.capture(a,state),.{})));
          const draws=qa_render_count;
          for(0..60)|tick|{if(tick==59){state.colonyTargets.count=0;state.visibleSprouts=0;}loop.pump(16);std.debug.assert(advanceFrame(0.016));std.debug.assert(AdvanceDay.current.completed==tick+1);if(tick<59)std.debug.assert(qa_render_count==draws);}
          std.debug.assert(qa_render_count==draws+1 and AdvanceDay.current.phase==.done and state.paused and state.timeScale==frozen.value.time_scale);
          std.debug.assert(std.mem.eql(u8,expected,try std.json.stringifyAlloc(a,try saves.capture(a,state),.{})));
          std.debug.assert(state.colonyTargets.count>0 and state.visibleSprouts>0);for(state.colonyTargets.items[0..state.colonyTargets.count])|target|std.debug.assert(micro.biomass(state.planet.microbeCells[target.cell])>0);
          std.debug.print("ADVANCE_PASSIVE_REFRESH glyphs={d} targets={d} actual_living_cells=true cache_cleared_before_final=true\n",.{state.visibleSprouts,state.colonyTargets.count});
          qa_capture("../site-tmp/advance-acceptance/final.ppm");
          // Held input cannot leak through after final redraw; only neutral callback releases latch.
          std.debug.assert(!advanceFrame(0.016) and AdvanceDay.blocksInput());
          const dismissed=try std.json.parseFromSlice(std.json.Value,a,std.mem.span(stella_advance_dismiss(token)),.{});std.debug.assert(dismissed.value.object.get("ok").?.bool);
          qa_pointer(20,20,1);std.debug.assert(!advanceFrame(0.016) and AdvanceDay.blocksInput());qa_pointer(20,20,0);std.debug.assert(!advanceFrame(0.016) and !AdvanceDay.blocksInput());
          const prior_free=state.freeCam;const prior_rotation=state.cameraRotation;state.freeCam=true;
          qa_pointer(200,400,0);std.debug.assert(@reduce(.And,state.cameraRotation.data==prior_rotation.data));
          qa_pointer(210,400,0);std.debug.assert(!@reduce(.And,state.cameraRotation.data==prior_rotation.data));state.freeCam=prior_free;state.cameraRotation=prior_rotation;
          std.debug.print("ADVANCE_CURSOR first_delta_zero=true next_delta_live=true\n",.{});
          std.debug.print("ADVANCE_ACCEPT complete60_exact_save=true exported_start_status_cancel=true writes_blocked=true one_final_real_draw=true held_input_latch=true\n",.{});
          for(0..5)|mode|{
            std.debug.print("ADVANCE_STAGE mode={d} begin\n",.{mode});
            try saves.apply(state,frozen.value);AdvanceDay.current=.{};
            _=stella_advance_environment(1,1);_=stella_advance_start(PerformanceDetails.world_serial);std.debug.print("ADVANCE_STAGE started={s}\n",.{std.mem.span(stella_advance_status())});std.debug.assert(AdvanceDay.busy());
            for(0..7)|_|{loop.pump(16);_=advanceFrame(0.016);}
            std.debug.print("ADVANCE_STAGE partial={s}\n",.{std.mem.span(stella_advance_status())});const time=state.gameTime;const partial=try std.json.stringifyAlloc(a,try saves.capture(a,state),.{});const d=qa_render_count;
            if(mode==0){_=stella_advance_cancel(AdvanceDay.current.token);_=stella_advance_environment(0,1);_=advanceFrame(0.016);std.debug.assert(qa_render_count==d and AdvanceDay.current.phase==.redraw);_=stella_advance_environment(1,1);}
            if(mode==1){
              _=stella_advance_environment(1,0);std.debug.assert(advanceFrame(0.016));_=stella_advance_environment(1,1);std.debug.assert(advanceFrame(0.016));
              std.debug.assert(qa_render_count==d and AdvanceDay.current.recovery_required and !AdvanceDay.current.context_ok and state.gameTime==time);
              const recovery=try std.json.parseFromSlice(std.json.Value,a,std.mem.span(stella_advance_status()),.{});std.debug.assert(!recovery.value.object.get("redraw_complete").?.bool and recovery.value.object.get("recovery_save_allowed").?.bool);
              const denied=try std.json.parseFromSlice(std.json.Value,a,std.mem.span(stella_advance_dismiss(AdvanceDay.current.token)),.{});std.debug.assert(!denied.value.object.get("ok").?.bool);
              std.debug.assert(stella_load()==-4 and stella_set_speed(3600)==-1 and stella_save()==0);
              const disk=try std.fs.cwd().readFileAlloc(a,saves.path,100*1024*1024);std.debug.assert(std.mem.eql(u8,partial,disk));
              state.paused=false;std.debug.assert(stella_save()==-4);state.paused=true;state.gameTime+=1440;std.debug.assert(stella_save()==-4);state.gameTime=time;
              PerformanceDetails.worldChanged();std.debug.assert(stella_save()==-4);
              std.debug.print("ADVANCE_RECOVERY permanent_after_context_restore=true no_render_or_tick=true exact_partial_save=true unsafe_save_denied=true explicit_reload_required=true\n",.{});
              continue;
            }
            if(mode==2){_=advanceFrame(3);}
            if(mode==3){PerformanceDetails.worldChanged();}
            if(mode==4){try saves.apply(state,frozen.value);}
            _=advanceFrame(0.016);std.debug.print("ADVANCE_STAGE terminal={s} draws={d}/{d}\n",.{std.mem.span(stella_advance_status()),qa_render_count,d});std.debug.assert(AdvanceDay.current.phase==.cancelled and AdvanceDay.current.completed==7 and qa_render_count==d+1);
            std.debug.assert(state.gameTime==if(mode==4)frozen.value.game_time else time);
            if(mode!=4){
              const after_partial=try std.json.stringifyAlloc(a,try saves.capture(a,state),.{});
              const partial_save=try std.json.parseFromSlice(saves.schema.Save,a,partial,.{.allocate=.alloc_always});const terminal_controller=AdvanceDay.current;
              try saves.apply(state,partial_save.value);AdvanceDay.current=.{};render(window);gl.finish();window.swapBuffers();
              const reference_draw=try std.json.stringifyAlloc(a,try saves.capture(a,state),.{});
              std.debug.assert(std.mem.eql(u8,after_partial,reference_draw));AdvanceDay.current=terminal_controller;
              std.debug.print("ADVANCE_PARTIAL matched_real_final_draw_fullsave_exact=true\n",.{});
            }
            _=stella_advance_dismiss(AdvanceDay.current.token);_=advanceFrame(0.016);std.debug.assert(!AdvanceDay.blocksInput());
            std.debug.print("ADVANCE_CANCEL mode={d} partial_ticks=7 no_extra_tick=true final_redraw=true pause={any}\n",.{mode,state.paused});
          }
          try saves.apply(state,frozen.value);AdvanceDay.current=.{};std.debug.assert(std.mem.eql(u8,frozen_bytes,try std.json.stringifyAlloc(a,try saves.capture(a,state),.{})));
          std.debug.print("ADVANCE_ACCEPT_PASS original_restored=true\n",.{});
        }
'''+s[b:];p.write_text(s)

p=o/'save_game.zig';s=p.read_text().replace('/saves',str(o.parent/'qa-saves'));p.write_text(s)
