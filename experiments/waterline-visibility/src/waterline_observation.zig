//! Read-only current-habitat evidence. Never advances RNG or infers adaptation.
const std=@import("std");const M=@import("simulation/microbes.zig");const F=@import("propagule_feedback.zig");
pub const Snapshot=struct{zone:[]const u8,growth_environment_ok:bool,living_descendants:usize,supported_descendants:usize,observed_paid_arrivals_still_present:usize};
pub fn inspect(cell:M.Cell,depth_km:f32,temp:f32,index:usize,events:[]const F.Event)Snapshot{
 var s:Snapshot=.{.zone=if(!std.math.isFinite(depth_km) or !std.math.isFinite(temp)) "unknown" else if(depth_km<=0) "dry" else if(depth_km<0.0002) "exposed_film" else if(depth_km<=0.001) "wet_edge" else if(depth_km>0.05) "deep" else "aquatic",.growth_environment_ok=M.habitable(depth_km,temp),.living_descendants=0,.supported_descendants=0,.observed_paid_arrivals_still_present=0};
 for(cell.cohorts)|co|{if(co.biomass<=0)continue;
  if(co.parent>0){s.living_descendants+=1;if(co.support_mass>0 and co.organization>0)s.supported_descendants+=1;}
  for(events)|e|if(e.serial>0 and e.kind==.arrival and e.cell==index and e.lineage==co.lineage){s.observed_paid_arrivals_still_present+=1;break;};
 }
 return s;
}
test "film residents and paid arrival are not labeled successful shore adaptation"{
 var c=M.initialized(9);c.cohorts[0]=.{.biomass=0.02,.parent=1,.lineage=2,.structure=0.8,.organization=0.2,.support_mass=0.004};
 var f:F.Tracker=.{};f.arrived(4,7,2,10);const before=c;const rng=c.rng;
 const s=inspect(c,0.0001,300,7,&f.events);try std.testing.expectEqualStrings("exposed_film",s.zone);try std.testing.expect(!s.growth_environment_ok);try std.testing.expectEqual(@as(usize,1),s.observed_paid_arrivals_still_present);try std.testing.expectEqual(@as(usize,1),s.supported_descendants);try std.testing.expectEqualDeep(before,c);try std.testing.expectEqual(rng,c.rng);
 const fresh=inspect(c,0.0001,300,7,&.{});try std.testing.expectEqual(@as(usize,0),fresh.observed_paid_arrivals_still_present);
}
test "actual water and temperature remain authoritative at wet edge"{
 const c=M.initialized(1);try std.testing.expect(inspect(c,0.0002,300,0,&.{}).growth_environment_ok);try std.testing.expect(!inspect(c,0.0002,250,0,&.{}).growth_environment_ok);try std.testing.expectEqualStrings("dry",inspect(c,0,300,0,&.{}).zone);
}
