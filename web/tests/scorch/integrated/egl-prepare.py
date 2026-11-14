#!/usr/bin/env python3
"""Create a temporary source copy for graphics QA, never modify production.
Adaptations: enter PlayState directly; miniaudio offline/no device engine.
The real renderer, shaders, planet generation and simulation remain unchanged.
Native desktop rendering is not browser/mobile/WebGL conformance evidence.
"""
from pathlib import Path
import shutil
import sys
root = Path(__file__).resolve().parents[2]
out = Path(next((arg for arg in sys.argv[1:] if not arg.startswith("--")), "/tmp/stella-egl-src"))
shutil.copytree(root/'src',out,dirs_exist_ok=True)
p=out/'main.zig'
s=p.read_text().replace('nosuspend game.setState(MainMenuState);','nosuspend game.setState(PlayState);').replace('nosuspend game.setState(SplashScreenState);','nosuspend game.setState(PlayState);')
p.write_text(s)
p=out/'audio.zig'
s=p.read_text().replace('if (c.ma_engine_init(null, engine)', 'var config = c.ma_engine_config_init();\n        config.noDevice = c.MA_TRUE;\n        config.channels = 2;\n        config.sampleRate = 48000;\n        if (c.ma_engine_init(&config, engine)')
p.write_text(s)
if '--mobile' in sys.argv:
    p=out/'states/play.zig'
    s=p.read_text().replace('@import("builtin").target.cpu.arch == .wasm32', 'true').replace('@import("builtin").target.cpu.arch != .wasm32', 'false')
    if '--paused' in sys.argv:
        s=s.replace('paused: bool = false', 'paused: bool = true')
    p.write_text(s)
p=out/'main.zig'
p.write_text(p.read_text()+r'''
pub export fn egl_trace(frame: c_int) void {
    if (!game.state_init) return;
    switch (game.state) {
        .Playing => |*state| {
            const i = state.selectedPoint;
            std.debug.print("QA frame={d} selected={d} elevation={d} water={d} vegetation={d} rabbits={d} time={d} paused={} tool={s} camera={d}\n", .{frame, i, state.planet.elevation[i], state.planet.waterMass[i], state.planet.vegetation[i], state.planet.lifeforms.items.len, state.gameTime, state.paused, @tagName(state.selectedTool), state.cameraDistance});
        },
        else => {},
    }
}
''')
print(out/'main.zig')

if '--ecosystem' in sys.argv:
    p=out/'states/play.zig'
    p.write_text(p.read_text().replace('var randomPrng = std.rand.DefaultPrng.init(@as(u64, @bitCast(std.time.milliTimestamp())));', 'var randomPrng = std.rand.DefaultPrng.init(20261113);'))
    p=out/'main.zig'
    s=p.read_text().replace('dt = dt * 0.9 + fullLoopTime * 0.1;', 'dt = 1.0 / 144.0 + fullLoopTime * 0;')
    marker='            const i = state.selectedPoint;'
    hook=r'''            if (frame == 75) {
                const selected = state.selectedPoint;
                const height = state.planet.elevation[selected];
                const raised = state.testAction(5);
                const higher = state.planet.elevation[selected] > height;
                const lowered = state.testAction(6);
                const restored = @abs(state.planet.elevation[selected] - height) < 0.001;
                const emitted = state.testAction(1);
                const wet = state.planet.waterMass[selected] > 0;
                const drained = state.testAction(2);
                const dry = state.planet.waterMass[selected] == 0;
                std.debug.print("TOOLS same vertex={d} raise={} lower={} addwater={} drain={}\n", .{selected,raised and higher,lowered and restored,emitted and wet,drained and dry});
            }
            if (frame >= 76 and frame <= 85) {
                state.paused = false;
                state.timeScale = 86400;
                state.selectedTool = .None;
                // Half a simulated day, using actual full update (climate,
                // water, plants and animals). No forced births or counter edits.
                const goal = state.gameTime + 43200;
                while (state.gameTime < goal) std.time.sleep(1_000_000);
                state.paused = true;
                std.time.sleep(50_000_000);
                render(game.window);
            }
            var biomass: f64 = 0;
            var cells: usize = 0;
            var max_veg: f32 = 0;
            var temp_min: f32 = 10000;
            var temp_max: f32 = 0;
            var trait_min: f32 = 1000;
            var trait_max: f32 = 0;
            for (state.planet.vegetation, state.planet.plantTraits, state.planet.temperature) |v, trait, temp| {
                biomass += v;
                max_veg = @max(max_veg, v);
                if (v > 0.001) { temp_min=@min(temp_min,temp); temp_max=@max(temp_max,temp); cells += 1; trait_min = @min(trait_min, trait.optimum); trait_max = @max(trait_max, trait.optimum); }
            }
            if (cells == 0) std.debug.print("HABITAT no vegetated cells\n", .{}) else std.debug.print("HABITAT temperatures={d:.2}..{d:.2}C\n",.{temp_min-273.15,temp_max-273.15});
            std.debug.print("ECO frame={d} days={d:.3} biomass={d:.3} cells={d} maxCover={d:.3} generation={d} traits={d:.3}..{d:.3} rabbits={d} births={d} meals={d} deaths={d}\n", .{frame,state.gameTime/86400,biomass,cells,max_veg,state.planet.plantGenerations,trait_min,trait_max,state.planet.lifeforms.items.len,state.planet.rabbitBirths,state.planet.rabbitMeals,state.planet.rabbitDeaths});
'''
    p.write_text(s.replace(marker,hook+marker))
