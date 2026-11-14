#!/usr/bin/env python3
"""Isolated actual-engine Origin QA; controlled scenario vs coupled-only env mode."""
from pathlib import Path
import subprocess,sys
here=Path(__file__).resolve().parent
out=Path(sys.argv[1] if len(sys.argv)>1 else '/tmp/stella-origin-src')
subprocess.run([sys.executable,str(here/'egl-prepare.py'),str(out),'--mobile','--paused'],check=True)
p=out/'main.zig';s=p.read_text().replace('nosuspend game.setState(PlayState);','game.startOriginNext = true; nosuspend game.setState(PlayState);').replace('const std = @import("std");','const std = @import("std");\nextern fn qa_click(x:f64,y:f64) void;\nextern fn qa_pointer(x:f64,y:f64,down:c_int) void;\nextern fn stella_bench_peak_rss() c_long;')
a=s.index('    std.log.debug("Creating update loop job.."');b=s.index('\nconst expect =',a)
p.write_text(s[:a]+(here/'egl-origin-main.zig.part').read_text()+s[b:]+(here/'egl-origin-save.zig.part').read_text())
p=out/'states/play.zig';p.write_text(p.read_text().replace('var randomPrng = std.rand.DefaultPrng.init(@as(u64, @bitCast(std.time.milliTimestamp())));','var randomPrng = std.rand.DefaultPrng.init(1337);'))
p=out/'loop.zig';p.write_text(p.read_text().replace('const is_web = @import("builtin").target.cpu.arch == .wasm32;','const is_web = true;'))
