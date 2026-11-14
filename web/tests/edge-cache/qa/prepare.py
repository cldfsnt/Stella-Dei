#!/usr/bin/env python3
from pathlib import Path
import os,sys,subprocess
root=Path(os.environ['STELLA_SOURCE_ROOT']).resolve();here=Path(__file__).resolve().parent;out=Path(sys.argv[1]).resolve()
subprocess.run([sys.executable,str(root/'web/tests/empty-bloom/qa/prepare.py'),str(out)],check=True)
p=out/'simulation/planet.zig'
if 'atmosphericEdgeScratch:' not in p.read_text():subprocess.run(['patch','-p2','--forward','-i',str(here/'edge-cache.patch')],cwd=out,check=True)
p=out/'main.zig';s=p.read_text();a=s.index('    if(std.posix.getenv("QA_WIND_LIFECYCLE")');b=s.index('    if(std.posix.getenv("QA_EMPTY_BLOOM")',a)
s=s[:a]+(here/'edge-checks.zig.part').read_text()+s[b:]
s=s.replace('        var probe_failure=std.testing.FailingAllocator.init','        if(state.planet.atmosphericWindScratch.len==0)state.planet.atmosphericWindScratch=try allocator.alloc([3]f32,state.planet.transformedPoints.len);\n        var probe_failure=std.testing.FailingAllocator.init')
s=s.replace('allocator.free(state.planet.atmosphericWindScratch);state.planet.atmosphericWindScratch=&.{};state.planet.allocator=probe_failure.allocator();','allocator.free(state.planet.atmosphericEdgeScratch);state.planet.atmosphericEdgeScratch=&.{};state.planet.allocator=probe_failure.allocator();')
p.write_text(s)
print(out/'main.zig')
