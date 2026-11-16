//! Test-only newborn body partition. Never called on a live colony or by scheduler.
const std=@import("std");const M=@import("simulation/microbes.zig");const S=@import("simulation/shared_soil.zig");const P=@import("simulation/wind_packet.zig");
fn develop(c:M.Cohort,enabled:bool) M.Cohort {
 if(!enabled)return c;
 std.debug.assert(c.biomass>0 and c.organization>=0 and c.organization<=0.7);
 var out=c;const target=@as(f64,c.biomass)*c.organization;out.support_mass=@floatCast(target);
 if(out.support_mass>target)out.support_mass=std.math.nextAfter(f32,out.support_mass,0);
 return out;
}
test "bounded newborn partition no added carbon nutrients water credit or randomness" {
 for([_]f32{0.004,0.01,0.02})|b|for([_]f32{0,0.025,0.25,0.7})|org|{
  const old=M.Cohort{.biomass=b,.support_mass=b*0.25,.organization=org,.root_fraction=0.5,.lineage=7,.parent=2,.generation=1};const c=develop(old,true);var normalized=c;normalized.support_mass=old.support_mass;
  try std.testing.expectEqualDeep(old,normalized);try std.testing.expectEqualDeep(old,develop(old,false));
  try std.testing.expect(c.support_mass<=c.biomass);try std.testing.expect(c.support_mass*c.root_fraction<=c.support_mass);
  try std.testing.expectEqual(old.biomass*M.nutrient_per_carbon,c.biomass*M.nutrient_per_carbon);
  try std.testing.expect(M.frondMass(c)<=c.biomass);if(org==0)try std.testing.expectEqual(@as(f32,0),c.support_mass);
 };
}
test "actual paid routes unchanged donor and stats with child-only positive negative organization partition" {
 const root=M.RootMutation.Config{.enabled=true,.law=1,.stream_seed=77};const wind=@import("simulation/wind_genetics.zig").Config{.enabled=true,.law=1};
 for(0..3)|route|for([_]f32{0,0.25,0.7})|org|{
  var d=M.initialized(22);d.cohorts[0]=.{.biomass=0.1,.support_mass=0.025,.organization=org,.root_fraction=0.5,.aerial_allocation=0.5,.lineage=1,.reproduction_credit=0.1};var t=M.Cell{};var stats=M.Stats{.next_lineage=2};
  if(route==0)try std.testing.expect(M.prepareCombinedPacket(&d,0,&t,&stats,true,root,wind)) else if(route==1)try std.testing.expect(M.reproduceCombinedLarge(&d,0,&t,&stats,root,wind)) else _=P.launchCombined(&d,0,&t,&stats,10,3,true,wind,root) orelse return error.Refused;
  const donor=d;const st=stats;const old=t;const oldc=t.cohorts[0];t.cohorts[0]=develop(oldc,true);
  try std.testing.expectEqualDeep(donor,d);try std.testing.expectEqualDeep(st,stats);try std.testing.expectEqual(M.carbon(old),M.carbon(t));try std.testing.expectEqual(M.nutrientTotal(old),M.nutrientTotal(t));
  t.cohorts[0]=develop(oldc,false);try std.testing.expectEqualDeep(old,t);
 };
 var d=M.initialized(22);d.cohorts[0]=.{.biomass=0.1,.support_mass=0.025,.organization=0.25,.root_fraction=0.5,.lineage=1,.reproduction_credit=0.1};var t=M.Cell{};var stats=M.Stats{.next_lineage=2};const rng=d.rng;
 const r=P.launchCombined(&d,0,&t,&stats,10,3,false,wind,root).?;try std.testing.expect(!r.arrived);try std.testing.expectEqual(@as(f32,0),M.biomass(t));try std.testing.expect(t.detritus>0 and t.nutrient>0);try std.testing.expectEqual(rng,d.rng);
}
fn probe(label:[]const u8,birth:M.Cohort,observed:M.Environment)!void {
 for([_]f32{birth.biomass,0.01,0.02})|b|for(0..2)|scenario|for([_]bool{false,true})|enabled|{
  var c=birth;c.biomass=b;c.support_mass=0;c.reproduction_credit=0;c=develop(c,enabled);
  var cell=M.Cell{.nutrient=0.02};cell.cohorts[0]=c;
  var e=observed;if(scenario==1){e.depth_km=0;e.temperature=c.optimum;e.light=1;}
  e.immersion_physiology=true;e.final_demand_physiology=true;e.carbon_available=0.02;e.oxygen_carbon_capacity=0.1;
  const exchange=S.stepBorrowed(&cell,1,1,1e10,e,1440,10,0).?;
  e.root_credit=exchange.credits;e.root_owner[0]=c.lineage;
  const h=M.fundedHydration(c,e,1440,0,M.rootDemand(c,e,1440));
  const before=cell;const flux=M.step(&cell,e,1440);
  try std.testing.expect(exchange.soil<=1 and exchange.paid>=0 and h>=0 and h<=1);
  try std.testing.expect(flux.fixed<=0.02 and flux.fixed<=before.nutrient/M.nutrient_per_carbon);
  std.debug.print("ROW {s} budget={d} scenario={d} develop={} support={e} roots={e} leaves={e} height={e} maintenance_day={e} demand={e} credit={e} h={d} growth={e} dead_C={e} respired={e} net={e}\n",.{label,b,scenario,enabled,c.support_mass,c.support_mass*c.root_fraction,M.frondMass(c),M.producerHeightMeters(c),M.supportMaintenancePerDay(c),exchange.demand[0],exchange.credits[0],h,flux.fixed,cell.detritus-before.detritus,flux.recycled,M.biomass(cell)-b});
 };
}
