//! Isolated fixed-cohort accounting candidate. NOT a general organism engine.
//! No support/organization/grazing/motility/reproduction/movement/save support.
const std=@import("std");const Old=@import("energy_community_core.zig");
pub const nutrient_per_carbon=Old.nutrient_per_carbon;pub const Cohort=Old.Cohort;pub const Environment=Old.Environment;
pub const Cell=struct{cohorts:[4]Cohort=.{.{},.{},.{},.{}},nutrient:f32=0.02,detritus:f32=0,rng:u64=1,nutrient_residual:f64=0,detritus_residual:f64=0,credit_residual:[4]f64=.{0}**4};
pub const Flux=struct{fixed:f64=0,recycled:f64=0};
pub fn initialized(seed:u64)Cell{return .{.rng=seed};}
pub fn biomass(cell:Cell)f32{var b:f32=0;for(cell.cohorts)|c|b+=c.biomass;return b;}
pub fn carbon(cell:Cell)f64{var b:f64=detritus(cell);for(cell.cohorts)|c|b+=c.biomass;return b;}
pub fn nutrientTotal(cell:Cell)f64{var n:f64=nutrient(cell);for(cell.cohorts)|c|n+=@as(f64,c.biomass)*nutrient_per_carbon;return n;}
pub fn nutrient(cell:Cell)f64{return @as(f64,cell.nutrient)+cell.nutrient_residual;}
pub fn detritus(cell:Cell)f64{return @as(f64,cell.detritus)+cell.detritus_residual;}
fn change(pool:*f32,residual:*f64,delta:f64)void{const exact=@as(f64,pool.*)+residual.*+delta;std.debug.assert(std.math.isFinite(exact) and exact>=0);pool.*=@floatCast(exact);residual.*=exact-@as(f64,pool.*);}
pub fn addN(cell:*Cell,delta:f64)void{change(&cell.nutrient,&cell.nutrient_residual,delta);}
pub fn addDead(cell:*Cell,delta:f64)void{change(&cell.detritus,&cell.detritus_residual,delta);}
fn cap(x:f64)f32{var n:f32=@floatCast(@min(x,std.math.floatMax(f32)));if(@as(f64,n)>x)n=std.math.nextAfter(f32,n,0);return n;}
fn remove(co:*Cohort,wanted:f64)f64{const old:f64=co.biomass;var left:f32=@floatCast(@max(0,old-wanted));if(old-@as(f64,left)>wanted)left=std.math.nextAfter(f32,left,co.biomass);co.biomass=left;return old-@as(f64,left);}
fn grow(co:*Cohort,wanted:f64)f64{const old:f64=co.biomass;var next:f32=@floatCast(old+wanted);if(@as(f64,next)-old>wanted)next=std.math.nextAfter(f32,next,co.biomass);co.biomass=next;return @as(f64,next)-old;}
pub fn validCell(cell:Cell,next:u64)bool{if(!std.math.isFinite(nutrient(cell)) or nutrient(cell)<0 or !std.math.isFinite(detritus(cell)) or detritus(cell)<0)return false;for(cell.cohorts)|co|if(!std.math.isFinite(co.biomass) or co.biomass<0 or (co.biomass>0 and (co.lineage==0 or co.lineage>=next)))return false;return true;}
pub fn supported(cell:Cell,env:Environment,activity:[4]f32)bool{
 if(env.temperature!=303 or env.depth_km!=0.001 or !std.math.isFinite(env.light) or env.light<0 or !std.math.isFinite(env.carbon_available) or env.carbon_available<0 or !std.math.isFinite(env.oxygen_carbon_capacity) or env.oxygen_carbon_capacity<0)return false;
 for(cell.cohorts,activity)|co,pace|if(co.structure!=0 or co.support_mass!=0 or co.organization!=0 or co.feeding!=0 or co.mobility!=0 or !std.math.isFinite(pace) or pace<0 or pace>1)return false;
 return true;
}
pub fn stepWithActivity(cell:*Cell,env:Environment,elapsed:f32,activity:[4]f32)Flux{
 // This candidate is deliberately restricted to the exact wet303K fixed-founder assay.
 std.debug.assert(supported(cell.*,env,activity));
 var result=Flux{};if(!std.math.isFinite(elapsed) or elapsed<=0)return result;
 const days=elapsed/86400;const available=@max(0,env.carbon_available);const light=Old.availableLight(env.light,env.depth_km);
 var potentials=[_]f32{0,0,0,0};
 for(&cell.cohorts,0..)|*co,i|{
  if(co.biomass<=0)continue;
  const fitness=Old.thermalFitness(env.temperature,co.optimum);const mortality:f32=0.04+(1-fitness)*0.7+0.10*co.structure+0.10*co.feeding+0.05*co.mobility;
  const wanted=co.biomass*(1-@exp(-mortality*days));const removed=remove(co,wanted);addDead(cell,removed);addN(cell,removed*nutrient_per_carbon);
  if(co.biomass<0.0025){addDead(cell,co.biomass);addN(cell,@as(f64,co.biomass)*nutrient_per_carbon);co.*=.{};cell.credit_residual[i]=0;}
 }
 const space=@max(0,1-biomass(cell.*));
 for(cell.cohorts,0..)|co,i|{
  if(co.biomass<=0)continue;
  const fitness=Old.thermalFitness(env.temperature,co.optimum);
  const rate=@max(0,3*Old.photosyntheticHabitat(co,env.depth_km,env.temperature)*fitness*light*co.efficiency*(1-0.5*co.structure)*(1-0.7*co.feeding)*(1-0.3*co.mobility)-0.15*co.efficiency*co.efficiency);
  potentials[i]=Old.frondMass(co)*(@exp(@min(20,rate*days))-1)*space;potentials[i]*=activity[i];
 }
 var potential:f32=0;for(potentials)|v|potential+=v;
 const growth=@min(potential,@min(space,@min(available,cap(nutrient(cell.*)/nutrient_per_carbon))));var remaining:f64=growth;
 if(potential>0)for(&cell.cohorts,0..)|*co,i|{
  const requested=growth*potentials[i]/potential;const actual=grow(co,@min(@as(f64,requested),remaining));remaining-=actual;result.fixed+=actual;
  change(&co.reproduction_credit,&cell.credit_residual[i],actual);
 };
 addN(cell,-result.fixed*nutrient_per_carbon);
 const wanted=detritus(cell.*)*@as(f64,1-@exp(-0.1*days));const recycled=@min(wanted,@as(f64,@max(0,env.oxygen_carbon_capacity)));
 addDead(cell,-recycled);result.recycled=recycled;return result;
}

