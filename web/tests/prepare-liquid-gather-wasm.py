from pathlib import Path
import shutil,json,hashlib
r=Path(__file__).resolve().parents[2];b=r.parent/'site-tmp';out=b/'liquid-gather-wasm';out.mkdir(exist_ok=True)
base=b/'wasm-planet-profile/plain/src';frozen=b/'liquid-timing-compact/src/simulation/planet.zig';old=frozen.read_text();at=old.index('                if(self.worldMode==.origin){',old.index('    pub fn simulate('));end=old.index('                std.mem.swap([]f32, &self.waterMass',at);block=old[at:end]
g=json.loads((b/'wasm-planet-profile/graph.json').read_text());g['neighbors']=[[ns[i]for i in [0,3,1,4,2,5]]for ns in g['neighbors']];(out/'helper-graph.json').write_text(json.dumps(g,separators=(',',':')))
for mode in ['candidate','candidate-trace','baseline-trace']:
 d=out/mode;shutil.copytree(base,d/'src',dirs_exist_ok=True);p=d/'src/simulation/planet.zig';s=p.read_text();candidate=mode.startswith('candidate');trace=mode.endswith('trace')
 if candidate:
  fields='\n'.join(x for x in old.splitlines()if x.strip().startswith('qaLiquid') and ':'in x and not 'const 'in x)+'\n'
  s=s.replace('    waterVaporMass: []f32,','    waterVaporMass: []f32,\n'+fields,1)
  s=s.replace('    fn computeNeighbours(planet: *Planet) void {','    pub fn invalidateLiquidTopology(self:*Planet)void{self.qaLiquidTopologyIdentity=0;}\n    fn computeNeighbours(planet: *Planet) void {\n        planet.invalidateLiquidTopology();',1)
  assert s.count('        if (dt < 86400 / 4) {')==1;s=s.replace('        if (dt < 86400 / 4) {','        if (dt < 86400 / 4 and self.worldMode != .origin) {',1)
  marker='                std.mem.swap([]f32, &self.waterMass, &self.newWaterMass);';assert s.count(marker)==1;s=s.replace(marker,block+marker,1)
  helper=(r/'src/experimental/liquid_gather_compact.zig').read_text()
  if trace:
   helper=helper.replace('const std=@import("std");','pub var qa_accum:[]f64=&.{};\nconst std=@import("std");',1);helper=helper.replace('  out[i]=@floatCast(next);','  qa_accum[i]=next;out[i]=@floatCast(next);')
   s=s.replace('                    _= @import("liquid_gather_compact.zig").step','                    if(@import("liquid_gather_compact.zig").qa_accum.len!=n)@import("liquid_gather_compact.zig").qa_accum=self.simulationArena.allocator().alloc(f64,n) catch unreachable;\n                    _= @import("liquid_gather_compact.zig").step',1)
  (d/'src/simulation/liquid_gather_compact.zig').write_text(helper)
  save=d/'src/save_game.zig';save.write_text(save.read_text().replace('    p.worldMode = saved.mode;','    p.invalidateLiquidTopology();\n    p.worldMode = saved.mode;',1))
 if trace:
  s='extern fn qa_trace(n:u32,tick:u32,area:f64,pre:[*]const f32,post:[*]const f32,edges:?[*]const [6]f32,accum:?[*]const f64) void;\nvar qa_tick:u32=0;\n'+s
  args='self.qaLiquidEdges.ptr,@import("liquid_gather_compact.zig").qa_accum.ptr'if candidate else 'null,null'
  marker='                std.mem.swap([]f32, &self.waterMass, &self.newWaterMass);'
  s=s.replace(marker,f'                qa_trace(@intCast(self.waterMass.len),qa_tick,self.getMeanPointArea(),self.waterMass.ptr,self.newWaterMass.ptr,{args});qa_tick+=1;\n'+marker,1)
 p.write_text(s)
print(out)
