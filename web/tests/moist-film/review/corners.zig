const std=@import("std");const M=@import("microbes.zig");
pub fn main() void {
 for([_]f32{0,1e-15,1e-12,1e-9,0.004})|support|for([_]f32{0,1e-12,0.000001,0.00005,0.00019})|depth|{
  var c=M.initialized(1);c.nutrient=1;c.cohorts[0]=.{.biomass=0.1,.support_mass=support,.structure=0.9,.lineage=1};
  const f=M.step(&c,.{.depth_km=depth,.temperature=303,.light=0,.carbon_available=1,.oxygen_carbon_capacity=1},1440);
  std.debug.print("support={d} depth_m={d} biomass={d} fixed={d}\n",.{support,depth*1000,M.biomass(c),f.fixed});
 };
 var cell=M.initialized(1);cell.nutrient=1;cell.cohorts[0]=.{.biomass=0.1,.support_mass=0.004,.structure=0.1,.lineage=1};
 const before=@as(f64,M.carbon(cell));const nutrients=M.nutrientTotal(cell);var atmosphere:f64=0;
 for(0..240)|i|{const f=M.step(&cell,.{.depth_km=if(i%2==0)0 else 1e-12,.temperature=303,.light=1,.carbon_available=1,.oxygen_carbon_capacity=1},1440);atmosphere+=@as(f64,f.recycled)-f.fixed;}
 std.debug.print("ALTERNATING carbon_residual={d} nutrient_residual={d} biomass={d}\n",.{@as(f64,M.carbon(cell))+atmosphere-before,M.nutrientTotal(cell)-nutrients,M.biomass(cell)});
}
