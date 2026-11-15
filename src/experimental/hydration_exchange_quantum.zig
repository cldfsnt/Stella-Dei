//! Isolated near-quantum exchange candidate. Never imported by production.
const Q=@import("near_quantum.zig");
const std=@import("std");pub const M=@import("hydration_continuous_core.zig");
fn sum(v:[4]f64,up:bool)f64{var a=v;std.mem.sort(f64,&a,{},std.sort.asc(f64));var t:f64=0;for(a)|x|{if(x==0)continue;t+=x;if(up)t=std.math.nextAfter(f64,t,std.math.inf(f64));}return t;}
pub fn take(pool:*f32,want:f64,conversion:f64)f64{if(want<=0)return 0;const old=pool.*;var after:f32=@floatCast(@max(0,@as(f64,old)-want/conversion));if((@as(f64,old)-after)*conversion>want)after=std.math.nextAfter(f32,after,std.math.inf(f32));if(after>old)return 0;pool.*=after;return (@as(f64,old)-after)*conversion;}
pub fn deposit(pool:*f32,escrow:*f64,conversion:f64)void{if(escrow.*<=0)return;const old=pool.*;var after:f32=@floatCast(@as(f64,old)+escrow.*/conversion);if(!std.math.isFinite(after))return;if((@as(f64,after)-old)*conversion>escrow.*)after=std.math.nextAfter(f32,after,-std.math.inf(f32));if(after<old)return;const paid=(@as(f64,after)-old)*conversion;pool.*=after;escrow.*-=paid;}
pub fn total(cell:M.Cell,liquid:f32,vapor:f32,area:f64)f64{return (@as(f64,liquid)+vapor)*(1e9/area)+M.waterTotal(cell);}
pub fn step(cell:*M.Cell,liquid:*f32,vapor:*f32,area:f64,env:M.Environment,dt:f32)?M.Flux{
 if(!std.math.isFinite(area) or area<=0 or !std.math.isFinite(1e9/area) or !std.math.isFinite(dt) or dt<=0 or !std.math.isFinite(liquid.*) or liquid.*<0 or !std.math.isFinite(vapor.*) or vapor.*<0 or !std.math.isFinite(env.temperature) or !std.math.isFinite(env.light) or env.light<0 or !std.math.isFinite(env.carbon_available) or env.carbon_available<0 or !std.math.isFinite(env.oxygen_carbon_capacity) or env.oxygen_carbon_capacity<0 or !M.validCell(cell.*,std.math.maxInt(u64)))return null;
 const conv=1e9/area;
 // Validate the largest pre-uptake liquid depth before any pool/biology mutation.
 // Return escrow may be deposited, so source pool alone is insufficient.
 const maximum_depth=(@as(f64,liquid.*)*conv+cell.liquid_return)/1e6;
 if(!std.math.isFinite(maximum_depth) or maximum_depth>std.math.floatMax(f32))return null;
 M.settleWater(cell);deposit(liquid,&cell.liquid_return,conv);deposit(vapor,&cell.vapor_return,conv);
 var demand=[_]f64{0,0,0,0};for(cell.cohorts,0..)|c,i|demand[i]=@max(0,M.waterCapacity(c)-c.stored_water);
 var any=false;for(demand)|d|{if(d>0){any=true;break;}}const wanted=if(any)sum(demand,true) else 0;const debit=take(liquid,wanted,conv);var paid=[_]f64{0,0,0,0};
 if(debit==0 and wanted>0){
  var stores:[4]f64=undefined;var caps:[4]f64=undefined;
  for(cell.cohorts,0..)|c,i|{stores[i]=c.stored_water;caps[i]=M.waterCapacity(c);}
  if(Q.plan(liquid.*,conv,stores,caps))|p|{if(Q.mergeEscrow(p,cell.liquid_return,stores,liquid.*,conv))|merged|{
   liquid.*=p.pool;cell.liquid_return=merged;for(&cell.cohorts,0..)|*c,i|c.stored_water=p.stores[i];
  }}
 }
 if(debit>0){for(&cell.cohorts,0..)|*c,i|{if(demand[i]==0)continue;const grant=std.math.nextAfter(f64,debit*std.math.nextAfter(f64,demand[i]/wanted,0),0);const before=c.stored_water;var after=@min(M.waterCapacity(c.*),before+grant);if(after-before>grant)after=std.math.nextAfter(f64,after,before);c.stored_water=after;paid[i]=after-before;}const used=sum(paid,false);std.debug.assert(used<=debit);cell.liquid_return+=debit-used;}
 var actual=env;actual.qa_hydration=.{0,0,0,0};actual.depth_km=@floatCast(@as(f64,liquid.*)*conv/1e6);
 for(&cell.cohorts,0..)|*c,i|{const before=c.stored_water;const evaporation=0.1*@as(f64,M.frondMass(c.*))*(@as(f64,dt)/86400)*(0.5+0.5*std.math.clamp(@as(f64,env.light),0,1));c.stored_water=@max(0,before-@min(before,evaporation));cell.vapor_return+=before-c.stored_water;const cap=M.waterCapacity(c.*);if(cap>0)actual.qa_hydration[i]=@floatCast(std.math.clamp(c.stored_water/cap,0,1));}
 const flux=M.step(cell,actual,dt);M.settleWater(cell);deposit(liquid,&cell.liquid_return,conv);deposit(vapor,&cell.vapor_return,conv);return flux;
}
