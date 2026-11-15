const std=@import("std");const H=@import("experimental/paid_hydration_fair.zig");
test "independent randomized nonzero stores: exact permutation receipts and wide-precision debit bound"{
 var rng=std.Random.DefaultPrng.init(0x7bde9c52);const random=rng.random();
 for(0..1000)|trial|{
  var base:H.State=.{};base.liquid=std.math.pow(f32,10,@as(f32,@floatFromInt(@as(i32,@intCast(trial%40))-30)));
  for(0..4)|i|{const support=random.float(f32)*0.1;base.cell.cohorts[i]=.{.lineage=i+1,.biomass=0.2,.support_mass=support,.qa_retention=random.float(f32)};base.retained[i]=H.capacity(base.cell.cohorts[i])*random.float(f64);}
  var reference:[4]f64=undefined;var count:usize=0;
  for(0..4)|a|for(0..4)|b|{if(b==a)continue;for(0..4)|c|{if(c==a or c==b)continue;for(0..4)|d|{if(d==a or d==b or d==c)continue;
   const ids=[_]usize{a,b,c,d};var s=base;for(ids,0..)|id,i|{s.cell.cohorts[i]=base.cell.cohorts[id];s.retained[i]=base.retained[id];}
   const before=s;s.simultaneousUptake();var increments:[4]f64=undefined;var credited:f128=0;
   for(ids,0..)|id,i|{const got=s.retained[i]-before.retained[i];increments[id]=got;credited+=@as(f128,got);try std.testing.expect(got>=0 and s.retained[i]<=H.capacity(s.cell.cohorts[i]));}
   // Test the allocator's realized source receipt, not nominal request.
   const debit=(@as(f64,before.liquid)-s.liquid)*(1e9/H.area);
   try std.testing.expect(credited<=@as(f128,debit));try std.testing.expect(s.liquid>=0 and s.liquid<=before.liquid);
   if(count==0)reference=increments else try std.testing.expectEqualDeep(reference,increments);count+=1;
  }}};try std.testing.expectEqual(@as(usize,24),count);
 }
 std.debug.print("FAIR_AUDIT randomized_cases=1000 permutations=24000 f128_receiver_sum_bound=true\n",.{});
}
