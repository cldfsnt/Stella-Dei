//! Experimental authoritative f64-density receiver only, not a mirrored pool.
const std=@import("std");const P=@import("physical_water_f64.zig");
pub const Receipt=struct{source:f64,vapor:f64,paid:f64=0};
fn receiver(old:f64,budget:f64)?f64{
 @setFloatMode(.strict);var next=old+budget;if(!std.math.isFinite(next))return null;
 const delta=P.difference(next,old);if(delta.hi>budget or (delta.hi==budget and delta.lo>0))next=std.math.nextAfter(f64,next,old);
 return next;
}
pub fn transfer(source:f64,vapor:f64,request:f64)?Receipt{
 @setFloatMode(.strict);
 if(!std.math.isFinite(source) or source<0 or !std.math.isFinite(vapor) or vapor<0 or !std.math.isFinite(request) or request<0)return null;
 const unchanged=Receipt{.source=source,.vapor=vapor};const budget=@min(source,request);
 const proposal=receiver(vapor,budget) orelse return null;const initial=P.downDifference(proposal,vapor);
 const removal=P.remove(source,initial) orelse return null;
 const target=receiver(vapor,removal.paid) orelse return null;const credit=P.difference(target,vapor);
 const actual=P.remove(source,credit.hi) orelse return null;const debit=P.difference(source,actual.after);
 if(credit.lo!=0 or debit.lo!=0 or credit.hi!=debit.hi or credit.hi<0 or credit.hi>budget)return unchanged;
 return .{.source=actual.after,.vapor=target,.paid=credit.hi};
}
