//! Isolated coherent physical-f64 local kernel. No production scheduling or rates.
const std=@import("std");const B=@import("physical_water_f64.zig");
pub const Cohort=struct{biomass:f64=0,support:f64=0,root_fraction:f64=0,storage_fraction:f64=0,water:f64=0};
pub const State=struct{surface:f64=0,soil:f64=0,vapor:f64=0,cohorts:[4]Cohort=[_]Cohort{.{}}**4};
pub const Params=struct{dt:f64,capacity:f64,infiltration_rate:f64=0,evaporation_rate:f64=0,drainage_rate:f64=0,conductance:f64=0,demand:[4]f64=.{0,0,0,0},exposure:[4]f64=.{0,0,0,0},temperature:f64=300,depth_m:f64=0};
pub const Result=struct{state:State,root_receipts:[4]f64,store_receipts:[4]f64,h_paid:[4]f64,root_carbon:[4]f64,reservoir_carbon:[4]f64,canopy_carbon:[4]f64,infiltrated:f64,evaporated:f64,drained:f64};

pub const Audited=struct{result:Result,ledger:B.Ledger,allocation_deficit:f64};
fn valid(x:f64)bool{return std.math.isFinite(x) and x>=0;}
pub fn step(original:State,p:Params)?Audited{
 @setFloatMode(.strict);
 if(!valid(p.dt) or p.dt==0 or !valid(p.capacity) or !valid(p.conductance) or !valid(p.depth_m) or !std.math.isFinite(p.temperature))return null;
 if(!valid(original.surface) or !valid(original.soil) or !valid(original.vapor) or original.soil>p.capacity)return null;
 for ([_]f64{p.infiltration_rate,p.evaporation_rate,p.drainage_rate})|rate|if(!valid(rate) or !std.math.isFinite(rate*p.dt))return null;
 var out=Audited{.result=.{.state=original,.root_receipts=.{0,0,0,0},.store_receipts=.{0,0,0,0},.h_paid=.{0,0,0,0},.root_carbon=.{0,0,0,0},.reservoir_carbon=.{0,0,0,0},.canopy_carbon=.{0,0,0,0},.infiltrated=0,.evaporated=0,.drained=0},.ledger=.{},.allocation_deficit=0};const r=&out.result;const s=&r.state;
 for (original.cohorts,0..)|c,i|{
  if(!valid(c.biomass) or !valid(c.support) or c.support>c.biomass or !valid(c.root_fraction) or !valid(c.storage_fraction) or c.root_fraction>1 or c.storage_fraction>1 or !valid(c.water) or !valid(p.demand[i]) or !valid(p.exposure[i]) or p.exposure[i]>1)return null;
  const remaining=B.downDifference(1,c.root_fraction);if(c.storage_fraction>remaining)return null;
  r.root_carbon[i]=B.downProduct(c.support,c.root_fraction);r.reservoir_carbon[i]=B.downProduct(c.support,c.storage_fraction);r.canopy_carbon[i]=@max(0,c.support-r.root_carbon[i]-r.reservoir_carbon[i]);const cap=c.support*c.storage_fraction*10;if(!valid(cap) or !valid(r.root_carbon[i]) or !valid(r.reservoir_carbon[i]) or !valid(r.canopy_carbon[i]) or c.water>cap)return null;
 }
 const deficit=B.downDifference(p.capacity,s.soil);
 r.infiltrated=B.transfer(&s.surface,&s.soil,@min(deficit,p.infiltration_rate*p.dt),&out.ledger) orelse return null;
 r.evaporated=B.transfer(&s.soil,&s.vapor,p.evaporation_rate*p.dt,&out.ledger) orelse return null;
 const wetness=if(p.capacity>0)s.soil/p.capacity else 0;var wanted=[_]f64{0,0,0,0};const eligible=p.temperature>273.15 and p.temperature<355 and p.depth_m<0.2;
 if(eligible)for (0..4)|i|{if(p.exposure[i]>0){const flow=B.downProduct(B.downProduct(B.downProduct(r.root_carbon[i],p.conductance),wetness),p.dt);if(!valid(flow))return null;wanted[i]=@min(p.demand[i],flow);}};
 const denominator=B.upperSum(wanted);const request=B.lowerSum(wanted);if(!valid(denominator) or !valid(request))return null;
 const root_source_before=s.soil;const paid=B.transfer(&s.soil,&s.vapor,request,&out.ledger) orelse return null;
 if(paid>0 and denominator>0)for (0..4)|i|{r.root_receipts[i]=@min(wanted[i],B.downProduct(paid,B.downRatio(wanted[i],denominator)));};
 const root_debit=B.difference(root_source_before,s.soil);var split_ledger=B.Ledger{};B.recordTerms(&split_ledger,.{root_debit.hi,root_debit.lo,-r.root_receipts[0],-r.root_receipts[1],-r.root_receipts[2],-r.root_receipts[3],0,0,0,0},0);out.allocation_deficit=split_ledger.absolute;
 // Independent storage sources are removed simultaneously; one canonical vapor addition.
 var removed=[_]f64{0,0,0,0};var oldstores=[_]f64{0,0,0,0};for (s.cohorts,0..)|c,i|{oldstores[i]=c.water;const unmet=if(eligible and p.exposure[i]>0)B.downDifference(p.demand[i],r.root_receipts[i])else 0;const rem=B.remove(c.water,unmet) orelse return null;s.cohorts[i].water=rem.after;r.store_receipts[i]=rem.paid;removed[i]=rem.paid;}
 const storetotal=B.canonicalSum(removed);const oldv=s.vapor;s.vapor+=storetotal;if(!valid(s.vapor))return null;
 // Attribute receiver rounding once, source rounding per private store.
 var terms=[_]f64{0}**10;var envelope:f64=0;for(0..4)|i|{const d=B.difference(oldstores[i],s.cohorts[i].water);terms[i*2]=d.hi;terms[i*2+1]=d.lo;envelope+=B.ulp(oldstores[i])+B.ulp(s.cohorts[i].water);}
 const credit=B.difference(s.vapor,oldv);terms[8]=-credit.hi;terms[9]=-credit.lo;B.recordTerms(&out.ledger,terms,envelope+B.ulp(oldv)+B.ulp(s.vapor)+B.ulp(storetotal)*4);
 for (0..4)|i|{const received=B.lowerSum(.{r.root_receipts[i],r.store_receipts[i],0,0});r.h_paid[i]=if(p.demand[i]>0)@min(1,B.downRatio(received,p.demand[i]))else 0;}
 r.drained=B.transfer(&s.soil,&s.surface,p.drainage_rate*p.dt,&out.ledger) orelse return null;if(!std.math.isFinite(out.ledger.signed) or !valid(out.ledger.absolute) or !valid(out.ledger.envelope))return null;return out;
}
