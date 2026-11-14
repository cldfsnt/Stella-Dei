#!/usr/bin/env python3
"""Actual earned detritus discovery and camera/pointer acceptance, no assigned fuel."""
from pathlib import Path
import subprocess,sys
root=Path(__file__).resolve().parents[2];out=Path(sys.argv[1])
subprocess.run([sys.executable,str(root/'web/tests/egl-nursery-watch-prepare.py'),str(out)],check=True)
p=out/'main.zig';s=p.read_text();needle='        try originSaveCheck(state,allocator);'
hook=r'''        {
            const saves=@import("save_game.zig");var arena=std.heap.ArenaAllocator.init(allocator);defer arena.deinit();const a=arena.allocator();
            const before=try saves.capture(a,state);const original=try std.json.stringifyAlloc(a,before,.{});
            const time=state.gameTime;const pace=state.timeScale;const paused=state.paused;
            var result=state.findDetritus(true);var calls:usize=1;
            while(result==2){const previous=state.detritusFinder.cursor;result=state.findDetritus(false);calls+=1;std.debug.assert(state.detritusFinder.cursor-previous<=512);std.debug.assert(calls<=(state.planet.microbeCells.len+511)/512);}
            std.debug.assert(result==1 or result==3 or result==4);
            const found=state.selectedPoint;std.debug.assert(state.planet.microbeCells[found].detritus>0);
            state.paused=true;state.update(&game,1.0/60.0);state.paused=paused;std.debug.assert(state.selectedPoint==found);
            const ready=state.previewIgnition(found);std.debug.assert((result==1)==ready.success());if(result==3)std.debug.assert(ready.failure==.wet);
            std.debug.assert(state.planet.getNearestPointTo(state.targetCameraPos)==found);
            std.debug.assert(state.gameTime==time and state.timeScale==pace and state.paused==paused);
            // Camera/display intentionally navigate; every other serialized field stays exact.
            var after=try saves.capture(a,state);after.camera=before.camera;after.camera_target=before.camera_target;after.camera_distance=before.camera_distance;after.target_distance=before.target_distance;after.display_mode=before.display_mode;
            std.debug.assert(std.mem.eql(u8,original,try std.json.stringifyAlloc(a,after,.{})));
            render(window);gl.finish();window.swapBuffers();
            const size=window.getFramebufferSize();var x=@as(f32,@floatFromInt(size.width))/2;var y=@as(f32,@floatFromInt(size.height))/2;
            for(state.colonyTargets.items[0..state.colonyTargets.count])|target|{if(target.cell==found){x=target.x;y=target.y;break;}}
            qa_pointer(x,y,0);state.mousePressed(&game,.left);std.debug.assert(state.selectedPoint==found);
            // Deliberate ordinary Water− taps expose naturally earned fuel; discovery itself changes no resources.
            const wet_bytes=try std.json.stringifyAlloc(a,try saves.capture(a,state),.{});
            const earned_fuel=state.planet.microbeCells[found].detritus;
            const water_before=try a.dupe(f32,state.planet.waterMass);
            var taps:usize=0;
            while(state.planet.waterMass[found]>0){std.debug.assert(taps<10000);std.debug.assert(state.testAction(2));taps+=1;}
            std.debug.assert(state.planet.microbeCells[found].detritus==earned_fuel);
            for(water_before,0..)|mass,i|if(i!=found)std.debug.assert(state.planet.waterMass[i]==mass);
            std.debug.assert(state.previewIgnition(found).success());
            const dry_before=try saves.capture(a,state);const dry_bytes=try std.json.stringifyAlloc(a,dry_before,.{});
            var dry_result=state.findDetritus(true);var dry_calls:usize=1;
            while(dry_result==2){const cursor=state.detritusFinder.cursor;dry_result=state.findDetritus(false);dry_calls+=1;std.debug.assert(state.detritusFinder.cursor-cursor<=512);std.debug.assert(dry_calls<=(state.planet.microbeCells.len+511)/512);}
            std.debug.assert(dry_result==1 and state.selectedPoint==found and state.previewIgnition(found).success());
            var dry_after=try saves.capture(a,state);dry_after.camera=dry_before.camera;dry_after.camera_target=dry_before.camera_target;dry_after.camera_distance=dry_before.camera_distance;dry_after.target_distance=dry_before.target_distance;dry_after.display_mode=dry_before.display_mode;
            std.debug.assert(std.mem.eql(u8,dry_bytes,try std.json.stringifyAlloc(a,dry_after,.{})));
            std.debug.assert(state.gameTime==time and state.timeScale==pace and state.paused==paused);
            const frozen_wet=try std.json.parseFromSlice(saves.schema.Save,a,wet_bytes,.{.allocate=.alloc_always});try saves.apply(state,frozen_wet.value);
            std.debug.assert(std.mem.eql(u8,wet_bytes,try std.json.stringifyAlloc(a,try saves.capture(a,state),.{})));
            std.debug.print("NATURAL_DETRITUS_FIND_DRY result={d} calls={d} selected={d} ordinary_water_minus_taps={d} earned_fuel={d} exact_preview_ready=true discovery_gameplay_unchanged_except_camera=true all_other_water_unchanged=true no_assigned_fuel=true no_ignition=true exact_wet_save_restored=true\n",.{dry_result,dry_calls,found,taps,earned_fuel});
            // A manual selection change during pending search cancels it, never steals selection.
            const pending=state.findDetritus(true);if(pending==2){state.selectedPoint=(state.selectedPoint+1)%state.planet.vertices.len;const manual=state.selectedPoint;std.debug.assert(state.findDetritus(false)==-4);std.debug.assert(state.selectedPoint==manual);}
            // Applying a save invalidates the transient scan even if memory and mesh size are reused.
            _=state.findDetritus(true);const parsed=try std.json.parseFromSlice(saves.schema.Save,a,original,.{.allocate=.alloc_always});try saves.apply(state,parsed.value);std.debug.assert(state.findDetritus(false)==-4);
            std.debug.print("NATURAL_DETRITUS_FIND result={d} calls={d} selected={d} fuel={d} pointer_pick=true camera_framed=true saved_gameplay_unchanged_except_camera=true no_drain_or_ignition=true manual_cancel=true load_cancel=true\n",.{result,calls,found,state.planet.microbeCells[found].detritus});
        }
'''
assert needle in s;s=s.replace(needle,hook+needle,1);p.write_text(s)