if '--ecosystem' in sys.argv:
    p=out/'main.zig'
    s=p.read_text().replace('            const i = state.selectedPoint;', '            if (frame == 85) qa_roundtrip(state) catch |err| std.debug.print("ROUNDTRIP FAILED {s}\\n", .{@errorName(err)});\n            const i = state.selectedPoint;')
    s += r'''
fn qa_roundtrip(state: *PlayState) !void {
    const saves = @import("save_game.zig");
    var arena = std.heap.ArenaAllocator.init(game.allocator);
    defer arena.deinit();
    const a = arena.allocator();
    const before = try saves.capture(a, state);
    const bytes = try std.json.stringifyAlloc(a, before, .{});
    try std.fs.cwd().writeFile(.{.sub_path="/tmp/stella-day5-save.json", .data=bytes});
    const parsed = try saves.schema.parse(a, bytes);
    // Delete living content to ensure apply restores rather than merely succeeds.
    @memset(state.planet.vegetation, 0);
    state.planet.lifeforms.clearRetainingCapacity();
    state.planet.rabbitBirths = 0;
    state.planet.rabbitMeals = 0;
    try saves.apply(state, parsed.value);
    const after = try saves.capture(a, state);
    const restored = try std.json.stringifyAlloc(a, after, .{});
    if (!std.mem.eql(u8, bytes, restored)) return error.RoundtripMismatch;
    std.debug.print("ROUNDTRIP PASS exact JSON restored {d} bytes, {d} rabbits, {d} births, {d} meals\n", .{bytes.len, state.planet.lifeforms.items.len, state.planet.rabbitBirths, state.planet.rabbitMeals});
}
'''
    p.write_text(s)

# Optional longer full-world soak; keeps the same ten observation/capture points.
soak_days = next((float(arg.split("=", 1)[1]) for arg in sys.argv if arg.startswith("--soak-days=")), None)
if soak_days is not None:
    if "--ecosystem" not in sys.argv or not 1 <= soak_days <= 100:
        raise SystemExit("--soak-days=1..100 requires --ecosystem")
    p = out / "main.zig"
    s = p.read_text().replace("state.gameTime + 43200", f"state.gameTime + {int(soak_days * 86400 / 10)}")
    s = s.replace("/tmp/stella-day5-save.json", f"/tmp/stella-day{soak_days:g}-save.json")
    s = s.replace("            var biomass: f64 = 0;", r'''            var invalid: usize = 0;
            inline for (.{state.planet.temperature, state.planet.waterMass, state.planet.vegetation, state.planet.elevation}) |values| {
                for (values) |value| { if (!std.math.isFinite(value)) invalid += 1; }
            }
            std.debug.print("FINITE invalid_primary_fields={d}\n", .{invalid});
            std.debug.assert(invalid == 0);
            var biomass: f64 = 0;''')
    p.write_text(s)
