//! Null experimental sidecar: no lower mortality/immunity, no descendants or saves.
//! Real Microbes.step for both pools; resting photosynthesis disabled. One lineage,
//! unstructured non-grazing nonmoving phenotype only. NOT production-compatible.
const std=@import("std");const M=@import("../simulation/microbes.zig");
pub const State=struct {active:M.Cell,rest:M.Cell,air:f64=10,oxygen:f64=10,transition_respired:f64=0,cutoff_losses:u32=0};
pub fn carbon(s:State) f64{return s.air+M.carbon(s.active)+M.carbon(s.rest);}
pub fn nutrient(s:State) f64{return @as(f64,M.nutrientTotal(s.active))+M.nutrientTotal(s.rest);}
pub fn valid(s:State)bool{
 if(!std.math.isFinite(s.air) or s.air<0 or !std.math.isFinite(s.oxygen) or s.oxygen<0)return false;
 for([_]M.Cell{s.active,s.rest})|c|{if(!M.validCell(c,std.math.maxInt(u64)))return false;for(c.cohorts,0..)|co,i|{if(co.biomass>0 and (i!=0 or co.lineage==0 or co.support_mass!=0 or co.organization!=0 or co.feeding!=0 or co.mobility!=0))return false;}}
 if(M.biomass(s.active)+M.biomass(s.rest)>1.0001)return false;
 const a=s.active.cohorts[0];const r=s.rest.cohorts[0];
 if(a.biomass>0 and r.biomass>0){
  if(a.lineage!=r.lineage)return false;
  inline for(.{"organization","structure","optimum","efficiency","feeding","mobility"})|name|if(@field(a,name)!=@field(r,name))return false;
 }
 return true;
}
/// Fund transfer from source carbon; cost is respired, nutrients returned once.
/// No oxygen => no transfer. All fields unchanged on refusal. No trait mutation.
pub fn transfer(s:*State,to_rest:bool,amount:f32)bool{
 if(!valid(s.*) or !std.math.isFinite(amount) or amount<=0)return false;
 const src=if(to_rest)&s.active else &s.rest;const dst=if(to_rest)&s.rest else &s.active;
 const old=src.cohorts[0];if(amount>old.biomass or old.biomass<=0)return false;
 const cost=amount*0.1;if(@as(f64,cost)>s.oxygen)return false;
 const received=amount-cost;if(received<=0)return false;
 if(dst.cohorts[0].biomass==0){dst.cohorts[0]=old;dst.cohorts[0].biomass=0;dst.cohorts[0].reproduction_credit=0;}
 dst.cohorts[0].biomass+=received;src.cohorts[0].biomass-=amount;
 if(src.cohorts[0].biomass==0)src.cohorts[0]=.{};
 s.active.nutrient+=cost*M.nutrient_per_carbon;s.air+=cost;s.oxygen-=cost;s.transition_respired+=cost;
 return true;
}
fn book(s:*State,f:M.Flux)void{s.air+=@as(f64,f.recycled)-f.fixed;s.oxygen+=@as(f64,f.fixed)-f.recycled;s.cutoff_losses+=f.failed_patches;}
/// Explicit sequential operator: resting mortality/decay first, then active.
/// Detached probes determine actual core potential without changing live state.
/// Both compartments count toward occupied space BEFORE active growth allocation.
pub fn step(s:*State,e:M.Environment,elapsed:f32)bool{
 if(!valid(s.*) or !std.math.isFinite(elapsed) or elapsed<=0 or !std.math.isFinite(e.temperature) or !std.math.isFinite(e.depth_km) or !std.math.isFinite(e.light))return false;
 var r=e;r.light=0;r.carbon_available=0;r.oxygen_carbon_capacity=@floatCast(s.oxygen);
 book(s,M.step(&s.rest,r,elapsed));
 // Release nutrients and organic detritus to shared active reservoir exactly once.
 s.active.nutrient+=s.rest.nutrient;s.rest.nutrient=0;
 // Keep newly decayed rest detritus separate until active step completes.
 var env=e;env.oxygen_carbon_capacity=@floatCast(s.oxygen);
 var mortality=s.active;var dark=env;dark.light=0;dark.carbon_available=0;
 _=M.step(&mortality,dark,elapsed);
 const a=M.biomass(mortality);const space=@max(0,1-a);const total_space=@max(0,1-a-M.biomass(s.rest));
 var probe=s.active;probe.nutrient=1000000;var plentiful=env;plentiful.carbon_available=1000000;
 const potential=M.step(&probe,plentiful,elapsed).fixed;
 env.carbon_available=@floatCast(@min(s.air,if(space>0)@as(f64,potential)*total_space/space else 0));
 book(s,M.step(&s.active,env,elapsed));s.active.detritus+=s.rest.detritus;s.rest.detritus=0;return valid(s.*);
}
