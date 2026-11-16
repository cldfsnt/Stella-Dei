from pathlib import Path
import shutil,json,hashlib
r=Path(__file__).resolve().parents[2];o=r.parent/'site-tmp/root-wind-stage-diagnostic';assert not o.exists();o.mkdir();d=o/'src';shutil.copytree(r.parent/'site-tmp/wasm-root-wind-screen/candidate/src',d)
p=d/'simulation/planet.zig';s=p.read_text();s='pub var qa_cost:[6]f64=.{0,0,0,0,0,0};\nextern fn emscripten_get_now()f64;\n'+s
start=s.index('    pub fn simulate(self: *Planet, loop: *EventLoop, options: SimulationOptions) void {');end=s.index('    /// Simulation already owns lifeformsLock',start);part=s[start:end]
def put(a,b):
 global part
 assert part.count(a)==1,a;part=part.replace(a,b)
put('        @import("../plant_receipt.zig").begin','        var qa_clock=emscripten_get_now();\n        @import("../plant_receipt.zig").begin')
put('        const dt = options.dt * options.timeScale;','        qa_cost[0]+=emscripten_get_now()-qa_clock;qa_clock=emscripten_get_now();\n        const dt = options.dt * options.timeScale;')
a='                if(self.landBeta.enabled)self.simulateLandAtmosphere(dt,options)else self.simulateAtmosphereWater(dt);';put(a,'                qa_cost[1]+=emscripten_get_now()-qa_clock;qa_clock=emscripten_get_now();\n'+a+'\n                qa_cost[2]+=emscripten_get_now()-qa_clock;qa_clock=emscripten_get_now();')
a='        if (self.worldMode == .origin) self.simulateMicrobes(options) else self.simulateVegetation(options, 0, self.vegetation.len);';put(a,'        qa_cost[3]+=emscripten_get_now()-qa_clock;qa_clock=emscripten_get_now();\n'+a+'\n        qa_cost[4]+=emscripten_get_now()-qa_clock;')
s=s[:start]+part+s[end:]
a='        var birth_cursor:usize=0;';assert s.count(a)==1;s=s.replace(a,'        const qa_birth_start=emscripten_get_now();\n'+a)
a='        WorldEcology.record(self,world,options.gameTime+dt,self.microbeStats.births-|birth_start,physiology_deaths);';assert s.count(a)==1;s=s.replace(a,'        qa_cost[5]+=emscripten_get_now()-qa_birth_start;\n'+a);p.write_text(s)
p=d/'qa_wasm_land.zig';s=p.read_text();a='  if(tick==warmup)begin=emscripten_get_now();';assert s.count(a)==1;s=s.replace(a,'  if(tick==warmup){begin=emscripten_get_now();@import("simulation/planet.zig").qa_cost=.{0,0,0,0,0,0};}')
a=' const elapsed=emscripten_get_now()-begin;';assert s.count(a)==1;s=s.replace(a,a+'\n std.debug.print("COST_STAGES temperature_liquid_landphase_misc_microbes_birthsubset={any}\\n",.{@import("simulation/planet.zig").qa_cost});');p.write_text(s)
(o/'source-hashes.json').write_text(json.dumps({str(p.relative_to(d)):hashlib.sha256(p.read_bytes()).hexdigest()for p in d.rglob('*')if p.is_file()},indent=2))
