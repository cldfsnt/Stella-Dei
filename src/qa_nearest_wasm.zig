const std=@import("std");const V=@import("zalgebra").Vec3;const N=@import("experimental/nearest_sqrt_prune.zig");const Candidate=@import("nearest_point.zig");
var hash:u64=1469598103934665603;var count:u32=0;
fn check(points:[]const V,q:V)bool{const a=N.reference(points,q);const b=Candidate.nearest(points,q);hash=(hash^@as(u64,b))*%1099511628211;count+=1;return a==b;}
export fn qa_run()u32{
 hash=1469598103934665603;count=0;var fail:u32=0;
 const z=V.zero();const a=V.new(1,0.00034526698,0);const b=V.new(1,0,0);
 if(!(a.dot(a)>b.dot(b) and a.distance(z)==b.distance(z)))fail|=1;
 if(!check(&.{a,b},z) or Candidate.nearest(&[_]V{a,b},z)!=0)fail|=2;
 if(!check(&.{b,a},z))fail|=4;
 var special=[_]V{V.new(std.math.nan(f32),0,0),V.new(std.math.inf(f32),0,0),V.new(1e30,0,0),V.new(-0.0,0,0),z,V.new(3,4,5)};
 for([_]V{z,V.new(1,2,3),V.new(-5000,100,200),V.new(1e10,0,0)})|q|if(!check(&special,q)){fail|=8;};
 special[3]=V.new(4000,2,3);special[4]=V.new(9,8,7);if(!check(&special,z))fail|=16;special[0]=V.new(0.01,0,0);if(!check(&special,z))fail|=32;
 var rng=std.rand.DefaultPrng.init(57265);var points:[128]V=undefined;
 for(0..1000)|_|{for(&points)|*p|p.*=V.new((rng.random().float(f32)-0.5)*20000,(rng.random().float(f32)-0.5)*20000,(rng.random().float(f32)-0.5)*20000);const q=V.new((rng.random().float(f32)-0.5)*30000,(rng.random().float(f32)-0.5)*30000,(rng.random().float(f32)-0.5)*30000);if(!check(&points,q))fail|=64;}
 return fail;
}
export fn qa_hash()u64{return hash;}
export fn qa_count()u32{return count;}
