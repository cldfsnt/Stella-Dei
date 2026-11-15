const std=@import("std");const H=@import("experimental/paid_hydration_fair.zig");
test "all24 permutations exact identity receipts for equal unequal and scarce demands"{
 for([_][4]f64{.{0.01,0.01,0.01,0.01},.{0,0.001,0.02,0.1}})|demand|{
 for([_]f32{0,1e-30,0.00001,0.01,1,1e9})|pool|{
 var reference:[4]f64=undefined;var count:usize=0;
 for(0..4)|a|{for(0..4)|b|{if(b==a)continue;for(0..4)|c|{if(c==a or c==b)continue;for(0..4)|d|{if(d==a or d==b or d==c)continue;
 const ids=[_]usize{a,b,c,d};var s:H.State=.{};s.liquid=pool;
 for(ids,0..)|id,i|{s.cell.cohorts[i]=.{.biomass=0.2,.support_mass=0.1,.qa_retention=0.25};s.retained[i]=H.capacity(s.cell.cohorts[i])-demand[id];}
 const before=s;const water=s.totalWater();s.simultaneousUptake();var received:[4]f64=undefined;
 for(ids,0..)|id,i|{received[id]=s.retained[i]-before.retained[i];try std.testing.expect(received[id]>=0 and received[id]<=demand[id]+1e-16);}
 if(count==0)reference=received else try std.testing.expectEqualDeep(reference,received);count+=1;
 try std.testing.expect(@abs(s.totalWater()-water)<=@max(1e-9,64*std.math.floatEps(f64)*water));try std.testing.expect(s.liquid<=before.liquid and s.liquid_escrow>=0);
 }}}}try std.testing.expectEqual(@as(usize,24),count);
 }}
}
test "unrepresentable debit gives no water and zero demands leave source untouched"{var s:H.State=.{};s.liquid=1e9;s.cell.cohorts[0]=.{.biomass=0.2,.support_mass=0.1,.qa_retention=0.25};const before=s;s.simultaneousUptake();try std.testing.expectEqualDeep(before,s);s.liquid=1;s.cell.cohorts[0].qa_retention=0;const zero=s;s.simultaneousUptake();try std.testing.expectEqualDeep(zero,s);}
