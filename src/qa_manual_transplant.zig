//! Controlled refusal fixtures only; native natural-world proof is separate.
const std=@import("std");const M=@import("simulation/microbes.zig");const D=@import("experimental/manual_transplant.zig");
const Planet=struct{worldMode:M.Mode=.origin,microbeCells:[2]M.Cell=.{.{},.{}},microbeStats:M.Stats=.{.next_lineage=10},pub fn getNeighbours(_: *@This(),from:usize)[]const usize{return if(from==0)&.{1} else &.{0};}};
const State=struct{paused:bool=true,gameTime:f64=123,planet:Planet=.{}};
test "manual transplant refusal cases are exact atomic and history not rewritten"{
 var s=State{};s.planet.microbeCells[0].cohorts[0]=.{.lineage=1,.biomass=0.2,.support_mass=0.03,.reproduction_credit=0.003};
 for(0..7)|case|{
  var t=s;
  switch(case){0=>{t.planet.microbeCells[0].cohorts[0].relocations=1;t.planet.microbeCells[0].cohorts[0].last_to=0;t.planet.microbeCells[0].cohorts[0].last_from=1;},1=>{for(&t.planet.microbeCells[1].cohorts,0..)|*c,i|c.*=.{.biomass=0.01,.lineage=2+i};},2=>t.planet.microbeCells[1].cohorts[0]=.{.biomass=0.9,.lineage=2},3=>t.paused=false,4=>t.gameTime=std.math.nan(f64),5=>t.planet.microbeCells[0].cohorts[0].last_move_time=10,else=>t.planet.worldMode=.sandbox}
  const before=t;
  if(D.prepare(&t,1,0,0,1))|ticket|try std.testing.expect(!D.execute(&t,1,ticket).ok);
  // NaN case compare float bit patterns through serialization instead of eql NaN.
  const a=try std.json.stringifyAlloc(std.testing.allocator,before,.{.emit_nonportable_numbers_as_strings=true});defer std.testing.allocator.free(a);const b=try std.json.stringifyAlloc(std.testing.allocator,t,.{.emit_nonportable_numbers_as_strings=true});defer std.testing.allocator.free(b);try std.testing.expectEqualStrings(a,b);
 }
 const ticket=D.prepare(&s,1,0,0,1).?;const donor=s.planet.microbeCells[0].cohorts[0];const stats=s.planet.microbeStats;try std.testing.expect(D.execute(&s,1,ticket).ok);try std.testing.expectEqualDeep(donor,s.planet.microbeCells[1].cohorts[0]);try std.testing.expectEqualDeep(stats,s.planet.microbeStats);try std.testing.expect(s.planet.microbeCells[0].cohorts[0].biomass==0);
}
test "stale source, source ID and stats tickets refuse atomically"{
 var s=State{};s.planet.microbeCells[0].cohorts[0]=.{.lineage=1,.biomass=0.2};
 const ticket=D.prepare(&s,1,0,0,1).?;
 for(0..3)|case|{var wrong=ticket;switch(case){0=>wrong.source.nutrient+=0.01,1=>wrong.id=2,else=>wrong.stats.births+=1}const before=s;try std.testing.expect(!D.execute(&s,1,wrong).ok);try std.testing.expectEqualDeep(before,s);}
}
