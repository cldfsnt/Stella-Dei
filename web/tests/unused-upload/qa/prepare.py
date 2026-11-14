#!/usr/bin/env python3
from pathlib import Path
import os,sys,subprocess
root=Path(os.environ['STELLA_SOURCE_ROOT']).resolve();here=Path(__file__).resolve().parent;r=Path(sys.argv[1]).resolve()
subprocess.run([sys.executable,str(root/'web/tests/empty-bloom/qa/prepare.py'),str(r)],check=True)
p=r/'simulation/planet.zig';s=p.read_text();needle='        {\n            const kmPerWaterMass = self.getKmPerWaterMass();\n            const STRIDE = 4;'
if needle not in s:
 needle='        if (@import("builtin").target.cpu.arch != .wasm32) {\n            const kmPerWaterMass = self.getKmPerWaterMass();\n            const STRIDE = 4;'
assert needle in s
s=s.replace(needle,'''        if (!qa_skip_unused_atmosphere) {
            var unused_timer=std.time.Timer.start() catch unreachable;
            defer qa_unused_ns+=unused_timer.read();qa_unused_uploads+=1;qa_unused_bytes+=16*self.atmosphereMesh.num_points;
            const kmPerWaterMass = self.getKmPerWaterMass();
            const STRIDE = 4;''',1)
s='pub var qa_skip_unused_atmosphere=false;\npub var qa_unused_uploads:u64=0;pub var qa_unused_bytes:u64=0;pub var qa_unused_ns:u64=0;\n'+s;p.write_text(s)
p=r/'states/play.zig';s=p.read_text();s='pub var qa_force_atmosphere=false;\n'+s;s=s.replace('self.displayMode == .Normal and false','qa_force_atmosphere or (self.displayMode == .Normal and false)');p.write_text(s)
p=r/'main.zig';s=p.read_text();needle='    if(std.posix.getenv("QA_EMPTY_BLOOM")!=null){';assert needle in s;s=s.replace(needle,(here/'upload-qa.zig.part').read_text()+'    if(std.posix.getenv("QA_UNUSED_ALWAYS")!=null)@import("simulation/planet.zig").qa_skip_unused_atmosphere=true;\n'+needle,1);p.write_text(s);print(r/'main.zig')
