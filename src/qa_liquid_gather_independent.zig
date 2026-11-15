const std=@import("std");const G=@import("experimental/liquid_gather.zig");
test "independent reciprocal duplicate self tail and order"{
 const mass=[_]f32{0,0,0,0,100};const elevation=[_]f32{0}**5;
 const clean=[_][6]usize{.{1,0,0,0,0,0},.{0,2,1,1,1,1},.{1,3,2,2,2,2},.{2,4,3,3,3,3},.{3,4,4,4,4,4}};
 var duplicate=clean;duplicate[3]=.{2,4,4,3,3,3};duplicate[4]=.{3,3,4,4,4,4};
 var edges:[5][6]f64=undefined;var a:[5]f32=undefined;var b:[5]f32=undefined;var c:[5]f32=undefined;
 _=try G.step(&mass,&elevation,&clean,&edges,&a,1,1440,false);_=try G.step(&mass,&elevation,&clean,&edges,&b,1,1440,true);_=try G.step(&mass,&elevation,&duplicate,&edges,&c,1,1440,false);
 try std.testing.expectEqualSlices(f32,&a,&b);try std.testing.expectEqualSlices(f32,&a,&c);try std.testing.expect(a[4]<mass[4] and a[3]>0);for(edges,0..)|es,i|{var sum:f64=0;for(es)|e|sum+=e;try std.testing.expect(sum<=mass[i]);}
 _=try G.step(&mass,&elevation,&clean,&edges,&a,1,0,false);try std.testing.expectEqualSlices(f32,&mass,&a);
}
test "independent invalid reciprocal and finite inputs refuse before outputs"{
 var mass=[_]f32{1,0};const elevation=[_]f32{0,0};const good=[_][6]usize{.{1,0,0,0,0,0},.{0,1,1,1,1,1}};const bad=[_][6]usize{.{1,0,0,0,0,0},.{1,1,1,1,1,1}};var edges:[2][6]f64=undefined;var out=[_]f32{-9,-9};
 try std.testing.expectError(error.InvalidTopology,G.step(&mass,&elevation,&bad,&edges,&out,1,1440,false));try std.testing.expectEqualSlices(f32,&.{-9,-9},&out);
 try std.testing.expectError(error.InvalidValue,G.step(&mass,&elevation,&good,&edges,&out,0,1440,false));try std.testing.expectError(error.InvalidValue,G.step(&mass,&elevation,&good,&edges,&out,1,-1,false));mass[0]=std.math.inf(f32);try std.testing.expectError(error.InvalidValue,G.step(&mass,&elevation,&good,&edges,&out,1,1440,false));
}
test "independent offset overlap must not mutate authoritative input"{
 var backing=[_]f32{1,0,0};var elevation=[_]f32{0,0};const graph=[_][6]usize{.{1,0,0,0,0,0},.{0,1,1,1,1,1}};var edges:[2][6]f64=undefined;
 try std.testing.expectError(error.InvalidShape,G.step(backing[0..2],&elevation,&graph,&edges,backing[1..3],1,1440,false));try std.testing.expectEqualSlices(f32,&.{1,0,0},&backing);
 try std.testing.expectError(error.InvalidShape,G.step(backing[0..2],&elevation,&graph,&edges,&elevation,1,1440,false));try std.testing.expectEqualSlices(f32,&.{0,0},&elevation);
}

test "independent wide scales immutable budgets and reverse order"{
 const graph=[_][6]usize{.{1,2,0,0,0,0},.{0,2,1,1,1,1},.{0,1,2,2,2,2}};const e=[_]f32{0,0,0};
 for([_][3]f32{.{1e30,1e-20,0},.{1e-30,0,0},.{0,0,0},.{1,1,1}})|mass|{
 var edges:[3][6]f64=undefined;var out:[3]f32=undefined;var rev:[3]f32=undefined;
 _=try G.step(&mass,&e,&graph,&edges,&out,1e-20,1440,false);_=try G.step(&mass,&e,&graph,&edges,&rev,1e-20,1440,true);
 try std.testing.expectEqualSlices(f32,&out,&rev);for(edges,0..)|row,i|{var sum:f64=0;for(row)|x|{try std.testing.expect(std.math.isFinite(x) and x>=0);sum+=x;}try std.testing.expect(sum<=mass[i]);}for(out)|x|try std.testing.expect(std.math.isFinite(x) and x>=0);
 }
}
