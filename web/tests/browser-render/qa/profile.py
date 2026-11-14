#!/usr/bin/env python3
from pathlib import Path
import sys,re
r=Path(sys.argv[1]).resolve();(r/'perf.zig').write_text('pub var values:[12]u64=.{0}**12;\n')
p=r/'states/play.zig';s=p.read_text();s='const perf=@import("../perf.zig");\n'+s
for name,id in [('render',0),('renderScene',1),('renderUI',2),('renderSprouts',3),('renderSeedZones',4)]:
 pattern=r'(    (?:pub )?fn '+name+r'\([^\n]+\) void \{)';s,n=re.subn(pattern,lambda m:m.group(1)+f'\n        var pt=std.time.Timer.start() catch unreachable;defer perf.values[{id}]+=pt.read();',s);assert n==1
bracket='--bracket' in sys.argv
if bracket:
 needle='        gl.clear(gl.COLOR_BUFFER_BIT | gl.DEPTH_BUFFER_BIT);\n        {\n            const program = renderer.postprocessProgram;';assert needle in s;s=s.replace(needle,'        gl.clear(gl.COLOR_BUFFER_BIT | gl.DEPTH_BUFFER_BIT);\n        gl.finish();var composite_timer=std.time.Timer.start() catch unreachable;\n        {\n            const program = renderer.postprocessProgram;',1)
 needle='        if (!self.paused) {\n            self.renderGameTime = self.gameTime;';assert needle in s;s=s.replace(needle,'        gl.finish();perf.values[5]+=composite_timer.read();\n\n'+needle,1)
p.write_text(s)
p=r/'main.zig';s=p.read_text().replace('var samples:[4096]f64=undefined;', '@import("perf.zig").values=.{0}**12;var samples:[4096]f64=undefined;')
a=s.index('std.debug.print("SB_RENDER');z=s.index('\n        }',a)
s=s[:z]+'''\n            std.debug.print("SB_STAGES pass={d} frames={d} scene_post_ns={d} scene_draw_ns={d} ui_ns={d} flora_ns={d} seedzones_ns={d} composite_completed_ns={d}\\n",.{pass,count,@import("perf.zig").values[0],@import("perf.zig").values[1],@import("perf.zig").values[2],@import("perf.zig").values[3],@import("perf.zig").values[4],@import("perf.zig").values[5]});'''+s[z:]
if bracket:s=s.replace('timer.read()<2_000_000_000','timer.read()<6_000_000_000')
p.write_text(s)
