from pathlib import Path
import shutil,json,hashlib
r=Path(__file__).resolve().parents[2];out=r.parent/'site-tmp/wasm-planet-profile';out.mkdir(exist_ok=True)
rows=[json.loads(x) for x in (r.parent/'site-tmp/propagule-graph/graph.jsonl').read_text().splitlines()][1:]
# Planet.Direction storage and getNeighbours share FL,BL,L,FR,BR,R order.
# Do NOT remap to sendWater call order (that remap is only for scalar solver fixtures).
(out/'graph.json').write_text(json.dumps({'points':[x['point'] for x in rows],'neighbors':[x['neighbors'] for x in rows]},separators=(',',':')))
for mode in ['plain','stages']:
 d=out/mode;shutil.copytree(r/'src',d/'src',dirs_exist_ok=True)
 (d/'src/qa_wasm_planet.zig').write_text((r/'web/tests/wasm-planet-profile.zig.part').read_text())
 s=(r/'src/simulation/planet.zig').read_text();s='pub var qa_substages:[5]f64=.{0,0,0,0,0};\n'+'pub var qa_stages:[4]f64=.{0,0,0,0};\nextern fn emscripten_get_now() f64;\n'+s
 if mode=='stages':
  a=s.index('    fn simulateAtmosphereWater(');b=s.index('    /// Compute partial pressure',a);part=s[a:b]
  part=part.replace('        // Velocity jobs have joined.', '        var qa_sub=emscripten_get_now();\n        // Velocity jobs have joined.',1)
  for marker,index in [('        // No static geometry/velocity cache',0),('        const divider=self.getSubstanceDivider()',1),('        // After the preceding swap',2),('        for(self.waterVaporMass,0..)|vapor,i|{\n            var total_rate:f64=0;for(self.getNeighbours(i),0..)|n,j|total_rate+=if(self.atmosphericEdgeScratch.len==self.transformedPoints.len)self.atmosphericEdgeScratch[i][j] else self.atmosphericEdgeRate(i,n);\n            var gathered',3),('        std.mem.swap([]f32,&self.waterVaporMass,&self.newWaterVaporMass);',4)]:
   assert part.count(marker)==1
   part=part.replace(marker,f'        qa_substages[{index}]+=emscripten_get_now()-qa_sub;qa_sub=emscripten_get_now();\n'+marker,1)
  s=s[:a]+part+s[b:]
  s=s.replace('        // Fill newTemp with the current temperatures','        var qa_begin=emscripten_get_now();\n        // Fill newTemp with the current temperatures',1)
  s=s.replace('        const dt = options.dt * options.timeScale;\n        // Disable water', '        qa_stages[0]+=emscripten_get_now()-qa_begin;qa_begin=emscripten_get_now();\n        const dt = options.dt * options.timeScale;\n        // Disable water',1)
  s=s.replace('                self.simulateAtmosphereWater(dt);','                qa_stages[1]+=emscripten_get_now()-qa_begin;qa_begin=emscripten_get_now();\n                self.simulateAtmosphereWater(dt);\n                qa_stages[2]+=emscripten_get_now()-qa_begin;qa_begin=emscripten_get_now();',1)
  s=s.replace('        if (self.worldMode == .origin) self.simulateMicrobes(options) else self.simulateVegetation(options, 0, self.vegetation.len);','        if (self.worldMode == .origin) self.simulateMicrobes(options) else self.simulateVegetation(options, 0, self.vegetation.len);\n        qa_stages[3]+=emscripten_get_now()-qa_begin;',1)
 (d/'src/simulation/planet.zig').write_text(s)
 b=(r/'web-build.zig').read_text().replace('b.path("src/main.zig")','.{ .cwd_relative = b.option([]const u8,"source","QA root").? }').replace('b.path("deps','b.path("../../deps').replace('b.path(entry[1])','b.path("../../" ++ entry[1])')
 (r/'web/tests/wasm-planet-build.zig').write_text(b)
print(out)
