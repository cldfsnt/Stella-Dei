//! Isolated homogeneous-unit physical kernel. No production imports or rates.
const std=@import("std");
pub const Cohort=struct{biomass:f64=0,support:f64=0,root_fraction:f64=0,storage_fraction:f64=0,water:f64=0};
pub const State=struct{surface:f64=0,soil:f64=0,vapor:f64=0,cohorts:[4]Cohort=[_]Cohort{.{}}**4};
pub const Params=struct{dt:f64,capacity:f64,infiltration_rate:f64=0,evaporation_rate:f64=0,drainage_rate:f64=0,conductance:f64=0,demand:[4]f64=.{0,0,0,0},exposure:[4]f64=.{0,0,0,0},temperature:f64=300,depth_m:f64=0};
pub const Result=struct{state:State,root_receipts:[4]f64,store_receipts:[4]f64,h_paid:[4]f64,root_carbon:[4]f64,reservoir_carbon:[4]f64,canopy_carbon:[4]f64,infiltrated:f64,evaporated:f64,drained:f64};
fn valid(x:f64)bool{return std.math.isFinite(x) and x>=0;}
fn add(a:f128,b:f128)?f128{@setFloatMode(.strict);const s=a+b;const bb=s-a;if(!std.math.isFinite(s) or (a-(s-bb))+(b-bb)!=0)return null;return s;}
fn down(x:f128)?f64{if(x<0 or !std.math.isFinite(x) or x>std.math.floatMax(f64))return null;var y:f64=@floatCast(x);if(@as(f128,y)>x)y=std.math.nextAfter(f64,y,0);return y;}
fn sum(a:[4]f64)?f64{var sorted=a;std.mem.sort(f64,&sorted,{},std.sort.asc(f64));var s:f128=0;for(sorted)|x|s=add(s,x) orelse return null;const f:f64=@floatCast(s);if(!std.math.isFinite(f) or @as(f128,f)!=s){std.debug.print("REFUSE_SUM rounded={d}\n",.{f});return null;}return f;}
fn remove(old:f64,want:f64)?struct{after:f64,paid:f64}{
 const request=@min(old,want);var after:f64=@floatCast(@as(f128,old)-request);
 var paid=add(old,-@as(f128,after)) orelse return null;
 if(paid>request){after=std.math.nextAfter(f64,after,old);paid=add(old,-@as(f128,after)) orelse return null;}
 const f:f64=@floatCast(paid);if(paid<0 or @as(f128,f)!=paid)return null;return .{.after=after,.paid=f};
}
fn receive(old:f64,paid:f64)?f64{const exact=add(old,paid) orelse return null;const after:f64=@floatCast(exact);if(!std.math.isFinite(after) or @as(f128,after)!=exact){std.debug.print("REFUSE_RECEIVER old={d} requested={d} rounded={d}\n",.{old,paid,after});return null;}return after;}
fn transfer(source:*f64,target:*f64,want:f64)?f64{const r=remove(source.*,want) orelse return null;const next=receive(target.*,r.paid) orelse return null;source.*=r.after;target.*=next;return r.paid;}
pub fn step(original:State,p:Params)?Result{
 @setFloatMode(.strict);
 if(!valid(p.dt) or p.dt==0 or !valid(p.capacity) or !valid(p.conductance) or !valid(p.depth_m) or !std.math.isFinite(p.temperature))return null;
 if(!valid(original.surface) or !valid(original.soil) or !valid(original.vapor) or original.soil>p.capacity)return null;
 for([_]f64{p.infiltration_rate,p.evaporation_rate,p.drainage_rate})|rate|if(!valid(rate) or !std.math.isFinite(rate*p.dt))return null;
 var result=Result{.state=original,.root_receipts=.{0,0,0,0},.store_receipts=.{0,0,0,0},.h_paid=.{0,0,0,0},.root_carbon=.{0,0,0,0},.reservoir_carbon=.{0,0,0,0},.canopy_carbon=.{0,0,0,0},.infiltrated=0,.evaporated=0,.drained=0};
 for(original.cohorts,0..)|c,i|{
  if(!valid(c.biomass) or !valid(c.support) or c.support>c.biomass or !valid(c.root_fraction) or !valid(c.storage_fraction) or c.root_fraction>1 or c.storage_fraction>1 or !valid(c.water) or !valid(p.demand[i]) or !valid(p.exposure[i]) or p.exposure[i]>1)return null;
  const partition=add(c.root_fraction,c.storage_fraction) orelse return null;if(partition>1)return null;
  result.root_carbon[i]=down(@as(f128,c.support)*c.root_fraction) orelse return null;result.reservoir_carbon[i]=down(@as(f128,c.support)*c.storage_fraction) orelse return null;
  const remaining=add(add(c.support,-@as(f128,result.root_carbon[i])) orelse return null,-@as(f128,result.reservoir_carbon[i])) orelse return null;result.canopy_carbon[i]=down(remaining) orelse return null;if(@as(f128,result.canopy_carbon[i])!=remaining)return null;
  if(@as(f128,c.water)>@as(f128,result.reservoir_carbon[i])*10)return null;
 }
 var s=&result.state;const deficit=down(@as(f128,p.capacity)-s.soil) orelse return null;
 result.infiltrated=transfer(&s.surface,&s.soil,@min(deficit,p.infiltration_rate*p.dt)) orelse return null;
 result.evaporated=transfer(&s.soil,&s.vapor,p.evaporation_rate*p.dt) orelse return null;
 const wetness=if(p.capacity>0)s.soil/p.capacity else 0;var wanted=[_]f64{0,0,0,0};
 const eligible=p.temperature>273.15 and p.temperature<355 and p.depth_m<0.2;
 if(eligible)for(0..4)|i|{if(p.exposure[i]>0){const flow=@as(f128,result.root_carbon[i])*p.conductance*wetness*p.dt;wanted[i]=@min(p.demand[i],down(flow) orelse return null);}};
 const total=sum(wanted) orelse return null;
 if(total>0){const budget=@min(s.soil,total);for(0..4)|i|result.root_receipts[i]=down(@as(f128,budget)*wanted[i]/total) orelse return null;const paid=sum(result.root_receipts) orelse return null;const actual=transfer(&s.soil,&s.vapor,paid) orelse return null;if(actual!=paid){std.debug.print("REFUSE_SOURCE actual={d} requested={d}\n",.{actual,paid});return null;}}
 if(eligible){for(&s.cohorts,0..)|*c,i|{if(p.exposure[i]==0)continue;const unmet=down(@as(f128,p.demand[i])-result.root_receipts[i]) orelse return null;const r=remove(c.water,unmet) orelse return null;c.water=r.after;result.store_receipts[i]=r.paid;}s.vapor=receive(s.vapor,sum(result.store_receipts) orelse return null) orelse return null;}
 for(0..4)|i|{const paid=add(result.root_receipts[i],result.store_receipts[i]) orelse return null;if(paid>p.demand[i])return null;result.h_paid[i]=if(p.demand[i]>0)down(paid/p.demand[i]) orelse return null else 0;}
 result.drained=transfer(&s.soil,&s.surface,p.drainage_rate*p.dt) orelse return null;
 return result;
}
