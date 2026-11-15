//! Isolated hypothesis: shared finite-resource competitors, no production trait/schema.
const std=@import("std");pub const M=@import("shared_pace_core.zig");
pub const State=struct{cell:M.Cell,air:f64=10,oxygen:f64=10};
pub const Receipt=struct{maintenance_n_error:f64=0,core_n_error:f64=0,paid:[4]f64=.{0}**4,dead:[4]f64=.{0}**4,rounding:f64=0,unmet:f64=0};
pub fn carbon(s:State)f64{return s.air+M.carbon(s.cell);}
pub fn nutrient(s:State)f64{return M.nutrientTotal(s.cell);}
pub fn preciseN(s:State)f64{var n:f64=s.cell.nutrient;for(s.cell.cohorts)|c|n+=@as(f64,c.biomass)*M.nutrient_per_carbon;return n;}
fn remove(c:*M.Cohort,wanted:f64)f64{const old:f64=c.biomass;var left:f32=@floatCast(old-@min(old,@max(0,wanted)));if(old-@as(f64,left)>wanted)left=std.math.nextAfter(f32,left,c.biomass);const actual=old-@as(f64,left);if(old>0)c.support_mass*=left/c.biomass;c.biomass=left;return actual;}
fn capacity(x:f64)f32{var v:f32=@floatCast(@min(x,std.math.floatMax(f32)));if(@as(f64,v)>x)v=std.math.nextAfter(f32,v,0);return v;}
pub fn step(state:*State,pace:[4]f32,rate:f64,light:f32,seconds:f32)?Receipt{
 if(!std.math.isFinite(rate) or rate<0 or !std.math.isFinite(seconds) or seconds<=0 or !std.math.isFinite(light) or light<0 or !std.math.isFinite(state.air) or state.air<0 or !std.math.isFinite(state.oxygen) or state.oxygen<0 or !M.validCell(state.cell,std.math.maxInt(u64)))return null;
 for(pace)|p|if(!std.math.isFinite(p) or p<=0 or p>1)return null;
 var s=state.*;var r=Receipt{};const days=@as(f64,seconds)/86400;var demands:[4]f64=undefined;var total:f64=0;
 for(s.cell.cohorts,0..)|c,i|{demands[i]=@as(f64,c.biomass)*(-std.math.expm1(-rate*pace[i]*days));total+=demands[i];}
 const funded=if(total>0)@min(@as(f64,1),s.oxygen/total) else 1;r.unmet=1-funded;
 var paid:f64=0;var dead:f64=0;
 for(&s.cell.cohorts,0..)|*c,i|{r.paid[i]=remove(c,demands[i]*funded);paid+=r.paid[i];r.dead[i]=remove(c,@as(f64,c.biomass)*(-std.math.expm1(-0.5*r.unmet*days)));dead+=r.dead[i];}
 r.rounding=total*funded-paid;s.air+=paid;s.oxygen-=paid;s.cell.nutrient+=@floatCast((paid+dead)*M.nutrient_per_carbon);s.cell.detritus+=@floatCast(dead);
 r.maintenance_n_error=preciseN(s)-preciseN(state.*);const before_core=preciseN(s);
 const flux=M.stepPaced(&s.cell,.{.temperature=303,.depth_km=0.001,.light=light,.carbon_available=capacity(s.air),.oxygen_carbon_capacity=capacity(s.oxygen)},seconds,pace);
 s.air+=@as(f64,flux.recycled)-flux.fixed;s.oxygen+=@as(f64,flux.fixed)-flux.recycled;
 r.core_n_error=preciseN(s)-before_core;
 if(s.air<0 or s.oxygen<0 or !M.validCell(s.cell,std.math.maxInt(u64)))return null;state.*=s;return r;
}
