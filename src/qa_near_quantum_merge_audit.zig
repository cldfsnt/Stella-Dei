const std=@import("std");const Q=@import("experimental/near_quantum.zig");
test "finite f128 equality is not arbitrary-exponent exact accounting" {
 const source:f32=1;const quantum=@as(f64,source)-std.math.nextAfter(f32,source,0);
 const stores=[_]f64{0,0,0,0};const caps=[_]f64{quantum*0.75,0x1p-200,0,0};
 const p=Q.plan(source,1,stores,caps) orelse return error.UnexpectedRefusal;
 const escrow=Q.mergeEscrow(p,0,stores,source,1) orelse return error.UnexpectedRefusal;
 // Large terms alone exactly exhaust source; tiny credited receiver is extra.
 try std.testing.expectEqual(quantum,p.stores[0]+escrow);
 try std.testing.expect(p.stores[1]>0);
 std.debug.print("extreme witness q={e}, large={e}, small={e}, escrow={e}; large+escrow=q with additional positive small receipt\n",.{quantum,p.stores[0],p.stores[1],escrow});
}
test "actual merge either refuses or balances in declared f128 arithmetic" {
 var rng=std.Random.DefaultPrng.init(28491);const random=rng.random();var accepted:usize=0;var refused:usize=0;
 for(0..10000)|k|{const source:f32=@floatCast(1+random.float(f64));const conversion=std.math.pow(f64,10,@as(f64,@floatFromInt(k%31))-15);const quantum=(@as(f64,source)-std.math.nextAfter(f32,source,0))*conversion;var stores:[4]f64=undefined;var caps:[4]f64=undefined;for(0..4)|i|{stores[i]=quantum*random.float(f64);caps[i]=stores[i]+quantum*(0.1+0.15*random.float(f64));}const p=Q.plan(source,conversion,stores,caps) orelse continue;const before=if(k%2==0)@as(f64,0) else quantum*random.float(f64);if(Q.mergeEscrow(p,before,stores,source,conversion))|after|{accepted+=1;var got:f128=@as(f128,after)-before;for(0..4)|i|got+=@as(f128,p.stores[i])-stores[i];const paid=(@as(f128,source)-p.pool)*@as(f128,conversion);try std.testing.expectEqual(paid,got);}else refused+=1;}
 std.debug.print("merge accepted={d}, refused={d}\n",.{accepted,refused});try std.testing.expect(accepted>0 and refused>0);
}
