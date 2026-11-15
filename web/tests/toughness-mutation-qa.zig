const std=@import("std");const E=@import("simulation/ecology.zig");const F=@import("simulation/foraging.zig");const M=@import("toughness_mutation.zig");
test "law2 fixed keys preserve thermal outcomes and bounded inherited costs"{
 for([_]u64{0,1,42})|stream|{
  var plus:usize=0;var minus:usize=0;var zero:usize=0;
  for(0..65536)|event|{
   const proposal=M.proposal(stream,event,7);if(proposal>0)plus+=1 else if(proposal<0)minus+=1 else zero+=1;
   for([_]f32{0,0.5,1})|d|{
    const parent=E.Plant{.optimum=297.125,.generation=7,.toughness=d};const old=E.offspring(parent,event);
    const off=E.offspringWithMutation(parent,event,.{.enabled=false,.stream_seed=stream});try std.testing.expectEqualDeep(old,off);
    const child=E.offspringWithMutation(parent,event,.{.enabled=true,.stream_seed=stream});
    try std.testing.expectEqual(@as(u32,@bitCast(old.optimum)),@as(u32,@bitCast(child.optimum)));try std.testing.expectEqual(old.generation,child.generation);
    try std.testing.expectEqual(std.math.clamp(d+proposal,0,1),child.toughness);try std.testing.expect(child.toughness>=0 and child.toughness<=1);
    try std.testing.expectEqualDeep(child,E.offspringWithMutation(parent,event,.{.enabled=true,.stream_seed=stream}));
    if(d==0 and proposal<0)try std.testing.expectEqual(@as(f32,0),child.toughness);
    if(d==1 and proposal>0)try std.testing.expectEqual(@as(f32,1),child.toughness);
   }
  }
  const rate=@as(f64,@floatFromInt(plus+minus))/65536;const imbalance=@abs(@as(i64,@intCast(plus))-@as(i64,@intCast(minus)));
  try std.testing.expect(rate>=0.012 and rate<=0.020);try std.testing.expect(@as(f64,@floatFromInt(imbalance))<=0.2*@as(f64,@floatFromInt(plus+minus)));
  std.debug.print("TOUGH_MUTATION stream={} events=65536 plus={} minus={} unchanged={} zero_parent_positive={} zero_parent_clipped={}\n",.{stream,plus,minus,zero,plus,minus});
 }
 for(0..33)|i|{const d=@as(f32,@floatFromInt(i))/32;try std.testing.expect(E.growTough(0.2,295.15,295.15,0,1,true,1440,d)<=E.grow(0.2,295.15,295.15,0,1,true,1440));const bite=F.takeTough(0.5,50,1440,d);try std.testing.expect(bite.eaten<=F.take(0.5,50,1440).eaten);try std.testing.expect(bite.eaten<=0.5);}
 const v=M.digest(42,123456,7);std.debug.print("TOUGH_VECTOR {s}\n",.{std.fmt.fmtSliceHexLower(&v)});
}
