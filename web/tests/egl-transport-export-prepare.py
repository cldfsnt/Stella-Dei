#!/usr/bin/env python3
"""Real exports through isolated native availability bridge, not browser DOM QA."""
from pathlib import Path
import subprocess,sys
root=Path(__file__).resolve().parents[2];out=Path(sys.argv[1])
subprocess.run([sys.executable,str(root/'web/tests/egl-ecology-pulse-prepare.py'),str(out)],check=True)
p=out/'main.zig';s=p.read_text();start=s.index('          var found=state.findRecordedFeeding(true);');end=s.index('\n        try originSaveCheck',start)
s=s[:start]+r'''
          _=pw;_=pm;const from:usize=12344;const dest:usize=13594;const slot:usize=3;
          state.selectedPoint=from;state.paused=true;state.timeScale=21600;state.showEscapeMenu=false;state.showPointDetails=false;state.showPlanetControl=false;
          state.watchLife();state.targetCameraPos=state.planet.transformedPoints[from];_=state.fitLivingClusterResult(390,700);render(window);gl.finish();window.swapBuffers();
          const co=state.planet.microbeCells[from].cohorts[slot];std.debug.assert(co.lineage==120 and co.support_mass>0);
          const frozen=try std.json.stringifyAlloc(a,try saves.capture(a,state),.{});const baseline=try std.json.parseFromSlice(saves.schema.Save,a,frozen,.{.allocate=.alloc_always});
          const options=try std.json.parseFromSlice(std.json.Value,a,std.mem.span(stella_transport_options()),.{.allocate=.alloc_always});std.debug.assert(options.value.object.get("available").?.bool);
          var has_source=false;for(options.value.object.get("sources").?.array.items)|o|if(std.mem.eql(u8,o.object.get("id").?.string,"120")){has_source=true;std.debug.assert(o.object.get("slot").?.integer==3);};std.debug.assert(has_source);
          var has_neighbor=false;for(options.value.object.get("neighbors").?.array.items)|o|if(o.object.get("cell").?.integer==dest){has_neighbor=true;};std.debug.assert(has_neighbor);
          std.debug.assert(std.mem.eql(u8,frozen,try std.json.stringifyAlloc(a,try saves.capture(a,state),.{})));
          for(0..8)|case|{
            try saves.apply(state,baseline.value);state.selectedPoint=from;
            const preview=try std.json.parseFromSlice(std.json.Value,a,std.mem.span(stella_transport_prepare(PerformanceDetails.world_serial,@intCast(from),@intCast(slot),@intCast(dest),"120")),.{.allocate=.alloc_always});std.debug.assert(preview.value.object.get("ok").?.bool);const token:u32=@intCast(preview.value.object.get("token").?.integer);
            std.debug.assert(std.mem.eql(u8,frozen,try std.json.stringifyAlloc(a,try saves.capture(a,state),.{})));
            switch(case){0=>state.selectedPoint=dest,1=>state.paused=false,2=>state.gameTime+=1,3=>state.planet.microbeCells[from].nutrient+=0.001,4=>state.planet.temperature[dest]+=1,5=>stella_transport_cancel(),6=>{try saves.apply(state,baseline.value);state.selectedPoint=from;},else=>{}}
            const immediate=try std.json.stringifyAlloc(a,try saves.capture(a,state),.{});
            const refused=try std.json.parseFromSlice(std.json.Value,a,std.mem.span(stella_transport_execute(if(case==7)token+1 else token)),.{.allocate=.alloc_always});std.debug.assert(!refused.value.object.get("ok").?.bool);
            std.debug.assert(std.mem.eql(u8,immediate,try std.json.stringifyAlloc(a,try saves.capture(a,state),.{})));
          }
          try saves.apply(state,baseline.value);state.selectedPoint=from;
          const stale=try std.json.parseFromSlice(std.json.Value,a,std.mem.span(stella_transport_prepare(PerformanceDetails.world_serial+%1,@intCast(from),@intCast(slot),@intCast(dest),"120")),.{});std.debug.assert(!stale.value.object.get("ok").?.bool);
          const preview=try std.json.parseFromSlice(std.json.Value,a,std.mem.span(stella_transport_prepare(PerformanceDetails.world_serial,@intCast(from),@intCast(slot),@intCast(dest),"120")),.{.allocate=.alloc_always});std.debug.assert(preview.value.object.get("ok").?.bool);const token:u32=@intCast(preview.value.object.get("token").?.integer);
          std.debug.assert(std.mem.eql(u8,frozen,try std.json.stringifyAlloc(a,try saves.capture(a,state),.{})));
          render(window);gl.finish();window.swapBuffers();qa_capture("/workspace/scratch/f67c3ac60ca3/site-tmp/transport-export/before.ppm");
          var before_dest_visible=false;for(state.colonyTargets.items[0..state.colonyTargets.count])|target|if(target.cell==dest){before_dest_visible=true;};std.debug.assert(!before_dest_visible);
          const arrivals=state.planet.propaguleArrivals;const attempts=state.planet.propaguleAttempts;const losses=state.planet.propaguleTrackedLosses;
          const committed=try std.json.parseFromSlice(std.json.Value,a,std.mem.span(stella_transport_execute(token)),.{.allocate=.alloc_always});std.debug.assert(committed.value.object.get("ok").?.bool and committed.value.object.get("manual").?.bool);std.debug.assert(std.mem.eql(u8,committed.value.object.get("id").?.string,"120"));
          std.debug.assert(state.paused and state.timeScale==21600 and state.selectedPoint==from and state.planet.propaguleArrivals==arrivals and state.planet.propaguleAttempts==attempts and state.planet.propaguleTrackedLosses==losses);
          const inspectFrozen=try std.json.stringifyAlloc(a,try saves.capture(a,state),.{});
          for(0..2)|wrong|{const denied=try std.json.parseFromSlice(std.json.Value,a,std.mem.span(stella_transport_inspect(if(wrong==0)PerformanceDetails.world_serial+%1 else PerformanceDetails.world_serial,@intCast(dest),if(wrong==1) "121" else "120")),.{});std.debug.assert(!denied.value.object.get("ok").?.bool and state.selectedPoint==from);std.debug.assert(std.mem.eql(u8,inspectFrozen,try std.json.stringifyAlloc(a,try saves.capture(a,state),.{})));}
          const inspectedReceipt=try std.json.parseFromSlice(std.json.Value,a,std.mem.span(stella_transport_inspect(PerformanceDetails.world_serial,@intCast(dest),"120")),.{});std.debug.assert(inspectedReceipt.value.object.get("ok").?.bool and state.selectedPoint==dest);std.debug.assert(std.mem.eql(u8,inspectFrozen,try std.json.stringifyAlloc(a,try saves.capture(a,state),.{})));
          const directSnapshot=try std.json.parseFromSlice(std.json.Value,a,std.mem.span(stella_life_snapshot()),.{});var directFound=false;for(directSnapshot.value.object.get("cohorts").?.array.items)|member|if(member.object.get("lineage").?.integer==120){directFound=true;std.debug.assert(@as(f32,@floatCast(member.object.get("support_mass").?.float))==co.support_mass);};std.debug.assert(directFound);
          state.selectedPoint=from;
          std.debug.print("TRANSPORT_INSPECT explicit_button_path=true no_globe_tap_required=true wrong_world_id_refused=true saved_state_camera_exact=true id_support_verified=true\n",.{});
          render(window);gl.finish();window.swapBuffers();qa_capture("/workspace/scratch/f67c3ac60ca3/site-tmp/transport-export/after.ppm");
          var destination_pick=false;for(state.colonyTargets.items[0..state.colonyTargets.count])|target|if(target.cell==dest){qa_pointer(target.x,target.y,0);state.mousePressed(&game,.left);destination_pick=true;break;};std.debug.assert(destination_pick and state.selectedPoint==dest);
          const inspect=try std.json.parseFromSlice(std.json.Value,a,std.mem.span(stella_life_snapshot()),.{});std.debug.assert(inspect.value.object.get("cell").?.integer==dest);
          var inspected=false;for(inspect.value.object.get("cohorts").?.array.items)|member|if(member.object.get("lineage").?.integer==120){inspected=true;};std.debug.assert(inspected);
          std.debug.assert(state.planet.microbeCells[from].cohorts[slot].biomass==0 and state.gameTime==baseline.value.game_time);
          std.debug.print("TRANSPORT_VISIBLE paused_zero_ticks=true new_destination_glyph=true actual_glyph_pick=true inspect_id120=true donor_slot_empty=true\n",.{});
          state.selectedPoint=from;
          const moved=try std.json.stringifyAlloc(a,try saves.capture(a,state),.{});
          const duplicate=try std.json.parseFromSlice(std.json.Value,a,std.mem.span(stella_transport_execute(token)),.{});std.debug.assert(!duplicate.value.object.get("ok").?.bool);std.debug.assert(std.mem.eql(u8,moved,try std.json.stringifyAlloc(a,try saves.capture(a,state),.{})));
          try saves.apply(state,baseline.value);state.planet.microbeCells[from].cohorts[slot]=.{};var moved_slot:?usize=null;for(state.planet.microbeCells[dest].cohorts,0..)|c,j|if(c.biomass==0){moved_slot=j;break;};state.planet.microbeCells[dest].cohorts[moved_slot.?]=co;
          std.debug.assert(std.mem.eql(u8,moved,try std.json.stringifyAlloc(a,try saves.capture(a,state),.{})));
          const saved=try std.json.parseFromSlice(saves.schema.Save,a,moved,.{.allocate=.alloc_always});try saves.apply(state,saved.value);std.debug.assert(std.mem.eql(u8,moved,try std.json.stringifyAlloc(a,try saves.capture(a,state),.{})));
          std.debug.assert(std.meta.eql(co,state.planet.microbeCells[dest].cohorts[moved_slot.?]));state.selectedPoint=dest;state.watchLife();state.targetCameraPos=state.planet.transformedPoints[dest];_=state.fitLivingClusterResult(390,700);render(window);gl.finish();window.swapBuffers();
          std.debug.print("TRANSPORT_EXPORT id=120 source=12344 target=13594 options_preview_commit=true preview_save_exact=true exact_two_slots=true roundtrip_identity=true natural_counters_unchanged=true pause_speed_preserved=true stale_cases=9 duplicate_refused=true mass={d} support={d} credit={d} native_bridge_only=true\n",.{co.biomass,co.support_mass,co.reproduction_credit});
        }
''' +s[end:];old='if (!is_web or !web_initialized or !game.state_init) return null;';assert old in s;s=s.replace(old,'if (!game.state_init) return null; // Isolated native export availability bridge only.');p.write_text(s)
