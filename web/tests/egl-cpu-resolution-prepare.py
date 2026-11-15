#!/usr/bin/env python3
"""Current production coupled CPU profile at selectable grid resolution; isolated source only."""
from pathlib import Path
import subprocess,sys
root=Path(__file__).resolve().parents[2];out=Path(sys.argv[1])
subprocess.run([sys.executable,str(root/'web/tests/egl-atmosphere-phase-profile-prepare.py'),str(out)],check=True)
p=out/'main.zig';s=p.read_text();s=s.replace('    originReport("seeded",state);','    originReport("seeded",state);\n    try profileFrames("early",state,window,allocator);',1);p.write_text(s)
p=out/'states/play.zig';s=p.read_text();needle='const subdivisions: usize = if (true or @import("builtin").mode == .Debug) 6 else 7;';assert needle in s
s=s.replace(needle,'const subdivisions: usize = std.fmt.parseInt(usize, std.posix.getenv("STELLA_CPU_LEVEL") orelse "6", 10) catch 6;');p.write_text(s)
