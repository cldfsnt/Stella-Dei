//! Root-only post-advection exchange. No abiotic phases, stores or return escrow.
const std=@import("std");
const M=@import("microbes.zig");
const P=@import("physical_water_f64.zig");
pub const Result=struct{soil:f64,vapor:f32,h:[4]f32=.{0,0,0,0},demand:[4]f64=.{0,0,0,0},credits:[4]f64=.{0,0,0,0},paid:f64=0,vapor_rounding_density:f64=0};
pub fn step(cell:M.Cell,soil:f64,vapor:f32,area:f64,env:M.Environment,dt:f32,conductance:u8)?Result{
 @setFloatMode(.strict);
 if(!std.math.isFinite(soil) or soil<0 or soil>1 or !std.math.isFinite(vapor) or vapor<0 or !std.math.isFinite(area) or area<=0 or !std.math.isFinite(dt) or dt<=0 or (conductance!=1 and conductance!=10))return null;
 if(!std.math.isFinite(env.temperature) or !std.math.isFinite(env.depth_km) or env.depth_km<0 or !std.math.isFinite(env.light) or env.light<0 or env.light>2)return null;
 for(cell.cohorts)|c|if(!std.math.isFinite(c.root_fraction) or c.root_fraction<0 or c.root_fraction>1 or !std.math.isFinite(c.biomass) or c.biomass<0 or !std.math.isFinite(c.support_mass) or c.support_mass<0 or c.support_mass>c.biomass)return null;
 var out=Result{.soil=soil,.vapor=vapor};
 if(env.temperature<=273.15 or env.temperature>=355 or env.depth_km>=0.0002)return out;
 const depth=@as(f64,env.depth_km)*1000;var wants=[_]f64{0,0,0,0};
 for(cell.cohorts,0..)|c,i|{
  if(c.biomass<=0 or c.root_fraction==0 or c.support_mass<=0)continue;
  const height=@as(f64,M.producerHeightMeters(c));const exposure=if(height>0)std.math.clamp((height-depth)/height,0,1)else if(depth==0)@as(f64,1)else 0;
  out.demand[i]=0.1*@as(f64,M.frondMass(c))*@as(f64,dt)/86400*(0.5+0.5*@as(f64,env.light))*exposure;
  const root=P.downProduct(c.support_mass,c.root_fraction);
  const flow=P.downProduct(P.downProduct(P.downProduct(root,@as(f64,@floatFromInt(conductance))/86400),soil),dt);
  if(!std.math.isFinite(flow) or !std.math.isFinite(out.demand[i]) or out.demand[i]<0)return null;
  wants[i]=@min(out.demand[i],flow);
 }
 const request=P.lowerSum(wants);const denominator=P.upperSum(wants);
 const removal=P.remove(soil,request) orelse return null;
 if(removal.paid==0)return out;
 const native=P.downRatio(P.downProduct(removal.paid,area),1e9);
 if(!std.math.isFinite(native))return null;
 const receiver:f32=@floatCast(@as(f64,vapor)+native);if(!std.math.isFinite(receiver))return null;
 // Source debit, not receiver rounding, funds the physiological signal.
 out.soil=removal.after;out.vapor=receiver;out.paid=removal.paid;
 out.vapor_rounding_density=(@as(f64,receiver)-vapor)*1e9/area-removal.paid;
 if(denominator>0)for(0..4)|i|{out.credits[i]=@min(wants[i],P.downProduct(removal.paid,P.downRatio(wants[i],denominator)));out.h[i]=P.signal32(out.credits[i],out.demand[i]);};
 return out;
}
