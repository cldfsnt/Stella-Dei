//! Illustrative law2: projected kgC/m2 / 100 kgC/m3 = basal metres.
//! Not empirically calibrated. No body-height epsilon or stored water.
const std=@import("std");
pub const density:f64=100;
pub fn height(biomass:f64,architecture:f64,material_density:f64)?f64 {
 if(!std.math.isFinite(biomass) or biomass<=0 or !std.math.isFinite(architecture) or architecture<0 or !std.math.isFinite(material_density) or material_density<=0)return null;
 const basal=biomass/material_density;
 if(!std.math.isFinite(basal) or basal<=0)return null;
 return @max(basal,architecture);
}
pub fn immersion(biomass:f64,architecture:f64,depth_m:f64,material_density:f64)?f64 {
 if(!std.math.isFinite(depth_m) or depth_m<0)return null;
 const h=height(biomass,architecture,material_density) orelse return null;
 return std.math.clamp(depth_m/h,0,1);
}
