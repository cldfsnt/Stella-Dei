#!/usr/bin/env python3
"""Prepare isolated fixed-seed cooperative performance experiment, not production."""
from pathlib import Path
import subprocess,sys
here=Path(__file__).resolve().parent
out=Path(sys.argv[1] if len(sys.argv)>1 else '/tmp/stella-egl-bench-src')
subprocess.run([sys.executable,str(here/'egl-prepare.py'),str(out),'--mobile'],check=True)
p=out/'loop.zig';s=p.read_text().replace('const is_web = @import("builtin").target.cpu.arch == .wasm32;','const is_web = true;');p.write_text(s)
p=out/'states/play.zig';s=p.read_text().replace('var randomPrng = std.rand.DefaultPrng.init(@as(u64, @bitCast(std.time.milliTimestamp())));','var randomPrng = std.rand.DefaultPrng.init(1337);').replace('const subdivisions = if (@import("builtin").mode == .Debug) 6 else 7;','const subdivisions = std.fmt.parseInt(u32, std.posix.getenv("STELLA_BENCH_LEVEL") orelse "7", 10) catch 7;');p.write_text(s)
p=out/'save_game.zig';s=p.read_text().replace('/saves','/tmp/stella-bench-saves');p.write_text(s)
p=out/'main.zig';s=p.read_text().replace('const std = @import("std");','const std = @import("std");\nextern fn stella_bench_peak_rss() c_long;').replace('fn main_wrap() !void {','fn main_wrap() !void {\n    var bench_start = try std.time.Timer.start();');a=s.index('    std.log.debug("Creating update loop job.."');b=s.index('\nconst expect =',a);p.write_text(s[:a]+(here/'egl-bench-main.zig.part').read_text()+s[b:])
