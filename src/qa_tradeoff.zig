//! Controlled mechanism probe, not a natural-world evolution acceptance.
const std=@import("std");const M=@import("simulation/microbes.zig");
pub fn main() !void {
 for(0..2)|habitat|for(0..2)|swap|{
  var cell=M.initialized(1337);cell.nutrient=0.2;
  const weak=swap;const strong=1-swap;
  cell.cohorts[weak]=.{.biomass=0.1,.support_mass=0.004,.organization=0.04,.structure=0,.lineage=1};
  cell.cohorts[strong]=.{.biomass=0.1,.support_mass=0.004,.organization=0.04,.structure=0.6,.lineage=2};
  var carbon:f32=2;const initial:f32=2.2;var fixed:f64=0;var failed:u64=0;var max_error:f32=0;
  for(0..600)|tick|{
   const depth:f32=if(habitat==0)0.001 else if(tick%60<30)0.001 else 0.00005;
   const flux=M.step(&cell,.{.temperature=303,.depth_km=depth,.light=1,.carbon_available=carbon,.oxygen_carbon_capacity=10},1440);
   carbon+=flux.recycled-flux.fixed;fixed+=flux.fixed;failed+=flux.failed_patches;
   var mass:f32=0;for(cell.cohorts)|c|mass+=c.biomass;
   max_error=@max(max_error,@abs(carbon+mass+cell.detritus-initial));
   if(!M.validCell(cell,3))return error.InvalidCell;
  }
  std.debug.print("TRADEOFF habitat={s} swapped={d} weak={d:.6} strong={d:.6} fixed={d:.6} failed_cohorts={d} carbon_error_max={d:.8} no_dispersal=true\n",.{if(habitat==0)"stable_1m" else "12h_1m_12h_5cm",swap,cell.cohorts[weak].biomass,cell.cohorts[strong].biomass,fixed,failed,max_error});
  if(max_error>0.0001)return error.CarbonDrift;
 };
}
