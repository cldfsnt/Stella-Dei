//! One already-paid interval allowance, not physical stored water.
const std=@import("std");const P=@import("physical_water_f64.zig");
pub fn signal(credit:f64,owner:u64,lineage:u64,demand:f64)f32{
 if(owner==0 or owner!=lineage or !std.math.isFinite(credit) or credit<=0 or !std.math.isFinite(demand) or demand<=0)return 0;
 return P.signal32(credit,demand);
}
