//! Experimental per-tick cache; formula/order intentionally identical to core.
const std=@import("std");const W=@import("../simulation/atmosphere_water.zig");
pub const Cache=struct{
 dt:f64,evaporation:f64=0,condensation:f64=0,rain_memory:f64=0,
 pub fn init(dt:f64)Cache{
  var c=Cache{.dt=dt};if(!std.math.isFinite(dt) or dt<=0)return c;
  c.evaporation=W.relaxation(dt,W.evaporation_seconds);c.condensation=W.relaxation(dt,W.condensation_seconds);c.rain_memory=W.relaxation(dt,W.rain_memory_seconds);return c;
 }
 pub fn phase(c:Cache,liquid:f64,vapor:f64,saturation:f64,temperature:f64,old_rain_rate:f64)?W.Phase{
  if(!valid(liquid) or !valid(vapor) or !valid(saturation) or !std.math.isFinite(temperature) or !std.math.isFinite(c.dt) or c.dt<0 or !valid(old_rain_rate))return null;
  if(c.dt==0)return .{.liquid=liquid,.vapor=vapor,.evaporated=0,.condensed=0,.rain_rate=old_rain_rate};
  const evap=if(temperature>273.15)@min(liquid,@max(0,saturation-vapor)*c.evaporation) else 0;
  const moist=vapor+evap;const rain=@min(moist,@max(0,moist-saturation)*c.condensation);const a=c.rain_memory;
  return .{.liquid=liquid-evap+rain,.vapor=moist-rain,.evaporated=evap,.condensed=rain,.rain_rate=old_rain_rate*(1-a)+(rain/c.dt*86400)*a};
 }
};
fn valid(x:f64)bool{return std.math.isFinite(x) and x>=0;}
