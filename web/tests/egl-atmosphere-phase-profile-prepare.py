#!/usr/bin/env python3
"""Copied-source atmospheric subphase timing; no algorithm changes."""
from pathlib import Path
import subprocess,sys
root=Path(__file__).resolve().parents[2];out=Path(sys.argv[1])
subprocess.run([sys.executable,str(root/'web/tests/egl-physics-phase-profile-prepare.py'),str(out)],check=True)
p=out/'qa_phase_metrics.zig';p.write_text(p.read_text().replace('[4]u64=.{0}**4','[9]u64=.{0}**9'))
p=out/'simulation/planet.zig';s=p.read_text();a=s.index('    fn simulateAtmosphereWater(');b=s.index('\n    /// Compute partial pressure',a);part=s[a:b]
part=part.replace('        // Velocity jobs have joined.','        const phase=@import("../qa_phase_metrics.zig");var sub_timer=std.time.Timer.start() catch unreachable;\n        // Velocity jobs have joined.',1)
for marker,index in [('        // No static geometry/velocity cache:',4),('        const divider=self.getSubstanceDivider();',5),('        // After the preceding swap,',6),('        for(self.waterVaporMass,0..)|vapor,i|{\n            var total_rate:f64=0;for(self.getNeighbours(i),0..)|n,j|total_rate+=if(self.atmosphericEdgeScratch.len==self.transformedPoints.len)self.atmosphericEdgeScratch[i][j] else self.atmosphericEdgeRate(i,n);\n            var gathered:',7),('        std.mem.swap([]f32,&self.waterVaporMass,&self.newWaterVaporMass);',8)]:
 assert marker in part
 part=part.replace(marker,f'        if(phase.enabled)phase.sums[{index}]+=sub_timer.lap() else _=sub_timer.lap();\n'+marker,1)
s=s[:a]+part+s[b:];p.write_text(s)
p=out/'main.zig';s=p.read_text().replace('phase.sums=.{0}**4','phase.sums=.{0}**9');needle='  const physics=perf.metrics.sample();';assert needle in s;s=s.replace(needle,'  std.debug.print("ATMOSPHERE_PHASE wind_cache_ms={d:.4} edge_cache_ms={d:.4} phase_relaxation_ms={d:.4} coefficient_ms={d:.4} gather_ms={d:.4}\\n",.{@as(f64,@floatFromInt(phase.sums[4]))/1e6,@as(f64,@floatFromInt(phase.sums[5]))/1e6,@as(f64,@floatFromInt(phase.sums[6]))/1e6,@as(f64,@floatFromInt(phase.sums[7]))/1e6,@as(f64,@floatFromInt(phase.sums[8]))/1e6});\n'+needle,1);p.write_text(s)
