from pathlib import Path
import shutil
r=Path(__file__).resolve().parents[2];base=r.parent/'site-tmp';source=base/'liquid-timing-candidate/src';out=base/'liquid-timing-cached/src';shutil.copytree(source,out,dirs_exist_ok=True)
p=out/'simulation/planet.zig';s=p.read_text()
s=s.replace('    qaLiquidNeighbors:[][6]usize=&.{},','    qaLiquidNeighbors:[][6]usize=&.{},\n    qaLiquidReverse:[][6]u8=&.{},\n    qaLiquidTopologyIdentity:usize=0,\n    pub fn invalidateLiquidTopology(self:*Planet)void{self.qaLiquidTopologyIdentity=0;}')
# Function declaration must not split container fields: place before existing fn.
s=s.replace('    pub fn invalidateLiquidTopology(self:*Planet)void{self.qaLiquidTopologyIdentity=0;}','')
s=s.replace('    fn computeNeighbours(planet: *Planet) void {','    pub fn invalidateLiquidTopology(self:*Planet)void{self.qaLiquidTopologyIdentity=0;}\n    fn computeNeighbours(planet: *Planet) void {\n        planet.invalidateLiquidTopology();')
old='''                    if(self.qaLiquidEdges.len!=n){
                        self.qaLiquidEdges=self.simulationArena.allocator().alloc([6]f64,n) catch unreachable;
                        self.qaLiquidNeighbors=self.simulationArena.allocator().alloc([6]usize,n) catch unreachable;
                        for(0..n)|j|{const ns=self.getNeighbours(j);self.qaLiquidNeighbors[j]=.{ns[0],ns[3],ns[1],ns[4],ns[2],ns[5]};}
                    }
                    _= @import("liquid_gather.zig").step(self.waterMass,self.elevation,self.qaLiquidNeighbors,self.qaLiquidEdges,self.newWaterMass,self.getKmPerWaterMass(),dt,false) catch unreachable;'''
new='''                    if(self.qaLiquidEdges.len!=n){
                        self.qaLiquidEdges=self.simulationArena.allocator().alloc([6]f64,n) catch unreachable;
                        self.qaLiquidNeighbors=self.simulationArena.allocator().alloc([6]usize,n) catch unreachable;
                        self.qaLiquidReverse=self.simulationArena.allocator().alloc([6]u8,n) catch unreachable;
                        self.invalidateLiquidTopology();
                    }
                    const topology_identity=@intFromPtr(self.verticesNeighbours.ptr);
                    if(self.qaLiquidTopologyIdentity!=topology_identity){
                        for(0..n)|j|{const ns=self.getNeighbours(j);self.qaLiquidNeighbors[j]=.{ns[0],ns[3],ns[1],ns[4],ns[2],ns[5]};}
                        @import("liquid_gather_cached.zig").prepare(self.qaLiquidNeighbors,self.qaLiquidReverse) catch unreachable;
                        self.qaLiquidTopologyIdentity=topology_identity;
                    }
                    _= @import("liquid_gather_cached.zig").step(self.waterMass,self.elevation,self.qaLiquidNeighbors,self.qaLiquidReverse,self.qaLiquidEdges,self.newWaterMass,self.getKmPerWaterMass(),dt,false) catch unreachable;'''
assert old in s;s=s.replace(old,new);p.write_text(s)
p=out/'save_game.zig';s=p.read_text();s=s.replace('    p.worldMode = saved.mode;','    p.invalidateLiquidTopology();\n    p.worldMode = saved.mode;');p.write_text(s)
(out/'simulation/liquid_gather_cached.zig').write_text((r/'src/experimental/liquid_gather_cached.zig').read_text())
p=out/'main.zig';s=p.read_text().replace(str(source.parent),str(out.parent));p.write_text(s);print(out)
