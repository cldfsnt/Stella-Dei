const std=@import("std");const V=@import("zalgebra").Vec3;const N=@import("experimental/nearest_sqrt_prune.zig");const Candidate=@import("nearest_point.zig");
test "rounded sqrt ties preserve first-index not squared-nearest" {
 const a=V.new(1,0.00034526698,0);const b=V.new(1,0,0);const z=V.zero();
 try std.testing.expect(a.dot(a)>b.dot(b));try std.testing.expectEqual(a.distance(z),b.distance(z));
 try std.testing.expectEqual(@as(usize,0),Candidate.nearest(&[_]V{a,b},z));try std.testing.expectEqual(@as(usize,0),Candidate.nearest(&[_]V{b,a},z));
}
test "defined winners retain signed zero ties NaNs infinities overflow and changed geometry" {
 var points=[_]V{V.new(std.math.nan(f32),0,0),V.new(std.math.inf(f32),0,0),V.new(1e30,0,0),V.new(-0.0,0,0),V.zero(),V.new(3,4,5)};
 for([_]V{V.zero(),V.new(1,2,3),V.new(-5000,100,200),V.new(1e10,0,0)})|q|try std.testing.expectEqual(N.reference(&points,q),Candidate.nearest(&points,q));
 points[3]=V.new(4000,2,3);points[4]=V.new(9,8,7);try std.testing.expectEqual(N.reference(&points,V.zero()),Candidate.nearest(&points,V.zero()));
 points[0]=V.new(0.01,0,0);try std.testing.expectEqual(@as(usize,0),Candidate.nearest(&points,V.zero()));
}
test "deterministic broad finite ranges preserve metric winner" {
 var rng=std.rand.DefaultPrng.init(57265);var points:[128]V=undefined;
 for(0..1000)|_|{for(&points)|*p|p.*=V.new((rng.random().float(f32)-0.5)*20000,(rng.random().float(f32)-0.5)*20000,(rng.random().float(f32)-0.5)*20000);const q=V.new((rng.random().float(f32)-0.5)*30000,(rng.random().float(f32)-0.5)*30000,(rng.random().float(f32)-0.5)*30000);try std.testing.expectEqual(N.reference(&points,q),Candidate.nearest(&points,q));}
}
