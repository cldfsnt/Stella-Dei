from pathlib import Path
import shutil,json,hashlib
r=Path(__file__).resolve().parents[2];o=r.parent/'site-tmp/wasm-land-phases';o.mkdir(exist_ok=True);src=r.parent/'site-tmp/wasm-land-screen/candidate/src'
for arm in ['plain','traced']:
 d=o/arm/'src';shutil.copytree(src,d,dirs_exist_ok=True)
 p=d/'simulation/planet.zig';s=p.read_text();s='pub var qa_phase:[7]f64=.{0,0,0,0,0,0,0};\n'+s
 if arm=='traced':
  s='extern fn emscripten_get_now() f64;\n'+s
  for name in ['simulateAtmosphereWater','simulateLandAtmosphere']:
   a=s.index('    fn '+name+'(');b=s.index('\n    }',a)+6;part=s[a:b]
   part=part.replace('        // Velocity jobs have joined.', '        var qa_begin=emscripten_get_now();\n        // Velocity jobs have joined.',1)
   marker='        const divider=self.getSubstanceDivider();';assert part.count(marker)==1
   part=part.replace(marker,'        qa_phase[2]+=emscripten_get_now()-qa_begin;qa_begin=emscripten_get_now();\n'+marker,1)
   marker='        // After the preceding swap';assert part.count(marker)==1
   part=part.replace(marker,'        qa_phase[3]+=emscripten_get_now()-qa_begin;qa_begin=emscripten_get_now();\n'+marker,1)
   marker='        for(self.landVapor,0..)|vapor,i|{'if name=='simulateLandAtmosphere'else '        for(self.waterVaporMass,0..)|vapor,i|{'
   # Two occurrences are coefficient and gather; columns iterate different slices.
   assert part.count(marker)==2;pos=part.index(marker,part.index(marker)+1);part=part[:pos]+'        qa_phase[4]+=emscripten_get_now()-qa_begin;qa_begin=emscripten_get_now();\n'+part[pos:]
   pos=part.rindex('\n    }');part=part[:pos]+'\n        qa_phase[5]+=emscripten_get_now()-qa_begin;'+part[pos:];s=s[:a]+part+s[b:]
  marker='    pub fn simulate(self: *Planet, loop: *EventLoop, options: SimulationOptions) void {';assert s.count(marker)==1;s=s.replace(marker,marker+'\n        var qa_tick=emscripten_get_now();')
  marker='        // Finish by swapping the new temperature';assert s.count(marker)==1;s=s.replace(marker,'        qa_phase[0]+=emscripten_get_now()-qa_tick;qa_tick=emscripten_get_now();\n'+marker)
  marker='                if(self.landBeta.enabled)self.simulateLandAtmosphere(dt,options)else self.simulateAtmosphereWater(dt);';assert s.count(marker)==1;s=s.replace(marker,'                qa_phase[1]+=emscripten_get_now()-qa_tick;\n'+marker+'\n                qa_tick=emscripten_get_now();')
  marker='        @import("../plant_receipt.zig").finish(self,@import("../performance_details.zig").world_serial);';assert s.count(marker)==1;s=s.replace(marker,marker+'\n        qa_phase[6]+=emscripten_get_now()-qa_tick;')
 p.write_text(s)
 p=d/'qa_wasm_land.zig';s=p.read_text().replace('if(tick==warmup)begin=emscripten_get_now();','if(tick==warmup){@import("simulation/planet.zig").qa_phase=.{0,0,0,0,0,0,0};begin=emscripten_get_now();}')
 s=s.replace(' const elapsed=emscripten_get_now()-begin;',' const elapsed=emscripten_get_now()-begin;std.debug.print("LAND_PHASES {any}\\n",.{@import("simulation/planet.zig").qa_phase});');p.write_text(s)
 (o/arm/'source-hashes.json').write_text(json.dumps({str(p.relative_to(d)):hashlib.sha256(p.read_bytes()).hexdigest()for p in d.rglob('*.zig')},indent=2))
shutil.copyfile(r.parent/'site-tmp/wasm-land-screen/graph.json',o/'graph.json')
