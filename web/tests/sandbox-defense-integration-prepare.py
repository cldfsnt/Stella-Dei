#!/usr/bin/env python3
"""Single-use isolated integration tree. Do not regenerate after peer source handoff."""
from pathlib import Path
import sys,shutil,json,hashlib
r=Path(__file__).resolve().parents[2];o=Path(sys.argv[1]).resolve();shutil.copytree(r/'src',o,dirs_exist_ok=True)
frozen=r.parent/'site-tmp/sandbox-toughness/candidate/src'
for f in ['simulation/ecology.zig','simulation/foraging.zig']:shutil.copy2(frozen/f,o/f)
shutil.copy2(r/'web/tests/toughness-mutation.zig',o/'toughness_mutation.zig');shutil.copy2(r/'web/tests/sandbox-defense-actions.zig',o/'sandbox_defense.zig')
p=o/'simulation/ecology.zig';s=p.read_text()+'''
pub const DefenseConfig=struct{enabled:bool=false,law:u8=0,mutation_law:u8=0,stream_seed:u64=0};
pub fn offspringWithDefense(parent:Plant,event_seed:u64,config:DefenseConfig)Plant{
 var child=offspring(parent,event_seed);
 if(config.enabled)child.toughness=@import("../toughness_mutation.zig").allocation(parent.toughness,event_seed,parent.generation,.{.enabled=true,.stream_seed=config.stream_seed});
 return child;
}
''';p.write_text(s)
p=o/'simulation/life.zig';s=p.read_text().replace('Foraging.take(planet.vegetation[idx], self.satiety, dt)','Foraging.takeTough(planet.vegetation[idx], self.satiety, dt,planet.plantTraits[idx].toughness)');p.write_text(s)
p=o/'simulation/planet.zig';s=p.read_text().replace('pub const Planet = struct {','pub const Planet = struct {\n    sandboxDefense:Ecology.DefenseConfig=. {},');s=s.replace('Ecology.grow(self.vegetationSnapshot[i], self.temperature[i], self.plantTraits[i].optimum, self.waterMass[i] * self.getKmPerWaterMass(), light, self.averageCarbonDioxideMass > 0, dt)','Ecology.growTough(self.vegetationSnapshot[i], self.temperature[i], self.plantTraits[i].optimum, self.waterMass[i] * self.getKmPerWaterMass(), light, self.averageCarbonDioxideMass > 0, dt,self.plantTraits[i].toughness)');s=s.replace('if (self.vegetationSnapshot[n] < 0.25) continue;','if (self.vegetationSnapshot[n] < 0.25 or self.plantTraits[n].toughness>=1) continue;');s=s.replace('const child = Ecology.offspring(self.plantTraits[n], self.seed ^ (@as(u64, @intCast(i)) *% 0x9e3779b97f4a7c15) ^ epoch);','const child = Ecology.offspringWithDefense(self.plantTraits[n], self.seed ^ (@as(u64, @intCast(i)) *% 0x9e3779b97f4a7c15) ^ epoch,self.sandboxDefense);');s=s.replace('cover += @min(0.08, dt / 86400 * self.vegetationSnapshot[n]);','cover += if(self.plantTraits[n].toughness==0) @min(0.08, dt / 86400 * self.vegetationSnapshot[n]) else @min(0.08, dt / 86400 * self.vegetationSnapshot[n])*(1-self.plantTraits[n].toughness);');s=s.replace('                        const epoch: u64 = @intFromFloat(@max(0, options.gameTime / 3600));','                        if(self.sandboxDefense.enabled or self.plantTraits[n].toughness!=0){\n                            const gift=@min(@as(f32,0.08),dt/86400*self.vegetationSnapshot[n])*(1-self.plantTraits[n].toughness);\n                            if(!std.math.isFinite(gift) or gift<=0 or !(cover+gift>cover))continue;\n                        }\n                        const epoch: u64 = @intFromFloat(@max(0, options.gameTime / 3600));');s=s.replace('self.worldMode = .origin;','self.worldMode = .origin;\n        self.sandboxDefense=.{};');p.write_text(s)
(o.parent/'core-source-hashes.json').write_text(json.dumps({str(p.relative_to(o)):hashlib.sha256(p.read_bytes()).hexdigest()for p in [o/f for f in ['simulation/ecology.zig','simulation/foraging.zig','simulation/planet.zig','simulation/life.zig','sandbox_defense.zig','toughness_mutation.zig']]},indent=2)+'\n')
