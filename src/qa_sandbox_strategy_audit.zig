//! Read-only current-model contrast. No new trait, rate or production hook.
const std=@import("std");const E=@import("simulation/ecology.zig");const F=@import("simulation/foraging.zig");
test "Sandbox inherited phenotype is thermal optimum and generation, not defense or form"{
 try std.testing.expectEqual(@as(usize,2),std.meta.fields(E.Plant).len);
 const temperatures=[_]f32{289.37143,295.15,301.70587};
 const bite=F.take(0.1,50,1440);
 for(temperatures)|optimum|{
  const growth=E.grow(0.1,303.15,optimum,0,1,true,86400);
  std.debug.print("SANDBOX_STRATEGY optimum={d} growth1d={d} same_cover_bite={d}\n",.{optimum,growth,bite.eaten});
  try std.testing.expectEqualDeep(bite,F.take(0.1,50,1440));
 }
 try std.testing.expect(E.grow(0.1,303.15,301.70587,0,1,true,86400)>E.grow(0.1,303.15,289.37143,0,1,true,86400));
}
test "current finite grazing has no protected perpatch floor"{
 const b=F.take(0.00005,50,1440);try std.testing.expectEqual(@as(f32,0),b.after);try std.testing.expect(b.eaten>0);
 try std.testing.expectEqual(@as(f32,0),E.grow(0,303.15,301.7,0,1,true,86400));
 // Recovery from exactly zero therefore requires the real neighbor-colonization path.
}
