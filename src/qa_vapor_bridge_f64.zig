const std=@import("std");const B=@import("experimental/vapor_bridge_f64.zig");const Old=@import("experimental/vapor_bridge_f128_reference.zig");
fn emit(i:usize,s:f64,v:f64,a:f64,w:f64) !void {
 const result=B.step(s,v,a,w);const reference=Old.step(s,v,a,w);
 const json=try std.json.stringifyAlloc(std.testing.allocator,.{.i=i,.soil=s,.vapor=v,.area=a,.wanted=w,.result=result,.reference=reference},.{});defer std.testing.allocator.free(json);std.debug.print("BRIDGE {s}\n",.{json});
}
test "all30 observed daylight receipts unchanged" {
 const F=struct{soil_before:f64,vapor_before:f64,area_m2:f64,wanted:f64,soil_after:f64,vapor_after:f64,paid:f64,funded:f64};
 const parsed=try std.json.parseFromSlice([]F,std.testing.allocator,@embedFile("experimental/vapor_bridge_daylight_fixtures.json"),.{});defer parsed.deinit();
 for(parsed.value,0..)|f,i|{const b=B.step(f.soil_before,f.vapor_before,f.area_m2,f.wanted).?;try std.testing.expectEqual(f.soil_after,b.soil);try std.testing.expectEqual(f.vapor_after,b.vapor);try std.testing.expectEqual(f.paid,b.paid);try std.testing.expectEqual(f.funded,b.funded);try emit(i,f.soil_before,f.vapor_before,f.area_m2,f.wanted);}
}
test "fixed scales include subnormal zero saturation and overflow" {
 const values=[_]f64{0,0x1p-1074,0x1p-1022,0x1p-500,0x1p-50,1,0x1p50,0x1p500,std.math.floatMax(f64)};
 var i:usize=30;for(values)|s|for(values)|v|for([_]f64{0x1p-500,1,7669529600,0x1p500})|a|for([_]f64{0,0.125,0.5,1})|f|{try emit(i,s,v,a,s*f);i+=1;};
 var rng=std.Random.DefaultPrng.init(0x874519);for(0..5000)|_|{const s=std.math.pow(f64,2,@floatFromInt(rng.random().intRangeAtMost(i32,-500,500)))*(1+rng.random().float(f64));const v=std.math.pow(f64,2,@floatFromInt(rng.random().intRangeAtMost(i32,-500,500)))*rng.random().float(f64);const a=std.math.pow(f64,2,@floatFromInt(rng.random().intRangeAtMost(i32,-500,500)));try emit(i,s,v,a,s*rng.random().float(f64));i+=1;}
}
test "invalid and zero requests are atomic" {
 for([_]f64{std.math.nan(f64),std.math.inf(f64),-1})|x|{try std.testing.expect(B.step(x,1,1,1)==null);try std.testing.expect(B.step(1,x,1,1)==null);try std.testing.expect(B.step(1,1,x,1)==null);try std.testing.expect(B.step(1,1,1,x)==null);}
 const edge=B.step(std.math.floatMax(f64),0,0x1p-500,std.math.floatMax(f64)*0.125).?;try std.testing.expectEqual(@as(f64,0),edge.paid);
 const b=B.step(1,10,7669529600,0).?;try std.testing.expectEqual(@as(f64,1),b.soil);try std.testing.expectEqual(@as(f64,10),b.vapor);try std.testing.expectEqual(@as(f64,0),b.paid);
}
