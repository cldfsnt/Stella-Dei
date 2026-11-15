#!/usr/bin/env python3
"""Actual exported post-seeding player journey, isolated native QA only."""
from pathlib import Path
import subprocess,sys,json,hashlib
r=Path(__file__).resolve().parents[2];o=Path(sys.argv[1]).resolve()
subprocess.run([sys.executable,str(r/'web/tests/egl-auto-seed-prepare.py'),str(o)],check=True)
p=o/'main.zig';s=p.read_text();a=s.index('          _=pm;_=pw;');b=s.index('\n        std.debug.print("AUTO_SEED_GATE',a)
s=s[:a]+r'''
          _=pm;_=pw;state.paused=true;state.showEscapeMenu=false;state.showPointDetails=false;state.showPlanetControl=false;state.selectedTool=.None;web_initialized=true;
          const original=try std.json.stringifyAlloc(a,try saves.capture(a,state),.{});const initial=try std.json.parseFromSlice(saves.schema.Save,a,original,.{.allocate=.alloc_always});
          const start_time=state.gameTime;const pace=state.timeScale;
          const begun=try std.json.parseFromSlice(std.json.Value,a,std.mem.span(stella_advance_start(PerformanceDetails.world_serial)),.{});std.debug.assert(begun.value.object.get("ok").?.bool);
          for(0..60)|_|{loop.pump(16);std.debug.assert(advanceFrame(0.016));}
          std.debug.assert(AdvanceDay.current.completed==60 and AdvanceDay.current.phase==.done and state.gameTime==start_time+86400 and state.paused and state.timeScale==pace);
          std.debug.print("JOURNEY_ADVANCE {s}\n",.{std.mem.span(stella_advance_status())});
          _=stella_advance_dismiss(AdvanceDay.current.token);qa_pointer(20,20,0);_=advanceFrame(0.016);std.debug.assert(!AdvanceDay.blocksInput());
          const after_day=try std.json.stringifyAlloc(a,try saves.capture(a,state),.{});
          var census=try std.json.parseFromSlice(std.json.Value,a,std.mem.span(stella_world_ecology(1)),.{.allocate=.alloc_always});var chunks:usize=1;
          while(std.mem.eql(u8,census.value.object.get("status").?.string,"pending")){std.debug.assert(chunks<100);census=try std.json.parseFromSlice(std.json.Value,a,std.mem.span(stella_world_ecology(0)),.{.allocate=.alloc_always});chunks+=1;}
          std.debug.assert(std.mem.eql(u8,census.value.object.get("status").?.string,"ready"));
          var live:usize=0;for(state.planet.microbeCells)|cell|for(cell.cohorts)|co|{if(co.biomass>0 and co.lineage>0)live+=1;};std.debug.assert(census.value.object.get("colonies").?.integer==live);
          std.debug.assert(std.mem.eql(u8,after_day,try std.json.stringifyAlloc(a,try saves.capture(a,state),.{})));
          std.debug.print("JOURNEY_CENSUS chunks={} exact_live={} response={s}\n",.{chunks,live,try std.json.stringifyAlloc(a,census.value,.{})});
          const prior_selected=state.selectedPoint;const prior_clicked=state.clickedPoint;
          std.debug.assert(state.findLivingClusterResult(100,100)==-3 and state.selectedPoint==prior_selected and state.clickedPoint==prior_clicked);
          const found=stella_find_life();std.debug.assert(found==1);const previous_selection=state.selectedPoint;
          std.debug.assert(state.colonyPeek.cell!=null and state.colonyPeek.cell.?==previous_selection and state.selectedTool==.None);
          const immediate=try std.json.parseFromSlice(std.json.Value,a,std.mem.span(stella_life_snapshot()),.{});std.debug.assert(immediate.value.object.get("cell").?.integer==previous_selection);
          var valid_identity=false;for(immediate.value.object.get("identities").?.array.items)|identity|{if(identity.object.get("living").?.bool)valid_identity=true;}std.debug.assert(valid_identity);
          const before_local=state.selectedPoint;_=state.fitLivingClusterResult(390,700);std.debug.assert(state.selectedPoint==before_local);
          var observational=try saves.capture(a,state);const prior_day=try std.json.parseFromSlice(saves.schema.Save,a,after_day,.{.allocate=.alloc_always});
          observational.camera=prior_day.value.camera;observational.camera_target=prior_day.value.camera_target;observational.camera_distance=prior_day.value.camera_distance;observational.target_distance=prior_day.value.target_distance;
          std.debug.assert(std.mem.eql(u8,after_day,try std.json.stringifyAlloc(a,observational,.{})));
          std.debug.print("JOURNEY_DIRECT_INSPECT living=true cell={} failure_preserved=true local_fit_preserved=true camera_only_save_difference=true\n",.{previous_selection});
          std.debug.print("JOURNEY_FIND cell={} snapshot={s}\n",.{previous_selection,std.mem.span(stella_life_snapshot())});
          for(0..40)|_|{state.update(&game,0);render(window);gl.finish();window.swapBuffers();}
          qa_capture("OUTPUT/found.ppm");
          std.debug.assert(state.colonyTargets.count>0);const first_hit=state.colonyTargets.items[0];qa_pointer(first_hit.x,first_hit.y,0);state.mousePressed(&game,.left);const selected=state.selectedPoint;
          std.debug.assert(state.colonyPeek.cell!=null and state.colonyPeek.cell.?==selected);
          std.debug.print("JOURNEY_EXPLICIT_PICK previous={} selected={} glyphs={}\n",.{previous_selection,selected,state.visibleSprouts});
          var parent_id:u64=0;for(state.planet.microbeCells[selected].cohorts)|co|{if(co.biomass>0 and co.lineage>0){parent_id=co.lineage;break;}}std.debug.assert(parent_id>0);
          var expected_children:usize=0;for(state.planet.microbeCells)|cell|for(cell.cohorts)|co|{if(co.biomass>0 and co.lineage>0 and co.parent==parent_id)expected_children+=1;};
          const id=try std.fmt.allocPrintZ(a,"{d}",.{parent_id});var offspring=stella_find_offspring(1,PerformanceDetails.world_serial,@intCast(selected),id);var scans:usize=1;
          while(offspring==2){std.debug.assert(scans<100);offspring=stella_find_offspring(0,PerformanceDetails.world_serial,@intCast(selected),id);scans+=1;}
          std.debug.print("JOURNEY_OFFSPRING parent={} source={} expected_living_children={} result={} chunks={} target={} snapshot={s}\n",.{parent_id,selected,expected_children,offspring,scans,state.selectedPoint,std.mem.span(stella_life_snapshot())});
          std.debug.assert(if(expected_children>0)offspring==1 else offspring==0);
          for(0..40)|_|{state.update(&game,0);render(window);gl.finish();window.swapBuffers();}qa_capture("OUTPUT/offspring.ppm");
          var picked=false;for(state.colonyTargets.items[0..state.colonyTargets.count])|hit|{if(hit.cell==state.selectedPoint){qa_pointer(hit.x,hit.y,0);state.mousePressed(&game,.left);picked=state.colonyPeek.cell!=null and state.colonyPeek.cell.?==hit.cell;break;}}
          std.debug.print("JOURNEY_INSPECT selected={} glyphs={} picked={} snapshot={s}\n",.{state.selectedPoint,state.visibleSprouts,picked,std.mem.span(stella_life_snapshot())});
          const saved=try saves.capture(a,state);const bytes=try std.json.stringifyAlloc(a,saved,.{});const own=try std.json.parseFromSlice(saves.schema.Save,a,bytes,.{.allocate=.alloc_always});try saves.apply(state,own.value);std.debug.assert(std.mem.eql(u8,bytes,try std.json.stringifyAlloc(a,try saves.capture(a,state),.{})));
          try saves.apply(state,initial.value);std.debug.assert(std.mem.eql(u8,original,try std.json.stringifyAlloc(a,try saves.capture(a,state),.{})));
          std.debug.print("JOURNEY_PASS advance60=true census_exact=true roundtrip=true original_restored=true actual_browser=false\n",.{});
        }
'''.replace('OUTPUT',str(o.parent))+s[b:];p.write_text(s)
subprocess.run([sys.executable,str(r/'web/tests/audit-zig-exports.py'),str(r/'src/main.zig'),str(p)],check=True,stdout=(o.parent/'journey-export-audit.json').open('w'))
(o.parent/'journey-provenance.json').write_text(json.dumps({'head':subprocess.check_output(['git','rev-parse','HEAD'],cwd=r,text=True).strip(),'input_sha256':hashlib.sha256((r.parent/'site-tmp/auto-seed/after.json').read_bytes()).hexdigest(),'source':{str(f.relative_to(o)):hashlib.sha256(f.read_bytes()).hexdigest()for f in o.rglob('*.zig')}},indent=2))
