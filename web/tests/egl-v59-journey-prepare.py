#!/usr/bin/env python3
"""Current-source scripted native journey, not browser/device interaction."""
from pathlib import Path
import sys,subprocess,hashlib,json
r=Path(__file__).resolve().parents[2];o=Path(sys.argv[1]).resolve();subprocess.run([sys.executable,str(r/'web/tests/egl-habitat-preview-prepare.py'),str(o)],check=True)
p=o/'main.zig';s=p.read_text();a=s.index('          _=first_id;');b=s.index('\n        try originSaveCheck',a)
s=s[:a]+r'''
          _=first_id;
          try saves.apply(state,baseline.value);state.selectedPoint=target;state.paused=true;state.pointerOnPlanet=true;
          const pace=state.timeScale;const before_births=state.planet.microbeStats.births;
          const prep=try std.json.parseFromSlice(std.json.Value,a,std.mem.span(stella_habitat_prepare(PerformanceDetails.world_serial,@intCast(target),1)),.{.allocate=.alloc_always});std.debug.assert(prep.value.object.get("ok").?.bool);
          const token:u32=@intCast(prep.value.object.get("token").?.integer);
          const habitat=try std.json.parseFromSlice(std.json.Value,a,std.mem.span(stella_habitat_execute(token)),.{.allocate=.alloc_always});std.debug.assert(habitat.value.object.get("ok").?.bool);std.debug.assert(state.planet.microbeStats.births==before_births);
          const seeded=stella_seed_colony(@intCast(target));std.debug.print("JOURNEY_SEED target={d} result={d} depth={d} biomass={d}\n",.{target,seeded,state.planet.waterMass[target]*conv*1000,M.biomass(state.planet.microbeCells[target])});std.debug.assert(seeded==1 and M.biomass(state.planet.microbeCells[target])>0);
          const started=try std.json.parseFromSlice(std.json.Value,a,std.mem.span(stella_advance_start(PerformanceDetails.world_serial)),.{});std.debug.assert(started.value.object.get("ok").?.bool);const advance_token=AdvanceDay.current.token;const start_time=state.gameTime;
          for(0..60)|_|{loop.pump(16);std.debug.assert(advanceFrame(0.016));}
          std.debug.assert(AdvanceDay.current.phase==.done and state.gameTime-start_time==86400 and state.paused and state.timeScale==pace);
          _=stella_advance_dismiss(advance_token);_=advanceFrame(0.016);std.debug.assert(!AdvanceDay.blocksInput());
          std.debug.print("JOURNEY_ADVANCE one_day_exact=true pace_preserved=true nursery_living={d}\n",.{M.biomass(state.planet.microbeCells[target])});
          const find=stella_find_life();std.debug.assert(find==1);render(window);gl.finish();window.swapBuffers();std.debug.assert(state.colonyTargets.count>0);
          const hit=state.colonyTargets.items[0];qa_pointer(hit.x,hit.y,0);state.mousePressed(&game,.left);std.debug.assert(state.selectedPoint==hit.cell and state.colonyPeek.cell.?==hit.cell);
          const inspected=try std.json.parseFromSlice(std.json.Value,a,std.mem.span(stella_life_snapshot()),.{.allocate=.alloc_always});std.debug.assert(inspected.value.object.get("cell").?.integer==hit.cell);
          const changed=stella_adjust_water(@intCast(hit.cell),0.1);std.debug.assert(std.math.isFinite(changed) and changed>0);
          std.debug.assert(stella_patch_watch_start_checked(@intCast(hit.cell),PerformanceDetails.world_serial,1)==1 and !state.paused and state.timeScale==pace);
          for(0..120)|_|{loop.pump(16);state.update(&game,1.0/60.0);loop.pump(16);}
          std.debug.print("JOURNEY_WATCH water_added_m={d} snapshot={s}\n",.{changed,std.mem.span(stella_patch_watch_snapshot())});
          state.paused=true;stella_patch_watch_stop(0);render(window);gl.finish();window.swapBuffers();qa_capture("../site-tmp/v59-journey/final.ppm");
          const saved_bytes=try std.json.stringifyAlloc(a,try saves.capture(a,state),.{});try saves.write(state,a);var decoded=try saves.read(a);defer decoded.deinit();
          const edited_point=state.selectedPoint;_=state.adjustSelectedWater(@intCast(edited_point),-0.1);std.debug.assert(!std.mem.eql(u8,saved_bytes,try std.json.stringifyAlloc(a,try saves.capture(a,state),.{})));
          try saves.apply(state,decoded.value);std.debug.assert(std.mem.eql(u8,saved_bytes,try std.json.stringifyAlloc(a,try saves.capture(a,state),.{})));
          try saves.apply(state,baseline.value);std.debug.assert(std.mem.eql(u8,frozen,try std.json.stringifyAlloc(a,try saves.capture(a,state),.{})));
          std.debug.print("JOURNEY_PASS native_scripted=true actual_export_actions=true filesystem_save_read_apply_exact=true original_restored=true browser_ui_tested=false\n",.{});
        }
'''+s[b:];p.write_text(s)
p=o/'save_game.zig';s=p.read_text().replace('/saves',str(o.parent/'saves'));p.write_text(s)
# Current production code except inherited explicit native availability/loop/browser-policy seams.
proof={'head':subprocess.check_output(['git','rev-parse','HEAD'],cwd=r,text=True).strip(),'input_sha256':hashlib.sha256((r.parent/'site-tmp/natural60-day60.json').read_bytes()).hexdigest(),'source':{}}
for f in ['states/play.zig','simulation/planet.zig','simulation/microbes.zig','main.zig','save_game.zig']:
 proof['source'][f]={'production':hashlib.sha256((r/'src'/f).read_bytes()).hexdigest(),'qa':hashlib.sha256((o/f).read_bytes()).hexdigest()}
(o.parent/'provenance.json').write_text(json.dumps(proof,indent=2)+'\n')
