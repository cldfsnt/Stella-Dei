//! Isolated native microbenchmark. Synthetic spherical mesh, not browser frame rate.
const std=@import("std");const P=@import("simulation/planet.zig").Planet;const V=@import("zalgebra").Vec3;
fn squared(points:[]const V,q:V,comptime preserve:bool)usize{
 var best:f32=std.math.inf(f32);var root:f32=std.math.inf(f32);var idx:usize=0;
 for(points,0..)|point,i|{const d=point.sub(q);const s=d.dot(d);if(s<best){if(preserve){const r=@sqrt(s);if(r>=root)continue;root=r;}best=s;idx=i;}}
 return idx;
}
test "nearest exact semantics and bounded native baseline" {
 var p:P=undefined;
 var edge=[_]V{V.new(1,0.0003,0),V.new(1,0,0)};p.transformedPoints=&edge;
 try std.testing.expectEqual(@as(usize,0),p.getNearestPointTo(V.zero()));
 try std.testing.expectEqual(@as(usize,1),squared(&edge,V.zero(),false));
 try std.testing.expectEqual(@as(usize,0),squared(&edge,V.zero(),true));
 const points=try std.testing.allocator.alloc(V,40962);defer std.testing.allocator.free(points);
 var random=std.Random.DefaultPrng.init(123456);const rng=random.random();
 for(points)|*point|point.*=V.new(rng.float(f32)*2-1,rng.float(f32)*2-1,rng.float(f32)*2-1).norm().scale(5000+rng.float(f32)*50);
 var queries:[200]V=undefined;for(&queries)|*q|q.*=V.new(rng.float(f32)*2-1,rng.float(f32)*2-1,rng.float(f32)*2-1).norm().scale(5000+rng.float(f32)*10000);
 p.transformedPoints=points;var naive_changes:usize=0;
 for(queries)|q|{const old=p.getNearestPointTo(q);try std.testing.expectEqual(old,squared(points,q,true));if(old!=squared(points,q,false))naive_changes+=1;}
 var checksum:usize=0;
 for(0..5)|repeat|{inline for(0..3)|kind|{var timer=try std.time.Timer.start();for(queries)|q|{checksum+%=if(kind==0)p.getNearestPointTo(q) else if(kind==1)squared(points,q,false) else squared(points,q,true);}const elapsed=timer.read();std.debug.print("NEAREST repeat={d} kind={d} n={d} queries={d} ns={d} ns_per_query={d} checksum={d} naive_changed={d}\n",.{repeat,kind,points.len,queries.len,elapsed,elapsed/queries.len,checksum,naive_changes});}}
}
