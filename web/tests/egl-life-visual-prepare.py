#!/usr/bin/env python3
"""Isolated, paused actual Origin seed; baseline toggle affects visuals only.
Read-only web exports are exposed to native EGL by a test-only platform guard.
"""
from pathlib import Path
import subprocess,sys
root=Path(__file__).resolve().parents[2]
out=Path(sys.argv[1] if len(sys.argv)>1 else '/tmp/stella-life-compare-src')
subprocess.run([sys.executable,str(root/'web/tests/egl-origin-menu-prepare.py'),str(out)],check=True)
hook=r'''            if (frame == 25) { _ = state.testAction(3); }
            const cellsBefore = std.hash.Wyhash.hash(0, std.mem.sliceAsBytes(state.planet.microbeCells));
            const statsBefore = state.planet.microbeStats;
            const oxygenBefore = state.planet.averageOxygenMass;
            const carbonBefore = state.planet.averageCarbonDioxideMass;
            const timeBefore = state.gameTime;
            const pointBefore = state.selectedPoint;
            const snapshot = std.mem.span(stella_life_snapshot());
            std.debug.assert(cellsBefore == std.hash.Wyhash.hash(0, std.mem.sliceAsBytes(state.planet.microbeCells)));
            std.testing.expectEqualDeep(statsBefore, state.planet.microbeStats) catch unreachable;
            std.debug.assert(oxygenBefore == state.planet.averageOxygenMass and carbonBefore == state.planet.averageCarbonDioxideMass);
            std.debug.assert(timeBefore == state.gameTime and pointBefore == state.selectedPoint);
            std.debug.print("LIFE_EXPORT_UNCHANGED PASS\n", .{});
            const parsed = std.json.parseFromSlice(std.json.Value, game.allocator, snapshot, .{}) catch unreachable;
            defer parsed.deinit();
            std.debug.assert(parsed.value.object.get("cohorts").?.array.items.len == 4);
            std.debug.assert(parsed.value.object.get("movement_reasons").?.array.items.len == 4);
            var saved: [4096]u8 = undefined;
            @memcpy(saved[0..snapshot.len], snapshot);
            const oldLight = state.stableDaylight;
            state.stableDaylight = !oldLight;
            const again = std.mem.span(stella_life_snapshot());
            std.debug.assert(std.mem.eql(u8, saved[0..snapshot.len], again));
            state.stableDaylight = oldLight;
            std.debug.print("LIGHT_VIEW_INDEPENDENT PASS\nLIFE_SNAPSHOT={s}\n", .{snapshot});
'''
p=out/'main.zig'
p.write_text(p.read_text().replace('            const i = state.selectedPoint;',hook+'            const i = state.selectedPoint;').replace('if (!is_web or !web_initialized or !game.state_init) return null;', 'if (!game.state_init) return null; // Test-only native read-only export bridge.'))
p=out/'states/play.zig'
s=p.read_text().replace('var randomPrng = std.rand.DefaultPrng.init(@as(u64, @bitCast(std.time.milliTimestamp())));','var randomPrng = std.rand.DefaultPrng.init(20261113);')
s=s.replace('program.setUniformBool("compactSelection", true);','program.setUniformBool("compactSelection", std.posix.getenv("STELLA_VISUAL_BASELINE") == null);')
s=s.replace('if (self.pointerOnPlanet and !self.cameraInputBlocked()) {','if (std.posix.getenv("STELLA_VISUAL_BASELINE") == null and self.pointerOnPlanet and !self.cameraInputBlocked()) {')
s=s.replace('const size = if (origin) 12 + 16 *','const size = if (origin) (if (std.posix.getenv("STELLA_VISUAL_BASELINE") == null) @as(f32,12) else 5) + 16 *')
p.write_text(s)
