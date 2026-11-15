const std=@import("std");const H=@import("experimental/hydration_signal.zig");const X=@import("experimental/hydration_exchange_signal.zig");
test "independent geometry metres and invalid boundaries"{
 try std.testing.expectEqual(@as(f64,0),H.exposure(0.01,0.1).?);try std.testing.expectApproxEqAbs(@as(f64,0.6),H.exposure(0.5,0.2).?,1e-15);
 for([_]f64{0,1e-300,0.01,0.5,1e300})|h|try std.testing.expectEqual(@as(f64,1),H.exposure(h,0).?);
 try std.testing.expectEqual(@as(f64,0),H.exposure(0,1e-300).?);
 for([_]f64{-1,std.math.inf(f64),std.math.nan(f64)})|bad|{try std.testing.expect(H.exposure(bad,0)==null);try std.testing.expect(H.exposure(1,bad)==null);try std.testing.expect(H.meanReserve(bad,1,1)==null);try std.testing.expect(H.meanReserve(0,bad,1)==null);try std.testing.expect(H.meanReserve(0,1,bad)==null);}
}
test "independent mean from clipped linear integral across scaling and exhaustion"{
 var rng=std.Random.DefaultPrng.init(38175);const r=rng.random();for(0..10000)|i|{const cap=std.math.pow(f64,10,@as(f64,@floatFromInt(i%601))-300);const w=cap*r.float(f64);const loss=cap*(r.float(f64)*4);const got=H.meanReserve(w,loss,cap).?;const lifetime:f128=if(loss==0)1 else @min(@as(f128,1),@as(f128,w)/loss);const integral=@as(f128,w)*lifetime-@as(f128,loss)*lifetime*lifetime/2;const expected:f64=@floatCast(integral/cap);try std.testing.expect(std.math.isFinite(got) and got>=0 and got<=1);try std.testing.expectApproxEqAbs(expected,got,4e-16);}
 try std.testing.expectEqual(@as(f64,0.125),H.meanReserve(1,4,1).?);try std.testing.expectEqual(@as(f64,0),H.meanReserve(0,0,0).?);try std.testing.expect(H.meanReserve(1,0,0)==null);
}
test "invalid adapter inputs refuse before mutation"{
 var c=X.M.initialized(17);c.cohorts[0]=.{.biomass=0.1,.lineage=1,.support_mass=0.01,.retention_allocation=0.25};var liquid:f32=1;var vapor:f32=0;const before=c;const env=X.M.Environment{.temperature=300,.depth_km=0,.light=1,.carbon_available=1,.oxygen_carbon_capacity=1};
 for([_]f32{0,-1,std.math.inf(f32),std.math.nan(f32)})|dt|{try std.testing.expect(X.step(3,&c,&liquid,&vapor,7669529600,env,dt)==null);try std.testing.expectEqualDeep(before,c);try std.testing.expectEqual(@as(f32,1),liquid);try std.testing.expectEqual(@as(f32,0),vapor);}
}
