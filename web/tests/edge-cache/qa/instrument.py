from pathlib import Path
import sys; r=Path(sys.argv[1]).resolve()
(r/'perf.zig').write_text('pub var values:[8]u64=.{0}**8; pub var ticks:u64=0;\n')
p=r/'simulation/planet.zig';s=p.read_text();s='const perf=@import("../perf.zig");\n'+s
s=s.replace('pub fn simulate(self: *Planet, loop: *EventLoop, options: SimulationOptions) void {','pub fn simulate(self: *Planet, loop: *EventLoop, options: SimulationOptions) void {\n var perf_timer=std.time.Timer.start() catch unreachable; perf.ticks+=1;')
s=s.replace('// Finish by swapping the new temperature','perf.values[0]+=perf_timer.lap();\n        // Finish by swapping the new temperature')
s=s.replace('self.simulateAtmosphereWater(dt);','perf.values[1]+=perf_timer.lap();\n                self.simulateAtmosphereWater(dt);\n                perf.values[2]+=perf_timer.lap();')
s=s.replace('if (self.worldMode == .origin) self.simulateMicrobes(options) else self.simulateVegetation(options, 0, self.vegetation.len);','perf.values[3]+=perf_timer.lap();\n        if (self.worldMode == .origin) self.simulateMicrobes(options) else self.simulateVegetation(options, 0, self.vegetation.len);\n        perf.values[4]+=perf_timer.lap();')
s=s.replace('pub fn upload(self: *Planet, loop: *EventLoop, displayMode: DisplayMode, axialTilt: f32) void {','pub fn upload(self: *Planet, loop: *EventLoop, displayMode: DisplayMode, axialTilt: f32) void {\n var pt=std.time.Timer.start() catch unreachable; defer perf.values[5]+=pt.read();')
p.write_text(s)
p=r/'main.zig';s=p.read_text();s='const perf=@import("perf.zig");\n'+s
s=s.replace('var wall=try std.time.Timer.start();var previous:u64=0;','perf.values=.{0}**8;perf.ticks=0;\n            var wall=try std.time.Timer.start();var previous:u64=0;')
s=s.replace('render(window);gl.finish();window.swapBuffers();\n                max_frame', 'var rt=try std.time.Timer.start();render(window);perf.values[6]+=rt.lap();gl.finish();perf.values[7]+=rt.lap();window.swapBuffers();\n                max_frame')
s=s.replace('const elapsed=@as(f64,@floatFromInt(wall.read()))/1e9;', 'const elapsed=@as(f64,@floatFromInt(wall.read()))/1e9;\n            std.debug.print("PERF ticks={d} temp_ns={d} liquid_ns={d} atmos_ns={d} other_sim_ns={d} microbe_ns={d} upload_ns={d} render_cpu_ns={d} gpu_wait_ns={d}\\n",.{perf.ticks,perf.values[0],perf.values[1],perf.values[2],perf.values[3],perf.values[4],perf.values[5],perf.values[6],perf.values[7]});')
p.write_text(s)
