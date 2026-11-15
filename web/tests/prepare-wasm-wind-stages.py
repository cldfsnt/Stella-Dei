from pathlib import Path
import shutil,json,hashlib
r=Path(__file__).resolve().parents[2];o=r.parent/'site-tmp/wasm-wind-stages';o.mkdir(exist_ok=True)
for arm in ['baseline','candidate']:
 d=o/arm/'src';assert not d.exists();shutil.copytree(r.parent/'site-tmp/wasm-wind-screen'/arm/'src',d)
 p=d/'simulation/planet.zig';s=p.read_text();s='pub var qa_wind_profile:[5]f64=.{0,0,0,0,0};\nextern fn emscripten_get_now()f64;\n'+s
 start=s.index('    pub fn simulate(self: *Planet, loop: *EventLoop, options: SimulationOptions) void {');end=s.index('    /// Simulation already owns lifeformsLock',start);part=s[start:end]
 markers=[('        @import("../plant_receipt.zig").begin', '        var qa_clock=emscripten_get_now();\n'),('        const dt = options.dt * options.timeScale;', '        qa_wind_profile[0]+=emscripten_get_now()-qa_clock;qa_clock=emscripten_get_now();\n'),('                self.simulateAtmosphereWater(dt);','                qa_wind_profile[1]+=emscripten_get_now()-qa_clock;qa_clock=emscripten_get_now();\n')]
 for marker,prefix in markers:assert part.count(marker)==1;part=part.replace(marker,prefix+marker,1)
 marker='                self.simulateAtmosphereWater(dt);';part=part.replace(marker,marker+'\n                qa_wind_profile[2]+=emscripten_get_now()-qa_clock;qa_clock=emscripten_get_now();',1)
 marker='        if (self.worldMode == .origin) self.simulateMicrobes(options) else self.simulateVegetation(options, 0, self.vegetation.len);';assert part.count(marker)==1;part=part.replace(marker,'        qa_wind_profile[3]+=emscripten_get_now()-qa_clock;qa_clock=emscripten_get_now();\n'+marker)
 marker='\n    }\n\n';assert part.endswith(marker);part=part[:-len(marker)]+'\n        qa_wind_profile[4]+=emscripten_get_now()-qa_clock;\n'+marker
 s=s[:start]+part+s[end:];p.write_text(s)
 p=d/'qa_wasm_wind.zig';s=p.read_text().replace('  if(tick==warmup)begin=emscripten_get_now();','  if(tick==warmup){begin=emscripten_get_now();@import("simulation/planet.zig").qa_wind_profile=.{0,0,0,0,0};}');s=s.replace(' const elapsed=emscripten_get_now()-begin;', ' const elapsed=emscripten_get_now()-begin;\n std.debug.print("WIND_STAGES temperature_liquid_atmosphere_rabbits_vegetation={any}\\n",.{@import("simulation/planet.zig").qa_wind_profile});');p.write_text(s)
 (o/arm/'source-hashes.json').write_text(json.dumps({str(p.relative_to(d)):hashlib.sha256(p.read_bytes()).hexdigest()for p in d.rglob('*.zig')},indent=2))
shutil.copyfile(r.parent/'site-tmp/wasm-wind-screen/graph.json',o/'graph.json')
