//! Isolated candidate inheritance versus exact production reproduction, no scheduler claim.
const std=@import("std");const M=@import("simulation/microbes.zig");const B=@import("production_microbes.zig");
fn equalOld(a:M.Cell,b:B.Cell)!void{
 try std.testing.expectEqual(b.rng,a.rng);try std.testing.expectEqual(b.nutrient,a.nutrient);try std.testing.expectEqual(b.detritus,a.detritus);
 for(a.cohorts,b.cohorts)|x,y|inline for(std.meta.fields(B.Cohort))|field|try std.testing.expectEqual(@field(y,field.name),@field(x,field.name));
}
test "root inheritance preserves actual funded legacy births and RNG"{
 var max_support_residual:f64=0;
 for(0..512)|seed|for([_]f32{0,0.25,1})|allocation|for(0..3)|kind|{
  var d=M.initialized(seed+1);d.cohorts[0]=.{.biomass=0.125,.support_mass=0.03125,.organization=0.25,.root_fraction=allocation,.lineage=1,.reproduction_credit=0.125};
  var b=B.initialized(seed+1);inline for(std.meta.fields(B.Cohort))|field|@field(b.cohorts[0],field.name)=@field(d.cohorts[0],field.name);
  var t=M.initialized(55);var bt=B.initialized(55);var stats=M.Stats{.next_lineage=2};var bs=B.Stats{.next_lineage=2};
  const ok=if(kind==0)M.reproduce(&d,0,&d,&stats,true)else if(kind==1)M.reproduce(&d,0,&t,&stats,true)else M.propagate(&d,0,&t,&stats);
  const bok=if(kind==0)B.reproduce(&b,0,&b,&bs,true)else if(kind==1)B.reproduce(&b,0,&bt,&bs,true)else B.propagate(&b,0,&bt,&bs);
  try std.testing.expect(ok and bok);try equalOld(d,b);try equalOld(t,bt);inline for(std.meta.fields(B.Stats))|field|try std.testing.expectEqual(@field(bs,field.name),@field(stats,field.name));
  const child=if(kind==0)d.cohorts[1]else t.cohorts[0];try std.testing.expectEqual(allocation,child.root_fraction);try std.testing.expectEqual(@as(u64,1),child.parent);
  const support_sum=@as(f64,d.cohorts[0].support_mass)+child.support_mass;
  const baseline_child=if(kind==0)b.cohorts[1]else bt.cohorts[0];
  const baseline_sum=@as(f64,b.cohorts[0].support_mass)+baseline_child.support_mass;
  try std.testing.expectEqual(baseline_sum,support_sum);
  max_support_residual=@max(max_support_residual,@abs(support_sum-0.03125));
 };
 std.debug.print("ROOT_INHERITANCE max_existing_support_roundoff={e}  4608 funded births oldfields/RNG exact; allocation inherited no new mutation draws\n",.{max_support_residual});
}
