const std=@import("std");const M=@import("experimental/hydration_lifecycle_core.zig");
test "net biomass gainer still releases water for gross predation before assimilation"{
 var c=M.initialized(17);
 c.cohorts[0]=.{.biomass=0.4,.support_mass=0.1,.organization=0.25,.retention_allocation=0.25,.stored_water=0.2,.feeding=1,.lineage=1};
 c.cohorts[1]=.{.biomass=0.2,.feeding=0.1,.lineage=2};
 const before=c;const water=M.waterTotal(c);_=M.graze(&c,0.2,10);
 try std.testing.expect(c.cohorts[0].biomass>before.cohorts[0].biomass);
 try std.testing.expect(c.cohorts[0].stored_water<before.cohorts[0].stored_water);
 try std.testing.expect(c.liquid_return>0);try std.testing.expectEqual(@as(f64,0),c.cohorts[1].stored_water);
 try std.testing.expectApproxEqAbs(water,M.waterTotal(c),1e-15);
 std.debug.print("LIFECYCLE_GROSS before_mass={d} after_mass={d} before_water={d} after_water={d} liquid_return={d}\n",.{before.cohorts[0].biomass,c.cohorts[0].biomass,before.cohorts[0].stored_water,c.cohorts[0].stored_water,c.liquid_return});
}
test "same-cell funded birth splits water once while retaining both existing phase escrows"{
 var c=M.initialized(17);c.liquid_return=0.03;c.vapor_return=0.07;
 c.cohorts[0]=.{.biomass=0.4,.support_mass=0.1,.organization=0.25,.retention_allocation=0.25,.stored_water=0.2,.reproduction_credit=0.3,.lineage=1};
 var stats:M.Stats=.{.next_lineage=2};const before=M.waterTotal(c);
 try std.testing.expect(M.reproduce(&c,0,&c,&stats,true));
 try std.testing.expectApproxEqAbs(before,M.waterTotal(c),1e-15);
 try std.testing.expectEqual(@as(f64,0.07),c.vapor_return);
 try std.testing.expect(c.cohorts[1].stored_water>0 and c.cohorts[0].stored_water<0.2);
 try std.testing.expectEqual(c.cohorts[0].retention_allocation,c.cohorts[1].retention_allocation);
 try std.testing.expect(M.validCell(c,stats.next_lineage));
}
