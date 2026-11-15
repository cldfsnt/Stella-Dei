//! Copy beside the generated root-only microbes/root_throughflow modules to test.
const std=@import("std");const M=@import("microbes.zig");const R=@import("root_throughflow.zig");
fn cell()M.Cell{var c=M.initialized(123);c.cohorts[0]=.{.biomass=0.125,.support_mass=0.03125,.root_fraction=0.25,.lineage=1};return c;}
fn env()M.Environment{return .{.temperature=300,.depth_km=0,.light=1,.carbon_available=1,.oxygen_carbon_capacity=1};}
test "independent per day low soil conductance regression"{
 for([_]f32{360,720,1440})|dt|for([_]u8{1,10})|k|{
  const c=cell();const s:f64=0.00001;const r=R.step(c,s,1000,7669529600,env(),dt,k).?;
  const ideal=@as(f64,c.cohorts[0].support_mass)*c.cohorts[0].root_fraction*@as(f64,@floatFromInt(k))/86400*s*dt;
  try std.testing.expect(r.paid>0 and r.paid<=ideal);try std.testing.expectApproxEqRel(ideal,r.paid,1e-8);
  try std.testing.expect(r.credits[0]<=s-r.soil and r.credits[0]<=r.demand[0]);
  try std.testing.expect(@as(f64,r.h[0])*r.demand[0]<=r.credits[0]);
  try std.testing.expectEqual(@as(f32,1000),r.vapor);try std.testing.expect(r.vapor_rounding_density<0);
  std.debug.print("ROOT_AUDIT dt={d} k={} ideal={e} paid={e} credit={e} h={e} receiver_error={e}\n",.{dt,k,ideal,r.paid,r.credits[0],r.h[0],r.vapor_rounding_density});
 };
}
test "independent invalid environment refuses without input mutation"{
 for(0..7)|i|{const c=cell();var e=env();switch(i){0=>e.temperature=std.math.nan(f32),1=>e.depth_km=std.math.nan(f32),2=>e.depth_km=-1,3=>e.light=std.math.inf(f32),4=>e.light=-1,5=>e.light=3,6=>e.temperature=std.math.inf(f32),else=>unreachable}const before=c;try std.testing.expect(R.step(c,0.25,1,7669529600,e,1440,1)==null);try std.testing.expectEqualDeep(before,c);}
}
test "independent cold deep absent root and absent soil give no water or signal"{
 for(0..6)|i|{var c=cell();var e=env();var soil:f64=0.25;switch(i){0=>e.temperature=270,1=>e.temperature=355,2=>e.depth_km=0.001,3=>c.cohorts[0].root_fraction=0,4=>soil=0,5=>c.cohorts[0].support_mass=0,else=>unreachable}const r=R.step(c,soil,1,7669529600,e,1440,1).?;try std.testing.expectEqual(soil,r.soil);try std.testing.expectEqual(@as(f32,1),r.vapor);try std.testing.expectEqual(@as(f64,0),r.paid);for(r.h)|h|try std.testing.expect(h==0);}
}
