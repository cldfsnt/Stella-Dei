const std=@import("std");const Old=@import("experimental/hydration_continuous_core.zig");const New=@import("experimental/hydration_mutation_core.zig");const R=@import("experimental/retention_mutation.zig");
test "independent Python hashlib tuple vector"{try std.testing.expectEqualStrings("22de0612c574954403e2b358218acc48a6d4e34ee6d3c6831faac4b81c93456c",&std.fmt.bytesToHex(R.digest(42,17,123456,2),.lower));}
test "all old birth fields RNG and paid water preserved across actual mutated births"{
 var mutations:usize=0;var lower:usize=0;
 for(2..2050)|id|for([_]bool{false,true})|same|{for([_]bool{false,true})|propagule|{
  var o=[_]Old.Cell{Old.initialized(173),Old.initialized(29)};var n=[_]New.Cell{New.initialized(173),New.initialized(29)};
  o[0].cohorts[0]=.{.biomass=0.4,.support_mass=0.1,.organization=0.25,.efficiency=1.05,.structure=0.1,.feeding=0.2,.mobility=0.1,.retention_allocation=0.5,.stored_water=0.5,.reproduction_credit=0.3,.lineage=1};
  inline for(std.meta.fields(Old.Cohort))|f|@field(n[0].cohorts[0],f.name)=@field(o[0].cohorts[0],f.name);
  var os:Old.Stats=.{.next_lineage=id};var ns:New.Stats=.{.next_lineage=id};const to:usize=if(same)0 else 1;
  const a=if(propagule)Old.propagate(&o[0],0,&o[to],&os) else Old.reproduce(&o[0],0,&o[to],&os,true);
  const b=if(propagule)New.propagateWithRetention(&n[0],0,&n[to],&ns,42) else New.reproduceWithRetention(&n[0],0,&n[to],&ns,true,42);
  try std.testing.expect(a and b);
  for(0..2)|ci|{try std.testing.expectEqual(o[ci].rng,n[ci].rng);try std.testing.expectEqual(o[ci].nutrient,n[ci].nutrient);try std.testing.expectEqual(o[ci].detritus,n[ci].detritus);
   for(0..4)|slot|{inline for(std.meta.fields(Old.Cohort))|f|{if(comptime !std.mem.eql(u8,f.name,"retention_allocation") and !std.mem.eql(u8,f.name,"stored_water"))try std.testing.expectEqual(@field(o[ci].cohorts[slot],f.name),@field(n[ci].cohorts[slot],f.name));}}
  }
  inline for(std.meta.fields(Old.Stats))|f|try std.testing.expectEqual(@field(os,f.name),@field(ns,f.name));
  try std.testing.expectApproxEqAbs(Old.waterTotal(o[0])+Old.waterTotal(o[1]),New.waterTotal(n[0])+New.waterTotal(n[1]),1e-15);
  try std.testing.expectEqual(o[0].cohorts[0].stored_water,n[0].cohorts[0].stored_water);try std.testing.expectEqual(@as(f32,0.5),n[0].cohorts[0].retention_allocation);
  const slot:usize=if(same)1 else 0;const old=o[to].cohorts[slot];const child=n[to].cohorts[slot];
  if(child.retention_allocation!=old.retention_allocation)mutations+=1;
  try std.testing.expect(child.stored_water<=old.stored_water);try std.testing.expect(child.stored_water<=New.waterCapacity(child));
  if(child.retention_allocation<old.retention_allocation){lower+=1;try std.testing.expectApproxEqAbs(old.stored_water-child.stored_water,n[to].liquid_return-o[to].liquid_return,1e-15);}
 }};
 try std.testing.expect(mutations>0 and lower>0);std.debug.print("MUTATION_AUDIT funded_births=8192 changed={d} lower_capacity={d} exact_old_traits_rng=true\n",.{mutations,lower});
}
