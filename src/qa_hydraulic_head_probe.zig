const std=@import("std");const S=@import("simulation/surface_physics.zig");
const Case=struct{label:[]const u8,terrain:f32,mass:f32};
test "frozen radius scale heads erase or exaggerate represented centimeter water changes"{
 const parsed=try std.json.parseFromSlice([]Case,std.testing.allocator,@embedFile("experimental/head_probe_fixture.json"),.{});defer parsed.deinit();
 const conversion:f32=@floatCast(1.0/1000.0/7669529600.0/1000.0*1e9);const fraction:f32=0.0048;
 for(parsed.value)|c|for([_]f64{0.01,0.02,0.05})|delta|{
  const updated:f32=@floatCast(@as(f64,c.mass)+delta/1000/conversion);const old_depth=c.mass*conversion;const new_depth=updated*conversion;
  const old_head=c.terrain+old_depth;const new_head=c.terrain+new_depth;const current=new_head-old_head;const relative=@as(f64,new_depth)-old_depth;
  const a=@min(updated*fraction,@max(0,S.heightLimitedMass(f32,current,conversion,fraction)));
  const b=@min(@as(f64,updated*fraction),@max(0,S.heightLimitedMass(f64,relative,conversion,fraction)));
  try std.testing.expect(new_depth>old_depth);try std.testing.expectApproxEqAbs(delta,relative*1000,0.000001);
  try std.testing.expect(current==0 or current==0.00048828125);try std.testing.expect(a!=b);
  std.debug.print("HEAD_NATIVE label={s} requested_m={d} represented_m={d} current_head_m={d} old_proposal={d} relative_proposal={d}\n",.{c.label,delta,relative*1000,current*1000,a,b});
 };
}
