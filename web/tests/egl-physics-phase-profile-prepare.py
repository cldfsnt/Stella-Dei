#!/usr/bin/env python3
"""Only isolated copied source gets phase timers; production never edited."""
from pathlib import Path
import subprocess,sys
root=Path(__file__).resolve().parents[2];out=Path(sys.argv[1])
subprocess.run([sys.executable,str(root/'web/tests/egl-full-frame-profile-prepare.py'),str(out)],check=True)
(out/'qa_phase_metrics.zig').write_text('pub var enabled:bool=false; pub var sums:[4]u64=.{0}**4; pub var ticks:u64=0;\n')
p=out/'simulation/planet.zig';s=p.read_text();start=s.index('    pub fn simulate(self: *Planet, loop: *EventLoop, options: SimulationOptions) void {');end=s.index('\n    /// Simulation already owns',start);part=s[start:end]
part=part.replace('        const newTemp = self.newTemperature;','        const phase=@import("../qa_phase_metrics.zig");var phase_timer=std.time.Timer.start() catch unreachable;\n        const newTemp = self.newTemperature;',1)
part=part.replace('        const dt = options.dt * options.timeScale;','        if(phase.enabled)phase.sums[0]+=phase_timer.lap() else _=phase_timer.lap();\n        const dt = options.dt * options.timeScale;',1)
part=part.replace('                self.simulateAtmosphereWater(dt);','                var atmosphere_timer=std.time.Timer.start() catch unreachable;\n                self.simulateAtmosphereWater(dt);\n                if(phase.enabled)phase.sums[2]+=atmosphere_timer.read();',1)
part=part.replace('        // Geologic simulation only happens','        if(phase.enabled)phase.sums[1]+=phase_timer.lap() else _=phase_timer.lap();\n        // Geologic simulation only happens',1)
needle='        if (self.worldMode == .origin) self.simulateMicrobes(options) else self.simulateVegetation(options, 0, self.vegetation.len);';assert needle in part
part=part.replace(needle,needle+'\n        if(phase.enabled){phase.sums[3]+=phase_timer.read();phase.ticks+=1;}')
s=s[:start]+part+s[end:];p.write_text(s)
p=out/'main.zig';s=p.read_text().replace('    try profileFrames("early",state,window,allocator);','')
s=s.replace('for([_]f32{0,21600,86400})','for([_]f32{86400})')
s=s.replace('  perf.metrics.setEnabled(true);const start_time=state.gameTime;','  const phase=@import("qa_phase_metrics.zig");phase.sums=.{0}**4;phase.ticks=0;phase.enabled=true;\n  perf.metrics.setEnabled(true);const start_time=state.gameTime;')
s=s.replace('  const physics=perf.metrics.sample();','  phase.enabled=false;std.debug.print("PHYSICS_PHASE ticks={d} temperature_total_ms={d:.4} water_inclusive_total_ms={d:.4} atmosphere_nested_total_ms={d:.4} water_excluding_atmosphere_total_ms={d:.4} organisms_total_ms={d:.4} scheduler_parallel_count={d}\\n",.{phase.ticks,@as(f64,@floatFromInt(phase.sums[0]))/1e6,@as(f64,@floatFromInt(phase.sums[1]))/1e6,@as(f64,@floatFromInt(phase.sums[2]))/1e6,@as(f64,@floatFromInt(phase.sums[1]-phase.sums[2]))/1e6,@as(f64,@floatFromInt(phase.sums[3]))/1e6,game.loop.getParallelCount()});\n  const physics=perf.metrics.sample();')
p.write_text(s)
