#!/usr/bin/env python3
"""Isolated exact atmospheric geometry reuse experiment; no production edits."""
from pathlib import Path
import shutil,sys
source=Path(sys.argv[1]);out=Path(sys.argv[2]);shutil.copytree(source,out,dirs_exist_ok=True)
p=out/'simulation/planet.zig';s=p.read_text();s=s.replace('    transformedPoints: []Vec3,','    transformedPoints: []Vec3,\n    qaGeometry: @import("../qa_geometry_cache.zig").Cache = .{},',1)
# No serialized state changes. Lifetime follows the Planet.
a=s.index('    pub fn deinit(');i=s.index('\n',a);s=s[:i]+ '\n        var qa_geometry=self.qaGeometry;qa_geometry.deinit();'+s[i:]
a=s.index('    fn atmosphericWind(');i=s.index('        const normal=',a);s=s[:i]+'''        if(self.qaGeometry.matches(self.transformedPoints.len)) {
            const basis=self.qaGeometry.bases[index];const velocity=self.airVelocity[index];
            const wind=basis[0].scale(velocity.x()).add(basis[1].scale(velocity.y()));
            return .{wind.x(),wind.y(),wind.z()};
        }
'''+s[i:]
a=s.index('    fn atmosphericEdgeRate(');i=s.index('        return AtmosphereWater.edgeRate',a);s=s[:i]+'''        if(self.qaGeometry.matches(self.transformedPoints.len)) {
            for(self.getNeighbours(from),0..)|n,j|if(n==to)return self.qaGeometry.rate(from,j,wind);
        }
'''+s[i:]
a=s.index('    fn simulateAtmosphereWater(');i=s.index('        // Velocity jobs',a);s=s[:i]+'''        self.qaGeometry.prepare(self.allocator,self.transformedPoints,self.verticesNeighbours) catch self.qaGeometry.deinit();
'''+s[i:]
p.write_text(s)
(out/'qa_geometry_cache.zig').write_text(r'''
const std=@import("std");const Vec3=@import("zalgebra").Vec3;
const Edge=struct {d:[3]f64=.{0,0,0},length2:f64=0,valid:bool=false};
fn samePoints(a:[]const Vec3,b:[]const [3]f32)bool{if(a.len!=b.len)return false;for(a,b)|p,q|{for(0..3)|k|if(@as(u32,@bitCast(p.data[k]))!=@as(u32,@bitCast(q[k])))return false;}return true;}
pub const Cache=struct {
 allocator:?std.mem.Allocator=null,points:[][3]f32=&.{},topology:[][6]u32=&.{},bases:[][2]Vec3=&.{},edges:[][6]Edge=&.{},ready:bool=false,
 pub fn deinit(c:*Cache)void{if(c.allocator)|a|{a.free(c.points);a.free(c.topology);a.free(c.bases);a.free(c.edges);}c.*=.{};}
 pub fn matches(c:Cache,n:usize)bool{return c.ready and c.points.len==n;}
 pub fn prepare(c:*Cache,a:std.mem.Allocator,points:[]const Vec3,topology:[]const [6]u32)!void{
  if(points.len!=topology.len)return error.BadShape;
  if(c.points.len!=points.len){c.deinit();c.allocator=a;errdefer c.deinit();c.points=try a.alloc([3]f32,points.len);c.topology=try a.alloc([6]u32,points.len);c.bases=try a.alloc([2]Vec3,points.len);c.edges=try a.alloc([6]Edge,points.len);}
  if(c.ready and samePoints(points,c.points) and std.mem.eql(u8,std.mem.sliceAsBytes(topology),std.mem.sliceAsBytes(c.topology)))return;
  c.ready=false;for(points,0..)|point,i|c.points[i]=.{point.x(),point.y(),point.z()};@memcpy(c.topology,topology);
  for(points,0..)|point,i|{
   const normal=point.norm();var right=normal.cross(Vec3.back());if(right.length()<0.000001)right=normal.cross(Vec3.new(0,1,0));right=right.norm();const up=normal.cross(right).norm();c.bases[i]=.{right,up};
   for(topology[i],0..)|n,j|{
    if(n>=points.len)return error.BadTopology;
    var e=Edge{.valid=true};for(0..3)|k|{const x:@TypeOf(@as(f64,0))=point.data[k];const y:f64=points[n].data[k];if(!std.math.isFinite(x) or !std.math.isFinite(y))e.valid=false;e.d[k]=y-x;e.length2+=e.d[k]*e.d[k];}
    if(!std.math.isFinite(e.length2) or e.length2<=0)e.valid=false;c.edges[i][j]=e;
   }
  }
  c.ready=true;
 }
 pub fn rate(c:Cache,from:usize,j:usize,wind:[3]f64)f64{const e=c.edges[from][j];if(!e.valid)return 0;var dot:f64=0;for(0..3)|k|{if(!std.math.isFinite(wind[k]))return 0;dot+=wind[k]*e.d[k];}if(!std.math.isFinite(dot))return 0;return @max(0,dot/e.length2);}
};
''')
# Snapshot AFTER timed frames, before restore, to independently compare complete state.
p=out/'main.zig';s=p.read_text();needle='  phase.enabled=false;';assert needle in s
s=s.replace(needle,'''  if(std.posix.getenv("STELLA_CPU_RESULT_PREFIX"))|prefix|{const name=try std.fmt.allocPrint(a,"{s}-{s}.json",.{prefix,label});try std.fs.cwd().writeFile(.{.sub_path=name,.data=try std.json.stringifyAlloc(a,try saves.capture(a,state),.{})});}
'''+needle,1);p.write_text(s)
p=out/'qa_geometry_cache.zig';p.write_text(p.read_text()+r'''
test "exact geometry cache rates and content invalidation"{
 const Ref=@import("simulation/atmosphere_water.zig");const a=std.testing.allocator;var c=Cache{};defer c.deinit();
 var points=[_]Vec3{Vec3.new(1,2,3),Vec3.new(4,5,6),Vec3.new(7,8,9)};var topo=[_][6]u32{.{0,1,2,0,1,2}}**3;
 var rng=std.rand.DefaultPrng.init(2027);const random=rng.random();
 for(0..5)|epoch|{
  if(epoch==1)points[1]=Vec3.new(-4,2,8);if(epoch==2)topo[0][1]=2;if(epoch==3)points[2]=Vec3.new(0,0,20);if(epoch==4)points[0]=Vec3.new(std.math.nan(f32),2,3);
  try c.prepare(a,&points,&topo);try c.prepare(a,&points,&topo);
  for(0..100)|_|for(0..3)|i|for(topo[i],0..)|n,j|{
   const w=[3]f64{random.float(f32)-0.5,random.float(f32)-0.5,random.float(f32)-0.5};const x=points[i];const y=points[n];const expected=Ref.edgeRate(.{x.x(),x.y(),x.z()},.{y.x(),y.y(),y.z()},w);
   try std.testing.expectEqual(@as(u64,@bitCast(expected)),@as(u64,@bitCast(c.rate(i,j,w))));
  };
 }
 std.debug.print("GEOMETRY_CACHE exact_rates=9000 geometry_and_topology_changes=true bytes_per_point={d} bytes40k={d} bytes163k={d}\\n",.{@sizeOf([3]f32)+@sizeOf([6]u32)+@sizeOf([2]Vec3)+@sizeOf([6]Edge),40962*(@sizeOf([3]f32)+@sizeOf([6]u32)+@sizeOf([2]Vec3)+@sizeOf([6]Edge)),163842*(@sizeOf([3]f32)+@sizeOf([6]u32)+@sizeOf([2]Vec3)+@sizeOf([6]Edge))});
}
''')
