const std=@import("std");const M=@import("simulation/microbes.zig");
test "chosen structure inherits through existing paid reproduction and has existing costs"{
 var d=M.initialized(42);d.cohorts[0]=.{.biomass=0.1,.support_mass=0.025,.root_fraction=0.5,.organization=0.25,.structure=0.5,.lineage=1,.reproduction_credit=0.1};var target=M.initialized(7);var stats=M.Stats{.next_lineage=2};const before=M.carbon(d)+M.carbon(target);
 try std.testing.expect(M.reproduce(&d,0,&target,&stats,false));try std.testing.expectEqual(@as(f32,0.5),target.cohorts[0].structure);try std.testing.expectApproxEqAbs(before,M.carbon(d)+M.carbon(target),0.000001);
 var base=M.initialized(42);base.cohorts[0]=.{.biomass=0.1,.support_mass=0.025,.root_fraction=0.5,.organization=0.25,.lineage=1};var hardy=base;hardy.cohorts[0].structure=0.5;
 const warm=M.Environment{.temperature=303,.depth_km=0.001,.light=1,.carbon_available=1,.oxygen_carbon_capacity=1};const ordinary_flux=M.step(&base,warm,1440);const hardy_flux=M.step(&hardy,warm,1440);try std.testing.expect(hardy_flux.fixed<ordinary_flux.fixed);
 base=M.initialized(42);base.cohorts[0]=.{.biomass=0.1,.support_mass=0.025,.root_fraction=0.5,.organization=0.25,.lineage=1};hardy=base;hardy.cohorts[0].structure=0.5;
 const cold=M.Environment{.temperature=270,.depth_km=0.00001,.light=1,.carbon_available=1,.oxygen_carbon_capacity=1};const b=M.step(&base,cold,1440);const h=M.step(&hardy,cold,1440);try std.testing.expectEqual(@as(f32,0),b.fixed);try std.testing.expectEqual(@as(f32,0),h.fixed);try std.testing.expect(M.biomass(hardy)>M.biomass(base));try std.testing.expect(M.biomass(hardy)<0.1);
}
