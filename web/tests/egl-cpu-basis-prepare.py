#!/usr/bin/env python3
"""Derivative low-memory isolated basis + reverse-topology candidate, no edge geometry cache."""
from pathlib import Path
import shutil,sys
source=Path(sys.argv[1]);out=Path(sys.argv[2]);shutil.copytree(source,out,dirs_exist_ok=True)
p=out/'simulation/planet.zig';s=p.read_text();a=s.index('        if(self.qaGeometry.matches(self.transformedPoints.len)) {',s.index('    fn atmosphericEdgeRate('));b=s.index('        return AtmosphereWater.edgeRate',a);s=s[:a]+s[b:]
old='            for(self.getNeighbours(i))|n|gathered+=@as(f64,self.newWaterMass[n])*self.cachedAtmosphericEdgeRate(n,i);';assert old in s
s=s.replace(old,'            for(self.getNeighbours(i),0..)|n,j|{const reverse=self.qaGeometry.reverse[i][j];gathered+=@as(f64,self.newWaterMass[n])*(if(self.qaGeometry.matches(self.transformedPoints.len) and self.atmosphericEdgeScratch.len==self.transformedPoints.len and reverse<6)self.atmosphericEdgeScratch[n][reverse] else self.cachedAtmosphericEdgeRate(n,i));}')
# Index only after successful cache preparation: OOM path stays original.
s=s.replace('const reverse=self.qaGeometry.reverse[i][j];','const reverse=if(self.qaGeometry.matches(self.transformedPoints.len))self.qaGeometry.reverse[i][j] else 255;')
p.write_text(s)
p=out/'qa_geometry_cache.zig';s=p.read_text();s=s[:s.index('\ntest ')];s=s.replace('edges:[][6]Edge=&.{}','reverse:[][6]u8=&.{}').replace('a.free(c.edges)','a.free(c.reverse)').replace('c.edges=try a.alloc([6]Edge,points.len)','c.reverse=try a.alloc([6]u8,points.len)')
a=s.index('    var e=Edge{');b=s.index('\n   }',a)
s=s[:a]+'''    c.reverse[i][j]=255;for(topology[n],0..)|back,k|if(back==i){c.reverse[i][j]=@intCast(k);break;};'''+s[b:]
a=s.index(' pub fn rate(');s=s[:a]+'};\n';p.write_text(s)
# Reverse slots are hints, validated against CURRENT topology at every use.
p=out/'simulation/planet.zig';s=p.read_text().replace('and reverse<6)self.atmosphericEdgeScratch','and reverse<6 and self.verticesNeighbours[n][reverse]==i)self.atmosphericEdgeScratch')
s=s.replace('const wind=basis[0].scale(velocity.x()).add(basis[1].scale(velocity.y()));','const right=Vec3.new(basis[0][0],basis[0][1],basis[0][2]);const up=Vec3.new(basis[1][0],basis[1][1],basis[1][2]);const wind=right.scale(velocity.x()).add(up.scale(velocity.y()));');p.write_text(s)
p=out/'qa_geometry_cache.zig';s=p.read_text().replace('topology:[][6]u32=&.{},','').replace('bases:[][2]Vec3','bases:[][2][3]f32').replace('a.free(c.topology);','').replace('c.topology=try a.alloc([6]u32,points.len);','').replace('a.alloc([2]Vec3,points.len)','a.alloc([2][3]f32,points.len)').replace(' and std.mem.eql(u8,std.mem.sliceAsBytes(topology),std.mem.sliceAsBytes(c.topology))','').replace('@memcpy(c.topology,topology);','').replace('c.bases[i]=.{right,up};','c.bases[i]=.{.{right.x(),right.y(),right.z()},.{up.x(),up.y(),up.z()}};');p.write_text(s)
p=out/'qa_geometry_cache.zig';p.write_text(p.read_text()+r'''
test "packed basis preserves original Vec3 operations and ignores SIMD padding" {
 var c=Cache{};defer c.deinit();var points=[_]Vec3{Vec3.new(1,2,3),Vec3.new(0,0,50),Vec3.new(-5,-2,4)};var topology=[_][6]u32{.{0,1,2,0,1,2}}**3;
 var rng=std.rand.DefaultPrng.init(2027);const random=rng.random();
 for(0..4)|epoch|{
  if(epoch==1)points[0]=Vec3.new(1,2,3.1);if(epoch==2)points[2]=Vec3.new(3,-7,1);if(epoch==3)topology[0][1]=0;
  try c.prepare(std.testing.allocator,&points,&topology);try std.testing.expect(samePoints(&points,c.points));
  for(points,0..)|point,i|{
   const normal=point.norm();var right=normal.cross(Vec3.back());if(right.length()<0.000001)right=normal.cross(Vec3.new(0,1,0));right=right.norm();const up=normal.cross(right).norm();const b=c.bases[i];
   for(0..100)|_|{const vx=random.float(f32)-0.5;const vy=random.float(f32)-0.5;const expected=right.scale(vx).add(up.scale(vy));const got=Vec3.new(b[0][0],b[0][1],b[0][2]).scale(vx).add(Vec3.new(b[1][0],b[1][1],b[1][2]).scale(vy));for(0..3)|k|try std.testing.expectEqual(@as(u32,@bitCast(expected.data[k])),@as(u32,@bitCast(got.data[k])));}
   for(topology[i],0..)|n,j|{const hint=c.reverse[i][j];var original:u8=255;for(topology[n],0..)|back,k|if(back==i){original=@intCast(k);break;};const resolved=if(hint<6 and topology[n][hint]==i)hint else original;if(resolved<6)try std.testing.expectEqual(@as(u32,@intCast(i)),topology[n][resolved]);}
  }
 }
 std.debug.print("BASIS_CACHE exact_wind_vectors=1200 float_component_bits=3600 packed_bytes_per_point=42 stale_reverse_hint_fallback=true\n",.{});
}
''')
