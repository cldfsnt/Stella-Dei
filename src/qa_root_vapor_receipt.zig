const std=@import("std");const T=@import("experimental/root_vapor_receipt.zig");const P=@import("experimental/physical_water_f64.zig");
fn check(s:f64,v:f64,w:f64)!T.Receipt{const r=T.transfer(s,v,w).?;const debit=P.difference(s,r.source);const credit=P.difference(r.vapor,v);try std.testing.expectEqual(@as(f64,0),debit.lo);try std.testing.expectEqual(@as(f64,0),credit.lo);try std.testing.expectEqual(debit.hi,credit.hi);try std.testing.expectEqual(r.paid,debit.hi);try std.testing.expect(r.paid<=w and r.paid<=s and r.paid>=0);return r;}
test "actual two pulse operands authoritative f64 receiver"{
 const samples=[_][3]f64{.{0.9999999167069676,1680.0450439453125,5.445914790658257e-5},.{0.9999991749741014,1635.706298828125,1.3555834952327928e-6}};
 for(samples,0..)|x,i|{const density=x[1]*1e9/7669529600.0;const r=try check(x[0],density,x[2]);const old:f32=@floatCast(x[1]+x[2]*7669529600.0/1e9);const oldcredit=(@as(f64,old)-x[1])*1e9/7669529600.0;std.debug.print("PULSE {} request={e} f32_received={e} f64_exact_receipt={e} refused_fraction={e}\n",.{i,x[2],oldcredit,r.paid,(x[2]-r.paid)/x[2]});try std.testing.expect(r.paid>0);}
}
test "fixed extreme and weak flow matrix exact funding no hidden accumulation"{
 var positive:usize=0;var refused:usize=0;
 for(0..10000)|i|{const es:i32=@intCast(i%41);const ev:i32=@intCast((i/41)%41);const er:i32=@intCast((i/1681)%6);const source=std.math.pow(f64,2,@as(f64,@floatFromInt(es-20)));const vapor=std.math.pow(f64,2,@as(f64,@floatFromInt(ev-20)));const want=source*std.math.pow(f64,2,@as(f64,@floatFromInt(-er*12-1)));const r=try check(source,vapor,want);if(r.paid>0)positive+=1 else refused+=1;}
 var source:f64=1;var vapor:f64=200;var paid:f64=0;for(0..10000)|_|{const r=try check(source,vapor,0.00001);paid+=r.paid;source=r.source;vapor=r.vapor;}try std.testing.expectApproxEqAbs(@as(f64,1)-source,paid,0);try std.testing.expectApproxEqAbs(vapor-200,paid,0);
 const weak=try check(1,1e30,1e-20);try std.testing.expectEqual(@as(f64,0),weak.paid);try std.testing.expectEqual(@as(f64,1),weak.source);const zero=try check(0,200,1);try std.testing.expectEqual(@as(f64,0),zero.paid);std.debug.print("MATRIX positive={} refused={} repeated_paid={e}\n",.{positive,refused,paid});
}
test "invalid values refuse without mutable state"{try std.testing.expect(T.transfer(1,std.math.inf(f64),1)==null);try std.testing.expect(T.transfer(-1,1,1)==null);try std.testing.expect(T.transfer(1,1,std.math.nan(f64))==null);}
