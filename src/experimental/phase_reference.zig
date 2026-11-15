//! Frozen independent phase algorithm before cache integration. Type alias only shared.
//! Phenomenological column water cycle, not energy-balanced weather.
//! Mass units are arbitrary but identical across liquid/vapor/rain. Times are s;
//! geometry and wind are km and km/s. No biology-dependent constants.
const std=@import("std");
pub const evaporation_seconds:f64=86400;
pub const condensation_seconds:f64=3600;
pub const rain_memory_seconds:f64=86400;
pub const Phase=@import("../simulation/atmosphere_water.zig").Phase;
fn finiteNonnegative(x:f64) bool{return std.math.isFinite(x) and x>=0;}
pub fn relaxation(dt:f64,tau:f64) f64{return -std.math.expm1(-dt/tau);}
pub fn phase(liquid:f64,vapor:f64,saturation:f64,temperature:f64,dt:f64,old_rain_rate:f64) ?Phase {
 if(!finiteNonnegative(liquid) or !finiteNonnegative(vapor) or !finiteNonnegative(saturation) or !std.math.isFinite(temperature) or !std.math.isFinite(dt) or dt<0 or !finiteNonnegative(old_rain_rate))return null;
 if(dt==0)return .{.liquid=liquid,.vapor=vapor,.evaporated=0,.condensed=0,.rain_rate=old_rain_rate};
 const evap=if(temperature>273.15) @min(liquid,@max(0,saturation-vapor)*relaxation(dt,evaporation_seconds)) else 0;
 const moist=vapor+evap;
 // Condensation uses only supersaturation, including frozen condensate which
 // the existing surface model interprets as ice through its temperature.
 const rain=@min(moist,@max(0,moist-saturation)*relaxation(dt,condensation_seconds));
 const a=relaxation(dt,rain_memory_seconds);
 return .{.liquid=liquid-evap+rain,.vapor=moist-rain,.evaporated=evap,.condensed=rain,.rain_rate=old_rain_rate*(1-a)+(rain/dt*86400)*a};
}
