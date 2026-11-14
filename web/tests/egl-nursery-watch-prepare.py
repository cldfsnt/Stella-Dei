#!/usr/bin/env python3
"""Actual coupled nursery followed by read-only Find and rendered-cell inspection.
No assigned biology. Uses normal starter APIs, then unchanged update scheduling.
"""
from pathlib import Path
import subprocess,sys
root=Path(__file__).resolve().parents[2];out=Path(sys.argv[1])
subprocess.run([sys.executable,str(root/'web/tests/egl-nursery-prepare.py'),str(out)],check=True)
p=out/'main.zig';s=p.read_text()
needle='        try originSaveCheck(state,allocator);'
assert needle in s
hook=r'''        {
            const before_time=state.gameTime;const before_pace=state.timeScale;const before_pause=state.paused;
            const saves=@import("save_game.zig");
            var audit_arena=std.heap.ArenaAllocator.init(allocator);defer audit_arena.deinit();const aa=audit_arena.allocator();
            const saved=try saves.capture(aa,state);const bytes=try std.json.stringifyAlloc(aa,saved,.{});
            const size=window.getFramebufferSize();
            const find_result=state.findLivingClusterResult(@floatFromInt(size.width),@floatFromInt(size.height));
            std.debug.print("NATURAL_WATCH find_result={d} seeded_once=true biology_assigned=false\n",.{find_result});
            std.debug.assert(find_result==1);
            std.debug.assert(state.gameTime==before_time and state.timeScale==before_pace and state.paused==before_pause);
            render(window);gl.finish();window.swapBuffers();
            const visible=state.colonyTargets;
            std.debug.assert(visible.count>0);
            var checked:usize=0;
            for(visible.items[0..visible.count])|target|{
                qa_pointer(target.x,target.y,0);state.mousePressed(&game,.left);
                std.debug.assert(state.selectedPoint==target.cell and state.colonyPeek.cell.?==target.cell);
                checked+=1;
            }
            // Observation changes camera/selection only; exact biological arrays stay unchanged.
            const after=try saves.capture(aa,state);
            std.debug.assert(std.mem.eql(u8,try std.json.stringifyAlloc(aa,saved.origin,.{}),try std.json.stringifyAlloc(aa,after.origin,.{})));
            _=bytes;
            std.debug.print("NATURAL_WATCH rendered_targets={d} exact_root_picks={d} biology_unchanged=true\n",.{visible.count,checked});
            // Same target internals used by stella_god_target, without native web-state substitution.
            const preview_before=try std.json.stringifyAlloc(aa,try saves.capture(aa,state),.{});
            const Actions=@import("god_actions.zig");const patch=state.selectedPoint;
            const capacity=state.planet.currentHeatCapacity(patch);
            const wave_preview=Actions.previewWave(&state.planet,patch,patch);
            const heat_preview=Actions.previewLightning(&state.planet,patch,patch,capacity);
            const scorch_preview=Actions.previewScorch(&state.planet,patch,patch,capacity);
            std.debug.assert(wave_preview.success() and heat_preview.success());
            std.debug.assert(scorch_preview.failure==.origin and !scorch_preview.success());
            std.debug.assert(wave_preview.moved_mass>0 and heat_preview.heat_joules>0);
            std.debug.assert(std.mem.eql(u8,preview_before,try std.json.stringifyAlloc(aa,try saves.capture(aa,state),.{})));
            std.debug.assert(state.gameTime==before_time and state.timeScale==before_pace and state.paused==before_pause);
            std.debug.print("NATURAL_GOD_PREVIEW selected={d} wave={s} lightning={s} scorch={s} water_m={d} heat_capacity={d} exact_save_unchanged=true time_pace_pause_unchanged=true\n",.{patch,@tagName(wave_preview.failure),@tagName(heat_preview.failure),@tagName(scorch_preview.failure),state.planet.waterMass[patch]*state.planet.getKmPerWaterMass()*1000,capacity});
            originReport("natural_nursery_watch",state);
        }
'''
s=s.replace(needle,hook+needle,1);p.write_text(s)
