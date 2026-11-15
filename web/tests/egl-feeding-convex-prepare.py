#!/usr/bin/env python3
"""Paired outlined convex history-band candidate, preserving selection fixes."""
from pathlib import Path
import subprocess,sys
r=Path(__file__).resolve().parents[2];o=Path(sys.argv[1]).resolve()
subprocess.run([sys.executable,str(r/'web/tests/egl-feeding-simple-prepare.py'),str(o)],check=True)
p=o/'states/play.zig';s=p.read_text();old='vg.moveTo(-13,0);vg.lineTo(-8,-2);vg.lineTo(-4,1);vg.lineTo(0,-1);vg.lineTo(4,1);vg.lineTo(8,-2);vg.lineTo(13,0);vg.lineTo(10,5);vg.lineTo(4,5);vg.lineTo(0,7);vg.lineTo(-4,5);vg.lineTo(-10,5);vg.closePath();vg.fill();vg.stroke();';new='vg.moveTo(-13,2);vg.lineTo(-8,-2);vg.lineTo(8,-2);vg.lineTo(13,2);vg.lineTo(8,6);vg.lineTo(-8,6);vg.closePath();vg.fill();vg.stroke();';assert s.count(old)==1;s=s.replace(old,new);p.write_text(s)
p=o/'main.zig';s=p.read_text().replace('[_]u8{0,1,2,3,3,2,1,0,0,2,1,3}','[_]u8{1,3,3,1,1,3}',1);p.write_text(s)
# Match shipped web's per-draw diagnostic opt-out, not native debug policy.
p=o/'renderer.zig';s=p.read_text();old='''            .debug = @import("render_diagnostics_policy.zig").nanoVGDebug(is_web,
                if (@hasDecl(@import("build_options"), "web_gl_debug")) @import("build_options").web_gl_debug else false),''';assert s.count(old)==1;s=s.replace(old,'            .debug = false, // QA matches shipped web per-draw policy only.');p.write_text(s)
# Exactly two preregistered confirmation pairs; no repeated-until-favorable loop.
p=o/'main.zig';s=p.read_text();s=s.replace('for([_]u8{1,3,3,1,1,3},0..)|mode,arm|{','const modes:[]const u8=if(std.posix.getenv("QA_TWO_EXTRA_PAIRS")!=null) &[_]u8{3,1,1,3} else &[_]u8{1,3,3,1,1,3};\n            for(modes,0..)|mode,arm|{',1);p.write_text(s)
