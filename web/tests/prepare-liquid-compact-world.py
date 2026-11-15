from pathlib import Path
import shutil
r=Path(__file__).resolve().parents[2];b=r.parent/'site-tmp';source=b/'liquid-timing-cached/src';out=b/'liquid-timing-compact/src';shutil.copytree(source,out,dirs_exist_ok=True)
p=out/'simulation/planet.zig';s=p.read_text().replace('qaLiquidEdges:[][6]f64','qaLiquidEdges:[][6]f32').replace('    qaLiquidReverse:[][6]u8=&.{},','    qaLiquidReverse:[][6]u8=&.{},\n    qaLiquidHeads:[]f32=&.{},').replace('alloc([6]f64,n)','alloc([6]f32,n)');s=s.replace('                        self.invalidateLiquidTopology();','                        self.qaLiquidHeads=self.simulationArena.allocator().alloc(f32,n) catch unreachable;\n                        self.invalidateLiquidTopology();');s=s.replace('liquid_gather_cached.zig','liquid_gather_compact.zig').replace('self.qaLiquidReverse,self.qaLiquidEdges,self.newWaterMass','self.qaLiquidReverse,self.qaLiquidEdges,self.qaLiquidHeads,self.newWaterMass');p.write_text(s)
(out/'simulation/liquid_gather_compact.zig').write_text((r/'src/experimental/liquid_gather_compact.zig').read_text())
p=out/'main.zig';p.write_text(p.read_text().replace(str(source.parent),str(out.parent)));print(out)
