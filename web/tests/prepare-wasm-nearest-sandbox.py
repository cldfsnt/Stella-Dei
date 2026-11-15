#!/usr/bin/env python3
from pathlib import Path
import shutil,json,hashlib
r=Path(__file__).resolve().parents[2];o=r.parent/'site-tmp/wasm-nearest-sandbox';d=o/'src';shutil.copytree(r/'src',d,dirs_exist_ok=True)
s=(r/'web/tests/wasm-planet-profile.zig.part').read_text()
s=s.replace('if(saved.mode!=.origin or saved.rabbits.len!=0)return error.OriginOnly;','if(saved.mode!=.sandbox)return error.SandboxOnly;')
a=s.index(' p.worldMode=.origin;');b=s.index('\n p.plantGenerations=',a)
s=s[:a]+' p.worldMode=.sandbox;\n'+s[b:]
save=(r/'src/save_game.zig').read_text()
a=save.index('    for (saved.rabbits) |rabbit| {');b=save.index('\n    }',a)+len('\n    }')
restore=save[a:b].replace('p.lifeforms.appendAssumeCapacity(life);','try p.lifeforms.append(p.simulationArena.allocator(),life);')
assert 'append' in restore
needle=' p.refreshTransformedPoints(saved.axial_tilt);'
s=s.replace(needle,restore+'\n'+needle)
s=s.replace(' const begin=emscripten_get_now();',' var begin=emscripten_get_now();const warmup:u32=if(ticks>=72)12 else 0;')
s=s.replace(' for(0..ticks)|tick|{',' for(0..ticks)|tick|{\n  if(tick==warmup)begin=emscripten_get_now();')
s=s.replace('if(tick==0){','if(tick==warmup){')
a=s.index(' const sparse=try S.captureSparse');b=s.index('\n saved.elevation=',a)
capture_start=save.index('    const rabbits = try allocator.alloc(schema.Rabbit, p.lifeforms.items.len);')
capture_end=save.index('\n    var origin:',capture_start)
capture=save[capture_start:capture_end]
capture=capture.replace('allocator.alloc(schema.Rabbit','a.alloc(S.Rabbit')
capture='\n'.join(l for l in capture.splitlines()if not l.strip().startswith('for (p.airVelocity, wind)') and not l.strip().startswith('for (p.airPositionError, wind_error)'))
s=s[:a]+capture+'''
 saved.rabbits=rabbits;saved.origin=null;
 saved.plant_generations=p.plantGenerations;saved.plant_births=p.plantBirths;saved.rabbit_births=p.rabbitBirths;saved.rabbit_meals=p.rabbitMeals;saved.rabbit_deaths=p.rabbitDeaths;saved.plant_color=p.plantColorWavelength;
'''+s[b:]
s+='\nexport fn qa_set_candidate(on:u32)void{@import("simulation/planet.zig").qa_candidate=on!=0;}\n'
s=s.replace('WASM_PLANET ticks={d}','WASM_PLANET ticks={d}') # total_ms excludes12warmup for72+ requests, explicitly parsed.
(d/'qa_wasm_nearest.zig').write_text(s)
p=d/'simulation/planet.zig';s=p.read_text()
s='pub var qa_candidate:bool=false;\npub var qa_stages:[4]f64=.{0,0,0,0};\npub var qa_substages:[5]f64=.{0,0,0,0,0};\n'+s
needle='return @import("../nearest_point.zig").nearest(self.transformedPoints, position);'
assert s.count(needle)==1
s=s.replace(needle,'''if(qa_candidate)return @import("../nearest_point.zig").nearest(self.transformedPoints, position);
        var best_distance:f32=std.math.inf(f32);var best:usize=undefined;
        for(self.transformedPoints,0..)|point,i|{const distance=point.distance(position);if(distance<best_distance){best_distance=distance;best=i;}}
        return best;''')
p.write_text(s)
shutil.copyfile(r.parent/'site-tmp/wasm-planet-profile/graph.json',o/'graph.json')
(o/'provenance.json').write_text(json.dumps({'input':str(r.parent/'site-tmp/foraging-production/warm-actual-end.json'),'input_sha256':hashlib.sha256((r.parent/'site-tmp/foraging-production/warm-actual-end.json').read_bytes()).hexdigest(),'graph_sha256':hashlib.sha256((o/'graph.json').read_bytes()).hexdigest(),'files':{str(p.relative_to(d)):hashlib.sha256(p.read_bytes()).hexdigest()for p in d.rglob('*.zig')}},indent=2)+'\n')
