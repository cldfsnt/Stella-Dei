//! Exact-bit native/WASM parity against frozen pre-hoist scalar formula.
const std=@import("std");const E=@import("simulation/atmosphere_water.zig").EdgeSource;
fn reference(from:[3]f64,to:[3]f64,wind:[3]f64)f64{
 var length2:f64=0;var dot:f64=0;for(0..3)|i|{if(!std.math.isFinite(from[i]) or !std.math.isFinite(to[i]) or !std.math.isFinite(wind[i]))return 0;const d=to[i]-from[i];length2+=d*d;dot+=wind[i]*d;}
 if(length2<=0 or !std.math.isFinite(length2) or !std.math.isFinite(dot))return 0;return @max(0,dot/length2);
}
fn same(a:[3]f64,b:[3]f64,w:[3]f64)bool{return @as(u64,@bitCast(reference(a,b,w)))==@as(u64,@bitCast(E.init(a,w).rate(b)));}
export fn qa_run()u32{
 var rng=std.rand.DefaultPrng.init(2027);const random=rng.random();var fail:u32=0;
 for(0..100000)|_|{var a:[3]f64=undefined;var b=a;var w=a;for(0..3)|k|{a[k]=random.float(f64)*20000-10000;b[k]=random.float(f64)*20000-10000;w[k]=random.float(f64)*20-10;}if(!same(a,b,w))fail+=1;}
 const specials=[_]f64{0,-0.0,std.math.inf(f64),-std.math.inf(f64),std.math.nan(f64),std.math.floatMax(f64),-std.math.floatMax(f64),std.math.floatMin(f64),@bitCast(@as(u64,1))};
 for(specials)|v|for(0..3)|k|for(0..3)|kind|{var a=[_]f64{1,2,3};var b=[_]f64{4,5,6};var w=[_]f64{0.1,-0.2,0.3};if(kind==0)a[k]=v else if(kind==1)b[k]=v else w[k]=v;if(!same(a,b,w))fail+=1;};
 if(!same(.{1,2,3},.{1,2,3},.{1,1,1}))fail+=1;
 return fail;
}
test "prepared edge source exact native parity"{try std.testing.expectEqual(@as(u32,0),qa_run());}
