const std=@import("std");const M=@import("simulation/microbes.zig");const L=@import("simulation/legacy_microbes.zig");const S=@import("simulation/shared_soil.zig");
test "graded paid entry, partial activity, funded dry roots and finite recovery"{
 M.qa_protection_enabled=true;defer M.qa_protection_enabled=false;
 const base=M.Cohort{.biomass=0.02,.support_mass=0.005,.root_fraction=0.5,.organization=0.25,.lineage=1};
 const warm=M.Environment{.temperature=298,.depth_km=0,.light=1,.carbon_available=1,.oxygen_carbon_capacity=1,.immersion_physiology=true,.final_demand_physiology=true};var cold=warm;cold.temperature=263;
 for([_]f32{0,0.03125,0.5,1})|p|{var cell=M.initialized(42);cell.cohorts[0]=base;cell.cohorts[0].protective_investment=p;const before=cell;
  try std.testing.expectEqual(@as(f32,0),M.protectBefore(&cell,warm,1440));try std.testing.expectEqualDeep(before,cell);
  const paid=M.protectBefore(&cell,cold,1440);try std.testing.expectEqual(before.cohorts[0].biomass-cell.cohorts[0].biomass,paid);try std.testing.expectEqual(p>0,cell.cohorts[0].protective_rest);try std.testing.expectApproxEqAbs(1-p,M.activity(cell.cohorts[0]),1e-7);
  const root=M.rootDemand(cell.cohorts[0],warm,1440);const water=S.stepBorrowed(&cell,0.5,1,7.6695296e9,warm,1440,10,0).?;try std.testing.expectApproxEqAbs(root,water.demand[0],1e-16);if(p==1){try std.testing.expectEqual(@as(f64,0),water.credits[0]);}else try std.testing.expect(water.credits[0]>0);
  if(p>0){for(0..5)|_|{_=M.protectBefore(&cell,warm,1440);try std.testing.expect(cell.cohorts[0].protective_rest);}_=M.protectBefore(&cell,warm,1440);try std.testing.expect(!cell.cohorts[0].protective_rest);}
 }
 std.debug.print("GRADED_MEMORY cohort{} cell{} historical_cohort{} cell{}\n",.{@sizeOf(M.Cohort),@sizeOf(M.Cell),@sizeOf(L.Cohort),@sizeOf(L.Cell)});
}
test "p0 unchanged actual old physiology and RNG"{
 var a=M.initialized(42);a.cohorts[0]=.{.biomass=0.02,.support_mass=0.005,.root_fraction=0.5,.organization=0.25,.lineage=1};var b=L.initialized(42);inline for(std.meta.fields(L.Cohort))|f|@field(b.cohorts[0],f.name)=@field(a.cohorts[0],f.name);
 const e=M.Environment{.temperature=298,.depth_km=0.001,.light=1,.carbon_available=1,.oxygen_carbon_capacity=1};var old:L.Environment=undefined;inline for(std.meta.fields(L.Environment))|f|@field(old,f.name)=@field(e,f.name);
 M.qa_protection_enabled=true;defer M.qa_protection_enabled=false;for(0..60)|_|{_=M.protectBefore(&a,e,1440);const fa=M.step(&a,e,1440);const fb=L.step(&b,old,1440);inline for(std.meta.fields(L.Flux))|f|try std.testing.expectEqual(@field(fb,f.name),@field(fa,f.name));for(0..4)|i|inline for(std.meta.fields(L.Cohort))|f|try std.testing.expectEqual(@field(b.cohorts[i],f.name),@field(a.cohorts[i],f.name));try std.testing.expectEqual(b.rng,a.rng);try std.testing.expectEqual(b.nutrient,a.nutrient);try std.testing.expectEqual(b.detritus,a.detritus);}
}
test "actual paid birth inherits intermediate but resets protective state"{
 M.qa_protection_enabled=true;defer M.qa_protection_enabled=false;for([_]f32{0.03125,0.5,1})|p|{var a=M.initialized(42);var b=M.initialized(43);a.cohorts[0]=.{.biomass=0.1,.support_mass=0.025,.lineage=1,.protective_investment=p,.reproduction_credit=0.1};var stats=M.Stats{.next_lineage=2};try std.testing.expect(M.propagate(&a,0,&b,&stats));try std.testing.expectEqual(p,b.cohorts[0].protective_investment);try std.testing.expect(!b.cohorts[0].protective_rest and b.cohorts[0].protective_recovery==0);try std.testing.expectApproxEqAbs(@as(f32,0.1),a.cohorts[0].biomass+b.cohorts[0].biomass,1e-8);}
}
test "entry requires oxygen and extreme damage remains finite"{
 M.qa_protection_enabled=true;defer M.qa_protection_enabled=false;
 for([_]f32{240,400})|temp|{var cell=M.initialized(42);cell.cohorts[0]=.{.biomass=0.02,.support_mass=0.005,.root_fraction=0.5,.organization=0.25,.lineage=1,.protective_investment=1};var env=M.Environment{.temperature=temp,.depth_km=0,.light=1,.carbon_available=1,.oxygen_carbon_capacity=0};const before=cell;try std.testing.expectEqual(@as(f32,0),M.protectBefore(&cell,env,1440));try std.testing.expectEqualDeep(before,cell);env.oxygen_carbon_capacity=1;try std.testing.expect(M.protectBefore(&cell,env,1440)>0);for(0..180)|_|{_=M.protectBefore(&cell,env,1440);_=M.step(&cell,env,1440);}try std.testing.expectEqual(@as(f32,0),M.biomass(cell));}
}
