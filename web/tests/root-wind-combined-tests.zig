const std=@import("std");const M=@import("simulation/microbes.zig");const G=@import("simulation/wind_genetics.zig");const P=@import("simulation/wind_packet.zig");
test "three composed routes mutate each inherited trait once with paid tissue"{
 const root=M.RootMutation.Config{.enabled=true,.law=1,.stream_seed=77};const wind=G.Config{.enabled=true,.law=1,.stream_seed=42};
 for(0..3)|route|{
  var d=M.initialized(22);d.cohorts[0]=.{.biomass=0.1,.support_mass=0.025,.root_fraction=0.5,.aerial_allocation=0.5,.organization=0.25,.lineage=1,.reproduction_credit=0.1};var t=M.initialized(33);var stats=M.Stats{.next_lineage=2};const original=d;
  if(route==0)try std.testing.expect(M.prepareCombinedPacket(&d,0,&t,&stats,true,root,wind)) else if(route==1)try std.testing.expect(M.reproduceCombinedLarge(&d,0,&t,&stats,root,wind)) else _=P.launchCombined(&d,0,&t,&stats,10,3,true,wind,root) orelse return error.LaunchFailed;
  const child=t.cohorts[0];try std.testing.expectEqual(M.RootMutation.allocation(0.5,77,1,2,1),child.root_fraction);try std.testing.expectEqual(G.mutation(0.5,42,1,2,1),child.aerial_allocation);try std.testing.expectEqual(@as(f32,0),child.reproduction_credit);try std.testing.expectEqual(@as(u64,1),stats.births);
  const source_area:@TypeOf(@as(f64,1))=if(route==2)10 else 1;const dest_area:f64=if(route==2)3 else 1;
  try std.testing.expect(@as(f64,child.support_mass)*dest_area<=(@as(f64,original.cohorts[0].support_mass)-d.cohorts[0].support_mass)*source_area+1e-9);try std.testing.expect(child.support_mass*child.root_fraction<=child.support_mass);
 }
}
test "historical root reproduction exact when wind off"{
 const root=M.RootMutation.Config{.enabled=true,.law=1,.stream_seed=77};var a=M.initialized(22);a.cohorts[0]=.{.biomass=0.1,.support_mass=0.025,.root_fraction=0.5,.lineage=1,.reproduction_credit=0.1};var b=a;var x=M.Cell{};var y=x;var sa=M.Stats{.next_lineage=2};var sb=sa;
 try std.testing.expect(M.propagateWithRoot(&a,0,&x,&sa,root));try std.testing.expect(M.prepareCombinedPacket(&b,0,&y,&sb,true,root,.{}));try std.testing.expectEqualDeep(a,b);try std.testing.expectEqualDeep(x,y);try std.testing.expectEqualDeep(sa,sb);
}
test "paid failed combined packet does not create child or mutate RNG"{
 var d=M.initialized(22);d.cohorts[0]=.{.biomass=0.1,.support_mass=0.025,.root_fraction=0.5,.aerial_allocation=0.5,.lineage=1,.reproduction_credit=0.1};var t=M.Cell{};var stats=M.Stats{.next_lineage=2};const rng=d.rng;const root=M.RootMutation.Config{.enabled=true,.law=1,.stream_seed=77};const receipt=P.launchCombined(&d,0,&t,&stats,10,3,false,.{.enabled=true,.law=1},root).?;
 try std.testing.expect(!receipt.arrived);try std.testing.expectEqual(@as(u64,2),stats.next_lineage);try std.testing.expectEqual(@as(u64,0),stats.births);try std.testing.expectEqual(rng,d.rng);try std.testing.expect(t.detritus>0 and t.nutrient>0);try std.testing.expectEqual(@as(f32,0),M.biomass(t));
 std.debug.print("COMBINED_LAYOUT cohort={} cell={} env={}\n",.{@sizeOf(M.Cohort),@sizeOf(M.Cell),@sizeOf(M.Environment)});
}
const Old=@import("simulation/combined_historical_reference.zig");
fn oldCell(c:M.Cell)Old.Cell{var o=Old.Cell{.nutrient=c.nutrient,.detritus=c.detritus,.rng=c.rng};for(c.cohorts,0..)|co,i|inline for(std.meta.fields(Old.Cohort))|f|{@field(o.cohorts[i],f.name)=@field(co,f.name);};return o;}
test "independent frozen root source disabled births physiology RNG exact"{
 std.debug.print("HISTORICAL_LAYOUT cohort={} cell={}\n",.{@sizeOf(Old.Cohort),@sizeOf(Old.Cell)});
 const root=M.RootMutation.Config{.enabled=true,.law=1,.stream_seed=77};
 for(0..2)|route|{
  var d=M.initialized(22);d.cohorts[0]=.{.biomass=0.1,.support_mass=0.025,.root_fraction=0.5,.organization=0.25,.lineage=1,.reproduction_credit=0.1};var target=M.Cell{};var stats=M.Stats{.next_lineage=2};var od=oldCell(d);var ot=oldCell(target);var os=Old.Stats{.next_lineage=2};
  if(route==0){try std.testing.expect(Old.propagateWithRoot(&od,0,&ot,&os,root));try std.testing.expect(M.prepareCombinedPacket(&d,0,&target,&stats,true,root,.{}));}else{try std.testing.expect(Old.reproduceWithRoot(&od,0,&ot,&os,true,root));try std.testing.expect(M.reproduceCombinedLarge(&d,0,&target,&stats,root,.{}));}
  try std.testing.expectEqualDeep(od,oldCell(d));try std.testing.expectEqualDeep(ot,oldCell(target));inline for(std.meta.fields(Old.Stats))|f|try std.testing.expectEqual(@field(os,f.name),@field(stats,f.name));
  const env=M.Environment{.temperature=290,.depth_km=0.00001,.light=0.5,.carbon_available=1,.oxygen_carbon_capacity=1,.immersion_physiology=true,.final_demand_physiology=true};var oe:Old.Environment=undefined;inline for(std.meta.fields(Old.Environment))|f|{@field(oe,f.name)=@field(env,f.name);}
  const a=M.step(&d,env,1440);const b=Old.step(&od,oe,1440);try std.testing.expectEqualDeep(od,oldCell(d));inline for(std.meta.fields(Old.Flux))|f|try std.testing.expectEqual(@field(b,f.name),@field(a,f.name));
 }
}
