#!/usr/bin/env python3
"""Isolated real-engine paired benchmark. No production timestep changes."""
from pathlib import Path
import subprocess,sys
here=Path(__file__).resolve().parent
out=Path(sys.argv[1]); inline='--inline' in sys.argv
subprocess.run([sys.executable,str(here/'egl-bench-prepare.py'),str(out)],check=True)
p=out/'main.zig';s=p.read_text()
s=s.replace('state.timeScale = 60;', 'state.timeScale = 3600;')
s=s.replace('        state.gameTime = @floatFromInt(i);','')
# Serialize the complete actual state after exactly 65 sixty-second ticks.
a=s.index('    if (std.posix.getenv("STELLA_BENCH_SAVE") != null) {'); b=s.index('\n}\n',a)
s=s[:a]+'''    game.loop.pump(100000);
    const saves=@import("save_game.zig");
    var arena=std.heap.ArenaAllocator.init(game.allocator); defer arena.deinit();
    const saved=try saves.capture(arena.allocator(),state);
    const bytes=try std.json.stringifyAlloc(arena.allocator(),saved,.{});
    try std.fs.cwd().writeFile(.{.sub_path=std.posix.getenv("STELLA_PROFILE_SAVE") orelse "/tmp/stella-profile.json",.data=bytes});
    std.debug.print("PROFILE final_time={d} bytes={d}\\n",.{state.gameTime,bytes.len});
''' + s[b:]
p.write_text(s)
p=out/'simulation/planet.zig';s=p.read_text().replace('    inline fn sendWater(self: Planet,','    fn sendWater(self: Planet,',1)
if inline:s=s.replace('    fn sendWater(self: Planet,','    inline fn sendWater(self: Planet,',1)
p.write_text(s)