test "accounted local receipts fund C N O2 and credit without target corrections"{
 for([_]f32{1,1440,86400})|dt|for([_]f32{0,1})|light|for([_]f32{0,1e-10,0.3})|co2|for([_]f32{0,1e-10,0.3})|oxygen|{
  var cell=initialized(9);cell.cohorts[0]=.{.biomass=0.2,.lineage=1};cell.cohorts[1]=.{.biomass=0.1,.lineage=2};
  const c0=carbon(cell);const n0=nutrientTotal(cell);
  const receipt=stepWithActivity(&cell,.{.temperature=303,.depth_km=0.001,.light=light,.carbon_available=co2,.oxygen_carbon_capacity=oxygen},dt,.{1,0.5,1,1});
  try std.testing.expect(receipt.fixed>=0 and receipt.fixed<=co2);try std.testing.expect(receipt.recycled>=0 and receipt.recycled<=oxygen);
  try std.testing.expectApproxEqAbs(c0,carbon(cell)+receipt.recycled-receipt.fixed,1e-12);try std.testing.expectApproxEqAbs(n0,nutrientTotal(cell),1e-12);
  var credit:f64=0;for(cell.cohorts,cell.credit_residual)|co,residual|credit+=@as(f64,co.reproduction_credit)+residual;
  try std.testing.expectApproxEqAbs(receipt.fixed,credit,1e-12);try std.testing.expect(validCell(cell,3));
 };
}
test "accounted compensation retains only actual local transfer residuals"{
 var cell=initialized(1);cell.nutrient=0.18;const n0=nutrient(cell);
 for(0..10000)|_|{addN(&cell,1e-10);addN(&cell,-1e-10);}
 try std.testing.expectEqual(n0,nutrient(cell));
 addN(&cell,1e-10);try std.testing.expectApproxEqAbs(n0+1e-10,nutrient(cell),1e-16);
 try std.testing.expect(cell.nutrient_residual!=0);
}

test "accounted experiment explicitly rejects unsupported ecological scope"{
 var c=initialized(1);const e=Environment{.temperature=303,.depth_km=0.001,.light=1,.carbon_available=1,.oxygen_carbon_capacity=1};
 try std.testing.expect(supported(c,e,.{1,1,1,1}));c.cohorts[0].feeding=0.1;try std.testing.expect(!supported(c,e,.{1,1,1,1}));c.cohorts[0].feeding=0;
 var dry=e;dry.depth_km=0;try std.testing.expect(!supported(c,dry,.{1,1,1,1}));try std.testing.expect(!supported(c,e,.{std.math.nan(f32),1,1,1}));
}
