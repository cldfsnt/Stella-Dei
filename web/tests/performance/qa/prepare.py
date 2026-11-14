#!/usr/bin/env python3
"""Reproducible isolated native QA; never edits production source."""
from pathlib import Path
import os,sys,subprocess
here=Path(__file__).resolve().parent;root=Path(os.environ['STELLA_SOURCE_ROOT']).resolve();out=Path(sys.argv[1]).resolve()
subprocess.run([sys.executable,str(root/'web/tests/speed-adapter/qa/prepare.py'),str(out)],check=True)
p=out/'simulation/planet.zig'
if 'atmosphericWindScratch:' not in p.read_text():
 subprocess.run(['patch','-p2','--forward','-i',str(here/'owned-wind-cache.patch')],cwd=out,check=True)
p=out/'main.zig';s=p.read_text();needle='    if(std.posix.getenv("QA_CLOCK")!=null){';assert needle in s
s=s.replace(needle,(here/'lifecycle-qa.zig.part').read_text()+(here/'long-qa.zig.part').read_text()+needle)
# Force the production allocation-failure fallback for a matching rendered baseline.
s=s.replace(needle,needle+'''\n        var probe_failure=std.testing.FailingAllocator.init(allocator,.{.fail_index=0});
        if(std.posix.getenv("QA_WIND_UNCACHED")!=null){allocator.free(state.planet.atmosphericWindScratch);state.planet.atmosphericWindScratch=&.{};state.planet.allocator=probe_failure.allocator();}
        defer state.planet.allocator=allocator;
''')
p.write_text(s)
print(out/'main.zig')
