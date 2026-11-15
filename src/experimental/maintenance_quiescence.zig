//! Uncalibrated gameplay hypothesis, NOT production physiology or inherited trait.
//! Common active/rest maintenance with finite O2 and equal deficit hazard.
const std=@import("std");const M=@import("../simulation/microbes.zig");pub const Q=@import("quiescence.zig");
pub const Parameters=struct{active_per_day:f64,rest_per_day:f64,unmet_stress_per_day:f64,uptake_fraction:f64=1};
pub const Receipt=struct{demand_active:f64=0,demand_rest:f64=0,paid_active:f64=0,paid_rest:f64=0,retained_rounding:f64=0,unmet_fraction:f64=0,stress_fraction:f64=0,dead_active:f64=0,dead_rest:f64=0};
fn validParameters(p:Parameters)bool{return std.math.isFinite(p.active_per_day) and p.active_per_day>0 and std.math.isFinite(p.rest_per_day) and p.rest_per_day>0 and p.rest_per_day<=p.active_per_day and std.math.isFinite(p.unmet_stress_per_day) and p.unmet_stress_per_day>0 and std.math.isFinite(p.uptake_fraction) and p.uptake_fraction>0 and p.uptake_fraction<=1;}
/// Remove only represented tissue, rounding remainder upward to never overspend.
fn remove(co:*M.Cohort,wanted:f64)f64{
 const old:f64=co.biomass;const budget=@min(old,@max(0,wanted));var left:f32=@floatCast(old-budget);
 if(old-@as(f64,left)>budget)left=std.math.nextAfter(f32,left,co.biomass);
 co.biomass=left;const actual=old-@as(f64,left);if(left==0)co.*=.{};return actual;
}
pub fn maintain(state:*Q.State,p:Parameters,seconds:f32)?Receipt{
 if(!Q.valid(state.*) or !validParameters(p) or !std.math.isFinite(seconds) or seconds<=0)return null;
 var s=state.*;const days=@as(f64,seconds)/86400;var r=Receipt{};
 const a:f64=s.active.cohorts[0].biomass;const b:f64=s.rest.cohorts[0].biomass;
 r.demand_active=a*(-std.math.expm1(-p.active_per_day*days));r.demand_rest=b*(-std.math.expm1(-p.rest_per_day*days));
 const total=r.demand_active+r.demand_rest;const funded=if(total>0)@min(@as(f64,1),s.oxygen/total) else 1;
 r.paid_active=remove(&s.active.cohorts[0],r.demand_active*funded);r.paid_rest=remove(&s.rest.cohorts[0],r.demand_rest*funded);
 const paid=r.paid_active+r.paid_rest;if(paid>s.oxygen)return null;
 const next_air=s.air+paid;const next_oxygen=s.oxygen-paid;
 if(!std.math.isFinite(next_air) or (paid>0 and (next_air==s.air or next_oxygen==s.oxygen)))return null;
 s.air=next_air;s.oxygen=next_oxygen;s.active.nutrient+=@floatCast(paid*M.nutrient_per_carbon);
 // Only unavailable oxygen creates physiological deficit; sub-ULP unpaid
 // tissue is retained and disclosed as numerical shortfall, not fake stress.
 r.retained_rounding=total*funded-paid;
 r.unmet_fraction=1-funded;
 r.stress_fraction=-std.math.expm1(-p.unmet_stress_per_day*r.unmet_fraction*days);
 // Identical fractional hazard for both pools, including maximal hazard at O2=0.
 r.dead_active=remove(&s.active.cohorts[0],@as(f64,s.active.cohorts[0].biomass)*r.stress_fraction);
 r.dead_rest=remove(&s.rest.cohorts[0],@as(f64,s.rest.cohorts[0].biomass)*r.stress_fraction);
 const dead=r.dead_active+r.dead_rest;s.active.detritus+=@floatCast(dead);s.active.nutrient+=@floatCast(dead*M.nutrient_per_carbon);
 if(!Q.valid(s))return null;state.*=s;return r;
}
/// Atomic wrapper: maintenance -> existing core mortality/growth/decay. Newly
/// fixed O2 is available NEXT step, never reused for this step's maintenance.
fn capacity(x:f64)f32{
 var v:f32=@floatCast(@min(x,std.math.floatMax(f32)));
 if(@as(f64,v)>x)v=std.math.nextAfter(f32,v,0);return v;
}
fn book(s:*Q.State,f:M.Flux)void{s.air+=@as(f64,f.recycled)-f.fixed;s.oxygen+=@as(f64,f.fixed)-f.recycled;s.cutoff_losses+=f.failed_patches;}
/// Same null sidecar operator, but directed capacity conversion prevents its
/// observed tiny O2 overspend at f64->f32 boundaries. Original Q remains untouched.
fn core(s:*Q.State,e:M.Environment,elapsed:f32,uptake_fraction:f64)bool{
 if(!std.math.isFinite(e.temperature) or !std.math.isFinite(e.depth_km) or !std.math.isFinite(e.light))return false;
 var resting=e;resting.light=0;resting.carbon_available=0;resting.oxygen_carbon_capacity=capacity(s.oxygen);book(s,M.step(&s.rest,resting,elapsed));
 s.active.nutrient+=s.rest.nutrient;s.rest.nutrient=0;
 var env=e;env.oxygen_carbon_capacity=capacity(s.oxygen);
 var mortality=s.active;var dark=env;dark.light=0;dark.carbon_available=0;_=M.step(&mortality,dark,elapsed);
 const a=M.biomass(mortality);const space=@max(0,1-a);const total_space=@max(0,1-a-M.biomass(s.rest));
 var probe=s.active;probe.nutrient=1000000;var plentiful=env;plentiful.carbon_available=1000000;const potential=M.step(&probe,plentiful,elapsed).fixed;
 env.carbon_available=capacity(@min(s.air,if(space>0)@as(f64,potential)*uptake_fraction*total_space/space else 0));
 book(s,M.step(&s.active,env,elapsed));s.active.detritus+=s.rest.detritus;s.rest.detritus=0;return Q.valid(s.*);
}
pub fn step(state:*Q.State,p:Parameters,e:M.Environment,seconds:f32)?Receipt{
 var s=state.*;const r=maintain(&s,p,seconds) orelse return null;
 if(!core(&s,e,seconds,p.uptake_fraction))return null;state.*=s;return r;
}
