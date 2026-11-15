from pathlib import Path
import shutil,sys
r=Path(__file__).resolve().parents[2];source=Path(sys.argv[1]).resolve();out=Path(sys.argv[2]).resolve();shutil.copytree(source,out,dirs_exist_ok=True)
p=out/'simulation/planet.zig';s=p.read_text()
def once(a,b):
 global s
 assert s.count(a)==1,(a,s.count(a));s=s.replace(a,b,1)
once('    waterVaporMass: []f32,','    waterVaporMass: []f32,\n    qaLiquidEdges:[][6]f64=&.{},\n    qaLiquidNeighbors:[][6]usize=&.{},')
once('        if (dt < 86400 / 4) {','        if (dt < 86400 / 4 and self.worldMode != .origin) {')
needle='                const qa_before_transport=self.qaWaterTotal();'
once(needle,'''                if(self.worldMode==.origin){
                    const begin=std.time.nanoTimestamp();const n=self.waterMass.len;
                    if(self.qaLiquidEdges.len!=n){
                        self.qaLiquidEdges=self.simulationArena.allocator().alloc([6]f64,n) catch unreachable;
                        self.qaLiquidNeighbors=self.simulationArena.allocator().alloc([6]usize,n) catch unreachable;
                        for(0..n)|j|{const ns=self.getNeighbours(j);self.qaLiquidNeighbors[j]=.{ns[0],ns[3],ns[1],ns[4],ns[2],ns[5]};}
                    }
                    const receipt=@import("liquid_gather.zig").step(self.waterMass,self.elevation,self.qaLiquidNeighbors,self.qaLiquidEdges,self.newWaterMass,self.getKmPerWaterMass(),dt,false) catch unreachable;
                    const elapsed=std.time.nanoTimestamp()-begin;
                    std.debug.print("LIQUID_GATHER {{\\"signed\\":{e},\\"sumabs\\":{e},\\"ns\\":{d},\\"scratch_bytes\\":{d}}}\\n",.{receipt.rounding_signed,receipt.rounding_absolute,elapsed,n*(@sizeOf([6]f64)+@sizeOf([6]usize))});
                }
'''+needle)
p.write_text(s);(out/'simulation/liquid_gather.zig').write_text((r/'src/experimental/liquid_gather.zig').read_text())
p=out/'main.zig';s=p.read_text().replace(str(source.parent),str(out.parent));p.write_text(s)
print(out)
