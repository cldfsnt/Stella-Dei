//! Read-only discovery of living microbial cohorts with actual recorded intake.
const std=@import("std");
pub const Match=struct{lineage:u64,intake:f32};
pub fn recorded(cell:anytype)?Match{
 for(cell.cohorts)|co|if(co.lineage>0 and std.math.isFinite(co.biomass) and co.biomass>0 and std.math.isFinite(co.feeding) and co.feeding>0 and std.math.isFinite(co.lifetime_grazed) and co.lifetime_grazed>0)return .{.lineage=co.lineage,.intake=co.lifetime_grazed};
 return null;
}
test "only living capable finite recorded feeders match, never capability alone"{
 const C=struct{biomass:f32=0,feeding:f32=0,lifetime_grazed:f32=0,lineage:u64=7};var cell=struct{cohorts:[1]C=.{.{}}}{};
 try std.testing.expect(recorded(cell)==null);cell.cohorts[0]=.{.biomass=1,.feeding=0.1};try std.testing.expect(recorded(cell)==null);
 cell.cohorts[0].lifetime_grazed=0.02;try std.testing.expectEqual(@as(u64,7),recorded(cell).?.lineage);
 cell.cohorts[0].biomass=0;try std.testing.expect(recorded(cell)==null);cell.cohorts[0].biomass=1;
 cell.cohorts[0].feeding=0;try std.testing.expect(recorded(cell)==null);cell.cohorts[0].feeding=0.1;
 cell.cohorts[0].lifetime_grazed=std.math.inf(f32);try std.testing.expect(recorded(cell)==null);
 cell.cohorts[0].lifetime_grazed=std.math.nan(f32);try std.testing.expect(recorded(cell)==null);
 cell.cohorts[0].lifetime_grazed=0.02;cell.cohorts[0].lineage=0;try std.testing.expect(recorded(cell)==null);cell.cohorts[0].lineage=7;
 cell.cohorts[0].biomass=std.math.nan(f32);try std.testing.expect(recorded(cell)==null);cell.cohorts[0].biomass=1;
 cell.cohorts[0].feeding=std.math.nan(f32);try std.testing.expect(recorded(cell)==null);
}
