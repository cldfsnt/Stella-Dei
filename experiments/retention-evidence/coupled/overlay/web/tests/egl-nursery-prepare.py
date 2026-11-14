#!/usr/bin/env python3
"""Current-source actual nursery API acceptance; no experimental geometry substitution."""
from pathlib import Path
import os,subprocess,sys
root=Path(os.environ.get('STELLA_SOURCE_ROOT',str(Path(__file__).resolve().parents[2])))
out=Path(sys.argv[1])
subprocess.run([sys.executable,str(root/'web/tests/egl-propagule-prepare.py'),str(out)],check=True)
p=out/'main.zig';s=p.read_text().replace('state.makeSelectedPond(', 'state.makeSelectedNursery(').replace('production_15m=true','actual_nursery_api=true')
s=s.replace('std.debug.assert(state.makeSelectedNursery(point)>0);','std.debug.assert(state.makeSelectedNursery(point+1)==-1);\n    std.debug.assert(state.makeSelectedNursery(point)>0);')
s=s.replace('std.debug.assert(@abs(state.planet.waterMass[patch]*state.planet.getKmPerWaterMass()*1000-depth)<0.001);','const expected_depth:f32=if(patch==center)5 else depth;\n        std.debug.assert(@abs(state.planet.waterMass[patch]*state.planet.getKmPerWaterMass()*1000-expected_depth)<0.001);')
assert 'const expected_depth:f32=if(patch==center)5 else depth;' in s
if '--replay' in sys.argv:
    needle='    originReport("empty",state);'
    s=s.replace(needle,needle+'\n'+(root/'web/tests/nursery-replay.zig.part').read_text())
p.write_text(s)
assert 'pub fn makeSelectedNursery(' in (out/'states/play.zig').read_text()
