const std=@import("std");const P=@import("physical_water_f64.zig");

pub const Result=struct{soil:f64,vapor:f64,paid:f64=0,funded:f64=0,native_received:f64=0,residual_density:f64=0};
pub fn step(soil:f64,vapor:f64,area:f64,wanted:f64)?Result{
 @setFloatMode(.strict);if(!std.math.isFinite(area) or area<=0 or !std.math.isFinite(vapor) or vapor<0)return null;
 const keep=Result{.soil=soil,.vapor=vapor};const removed=P.remove(soil,wanted) orelse return null;if(removed.paid==0)return keep;
 const budget=P.downRatio(P.downProduct(removed.paid,area),1e9);if(!std.math.isFinite(budget))return null;
 var after=vapor+budget;if(!std.math.isFinite(after))return null;const delta=P.difference(after,vapor);if(delta.hi>budget or (delta.hi==budget and delta.lo>0))after=std.math.nextAfter(f64,after,vapor);
 const received=P.downDifference(after,vapor);if(received<=0)return keep;
 const sd=P.difference(soil,removed.after);const vd=P.difference(after,vapor);
 // F64 outward intervals enclose exact represented source/receiver deltas.
 // Reject nonfinite bounds or an unresolved positive lower bound; never top up.
 const source_sum=sd.hi+sd.lo;const receiver_sum=vd.hi+vd.lo;
 const source_lo=lower(lower(source_sum)*area);const source_hi=upper(upper(source_sum)*area);
 const receiver_lo=lower(lower(receiver_sum)*1e9);const receiver_hi=upper(upper(receiver_sum)*1e9);
 const error_hi=@max(upper(@abs(receiver_lo-source_hi)),upper(@abs(receiver_hi-source_lo)));
 const vu=@max(std.math.nextAfter(f64,after,std.math.inf(f64))-after,after-std.math.nextAfter(f64,after,-std.math.inf(f64)));
 const su=@max(std.math.nextAfter(f64,soil,std.math.inf(f64))-soil,soil-std.math.nextAfter(f64,soil,-std.math.inf(f64)));
 if(!std.math.isFinite(vu) or !std.math.isFinite(su))return keep;
 // Lower, not upper, budget prevents an outward-rounded allowance relaxing
 // the original exact arithmetic envelope used by the offline oracle.
 const vapor_ulp=lower(vu*1e9);const soil_ulp=lower(su*area);
 const envelope=lower(lower(lower(2*vapor_ulp)+lower(2*soil_ulp))+lower((16*std.math.floatEps(f64))*source_lo));
 const relative=lower(source_lo*0x1p-20);
 if(!std.math.isFinite(source_hi) or !std.math.isFinite(receiver_hi) or !std.math.isFinite(envelope) or !std.math.isFinite(error_hi) or source_lo<=0 or error_hi>relative or error_hi>envelope)return keep;
 const funded=@min(removed.paid,P.downRatio(P.downProduct(received,1e9),area));
 return .{.soil=removed.after,.vapor=after,.paid=removed.paid,.funded=funded,.native_received=received,.residual_density=(after-vapor)*1e9/area-(soil-removed.after)};
}


fn upper(x:f64)f64{return std.math.nextAfter(f64,x,std.math.inf(f64));}
fn lower(x:f64)f64{if(!std.math.isFinite(x))return x;return @max(0,std.math.nextAfter(f64,x,-std.math.inf(f64)));}
