//! Explicit selected-patch removal, not hydrology or evaporation.
const std=@import("std");const rates=@import("edit_rates.zig");
pub const Status=enum{changed,dry,no_change,invalid,precision};
pub const Result=struct{status:Status,removed_m:f64=0};
pub fn remove(water:[]f32,index:usize,km_per_mass:f32,tap:bool,elapsed:f32) Result {
 if(index>=water.len or !std.math.isFinite(km_per_mass) or km_per_mass<=0)return .{.status=.invalid};
 const before=water[index];if(!std.math.isFinite(before) or before<0 or (!tap and (!std.math.isFinite(elapsed) or elapsed<0)))return .{.status=.invalid};
 if(before==0)return .{.status=.dry};
 const requested:f64=rates.water(tap,elapsed);if(requested<=0)return .{.status=.no_change};
 const next:f32=@floatCast(@max(0,@as(f64,before)-requested/@as(f64,km_per_mass)));
 const removed_km=(@as(f64,before)-next)*km_per_mass;
 if(!std.math.isFinite(removed_km) or removed_km<=0 or removed_km>requested+@max(1e-12,requested*1e-5))return .{.status=.precision};
 water[index]=next;return .{.status=.changed,.removed_m=removed_km*1000};
}
test "selected water removal is gradual bounded and never changes neighbors" {
 var water=[_]f32{5,7,9};const first=remove(&water,0,0.001,true,0);try std.testing.expectEqual(Status.changed,first.status);try std.testing.expectApproxEqAbs(@as(f64,1),first.removed_m,0.00001);try std.testing.expectEqual(@as(f32,4),water[0]);try std.testing.expectEqual(@as(f32,7),water[1]);try std.testing.expectEqual(@as(f32,9),water[2]);
 water[0]=0.25;const last=remove(&water,0,0.001,true,0);try std.testing.expectApproxEqAbs(@as(f64,0.25),last.removed_m,0.00001);try std.testing.expectEqual(@as(f32,0),water[0]);try std.testing.expectEqual(Status.dry,remove(&water,0,0.001,true,0).status);
}
test "removal gesture matches rate across frames and no elapsed spike" {
 for([_]u32{15,30,60,120})|fps|{var water=[_]f32{20,7};var total=remove(&water,0,0.001,true,0).removed_m;for(0..fps*2)|_|total+=remove(&water,0,0.001,false,1/@as(f32,@floatFromInt(fps))).removed_m;try std.testing.expectApproxEqAbs(@as(f64,11),total,0.001);try std.testing.expectEqual(@as(f32,7),water[1]);}
 var water=[_]f32{20};const r=remove(&water,0,0.001,false,999);try std.testing.expect(r.removed_m<=0.50001);try std.testing.expectEqual(Status.no_change,remove(&water,0,0.001,false,0).status);
}
test "invalid or unresolved water removal refuses atomically" {
 for(0..7)|case|{var water=[_]f32{10,7};var conversion:f32=0.001;var index:usize=0;var elapsed:f32=0.1;switch(case){0=>conversion=0,1=>conversion=std.math.nan(f32),2=>index=99,3=>water[0]=std.math.inf(f32),4=>water[0] = -1,5=>elapsed=std.math.nan(f32),6=>elapsed = -1,else=>unreachable}const before=water;try std.testing.expectEqual(Status.invalid,remove(&water,index,conversion,false,elapsed).status);try std.testing.expectEqualSlices(u8,std.mem.asBytes(&before),std.mem.asBytes(&water));}
 var deep=[_]f32{1e20,7};const old=deep;try std.testing.expectEqual(Status.precision,remove(&deep,0,0.001,true,0).status);try std.testing.expectEqualSlices(f32,&old,&deep);
}
