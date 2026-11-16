//! Controlled local physiology only: no global climate, reproduction, or changed laws.
const std=@import("std");const M=@import("simulation/microbes.zig");const S=@import("simulation/shared_soil.zig");const C=@import("climate_fixtures.zig");
const State=struct{cell:M.Cell,soil:f64=0.7101186234866845,vapor:f64=1,carbon:f32=0.2,oxygen:f32=0.2,growth:f64=0,recycled:f64=0,water:f64=0,positive_h:u32=0,death_tick:u32=0};
fn run(name:[]const u8,phenotype:M.Cohort,climate:usize)!void{
 var s=State{.cell=.{.nutrient=0.02}};s.cell.cohorts[0]=phenotype;const initial=s;const initial_c=@as(f64,M.carbon(s.cell))+s.carbon;const initial_n=M.nutrientTotal(s.cell);
 for(0..420)|tick|{
  const phase=@as(f64,@floatFromInt(tick%60))/60;
  const sun=@max(@as(f64,0),@sin(2*std.math.pi*phase));
  var env=if(climate==0)M.Environment{.temperature=@floatCast(298+2*@sin(2*std.math.pi*phase)),.depth_km=0.0000005,.light=@floatCast(sun),.carbon_available=0,.oxygen_carbon_capacity=0} else C.weather[if(climate==1)0 else 1][tick%60];
  if(climate==3)env.temperature=@floatCast(298+2*@sin(2*std.math.pi*phase));
  env.immersion_physiology=true;env.final_demand_physiology=true;env.carbon_available=s.carbon;env.oxygen_carbon_capacity=s.oxygen;
  const water=S.stepBorrowed(&s.cell,s.soil,s.vapor,7.6695296e9,env,1440,10,0).?;
  s.soil=water.soil;s.vapor=water.vapor;s.water+=water.paid;env.root_credit=water.credits;
  for(s.cell.cohorts,0..)|c,i|{env.root_owner[i]=c.lineage;if(M.fundedHydration(c,env,1440,i,M.rootDemand(c,env,1440))>0)s.positive_h+=1;}
  const flux=M.step(&s.cell,env,1440);s.growth+=flux.fixed;s.recycled+=flux.recycled;
  s.carbon=@max(0,s.carbon-flux.fixed+flux.recycled);s.oxygen=@max(0,s.oxygen+flux.fixed-flux.recycled);
  if(M.biomass(s.cell)==0 and s.death_tick==0)s.death_tick=@intCast(tick+1);
  try std.testing.expect(s.soil>=0 and s.soil<=initial.soil and s.carbon>=0 and s.cell.nutrient>=0);
  try std.testing.expectApproxEqAbs(initial_c,@as(f64,M.carbon(s.cell))+s.carbon,0.00001);
  try std.testing.expectApproxEqAbs(initial_n,M.nutrientTotal(s.cell),0.00001);
  if((tick+1)%60==0)std.debug.print("DAY {s} climate={} day={} B={d} ratio={d} soil={d} C={d} N={d} growth={d} recycled={d} root_water={d} hydrated_ticks={} death_tick={}\n",.{name,climate,(tick+1)/60,M.biomass(s.cell),M.biomass(s.cell)/phenotype.biomass,s.soil,s.carbon,s.cell.nutrient,s.growth,s.recycled,s.water,s.positive_h,s.death_tick});
 }
}
test "fixed climate contrasts actual finite shared soil and unchanged physiology"{
 for(C.phenotypes,0..)|c,i|for(0..4)|climate|try run(C.names[i],c,climate);
}
