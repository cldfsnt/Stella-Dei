//! Read-only hypothetical paid-founder local water reference, NOT a forecast.
const std=@import("std");const M=@import("simulation/microbes.zig");const Column=@import("simulation/capillary_bucket.zig");
pub const Estimate=struct{reference_seconds:u32=1440,status:enum{inactive_temperature,no_exposed_demand,no_root_water,available},soil_kg_m2:f64,current_immersion:f64,root_tissue_kg_c_m2:f64,exposed_demand_kg_m2:f64,modeled_credit_kg_m2:f64,modeled_funded_fraction:f32,reference_end_depth_m:f64};
pub fn evaluate(cell:M.Cell,slot:usize,initial:Column.State,area:f64,conversion:f32,saturation:f64,environment:M.Environment)?Estimate{
 if(slot>=4 or !M.validCell(cell,std.math.maxInt(u64)) or !std.math.isFinite(conversion) or conversion<=0)return null;
 const c=cell.cohorts[slot];if(c.biomass<=0 or c.lineage==0)return null;
 var env=environment;env.immersion_physiology=true;env.final_demand_physiology=true;
 const physical=@import("simulation/basal_geometry.zig").immersion(c.biomass,M.producerHeightMeters(c),@as(f64,env.depth_km)*1000,100) orelse return null;
 const col=Column.stepBorrowed(initial,.{.dt=1440,.area=area,.temperature=env.temperature,.saturation=saturation,.environment=env,.conductance=10},&cell) orelse return null;
 env.depth_km=col.state.liquid*conversion;env.root_credit=col.root_credits;for(cell.cohorts,0..)|co,i|env.root_owner[i]=co.lineage;
 const demand=M.rootDemand(c,env,1440);const h=M.effectiveHydration(M.fundedHydration(c,env,1440,slot,demand),env.depth_km,env.temperature);
 return .{.status=if(env.temperature<=273.15 or env.temperature>=355).inactive_temperature else if(demand<=0).no_exposed_demand else if(h<=0).no_root_water else .available,.soil_kg_m2=initial.soil,.current_immersion=physical,.root_tissue_kg_c_m2=@as(f64,c.support_mass)*c.root_fraction,.exposed_demand_kg_m2=demand,.modeled_credit_kg_m2=col.root_credits[slot],.modeled_funded_fraction=h,.reference_end_depth_m=@as(f64,env.depth_km)*1000};
}
test "actual water reference is pure and distinguishes tiny dry soil from usable supply"{
 var cell=M.initialized(77);cell.cohorts[0]=.{.biomass=0.02,.support_mass=0.005,.root_fraction=0.5,.organization=0.25,.lineage=1};const original=cell;const env=M.Environment{.temperature=303,.depth_km=0,.light=1,.carbon_available=1,.oxygen_carbon_capacity=1};const conversion:f32=1e-7;
 const tiny=evaluate(cell,0,.{.liquid=0,.vapor=1,.soil=5.7856749216317645e-40},1e10,conversion,1,env).?;std.debug.print("TINY {any}\n",.{tiny});try std.testing.expect(tiny.modeled_funded_fraction>=0 and tiny.modeled_funded_fraction<1e-30);
 const good=evaluate(cell,0,.{.liquid=0,.vapor=1,.soil=0.5},1e10,conversion,1,env).?;std.debug.print("GOOD {any}\n",.{good});try std.testing.expect(good.status==.available);try std.testing.expect(good.modeled_credit_kg_m2>0 and good.modeled_funded_fraction>0);try std.testing.expectEqualDeep(original,cell);
 const scarce=evaluate(original,0,.{.liquid=0,.vapor=1,.soil=1e-6},1e10,conversion,1,env).?;
 cell.cohorts[1]=.{.biomass=0.1,.support_mass=0.05,.root_fraction=0.5,.lineage=2};const competed=evaluate(cell,0,.{.liquid=0,.vapor=1,.soil=1e-6},1e10,conversion,1,env).?;std.debug.print("COMPETE {any}\n",.{competed});try std.testing.expect(competed.modeled_credit_kg_m2<=scarce.modeled_credit_kg_m2+1e-18);
 var cold=env;cold.temperature=270;const frozen=evaluate(original,0,.{.liquid=0,.vapor=1,.soil=0.5},1e10,conversion,1,cold).?;std.debug.print("COLD {any}\n",.{frozen});try std.testing.expect(frozen.status==.inactive_temperature);
 var submerged=env;submerged.depth_km=0.0001;const wet=evaluate(original,0,.{.liquid=1000,.vapor=1,.soil=0.5},1e10,conversion,1,submerged).?;std.debug.print("WET {any}\n",.{wet});try std.testing.expectEqual(@as(f64,1),wet.current_immersion);try std.testing.expect(wet.status==.no_exposed_demand);
 try std.testing.expect(evaluate(original,0,.{.liquid=0,.vapor=std.math.nan(f64),.soil=0.5},1e10,conversion,1,env)==null);
 var partial=original;partial.cohorts[0].biomass=0.004;partial.cohorts[0].support_mass=0.001;const small=evaluate(partial,0,.{.liquid=0,.vapor=1,.soil=0.5},1e10,conversion,1,env).?;std.debug.print("SMALL {any}\n",.{small});try std.testing.expect(small.root_tissue_kg_c_m2<good.root_tissue_kg_c_m2 and small.exposed_demand_kg_m2<good.exposed_demand_kg_m2);
}
