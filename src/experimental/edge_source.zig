//! Exact per-source validation; no cache or coordinate approximation.
const std=@import("std");
pub const EdgeSource=struct{
 from:[3]f64,wind:[3]f64,valid:bool,
 pub fn init(from:[3]f64,wind:[3]f64)EdgeSource{
  var valid=true;for(0..3)|i|{if(!std.math.isFinite(from[i]) or !std.math.isFinite(wind[i]))valid=false;}
  return .{.from=from,.wind=wind,.valid=valid};
 }
 pub fn rate(s:EdgeSource,to:[3]f64)f64{
  if(!s.valid)return 0;
  var length2:f64=0;var dot:f64=0;
  for(0..3)|i|{if(!std.math.isFinite(to[i]))return 0;const d=to[i]-s.from[i];length2+=d*d;dot+=s.wind[i]*d;}
  if(length2<=0 or !std.math.isFinite(length2) or !std.math.isFinite(dot))return 0;
  return @max(0,dot/length2);
 }
};
