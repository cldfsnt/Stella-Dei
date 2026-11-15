const std=@import("std");const A=@import("experimental/allocation_sampler.zig");
test "fixed proposal distribution and boundary expression"{
 var bins=[_]usize{0}**4;var accepted=[_]usize{0}**3;const pairs=[_]A.Pair{.{.root=0,.storage=0},.{.root=0.25,.storage=0.25},.{.root=0.5,.storage=0.5}};
 for(0..262144)|i|{const d=A.draw(2027,478,i+1000,7);try std.testing.expectEqualDeep(d,A.draw(2027,478,i+1000,7));if(d.event)bins[(if(d.root)@as(usize,0) else 2)+(if(d.positive)@as(usize,0) else 1)]+=1;
 for(pairs,0..)|p,j|{try std.testing.expectEqualDeep(p,A.apply(p,false,d).?);const next=A.apply(p,true,d).?;try std.testing.expect(A.valid(next));if(next.root!=p.root or next.storage!=p.storage)accepted[j]+=1;}}
 var count:usize=0;for(bins)|b|{count+=b;try std.testing.expect(b>=750 and b<=1300);}try std.testing.expect(count>=3500 and count<=4700);std.debug.print("SAMPLER events={} root+/- storage+/-={any} accepted origin/interior/saturated={any}\n",.{count,bins,accepted});
}
test "invalid input refuses and allocation sum never projected"{for([_]A.Pair{.{.root=std.math.nan(f32),.storage=0},.{.root=0,.storage=std.math.inf(f32)},.{.root=-0.1,.storage=0},.{.root=0.75,.storage=0.5}})|p|try std.testing.expect(A.apply(p,false,.{.event=false,.root=true,.positive=true})==null);const p=A.Pair{.root=0.5,.storage=0.5};try std.testing.expectEqualDeep(p,A.apply(p,true,.{.event=true,.root=true,.positive=true}).?);}
test "disabled new sampler preserves legacy retention law outputs"{const R=@import("experimental/retention_mutation.zig");for(0..4096)|i|{const legacy=A.Pair{.root=0,.storage=R.allocation(0.5,2027,478,i+1000,7)};try std.testing.expectEqualDeep(legacy,A.apply(legacy,false,A.draw(2027,478,i+1000,7)).?);}}
