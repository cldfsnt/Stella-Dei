#!/usr/bin/env python3
"""Actual earned feeding discovery, no assigned cohort/feeding records."""
from pathlib import Path
import subprocess,sys
root=Path(__file__).resolve().parents[2];out=Path(sys.argv[1]);subprocess.run([sys.executable,str(root/'web/tests/egl-nursery-prepare.py'),str(out)],check=True)
p=out/'main.zig';s='extern fn qa_capture(path:[*:0]const u8) void;\n'+p.read_text();n='    originReport("empty",state);';assert n in s;s=s.replace(n,n+r'''
    {var empty=state.findRecordedFeeding(true);var chunks:usize=1;while(empty==2){empty=state.findRecordedFeeding(false);chunks+=1;std.debug.assert(chunks<=81);}std.debug.assert(empty==0);std.debug.print("FEEDING_EMPTY result=0 chunks={d} no_assigned_history=true\n",.{chunks});}
''',1)
n='        try originSaveCheck(state,allocator);';h=r'''        {
            const saves=@import("save_game.zig");var arena=std.heap.ArenaAllocator.init(allocator);defer arena.deinit();const a=arena.allocator();
            const before=try saves.capture(a,state);const original=try std.json.stringifyAlloc(a,before,.{});const paused=state.paused;
            var result=state.findRecordedFeeding(true);var calls:usize=1;
            while(result==2){const old=state.feedingFinder.cursor;result=state.findRecordedFeeding(false);calls+=1;std.debug.assert(state.feedingFinder.cursor-old<=512);std.debug.assert(calls<=81);}
            std.debug.assert(result==1);const found=state.selectedPoint;const feeding_match=@import("feeding_discovery.zig").recorded(state.planet.microbeCells[found]).?;
            state.paused=true;state.update(&game,1.0/60.0);state.paused=paused;std.debug.assert(state.selectedPoint==found);
            std.debug.assert(state.planet.getNearestPointTo(state.targetCameraPos)==found);
            const snap=try std.json.parseFromSlice(std.json.Value,a,std.mem.span(lifeSnapshotForState(state)),.{});
            std.debug.assert(snap.value.object.get("cell").?.integer==found);var snapshot_found=false;
            for(snap.value.object.get("cohorts").?.array.items)|co|{if(co.object.get("lineage").?.integer==feeding_match.lineage){snapshot_found=true;std.debug.assert(co.object.get("lifetime_grazed").?.float>0);}}
            std.debug.assert(snapshot_found);
            var after=try saves.capture(a,state);after.camera=before.camera;after.camera_target=before.camera_target;after.camera_distance=before.camera_distance;after.target_distance=before.target_distance;after.display_mode=before.display_mode;
            std.debug.assert(std.mem.eql(u8,original,try std.json.stringifyAlloc(a,after,.{})));
            render(window);gl.finish();window.swapBuffers();if(std.posix.getenv("STELLA_FEEDING_SCREENSHOT"))|path|{const z=try a.dupeZ(u8,path);qa_capture(z);}
            const size=window.getFramebufferSize();var x=@as(f32,@floatFromInt(size.width))/2;var y=@as(f32,@floatFromInt(size.height))/2;
            for(state.colonyTargets.items[0..state.colonyTargets.count])|target|if(target.cell==found){x=target.x;y=target.y;break;};
            qa_pointer(x,y,0);state.mousePressed(&game,.left);std.debug.assert(state.selectedPoint==found);
            const pending=state.findRecordedFeeding(true);std.debug.assert(pending==2);state.selectedPoint=(found+1)%state.planet.vertices.len;std.debug.assert(state.findRecordedFeeding(false)==-4);
            _=state.findRecordedFeeding(true);const frozen=try std.json.parseFromSlice(saves.schema.Save,a,original,.{.allocate=.alloc_always});try saves.apply(state,frozen.value);std.debug.assert(state.findRecordedFeeding(false)==-4);
            std.debug.assert(std.mem.eql(u8,original,try std.json.stringifyAlloc(a,try saves.capture(a,state),.{})));
            std.debug.print("NATURAL_FEEDING_FIND result={d} calls={d} selected={d} lineage={d} intake={d} actual_snapshot_matches=true next_paused_update_retains_target=true pointer_pick=true save_unchanged_except_camera=true original_restored=true manual_and_load_cancel=true\n",.{result,calls,found,feeding_match.lineage,feeding_match.intake});
        }
''';assert n in s;s=s.replace(n,h+n,1);p.write_text(s)
