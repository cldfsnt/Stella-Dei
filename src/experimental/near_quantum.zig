//! Isolated numerical fallback only. No production import or biological law.
const std=@import("std");
pub const Plan=struct{pool:f32,stores:[4]f64,debit:f64,credited:f64,remainder:f64};
// Error-free TwoSum check: f128 alone is not exact across arbitrary exponents.
fn exactAdd(a:f128,b:f128)?f128{@setFloatMode(.strict);const s=a+b;const bb=s-a;const err=(a-(s-bb))+(b-bb);if(!std.math.isFinite(s) or err!=0)return null;return s;}
fn down(x:f128)f64{var y:f64=@floatCast(x);if(@as(f128,y)>x)y=std.math.nextAfter(f64,y,0);return y;}
pub fn plan(pool:f32,conversion:f64,stores:[4]f64,caps:[4]f64)?Plan{
 @setFloatMode(.strict);
 if(!std.math.isFinite(pool) or pool<=0 or !std.math.isFinite(conversion) or conversion<=0)return null;
 var deficits:[4]f64=undefined;var total:f128=0;
 for(stores,caps,0..)|s,c,i|{if(!std.math.isFinite(s) or !std.math.isFinite(c) or s<0 or c<s)return null;deficits[i]=down(exactAdd(@as(f128,c),-@as(f128,s)) orelse return null);total=exactAdd(total,deficits[i]) orelse return null;}
 const demand=down(total);if(demand<=0 or !std.math.isFinite(demand))return null;
 // Verify the unchanged conservative algorithm would produce no debit.
 var ordinary:f32=@floatCast(@max(0,@as(f64,pool)-demand/conversion));
 if((@as(f64,pool)-ordinary)*conversion>demand)ordinary=std.math.nextAfter(f32,ordinary,std.math.inf(f32));
 if(ordinary<pool)return null;
 const after=std.math.nextAfter(f32,pool,0);const debit=(@as(f64,pool)-after)*conversion;
 if(!std.math.isFinite(debit) or debit<=0 or debit<=demand or debit-demand>demand)return null;
 var result=stores;var used:f128=0;
 for(stores,caps,0..)|s,c,i|{const grant=down(@as(f128,demand)*deficits[i]/total);const receiver=down(@as(f128,s)+grant);result[i]=@min(c,receiver);const receipt=exactAdd(@as(f128,result[i]),-@as(f128,s)) orelse return null;used=exactAdd(used,receipt) orelse return null;}
 // Stronger than nominal threshold: actual unused debit <= actual receipts.
 const excess=exactAdd(@as(f128,debit),-used) orelse return null;if(used<=0 or excess<0 or excess>used or excess>demand)return null;
 const remainder:f64=@floatCast(excess);if(!std.math.isFinite(remainder))return null;
 return .{.pool=after,.stores=result,.debit=debit,.credited=@floatCast(used),.remainder=remainder};
}

/// Commit preparation only: no mutation. Refuse a rounded-away/rounded-up
/// escrow increment rather than silently inventing or dropping stored water.
pub fn mergeEscrow(p:Plan,before:f64,old_stores:[4]f64,source_before:f32,conversion:f64)?f64{
 @setFloatMode(.strict);
 if(!std.math.isFinite(before) or before<0)return null;
 var used:f128=0;for(old_stores,p.stores)|old,new|{if(new<old)return null;const receipt=exactAdd(@as(f128,new),-@as(f128,old)) orelse return null;used=exactAdd(used,receipt) orelse return null;}
 if(!std.math.isFinite(source_before) or source_before<p.pool or !std.math.isFinite(conversion) or conversion<=0)return null;
 const physical=(@as(f128,source_before)-p.pool)*@as(f128,conversion);
 const exact=exactAdd(physical,-used) orelse return null;if(exact<0 or exact>used)return null;
 const after:f64=@floatCast(exactAdd(@as(f128,before),exact) orelse return null);
 if(!std.math.isFinite(after) or (exactAdd(@as(f128,after),-@as(f128,before)) orelse return null)!=exact)return null;
 return after;
}
