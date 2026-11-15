//! Fixed-cohort common-resource competition; no reproduction or inheritance claim.
const std=@import("std");const M=@import("experimental/energy_community_core.zig");
const Gas=struct{carbon:f64=10,oxygen:f64=10};
const Energy=struct{paid:[4]f64=.{0,0,0,0},dead:[4]f64=.{0,0,0,0},rounding:f64=0};
fn cap(x:f64)f32{var v:f32=@floatCast(@min(x,std.math.floatMax(f32)));if(@as(f64,v)>x)v=std.math.nextAfter(f32,v,0);return v;}
fn remove(co:*M.Cohort,wanted:f64)f64{const old:f64=co.biomass;var left:f32=@floatCast(@max(0,old-wanted));if(old-@as(f64,left)>wanted)left=std.math.nextAfter(f32,left,co.biomass);co.biomass=left;if(left==0)co.*=.{};return old-@as(f64,left);}
fn maintain(cell:*M.Cell,gas:*Gas,activity:[4]f32,rate:f64,seconds:f32)Energy{
 const days=@as(f64,seconds)/86400;var demand:[4]f64=undefined;var total:f64=0;
 for(cell.cohorts,0..)|co,i|{demand[i]=co.biomass*(-std.math.expm1(-rate*activity[i]*days));total+=demand[i];}
 const f=if(total>0)@min(@as(f64,1),gas.oxygen/total) else 1;const hazard=-std.math.expm1(-0.5*(1-f)*days);
 var result=Energy{};var paid:f64=0;var dead:f64=0;
 for(&cell.cohorts,0..)|*co,i|{result.paid[i]=remove(co,demand[i]*f);paid+=result.paid[i];result.dead[i]=remove(co,@as(f64,co.biomass)*hazard);dead+=result.dead[i];}
 gas.carbon+=paid;gas.oxygen-=paid;cell.nutrient+=@floatCast((paid+dead)*M.nutrient_per_carbon);cell.detritus+=@floatCast(dead);result.rounding=total*f-paid;return result;
}
const Outcome=struct{mass:[2]f32,paid:[2]f64,stress:[2]f64,detritus:f32,carbon:f64,oxygen:f64};
fn run(rate:f64,slow:f32,habitat:usize,crowded:bool,swap:usize)!Outcome{
 var cell=M.initialized(42);cell.nutrient=if(habitat==2)0.005 else 0.1;
 var gas=Gas{};if(habitat==2)gas=.{.carbon=0.05,.oxygen=0.01};
 for(0..2)|who|cell.cohorts[who^swap]=.{.biomass=if(crowded)0.4 else 0.02,.lineage=who+1};
 var activity=[4]f32{1,1,1,1};activity[1^swap]=slow;
 const c0=gas.carbon+M.carbon(cell);const n0=M.nutrientTotal(cell);var paid=[2]f64{0,0};var stress=[2]f64{0,0};var extinct=[2]bool{false,false};
 for(0..20*60)|tick|{
  const day=tick/60;const dark=habitat>0 and day>=2 and day%4>=2;
  const r=maintain(&cell,&gas,activity,rate,1440);for(0..2)|who|{paid[who]+=r.paid[who^swap];stress[who]+=r.dead[who^swap];}
  const flux=M.stepWithActivity(&cell,.{.temperature=303,.depth_km=0.001,.light=if(dark)0 else 1,.carbon_available=cap(gas.carbon),.oxygen_carbon_capacity=cap(gas.oxygen)},1440,activity);
  gas.carbon+=@as(f64,flux.recycled)-flux.fixed;gas.oxygen+=@as(f64,flux.fixed)-flux.recycled;
  try std.testing.expect(gas.carbon>=0 and gas.oxygen>=0 and M.validCell(cell,3));
  try std.testing.expectApproxEqAbs(c0,gas.carbon+M.carbon(cell),0.0001);try std.testing.expectApproxEqAbs(n0,M.nutrientTotal(cell),0.00001);
  for(0..2)|who|{if(extinct[who])try std.testing.expectEqual(@as(f32,0),cell.cohorts[who^swap].biomass);if(cell.cohorts[who^swap].biomass==0)extinct[who]=true;}
  if(tick+1==120 or tick+1==600 or tick+1==1200)std.debug.print("COMMUNITY rate={d} slow={d} habitat={d} crowded={} swap={d} day={d} fast={d:.9} slow_mass={d:.9} paid_fast={d:.9} paid_slow={d:.9} stress_fast={d:.9} stress_slow={d:.9} detritus={d:.9} carbon={d:.9} oxygen={d:.9} carbon_error={e} nutrient_error={e}\n",.{rate,slow,habitat,crowded,swap,(tick+1)/60,cell.cohorts[swap].biomass,cell.cohorts[1^swap].biomass,paid[0],paid[1],stress[0],stress[1],cell.detritus,gas.carbon,gas.oxygen,gas.carbon+M.carbon(cell)-c0,M.nutrientTotal(cell)-n0});
 }
 return .{.mass=.{cell.cohorts[swap].biomass,cell.cohorts[1^swap].biomass},.paid=paid,.stress=stress,.detritus=cell.detritus,.carbon=gas.carbon,.oxygen=gas.oxygen};
}
test "actual shared-resource fixed-cohort competition sensitivity and slot invariance"{
 for([_]f64{0.05,0.2,0.6})|rate|for([_]f32{0.25,0.5,1})|slow|for(0..3)|habitat|for([_]bool{false,true})|crowded|{
  const a=try run(rate,slow,habitat,crowded,0);const b=try run(rate,slow,habitat,crowded,1);
  var maxmass:f64=0;var maxpaid:f64=0;var maxstress:f64=0;
  for(0..2)|who|{try std.testing.expectApproxEqAbs(a.mass[who],b.mass[who],0.00001);try std.testing.expectApproxEqAbs(a.paid[who],b.paid[who],0.00001);try std.testing.expectApproxEqAbs(a.stress[who],b.stress[who],0.00001);maxmass=@max(maxmass,@abs(a.mass[who]-b.mass[who]));maxpaid=@max(maxpaid,@abs(a.paid[who]-b.paid[who]));maxstress=@max(maxstress,@abs(a.stress[who]-b.stress[who]));}
  try std.testing.expectApproxEqAbs(a.detritus,b.detritus,0.00001);try std.testing.expectApproxEqAbs(a.carbon,b.carbon,0.00001);try std.testing.expectApproxEqAbs(a.oxygen,b.oxygen,0.00001);
  std.debug.print("COMMUNITY_SWAP rate={d} slow={d} habitat={d} crowded={} living_delta={e} paid_delta={e} stress_delta={e} detritus_delta={e} gas_delta={e}\n",.{rate,slow,habitat,crowded,maxmass,maxpaid,maxstress,@abs(a.detritus-b.detritus),@abs(a.carbon-b.carbon)});
 };
}
test "instrumented core at activity one matches actual production scalar fields"{
 const Original=@import("simulation/microbes.zig");var a=Original.initialized(42);a.nutrient=0.1;a.cohorts[0]=.{.biomass=0.2,.lineage=1};a.cohorts[1]=.{.biomass=0.1,.lineage=2};
 var b=M.initialized(42);b.nutrient=a.nutrient;
 for(a.cohorts,0..)|co,i|{inline for(std.meta.fields(Original.Cohort))|field|@field(b.cohorts[i],field.name)=@field(co,field.name);}
 for(0..240)|tick|{
  const light:f32=if(tick%60<30)1 else 0;
  const af=Original.step(&a,.{.temperature=303,.depth_km=0.001,.light=light,.carbon_available=10,.oxygen_carbon_capacity=10},1440);
  const bf=M.stepWithActivity(&b,.{.temperature=303,.depth_km=0.001,.light=light,.carbon_available=10,.oxygen_carbon_capacity=10},1440,.{1,1,1,1});
  inline for(std.meta.fields(Original.Flux))|field|try std.testing.expectEqual(@field(af,field.name),@field(bf,field.name));
  for(a.cohorts,0..)|co,i|{inline for(std.meta.fields(Original.Cohort))|field|try std.testing.expectEqual(@field(co,field.name),@field(b.cohorts[i],field.name));}
  try std.testing.expectEqual(a.nutrient,b.nutrient);try std.testing.expectEqual(a.detritus,b.detritus);try std.testing.expectEqual(a.rng,b.rng);
 }
}
