//! Isolated mixed-authority phase probe. No Planet wiring or escrow.
const std=@import("std");
const P=@import("physical_water_f64.zig");
const A=@import("../simulation/atmosphere_water.zig");
pub const State=struct{liquid:f32,vapor:f64};
pub const Result=struct{state:State,evap_requested:f64=0,evap_paid:f64=0,rain_requested:f64=0,rain_paid:f64=0};
fn valid(x:f64)bool{return std.math.isFinite(x) and x>=0;}
fn exchange(s:State,w:f64,evap:bool)State{
 @setFloatMode(.strict);
 const old=@as(f64,s.liquid);const budget=@min(w,if(evap)old else s.vapor);
 var next:f32=@floatCast(if(evap)old-budget else old+budget);
 if(!std.math.isFinite(next))return s;
 var paid=if(evap)old-@as(f64,next) else @as(f64,next)-old;
 if(paid>budget){next=std.math.nextAfter(f32,next,s.liquid);paid=if(evap)old-@as(f64,next) else @as(f64,next)-old;}
 if(paid<=0 or paid>budget)return s;
 const v=if(evap)s.vapor+paid else s.vapor-paid;
 if(!valid(v))return s;
 const dl=if(evap)P.difference(old,next) else P.difference(next,old);
 const dv=if(evap)P.difference(v,s.vapor) else P.difference(s.vapor,v);
 if(dl.lo!=0 or dv.lo!=0 or dl.hi!=dv.hi)return s;
 return .{.liquid=next,.vapor=v};
}
pub fn phase(s:State,saturation:f64,temp:f64,dt:f64)?Result{
 @setFloatMode(.strict);
 if(!valid(s.liquid) or !valid(s.vapor) or !valid(saturation) or !std.math.isFinite(temp) or !valid(dt))return null;
 var r=Result{.state=s};
 r.evap_requested=if(temp>273.15)@min(@as(f64,s.liquid),@max(0,saturation-s.vapor)*A.relaxation(dt,A.evaporation_seconds)) else 0;
 r.state=exchange(s,r.evap_requested,true);r.evap_paid=@as(f64,s.liquid)-r.state.liquid;
 r.rain_requested=@min(r.state.vapor,@max(0,r.state.vapor-saturation)*A.relaxation(dt,A.condensation_seconds));
 const before=r.state;r.state=exchange(before,r.rain_requested,false);r.rain_paid=@as(f64,r.state.liquid)-before.liquid;
 return r;
}
