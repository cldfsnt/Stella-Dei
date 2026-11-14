//! Controlled grazing contrast; funded real production-size daughter, no engine edits.
const std=@import("std");const M=@import("simulation/microbes.zig");
test "paid propagule faces scarce-prey resident grazing contrast"{
 var donor=M.initialized(42);donor.cohorts[0]=.{.biomass=0.1,.reproduction_credit=0.02,.lineage=1};donor.nutrient=0.11;
 var target=M.initialized(43);target.cohorts[0]=.{.biomass=0.8,.feeding=0.14,.lineage=2};target.nutrient=0.04;
 var stats:M.Stats=.{.next_lineage=3};const before=M.carbon(donor)+M.carbon(target);try std.testing.expect(M.propagate(&donor,0,&target,&stats));
 try std.testing.expectApproxEqAbs(before,M.carbon(donor)+M.carbon(target),0.000001);
 const initial=target;
 for(0..2)|variant|{var cell=initial;if(variant==1)cell.cohorts[0].feeding=0;const n=M.nutrientTotal(cell);const c=M.carbon(cell);var recycle:f64=0;var fixed:f64=0;var grazed:f64=0;
  for(0..60)|i|{const flux=M.step(&cell,.{.temperature=303,.depth_km=0.001,.light=0,.carbon_available=1,.oxygen_carbon_capacity=1},1440);recycle+=flux.recycled;fixed+=flux.fixed;grazed+=flux.grazed;
   try std.testing.expectApproxEqAbs(@as(f64,c)+fixed-recycle,@as(f64,M.carbon(cell)),0.00001);try std.testing.expectApproxEqAbs(n,M.nutrientTotal(cell),0.00001);
   if(i==0 or i==1 or i==59)std.debug.print("GRAZING_CONTRAST variant={d} tick={d} resident={d:.8} child={d:.8} child_credit={d:.8} grazed={d:.8} child_traits_structure={d:.6} feeding={d:.6}\n",.{variant,i+1,cell.cohorts[0].biomass,cell.cohorts[1].biomass,cell.cohorts[1].reproduction_credit,grazed,initial.cohorts[1].structure,initial.cohorts[1].feeding});
   if(i==0){if(variant==0)try std.testing.expectEqual(@as(f32,0),cell.cohorts[1].biomass) else try std.testing.expect(cell.cohorts[1].biomass>0.0025);}
  }
 }
}
